from AutoComplete import *

Misc.SetSharedValue( 'OldServer', True )

if Player.Name == 'TheWarMage':
    # if Player.Name == 'TheWarMage':

    Misc.SetSharedValue( 'reagentsBag', 0x41323379 )
elif Player.Name == 'Hobofactual':
    # elif Player.Name == 'TheWarPhysician':

    Misc.SetSharedValue( 'reagentsBag', 0x40D386F6 )
elif Player.Name == 'Suamaim':
    # elif Player.Name == 'TheWarMapper':

    Misc.SetSharedValue( 'beetle', 0x001D9588 )
    Misc.SetSharedValue( 'reagentsBag', 0x41323379 )
    Misc.SetSharedValue( 'weaponsBag', 0x40DB94B2 )
    Misc.SetSharedValue( 'armorBag', 0x40DB94B2 )
    Misc.SetSharedValue( 'gemsBag', 0x40138D92 )
    Misc.SetSharedValue( 'scrollsBag', 0x413A39D7 )
elif Player.Name == 'TombRaider':
    # elif Player.Name == 'TombRaider':

    Misc.SetSharedValue( 'reagentsBag', 0x402916FB )
