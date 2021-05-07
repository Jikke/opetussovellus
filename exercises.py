from db import db
import users, courses

def get_list(course_id):
    sql = "SELECT * FROM exercises WHERE course_id=:course_id AND visible=1 ORDER BY id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchall()

def add(course_id, question, answer, options):
    sql = "INSERT INTO exercises (course_id, question, answer, options, visible) VALUES (:course_id, :question, :answer, :options, 1)"
    db.session.execute(sql, {"course_id":course_id, "question":question, "answer":answer, "options":options})
    db.session.commit()
    return True

def remove(id):
    if get_list(id) == None:
        return False
    else:
        try:
            sql = "UPDATE exercises SET visible=0 WHERE id=:id AND visible=1"
            db.session.execute(sql, {"id":id})
            db.session.commit()
            return True
        except:
            return False

def answer(id):
    sql = "SELECT * FROM exercises WHERE id=:id AND visible=1"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()  

def get_answers(exercises):
    answers = []
    for i in range(len(exercises)):
        answers.append(str(exercises[i][3]))
    return answers

def correct(submissions, answers):
    correct = 0      
    for i in range(len(submissions)):
        if submissions[i] == answers[i]:
            correct += 1
    return correct

def get_index(exercise_list, answer):
    for index, exercise in enumerate(exercise_list):
        if exercise[3] == answer:
            return index
    return -1


    