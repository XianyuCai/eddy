import sys
from typing import List, Callable, Optional
from command_factory import CommandFactory

class Eddy:
    def __init__(self, command_strings, print_by_default=True):
        self.commands = []
        factory = CommandFactory()
        for cmd in command_strings:
            if cmd and not cmd.startswith('#'):
                self.commands.append(factory.create_command(cmd))
        self.print_by_default = print_by_default

    def process_stream(self, stream: Callable[[], str]):
        lines = list(stream())
        last_line = len(lines)
        for line_number, line in enumerate(lines, start=1):
            line = line.rstrip('\n')
            output = self._process_line(line, line_number, last_line)
            if output is not None:
                print(output)

    def _process_line(self, line: str, line_number: int, last_line: int) -> Optional[str]:
        printed = False
        original_line = line
        for command in self.commands:
            if command.matches(line_number, line, last_line):
                output = command.execute(line)
                if output is None:
                    return None
                if output != original_line:
                    print(output)
                    printed = True
                if not self.print_by_default:
                    print(output)
                elif not printed:
                    print(output)
                    printed = True

        if self.print_by_default and not printed:
            return line
        return None