from app import app
from flask import render_template, redirect, request, session
from os import getenv
import users, courses, exercises, performance

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
            return render_template("error.html",message="Väärä tunnus tai salasana", url="/login")

@app.route("/logout")
def logout():
    if users.user_id == 0:
        return render_template("error.html",message="Et ole kirjautunut sisään.", url="/login")
    else:
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
            return render_template("error.html",message="Rekisteröinti ei onnistunut", url="/register")

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
            return render_template("error.html",message="Kurssin luominen ei onnistunut", url="/new")


@app.route("/course/<topic>")
def course(topic):
    if courses.get(topic) != None:
        course_id = courses.get(topic)[0]
        content = courses.get(topic)[2]
        student_id = users.user_id()
        student = performance.student(course_id, student_id)
        previous = performance.get(course_id, student_id)
        return render_template("course.html",topic=topic,course_id=course_id,content=content,student=student,mchoice=0,previous=previous)
    else:
        return render_template("error.html",message="Kurssia ei löytynyt.", url="/")

@app.route("/join", methods=["POST"])
def join():
    topic = request.form["topic"]
    course = courses.get(topic)
    student_id = users.user_id
    maximum = performance.getmax(course_id)
    if performance.join(course[0], student_id, 0, maximum):
        return redirect("/course/"+topic)
    else:
        return render_template("error.html",message="Kurssille liittyminen ei onnistunut.", url="/")

@app.route("/delete", methods=["POST"])
def delete():
    topic = request.form["topic"]
    if courses.delete(topic):
        return redirect("/")
    else:
        return render_template("error.html",message="Kurssin postaminen ei onnistunut", url="/")

@app.route("/modify", methods=["POST"])
def modify():
    topic = request.form["topic"]
    content = request.form["content"]
    if topic == "" or content == "":
        return render_template("error.html",message="Syötit tyhjän kurssinimen tai sisällön", url="/")
    course_id = request.form["course_id"]
    if courses.modify(course_id, topic, content):
        return redirect("/course/"+topic)
    else:
        return render_template("error.html",message="Kurssin muokkaaminen ei onnistunut", url="/")


@app.route("/course/<topic>/exercise", methods=["GET","POST"])
def exercise(topic):
    course = courses.get(topic)
    previous = performance.get(course[0], users.user_id())
    if course != None:
        list = exercises.get_list(course[0])
        if request.method == "GET":
            return render_template("exercise.html",topic=course[1],course_id=course[0],count=len(list),exercises=list)
        if request.method == "POST":
            submissions = []
            for key,val in request.form.items():
                if val != None:
                    submissions.append(val)
                else: submissions.append("-wronganswer-")
            answers = []
            for i in range(len(list)):
                answers.append(str(list[i][3]))
            correct = exercises.correct(submissions, answers)
            
            if previous != None:
                if previous[3] < correct:
                    performance.update(course[0], users.user_id(), correct)
            else:
                performance.add(course[0], users.user_id(), correct, len(list))
            return redirect("/course/"+topic)

    else:
        return render_template("error.html",message="Kyselyä ei löytynyt!",url="/course"+topic)


@app.route("/course/<topic>/exercise/edit/<mchoice>", methods=["GET", "POST"])
def edit(topic, mchoice):
    if request.method == "GET":
        return render_template("edit.html",topic=topic,mchoice=mchoice)
    if request.method == "POST":
        course = courses.get(topic)
        course_id = course[0]
        question = request.form["question"]
        answer = request.form["answer"]
        if question == "" or answer == "":
            return render_template("error.html",message="Osa kentistä jätettiin tyhjiksi.", url="/course/"+topic)
        options = request.form["options"]
        print(options)
        if options != None:
            optionlist = options.split(",")
            if len(optionlist) > 1:
                for option in optionlist:
                    if option == answer:
                        performance.newmax(course_id)
                        exercises.add(course_id, question, answer, options)
                        return redirect("/course/"+topic+"/exercise/edit/"+mchoice)
            return render_template("error.html",message="Virheelliset syötteet.", url="/course/"+topic)
        else:
            performance.newmax(course_id)
            exercises.add(course_id, question, answer, options)
            return redirect("/course/"+topic+"/exercise/edit/"+mchoice)



    
