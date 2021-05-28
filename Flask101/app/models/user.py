from db import db
from logger import logger

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    emailAddress = db.Column(db.String(80))


    @classmethod
    def findById(cls, userId):
        logger.info(f"Fetch the user information for the given user: {userId}")
        return cls.query.filter_by(username=userId).first()

    def add(self):
        logger.info(f"Add new user with username: {self.username}")
        db.session.add(self)
        db.session.commit()
        db.session.flush()
        return self

    def delete(self):
        logger.info(f"Delete user with username: {self.username}")
        db.session.delete(self)
        db.session.commit()
        db.session.flush()

        return self

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstName,
            "lastname": self.lastName,
            "emailAddress": self.emailAddress
        }