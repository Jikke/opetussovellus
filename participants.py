from db import db
from flask import session
import users, courses

def student(course_id, student_id):
    sql = "SELECT * FROM participants WHERE course_id=:course_id AND student_id=:student_id AND visible=1"
    result = db.session.execute(sql, {"course_id":course_id, "student_id":student_id})
    student = result.fetchone()
    if student == None:
        return False
    else:
        return True

def join(topic):
    course_id = courses.get(topic)[0]
    student_id = users.user_id()
    if course_id == None or student_id == 0:
        return False
    sql = "INSERT INTO participants (course_id, student_id, visible) VALUES (:course_id, :student_id, 1)"
    db.session.execute(sql, {"course_id":course_id, "student_id":student_id})
    db.session.commit()
    return True