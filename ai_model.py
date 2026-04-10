import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_all_data():
    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()

    data = []

    # FAQ
    cursor.execute("SELECT question, answer FROM faq")
    for q, a in cursor.fetchall():
        data.append((q, a))

    # Courses
    cursor.execute("SELECT name, eligibility, fees, duration FROM courses")
    for name, eligibility, fees, duration in cursor.fetchall():
        question = f"{name} course details fees eligibility duration"
        answer = f"{name}\nEligibility: {eligibility}\nFees: {fees}\nDuration: {duration}"
        data.append((question, answer))
    # Scholarships
    # Scholarships
    cursor.execute("SELECT name, details FROM scholarships")
    for name, details in cursor.fetchall():
        question = f"{name} scholarship details"
        answer = f"{name}\n{details}"
        data.append((question, answer))

    conn.close()
    return data


def get_answer(user_input):
    data = get_all_data()

    if not data:
        return "No data available."

    questions = [d[0] for d in data]
    answers = [d[1] for d in data]

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(questions + [user_input])

    similarity = cosine_similarity(vectors[-1], vectors[:-1])
    best_index = similarity.argmax()

    if similarity[0][best_index] > 0.2:
        return answers[best_index]
    else:
        return "Sorry, I couldn't find relevant information."