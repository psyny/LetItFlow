from typing import Dict, List, Optional
import copy
import random

from backend.models.command import Command
from backend.models.gamestate_change import GamestateChange
from backend.controllers.app.app_controller import AppController
from backend.modules.utils.app_utils import AppUtils

def instance_condition_change(command: Command, partyId: str) -> List[GamestateChange]:
    """
    ...
    """

    # Get gamestate and controllers    
    gamestate = AppUtils.get_gamestate(partyId)

    # Change struct
    changes: List[GamestateChange] = []
    change = GamestateChange("", GamestateChange.Type.INSTANCE_CONDITION_CHANGED.value)  

    # Execute
    changeType = command.actionData["type"]
    changeCondition = command.actionData["condition"]
    changeValue = command.actionData["value"]
    changeEndCondition = command.actionData["end_condition"]

    change.actionData = command.actionData

    for instance_id in command.targetIds:
        instance = gamestate.get_entity_instance(instance_id)
        if instance:
            change.targetIds(instance_id)

            if changeType == "add":
                condition = {
                    "conditionId": changeCondition,
                    "value": changeValue,
                    "end_condition": changeEndCondition,
                }
                instance.add_condition(condition)

            elif changeType == "remove":
                instance.remove_condition(changeCondition)

    # Change list
    if len(change.targetIds) > 0:
        changes.append(change)

    return changes


