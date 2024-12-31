import unittest

from backend.test.repository.core import TestCoreReposityFunctions
from backend.test.controllers.gamestate_controller_tactical import TestGamestateControllerTactical
from backend.test.controllers.gamestate_controller_exploration import TestGamestateControllerExploration
from backend.test.controllers.entity_controller import TestEntityController

from backend.test.command.turn_order import TestCommandTurnOrder
from backend.test.command.instance_stat_change import TestInstanceStatChange

if __name__ == '__main__':
    unittest.main()
    pass