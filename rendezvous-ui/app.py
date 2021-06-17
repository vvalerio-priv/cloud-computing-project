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

from flask import Flask, render_template, flash, redirect, request, session, logging, url_for, Response
import logging

import requests

from forms import LoginForm, RegisterForm, MessageForm, RoomForm

from werkzeug.security import generate_password_hash, check_password_hash

import json


app = Flask(__name__)

app.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register/', methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        params = {"username":form.username.data, "password":form.password.data, "email":form.email.data}
        response = requests.post(url="http://"+os.environ['AUTH-HOST']+":5000/register/?username="+form.username.data+"&password="+form.password.data+"&email="+form.email.data)
        response = response.json()
        flash(response['message'], 'success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', form = form)

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    
    if request.method == 'POST' and form.validate:
        params = {"password":form.password.data, "email":form.email.data}
        response = requests.post(url="http://"+os.environ['AUTH-HOST']+":5000/login/?password="+form.password.data+"&email="+form.email.data)
        response = response.json()
        if response['code'] == 200:
            flash(response['message'], "success")
            session['logged_in'] = True
            session['email'] = response['email']
            session['username'] = response['username']
            session['userid'] = response['id']
            return redirect(url_for('home'))

        else:
            flash(response['message'], "Danger")
            return redirect(url_for('login'))
    return render_template('login.html', form = form)

@app.route('/newroom/', methods = ['GET','POST'])
def newroom():
    form = RoomForm(request.form)
    
    if request.method == 'POST' and form.validate:
        response = requests.post(url="http://"+os.environ['ROOMROUTER-HOST']+":5000/createroom/?name="+form.name.data+"&type="+form.typeroom.data+"&userid="+session['userid'])
        response = response.json()
        if response['code'] == 200:
            flash(response['message'], "success")
            return redirect(url_for('rooms'))
        else:
            flash(response['message'], "Danger")
            return redirect(url_for('newroom'))
    return render_template('newroom.html', form = form)


@app.route('/rooms/', methods = ['GET','POST'])
def rooms():
    if request.method == 'GET':
        response = requests.get(url="http://"+os.environ['ROOMROUTER-HOST']+":5000/getroom/?userid="+session['userid'])
        response = response.json()
        app.logger.info(response)

        resultList = []
        columnNames = ["name", "url"]

        if 'rooms' in response :
            dictionary = json.loads(json.dumps(response['rooms']))
            for room in dictionary:
                app.logger.info(room)
                data_set = {"name": room['name'], "url":"/chatroom/?chaturl="+room['url_chat']}
                resultList.append(data_set)
            resultList = json.loads(json.dumps(resultList))

    return render_template('rooms.html', records=resultList, colnames=columnNames)

@app.route('/chatroom/')
def chatroom():
    chaturl = request.args.get("chaturl")
    os.environ['CHATROOM-HOST'] = chaturl
    return render_template('chatroom.html')

@app.route('/message/', methods = ['GET','POST'])
def message():
    if request.method == 'GET':
        resultList = []
        last_seen_id = request.args.get("last_seen_id", 0)
        messages = requests.get(url="http://"+os.environ['CHATROOM-HOST']+":5000/message/?last_seen_id="+last_seen_id)
        messages = messages.json()
        app.logger.info(messages)
        for message in messages:
            data_set = {"id": message['id'], "sender_name":message['sender_name'], "content":message['content'], "server_timestamp":str(message['server_timestamp'])}
            resultList.append(data_set)
        messages = json.dumps(resultList)
        return messages
    else:
        resultList = []
        data = request.json
        content = data["content"].strip()
        messages = requests.post(url="http://"+os.environ['CHATROOM-HOST']+":5000/message/?username="+session['username']+"&content="+content)
        messages = messages.json()
        return messages

@app.route('/videoroom/')
def videoroom():
    return render_template('videoroom.html')

@app.route('/logout/')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc', TEMPLATES_AUTO_RELOAD=True)
