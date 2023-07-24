from flask import session
from config import APPS

class App():
    def getAll(owner):
        return APPS