from flask import Blueprint, request, jsonify, session
from models.database import db, User, Points

gamification_bp = Blueprint("gamification", __name__)


@gamification_bp.route("/add-points", methods=["POST"])
def add_points():
    from auth_helper import get_current_user_id
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    pts = data.get("points", 10)
    reason = data.get("reason", "Meeting participation")

    user = User.query.get(user_id)
    user.total_points += pts

    record = Points(user_id=user_id, points=pts, reason=reason)
    db.session.add(record)
    db.session.commit()

    return jsonify({"message": f"+{pts} points added!", "total": user.total_points}), 200


@gamification_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    top_users = User.query.order_by(User.total_points.desc()).limit(10).all()
    board = []
    for i, u in enumerate(top_users):
        board.append({
            "rank": i + 1,
            "name": u.name,
            "points": u.total_points,
            "personality_type": u.personality_type or "—",
            "is_sign_language": u.is_sign_language,
        })
    return jsonify({"leaderboard": board}), 200


@gamification_bp.route("/my-points", methods=["GET"])
def my_points():
    from auth_helper import get_current_user_id
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user = User.query.get(user_id)
    history = Points.query.filter_by(user_id=user_id).order_by(Points.created_at.desc()).limit(20).all()

    return jsonify({
        "total_points": user.total_points,
        "history": [{"points": p.points, "reason": p.reason, "date": p.created_at.strftime("%Y-%m-%d %H:%M")} for p in history],
    }), 200
