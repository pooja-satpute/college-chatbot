import sqlite3

def init_db():
    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS faq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        eligibility TEXT,
        fees TEXT,
        duration TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS scholarships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        details TEXT)''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
