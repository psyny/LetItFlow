import random
from typing import Dict, List, Optional

class EntityInstance:
    def __init__(self, instanceId: str, entityId: str):
        """Initialize the EntityInstance object with immutable instanceId and entityId."""
        self._instanceId = instanceId  # Instance ID is fixed and immutable
        self._entityId = entityId      # Entity ID is fixed and immutable
        self.playerId: str = ""
        self.label: str = ""
        self.stats: Dict[str, any] = {
            'hp': 0,
            'tempHp': 0,
            'initiative': 0, # Rolled initative, with the dex mod 
            'ally': False,
            'visible': True,
            'conditions': []  # List of conditions (represented as dicts)
        }

        self.seed: int = random.randint(0, 100)  # Random number between 0 and 100
        self.healthPoint1: int = random.randint(20, 45)  # Random number between 20 and 45
        self.healthPoint2: int = random.randint(55, 80)  # Random number between 55 and 80

    @property
    def instanceId(self) -> str:
        """Get the instanceId (immutable)."""
        return self._instanceId

    @property
    def entityId(self) -> str:
        """Get the entityId (immutable)."""
        return self._entityId

    # Getters for base stats
    def get_hp(self) -> int:
        """Get the hp stat of the entityInstance."""
        return self.stats["hp"]

    def get_tempHp(self) -> int:
        """Get the tempHp stat of the entityInstance."""
        return self.stats["tempHp"]

    def get_initiative(self) -> int:
        """Get the initiative stat of the entityInstance."""
        return self.stats["initiative"]

    def get_ally(self) -> bool:
        """Check if the entityInstance is an ally."""
        return self.stats["ally"]

    def get_visible(self) -> bool:
        """Check if the entityInstance is visible."""
        return self.stats["visible"]

    # Setters for base stats
    def set_hp(self, new_hp: int):
        """Update the hp stat of the entityInstance."""
        self.stats["hp"] = new_hp

    def set_tempHp(self, new_tempHp: int):
        """Update the tempHp stat of the entityInstance."""
        self.stats["tempHp"] = new_tempHp

    def set_initiative(self, new_initiative: int):
        """Update the initiative stat of the entityInstance."""
        self.stats["initiative"] = new_initiative

    def set_ally(self, ally: bool):
        """Update whether the entityInstance is an ally."""
        self.stats["ally"] = ally

    def set_visible(self, visible: bool):
        """Update the visibility of the entityInstance."""
        self.stats["visible"] = visible

    # Methods to manage conditions
    def add_condition(self, condition: Dict):
        """Add a condition to the entityInstance."""
        self.stats["conditions"].append(condition)

    def remove_condition(self, conditionId: str):
        """Remove a condition from the entityInstance by conditionId."""
        self.stats["conditions"] = [
            cond for cond in self.stats["conditions"] if cond["conditionId"] != conditionId
        ]

    # Convert to a primitive dictionary
    def to_primitive(self) -> Dict:
        """Convert the EntityInstance object to a dictionary."""
        return {
            "instanceId": self._instanceId,
            "entityId": self._entityId,
            "playerId": self.playerId,
            "label": self.label,
            "stats": self.stats,
            "seed": self.seed,
            "healthPoint1": self.healthPoint1,
            "healthPoint2": self.healthPoint2
        }

    # Create from a primitive dictionary
    @staticmethod
    def from_primitive(data: Dict) -> "EntityInstance":
        """Create an EntityInstance object from a dictionary."""
        entityInstance = EntityInstance(
            instanceId=data["instanceId"],
            entityId=data["entityId"],
        )

        entityInstance.playerId = data.get("playerId", entityInstance.playerId)
        entityInstance.label = data.get("label", entityInstance.label)
        entityInstance.stats = data.get("stats", entityInstance.stats)
        entityInstance.seed = data.get("seed", entityInstance.seed) 
        entityInstance.healthPoint1 = data.get("healthPoint1", entityInstance.healthPoint1)
        entityInstance.healthPoint2 = data.get("healthPoint2", entityInstance.healthPoint2)

        return entityInstance