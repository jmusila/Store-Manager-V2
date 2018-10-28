"""
This is db.py file which creates database tables when run
"""
import psycopg2

try:
    conn = psycopg2.connect("dbname=storemanager host=localhost user=store password= '123store'")
except Exception as e:
    print("connect to database failed ", e)

def create_tables():
    cur = conn.cursor()
    try:
        # delete tables if they exist
        cur.execute("DROP TABLE IF EXISTS products,sales, users;")
        cur.execute("DROP TABLE IF EXISTS tokens;")

        # create table users
        users = "CREATE TABLE users(id VARCHAR(256) PRIMARY KEY, firstname VARCHAR(64),lastname VARCHAR(64), email VARCHAR(64) UNIQUE," \
                "password_hash VARCHAR(256),role VARCHAR(10), time_created TIMESTAMP );"

        # create table products
        products = "CREATE TABLE products(id VARCHAR(256) PRIMARY KEY, name VARCHAR(256)," \
                    "quantity INT,price NUMERIC, time_added TIMESTAMP);"

        # create table sales
        sales = "CREATE TABLE sales(id VARCHAR(256) PRIMARY KEY, total_amount NUMERIC," \
                  "quntity INT, time_created TIMESTAMP, created_by VARCHAR(64));"

        # create table tokens
        tokens = "CREATE TABLE tokens(id VARCHAR(256) PRIMARY KEY, expired_tokens VARCHAR(256));"


        cur.execute(users)
        cur.execute(products)
        cur.execute(sales)
        cur.execute(tokens)

        conn.commit()
    except Exception as ex:
        print('error in migration', ex)


def delete_tables():
    cur = conn.cursor()
    cur.execute("DELETE from users;")
    cur.execute("DELETE from products;")
    cur.execute("DELETE from sales;")
    cur.execute("DELETE from tokens;")
    conn.commit()