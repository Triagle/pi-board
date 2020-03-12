from flask import Flask, render_template
from flask import request
import db


app = Flask(__name__)


@app.route("/leaderboard")
def leaderboard():
    entries = sorted(db.get_entries(), key=lambda s: s.score, reverse=True)[:10]
    return render_template("leaderboard.html", entries=entries)


def longest_common_prefix(a, b):
    i = 0
    count = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        if a[i] != ".":
            count += 1
        i += 1
    return count


@app.route("/submit", methods=["POST"])
def submit():
    with open("pi.txt", "r") as infile:
        pi = infile.read().strip()
    score = longest_common_prefix(pi, request.form["pi"])
    db.push_submission(request.form["user"], score)
    return render_template("submission.html", score=score)


@app.route("/")
def submission_form():
    return render_template("index.html")


if __name__ == "__main__":
    db.create_schema()
    app.run()
