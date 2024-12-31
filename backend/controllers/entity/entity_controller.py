from typing import Dict, Optional
from backend.modules.repository.repository import Repository
from backend.models.entity import Entity
from backend.models.entity_instance import EntityInstance, ENUMDisplayLevel
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

    def get_instance_by_display_level(self, entity_instance: EntityInstance, display_level: str, party_id: str) -> EntityInstance:
        party = self.party_controller.get_party_by_id(party_id)
        gamestate = party.get_gamestate()
        entity = gamestate.get_entity(entity_instance.entityId)

        primitive = entity_instance.to_primitive()
        newInstance = EntityInstance.from_primitive(primitive)
        newInstance.display_level = display_level

        if display_level == ENUMDisplayLevel.COMPLETE.value:
            return newInstance
        
        if display_level == ENUMDisplayLevel.TACTICAL.value:
            return newInstance
        
        if display_level == ENUMDisplayLevel.IMMERSIVE.value:
            hpPerc = 0
            hpCat = 0

            if newInstance.stats["hp"] == entity.stats["hp"]:
                hpCat = 4

            elif newInstance.stats["hp"] > 0:
                hpPerc = 100 * newInstance.stats["hp"] / entity.stats["hp"]

                if hpPerc <= entity_instance.healthPoint1:
                    hpCat = 1
                elif hpPerc <= entity_instance.healthPoint2:
                    hpCat = 2
                else:
                    hpCat = 3

            newInstance.stats["hp"] = hpCat
            newInstance.healthPoint1 = 0
            newInstance.healthPoint2 = 0

            return newInstance

        if display_level == ENUMDisplayLevel.MINIMUM.value:
            if newInstance.stats["hp"] > 0:
                newInstance.stats["hp"] = 1
            else:
                newInstance.stats["hp"] = 0

            return newInstance

        if display_level == ENUMDisplayLevel.INCOGNITO.value:
            if newInstance.stats["hp"] > 0:
                newInstance.stats["hp"] = 1
            else:
                newInstance.stats["hp"] = 0
            newInstance.label = ""

            return newInstance

    def create_entity_instance_from_entity(self, entity: Entity, party_id: str) -> EntityInstance:
        instance_id = self.get_next_entity_instance_id(party_id)
        instance = EntityInstance(instance_id, entity.entityId)

        instance.stats["hp"] = entity.stats["hp"]
        instance.stats["initiative"] = entity.stats["initiative"]
        instance.label = entity.label

        return instance
    
    def get_entity_from_entity_instance_id(self, party_id: str, instance_id: str) -> Entity:
        party = self.party_controller.get_party_by_id(party_id)
        gamestate = party.get_gamestate()
        entity_instance = gamestate.get_entity_instance(instance_id)
        entity = gamestate.get_entity(entity_instance.entityId)

        return entity

