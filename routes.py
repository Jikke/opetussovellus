from app import app
from flask import render_template, redirect, request, session
from os import getenv
import users, courses, exercises, performances

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
        if topic == "" or content == "":
            return render_template("error.html",message="Syötit tyhjän kurssinimen tai sisällön", url="/")
        if courses.create(topic, content):
            return redirect("/")
        else:
            return render_template("error.html",message="Kurssin luominen ei onnistunut", url="/new")


@app.route("/course/<topic>")
def course(topic):
    if courses.get(topic) != None:
        course = courses.get(topic)
        student_id = users.user_id()
        previous = performances.get(course[0],student_id)
        student = performances.student(course[0],student_id)
        return render_template("course.html",topic=topic,course=course,student=student,mchoice=0,previous=previous,points=None)
    else:
        return render_template("error.html",message="Kurssia ei löytynyt.", url="/")

@app.route("/join", methods=["POST"])
def join():
    topic = request.form["topic"]
    course = courses.get(topic)
    student_id = users.user_id()
    if performances.returning(course[0], student_id):
        performances.update(course[0], student_id, 0, None)
    else:
        performances.join(course[0], student_id, 0)
    return redirect("/course/"+topic)


@app.route("/leave", methods=["POST"])
def leave():
    topic = request.form["topic"]
    course_id = courses.get(topic)[0] 
    student_id = users.user_id()
    if performances.leave(course_id, student_id):
        return redirect("/course/"+topic)
    else:
        return render_template("error.html",message="Kurssilta poistuminen ei onnistunut.", url="/")


@app.route("/delete", methods=["POST"])
def delete():
    topic = request.form["topic"]
    course_id = courses.get(topic)[0]
    if courses.delete(topic):
        performances.delete(course_id)
        return redirect("/")
    else:
        return render_template("error.html",message="Kurssin postaminen ei onnistunut", url="/")

@app.route("/check")
def check():
    student_id = users.user_id()
    perf_list = performances.get_joined(student_id)
    course_list = []
    for perf in perf_list:
        course = courses.get_joined(perf[1])
        course_list.append(course)
    return render_template("check.html",course_list=course_list,perf_list=perf_list,count=len(course_list))

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
    if course != None:
        list = exercises.get_list(course[0])
        if request.method == "GET":
            return render_template("exercise.html",topic=course[1],course_id=course[0],count=len(list),exercises=list)
        if request.method == "POST":
            previous = performances.get(course[0], users.user_id())
            submissionlist = []
            for key, val in request.form.items():
                if val != None:
                    submissionlist.append(val)
                else: submissionlist.append("-wronganswer-")
            print(submissionlist)
            answers = exercises.get_answers(list)
            correct = exercises.correct(submissionlist, answers)
            print(answers)
            if previous[3] <= correct:
                submission = ','.join(submissionlist)
                performances.update(course[0], users.user_id(), correct, submission)
                previous = performances.get(course[0], users.user_id())
            return render_template("course.html",topic=topic,course=course,student=True,mchoice=0,previous=previous,points=correct)
    else:
        return render_template("error.html",message="Kyselyä ei löytynyt!",url="/course/"+topic)


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
        if options != "None":
            optionlist = options.split(",")
            if len(optionlist) > 1:
                for option in optionlist:
                    if option == answer:
                        courses.maxup(course_id)
                        exercises.add(course_id, question, answer, options)
                        return redirect("/course/"+topic+"/exercise/edit/"+mchoice)
            return render_template("error.html",message="Virheelliset syötteet.", url="/course/"+topic)
        else:
            courses.maxup(course_id)
            exercises.add(course_id, question, answer, options)
            return redirect("/course/"+topic+"/exercise/edit/"+mchoice)

@app.route("/remove", methods=["POST"])
def remove():
    exercise_id = request.form["exercise_id"]
    topic = request.form["topic"]
    course_id = courses.get(topic)[0]
    exercise_list = exercises.get_list(course_id)
    removed_answer = exercises.answer(exercise_id)[3] # ID OK
    answer_index = exercises.get_index(exercise_list, removed_answer)
    if  answer_index != -1 and exercises.remove(exercise_id):
        courses.maxdown(course_id)
        performances.remove(course_id, answer_index, removed_answer)
        return redirect("/course/"+topic+"/exercise")
    else:
        return render_template("error.html",message="Kysymyksen poistaminen ei onnistunut", url="/course/"+topic+"/exercise")

@app.route("/course/<topic>/ratings")
def ratings(topic):
    if topic != None:
        course = courses.get(topic)
        perf_list = performances.get_all(course[0])
        stdn_list = []
        for performance in perf_list:
            name = users.get(performance[2])[1]
            stdn_list.append(name)
        return render_template("ratings.html",topic=topic,perf_list=perf_list,stdn_list=stdn_list,max=course[4])
    else:
        return render_template("error.html",message="Kurssin "+topic+" suorituksia ei löydy.", url="/course/"+topic)
