from typing import Dict, List, Optional
import random

from backend.models.gamestate import Gamestate
from backend.models.gamestate import ENUMGamestatePhases

class PhaseExplorationController:
    def start_exploration_phase(self, gamestate: Gamestate) -> bool:
        gamestate.phase = ENUMGamestatePhases.EXPLORATION.value
        return True
    
    # ----------------------------------------
    # Add/remove places
    # ----------------------------------------    

    def place_exists(self, gamestate: Gamestate, place_name: str) -> bool:
        if len(place_name) == 0:
            return True
        return place_name in gamestate.exploration['places']
    
    def add_place(self, gamestate: Gamestate, place_name: str) -> bool:
        if len(place_name) == 0:
            return False        
        if place_name in gamestate.exploration['places']:
            return False
        
        gamestate.exploration['places'][place_name] = {}
        return True
        
    def remove_place(self, gamestate: Gamestate, place_name: str) -> List[str]:
        if place_name in gamestate.exploration['places']:
            instance_ids = list(gamestate.exploration['places'][place_name].keys())
            for instance_id in instance_ids:
                # Move everyone to empty place 
                self.remove_from_place(gamestate, instance_id)
                
            # Remove place
            del gamestate.exploration['places'][place_name]    
            return True
        return False

    # ----------------------------------------
    # Add/remove instance to exploration
    # ----------------------------------------
    
    def is_in_exploration(self, gamestate: Gamestate, instance_id: str) -> bool:
        return instance_id in gamestate.exploration['in_exploration']
    
    def add_to_exploration(self, gamestate: Gamestate, instance_id: str) -> bool:
        if not self.is_in_exploration(gamestate, instance_id):
            gamestate.exploration['in_exploration'][instance_id] = ''
            return True
        return False

    def remove_from_exploration(self, gamestate: Gamestate, instance_id: str) -> bool:
        if self.is_in_exploration(gamestate, instance_id):
            self.remove_from_place(gamestate, instance_id)
            del gamestate.exploration['in_exploration'][instance_id]
            return True
        return False
    
    # ----------------------------------------
    # Add/remove instance to places
    # ----------------------------------------

    def is_in_place(self, gamestate: Gamestate, instance_id: str, place_name: str) -> bool:
        if not self.is_in_exploration(gamestate, instance_id):
            return False
        if not self.place_exists(gamestate, place_name):
            return False
        
        if gamestate.exploration['in_exploration'][instance_id] == place_name:
            return True
        
        return False

    def add_to_place(self, gamestate: Gamestate, instance_id: str, place_name: str) -> bool:
        if not self.is_in_exploration(gamestate, instance_id):
            return False
        if not self.place_exists(gamestate, place_name):
            return False
        
        current_place = gamestate.exploration['in_exploration'][instance_id]

        if current_place == place_name:
            return False

        if len(current_place) > 0: 
            self.remove_from_place(gamestate, instance_id)           
        
        gamestate.exploration['in_exploration'][instance_id] = place_name

        if len(place_name) > 0:
            gamestate.exploration['places'][place_name][instance_id] = True

        return True

    def remove_from_place(self, gamestate: Gamestate, instance_id: str) -> bool:
        if not self.is_in_exploration(gamestate, instance_id):
            return False
        
        current_place = gamestate.exploration['in_exploration'][instance_id]

        if len(current_place) == 0:
            return False
        
        if not self.place_exists(gamestate, current_place):
            return False        
        
        del gamestate.exploration['places'][current_place][instance_id]
        gamestate.exploration['in_exploration'][instance_id] = ''
        return True