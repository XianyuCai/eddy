import sys
from eddy import Eddy

# Configuration
DEFAULT_SCRIPT_FILE = None

def parse_args():
    args = sys.argv[1:]
    print_by_default = True
    script_file = None
    commands = []
    files = []

    i = 0
    while i < len(args):
        if args[i] == '-n':
            print_by_default = False
        elif args[i] == '-f' and i + 1 < len(args):
            script_file = args[i + 1]
            i += 1
        elif not args[i].startswith('-') and not commands:
            commands = args[i].split(';')
        else:
            files.append(args[i])
        i += 1

    if script_file:
        with open(script_file, 'r') as f:
            commands = f.readlines()
    elif not commands and DEFAULT_SCRIPT_FILE:
        with open(DEFAULT_SCRIPT_FILE, 'r') as f:
            commands = f.readlines()

    # 移除开头结尾的空格
    commands = [cmd.strip() for cmd in commands if cmd.strip()]

    return print_by_default, commands, files

def main():
    print_by_default, commands, files = parse_args()
    eddy = Eddy(commands, print_by_default)

    if not files:
        eddy.process_stream(sys.stdin.readlines)
    else:
        for file in files:
            with open(file, 'r') as f:
                eddy.process_stream(f.readlines)

if __name__ == "__main__":
    main()