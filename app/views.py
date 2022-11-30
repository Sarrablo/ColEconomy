from app import app
from flask import render_template
from flask import request, redirect, session, url_for
from .models import MongoModel

app.config["SECRET_KEY"] = "07246f1339134fbda4d2aa2dbab8cc8d"
mongo = MongoModel()


@app.route("/")
def index():
    operations = mongo.find_operations()
    total = 0
    for operation in operations:
        total = total+ float(operation['cuantia']) * int(operation["direccion"]) 
    return render_template("public/index.html", operations=operations, total=total)


@app.route("/about")
def about():
    return render_template("public/about.html")


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":

        req = request.form

        missing = list()

        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("public/sign_up.html", feedback=feedback)
        else:
            if mongo.compare_by_pass(req.get("email"), req.get("password")):
                session["USERNAME"] = req.get("email")
                return redirect(url_for("admin_dashboard"))
            else:
                feedback = f"Error on user or password"
                return render_template("public/sign_up.html",
                                       feedback=feedback)

        return redirect(request.url)

    return render_template("public/sign_up.html")


@app.route("/jinja")
def jinja():
    # Strings
    my_name = "Julian"

    # Integers
    my_age = 30

    # Lists
    langs = ["Python", "JavaScript", "Bash", "Ruby", "C", "Rust"]

    # Dictionaries
    friends = {
        "Tony": 43,
        "Cody": 28,
        "Amy": 26,
        "Clarissa": 23,
        "Wendell": 39
    }

    # Tuples
    colors = ("Red", "Blue")

    # Booleans
    cool = True

    # Classes
    class GitRemote:
        def __init__(self, name, description, domain):
            self.name = name
            self.description = description
            self.domain = domain

        def clone(self, repo):
            return f"Cloning into {repo}"

        def pull(self):
            return f"Pulling"

    my_remote = GitRemote(
        name="Learning Flask",
        description="Learn the Flask web framework for Python",
        domain="https://github.com/Julian-Nash/learning-flask.git")

    # Functions
    def repeat(x, qty=1):
        return x * qty

    return render_template("public/jinja.html",
                           my_name=my_name,
                           my_age=my_age,
                           langs=langs,
                           friends=friends,
                           colors=colors,
                           cool=cool,
                           GitRemote=GitRemote,
                           my_remote=my_remote,
                           repeat=repeat)
