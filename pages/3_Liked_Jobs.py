"""
3_Liked_Jobs.py — Saved jobs the student liked, with one-click Apply.
"""

import streamlit as st

import auth
import ui
from db import (
    init_db,
    list_liked_jobs,
    get_job,
    get_student,
    get_startup,
    create_application,
)
from mailer import send_email
from templates import (
    application_confirm_student,
    application_notify_startup,
)

st.set_page_config(page_title="Saved · gigly", page_icon="g", layout="centered", initial_sidebar_state="expanded")
init_db()
auth.restore_login()
ui.load_css()
ui.sidebar()

# ---- Auth guard: students only -----------------------------------------
if st.session_state.get("role") != "student" or not st.session_state.get("student_id"):
    st.warning("Please create your student profile first.")
    if st.button("Go to Profile", type="primary", use_container_width=True):
        st.switch_page("pages/1_Profile.py")
    st.stop()

student_id = st.session_state["student_id"]

st.markdown("# Saved roles")
st.caption("Gigs you said yes to. Apply when you're ready — we'll email the startup for you.")
st.write("")


def send_application_emails(student_id, job_id):
    student = get_student(student_id)
    full_job = get_job(job_id)
    startup = get_startup(full_job["startup_id"])

    subject, body = application_confirm_student(student, full_job, startup)
    send_email(student["email"], subject, body)

    subject2, body2 = application_notify_startup(student, full_job, startup)
    send_email(startup["email"], subject2, body2)


def render_liked_job(job, student_id):
    with st.container(border=True):
        if job["image_url"]:
            st.markdown(
                f"<div class='gigly-job-image-wrap'>"
                f"<div class='gigly-job-image' style=\"background-image:url('{job['image_url']}')\" aria-label='{job['title']}'></div>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.caption(f"{job['startup_name']}  ·  {job['industry']}")
        st.markdown(f"### {job['title']}")
        st.caption(f"{job['location']}  ·  {job['duration']}")
        st.write(job["short_desc"])

        with st.expander("View full description"):
            st.markdown("**About this role**")
            st.write(job["long_desc"])
            st.markdown("**What we're looking for**")
            st.write(job["requirements"])
            st.markdown(f"**Pay:**  {job['pay_rate']}")

        if job["already_applied"]:
            st.success("Applied — we'll email you when the startup decides.")
            return

        if st.button("Apply", key=f"apply_{job['id']}",
                     type="primary", use_container_width=True):
            app_id = create_application(student_id, job["id"])
            if app_id is None:
                st.warning("Already applied.")
                st.rerun()

            send_application_emails(student_id, job["id"])
            st.toast("Application sent.")
            st.rerun()

liked = list_liked_jobs(student_id)
if not liked:
    st.info(
        "Nothing saved yet. Open **Discover**, save a few gigs, "
        "and they'll show up here."
    )
    if st.button("Go to Discover", type="primary", use_container_width=True):
        st.switch_page("pages/2_Discovery.py")
    st.stop()

for job in liked:
    render_liked_job(job, student_id)
