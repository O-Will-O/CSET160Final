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

app.secret_key = 'cyber241'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'cyber241'
app.config['MYSQL_DB'] = '160Final'

mysql = MySQL(app)


@app.route('/')
def index():
    if 'loggedin' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['UserID'] = account['UserID']
            session['username'] = account['username']
            session['account_type'] = account['account_type']  # recent change
            msg = 'Login success!'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Wrong username or password'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('UserID', None)
    session.pop('username', None)
    session.pop('account_type', None)  # Recent
    return redirect(url_for('login'))



@app.route('/signup', methods =['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account_type = request.form['account_type']  # Recent
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = %s', (username,))
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
            cursor.execute('INSERT INTO User  (username, password, email, account_type) VALUES (%s, %s, %s, %s)', (username, password, email, account_type))
            mysql.connection.commit()
            msg = 'Successfully registered!'

            session['account_type'] = account_type  # Recent

            return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form'
    return render_template('signup.html', msg=msg)

@app.route('/all_users')
def get_accounts():
    account_type_filter = request.args.get('account_type')
    if account_type_filter == 'teacher':
        query = text("SELECT UserID, username, email, account_type FROM User WHERE account_type = 'teacher'")
    elif account_type_filter == 'student':
        query = text("SELECT UserID, username, email, account_type FROM User WHERE account_type = 'student'")
    else:
        query = text("SELECT UserID, username, email, account_type FROM User")

    people = conn.execute(query).all()
    print(people)
    return render_template("all_users.html", user_info=people[0:25], account_type_filter=account_type_filter)



@app.route('/testselect')
def selectTest():
    testslist = conn.execute(text("select testID, TeacherID, name from StoredTests natural join teacher;")).all()
    print(testslist)
    return render_template("TestSelect.html", tests=testslist)

@app.route('/<Test>', methods=['GET'])
def take(Test):
    if request.path.endswith('.ico'):  # Filter out requests for favicon.ico
        return "Resource Not Found", 404
    testsques = conn.execute(text(f"select questions from StoredTests where TestID = '{Test}';")).all()
    testsques = testsques[0]
    removeComma = testsques[0][:-1]
    split_list = removeComma[0::].split(';')
    print(split_list)
    return render_template("TakeTest.html", testq=split_list, Test=Test)

@app.route('/<Test>', methods=['POST'])
def post(Test):
    conn.execute(text("INSERT INTO FinishedTests (responses) VALUES (:Ques)"), request.form)
    conn.commit()
    return render_template('TestSelect.html')
@app.route('/')
def hello():
    return render_template('base.html')
@app.route('/teacherAccount', methods=['GET'])
def teacher():
    return render_template('account.html')
@app.route('/teacherAccount', methods=['POST'])
def teacherAcc():
    conn.execute(text('Insert into teacher (TeacherID, name) Values (:TeacherID, :name)', request.form))
    conn.commit()
    return render_template('account.html')
@app.route('/createTest', methods=['GET'])
def create():
    return render_template('create.html')
@app.route('/createTest', methods=['POST'])
def createTest():
    conn.execute(text('INSERT INTO StoredTests (testID, TeacherID, questions) VALUES (:testID, :TeacherID, :questions)'), request.form)
    conn.commit()
    return render_template('create.html')
@app.route('/editTest', methods=['GET'])
def edit():
    return render_template('edit.html')
@app.route('/editTest', methods=['POST'])
def editTest():
    test_id = request.form['test_id']
    new_questions = request.form['new_questions']
    conn.execute(text('ALTER TABLE StoredTests SET questions = :new_questions WHERE testID = :test_id'), {"new_questions": new_questions, "test_id": test_id})
    conn.commit()
    return render_template('edit.html')
@app.route('/deleteTest', methods=['GET'])
def delete():
    return render_template('delete.html')
# @app.route('/deleteTest', methods=['POST'])
# def deleteTest():
#     conn.execute(text('Alter')

if __name__ == '__main__':
    app.run(debug=True)

