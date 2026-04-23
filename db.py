import sqlite3
from typing import Dict, List

DB_NAME = "skillswipe.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


conn = get_connection()


def init_db():
    # TASKS TABLE
    conn.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        startup_name TEXT,
        category TEXT,
        location TEXT,
        duration TEXT,
        budget TEXT,
        remote_type TEXT,
        description TEXT,
        skills_required TEXT,
        deadline TEXT,
        task_details TEXT,
        status TEXT
    )
    """)

    # APPLICATIONS TABLE
    conn.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        task_title TEXT,
        startup_name TEXT,
        student_name TEXT,
        email TEXT,
        phone TEXT,
        message TEXT,
        cv_name TEXT,
        status TEXT DEFAULT 'Applied',
        task_details TEXT DEFAULT '',
        submission_note TEXT DEFAULT '',
        submission_link TEXT DEFAULT '',
        end_reason TEXT DEFAULT ''
    )
    """)

    conn.commit()


# ---------------- SEED TASKS ----------------

def seed_tasks():
    count = conn.execute("SELECT COUNT(*) as c FROM tasks").fetchone()["c"]
    if count > 0:
        return

    sample_tasks = [
        {
            "title": "Market Research Sprint",
            "startup_name": "GrowthAI",
            "category": "Marketing",
            "location": "Zurich",
            "duration": "3 days",
            "budget": "CHF 250",
            "remote_type": "Hybrid",
            "description": "Research competitors and summarize insights.",
            "skills_required": "Research, Slides",
            "deadline": "30 April",
            "task_details": "Create a short 5-slide summary.",
            "status": "Open"
        },
        {
            "title": "Pitch Deck Refresh",
            "startup_name": "BrightLabs",
            "category": "Strategy",
            "location": "Remote",
            "duration": "1 week",
            "budget": "CHF 400",
            "remote_type": "Remote",
            "description": "Improve investor pitch deck.",
            "skills_required": "Strategy, PowerPoint",
            "deadline": "2 May",
            "task_details": "Update flow + visuals.",
            "status": "Open"
        },
        {
            "title": "UX Feedback Review",
            "startup_name": "Nova Studio",
            "category": "Design",
            "location": "Geneva",
            "duration": "4 days",
            "budget": "CHF 300",
            "remote_type": "On-site",
            "description": "Review onboarding UX.",
            "skills_required": "UX, Figma",
            "deadline": "5 May",
            "task_details": "Suggest improvements.",
            "status": "Open"
        }
    ]

    for t in sample_tasks:
        conn.execute("""
        INSERT INTO tasks (
            title, startup_name, category, location, duration, budget,
            remote_type, description, skills_required, deadline, task_details, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            t["title"], t["startup_name"], t["category"], t["location"],
            t["duration"], t["budget"], t["remote_type"], t["description"],
            t["skills_required"], t["deadline"], t["task_details"], t["status"]
        ))

    conn.commit()


# ---------------- APPLICATION LOGIC ----------------

def create_application(task, name, email, phone, message, cv_name):
    conn.execute("""
    INSERT INTO applications (
        task_id, task_title, startup_name,
        student_name, email, phone, message, cv_name
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        task["id"], task["title"], task["startup_name"],
        name, email, phone, message, cv_name
    ))
    conn.commit()


def get_applications_for_startup(startup_name: str):
    rows = conn.execute(
        "SELECT * FROM applications WHERE startup_name = ?",
        (startup_name,)
    ).fetchall()
    return [dict(r) for r in rows]


def get_applications_for_student(student_name: str):
    rows = conn.execute(
        "SELECT * FROM applications WHERE student_name = ?",
        (student_name,)
    ).fetchall()
    return [dict(r) for r in rows]


def update_application_status(app_id, status):
    conn.execute(
        "UPDATE applications SET status = ? WHERE id = ?",
        (status, app_id)
    )
    conn.commit()


def update_application_task_details(app_id, details):
    conn.execute(
        "UPDATE applications SET task_details = ? WHERE id = ?",
        (details, app_id)
    )
    conn.commit()


def submit_work(app_id, note, link):
    conn.execute("""
    UPDATE applications
    SET submission_note = ?, submission_link = ?, status = 'Submitted'
    WHERE id = ?
    """, (note, link, app_id))
    conn.commit()


def cancel_application(app_id, reason):
    conn.execute("""
    UPDATE applications
    SET status = 'Cancelled', end_reason = ?
    WHERE id = ?
    """, (reason, app_id))
    conn.commit()
