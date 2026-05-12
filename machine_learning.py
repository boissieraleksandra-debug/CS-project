"""
machine_learning.py: Logistic Regression job preference model.

This file is the learning core of the recommender system. It builds
training data from the student's past swipes, trains a Logistic Regression
model to predict which jobs they will like, and returns probability scores
for new unseen jobs.

If the student has fewer than 5 swipes, the model returns None and the
recommender falls back to the TF-IDF similarity approach in recommender.py.
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

from db import list_swipes, get_job



# Feature building part
# In this section we convert the job listings (title, description, tags, industry) 
# into plain text in one long string, that the computer can analyze. 

def job_to_text(job):
    return " ".join([
        job["title"] or "",
        job["long_desc"] or "",
        job["tags"] or "",
        job["industry"] or "",
    ])

def build_training_data(student_id: int):
    """
    Builds training data for logistic regression:

    X = job text (TF-IDF features)
    y = 1 (like), 0 (dislike)
    
    """

    # Here for every job you've swiped on, it records
    # what the jobs said and if you liked (1) or disliked (0) it.
    # This is the data that the model will learn from.

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



# Model training part

# Here the code checks, if there is enough past data to learn from
# so if a student has swiped on less then 5 jobs
# there is not enough data to spot a pattern, so it returns None.

def train_model(student_id: int):
    texts, y = build_training_data(student_id)

    if len(texts) < 5:
        return None, None
    
    # If there is enough data, it runs the text from the string through 
    # the TF-IDF vectorizer, which scores words from the string by how important 
    # they are to the respective jobs and how unique they are across all jobs.

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        max_features=2000,
        token_pattern=r"\b[a-zA-Z][a-zA-Z]+\b",
    )
    # Here we feed all the job description strings into the vectorizer.
    X = vectorizer.fit_transform(texts)

    # Here we create the Logistic Regression model.
    # max_iter=300 means "try up to 300 rounds of adjusting before giving up".
    # The model works by assigning a positive weight to words that appear
    # in liked jobs, and a negative weight to words from disliked jobs,
    # then uses those weights to score new unseen jobs.

    model = LogisticRegression(max_iter=300)
    model.fit(X, y)

    return model, vectorizer



# Prediction part

# Given the new trained model and a list of completely new jobs,
# this section converts each new job into text and asks the model
# to predict the probability that the student will like it (score from 0 to 1).

def predict_scores(model, vectorizer, jobs):
    """
    Returns probability that user will LIKE each job.
    Output: float array in range [0, 1]
    """

    job_texts = [job_to_text(j) for j in jobs]
    X = vectorizer.transform(job_texts)

    probs = model.predict_proba(X)[:, 1]  # probability of "like"

    return probs