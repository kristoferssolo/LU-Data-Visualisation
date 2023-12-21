from pathlib import Path

import pandas as pd


def read_file(file_name: Path) -> pd.DataFrame:
    """Reads a file and returns a pandas DataFrame."""
    return pd.read_excel(file_name)


def base_path() -> Path:
    """Returns the base path of the project."""
    return Path(__file__).parent.parent.parent
