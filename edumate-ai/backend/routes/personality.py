from flask import Blueprint, request, jsonify, session
from models.database import db, User, Group, PersonalityResult

personality_bp = Blueprint("personality", __name__)

QUESTIONS = [
    {"id": 1, "text": "At a party, you prefer to:", "a": "Talk to many different people", "b": "Have a few deep conversations", "dimension": "EI"},
    {"id": 2, "text": "You are more:", "a": "Practical and realistic", "b": "Imaginative and future-focused", "dimension": "SN"},
    {"id": 3, "text": "When making decisions, you prefer to:", "a": "Analyze the facts logically", "b": "Consider people's feelings first", "dimension": "TF"},
    {"id": 4, "text": "You prefer to:", "a": "Plan things well in advance", "b": "Decide things at the last minute", "dimension": "JP"},
    {"id": 5, "text": "You find it easier to:", "a": "Start conversations with new people", "b": "Wait for others to approach you", "dimension": "EI"},
    {"id": 6, "text": "You focus more on:", "a": "What is actually happening", "b": "What could potentially happen", "dimension": "SN"},
    {"id": 7, "text": "You are seen as:", "a": "Tough-minded and firm", "b": "Warm-hearted and caring", "dimension": "TF"},
    {"id": 8, "text": "You like your life to be:", "a": "Structured and organized", "b": "Flexible and spontaneous", "dimension": "JP"},
    {"id": 9, "text": "Social events leave you feeling:", "a": "Energized", "b": "Drained", "dimension": "EI"},
    {"id": 10, "text": "You trust more:", "a": "Your direct experience", "b": "Your gut instinct", "dimension": "SN"},
    {"id": 11, "text": "When someone makes a mistake:", "a": "You point out the facts clearly", "b": "You consider how to avoid hurting them", "dimension": "TF"},
    {"id": 12, "text": "You prefer:", "a": "Having a clear to-do list", "b": "Figuring things out as you go", "dimension": "JP"},
    {"id": 13, "text": "You prefer to work:", "a": "With others in a team", "b": "Alone or in small groups", "dimension": "EI"},
    {"id": 14, "text": "You prefer information that is:", "a": "Concrete and specific", "b": "Abstract and theoretical", "dimension": "SN"},
    {"id": 15, "text": "You believe:", "a": "Justice is more important than mercy", "b": "Mercy is more important than justice", "dimension": "TF"},
    {"id": 16, "text": "You prefer:", "a": "Finishing tasks before relaxing", "b": "Relaxing before finishing tasks", "dimension": "JP"},
    {"id": 17, "text": "You are more:", "a": "Outgoing and expressive", "b": "Reserved and thoughtful", "dimension": "EI"},
    {"id": 18, "text": "You pay more attention to:", "a": "Details and facts", "b": "Patterns and possibilities", "dimension": "SN"},
    {"id": 19, "text": "You tend to be more:", "a": "Rational than emotional", "b": "Emotional than rational", "dimension": "TF"},
    {"id": 20, "text": "You prefer environments that are:", "a": "Predictable and routine", "b": "Varied and changing", "dimension": "JP"},
]


@personality_bp.route("/questions", methods=["GET"])
def get_questions():
    return jsonify({"questions": QUESTIONS}), 200


@personality_bp.route("/submit", methods=["POST"])
def submit_personality():
    from auth_helper import get_current_user_id
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    answers = data.get("answers", {})  # {question_id: "a" or "b"}

    ei = sn = tf = jp = 0
    for q in QUESTIONS:
        ans = answers.get(str(q["id"]))
        if not ans:
            continue
        dim = q["dimension"]
        if dim == "EI":
            ei += 1 if ans == "a" else -1
        elif dim == "SN":
            sn += 1 if ans == "a" else -1
        elif dim == "TF":
            tf += 1 if ans == "a" else -1
        elif dim == "JP":
            jp += 1 if ans == "a" else -1

    ptype = (
        ("E" if ei >= 0 else "I") +
        ("S" if sn >= 0 else "N") +
        ("T" if tf >= 0 else "F") +
        ("J" if jp >= 0 else "P")
    )

    result = PersonalityResult(
        user_id=user_id, personality_type=ptype,
        ei_score=ei, sn_score=sn, tf_score=tf, jp_score=jp
    )
    db.session.add(result)

    user = User.query.get(user_id)
    user.personality_type = ptype
    db.session.commit()

    # Auto-assign to group
    assigned_group = _assign_to_group(user, ptype)
    db.session.commit()

    return jsonify({
        "personality_type": ptype,
        "description": _describe(ptype),
        "group": assigned_group.to_dict() if assigned_group else None,
        "is_leader": user.is_leader,
    }), 200


def _assign_to_group(user, ptype):
    # Find a group with space (< 5 members) that has compatible personality
    groups = Group.query.all()
    for g in groups:
        members = User.query.filter_by(group_id=g.id).all()
        if len(members) < 5:
            user.group_id = g.id
            # Assign leadership: first extrovert+judger in group
            extroverts = [m for m in members if m.personality_type and m.personality_type[0] == "E" and m.personality_type[3] == "J"]
            if not extroverts and ptype[0] == "E" and ptype[3] == "J":
                user.is_leader = True
            return g

    # No group with space — create a new one
    group_num = Group.query.count() + 1
    new_group = Group(name=f"Group {group_num}", personality_focus=ptype[:2])
    db.session.add(new_group)
    db.session.flush()  # get ID
    user.group_id = new_group.id
    user.is_leader = True  # First person becomes leader
    return new_group


def _describe(ptype):
    descriptions = {
        "ENTJ": "The Commander — natural born leader, confident and decisive.",
        "ENFJ": "The Teacher — charismatic, inspiring, and people-focused.",
        "INTJ": "The Architect — strategic, independent, and visionary.",
        "INFJ": "The Counselor — insightful, principled, and creative.",
        "ENTP": "The Debater — innovative, clever, and curious.",
        "ENFP": "The Champion — enthusiastic, creative, and sociable.",
        "INTP": "The Thinker — analytical, logical, and objective.",
        "INFP": "The Mediator — idealistic, empathetic, and creative.",
        "ESTJ": "The Supervisor — organized, reliable, and hardworking.",
        "ESFJ": "The Provider — caring, social, and traditional.",
        "ISTJ": "The Inspector — dependable, meticulous, and responsible.",
        "ISFJ": "The Protector — loyal, warm, and observant.",
        "ESTP": "The Entrepreneur — energetic, perceptive, and direct.",
        "ESFP": "The Performer — fun-loving, spontaneous, and enthusiastic.",
        "ISTP": "The Virtuoso — practical, observant, and reserved.",
        "ISFP": "The Adventurer — flexible, charming, and artistic.",
    }
    return descriptions.get(ptype, "A unique personality type with great potential!")
