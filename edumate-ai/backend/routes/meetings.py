from flask import Blueprint, request, jsonify, session
from models.database import db, User, Meeting
from datetime import datetime

meetings_bp = Blueprint("meetings", __name__)


@meetings_bp.route("/schedule", methods=["POST"])
def schedule():
    from auth_helper import get_current_user_id
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user = User.query.get(user_id)
    if not user.is_leader:
        return jsonify({"error": "Only the group leader can schedule meetings"}), 403

    data = request.get_json()
    title = data.get("title", "").strip()
    scheduled_str = data.get("scheduled_at", "")

    if not title or not scheduled_str:
        return jsonify({"error": "Title and date/time are required"}), 400

    try:
        scheduled_at = datetime.strptime(scheduled_str, "%Y-%m-%dT%H:%M")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DDTHH:MM"}), 400

    # Generate a simple Jitsi Meet room URL (free, no account needed)
    room_name = f"edumate-group{user.group_id}-{int(scheduled_at.timestamp())}"
    room_url = f"https://meet.jit.si/{room_name}"

    meeting = Meeting(
        group_id=user.group_id,
        title=title,
        scheduled_at=scheduled_at,
        room_url=room_url,
        created_by=user_id,
    )
    db.session.add(meeting)
    db.session.commit()

    return jsonify({"message": "Meeting scheduled!", "meeting": meeting.to_dict()}), 201


@meetings_bp.route("/my-meetings", methods=["GET"])
def my_meetings():
    from auth_helper import get_current_user_id
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user = User.query.get(user_id)
    if not user or not user.group_id:
        return jsonify({"meetings": []}), 200

    meetings = Meeting.query.filter_by(group_id=user.group_id).order_by(Meeting.scheduled_at).all()
    return jsonify({"meetings": [m.to_dict() for m in meetings]}), 200


@meetings_bp.route("/join/<int:meeting_id>", methods=["POST"])
def join_meeting(meeting_id):
    from auth_helper import get_current_user_id
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    meeting = Meeting.query.get(meeting_id)
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404

    # Award points for joining
    from models.database import Points
    user = User.query.get(user_id)
    user.total_points += 15
    pts = Points(user_id=user_id, points=15, reason=f"Joined meeting: {meeting.title}")
    db.session.add(pts)
    db.session.commit()

    return jsonify({
        "message": "Joined meeting! +15 points earned",
        "room_url": meeting.room_url,
        "total_points": user.total_points,
    }), 200
