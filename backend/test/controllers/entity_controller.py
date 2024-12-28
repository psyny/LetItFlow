import copy

import unittest
from backend.libs.psn.appconfig.appconfig import AppConfig
from backend.controllers.app.app_controller import AppController
from backend.controllers.entity.entity_controller import EntityController
from backend.models.gamestate import Gamestate
from backend.models.entity_instance import ENUMDisplayLevel

from backend.test.util.mock_sets import create_mock_party1

class TestEntityController(unittest.TestCase):
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

    def test_get_instance_from_entity(self):
        party = create_mock_party1()
        gamestate = party.get_gamestate()
        gamestate_controller = AppController().gamestate_controller
        entity_controller = AppController().entity_controller

        instanceIds = [] # also the current turn order
        entity = None
        for _, instance in gamestate.get_entity_instances().items():
            entity = gamestate.get_entity(instance.entityId)
            break

        instance = entity_controller.create_entity_instance_from_entity(entity, party.partyId)

        instance_hp, _, _ = instance.get_stat("hp")
        entity_hp, _, _ = entity.get_stat("hp")
        self.assertEqual(instance_hp, entity_hp)

        instance_initiative, _, _ = instance.get_stat("initiative")
        entity_initiative, _, _ = entity.get_stat("initiative")
        self.assertEqual(instance_initiative, entity_initiative)

        instance_hp2, _, _ = instance.set_stat("hp", instance_hp + 1)
        self.assertNotEqual(instance_hp, instance_hp2)

        instance_hp3, _, _ = instance.add_stat("hp", 1)
        self.assertNotEqual(instance_hp, instance_hp3)

    def test_display_level(self):
        party = create_mock_party1()
        gamestate = party.get_gamestate()
        gamestate_controller = AppController().gamestate_controller
        entity_controller = AppController().entity_controller

        entity = None
        for _, instance in gamestate.get_entity_instances().items():
            entity = gamestate.get_entity(instance.entityId)
            break

        instance = entity_controller.create_entity_instance_from_entity(entity, party.partyId)

        # Display Level: Complete
        instance_complete = entity_controller.get_instance_by_display_level(instance, ENUMDisplayLevel.COMPLETE.value, party.partyId)
        self.assertEqual(instance.get_stat("hp")[0], instance_complete.get_stat("hp")[0])
        self.assertEqual(instance.get_stat("initiative")[0], instance_complete.get_stat("initiative")[0])
        self.assertEqual(instance.get_label(), instance_complete.get_label())

        # Display Level: Tactical
        instance_tactical = entity_controller.get_instance_by_display_level(instance, ENUMDisplayLevel.TACTICAL.value, party.partyId)
        self.assertEqual(instance.get_stat("hp")[0], instance_tactical.get_stat("hp")[0])
        self.assertEqual(instance.get_stat("initiative")[0], instance_tactical.get_stat("initiative")[0])
        self.assertEqual(instance.get_label(), instance_tactical.get_label())

        # Display Level: Immersive
        instance_immersive1 = entity_controller.get_instance_by_display_level(instance, ENUMDisplayLevel.IMMERSIVE.value, party.partyId)
        self.assertNotEqual(instance.get_stat("hp")[0], instance_immersive1.get_stat("hp")[0])
        self.assertEqual(instance.get_stat("initiative")[0], instance_immersive1.get_stat("initiative")[0])
        self.assertEqual(instance.get_label(), instance_immersive1.get_label())

        # Display Level: Minimum
        instance_minimum = entity_controller.get_instance_by_display_level(instance, ENUMDisplayLevel.MINIMUM.value, party.partyId)
        self.assertNotEqual(instance.get_stat("hp")[0], instance_minimum.get_stat("hp")[0])

        # Display Level: Incognito
        instance_incognito = entity_controller.get_instance_by_display_level(instance, ENUMDisplayLevel.INCOGNITO.value, party.partyId)
        self.assertNotEqual(instance.get_stat("hp")[0], instance_incognito.get_stat("hp")[0])
        self.assertNotEqual(instance.get_label(), instance_incognito.get_label())

        # Display Level: Immersive, part 2
        instance_immersive1 = entity_controller.get_instance_by_display_level(instance, ENUMDisplayLevel.IMMERSIVE.value, party.partyId)
        self.assertEqual(instance_immersive1.get_stat("hp")[0], 4)             
        instance.add_stat("hp", -1)
        instance_immersive2 = entity_controller.get_instance_by_display_level(instance, ENUMDisplayLevel.IMMERSIVE.value, party.partyId)
        self.assertEqual(instance_immersive2.get_stat("hp")[0], 3)     

        instance.set_stat("hp", instance.get_stat("hp")[0] * 0.5)
        instance_immersive3 = entity_controller.get_instance_by_display_level(instance, ENUMDisplayLevel.IMMERSIVE.value, party.partyId)
        self.assertEqual(instance_immersive3.get_stat("hp")[0], 2)    

        instance.set_stat("hp", 2)
        instance_immersive4 = entity_controller.get_instance_by_display_level(instance, ENUMDisplayLevel.IMMERSIVE.value, party.partyId)
        self.assertEqual(instance_immersive4.get_stat("hp")[0], 1)

        instance.set_stat("hp", 0)
        instance_immersive5 = entity_controller.get_instance_by_display_level(instance, ENUMDisplayLevel.IMMERSIVE.value, party.partyId)
        self.assertEqual(instance_immersive5.get_stat("hp")[0], 0)
