from flask import session

def set(key, value):
    session[key] = value
    session.update

def get(key):
    try:
        if key in session:
            return session[key]
        return None
    except Exception as e:
        return None

def pop(key):
    session.pop(key)

def clearup():
    session.clear()