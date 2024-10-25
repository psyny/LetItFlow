from typing import Dict, List, Optional
import copy
import random

from backend.models.command import Command
from backend.models.gamestate_change import GamestateChange
from backend.controllers.app.app_controller import AppController
from backend.modules.utils.app_utils import AppUtils

from backend.modules.command_executor.utils.utils import get_gamestate_tactical_turn_order_changes
from backend.modules.command_executor.utils.utils import get_gamestate_tactical_intactical_changes

def remove_from_tactical(command: Command, partyId: str) -> List[GamestateChange]:
    """
    ...
    """

    # Get gamestate and controllers    
    gamestate = AppUtils.get_gamestate(partyId)
    gamestate_controller = AppController().gamestate_controller
    
    # Get current
    old_in_tactical = copy.deepcopy(gamestate.get_in_tactical())
    old_turn_order = copy.deepcopy(gamestate.get_turn_order())

    # Execute command
    gamestate_controller.phase_tactical_controller.remove_from_tactical(gamestate, command.targetIds)

    # Get new
    current_in_tactical = copy.deepcopy(gamestate.get_in_tactical())
    current_turn_order = copy.deepcopy(gamestate.get_turn_order())

    # Get the changes
    turnOrderChanges = get_gamestate_tactical_turn_order_changes(old_turn_order, current_turn_order)
    inTacticalChanges = get_gamestate_tactical_intactical_changes(old_in_tactical, current_in_tactical)

    changes = turnOrderChanges + inTacticalChanges
    return changes


