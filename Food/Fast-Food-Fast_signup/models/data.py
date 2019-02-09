import os
import time
import datetime
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

class DatabaseConnection():
    """
       Class for processing logic for endpoints for new user..
    """

    def __init__(self):
        params = (
            """
            CREATE TABLE IF NOT EXISTS "users" (
                    user_id SERIAL PRIMARY KEY,
                    user_name VARCHAR(50) NOT NULL,
                    email VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(200) NOT NULL,
                    User_type BOOLEAN  NOT NULL

                )
            """,
            """
            CREATE TABLE IF NOT EXISTS "orders" (                    
                    order_id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES users(user_id),
                    user_name VARCHAR(30) NOT NULL,
                    order_name VARCHAR(20) NOT NULL,
                    order_status VARCHAR(20) NOT NULL,
                    order_date date                                    

                )
            """,
            """
            CREATE TABLE IF NOT EXISTS "items" (
                    item_id SERIAL PRIMARY KEY,
                    item VARCHAR(100) NOT NULL,
                    price VARCHAR(20) NOT NULL
                    
                    
                )
            """,)

        try:
            if (os.getenv("FLASK_ENV")) == "Production":
                self.connection = psycopg2.connect(os.getenv("DATABASE_URL"))
            else:
                self.connection = psycopg2.connect(dbname='andela',
                                                   user='postgres',
                                                   password='samr2015',
                                                   host='localhost',
                                                   port='5432')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            for param in params:
                self.cursor.execute(param)
        except(Exception, psycopg2.DatabaseError) as error:
            raise error

    def insert_new_user(self, user_name, email, password,user_type):

        self.cursor.execute("SELECT * FROM users WHERE email = %s", [email])
        check_email = self.cursor.fetchone()
        hashed_password = generate_password_hash(password, method='sha256')
        if check_email:
            return "email already exist"

        insert_item = "INSERT INTO users(user_name, email, password,user_type) VALUES('" + user_name + "', '" + email + "', '" + hashed_password + "', False)"
        self.cursor.execute(insert_item)
        return "Account created successfully"