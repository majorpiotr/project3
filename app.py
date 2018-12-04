from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
app = Flask(__name__)
# MySql config
app.config['MySLQ_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'project3' 
app.config['MYSQL_PASSWORD'] = 'project3' 
app.config['MYSQL_DB'] = 'project3' 
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Init MySql
mysql = MySQL(app) 



app.debug = True
@app.route('/')
def index():
	return render_template("index.html")

#	Register form class
class RegisterForm(Form):
	"""docstring for RegisterForm"""
	name = StringField( 'Name' , [ validators.Length( min = 1 , max = 50 ) ] )
	username = StringField( 'UserName' , [ validators.Length( min = 4 , max = 25 ) ] )
	email = StringField( 'Email' , [ validators.Length( min = 6 , max = 50 ) ] )
	password = PasswordField( 'Password' ,[
		validators.DataRequired(),
		validators.EqualTo( 'confirm' , 'Password do not match :( ')
	] )
	confirm = PasswordField( 'Confirm')

@app.route('/register', methods = ['GET','POST'] )
#	User register
def register():
	form = RegisterForm( request.form )
	if request.method == 'POST' and form.validate():		
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))
		# Create Cursor
		cur = mysql.connection.cursor()
		
		cur.execute('INSERT INTO users( name , email ,  username , password ) VALUES( %s , %s , %s , %s )', ( name , email ,username , password ))

		# Commit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash("Welcome in team :)", 'success')

		return redirect(url_for('index'))
		#return render_template( 'register.html' )
	return render_template( 'register.html' , form = form )
#	User login
@app.route('/login', methods = ['GET','POST'] )
def login():
	if request.method == 'POST':
		# Get form fields 
		username = request.form['username']
		passwordcandidate = request.form['password']

		# CREATE CURSOR
		cur=mysql.connection.cursor()
		# Get user by username 
		result = cur.execute('SELECT * FROM users WHERE name = %s', [username])
		if result > 0:
			# Get hash
			data = cur.fetchone()
			password = data['password']
			# Compare password
			if sha256_crypt.verify(passwordcandidate,password):
				session['logged_in']= True
				session['username']= username

				flash("your are now logged in")
				return redirect(url_for('dashboard'))
				message = 'Welcome again ' + username + "  :)  I wish you a lot of succeses in learning :)"
				#message[1] = 'success'
				return render_template('login.html', message = message, status = 'success')
			else:
				message = 'Unfortunetly :( Your password seams to be wrong. Are you sure that you are : ' + username + " ?"
				#message[1] = 'danger'
				return render_template('login.html', message = message, status ='danger')
			cur.close()
	else:
		app.logger.info('There is no such a user')

	return render_template('login.html')
def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			return redirect(url_for('login'))
	return wrap
#	user logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	return redirect(url_for('login'))

#	Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
	return render_template("dashboard.html")
app.secret_key='secret123'
if __name__ == '__main__':
  app.run()