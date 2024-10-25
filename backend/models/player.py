from typing import Dict, Optional
from enum import Enum

class Player:
    class AcessLevel(Enum):
        PLAYER = "player"
        DUNGEONMASTER = "dungeonmaster"
        VETERAN = "veteran"
        ROOKIE = "rookie"
        SPECTATOR = "spectator"
        NONE = "none"
    
    def __init__(self, playerId: str, name: str):
        """Initialize the Player object with playerId and other fields."""
        self._playerId = playerId  # Player ID is fixed and immutable
        self.name: str = name
        self.active: bool = True
        self.accessLevel: Dict[str, str] = {}  # Access level is a dictionary of partyId to access level

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
            "accessLevel": self.accessLevel
        }

    @staticmethod
    def from_primitive(data: Dict) -> "Player":
        """Create a Player object from a dictionary."""
        player = Player(
            playerId=data.get("playerId"),
            name=data.get("name",""),
        )
        player.active = data.get("active", player.active)
        player.accessLevel = data.get("accessLevel", player.accessLevel)

        return player
