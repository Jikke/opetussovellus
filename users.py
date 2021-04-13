from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username,password):
    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[2],password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["role"] = user[3]
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["role"]
    del session["username"]

def register(username,password,role):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password,role,visible) VALUES (:username,:password,:role,1)"
        db.session.execute(sql, {"username":username,"password":hash_value,"role":role})
        db.session.commit()
    except:
        return False
    return login(username,password)

def user_id():
    return session.get("user_id",0)

def user_role():
    return session.get("role",0)