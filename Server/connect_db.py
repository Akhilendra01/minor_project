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
