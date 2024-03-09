import random
import string
import uuid
from flask import Flask, request
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import mysql.connector


def connectDB():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin@123',
            database='test'
        )

        if connection.is_connected():
            print('Connected to MySQL database')

        return connection

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")

connection=connectDB()
cursor=connection.cursor()

def query(sql):
    cursor.execute(sql)
    return cursor.fetchall()

def generate_pseudonym(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048 
    )
    return private_key

def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ':'.join([mac[e:e+2] for e in range(0, 11, 2)])

app=Flask(__name__)



@app.route('/')
def hello():
    print(query('select * from user;'))
    return f"{request.remote_addr}"


if __name__ == "__main__":
    app.run(debug=True)
