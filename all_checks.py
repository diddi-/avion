import argparse
from os import system

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=str, choices=["lint", "mypy", "unit", "all"], default="all")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.check in ("lint", "all"):
        print("##### PYLINT #####")
        system("pylint avion-api/ all_checks.py")
    if args.check in ("mypy", "all"):
        print("##### MYPY #####")
        system("mypy .")
    if args.check in ("unit", "all"):
        print("##### UNIT TEST #####")
        system("pytest")

main()
