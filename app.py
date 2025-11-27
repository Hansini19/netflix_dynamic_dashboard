import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Netflix Dynamic Dashboard", layout="wide")

# -------------------------
# 🔴 DYNAMIC DATA GENERATION (NO STATIC CSV)
# -------------------------

@st.cache_data
def load_dynamic_data():
    titles = [
        "Money Heist", "Stranger Things", "Extraction", "RRR", "Wednesday",
        "Jawan", "Lucifer", "Dark", "Peaky Blinders", "The Crown"
    ]

    types = ["Movie", "TV Show"]
    countries = ["India", "United States", "United Kingdom", "Korea", "Spain", "Germany"]
    genres = ["Drama", "Thriller", "Comedy", "Action", "Romance", "Sci-Fi"]

    years = list(range(2015, 2028))  # up to 2027

    np.random.seed(42)

    data = {
        "title": np.random.choice(titles, 200),
        "type": np.random.choice(types, 200),
        "release_year": np.random.choice(years, 200),
        "country": np.random.choice(countries, 200),
        "duration": np.random.randint(30, 180, 200),
        "genre": np.random.choice(genres, 200)
    }

    df = pd.DataFrame(data)
    return df


df = load_dynamic_data()

# -------------------------
# 🎛 SIDEBAR FILTERS
# -------------------------
st.sidebar.title("Filters")

year_range = st.sidebar.slider(
    "Select Release Year Range",
    min_value=2015,
    max_value=2027,
    value=(2017, 2027)
)

selected_type = st.sidebar.multiselect(
    "Select Type",
    options=df["type"].unique(),
    default=df["type"].unique()
)

selected_genre = st.sidebar.multiselect(
    "Select Genre",
    options=df["genre"].unique(),
    default=df["genre"].unique()
)

# FILTER DATA
df_filtered = df[
    (df["release_year"].between(year_range[0], year_range[1])) &
    (df["type"].isin(selected_type)) &
    (df["genre"].isin(selected_genre))
]

# -------------------------
# 📌 KPI SECTION
# -------------------------
st.title("🎬 Netflix Dynamic Movies & Series Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Titles", len(df_filtered))
col2.metric("Movies Count", sum(df_filtered["type"] == "Movie"))
col3.metric("TV Shows Count", sum(df_filtered["type"] == "TV Show"))
col4.metric("Unique Genres", df_filtered["genre"].nunique())

st.markdown("---")

# -------------------------
# 📊 VISUALIZATIONS (8 GRAPHS)
# -------------------------

# 1. Bar Chart - Titles by Year
fig1 = px.bar(df_filtered.groupby("release_year").size().reset_index(name="count"),
              x="release_year", y="count", title="Titles by Release Year")
st.plotly_chart(fig1, use_container_width=True)

# 2. Pie Chart - Movies vs TV Shows
fig2 = px.pie(df_filtered, names="type", title="Distribution: Movies vs TV Shows")
st.plotly_chart(fig2, use_container_width=True)

# 3. Horizontal Bar - Top Genres
fig3 = px.bar(df_filtered.groupby("genre").size().reset_index(name="count"),
              x="count", y="genre", orientation='h', title="Top Genres")
st.plotly_chart(fig3, use_container_width=True)

# 4. Country Distribution
fig4 = px.bar(df_filtered.groupby("country").size().reset_index(name="count"),
              x="country", y="count", title="Titles by Country")
st.plotly_chart(fig4, use_container_width=True)

# 5. Scatter Plot: Duration vs Year
fig5 = px.scatter(df_filtered, x="release_year", y="duration",
                  color="type", title="Duration Trend Over Years")
st.plotly_chart(fig5, use_container_width=True)

# 6. Box Plot - Duration Distribution
fig6 = px.box(df_filtered, x="type", y="duration",
              title="Duration Comparison (Movies vs TV Shows)")
st.plotly_chart(fig6, use_container_width=True)

# 7. Line Chart: Titles Trend
fig7 = px.line(df_filtered.groupby("release_year").size().reset_index(name="count"),
               x="release_year", y="count", title="Trend of Titles Over Time")
st.plotly_chart(fig7, use_container_width=True)

# 8. Heatmap: Genre vs Year
pivot = df_filtered.pivot_table(index="genre", columns="release_year", values="title", aggfunc="count").fillna(0)
fig8 = px.imshow(pivot, title="Heatmap: Genre vs Year")
st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")
st.write("© 2025 - Dynamic Netflix Dashboard | Generated Live (No Static Dataset)")
