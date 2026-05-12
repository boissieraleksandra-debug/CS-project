# machine_learning.py
# Logistic Regression job preference model (hybrid recommender core)

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

from db import list_swipes, get_job


# -----------------------------
# Feature building
# -----------------------------

def job_to_text(job):
    return " ".join([
        job["title"] or "",
        job["long_desc"] or "",
        job["tags"] or "",
        job["industry"] or "",
    ])

#this does this
def build_training_data(student_id: int):
    """
    Builds training data for logistic regression:

    X = job text (TF-IDF features)
    y = 1 (like), 0 (dislike)
    """

    swipes = list_swipes(student_id)

    texts = []
    labels = []

    for s in swipes:
        job = get_job(s["job_id"])
        if not job:
            continue

        if s["action"] == "like":
            texts.append(job_to_text(job))
            labels.append(1)

        elif s["action"] == "dislike":
            texts.append(job_to_text(job))
            labels.append(0)

    return texts, np.array(labels)


# -----------------------------
# Model training
# -----------------------------

def train_model(student_id: int):
    texts, y = build_training_data(student_id)

    # Not enough data → fallback to TF-IDF system
    if len(texts) < 5:
        return None, None

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        max_features=2000,
        token_pattern=r"\b[a-zA-Z][a-zA-Z]+\b",
    )

    X = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=300)
    model.fit(X, y)

    return model, vectorizer


# -----------------------------
# Prediction
# -----------------------------

def predict_scores(model, vectorizer, jobs):
    """
    Returns probability that user will LIKE each job.
    Output: float array in range [0, 1]
    """

    job_texts = [job_to_text(j) for j in jobs]
    X = vectorizer.transform(job_texts)

    probs = model.predict_proba(X)[:, 1]  # probability of "like"

    return probs