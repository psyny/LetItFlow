from enum import Enum
import random
from typing import Dict, List, Optional

class ENUMDisplayLevel(Enum):
    COMPLETE = "complete" # Full resource and stats sheet disclosure
    TACTICAL = "tactical" # Numerical HP values, name, conditions
    IMMERSIVE = "immersive" # Categorical HP values, name, conditions        
    MINIMUM = "minimum" # No HP. Just name and conditions
    INCOGNITO = "incognito" # No HP, no picture, no name, just the existance

class EntityInstance:
    def __init__(self, instanceId: str, entityId: str):
        """Initialize the EntityInstance object with immutable instanceId and entityId."""
        self._instanceId = instanceId  # Instance ID is fixed and immutable
        self._entityId = entityId      # Entity ID is fixed and immutable
        self.playerId: str = ""
        self.label: str = ""
        self.stats: Dict[str, any] = {
            'hp': 0,
            'temp_hp': 0,
            'initiative': 0, # Rolled initative, with the dex mod 
            'death_rolls_successes': 0,
            'death_rolls_fails': 0,
            'ally': False,
            'visible': True,
            'conditions': []  # List of conditions (represented as dicts)
        }

        self.seed: int = random.randint(0, 100)  # Random number between 0 and 100
        self.healthPoint1: int = random.randint(20, 45)  # Random number between 20 and 45
        self.healthPoint2: int = random.randint(55, 80)  # Random number between 55 and 80
        self.display_level: str = ENUMDisplayLevel.MINIMUM.value

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

    def new_temp_hp(self) -> int:
        """Get the temp_hp stat of the entityInstance."""
        return self.stats["temp_hp"]

    def get_initiative(self) -> int:
        """Get the initiative stat of the entityInstance."""
        return self.stats["initiative"]

    def get_ally(self) -> bool:
        """Check if the entityInstance is an ally."""
        return self.stats["ally"]

    def get_visible(self) -> bool:
        """Check if the entityInstance is visible."""
        return self.stats["visible"]
    
    def get_death_rolls(self) -> tuple[int, int]:
        return self.stats["death_rolls_successes"], self.stats["death_rolls_fails"]    

    # Setters for base stats
    def set_hp(self, new_hp: int):
        """Update the hp stat of the entityInstance."""
        self.stats["hp"] = new_hp

    def set_temp_hp(self, new_temp_hp: int):
        """Update the temp_hp stat of the entityInstance."""
        self.stats["temp_hp"] = new_temp_hp

    def set_initiative(self, new_initiative: int):
        """Update the initiative stat of the entityInstance."""
        self.stats["initiative"] = new_initiative

    def set_ally(self, ally: bool):
        """Update whether the entityInstance is an ally."""
        self.stats["ally"] = ally

    def set_visible(self, visible: bool):
        """Update the visibility of the entityInstance."""
        self.stats["visible"] = visible

    def inc_death_rolls(self, success: bool) -> bool:
        if success == True:
            self.stats["death_rolls_successes"] += 1
        else:
            self.stats["death_rolls_fails"] += 1

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
            "healthPoint2": self.healthPoint2,
            "display_level": self.display_level
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
        entityInstance.display_level = data.get("display_level", entityInstance.display_level)

        return entityInstance