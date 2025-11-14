
import os
import json
from pathlib import Path
from llama_index.core import StorageContext, load_index_from_storage

INDEX_DIR = Path(__file__).parent.resolve() / "codequery" / "my_index"
CODE_ROOT = Path(__file__).parent.resolve() / "codequery" / "code"

MERMAID_FILE = Path("topology.html")
DOT_FILE = Path("topology.dot")

def list_modules():
    modules = []
    for tech_dir in CODE_ROOT.iterdir():
        if not tech_dir.is_dir():
            continue
        for module in tech_dir.iterdir():
            if module.is_dir():
                modules.append(module)
    return modules

def ask_about_module(query_engine, module_path):
    module_name = module_path.name
    print(f"🔍 Analyzing: {module_name}")
    prompt = f"""
You are analyzing the source code located in: {module_path}.
What other services, modules, HTTP endpoints, or Kafka topics does this module talk to?
Please answer with a plain list of external connections (one per line)."""
    try:
        result = query_engine.query(prompt)
        return module_name, str(result)
    except Exception as e:
        return module_name, f"ERROR: {e}"

def parse_connections(output):
    links = []
    for line in output.splitlines():
        line = line.strip("-•>* ").strip()
        if not line or line.startswith("ERROR"):
            continue
        if "->" in line:
            source, target = map(str.strip, line.split("->"))
            links.append((source, target))
        elif ":" in line:
            source, target = line.split(":", 1)
            links.append((source.strip(), target.strip()))
        elif " " in line:
            parts = line.split(" ")
            links.append((parts[0], parts[-1]))
        else:
            links.append(("?", line))
    return links

def write_dot(connections):
    with open(DOT_FILE, "w") as f:
        f.write("digraph G {\n")
        for src, tgt in connections:
            f.write(f"  \"{src}\" -> \"{tgt}\";\n")
        f.write("}\n")

def write_mermaid(connections):
    with open(MERMAID_FILE, "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true });
  </script>
</head>
<body>
  <pre class="mermaid">
graph TD
""")
        for src, tgt in connections:
            f.write(f"    {src} --> {tgt}\n")
        f.write("""  </pre>
</body>
</html>
""")

def main():
    print("📦 Loading index...")
    storage_context = StorageContext.from_defaults(persist_dir=str(INDEX_DIR))
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine(similarity_top_k=5)

    all_connections = []
    modules = list_modules()
    for mod in modules:
        name, result = ask_about_module(query_engine, mod)
        links = parse_connections(result)
        all_connections.extend((name, tgt) for _, tgt in links if tgt != name)

    print("\n🧠 Inferred Connections:")
    for src, tgt in all_connections:
        print(f"  {src} --> {tgt}")

    write_dot(all_connections)
    write_mermaid(all_connections)
    print("\n✅ Output written to:")
    print(f"  - {DOT_FILE}")
    print(f"  - {MERMAID_FILE}")

if __name__ == "__main__":
    main()
