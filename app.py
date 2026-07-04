"""
CodeAlpha Secure Coding Review — Sample Application
A small Flask-based user account and file-sharing service.

NOTE: This application is used purely as the subject of a secure code
review (Task 3). It intentionally reproduces vulnerability patterns
commonly found in early-stage web applications.
"""

import sqlite3
import os
import hashlib
import subprocess
from flask import Flask, request, render_template_string, redirect, session

app = Flask(__name__)
app.secret_key = "supersecret123"  # hardcoded secret key

DB_PATH = "users.db"
UPLOAD_DIR = "uploads"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, "
        "username TEXT, password TEXT, is_admin INTEGER DEFAULT 0)"
    )
    conn.execute(
        "INSERT OR IGNORE INTO users (id, username, password, is_admin) "
        "VALUES (1, 'admin', ?, 1)",
        (hashlib.md5(b"admin123").hexdigest(),),
    )
    conn.commit()
    conn.close()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Vulnerable: string-formatted SQL query (SQL Injection)
        conn = get_db()
        query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (
            username,
            hashlib.md5(password.encode()).hexdigest(),
        )
        cursor = conn.execute(query)
        user = cursor.fetchone()

        if user:
            session["user"] = username
            session["is_admin"] = bool(user[3])
            return redirect("/dashboard")
        return "Invalid credentials"

    return """
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit">
        </form>
    """


@app.route("/dashboard")
def dashboard():
    username = session.get("user", "Guest")
    # Vulnerable: unsanitized value rendered directly (Reflected/Stored XSS)
    greeting = request.args.get("msg", f"Welcome back, {username}!")
    return render_template_string(f"<h1>{greeting}</h1>")


@app.route("/download")
def download():
    # Vulnerable: user-controlled filename with no path sanitization (Path Traversal)
    filename = request.args.get("file")
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "rb") as f:
        return f.read()


@app.route("/ping")
def ping():
    # Vulnerable: user input passed to shell (Command Injection)
    host = request.args.get("host", "127.0.0.1")
    result = subprocess.check_output("ping -c 1 " + host, shell=True)
    return result


@app.route("/admin/promote")
def promote():
    # Vulnerable: missing authorization check (Broken Access Control)
    user_id = request.args.get("id")
    conn = get_db()
    conn.execute("UPDATE users SET is_admin = 1 WHERE id = ?", (user_id,))
    conn.commit()
    return "User promoted"


if __name__ == "__main__":
    init_db()
    # Vulnerable: debug mode enabled in what could be a production deployment
    app.run(debug=True, host="0.0.0.0")
