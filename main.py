from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, text
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app = Flask(__name__)

# connection string is in the format mysql://user:password@server/database
conn_str = "mysql://root:cyber241@localhost/160final"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'cyber241'
app.config['MYSQL_DB'] = '160Final'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['UserID'] = account['UserID']
            session['username'] = account['username']
            msg = 'Login success!'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Wrong username or password'
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('UserID', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/signup', methods =['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Please enter only numbers or letters !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO User VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'Successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form'
    return render_template('signup.html', msg = msg)

if __name__ == '__main__':
    app.run(debug=True)

