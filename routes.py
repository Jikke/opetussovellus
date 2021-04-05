from app import app
from flask import render_template, redirect, request, session
from os import getenv
import users

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":    
        username = request.form["username"]
        password = request.form["password"]
        # TODO: check username and password
        session["username"] = username
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        print(username+', '+password+', '+role)
        if users.register(username,password,role):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

