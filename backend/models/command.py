from typing import List, Dict, Optional
from enum import Enum

class Command:
    class Type(Enum):
        # Basic Commands
        CHANGE_GAMESTATE_PHASE = "change_gamestate_phase"

        # Phase - Exploration
        ADD_TO_EXPLORATION = "add_to_exploration"
        REMOVE_FROM_EXPLORATION = "remove_from_exploration"
        ADD_PLACE = "add_place"
        REMOVE_PLACE = "remove_place"
        ADD_TO_PLACE = "add_to_place"
        REMOVE_FROM_PLACE = "remove_from_place"

        # Phase - Tactical
        ADD_TO_TACTICAL = "add_to_tactical"
        REMOVE_FROM_TACTICAL = "remove_from_tactical"
        ADD_TO_TURN_ORDER = "add_to_turn_order"
        REMOVE_FROM_TURN_ORDER = "remove_from_turn_order"
        CHANGE_TURN_ORDER = "change_from_turn_order"


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
