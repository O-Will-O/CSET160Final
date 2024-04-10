from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, text


app = Flask(__name__)

# connection string is in the format mysql://user:password@server/database
conn_str = "mysql://root:cyber241@localhost/160final"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup', methods=['GET'])
def create_get_request():
    return render_template("signup.html")

@app.route('/signup', methods=['POST'])
def create_boats():
    conn.execute(text("INSERT INTO User VALUES (:user_id, :username, :password, :email)"), request.form)
    conn.commit()
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)

