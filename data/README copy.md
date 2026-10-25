# Song Dataset

File: `songs.csv`

Columns:
- `song_name`: title of the song
- `artist`: artist name
- `danceability`: illustrative score from 0 to 1
- `energy`: illustrative score from 0 to 1
- `valence`: illustrative musical positivity score from 0 to 1
- `acousticness`: illustrative score from 0 to 1
- `tempo_bpm`: tempo in beats per minute

Important: the song titles and artist names are real, but the numerical audio
feature values in this starter dataset are simulated estimates, not verified
measurements from the actual recordings. Replace them with measured values
before treating the recommendations as musically accurate.

To validate and clean the CSV, run from the project root:

```bash
python -m src.data_loader
```

This creates `cleaned_songs.csv` in this folder.
