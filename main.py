from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)

# connection string is in the format mysql://user:password@server/database
conn_str = "mysql://root:Ilikegames05!@localhost/160final"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route('/')
def index():
    return render_template("index.html")


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
    return render_template("TakeTest.html", testq=split_list)

if __name__ == '__main__':
    app.run(debug=True)
