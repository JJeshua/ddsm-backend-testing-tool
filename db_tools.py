import argparse
import subprocess


def populate_database():
    subprocess.run(["python", "./db/populate_db.py"])


def clear_database():
    subprocess.run(["python", "./db/clear_db.py"])


def main():
    parser = argparse.ArgumentParser(description="Test Script Menu")
    parser.add_argument(
        "action", choices=["populate", "clear"], help="Action to perform"
    )
    args = parser.parse_args()

    if args.action == "populate":
        populate_database()
    elif args.action == "clear":
        clear_database()


if __name__ == "__main__":
    main()
