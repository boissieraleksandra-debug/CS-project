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

# this sets up the dashboard page and loads the layout of the app
st.set_page_config(page_title="Dashboard · gigly", page_icon="g", layout="centered", initial_sidebar_state="expanded")
init_db()
auth.restore_login()
ui.load_css()
ui.sidebar()

# ---- Auth guard ---------------------------------------------------------
if st.session_state.get("role") != "student" or not st.session_state.get("student_id"):
    st.warning("Please create your student profile first.")
    if st.button("Go to Profile", type="primary", use_container_width=True):
        st.switch_page("pages/1_Profile.py")
    st.stop()

# here we get the id of the student who is currently logged in so we can load their dashboard data
student_id = st.session_state["student_id"]

# these are the colors used in for the different phases of the application and the different industries
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

# this tells the dashboard what style, label, and message to show for each application status
STATUS_PILL = {
    "pending":   ("pending",   "Pending",   "Waiting for the startup to decide."),
    "accepted":  ("accepted",  "Accepted",  "Check your email — the startup sent contact info."),
    "declined":  ("declined",  "Declined",  "Better luck next time."),
    "completed": ("completed", "Completed", "Job done."),
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


def build_status_chart_data(pending, accepted, declined, completed):
    # here is the data table used by the donut chart that shows the application breakdown
    chart_data = []

    if pending > 0:
        chart_data.append({"status": "Pending", "count": pending})
    if accepted > 0:
        chart_data.append({"status": "Accepted (in progress)", "count": accepted})
    if completed > 0:
        chart_data.append({"status": "Completed", "count": completed})
    if declined > 0:
        chart_data.append({"status": "Declined", "count": declined})
    return chart_data


def count_liked_industries(liked_jobs):
    # this function counts liked jobs by industry so we can see which areas interest the student most
    marketing = 0
    tech = 0
    finance = 0
    sustainability = 0
    design = 0

    for job in liked_jobs:
        industry = job["industry"]
        if industry == "Marketing":
            marketing += 1
        if industry == "Tech":
            tech += 1
        if industry == "Finance":
            finance += 1
        if industry == "Sustainability":
            sustainability += 1
        if industry == "Design":
            design += 1
    return marketing, tech, finance, sustainability, design


def build_industry_chart_data(marketing, tech, finance, sustainability, design):
    # # here we put the industry data into the format the chart needs and sort it from biggest to smallest
    chart_data = []

    if marketing > 0:
        chart_data.append({"industry": "Marketing", "count": marketing})
    if tech > 0:
        chart_data.append({"industry": "Tech", "count": tech})
    if finance > 0:
        chart_data.append({"industry": "Finance", "count": finance})
    if sustainability > 0:
        chart_data.append({"industry": "Sustainability", "count": sustainability})
    if design > 0:
        chart_data.append({"industry": "Design", "count": design})

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

# ---- KPI tiles ----------------------------------------------------------
# here we calculate the numbers we want to show at the top, like applied, pending, and completed 
total       = len(apps)
pending, in_progress, declined, completed = count_application_statuses(apps)

# wider ratio for the last two columns so "In progress" and "Completed" don't get truncated
c1, c2, c3, c4 = st.columns([2, 2, 3, 3])
c1.metric("Applied",     total)
c2.metric("Pending",     pending)
c3.metric("In progress", in_progress)
c4.metric("Completed",   completed)

st.write("")

# ---- Donut chart: status breakdown --------------------------------------
if total > 0:
    # this donut chart shows how the applications are split by status, like pending or completed
    st.markdown("### Application status")
    chart_data = build_status_chart_data(pending, in_progress, declined, completed)
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
    # if there are no applications yet, we show a message 
    st.info("Apply to a few roles to see your status breakdown here.")

st.write("")

# ---- Bar chart: liked jobs by industry ----------------------------------
if liked:
    # this chart shows which industries appear most in the saved jobs the student liked
    st.markdown("### Saved roles by industry")
    marketing, tech, finance, sustainability, design = count_liked_industries(liked)
    chart_data2 = build_industry_chart_data(marketing, tech, finance, sustainability, design)
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
    # if no jobs were saved yet we show a message 
    st.info("Save a few roles in Discover to see your interests visualized here.")

st.write("")

# ---- Detailed application list ------------------------------------------
# here we show the full list of applications and their current status under the charts
st.markdown("### All applications")
if not apps:
    st.caption("You haven't applied to anything yet.")
else:
    for app in apps:
        render_application_card(app)
