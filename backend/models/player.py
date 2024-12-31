from typing import Dict, Optional
from enum import Enum

class Player:
    class AcessLevel(Enum):
        ADMIN = "admin"
        DUNGEONMASTER = "dungeonmaster"
        VETERAN = "veteran"
        ROOKIE = "rookie"
        SPECTATOR = "spectator"
        NONE = "none"

    access_level_level = {
        AcessLevel.ADMIN.value: 100,
        AcessLevel.DUNGEONMASTER.value: 90,
        AcessLevel.VETERAN.value: 30,
        AcessLevel.ROOKIE.value: 20,
        AcessLevel.SPECTATOR.value: 10,
        AcessLevel.NONE.value: 0,
    }
   
    def __init__(self, playerId: str, name: str):
        """Initialize the Player object with playerId and other fields."""
        self._playerId = playerId  # Player ID is fixed and immutable
        self.name: str = name
        self.active: bool = True
        self.accessLevelDefault: str = "spectator"
        self.accessLevel: Dict[str, str] = {}  # Access level is a dictionary of partyId to access level

    def accessLevelCompare(baseReference: str, comparingReference: str):
        baseReferenceLevel = Player.access_level_level.get(baseReference)
        if baseReferenceLevel == None:
            return None
        comparingReferenceLevel = Player.access_level_level.get(comparingReference)
        if comparingReferenceLevel == None:
            return None
        return comparingReferenceLevel - baseReferenceLevel

    @property
    def playerId(self) -> str:
        """Get the playerId (immutable)."""
        return self._playerId

    def update_access_level(self, partyId: str, access_level: str):
        """Update the player's access level for a specific party."""
        self.accessLevel[partyId] = str(access_level)

    def remove_access_level(self, partyId: str):
        """Remove the player's access level for a specific party."""
        if partyId in self.accessLevel:
            del self.accessLevel[partyId]

    def get_access_level(self, partyId: str) -> str:
        """Get the player's access level for a specific party."""
        access_level = self.accessLevel.get(partyId, self.AcessLevel.NONE)
        if access_level == self.AcessLevel.NONE:
            access_level = self.AcessLevel.NONE.value
        return access_level
    
    def to_primitive(self) -> Dict:
        """Convert the Player object to a dictionary."""
        return {
            "playerId": self._playerId,
            "name": self.name,
            "active": self.active,
            "accessLevelDefault": self.accessLevelDefault,
            "accessLevel": self.accessLevel,
        }

    @staticmethod
    def from_primitive(data: Dict) -> "Player":
        """Create a Player object from a dictionary."""
        player = Player(
            playerId=data.get("playerId"),
            name=data.get("name",""),
        )
        player.active = data.get("active", player.active)
        player.accessLevelDefault = data.get("accessLevelDefault", player.accessLevelDefault)
        player.accessLevel = data.get("accessLevel", player.accessLevel)

        return player
