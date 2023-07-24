from app.extensions import db

class Repo(db.Model):
    __tablename__ = 'repo'

    # The current version does not support this feature
