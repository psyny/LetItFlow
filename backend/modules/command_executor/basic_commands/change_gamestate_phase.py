from typing import Dict, List, Optional
import copy
import random

from backend.models.command import Command
from backend.models.gamestate import ENUMGamestatePhases
from backend.models.gamestate_change import GamestateChange
from backend.controllers.app.app_controller import AppController
from backend.modules.utils.app_utils import AppUtils

from backend.modules.command_executor.utils.utils import get_gamestate_tactical_intactical_changes

def change_gamestate_phase(command: Command, partyId: str) -> List[GamestateChange]:
    """
    ...
    """

    # Get gamestate and controllers    
    gamestate = AppUtils.get_gamestate(partyId)
    gamestate_controller = AppController().gamestate_controller
    
    # Change based on phase
    phase_name = command.targetIds[0]

    if phase_name == ENUMGamestatePhases.INACTIVE.value:
        gamestate_controller.phase_inactive_controller.start_inactive_phase(gamestate)
        change = GamestateChange("", GamestateChange.Type.CHANGED_GAMESTATE_PHASE.value)     
        change.targetIds.append(phase_name)   
        return [change,]     

    if phase_name == ENUMGamestatePhases.LOBBY.value:
        gamestate_controller.phase_lobby_controller.start_lobby_phase(gamestate)
        change = GamestateChange("", GamestateChange.Type.CHANGED_GAMESTATE_PHASE.value)     
        change.targetIds.append(phase_name)   
        return [change,]       

    if phase_name == ENUMGamestatePhases.EXPLORATION.value:
        gamestate_controller.phase_exploration_controller.start_exploration_phase(gamestate)
        change = GamestateChange("", GamestateChange.Type.CHANGED_GAMESTATE_PHASE.value)     
        change.targetIds.append(phase_name)   
        return [change,]              

    if phase_name == ENUMGamestatePhases.TACTICAL.value:
        gamestate_controller.phase_tactical_controller.start_tactical_phase(gamestate)
        change = GamestateChange("", GamestateChange.Type.CHANGED_GAMESTATE_PHASE.value)     
        change.targetIds.append(phase_name)   
        return [change,]  
      
    return []

