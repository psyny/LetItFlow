from typing import List, Dict, Optional
from enum import Enum

class GamestateChange:
    class Type(Enum):
        # Basic Changes
        CHANGED_GAMESTATE_PHASE = "changed_gamestate_phase"         

        # Gamestate - Exploration
        ADDED_TO_EXPLORATION = "added_to_exploration"
        REMOVED_FROM_EXPLORATION = "removed_from_exploration"
        ADDED_PLACE = "added_place"
        REMOVED_PLACE = "removed_place"
        ADDED_TO_PLACE = "added_to_place"
        REMOVED_FROM_PLACE = "removed_from_place"

        # Gamestate - Tactical
        ADDED_TO_TACTICAL = "added_to_tactical"
        REMOVED_FROM_TACTICAL = "removed_from_tactical"
        ADDED_TO_TURN_ORDER = "added_to_turn_order"
        REMOVED_FROM_TURN_ORDER = "removed_from_turn_order"
        CHANGED_IN_TURN_ORDER = "changed_in_turn_order"

        # Instances
        INSTANCE_STAT_CHANGED = "instance_stat_changed"
        INSTANCE_CONDITION_CHANGED = "instance_condition_changed"
        

    def __init__(self, changeId: str, changeType: str):
        """Initialize the Action object with immutable actionId."""
        self._changeId = changeId  # Change ID is fixed and immutable
        self.changeType: str = changeType
        self.sourceIds: List[str] = []  # List of instance IDs of the sources
        self.targetIds: List[str] = []  # List of instance IDs of the targets
        self.actionData: Dict[str, str] = {}  # List of actionData objects

    def to_primitive(self) -> Dict:
        """Convert the Action object to a dictionary."""
        return {
            "changeId": self._changeId,
            "changeType": self.changeType,
            "sourceIds": self.sourceIds,
            "targetIds": self.targetIds,
            "actionData": self.actionData
        }
    
    def __str__(self):
        return f"GamestateChange(changeType={self.changeType}, sourceIds={self.sourceIds}, targetIds={self.targetIds}, actionData={self.actionData} )"    

    @staticmethod
    def from_primitive(data: Dict) -> "GamestateChange":
        """Create an GamestateChange object from a dictionary."""
        action = GamestateChange(
            changeId=data["changeId"],
            changeType=data.get("changeType"),
        )
        action.sourceIds = data.get("sourceIds", [])
        action.targetIds = data.get("targetIds", [])
        action.actionData = data.get("actionData", {})
        return action

