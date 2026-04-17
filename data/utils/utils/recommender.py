def calculate_match_score(job, profile, liked_categories):
    score = 50

    if profile.get("education") and str(profile["education"]).lower() in str(job["education"]).lower():
        score += 15

    if profile.get("availability") and str(profile["availability"]).lower() in str(job["availability"]).lower():
        score += 15

    interests = profile.get("interests", "")
    if interests and str(job["category"]).lower() in interests.lower():
        score += 10

    if job["category"] in liked_categories:
        score += 10

    return min(score, 100)
