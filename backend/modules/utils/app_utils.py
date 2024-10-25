from backend.controllers.app.app_controller import AppController
from backend.models.gamestate import Gamestate

class AppUtils:
    @staticmethod
    def get_gamestate(partyId: str) -> Gamestate:
        appController = AppController()
        party = appController.partycontroller.get_party_by_id(partyId)
        gamestate = party.get_gamestate()

        return gamestate