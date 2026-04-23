import streamlit as st

STATUS_COLORS = {
    "Applied": "#EF4444",
    "Matched": "#3B82F6",
    "In Progress": "#F59E0B",
    "Submitted": "#8B5CF6",
    "Completed": "#10B981",
    "Rejected": "#6B7280",
}

CATEGORY_COLORS = {
    "Marketing": "#EC4899",
    "Strategy": "#8B5CF6",
    "Design": "#06B6D4",
    "Operations": "#F97316",
    "Product": "#3B82F6",
    "Research": "#14B8A6",
    "Tech": "#6366F1",
}


def apply_styles():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #F8FAFF 0%, #F3F5FB 100%);
    }

    .block-container {
        max-width: 1120px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: #111827;
        letter-spacing: -0.4px;
    }

    .hero-card {
        background: linear-gradient(135deg, #6C63FF 0%, #4F46E5 100%);
        border-radius: 30px;
        padding: 38px;
        color: white;
        box-shadow: 0 20px 44px rgba(79, 70, 229, 0.22);
        margin-bottom: 26px;
    }

    .hero-title {
        font-size: 44px;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 17px;
        line-height: 1.6;
        color: rgba(255,255,255,0.92);
        max-width: 720px;
    }

    .page-title {
        font-size: 40px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 6px;
    }

    .page-subtitle {
        font-size: 16px;
        color: #6B7280;
        margin-bottom: 22px;
    }

    .app-card {
        background: white;
        border: 1px solid #E8ECF4;
        border-radius: 26px;
        padding: 22px;
        box-shadow: 0 12px 28px rgba(17, 24, 39, 0.06);
        margin-bottom: 16px;
    }

    .task-title {
        font-size: 24px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 4px;
    }

    .task-startup {
        font-size: 14px;
        color: #6B7280;
        margin-bottom: 12px;
    }

    .task-description {
        color: #4B5563;
        font-size: 15px;
        line-height: 1.65;
        margin-bottom: 14px;
    }

    .pill {
        display: inline-block;
        padding: 8px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 800;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .neutral-pill {
        background: #F3F4F6;
        color: #374151;
    }

    .soft-pill {
        background: #EEF2FF;
        color: #4338CA;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #E8ECF4;
        padding: 18px;
        border-radius: 22px;
        box-shadow: 0 10px 30px rgba(17, 24, 39, 0.05);
    }

    .small-note {
        color: #6B7280;
        font-size: 13px;
        margin-top: -6px;
        margin-bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True)


def header(title: str, subtitle: str):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def status_badge(status: str):
    color = STATUS_COLORS.get(status, "#111827")
    return f"""
    <span style="
        display:inline-block;
        padding:8px 14px;
        border-radius:999px;
        font-size:12px;
        font-weight:800;
        background:{color};
        color:white;
        margin-top:10px;
    ">{status}</span>
    """


def category_badge(category: str):
    color = CATEGORY_COLORS.get(category, "#6B7280")
    return f"""
    <span style="
        display:inline-block;
        padding:8px 12px;
        border-radius:999px;
        font-size:12px;
        font-weight:800;
        background:{color};
        color:white;
        margin-right:8px;
        margin-bottom:8px;
    ">{category}</span>
    """


def task_card(task: dict, show_status: bool = False, show_score: bool = False):
    category_html = category_badge(task["category"])
    status_html = status_badge(task["status"]) if show_status and "status" in task else ""

    score_html = ""
    if show_score and "match_score" in task:
        score_html = f'<span class="pill soft-pill">🎯 {task["match_score"]}% match</span>'

    return f"""
    <div class="app-card">
        <div class="task-title">{task['title']}</div>
        <div class="task-startup">🏢 {task['startup_name']}</div>
        <div class="task-description">{task['description']}</div>

        {category_html}
        <span class="pill neutral-pill">📍 {task['location']}</span>
        <span class="pill neutral-pill">⏳ {task['duration']}</span>
        <span class="pill neutral-pill">💰 {task['budget']}</span>
        <span class="pill neutral-pill">🖥️ {task['remote_type']}</span>
        <span class="pill neutral-pill">🛠️ {task['skills_required']}</span>
        <span class="pill neutral-pill">⏰ Apply by {task['deadline']}</span>
        {score_html}

        <div style="margin-top:8px;">
            {status_html}
        </div>
    </div>
    """
