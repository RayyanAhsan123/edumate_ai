from flask import Blueprint, request, jsonify, session
from models.database import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    is_sign_language = data.get("is_sign_language", False)

    if not name or not email or not password:
        return jsonify({"error": "Sab fields zaroor bhari jayen"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Yeh email pehle se registered hai"}), 409

    hashed = generate_password_hash(password)
    user = User(name=name, email=email, password=hashed, is_sign_language=is_sign_language)
    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.id
    return jsonify({"message": "Account ban gaya!", "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Email ya password galat hai"}), 401

    session["user_id"] = user.id
    return jsonify({"message": "Login ho gaya!", "user": user.to_dict()}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logout ho gaya"}), 200


@auth_bp.route("/me", methods=["GET"])
def me():
    from auth_helper import get_current_user_id
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Login nahi hai"}), 401
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User nahi mila"}), 404
    return jsonify({"user": user.to_dict()}), 200
