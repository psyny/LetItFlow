from typing import List, Dict, Optional

from backend.models.command import Command
from backend.models.gamestate_change import GamestateChange

from backend.modules.command_executor.basic_commands.change_gamestate_phase import change_gamestate_phase

from backend.modules.command_executor.basic_commands.add_to_tactical import add_to_tactical
from backend.modules.command_executor.basic_commands.remove_from_tactical import remove_from_tactical
from backend.modules.command_executor.basic_commands.add_to_turn_order import add_to_turn_order
from backend.modules.command_executor.basic_commands.remove_from_turn_order import remove_from_turn_order
from backend.modules.command_executor.basic_commands.change_turn_order import change_turn_order

from backend.modules.command_executor.basic_commands.add_to_exploration import add_to_exploration
from backend.modules.command_executor.basic_commands.remove_from_exploration import remove_from_exploration
from backend.modules.command_executor.basic_commands.add_place import add_place
from backend.modules.command_executor.basic_commands.remove_place import remove_place
from backend.modules.command_executor.basic_commands.add_to_place import add_to_place
from backend.modules.command_executor.basic_commands.remove_from_place import remove_from_place

from backend.modules.command_executor.basic_commands.instance_stat_change import instance_stat_change
from backend.modules.command_executor.basic_commands.instance_condition_change import instance_condition_change


commandCallMap = {
    Command.Type.CHANGE_GAMESTATE_PHASE.value: change_gamestate_phase,

    Command.Type.ADD_TO_TACTICAL.value: add_to_tactical,
    Command.Type.REMOVE_FROM_TACTICAL.value: remove_from_tactical,
    Command.Type.ADD_TO_TURN_ORDER.value: add_to_turn_order,
    Command.Type.REMOVE_FROM_TURN_ORDER.value: remove_from_turn_order,
    Command.Type.CHANGE_TURN_ORDER.value: change_turn_order,

    Command.Type.ADD_TO_EXPLORATION.value: add_to_exploration,
    Command.Type.REMOVE_FROM_EXPLORATION.value: remove_from_exploration,
    Command.Type.ADD_PLACE.value: add_place,
    Command.Type.REMOVE_PLACE.value: remove_place,
    Command.Type.ADD_TO_PLACE.value: add_to_place,
    Command.Type.REMOVE_FROM_PLACE.value: remove_from_place,

    Command.Type.INSTANCE_CHANGE_STAT.value: instance_stat_change,
    Command.Type.INSTANCE_CHANGE_CONDITION.value: instance_condition_change,
    }

class CommandExecutor:
    @staticmethod
    def execute_command(command: Command, partyId: str) -> List[GamestateChange]:
        commandFunc = commandCallMap.get(command.commandType, None)

        if commandFunc == None:
            print("NONE")
            pass
        changes = []
        changes = commandFunc(command, partyId)
        return changes