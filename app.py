import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

entries = []

class GalileanMoons:
    def __init__(self, first, second, third, fourth):
        self.first = first
        self.second = second
        self.third = third
        self.fouth = fourth


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entry_content = request.form.get("content")
        formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
        entries.append((entry_content, formatted_date))

        entries_with_date = [
            (entry[0], entry[1], datetime.datetime.strptime(entry[1], "%Y-%m-%d").strftime("%b %d"))
            for entry in entries
        ]

        
    
    return render_template("index.html", entries=entries_with_date)


@app.route("/first_page")
def hello_world():

    planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neputune"]

    user_os = {
        "bob smith": "mac",
        "anne": "linus",
        "adam" : "window"
    }

    return render_template("first_page.html",  name="bob", template_name='python', company='Microsoft', planets=planets, user_os=user_os) #html파일을 jinja 템플릿으로 넘긴다

@app.route("/second")
def secont_page():
    movies = [
        "west side story", 
        "marvel series",
        "simpsons"
    ]

    moons = GalileanMoons("Io", "Europa", "Ganymded", "Gallisto"
    )

    kwargs = { "movies": movies, "moons" :moons}
    return render_template("second_page.html", **kwargs)