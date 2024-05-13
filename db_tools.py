import argparse
import subprocess
import cProfile
import pstats


def populate_database():
    subprocess.run(["python", "./db/populate_db.py"])


def clear_database():
    subprocess.run(["python", "./db/clear_db.py"])


def main():
    parser = argparse.ArgumentParser(description="Test Script Menu")
    parser.add_argument(
        "action", choices=["populate", "clear"], help="Action to perform"
    )
    parser.add_argument(
        "--profile", action="store_true", help="Enable profiling with cProfile."
    )
    args = parser.parse_args()

    if args.profile:
        with cProfile.Profile() as profile:
            perform_action(args.action)
            print("Successfully performed action:", args.action)

        results = pstats.Stats(profile)
        results.sort_stats(pstats.SortKey.TIME)
        results.print_stats()
    else:
        perform_action(args.action)
        print("Successfully performed action:", args.action)


def perform_action(action):
    if action == "populate":
        populate_database()
    elif action == "clear":
        clear_database()


if __name__ == "__main__":
    main()
