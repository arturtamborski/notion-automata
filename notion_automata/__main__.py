from notion_automata.console import launch
from sys import argv


if __name__ == "__main__":
    try:
        token = open(argv[1]).read().strip()
        launch(token)
    except KeyboardInterrupt:
        print("exiting.")
