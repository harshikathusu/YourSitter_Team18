# *** The routes python file directs the flask application to conduct specific tasks associated with each HTML page. *** 



# importing all dependencies 
from flask import render_template, url_for, redirect, request, flash, session
from datetime import datetime
from flask_login import current_user, login_manager, logout_user, login_required, login_user
from main.forms import SignUpForm, SitterSignUpForm, LoginForm, ZipcodeForm
from main import app,db
from main.models import User, Parent, Sitter
import time


#app.config['SECRET_KEY'] = '0a31d758c1ff2046'


# Routing for each HTML page in the website

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# Admin display page    

@app.route('/display_all', methods=["GET", "POST"])
def display_all():
    # Accept user input to delete a user
    if request.method== "POST":
        if 'delSitterEmail' in request.form:
            email= request.form["delSitterEmail"]
            Sitter.query.filter(Sitter.SEmail == email).delete()
            User.query.filter(User.UserEmail == email).delete()
            db.session.commit()
        elif 'delParentEmail' in request.form:
            email= request.form["delParentEmail"]
            Parent.query.filter(Parent.PEmail == email).delete()
            User.query.filter(User.UserEmail == email).delete()
            db.session.commit()
    return render_template('display_all.html', Sitter=Sitter.query.all(), User=User.query.all(), Parent=Parent.query.all())

# Errorpage

@app.route('/error')
def error():
    return render_template('errorpage.html')

# Sign up page

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))	

    #Accept form input and input data into tables 

    if request.method == 'POST':
        user = User(UserEmail=request.form['email'], UserFName=request.form['firstname'], UserLName=request.form['lastname'], UserPw= request.form['password'] , is_Active=True, is_Parent=True)
        parent = Parent(PEmail=request.form['email'], PZipCode = request.form['zip'])

        #Validate user credentials
        e = db.session.query(User).filter_by(UserEmail= request.form['email']).first()
        if e is not None:
            flash('There is another account with this email. Try again')
            return redirect(url_for('signup'))
        entered = request.form['password']		
        confirmed = request.form['confirmpassword'] 
        if (entered != confirmed):
            flash('Passwords do not match. Try Again!')
            return redirect(url_for('signup'))
        else:
            users = [user]
            parents = [parent]
            db.session.merge(user)
            db.session.merge(parent)
            db.session.commit() 
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
	    
    return render_template('signup.html', title='SignUp')




# USer Login page

  
@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))	

    if request.method == 'POST':
        user = User.query.filter_by(UserEmail= request.form['email']).first()
        if user is None or not user.check_password(request.form['password']):
            flash('Invalid credentials. Try Again!')
            return redirect(url_for('login'))

            # Validate admin login
        elif (request.form['email']=="admin@admin.com" and request.form['password']=="admin"):
            return redirect(url_for('display_all'))
        
        else:	
            session['first_name'] = user.UserFName
            session['last_name'] = user.UserLName
            session['email'] = user.UserEmail
            if user.is_Parent==1:
                return redirect(url_for('parents_profile'))
            else:
                return redirect(url_for('sitters_profile'))
    else:
        return render_template('login.html', title='Login')  



# Profile page routing

@app.route('/Profile', methods=["GET", "POST"])
def Profile():
    return render_template('Profile.html')


# Route to render parents profile page

@app.route('/parents_profile', methods=["GET","POST"])
def parents_profile():
    
    if request.method == 'POST':
        # Filter sitters based on user input zipcode
        if 'zipcode' in request.form:
            zipcode= request.form["zipcode"]
            sitters = Sitter.query.filter_by(SZipcode=zipcode)
            users = User.query.all()
            return render_template('parents_profile.html', Sitter=sitters, User=users)
        else:
            password = request.form["password"]
            fname= request.form["fname"]
            lname= request.form["lname"]
            
            user = User.query.filter_by(UserEmail=session['email']).first()
            
            user.UserPw = password
            user.UserFName = fname
            user.UserLName = lname
            
            session['first_name'] = user.UserFName
            session['last_name'] = user.UserLName
            session['email'] = user.UserEmail
            
            db.session.merge(user)
            
            db.session.commit()        

    # Displaying list of all sitters
    sitters = Sitter.query.all()
    users = User.query.all()
    return render_template('parents_profile.html', Sitter=sitters, User=users)
    

# Route to render sitters profile page

@app.route('/sitters_profile', methods=["GET","POST"])
def sitters_profile():
    
    if request.method == 'POST':
        if 'zipcode' in request.form:
            zipcode= request.form["zipcode"]
            parents = Parent.query.filter_by(PZipCode=zipcode)
            users = User.query.all()
            return render_template('sitters_profile.html', Parent=parents, User=users)
        else:
            password = request.form["password"]
            fname= request.form["fname"]
            lname= request.form["lname"]
            
            user = User.query.filter_by(UserEmail=session['email']).first()
            
            user.UserPw = password
            user.UserFName = fname
            user.UserLName = lname
            
            session['first_name'] = user.UserFName
            session['last_name'] = user.UserLName
            session['email'] = user.UserEmail
            
            db.session.merge(user)
            
            db.session.commit()   

    # Display list of all parents to the  sitter  
    else:
        parents = Parent.query.all()
        users = User.query.all()
        return render_template('sitters_profile.html', Parent=parents, User=users)
    

# Route to display signup page to a sitter

@app.route('/sittersignup2', methods=["GET", "POST"])
def sittersignup2():
    if current_user.is_authenticated:
        return redirect(url_for('index'))   
    
    if request.method == 'POST':
        
        # Accept user input and create the respective records in the user and sitter table 

        user = User(UserEmail=request.form['email'], UserFName=request.form['firstname'], UserLName=request.form['lastname'], UserPw= request.form['password'], is_Active=True, is_Parent=False)
        sitter = Sitter(SEmail = request.form['email'], SZipcode= request.form['zip'])
        
        e = db.session.query(User).filter_by(UserEmail= request.form['email']).first()
        if e is not None:
            flash('There is another account with this email. Try again')
            return redirect(url_for('sittersignup2'))
        entered = request.form['password']        
        confirmed = request.form['confirmpassword']
        if (entered != confirmed):
            flash('Passwords do not match. Try Again!')
            return redirect(url_for('signup'))
        else:
            users = [user]
            sitters = [sitter]
            db.session.merge(user)
            db.session.merge(sitter)
            db.session.commit() 
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        
    return render_template('sittersignup2.html', title='Sitter SignUp')



# Logout

@app.route('/logout')
def logout():
    logout_user()
    
    return redirect(url_for('index'))
        # return redirect(url_for('index'))
