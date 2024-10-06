import json

from flask import Flask, session, request, abort, redirect, send_from_directory
from flask_cors import CORS
import db
from environ import *


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.secret_key = 'asassfasfwg3h421'


def _auth():
    username, password = map(lambda x: session.get(x), ['username', 'password'])
    if not (username and password):
        abort(401)
    return username, password


@app.route("/logged_in")
def logged_in():
    username, password = map(lambda x: session.get(x), ['username', 'password'])
    if not (username and password):
        abort(401)
    return ""


@app.route('/login', methods=['POST'])
def login():
    if request.json.get("use_cookie"):
        username, password = _auth()
    else:
        username, password = map(lambda x: request.json.get(x), ['username', 'password'])
        if not (username and password):
            abort(400)
    if not db.check_user_exists(username):
        abort(403)
    else:
        if not db.check_password(username, password):
            abort(403)

    session["username"], session["password"] = username, password
    return json.dumps({
        "host": get_external_db_host(),
        "port": get_db_port(),
        "user": username,
        "password": password,
        "database": db.get_db_name(username),
    })


@app.route('/reg', methods=['POST'])
def reg():
    username, password = map(lambda x: request.json.get(x), ['username', 'password'])
    if not (username and password):
        abort(400)
    if not db.check_user_exists(username):
        db.create_user(username, password)
    else:
        abort(403)
    session["username"], session["password"] = username, password
    return "created"


@app.route('/tables', methods=['GET'])
def tables():
    _, _ = _auth()
    return json.dumps({
        "tables": list(map(lambda t: t[0], db.collect_tables()))
    })


@app.route('/recreate_table', methods=['POST'])
def recreate_table():
    username, password = _auth()
    db.recreate_table(username, password, request.json["table"])
    return ""


@app.route('/recreate_all_tables', methods=['POST'])
def recreate_all_tables():
    username, password = _auth()
    db.init_tables(username, password)
    return ""


@app.route('/<path:path>')
def send_report(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run()
