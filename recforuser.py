import json
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

profile = "Jasonsoo"

ids = user_preferences.get(profile, {}).get("liked", [])
disliked = user_preferences.get(profile, {}).get("disliked", [])

movie_ids = ids
top_k_movies, scores = get_movie_recommendations(movie_ids, movie_embeddings, top_k=5)

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

csv_filepath = 'cleaned_movies.csv'
file_path = 'node_index_to_imdb.json'
data = read_json_file(file_path)

# Step 7: Display the recommendations
print(f"\nTop 5 similar movies to Movies {movie_ids}:")
# for idx, score in zip(top_k_movies, scores):
#     print(f"Movie {idx.item()} with similarity score: {score.item():.4f}")

# Step 8: Load metadata for genre information
df = pd.read_csv("cleaned_movies.csv")
imdb_to_metadata = dict(zip(df["movie_id"], df["genre"]))  # Map IMDb ID to Genre

for movie_id in movie_ids:
    name = get_name_by_id(csv_filepath, data[str(movie_id)])
    genre = imdb_to_metadata.get(data[str(movie_id)], "Unknown")
    print(f"Movie {movie_id} = {name} (Genre: {genre})")

# Example of displaying genre for the recommended movies
for idx, score in zip(top_k_movies, scores):
    genre = imdb_to_metadata.get(data[str(idx.item())], "Unknown")
    name = get_name_by_id(csv_filepath, data[str(idx.item())])
    print(f"({name}) Movie {idx.item()} with similarity score: {score.item():.4f}, Genre: {genre}")

