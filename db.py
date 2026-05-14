"""
db.py — SQLite database layer for the Student↔Startup matching app.

This module is the ONLY place that talks to the database. Every other file
calls helper functions from here so we never have raw SQL spread across
the codebase. That keeps the rest of the app readable for the team.

Usage:
    from db import init_db, get_conn, create_student, list_open_jobs, ...
    init_db()                  # safe to call at app start; idempotent
"""

#This file is the one that is directly in relation with the database. 
# The other pages use this page to use its functions everytime they need to save or retrieve a data. So it acts as an intermediate.

import sqlite3
from pathlib import Path #tool that locates the files on the computer.

# The database is a single file in the project folder. Easy to back up/copy, delete or reset for demos.
DB_PATH = Path(__file__).parent / "app.db"

#So before the app can read anything from the database, it needs to "open a door to it", like having a connection to it.
#And we have 2 settings: we can access the data by column name and there's a relationship rule between the tables.
def get_conn():
    """Return a SQLite connection. Rows are accessible by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row     # row["name"] instead of row[0]
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

#Here this function creates the tables in the database when the app runs for the first time.
# The tables are like excel sheets with rows & columns.
# The IF NOT EXISTS means that there will be no problem if the tables already exist
#The existing tables won't be overwritten by new ones or anything -> won't crash.
def init_db():
    """Create all tables if they don't exist. Safe to call multiple times."""
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS students (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        name          TEXT NOT NULL,
        email         TEXT NOT NULL UNIQUE,
        linkedin      TEXT,
        cv_filename   TEXT,
        education     TEXT,
        interests     TEXT,
        availability  TEXT,
        created_at    TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS startups (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        name           TEXT NOT NULL,
        email          TEXT NOT NULL UNIQUE,
        phone          TEXT,
        industry       TEXT,
        description    TEXT,
        website        TEXT,
        logo_filename  TEXT,
        created_at     TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS jobs (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        startup_id   INTEGER NOT NULL REFERENCES startups(id) ON DELETE CASCADE,
        title        TEXT NOT NULL,
        short_desc   TEXT,
        long_desc    TEXT,
        requirements TEXT,
        location     TEXT,
        duration     TEXT,
        pay_rate     TEXT,
        industry     TEXT,
        tags         TEXT,
        image_url    TEXT,
        status       TEXT NOT NULL DEFAULT 'open'
                     CHECK (status IN ('open','in_progress','done')),
        created_at   TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS swipes (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id  INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
        job_id      INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
        action      TEXT NOT NULL CHECK (action IN ('like','dislike','click')),
        created_at  TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS applications (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id  INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
        job_id      INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
        status      TEXT NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending','accepted','declined','completed')),
        created_at  TEXT NOT NULL DEFAULT (datetime('now')),
        decided_at  TEXT,
        UNIQUE(student_id, job_id)
    );

    CREATE TABLE IF NOT EXISTS emails_log (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        to_email    TEXT NOT NULL,
        subject     TEXT NOT NULL,
        body        TEXT NOT NULL,
        sent_ok     INTEGER NOT NULL DEFAULT 0,
        error       TEXT,
        created_at  TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE INDEX IF NOT EXISTS idx_swipes_student ON swipes(student_id);
    CREATE INDEX IF NOT EXISTS idx_apps_student  ON applications(student_id);
    CREATE INDEX IF NOT EXISTS idx_apps_job      ON applications(job_id);
    """)
    conn.commit()
    conn.close()

#swipes recrds everytime a student scrolls trough the jobs and swipes either left or right.
#applications record everytime a student applies to a job, there's a status and the application cannot be duplicated.
#emails log: records the email that the app sends.
# ---------------------------------------------------------------------------
# Student helpers
#These functions takes care all info related to students (new profile info, changes, login details with the email & ID -> see if they have already an account)
# ---------------------------------------------------------------------------

def create_student(name, email, linkedin, cv_filename, education, interests, availability):
    """Insert a new student. Returns the new student id."""
    conn = get_conn()
    cur = conn.execute(
        """INSERT INTO students
                  (name, email, linkedin, cv_filename, education, interests, availability)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (name, email, linkedin, cv_filename, education, interests, availability),
    )
    conn.commit()
    sid = cur.lastrowid
    conn.close()
    return sid


def update_student(student_id, **fields):
    """Update any subset of student columns by keyword. Quietly no-ops if empty."""
    if not fields:
        return
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [student_id]
    conn = get_conn()
    conn.execute(f"UPDATE students SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()


def get_student_by_email(email):
    conn = get_conn()
    row = conn.execute("SELECT * FROM students WHERE email = ?", (email,)).fetchone()
    conn.close()
    return row


def get_student(student_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    conn.close()
    return row


# ---------------------------------------------------------------------------
# Startup helpers
#Same as student helpers but for startups.
# ---------------------------------------------------------------------------

def create_startup(name, email, phone, industry, description, website, logo_filename=None):
    conn = get_conn()
    cur = conn.execute(
        """INSERT INTO startups
                  (name, email, phone, industry, description, website, logo_filename)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (name, email, phone, industry, description, website, logo_filename),
    )
    conn.commit()
    sid = cur.lastrowid
    conn.close()
    return sid


def update_startup(startup_id, **fields):
    if not fields:
        return
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [startup_id]
    conn = get_conn()
    conn.execute(f"UPDATE startups SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()


def get_startup_by_email(email):
    conn = get_conn()
    row = conn.execute("SELECT * FROM startups WHERE email = ?", (email,)).fetchone()
    conn.close()
    return row


def get_startup_by_name(name):
    conn = get_conn()
    row = conn.execute("SELECT * FROM startups WHERE name = ?", (name,)).fetchone()
    conn.close()
    return row


def get_startup(startup_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM startups WHERE id = ?", (startup_id,)).fetchone()
    conn.close()
    return row


# ---------------------------------------------------------------------------
# Job helpers
#Takes care of all features related to the job listings.
# So it saves the new jobs and link them to the appropriate startup and gives the job ID.
# ---------------------------------------------------------------------------

def create_job(startup_id, title, short_desc, long_desc, requirements,
               location, duration, pay_rate, industry, tags, image_url):
    conn = get_conn()
    cur = conn.execute(
        """INSERT INTO jobs
                  (startup_id, title, short_desc, long_desc, requirements,
                   location, duration, pay_rate, industry, tags, image_url)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (startup_id, title, short_desc, long_desc, requirements,
         location, duration, pay_rate, industry, tags, image_url),
    )
    conn.commit()
    jid = cur.lastrowid
    conn.close()
    return jid

# Saves the changes made to the job listing.
def update_job(job_id, **fields):
    if not fields:
        return
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [job_id]
    conn = get_conn()
    conn.execute(f"UPDATE jobs SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()

def delete_job(job_id):
    conn = get_conn()
    conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()

#Groups all jobs with the status "open" + the startups info -> what is used to show the students the available jobs. -> "Discover" page"
def list_open_jobs():
    """All currently-open jobs joined with their startup info."""
    conn = get_conn()
    rows = conn.execute(
        """SELECT j.*, s.name AS startup_name, s.email AS startup_email,
                  s.phone AS startup_phone
           FROM jobs j JOIN startups s ON j.startup_id = s.id
           WHERE j.status = 'open'
           ORDER BY j.created_at DESC"""
    ).fetchall()
    conn.close()
    return rows

#Groups all cards/jobs posted per startup -> what is used to show the startups the jobs they posted and allows them to manage them. -> "Listing" page"
def list_jobs_for_startup(startup_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM jobs WHERE startup_id = ? ORDER BY created_at DESC",
        (startup_id,),
    ).fetchall()
    conn.close()
    return rows

#Goups the job by ID with some info about the startup
def get_job(job_id):
    conn = get_conn()
    row = conn.execute(
        """SELECT j.*, s.name AS startup_name, s.email AS startup_email,
                  s.phone AS startup_phone
           FROM jobs j JOIN startups s ON j.startup_id = s.id
           WHERE j.id = ?""",
        (job_id,),
    ).fetchone()
    conn.close()
    return row


# ---------------------------------------------------------------------------
# Swipe + application helpers
# Describes the app's matching system
# ---------------------------------------------------------------------------
#Records evry interaction and saves whether the students liked ,passed or just viewed the job.
def record_swipe(student_id, job_id, action):
    """action is one of 'like', 'dislike', 'click'."""
    assert action in ("like", "dislike", "click")
    conn = get_conn()
    conn.execute(
        "INSERT INTO swipes (student_id, job_id, action) VALUES (?, ?, ?)",
        (student_id, job_id, action),
    )
    conn.commit()
    conn.close()

#Categorises the swipes per student 
def list_swipes(student_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM swipes WHERE student_id = ? ORDER BY created_at DESC",
        (student_id,),
    ).fetchall()
    conn.close()
    return rows

#Here all the liked jobs are grouped + there's an indication whether they already applied to the job. -> useful for the likes jobs page
def list_liked_jobs(student_id):
    """Jobs the student liked, with startup info and an already_applied flag."""
    conn = get_conn()
    rows = conn.execute(
        """SELECT j.*, s.name AS startup_name,
                  EXISTS(SELECT 1 FROM applications a
                         WHERE a.student_id = ? AND a.job_id = j.id) AS already_applied
           FROM swipes sw
           JOIN jobs j     ON sw.job_id = j.id
           JOIN startups s ON j.startup_id = s.id
           WHERE sw.student_id = ? AND sw.action = 'like'
           GROUP BY j.id
           ORDER BY MAX(sw.created_at) DESC""",
        (student_id, student_id),
    ).fetchall()
    conn.close()
    return rows

#Baiscally this function makes that a student doesn't apply twice (or more) to a specific job. 
#So instead of crashing, the app will just return None.
def create_application(student_id, job_id):
    """Insert a pending application; returns id or None if it already exists."""
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO applications (student_id, job_id) VALUES (?, ?)",
            (student_id, job_id),
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

#Groups all pplications a specific student submitted + adds info about the job and the startup.
def list_applications_for_student(student_id):
    conn = get_conn()
    rows = conn.execute(
        """SELECT a.*, j.title AS job_title, j.industry,
                  s.name AS startup_name, s.email AS startup_email,
                  s.phone AS startup_phone
           FROM applications a
           JOIN jobs j     ON a.job_id = j.id
           JOIN startups s ON j.startup_id = s.id
           WHERE a.student_id = ?
           ORDER BY a.created_at DESC""",
        (student_id,),
    ).fetchall()
    conn.close()
    return rows

#Groups all applications submitted to the jobs posted by a specific startup + adds info about the job and the student. -> useful for the "Application" page of the startup.
def list_applications_for_startup(startup_id):
    """All applications across every job this startup has posted."""
    conn = get_conn()
    rows = conn.execute(
        """SELECT a.*, j.title AS job_title, j.industry,
                  st.name AS student_name, st.email AS student_email,
                  st.linkedin, st.education, st.interests, st.availability,
                  st.cv_filename
           FROM applications a
           JOIN jobs j      ON a.job_id = j.id
           JOIN students st ON a.student_id = st.id
           WHERE j.startup_id = ?
           ORDER BY a.created_at DESC""",
        (startup_id,),
    ).fetchall()
    conn.close()
    return rows

#Here it's the same as above but this time it's specific to a specific job rather than for all jobs from a startup.
def list_applications_for_job(job_id):
    conn = get_conn()
    rows = conn.execute(
        """SELECT a.*, st.name AS student_name, st.email AS student_email,
                  st.linkedin, st.education, st.interests, st.availability,
                  st.cv_filename
           FROM applications a
           JOIN students st ON a.student_id = st.id
           WHERE a.job_id = ?
           ORDER BY a.created_at DESC""",
        (job_id,),
    ).fetchall()
    conn.close()
    return rows

# Gets one specific application by its ID with the important info (from student, startup etc)
def get_application(app_id):
    conn = get_conn()
    row = conn.execute(
        """SELECT a.*, j.title AS job_title, j.industry,
                  st.name AS student_name, st.email AS student_email,
                  st.linkedin, st.education, st.interests, st.availability,
                  st.cv_filename,
                  s.name AS startup_name, s.email AS startup_email,
                  s.phone AS startup_phone
           FROM applications a
           JOIN jobs j      ON a.job_id = j.id
           JOIN students st ON a.student_id = st.id
           JOIN startups s  ON j.startup_id = s.id
           WHERE a.id = ?""",
        (app_id,),
    ).fetchone()
    conn.close()
    return row

#here the status of a job is updated + the time at which it was made.
def update_application_status(app_id, new_status):
    assert new_status in ("pending", "accepted", "declined", "completed")
    conn = get_conn()
    conn.execute(
        """UPDATE applications
           SET status = ?, decided_at = datetime('now')
           WHERE id = ?""",
        (new_status, app_id),
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Email-log helpers (used by mailer.py)
#These functions support the emailing system. 
# ---------------------------------------------------------------------------

#Every emmail sent or attemp to sent an email is recorded here with the details (sender, subject, recipient)etc) + if it succeeded.
def log_email(to_email, subject, body, sent_ok, error=None):
    conn = get_conn()
    conn.execute(
        """INSERT INTO emails_log (to_email, subject, body, sent_ok, error)
           VALUES (?, ?, ?, ?, ?)""",
        (to_email, subject, body, 1 if sent_ok else 0, error),
    )
    conn.commit()
    conn.close()

#Here the recent emails are recorded and they can be sorted by the recipients' address.
def list_emails(limit=20, to_email=None):
    """List recent emails. If to_email is given, only return emails sent to that address."""
    conn = get_conn()
    if to_email:
        rows = conn.execute(
            "SELECT * FROM emails_log WHERE to_email = ? ORDER BY created_at DESC LIMIT ?",
            (to_email, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM emails_log ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    conn.close()
    return rows
