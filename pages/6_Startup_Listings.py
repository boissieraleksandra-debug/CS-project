"""
6_Startup_Listings.py — Startup's "main feed": their own job listings.
"""
# the page aims to allow the startups to manage the jobs they post. So they can 
# post new job, edit those already posted and so on. So we begin by importing the external tools we need. 

#import streamlit to be able to see the results.
import streamlit as st 

#These are modules created to handle the login & the session logic. So it checks who logged in 
# or takes care of restoring the session.
import auth

#Takes care of the visual part/ apprearance of the app.
import ui

#here instead of importing the whole database file, we import just the functions we need.
# 1. initialise databse -> setup the database structure the first time the program runs.
# 2. Inserts a new job that has been created into the database
#3. With that we can edit a job that has already been created.
#4. Collect all jobs belonging to a specific startup.
#5. Give info about the startup profile.
#6 Give info about the job details.
from db import (
    init_db,
    create_job,
    update_job,
    delete_job,
    list_jobs_for_startup,
    get_startup,
    get_job,
)

from mailer import send_email
from templates import job_listed_confirm

#The block will run again everytime the page loads or refreshes.
#It sets up how the browser looks like (the layout, tab, titles etc).
st.set_page_config(page_title="Listings · gigly", page_icon="g", layout="centered", initial_sidebar_state="expanded")
init_db()
auth.restore_login() #saves the session such that one stays logged in if the page gets refreshed.
ui.load_css()
ui.sidebar()

# ---- Auth guard: startups only -----------------------------------------
#ere the app makes sure that only startups can access this page. So if they don't have a profile set up, then they receive a message redirting them towards the profile page.
#So they cannot create jobs if they didn't set up a profile. 
if st.session_state.get("role") != "startup" or not st.session_state.get("startup_id"):
    st.warning("Please create your company profile first.")
    if st.button("Go to Company", type="primary", use_container_width=True):
        st.switch_page("pages/5_Startup_Profile.py")
    st.stop()

startup_id = st.session_state["startup_id"]
startup = get_startup(startup_id)

#Have some lists/ dico here to not have to retype them all the time. So we have the industries and the job status.
#The status shows whether the posted job is still running or is in progress (so a student is working on the task) or done.
INDUSTRY_CHOICES = ["Marketing", "Technology", "Finance", "Sustainability", "Design", "Other"]
STATUS_CHOICES = [
    ("open",        "Open (accepting applicants)"),
    ("in_progress", "In progress"),
    ("done",        "Done"),
]
STATUS_LABEL = dict(STATUS_CHOICES)
STATUS_CSS = {
    "open": "open",
    "in_progress": "in_progress",
    "done": "done",
}

#Here we made sure that every job card gets a picture even if the startup doesn't provide one on its own. It's based on the job title.
#So if they don't provide a picture, the function will pick a picture that matches the job, according the industry.
# reloads then it's still the same image.
def _default_image(title: str, industry: str = "") -> str:
    # Curated Unsplash photo IDs matched to job categories — deterministic, always relevant
    #Each category is mapped to a specific pcture ID.
    CATEGORY_IMAGES = {
        "software":   "photo-1517694712202-14dd9538aa97",  # laptop with code
        "design":     "photo-1561070791-2526d30994b5",     # design workspace
        "marketing":  "photo-1460925895917-afdab827c52f",  # marketing laptop
        "data":       "photo-1551288049-bebda4e38f71",     # analytics dashboard
        "sales":      "photo-1521791136064-7986c2920216",  # business handshake
        "product":    "photo-1507925921958-8a62f3d1a50d",  # sticky notes / planning
        "finance":    "photo-1554224155-8d04cb21cd6c",     # finance / charts
        "hr":         "photo-1529156069898-49953e39b3ac",  # team / people
        "operations": "photo-1454165804606-c3d57bc86b40",  # office operations
        "research":   "photo-1532094349884-543559c5b1dc",  # research / lab
        "customer":   "photo-1556742049-0cfed4f6a45d",    # customer service
        "legal":      "photo-1589829545856-d10d557cf95f",  # legal / documents
        "writing":    "photo-1455390582262-044cdead277a",  # writing / content
        "video":      "photo-1536240478700-b869ad10e128",  # video / camera
        "default":    "photo-1497366216548-37526070297c",  # modern office
    }
    #And here, each category has a list of keywords to ensure that the most words are covered and therefore get a picture.
    #Allows to reload thepage and still have the same picture.

    KEYWORDS = {
        "software":   ["software", "engineer", "developer", "coding", "backend", "frontend", "fullstack",
                        "web", "mobile", "app", "programmer", "devops", "cloud", "security", "cybersecurity",
                        "infrastructure", "platform", "api", "database", "qa", "testing", "embedded", "firmware"],
        "design":     ["design", "designer", "ux", "ui", "graphic", "visual", "creative", "art",
                        "illustration", "branding", "motion", "3d", "figma", "photoshop"],
        "marketing":  ["marketing", "growth", "seo", "content", "social media", "social", "brand",
                        "digital", "campaign", "media", "communications", "pr", "public relations",
                        "email", "copywriter", "copy", "blogger", "influencer", "advertising"],
        "data":       ["data", "analytics", "analyst", "scientist", "machine learning", "ai", "ml",
                        "artificial intelligence", "deep learning", "nlp", "bi", "business intelligence",
                        "statistics", "quantitative", "data engineer", "etl"],
        "sales":      ["sales", "business development", "biz dev", "account", "revenue", "bdr", "sdr",
                        "partnership", "partnerships", "deal", "closer", "commercial"],
        "product":    ["product", "pm", "product manager", "program manager", "project manager",
                        "scrum", "agile", "roadmap", "strategy"],
        "finance":    ["finance", "financial", "accounting", "accountant", "cfo", "controller",
                        "tax", "audit", "treasury", "investment", "budget", "payroll"],
        "hr":         ["hr", "human resources", "recruiting", "recruiter", "talent", "people",
                        "culture", "diversity", "onboarding", "benefits", "compensation"],
        "operations": ["operations", "ops", "logistics", "supply chain", "procurement",
                        "office manager", "facilities", "office", "admin", "administrative"],
        "research":   ["research", "researcher", "scientist", "lab", "biology", "chemistry",
                        "physics", "clinical", "scientific", "r&d"],
        "customer":   ["customer", "support", "success", "service", "helpdesk", "care",
                        "client", "cx", "community", "community manager"],
        "legal":      ["legal", "law", "lawyer", "attorney", "compliance", "regulatory",
                        "counsel", "policy", "privacy"],
        "writing":    ["writer", "writing", "editor", "editorial", "journalist", "reporter",
                        "technical writer", "documentation", "docs"],
        "video":      ["video", "film", "filmmaker", "cinematographer", "editor", "youtube",
                        "production", "multimedia", "podcast", "audio"],
    }
#If no key word matches, then the fall back option is chosen ("default photo").
    t = title.lower()
    for category, kws in KEYWORDS.items():
        if any(kw in t for kw in kws):
            pid = CATEGORY_IMAGES[category]
            return f"https://images.unsplash.com/{pid}?w=400&h=240&fit=crop&auto=format"

    return f"https://images.unsplash.com/{CATEGORY_IMAGES['default']}?w=400&h=240&fit=crop&auto=format"


# ---- Header + new-job toggle -------------------------------------------
#title Job Listing + ability to create a job by clicking on the + button, which then opens the job form.
header_l, header_r = st.columns([4, 1])
with header_l:
    st.markdown("# Listings")
with header_r:
    st.write("")
    if st.button("New", help="Post a new role", use_container_width=True):
        st.session_state["new_job_form_open"] = not st.session_state.get(
            "new_job_form_open", False,
        )
        st.rerun()

st.caption(f"{startup['name']} · {startup['industry'] or 'Industry not set'}")
st.write("")


# ---- New-job form (toggled) --------------------------------------------
#here the startups can create a new job card. they have to fulfill the fields. 
#The publish button Published is pressed then the required fields are checked (they must be fulfilled). 
#If correctly fulfilled then the job is saved in the database and the startup will receive a confirmation notification + the page will reload such that the job appears below and the job is saved in the database.
#Cancel button just closes the form without saving the job.
if st.session_state.get("new_job_form_open"):
    st.markdown("### Post a new role")
    with st.form("new_job"):
        title = st.text_input(
            "Role title *",
            placeholder="e.g. Marketing Analytics Intern",
        )
        short_desc = st.text_input(
            "Short description *",
            placeholder="One-sentence summary, shows on the card",
        )
        long_desc = st.text_area("Long description *", height=140)
        requirements = st.text_area(
            "Requirements", height=100,
            placeholder="Skills, tools, languages, etc.",
        )
        email = st.text_input("Email")
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("Location *", placeholder="Zurich, CH (hybrid)")
            duration = st.text_input("Duration *", placeholder="3 months")
        with col2:
            pay_rate = st.text_input("Pay rate *", placeholder="CHF 25/hr")
            ind_idx = (
                INDUSTRY_CHOICES.index(startup["industry"])
                if startup["industry"] in INDUSTRY_CHOICES else 0
            )
            industry = st.selectbox("Industry", INDUSTRY_CHOICES, index=ind_idx)
        tags = st.text_input(
            "Tags (comma-separated)",
            placeholder="data, analytics, marketing",
        )
        image_url = st.text_input(
            "Image URL (optional)",
            placeholder="leave empty to auto-generate one",
        )

        col_a, col_b = st.columns(2)
        with col_a:
            listed = st.form_submit_button(
                "Publish", type="primary", use_container_width=True,
            )
        with col_b:
            cancelled = st.form_submit_button("Cancel", use_container_width=True)

    if cancelled:
        st.session_state["new_job_form_open"] = False
        st.rerun()

    if listed:
        required = [title, short_desc, long_desc, location, duration, pay_rate]
        if not all(s.strip() for s in required):
            st.error("All fields marked with * are required.")
            st.stop()

        new_id = create_job(
            startup_id=startup_id,
            title=title.strip(),
            short_desc=short_desc.strip(),
            long_desc=long_desc.strip(),
            requirements=requirements.strip(),
            location=location.strip(),
            duration=duration.strip(),
            pay_rate=pay_rate.strip(),
            industry=industry,
            tags=tags.strip(),
            image_url=image_url.strip() or _default_image(title, industry),
        )

        new_job = get_job(new_id)
        subject, body = job_listed_confirm(startup, new_job)
        send_email(startup["email"], subject, body)

        st.session_state["new_job_form_open"] = False
        st.toast("Role published.")
        st.rerun()

st.write("")


# ---- Existing job listings ---------------------------------------------
#Here the jobs a startup has already posted, appear as card with the details of the jobs like the tags, duration, location etc.
#Each card has an edit button to edit the job if needed. The changes are then saved into the database and the page reloads to show them directly.
#The startup can also decide to delete a job listing.
jobs = list_jobs_for_startup(startup_id)

if not jobs:
    st.info("No listings yet. Click **New** above to post your first role.")
    st.stop()

for job in jobs:
    with st.container(border=True):
        if job["image_url"]:
            st.markdown(
                f"<div class='gigly-job-image-wrap'>"
                f"<div class='gigly-job-image' style=\"background-image:url('{job['image_url']}')\" aria-label='{job['title']}'></div>"
                f"</div>",
                unsafe_allow_html=True,
            )

        cls = STATUS_CSS.get(job["status"], "")
        st.markdown(
            f"<span class='status-pill {cls}'>"
            f"{STATUS_LABEL.get(job['status'], job['status'])}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(f"### {job['title']}")
        st.caption(
            f"{job['location']}  ·  {job['duration']}  ·  {job['pay_rate']}"
        )
        st.write(job["short_desc"])

        with st.expander("Edit role"):
            with st.form(f"edit_job_{job['id']}"):
                e_title = st.text_input("Title", value=job["title"])
                e_short = st.text_input("Short description", value=job["short_desc"])
                e_long = st.text_area(
                    "Long description", value=job["long_desc"], height=140,
                )
                e_req = st.text_area(
                    "Requirements", value=job["requirements"] or "", height=100,
                )
                ec1, ec2 = st.columns(2)
                with ec1:
                    e_location = st.text_input("Location", value=job["location"])
                    e_duration = st.text_input("Duration", value=job["duration"])
                with ec2:
                    e_pay = st.text_input("Pay rate", value=job["pay_rate"])
                    ind_idx = (
                        INDUSTRY_CHOICES.index(job["industry"])
                        if job["industry"] in INDUSTRY_CHOICES else 0
                    )
                    e_industry = st.selectbox(
                        "Industry", INDUSTRY_CHOICES, index=ind_idx,
                    )
                e_tags = st.text_input("Tags", value=job["tags"] or "")
                e_image = st.text_input("Image URL", value=job["image_url"] or "")

                stat_idx = next(
                    (i for i, (k, _) in enumerate(STATUS_CHOICES) if k == job["status"]),
                    0,
                )
                e_status = st.selectbox(
                    "Status",
                    [v for _, v in STATUS_CHOICES],
                    index=stat_idx,
                )
                e_status_key = next(k for k, v in STATUS_CHOICES if v == e_status)

                e_saved = st.form_submit_button(
                    "Save changes", type="primary", use_container_width=True,
                )

            if e_saved:
                update_job(
                    job["id"],
                    title=e_title.strip(),
                    short_desc=e_short.strip(),
                    long_desc=e_long.strip(),
                    requirements=e_req.strip() or None,
                    location=e_location.strip(),
                    duration=e_duration.strip(),
                    pay_rate=e_pay.strip(),
                    industry=e_industry,
                    tags=e_tags.strip() or None,
                    image_url=e_image.strip() or None,
                    status=e_status_key,
                )
                st.success("Role updated.")
                st.rerun()

            st.divider()
            confirm_key = f"confirm_delete_{job['id']}"
            st.checkbox("I want to delete this listing", key=confirm_key)
            if st.button(
                "Delete listing",
                key=f"delete_{job['id']}",
                type="primary",
                disabled=not st.session_state.get(confirm_key, False),
            ):
                delete_job(job["id"])
                st.toast("Listing deleted.")
                st.rerun()
