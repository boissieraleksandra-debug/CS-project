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


# ---------- APPLICATIONS ----------

def get_applications_for_startup(startup_name: str) -> List[Dict]:
    rows = conn.execute(
        "SELECT * FROM applications WHERE startup_name = ? ORDER BY id DESC",
        (startup_name,)
    ).fetchall()
    return [dict(r) for r in rows]


def get_applications_for_student(student_name: str) -> List[Dict]:
    rows = conn.execute(
        "SELECT * FROM applications WHERE student_name = ? ORDER BY id DESC",
        (student_name,)
    ).fetchall()
    return [dict(r) for r in rows]


def update_application_status(application_id: int, status: str):
    conn.execute(
        "UPDATE applications SET status = ? WHERE id = ?",
        (status, application_id)
    )
    conn.commit()


def update_application_task_details(application_id: int, details: str):
    conn.execute(
        "UPDATE applications SET task_details = ? WHERE id = ?",
        (details, application_id)
    )
    conn.commit()


def submit_work(application_id: int, note: str, link: str):
    conn.execute("""
    UPDATE applications
    SET submission_note = ?, submission_link = ?, status = 'Submitted'
    WHERE id = ?
    """, (note, link, application_id))
    conn.commit()


def cancel_application(application_id: int, reason: str):
    conn.execute("""
    UPDATE applications
    SET status = 'Cancelled', end_reason = ?
    WHERE id = ?
    """, (reason, application_id))
    conn.commit()
