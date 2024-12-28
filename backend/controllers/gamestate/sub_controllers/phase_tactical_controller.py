from typing import Dict, List, Optional
import random

from backend.models.gamestate import Gamestate
from backend.models.gamestate import ENUMGamestatePhases

class PhaseTacticalController:
    def start_tactical_phase(self, gamestate: Gamestate) -> bool:
        gamestate.phase = ENUMGamestatePhases.TACTICAL.value
        gamestate.tactical = {
            'inTactical':  {},
            'initiativeScore': {},
            'randomTickets': [],
            'turnOrder': [],
            'currentTurn': ""
        }        
        self.generate_random_tickets(gamestate)
        return True

    def generate_initiative_score_val(self, gamestate: Gamestate, rolledScore: int, dexMod: int) -> int:
        # Generate a random ticket value (should be between 0 and 99 inclusive)
        ticketsLeft = len(gamestate.tactical['randomTickets'])
        if ticketsLeft == 0:
            return 0
        
        ticketIdx = random.randint(0, ticketsLeft - 1)
        ticketVal = gamestate.tactical['randomTickets'][ticketIdx]
        gamestate.tactical['randomTickets'].pop(ticketIdx)

        # Build the score
        score = (rolledScore * 10000) + (dexMod * 100) + (ticketVal)
        return score
    

    def generate_random_tickets(self, gamestate: Gamestate):
        gamestate.tactical['randomTickets'] = [i for i in range(100)]


    def regenerate_turn_order(self, gamestate: Gamestate):
        # Build new turn order data - only instances that have score data will be in the turn order
        sorted_score_datas = []
        for instance_id, score_data in gamestate.get_initiative_scores().items():
            sorted_score_datas.append(score_data)
                
        # Sort entity instances
        sorted_score_datas.sort(key=lambda x: (-x['currentScore'], x['untier'], -x['rolledScore']))

        # Extract the sorted instance IDs
        new_turn_order = [score_data['instanceId'] for score_data in sorted_score_datas]

        # Set the new turn order in the gamestate
        gamestate.set_turn_order(new_turn_order)

    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------

    def add_to_tactical(self, gamestate: Gamestate, instance_ids: List[str]) -> bool:
        for instance_id in instance_ids:
            gamestate.add_to_tactical(instance_id)
        return True
    
    def remove_from_tactical(self, gamestate: Gamestate, instance_ids: List[str]) -> bool:
        self.remove_from_turn_order(gamestate, instance_ids)
        
        for instance_id in instance_ids:
            gamestate.remove_from_tactical(instance_id)

        return True

    def add_to_turn_order(self, gamestate: Gamestate, instance_ids: List[str]) -> bool:
        """
        Add instances to turn order and reorder the order based on that
        """

        # We want only to add to turn order entities already in taticalmode but dont have a initiative score (so not in turn order)
        add_to_turn = set()
        currently_in_tactical = gamestate.get_in_tactical()
        intiative_scores = gamestate.get_initiative_scores()
        for instance_id in instance_ids:
            if instance_id in currently_in_tactical:
                if instance_id not in intiative_scores:
                    add_to_turn.add(instance_id)

        # Build initiative Score data for adding instance
        for instance_id in add_to_turn:
            entity_instance = gamestate.get_entity_instance(instance_id)
            entity = gamestate.get_entity(entity_instance.entityId)
            instance_init, _, _ = entity_instance.get_stat("initiative")
            entity_dex, _, _ = entity.get_stat("dex")
            score_val = self.generate_initiative_score_val(gamestate, instance_init, entity_dex)
            gamestate.set_initiative_score(instance_id, score_val, 0, score_val)

        # regenerate turn order
        self.regenerate_turn_order(gamestate)

        return True
    

    def remove_from_turn_order(self, gamestate: Gamestate, instance_ids: List[str]) -> bool:
        """
        Remove instances to turn order and reorder the order based on that
        """

        # We want only to add to turn order entities already in taticalmode but dont have a initiative score (so not in turn order)
        remove_from_turn = set()
        old_turn_order = gamestate.get_turn_order()
        currently_in_turn = set(old_turn_order)
        for instance_id in instance_ids:
            if instance_id in currently_in_turn:
                remove_from_turn.add(instance_id)
                    
        # Remove initiative Score data for adding instance        
        for instance_id in remove_from_turn:
            gamestate.remove_initiative_score(instance_id)

        # regenerate turn order
        self.regenerate_turn_order(gamestate)

        return True 


    def change_turn_order(self, gamestate: Gamestate, delaying_instance_id: str, after_instance_id: str) -> bool:
        """
        ...
        """
        # The instances should already be in the turn order
        scores = gamestate.get_initiative_scores()
        if delaying_instance_id not in scores or after_instance_id not in scores:
            return False                
        
        # We will copy the instance and add
        targetCurrentScore = scores[after_instance_id].get("currentScore", 0)
        targetCurrentUntier = scores[after_instance_id].get("untier", 0)
        delayingRolledScore = scores[delaying_instance_id].get("rolledScore", 0)
        gamestate.set_initiative_score(delaying_instance_id, targetCurrentScore, targetCurrentUntier + 1,  delayingRolledScore)

        # regenerate turn order
        self.regenerate_turn_order(gamestate)

        return True 


