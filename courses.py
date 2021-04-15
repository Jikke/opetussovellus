from db import db
import users, courses

def get(topic):
    sql = "SELECT * FROM courses WHERE topic=:topic AND visible=1"
    result = db.session.execute(sql, {"topic":topic})
    return result.fetchone()

def get_list():
    sql = "SELECT topic, modified FROM courses WHERE visible=1 ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def get_owned():
    owner_id = users.user_id()
    sql = "SELECT topic, modified FROM courses WHERE owner_id=:owner_id AND visible=1 ORDER BY id"
    result = db.session.execute(sql, {"owner_id":owner_id})
    return result.fetchall()

def create(topic, content):
    owner_id = users.user_id()
    if owner_id == 0:
        return False
    if topic == "":
        return False
    # Check if topic is in use (visible = 1)     
    if get(topic) == None:
        # Not in use, check if deleted topic (visible = 0)
        check = "SELECT id, topic, content FROM courses WHERE topic=:topic"
        result = db.session.execute(check, {"topic":topic})        
        exists = result.fetchone()
        if exists == None:
            # Topic has never been in use
            sql = "INSERT INTO courses (topic, content, owner_id, modified, visible) VALUES (:topic, :content, :owner_id, NOW(), 1)"
            db.session.execute(sql, {"topic":topic, "content":content, "owner_id":owner_id})
            db.session.commit()
        else:
            # Topic has been deleted, will retake it
            sql = "UPDATE courses SET content=:content, owner_id=:owner_id, modified=NOW(), visible=1 WHERE topic=:topic AND visible=0"
            db.session.execute(sql, {"topic":topic, "content":content, "owner_id":owner_id})
            db.session.commit()
        return True
    else:
        # Topic is in use
        return False

def modify(course_id, topic, content):
    owner_id = users.user_id()
    if owner_id == 0:
        return False
    else:
        sql = "UPDATE courses SET topic=:topic, content=:content, owner_id=:owner_id, modified=NOW() WHERE id=:course_id"
        db.session.execute(sql, {"topic":topic, "content":content, "owner_id":owner_id, "course_id":course_id})
        db.session.commit()
        return True        
    

def delete(topic):
    owner_id = users.user_id()
    if owner_id == 0:
        return False
    if topic == "":
        return False    
    exists = get(topic)
    if exists == None:
        return False
    else:
        sql = "UPDATE courses SET visible=0 WHERE topic=:topic AND visible=1"
        db.session.execute(sql, {"topic":topic})
        db.session.commit()
        return True        



