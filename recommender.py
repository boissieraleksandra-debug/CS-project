"""
recommender.py — TF-IDF + Logistic Regression + cosine similarity job recommender.

This is the project's "machine learning" component. It is now a hybrid system:
- Primary model: Logistic Regression (learns from user interactions)
- Fallback model: TF-IDF cosine similarity (cold start / low-data users)

We still keep the original TF-IDF logic because it is transparent and useful
for debugging and demo explanation.

How it works
------------
1. Build the corpus = every currently-open job as a single text:
       title + long_desc + tags + industry

2. Build the student profile text:
       interests + education + availability
   then append:
     * the text of every job the student LIKED (full weight)
     * the text of every job the student CLICKED (soft signal)

3. Train Logistic Regression on past user interactions (if enough data exists)
   and predict probability of "like" for each job.

4. If Logistic Regression is NOT possible (not enough data),
   fall back to TF-IDF + cosine similarity:

     * Fit TF-IDF vectorizer jointly on jobs + student
     * Penalize disliked jobs by subtracting 0.3 × mean disliked vector
     * Compute cosine similarity between student and jobs

5. Return the top N along with:
     * an integer match percentage (clipped to 1..99 so UI stays stable)
     * up to 2 "why this matches" terms from TF-IDF overlap (fallback only)

Each refresh re-runs this from scratch, which is what "the app learns"
looks like in the demo.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from db import (
    list_open_jobs,
    list_swipes,
    get_student,
    get_job,
)

from machine_learning import train_model, predict_scores


def _job_text(job):
    return " ".join([
        job["title"]    or "",
        job["long_desc"] or "",
        job["tags"]      or "",
        job["industry"]  or "",
    ])


def _student_text(student):
    return " ".join([
        student["interests"]    or "",
        student["education"]    or "",
        student["availability"] or "",
    ])


def _match_percent(score: float) -> int:
    """Turn a cosine score into a UI-friendly 1..99 percentage."""
    return max(1, min(99, round(score * 100)))


def recommend_jobs(student_id: int, max_results: int = 8):
    """Return [(job, match_pct, why_terms), ...] sorted by predicted match.

    `match_pct` is an int in 1..99.
    `why_terms` is a list of up to 2 short strings used by the UI
    as a "Matches your: …" caption.

    Already-liked / disliked jobs are filtered out.
    """

    student = get_student(student_id)
    if not student:
        return []

    swipes = list_swipes(student_id)
    decided_ids = {s["job_id"] for s in swipes if s["action"] in ("like", "dislike")}

    candidates = [j for j in list_open_jobs() if j["id"] not in decided_ids]
    if not candidates:
        return []

    # =========================================================
    # 1. MACHINE LEARNING LAYER (LOGISTIC REGRESSION)
    # =========================================================

    model, vectorizer = train_model(student_id)

    if model is not None:
        scores = predict_scores(model, vectorizer, candidates)

        order = np.argsort(scores)[::-1][:max_results]

        results = []
        for idx in order:
            pct = int(round(float(scores[idx]) * 100))
            pct = max(1, min(99, pct))

            results.append((candidates[idx], pct, []))

        return results

    # =========================================================
    # 2. FALLBACK: TF-IDF CONTENT-BASED MODEL
    # =========================================================

    job_texts = [_job_text(j) for j in candidates]

    # Build the student profile text + boost from interaction history.
    parts = [_student_text(student)]
    liked_ids    = [s["job_id"] for s in swipes if s["action"] == "like"]
    clicked_ids  = [s["job_id"] for s in swipes if s["action"] == "click"]
    disliked_ids = [s["job_id"] for s in swipes if s["action"] == "dislike"]

    for jid in liked_ids:
        j = get_job(jid)
        if j:
            parts.append(_job_text(j))   # full weight

    for jid in clicked_ids:
        j = get_job(jid)
        if j:
            parts.append(_job_text(j))   # soft signal

    student_text = " ".join(parts).strip()

    # Cold-start guard
    if not student_text:
        return [(j, 50, []) for j in candidates[:max_results]]

    vectorizer_tf = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        token_pattern=r"\b[a-zA-Z][a-zA-Z]+\b",
        max_features=2000,
    )

    matrix = vectorizer_tf.fit_transform(job_texts + [student_text])
    vocab = vectorizer_tf.get_feature_names_out()

    job_matrix  = matrix[: len(job_texts)]
    student_vec = np.asarray(matrix[len(job_texts):].todense())

    # Penalize disliked jobs
    if disliked_ids:
        disliked_texts = []
        for jid in disliked_ids:
            j = get_job(jid)
            if j:
                disliked_texts.append(_job_text(j))

        if disliked_texts:
            disliked = np.asarray(
                vectorizer_tf.transform(disliked_texts).mean(axis=0)
            )
            student_vec = np.maximum(student_vec - 0.3 * disliked, 0)

    # Score jobs
    scores = cosine_similarity(student_vec, job_matrix)[0]
    order = np.argsort(scores)[::-1][:max_results]

    # "why" explanation uses original (pre-penalty) vector
    student_vec_for_why = (
        np.asarray(matrix[len(job_texts):].todense()).ravel()
    )

    results = []

    for idx in order:
        pct = _match_percent(float(scores[idx]))
        job_vec = np.asarray(job_matrix[idx].todense()).ravel()
        overlap = student_vec_for_why * job_vec

        why = []
        if overlap.max() > 0:
            top2 = np.argsort(overlap)[::-1][:2]
            why = [vocab[i] for i in top2 if overlap[i] > 0]

        results.append((candidates[idx], pct, why))

    return results