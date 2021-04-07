from db import db
from flask import session
import users

def student(course_id, student_id):
    sql = "SELECT * FROM participants WHERE course_id=:course_id AND student_id=:student_id AND visible=1"
    result = db.session.execute(sql, {"course_id":course_id, "student_id":student_id})
    student = result.fetchone()
    if student == None:
        return False
    else:
        return True