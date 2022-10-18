import argparse
from os import system

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=str, choices=["lint", "mypy", "unit", "all"], default="all")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.check == "lint" or args.check == "all":
        print("##### PYLINT #####")
        system("pylint avion-api/*/*/*")
    if args.check == "mypy" or args.check == "all":
        print("##### MYPY #####")
        system("mypy .")
    if args.check == "unit" or args.check == "all":
        print("##### UNIT TEST #####")
        system("pytest")

main()
