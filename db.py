import sqlite3
from typing import Dict, List

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
        title TEXT NOT NULL,
        startup_name TEXT NOT NULL,
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
        submission_link TEXT DEFAULT ''
    )
    """)
    conn.commit()


def seed_tasks():
    count = conn.execute("SELECT COUNT(*) AS c FROM tasks").fetchone()["c"]
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
            "description": "Research competitors and summarize 5 key market insights in a short slide deck.",
            "skills_required": "Research, Slides, Marketing",
            "deadline": "30 April",
            "task_details": "Deliver a short 5-slide deck with competitor benchmarking and positioning insights.",
            "status": "Open",
        },
        {
            "title": "Pitch Deck Refresh",
            "startup_name": "BrightLabs",
            "category": "Strategy",
            "location": "Remote",
            "duration": "1 week",
            "budget": "CHF 400",
            "remote_type": "Remote",
            "description": "Improve our investor pitch deck structure and sharpen the business story.",
            "skills_required": "Strategy, PowerPoint, Storytelling",
            "deadline": "2 May",
            "task_details": "Update the deck flow, sharpen wording, and improve the visual logic.",
            "status": "Open",
        },
        {
            "title": "UX Feedback Review",
            "startup_name": "Nova Studio",
            "category": "Design",
            "location": "Geneva",
            "duration": "4 days",
            "budget": "CHF 300",
            "remote_type": "On-site",
            "description": "Review the onboarding flow and identify friction points with improvement suggestions.",
            "skills_required": "UX, Figma, Design",
            "deadline": "5 May",
            "task_details": "Review the existing onboarding and suggest wireframe-level improvements.",
            "status": "Open",
        },
        {
            "title": "CRM Data Cleanup",
            "startup_name": "FlowTech",
            "category": "Operations",
            "location": "Remote",
            "duration": "2 days",
            "budget": "CHF 180",
            "remote_type": "Remote",
            "description": "Clean and reorganize lead records in our CRM and fix category tagging.",
            "skills_required": "Excel, Operations, Detail-oriented",
            "deadline": "28 April",
            "task_details": "Update CRM tags, deduplicate records, and create one clean export.",
            "status": "Open",
        },
        {
            "title": "Social Content Support",
            "startup_name": "SparkStudio",
            "category": "Marketing",
            "location": "Lausanne",
            "duration": "1 week",
            "budget": "CHF 220",
            "remote_type": "Hybrid",
            "description": "Help draft LinkedIn posts and content ideas for launch week.",
            "skills_required": "Content, Social Media, Copywriting",
            "deadline": "1 May",
            "task_details": "Prepare 5 LinkedIn post drafts and propose 3 campaign content angles.",
            "status": "Open",
        },
    ]

    for task in sample_tasks:
        conn.execute("""
        INSERT INTO tasks (
            title, startup_name, category, location, duration, budget,
            remote_type, description, skills_required, deadline, task_details, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task["title"],
            task["startup_name"],
            task["category"],
            task["location"],
            task["duration"],
            task["budget"],
            task["remote_type"],
            task["description"],
            task["skills_required"],
            task["deadline"],
            task["task_details"],
            task["status"],
        ))
    conn.commit()


# ---------- student profile ----------
def get_student_profile() -> Dict:
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
        "cv_name": "",
    }


def save_student_profile(profile: Dict):
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
        profile["cv_name"],
    ))
    conn.commit()


# ---------- startup profile ----------
def get_startup_profile() -> Dict:
    row = conn.execute("SELECT * FROM startup_profile WHERE id = 1").fetchone()
    if row:
        return dict(row)
    return {
        "id": 1,
        "startup_name": "",
        "industry": "",
        "location": "",
        "description": "",
        "contact_email": "",
    }


def save_startup_profile(profile: Dict):
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
        profile["contact_email"],
    ))
    conn.commit()


# ---------- tasks ----------
def create_task(task: Dict):
    conn.execute("""
    INSERT INTO tasks (
        title, startup_name, category, location, duration, budget,
        remote_type, description, skills_required, deadline, task_details, status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        task["title"],
        task["startup_name"],
        task["category"],
        task["location"],
        task["duration"],
        task["budget"],
        task["remote_type"],
        task["description"],
        task["skills_required"],
        task["deadline"],
        task.get("task_details", ""),
        task.get("status", "Open"),
    ))
    conn.commit()


def get_all_tasks() -> List[Dict]:
    rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]


def get_startup_tasks(startup_name: str) -> List[Dict]:
    rows = conn.execute("SELECT * FROM tasks WHERE startup_name = ? ORDER BY id DESC", (startup_name,)).fetchall()
    return [dict(r) for r in rows]


def update_task_details(task_id: int, details: str):
    conn.execute("UPDATE tasks SET task_details = ? WHERE id = ?", (details, task_id))
    conn.commit()


# ---------- saved ----------
def get_saved_task_ids() -> List[int]:
    rows = conn.execute("SELECT task_id FROM saved_tasks").fetchall()
    return [r["task_id"] for r in rows]


def save_task_for_student(task_id: int):
    conn.execute("INSERT OR IGNORE INTO saved_tasks (task_id) VALUES (?)", (task_id,))
    conn.commit()


def remove_saved_task(task_id: int):
    conn.execute("DELETE FROM saved_tasks WHERE task_id = ?", (task_id,))
    conn.commit()


# ---------- applications ----------
def create_application(application: Dict):
    conn.execute("""
    INSERT INTO applications (
        task_id, task_title, startup_name, student_name, email, phone,
        message, cv_name, status, task_details, submission_note, submission_link
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        application["task_id"],
        application["task_title"],
        application["startup_name"],
        application["student_name"],
        application["email"],
        application["phone"],
        application["message"],
        application["cv_name"],
        application.get("status", "Applied"),
        application.get("task_details", ""),
        application.get("submission_note", ""),
        application.get("submission_link", ""),
    ))
    conn.commit()


def get_applications_for_student(student_name: str) -> List[Dict]:
    rows = conn.execute("SELECT * FROM applications WHERE student_name = ? ORDER BY id DESC", (student_name,)).fetchall()
    return [dict(r) for r in rows]


def get_applications_for_startup(startup_name: str) -> List[Dict]:
    rows = conn.execute("SELECT * FROM applications WHERE startup_name = ? ORDER BY id DESC", (startup_name,)).fetchall()
    return [dict(r) for r in rows]


def update_application_status(application_id: int, status: str):
    conn.execute("UPDATE applications SET status = ? WHERE id = ?", (status, application_id))
    conn.commit()


def update_application_task_details(application_id: int, details: str):
    conn.execute("UPDATE applications SET task_details = ? WHERE id = ?", (details, application_id))
    conn.commit()


def submit_work(application_id: int, note: str, link: str):
    conn.execute("""
    UPDATE applications
    SET submission_note = ?, submission_link = ?, status = 'Submitted'
    WHERE id = ?
    """, (note, link, application_id))
    conn.commit()
