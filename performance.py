from db import db

def get(course_id, student_id):
    sql = "SELECT * FROM performance WHERE course_id=:course_id AND student_id=:student_id AND visible=1 ORDER BY id"
    result = db.session.execute(sql, {"course_id":course_id, "student_id":student_id})
    return result.fetchone()

def join(course_id, student_id, points, maximum):
    sql = "INSERT INTO performance (course_id, student_id, points, maximum, visible) VALUES (:course_id, :student_id, :points, :maximum, 1)"
    db.session.execute(sql, {"course_id":course_id, "student_id":student_id, "points":points, "maximum":maximum})
    db.session.commit()
    return True

def update(course_id, student_id, points):
    sql = "UPDATE performance SET points=:points WHERE course_id=:course_id AND student_id=:student_id"
    db.session.execute(sql, {"points":points, "course_id":course_id, "student_id":student_id})
    db.session.commit()
    return True

def student(course_id, student_id):
    sql = "SELECT * FROM performance WHERE course_id=:course_id AND student_id=:student_id AND visible=1"
    result = db.session.execute(sql, {"course_id":course_id, "student_id":student_id})
    student = result.fetchone()
    if student == None:
        return False
    else:
        return True

def getmax(course_id):
    sql = "SELECT maximum FROM performance WHERE course_id=:course_id AND visible=1"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchone()


def newmax(course_id):
    sql = "UPDATE performance SET maximum = maximum + 1 WHERE course_id=:course_id"
    db.session.execute(sql, {"course_id":course_id})
    db.session.commit()
    return True