import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Movie Ratings Analytics",
    page_icon="🎬",
    layout="wide"
)

# Load dataset
df = pd.read_csv("movies.csv")

# Title
st.title("🎬 Movie Ratings Analytics Dashboard")
st.write("Explore movie ratings, genres, revenue and trends.")

# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("🔎 Filters")

# Genre filter
genres = ["All"] + sorted(df["Genre"].unique().tolist())

selected_genre = st.sidebar.selectbox(
    "Select Genre",
    genres
)

# Year filter
min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

selected_years = st.sidebar.slider(
    "Select Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)

# Rating filter
selected_rating = st.sidebar.slider(
    "Minimum Rating",
    0.0,
    10.0,
    0.0,
    0.1
)

# Apply filters
filtered_df = df.copy()

if selected_genre != "All":
    filtered_df = filtered_df[
        filtered_df["Genre"] == selected_genre
    ]

filtered_df = filtered_df[
    (filtered_df["Year"] >= selected_years[0]) &
    (filtered_df["Year"] <= selected_years[1])
]

filtered_df = filtered_df[
    filtered_df["Rating"] >= selected_rating
]

# ---------------- KPI SECTION ----------------

total_movies = len(filtered_df)

average_rating = (
    filtered_df["Rating"].mean()
    if len(filtered_df) > 0
    else 0
)

average_revenue = (
    filtered_df["Revenue"].mean()
    if len(filtered_df) > 0
    else 0
)

highest_rating = (
    filtered_df["Rating"].max()
    if len(filtered_df) > 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🎬 Total Movies",
    total_movies
)

col2.metric(
    "⭐ Average Rating",
    f"{average_rating:.2f}"
)

col3.metric(
    "💰 Average Revenue",
    f"${average_revenue:.1f}M"
)

col4.metric(
    "🏆 Highest Rating",
    f"{highest_rating:.1f}"
)

st.divider()

# ---------------- CHART 1 ----------------

col1, col2 = st.columns(2)

with col1:

    genre_data = (
        filtered_df["Genre"]
        .value_counts()
        .reset_index()
    )

    genre_data.columns = ["Genre", "Movies"]

    fig_genre = px.bar(
        genre_data,
        x="Genre",
        y="Movies",
        title="🎭 Movies by Genre"
    )

    st.plotly_chart(
        fig_genre,
        use_container_width=True
    )

# ---------------- CHART 2 ----------------

with col2:

    fig_rating = px.histogram(
        filtered_df,
        x="Rating",
        nbins=10,
        title="⭐ Rating Distribution"
    )

    st.plotly_chart(
        fig_rating,
        use_container_width=True
    )

# ---------------- CHART 3 ----------------

col1, col2 = st.columns(2)

with col1:

    year_data = (
        filtered_df
        .groupby("Year")
        .size()
        .reset_index(name="Movies")
    )

    fig_year = px.line(
        year_data,
        x="Year",
        y="Movies",
        markers=True,
        title="📅 Movies Released by Year"
    )

    st.plotly_chart(
        fig_year,
        use_container_width=True
    )

# ---------------- CHART 4 ----------------

with col2:

    fig_revenue = px.scatter(
        filtered_df,
        x="Rating",
        y="Revenue",
        size="Votes",
        hover_name="Title",
        title="💰 Revenue vs Rating"
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True
    )

# ---------------- TOP MOVIES ----------------

st.subheader("🏆 Top 10 Highest Rated Movies")

top_movies = (
    filtered_df
    .sort_values("Rating", ascending=False)
    .head(10)
)

st.dataframe(
    top_movies[
        [
            "Title",
            "Year",
            "Genre",
            "Rating",
            "Votes",
            "Revenue"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# ---------------- INSIGHTS ----------------

st.subheader("💡 Key Insights")

if len(filtered_df) > 0:

    best_movie = filtered_df.loc[
        filtered_df["Rating"].idxmax(),
        "Title"
    ]

    highest_revenue_movie = filtered_df.loc[
        filtered_df["Revenue"].idxmax(),
        "Title"
    ]

    best_genre = (
        filtered_df
        .groupby("Genre")["Rating"]
        .mean()
        .idxmax()
    )

    st.write(
        f"🎬 **Highest Rated Movie:** {best_movie}"
    )

    st.write(
        f"💰 **Highest Revenue Movie:** "
        f"{highest_revenue_movie}"
    )

    st.write(
        f"⭐ **Highest Average Rated Genre:** "
        f"{best_genre}"
    )

else:

    st.warning(
        "No movies match the selected filters."
    )

# ---------------- DATASET ----------------

st.subheader("📋 Movie Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)