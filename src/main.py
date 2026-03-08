import argparse
import sys
import traceback
from pathlib import Path

import use_cases
from botkit.sensor_util import CannotLocateGameException

if __name__ == "__main__":
    logs_folder = Path("logs")
    if not logs_folder.exists():
        logs_folder.mkdir()

    parser = argparse.ArgumentParser(
        prog="Cook, Serve, Delicious!",
        description="Bunch of utilities to play Cook, Serve, Delicious!, namely autoplay",
    )

    choice = parser.add_mutually_exclusive_group()
    choice.add_argument("--autoplay", action="store_true", help="Whether to autoplay the game;")
    choice.add_argument("--capture", action="store_true", help="to capture a game session;")
    choice.add_argument("--optimize-menu", action="store_true", help="to optimize the menu,")

    args = parser.parse_args()

    try:
        if args.autoplay:
            use_cases.run_bot()
        elif args.capture:
            use_cases.run_capture()
        elif args.optimize_menu:
            use_cases.optimize_menu()
        else:
            parser.print_help()
            exit(0)
    except CannotLocateGameException as e:
        traceback.print_exc()
        print("\nMaybe you should open the game first?", file=sys.stderr)
        exit(1)
