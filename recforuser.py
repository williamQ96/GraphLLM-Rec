import json
import csv
import pandas as pd
from reco2 import *

# Function to read the JSON file
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None

# Read the data from the file
data = read_json_file("data/users.json")

# Create a dictionary for storing user preferences
user_preferences = {}

if data:
    # Loop over each user and extract their preferences
    for username, user_data in data.items():
        # Extract the liked and disliked movies for each user
        liked_movies = user_data["preferences"].get("liked", [])
        disliked_movies = user_data["preferences"].get("disliked", [])

        # Add this user's preferences to the dictionary
        user_preferences[username] = {
            "liked": liked_movies,
            "disliked": disliked_movies
        }

def get_name_by_id(csv_filepath, target_id):
    with open(csv_filepath, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row

        # Determine the index of 'ID' and 'Name' columns
        id_index = header.index('movie_id')
        name_index = header.index('movie_name')

        for row in reader:
            if row[id_index] == str(target_id):
                return row[name_index]
    return None

def user_rec(profile):

    ids = user_preferences.get(profile, {}).get("liked", [])
    disliked = user_preferences.get(profile, {}).get("disliked", [])

    movie_ids = ids
    top_k_movies, scores = get_movie_recommendations(movie_ids, movie_embeddings, disliked, top_k=8)

    data = read_json_file('node_index_to_imdb.json')
    df = pd.read_csv("cleaned_movies.csv")



    imdb_to_metadata = dict(zip(df["movie_id"], df["genre"])) # Map IMDb ID to Genre
    imdb_to_metadata2 = dict(zip(df["movie_id"], df["rating"]))
    imdb_to_metadata3 = dict(zip(df["movie_id"], df["year"]))
    imdb_to_metadata4 = dict(zip(df["movie_id"], df["description"]))


    recommendations = []
    for idx in top_k_movies:
        name = get_name_by_id("cleaned_movies.csv", data[str(idx.item())])
        genre = imdb_to_metadata.get(data[str(idx.item())], "Unknown")
        year = imdb_to_metadata3.get(data[str(idx.item())], "Unknown")
        rating = imdb_to_metadata2.get(data[str(idx.item())], "Unknown")
        description = imdb_to_metadata4.get(data[str(idx.item())], "Unknown")
        recommendations.append({
            "id": idx.item(),
            "title": name,
            "genre": genre,
            "year": year,
            "rating": rating,
            "description": description
        })

    return recommendations

