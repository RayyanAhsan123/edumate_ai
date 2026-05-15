# 🎓 Edumate AI — Learning Management System

> Final Year Project | Smart LMS with Personality-Based Groups, Sign Language Support, Video Conferencing, Gamification & AI Chatbot

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Tech Stack](#tech-stack)
5. [Prerequisites](#prerequisites)
6. [Installation & Setup](#installation--setup)
7. [Running the Project](#running-the-project)
8. [Using the App Step by Step](#using-the-app-step-by-step)
9. [API Endpoints Reference](#api-endpoints-reference)
10. [Adding Claude AI Chatbot API Key](#adding-claude-ai-chatbot-api-key)
11. [GitHub Setup and Version Control](#github-setup-and-version-control)
12. [Deployment Free Hosting](#deployment-free-hosting)
13. [Common Errors and Fixes](#common-errors-and-fixes)

---

## Project Overview

**Edumate AI** is a smart Learning Management System designed to help students learn better — especially students who cannot speak or use sign language. The system groups students automatically based on their personality test results, provides video conferencing so sign language students can participate, tracks participation points with a leaderboard, and includes an AI Chatbot for subject help.

---

## Features

| Feature | Description |
|---|---|
| Auth | Signup, Login, Logout with password hashing |
| Personality Test | 20-question MBTI-style quiz |
| Auto Group Assignment | Groups of 4 to 5 students based on personality |
| Leader Assignment | Best-suited student becomes group leader |
| Meeting Scheduler | Leader schedules meetings using Jitsi Meet (free video call) |
| Sign Language Support | Flag for sign-language users in their profile |
| Gamification | Points for attending meetings and doing activities |
| Leaderboard | Top 10 students by points |
| AI Chatbot | Subject Q&A using rule-based answers plus Claude AI |

---

## Project Structure

```
edumate-ai/
│
├── backend/                  ← Python Flask API
│   ├── app.py                ← Main Flask app — start here
│   ├── requirements.txt      ← Python packages to install
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py       ← All database tables (SQLite)
│   └── routes/
│       ├── __init__.py
│       ├── auth.py           ← signup, login, logout
│       ├── personality.py    ← questions + submit
│       ├── groups.py         ← my-group, all groups
│       ├── gamification.py   ← leaderboard, add-points
│       ├── chatbot.py        ← AI tutor ask endpoint
│       └── meetings.py       ← schedule, join meeting
│
├── frontend/                 ← Plain HTML + Bootstrap
│   ├── login.html
│   ├── signup.html
│   ├── personality.html      ← 20-question personality test
│   ├── dashboard.html        ← Main home screen
│   ├── group.html            ← Group members + meetings
│   ├── leaderboard.html      ← Top 10 leaderboard
│   ├── chatbot.html          ← AI tutor chatbot
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── api.js            ← API helper used by all pages
│
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Bootstrap 5, Vanilla JavaScript |
| Backend | Python 3, Flask, Flask-SQLAlchemy, Flask-CORS |
| Database | SQLite (zero setup, file-based) |
| Video Calls | Jitsi Meet (free, no account needed) |
| AI Chatbot | Claude API by Anthropic, or built-in fallback |
| Auth | Session-based with Werkzeug password hashing |

---

## Prerequisites

Install these before starting:

### 1. Python 3.10 or higher

Download from: https://www.python.org/downloads/

After installing open terminal and check:
```
python --version
```
It should show Python 3.10 or higher.

**IMPORTANT for Windows:** During Python installation, check the box that says **"Add Python to PATH"** before clicking Install.

### 2. VS Code (Recommended Editor)

Download from: https://code.visualstudio.com/

### 3. Live Server Extension for VS Code

- Open VS Code
- Press Ctrl + Shift + X
- Search for **Live Server** by Ritwick Dey
- Click Install

### 4. Git (for GitHub)

Download from: https://git-scm.com/downloads

---

## Installation and Setup

### Step 1: Extract the Project

If you downloaded the ZIP file:
1. Right-click the ZIP file
2. Click Extract All
3. Choose a folder for example: `C:\Projects\edumate-ai`

---

### Step 2: Open Terminal

**Windows:** Press Win + R, type `cmd`, press Enter

**Mac:** Press Cmd + Space, type Terminal, press Enter

Go to the backend folder:
```
cd C:\Projects\edumate-ai\backend
```
Replace the path with wherever you extracted the project.

---

### Step 3: Create Python Virtual Environment

This keeps your project packages separate from other Python projects.

```
python -m venv venv
```

Now activate it:

**Windows:**
```
venv\Scripts\activate
```

**Mac or Linux:**
```
source venv/bin/activate
```

You will see **(venv)** appear at the start of your terminal line. This means it is working correctly.

---

### Step 4: Install Required Packages

```
pip install -r requirements.txt
```

Wait for it to finish. You will see "Successfully installed" messages at the end.

---

### Step 5: Optional — Add Claude AI API Key

The chatbot works without any API key using built-in answers. To use real Claude AI:

1. Go to https://console.anthropic.com
2. Sign up for a free account
3. Go to API Keys section and create a key

Set the key before running the app:

**Windows:**
```
set ANTHROPIC_API_KEY=your_key_here
```

**Mac or Linux:**
```
export ANTHROPIC_API_KEY=your_key_here
```

---

## Running the Project

### Start the Backend

Make sure you are in the backend folder and virtual environment is active (you see venv in terminal):

```
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**Keep this terminal open.** Do not close it. The backend must be running.

---

### Start the Frontend

**Method 1 — VS Code Live Server (Best Method)**

1. Open VS Code
2. Go to File → Open Folder → select the `frontend` folder
3. Right-click on `login.html` in the file list on the left
4. Click **Open with Live Server**
5. Your browser opens at `http://127.0.0.1:5500/login.html`

**Method 2 — Direct Open**

1. Open the `frontend` folder in File Explorer
2. Double-click `login.html`
3. It opens in your browser directly

---

## Using the App Step by Step

### Step 1 — Create Account

1. The app opens on the Login page
2. Click **Sign up here** at the bottom
3. Enter your full name, email address, and password
4. If you use sign language, toggle the switch ON
5. Click **Create Account**
6. You are automatically taken to the Personality Test

---

### Step 2 — Take Personality Test

1. You will see 20 questions one at a time
2. Each question has two options: A or B
3. Click your answer and the Next button appears
4. Answer all 20 questions
5. On the last question, click **Submit**
6. Your 4-letter personality type is shown (like ENFJ or INTJ)
7. Your group is automatically assigned
8. If you are the best personality match for leadership, you become the Group Leader

---

### Step 3 — Dashboard

After the test you are taken to the Dashboard. Here you can see:
- Your personality type
- Your group name
- Upcoming meetings
- Your total points
- A quick link to the AI Tutor

---

### Step 4 — My Group Page

Click **My Group** in the top navigation bar. You will see:
- All members of your group with their personality types
- Sign language users are shown with a special badge
- All scheduled meetings with Join buttons

**If you are the Group Leader:**
- A yellow "You are Leader" badge appears
- The **Schedule Meeting** button appears

---

### Step 5 — Schedule a Meeting (Leaders Only)

1. On the My Group page, click **Schedule Meeting**
2. Enter a meeting title like "Week 3 Project Discussion"
3. Select a date and time using the calendar picker
4. Click **Schedule**
5. A Jitsi Meet video room is automatically created and shared with all group members

---

### Step 6 — Join a Meeting and Earn Points

1. On the My Group page or Dashboard, find an upcoming meeting
2. Click the green **Join** button
3. You earn **+15 points** automatically
4. The Jitsi Meet room opens in a new browser tab
5. No account needed for Jitsi — just enter your name and join

---

### Step 7 — Leaderboard

Click **Leaderboard** in the navigation bar to see the Top 10 students by points. You can earn points by:
- Joining meetings: +15 points each time
- Completing practice sessions from the Dashboard: +10 points
- More activities can be added by the developer

---

### Step 8 — AI Tutor Chatbot

Click the robot button floating at the bottom-right corner of any page, or click **AI Tutor** in the navigation bar. Type any question about:
- Programming topics like Python, algorithms, data structures
- Your group or meetings
- How the points system works
- Any subject-related question

---

## API Endpoints Reference

All API calls go to `http://localhost:5000`

### Auth Endpoints
| Method | URL | What it does |
|---|---|---|
| POST | /api/auth/signup | Create new student account |
| POST | /api/auth/login | Login with email and password |
| POST | /api/auth/logout | Logout current user |
| GET | /api/auth/me | Get logged-in user info |

### Personality Endpoints
| Method | URL | What it does |
|---|---|---|
| GET | /api/personality/questions | Get all 20 quiz questions |
| POST | /api/personality/submit | Submit answers, get type and group |

### Group Endpoints
| Method | URL | What it does |
|---|---|---|
| GET | /api/groups/my-group | Get your group, members, meetings |
| GET | /api/groups/all | Get all groups |

### Gamification Endpoints
| Method | URL | What it does |
|---|---|---|
| GET | /api/gamification/leaderboard | Top 10 students |
| GET | /api/gamification/my-points | Your total points and history |
| POST | /api/gamification/add-points | Add points to your account |

### Meeting Endpoints
| Method | URL | What it does |
|---|---|---|
| POST | /api/meetings/schedule | Schedule a meeting (leaders only) |
| GET | /api/meetings/my-meetings | Get all your group meetings |
| POST | /api/meetings/join/ID | Join a meeting and earn 15 points |

### Chatbot Endpoints
| Method | URL | What it does |
|---|---|---|
| POST | /api/chatbot/ask | Send message, get AI reply |
| GET | /api/chatbot/history | Get your chat history |

---

## Adding Claude AI Chatbot API Key

By default the chatbot uses built-in rule-based responses. To upgrade to real Claude AI:

1. Go to https://console.anthropic.com
2. Sign up (free account available)
3. Click **API Keys** → **Create Key**
4. Copy the key that starts with `sk-ant-`

Open `backend/routes/chatbot.py` and find this line near the top:
```python
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
```

For quick testing during development you can replace it with:
```python
ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
```

Restart the backend and the chatbot now uses real Claude AI.

---

## GitHub Setup and Version Control

### Step 1: Create GitHub Account

Go to https://github.com and create a free account if you do not have one.

### Step 2: Create New Repository

1. After logging in, click the plus button at the top right
2. Click **New repository**
3. Name it `edumate-ai`
4. Choose Public or Private
5. Do NOT check "Initialize this repository with a README" (we have our own)
6. Click **Create repository**

### Step 3: Set Up Git in Your Project

Open terminal in the `edumate-ai` root folder (not inside backend or frontend):

```
git init
git add .
git commit -m "feat: initial Edumate AI project setup"
```

### Step 4: Create .gitignore File

Create a file named `.gitignore` in the root folder with this content:

```
venv/
__pycache__/
*.pyc
*.db
.env
.DS_Store
Thumbs.db
.vscode/
```

Then add and commit it:
```
git add .gitignore
git commit -m "chore: add gitignore file"
```

### Step 5: Connect and Push to GitHub

Copy the repository URL from GitHub (looks like https://github.com/yourname/edumate-ai.git)

```
git remote add origin https://github.com/YOUR_USERNAME/edumate-ai.git
git branch -M main
git push -u origin main
```

### Step 6: Daily Workflow

Every time you make changes and want to save them to GitHub:

```
git status
git add .
git commit -m "feat: describe what you changed here"
git push
```

### Commit Message Guide

Use these prefixes so your commit history is clean:
- `feat:` when you add a new feature
- `fix:` when you fix a bug
- `style:` when you change CSS or design only
- `chore:` for small maintenance tasks
- `docs:` when you update the README or documentation

Example commits:
```
feat: add sign language badge to member cards
fix: leaderboard not refreshing after joining meeting
style: improve dashboard card colors
docs: update README with deployment steps
```

### Feature Branch Workflow (Recommended)

Create a separate branch for each new feature:
```
git checkout -b feature/sign-language-detection
# make your changes
git add .
git commit -m "feat: add MediaPipe hand detection overlay"
git push origin feature/sign-language-detection
```

When the feature is done, merge it back:
```
git checkout main
git merge feature/sign-language-detection
git push
```

---

## Deployment Free Hosting

### Deploy Backend to Render.com

1. Go to https://render.com and sign up with your GitHub account
2. Click **New** then **Web Service**
3. Connect your GitHub repository
4. Configure the service:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. Add environment variable: Key = `ANTHROPIC_API_KEY`, Value = your key
6. Click **Deploy**
7. You get a live URL like `https://edumate-ai-xxxx.onrender.com`

### Deploy Frontend to Netlify

1. Go to https://netlify.com and sign up
2. Drag and drop your entire `frontend` folder onto the Netlify dashboard
3. You get a URL like `https://edumate-ai.netlify.app`
4. Open `frontend/js/api.js` and change the BASE_URL to your Render backend URL

---

## Common Errors and Fixes

### Error: ModuleNotFoundError: No module named flask

This means the virtual environment is not activated.

Fix: Run this and try again:
```
# Windows
venv\Scripts\activate

# Mac or Linux
source venv/bin/activate
```

---

### Error: Address already in use port 5000

Another program is already using port 5000.

Fix: Change the port in `backend/app.py` last line:
```python
app.run(debug=True, port=5001)
```
Also open `frontend/js/api.js` and change `5000` to `5001`.

---

### Error: CORS error in browser console

The backend is not running.

Fix: Open a terminal, go to backend folder, activate venv, run `python app.py`. Make sure you see "Running on http://127.0.0.1:5000".

---

### Error: Database table not found

The database file is corrupted or outdated.

Fix: Delete the old database and restart:
```
# Windows
del backend\edumate.db

# Mac or Linux
rm backend/edumate.db
```
Then restart with `python app.py`. The database is recreated automatically.

---

### Error: pip is not recognized

Fix: Try using pip3 instead:
```
pip3 install -r requirements.txt
python3 app.py
```

---

### Chatbot says "Sorry, I couldn't connect"

This means either no API key is set, or the key is wrong.

Fix: Either set a valid ANTHROPIC_API_KEY or leave it empty to use the built-in fallback responses. The chatbot still works without an API key.

---

## Project Team

**Project Name:** Edumate AI
**Type:** Final Year Project (FYP)
**Stack:** Python Flask + Bootstrap HTML + SQLite
**Purpose:** Smart LMS for all students including those with speech or hearing disabilities
