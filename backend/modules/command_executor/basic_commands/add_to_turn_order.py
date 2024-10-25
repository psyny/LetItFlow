from typing import Dict, List, Optional
import copy
import random

from backend.models.command import Command
from backend.models.gamestate_change import GamestateChange
from backend.controllers.app.app_controller import AppController
from backend.modules.utils.app_utils import AppUtils

def add_to_turn_order(command: Command, partyId: str) -> List[GamestateChange]:
    """
    ...
    """

    # Get gamestate    
    gamestate = AppUtils.get_gamestate(partyId)

    # Get current turn order
    old_turn_order = gamestate.get_turn_order()    

    # We want only to add to turn order entities already in taticalmode but dont have a initiative score (so not in turn order)
    add_to_turn = set()
    currently_in_tactical = gamestate.get_in_tactical()
    intiative_scores = gamestate.get_initiative_scores()
    for instance_id in command.targetIds:
        if instance_id in currently_in_tactical:
            if instance_id not in intiative_scores:
                add_to_turn.add(instance_id)

    # Build initiative Score data for adding instance
    for instance_id in add_to_turn:
        entity_instance = gamestate.get_entity_instance(instance_id)
        entity = gamestate.get_entity(entity_instance.entityId)
        score_val = gamestate.generate_initiative_score_val(entity_instance.get_initiative(), entity.get_dex())
        gamestate.set_initiative_score(instance_id, score_val, 0, score_val)

    # Build new turn order data - only instances that have score data will be in the turn order
    sorted_score_datas = []
    for instance_id, score_data in gamestate.get_initiative_scores().items():
        sorted_score_datas.append(score_data)
            
    # Sort entity instances
    sorted_score_datas.sort(key=lambda x: (-x['currentScore'], x['untier'], -x['rolledScore']))

    # Extract the sorted instance IDs
    new_turn_order = [score_data['instanceId'] for score_data in sorted_score_datas]

    # Set the new turn order in the gamestate
    gamestate.set_turn_order(new_turn_order)

    # ------------------------

    # Now, lets get the differences in turn order
    changes: list[GamestateChange] = []
    changes_added: list[GamestateChange] = []
    changed_changed: list[GamestateChange] = []

    # Get the current turn order and compare with the new sorted order
    for position, instance_id in enumerate(new_turn_order):
        if position >= len(old_turn_order) or old_turn_order[position] != instance_id:
            if instance_id in add_to_turn:
                change = GamestateChange("", GamestateChange.Type.ADDED_TO_TURN_ORDER.value)
                change.targetIds.append(instance_id)   
                change.actionData["position"] = position
                changes_added.append(change)
            else:
                change = GamestateChange("", GamestateChange.Type.CHANGED_IN_TURN_ORDER.value)     
                change.targetIds.append(instance_id)   
                change.actionData["position"] = position       
                changed_changed.append(change)    

    # Return the log of changes
    changes = changed_changed + changes_added
    return changes

