from typing import Dict, List, Optional
import copy
import random

from backend.models.command import Command
from backend.models.gamestate_change import GamestateChange
from backend.controllers.app.app_controller import AppController
from backend.modules.utils.app_utils import AppUtils

def instance_stat_change(command: Command, partyId: str) -> List[GamestateChange]:
    """
    ...
    """

    # Get gamestate and controllers    
    gamestate = AppUtils.get_gamestate(partyId)

    # Change struct
    changes: List[GamestateChange] = []
    change = GamestateChange("", GamestateChange.Type.INSTANCE_STAT_CHANGED.value)  

    # Execute
    changeType = command.actionData["type"]
    changeStat = command.actionData["stat"]
    changeValue = command.actionData["value"]

    change.actionData = command.actionData

    for instance_id in command.targetIds:
        instance = gamestate.get_entity_instance(instance_id)
        if instance:
            if changeType == "add":
                _, _, succeed = instance.add_stat(changeStat, changeValue)
                if succeed:
                    change.targetIds.append(instance_id)
            elif changeType == "set":
                _, _, succeed = instance.set_stat(changeStat, changeValue)
                if succeed:
                    change.targetIds.append(instance_id)

            if changeStat == "hp":
                entity = gamestate.get_entity(instance.entityId)
                maxHp, _, _ = entity.get_stat("hp")
                currHp, _, _ = instance.get_stat("hp")
                if currHp > maxHp:
                    instance.set_stat(changeStat, maxHp)

    # Change list
    if len(change.targetIds) > 0:
        changes.append(change)

    return changes


