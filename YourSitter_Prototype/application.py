
# *** The application file runs the flask application ***


from main import app, db

#code to run the flask application in debug mode

if __name__=='__main__':
	app.run(host= '0.0.0.0', debug=True)
