import mysql.connector

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin@123",
            database="minor_project"
        )
        print("Connected to database")
        return connection
    except mysql.connector.Error as err:
        print("Error occured while connecting to database:", err)
        return None

import Helpers

def generate_data():
    name=Helpers.generate_pseudonym()
    private_key, public_key=Helpers.generate_rsa_key_pair()
    private_key=Helpers.private_key_to_text(private_key)
    public_key=Helpers.public_key_to_text(public_key)
    return {
        "name": name,
        "private_key": private_key,
        "public_key": public_key
    }

def get_public_key(name: str, connection)->str:
    sql=f"select public_key from users where pseudonym='{name.strip()}' or ip='{name.strip()}';"
    cursor=connection.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    return rows[0][0]

def search(name: str, connection):
    sql=f"select * from users where pseudonym='{name.strip()}' or ip='{name.strip()}';"
    cursor=connection.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    return rows if rows else None

def getnym(ip, connection):
    sql=f"select pseudonym from users where ip='{ip.strip()}';"
    cursor=connection.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    return rows[0][0]