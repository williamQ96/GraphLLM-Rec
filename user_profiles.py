import json
import os

USER_DATA_FILE = "user_data.json"

def load_user_profile(user_id):
    """Load user profile from stored data."""
    if not os.path.exists(USER_DATA_FILE):
        return {}
    
    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        user_data = json.load(f)
    
    return user_data.get(str(user_id), {})

def update_user_profile(user_id, interactions):
    """Update user profile with new interactions (views, reviews, etc.)."""
    user_data = {}
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            user_data = json.load(f)
    
    user_id = str(user_id)
    if user_id not in user_data:
        user_data[user_id] = {"views": [], "reviews": [], "preferences": {}}
    
    if "views" in interactions:
        user_data[user_id]["views"].extend(interactions["views"])
    if "reviews" in interactions:
        user_data[user_id]["reviews"].extend(interactions["reviews"])
    if "preferences" in interactions:
        user_data[user_id]["preferences"].update(interactions["preferences"])
    
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(user_data, f, indent=4)

def interpret_review_with_llm(user_id, review_text):
    """Process user reviews using an LLM to extract preferences."""
    # Placeholder function - integrate with actual LLM
    extracted_preferences = {"genre": "Sci-Fi", "mood": "Exciting"}  # Example output
    
    update_user_profile(user_id, {"preferences": extracted_preferences})
    return extracted_preferences

def merge_profiles(user1_id, user2_id):
    """Merge two user profiles to generate shared recommendations."""
    profile1 = load_user_profile(user1_id)
    profile2 = load_user_profile(user2_id)
    
    merged_profile = {
        "views": list(set(profile1.get("views", []) + profile2.get("views", []))),
        "reviews": profile1.get("reviews", []) + profile2.get("reviews", []),
        "preferences": {**profile1.get("preferences", {}), **profile2.get("preferences", {})}
    }
    return merged_profile

# Example usage
if __name__ == "__main__":
    update_user_profile(1, {"views": ["Movie A"], "reviews": ["Great visuals!"], "preferences": {"genre": "Action"}})
    print(load_user_profile(1))
