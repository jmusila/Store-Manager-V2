import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash

from db import conn

try:
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()

except Exception as e:
    print('connection exception ', e)
    cur = conn.cursor()
    cur.execute("ROLLBACK")


class User(object):
    def __init__(self, firstname, lastname, email, password_hash):
        self.user_id = ''
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password_hash = password_hash
        self.time_created = datetime.now()

    def create_user(self, password):
        """Create user in db DONE"""
        password_hash = generate_password_hash(password)
        user_id = uuid.uuid4()
        query = "INSERT INTO " \
                "users (id, firstname, lastname, email, password_hash, role, time_created)" \
                "VALUES('%s','%s', '%s', '%s', '%s', '%s', '%s')" % (
                user_id, self.firstname, self.lastname, self.email, password_hash, False, self.time_created)
        cur.execute(query)
        conn.commit()

    def get_user(self, user_id):
        """get user using user_id"""
        cur.execute("SELECT * FROM users WHERE id = %s;" % user_id)
        user = cur.fetchone()
        user_dict = {'id': user[0], 'firstname': user[1], 'lastname': user[2], 'email': user[3], 'password_hash': user[4],
                     'time_created': user[5]}
        print(user_dict, "userdict")
        return user_dict

    def exists(self,email):
        """check if user exists using"""
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cur.fetchone()
        return user


class Product(object):
    def __init__(self, name, quantity, price):
        self.product_id = ''
        self.name = name
        self.quantity = quantity
        self.price = price
        self.time_added = datetime.now()

    def insert_product(self):
        """insert product to db"""
        self.product_id = uuid.uuid4()
        # products titles should not be the same
        if self.get_product(self.product_id) is None:
            query = "INSERT INTO products (id, name, quantity, price, time_added)" \
                    "VALUES ('%s', '%s', '%s', '%s', '%s')" % (self.product_id, self.name, self.quantity, self.price,
                                                                     self.time_added)
            cur.execute(query)
            conn.commit()
            return True
        else:
            return False

    @staticmethod
    def delete_product(product_id):
        """delete product from db"""
        if Product.get_product(product_id) is not None:
            cur.execute("DELETE FROM products WHERE id='%s';" % product_id)
            return True
        else:
            return False

    @staticmethod
    def get_all_products():
        """get all products in db"""
        cur.execute("SELECT * FROM products;")
        all_products = cur.fetchall()
        product_list = []
        for product in all_products:
            product_dict = {'product_id': product[0], 'price': product[1], 'quantity': product[2],'time_added': product[4]}
            product_list.append(product_dict)
        return product_list

    @staticmethod
    def get_product(name):
        """get specific product from db using id"""
        cur.execute("SELECT * FROM products WHERE id = '%s'", (name))
        product = cur.fetchone()
        if product is not None:
            item = Product(product[1], product[2], product[3])
            item.name = name
            item.time_added = product[4]
            return item
        return None


    def update_product(self):
        cur.execute("UPDATE products SET quantity=%s, price=%s, time_added=%s"
                    "WHERE id=%s;",
                    (self.quantity, self.price, self.time_added, self.product_id))
        conn.commit()

