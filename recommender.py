"""
recommender.py: Hybrid job recommender (Logistic Regression + TF-IDF fallback).

This file decides which jobs to show each student. It filters out already-decided
jobs, then ranks the remaining candidates using one of two approaches:
- Primary: Logistic Regression from machine_learning.py (if enough swipe data exists)
- Fallback: TF-IDF cosine similarity, which matches the student's profile text
  against each job's text, and penalizes jobs similar to ones they disliked.

Each call re-runs the ranking from scratch so recommendations improve over time.
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



# Helper Function

from machine_learning import train_model, predict_scores

# Here we build the foundation for the recommender system
# We take the jobs and stitch title, description, tags, industry 
# into one long string of text.

def _job_text(job):
    return " ".join([
        job["title"]    or "",
        job["long_desc"] or "",
        job["tags"]      or "",
        job["industry"]  or "",
    ])

# Here we do the same thing for the students, 
# we take their interests, education, availability
# and stitch them into one long string of text.

def _student_text(student):
    return " ".join([
        student["interests"]    or "",
        student["education"]    or "",
        student["availability"] or "",
    ])

# Here we convert decimal scores into percentages between 1 and 99

def _match_percent(score: float) -> int:
    """Turn a cosine score into a UI-friendly 1..99 percentage."""
    return max(1, min(99, round(score * 100)))



# Main recommendation function

def recommend_jobs(student_id: int, max_results: int = 8):

    # Here we load the students from the database
    # Then we look up all the jobs they've swiped on
    # And filter those out from the recommendation candidates.

    # We check if the student exists, if not we return an empty list.

    student = get_student(student_id)
    if not student:
        return []

    # We check all the jobs the student has swiped on, and we create a set of 
    # Job IDs that they have already decided on (liked or disliked).

    swipes = list_swipes(student_id)
    decided_ids = {s["job_id"] for s in swipes if s["action"] in ("like", "dislike")}

    # We get a list of all the open jobs, and filter out the ones they've already decided on.
    # If nothing is left, meaning the student has already swiped on every single job 
    # then we return an empty list.

    candidates = [j for j in list_open_jobs() if j["id"] not in decided_ids]
    if not candidates:
        return []

    

    # 1. MACHINE LEARNING LAYER (LOGISTIC REGRESSION)
    
    # Here we call on the machine learning code in machine_learning.py 
    # to train a Logistic Regression model on the student's past swipes
    model, vectorizer = train_model(student_id)

    # if there is enough past data to train a model, we use it
    # to predict scores for the candidate jobs
    # and then we sort the candidates by score and return the top results.

    if model is not None:
        scores = predict_scores(model, vectorizer, candidates)

        order = np.argsort(scores)[::-1][:max_results]

        results = []
        for idx in order:
            pct = int(round(float(scores[idx]) * 100))
            pct = max(1, min(99, pct))

            results.append((candidates[idx], pct, []))

        return results

    

    # 2. FALLBACK: TF-IDF CONTENT-BASED MODEL

    # If there is not enough past data to train a model
    # we fall back to a simpler TF-IDF + cosine similarity approach,
    # which doesn't learn weights but just matches the student's profile text
    # against the job texts, and penalizes jobs similar to ones they disliked.
  
    # First we convert all the candidate jobs into text using the _job_text function.

    job_texts = [_job_text(j) for j in candidates]

    # Then we create the student's profile text by combining 
    # their own info with the text of jobs they liked or clicked on.

    parts = [_student_text(student)]
    liked_ids    = [s["job_id"] for s in swipes if s["action"] == "like"]
    clicked_ids  = [s["job_id"] for s in swipes if s["action"] == "click"]
    disliked_ids = [s["job_id"] for s in swipes if s["action"] == "dislike"]

    # Here we give more weight to the jobs they liked, and less weight 
    # to the jobs they clicked on, meaning we treat clicks as a positive signal,
    # but not as strong as likes. We ignore dislikes for now, and apply those as
    # a penalty later on.

    for jid in liked_ids:
        j = get_job(jid)
        if j:
            parts.append(_job_text(j))   # full weight

    for jid in clicked_ids:
        j = get_job(jid)
        if j:
            parts.append(_job_text(j))   # soft signal

    
    # Here we combine all the parts into one long string 
    # of text for the student profile. 
    # If the student has no text at all, it returns the first 8 jobs 
    # with a default 50% match score, as there is nothing to compare against yet.

    student_text = " ".join(parts).strip()
    
    if not student_text:
        return [(j, 50, []) for j in candidates[:max_results]]

    # Here we set up the TF-IDF vectorizer, which will convert the job listings
    # and the student profiles into vectors of numbers that we can do math with.
    # Because then the word scoring is consistent 
    # between student profile and job listing
    # It also removes common stop words like "the" and "and", and only looks
    # at words that are purely alphabetic and at least 2 characters long, and it
    # only keeps the top 2000 most important words to reduce noise.

    vectorizer_tf = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        token_pattern=r"\b[a-zA-Z][a-zA-Z]+\b",
        max_features=2000,
    )

    matrix = vectorizer_tf.fit_transform(job_texts + [student_text])
    vocab = vectorizer_tf.get_feature_names_out()

    # Here we split the matrix from before into two parts
    # One is the job matrix and one the student vector
    # We have to separate them, to compare them against each other.

    job_matrix  = matrix[: len(job_texts)]
    student_vec = np.asarray(matrix[len(job_texts):].todense())

    # Penalize disliked jobs
    # Here we take the jobs, that the student disliked
    # and we apply a penalty to the student vector
    # Which means, we move the student vector further away
    # from the disliked jobs in the vector space
    # So, that they score lower on similar jobs in the future.

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

    # Here we then measure how similar the student vector is
    # to the job matrix using cosine similarity,
    # which gives us a score for each job, 
    # and then we sort the jobs by score and take the top results

    scores = cosine_similarity(student_vec, job_matrix)[0]
    order = np.argsort(scores)[::-1][:max_results]

    # "why" explanation uses original (pre-penalty) vector
    # Here we take the original student vector, pre-penalty
    # And we compare it to the job vectores, to see, 
    # which words are the reason for the match, by looking at the overlap
    # between the student vector and the job vector,
    # and we pick the top 2 words that have the most overlap as the "why
    
    student_vec_for_why = (
        np.asarray(matrix[len(job_texts):].todense()).ravel()
    )

    results = []

    # For each of the top recommended jobs, we then score 
    # the match percentage and also generate a "why" explanation 
    # by looking at the word overlap between
    # the student and job vector
    # We then return a list of recommended jobs, 
    # each with a match percentage and a list of "why" words

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