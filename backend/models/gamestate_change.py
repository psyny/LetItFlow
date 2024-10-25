from typing import List, Dict, Optional
from enum import Enum

class GamestateChange:
    class Type(Enum):
        # Basic Types
        ADDED_TO_TURN_ORDER = "added_to_turn_order"
        CHANGED_IN_TURN_ORDER = "changed_in_turn_order"

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

