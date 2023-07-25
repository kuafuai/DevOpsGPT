from config import APPS, USERS

class User():
    def checkPassword(username, password):
        if username in USERS and USERS[username] == password:
            return True
        else:
            return False