from flask import Flask, render_template, request, redirect, url_for, session, Response
from werkzeug.security import check_password_hash, generate_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from functools import wraps
import sqlite3, time, datetime, csv
from urllib.parse import urlparse
from math import floor

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)

conn = sqlite3.connect("votely.db", check_same_thread=False)
cur = conn.cursor()

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def error(message):
    return render_template("error.html", message=message)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def feedback_key():
    return f"{get_remote_address()}:{request.view_args.get('id', 'noid')}"

@app.errorhandler(429)
def too_many(e):
    return error("Too many requests")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("passwordconfirmation")
        if not username:
            return error("Please enter username")
        if not email:
            return error("Please enter email")
        if not password:
            return error("Please enter password")
        if password != confirmation:
            return error("The two passwords must be the same")
        try:
            cur.execute("INSERT INTO users (name, email, hash) VALUES (?, ?, ?)", (username, email, generate_password_hash(password)))
            conn.commit()
            session.clear()
            user = cur.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            session['user_id'] = user[0]
            return redirect("/")
        except Exception as e:
            return error("There's already an account with this email")
    else:
        if session.get("user_id"):
            return redirect("/")
        return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if not email:
            return error("Please enter email")
        if not password:
            return error("Please enter password")
        user = cur.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if not user:
            return error("Password or Email is wrong")
        if check_password_hash(user[3], password):
            session.clear()
            session['user_id'] = user[0]
        else:
            return error("Password or Email is wrong")
        return redirect("/")
    else:
        if session.get("user_id"):
            return redirect("/")
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        return redirect("/")
    else:
        votes = cur.execute("SELECT * FROM votes WHERE user_id = ?", (session['user_id'],)).fetchall()
        total_votes = len(votes)
        last_24h = 0
        last_7d = 0
        last_1y = 0
        for i in range(total_votes):
            vote = votes[i]
            vote_time = vote[4]
            timestamp = floor(time.time())
            if vote_time >= timestamp-86400:
                last_1y += 1
                last_7d += 1
                last_24h += 1
            elif vote_time >= timestamp-604800:
                last_1y += 1
                last_7d += 1
            elif vote_time >= timestamp-31556926:
                last_1y += 1


        now = datetime.datetime.now()

        start = (now - datetime.timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        line_labels = [weekdays[(start + datetime.timedelta(days=d)).weekday()] for d in range(7)]

        line_number = [0] * 7

        for j in range(total_votes):
            vote = votes[j]
            vote_time = vote[4]
            vote_dt = datetime.datetime.fromtimestamp(vote_time)

            day_index = (vote_dt.date() - start.date()).days
            if 0 <= day_index < 7:
                line_number[day_index] += 1

        line_chart = {
            "labels": line_labels,
            "numbers": line_number
        }

        pie_labels = ["Green", "Yellow", "Red"]

        pie_numbers = [0, 0, 0]

        for i in range(total_votes):
            vote = votes[i]
            rating = vote[2]
            pie_numbers[-rating + 3] += 1

        pie_chart = {
            "labels": pie_labels,
            "numbers": pie_numbers
        }

        latest_10_votes = votes[-10:]

        table_votes = []

        ratings = ["Bad", "Okay", "Good"]

        for i in latest_10_votes:
            table_votes.append([ratings[int(i[2])-1], i[3], datetime.datetime.utcfromtimestamp(int(i[4])).strftime('%Y-%m-%d %H:%M')])

        data = {
            "total_votes": total_votes,
            "last_24h": last_24h,
            "last_7d": last_7d,
            "last_1y": last_1y,
        }
        return render_template("dashboard.html", id=session['user_id'], url=urlparse(request.url).netloc, data=data, line_chart=line_chart, pie_chart=pie_chart, votes=votes, table_votes=table_votes)

@app.route('/dashboard/votes', methods=["GET", "POST"])
@login_required
def votes():
    if request.method == "POST":
        return redirect("/")
    else:
        ratings = ["Bad", "Okay", "Good"]
        votes = cur.execute("SELECT * FROM votes WHERE user_id = ? ORDER BY created_at DESC", (session['user_id'],)).fetchall()
        for i in range(len(votes)):
            votes[i] = (ratings[int(votes[i][2])-1], votes[i][3], datetime.datetime.utcfromtimestamp(int(votes[i][4])).strftime('%Y-%m-%d %H:%M'))
        return render_template("votes.html", votes=votes)

@app.route('/dashboard/download_votes')
@login_required
def download_votes():
    ratings = ["Bad", "Okay", "Good"]
    votes = cur.execute("SELECT * FROM votes WHERE user_id = ? ORDER BY created_at DESC", (session['user_id'],)).fetchall()
    for i in range(len(votes)):
        votes[i] = [ratings[int(votes[i][2])-1], votes[i][3], datetime.datetime.utcfromtimestamp(int(votes[i][4])).strftime('%Y-%m-%d %H:%M')]
    votes.insert(0, ["Rating", "Comment", "Time"])
    def generate():
        for row in votes:
            yield ",".join(map(str, row)) + "\n"
    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=votes.csv"}
    )

@app.route('/f/<id>', methods=["GET", "POST"])
@limiter.limit("10 per minute; 30 per hour", key_func=feedback_key)
def feedback(id):
    ratings = ["bad", "okay", "good"]
    if request.method == "POST":
        rating = request.form.get("rating")
        if not rating:
            return render_template("feedback.html")
        if rating not in ("1", "2", "3"):
            return render_template("feedback.html")
        rating_int = int(rating)
        comment = str(request.form.get("comment"))
        cur.execute("INSERT INTO votes (user_id, rating, comment, created_at) VALUES (?, ?, ?, ?)", (id, rating, comment, floor(time.time())))
        conn.commit()
        return render_template("thankyou.html", feedback=ratings[rating_int - 1])
    else:
        return render_template("feedback.html")

@app.route('/s/<id>', methods=["GET", "POST"])
@limiter.limit("10 per minute; 30 per hour", key_func=feedback_key)
def onsite_feedback(id):
    if request.method == "POST":
        ratings = ["bad", "okay", "good"]
        rating = request.form.get("rating")
        if not rating:
            return render_template("onsite_feedback.html")
        if rating not in ("1", "2", "3"):
            return render_template("onsite_feedback.html")
        rating_int = int(rating)
        cur.execute("INSERT INTO votes (user_id, rating, comment, created_at) VALUES (?, ?, ?, ?)", (id, rating_int, "", floor(time.time())))
        conn.commit()
        return render_template(
            "onsite_thankyou.html",
            feedback=ratings[rating_int - 1],
            rating=rating_int
        )
    return render_template("onsite_feedback.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0")
