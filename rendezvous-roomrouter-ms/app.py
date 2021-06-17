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

import docker

# Now create flask application object

app = Flask(__name__)

# Database Configuration and Creating object of SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@'+os.environ['DBHOST']+':3306/'+os.environ['DBSCHEMA']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


client = docker.from_env()

# Create User Model which contains id [Auto Generated], name, username, email and password

class Room(db.Model):

    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), unique=False)

class ChatRoom(db.Model):

    __tablename__ = 'chatroom'

    id = db.Column(db.Integer, primary_key=True)
    serverurl = db.Column(db.String(45), unique=False)

class VideoRoom(db.Model):

    __tablename__ = 'videoroom'

    id = db.Column(db.Integer, primary_key=True)
    serverurl = db.Column(db.String(45), unique=False)

class UserRoom(db.Model):

    __tablename__ = 'user_has_room'

    user_id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, primary_key=True)

class RoomChatRoom(db.Model):

    __tablename__ = 'room_has_chatroom'

    room_id = db.Column(db.Integer, primary_key=True)
    chatroom_id = db.Column(db.Integer, primary_key=True)

class RoomVideoRoom(db.Model):

    __tablename__ = 'room_has_videoroom'

    room_id = db.Column(db.Integer, primary_key=True)
    videoroom_id = db.Column(db.Integer, primary_key=True)



# Room 
@app.route('/createroom/', methods = ['POST'])
def createroom():
    
    if request.method == 'POST':
        userid = request.args.get('userid')
        name = request.args.get('name')
        typeroom = request.args.get('type')

        room_id = str(uuid.uuid4())
        print(userid)
        print(name)
        print(typeroom)

        new_room = Room(
            id = room_id,
            name = name
        )

        new_room_user = UserRoom(
            user_id = userid, 
            room_id = room_id )

        if(typeroom == 'videochat') :
            print('videochat')
            #TODO: create url

            videoroom_id = str(uuid.uuid4())

            new_videoroom = VideoRoom(
            id = videoroom_id,
            serverurl = name
            )

            new_room_videoroom = RoomVideoRoom(
                videoroom_id = videoroom_id, 
                room_id = room_id )

            chatroom_id = str(uuid.uuid4())

            new_chatroom = ChatRoom(
            id = chatroom_id,
            serverurl = name
            )

            new_room_chatroom = RoomChatRoom(
                chatroom_id = chatroom_id, 
                room_id = room_id 
            )

            db.session.add(new_videoroom)
            db.session.add(new_chatroom)
            db.session.add(new_room_videoroom)
            db.session.add(new_room_chatroom)
            db.session.commit()
        
        if(typeroom == 'chat') :
            print('chat')
            chatroom_id = str(uuid.uuid4())

            chatroom_db = chatroom_id+"-db"

            app.logger.info("creating room")

            if os.environ['CLOUD_ENV'] == 'docker' :
                container_db = client.containers.run(
                    image="valeriovinciarelli/rendezvous-chatroom-database:0.1.2",
                    name=chatroom_db,
                    network='docker-compose_rendezvous',
                    detach=True
                )

                app.logger.info("room database")
                app.logger.info(container_db)

                hostdb= "DBHOST="+chatroom_db
                schemadb= "DBSCHEMA=rendezvous-chatroom"


                container = client.containers.run(
                    image="valeriovinciarelli/rendezvous-chatroom:0.1.2",
                    name=chatroom_id,
                    environment=[hostdb, schemadb],
                    network='docker-compose_rendezvous',
                    detach=True
                )

                app.logger.info("room chat")
                app.logger.info(container)

            new_chatroom = ChatRoom(
            id = chatroom_id,
            serverurl = chatroom_id
            )

            new_room_chatroom = RoomChatRoom(
                chatroom_id = chatroom_id, 
                room_id = room_id 
            )

            db.session.add(new_chatroom)
            db.session.add(new_room_chatroom)
            db.session.commit()
        
        if(typeroom == 'video') :
            print('video')
            #TODO: create url
            videoroom_id = str(uuid.uuid4())

            new_videoroom = VideoRoom(
            id = videoroom_id,
            serverurl = videoroom_id
            )

            new_room_videoroom = RoomVideoRoom(
                videoroom_id = videoroom_id, 
                room_id = room_id )

            db.session.add(new_videoroom)
            db.session.add(new_room_videoroom)
            db.session.commit()

        db.session.add(new_room)
        db.session.add(new_room_user)
        db.session.commit()
        
        data_set = {"code":200, "message":"You have successfully create a room"}
        json_dump = json.dumps(data_set)
        print(json_dump)
        return json_dump
    else:
        data_set = {"code":400, "message":"Bad Request."}
        json_dump = json.dumps(data_set)
        print(json_dump)
        return json_dump

# Login API endpoint implementation
@app.route('/getroom/', methods = ['GET'])
def getroom():

    resultList = []

    print(request.args.get('userid'))
    print(request.args.get('roomid'))

    user_id = request.args.get('userid')
    room_id = request.args.get('roomid')

    print(user_id)
    print(room_id)

    if request.method == 'GET':
        if(room_id == None):
            rooms = UserRoom.query.filter_by(user_id = user_id).all()
            for room in rooms:
                print(room.room_id)
                single = Room.query.filter_by(id = room.room_id).first()
                data_set = {"id":single.id,"name":single.name}
                single_chat = RoomChatRoom.query.filter_by(room_id = single.id).first()
                single_video = RoomVideoRoom.query.filter_by(room_id = single.id).first()

                videourl = None
                chaturl = None
                if single_chat != None:
                    chat = ChatRoom.query.filter_by(id = single_chat.chatroom_id).first()
                    chaturl = chat.serverurl
                if single_video != None:
                    video = VideoRoom.query.filter_by(id = single_video.videoroom_id).first()
                    videourl = video.serverurl

                data_set = {"id":single.id,"name":single.name, "url_video": videourl,"url_chat": chaturl}

                resultList.append(data_set)
                print(single.name)
        else:
            single = Room.query.filter_by(id = room_id).first()
            single_chat = RoomChatRoom.query.filter_by(room_id = single.id).first()
            single_video = RoomVideoRoom.query.filter_by(room_id = single.id).first()

            videourl = None
            chaturl = None
            if single_chat != None:
                chat = ChatRoom.query.filter_by(id = single_chat.chatroom_id).first()
                chaturl = chat.serverurl
            if single_video != None:
                video = VideoRoom.query.filter_by(id = single_video.videoroom_id).first()
                videourl = video.serverurl

            data_set = {"id":single.id,"name":single.name, "url_video": videourl,"url_chat": chaturl}

            resultList.append(data_set)
            print(single.name)
    # rendering login page
    if len(resultList) == 0 :
        data_set = {"code":200,"message":"Empty"}
    else:
        data_set = {"code":200,"message":"Rooms retrieved", "rooms": resultList}

    json_dump = json.dumps(data_set)
    print(json_dump)
    return json_dump

if __name__ == '__main__':
    # Creating database tables
    db.create_all()
    # running server
    app.run(debug=True)
