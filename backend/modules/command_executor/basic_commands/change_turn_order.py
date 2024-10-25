from typing import Dict, List, Optional
import copy
import random

from backend.models.command import Command
from backend.models.gamestate_change import GamestateChange
from backend.controllers.app.app_controller import AppController
from backend.modules.utils.app_utils import AppUtils

from backend.modules.command_executor.utils.utils import get_gamestate_tactical_turn_order_changes

def change_turn_order(command: Command, partyId: str) -> List[GamestateChange]:
    """
    ...
    """

    # Get gamestate and controllers    
    gamestate = AppUtils.get_gamestate(partyId)
    gamestate_controller = AppController().gamestate_controller
    
    # Get current turn order
    old_turn_order = copy.deepcopy(gamestate.get_turn_order())

    # Execute command
    gamestate_controller.phase_tatical_controller.change_turn_order(gamestate, command.sourceIds[0], command.targetIds[0])

    # Get new turn order
    new_turn_order = copy.deepcopy(gamestate.get_turn_order())

    # Get the changes
    changes = get_gamestate_tactical_turn_order_changes(old_turn_order, new_turn_order)
    return changes

