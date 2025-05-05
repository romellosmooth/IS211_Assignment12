import sqlite3

conn = sqlite3.connect('hw13.db')
c = conn.cursor()

# Load schema
with open('schema.sql') as f:
    c.executescript(f.read())

# Insert sample data
c.execute("INSERT INTO students (first_name, last_name) VALUES (?, ?)", ("John", "Smith"))
c.execute("INSERT INTO quizzes (subject, num_questions, date) VALUES (?, ?, ?)",
          ("Python Basics", 5, "2015-02-05"))
c.execute("INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)", (1, 1, 85))

conn.commit()
conn.close()
