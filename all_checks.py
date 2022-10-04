from os import system


def main():
    print("##### PYLINT #####")
    system("pylint avion-api/*/*/*")
    print("##### MYPY #####")
    system("mypy .")
    print("##### UNIT TEST #####")
    system("pytest")

main()
