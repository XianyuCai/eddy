from command import Command, PrintCommand, SubstituteCommand, DeleteCommand, QuitCommand

class CommandFactory:
    @staticmethod
    def create_command(command_str: str) -> Command:
        if command_str == 'p':
            return PrintCommand('')
        elif command_str == 'd':
            return DeleteCommand('')
        elif command_str == 'q':
            return QuitCommand('')
        elif command_str.startswith('s'):
            parts = command_str.split('/')
            if len(parts) != 4:
                raise ValueError(f"Invalid substitute command: {command_str}")
            _, pattern, repl, flags = parts
            return SubstituteCommand('', pattern, repl, flags)
        else:
            address, action = command_str.rsplit(command_str[-1], 1)
            action += command_str[-1]
            if action == 'p':
                return PrintCommand(address)
            elif action == 'd':
                return DeleteCommand(address)
            elif action == 'q':
                return QuitCommand(address)
            elif action.startswith('s'):
                parts = action.split('/')
                if len(parts) != 4:
                    raise ValueError(f"Invalid substitute command: {command_str}")
                _, pattern, repl, flags = parts
                return SubstituteCommand(address, pattern, repl, flags)
            else:
                raise ValueError(f"Unknown command: {command_str}")