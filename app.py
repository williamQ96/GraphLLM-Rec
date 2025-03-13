from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
from pathlib import Path
import os
import random
from recforuser import *

app = Flask(__name__)

# Allow requests from webui running on port 5500
CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"]}})

# 数据存储路径
DATA_DIR = Path("data")
USERS_FILE = DATA_DIR / "users.json"
RATINGS_FILE = DATA_DIR / "ratings.json"

# 示例电影数据
SAMPLE_MOVIES = [
    {
        "id": "1",
        "title": "盗梦空间",
        "year": "2010",
        "genre": "科幻",
        "rating": "9.3",
        "description": "在这部精彩的科幻动作片中，一位技术高超的窃贼能够进入他人的梦境窃取情报。",
        "poster": "https://source.unsplash.com/random/300x450?inception"
    },
    {
        "id": "2",
        "title": "肖申克的救赎",
        "year": "1994",
        "genre": "剧情",
        "rating": "9.7",
        "description": "两个被囚禁的人通过多年的时间找到慰藉和最终的救赎，通过他们发现希望是一件好事。",
        "poster": "https://source.unsplash.com/random/300x450?prison"
    },
    {
        "id": "3",
        "title": "黑暗骑士",
        "year": "2008",
        "genre": "动作",
        "rating": "9.0",
        "description": "当小丑在哥谭市掀起一场混乱和破坏的浪潮时，蝙蝠侠必须面对他所遇到的最大的心理和身体考验。",
        "poster": "https://source.unsplash.com/random/300x450?batman"
    },
    {
        "id": "4",
        "title": "星际穿越",
        "year": "2014",
        "genre": "科幻",
        "rating": "9.2",
        "description": "一组探险家通过新发现的虫洞进行星际旅行，试图为人类寻找新的家园。",
        "poster": "https://source.unsplash.com/random/300x450?space"
    },
    {
        "id": "5",
        "title": "教父",
        "year": "1972",
        "genre": "犯罪",
        "rating": "9.2",
        "description": "一个有组织犯罪家族的老教父将他的地下帝国转交给他不情愿的儿子。",
        "poster": "https://source.unsplash.com/random/300x450?godfather"
    },
    {
        "id": "6",
        "title": "泰坦尼克号",
        "year": "1997",
        "genre": "爱情",
        "rating": "9.1",
        "description": "一个贫穷的艺术家和一个富有的女子在注定沉没的泰坦尼克号上坠入爱河。",
        "poster": "https://source.unsplash.com/random/300x450?titanic"
    },
    {
        "id": "7",
        "title": "千与千寻",
        "year": "2001",
        "genre": "动画",
        "rating": "9.3",
        "description": "小女孩千寻意外进入神灵世界，为了救出变成猪的父母而努力工作。",
        "poster": "https://source.unsplash.com/random/300x450?spirited"
    },
    {
        "id": "8",
        "title": "这个杀手不太冷",
        "year": "1994",
        "genre": "动作",
        "rating": "9.4",
        "description": "一个职业杀手收留了一个小女孩，教会了她生存之道，两人建立了深厚的友谊。",
        "poster": "https://source.unsplash.com/random/300x450?professional"
    }
]

# 确保数据目录存在
DATA_DIR.mkdir(exist_ok=True)

# 初始化数据文件
def init_data_files():
    if not USERS_FILE.exists():
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)
    
    if not RATINGS_FILE.exists():
        with open(RATINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)

init_data_files()

def load_users():
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)

def load_ratings():
    with open(RATINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_ratings(ratings):
    with open(RATINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(ratings, f, indent=2)

@app.route('/')
def index():
    return render_template('webui.html')

@app.route('/api/signin', methods=['POST'])
def signin():
    data = request.json
    username = data.get('username', '').strip()

    if not username:
        return jsonify({"error": "用户名不能为空"}), 400

    # 加载用户数据
    users = load_users()
    
    # 检查用户是否存在
    user_data = users.get(username, {})
    is_new_user = not user_data
    
    if is_new_user:
        # 创建新用户
        users[username] = {
            "completed_cold_start": False,
            "preferences": {
                "liked": [],
                "disliked": []
            }
        }
        save_users(users)
        return jsonify({
            "user": username,
            "cold_start": True
        })
    
    # 返回现有用户信息
    return jsonify({
        "user": username,
        "cold_start": not user_data.get("completed_cold_start", False)
    })

@app.route('/api/complete_cold_start', methods=['POST'])
def complete_cold_start():
    data = request.json
    username = data.get('username')
    preferences = data.get('preferences', {})
    
    if not username:
        return jsonify({"error": "用户名不能为空"}), 400
    
    users = load_users()
    if username not in users:
        return jsonify({"error": "用户不存在"}), 404
    
    # 更新用户偏好
    users[username]["preferences"] = preferences
    users[username]["completed_cold_start"] = True
    save_users(users)
    
    return jsonify({"success": True})

@app.route('/api/rate_movie', methods=['POST'])
def rate_movie():
    data = request.json
    username = data.get('username')
    movie_id = data.get('movieId')
    rating = data.get('rating')  # 'like' 或 'dislike'
    
    if not all([username, movie_id, rating]):
        return jsonify({"error": "缺少必要参数"}), 400
    
    ratings = load_ratings()
    
    # 初始化用户的评分数据
    if username not in ratings:
        ratings[username] = {"liked": [], "disliked": []}
    
    # 更新评分
    if rating == 'like':
        if movie_id not in ratings[username]["liked"]:
            ratings[username]["liked"].append(movie_id)
        # 从不喜欢列表中移除（如果存在）
        if movie_id in ratings[username]["disliked"]:
            ratings[username]["disliked"].remove(movie_id)
    else:
        if movie_id not in ratings[username]["disliked"]:
            ratings[username]["disliked"].append(movie_id)
        # 从喜欢列表中移除（如果存在）
        if movie_id in ratings[username]["liked"]:
            ratings[username]["liked"].remove(movie_id)
    
    save_ratings(ratings)
    return jsonify({"success": True})


@app.route('/api/get_recommendations', methods=['GET'])
def get_recommendations():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "用户名不能为空"}), 400

    # 加载用户数据和评分数据
    users = load_users()
    ratings = load_ratings()

    if username not in users:
        return jsonify({"error": "用户不存在"}), 404

    # Get recommendations by calling user_rec from recommender.py
    recommendations = user_rec(username)

    return jsonify({"recommendations": recommendations})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
