from typing import Dict, Optional

class Entity:
    def __init__(self, entityId: str, playerId: Optional[str] = None, entityType: Optional[str] = None, 
                 name: Optional[str] = None, label: Optional[str] = None, active: bool = False, 
                 imageName: Optional[str] = None, baseStats: Optional[Dict[str, int]] = None):
        """Initialize the Entity object with immutable entityId."""
        self._entityId = entityId  # Entity ID is fixed and immutable
        self.playerId: Optional[str] = playerId
        self.type: Optional[str] = entityType
        self.name: Optional[str] = name
        self.label: Optional[str] = label
        self.active: bool = active
        self.imageName: Optional[str] = imageName
        self.baseStats: Dict[str, int] = baseStats if baseStats else {'hp': 0, 'initiative': 0, 'dex': 0}

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

    # Individual methods for updating base stats
    def set_hp(self, new_hp: int):
        """Update the hp stat of the entity."""
        self.baseStats['hp'] = new_hp

    def set_initiative(self, new_initiative: int):
        """Update the initiative stat of the entity."""
        self.baseStats['initiative'] = new_initiative

    def set_dex(self, new_dex: int):
        """Update the dex stat of the entity."""
        self.baseStats['dex'] = new_dex

    # Individual methods for get base stats
    def get_hp(self,):
        """Update the hp stat of the entity."""
        return self.baseStats['hp']

    def get_initiative(self):
        """Update the initiative stat of the entity."""
        return self.baseStats['initiative']

    def get_dex(self):
        """Update the dex stat of the entity."""
        return self.baseStats['dex']     

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
            "baseStats": self.baseStats
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
            baseStats=data.get("baseStats", {"hp": 0, "initiative": 0, "dex": 0})
        )
