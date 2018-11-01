import json
import re

import psycopg2
from functools import wraps
from flask import request, jsonify

from ..views.users import get_token, get_user_email
from . import products
from ..models.products import *


def token_is_expired():
    """check if token is valid"""
    token = request.headers.get('token', None)

    # try getting user_id from token
    if get_user_email() is None:
        return 'Invalid token'
    else:
        # check if token is expired
        token_found = get_token(token)
        if token_found:
            return token_found


@products.app_errorhandler(404)
def not_found(error):
    return jsonify({'response': 'Nothing to see here'}), 404


@products.route('/products', methods=['GET'])
def get_products():
    """
    get:
        summary: Get products endpoint.
        description: Fetch all products.
        headers:
                token: <auth-token>
        responses:
            200:
                description: a list of products.
                schema: {"products":
                     [
                         {"name:"my name", "price":"price of product", "product_id": "product20"},
                         {"name:"my name", "price":"price of product", "product_id": "product20"}
                     ]
                 }
            204:
                description: returned if there are no products.
                schema: {"response": "It's empty here"}
            409:
                description: returned if token used is invalid.
                schema: {"error": "invalid token ..."}
            500:
                description: Internal server error.
                schema: {"error": "something went wrong ..."}
    """
    try:
            products = Product.get_all_products()
            if products:
                return jsonify({'products': products}), 200
            else:
                return jsonify({}), 204
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as ex:
        print('response', ex)
        return jsonify({'response': 'something went wrong'}), 500 

@products.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
            product = Product.get_product(product_id)
            if product:
                return jsonify({"product": product.__dict__}), 200
            else:
                return jsonify({"response": "product not found"}), 404
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as ex:
        print('response', ex)
        return jsonify({'response': 'something went wrong'}), 500
@products.route('/products', methods=['POST'])
def add_product():

    if token_is_expired() is None:
        try:
            name = json.loads(request.data.decode())['name']
            quantity = json.loads(request.data.decode())['quantity']
            price = json.loads(request.data.decode())['price']
            email = get_user_email()
            if email:
                product = Product(name=name, quantity=quantity, price=price)
                if not product.insert_product():
                    return jsonify({'response': 'product posted successfully'}), 201
                else:
                    return jsonify({'response': 'product with same name already exists'}), 409
            else:
                return jsonify({'response': 'could not generate token from user email'}), 401
        except (KeyError, ValueError) as ex:
            print('response', ex)
            return jsonify({'response': 'invalid json'}), 400
        except (psycopg2.DatabaseError, psycopg2.IntegrityError, KeyError, Exception) as ex:
            print('response', ex)
            return jsonify({'response': 'something went wrong'}), 500
    return jsonify({'response': 'Token not valid '}), 401

