from flask import Flask, render_template, redirect, url_for, request, session, g, Blueprint, abort, send_from_directory, flash, jsonify
import docker, os, requests, json, flask_sqlalchemy
from docker import client
from flask_session import Session
from json import JSONEncoder
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.secret_key = "MXjsdyyD34D"  

class Contentdecorator:
    def UserGetDecorator(user):
        # user = UserInfo.query.all()
        output = []
        for user_detail in user:
            UserInformation = Contentdecorator.ContentMapper(user_detail)
            output.append(UserInformation)
        return output

    def ContentMapper(user_detail):
        PerUserInfo = {'Firstname':  user_detail.firstname, 'Last Name': user_detail.lastname, 
        'Docker Username' : user_detail.docker_username, 'Docker password' : user_detail.docker_password, 
        'Docker Registry' : user_detail.docker_registry} 
        return PerUserInfo

    # def UserCreateDecorator(user_detail):

    #     firstname=user_detail['firstname'] 
    #     lastname=user_detail['lastname'] 
    #     docker_username=user_detail['docker_username']
    #     docker_password=user_detail['docker_password']
    #     docker_registry=user_detail['docker_registry']
    #     for UserInformation in (firstname, lastname, docker_username, docker_password, docker_registry):
    #     # #     print(UserInformation)
    #     # UserInformation = 
    #     # # return usertoAdd


