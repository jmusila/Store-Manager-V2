import json
import re

import uuid
from datetime import datetime, timedelta

import jwt
import psycopg2
from flask import jsonify, request
from validate_email import validate_email
from werkzeug.security import check_password_hash

from instance.config import Config
from db import conn
from app.api.v2.models.products import User 
from . import users

try:
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()

except Exception as e:
    print('connection exception ', e)
    cur = conn.cursor()
    cur.execute("ROLLBACK")


def auth_encode(user_id):
    """Generate auth token"""
    try:
        payload = {
            'exp': datetime.now() + timedelta(hours=1),
            'iat': datetime.now(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            Config.SECRET
        )
    except Exception as ex:
        raise ex


def auth_decode(token):
    """Decode auth token"""
    try:
        payload = jwt.decode(token, Config.SECRET)
        return payload['sub']
    except Exception as e:
        print('auth_token error', e)
        return None


def insert_token(token):
    """change the status of a request"""
    query = "INSERT INTO tokens (id, expired_tokens) VALUES ('%s','%s');" % (uuid.uuid4(), token)
    cur.execute(query)
    conn.commit()


def get_token(token):
    """get token from db"""
    cur.execute("SELECT expired_tokens FROM tokens WHERE expired_tokens = '%s';" % token)
    token = cur.fetchone()
    return token


def get_user_id():
    """ get user_id from token"""
    token = request.headers.get('token', None)
    return auth_decode(token)


@users.route('/user/register', methods=['POST'])
def signup():
    """sign up a new user"""
    try:
        firstname = json.loads(request.data.decode())['firstname']
        lastname = json.loads(request.data.decode())['lastname']
        password = json.loads(request.data.decode())['password'].replace(" ", "")
        email = json.loads(request.data.decode())['email'].replace(" ", "")

        if not validate_email(email):
            return jsonify({'response': 'invalid email'}), 400
        if re.match('[A-Za-z0-9@#$%^&+=]{8,}', password) is None:
            return jsonify({'response': 'password must contain 8 or more characters'}), 400

        """
        search if the user exists in the database
        """
        user = User(firstname, lastname, email, "")
        if user.exists(email) is None:
            user.create_user(password)
            return jsonify({'response': 'user created successfully'}), 201
        else:
            return jsonify({'response': 'user already exists'}), 409
    except (KeyError, ValueError) as ex:
        print('response', ex)
        return jsonify({'response': 'json body must contain firstname,lastname, password and email'}), 400
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as ex:
        print('error in signup', ex)
        return jsonify({'response': 'something went wrong'}), 500

@users.route('/user/login', methods=['POST']) 
def login():
    """
    login an existing user
    """
    try:

        email = json.loads(request.data.decode())['email'].replace(" ", "")
        password = json.loads(request.data.decode())['password'].replace(" ", "")
        user = User(email, "", "", "")

        user = user.exists(email)
        if check_password_hash(user[4], password):
            """token if password is correct"""
            token = auth_encode(email)
            if token:
                response = {'response': 'login successful', 'token': token.decode()}
                return jsonify(response), 200
        else:
            return jsonify({'response': 'invalid email/password'}), 422
    except (KeyError, ValueError) as ex:
        print('error in login', ex)
        return jsonify({'response': 'json body must contain email and password'}), 400
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as ex:
        print('error in login', ex)
        return jsonify({'response': 'user not found'}), 404

@users.route('/user/logout', methods=['POST'])
def signout():
    """sign out user """
    try:
        token = request.headers.get('token')
        # insert token to expired db
        if get_token(token) is None:
            insert_token(token)
            return jsonify({'response': 'signed out'}), 200
        else:
            return jsonify({'response': 'Invalid token'}), 401
    except Exception as ex:
        print('response', ex)
        return jsonify({'response': 'something went wrong'}), 500