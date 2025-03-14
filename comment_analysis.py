import json
from transformers import pipeline

# Initialize the sentiment analysis pipeline
sentiment_analysis = pipeline("sentiment-analysis")
feature_extraction = pipeline("feature-extraction", model="distilbert-base-uncased")

def extract_features_from_comment(comment):
    # Use DistilBERT to extract features from the comment
    features = feature_extraction(comment)
    # Process the features to extract liked and disliked genres, actors, and directors
    liked_genres = []
    disliked_genres = []
    liked_actors = []
    disliked_actors = []
    liked_directors = []
    disliked_directors = []

    # Example processing logic (you need to adapt this based on your specific requirements)
    for feature in features[0]:
        if feature['token'] in ['genre', 'genres']:
            if feature['score'] > 0.7:
                liked_genres.append(feature['token'])
            else:
                disliked_genres.append(feature['token'])
        elif feature['token'] in ['actor', 'actors']:
            if feature['score'] > 0.7:
                liked_actors.append(feature['token'])
            else:
                disliked_actors.append(feature['token'])
        elif feature['token'] in ['director', 'directors']:
            if feature['score'] > 0.7:
                liked_directors.append(feature['token'])
            else:
                disliked_directors.append(feature['token'])

    return {
        'liked_genres': liked_genres,
        'disliked_genres': disliked_genres,
        'liked_actors': liked_actors,
        'disliked_actors': disliked_actors,
        'liked_directors': liked_directors,
        'disliked_directors': disliked_directors
}

def update_user_preferences(username, comment, users_file):
    # Load existing users data
    with open(users_file, 'r', encoding='utf-8') as f:
        users = json.load(f)

    # Ensure the user exists in the data
    if username not in users:
        users[username] = {
            "completed_cold_start": False,
            "preferences": {
                "liked": [],
                "disliked": []
            },
            "comments": []
        }

    # Analyze the sentiment of the comment
    result = sentiment_analysis(comment)[0]
    sentiment = result['label']
    score = result['score']

    # Extract features from the comment
    features = extract_features_from_comment(comment)

    # Update user preferences based on the sentiment and extracted features
    if sentiment == 'POSITIVE' and score > 0.7:
        users[username]["preferences"]["liked"].extend(features['liked_genres'])
        users[username]["preferences"]["liked"].extend(features['liked_actors'])
        users[username]["preferences"]["liked"].extend(features['liked_directors'])
    elif sentiment == 'NEGATIVE' and score > 0.7:
        users[username]["preferences"]["disliked"].extend(features['disliked_genres'])
        users[username]["preferences"]["disliked"].extend(features['disliked_actors'])
        users[username]["preferences"]["disliked"].extend(features['disliked_directors'])

    # Save the updated users data
    with open(users_file, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)

    return users[username]["preferences"]