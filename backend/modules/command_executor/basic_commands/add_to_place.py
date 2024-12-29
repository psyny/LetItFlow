from typing import Dict, List, Optional
import copy
import random

from backend.models.command import Command
from backend.models.gamestate_change import GamestateChange
from backend.controllers.app.app_controller import AppController
from backend.modules.utils.app_utils import AppUtils

def add_to_place(command: Command, partyId: str) -> List[GamestateChange]:
    """
    ...
    """

    # Get gamestate and controllers    
    gamestate = AppUtils.get_gamestate(partyId)
    gamestate_controller = AppController().gamestate_controller

    # Change struct
    changes: List[GamestateChange] = []
    change = GamestateChange("", GamestateChange.Type.ADDED_TO_PLACE.value)  

    placeName = command.actionData.get("place_name")
    if not placeName:
        return changes
    
    change["place_name"] = placeName
    
    # Execute command
    for instance_id in command.targetIds:
        added = gamestate_controller.phase_exploration_controller.add_to_place(gamestate, instance_id, placeName)
        if added:
            change.targetIds.append(instance_id)  

    if len(change.targetIds) > 0:
        changes.append(change)
    
    return changes


