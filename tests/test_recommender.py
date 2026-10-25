
import pandas as pd

from src.recommender import recommend_songs


def test_recommend_songs_returns_results():
    df = pd.DataFrame({
        "song_name": ["Song A", "Song B", "Song C"],
        "artist": ["Artist A", "Artist B", "Artist C"],
        "danceability": [0.8, 0.78, 0.2],
        "energy": [0.9, 0.88, 0.3],
        "valence": [0.7, 0.72, 0.2],
        "acousticness": [0.1, 0.12, 0.9],
        "tempo_bpm": [120, 122, 70],
    })

    results = recommend_songs(df, "Song A", top_n=2)

    assert len(results) == 2
    assert "similarity_score" in results.columns
    assert results.iloc[0]["song_name"] == "Song B"


def test_selected_song_is_not_recommended():
    df = pd.DataFrame({
        "song_name": ["Song A", "Song B", "Song C"],
        "artist": ["Artist A", "Artist B", "Artist C"],
        "danceability": [0.8, 0.78, 0.2],
        "energy": [0.9, 0.88, 0.3],
        "valence": [0.7, 0.72, 0.2],
        "acousticness": [0.1, 0.12, 0.9],
        "tempo_bpm": [120, 122, 70],
    })

    results = recommend_songs(df, "Song A", top_n=2)

    assert "Song A" not in results["song_name"].values


