from typing import Dict, Optional
from backend.models.gamestate import Gamestate

class Party:
    def __init__(self, partyId: str, name: str):
        """Initialize the Party object with immutable partyId."""
        self._partyId = partyId  # Party ID is fixed and immutable
        self.name: str = name
        self.playerColors: Dict[str, str] = {}
        self.gamestate = Gamestate(self._partyId, self.name)

    @property
    def partyId(self) -> str:
        """Get the partyId (immutable)."""
        return self._partyId

    def set_name(self, new_name: str):
        """Update the name of the party."""
        self.name = new_name

    def add_player_color(self, playerId: str, color: str):
        """Map a player's color by playerId."""
        self.playerColors[playerId] = color

    def remove_player_color(self, playerId: str):
        """Remove the player's color mapping by playerId."""
        if playerId in self.playerColors:
            del self.playerColors[playerId]

    def get_player_color(self, playerId: str) -> Optional[str]:
        """Get the player's color by playerId."""
        return self.playerColors.get(playerId, None)

    def set_gamestate(self, gamestate: Gamestate):
        """Set the reference to the gamestate object."""
        self.gamestate = gamestate

    def get_gamestate(self) -> Gamestate:
        """Get the referenced gamestate object."""
        return self.gamestate

    def to_primitive(self) -> Dict:
        """Convert the Party object to a dictionary."""
        return {
            "partyId": self._partyId,
            "name": self.name,
            "playerColors": self.playerColors,
        }

    @staticmethod
    def from_primitive(data: Dict) -> "Party":
        print(data)

        """Create a Party object from a dictionary."""
        party = Party(
            partyId=data["partyId"],
            name=data["name"],
        )
        party.playerColors = data.get("playerColors", {})
        return party
