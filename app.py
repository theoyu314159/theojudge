from flask import Flask
from flask import request
import textwrap
import io
import contextlib


app = Flask(__name__)
ans = ""


@app.route("/")
def home():
    html = ""
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.route("/problems")
def problems():
    # html = ""
    with open("problems.html", "r", encoding="utf-8") as f:
        return f.read()


@app.route("/about")
def about():
    # html = ""
    with open("about.html", "r", encoding="utf-8") as f:
        return f.read()


@app.route("/solve/<string:problem>", methods=["GET", "POST"])
def solve(problem):
    html = ""
    with open("solve.html", "r", encoding="utf-8") as f:
        html = f.read()
    dis = ""
    with open(f"problems/{problem}.html", "r", encoding="utf-8") as f:
        dis = f.read()
    test = ""
    ans = ""
    mode = ""
    with open(f"problems/{problem}.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    test = lines[0].strip()
    ans = lines[1].strip()

    if request.method == "POST":
        code = request.form.get("code")

        inputs = test.splitlines()
        input_iter = iter(inputs)

        def fake_input(prompt=""):
            print(prompt, end="")
            return next(input_iter)

        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                exec(textwrap.dedent(code), {"input": fake_input})
            result = output.getvalue().strip()
            if result == ans:
                mode = "AC"
            else:
                mode = "NA"
        except Exception as e:
            result = f"錯誤：{e}"
            mode = "RE"
    return html.replace("<dis/>", dis).replace("<out/>", mode)


app.run(debug=True, host="0.0.0.0")
