from flask import Blueprint, request, jsonify, session
from models.database import db, Message
from auth_helper import get_current_user_id
import json
import urllib.request
import urllib.error

chatbot_bp = Blueprint("chatbot", __name__)


def get_api_key():
    """config.py se API key lo"""
    try:
        import config
        key = config.ANTHROPIC_API_KEY
        if key and key != "YOUR_API_KEY_HERE":
            return key
    except Exception:
        pass
    return ""


def ask_claude(user_message, history=[]):
    """Claude API call karo"""
    api_key = get_api_key()

    if not api_key:
        return _fallback_response(user_message)

    messages = history + [{"role": "user", "content": user_message}]
    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 600,
        "system": (
            "You are Edumate, a helpful and friendly AI tutor for university students in Pakistan. "
            "Answer questions about programming (Python, Java, C++), computer science, data structures, "
            "algorithms, math, databases, and general studies. "
            "Keep answers clear and concise. Use simple language. "
            "If someone asks in Urdu or Roman Urdu, reply in Roman Urdu mixed with English. "
            "Be encouraging and supportive. Use emojis sometimes to be friendly."
        ),
        "messages": messages,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read().decode())
            return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "invalid_api_key" in body or "authentication" in body.lower():
            return "❌ API key galat hai. backend/config.py kholo aur apni sahi key daalo."
        return f"❌ API Error: {e.code} — {body[:200]}"
    except Exception as e:
        return f"❌ Connection error: {str(e)}"


def _fallback_response(msg):
    """Jab API key nahi hoti tab built-in jawab"""
    msg_lower = msg.lower()
    if any(w in msg_lower for w in ["hello", "hi", "hey", "salam", "assalam"]):
        return "Salam! Main Edumate AI hoon. Apne studies ke baare mein kuch bhi poocho! 😊"
    if "python" in msg_lower:
        return "Python ek beginner-friendly language hai. Loops, functions, OOP — kya specifically chahiye? 🐍"
    if "oop" in msg_lower or "object" in msg_lower:
        return "OOP ke 4 pillars hain:\n1. Encapsulation\n2. Inheritance\n3. Polymorphism\n4. Abstraction\n\nKaunsa detail mein samjhaun? 🏗️"
    if "array" in msg_lower or "list" in msg_lower:
        return "Array ek fixed-size data structure hai. Python mein list use hoti hai jo dynamic hai. Index se access hota hai — jaise list[0] pehla element. 📋"
    if "recursion" in msg_lower:
        return "Recursion matlab function khud ko call kare! Jaise factorial(5) = 5 × factorial(4). Har recursion mein base case zaroor hona chahiye warna infinite loop ho jata hai. 🔄"
    if "linked list" in msg_lower:
        return "Linked List mein nodes hoti hain. Har node mein data + next node ka address hota hai. Array se fark: memory continuous nahi hoti. Insert/Delete fast hai! 🔗"
    if "group" in msg_lower:
        return "Tumhara group personality test ke results se assign hota hai. Group mein 4-5 members hote hain. Leader meetings schedule kar sakta hai! 👥"
    if "point" in msg_lower or "score" in msg_lower:
        return "Points kaisy milte hain:\n• Meeting join karo: +15 pts\n• Practice session: +10 pts\n\nLeaderboard mein top 10 students dikhte hain! 🏆"
    if "meeting" in msg_lower:
        return "Meeting sirf group leader schedule kar sakta hai. Schedule hone ke baad sab members 'Join' button se video call mein aa sakte hain. Jitsi Meet free hai — koi account nahi chahiye! 📹"
    if "api" in msg_lower and "key" in msg_lower:
        return "backend/config.py kholo. ANTHROPIC_API_KEY = 'YOUR_KEY' wali line mein apni real key paste karo. console.anthropic.com se milegi. Server restart karo phir! 🔑"
    if "sort" in msg_lower:
        return "Common sorting algorithms:\n• Bubble Sort: O(n²) — slow but simple\n• Merge Sort: O(n log n) — fast, divide & conquer\n• Quick Sort: O(n log n) avg — most used\n\nKaunsa detail mein chahiye? 📊"
    if "database" in msg_lower or "sql" in msg_lower:
        return "SQL basics:\nSELECT * FROM table — data lo\nINSERT INTO table VALUES(...) — data daalo\nUPDATE table SET col=val — update karo\nDELETE FROM table WHERE... — delete karo\n\n💾 Kya specific query chahiye?"
    return "Yeh interesting question hai! Main programming, CS, math, aur Edumate system ke baare mein help kar sakta hoon. Thoda aur detail mein poocho! 🤖"


@chatbot_bp.route("/ask", methods=["POST"])
def ask():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Pehle login karo"}), 401

    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Message khali hai"}), 400

    # Last 6 messages context ke liye
    past = Message.query.filter_by(user_id=user_id)\
        .order_by(Message.created_at.desc()).limit(6).all()
    history = []
    for m in reversed(past):
        history.append({"role": "user", "content": m.content})
        if m.response:
            history.append({"role": "assistant", "content": m.response})

    response = ask_claude(user_message, history)

    record = Message(user_id=user_id, content=user_message, response=response)
    db.session.add(record)
    db.session.commit()

    return jsonify({"response": response}), 200


@chatbot_bp.route("/history", methods=["GET"])
def history():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Pehle login karo"}), 401

    msgs = Message.query.filter_by(user_id=user_id)\
        .order_by(Message.created_at.asc()).limit(50).all()
    return jsonify({
        "history": [
            {"you": m.content, "bot": m.response,
             "time": m.created_at.strftime("%H:%M")}
            for m in msgs
        ]
    }), 200


@chatbot_bp.route("/status", methods=["GET"])
def status():
    """Check karo API key set hai ya nahi"""
    key = get_api_key()
    return jsonify({
        "api_key_set": bool(key),
        "mode": "Claude AI (Real)" if key else "Built-in fallback responses"
    }), 200
