import copy

import unittest
from backend.libs.psn.appconfig.appconfig import AppConfig
from backend.controllers.app.app_controller import AppController
from backend.models.gamestate import Gamestate

from backend.test.util.mock_sets import create_mock_party1

class TestGamestateControllerTactical(unittest.TestCase):
    def setUp(self):
        AppConfig().initialize()
        AppConfig().set("persistdata", False)
        AppController().initialize()

    def tearDown(self):
        pass

    def _get_basic_gamestate(self):
        party = create_mock_party1()
        gamestate = party.get_gamestate()
        gamestate_controller = AppController().gamestate_controller
        gamestate_controller.phase_tactical_controller.start_tactical_phase(gamestate)

        # Configure initiative and gamestate        
        instanceIds = [] # also the current turn order
        init = 10
        for instanceId, instance in gamestate.get_entity_instances().items():
            instance.set_initiative(init)
            init += 1
            instanceIds.append(instanceId)

        # Add every instance to tactical mode        
        gamestate_controller.phase_tactical_controller.add_to_tactical(gamestate, instanceIds)

        # Add to turn order
        gamestate_controller.phase_tactical_controller.add_to_turn_order(gamestate, instanceIds)

        return party, gamestate   


    def test_turnorder_1(self):
        # Basic ADD and REMOVE from turn order

        party, gamestate = self._get_basic_gamestate()
        gamestate_controller = AppController().gamestate_controller

        # Assert - Turn sorting worked
        turnOrder = gamestate.get_turn_order()        
        self.assertEqual(len(turnOrder), 4)

        # Remove unit from turn order
        turnOrder = gamestate.get_turn_order()
        instanceId = turnOrder[2]

        # Remove from turn order
        gamestate_controller.phase_tactical_controller.remove_from_turn_order(gamestate, [instanceId,])

        # Asset - Unit was removed        
        new_turn_order = gamestate.get_turn_order()
        self.assertNotIn(instanceId, new_turn_order)

        old_turn_order = copy.deepcopy(turnOrder)
        new_turn_order_manual = copy.deepcopy(old_turn_order)
        new_turn_order_manual.remove(instanceId)        
        self.assertEqual(new_turn_order_manual, new_turn_order)


    def test_turnorder_2(self):
        # Two stage ADD

        # Prepare game state
        party = create_mock_party1()
        gamestate = party.get_gamestate()
        gamestate_controller = AppController().gamestate_controller
        gamestate_controller.phase_tactical_controller.start_tactical_phase(gamestate)

        # Configure initiative and gamestate        
        instanceIds = [] # also the current turn order
        init = 10
        for instanceId, instance in gamestate.get_entity_instances().items():
            instance.set_initiative(init)
            init += 1
            instanceIds.append(instanceId)

        # Add every instance to tactical mode        
        gamestate_controller.phase_tactical_controller.add_to_tactical(gamestate, instanceIds)

        # Add one by one, in any order
        gamestate_controller.phase_tactical_controller.add_to_turn_order(gamestate, [instanceIds[2],])
        gamestate_controller.phase_tactical_controller.add_to_turn_order(gamestate, [instanceIds[3],])
        gamestate_controller.phase_tactical_controller.add_to_turn_order(gamestate, [instanceIds[0],])
        gamestate_controller.phase_tactical_controller.add_to_turn_order(gamestate, [instanceIds[1],])


        # Assert - Turn sorting worked
        turn_order = gamestate.get_turn_order()  
        turn_order_manual = [instanceIds[3],instanceIds[2],instanceIds[1],instanceIds[0],]
        self.assertEqual(turn_order_manual, turn_order)
    

    def test_turnorder_3(self):
        # DELAY

        party, gamestate = self._get_basic_gamestate()
        gamestate_controller = AppController().gamestate_controller

        # Delay turn
        original_turn_order = copy.deepcopy(gamestate.get_turn_order())
        gamestate_controller.phase_tactical_controller.change_turn_order(gamestate, original_turn_order[0], original_turn_order[3])

        # Asserts
        new_turn_order = gamestate.get_turn_order()
        new_turn_order_manual = [ original_turn_order[1], original_turn_order[2], original_turn_order[3], original_turn_order[0],]
        self.assertEqual(new_turn_order, new_turn_order_manual)
        
        # Delay turn - Again
        gamestate_controller.phase_tactical_controller.change_turn_order(gamestate, original_turn_order[1], original_turn_order[3])

        # Asserts
        new_turn_order = gamestate.get_turn_order()
        new_turn_order_manual = [ original_turn_order[2], original_turn_order[3], original_turn_order[0], original_turn_order[1],]
        self.assertEqual(new_turn_order, new_turn_order_manual)
        



    