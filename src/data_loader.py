
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "songs.csv"


def load_songs():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Song dataset not found at: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    required_columns = [
        "song_name",
        "artist",
        "danceability",
        "energy",
        "valence",
        "acousticness",
        "tempo_bpm",
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Dataset is missing required columns: {missing}"
        )

    df = df.dropna(subset=required_columns).copy()
    return df

