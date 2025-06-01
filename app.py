import streamlit as st
import pandas as pd


ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")

df = pd.merge(ratings, movies, on='movieId')

agg_df = df.groupby(['movieId', 'title', 'genres']).agg(
    avg_rating=('rating', 'mean'),
    rating_count=('rating', 'count')
).reset_index()

agg_df['year'] = agg_df['title'].str.extract(r'\((\d{4})\)').astype('Int64')

st.sidebar.header("Filtri")
min_ratings = st.sidebar.slider("Minimalno število ocen", 1, 500, 10)
selected_genre = st.sidebar.selectbox("Žanr", ['Vsi'] + sorted(set('|'.join(agg_df['genres']).split('|'))))
selected_year = st.sidebar.selectbox("Leto", ['Vsa leta'] + sorted(agg_df['year'].dropna().unique().astype(str)))

filtered_df = agg_df[agg_df['rating_count'] >= min_ratings]

if selected_genre != 'Vsi':
    filtered_df = filtered_df[filtered_df['genres'].str.contains(selected_genre)]

if selected_year != 'Vsa leta':
    filtered_df = filtered_df[agg_df['year'] == int(selected_year)]


top_movies = filtered_df.sort_values(by='avg_rating', ascending=False).head(10)

st.title("Top 10 filmov po povprečni oceni")
st.write("Filtri: minimalno število ocen, žanr, leto")

st.dataframe(top_movies[['title', 'avg_rating', 'rating_count']])
