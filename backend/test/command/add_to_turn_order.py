import unittest
import copy

from backend.models.gamestate import ENUMGamestatePhases
from backend.libs.psn.appconfig.appconfig import AppConfig
from backend.controllers.app.app_controller import AppController
from backend.modules.command_executor.command_executor import CommandExecutor
from backend.models.command import Command

from backend.test.util.mock_sets import create_mock_party1

class TestCommandAddtoTurnOrder(unittest.TestCase):
    def setUp(self):
        AppConfig().initialize()
        AppConfig().set("persistdata", False)
        AppController().initialize()

    def tearDown(self):
        pass

    def test_turnorder_1(self):
        party = create_mock_party1()
        gamestate = party.get_gamestate()

        # Set phase
        gamestate.start_tactical_phase()

        # Configure initiative and gamestate        
        instanceIds = [] # also the current turn order
        init = 10
        for instanceId, instance in gamestate.get_entity_instances().items():
            instance.set_initiative(init)
            init += 1
            instanceIds.append(instanceId)

            # Add every instance to tactical mode
            gamestate.add_to_tactical(instanceId)

        # Prepare and execute the command
        command = Command(Command.Type.ADD_TO_TURN_ORDER.value)
        command.targetIds = instanceIds

        changes = CommandExecutor.execute_command(command, party.partyId)
  
        # Assert - Turn sorting worked
        turnOrder = gamestate.get_turn_order()        
        self.assertNotEqual(instanceIds, turnOrder)

        # Assert - Changes matches turn order (the turn order was empty before)
        for i, change in enumerate(changes):
            self.assertEqual(change.targetIds[0], turnOrder[i])





        

