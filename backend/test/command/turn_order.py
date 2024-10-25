import unittest
import copy

from backend.models.gamestate import ENUMGamestatePhases
from backend.libs.psn.appconfig.appconfig import AppConfig
from backend.controllers.app.app_controller import AppController
from backend.modules.command_executor.command_executor import CommandExecutor
from backend.models.command import Command

from backend.test.util.mock_sets import create_mock_party1

class TestCommandTurnOrder(unittest.TestCase):
    def setUp(self):
        AppConfig().initialize()
        AppConfig().set("persistdata", False)
        AppController().initialize()

    def tearDown(self):
        pass

    def test_command_1(self):
        pass