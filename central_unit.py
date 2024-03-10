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
            database="minor_project"
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

def search(name: str, connection):
    sql=f"select * from users where pseudonym='{name.strip()}';"
    cursor=connection.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    return rows if rows else None

def get_public_key(name: str, connection)->str:
    sql=f"select public_key from users where pseudonym='{name.strip()}';"
    cursor=connection.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    return rows[0][0]

def run_server(host="10.12.184.78", port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    while True: 
        client_socket, client_addr = server_socket.accept()
        print("Connection accepted from:", client_addr)
        
        command = client_socket.recv(2048).decode().lower().strip()
        if command == "generate":
            try: 
                data = generate()
                connection = connectDB()
                cursor = connection.cursor()
                sql = f"INSERT INTO users values('{client_addr[0]}', '{data['name'].strip()}', '{data['public_key']}')"
                try: 
                    cursor.execute(sql)
                    connection.commit()
                    print('Entry done in database')                
                    client_socket.send(json.dumps(data).encode())
                except:
                    print('error in executing sql')
                finally:
                    client_socket.close()
                    connection.close()
            except mysql.connector.Error as err:
                print("Error occurred while connecting to database:", err)
                client_socket.close()

        elif command[: 3].lower()=="get":
            connection=connectDB()
            name=command.split(' ')[1]
            if search(name, connection):
                public_key=get_public_key(name, connection)
                client_socket.send(public_key.encode())
            else:
                client_socket.send("No such psedunym exists".encode())
            connection.close()
            client_socket.close()
        else:
            client_socket.send("Bye".encode())
            client_socket.close()           

run_server()
