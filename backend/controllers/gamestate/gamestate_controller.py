
from backend.controllers.gamestate.sub_controllers.phase_tactical_controller import PhaseTacticalController

class GamestateController:    
    def __init__(self) -> None:
        self.phase_tatical_controller: PhaseTacticalController = PhaseTacticalController()
        pass

