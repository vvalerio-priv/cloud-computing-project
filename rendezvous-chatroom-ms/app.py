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

from flask import Flask, render_template, flash, redirect, request, session, logging, url_for, jsonify

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

import json

import uuid

import datetime

import time;



# Now create flask application object

app = Flask(__name__)

# Database Configuration and Creating object of SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@'+os.environ['DBHOST']+':3306/'+os.environ['DBSCHEMA']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):

    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.String(15), unique=False)

    sender_name = db.Column(db.String(50), unique=True)

    server_timestamp = db.Column(
        db.DateTime
    )


initializated = False

# User Registration Api End Point
@app.route('/message/', methods = ['GET', 'POST'])
def message():
    if request.method == 'POST':
        sender_name = request.args.get('username')
        content = request.args.get('content')
    
        if len(content) == 0:
            return {}

        new_message = Message(
            sender_name = sender_name, 
            content = content
        )
        db.session.add(new_message)
        db.session.commit()
        data_set = {"sender_name":sender_name, "content":content}
        json_dump = json.dumps(data_set)
        print(json_dump)
        return json_dump
    else:
        resultList = []

        last_seen_id = request.args.get("last_seen_id", 0)

        app.logger.info("last seen id "+str(last_seen_id))
        messages = Message.query.filter(Message.id > last_seen_id).all()
        app.logger.info(len(messages))

        #return messages
        for message in messages:
            data_set = {"id": message.id, "sender_name":message.sender_name, "content":message.content, "server_timestamp":str(message.server_timestamp)}
            resultList.append(data_set)
        json_dump = json.dumps(resultList)
        print(json_dump)
        return json_dump

if __name__ == '__main__':
    # Creating database tables
    db.create_all()
    # running server
    app.run(debug=True)
