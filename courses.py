from db import db
import users, courses

def get_list():
    sql = "SELECT topic, created FROM courses WHERE visible=1 ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def get_owned():
    owner_id = users.user_id()
    sql = "SELECT topic, created FROM courses WHERE owner_id=:owner_id AND visible=1 ORDER BY id"
    result = db.session.execute(sql, {"owner_id":owner_id})
    return result.fetchall()

def create(topic, content):
    owner_id = users.user_id()
    if owner_id == 0:
        return False
    sql = "INSERT INTO courses (topic, content, owner_id, created, visible) VALUES (:topic, :content, :owner_id, NOW(), 1)"
    db.session.execute(sql, {"topic":topic, "content":content, "owner_id":owner_id})
    db.session.commit()
    return True

def get(topic):
    sql = "SELECT id, topic, content FROM courses WHERE topic=:topic AND visible=1"
    result = db.session.execute(sql, {"topic":topic})
    return result.fetchone()

def join(topic):
    course_id = courses.get(topic)[0]
    student_id = users.user_id()
    if course_id == None or student_id == 0:
        return False
    sql = "INSERT INTO participants (course_id, student_id, visible) VALUES (:course_id, :student_id, 1)"
    db.session.execute(sql, {"course_id":course_id, "student_id":student_id})
    db.session.commit()
    return True