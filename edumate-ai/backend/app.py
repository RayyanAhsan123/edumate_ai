from flask import Flask, request, jsonify, session
from flask_cors import CORS
from models.database import db, User, Group, PersonalityResult, Points, Meeting, Message
from routes.auth import auth_bp
from routes.personality import personality_bp
from routes.groups import groups_bp
from routes.gamification import gamification_bp
from routes.chatbot import chatbot_bp
from routes.meetings import meetings_bp
import os

app = Flask(__name__)
app.secret_key = "edumate_secret_key_2024_fyp"

# Session cookie settings — file:// aur localhost dono pe kaam kare
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///edumate.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app, supports_credentials=True, origins=["*"])
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(personality_bp, url_prefix="/api/personality")
app.register_blueprint(groups_bp, url_prefix="/api/groups")
app.register_blueprint(gamification_bp, url_prefix="/api/gamification")
app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")
app.register_blueprint(meetings_bp, url_prefix="/api/meetings")

@app.route("/")
def home():
    return jsonify({"message": "Edumate AI API is running!"})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
