import json
from comment_analysis import update_user_preferences
from enhanced_rec import generate_recommendations

# Hard-coded user data for testing
users_file = "data/users.json"
test_username = "test_user"
test_comment_positive = "I absolutely loved the thrilling action scenes and the deep character development!"
test_comment_negative = "I didn't like the slow pacing and the lack of character depth."

# Initialize user data
def initialize_user_data():
    users = {
        test_username: {
            "completed_cold_start": False,
            "preferences": {
                "liked": [],
                "disliked": []
            },
            "comments": []
        }
    }
    with open(users_file, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)

# Test updating user preferences with a positive comment
def test_update_user_preferences_positive():
    print("Testing positive comment...")
    preferences = update_user_preferences(test_username, test_comment_positive, users_file)
    print("Updated preferences:", preferences)

# Test updating user preferences with a negative comment
def test_update_user_preferences_negative():
    print("Testing negative comment...")
    preferences = update_user_preferences(test_username, test_comment_negative, users_file)
    print("Updated preferences:", preferences)

# Test generating recommendations
def test_generate_recommendations():
    print("Generating recommendations...")
    recommendations = generate_recommendations(test_username, users_file)
    print("Recommendations:", recommendations)

# Run tests
if __name__ == "__main__":
    initialize_user_data()
    test_update_user_preferences_positive()
    test_update_user_preferences_negative()
    test_generate_recommendations()