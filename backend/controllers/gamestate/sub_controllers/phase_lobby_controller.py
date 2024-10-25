from typing import Dict, List, Optional
import random

from backend.models.gamestate import Gamestate
from backend.models.gamestate import ENUMGamestatePhases

class PhaseLobbyController:
    def start_lobby_phase(self, gamestate: Gamestate) -> bool:
        gamestate.phase = ENUMGamestatePhases.LOBBY.value
        gamestate.lobby = {
            'title':  ''
        }     
        return True