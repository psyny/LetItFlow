from typing import List, Dict, Optional

from backend.models.command import Command
from backend.models.gamestate_change import GamestateChange

from backend.modules.command_executor.basic_commands.add_to_turn_order import add_to_turn_order

commandCallMap = {
    Command.Type.ADD_TO_TURN_ORDER.value: add_to_turn_order,
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
