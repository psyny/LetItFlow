import os
import copy 

from backend.libs.psn.appconfig.appconfig import AppConfig

from backend.libs.psn.filemanager.filemanager import FileManager
from backend.libs.psn.appconfig.appconfig import AppConfig
from backend.models.party import Party
from backend.models.entity import Entity
from backend.models.entity_instance import EntityInstance
from backend.models.player import Player
from backend.models.gamestate import Gamestate


class Repository:
    def __init__(self):
        """Initialize the Repository, setting up the folder structure from the repopath."""
        appconfig = AppConfig()
        self.persistdata = appconfig.get("persistdata")

        # Get the repopath from AppConfig and convert it into a folder structure
        self.repopath = AppConfig().get("repopath")
        self.db_structure = self.repopath.split("/")  # Break path into array for FileManager usage

        # Setup base paths for metadata, players, parties, and credentials
        self.party_metadata_path = self.db_structure + ["PartyMetadata.json"]
        self.players_folder = self.db_structure + ["player"]
        self.parties_folder = self.db_structure + ["party"]
        self.credentials_folder = self.db_structure + ["credentials"]

        # Ensure base folders exist
        FileManager.createFolders(self.db_structure)
        FileManager.createFolders(self.players_folder)
        FileManager.createFolders(self.parties_folder)
        FileManager.createFolders(self.credentials_folder)

    # --------------------------------------------------------------
    # Credential Management
    # --------------------------------------------------------------

    def save_credentials(self, playerId: str, playerKey: str):
        """Save the player's credentials to the credentials folder."""
        if self.persistdata == False:
            return True
                
        credentials_file = [f"{playerId}.json"]
        credentials_data = {
            "playerId": playerId,
            "playerKey": playerKey
        }
        FileManager.saveJsonFile(credentials_data, credentials_file, self.credentials_folder)

    def retrieve_credentials(self, playerId: str):
        """Retrieve the player's credentials from the credentials folder."""
        if self.persistdata == False:
            return None

        credentials_file = self.credentials_folder + [f"{playerId}.json"]
        return FileManager.loadJsonFile(f"{playerId}.json", self.credentials_folder)

    def delete_credentials(self, playerId: str):
        """Delete the player's credentials from the credentials folder."""
        if self.persistdata == False:
            return True
                                        
        credentials_file = self.credentials_folder + [f"{playerId}.json"]
        FileManager.remove_file(credentials_file)

    # --------------------------------------------------------------
    # Party Management
    # --------------------------------------------------------------

    def save_party(self, party: Party) -> bool:
        if self.persistdata == False:
            return True
                
        """Save a party object and cascade its sub-objects (gamestate, entities, entityInstances) to disk."""
        party_folder = self.parties_folder + [party.partyId]
        entity_folder = party_folder + ["entity"]
        entity_instance_folder = party_folder + ["entityinstance"]
        image_folder = party_folder + ["image"]

        # Ensure party folder and subfolders exist
        FileManager.createFolders(party_folder)
        FileManager.createFolders(entity_folder)
        FileManager.createFolders(entity_instance_folder)
        FileManager.createFolders(image_folder)

        # Save party data
        FileManager.saveJsonFile(party.to_primitive(), "party.json", party_folder)

        # Save gamestate data
        gamestate = party.get_gamestate()
        if gamestate:
            self.save_gamestate(gamestate, party.partyId)

        # Update PartyMetadata file
        self.update_party_metadata(party)

    def load_party(self, partyId: str) -> Party:
        """Load a party object and its sub-objects from disk."""
        if self.persistdata == False:
            return None
        
        party_folder = self.parties_folder + [partyId]
        party_data = FileManager.loadJsonFile("party.json", party_folder)
        if party_data:
            party = Party.from_primitive(party_data)

            # Load gamestate
            gamestate = self.load_gamestate(partyId)
            if gamestate:
                party.set_gamestate(gamestate)

            return party
        return None

    def delete_party(self, partyId: str) -> bool:
        if self.persistdata == False:
            return True
                
        """Delete a party and all related files (entities, entityInstances, images)."""
        party_folder = self.parties_folder + [partyId]

        # Remove the party folder and everything inside it
        FileManager.remove_folder(party_folder)

        # Update PartyMetadata
        self.remove_from_party_metadata(partyId)

    # --------------------------------------------------------------
    # Gamestate Management
    # --------------------------------------------------------------

    def save_gamestate(self, gamestate: Gamestate, partyId: str):
        """Save a gamestate object to disk, except for entities and entityInstances."""
        if self.persistdata == False:
            return True
                                        
        party_folder = self.parties_folder + [partyId]
        gamestate_file = "gamestate.json"

        # Save the main gamestate file, excluding entities and entityInstances
        FileManager.saveJsonFile(gamestate.to_primitive(), gamestate_file, party_folder)

        # Save entities and entityInstances separately
        for entity in gamestate.entities.values():
            self.save_entity(entity, partyId)
        for instance in gamestate.entityInstances.values():
            self.save_entity_instance(instance, partyId)

    def load_gamestate(self, partyId: str) -> Gamestate:
        """Load a gamestate object from disk, along with its entities and entityInstances."""
        if self.persistdata == False:
            return None
                                        
        party_folder = self.parties_folder + [partyId]
        gamestate_data = FileManager.loadJsonFile("gamestate.json", party_folder)
        if gamestate_data:
            gamestate = Gamestate.from_primitive(gamestate_data)

            # Load entities
            entity_folder = party_folder + ["entity"]
            for entity_file in FileManager.getFiles(entity_folder):
                entity_data = FileManager.loadJsonFile(entity_file, entity_folder)
                if entity_data:
                    entity = Entity.from_primitive(entity_data)
                    gamestate.add_entity(entity.entityId, entity)

            # Load entityInstances
            instance_folder = party_folder + ["entityinstance"]
            for instance_file in FileManager.getFiles(instance_folder):
                instance_data = FileManager.loadJsonFile(instance_file, instance_folder)
                if instance_data:
                    instance = EntityInstance.from_primitive(instance_data)
                    gamestate.add_entity_instance(instance)

            return gamestate
        return None

    def delete_gamestate(self, partyId: str):
        """Delete a gamestate and its associated entities and entityInstances from disk."""
        if self.persistdata == False:
            return True
                                        
        party_folder = self.parties_folder + [partyId]

        # Delete gamestate file
        FileManager.remove_file(party_folder + ["gamestate.json"])

        # Delete entities and entityInstances
        entity_folder = party_folder + ["entity"]
        entity_instance_folder = party_folder + ["entityinstance"]
        FileManager.remove_folder(entity_folder)
        FileManager.remove_folder(entity_instance_folder)

    # --------------------------------------------------------------
    # Entity Management
    # --------------------------------------------------------------

    def save_entity(self, entity: Entity, partyId: str):
        """Save an entity to disk and manage image cleanup."""
        if self.persistdata == False:
            return True
                                        
        entity_folder = self.parties_folder + [partyId, "entity"]
        image_folder = self.parties_folder + [partyId, "image"]
        
        # Ensure entity folder exists
        FileManager.createFolders(entity_folder)

        # Handle image cleanup
        existing_entity = self.load_entity(entity.entityId, partyId)
        if existing_entity and existing_entity.imageName and existing_entity.imageName != entity.imageName:
            FileManager.remove_file(image_folder + [existing_entity.imageName])

        # Save entity and image
        FileManager.saveJsonFile(entity.to_primitive(), f"{entity.entityId}.json", entity_folder)

    def load_entity(self, entityId: str, partyId: str) -> Entity:
        """Load an entity from disk."""
        if self.persistdata == False:
            return None
                                        
        entity_folder = self.parties_folder + [partyId, "entity"]
        entity_data = FileManager.loadJsonFile(f"{entityId}.json", entity_folder)
        if entity_data:
            return Entity.from_primitive(entity_data)
        return None

    def delete_entity(self, entityId: str, partyId: str):
        """Delete an entity from disk and clean up its image."""
        if self.persistdata == False:
            return True
                                        
        entity_folder = self.parties_folder + [partyId, "entity"]
        image_folder = self.parties_folder + [partyId, "image"]

        # Delete the entity file
        entity = self.load_entity(entityId, partyId)
        if entity and entity.imageName:
            FileManager.remove_file(image_folder + [entity.imageName])
        FileManager.remove_file(entity_folder + [f"{entityId}.json"])

    # --------------------------------------------------------------
    # EntityInstance Management
    # --------------------------------------------------------------

    def save_entity_instance(self, instance: EntityInstance, partyId: str):
        """Save an entityInstance to disk."""
        if self.persistdata == False:
            return True
                                        
        instance_folder = self.parties_folder + [partyId, "entityinstance"]
        FileManager.createFolders(instance_folder)
        FileManager.saveJsonFile(instance.to_primitive(), f"{instance.instanceId}.json", instance_folder)

    def load_entity_instance(self, instanceId: str, partyId: str) -> EntityInstance:
        """Load an entityInstance from disk."""
        if self.persistdata == False:
            return None
                                        
        instance_folder = self.parties_folder + [partyId, "entityinstance"]
        instance_data = FileManager.loadJsonFile(f"{instanceId}.json", instance_folder)
        if instance_data:
            return EntityInstance.from_primitive(instance_data)
        return None

    def delete_entity_instance(self, instanceId: str, partyId: str):
        """Delete an entityInstance from disk."""
        if self.persistdata == False:
            return True
                                        
        instance_folder = self.parties_folder + [partyId, "entityinstance"]
        FileManager.remove_file(instance_folder + [f"{instanceId}.json"])

    # --------------------------------------------------------------
    # Player Management
    # --------------------------------------------------------------

    def save_player(self, player: Player):
        """Save a player to disk."""
        if self.persistdata == False:
            return True
        
        FileManager.saveJsonFile(player.to_primitive(), f"{player.playerId}.json", self.players_folder)

    def load_player(self, playerId: str) -> Player:
        """Load a player from disk."""
        if self.persistdata == False:
            return None
                        
        player_data = FileManager.loadJsonFile(f"{playerId}.json", self.players_folder)
        if player_data:
            return Player.from_primitive(player_data)
        return None

    def delete_player(self, playerId: str):
        """Delete a player from disk."""
        if self.persistdata == False:
            return True
                        
        FileManager.remove_file(self.players_folder + [f"{playerId}.json"])

    # --------------------------------------------------------------
    # Party Metadata Management
    # --------------------------------------------------------------

    def update_party_metadata(self, party: Party):
        """Update PartyMetadata with the new party information."""
        metadata = FileManager.loadJsonFile("PartyMetadata.json", self.db_structure) or {}
        metadata[party.partyId] = party.name
        FileManager.saveJsonFile(metadata, "PartyMetadata.json", self.db_structure)

    def remove_from_party_metadata(self, partyId: str):
        """Remove a party from PartyMetadata."""
        metadata = FileManager.loadJsonFile("PartyMetadata.json", self.db_structure) or {}
        if partyId in metadata:
            del metadata[partyId]
        FileManager.saveJsonFile(metadata, "PartyMetadata.json", self.db_structure)