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

def correct(submissions, answers):
    correct = 0      
    for i in range(len(submissions)):
        if submissions[i] == answers[i]:
            correct += 1
    return correct

        


    