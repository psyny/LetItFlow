import unittest

from backend.libs.psn.appconfig.appconfig import AppConfig
from backend.controllers.app.app_controller import AppController
from backend.test.util.mock_sets import create_mock_party1
from backend.models.party import Party
from backend.models.player import Player
from backend.models.entity import Entity
from backend.models.gamestate import Gamestate

class TestCoreReposityFunctions(unittest.TestCase):
    def setUp(self):
        AppConfig().initialize()
        AppConfig().set("repopath", "db_test")             
        AppConfig().set("persistdata", True)      
        AppController().initialize()

    def tearDown(self):
        pass

    def test_repository(self):
        """Test the save and load functions of the Repository."""
        # Initialize AppController and get Repository instance
        app_controller = AppController()
        repository = app_controller.repository

        # Create mock party and players
        mock_party = create_mock_party1()

        # Save the mock party (including gamestate)
        print("Saving party with gamestate...")
        repository.save_party(mock_party)

        # Load the saved party
        print("Loading party...")
        loaded_party = repository.load_party(mock_party.partyId)
        print(f"Loaded party: {loaded_party.to_primitive()}")

        # Load the saved players
        print("Loading players...")
        loaded_player1 = repository.load_player("player1")
        loaded_player2 = repository.load_player("player2")
        print(f"Loaded player1: {loaded_player1.to_primitive()}")
        print(f"Loaded player2: {loaded_player2.to_primitive()}")

        # Load the saved gamestate
        print("Loading gamestate...")
        loaded_gamestate = loaded_party.get_gamestate()
        print(f"Loaded gamestate: {loaded_gamestate.to_primitive()}")