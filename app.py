from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("first_page.html",  name="bob", template_name='python') #html파일을 jinja 템플릿으로 넘긴다

@app.route("/second")
def secont_page():
    return render_template("second_page.html")