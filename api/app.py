from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint, abort, send_from_directory, flash, jsonify
import docker, os, requests, json, flask_sqlalchemy
from docker import client
from flask_session import Session
from json import JSONEncoder
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


# Classes Import Section
import modules
from modules.Container import Container
from modules.decorator import Contentdecorator
# from modules import decorator
# from modules.dbmodel import Student
# from users import register # DB connection Module 

app = Flask(__name__)
app.secret_key = "MXjsdyyD34D"  

# Application configuration file
app.config.from_pyfile(os.path.join("conf/app.conf"), silent=False)

# connection details below
app.config['DOCKER_HOST'] = app.config.get("DOCKER_HOST")
app.config['DOCKER_PORT'] = app.config.get('DOCKER_PORT')

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://dockerapi:masdfh45JJh$@172.17.0.3/docker'

db = SQLAlchemy(app)

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    docker_username = db.Column(db.String(80), unique=True, nullable=False)
    docker_password = db.Column(db.String(120))
    docker_registry = db.Column(db.String(180), nullable=False)

    def __repr__(self):
        return f'<Student {self.firstname}>'

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "devop-simulator"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###


@app.route('/api/v1/user/register', methods=['POST'])
def registerUser():
    try:
        user_detail = request.get_json()
        firstname=user_detail['firstname'] 
        lastname=user_detail['lastname'] 
        docker_username=user_detail['docker_username']
        docker_password=user_detail['docker_password']
        docker_registry=user_detail['docker_registry']    
        usertoGenerate = UserInfo(firstname=firstname,lastname=lastname, docker_username=docker_username, 
                                    docker_password=docker_password, docker_registry=docker_registry)
        db.session.add(usertoGenerate)
        db.session.commit()
        return "User registered successully"
    except:
        abort(409)

@app.route("/api/v1/user/get_all")
def user_detail():
    user = UserInfo.query.all()
    UserInformation = Contentdecorator.UserGetDecorator(user)
    return UserInformation

@app.route('/', methods=['GET'])
def rootindex():
    return "Wolcome to Docker API"
@app.route('/containers/<dockerhost>', methods=['GET'])
def index(dockerhost):
    return Container.listContainerAll(dockerhost)

@app.route('/containers/<dockerhost>/<userid>', methods=['GET', 'POST', 'PATCH'])
def home(dockerhost, userid):
    if request.method == 'GET':
        return Container.listContainerSpecific(dockerhost, userid)
    elif request.method == 'POST':
        return Container.containerCreate(dockerhost, request.get_json(force=True))
    else:
        abort(405)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')
@app.route('/containers/commit/<dockerhost>/<userid>/')
def commit(dockerhost, userid):
    return Container.containerCommitdelete(dockerhost, userid)
# start the server with the 'run()' method
if __name__ == '__main__':
    with app.app_context():
       db = SQLAlchemy(app) 
       db.create_all()
    app.run(host="0.0.0.0", port=5000, threaded=True)

