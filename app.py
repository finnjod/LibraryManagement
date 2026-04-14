import psycopg2
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()  # reads your .env file

def connect():
    return psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT", "5432")
    )


def view_books(search=None):
    conn = connect()
    cur = conn.cursor()

    if search:
        fuzzy = search[:-1] if len(search) > 3 else search
        # Build patterns as variables first — avoids psycopg2 % conflict
        p1 = f"%{search}%"
        p2 = f"%{fuzzy}%"
        cur.execute(
            """SELECT * FROM libraryspn 
               WHERE title ILIKE %s OR author ILIKE %s
               OR title ILIKE %s OR author ILIKE %s""",
            (p1, p1, p2, p2)
        )
    else:
        cur.execute("SELECT * FROM libraryspn")

    books = cur.fetchall()
    cur.close()
    conn.close()
    return books

def add_book(title, author):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO books (title, author) VALUES (%s, %s)",
        (title, author)
    )
    conn.commit()
    cur.close()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    search = request.form.get("search", "")
    books = view_books(search)
    return render_template("index.html", books=books, search=search)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    author = request.form.get("author")
    if title and author:
        add_book(title, author)
    return index()  # Re-render the page after adding

if __name__ == "__main__":
    app.run(debug=True)