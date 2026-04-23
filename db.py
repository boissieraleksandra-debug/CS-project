import sqlite3

DB_NAME = "skillswipe.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


conn = get_connection()


def init_db():
    conn.execute("""
    CREATE TABLE IF NOT EXISTS student_profile (
        id INTEGER PRIMARY KEY,
        full_name TEXT,
        linkedin TEXT,
        education TEXT,
        availability TEXT,
        interests TEXT,
        bio TEXT,
        cv_name TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS startup_profile (
        id INTEGER PRIMARY KEY,
        startup_name TEXT,
        industry TEXT,
        location TEXT,
        description TEXT,
        contact_email TEXT
    )
    """)

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
        task_details TEXT DEFAULT '',
        status TEXT DEFAULT 'Open'
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS saved_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER UNIQUE
    )
    """)

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


# ---------- STUDENT PROFILE ----------
def get_student_profile():
    row = conn.execute("SELECT * FROM student_profile WHERE id = 1").fetchone()
    if row:
        return dict(row)
    return {
        "id": 1,
        "full_name": "",
        "linkedin": "",
        "education": "",
        "availability": "",
        "interests": "",
        "bio": "",
        "cv_name": ""
    }


def save_student_profile(profile):
    conn.execute("""
    INSERT INTO student_profile (id, full_name, linkedin, education, availability, interests, bio, cv_name)
    VALUES (1, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        full_name=excluded.full_name,
        linkedin=excluded.linkedin,
        education=excluded.education,
        availability=excluded.availability,
        interests=excluded.interests,
        bio=excluded.bio,
        cv_name=excluded.cv_name
    """, (
        profile["full_name"],
        profile["linkedin"],
        profile["education"],
        profile["availability"],
        profile["interests"],
        profile["bio"],
        profile["cv_name"]
    ))
    conn.commit()


# ---------- STARTUP PROFILE ----------
def get_startup_profile():
    row = conn.execute("SELECT * FROM startup_profile WHERE id = 1").fetchone()
    if row:
        return dict(row)
    return {
        "id": 1,
        "startup_name": "",
        "industry": "",
        "location": "",
        "description": "",
        "contact_email": ""
    }


def save_startup_profile(profile):
    conn.execute("""
    INSERT INTO startup_profile (id, startup_name, industry, location, description, contact_email)
    VALUES (1, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        startup_name=excluded.startup_name,
        industry=excluded.industry,
        location=excluded.location,
        description=excluded.description,
        contact_email=excluded.contact_email
    """, (
        profile["startup_name"],
        profile["industry"],
        profile["location"],
        profile["description"],
        profile["contact_email"]
    ))
    conn.commit()


# ---------- TASKS ----------
def create_task(title, startup_name, category, location, duration, budget, remote_type, description, skills_required, deadline, task_details):
    conn.execute("""
    INSERT INTO tasks (
        title, startup_name, category, location, duration, budget,
        remote_type, description, skills_required, deadline, task_details, status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Open')
    """, (
        title, startup_name, category, location, duration, budget,
        remote_type, description, skills_required, deadline, task_details
    ))
    conn.commit()


def get_all_tasks():
    rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]


def get_tasks_for_startup(startup_name):
    rows = conn.execute(
        "SELECT * FROM tasks WHERE startup_name = ? ORDER BY id DESC",
        (startup_name,)
    ).fetchall()
    return [dict(r) for r in rows]


# ---------- SAVED TASKS ----------
def get_saved_task_ids():
    rows = conn.execute("SELECT task_id FROM saved_tasks").fetchall()
    return [r["task_id"] for r in rows]


def save_task_for_student(task_id):
    conn.execute("INSERT OR IGNORE INTO saved_tasks (task_id) VALUES (?)", (task_id,))
    conn.commit()


def remove_saved_task(task_id):
    conn.execute("DELETE FROM saved_tasks WHERE task_id = ?", (task_id,))
    conn.commit()


# ---------- APPLICATIONS ----------
def create_application(task, name, email, phone, message, cv_name):
    conn.execute("""
    INSERT INTO applications (
        task_id, task_title, startup_name, student_name, email, phone, message, cv_name,
        task_details, status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Applied')
    """, (
        task["id"],
        task["title"],
        task["startup_name"],
        name,
        email,
        phone,
        message,
        cv_name,
        task.get("task_details", "")
    ))
    conn.commit()


def get_applications_for_startup(startup_name):
    rows = conn.execute(
        "SELECT * FROM applications WHERE startup_name = ? ORDER BY id DESC",
        (startup_name,)
    ).fetchall()
    return [dict(r) for r in rows]


def get_applications_for_student(student_name):
    rows = conn.execute(
        "SELECT * FROM applications WHERE student_name = ? ORDER BY id DESC",
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
