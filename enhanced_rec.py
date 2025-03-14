import json
import pandas as pd
import torch
import torch.nn.functional as F

# Load the GNN model
model = torch.load('hetero_gnn_model.pth')
model.eval()

# Load movie embeddings
movie_embeddings = torch.load("movie_embeddings.pth")

# Load movie details
df = pd.read_csv("cleaned_movies.csv")

def get_movie_details(movie_id):
    movie = df[df['movie_id'] == movie_id].iloc[0]
    return {
        'id': movie_id,
        'title': movie['title'],
        'genre': movie['genre'],
        'director': movie['director_id'],
        'actors': movie['star_id'].split(',')
    }

def rank_movies(user_preferences, movie_ids):
    ranked_movies = []
    for movie_id in movie_ids:
        movie_details = get_movie_details(movie_id)
        score = 0
        if movie_details['genre'] in user_preferences['liked']:
            score += 1
        if movie_details['director'] in user_preferences['liked']:
            score += 1
        if any(actor in user_preferences['liked'] for actor in movie_details['actors']):
            score += 1
        if movie_details['genre'] in user_preferences['disliked']:
            score -= 1
        if movie_details['director'] in user_preferences['disliked']:
            score -= 1
        if any(actor in user_preferences['disliked'] for actor in movie_details['actors']):
            score -= 1
        ranked_movies.append((movie_id, score))
    ranked_movies.sort(key=lambda x: x[1], reverse=True)
    return [movie_id for movie_id, score in ranked_movies]

def generate_recommendations(username, users_file):
    # Load user preferences
    with open(users_file, 'r', encoding='utf-8') as f:
        users = json.load(f)
    user_preferences = users[username]["preferences"]

    # Generate initial recommendations using GNN model
    liked_movie_ids = [movie_id for movie_id in user_preferences['liked'] if isinstance(movie_id, int)]
    disliked_movie_ids = [movie_id for movie_id in user_preferences['disliked'] if isinstance(movie_id, int)]
    initial_recommendations = get_movie_recommendations(liked_movie_ids, movie_embeddings, disliked_movie_ids)

    # Rank the initial recommendations based on user preferences
    final_recommendations = rank_movies(user_preferences, initial_recommendations)

    return final_recommendations

def get_movie_recommendations(liked_movie_ids, movie_embeddings, disliked_movie_ids):
    # Dummy implementation for testing purposes
    # Replace with actual GNN model inference code
    all_movie_ids = list(range(len(movie_embeddings)))
    recommendations = [movie_id for movie_id in all_movie_ids if movie_id not in liked_movie_ids + disliked_movie_ids]
    return recommendations[:10]  # Return top 10 recommendations for testing

# Example usage
if __name__ == "__main__":
    username = "test_user"
    users_file = "data/users.json"
    recommendations = generate_recommendations(username, users_file)
    print("Final Recommendations:", recommendations)