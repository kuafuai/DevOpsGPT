from flask import session
from config import APPS

class UserPro():
    def checkPassword(username, password):
        return True