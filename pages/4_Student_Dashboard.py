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

student_id = st.session_state["student_id"]

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

STATUS_PILL = {
    "pending":   ("pending",   "Pending",   "Waiting for the startup to decide."),
    "accepted":  ("accepted",  "Accepted",  "Check your email — the startup sent contact info."),
    "declined":  ("declined",  "Declined",  "Better luck next time."),
    "completed": ("completed", "Completed", "Job done."),
}


def count_application_statuses(apps):
    counts = {}
    for app in apps:
        status = app["status"]
        counts[status] = counts.get(status, 0) + 1
    return counts


def build_status_chart_data(status_counts):
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
    counts = {}
    for job in liked_jobs:
        industry = job["industry"]
        if industry:
            counts[industry] = counts.get(industry, 0) + 1
    return counts


def build_industry_chart_data(industry_counts):
    chart_data = []
    for industry, count in industry_counts.items():
        chart_data.append({"industry": industry, "count": count})
    chart_data.sort(key=lambda row: row["count"], reverse=True)
    return chart_data


def render_application_card(app):
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

st.markdown("# Dashboard")
st.caption("How your applications are going.")
st.write("")

apps = list_applications_for_student(student_id)
liked = list_liked_jobs(student_id)

# ---- KPI tiles ----------------------------------------------------------
status_counts = count_application_statuses(apps)
total       = len(apps)
pending     = status_counts.get("pending",   0)
in_progress = status_counts.get("accepted",  0)
completed   = status_counts.get("completed", 0)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Applied",     total)
c2.metric("Pending",     pending)
c3.metric("In progress", in_progress)
c4.metric("Completed",   completed)

st.write("")

# ---- Donut chart: status breakdown --------------------------------------
if total > 0:
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
    st.info("Apply to a few roles to see your status breakdown here.")

st.write("")

# ---- Bar chart: liked jobs by industry ----------------------------------
if liked:
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
    st.info("Save a few roles in Discover to see your interests visualized here.")

st.write("")

# ---- Detailed application list ------------------------------------------
st.markdown("### All applications")
if not apps:
    st.caption("You haven't applied to anything yet.")
else:
    for app in apps:
        render_application_card(app)
