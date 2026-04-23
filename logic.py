from typing import Dict, List


def normalize(text: str) -> str:
    return (text or "").strip().lower()


def recommendation_score(task: Dict, profile: Dict) -> int:
    score = 50

    interests = normalize(profile.get("interests", ""))
    education = normalize(profile.get("education", ""))
    availability = normalize(profile.get("availability", ""))

    title = normalize(task.get("title", ""))
    category = normalize(task.get("category", ""))
    description = normalize(task.get("description", ""))
    skills = normalize(task.get("skills_required", ""))

    combined_task_text = f"{title} {category} {description} {skills}"

    interest_words = [w.strip() for w in interests.replace(",", " ").split() if w.strip()]
    for word in interest_words:
        if word in combined_task_text:
            score += 6

    if education and education in combined_task_text:
        score += 8

    if availability == "part-time" and ("week" in normalize(task.get("duration", "")) or "day" in normalize(task.get("duration", ""))):
        score += 4

    if category in interests:
        score += 12

    if "remote" in normalize(task.get("remote_type", "")) and availability in ["flexible", "part-time", "evenings"]:
        score += 4

    return max(55, min(score, 98))


def attach_scores(tasks: List[Dict], profile: Dict) -> List[Dict]:
    scored = []
    for task in tasks:
        item = dict(task)
        item["match_score"] = recommendation_score(task, profile)
        scored.append(item)

    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored
