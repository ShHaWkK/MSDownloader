import sys
from ui.gui import GUI
from ui.cli import CLI

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        CLI().run()
    else:
        GUI().run()

if __name__ == "__main__":
    main()
