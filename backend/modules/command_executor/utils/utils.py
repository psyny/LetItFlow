from typing import Dict, List, Optional
from backend.models.gamestate_change import GamestateChange

def get_gamestate_tactical_turn_order_changes(old_turn_order: List[str], new_turn_order: List[str]) -> List[GamestateChange]:    
    # Support structures
    old_turn_order_set = set(old_turn_order)
    new_turn_order_set = set(new_turn_order)

    # Changes list
    changed_added: list[GamestateChange] = []
    changed_changed: list[GamestateChange] = []
    changed_removed: list[GamestateChange] = []

    # Get removeds
    for position, instance_id in enumerate(old_turn_order):
        if instance_id not in new_turn_order_set:
            change = GamestateChange("", GamestateChange.Type.REMOVED_FROM_TURN_ORDER.value)
            change.targetIds.append(instance_id)   
            change.actionData["position"] = position
            changed_removed.append(change)

    # Get addeds and changeds
    for position, instance_id in enumerate(new_turn_order):
        # Addeds
        if instance_id not in old_turn_order_set:
            change = GamestateChange("", GamestateChange.Type.ADDED_TO_TURN_ORDER.value)
            change.targetIds.append(instance_id)   
            change.actionData["position"] = position
            changed_added.append(change)
        else:
            # Changeds
            if position >= len(old_turn_order) or old_turn_order[position] != instance_id:
                change = GamestateChange("", GamestateChange.Type.CHANGED_IN_TURN_ORDER.value)     
                change.targetIds.append(instance_id)   
                change.actionData["position"] = position       
                changed_changed.append(change) 

    # Return the log of changes
    changes: list[GamestateChange] = []
    changes = changed_removed + changed_changed + changed_added
    return changes

def get_gamestate_tactical_intactical_changes(before_in_tactical: List[str], current_in_tactical: List[str]) -> List[GamestateChange]:
    before = set(before_in_tactical)
    current = set(current_in_tactical)

    changes_removed: list[GamestateChange] = []
    for instance_id in before_in_tactical:
        if instance_id not in current:
            change = GamestateChange("", GamestateChange.Type.REMOVED_FROM_TACTICAL.value)     
            change.targetIds.append(instance_id)   
            changes_removed.append(change) 

    changes_added: list[GamestateChange] = []
    for instance_id in current_in_tactical:
        if instance_id not in before:
            change = GamestateChange("", GamestateChange.Type.ADDED_TO_TACTICAL.value)     
            change.targetIds.append(instance_id)   
            changes_removed.append(change) 

    changes: list[GamestateChange] = []
    changes = changes_removed + changes_added

    return changes