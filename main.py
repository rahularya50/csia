from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def homepage():
    statement = get_statement()
    return render_template("index.html", statement=statement)


@app.route('/go', methods=["POST"])
def go():
    stuff = request.form["test"]
    return render_template("index.html", statement=stuff)


def get_statement():
    return "Testing :)"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
