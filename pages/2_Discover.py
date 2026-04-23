import streamlit as st
from app_data import initialize_state, save_task, task_exists
from ui import apply_global_styles, page_header, task_card_html

st.set_page_config(page_title="Discover Tasks", page_icon="🔍", layout="wide")

initialize_state()
apply_global_styles()
page_header("🔍 Discover Tasks", "Browse startup micro-tasks and save the ones that fit you best.")

profile = st.session_state.profile
tasks = st.session_state.tasks

if profile["interests"]:
    st.success(f"Recommendations are currently influenced by your interests: {profile['interests']}")

for task in tasks:
    st.markdown(task_card_html(task), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("Pass", key=f"pass_{task['id']}", use_container_width=True)

    with col2:
        with st.expander("View Details"):
            st.write(f"**Task:** {task['title']}")
            st.write(f"**Startup:** {task['startup']}")
            st.write(f"**Skills:** {', '.join(task['skills'])}")
            st.write(f"**Description:** {task['description']}")

    with col3:
        if st.button("❤️ Save", key=f"save_{task['id']}", use_container_width=True):
            already_saved = task_exists(st.session_state.saved_tasks, task["id"])
            already_applied = task_exists(st.session_state.applied_tasks, task["id"])

            if already_applied:
                st.info("You already applied to this task.")
            elif already_saved:
                st.info("This task is already saved.")
            else:
                save_task(task)
                st.success(f"Saved: {task['title']}")

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
