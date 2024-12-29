from typing import Dict, List, Optional
from backend.models.entity import Entity
from backend.models.entity_instance import EntityInstance
from backend.models.vfx import Vfx

class GamestateView:
    def __init__(self, partyId: str, partyName: str):
        """Initialize the GamestateView object with partyId and partyName."""
        self.partyId: str = partyId
        self.partyName: str = partyName
        self.entities: Dict[str, Entity] = {}  # Map of entityId to Entity objects based on access level
        self.entityInstances: Dict[str, EntityInstance] = {}  # Map of instanceId to EntityInstance objects based on access level
        self.phase: str = 'inactive'  # Default phase is inactive
        self.inactive: Dict[str, Optional[str]] = {'title': None}
        self.tactical: Dict[str, List[str]] = {
            'inTactical': [],
            'turnOrder': [],
            'currentTurn': None
        }
        self.exploration: Dict[str, str] = {'places': {}}
        self.lobby: Dict[str, Optional[str]] = {'title': None}
        self.vfxs: List[Vfx] = []  # List of active Vfx objects

    # Entity Management
    def add_entity(self, entityId: str, entity: Entity):
        """Add an Entity object to the gamestateView."""
        self.entities[entityId] = entity

    def remove_entity(self, entityId: str):
        """Remove an Entity object from the gamestateView."""
        if entityId in self.entities:
            del self.entities[entityId]

    def get_entity(self, entityId: str) -> Optional[Entity]:
        """Get an Entity object from the gamestateView."""
        return self.entities.get(entityId, None)

    # EntityInstance Management
    def add_entity_instance(self, instanceId: str, entityInstance: EntityInstance):
        """Add an EntityInstance object to the gamestateView."""
        self.entityInstances[instanceId] = entityInstance

    def remove_entity_instance(self, instanceId: str):
        """Remove an EntityInstance object from the gamestateView."""
        if instanceId in self.entityInstances:
            del self.entityInstances[instanceId]

    def get_entity_instance(self, instanceId: str) -> Optional[EntityInstance]:
        """Get an EntityInstance object from the gamestateView."""
        return self.entityInstances.get(instanceId, None)

    # Phase Management
    def set_phase(self, new_phase: str):
        """Update the game phase."""
        self.phase = new_phase

    def set_inactive_title(self, title: str):
        """Set the title of the inactive phase."""
        self.inactive['title'] = title

    # Tactical Phase Management
    def add_to_tactical(self, instanceId: str):
        """Add an EntityInstance to the tactical mode."""
        if instanceId not in self.tactical['inTactical']:
            self.tactical['inTactical'].append(instanceId)

    def remove_from_tactical(self, instanceId: str):
        """Remove an EntityInstance from the tactical mode."""
        if instanceId in self.tactical['inTactical']:
            self.tactical['inTactical'].remove(instanceId)

    def set_turn_order(self, turnOrder: List[str]):
        """Set the turn order for tactical phase."""
        self.tactical['turnOrder'] = turnOrder

    def set_current_turn(self, instanceId: str):
        """Set the current turn in tactical phase."""
        self.tactical['currentTurn'] = instanceId

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
        """Convert the GamestateView object to a dictionary."""
        return {
            "partyId": self.partyId,
            "partyName": self.partyName,
            "entities": {entityId: entity.to_primitive() for entityId, entity in self.entities.items()},
            "entityInstances": {instanceId: entityInstance.to_primitive() for instanceId, entityInstance in self.entityInstances.items()},
            "entityInstanceViews": {instanceViewId: entityInstanceView.to_primitive() for instanceViewId, entityInstanceView in self.entityInstanceViews.items()},
            "phase": self.phase,
            "inactive": self.inactive,
            "tactical": self.tactical,
            "exploration": self.exploration,
            "lobby": self.lobby,
            "vfxs": [vfx.to_primitive() for vfx in self.vfxs]
        }

    @staticmethod
    def from_primitive(data: Dict) -> "GamestateView":
        """Create a GamestateView object from a dictionary."""
        gamestateView = GamestateView(
            partyId=data["partyId"],
            partyName=data["partyName"]
        )
        gamestateView.entities = {entityId: Entity.from_primitive(entity_data) for entityId, entity_data in data.get("entities", {}).items()}
        gamestateView.entityInstances = {instanceId: EntityInstance.from_primitive(instance_data) for instanceId, instance_data in data.get("entityInstances", {}).items()}
        gamestateView.phase = data["phase"]
        gamestateView.inactive = data["inactive"]
        gamestateView.tactical = data["tactical"]
        gamestateView.exploration = data["exploration"]
        gamestateView.lobby = data["lobby"]
        gamestateView.vfxs = [Vfx.from_primitive(vfx_data) for vfx_data in data.get("vfxs", [])]
        return gamestateView
