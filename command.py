import re
from typing import Optional

class Command:
    def __init__(self, address: str):
        self.address = address

    def matches(self, line_number: int, line: str, last_line: int) -> bool:
        pass

    def execute(self, line: str) -> Optional[str]:
        pass

    def _address_matches(self, line_number: int, line: str, last_line: int) -> bool:
        if self.address == '':
            return True
        elif self.address == '$':
            return line_number == last_line
        elif self.address.isdigit():
            return line_number == int(self.address)
        elif ',' in self.address:
            start, end = self.address.split(',')
            return self._range_matches(start, end, line_number, line, last_line)
        elif self.address.startswith('/'):
            pattern = self.address[1:-1]
            return re.search(pattern, line) is not None
        return False

    def _range_matches(self, start: str, end: str, line_number: int, line: str, last_line: int) -> bool:
        start_match = self._single_address_matches(start, line_number, line, last_line)
        end_match = self._single_address_matches(end, line_number, line, last_line)
        return start_match or (hasattr(self, 'range_active') and not end_match)

    def _single_address_matches(self, addr: str, line_number: int, line: str, last_line: int) -> bool:
        if addr == '$':
            return line_number == last_line
        elif addr.isdigit():
            return line_number == int(addr)
        elif addr.startswith('/'):
            pattern = addr[1:-1]
            return re.search(pattern, line) is not None
        return False

class PrintCommand(Command):
    def matches(self, line_number: int, line: str, last_line: int) -> bool:
        return self._address_matches(line_number, line, last_line)

    def execute(self, line: str) -> Optional[str]:
        return line

class SubstituteCommand(Command):
    def __init__(self, address: str, pattern: str, repl: str, flags: str):
        super().__init__(address)
        self.pattern = pattern
        self.repl = repl
        self.flags = flags

    def matches(self, line_number: int, line: str, last_line: int) -> bool:
        return self._address_matches(line_number, line, last_line)

    def execute(self, line: str) -> Optional[str]:
        try:
            count = 0 if 'g' in self.flags else 1
            return re.sub(self.pattern, self.repl, line, count=count)
        except re.error as e:
            raise ValueError(f"Invalid regex in substitute command: {str(e)}")

class DeleteCommand(Command):
    def matches(self, line_number: int, line: str, last_line: int) -> bool:
        return self._address_matches(line_number, line, last_line)

    def execute(self, line: str) -> Optional[str]:
        return None

class QuitCommand(Command):
    def matches(self, line_number: int, line: str, last_line: int) -> bool:
        return self._address_matches(line_number, line, last_line)

    def execute(self, line: str) -> Optional[str]:
        raise SystemExit(0)