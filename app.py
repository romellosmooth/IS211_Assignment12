from flask import Flask, request, redirect, render_template, session, url_for
import sqlite3


app = Flask(__name__)
app.secret_key = '173451'

@app.route('/')
def home():
    return redirect(url_for('login'))


def flask(param):
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['logged_in'] = True
            return redirect('/dashboard')
        else:
            flask("Incorrect credentials")
            return redirect('/login')
    return render_template('login.html')

@app.before_request
def require_login():
    if request.endpoint not in ['login', 'static'] and not session.get('logged_in'):
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):  # Ensure session is checked correctly
        return redirect(url_for('login'))

    conn = sqlite3.connect('hw13.db')
    c = conn.cursor()

    students = conn.execute('SELECT id, first_name, last_name FROM students').fetchall()
    quizzes = conn.execute('SELECT id, subject, num_questions, date FROM quizzes').fetchall()
    conn.close()

    return render_template('dashboard.html', students=students, quizzes=quizzes)



@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        try:
            conn = sqlite3.connect('hw13.db')
            c = conn.cursor()
            c.execute("INSERT INTO students (first_name, last_name) VALUES (?, ?)", (first, last))
            conn.commit()
            conn.close()
            return redirect('/dashboard')
        except:
            flash("Error adding student")
    return render_template('add_student.html')

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        subject = request.form['subject']
        num_questions = int(request.form['num_questions'])
        date = request.form['date']
        try:
            conn = sqlite3.connect('hw13.db')
            c = conn.cursor()
            c.execute("INSERT INTO quizzes (subject, num_questions, date) VALUES (?, ?, ?)", (subject, num_questions, date))
            conn.commit()
            conn.close()
            return redirect('/dashboard')
        except:
            flash("Error adding quiz")
    return render_template('add_quiz.html')



@app.route('/student/<int:id>')
def view_student(id):
    conn = sqlite3.connect('hw13.db')
    c = conn.cursor()
    results = c.execute('''SELECT quizzes.id, quizzes.subject, results.score
                           FROM results
                           JOIN quizzes ON results.quiz_id = quizzes.id
                           WHERE results.student_id = ?''', (id,)).fetchall()
    conn.close()
    return render_template('student_results.html', results=results)


@app.route('/results/add', methods=['GET', 'POST'])
def add_quiz_result():
    conn = sqlite3.connect('hw13.db')
    c = conn.cursor()

    if request.method == 'POST':
        student_id = request.form['student_id']
        quiz_id = request.form['quiz_id']
        score = request.form['score']
        try:
            c.execute("INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)",
                      (student_id, quiz_id, score))
            conn.commit()
            conn.close()
            return redirect('/dashboard')
        except:
            flash("Error adding result")
            conn.close()
            return redirect('/results/add')

    # On GET: fetch students and quizzes for dropdowns
    students = c.execute("SELECT id, first_name, last_name FROM students").fetchall()
    quizzes = c.execute("SELECT id, subject, num_questions, date FROM quizzes").fetchall()
    conn.close()
    return render_template('add_result.html', students=students, quizzes=quizzes)




if __name__ == '__main__':
    app.run(debug=True)
