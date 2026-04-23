import streamlit as st


def get_sample_tasks():
    return [
        {
            "id": 1,
            "title": "Market Research Sprint",
            "startup": "GrowthAI",
            "category": "Marketing",
            "location": "Zurich",
            "duration": "3 days",
            "pay": "CHF 250",
            "remote_type": "Hybrid",
            "description": "Research AI competitors and summarize 5 key market insights in a short slide deck.",
            "skills": ["Research", "Slides", "Marketing"],
            "match": 91,
            "deadline": "30 April",
        },
        {
            "id": 2,
            "title": "Pitch Deck Refresh",
            "startup": "BrightLabs",
            "category": "Strategy",
            "location": "Remote",
            "duration": "1 week",
            "pay": "CHF 400",
            "remote_type": "Remote",
            "description": "Help improve the structure, wording, and visual clarity of our investor pitch deck.",
            "skills": ["Strategy", "PowerPoint", "Storytelling"],
            "match": 87,
            "deadline": "2 May",
        },
        {
            "id": 3,
            "title": "UX Feedback Review",
            "startup": "Nova Studio",
            "category": "Design",
            "location": "Geneva",
            "duration": "4 days",
            "pay": "CHF 300",
            "remote_type": "On-site",
            "description": "Review our onboarding flow, identify friction points, and suggest UI improvements.",
            "skills": ["UX", "Figma", "Design"],
            "match": 84,
            "deadline": "5 May",
        },
        {
            "id": 4,
            "title": "CRM Data Cleanup",
            "startup": "FlowTech",
            "category": "Operations",
            "location": "Remote",
            "duration": "2 days",
            "pay": "CHF 180",
            "remote_type": "Remote",
            "description": "Clean and reorganize lead records in our CRM and tag key business categories.",
            "skills": ["Excel", "Operations", "Detail-oriented"],
            "match": 80,
            "deadline": "28 April",
        },
        {
            "id": 5,
            "title": "Social Content Support",
            "startup": "SparkStudio",
            "category": "Marketing",
            "location": "Lausanne",
            "duration": "1 week",
            "pay": "CHF 220",
            "remote_type": "Hybrid",
            "description": "Help draft LinkedIn posts, simple campaign ideas, and content captions for launch week.",
            "skills": ["Content", "Social Media", "Copywriting"],
            "match": 88,
            "deadline": "1 May",
        },
    ]


def initialize_state():
    if "tasks" not in st.session_state:
        st.session_state.tasks = get_sample_tasks()

    if "saved_tasks" not in st.session_state:
        st.session_state.saved_tasks = []

    if "applied_tasks" not in st.session_state:
        st.session_state.applied_tasks = []

    if "show_apply_for" not in st.session_state:
        st.session_state.show_apply_for = None

    if "profile" not in st.session_state:
        st.session_state.profile = {
            "full_name": "",
            "linkedin": "",
            "education": "",
            "availability": "",
            "interests": "",
            "bio": "",
            "cv_name": "",
        }


def task_exists(task_list, task_id):
    return any(task["id"] == task_id for task in task_list)


def save_task(task):
    if not task_exists(st.session_state.saved_tasks, task["id"]):
        st.session_state.saved_tasks.append(task)


def remove_saved_task(task_id):
    st.session_state.saved_tasks = [
        task for task in st.session_state.saved_tasks if task["id"] != task_id
    ]


def apply_to_task(task, applicant_data):
    if not task_exists(st.session_state.applied_tasks, task["id"]):
        new_task = task.copy()
        new_task["status"] = "Applied"
        new_task["applicant"] = applicant_data
        st.session_state.applied_tasks.append(new_task)
    remove_saved_task(task["id"])


def update_task_status(task_id, new_status):
    for task in st.session_state.applied_tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            break


def remove_applied_task(task_id):
    st.session_state.applied_tasks = [
        task for task in st.session_state.applied_tasks if task["id"] != task_id
    ]
