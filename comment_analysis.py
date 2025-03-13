import json
from transformers import pipeline

# Initialize the sentiment analysis pipeline
sentiment_analysis = pipeline("sentiment-analysis")

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

    # Update user preferences based on the sentiment
    if sentiment == 'POSITIVE' and score > 0.7:
        users[username]["preferences"]["liked"].append(comment)
    elif sentiment == 'NEGATIVE' and score > 0.7:
        users[username]["preferences"]["disliked"].append(comment)

    # Save the updated users data
    with open(users_file, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)

    return users[username]["preferences"]