from typing import Dict, List, Optional
import copy
import random

from backend.models.command import Command
from backend.models.gamestate_change import GamestateChange
from backend.controllers.app.app_controller import AppController
from backend.modules.utils.app_utils import AppUtils

def add_place(command: Command, partyId: str) -> List[GamestateChange]:
    """
    ...
    """

    # Get gamestate and controllers    
    gamestate = AppUtils.get_gamestate(partyId)
    gamestate_controller = AppController().gamestate_controller

    # Change struct
    changes: List[GamestateChange] = []
    change = GamestateChange("", GamestateChange.Type.ADDED_PLACE.value)  

    placeName = command.actionData.get("place_name")
    if not placeName:
        return changes
    
    # Execute command
    added = gamestate_controller.phase_exploration_controller.add_place(gamestate, placeName)
    if added:
        change.actionData["place_name"] = placeName
        changes.append(change)
    
    return changes


