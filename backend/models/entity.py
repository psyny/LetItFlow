from typing import Dict, Optional
import copy

ExpectedStats = {
    "hp": True,
    "initiative": True,
    "dex": True,
}

class Entity:
    def __init__(self, entityId: str, playerId: Optional[str] = None, entityType: Optional[str] = None, 
                 name: Optional[str] = None, label: Optional[str] = None, active: bool = False, 
                 imageName: Optional[str] = None, stats: Optional[Dict[str, int]] = None):
        """Initialize the Entity object with immutable entityId."""
        self._entityId = entityId  # Entity ID is fixed and immutable
        self.playerId: Optional[str] = playerId
        self.type: Optional[str] = entityType
        self.name: Optional[str] = name
        self.label: Optional[str] = label
        self.active: bool = active
        self.imageName: Optional[str] = imageName
        self.stats: Dict[str, int] = stats if stats else {
            'hp': 0, 
            'initiative': 0, 
            'dex': 0,
        }

    @property
    def entityId(self) -> str:
        """Get the entityId (immutable)."""
        return self._entityId

    def set_playerId(self, new_playerId: str):
        """Update the entity's playerId."""
        self.playerId = new_playerId

    def set_type(self, new_type: str):
        """Update the entity's type."""
        self.type = new_type

    def set_name(self, new_name: str):
        """Update the entity's name."""
        self.name = new_name

    def set_label(self, new_label: str):
        """Update the entity's label."""
        self.label = new_label

    def set_active(self, is_active: bool):
        """Update the entity's active status."""
        self.active = is_active

    def set_imageName(self, new_imageName: str):
        """Update the entity's image name."""
        self.imageName = new_imageName

    # Gets
    def get_playerId(self) -> str:
        """Retrieve the entity's playerId."""
        return self.playerId

    def get_type(self) -> str:
        """Retrieve the entity's type."""
        return self.type

    def get_name(self) -> str:
        """Retrieve the entity's name."""
        return self.name

    def get_label(self) -> str:
        """Retrieve the entity's label."""
        return self.label

    def get_active(self) -> bool:
        """Retrieve the entity's active status."""
        return self.active

    def get_imageName(self) -> str:
        """Retrieve the entity's image name."""
        return self.imageName
    
    # Individual methods for updating base stats
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

    def to_primitive(self) -> Dict:
        """Convert the Entity object to a dictionary."""
        return {
            "entityId": self._entityId,
            "playerId": self.playerId,
            "type": self.type,
            "name": self.name,
            "label": self.label,
            "active": self.active,
            "imageName": self.imageName,
            "stats": copy.deepcopy(self.stats)
        }

    @staticmethod
    def from_primitive(data: Dict) -> "Entity":
        """Create an Entity object from a dictionary."""
        return Entity(
            entityId=data["entityId"],
            playerId=data.get("playerId"),
            entityType=data.get("type"),
            name=data.get("name"),
            label=data.get("label"),
            active=data.get("active", False),
            imageName=data.get("imageName"),
            stats=copy.deepcopy(data.get("stats", {"hp": 0, "initiative": 0, "dex": 0}))
        )
