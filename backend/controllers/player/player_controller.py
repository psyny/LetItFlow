from typing import Dict, Optional
from backend.models.player import Player
from backend.modules.repository.repository import Repository
from backend.libs.psn.filemanager.filemanager import FileManager

class PlayerController:
    def __init__(self, repository: Repository):
        """Initialize the PlayerController, load all players from the repository into memory."""
        self.repository: Repository = repository  # Store the repository instance
        self.players: Dict[str, Player] = {}  # Map from playerId to Player object
        self._load_players_from_repo()

    def _load_players_from_repo(self) -> None:
        """Load all players from the repository into memory."""
        player_files = FileManager.getFiles(self.repository.players_folder, "json")  # Get all player JSON files
        for player_file in player_files:
            player_id = player_file.split(".")[0]  # Extract playerId from the file name
            player_data: Optional[Player] = self.repository.load_player(player_id)
            if player_data:
                self.players[player_id] = player_data

    def save_player(self, player: Player) -> None:
        """Save the player info to memory and update the repository."""
        self.players[player.playerId] = player  # Update the player in memory
        self.repository.save_player(player)  # Save the player to the repository

    def get_player_by_id(self, player_id: str) -> Optional[Player]:
        """Retrieve a player by its ID."""
        return self.players.get(player_id, None)  # Return the player object or None if not found

    def delete_player(self, player_id: str) -> bool:
        """Delete a player from memory and the repository."""
        # Check if player exists in memory
        if player_id in self.players:
            del self.players[player_id]  # Remove from memory

        # Delete the player from the repository
        if self.repository.load_player(player_id):
            self.repository.delete_player(player_id)  # Delete from the repository
            return True

        return False
