from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('studyplanner.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            chapters INTEGER,
            days INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    plan = []
    if request.method == 'POST':
        subject = request.form['subject']
        chapters = int(request.form['chapters'])
        days = int(request.form['days'])

        per_day = chapters // days
        extra = chapters % days

        current = 1

        for i in range(1, days + 1):
            end = current + per_day - 1
            if extra > 0:
                end += 1
                extra -= 1

            plan.append(f"Day {i}: Chapter {current} to {end}")
            current = end + 1

        # Save to database
        conn = sqlite3.connect('studyplanner.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO plans (subject, chapters, days) VALUES (?, ?, ?)",
            (subject, chapters, days)
        )
        conn.commit()
        conn.close()

    return render_template('index.html', plan=plan)

# Important for Render (Gunicorn will use this)
if __name__ == '__main__':
    app.run()