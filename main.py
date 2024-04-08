from flask import Flask, render_template, request
from sqlalchemy import create_engine, text


app = Flask(__name__)

# connection string is in the format mysql://user:password@server/database
conn_str = "mysql://root:Ilikegames05!@localhost/160Final"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


if __name__ == '__main__':
    app.run(debug=True)

