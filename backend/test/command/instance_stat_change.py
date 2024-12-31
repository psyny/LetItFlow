import copy

import unittest
from backend.libs.psn.appconfig.appconfig import AppConfig
from backend.controllers.app.app_controller import AppController
from backend.modules.command_executor.basic_commands.instance_stat_change import instance_stat_change
from backend.models.gamestate import Gamestate
from backend.models.command import Command

from backend.test.util.mock_sets import create_mock_party1

class TestInstanceStatChange(unittest.TestCase):
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
    
    def test_instance_stat_change_add(self):
        gamestate_controller = AppController().gamestate_controller

        # Setup Exploration Phase
        party, gamestate = self._get_basic_gamestate()

        # Get Entity
        targetInstance = None
        for _, instance in gamestate.get_entity_instances().items():
            targetInstance = instance
            break
            
        # Build command 1
        command = Command(Command.Type.INSTANCE_CHANGE_STAT)
        command.targetIds.append(targetInstance.instanceId)

        command.actionData["type"] = "add"
        command.actionData["stat"] = "hp"
        command.actionData["value"] = -10

        # Values 1
        hp1, _, _ = targetInstance.get_stat("hp")
        changes = instance_stat_change(command, party.partyId)
        hp2, _, _ = targetInstance.get_stat("hp")

        self.assertEqual(1, len(changes))
        self.assertEqual(changes[0].targetIds[0], targetInstance.instanceId)
        self.assertNotEqual(hp1, hp2)

        # Build command 2 - If we add too much HP, the command should cap the max HP to the HP value of base entity
        command = Command(Command.Type.INSTANCE_CHANGE_STAT)
        command.targetIds.append(targetInstance.instanceId)

        command.actionData["type"] = "add"
        command.actionData["stat"] = "hp"
        command.actionData["value"] = 100000

        # Values 2
        changes = instance_stat_change(command, party.partyId)
        hp3, _, _ = targetInstance.get_stat("hp")

        self.assertEqual(hp1, hp3)
        self.assertNotEqual(hp2, hp3)