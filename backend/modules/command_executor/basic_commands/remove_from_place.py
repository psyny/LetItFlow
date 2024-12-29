from typing import Dict, List, Optional
import copy
import random

from backend.models.command import Command
from backend.models.gamestate_change import GamestateChange
from backend.controllers.app.app_controller import AppController
from backend.modules.utils.app_utils import AppUtils

def remove_from_place(command: Command, partyId: str) -> List[GamestateChange]:
    """
    ...
    """

    # Get gamestate and controllers    
    gamestate = AppUtils.get_gamestate(partyId)
    gamestate_controller = AppController().gamestate_controller

    # Change struct
    changes: List[GamestateChange] = []
    change = GamestateChange("", GamestateChange.Type.REMOVED_FROM_PLACE.value)  

    # Execute command
    for instance_id in command.targetIds:
        removed = gamestate_controller.phase_exploration_controller.remove_from_place(gamestate, instance_id)
        if removed:
            change.targetIds.append(instance_id)  

    if len(change.targetIds) > 0:
        changes.append(change)
    
    return changes


