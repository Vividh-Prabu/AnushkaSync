
import html
from pathlib import Path
from urllib.parse import quote_plus

import numpy as np
import pandas as pd
import streamlit as st

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="AnuskaSync | Music Meets Mathematics",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent
# Prefer the project's data/songs.csv; also support a songs.csv beside app.py.
DATA_PATH = ROOT / "data" / "songs.csv"
if not DATA_PATH.exists() and (ROOT / "songs.csv").exists():
    DATA_PATH = ROOT / "songs.csv"
FEATURES = ["energy", "danceability", "acousticness", "valence"]

# ==================================================
# FUTURISTIC DESIGN SYSTEM
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #070914;
    --panel: #0e1224;
    --border: #252b4c;
    --cyan: #28dfff;
    --purple: #9d5cff;
    --pink: #ff43d1;
    --muted: #9ba6c8;
}

.stApp {
    background:
      radial-gradient(ellipse at 60% 0%, #172052 0%, transparent 38%),
      radial-gradient(ellipse at 100% 55%, #25103b 0%, transparent 32%),
      var(--bg);
    color: #f4f6ff;
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3, p, label {
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1600px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}

/* Futuristic sidebar */
[data-testid="stSidebar"] {
    background:
      radial-gradient(ellipse at 0% 0%, #33205b55, transparent 42%),
      linear-gradient(180deg, #0b0d1b 0%, #101329 55%, #0a0d19 100%);
    border-right: 1px solid #29294e;
    box-shadow: 8px 0 30px #00000020;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.4rem;
}

[data-testid="stSidebar"] * {
    color: #e7eaff;
}

[data-testid="stSidebar"] hr {
    border-color: #292c4d;
    margin-top: 1.1rem;
    margin-bottom: 1.1rem;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f1efff;
    font-size: 1rem;
    font-weight: 700;
}

/* Sidebar navigation: hover + selected state */
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 5px;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    background: #ffffff03;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 8px 10px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: linear-gradient(90deg, #8c5cff18, #35dfff0b);
    border-color: #5c4a8b;
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(100deg, #7040bd35, #28dfff12);
    border: 1px solid #8663d9;
    box-shadow: 0 0 16px #895cff17;
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
    color: #d9c4ff;
    font-weight: 700;
}

/* Sidebar song selector */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: linear-gradient(110deg, #15182e, #111528);
    border: 1px solid #51467e;
    border-radius: 11px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
    border-color: #9a6aff;
    box-shadow: 0 0 14px #885cff20;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #838eaf;
    font-size: 0.77rem;
    line-height: 1.6;
}

[data-testid="stSidebar"] ::-webkit-scrollbar { width: 5px; }
[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
    background: #51417b;
    border-radius: 10px;
}

#MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.neon-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(30px, 3.5vw, 48px);
    font-weight: 700;
    line-height: 1.12;
    letter-spacing: -1.8px;
    color: white;
    margin: 14px 0;
}

.gradient-text {
    background: linear-gradient(90deg, #28dfff, #a66aff, #ff43d1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.muted {
    color: #a9b3d5;
    line-height: 1.65;
}

.eyebrow {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #c0a5ff;
}

.hero {
    border: 1px solid #393b77;
    border-radius: 22px;
    padding: 28px;
    background:
      radial-gradient(circle at 80% 20%, #49309b88, transparent 35%),
      linear-gradient(120deg, #12172f, #17102c 70%, #0e1631);
    box-shadow: 0 0 30px #6946ff14, inset 0 0 35px #7052ff0a;
    min-height: 260px;
}

.vinyl {
    margin: auto;
    width: 190px;
    height: 190px;
    border-radius: 50%;
    background: repeating-radial-gradient(
        circle,
        #171a39 0px,
        #171a39 5px,
        #262454 6px,
        #090c1b 8px
    );
    border: 3px solid #735cff;
    box-shadow: 0 0 22px #5c65ff, 0 0 50px #b143ff65;
    display: flex;
    align-items: center;
    justify-content: center;
}

.vinyl-center {
    width: 62px;
    height: 62px;
    border-radius: 50%;
    background: radial-gradient(circle, #ff70e8, #792eff 55%, #11152a 58%);
    border: 2px solid #e5d5ff;
}

.panel {
    background: linear-gradient(145deg, #11162b, #0c1020);
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 19px;
    height: 100%;
    box-shadow: inset 0 0 20px #283dff08;
}

.metric {
    background: linear-gradient(135deg, #151831, #0d1224);
    border: 1px solid #37366b;
    border-radius: 15px;
    padding: 17px;
    box-shadow: 0 0 18px #6c4bff0b;
}

.metric-label {
    color: #9ba6c8;
    font-size: 10px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.metric-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 27px;
    font-weight: 700;
    margin-top: 7px;
    color: #fff;
}

.section-label {
    color: #bca4ff;
    letter-spacing: 2px;
    font-size: 11px;
    font-weight: 700;
    margin: 10px 0;
}

.song-card {
    background: linear-gradient(130deg, #171b36, #101426);
    border: 1px solid #333963;
    border-radius: 13px;
    padding: 13px;
    margin: 9px 0;
}

.rank {
    display: inline-block;
    color: #070914;
    background: linear-gradient(120deg, #28dfff, #b27aff);
    font-weight: 800;
    font-size: 11px;
    padding: 4px 8px;
    border-radius: 6px;
}

.score {
    font-size: 20px;
    font-weight: 700;
    color: #53e7ff;
}

.track-name {
    color: #fff;
    font-size: 16px;
    font-weight: 700;
    margin-top: 8px;
}

.track-artist {
    color: #9ba6c8;
    font-size: 12px;
}

.feature-label {
    display: flex;
    justify-content: space-between;
    color: #e4e9ff;
    font-size: 12px;
    margin: 13px 0 6px;
}

.feature-track {
    background: #252a45;
    height: 7px;
    border-radius: 10px;
    overflow: hidden;
}

.feature-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #4d8dff, #29e0ff, #d45dff);
    box-shadow: 0 0 10px #38bfff66;
}

div.stButton > button {
    border-radius: 10px;
    border: 1px solid #6553bc;
    background: linear-gradient(100deg, #703cff, #bd42f4);
    color: white;
    font-weight: 700;
    min-height: 43px;
    transition: 0.2s;
}

div.stButton > button:hover {
    border-color: #53e7ff;
    box-shadow: 0 0 18px #8b5cff55;
    color: white;
}

[data-testid="stSidebar"] div.stButton > button {
    background: linear-gradient(100deg, #7542d6, #9c4fe7);
    color: white;
    border: 1px solid #a26dff;
    border-radius: 10px;
    font-weight: 700;
}

[data-testid="stSidebar"] div.stButton > button:hover {
    box-shadow: 0 0 18px #995dff55;
    border-color: #46e4ff;
}

div[data-baseweb="select"] > div {
    background: #11152a;
    border-color: #414775;
    border-radius: 10px;
}

[data-testid="stMetric"] {
    background: #11152a;
    padding: 13px;
    border: 1px solid #292e50;
    border-radius: 12px;
}

hr {
    border-color: #292e50;
}

.footer {
    color: #7d88ad;
    text-align: center;
    padding: 28px 0 0;
    font-size: 11px;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# DATA
# ==================================================
def sample_data():
    return pd.DataFrame([
        ["Shape of You", "Ed Sheeran", .50, .55, .32, .66],
        ["Perfect", "Ed Sheeran", .45, .60, .16, .48],
        ["Blinding Lights", "The Weeknd", .73, .51, .05, .33],
        ["Levitating", "Dua Lipa", .78, .70, .01, .88],
        ["Someone Like You", "Adele", .31, .56, .89, .28],
        ["Believer", "Imagine Dragons", .88, .77, .06, .67],
        ["Photograph", "Ed Sheeran", .38, .46, .66, .27],
        ["As It Was", "Harry Styles", .64, .52, .34, .68],
        ["Stay", "The Kid LAROI", .72, .59, .04, .48],
        ["Lovely", "Billie Eilish", .29, .35, .93, .12],
        ["Dance The Night", "Dua Lipa", .84, .77, .02, .91],
        ["Yellow", "Coldplay", .44, .43, .28, .35],
    ], columns=["title", "artist"] + FEATURES)


def load_songs():
    if not DATA_PATH.exists():
        return sample_data(), True, "Sample dataset is being used."

    df = pd.read_csv(DATA_PATH)
    df.columns = [
        str(c).strip().lower().replace(" ", "_").replace("-", "_")
        for c in df.columns
    ]

    aliases = {
        "title": ["song_name", "song", "track_name", "track", "name"],
        "artist": ["artist_name", "singer", "performer"],
        "danceability": ["dance"],
        "acousticness": ["acoustic"],
        "valence": ["positivity", "mood"],
    }

    for target, alternatives in aliases.items():
        if target not in df.columns:
            for alternative in alternatives:
                if alternative in df.columns:
                    df = df.rename(columns={alternative: target})
                    break

    required = ["title", "artist"] + FEATURES
    missing = [c for c in required if c not in df.columns]

    if missing:
        return (
            sample_data(),
            True,
            "CSV is missing: " + ", ".join(missing),
        )

    df = df.dropna(subset=["title", "artist"]).copy()
    df["title"] = df["title"].astype(str)
    df["artist"] = df["artist"].astype(str)

    for feature in FEATURES:
        df[feature] = pd.to_numeric(df[feature], errors="coerce")

    df = df.dropna(subset=FEATURES).reset_index(drop=True)

    if df.empty:
        return sample_data(), True, "No valid songs found in CSV."

    return df, False, ""


songs, demo_mode, data_message = load_songs()

if demo_mode:
    st.sidebar.info(data_message)


# ==================================================
# RECOMMENDATION ENGINE
# Replace this function with Member 1's import later.
# ==================================================
def recommend_songs(data, selected_title, top_n=5):
    matrix = data[FEATURES].to_numpy(dtype=float)
    positions = np.flatnonzero(data["title"].to_numpy() == selected_title)

    if len(positions) == 0:
        return pd.DataFrame(columns=["title", "artist", "similarity"])

    position = int(positions[0])
    target = matrix[position]

    denominator = np.linalg.norm(matrix, axis=1) * np.linalg.norm(target)

    scores = np.divide(
        matrix @ target,
        denominator,
        out=np.zeros(len(matrix), dtype=float),
        where=denominator > 0,
    )

    result = data[["title", "artist"]].copy()
    result["similarity"] = scores
    result = result.drop(index=position)
    result = result.sort_values("similarity", ascending=False)

    return result.head(top_n).reset_index(drop=True)


def youtube_video_url(song_row):
    """Return a directly playable YouTube video URL, if the CSV contains one."""
    raw = song_row.get("youtube_url", "")
    if raw is None or pd.isna(raw):
        return None
    value = str(raw).strip()
    if not value:
        return None

    # Direct YouTube video links can be played with st.video().
    if "youtube.com/watch" in value or "youtu.be/" in value or "youtube.com/shorts/" in value:
        return value
    return None


def render_song_audio(song_row, key_suffix):
    """Play a direct YouTube video when possible, otherwise open the CSV's YouTube link."""
    title = str(song_row.get("title", song_row.get("song_name", "")))
    artist = str(song_row.get("artist", ""))
    raw_url = song_row.get("youtube_url", "")
    youtube_url = "" if raw_url is None or pd.isna(raw_url) else str(raw_url).strip()
    direct_video_url = youtube_video_url(song_row)

    if direct_video_url:
        st.video(direct_video_url)
        st.caption("Audio/video playback is provided by YouTube.")
    elif youtube_url.startswith(("https://www.youtube.com/", "https://youtube.com/", "https://youtu.be/")):
        st.info("This CSV entry is a YouTube search/results link, not a direct video. Open it to choose the exact song.")
        st.link_button("▶️ Find / play on YouTube", youtube_url, use_container_width=True)
    else:
        query = quote_plus(f"{title} {artist} official song".strip())
        search_url = f"https://www.youtube.com/results?search_query={query}"
        st.info("No YouTube URL was found for this song, so you can search for it on YouTube.")
        st.link_button("▶️ Search / play on YouTube", search_url, use_container_width=True)


# ==================================================
# NAVIGATION CALLBACK
# ==================================================
def go_to_recommendations():
    st.session_state["page"] = "Recommendations"


# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.markdown("""
    <div style="
        padding:8px 0 18px;
        border-bottom:1px solid #292c4d;
        margin-bottom:18px;
    ">
        <div style="
            font-size:27px;
            font-weight:800;
            letter-spacing:-0.8px;
            background:linear-gradient(90deg,#d1a2ff,#9b72ff,#4bdfff);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
        ">〽 AnuskaSync</div>
        <div style="color:#9ba7cc;font-size:12px;margin-top:6px">
            Your personal music discovery studio
        </div>
        <div style="
            margin-top:14px;display:flex;align-items:center;gap:7px;
            color:#52e7ff;font-size:10px;letter-spacing:1.2px;font-weight:700;
        "><span>●</span> MUSIC ENGINE READY</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### ◈ Navigation")

    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    page = st.radio(
        "Navigation",
        ["Home", "Recommendations", "Song Explorer", "About the Math"],
        key="page",
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### 🎧 Listening space")

    selected_title = st.selectbox(
        "Choose your favourite track",
        songs["title"].tolist(),
    )

    st.caption("Pick a song to explore its mathematical fingerprint.")

    st.divider()
    st.markdown("### ∑ Mathematics lab")

    math_topics = [
        ("01", "Dot product"),
        ("02", "Vector norms"),
        ("03", "Cosine similarity"),
        ("04", "Vector angles"),
        ("05", "Orthogonality"),
    ]

    for number, topic in math_topics:
        st.markdown(
            f"""
            <div style="
                display:flex;align-items:center;gap:10px;
                padding:7px 9px;margin:4px 0;
                border:1px solid #292d4b;border-radius:8px;
                background:#ffffff03;
            ">
                <span style="color:#9e7aff;font-size:10px;font-weight:800">{number}</span>
                <span style="color:#b9c3e2;font-size:12px">{topic}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    st.caption("✦ Built with Python · NumPy · Streamlit")


# ==================================================
# TOP BAR
# ==================================================
top_left, top_right = st.columns([5, 1])

with top_left:
    st.markdown(
        '<div class="eyebrow">AnuskaSync / MUSIC DISCOVERY SYSTEM</div>',
        unsafe_allow_html=True,
    )

with top_right:
    st.markdown(
        '<div style="text-align:right;color:#53e7ff;'
        'font-size:12px;padding-top:3px">● SYSTEM ONLINE</div>',
        unsafe_allow_html=True,
    )


# ==================================================
# HOME PAGE
# ==================================================
if page == "Home":
    hero_left, hero_right = st.columns([1.65, 1], gap="large")

    with hero_left:
        st.markdown(f"""
        <div class="hero">
            <div class="eyebrow">✦ YOUR PERSONAL SOUNDTRACK</div>
            <div class="neon-title">
                Discover your next<br>
                <span class="gradient-text">dimension of sound.</span>
            </div>
            <p class="muted">
                One song can lead to a whole new playlist.
                Explore music through vector mathematics and discover
                tracks with a similar musical fingerprint.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "✦  FIND SIMILAR SONGS  →",
            type="primary",
            on_click=go_to_recommendations,
        )

    with hero_right:
        st.markdown("""
        <div class="hero" style="height:260px;display:flex;
        align-items:center;justify-content:center;overflow:hidden;">
            <div style="text-align:center">
                <div class="vinyl">
                    <div class="vinyl-center"></div>
                </div>
                <div style="font-size:10px;letter-spacing:3px;
                color:#9ba6c8;margin-top:15px">
                    MUSIC MEETS MATHEMATICS
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Stats
    a, b, c = st.columns(3)

    with a:
        st.markdown(f"""
        <div class="metric">
            <div class="metric-label">♫ Tracks in collection</div>
            <div class="metric-value">{len(songs)}</div>
            <div class="muted" style="font-size:11px">Songs ready to explore</div>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="metric">
            <div class="metric-label">◈ Musical dimensions</div>
            <div class="metric-value">04</div>
            <div class="muted" style="font-size:11px">Energy · Dance · Acoustic · Valence</div>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="metric">
            <div class="metric-label">✧ Recommendations</div>
            <div class="metric-value">TOP 05</div>
            <div class="muted" style="font-size:11px">Closest mathematical matches</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    selected = songs[songs["title"] == selected_title].iloc[0]

    song_col, feature_col = st.columns([1, 1.2], gap="large")

    with song_col:
        st.markdown('<div class="section-label">NOW EXPLORING</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### 🎵 Selected track")
        st.markdown(
            f'<div style="font-size:25px;font-weight:700">'
            f'{html.escape(selected["title"])}</div>'
            f'<div class="muted">{html.escape(selected["artist"])}</div>',
            unsafe_allow_html=True,
        )
        st.write("")
        st.markdown('<div class="eyebrow">SONG FEATURE VECTOR</div>',
                    unsafe_allow_html=True)
        st.code(
            "v = (" + ", ".join(f"{selected[f]:.2f}" for f in FEATURES) + ")"
        )
        st.caption("Energy · Danceability · Acousticness · Valence")
        st.markdown("</div>", unsafe_allow_html=True)

    with feature_col:
        st.markdown('<div class="section-label">MUSICAL FINGERPRINT</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### 📐 Feature profile")

        labels = {
            "energy": ("⚡", "Energy"),
            "danceability": ("♬", "Danceability"),
            "acousticness": ("♢", "Acousticness"),
            "valence": ("☀", "Valence"),
        }

        for feature in FEATURES:
            value = float(selected[feature])
            emoji, label = labels[feature]
            st.markdown(
                f'<div class="feature-label">'
                f'<span>{emoji} {label}</span><span>{value:.2f}</span></div>'
                f'<div class="feature-track"><div class="feature-fill" '
                f'style="width:{max(0, min(value, 1))*100:.1f}%">'
                f'</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="section-label">YOUR NEXT OBSESSION</div>',
                unsafe_allow_html=True)
    st.markdown("## ✨ Top 5 recommendations")

    st.button(
        "⚡  Calculate my top 5 matches",
        type="primary",
        on_click=go_to_recommendations,
    )



elif page == "Recommendations":
    selected = songs[songs["title"] == selected_title].iloc[0]
    results = recommend_songs(songs, selected_title, 5)

    # ================================================
    # PREMIUM TUNEMATCH RECOMMENDATIONS
    # ================================================
    st.markdown("""
    <style>
    .premium-hero {
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(ellipse at 95% 5%, #9b5cff35, transparent 38%),
            radial-gradient(ellipse at 5% 100%, #26dfff12, transparent 35%),
            linear-gradient(125deg, #171b38, #211333 68%, #101529);
        border: 1px solid #51447d;
        border-radius: 24px;
        padding: 30px;
        margin: 10px 0 24px;
        box-shadow: 0 15px 45px #00000022;
    }
    .premium-eyebrow {
        color: #c4a4ff;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .premium-title {
        color: #fff;
        font-size: clamp(30px, 4vw, 44px);
        line-height: 1.12;
        font-weight: 800;
        letter-spacing: -1.3px;
        margin: 13px 0;
    }
    .premium-subtitle {
        color: #aab5d7;
        font-size: 13px;
        line-height: 1.8;
        max-width: 650px;
    }
    .premium-status {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 7px 10px;
        margin-top: 17px;
        border: 1px solid #3a6072;
        background: #21dfff0d;
        border-radius: 20px;
        color: #6cecff;
        font-size: 10px;
        letter-spacing: 1px;
        font-weight: 800;
    }
    .premium-metric {
        background: linear-gradient(145deg, #151a32, #101426);
        border: 1px solid #2d3659;
        border-radius: 16px;
        padding: 17px;
        min-height: 105px;
    }
    .premium-metric-label {
        color: #a8b3d5;
        font-size: 10px;
        letter-spacing: 1.5px;
        font-weight: 800;
    }
    .premium-metric-value {
        font-size: 27px;
        color: #f4f4ff;
        font-weight: 800;
        margin-top: 8px;
    }
    .premium-panel {
        background: linear-gradient(145deg, #151a32, #0d1121);
        border: 1px solid #2e375c;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .premium-card {
        position: relative;
        background:
            radial-gradient(ellipse at 100% 0%, #8b5cff12, transparent 42%),
            linear-gradient(125deg, #171c35, #101426);
        border: 1px solid #303a60;
        border-radius: 17px;
        padding: 18px;
        margin: 12px 0;
        transition: border-color .2s ease, box-shadow .2s ease;
    }
    .premium-card:hover {
        border-color: #8d6bce;
        box-shadow: 0 0 22px #825cff16;
    }
    .premium-card-first {
        background:
            radial-gradient(ellipse at 100% 0%, #c65cff25, transparent 45%),
            linear-gradient(120deg, #21183e, #11172b);
        border-color: #8b65cb;
        box-shadow: 0 0 22px #9d5cff12;
    }
    .premium-rank {
        display: inline-block;
        padding: 5px 9px;
        background: linear-gradient(100deg, #31dfff, #a86cff);
        border-radius: 7px;
        color: #080b18;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: .4px;
    }
    .premium-featured {
        display: inline-block;
        padding: 5px 8px;
        border: 1px solid #b98cff66;
        border-radius: 7px;
        color: #d8bdff;
        background: #a46cff13;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: .8px;
        margin-left: 5px;
    }
    .premium-song {
        color: #fff;
        font-size: 19px;
        font-weight: 800;
        letter-spacing: -.3px;
        line-height: 1.35;
        margin-top: 12px;
        overflow-wrap: anywhere;
    }
    .premium-artist {
        color: #a5b0d1;
        font-size: 12px;
        margin-top: 5px;
    }
    .premium-score {
        color: #51e7ff;
        font-size: 27px;
        font-weight: 900;
        text-align: right;
        line-height: 1.1;
    }
    .premium-score-label {
        color: #9ba8cc;
        font-size: 9px;
        text-align: right;
        letter-spacing: 1.2px;
        margin-top: 6px;
    }
    .premium-track {
        height: 6px;
        width: 100%;
        overflow: hidden;
        border-radius: 10px;
        background: #292e4b;
        margin-top: 17px;
    }
    .premium-fill {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #26dfff, #8c68ff, #d35cff);
    }
    .premium-section-label {
        color: #c5a6ff;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }
    .premium-note {
        color: #aab5d5;
        font-size: 12px;
        line-height: 1.7;
    }
    /* Native Streamlit recommendation cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #303a60 !important;
        border-radius: 17px !important;
        background: linear-gradient(125deg, #171c35, #101426) !important;
        margin: 12px 0 !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMetric"] {
        background: #10182a !important;
        border: 1px solid #334263 !important;
        border-radius: 12px !important;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #30395b;
        border-radius: 12px;
        background: #111528;
        margin-bottom: 10px;
    }
    div[data-testid="stExpander"] summary:hover {
        color: #c5a5ff;
    }
    </style>
    """, unsafe_allow_html=True)

    # -----------------------------------------------
    # HERO
    # -----------------------------------------------
    st.markdown(f"""
    <div class="premium-hero">
        <div class="premium-eyebrow">
            AnuskaSync / PERSONALIZED DISCOVERY
        </div>
        <div class="premium-title">
            Your next obsession.<br>
            <span style="color:#b58aff">Mathematically matched.</span>
        </div>
        <div class="premium-subtitle">
            Your selected song becomes a vector in musical feature space.
            We compare it against the collection and rank the closest
            feature profiles using cosine similarity.
        </div>
        <div class="premium-status">
            <span>●</span> SIMILARITY ENGINE ACTIVE
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------
    # SELECTED SONG PANEL
    # -----------------------------------------------
    selected_col, method_col = st.columns([1.15, 1], gap="large")

    with selected_col:
        st.markdown('<div class="premium-panel">', unsafe_allow_html=True)
        st.markdown(
            '<div class="premium-section-label">◉ YOUR STARTING TRACK</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="font-size:25px;font-weight:800;color:#fff">'
            f'🎧 {html.escape(str(selected["title"]))}</div>'
            f'<div class="premium-artist">'
            f'{html.escape(str(selected["artist"]))}</div>',
            unsafe_allow_html=True,
        )
        st.write("")
        st.caption("FOUR-DIMENSIONAL FEATURE VECTOR")
        vector_text = ", ".join(f"{float(selected[f]):.3f}" for f in FEATURES)
        st.code(f"A = ({vector_text})", language="text")
        st.markdown(
            '<div class="premium-note">'
            'Feature order: Energy · Danceability · Acousticness · Valence'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with method_col:
        st.markdown('<div class="premium-panel">', unsafe_allow_html=True)
        st.markdown(
            '<div class="premium-section-label">∑ MATCHING METHOD</div>',
            unsafe_allow_html=True,
        )
        st.markdown("### Cosine similarity")
        st.latex(
            r"\operatorname{cosSim}(A,B)="
            r"\frac{A\cdot B}{\|A\|\,\|B\|}"
        )
        st.markdown(
            '<div class="premium-note">'
            'The algorithm compares vector directions, excludes the selected '
            'song itself, and ranks the remaining songs by score.'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------
    # EMPTY RESULTS HANDLING
    # -----------------------------------------------
    st.markdown("## ✨ Your top matches")
    st.markdown(
        '<div class="premium-note">'
        'Explore the songs with the closest musical feature profiles.'
        '</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    if results.empty:
        st.warning("There aren't enough alternative songs to recommend yet.")

    else:
        # -------------------------------------------
        # METRICS
        # -------------------------------------------
        best_score = float(results["similarity"].max())
        average_score = float(results["similarity"].mean())

        metric1, metric2, metric3 = st.columns(3)

        with metric1:
            st.markdown(f"""
            <div class="premium-metric">
                <div class="premium-metric-label">TRACKS FOUND</div>
                <div class="premium-metric-value">{len(results):02d}</div>
                <div class="premium-note">Ranked alternatives</div>
            </div>
            """, unsafe_allow_html=True)

        with metric2:
            st.markdown(f"""
            <div class="premium-metric">
                <div class="premium-metric-label">BEST MATCH SCORE</div>
                <div class="premium-metric-value"
                     style="color:#50e6ff">{best_score:.3f}</div>
                <div class="premium-note">Highest cosine similarity</div>
            </div>
            """, unsafe_allow_html=True)

        with metric3:
            st.markdown(f"""
            <div class="premium-metric">
                <div class="premium-metric-label">AVERAGE SCORE</div>
                <div class="premium-metric-value"
                     style="color:#c19aff">{average_score:.3f}</div>
                <div class="premium-note">Across displayed matches</div>
            </div>
            """, unsafe_allow_html=True)

        if len(results) < 5:
            st.info(f"Your collection currently has {len(results)} alternative matches.")

        st.write("")
        cards_col, chart_col = st.columns([1.2, 0.8], gap="large")

        # -------------------------------------------
        # PREMIUM RECOMMENDATION CARDS
        # -------------------------------------------
        with cards_col:
            st.markdown(
                '<div class="premium-section-label">'
                '▤ YOUR PERSONAL RECOMMENDATION QUEUE</div>',
                unsafe_allow_html=True,
            )

            for rank, (_, song) in enumerate(results.iterrows(), start=1):
                score = float(song["similarity"])
                score_percent = max(0.0, min(score, 1.0))

                # Use native Streamlit components for every card so all five
                # render consistently; no raw HTML is passed through Markdown.
                with st.container(border=True):
                    header_left, header_right = st.columns([4, 1])

                    with header_left:
                        if rank == 1:
                            st.markdown("**🏆 MATCH #01 · TOP PICK**")
                        else:
                            st.markdown(f"**MATCH #{rank:02d}**")
                        st.subheader(str(song["title"]))
                        st.caption(str(song["artist"]))

                    with header_right:
                        st.metric("Cosine score", f"{score:.3f}")

                    st.progress(score_percent)
                    st.caption(f"Vector similarity · {score_percent * 100:.1f}% of scale")

                    # YouTube playback uses the existing youtube_url column;
                    # recommendation calculations remain unchanged.
                    source_rows = songs[songs["title"].astype(str) == str(song["title"])]
                    audio_row = source_rows.iloc[0] if not source_rows.empty else song
                    with st.expander("▶️ Listen on YouTube", expanded=False):
                        render_song_audio(audio_row, rank)

                with st.expander(
                    f"🔬 Why this match? — {song['title']}",
                    expanded=False,
                ):
                    match_row = songs[
                        songs["title"].astype(str) == str(song["title"])
                    ]

                    if match_row.empty:
                        st.info("Feature details are unavailable for this track.")
                    else:
                        candidate = match_row.iloc[0]
                        st.markdown(
                            f"**{song['title']}** compared with **{selected['title']}**"
                        )

                        differences = []
                        for feature in FEATURES:
                            a = float(selected[feature])
                            b = float(candidate[feature])
                            differences.append({
                                "Feature": feature.replace("_", " ").title(),
                                "Selected song": a,
                                "Recommended song": b,
                                "Absolute difference": abs(a - b),
                            })

                        difference_df = pd.DataFrame(differences)
                        st.dataframe(
                            difference_df.style.format({
                                "Selected song": "{:.3f}",
                                "Recommended song": "{:.3f}",
                                "Absolute difference": "{:.3f}",
                            }),
                            use_container_width=True,
                            hide_index=True,
                        )

                        st.caption(
                            "Individual feature differences help explain the comparison. "
                            "The recommendation rank is determined by cosine similarity "
                            "across the complete vectors."
                        )

        # -------------------------------------------
        # ANALYTICS AND CHART
        # -------------------------------------------
        with chart_col:
            st.markdown('<div class="premium-panel">', unsafe_allow_html=True)
            st.markdown(
                '<div class="premium-section-label">'
                '◈ SIMILARITY ANALYTICS</div>',
                unsafe_allow_html=True,
            )
            st.markdown("### Similarity landscape")

            chart_data = results.set_index("title")[["similarity"]]
            st.bar_chart(
                chart_data,
                horizontal=True,
                height=320,
            )

            st.markdown(
                '<div class="premium-note">'
                'Each bar represents the cosine similarity score of one '
                'recommended song. Higher scores indicate more closely '
                'aligned vector directions.'
                '</div>',
                unsafe_allow_html=True,
            )

            st.divider()
            st.markdown("### The mathematics")
            st.latex(
                r"\operatorname{cosSim}(A,B)="
                r"\frac{A\cdot B}{\|A\|\,\|B\|}"
            )
            st.markdown(
                '<div class="premium-note">'
                'Cosine similarity is not a probability of liking a song. '
                'It measures directional similarity between feature vectors.'
                '</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # -------------------------------------------
        # EXACT SCORES TABLE
        # -------------------------------------------
        with st.expander("📊 Inspect exact recommendation scores"):
            exact_scores = results[["title", "artist", "similarity"]].copy()
            exact_scores.insert(
                0, "Rank", range(1, len(exact_scores) + 1)
            )
            st.dataframe(
                exact_scores.style.format({"similarity": "{:.5f}"}),
                use_container_width=True,
                hide_index=True,
            )

    # -----------------------------------------------
    # FOOTER
    # -----------------------------------------------
    st.markdown("""
    <div style="text-align:center;color:#7f8aaf;font-size:10px;
                letter-spacing:1.5px;padding:28px 0 12px">
        AnuskaSync· MUSIC MEETS MATHEMATICS<br>
        VECTOR SPACE / COSINE SIMILARITY / PERSONALIZED DISCOVERY
    </div>
    """, unsafe_allow_html=True)


elif page == "Song Explorer":
    # ================================================
    # FUTURISTIC SONG EXPLORER
    # Uses the existing `songs` DataFrame
    # ================================================

    st.markdown("""
    <style>
    .explorer-hero {
        background:
            radial-gradient(circle at 90% 15%, #733bce55, transparent 32%),
            linear-gradient(115deg, #151a38, #241436 72%, #10162d);
        border: 1px solid #4b407b;
        border-radius: 22px;
        padding: 27px;
        margin: 12px 0 22px;
        box-shadow: 0 0 28px #754cff12;
    }
    .explorer-eyebrow {
        color: #c6a7ff;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
    }
    .explorer-heading {
        color: #fff;
        font-size: clamp(30px, 4vw, 43px);
        line-height: 1.15;
        font-weight: 800;
        margin: 12px 0;
    }
    .explorer-gradient {
        background: linear-gradient(90deg, #31e1ff, #b58aff, #ff76d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .explorer-muted {
        color: #aab4d4;
        font-size: 13px;
        line-height: 1.7;
    }
    .explorer-panel {
        background: linear-gradient(145deg, #151a32, #0d1121);
        border: 1px solid #30395e;
        border-radius: 17px;
        padding: 19px;
        margin-bottom: 15px;
    }
    .explorer-metric {
        background: linear-gradient(135deg, #161b36, #0d1224);
        border: 1px solid #343b65;
        border-radius: 15px;
        padding: 17px;
        min-height: 105px;
    }
    .explorer-metric-label {
        color: #9da9cb;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.3px;
    }
    .explorer-metric-value {
        color: #f7f7ff;
        font-size: 27px;
        font-weight: 800;
        margin-top: 7px;
    }
    .explorer-track {
        background: linear-gradient(120deg, #191e3b, #11152a);
        border: 1px solid #343c65;
        border-radius: 13px;
        padding: 13px;
        margin: 8px 0;
    }
    .explorer-track-title {
        font-size: 15px;
        font-weight: 700;
        color: #fff;
    }
    .explorer-track-artist {
        font-size: 12px;
        color: #a2adcf;
        margin-top: 4px;
    }
    .explorer-badge {
        display: inline-block;
        background: #29dfff18;
        border: 1px solid #29dfff66;
        color: #59e8ff;
        border-radius: 7px;
        padding: 4px 8px;
        font-size: 10px;
        font-weight: 700;
    }
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background: #11162b;
        border-color: #3a416b;
        border-radius: 10px;
    }
    div.stButton > button {
        border: 1px solid #6653b8;
        border-radius: 10px;
        background: linear-gradient(100deg, #713cff, #b842ef);
        color: white;
        font-weight: 700;
    }
    div.stButton > button:hover {
        border-color: #39e5ff;
        box-shadow: 0 0 16px #8b5cff55;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    import html

    # -----------------------------------------------
    # Prepare the explorer data
    # -----------------------------------------------
    explorer_df = songs.copy()

    # Identify optional tempo column without requiring it.
    tempo_candidates = ["tempo_bpm", "tempo", "bpm"]
    tempo_col = next(
        (c for c in tempo_candidates if c in explorer_df.columns),
        None,
    )

    feature_cols = [
        c for c in FEATURES
        if c in explorer_df.columns
    ]

    # -----------------------------------------------
    # Hero section
    # -----------------------------------------------
    st.markdown("""
    <div class="explorer-hero">
        <div class="explorer-eyebrow">
            AnuskaSync / MUSIC DATABASE
        </div>
        <div class="explorer-heading">
            Explore your<br>
            <span class="explorer-gradient">sound universe.</span>
        </div>
        <div class="explorer-muted">
            Search your collection, discover artists, inspect musical
            fingerprints, and explore the features powering your
            recommendation algorithm.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------
    # Collection metrics
    # -----------------------------------------------
    total_tracks = len(explorer_df)

    if "artist" in explorer_df.columns:
        total_artists = explorer_df["artist"].nunique()
    else:
        total_artists = 0

    if tempo_col and total_tracks:
        tempo_values = pd.to_numeric(
            explorer_df[tempo_col], errors="coerce"
        ).dropna()
        average_tempo = (
            f"{tempo_values.mean():.0f} BPM"
            if not tempo_values.empty else "N/A"
        )
    else:
        average_tempo = "N/A"

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(f"""
        <div class="explorer-metric">
            <div class="explorer-metric-label">♫ TRACKS IN LIBRARY</div>
            <div class="explorer-metric-value">{total_tracks}</div>
            <div class="explorer-muted">Available songs</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="explorer-metric">
            <div class="explorer-metric-label">✦ UNIQUE ARTISTS</div>
            <div class="explorer-metric-value">{total_artists}</div>
            <div class="explorer-muted">Across your collection</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="explorer-metric">
            <div class="explorer-metric-label">〰 AVERAGE TEMPO</div>
            <div class="explorer-metric-value">{average_tempo}</div>
            <div class="explorer-muted">Collection-wide average</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # -----------------------------------------------
    # Search and filters
    # -----------------------------------------------
    st.markdown(
        '<div class="explorer-eyebrow">⌕ SEARCH YOUR COLLECTION</div>',
        unsafe_allow_html=True,
    )
    st.markdown("## Find your track")

    search_col, artist_col = st.columns([1.6, 1])

    with search_col:
        query = st.text_input(
            "Search",
            placeholder="⌕  Search song title or artist...",
            key="explorer_query",
            label_visibility="collapsed",
        )

    with artist_col:
        artist_options = ["All artists"] + sorted(
            explorer_df["artist"].dropna().astype(str).unique().tolist()
        ) if "artist" in explorer_df.columns else ["All artists"]

        selected_artist = st.selectbox(
            "Filter by artist",
            artist_options,
            label_visibility="collapsed",
        )

    filtered_df = explorer_df.copy()

    if query.strip():
        mask = pd.Series(False, index=filtered_df.index)

        for col in ["title", "artist"]:
            if col in filtered_df.columns:
                mask |= filtered_df[col].astype(str).str.contains(
                    query.strip(),
                    case=False,
                    na=False,
                    regex=False,
                )

        filtered_df = filtered_df[mask]

    if selected_artist != "All artists" and "artist" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["artist"].astype(str) == selected_artist
        ]

    st.markdown(
        f'<div class="explorer-muted">'
        f'Showing <b>{len(filtered_df)}</b> of '
        f'<b>{total_tracks}</b> tracks</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------
    # Featured track
    # -----------------------------------------------
    st.write("")
    st.markdown(
        '<div class="explorer-eyebrow">◈ TRACK SPOTLIGHT</div>',
        unsafe_allow_html=True,
    )

    if filtered_df.empty:
        st.warning(
            "No tracks match your search. Try a different title or artist."
        )
    else:
        track_titles = filtered_df["title"].astype(str).tolist()

        featured_title = st.selectbox(
            "Choose a track to inspect",
            track_titles,
            key="explorer_featured_track",
        )

        featured_matches = filtered_df[
            filtered_df["title"].astype(str) == featured_title
        ]
        featured = featured_matches.iloc[0]

        featured_col, profile_col = st.columns([1, 1.15], gap="large")

        with featured_col:
            st.markdown('<div class="explorer-panel">', unsafe_allow_html=True)

            st.markdown(
                '<span class="explorer-badge">SELECTED TRACK</span>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div style="font-size:48px;margin-top:15px">🎧</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div style="font-size:25px;font-weight:800;color:white">'
                f'{html.escape(str(featured["title"]))}</div>',
                unsafe_allow_html=True,
            )

            artist_name = str(featured.get("artist", "Unknown artist"))

            st.markdown(
                f'<div class="explorer-track-artist" '
                f'style="font-size:15px;margin-top:5px">'
                f'{html.escape(artist_name)}</div>',
                unsafe_allow_html=True,
            )

            st.divider()

            if tempo_col:
                tempo = pd.to_numeric(
                    pd.Series([featured[tempo_col]]),
                    errors="coerce",
                ).iloc[0]

                if pd.notna(tempo):
                    st.metric("♬ Tempo", f"{tempo:.1f} BPM")

            st.caption(
                "This track can also be selected in the listening space "
                "in the sidebar for recommendations."
            )

            if st.button(
                "✦ Recommend songs like this",
                key="explorer_recommend_button",
                type="primary",
            ):
                # The sidebar selectbox uses the same session-state key.
                st.session_state["selected_song"] = featured_title
                st.session_state["page"] = "Recommendations"
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

        with profile_col:
            st.markdown('<div class="explorer-panel">', unsafe_allow_html=True)
            st.markdown("### 📐 Musical fingerprint")
            st.caption("Numerical features used by the similarity engine")

            if feature_cols:
                for feature in feature_cols:
                    value = pd.to_numeric(
                        pd.Series([featured[feature]]),
                        errors="coerce",
                    ).iloc[0]

                    if pd.isna(value):
                        continue

                    # Values are expected to be normalized to 0–1.
                    # Clamp only the displayed bar; show the actual value.
                    bar_value = max(0.0, min(float(value), 1.0))

                    st.markdown(
                        f'<div style="display:flex;justify-content:'
                        f'space-between;margin:13px 0 6px;color:#e6eaff;'
                        f'font-size:12px">'
                        f'<span>{html.escape(feature.replace("_", " ").title())}'
                        f'</span><b>{float(value):.3f}</b></div>'
                        f'<div style="height:7px;background:#272e4e;'
                        f'border-radius:8px;overflow:hidden">'
                        f'<div style="height:100%;width:{bar_value*100:.1f}%;'
                        f'background:linear-gradient(90deg,#31dfff,#bd66ff);'
                        f'border-radius:8px"></div></div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No recognized numerical song features are available.")

            st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------
    # Collection table
    # -----------------------------------------------
    st.write("")
    st.markdown(
        '<div class="explorer-eyebrow">▤ ALL TRACKS</div>',
        unsafe_allow_html=True,
    )
    st.markdown("## Your music library")

    if not filtered_df.empty:
        display_df = filtered_df.copy()

        # Put identifying information first.
        preferred = [
            c for c in ["title", "artist"] if c in display_df.columns
        ]
        remaining = [c for c in display_df.columns if c not in preferred]
        display_df = display_df[preferred + remaining]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=390,
        )

        csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Export filtered tracks as CSV",
            data=csv_bytes,
            file_name="AnuskaSync_filtered_songs.csv",
            mime="text/csv",
        )

    # -----------------------------------------------
    # Feature distribution
    # -----------------------------------------------
    if feature_cols and not filtered_df.empty:
        st.write("")
        st.markdown(
            '<div class="explorer-eyebrow">◈ DATA INSIGHTS</div>',
            unsafe_allow_html=True,
        )
        st.markdown("## Collection feature overview")

        numeric_features = filtered_df[feature_cols].apply(
            pd.to_numeric, errors="coerce"
        )

        avg_features = numeric_features.mean().dropna()

        if not avg_features.empty:
            chart_col, summary_col = st.columns([1.25, 0.75], gap="large")

            with chart_col:
                st.markdown(
                    '<div class="explorer-panel">',
                    unsafe_allow_html=True,
                )
                st.markdown("### Average feature values")
                st.bar_chart(avg_features, height=300)
                st.caption(
                    "Average values of the numerical features in the "
                    "currently filtered collection."
                )
                st.markdown("</div>", unsafe_allow_html=True)

            with summary_col:
                st.markdown(
                    '<div class="explorer-panel">',
                    unsafe_allow_html=True,
                )
                st.markdown("### Feature statistics")

                for feature in feature_cols:
                    values = numeric_features[feature].dropna()

                    if values.empty:
                        continue

                    st.markdown(
                        f'<div class="explorer-track">'
                        f'<div class="explorer-track-title">'
                        f'{html.escape(feature.replace("_", " ").title())}'
                        f'</div>'
                        f'<div class="explorer-track-artist">'
                        f'Mean: {values.mean():.3f} · '
                        f'Min: {values.min():.3f} · '
                        f'Max: {values.max():.3f}'
                        f'</div></div>',
                        unsafe_allow_html=True,
                    )

                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;color:#7f8aaf;font-size:11px;
    padding:28px 0 8px;letter-spacing:1px">
        AnuskaSync· MUSIC MEETS MATHEMATICS<br>
        SEARCH / EXPLORE / ANALYZE / DISCOVER
    </div>
    """, unsafe_allow_html=True)


elif page == "About the Math":
    import math

    st.markdown("""
    <style>
    .math-hero {
        background:
            radial-gradient(circle at 90% 10%, #6334a855, transparent 34%),
            linear-gradient(120deg, #141a37, #201334 75%, #10172d);
        border: 1px solid #51417c;
        border-radius: 22px;
        padding: 28px;
        margin: 12px 0 22px;
    }
    .math-eyebrow {
        color: #c2a5ff;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
    }
    .math-heading {
        font-size: clamp(29px, 4vw, 43px);
        font-weight: 800;
        line-height: 1.15;
        margin: 12px 0;
        color: #fff;
    }
    .math-muted {
        color: #aeb8d8;
        line-height: 1.75;
        font-size: 14px;
    }
    .math-panel {
        background: linear-gradient(145deg, #141a31, #0d1121);
        border: 1px solid #30395e;
        border-radius: 17px;
        padding: 21px;
        margin: 12px 0;
    }
    .math-number {
        color: #45e4ff;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.5px;
    }
    .math-callout {
        border-left: 3px solid #9d6aff;
        background: #8b5cff12;
        border-radius: 0 10px 10px 0;
        padding: 12px 15px;
        color: #dce2ff;
        line-height: 1.7;
        margin-top: 12px;
    }
    .math-result {
        background: #10182d;
        border: 1px solid #315071;
        border-radius: 13px;
        padding: 16px;
    }
    .math-result-label {
        font-size: 10px;
        color: #9ba8cb;
        letter-spacing: 1.4px;
    }
    .math-result-value {
        font-size: 25px;
        color: #50e7ff;
        font-weight: 800;
        margin-top: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------------------
    # HERO
    # --------------------------------------------------
    st.markdown("""
    <div class="math-hero">
        <div class="math-eyebrow">AnuskaSync / MATHEMATICAL CORE</div>
        <div class="math-heading">
            Where music meets<br>
            <span style="color:#b58aff">vector mathematics.</span>
        </div>
        <div class="math-muted">
            Every song becomes a point in a four-dimensional feature space.
            By comparing vector directions, AnuskaSync estimates which songs
            have the most similar musical feature profiles.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## The mathematical journey")
    st.markdown(
        '<div class="math-muted">From numerical song features to a ranked '
        'list of recommendations — here is how the algorithm works.</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------
    # 1. VECTOR REPRESENTATION
    # --------------------------------------------------
    st.markdown('<div class="math-panel">', unsafe_allow_html=True)
    st.markdown(
        '<div class="math-number">01 / REPRESENTATION</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Represent every song as a vector")

    st.markdown("""
    A song is represented using four numerical features, each assumed
    to be on a scale from 0 to 1:

    - **Energy (E):** how energetic the song is.
    - **Danceability (D):** how suitable its rhythmic properties are for dancing.
    - **Acousticness (A):** the estimated degree of acoustic character.
    - **Valence (V):** the musical positivity conveyed by the track.
    """)

    st.latex(r"\mathbf{x} = [E, D, A, V]")

    st.markdown("For example, consider this illustrative feature vector:")
    st.latex(r"\mathbf{x}_A = [0.50, 0.55, 0.32, 0.66]")

    st.markdown("""
    <div class="math-callout">
        <b>Why vectors?</b><br>
        They transform songs into comparable numerical objects. We can then
        apply linear algebra to compare their feature profiles.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------
    # 2. DOT PRODUCT
    # --------------------------------------------------
    st.markdown('<div class="math-panel">', unsafe_allow_html=True)
    st.markdown(
        '<div class="math-number">02 / ALIGNMENT</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Dot product")

    st.markdown("""
    The dot product multiplies corresponding components of two vectors
    and adds the results. It is a fundamental ingredient of cosine similarity.
    """)

    st.latex(
        r"\mathbf{A}\cdot\mathbf{B}"
        r"=\sum_{i=1}^{n}a_i b_i"
    )

    st.markdown("**Worked example**")

    st.latex(
        r"\begin{aligned}"
        r"\mathbf{A}&=[1,2,3]\\"
        r"\mathbf{B}&=[4,5,6]\\"
        r"\mathbf{A}\cdot\mathbf{B}"
        r"&=1(4)+2(5)+3(6)\\"
        r"&=4+10+18=32"
        r"\end{aligned}"
    )

    st.markdown("""
    <div class="math-callout">
        <b>In AnuskaSync:</b> the dot product combines the four corresponding
        song features into one numerical quantity. By itself, it is affected
        by vector magnitude, so we normalize it when calculating cosine similarity.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------
    # 3. VECTOR NORM
    # --------------------------------------------------
    st.markdown('<div class="math-panel">', unsafe_allow_html=True)
    st.markdown(
        '<div class="math-number">03 / MAGNITUDE</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Vector norm")

    st.markdown("""
    The Euclidean norm measures the length or magnitude of a vector.
    """)

    st.latex(
        r"\|\mathbf{A}\|"
        r"=\sqrt{\sum_{i=1}^{n}a_i^2}"
    )

    st.markdown("For the vector A = [3, 4]:")

    st.latex(
        r"\|\mathbf{A}\|"
        r"=\sqrt{3^2+4^2}"
        r"=\sqrt{25}=5"
    )

    st.markdown("""
    <div class="math-callout">
        <b>In AnuskaSync:</b> the norms of both song vectors form the
        denominator of cosine similarity. This helps compare directions
        rather than simply rewarding songs with larger vector magnitudes.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------
    # 4. COSINE SIMILARITY
    # --------------------------------------------------
    st.markdown('<div class="math-panel">', unsafe_allow_html=True)
    st.markdown(
        '<div class="math-number">04 / THE CORE ALGORITHM</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Cosine similarity")

    st.markdown("""
    Cosine similarity measures the cosine of the angle between two nonzero
    vectors. It is the main score used by our recommendation algorithm.
    """)

    st.latex(
        r"\operatorname{cosSim}(\mathbf{A},\mathbf{B})"
        r"=\frac{\mathbf{A}\cdot\mathbf{B}}"
        r"{\|\mathbf{A}\|\|\mathbf{B}\|}"
    )

    st.markdown("**Interpretation for nonzero vectors:**")

    meaning_col1, meaning_col2, meaning_col3 = st.columns(3)

    with meaning_col1:
        st.markdown("""
        <div class="math-result">
            <div class="math-result-label">SAME DIRECTION</div>
            <div class="math-result-value">+1</div>
            <div class="math-muted">Maximum similarity</div>
        </div>
        """, unsafe_allow_html=True)

    with meaning_col2:
        st.markdown("""
        <div class="math-result">
            <div class="math-result-label">PERPENDICULAR</div>
            <div class="math-result-value">0</div>
            <div class="math-muted">Zero cosine similarity</div>
        </div>
        """, unsafe_allow_html=True)

    with meaning_col3:
        st.markdown("""
        <div class="math-result">
            <div class="math-result-label">OPPOSITE DIRECTION</div>
            <div class="math-result-value">−1</div>
            <div class="math-muted">Opposite vectors</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="math-callout">
        <b>Important:</b> our four song features are nonnegative, so valid
        nonzero song vectors have cosine similarities between 0 and 1.
        The −1 case is part of the general mathematical definition, but
        it does not normally occur with these features.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------
    # 5. ANGLE AND ORTHOGONALITY
    # --------------------------------------------------
    angle_col, ortho_col = st.columns(2, gap="large")

    with angle_col:
        st.markdown('<div class="math-panel">', unsafe_allow_html=True)
        st.markdown(
            '<div class="math-number">05 / GEOMETRY</div>',
            unsafe_allow_html=True,
        )
        st.markdown("### Angle between vectors")
        st.markdown("The angle describes how closely the directions align.")
        st.latex(
            r"\theta=\cos^{-1}\left("
            r"\frac{\mathbf{A}\cdot\mathbf{B}}"
            r"{\|\mathbf{A}\|\|\mathbf{B}\|}\right)"
        )
        st.markdown("""
        - Smaller angle → vectors point in more similar directions.
        - A zero-degree angle → same direction.
        - A 90-degree angle → perpendicular vectors.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with ortho_col:
        st.markdown('<div class="math-panel">', unsafe_allow_html=True)
        st.markdown(
            '<div class="math-number">06 / PERPENDICULARITY</div>',
            unsafe_allow_html=True,
        )
        st.markdown("### Orthogonality")
        st.markdown("Two vectors are orthogonal when their dot product is zero.")
        st.latex(r"\mathbf{A}\cdot\mathbf{B}=0")
        st.markdown("""
        Example: A = [1, 0] and B = [0, 1].

        Their dot product is 1(0) + 0(1) = 0, so the vectors are
        perpendicular.
        """)
        st.markdown("""
        <div class="math-callout">
            Orthogonality is an important concept to demonstrate in the
            mathematics section. It is not an extra filter used by the
            current recommendation ranking.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------
    # LIVE INTERACTIVE CALCULATOR
    # --------------------------------------------------
    st.markdown("## 🧪 Interactive vector laboratory")
    st.markdown("""
    Choose two songs from your current dataset and inspect their vectors,
    dot product, norms, cosine similarity, and angle. This is a live
    calculation using the feature values currently loaded by the app.
    """)

    calc_left, calc_right = st.columns(2)

    with calc_left:
        song_a_title = st.selectbox(
            "Vector A — first song",
            songs["title"].tolist(),
            index=songs["title"].tolist().index(selected_title),
            key="math_song_a",
        )

    with calc_right:
        song_b_title = st.selectbox(
            "Vector B — comparison song",
            songs["title"].tolist(),
            index=min(1, len(songs) - 1),
            key="math_song_b",
        )

    song_a = songs[songs["title"] == song_a_title].iloc[0]
    song_b = songs[songs["title"] == song_b_title].iloc[0]

    vector_a = song_a[FEATURES].to_numpy(dtype=float)
    vector_b = song_b[FEATURES].to_numpy(dtype=float)

    dot = float(np.dot(vector_a, vector_b))
    norm_a = float(np.linalg.norm(vector_a))
    norm_b = float(np.linalg.norm(vector_b))
    denominator = norm_a * norm_b

    if denominator > 0:
        cosine = float(np.clip(dot / denominator, -1.0, 1.0))
        angle = math.degrees(math.acos(cosine))
        cosine_text = f"{cosine:.4f}"
        angle_text = f"{angle:.2f}°"
    else:
        cosine = None
        angle = None
        cosine_text = "Undefined"
        angle_text = "Undefined"

    with st.container(border=True):
        st.markdown("### Your calculation")

        vcol_a, vcol_b = st.columns(2)

        with vcol_a:
            st.markdown(f"**A — {song_a_title}**")
            st.code(
                "[" + ", ".join(f"{v:.3f}" for v in vector_a) + "]"
            )

        with vcol_b:
            st.markdown(f"**B — {song_b_title}**")
            st.code(
                "[" + ", ".join(f"{v:.3f}" for v in vector_b) + "]"
            )

        r1, r2, r3, r4 = st.columns(4)

        r1.metric("Dot product", f"{dot:.4f}")
        r2.metric("Norm of A", f"{norm_a:.4f}")
        r3.metric("Norm of B", f"{norm_b:.4f}")
        r4.metric("Angle", angle_text)

        st.markdown("#### Cosine similarity")
        st.latex(
            r"\frac{" + f"{dot:.4f}" + r"}{"
            + f"{norm_a:.4f}"
            + r"\times "
            + f"{norm_b:.4f}"
            + "}"
            + "="
            + (f"{cosine:.4f}" if cosine is not None else r"\text{undefined}")
        )

        if cosine is not None:
            st.progress(max(0.0, min(1.0, cosine)))
            st.markdown(
                f"**Result:** cosine similarity = `{cosine:.4f}` "
                f"({cosine * 100:.2f}% when displayed on a 0–100 scale)."
            )
            st.caption(
                "This percentage is a display conversion of cosine similarity, "
                "not a probability that you will like the song."
            )
        else:
            st.warning(
                "Cosine similarity and the angle are undefined when either "
                "vector has zero magnitude."
            )

        st.markdown("#### Calculation breakdown")

        st.latex(
            r"A\cdot B="
            + "+".join(
                f"({a:.2f}\\times{b:.2f})"
                for a, b in zip(vector_a, vector_b)
            )
            + f"={dot:.4f}"
        )

        st.latex(
            r"\|A\|=\sqrt{"
            + "+".join(f"{x:.2f}^2" for x in vector_a)
            + f"}}={norm_a:.4f}"
        )

        st.latex(
            r"\|B\|=\sqrt{"
            + "+".join(f"{x:.2f}^2" for x in vector_b)
            + f"}}={norm_b:.4f}"
        )

    # --------------------------------------------------
    # LIVE MATHEMATICAL BREAKDOWN FOR THE PROJECT DEMO
    # --------------------------------------------------
    st.markdown("## 🧮 Live mathematical breakdown")
    st.markdown("Trace every multiplication, norm, denominator, and final cosine score. The worked vector A starts with the example used in our project explanation.")

    demo_a = np.array([0.50, 0.55, 0.32, 0.66], dtype=float)
    breakdown_titles = songs["title"].astype(str).tolist()
    default_b_index = min(1, len(breakdown_titles) - 1)
    breakdown_b_title = st.selectbox(
        "Choose comparison song B",
        breakdown_titles,
        index=default_b_index,
        key="live_breakdown_song_b",
    )
    breakdown_b_row = songs[songs["title"].astype(str) == breakdown_b_title].iloc[0]
    demo_b = breakdown_b_row[FEATURES].to_numpy(dtype=float)
    term_values = demo_a * demo_b
    demo_dot = float(np.dot(demo_a, demo_b))
    demo_norm_a = float(np.linalg.norm(demo_a))
    demo_norm_b = float(np.linalg.norm(demo_b))
    demo_denom = demo_norm_a * demo_norm_b
    demo_cosine = float(np.clip(demo_dot / demo_denom, -1.0, 1.0)) if demo_denom > 0 else None

    st.markdown("**Vector A — fixed worked example**")
    st.latex(r"A=(0.50,\;0.55,\;0.32,\;0.66)")
    st.markdown(f"**Vector B — {html.escape(breakdown_b_title)}**")
    st.latex("B=(" + ",\;".join(f"{x:.3f}" for x in demo_b) + ")")

    breakdown_cols = st.columns(4)
    feature_labels = ["Energy", "Danceability", "Acousticness", "Valence"]
    for col, label, a_value, b_value, term in zip(breakdown_cols, feature_labels, demo_a, demo_b, term_values):
        with col:
            st.markdown(f"**{label}**")
            st.code(f"{a_value:.2f} × {b_value:.3f}\n= {term:.4f}")

    st.markdown("#### Step 1 — Add the dot-product terms")
    st.latex(r"A\cdot B=" + "+".join(f"({a:.2f}\times{b:.3f})" for a, b in zip(demo_a, demo_b)) + f"={demo_dot:.5f}")
    st.markdown("#### Step 2 — Calculate both vector norms")
    st.latex(r"\|A\|=\sqrt{0.50^2+0.55^2+0.32^2+0.66^2}" + f"={demo_norm_a:.5f}")
    st.latex(r"\|B\|=\sqrt{" + "+".join(f"{x:.3f}^2" for x in demo_b) + f"}}={demo_norm_b:.5f}")
    st.markdown("#### Step 3 — Multiply the norms and divide")
    if demo_cosine is not None:
        st.latex(r"\operatorname{cosSim}(A,B)=\frac{A\cdot B}{\|A\|\,\|B\|}=\frac{" + f"{demo_dot:.5f}" + r"}{" + f"{demo_norm_a:.5f}\times{demo_norm_b:.5f}" + r"}= " + f"{demo_cosine:.5f}")
        st.success(f"Final cosine similarity: {demo_cosine:.5f}. This is a vector-similarity score, not a probability of liking the song.")
    else:
        st.warning("Cosine similarity is undefined if either vector has zero magnitude.")

    st.divider()

    # --------------------------------------------------
    # COMPARE COSINE SIMILARITY WITH EUCLIDEAN DISTANCE
    # --------------------------------------------------
    st.markdown("## ⚖️ Compare two recommendation methods")
    st.markdown("Cosine similarity compares vector **direction**; Euclidean distance measures straight-line **separation** in feature space. Both methods use the same four features, but can rank songs differently.")
    compare_title = st.selectbox(
        "Reference song for method comparison",
        breakdown_titles,
        index=breakdown_titles.index(selected_title) if selected_title in breakdown_titles else 0,
        key="method_compare_song",
    )
    compare_row = songs[songs["title"].astype(str) == compare_title].iloc[0]
    compare_vector = compare_row[FEATURES].to_numpy(dtype=float)
    compare_matrix = songs[FEATURES].to_numpy(dtype=float)
    compare_norms = np.linalg.norm(compare_matrix, axis=1) * np.linalg.norm(compare_vector)
    compare_dots = compare_matrix @ compare_vector
    compare_cos = np.divide(compare_dots, compare_norms, out=np.zeros(len(songs), dtype=float), where=compare_norms > 0)
    compare_dist = np.linalg.norm(compare_matrix - compare_vector, axis=1)
    method_df = songs[["title", "artist"]].copy()
    method_df["Cosine similarity"] = compare_cos
    method_df["Euclidean distance"] = compare_dist
    method_df = method_df[method_df["title"].astype(str) != compare_title]
    method_df["Cosine rank"] = method_df["Cosine similarity"].rank(method="first", ascending=False).astype(int)
    method_df["Distance rank"] = method_df["Euclidean distance"].rank(method="first", ascending=True).astype(int)
    method_df = method_df.sort_values("Cosine rank")
    cm1, cm2 = st.columns(2)
    with cm1:
        st.markdown('<div class="math-panel">', unsafe_allow_html=True)
        st.markdown("### Cosine similarity")
        st.latex(r"\operatorname{cosSim}(A,B)=\frac{A\cdot B}{\|A\|\,\|B\|}")
        st.markdown("Higher is better. It focuses on the angle/direction between vectors and is less affected by their overall magnitude.")
        st.markdown('</div>', unsafe_allow_html=True)
    with cm2:
        st.markdown('<div class="math-panel">', unsafe_allow_html=True)
        st.markdown("### Euclidean distance")
        st.latex(r"d(A,B)=\sqrt{\sum_i(a_i-b_i)^2}")
        st.markdown("Lower is better. It measures the straight-line distance between the feature points, so differences in component values directly matter.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("#### Ranking comparison")
    st.dataframe(
        method_df[["title", "artist", "Cosine similarity", "Cosine rank", "Euclidean distance", "Distance rank"]].head(10).style.format({"Cosine similarity": "{:.4f}", "Euclidean distance": "{:.4f}"}),
        use_container_width=True,
        hide_index=True,
    )
    st.caption("Cosine rank 1 is the highest cosine score; distance rank 1 is the smallest Euclidean distance. Different rankings are possible because the measures capture different geometry.")

    st.divider()

    # --------------------------------------------------
    # PERSONALIZED FEATURE WEIGHTS
    # --------------------------------------------------
    st.markdown("## 🎚️ Personalized feature weights")
    st.markdown("Prioritize the features that matter to you. We apply the square root of each nonnegative weight to its feature component before cosine similarity. This makes the resulting dot product equivalent to a weighted dot product, then cosine normalization is applied.")
    weight_cols = st.columns(4)
    weight_values = {}
    weight_defaults = {"energy": 1.0, "danceability": 1.0, "acousticness": 1.0, "valence": 1.0}
    for col, feature, label in zip(weight_cols, FEATURES, feature_labels):
        with col:
            weight_values[feature] = st.slider(label, 0.0, 3.0, weight_defaults[feature], 0.1, key=f"weight_{feature}", help="0 ignores this feature; larger values give it more influence.")
    weights = np.array([weight_values[f] for f in FEATURES], dtype=float)
    if not np.any(weights > 0):
        st.warning("Set at least one feature weight above zero to calculate recommendations.")
    else:
        sqrt_weights = np.sqrt(weights)
        weighted_matrix = compare_matrix * sqrt_weights
        weighted_target = compare_vector * sqrt_weights
        weighted_denoms = np.linalg.norm(weighted_matrix, axis=1) * np.linalg.norm(weighted_target)
        weighted_dots = weighted_matrix @ weighted_target
        weighted_scores = np.divide(weighted_dots, weighted_denoms, out=np.zeros(len(songs), dtype=float), where=weighted_denoms > 0)
        weighted_df = songs[["title", "artist"]].copy()
        weighted_df["Weighted cosine score"] = weighted_scores
        weighted_df = weighted_df[weighted_df["title"].astype(str) != compare_title]
        weighted_df = weighted_df.sort_values("Weighted cosine score", ascending=False).head(5).reset_index(drop=True)
        st.markdown("**Normalized weight proportions**")
        total_weight = float(weights.sum())
        if total_weight > 0:
            st.caption(" · ".join(f"{label}: {weight_values[f] / total_weight:.0%}" for f, label in zip(FEATURES, feature_labels)))
        st.markdown(f"### Top {len(weighted_df)} personalized matches for **{html.escape(compare_title)}**")
        if weighted_df.empty:
            st.info("Add more songs to the dataset to generate alternative matches.")
        else:
            st.dataframe(weighted_df.style.format({"Weighted cosine score": "{:.4f}"}), use_container_width=True, hide_index=True)
        with st.expander("See the weighted-vector transformation"):
            st.latex(r"A_w=(\sqrt{w_E}E,\sqrt{w_D}D,\sqrt{w_A}A,\sqrt{w_V}V)")
            st.code("Weights = (" + ", ".join(f"{weights[i]:.2f}" for i in range(4)) + ")\nSquare-root weights = (" + ", ".join(f"{sqrt_weights[i]:.3f}" for i in range(4)) + ")")
            st.caption("Multiplying by √weight ensures each feature contributes in proportion to its chosen weight in the weighted dot product and squared norm.")

    st.divider()

    # --------------------------------------------------
    # RECOMMENDATION QUALITY TESTING
    # --------------------------------------------------
    st.markdown("## 🧪 Recommendation quality testing")
    st.markdown("This built-in test checks the data's closest and most separated song pairs, compares the two ranking methods, and lets you perturb one feature to observe how recommendations change. These are dataset-derived checks, not human-verified genre or preference labels.")
    quality_matrix = songs[FEATURES].to_numpy(dtype=float)
    if len(songs) >= 2:
        quality_cosine = np.zeros((len(songs), len(songs)), dtype=float)
        quality_norms = np.linalg.norm(quality_matrix, axis=1)
        quality_denominator = quality_norms[:, None] * quality_norms[None, :]
        quality_dots = quality_matrix @ quality_matrix.T
        quality_cosine = np.divide(quality_dots, quality_denominator, out=np.zeros_like(quality_dots), where=quality_denominator > 0)
        quality_distance = np.linalg.norm(quality_matrix[:, None, :] - quality_matrix[None, :, :], axis=2)
        np.fill_diagonal(quality_cosine, -np.inf)
        np.fill_diagonal(quality_distance, np.inf)
        close_i, close_j = np.unravel_index(np.argmax(quality_cosine), quality_cosine.shape)
        far_i, far_j = np.unravel_index(np.argmin(quality_cosine), quality_cosine.shape)
        qa, qb, qc = st.columns(3)
        with qa:
            st.markdown(f'<div class="math-result"><div class="math-result-label">CLOSEST DIRECTIONAL PAIR</div><div style="font-size:15px;font-weight:800;margin-top:8px">{html.escape(str(songs.iloc[close_i]["title"]))}</div><div class="math-muted">↔ {html.escape(str(songs.iloc[close_j]["title"]))}</div><div class="math-result-value">{quality_cosine[close_i, close_j]:.3f}</div></div>', unsafe_allow_html=True)
        with qb:
            st.markdown(f'<div class="math-result"><div class="math-result-label">MOST SEPARATED BY COSINE</div><div style="font-size:15px;font-weight:800;margin-top:8px">{html.escape(str(songs.iloc[far_i]["title"]))}</div><div class="math-muted">↔ {html.escape(str(songs.iloc[far_j]["title"]))}</div><div class="math-result-value">{quality_cosine[far_i, far_j]:.3f}</div></div>', unsafe_allow_html=True)
        with qc:
            st.markdown(f'<div class="math-result"><div class="math-result-label">DATASET SIZE</div><div class="math-result-value">{len(songs)}</div><div class="math-muted">Songs available for pairwise checks</div></div>', unsafe_allow_html=True)

        st.markdown("#### Feature sensitivity experiment")
        perturb_song = st.selectbox("Song to perturb", breakdown_titles, key="quality_perturb_song")
        perturb_feature = st.selectbox("Feature to change", FEATURES, format_func=lambda x: x.replace("_", " ").title(), key="quality_perturb_feature")
        perturb_amount = st.slider("Change feature value", -0.5, 0.5, 0.2, 0.05, key="quality_perturb_amount")
        original_row = songs[songs["title"].astype(str) == perturb_song].iloc[0]
        original_vector = original_row[FEATURES].to_numpy(dtype=float)
        changed_vector = original_vector.copy()
        feature_index = FEATURES.index(perturb_feature)
        changed_vector[feature_index] = np.clip(changed_vector[feature_index] + perturb_amount, 0.0, 1.0)
        original_norms = np.linalg.norm(quality_matrix, axis=1) * np.linalg.norm(original_vector)
        changed_norms = np.linalg.norm(quality_matrix, axis=1) * np.linalg.norm(changed_vector)
        original_scores = np.divide(quality_matrix @ original_vector, original_norms, out=np.zeros(len(songs)), where=original_norms > 0)
        changed_scores = np.divide(quality_matrix @ changed_vector, changed_norms, out=np.zeros(len(songs)), where=changed_norms > 0)
        perturb_df = songs[["title", "artist"]].copy()
        perturb_df["Before"] = original_scores
        perturb_df["After change"] = changed_scores
        perturb_df["Score change"] = changed_scores - original_scores
        perturb_df = perturb_df[perturb_df["title"].astype(str) != perturb_song]
        perturb_df["Before rank"] = perturb_df["Before"].rank(method="first", ascending=False).astype(int)
        perturb_df["After rank"] = perturb_df["After change"].rank(method="first", ascending=False).astype(int)
        perturb_df["Rank shift"] = perturb_df["Before rank"] - perturb_df["After rank"]
        perturb_df = perturb_df.sort_values("After rank").head(10)
        st.caption(f"Changed {perturb_feature.replace('_', ' ')} from {original_vector[feature_index]:.3f} to {changed_vector[feature_index]:.3f}. Feature values are clamped to the dataset's expected 0–1 range for this experiment.")
        st.dataframe(perturb_df.style.format({"Before": "{:.4f}", "After change": "{:.4f}", "Score change": "{:+.4f}"}), use_container_width=True, hide_index=True)
        st.caption("Quality note: without independent human relevance labels, this validates calculations and sensitivity—not whether listeners will personally like the recommendations. For a formal evaluation, annotate similar/dissimilar pairs and report precision@5 or ranking agreement.")
    else:
        st.info("Add at least two songs to the collection to run pairwise quality checks.")

    # --------------------------------------------------
    # THE TOP FIVE ALGORITHM
    # --------------------------------------------------
    st.markdown("## ⚙️ How AnuskaSync generates recommendations")

    steps = [
        (
            "01",
            "Represent",
            "Represent each song using the same four numerical features.",
        ),
        (
            "02",
            "Compare",
            "Calculate cosine similarity between the selected song and every other song.",
        ),
        (
            "03",
            "Exclude",
            "Remove the selected song from its own candidate recommendations.",
        ),
        (
            "04",
            "Rank",
            "Sort the remaining songs by cosine similarity, highest first.",
        ),
        (
            "05",
            "Recommend",
            "Return the top five songs, or fewer if fewer alternatives exist.",
        ),
    ]

    for number, title, description in steps:
        st.markdown(f"""
        <div class="math-panel" style="padding:15px 19px">
            <div style="display:flex;gap:16px;align-items:flex-start">
                <div style="font-size:22px;font-weight:900;color:#51e6ff">
                    {number}
                </div>
                <div>
                    <div style="font-weight:800;font-size:17px">{title}</div>
                    <div class="math-muted">{description}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Why the feature data matters")
    st.markdown("""
    Cosine similarity compares the directions of feature vectors. It does not
    automatically know musical genre, lyrics, artist identity, or a listener's
    personal preferences. Recommendations are meaningful only to the extent
    that the chosen features capture useful musical similarities.

    For a stronger project evaluation, test the recommendations on multiple
    songs, verify the numerical calculations independently, and explain the
    limitations of the dataset.
    """)

    st.success(
        "AnuskaSync combines vector representation, dot products, norms, "
        "angles, cosine similarity, and ranking into one recommendation workflow."
    )


# ==================================================
# FOOTER
# ==================================================
st.markdown("""
<div class="footer">
    AnuskaSync · MUSIC MEETS MATHEMATICS<br>
    VECTOR SPACE / COSINE SIMILARITY / MUSIC DISCOVERY
</div>
""", unsafe_allow_html=True)
