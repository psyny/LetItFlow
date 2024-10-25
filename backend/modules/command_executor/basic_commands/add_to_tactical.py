from typing import Dict, List, Optional
import copy
import random

from backend.models.command import Command
from backend.models.gamestate_change import GamestateChange
from backend.controllers.app.app_controller import AppController
from backend.modules.utils.app_utils import AppUtils

from backend.modules.command_executor.utils.utils import get_gamestate_tactical_intactical_changes

def add_to_tactical(command: Command, partyId: str) -> List[GamestateChange]:
    """
    ...
    """

    # Get gamestate and controllers    
    gamestate = AppUtils.get_gamestate(partyId)
    gamestate_controller = AppController().gamestate_controller
    
    # Get current inTactical
    old_in_tactical = copy.deepcopy(gamestate.get_in_tactical())

    # Execute command
    gamestate_controller.phase_tatical_controller.add_to_tactical(gamestate, command.targetIds)

    # Get new inTactical
    current_in_tactical = copy.deepcopy(gamestate.get_in_tactical())

    # Get the changes
    changes = get_gamestate_tactical_intactical_changes(old_in_tactical, current_in_tactical)
    return changes


