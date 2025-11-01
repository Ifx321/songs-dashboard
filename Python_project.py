import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

# --- Page Configuration (App Title & Icon) ---
# THIS MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Music Data Explorer (2000-2020)",
    page_icon="🎵",
    layout="wide"
)

# --- Data Loading (Caching for Performance) ---
@st.cache_data
def load_data():
    file_path = 'songs_2000_2020_50k.csv'
    try:
        df = pd.read_csv(file_path)
        # Convert release date and extract year
        df['release_datetime'] = pd.to_datetime(df['Release Date'], format='%d-%m-%Y', errors='coerce')
        df['release_year'] = df['release_datetime'].dt.year
        # Filter out any potential errors
        df = df.dropna(subset=['release_year'])
        df['release_year'] = df['release_year'].astype(int)
        return df
    except FileNotFoundError:
        st.error(f"Error: The data file '{file_path}' was not found.")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        st.stop()

# Load the data (ONLY ONCE)
df = load_data()


# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
st.sidebar.write("*You can actually play song in here*")

# --- ADD THIS CODE FOR BACKGROUND MUSIC ---
# --- (Examiner's Note: I added .mp3. Make sure your file has the right extension!) ---
try:
    st.sidebar.audio("RXVEN_-_REBOLATON_KLICKAUD.mp3", autoplay=True, loop=True)
except FileNotFoundError:
    st.sidebar.error("Audio file not found. Make sure it's in the folder and has the correct extension.")
# -------------------------------------------

page = st.sidebar.selectbox(
    "Choose a page:",
    [
        "Overview Dashboard",
        "Genre Deep Dive",
        "Feature & Popularity Analysis",
        "Interactive Song Explorer"
    ]
)

# --- Main App Title ---
# (I used your original title here)
st.title("Python Project by Irfan:🎵Songs Analysis From 2000 To 2020")
st.write(f"Currently viewing: **{page}**")
st.markdown("---")

# --- (I moved your data preview to the Overview page) ---

# ==============================================================================
# Page 1: Overview Dashboard
# ==============================================================================
if page == "Overview Dashboard":
    st.header("Main Dashboard: At a Glance")
    
    # --- (Moved your data preview here) ---
    st.subheader("Data Preview and Shape")
    st.dataframe(df.head())
    st.write("Shape of Dataset:", df.shape)
    st.write("Columns:", list(df.columns))
    st.markdown("---")
    
    # --- Key Metrics (KPIs) ---
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Songs", f"{len(df):,}")
    col2.metric("Total Genres", df['Genre'].nunique())
    col3.metric("Total Unique Artists", df['Artist'].nunique())
    col4.metric("Average Popularity", f"{df['Popularity'].mean():.2f}")

    # --- Plot 1: Music Release Trend (Live Altair Chart) ---
    st.subheader("Music Release Trend (2000-2020)")
    
    data_songs_per_year = df.groupby('release_year').size().reset_index(name='song_count')
    
    chart_songs_per_year = alt.Chart(data_songs_per_year).mark_line(point=True).encode(
        x=alt.X('release_year', title='Year', axis=alt.Axis(format='d')), # 'd' format removes comma
        y=alt.Y('song_count', title='Number of Songs Released'),
        tooltip=[alt.Tooltip('release_year', title='Year'), alt.Tooltip('song_count', title='Songs')]
    ).interactive()
    
    st.altair_chart(chart_songs_per_year, use_container_width=True)

    # --- Plot 2: Genre Distribution (Live Altair Chart) ---
    st.subheader("Genre Distribution")

    chart_genre_dist = alt.Chart(df).mark_bar().encode(
        x=alt.X('Genre', title='Genre', sort='-y'), 
        y=alt.Y('count()', title='Number of Songs'),
        tooltip=['Genre', 'count()']
    ).interactive()

    st.altair_chart(chart_genre_dist, use_container_width=True)
    st.markdown("Note: This bar chart shows the total count of songs for each genre.")


# ==============================================================================
# Page 2: Genre Deep Dive
# ==============================================================================
elif page == "Genre Deep Dive":
    st.header("Genre Deep Dive")
 
    st.subheader("Average Popularity by Genre")
    
    avg_popularity_genre = df.groupby('Genre')['Popularity'].mean().reset_index()
    chart_avg_pop = alt.Chart(avg_popularity_genre).mark_bar().encode(
        x=alt.X('Genre', title='Genre', sort='-y'), # Sorts bars from high to low
        y=alt.Y('Popularity', title='Average Popularity Score'),
        tooltip=['Genre', alt.Tooltip('Popularity', format='.2f')]
    ).interactive()
    st.altair_chart(chart_avg_pop, use_container_width=True)
 
    st.subheader("Popularity Trends by Genre (Over Time)")
    
    data_pop_trends = df.groupby(['release_year', 'Genre'])['Popularity'].mean().reset_index()
    
    chart_pop_trends = alt.Chart(data_pop_trends).mark_line(point=True).encode(
        x=alt.X('release_year', title='Year', axis=alt.Axis(format='d')),
        y=alt.Y('Popularity', title='Average Popularity'),
        color=alt.Color('Genre', title='Genre'), # This creates the multiple lines
        tooltip=['release_year', 'Genre', alt.Tooltip('Popularity', format='.2f')]
    ).interactive()
    
    st.altair_chart(chart_pop_trends, use_container_width=True)
    st.markdown("Note: Hover to see details. Click a genre in the legend to hide/show it.")
    

# ==============================================================================
# Page 3: Feature & Popularity Analysis
# ==============================================================================
elif page == "Feature & Popularity Analysis":
    st.header("Feature & Popularity Analysis")
    
    st.markdown("This page explores the relationships between song features.")

    st.subheader("Popularity Score Distribution (Histogram)")

    chart_hist = alt.Chart(df).mark_bar().encode(
        x=alt.X('Popularity', bin=alt.Bin(maxbins=30), title='Popularity Score'), # This makes it a histogram
        y=alt.Y('count()', title='Number of Songs'),
        tooltip=[alt.Tooltip('Popularity', bin=True), 'count()']
    ).interactive()
    st.altair_chart(chart_hist, use_container_width=True)
    st.markdown("Note: This histogram shows a very uniform distribution of popularity.")

    st.subheader("Duration vs. Popularity (Scatter Plot)")
    
    df_sample = df.sample(5000) 
    
    chart_scatter = alt.Chart(df_sample).mark_circle(opacity=0.4).encode(
        x=alt.X('Duration', title='Duration (seconds)'),
        y=alt.Y('Popularity', title='Popularity Score'),
        tooltip=['Title', 'Artist', 'Duration', 'Popularity'] # Great tooltips!
    ).interactive()
    
    st.altair_chart(chart_scatter, use_container_width=True)
    st.markdown(
        """
         This plot is a sample of 5,000 songs. 
        As you can see, there is no clear correlation. 
        Hover over any point to see the song's title.
        """
    )


# ==============================================================================
# Page 4: Interactive Song Explorer
# ==============================================================================
elif page == "Interactive Song Explorer":
    st.header("Interactive Song Explorer")
    st.write("Use the filters in the sidebar to explore the dataset yourself!")
    
    # --- Sidebar Filters ---
    st.sidebar.markdown("---")
    st.sidebar.header("Song Explorer Filters")

    # Filter 1: Genre (Multiselect)
    genres_list = sorted(df['Genre'].unique())
    selected_genres = st.sidebar.multiselect(
        'Select Genres:',
        options=genres_list,
        default=genres_list
    )

    # Filter 2: Year (Slider)
    min_year, max_year = int(df['release_year'].min()), int(df['release_year'].max())
    selected_year_range = st.sidebar.slider(
        'Select Release Year Range:',
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    # Filter 3: Popularity (Slider)
    selected_pop_range = st.sidebar.slider(
        'Select Popularity Range:',
        min_value=0,
        max_value=100,
        value=(50, 100)
    )
    
    # --- Filter Logic ---
    if not selected_genres:
        st.warning("Please select at least one genre.")
        st.stop()
        
    filtered_df = df[
        (df['Genre'].isin(selected_genres)) &
        (df['release_year'] >= selected_year_range[0]) &
        (df['release_year'] <= selected_year_range[1]) &
        (df['Popularity'] >= selected_pop_range[0]) &
        (df['Popularity'] <= selected_pop_range[1])
    ]

    # --- Display Results ---
    st.subheader(f"Found {len(filtered_df)} songs matching your criteria:")
    
    display_cols = ['Title', 'Artist', 'Genre', 'release_year', 'Popularity', 'Duration']
    st.dataframe(filtered_df[display_cols], use_container_width=True)
    st.title(" Enjoy Exploring the Music Data!🎵, Its fun right?! Thanks for Wasting your valuable time in here")