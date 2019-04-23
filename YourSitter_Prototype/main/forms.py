

# *** The forms file declares the structure of all the forms used through which user input is accepted while checking for constraints ***


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo 
from main.models import User, Sitter 


# SignUP Form for a parent

class SignUpForm(FlaskForm):
	#userID = StringField('UserID', validators = [DataRequired()])	
	email = StringField('Email', validators = [DataRequired(), Email()])
	userfname = StringField('First Name', validators = [DataRequired()])
	userlname = StringField('Last Name', validators = [DataRequired()])	
	password = PasswordField('Password', validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
	zipcode = StringField('ZipCode', validators = [DataRequired()])
	submit = SubmitField('SIGNUP')

# SignUp Form for a sitter

class SitterSignUpForm(FlaskForm):
	#userID = StringField('UserID', validators = [DataRequired()])	
	email = StringField('Email', validators = [DataRequired(), Email()])
	userfname = StringField('First Name', validators = [DataRequired()])
	userlname = StringField('Last Name', validators = [DataRequired()])	
	password = PasswordField('Password', validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
	zipcode = StringField('ZipCode', validators = [DataRequired()])
	submit = SubmitField('SIGNUP')


# Form for login functionality

class LoginForm(FlaskForm):
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	remember = BooleanField('checkbox') 
	submit = SubmitField('LOGIN')

# Form to accept zipcode

class ZipcodeForm(FlaskForm):
	zipcode = StringField('Zipcode', validators = [DataRequired()])
	submit = SubmitField('Search')


