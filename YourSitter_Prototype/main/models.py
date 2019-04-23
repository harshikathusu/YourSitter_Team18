
# *** The models file defines the strucutre of the tables in the database ****


from flask_login import UserMixin
from datetime import datetime
from main import db
from main import login
#from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,  SelectField


# Table structure of User table that defines a user

class User(UserMixin, db.Model):
	#UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
	UserEmail = db.Column(db.String(30), nullable=False, primary_key=True)
	UserFName = db.Column(db.String(30), nullable=False )
	UserLName = db.Column(db.String(30), nullable=False)
	UserPw = db.Column(db.String(20), nullable=False)
	is_Parent = db.Column(db.Boolean)
	is_Active = db.Column(db.Boolean, default = True)
	parents = db.relationship('Parent',backref='parent',lazy=True)
	sitters = db.relationship('Sitter',backref='sitter',lazy=True)



	# function to check a user's password
	def check_password(self, password):
		return self.UserPw == password

	# def set_password(self, password):
 	# self.password = password

	# function to check if  user is active
	def check_active(self):
		return self.is_Active
	
	# function to distinguish between parent and user
	def check_parent(self):
		return self.is_Parent


# Function to get unique rowID of a User from the USer table

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
 	
# table structure of a parent

class Parent(db.Model):
	PID = db.Column(db.Integer, primary_key=True, autoincrement=True)
	PEmail= db.Column(db.String(30), db.ForeignKey('user.UserEmail'))
	PZipCode = db.Column(db.String(6))

	
# table structure of a sitter

class Sitter(db.Model):
	SID = db.Column(db.Integer, primary_key=True, autoincrement=True)
	SEmail = db.Column(db.String(30), db.ForeignKey('user.UserEmail'))
	SZipcode = db.Column(db.String(6), default="77801")
	
