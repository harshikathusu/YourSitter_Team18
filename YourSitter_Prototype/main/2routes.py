from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user, login_manager
from forms import SignUpForm, LoginForm
from main import app,db
from models import User, Parent

app.config['SECRET_KEY'] = '0a31d758c1ff2046'



@app.route('/display_all', methods=["GET", "POST"])
def display_all():
   return render_template('display_all.html')

@app.route('/error')
def error():
    return render_template('errorpage.html')

@app.route('/')
@app.route('/mainpage')
def mainpage():
    return render_template('mainpage.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
	if current_user.is_authenticated:
	   return redirect(url_for('mainpage'))	
	#form = SignUpForm() 
	#if form.validate_on_submit():
	if request.method == 'POST':
	  useremail = request.form['UserEmail']
	  userfname = request.form['UserFName']
	  userlname = request.form['UserLName']
	  #userpw = request.form['UserPw']
	  #useremail = request.form['UserEmail']
	  #email = request.form['UserEmail']
	  #user = User(UserEmail=request.form.get('UserEmail'))
	  user = User(UserFName=userfname,UserLName=userlname,UserEmail=useremail)
          #user = User(UserEmail=form.userEmail.data, UserFName=form.userfname.data, UserLName=form.userlname.data, UserPw = form.password.data,  confirm_password=form.confirm_password.data) 

	  try:
	
	    db.session.add(user)
	    db.session.commit()

	  except Exception, e:
	    return render_template('mainpage')

	  return render_template('display_all', users=email)
	    #flash('Account created for {{ form.userfname.data }}')
	#return redirect(url_for('login'))
	return render_template('signup.html', title='SignUp')

        
@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
	return redirect(url_for('mainpage'))
    form= LoginForm() 
    if form.validate_on_submit():
	user = User.query.filter_by(UserEmail=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password') 
	    return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)






