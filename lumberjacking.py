# Author: credzba
from AutoComplete import *
import time
import sys
from Scripts.glossary.colors import colors

#
# If you use storage keys, remember to [keyguard your shovels
##
# Things to change:
#   Verify that these variables match your server
#   WoodID and LogID are usually the same, but many of the other items may be different
#   MoveIDs is a list of items that you want to move to the Bag of Holding and currently
#      includes boards, luminescent fungi, switch, parasiteic plant, and bark fragment
#
OldServer = True
# HatchetID = 0x0F43
HatchetID = 0x48B2 # Gargish Axe
LogID = 0x1BDD
WoodID = 0x1BD7
#
# Used only if your storing in a llama or mule
# MuleID = 0x0317 
MuleID = 0x0123
MuleColor = 0
LlamaID = 0x0124
LlamaColor = 0
#
## Used only on servers that have key storage systems
KeyGumpID =  0xe13358f7
WoodKeyID = 0x1BD9 
WoodKeyColor = 0 
MasterKeyID = 0x176B  
MasterKeyColor = 0x0481
#
# Internal variables shouldnt normally need changes
#
MaxChopSeconds = 10
MoveIDs = [WoodID, 0x318F, 0x3199, 0x3190, 0x2F5F, 0x3191, 0x1BDD]
TreeStaticID = [ 0xc95, 0xc96, 0xc99, 0xc9b, 0xc9c, 0xc9D, 0xc8a, 0xca6, 0xca8, 
0xcaa, 0xcab, 0xcc3, 0xcc4, 0xcc8, 0xcc9, 0xcca, 0xccb, 0xccc, 0xccd, 0xcd3, 0xcd1, 0xcd0, 0xcd6, 0xcd8, 
0xcda, 0xcdd, 0xce0, 0xce3, 0xce6, 0xcf8, 0xcf8, 0xcfe, 0xd01, 0xd25, 0xd27, 0xd35, 0xd37, 0xd38, 
0xd42, 0xd43, 0xd59, 0xd70, 0xd85, 0xd94, 0xd96, 0xd98, 0xd9a, 0xd9c, 0xd9e, 0xda0, 0xda2, 0xda04, 
0xda8, 0x0DAC, 0x0DAD ]
#
if OldServer:
    class Tree:
        def __init__(self, x, y, z, id):
            self.X = x
            self.Y = y
            self.Z = z
            self.ID = id
#
#
def FindAxe():
    global HatchetID, OldServer
    if OldServer:
        axe = Player.GetItemOnLayer("RightHand")
        if axe is None:
            axe = Player.GetItemOnLayer("LeftHand")
        if axe is None or ("axe" not in axe.Name.lower() and "hatchet" not in axe.Name.lower()):
            print("You must have an axe equipped")
            axe = None
    else:
        axe = Items.FindByID(HatchetID, 0, Player.Backpack.Serial, -1)
    if axe:
        return axe
    else:
        Misc.SendMessage("Cannot find an axe")
        return None
#    
def FindBagOfHolding():
    for item in Player.Backpack.Contains:
        if item.IsContainer and not item.IsBagOfSending:
            props = Items.GetProperties(item.Serial, 5000)
            for prop in props:
                if "Bag of Holding" in prop.ToString():
                    return item                
    return None                
#
def FindMule():
    global MuleID, MuleColor, LlamaID, LlamaColor
    mule = None
    llama = None
    pets = Player.Pets
    for pet in pets:
        if pet.MobileID == MuleID and pet.Hue == MuleColor:
            #print(f"Name: \"{pet.Name}\"")
            mule = pet
        if pet.MobileID == LlamaID and pet.Hue == MuleColor:
            #print(f"Name: \"{pet.Name}\"")
            llama = pet
    if mule == None and llama == None:
        return None
    if mule == None:
        return llama
    if llama == None:
        return mule
    if Player.DistanceTo(llama) < Player.DistanceTo(mule):
        return llama
    return mule

def MoveToMule():
    global WoodID
    # Move to Mule
    mule = FindMule()
    if mule == None:
        print(f"Cannot find a mule")
        return 
    ores = Items.FindAllByID(WoodID, -1, Player.Backpack.Serial, 0, False)       
    for ore in ores:
        Items.Move(ore.Serial, mule.Serial, -1)
        Misc.Pause(800)   
#
def ConvertLogsToWood():
    global LogID
    axe = FindAxe()
    log = Items.FindByID(LogID, -1, Player.Backpack.Serial, -1) 
    prev_log = 0  
    max_tries = 10 
    while log != None:
        prev_log = log.Serial
        Items.UseItem(axe)
        Target.WaitForTarget(5000, False)
        Target.TargetExecute(log)
        Misc.Pause(1000)
        log = Items.FindByID(LogID, -1, Player.Backpack.Serial)        
#   
def MoveWoodToBOH():
    global WoodID, MoveIDs
    # Move to BagOfHolding       
    BOH = FindBagOfHolding()
    if BOH == None:
        print(f"Cannot find a Bag of Holding")
        return
    for moveID in MoveIDs:
        while Items.ContainerCount(Player.Backpack.Serial, moveID, -1, False) > 0:  
            thing = Items.FindByID(moveID, -1, Player.Backpack.Serial, 0)
            if thing != None:
                Items.Move(thing.Serial, BOH, -1)
                Misc.Pause(800)
#
def StoreInKey(): 
    global WoodID, WoodKeyID, WoodKeyColor, MasterKeyID, MasterKeyColor, KeyGumpID
    retValue = False

    allWood = Items.FindAllByID(WoodID, -1, Player.Backpack.Serial, 2 , False)
    if len(allWood) == 0:
        return retValue  
    woodKey = Items.FindByID(WoodKeyID, WoodKeyColor, Player.Backpack.Serial, 2 , False) 
    if woodKey == None:
        woodKey = Items.FindByID(MasterKeyID, MasterKeyColor, Player.Backpack.Serial, 2 , False)
        if woodKey == None:
            print("No key for wood storage found")
            return retValue
    #
    contextList = Misc.WaitForContext(woodKey.Serial, 5000)  
    found = retValue
    for entry in contextList:        
        if entry.Entry == "Refill from stock":
            found = True
            break  
    if found:
        Misc.ContextReply(woodKey.Serial, "Refill from stock")
        Gumps.WaitForGump(KeyGumpID, 5000)
        if Gumps.HasGump(KeyGumpID):
            Gumps.SendAction(KeyGumpID, 0)
            Gumps.CloseGump(KeyGumpID)
            Misc.Pause(500)
            retValue = True
    else:
        print("key didnt have right context")
        retValue = False
    Target.Cancel()  
    #
    return retValue
#
def ScanStaticTrees(start_x, start_y): 
    # Used for old servers
    trees = []
    #
    for y in range(start_y, start_y+8+1):
        for x in range(start_x, start_x+8+1):
            tileinfo = Statics.GetStaticsTileInfo(x, y, Player.Map)
            # print("X:{} Y:{} tilenum: {} map{}".format( 
            # x, y, tileinfo.Count, Player.Map))
            if tileinfo.Count > 0:
                for tile in tileinfo: 
                    if tile.StaticID in TreeStaticID:
                        # print('--> Tree X: %i - Y: %i - Z: %i' % (x, y, tile.StaticZ), 66)
                        tree = Tree(x, y, tile.StaticZ, tile.StaticID)
                        trees.append(tree)
    return trees

def NearestTree(trees):
    tree = None
    nearestDistance = 9999
    for t in trees:
        dist = Misc.Distance(Player.Position.X, Player.Position.Y, t.X, t.Y)
        if dist < nearestDistance:
            nearestDistance = dist
            tree = t
    return tree
#
def ChopTree():
    global OldServer, TreeStaticID
    wood_to_chop = True
    find_new_tree = False
    Journal.Clear() 
    while wood_to_chop:
        axe = FindAxe()
        failed_chop_time = time.time() + MaxChopSeconds
        if Target.HasTarget():
            Target.Cancel
        #    
        if OldServer:
            print("Scanning for trees...")
            trees = ScanStaticTrees(int(Player.Position.X/8)*8, int(Player.Position.Y/8)*8)
            if len(trees) == 0:
                print(f"Tree not found")
                return
            tree = NearestTree(trees)
            find_new_tree = tree is not None
            route = PathFinding.Route()
            route.X = tree.X - 1
            route.Y = tree.Y - 1
            route.MaxRetry = 5
            PathFinding.Go( route )
            if not PathFinding.Go( route ):
                print(f"Cannot pathfind to tree at X:{tree.X} Y:{tree.Y}")
                # Player.HeadMessage( colors[ 'cyan' ], 'Cannot pathfind to tree, please move within range manually' )
            else:
                PathFinding.PathFindTo(route.X, route.Y)
            tiles = PathFinding.GetPath(tree.X, tree.Y)
            PathFinding.RunPath(tiles)

            Misc.Pause(1000)
            Items.UseItem(axe)
            Target.WaitForTarget(5000, False)
            #print("Chop Tree at X:{} Y:{} Z:{} Tile:{}".format(tree.X, tree.Y, tree.Z, tree.ID))
            if Target.HasTarget():
                Target.TargetExecute(tree.X, tree.Y, tree.Z, tree.ID)
            else:
                print(f"Unable to target tree at {Player.Position.X} {Player.Position.Y}")
                break
        else:
            Target.TargetResource(axe, "wood")
        Misc.Pause(700)
        if Journal.Search("not enough wood here"):
            print("Stopping due to finished")
            find_new_tree = True
            # wood_to_chop = False
        if Journal.Search("You put") or Journal.Search("You put"):
            failed_chop_time = time.time() + MaxChopSeconds
        if Journal.Search("no more wood"):
            print("Stopping due to Journal")
            wood_to_chop = False
        if Player.Weight > Player.MaxWeight * .95:
            ConvertLogsToWood()
            if FindMule():
                MoveToMule()  
            if FindBagOfHolding():
                MoveWoodToBOH()          
            if Player.Weight > Player.MaxWeight * .95:
                print("Stopping due to Player Weight")
                wood_to_chop = False
        if Journal.Search("Can't get there"):
            print("Stopping due to Unreachable")
            #all comeMisc.CheckIgnoreObject(tree)
            wood_to_chop = False    
        if Journal.Search("far away"):
            print("Stopping due to Unreachable")
            #Misc.IgnoreObject(tree)
            wood_to_chop = False
        if Journal.Search("lack the skill"):
            print("Stopping due to lack of skill")
            #Misc.IgnoreObject(tree)
            wood_to_chop = False    
        if Journal.Search("cannot be seen"):
            print("Stopping due to lack of visibility")
            #Misc.IgnoreObject(tree)
            wood_to_chop = False  
        if Journal.Search("can't use an axe"):
            print("Stopping due to invalid target")
            #Misc.IgnoreObject(tree)
            wood_to_chop = False                     
        if Journal.Search("You broke your axe"):
            axe = FindAxe()
            if axe:
                failed_chop_time = time.time() + MaxChopSeconds
                wood_to_chop = True
            else:
                Misc.SendMessage("Cannot find a new axe")
                wood_to_chop = False
        if failed_chop_time <= time.time():
            print("Stopping due to Time-out")
            #Misc.IgnoreObject(tree)
            wood_to_chop = False       


ChopTree()        
ConvertLogsToWood()
#MoveWoodToBOH()
#StoreInKey()
