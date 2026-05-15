# ============================================================
#  Edumate AI — Auth Helper
#  Session ya X-User-Id header dono se user_id milta hai
# ============================================================

from flask import session, request


def get_current_user_id():
    """
    Session se user_id lo.
    Agar session nahi to X-User-Id header check karo.
    Yeh ensure karta hai ke file:// aur Live Server dono kaam karen.
    """
    uid = session.get("user_id")
    if uid:
        return uid
    # Fallback: header se lo (frontend har request mein bhejta hai)
    header_id = request.headers.get("X-User-Id")
    if header_id and header_id.isdigit():
        return int(header_id)
    return None
