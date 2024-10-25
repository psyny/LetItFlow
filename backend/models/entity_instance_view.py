from typing import Dict, List, Optional

class EntityInstanceView:
    def __init__(self, entityDisplayId: str, instanceId: str, name: Optional[str] = None, label: Optional[str] = None,
                 displayType: Optional[str] = None, stats: Optional[Dict[str, Optional[int]]] = None):
        """Initialize the EntityInstanceView object with immutable entityDisplayId and instanceId."""
        self._entityDisplayId = entityDisplayId  # Entity display ID is fixed and immutable
        self._instanceId = instanceId            # Instance ID is fixed and immutable
        self.name: Optional[str] = name
        self.label: Optional[str] = label
        self.displayType: Optional[str] = displayType
        self.stats: Dict[str, Optional[int]] = stats if stats else {
            'hp': 0,
            'tempHp': 0,
            'ally': False,
            'conditions': []  # List of conditions (represented as dicts)
        }

    @property
    def entityDisplayId(self) -> str:
        """Get the entityDisplayId (immutable)."""
        return self._entityDisplayId

    @property
    def instanceId(self) -> str:
        """Get the instanceId (immutable)."""
        return self._instanceId

    def set_name(self, new_name: str):
        """Update the displayed name of the entityInstanceView."""
        self.name = new_name

    def set_label(self, new_label: str):
        """Update the label of the entityInstanceView."""
        self.label = new_label

    def set_displayType(self, new_displayType: str):
        """Update the display type of the entityInstanceView."""
        self.displayType = new_displayType

    # Individual methods for updating stats
    def set_hp(self, new_hp: int):
        """Update the hp stat of the entityInstanceView."""
        self.stats["hp"] = new_hp

    def set_tempHp(self, new_tempHp: int):
        """Update the tempHp stat of the entityInstanceView."""
        self.stats["tempHp"] = new_tempHp

    def set_ally(self, ally: bool):
        """Update whether the entityInstanceView is an ally."""
        self.stats["ally"] = ally

    def add_condition(self, condition: Dict):
        """Add a condition to the entityInstanceView."""
        self.stats["conditions"].append(condition)

    def remove_condition(self, conditionId: str):
        """Remove a condition from the entityInstanceView by conditionId."""
        self.stats["conditions"] = [
            cond for cond in self.stats["conditions"] if cond["conditionId"] != conditionId
        ]

    def to_primitive(self) -> Dict:
        """Convert the EntityInstanceView object to a dictionary."""
        return {
            "entityDisplayId": self._entityDisplayId,
            "instanceId": self._instanceId,
            "name": self.name,
            "label": self.label,
            "displayType": self.displayType,
            "stats": self.stats
        }

    @staticmethod
    def from_primitive(data: Dict) -> "EntityInstanceView":
        """Create an EntityInstanceView object from a dictionary."""
        return EntityInstanceView(
            entityDisplayId=data["entityDisplayId"],
            instanceId=data["instanceId"],
            name=data.get("name"),
            label=data.get("label"),
            displayType=data.get("displayType"),
            stats=data.get("stats", {
                "hp": 0,
                "tempHp": 0,
                "ally": False,
                "conditions": []
            })
        )
