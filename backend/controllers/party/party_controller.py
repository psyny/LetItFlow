from typing import Dict, Optional
from backend.models.party import Party
from backend.modules.repository.repository import Repository

class PartyController:
    def __init__(self, repository: Repository):
        """Initialize the PartyController with the repository and a map for loaded parties."""
        self.repository: Repository = repository  # Store the repository instance
        self.parties: Dict[str, Party] = {}  # Dictionary to store loaded parties by partyId

    def load_party(self, party_id: str) -> Optional[Party]:
        """Load a party by its partyId from the repository if it's not already loaded."""
        if party_id not in self.parties:
            # Load the party from the repository
            party = self.repository.load_party(party_id)
            if party:
                self.parties[party_id] = party  # Cache the loaded party
            else:
                return None            
        return self.parties.get(party_id, None)  # Return the party, whether it's loaded or not

    def save_party(self, party: Party) -> None:
        """Save a party to both the memory (cache) and the repository."""
        self.parties[party.partyId] = party  # Update the party in memory

        self.repository.save_party(party)  # Save the party to the repository

    def delete_party(self, party_id: str) -> bool:
        """Delete a party from memory and the repository."""
        # Remove the party from memory if it exists
        if party_id in self.parties:
            del self.parties[party_id]
        
        # Delete the party from the repository
        if self.repository.load_party(party_id):
            self.repository.delete_party(party_id)
            return True
        return False

    def get_party_by_id(self, party_id: str) -> Optional[Party]:
        """Retrieve a party by its ID, loading it from the repository if necessary."""
        return self.load_party(party_id)

    def save_all_loaded_parties(self) -> None:
        """Save all currently loaded parties to the repository."""
        for party in self.parties.values():
            self.save_party(party)