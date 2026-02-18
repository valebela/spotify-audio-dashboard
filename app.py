#please look at READ.md first.
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#Setting up the page
st.set_page_config(
    page_title="Spotify Audio Features Dashboard",
    layout="wide"
)

st.title("Spotify Audio Features Dashboard")

st.caption(
    "Vale Rodriguez • 2026  \n"
    "Use the sidebar on the left to filter tracks by genre and artist."
)

#The purpose of the dash!
st.markdown(
    """
    ### Dashboard Purpose
    This dashboard explores how musical characteristics such as tempo, energy,
    danceability, and emotional tone vary across Spotify tracks.

    By filtering the dataset by genre and artist, patterns emerge that help explain
    how different styles of music are structured and experienced.
    """
)


# Loading the data set from Kaggle
@st.cache_data
def load_data():
    return pd.read_csv("dataset.csv")


df = load_data()

#Sidebar
st.sidebar.markdown("##  Filters")
st.sidebar.markdown(
    "Use these controls to explore how audio features change "
    "across genres and artists."
)

# Genre filter
genre = st.sidebar.selectbox(
    " Select Genre",
    ["All"] + sorted(df["track_genre"].dropna().unique().tolist())
)

if genre != "All":
    df = df[df["track_genre"] == genre]

#Artist filter
artist = st.sidebar.selectbox(
    "Select Artist",
    ["All"] + sorted(
        set(";".join(df["artists"].dropna()).split(";"))
    )
)

if artist != "All":
    df = df[df["artists"].str.contains(artist)]

st.sidebar.markdown("---")
st.sidebar.caption("Filters update all charts below")

#Preview of Dataset
st.subheader("Dataset Preview")
st.dataframe(df.head())

col1, col2, col3 = st.columns(3)
col1.metric("Tracks Displayed", len(df))
col2.metric("Average Tempo (BPM)", round(df["tempo"].mean(), 1))
col3.metric("Average Popularity", round(df["popularity"].mean(), 1))

#TEMPO SECTION
st.subheader("🎚 Tempo Overview")
st.caption(
    "This boxplot summarizes the distribution of tempo values across tracks, "
    "highlighting the median and extreme outliers."
)

fig, ax = plt.subplots()
ax.boxplot(df["tempo"], vert=False)
ax.set_xlabel("Tempo (BPM)")

st.pyplot(fig)

st.markdown(
    """
    **Interpretation:**
    - Most tracks fall within a moderate tempo range, suggesting mainstream music
      favors steady, danceable speeds.
    - Extremely fast or slow tracks exist but appear as outliers, indicating they
      are stylistic choices rather than the norm.
    - Filtering by genre reveals clear differences in tempo preferences across
      musical styles.
    """
)

#ENERGY VS DANCEABILITY SECTION
st.subheader("Energy vs Danceability")
st.caption(
    "Each point represents a track. Areas with higher density indicate common "
    "combinations of energy and danceability."
)

fig, ax = plt.subplots()
ax.scatter(
    df["danceability"],
    df["energy"],
    alpha=0.15,
    s=10
)

ax.set_xlabel("Danceability (low → high)")
ax.set_ylabel("Energy (low → high)")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

st.pyplot(fig)

st.markdown(
    """
    **Interpretation:**
    - A dense cluster appears in the upper right region, showing that popular music
      often combines high energy with high danceability.
    - Tracks with low energy rarely score high on danceability, suggesting that
      rhythmic structure alone is not enough to make a song suitable for dancing.
    - This relationship becomes more pronounced in genres designed for movement,
      such as pop and electronic music.
    """
)

#VALENCE DISTRIBUTION SECTION
st.subheader("Valence (Emotional Tone) Distribution")
st.caption(
    "Valence represents the emotional positivity of a track, ranging from sad or "
    "angry to happy or euphoric."
)

fig, ax = plt.subplots()
ax.hist(df["valence"], bins=30)
ax.set_xlabel("Valence (low → high)")
ax.set_ylabel("Number of Tracks")

st.pyplot(fig)

st.markdown(
    """
    **Interpretation:**
    - Most tracks cluster around mid range valence, indicating that mainstream music
      often expresses mixed or neutral emotional tones.
    - Extremely positive or negative moods are less common, possibly because they
      appeal to more niche audiences.
    - Genre filtering significantly shifts this distribution, highlighting how
      emotional expression varies across musical styles.
    """
)

#TOP TRACKS SECTION
st.subheader("Most Popular Tracks")

top_tracks = (
    df[["track_name", "artists", "popularity", "track_genre"]]
    .sort_values(by="popularity", ascending=False)
    .head(10)
)

st.dataframe(top_tracks)

#Footer!
st.markdown("---")
st.caption("Built with Streamlit • Spotify Audio Features Dataset (Kaggle) • Vale Rodriguez")
