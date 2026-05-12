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

# 1. Imports and Constants

# Here we import all the necessary tools needed
# json for readying sample data and Path for working with file paths
# We also import all the database functions we need to create startups and jobs

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

# This points to the folder, where our sample data is stored
# We also set up some constants to help with generating startup contact info
# These lookup tables map each industry to a 
# realistic email prefix and domain ending,
# so the seeder can generate convincing fake contact details 
# for each sample company.

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

# 2. Helper functions

# We read the json file and return the data as a Python object

def load_json(name):
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))

# Here we convert the startup name into a clean version
# without spaces or special characters,
# so it can be used to generate a realistic email address
# and website URL for each startup, based on their industry and name.

def _company_slug(name):
    return "".join(ch for ch in name.lower() if ch.isalnum() or ch == "-")

# Here comes the actual email generation function,
# Which uses the industry to look up a realistic email prefix
# and domain ending, and combines it with the cleaned up company name

def _startup_email(name, industry):
    industry_key = (industry or "").strip().lower()
    slug = _company_slug(name)
    if industry_key in CORPORATE_INDUSTRIES:
        prefix, tld = CORPORATE_DEFAULTS.get(industry_key, FALLBACK_CORPORATE)
    else:
        prefix, tld = STARTUP_DEFAULTS.get(industry_key, FALLBACK_STARTUP)
    return f"{prefix}@{slug}.{tld}"

# Here we build the URL from the email address
# By taking the domain part of the email
# and adding "https://" in front of it

def _website(name, industry):
    return "https://" + _startup_email(name, industry).split("@", 1)[1]

# This function takes the raw startup data from the JSON file,
# generates the email and website, 
# and returns a new dict with all the info.

def normalize_startup_contact(startup):
    startup = dict(startup)
    startup["email"] = _startup_email(startup["name"], startup.get("industry"))
    startup["website"] = _website(startup["name"], startup.get("industry"))
    return startup

# 3. Seeding functions

# Here we loop through every startup in the sample data
# and check if it already exists in the database (matched by email).
# If it already exists, we update the existing record 
# with any new information from the JSON file
# (like phone number, industry, description, website, logo).
# If it doesn't exist, we create a new record in the database.

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

# Here we load all job titles already in the database into a set
# So that we avoid inserting duplicates
# So for each json file, we skip, if a job with the same title
# already exists in the database.
# If the job is new, we look up the startup by email, and if it exists
# we create a new job record in the database linked to that startup.

def seed_jobs():
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

# 4. Main execution

# This block runs, when you execute this script directly,
# It initializes the database and runs the seeding functions.
# And prints done when you're finished
# You can run this script multiple times without creating duplicates,
# Thanks to our checks for existing startups and jobs
# before inserting new records.

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Seeding startups...")
    seed_startups()
    print("Seeding jobs...")
    seed_jobs()
    print("Done.")
