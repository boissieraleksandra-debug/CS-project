import streamlit as st
import streamlit.components.v1 as components
from utils.data_loader import load_jobs
from utils.recommender import calculate_match_score

st.title("🔥 Discover Jobs")

jobs = load_jobs()

if "job_index" not in st.session_state:
    st.session_state.job_index = 0

if "liked_jobs" not in st.session_state:
    st.session_state.liked_jobs = []

if "passed_jobs" not in st.session_state:
    st.session_state.passed_jobs = []

if "profile" not in st.session_state:
    st.session_state.profile = {
        "full_name": "",
        "linkedin": "",
        "education": "",
        "interests": "",
        "availability": ""
    }

liked_categories = [job["category"] for job in st.session_state.liked_jobs]

job_records = jobs.to_dict(orient="records")
for job in job_records:
    job["match_score"] = calculate_match_score(job, st.session_state.profile, liked_categories)

job_records = sorted(job_records, key=lambda x: x["match_score"], reverse=True)

query_params = st.query_params
swipe_action = query_params.get("swipe")

if swipe_action and st.session_state.job_index < len(job_records):
    current_job = job_records[st.session_state.job_index]

    if swipe_action == "right":
        st.session_state.liked_jobs.append(current_job)
    elif swipe_action == "left":
        st.session_state.passed_jobs.append(current_job)

    st.session_state.job_index += 1
    st.query_params.clear()
    st.rerun()

if st.session_state.job_index < len(job_records):
    job = job_records[st.session_state.job_index]

    swipe_card_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                background: transparent;
                font-family: Arial, sans-serif;
            }}

            .card {{
                width: 320px;
                height: 460px;
                background: white;
                border-radius: 20px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.15);
                padding: 20px;
                position: absolute;
                cursor: grab;
                user-select: none;
            }}

            .title {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 8px;
            }}

            .startup {{
                color: #666;
                margin-bottom: 12px;
            }}

            .info {{
                margin-bottom: 10px;
                font-size: 15px;
            }}

            .score {{
                font-size: 18px;
                font-weight: bold;
                color: #ff4b4b;
                margin-top: 12px;
            }}

            .hint {{
                margin-top: 18px;
                font-size: 14px;
                color: #888;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="card" id="swipeCard">
            <div class="title">{job['title']}</div>
            <div class="startup">{job['startup_name']}</div>
            <div class="info"><b>Category:</b> {job['category']}</div>
            <div class="info"><b>Description:</b> {job['short_description']}</div>
            <div class="info"><b>Pay:</b> ${job['pay_rate']}/hour</div>
            <div class="info"><b>Location:</b> {job['location']}</div>
            <div class="info"><b>Duration:</b> {job['duration']}</div>
            <div class="score">Match Score: {job['match_score']}%</div>
            <div class="hint">Swipe right = Interested ❤️<br>Swipe left = Pass ❌</div>
        </div>

        <script>
            const card = document.getElementById("swipeCard");

            let isDragging = false;
            let startX = 0;
            let currentX = 0;

            card.addEventListener("mousedown", startDrag);
            card.addEventListener("touchstart", startDrag);

            document.addEventListener("mousemove", drag);
            document.addEventListener("touchmove", drag);

            document.addEventListener("mouseup", endDrag);
            document.addEventListener("touchend", endDrag);

            function startDrag(e) {{
                isDragging = true;
                startX = e.touches ? e.touches[0].clientX : e.clientX;
                card.style.transition = "none";
            }}

            function drag(e) {{
                if (!isDragging) return;
                currentX = e.touches ? e.touches[0].clientX : e.clientX;
                let moveX = currentX - startX;
                let rotate = moveX * 0.05;
                card.style.transform = `translateX(${{moveX}}px) rotate(${{rotate}}deg)`;
            }}

            function endDrag() {{
                if (!isDragging) return;
                isDragging = false;

                let moveX = currentX - startX;

                if (moveX > 120) {{
                    card.style.transition = "transform 0.3s ease";
                    card.style.transform = "translateX(500px) rotate(25deg)";
                    setTimeout(() => {{
                        window.parent.location.search = "?swipe=right";
                    }}, 250);
                }} else if (moveX < -120) {{
                    card.style.transition = "transform 0.3s ease";
                    card.style.transform = "translateX(-500px) rotate(-25deg)";
                    setTimeout(() => {{
                        window.parent.location.search = "?swipe=left";
                    }}, 250);
                }} else {{
                    card.style.transition = "transform 0.3s ease";
                    card.style.transform = "translateX(0px) rotate(0deg)";
                }}
            }}
        </script>
    </body>
    </html>
    """

    components.html(swipe_card_html, height=520)

    with st.expander("View Job Details"):
        st.write(f"**Long Description:** {job['long_description']}")
        st.write(f"**Education Needed:** {job['education']}")
        st.write(f"**Availability Needed:** {job['availability']}")
        st.button("Contact Startup")
else:
    st.success("No more jobs left to discover.")
