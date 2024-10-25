from typing import Dict, Optional
from backend.modules.repository.repository import Repository
from backend.models.entity import Entity
from backend.models.entity_instance import EntityInstance
from backend.models.entity_instance_view import EntityInstanceView
from backend.controllers.party.party_controller import PartyController


class EntityController:
    def __init__(self, repository: Repository, party_controller: PartyController):
        """Initialize the PartyController with the repository and a map for loaded parties."""
        self.repository: Repository = repository  # Store the repository instance
        self.party_controller: PartyController = party_controller

        self.last_entity_id: Dict[str, int] = {}
        self.last_entity_instance_id: Dict[str, int] = {}

    def get_next_entity_id(self, party_id: str) -> str:
        nextid = self.last_entity_id.get(party_id, -1)
        nextid += 1
        self.last_entity_id[party_id] = nextid

        return str(nextid)
    
    def get_next_entity_instance_id(self, party_id: str) -> str:
        nextid = self.last_entity_instance_id.get(party_id, -1)
        nextid += 1
        self.last_entity_instance_id[party_id] = nextid

        return str(nextid)            

    def create_entity_instance_from_entity(self, entity: Entity, partyId: str) -> EntityInstance:
        instance_id = self.get_next_entity_instance_id(partyId)
        instance = EntityInstance(instance_id, entity.entityId)

        instance.set_hp(entity.baseStats["hp"])
        instance.label = entity.label
        instance.set_initiative(entity.get_initiative())

        return instance
    
    def get_entity_from_entity_instance_id(self, party_id: str, instance_id: str) -> Entity:
        party = self.party_controller.get_party_by_id(party_id)
        gamestate = party.get_gamestate()
        entity_instance = gamestate.get_entity_instance(instance_id)
        entity = gamestate.get_entity(entity_instance.entityId)
        return entity
