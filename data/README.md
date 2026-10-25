# Multilingual Song Dataset

Contains 90 songs: 30 English, 30 Tamil, and 30 Hindi.

Columns:
- `song_name`: song title
- `artist`: artist/performers
- `language`: English, Tamil, or Hindi
- `danceability`, `energy`, `valence`, `acousticness`: illustrative scores from 0 to 1
- `tempo_bpm`: illustrative tempo in beats per minute
- `youtube_url`: YouTube search-result URL for the song and artist

Important:
The song titles and artist names are curated entries, but audio feature values are simulated illustrative estimates, not verified measurements of the recordings. Replace these with real audio-feature measurements before claiming recommendations are musically accurate.

The `youtube_url` column contains search links, not direct video/watch URLs. They are suitable as clickable “Find on YouTube” links, but not for embedding with `st.video()`. For in-page playback, replace each with a verified direct YouTube watch URL for a video that allows embedding.
