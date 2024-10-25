
from backend.controllers.gamestate.sub_controllers.phase_inactive_controller import PhaseInactiveController
from backend.controllers.gamestate.sub_controllers.phase_lobby_controller import PhaseLobbyController
from backend.controllers.gamestate.sub_controllers.phase_exploration_controller import PhaseExplorationController
from backend.controllers.gamestate.sub_controllers.phase_tactical_controller import PhaseTacticalController

class GamestateController:    
    def __init__(self) -> None:
        self.phase_inactive_controller: PhaseInactiveController = PhaseInactiveController()
        self.phase_lobby_controller: PhaseLobbyController = PhaseLobbyController()
        self.phase_exploration_controller: PhaseExplorationController = PhaseExplorationController()
        self.phase_tactical_controller: PhaseTacticalController = PhaseTacticalController()        
        pass

