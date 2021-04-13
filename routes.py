from app import app
from flask import render_template, redirect, request, session
from os import getenv
import users, courses, participants

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    if users.user_id != 0:
        if users.user_role() == 1:
            list = courses.get_owned()
        else:
            list = courses.get_list()
        return render_template("index.html", count=len(list), courses=list)
    return render_template("index.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":    
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html",message="Väärä tunnus tai salasana")

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
        role     = request.form["role"]
        if users.register(username,password,role):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    topic = request.form["topic"]
    content = request.form["content"]
    if courses.create(topic, content):
        return redirect("/")
    else:
        return render_template("error.html",message="Kurssin luominen ei onnistunut")

@app.route("/course/<topic>")
def course(topic):
    if courses.get(topic) != None:
        course_id = courses.get(topic)[0]
        student_id = users.user_id()
        student = participants.student(course_id, student_id)
        content = courses.get(topic)[2]
        return render_template("course.html",topic=topic,content=content,student=student,course_id=course_id)
    else:
        return render_template("error.html",message="Kurssia ei löytynyt.")

@app.route("/join", methods=["POST"])
def join():
    topic = request.form["topic"]
    if courses.join(topic):
        return redirect("/course/"+topic)
    else:
        return render_template("error.html",message="Kurssille liittyminen ei onnistunut.")

@app.route("/delete", methods=["POST"])
def delete():
    topic = request.form["topic"]
    if courses.delete(topic):
        return redirect("/")
    else:
        return render_template("error.html",message="Kurssin postaminen ei onnistunut")

@app.route("/modify", methods=["POST"])
def modify():
    topic = request.form["topic"]
    content = request.form["content"]
    course_id = request.form["course_id"]
    print("Modify, ennen courses.modify() -metodia")
    if courses.modify(course_id, topic, content):
        print("Modify, courses.modify() -metodi onnistui")
        return redirect("/course/"+topic)
    else:
        return render_template("error.html",message="Kurssin muokkaaminen ei onnistunut")

