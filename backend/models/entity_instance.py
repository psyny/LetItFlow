from enum import Enum
import random
from typing import Dict, List, Optional
import copy

class ENUMDisplayLevel(Enum):
    COMPLETE = "complete" # Full resource and stats sheet disclosure
    TACTICAL = "tactical" # Numerical HP values, name, conditions
    IMMERSIVE = "immersive" # Categorical HP values, name, conditions        
    MINIMUM = "minimum" # No HP. Just name and conditions
    INCOGNITO = "incognito" # No HP, no picture, no name/label, just the existance

ExpectedStats = {
    "hp": True,
    "temp_hp": True,
    "initiative": True,
    "death_rolls_successes": True,
    "death_rolls_fails": True,
    "group": True,
    "visible": True,
    "perception": True,
    "insight": True,
    "investigaton": True,
}

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
            'group': 0,
            'visible': 1,
            'perception': 0,
            'insight': 0,
            'investigaton': 0,
        }
        self.conditions: List[Dict] = []

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
    def set_stat(self, statName: str, value: any) -> tuple[any, bool, bool]:
        """Set Any Stat, returns curr value, exptected, and success state"""
        expected = ExpectedStats.get(statName, False)
        
        self.stats[statName] = value
        return value, expected, True

    def add_stat(self, statName: str, value: any) -> tuple[any, bool, bool]:
        """Add to a stat, returns new value, exptected, and success state"""
        expected = ExpectedStats.get(statName, False)

        currValue = self.stats.get(statName, 0)
        newValue = currValue

        try:
            newValue += value
        except TypeError:
            return 0, expected, False
        
        self.stats[statName] = newValue
        return newValue, expected, True
    
    def get_stat(self, statName: str) -> tuple[any, bool, bool]:
        """Get Any Stat, returns curr value, exptected, and existing state"""
        expected = ExpectedStats.get(statName, False)

        value = self.stats.get(statName)
        if value:
            exists = True
        else:
            exists = False
            value = 0

        return value, expected, exists

    # Methods to manage conditions
    def add_condition(self, condition: Dict):
        """Add a condition to the entityInstance."""
        self.conditions.append(condition)

    def remove_condition(self, conditionId: str):
        """Remove a condition from the entityInstance by conditionId."""
        self.conditions = [
            cond for cond in self.conditions if cond["conditionId"] != conditionId
        ]

    # Get Display Level
    def get_displayLevel(self) -> ENUMDisplayLevel:
        return self.display_level

    # Get Label
    def get_label(self) -> str:
        return self.label

    # Convert to a primitive dictionary
    def to_primitive(self) -> Dict:
        """Convert the EntityInstance object to a dictionary."""
        return {
            "instanceId": self._instanceId,
            "entityId": self._entityId,
            "playerId": self.playerId,
            "label": self.label,
            "stats": copy.deepcopy(self.stats),
            "conditions": copy.deepcopy(self.conditions),
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
        entityInstance.stats = copy.deepcopy(data.get("stats", entityInstance.stats))
        entityInstance.conditions = copy.deepcopy(data.get("conditions", entityInstance.conditions))
        entityInstance.seed = data.get("seed", entityInstance.seed) 
        entityInstance.healthPoint1 = data.get("healthPoint1", entityInstance.healthPoint1)
        entityInstance.healthPoint2 = data.get("healthPoint2", entityInstance.healthPoint2)
        entityInstance.display_level = data.get("display_level", entityInstance.display_level)

        return entityInstance