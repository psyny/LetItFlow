from typing import Dict, List, Optional
import random

from backend.models.gamestate import Gamestate
from backend.models.gamestate import ENUMGamestatePhases

class PhaseInactiveController:
    def start_inactive_phase(self, gamestate: Gamestate) -> bool:
        gamestate.phase = ENUMGamestatePhases.INACTIVE.value
        gamestate.tactical = {
            'inTactical':  {},
            'initiativeScore': {},
            'randomTickets': [],
            'turnOrder': [],
            'currentTurn': ""
        }        
        self.generate_random_tickets(gamestate)
        return True