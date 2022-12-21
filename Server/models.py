from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct, func, desc, inspect, or_
from sqlalchemy_utils import EmailType

db = SQLAlchemy()

def object_as_dict(obj):                                    # map queries into object(dict)
  return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class User(db.Model):
    __tablename__ = 'users'
    # child class
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(EmailType, nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    queries = db.relationship('Query', backref=db.backref('user', lazy="joined", innerjoin=True), cascade="all, delete, delete-orphan")

    def __repr__(self):
      return f'<User_ID:{self.id}, Name:{ self.name}, User_Name:{self.user_name}, Email:{self.email}, Password:{self.password} >'


class Query(db.Model):
	__tablename__ = 'queries'
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)


class Rec(db.Model):
	__tablename__ = 'recommendations'
	user_1_id = db.Column( db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
	user_2_id = db.Column( db.Integer, db.ForeignKey('users.id', ondelete="CASCADE") , primary_key=True)
	score = db.Column( db.Float, nullable=False)



