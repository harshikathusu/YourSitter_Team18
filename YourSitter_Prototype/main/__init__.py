# **** The initialisation file declares the flask application, database and imports key flask packages ***



# import dependencies and necessary packages

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# create the flask application object
application=Flask(__name__)
app=application


# Secret key to prevent CSRF

app.config['SECRET_KEY'] = 'Team18'

# path to connect the application to the MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Team18:araujoteam18@team18instance.crpo3dbnct0f.us-east-2.rds.amazonaws.com/team18instance'


## path to connect the application to the local SQLite database

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Team18:araujoteam18@mysqldb.crpo3dbnct0f.us-east-2.rds.amazonaws.com/team18db'
# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_file = "sqlite:///{}".format(os.path.join(project_dir, "yoursitter.db"))
# app.config['SQLALCHEMY_DATABASE_URI']= database_file


# initalize SQLAlchemy for CRUD operations

db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

from main import routes
