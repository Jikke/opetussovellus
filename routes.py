from app import app
from flask import render_template, redirect, request, session
from os import getenv
import users, courses, participants, exercises

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

@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    if request.method == "POST":
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
        content = courses.get(topic)[2]
        student_id = users.user_id()
        student = participants.student(course_id, student_id)
        return render_template("course.html",topic=topic,course_id=course_id,content=content,student=student,mchoice=0)
    else:
        return render_template("error.html",message="Kurssia ei löytynyt.")

@app.route("/join", methods=["POST"])
def join():
    topic = request.form["topic"]
    if participants.join(topic):
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
    if courses.modify(course_id, topic, content):
        return redirect("/course/"+topic)
    else:
        return render_template("error.html",message="Kurssin muokkaaminen ei onnistunut")


@app.route("/course/<topic>/exercise", methods=["GET","POST"])
def exercise(topic):
    course = courses.get(topic)
    if course != None:
        list = exercises.get_list(course[0])
        if request.method == "GET":
            return render_template("exercise.html",topic=course[1],course_id=course[0],count=len(list),exercises=list)
        if request.method == "POST":
            submissions = []
            for i in range(len(list)):
                submissions.append(request.form[list[i][0]])
            answers = []
            for i in range(len(list)):
                answers.append(list[i][3])
            correct = exercises.correct(submissions, answers)    
            #LISÄÄ PERFORMACE TAULU JA TALLETA SINNE CORRECT ARVO USER_ID:N MUKAAN#
            print(correct)
            return redirect("/course/"+topic+"/exercise")

    else:
        return render_template("error.html",message="Kyselyä ei löytynyt!")


@app.route("/course/<topic>/exercise/edit/<mchoice>", methods=["GET", "POST"])
def edit(topic, mchoice):
    if request.method == "GET":
        return render_template("edit.html",topic=topic,mchoice=mchoice)
    if request.method == "POST":
        course = courses.get(topic)
        course_id = course[0]
        question = request.form["question"]
        answer = request.form["answer"]
        options = request.form["options"]
        if exercises.add(course_id, question, answer, options):
            return redirect("/course/"+topic+"/exercise/edit/"+mchoice)
        else:
                return render_template("error.html",message="Kysymyksen luominen ei onnistunut.")



    
