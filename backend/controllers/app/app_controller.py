from backend.modules.repository.repository import Repository
from backend.controllers.credentials.credentials_controller import CredentialsController
from backend.controllers.player.player_controller import PlayerController
from backend.controllers.party.party_controller import PartyController
from backend.controllers.entity.entity_controller import EntityController
from backend.controllers.gamestate.gamestate_controller import GamestateController

class AppController:
    _instance = None
    repository = None  # Class field to hold the Repository instance
    # You can add other fields for other components here
    other_component = None

    def __new__(cls):
        """Ensure AppController is a singleton."""
        if cls._instance is None:
            cls._instance = super(AppController, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        """Initialize the AppController's components."""
        self.repository: Repository = Repository()  # Set repository as a class-level field
        self.credentialsController: CredentialsController = CredentialsController(self.repository)
        self.playercontroller: PlayerController = PlayerController(self.repository)
        self.partycontroller: PartyController = PartyController(self.repository)
        self.entity_controller: EntityController = EntityController(self.repository, self.partycontroller)
        self.gamestate_controller: GamestateController = GamestateController()

        


