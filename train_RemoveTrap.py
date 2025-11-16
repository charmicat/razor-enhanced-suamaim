from AutoComplete import *

from Scripts import config
from Scripts.glossary.colors import colors
from Scripts.glossary.items.tools import tools
from Scripts.utilities.items import FindItem

def RemoveTrap():
    trappedChestSerial = Target.PromptTarget( 'Select chest untrap' )
    trappedChest = Items.FindBySerial( trappedChestSerial )
    trappedChest_ID = Items.FindByID("0xA393")

    if trappedChest == None or not trappedChest.IsContainer:
        Player.HeadMessage( colors[ 'red' ], 'Invalid chest!' )
        return
        
    if Player.DistanceTo( trappedChest ) > 1:
        Player.HeadMessage( colors[ 'cyan' ], 'Moving into range of chest' )
        
        route = PathFinding.Route()
        chestPosition = trappedChest.Position
        playerPosition = Player.Position
        
        destinationX = 0
        if playerPosition.X > chestPosition.X:
            destinationX = chestPosition.X + 1
        elif playerPosition.X < chestPosition.X:
            destinationX = chestPosition.X - 1
        else:
            destinationX = chestPosition.X
            
        destinationY = 0
        if playerPosition.Y > chestPosition.Y:
            destinationY = chestPosition.Y + 1
        elif playerPosition.Y < chestPosition.Y:
            destinationY = chestPosition.Y - 1
        else:
            destinationY = chestPosition.Y
            
            
        route.X = destinationX
        route.Y = destinationY
        route.DebugMessage = False
        route.StopIfStuck = True
        
        if not PathFinding.Go( route ):
            Player.HeadMessage( colors[ 'cyan' ], 'Cannot pathfind to chest, please move within range manually' )
            while not Player.DistanceTo( trappedChest ) < 2:
                Misc.Pause( 100 )
                
    Player.HeadMessage( colors[ 'cyan' ], 'Starting chest untrap!' )
    
    # Journal.Clear()
    # while not ( Journal.SearchByName( 'The lock quickly yields to your skill.', '' ) or
    #         Journal.SearchByType( 'This does not appear to be locked.', 'Regular' ) ):
    #     Items.UseItem( lockpicks )
    #     Target.WaitForTarget( 2000, True )
    #     Target.TargetExecute( trappedChest )
    #     Misc.Pause( 4000 )
    #     Misc.Pause( config.journalEntryDelayMilliseconds )

    #     lockpicks = FindItem( lockpicks.ItemID, Player.Backpack )
    #     if lockpicks == None:
    #         Player.HeadMessage( colors[ 'red' ], 'Ran out of lockpicks!' )
    #         return
        
    target = Target.PromptTarget( 'Select trapped chest' )
    Journal.Clear()
    while not Journal.SearchByName( 'You start to tame the creature', Player.Name ):
        Player.UseSkill( 'Remove Trap' )
        Target.WaitForTarget( 2000, False )
        Target.TargetExecute( target )
        Misc.Pause( 100 )

RemoveTrap()
