import argparse
from os import system

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=str, choices=["lint", "mypy", "unit", "all"], default="all")
    return parser.parse_args()

def main():
    # This PACKAGES list is necessary because some tools include packages in one large global import table resulting in
    # import conflicts. I.e. MyProj/src/pkg/*.py and MyProj/tests/pkg/*.py will cause package name conflict and strange
    # behaviors when running lint/mypy et al. To aviod this, we check each package src/ and tests/ directory
    # individually.
    PACKAGES = ["avion-api", "avion-wsgi"]
    args = parse_args()

    for pkg in PACKAGES:
        print(f">>> Running checks for {pkg} <<<")
        if args.check in ("lint", "all"):
            print("##### PYLINT #####")
            system(f"pylint {pkg}")
        if args.check in ("mypy", "all"):
            print("##### MYPY #####")
            system(f"mypy {pkg}/src")
            system(f"mypy {pkg}/tests")
        if args.check in ("unit", "all"):
            print("##### UNIT TEST #####")
            system(f"pytest {pkg}/tests")

main()
