"""
8_Startup_Dashboard.py — Startup status & insights.
"""

import plotly.express as px
import streamlit as st

import auth
import ui
from db import (
    init_db,
    list_jobs_for_startup,
    list_applications_for_startup,
)

# this sets up the dashboard page and loads the layout of the app
st.set_page_config(page_title="Dashboard · gigly", page_icon="g", layout="centered", initial_sidebar_state="expanded")
init_db()
auth.restore_login()
ui.load_css()
ui.sidebar()

# ---- Auth guard ---------------------------------------------------------
if st.session_state.get("role") != "startup" or not st.session_state.get("startup_id"):
    st.warning("Please create your company profile first.")
    if st.button("Go to Company", type="primary", use_container_width=True):
        st.switch_page("pages/5_Startup_Profile.py")
    st.stop()

# here we get the id of the startup that is currently logged in so we can load its jobs and applicants
startup_id = st.session_state["startup_id"]

# these labels are used to show the job status and application status
JOB_STATUS_PILL = {
    "open":        ("open",        "Open"),
    "in_progress": ("in_progress", "In progress"),
    "done":        ("done",        "Done"),
}

APP_STATUS_PILL = {
    "pending":   ("pending",   "Pending"),
    "accepted":  ("accepted",  "Accepted (in progress)"),
    "declined":  ("declined",  "Declined"),
    "completed": ("completed", "Completed"),
}


def count_application_statuses(apps):
    # this function counts how many applications are pending, accepted, declined, or completed
    pending = 0
    accepted = 0
    declined = 0
    completed = 0

    for app in apps:
        if app["status"] == "pending":
            pending += 1
        if app["status"] == "accepted":
            accepted += 1
        if app["status"] == "declined":
            declined += 1
        if app["status"] == "completed":
            completed += 1
    return pending, accepted, declined, completed


def count_apps_by_job_id(apps):
    # here we count how many applications each job listing received so we can build the chart
    counts = {}
    for app in apps:
        job_id = app["job_id"]
        counts[job_id] = counts.get(job_id, 0) + 1
    return counts


def build_listing_chart_data(jobs, apps_by_job_id):
    # this builds the bar chart data and shortens long job titles so the chart stays easy to read
    chart_data = []
    for job in jobs:
        title = job["title"]
        if len(title) > 30:
            title = title[:30] + "…"
        chart_data.append(
            {
                "job": title,
                "applications": apps_by_job_id.get(job["id"], 0),
            }
        )
    return chart_data


def group_apps_by_job(apps):
    # here we group applications by job so each listing can show its own applicants
    grouped = {}
    for app in apps:
        job_id = app["job_id"]
        if job_id not in grouped:
            grouped[job_id] = []
        grouped[job_id].append(app)
    return grouped


def group_apps_by_status(apps):
    # this groups the applications by status inside one job listing, like pending or accepted
    grouped = {}
    for app in apps:
        status = app["status"]
        if status not in grouped:
            grouped[status] = []
        grouped[status].append(app)
    return grouped


# this is the title and short text shown at the top of the startup dashboard
st.markdown("# Dashboard")
st.caption("Listings and applicants at a glance.")
st.write("")

# here we load all jobs and applications linked to this startup from the database
jobs = list_jobs_for_startup(startup_id)
apps = list_applications_for_startup(startup_id)

# ---- KPI tiles -----------------------------------------------------------
# here we calculate the numbers shown at the top of the page, like listings and total applications
total_jobs    = len(jobs)
total_apps    = len(apps)
pending_apps, accepted_apps, declined_apps, completed_apps = count_application_statuses(apps)

# this row shows the startup dashboard metrics so the company gets a quick summary first
c1, c2, c3, c4 = st.columns(4)
c1.metric("Listings",   total_jobs)
c2.metric("Total apps", total_apps)
c3.metric("Pending",    pending_apps)
c4.metric("Accepted",   accepted_apps)

st.write("")

# ---- Bar chart: applications per listing --------------------------------
if jobs:
    # this chart shows how many applications each listing received so the startup can compare its roles
    st.markdown("### Applications per listing")
    apps_by_job_id = count_apps_by_job_id(apps)
    chart_data = build_listing_chart_data(jobs, apps_by_job_id)
    fig = px.bar(
        chart_data,
        x="job",
        y="applications",
        color="applications",
        color_continuous_scale=["#EDE5FC", "#A78BFA", "#7C3AED", "#5B21B6"],
    )
    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=300,
        showlegend=False,
        coloraxis_showscale=False,
        yaxis_title=None,
        xaxis_title=None,
        font=dict(family="Inter, -apple-system, sans-serif", color="#1B1530"),
    )
    st.plotly_chart(fig, use_container_width=True)

st.write("")

# ---- Per-job detailed breakdown -----------------------------------------------
# here we start the section that shows one breakdown card for each listing
st.markdown("### Per-listing breakdown")

if not jobs:
    # if the startup has no jobs yet we show a message
    st.info("Post your first role from the Listings page to see status here.")
    st.stop()

# here we organize the applications by job before showing the listing cards
apps_by_job = group_apps_by_job(apps)

for job in jobs:
    # for each listing, we get its applications and group them by status for an easier overview
    job_apps = apps_by_job.get(job["id"], [])
    by_status = group_apps_by_status(job_apps)

    # this card shows the listing title, its status, and total number of applications
    with st.container(border=True):
        head_l, head_r = st.columns([3, 1])
        with head_l:
            st.markdown(f"**{job['title']}**")
            cls, label = JOB_STATUS_PILL.get(job["status"], ("", job["status"]))
            st.markdown(
                f"<span class='status-pill {cls}'>{label}</span>",
                unsafe_allow_html=True,
            )
        with head_r:
            st.markdown(f"### {len(job_apps)}")
            st.caption("apps")

        if not job_apps:
            # if this listing has no applicants yet we show a simple message 
            st.caption("No applications yet.")
            continue

        # here we separate the applicants into status sections so the startup can review them more easily
        for status_key, (cls, status_label) in APP_STATUS_PILL.items():
            people = by_status.get(status_key, [])
            if not people:
                continue
            with st.expander(f"{status_label} · {len(people)}"):
                # inside each section, we show the student name and email for quick contact details
                for a in people:
                    st.write(f"• **{a['student_name']}** — {a['student_email']}")
