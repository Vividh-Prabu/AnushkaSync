
import numpy as np
import pandas as pd

from src.vector_math import cosine_similarity


FEATURES = [
    "danceability",
    "energy",
    "valence",
    "acousticness",
    "tempo_bpm",
]


def create_song_vectors(df):
    """Convert song features into standardized vectors."""
    missing = [col for col in FEATURES if col not in df.columns]

    if missing:
        raise ValueError(f"Missing feature columns: {missing}")

    values = df[FEATURES].astype(float)

    means = values.mean()
    stds = values.std(ddof=0).replace(0, 1)

    standardized = (values - means) / stds

    return standardized.to_numpy(dtype=float)


def recommend_songs(df, selected_song, top_n=5):
    """Return the top similar songs, excluding the selected song."""
    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    if "song_name" not in df.columns:
        raise ValueError("Dataset needs a song_name column.")

    if "artist" not in df.columns:
        raise ValueError("Dataset needs an artist column.")

    names = df["song_name"].astype(str).str.strip().str.casefold()

    matches = np.flatnonzero(
        names.to_numpy() == selected_song.strip().casefold()
    )

    if len(matches) == 0:
        raise ValueError(f"Song not found: {selected_song}")

    selected_position = int(matches[0])
    vectors = create_song_vectors(df)
    selected_vector = vectors[selected_position]

    results = []

    for position, (_, row) in enumerate(df.iterrows()):
        if position == selected_position:
            continue

        score = cosine_similarity(
            selected_vector,
            vectors[position]
        )

        results.append({
            "song_name": row["song_name"],
            "artist": row["artist"],
            "similarity_score": round(score, 4),
        })

    results.sort(
        key=lambda item: item["similarity_score"],
        reverse=True
    )

    return pd.DataFrame(results[:top_n])
