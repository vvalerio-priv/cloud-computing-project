# Copyright 2021 valerio
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Importing require libraries
import os

from flask import Flask, render_template, flash, redirect, request, session, logging, url_for

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

import json

import uuid


# Now create flask application object

app = Flask(__name__)

# Database Configuration and Creating object of SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@'+os.environ['DBHOST']+':3306/'+os.environ['DBSCHEMA']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# Create User Model which contains id [Auto Generated], name, username, email and password

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(15), unique=False)

    email = db.Column(db.String(50), unique=True)

    password = db.Column(db.String(256), unique=False)



# User Registration Api End Point
@app.route('/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.args.get('username')
        email = request.args.get('email')
        password = request.args.get('password')

        print(username)
        print(email)
        print(password)

        user_id = str(uuid.uuid4())

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(
            id = user_id,
            username = username, 
            email = email, 
            password = hashed_password )
        db.session.add(new_user)
        db.session.commit()
        data_set = {"code":200, "message":"You have successfully registered"}
        json_dump = json.dumps(data_set)
        print(json_dump)
        return json_dump
    else:
        data_set = {"code":200, "message":"Just a redirect."}
        json_dump = json.dumps(data_set)
        print(json_dump)
        return json_dump

# Login API endpoint implementation
@app.route('/login/', methods = ['GET', 'POST'])
def login():

    email = request.args.get('email')
    password = request.args.get('password')

    if request.method == 'POST':
        user = User.query.filter_by(email = email).first()
        if user:
            # if user exist in database than we will compare our database hased password and password come from login form 
            if check_password_hash(user.password, password):
                data_set = {"code":200,"logged_in": True, "id":user.id, "email": user.email , "username": user.username, "message":"You have successfully logged in."}
                json_dump = json.dumps(data_set)
                print(json_dump)
                return json_dump
            else:
                # if password is in correct , redirect to login page
                #flash('Username or Password Incorrect', "Danger")
                data_set = {"code":400,"logged_in": True, "message":"Username or Password Incorrect"}
                json_dump = json.dumps(data_set)
                print(json_dump)
                return json_dump
    # rendering login page
    data_set = {"code":200,"message":"Empty"}
    json_dump = json.dumps(data_set)
    print(json_dump)
    return json_dump


@app.route('/logout/')
def logout():
    data_set = {"code":200,"logged_in": False, "message":"You have successfully logged out."}
    json_dump = json.dumps(data_set)
    print(json_dump)
    return json_dump

if __name__ == '__main__':
    # Creating database tables
    db.create_all()
    # running server
    app.run(debug=True)
