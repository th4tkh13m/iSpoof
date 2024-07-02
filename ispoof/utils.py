from pathlib import Path

HOME = Path.home() / ".ispoof"


def get_home_folder() -> Path:
    HOME.mkdir(parents=True, exist_ok=True)
    return HOME
