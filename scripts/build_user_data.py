"""Build per-user JSON data."""

import csv
import datetime as dt
import json
from pathlib import Path
from typing import cast

DATA_DIR = Path("..", "charlie-data", "data")
RAW_DATA_DIR = DATA_DIR / "raw"


def get_last_fetch() -> str:
    """Get the timestamp of the latest raw data."""
    latest_dir = max(RAW_DATA_DIR.iterdir())
    latest_file = max(latest_dir.iterdir())
    my_date_time = dt.datetime.strptime(latest_file.stem, "%Y%m%d%H%M%S")

    return my_date_time.isoformat()


def load_users() -> set[str]:
    """Load users from the users CSV file."""
    with open(DATA_DIR / "input" / "users.csv", newline="") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        return {username for [username] in csv_reader}


def load_user_daily_steps(
    registered_users: set[str],
) -> dict[str, dict[str, int]]:
    """Load daily steps for each registered user.

    Args:
        registered_users: Usernames to include.

    Returns:
        Mapping of usernames to daily steps, with dates as keys and step counts
        as values.
    """
    user_daily_steps: dict[str, dict[str, int]] = {}

    raw_data_dirs = sorted(RAW_DATA_DIR.iterdir())
    for raw_data_dir in raw_data_dirs:
        user_latest_steps = load_user_latest_steps(
            raw_data_dir, registered_users
        )
        for username, steps_by_date in user_latest_steps.items():
            user_daily_steps.setdefault(username, {}).update(steps_by_date)

    return user_daily_steps


def load_user_latest_steps(
    raw_data_dir: Path, registered_users: set[str]
) -> dict[str, dict[str, int]]:
    """Load the latest available steps for each registered user.

    Args:
        raw_data_dir: Directory containing raw CSV files.
        registered_users: Usernames to include.

    Returns:
        Mapping of usernames to their latest steps, with dates as keys and step
        counts as values.
    """
    csv_paths = sorted(raw_data_dir.iterdir(), reverse=True)

    user_latest_steps = {}
    for csv_path in csv_paths:
        with open(csv_path, newline="") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for username, steps, date in csv_reader:
                if (
                    username in registered_users
                    and username not in user_latest_steps
                ):
                    user_latest_steps[username] = {date: int(steps)}

        if user_latest_steps.keys() >= registered_users:
            break

    return user_latest_steps


def load_user_public_ids() -> dict[str, str]:
    """Load user public IDs from the JSON file."""
    return cast(
        dict[str, str],
        json.loads((DATA_DIR / "output" / "user_public_ids.json").read_text()),
    )


def write_user_json_files(
    user_public_ids: dict[str, str],
    user_daily_steps: dict[str, dict[str, int]],
    last_fetch: str,
) -> None:
    """Write per-user JSON files to the public users directory."""
    output_dir = Path("public", "users")
    output_dir.mkdir(parents=True, exist_ok=True)

    for username, public_id in user_public_ids.items():
        user_data = {
            "username": username,
            "lastFetch": last_fetch,
            "dailySteps": user_daily_steps.get(username, {}),
        }
        (output_dir / f"{public_id}.json").write_text(
            json.dumps(user_data, ensure_ascii=False, indent=2)
        )


def main() -> None:
    """Main function."""
    last_fetch = get_last_fetch()
    user_public_ids = load_user_public_ids()
    user_daily_steps = load_user_daily_steps(set(user_public_ids))
    write_user_json_files(user_public_ids, user_daily_steps, last_fetch)


if __name__ == "__main__":
    main()
