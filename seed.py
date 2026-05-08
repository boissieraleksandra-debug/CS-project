"""
seed.py — One-shot script that fills app.db with sample startups and jobs.

Run from the project root:
    python seed.py

It will:
  1) Create the database schema if needed (calls db.init_db()).
  2) Insert the 5 sample startups from data/sample_startups.json,
     skipping any that already exist (matched by email).
  3) Insert the 15 sample jobs from data/sample_jobs.json, looking up
     each startup by its email.

Re-running is safe — existing rows are not duplicated.
To reset everything: delete app.db, then run this script again.
"""

import json
from pathlib import Path

from db import (
    init_db,
    get_conn,
    create_startup,
    update_startup,
    get_startup_by_email,
    get_startup_by_name,
    create_job,
)

DATA_DIR = Path(__file__).parent / "data"
STARTUP_INDUSTRIES = {"marketing", "tech", "design", "sustainability"}
CORPORATE_INDUSTRIES = {"finance", "operations", "business development", "data / analytics"}
STARTUP_DEFAULTS = {
    "marketing": ("hello", "co"),
    "tech": ("talent", "io"),
    "design": ("hiring", "app"),
    "sustainability": ("people", "app"),
}
CORPORATE_DEFAULTS = {
    "finance": ("careers", "ch"),
    "operations": ("hr", "com"),
    "business development": ("recruiting", "com"),
    "data / analytics": ("careers", "ai"),
}
FALLBACK_STARTUP = ("hello", "app")
FALLBACK_CORPORATE = ("careers", "com")


def load_json(name):
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def _company_slug(name):
    return "".join(ch for ch in name.lower() if ch.isalnum() or ch == "-")


def _startup_email(name, industry):
    industry_key = (industry or "").strip().lower()
    slug = _company_slug(name)
    if industry_key in CORPORATE_INDUSTRIES:
        prefix, tld = CORPORATE_DEFAULTS.get(industry_key, FALLBACK_CORPORATE)
    else:
        prefix, tld = STARTUP_DEFAULTS.get(industry_key, FALLBACK_STARTUP)
    return f"{prefix}@{slug}.{tld}"


def _website(name, industry):
    return "https://" + _startup_email(name, industry).split("@", 1)[1]


def normalize_startup_contact(startup):
    startup = dict(startup)
    startup["email"] = _startup_email(startup["name"], startup.get("industry"))
    startup["website"] = _website(startup["name"], startup.get("industry"))
    return startup


def seed_startups():
    for raw_startup in load_json("sample_startups.json"):
        s = normalize_startup_contact(raw_startup)
        existing = get_startup_by_name(s["name"]) or get_startup_by_email(s["email"])
        if existing:
            update_startup(
                existing["id"],
                email=s["email"],
                phone=s.get("phone"),
                industry=s.get("industry"),
                description=s.get("description"),
                website=s.get("website"),
                logo_filename=s.get("logo_filename"),
            )
            print(f"  ~ startup: {s['name']}")
            continue
        create_startup(
            name=s["name"],
            email=s["email"],
            phone=s.get("phone"),
            industry=s.get("industry"),
            description=s.get("description"),
            website=s.get("website"),
            logo_filename=s.get("logo_filename"),
        )
        print(f"  + startup: {s['name']}")


def seed_jobs():
    # Avoid inserting jobs that share a title with an existing one — keeps
    # the seeder idempotent without needing a unique constraint on title.
    conn = get_conn()
    existing_titles = {row["title"] for row in conn.execute("SELECT title FROM jobs")}
    conn.close()

    for j in load_json("sample_jobs.json"):
        if j["title"] in existing_titles:
            continue
        startup = get_startup_by_email(j["startup_email"])
        if not startup:
            print(f"  ! skipping '{j['title']}' (startup '{j['startup_email']}' not found)")
            continue
        create_job(
            startup_id=startup["id"],
            title=j["title"],
            short_desc=j["short_desc"],
            long_desc=j["long_desc"],
            requirements=j["requirements"],
            location=j["location"],
            duration=j["duration"],
            pay_rate=j["pay_rate"],
            industry=j["industry"],
            tags=j["tags"],
            image_url=j["image_url"],
        )
        print(f"  + job: {j['title']}")


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Seeding startups...")
    seed_startups()
    print("Seeding jobs...")
    seed_jobs()
    print("Done.")
