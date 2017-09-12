from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from paper import Paper
import pickle as pkl
import random

app = Flask(__name__)

papers = []
questions = {}


@app.route('/')
def homepage():
    i = random.choice(list(questions.keys()))
    q = questions[i]
    return render_template("index.html", statement=q.question, qid=str(i))


@app.route('/questions')
def add_questions_page():
    return render_template("questions.html")


@app.route('/add', methods=["POST"])
def add_questions():
    global papers
    if 'ms_file' not in request.files:
        flash("No file attached.")
        return redirect(request.url)
    ms_file = request.files["ms_file"]
    if ms_file.filename == '':
        flash("No file attached.")
        return redirect(request.url)
    if ms_file and '.' in ms_file.filename and ms_file.filename.rsplit(".", 1)[1].lower() == "html":
        filename = secure_filename(ms_file.filename)
        ppr = Paper(filename, None)
        papers.append(ppr)
        write_database()
    return redirect(url_for("list"))


@app.route('/list')
def list_questions():
    global questions
    read_database()
    get_all_questions()
    string = ""
    for i, q in questions:
        string += i + ": &nbsp; " + q + "<br />"
    return render_template("list.html", text=string)


@app.route('/go', methods=["POST"])
def go():
    i = int(request.form["qid"])
    answer = request.form["answer"]
    q = questions[i]
    mark = q.mark_question(answer)
    return render_template("go.html", question=q.question, answer=answer, mark=str(mark), total=q.marks)


def get_statement():
    return "Testing :)"


def write_database():
    global papers
    with open("data/papers.txt", 'wb') as f:
        pkl.dump(papers, f)


def read_database():
    global papers
    with open("data/papers.txt", 'rb') as f:
        papers = pkl.load(f)


def get_all_questions():
    global questions
    for p in papers:
        for i, q in p.questions:
            questions[p.id + i] = q

read_database()
get_all_questions()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
