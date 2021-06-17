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

# Importing Require Module

from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField, SelectField

from wtforms.validators import DataRequired

# Creating Login Form contains email and password
class LoginForm(Form):

    email = StringField("Email", validators=[validators.Length(min=7, max=50), validators.DataRequired(message="Please Fill This Field")])

    password = PasswordField("Password", validators=[validators.DataRequired(message="Please Fill This Field")])

# Creating Registration Form contains username, name, email, password and confirm password.

class RegisterForm(Form):

    username = StringField("Username", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Please Fill This Field")])

    email = StringField("Email", validators=[validators.Email(message="Please enter a valid email address")])

    password = PasswordField("Password", validators=[

        validators.DataRequired(message="Please Fill This Field"),

        validators.EqualTo(fieldname="confirm", message="Your Passwords Do Not Match")
    ])

    confirm = PasswordField("Confirm Password", validators=[validators.DataRequired(message="Please Fill This Field")])

class MessageForm(Form):

    content = StringField("Content", validators=[validators.Length(min=1, max=600), validators.DataRequired(message="Please Fill This Field")])

class RoomForm(Form):
    CHOICES = ["chat", "video", "videochat"]
    name = StringField("Name", validators=[validators.Length(min=1, max=200), validators.DataRequired(message="Please Fill This Field")])
    typeroom = SelectField("Type", choices=CHOICES)