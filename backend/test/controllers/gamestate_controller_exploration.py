import copy

import unittest
from backend.libs.psn.appconfig.appconfig import AppConfig
from backend.controllers.app.app_controller import AppController
from backend.models.gamestate import Gamestate

from backend.test.util.mock_sets import create_mock_party1

class TestGamestateControllerExploration(unittest.TestCase):
    def setUp(self):
        AppConfig().initialize()
        AppConfig().set("persistdata", False)
        AppController().initialize()

    def tearDown(self):
        pass

    def _get_basic_gamestate(self):
        # Setup Exploration Phase
        party = create_mock_party1()
        gamestate = party.get_gamestate()
        gamestate_controller = AppController().gamestate_controller
        gamestate_controller.phase_exploration_controller.start_exploration_phase(gamestate)

        return party, gamestate       

    def test_add_to_exploration(self):
        gamestate_controller = AppController().gamestate_controller

        # Setup Exploration Phase
        party, gamestate = self._get_basic_gamestate()

        # Add entitiy to exploration
        instances_ids = list(gamestate.get_entity_instances().keys())
        instance_id = instances_ids[0]
        gamestate_controller.phase_exploration_controller.add_to_exploration(gamestate, instance_id)

        # Assert
        self.assertTrue(gamestate_controller.phase_exploration_controller.is_in_exploration(gamestate, instance_id))

        # Test remove too
        gamestate_controller.phase_exploration_controller.remove_from_exploration(gamestate, instance_id)

        # Assert        
        self.assertFalse(gamestate_controller.phase_exploration_controller.is_in_exploration(gamestate, instance_id))

    def test_add_place(self):
        gamestate_controller = AppController().gamestate_controller

        # Setup Exploration Phase
        party, gamestate = self._get_basic_gamestate()

        # Place
        gamestate_controller.phase_exploration_controller.add_place(gamestate, "place_1")

        # Assert
        self.assertTrue(gamestate_controller.phase_exploration_controller.place_exists(gamestate, "place_1"))

        # Test remove too
        gamestate_controller.phase_exploration_controller.remove_place(gamestate, "place_1")

        # Assert
        self.assertFalse(gamestate_controller.phase_exploration_controller.place_exists(gamestate, "place_1"))

    def test_add_to_place(self):
        gamestate_controller = AppController().gamestate_controller

        # Setup Exploration Phase
        party, gamestate = self._get_basic_gamestate()

        # Add entitiy to exploration
        instances_ids = list(gamestate.get_entity_instances().keys())
        instance_id = instances_ids[0]
        gamestate_controller.phase_exploration_controller.add_to_exploration(gamestate, instance_id)

        # Add places
        place_name_1 = "place_1"
        gamestate_controller.phase_exploration_controller.add_place(gamestate, place_name_1)
        place_name_2 = "place_2"
        gamestate_controller.phase_exploration_controller.add_place(gamestate, place_name_2)

        # Add entity to place 1
        gamestate_controller.phase_exploration_controller.add_to_place(gamestate, instance_id, place_name_1)

        # Assert
        self.assertTrue(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, place_name_1))
        self.assertFalse(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, place_name_2))
        self.assertFalse(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, ''))

        # Add entity to place 2
        gamestate_controller.phase_exploration_controller.add_to_place(gamestate, instance_id, place_name_2)

        # Assert
        self.assertTrue(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, place_name_2))
        self.assertFalse(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, place_name_1))
        self.assertFalse(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, ''))

        # Remove entity from place
        gamestate_controller.phase_exploration_controller.remove_from_place(gamestate, instance_id)

        # Assert
        self.assertTrue(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, ''))
        self.assertFalse(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, place_name_1))
        self.assertFalse(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, place_name_2))
        
        # Add entity to place 2 and remove place
        gamestate_controller.phase_exploration_controller.add_to_place(gamestate, instance_id, place_name_2)
        gamestate_controller.phase_exploration_controller.remove_place(gamestate, place_name_2)

        # Assert        
        self.assertTrue(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, ''))
        self.assertFalse(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, place_name_1))
        self.assertFalse(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, place_name_2))

        # Add entity to place 1 and remove from exploration
        gamestate_controller.phase_exploration_controller.add_to_place(gamestate, instance_id, place_name_1)
        gamestate_controller.phase_exploration_controller.remove_from_exploration(gamestate, instance_id)        

        # Assert        
        self.assertFalse(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, ''))
        self.assertFalse(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, place_name_1))
        self.assertFalse(gamestate_controller.phase_exploration_controller.is_in_place(gamestate, instance_id, place_name_2))        