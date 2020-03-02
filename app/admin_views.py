from app import app
from flask import render_template
from flask import render_template, request, session, redirect, url_for
from datetime import datetime
from .models import MongoModel

mongo = MongoModel()


@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("USERNAME") is None:
        return redirect(url_for("sign_up"))
    else:
        operations = mongo.find_operations()
        total = 0
        for operation in operations:
            total = total+ float(operation['cuantia']) * int(operation["direccion"]) 
        return render_template("admin/dashboard.html", operations=operations, total=total)

@app.route("/admin/activities/dashboard")
def activities_dashboard():
    if session.get("USERNAME") is None:
        return redirect(url_for("sign_up"))
    else:
        operations = mongo.find_operations()
        return render_template("admin/activities/dashboard.html")



@app.route("/admin/del", methods=["POST"])
def delete_dashboard():
    if session.get("USERNAME") is None:
        return redirect(url_for("sign_up"))
    else:
        req = request.form
        data = req.to_dict(flat=True)
        print(data)
        mongo.delete_operations(data['identifier'], session.get("USERNAME"))
        return redirect(url_for("admin_dashboard"))


@app.route("/admin/add", methods=["GET", "POST"])
def add_dashboard():
    if session.get("USERNAME") is None:
        return redirect(url_for("sign_up"))
    else:
        if request.method == "POST":
            req = request.form
            data = req.to_dict(flat=True)
            data["user"] = session.get("USERNAME")
            data["date"] = datetime.today()
            data["cuantia"] = abs(int(data["cuantia"]))
            mongo.insert_in_operations(data)
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin/add.html")

@app.route("/admin/activities/add", methods=["GET", "POST"])
def activities_add_dashboard():
    if session.get("USERNAME") is None:
        return redirect(url_for("sign_up"))
    else:
        if request.method == "POST":
            req = request.form
            data = req.to_dict(flat=True)
            data["user"] = session.get("USERNAME")
            data["date"] = datetime.today()
            data["cuantia"] = abs(int(data["cuantia"]))
            mongo.insert_in_operations(data)
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin/activities/add.html")



@app.route("/admin/stock")
def stock_dashboard():
    if session.get("USERNAME") is None:
        return redirect(url_for("sign_up"))
    else:
        return render_template("admin/stock.html")
