from db import db
import users, courses

def get(course_id, student_id):
    sql = "SELECT * FROM performance WHERE course_id=:course_id AND student_id=:student_id AND visible=1 ORDER BY id"
    result = db.session.execute(sql, {"course_id":course_id, "student_id":student_id})
    return result.fetchone()

def returning(course_id, student_id):
    sql = "SELECT * FROM performance WHERE course_id=:course_id AND student_id=:student_id AND visible=0 ORDER BY id"
    result = db.session.execute(sql, {"course_id":course_id, "student_id":student_id})
    if result.fetchone() != None:
        return True
    else:
        return False

def get_all(course_id):
    sql = "SELECT * FROM performance WHERE course_id=:course_id AND visible=1 ORDER BY student_id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchall()

def join(course_id, student_id, points):
    sql = "INSERT INTO performance (course_id, student_id, points, visible) VALUES (:course_id, :student_id, 0, 1)"
    db.session.execute(sql, {"course_id":course_id, "student_id":student_id})
    db.session.commit()
    return True

def update(course_id, student_id, points, submission):
    sql = "UPDATE performance SET points=:points, submission=:submission, visible=1 WHERE course_id=:course_id AND student_id=:student_id"
    db.session.execute(sql, {"points":points, "submission":submission, "course_id":course_id, "student_id":student_id})
    db.session.commit()
    return True

def get_joined(student_id):
    sql = "SELECT * FROM performance WHERE student_id=:student_id AND visible=1"
    result = db.session.execute(sql, {"student_id":student_id})
    return result.fetchall()

def student(course_id, student_id):
    sql = "SELECT * FROM performance WHERE course_id=:course_id AND student_id=:student_id AND visible=1"
    result = db.session.execute(sql, {"course_id":course_id, "student_id":student_id})
    student = result.fetchone()
    if student == None:
        return False
    else:
        return True

def remove(course_id, answer_index, removed_answer):
    performances = get_all(course_id)
    for index, performance in enumerate(performances):
        submission = performance[4]
        if(submission != None):
            submissionlist = submission.split(",")
        if len(submissionlist) >= 1:
            print(submissionlist)
            removed_submit = submissionlist.pop(answer_index)
            new_submission = ','.join(submissionlist)
            student_id = performances[index][2]
            points = get(course_id, student_id)[3]
            if removed_submit == removed_answer:
                points -= 1
            update(course_id, student_id, points, new_submission)

def delete(course_id):
    sql = "UPDATE performance SET visible=0 WHERE course_id=:course_id AND visible=1"
    db.session.execute(sql, {"course_id":course_id})
    db.session.commit()
    return True

def leave(course_id, student_id):
    sql = "UPDATE performance SET visible=0 WHERE course_id=:course_id AND student_id=:student_id AND visible=1"
    db.session.execute(sql, {"course_id":course_id, "student_id":student_id})
    db.session.commit()
    return True
            