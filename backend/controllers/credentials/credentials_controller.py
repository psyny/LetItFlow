import hashlib
import uuid

from backend.modules.repository.repository import Repository
from backend.libs.psn.filemanager.filemanager import FileManager

class CredentialsController:
    def __init__(self, repository: Repository):
        """Initialize the CredentialsController with a given Repository instance."""
        self.repository: Repository = repository  # Strongly type the repository instance
        self.credentials_map: dict[str, str] = {}  # Holds playerId -> hashed playerKey
        self.tokens: dict[str, str] = {}
        self._load_credentials()

    def _load_credentials(self):
        """Load all credentials from the Repository into memory."""
        players_folder = self.repository.credentials_folder
        player_files = FileManager.getFiles(players_folder)

        for player_file in player_files:
            # Assuming each file is named after playerId
            player_id = FileManager.getFileParts(player_file)[0]  # Get playerId from the filename
            credentials = self.repository.retrieve_credentials(player_id)
            if credentials:
                self.credentials_map[credentials["playerId"]] = credentials["playerKey"]

    def hash_key(self, playerKey: str) -> str:
        """Hash a playerKey using SHA-256."""
        return hashlib.sha256(playerKey.encode('utf-8')).hexdigest()

    def validate_credentials(self, playerId: str, playerKey: str) -> bool:
        """Validate player credentials by comparing the hashed playerKey."""

        if self.credentials_map is None or len(self.credentials_map.keys()) == 0:
            return True
                
        if playerId not in self.credentials_map:
            return False
        
        # Hash the incoming playerKey to compare with stored hash
        hashed_key = self.hash_key(playerKey)
        return hashed_key == self.credentials_map.get(playerId)

    def change_player_key(self, playerId: str, newPlayerKey: str):
        """Change the player's key, hash it, and store it in the Repository."""
        # Hash the new player key
        hashed_new_key = self.hash_key(newPlayerKey)
        
        # Update the in-memory map
        self.credentials_map[playerId] = hashed_new_key

        # Store the updated credentials back into the Repository
        self.repository.save_credentials(playerId, hashed_new_key)

    def token_generate(self, playerId: str) -> str:
        unique_id = str(uuid.uuid4())
        self.tokens[playerId] = unique_id
        return unique_id

    def token_validate(self, token: str):
        return self.tokens.get(token, None)

    def player_exists(self, playerId: str):
        """Check if player exists."""

        hasPlayerId = self.credentials_map.get(playerId)

        if hasPlayerId:
            return True
        else:
            return False