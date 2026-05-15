from flask import Blueprint, request, jsonify, session
from models.database import db, User, Group, Meeting

groups_bp = Blueprint("groups", __name__)


@groups_bp.route("/my-group", methods=["GET"])
def my_group():
    from auth_helper import get_current_user_id
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user = User.query.get(user_id)
    if not user or not user.group_id:
        return jsonify({"error": "No group assigned yet"}), 404

    group = Group.query.get(user.group_id)
    members = User.query.filter_by(group_id=group.id).all()
    meetings = Meeting.query.filter_by(group_id=group.id).order_by(Meeting.scheduled_at).all()

    return jsonify({
        "group": group.to_dict(),
        "members": [m.to_dict() for m in members],
        "meetings": [m.to_dict() for m in meetings],
        "is_leader": user.is_leader,
    }), 200


@groups_bp.route("/all", methods=["GET"])
def all_groups():
    groups = Group.query.all()
    result = []
    for g in groups:
        members = User.query.filter_by(group_id=g.id).all()
        leader = next((m for m in members if m.is_leader), None)
        result.append({
            **g.to_dict(),
            "members": [m.to_dict() for m in members],
            "leader_name": leader.name if leader else "Not assigned",
        })
    return jsonify({"groups": result}), 200
