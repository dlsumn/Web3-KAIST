from flask import Flask, Blueprint, render_template, request, flash
from signup import signup_bp, profile_bp
from post import post_bp
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 블루프린트 등록
app.register_blueprint(signup_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(post_bp)

# 루트 경로에 대한 라우팅
@app.route("/")
def index():
    return render_template("index.html")


def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL,
                 address TEXT NOT NULL,
                 private_key TEXT NOT NULL)''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS Post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reward_address TEXT NOT NULL);
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

