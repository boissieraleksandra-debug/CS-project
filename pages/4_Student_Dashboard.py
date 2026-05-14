"""
4_Student_Dashboard.py — The student's status & insights page.
"""

import plotly.express as px
import streamlit as st

import auth
import ui
from db import (
    init_db,
    list_applications_for_student,
    list_liked_jobs,
)

# this sets up the dashboard page and loads the shared layout used across the app
st.set_page_config(page_title="Dashboard · gigly", page_icon="g", layout="centered", initial_sidebar_state="expanded")
init_db()
auth.restore_login()
ui.load_css()
ui.sidebar()

# student-only access check
if st.session_state.get("role") != "student" or not st.session_state.get("student_id"):
    st.warning("Please create your student profile first.")
    if st.button("Go to Profile", type="primary", use_container_width=True):
        st.switch_page("pages/1_Profile.py")
    st.stop()

# here we get the id of the student who is currently logged in so we can load their dashboard data
student_id = st.session_state["student_id"]

# these colors are used in the charts on this page to keep the dashboard style consistent
PURPLE_PALETTE = {
    "Pending":                "#A78BFA",
    "Accepted (in progress)": "#7C3AED",
    "Completed":              "#5B21B6",
    "Declined":               "#C4B5FD",
}

INDUSTRY_PALETTE = {
    "Marketing":      "#EC4899",
    "Tech":           "#7C3AED",
    "Finance":        "#10B981",
    "Sustainability": "#06B6D4",
    "Design":         "#A78BFA",
}

# this keeps the label and helper text for each application status in one place for easier reuse
STATUS_PILL = {
    "pending":   ("pending",   "Pending",   "Waiting for the startup to decide."),
    "accepted":  ("accepted",  "Accepted",  "Check your email — the startup sent contact info."),
    "declined":  ("declined",  "Declined",  "Better luck next time."),
    "completed": ("completed", "Completed", "Job done."),
}


def count_application_statuses(apps):
    # this function counts how many applications are in each status so we can show metrics and charts
    counts = {}
    for app in apps:
        status = app["status"]
        counts[status] = counts.get(status, 0) + 1
    return counts


def build_status_chart_data(status_counts):
    # here we build the small data table used by the donut chart that shows the application breakdown
    chart_data = []
    status_pairs = [
        ("pending", "Pending"),
        ("accepted", "Accepted (in progress)"),
        ("completed", "Completed"),
        ("declined", "Declined"),
    ]
    for key, label in status_pairs:
        count = status_counts.get(key, 0)
        if count > 0:
            chart_data.append({"status": label, "count": count})
    return chart_data


def count_liked_industries(liked_jobs):
    # this function counts liked jobs by industry so we can see which areas interest the student most
    counts = {}
    for job in liked_jobs:
        industry = job["industry"]
        if industry:
            counts[industry] = counts.get(industry, 0) + 1
    return counts


def build_industry_chart_data(industry_counts):
    # here we turn the industry counts into a simple format that the bar chart can use
    chart_data = []
    for industry, count in industry_counts.items():
        chart_data.append({"industry": industry, "count": count})
    chart_data.sort(key=lambda row: row["count"], reverse=True)
    return chart_data


def render_application_card(app):
    # this function shows one application as a small dashboard card with its current status
    cls, label, hint = STATUS_PILL.get(app["status"], ("", "—", ""))
    with st.container(border=True):
        st.markdown(f"**{app['job_title']}** — *{app['startup_name']}*")
        st.markdown(
            f"<span class='status-pill {cls}'>{label}</span>"
            f" <span style='color:#8E8AA8;font-size:0.82rem'>"
            f"applied {app['created_at'][:10]}</span>",
            unsafe_allow_html=True,
        )
        st.caption(hint)
        if app["startup_email"]:
            st.markdown(f"**Company email:** {app['startup_email']}")


# this is the title and short text shown at the top of the dashboard page
st.markdown("# Dashboard")
st.caption("How your applications are going.")
st.write("")

# here we load the applications and liked jobs for this student from the database
apps = list_applications_for_student(student_id)
liked = list_liked_jobs(student_id)

# top metrics
# here we calculate the numbers shown in the top metrics row, like pending and completed
status_counts = count_application_statuses(apps)
total       = len(apps)
pending     = status_counts.get("pending",   0)
in_progress = status_counts.get("accepted",  0)
completed   = status_counts.get("completed", 0)

# this row shows the main dashboard metrics so the student gets a quick overview first
c1, c2, c3, c4 = st.columns([1.4, 1.4, 1.4, 1.4])
c1.metric("Applied",     total)
c2.metric("Pending",     pending)
c3.metric("In progress", in_progress)
c4.metric("Completed",   completed)

st.write("")

# application status chart
if total > 0:
    # this donut chart shows how the applications are split by status, like pending or completed
    st.markdown("### Application status")
    chart_data = build_status_chart_data(status_counts)
    fig = px.pie(
        chart_data,
        names="status",
        values="count",
        hole=0.6,
        color="status",
        color_discrete_map=PURPLE_PALETTE,
    )
    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=300,
        showlegend=True,
        font=dict(family="Inter, -apple-system, sans-serif", color="#1B1530"),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    # if there are no applications yet, we show a helpful message instead of an empty chart
    st.info("Apply to a few roles to see your status breakdown here.")

st.write("")

# saved jobs by industry chart
if liked:
    # this chart shows which industries appear most in the saved jobs the student liked
    st.markdown("### Saved roles by industry")
    industry_counts = count_liked_industries(liked)
    chart_data2 = build_industry_chart_data(industry_counts)
    fig2 = px.bar(
        chart_data2,
        x="industry",
        y="count",
        color="industry",
        color_discrete_map=INDUSTRY_PALETTE,
    )
    fig2.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=280,
        showlegend=False,
        yaxis_title=None,
        xaxis_title=None,
        font=dict(family="Inter, -apple-system, sans-serif", color="#1B1530"),
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    # if no jobs were saved yet, we show a helpful message instead of an empty chart
    st.info("Save a few roles in Discover to see your interests visualized here.")

st.write("")

# full application list
# here we show the full list of applications and their current status under the charts
st.markdown("### All applications")
if not apps:
    st.caption("You haven't applied to anything yet.")
else:
    for app in apps:
        render_application_card(app)
