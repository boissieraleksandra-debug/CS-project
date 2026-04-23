import streamlit as st
from db import init_db, get_all_tasks, save_task_for_student, get_saved_task_ids, get_student_profile
from logic import attach_scores
from ui import apply_styles, header, task_card

st.set_page_config(page_title="Discover Tasks", page_icon="🔍", layout="wide")
init_db()
apply_styles()

if st.session_state.get("role") != "student":
    st.stop()

header("🔍 Discover Tasks", "Browse startup tasks recommended for your profile and save the ones you like.")

profile = get_student_profile()
tasks = get_all_tasks()
saved_ids = set(get_saved_task_ids())

if profile["interests"]:
    st.success(f"Recommendations currently use your profile interests: {profile['interests']}")

if not tasks:
    st.info("No startup tasks have been posted yet.")
else:
    scored_tasks = attach_scores(tasks, profile)

    for task in scored_tasks:
        st.markdown(task_card(task, show_score=True), unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.button("Pass", key=f"pass_{task['id']}", use_container_width=True)

        with col2:
            with st.expander("View Details"):
                st.write(f"**Startup:** {task['startup_name']}")
                st.write(f"**Skills:** {task['skills_required']}")
                st.write(f"**Deadline:** {task['deadline']}")
                st.write(f"**Detailed instructions:** {task['task_details'] or 'Will be shared after matching.'}")

        with col3:
            if st.button("❤️ Save", key=f"save_{task['id']}", use_container_width=True):
                if task["id"] in saved_ids:
                    st.info("This task is already saved.")
                else:
                    save_task_for_student(task["id"])
                    st.success("Task saved.")
                    st.rerun()
