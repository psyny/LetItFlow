from backend.controllers.app.app_controller import AppController
from backend.controllers.entity.entity_controller import EntityController

from backend.models.party import Party
from backend.models.player import Player
from backend.models.entity import Entity
from backend.models.gamestate import Gamestate
from backend.models.entity_instance import EntityInstance

def create_mock_party1() -> Party:
    appController = AppController()

    """Create a mock Party object with a Gamestate."""
    partyId = "party1"

    # Create the party
    party = Party(partyId=partyId, name="Mock Party 1")
    appController.partycontroller.save_party(party)

    # Create players
    player1 = Player(playerId="player1", name="Player 1 Name")
    player1.update_access_level(partyId, Player.AcessLevel.VETERAN.value)
    appController.playercontroller.save_player(player1)

    player2 = Player(playerId="player2", name="Player 2 Name")
    player2.update_access_level(partyId, Player.AcessLevel.VETERAN.value)
    appController.playercontroller.save_player(player2)

    player3 = Player(playerId="player3", name="Player 3 Name")
    player3.update_access_level(partyId, Player.AcessLevel.ROOKIE.value)
    appController.playercontroller.save_player(player3)

    player4 = Player(playerId="player4", name="Player 4 Name")
    player4.update_access_level(partyId, Player.AcessLevel.ROOKIE.value)    
    appController.playercontroller.save_player(player4)

    # Create a Gamestate for the party
    gamestate = party.get_gamestate()
    
    # Add mock entities and configure them
    entity1 = Entity(entityId="entity1")
    entity1.set_playerId(player1.playerId)
    entity1.set_type("character")
    entity1.set_name("Mock Entity 1")
    entity1.set_label("001")
    entity1.set_active(True)
    entity1.set_imageName("entity1.png")
    entity1.set_hp(100)
    entity1.set_initiative(10)
    entity1.set_dex(5)
    gamestate.add_entity(entity1.entityId, entity1)

    entity2 = Entity(entityId="entity2")
    entity2.set_playerId(player2.playerId)
    entity2.set_type("creature")
    entity2.set_name("Mock Entity 2")
    entity2.set_label("002")
    entity2.set_active(True)
    entity2.set_imageName("entity2.png")
    entity2.set_hp(80)
    entity2.set_initiative(12)
    entity2.set_dex(6)
    gamestate.add_entity(entity2.entityId, entity2)

    entity3 = Entity(entityId="entity3")
    entity3.set_playerId(player3.playerId)
    entity3.set_type("creature")
    entity3.set_name("Mock Entity 3")
    entity3.set_label("003")
    entity3.set_active(True)
    entity3.set_imageName("entity3.png")
    entity3.set_hp(85)
    entity3.set_initiative(15)
    entity3.set_dex(6)
    gamestate.add_entity(entity3.entityId, entity3)    

    entity4 = Entity(entityId="entity4")
    entity4.set_playerId(player4.playerId)
    entity4.set_type("creature")
    entity4.set_name("Mock Entity 4")
    entity4.set_label("004")
    entity4.set_active(True)
    entity4.set_imageName("entity4.png")
    entity4.set_hp(34)
    entity4.set_initiative(3)
    entity4.set_dex(3)
    gamestate.add_entity(entity4.entityId, entity4)        

    # Add mock entities instnaces
    entityController = appController.entity_controller

    entity_instance_1 = entityController.create_entity_instance_from_entity(entity1, appController.partycontroller)
    gamestate.add_entity_instance(entity_instance_1)
    
    entity_instance_2 = entityController.create_entity_instance_from_entity(entity2, appController.partycontroller)
    gamestate.add_entity_instance(entity_instance_2)

    entity_instance_3 = entityController.create_entity_instance_from_entity(entity3, appController.partycontroller)
    gamestate.add_entity_instance(entity_instance_3)    

    entity_instance_4 = entityController.create_entity_instance_from_entity(entity4, appController.partycontroller)
    gamestate.add_entity_instance(entity_instance_4)       
    
    return party