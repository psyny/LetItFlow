from typing import Dict, List, Optional
import random

from backend.models.gamestate import Gamestate
from backend.models.gamestate import ENUMGamestatePhases

class PhaseExplorationController:
    def start_exploration_phase(self, gamestate: Gamestate) -> bool:
        gamestate.phase = ENUMGamestatePhases.EXPLORATION.value
        gamestate.tactical = {
            'inTactical':  {},
            'initiativeScore': {},
            'randomTickets': [],
            'turnOrder': [],
            'currentTurn': ""
        }        
        self.generate_random_tickets(gamestate)
        return True