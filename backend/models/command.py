from typing import List, Dict, Optional
from enum import Enum

class Command:
    class Type(Enum):
        # Basic Types
        ADD_TO_TURN_ORDER = "add_to_turn_order"

    def __init__(self, commandType: str):
        """Initialize the Action object with immutable actionId."""
        self.commandType: str = commandType
        self.sourceIds: List[str] = []  # List of instance IDs of the sources
        self.targetIds: List[str] = []  # List of instance IDs of the targets
        self.actionData: Dict[str, str] = {}  # List of actionData objects

    def to_primitive(self) -> Dict:
        """Convert the Action object to a dictionary."""
        return {
            "commandType": self.commandType,
            "sourceIds": self.sourceIds,
            "targetIds": self.targetIds,
            "actionData": self.actionData
        }

    @staticmethod
    def from_primitive(data: Dict) -> "Command":
        """Create an Action object from a dictionary."""
        action = Command(
            commandType=data.get("commandType"),
        )
        action.sourceIds = data.get("sourceIds", [])
        action.targetIds = data.get("targetIds", [])
        action.actionData = data.get("actionData", {})
        return action
