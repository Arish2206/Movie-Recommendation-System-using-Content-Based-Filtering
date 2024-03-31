import pandas as pd
import streamlit as st
import pickle
import requests

# Function to fetch movie poster from API
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=0902a537c1adfd0ea0411e30ae682455&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Function to fetch movie details from API
def fetch_movie_details(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=0902a537c1adfd0ea0411e30ae682455&language=en-US'.format(movie_id))
    data = response.json()
    return data

# Function to recommend similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # Fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Add some custom CSS for background and other styling
st.markdown(
    """
    <style>
        body {
            background-color: #0f2027;
            background-image: linear-gradient(to bottom, #203a43, #2c5364);
            font-family: 'Arial', sans-serif;
            color: #ffffff;
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }
        .stApp {
            padding: 1rem;
        }
        .stTitle {
            color: #FF5733;
            font-size: 36px;
            text-align: center;
            margin-bottom: 20px;
        }
        .stSelectbox {
            font-size: 18px;
            color: #ffffff;
        }
        .stButton button {
            background-color: #FF5733;
            color: white;
            font-weight: bold;
            font-size: 16px;
            border-radius: 5px;
            padding: 8px 20px;
            margin-top: 20px;
        }
        .stButton button:hover {
            background-color: #d93c17;
        }
        .stImage {
            border-radius: 5px;
        }
        .stText {
            font-size: 20px;
            color: #ffffff;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Frontend design
st.markdown("<div class='stApp'>", unsafe_allow_html=True)
st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
    'Select the Movie',
    movies['title'].values
)

# Fetch movie details from API and display the description and poster
selected_movie_id = movies[movies['title'] == selected_movie_name].iloc[0]['movie_id']
movie_details = fetch_movie_details(selected_movie_id)
st.subheader("Description:")
st.write(movie_details['overview'])
st.subheader("Movie Poster:")
st.image(fetch_poster(selected_movie_id), use_column_width=True)

if st.button('Recommend'):
    st.markdown("<div class='stTitle'>Recommended Movies</div>", unsafe_allow_html=True)
    names, posters = recommend(selected_movie_name)
    columns = st.columns(5)  # Create 5 equal-width columns
    for i, col in enumerate(columns):
        col.image(posters[i], use_column_width=True)
        col.markdown("<div class='stText'>" + names[i] + "</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
