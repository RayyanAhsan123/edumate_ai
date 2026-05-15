# ============================================================
#  Edumate AI — CONFIGURATION FILE
#
#  CHATBOT KE LIYE YAHAN API KEY DAALO:
#
#  Step 1: https://console.anthropic.com par jao
#  Step 2: Sign up karo (free account)
#  Step 3: Baayein menu mein "API Keys" click karo
#  Step 4: "Create Key" click karo
#  Step 5: Key copy karo (sk-ant-... se start hogi)
#  Step 6: Neeche YOUR_API_KEY_HERE ki jagah paste karo
#  Step 7: File save karo (Ctrl+S)
#  Step 8: Terminal mein server restart karo (Ctrl+C phir python app.py)
#
# ============================================================

ANTHROPIC_API_KEY = "YOUR_API_KEY_HERE"

# Example (yeh real key nahi hai, sirf format dikhane ke liye):
# ANTHROPIC_API_KEY = "sk-ant-api03-abcdefghijklmnop-xxxxxxxxxxxxxxxxxxxx-XXXXXXXXXXXXXXXXXXXXXXXX"

# ============================================================
#  Baaki settings — inhe mat badlo
# ============================================================
SECRET_KEY = "edumate_secret_2024_fyp"
DATABASE_URI = "sqlite:///edumate.db"
DEBUG = True
PORT = 5000
