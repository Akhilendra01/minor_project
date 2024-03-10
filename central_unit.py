import socket
import mysql.connector
import helpers as hlp
import json

def connectDB():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin@123",
            database="test"
        )
        print("Connected to database")
        return connection
    except mysql.connector.Error as err:
        print("Error occured while connecting to database:", err)
        return None

def generate():
        name=hlp.generate_pseudonym()
        private_key, public_key=hlp.generate_rsa_key_pair()
        private_key=hlp.private_key_to_text(private_key)
        public_key=hlp.public_key_to_text(public_key)
        return {
            "name": name,
            "private_key": private_key,
            "public_key": public_key
        }

def run_server(host="10.12.184.78", port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    while True: 
        client_socket, client_addr = server_socket.accept()
        print("Connection accepted from:", client_addr)

        command = client_socket.recv(2048).decode().lower().strip()
        if command=="generate":
            data=generate()
            client_socket.send(json.dumps(data).encode())
            client_socket.close()

run_server()
