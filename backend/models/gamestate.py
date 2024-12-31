from enum import Enum
from typing import Dict, List, Optional

from backend.models.entity import Entity
from backend.models.entity_instance import EntityInstance
from backend.models.vfx import Vfx

class ENUMGamestatePhases(Enum):
    INACTIVE = "inactive"
    LOBBY = "lobby"
    EXPLORATION = "exploration"
    TACTICAL = "tactical"

class Gamestate:
    def __init__(self, partyId: str, partyName: str):
        """Initialize the Gamestate object with partyId and partyName."""
        self.partyId: str = partyId
        self.partyName: str = partyName
        self.entities: Dict[str, Entity] = {}  # Map of entityId to Entity objects
        self.entityInstances: Dict[str, EntityInstance] = {}  # Map of instanceId to EntityInstance objects
        self.phase: str = 'inactive'  # Default phase is inactive

        self.inactive: Dict[str, any] = {
            'title': None
            }        
        self.lobby: Dict[str, any] = {
            'title': None
            }        
        self.tactical: Dict[str, any] = {
            'inTactical':  {},
            'initiativeScore': {},
            'randomTickets': [],
            'turnOrder': [],
            'currentTurn': ""
        }
        self.exploration: Dict[str, any] = {
            'in_exploration': {},
            'places': {},
            }
        
        self.vfxs: List[Vfx] = []  # List of active Vfx objects

    # Entity Management
    def add_entity(self, entityId: str, entity: Entity):
        """Add an Entity object to the gamestate."""
        self.entities[entityId] = entity

    def remove_entity(self, entityId: str):
        """Remove an Entity object from the gamestate."""
        if entityId in self.entities:
            del self.entities[entityId]

    def get_entity(self, entityId: str) -> Optional[Entity]:
        """Get an Entity object from the gamestate."""
        return self.entities.get(entityId, None)

    # EntityInstance Management
    def add_entity_instance(self, entityInstance: EntityInstance):
        """Add an EntityInstance object to the gamestate."""
        self.entityInstances[entityInstance.instanceId] = entityInstance

    def remove_entity_instance(self, instanceId: str):
        """Remove an EntityInstance object from the gamestate."""
        if instanceId in self.entityInstances:
            del self.entityInstances[instanceId]

    def get_entity_instance(self, instanceId: str) -> Optional[EntityInstance]:
        """Get an EntityInstance object from the gamestate."""
        return self.entityInstances.get(instanceId, None)
    
    def get_entity_instances(self) -> Dict[str, EntityInstance]:
        """Get an EntityInstance object from the gamestate."""
        return self.entityInstances

    # Phase Management
    def set_inactive_title(self, title: str):
        """Set the title of the inactive phase."""
        self.inactive['title'] = title

    # Tactical Phase Management
    def add_to_tactical(self, instanceId: str):
        """Add an EntityInstance to the tactical mode."""
        self.tactical['inTactical'][instanceId] = True

    def remove_from_tactical(self, instanceId: str):
        """Remove an EntityInstance from the tactical mode."""
        if instanceId in self.tactical['inTactical']:
            del self.tactical['inTactical']

    def get_in_tactical(self) -> Dict[str, bool]:
        return self.tactical.get('inTactical', {})
        
    def set_turn_order(self, turnOrder: List[str]):
        """Set the turn order for tactical phase."""
        self.tactical['turnOrder'] = turnOrder

    def get_turn_order(self) -> List[str]:
        return self.tactical.get('turnOrder', [])

    def set_current_turn(self, instanceId: str):
        """Set the current turn in tactical phase."""
        self.tactical['currentTurn'] = instanceId

    def get_initiative_score(self, instanceId: str):
        return self.tactical['initiativeScore'].get(instanceId,None)
    
    def get_initiative_scores(self) -> Dict:
        return self.tactical['initiativeScore']
    
    def set_initiative_score(self, instanceId: str, currentScore: int, untier: int, rolledScore: int):
        self.tactical['initiativeScore'][instanceId] = {
            "instanceId": instanceId,
            "currentScore": currentScore,
            "untier": untier,
            "rolledScore": rolledScore,
        }

    def remove_initiative_score(self, instanceId: str):
        if instanceId in self.tactical['initiativeScore']:
            del self.tactical['initiativeScore'][instanceId]

    # Exploration Phase Management
    def add_exploration_place(self, place: str, instanceId: str):
        """Map a place to an EntityInstance in exploration phase."""
        self.exploration['places'][place] = instanceId

    def remove_exploration_place(self, place: str):
        """Remove a place from exploration mapping."""
        if place in self.exploration['places']:
            del self.exploration['places'][place]

    # Lobby Phase Management
    def set_lobby_title(self, title: str):
        """Set the title for the lobby phase."""
        self.lobby['title'] = title

    # VFX Management
    def add_vfx(self, vfx: Vfx):
        """Add a Vfx object to the active Vfx list."""
        self.vfxs.append(vfx)

    def remove_vfx(self, vfxId: str):
        """Remove a Vfx object by vfxId from the active Vfx list."""
        self.vfxs = [vfx for vfx in self.vfxs if vfx.vfxId != vfxId]

    def to_primitive(self) -> Dict:
        """Convert the Gamestate object to a dictionary."""
        return {
            "partyId": self.partyId,
            "partyName": self.partyName,
            "entities": {entityId: entity.to_primitive() for entityId, entity in self.entities.items()},
            "entityInstances": {instanceId: entityInstance.to_primitive() for instanceId, entityInstance in self.entityInstances.items()},
            "phase": self.phase,
            "inactive": self.inactive,
            "tactical": self.tactical,
            "exploration": self.exploration,
            "lobby": self.lobby,
            "vfxs": [vfx.to_primitive() for vfx in self.vfxs]
        }

    @staticmethod
    def from_primitive(data: Dict) -> "Gamestate":
        """Create a Gamestate object from a dictionary."""
        gamestate = Gamestate(
            partyId=data["partyId"],
            partyName=data["partyName"]
        )
        gamestate.entities = {entityId: Entity.from_primitive(entity_data) for entityId, entity_data in data.get("entities", {}).items()}
        gamestate.entityInstances = {instanceId: EntityInstance.from_primitive(instance_data) for instanceId, instance_data in data.get("entityInstances", {}).items()}
        gamestate.phase = data.get("phase", gamestate.phase)
        gamestate.inactive = data.get("inactive", gamestate.inactive) 
        gamestate.tactical = data.get("tactical", gamestate.tactical) 
        gamestate.exploration = data.get("exploration", gamestate.exploration) 
        gamestate.lobby = data.get("lobby", gamestate.lobby) 
        gamestate.vfxs = [Vfx.from_primitive(vfx_data) for vfx_data in data.get("vfxs", [])]
        return gamestate
