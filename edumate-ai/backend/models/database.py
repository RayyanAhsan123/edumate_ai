from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_sign_language = db.Column(db.Boolean, default=False)
    personality_type = db.Column(db.String(10), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=True)
    is_leader = db.Column(db.Boolean, default=False)
    total_points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_sign_language": self.is_sign_language,
            "personality_type": self.personality_type,
            "group_id": self.group_id,
            "is_leader": self.is_leader,
            "total_points": self.total_points,
        }


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    personality_focus = db.Column(db.String(50))
    members = db.relationship("User", backref="group", lazy=True)
    meetings = db.relationship("Meeting", backref="group", lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "personality_focus": self.personality_focus,
            "member_count": len(self.members),
        }


class PersonalityResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    personality_type = db.Column(db.String(10))
    ei_score = db.Column(db.Integer)  # Extrovert(+) / Introvert(-)
    sn_score = db.Column(db.Integer)  # Sensing(+) / Intuition(-)
    tf_score = db.Column(db.Integer)  # Thinking(+) / Feeling(-)
    jp_score = db.Column(db.Integer)  # Judging(+) / Perceiving(-)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Points(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    points = db.Column(db.Integer, default=0)
    reason = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False)
    room_url = db.Column(db.String(300))
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "group_id": self.group_id,
            "title": self.title,
            "scheduled_at": self.scheduled_at.strftime("%Y-%m-%d %H:%M"),
            "room_url": self.room_url,
            "created_by": self.created_by,
        }


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
