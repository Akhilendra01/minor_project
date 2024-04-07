import Constants
import Helpers
import socket
import mysql.connector
import json
# import commands
from .utils import *

class Server:
    def __init__(self):
        self.host=Helpers.get_ip_address()
        self.port=Constants.CENTRAL_PORT
        self.db=connect_db()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

    def run(self):
        print(f"Central Server [HOST {self.host}, PORT {self.port}]")
        while True:
            client_socket, client_addr = self.server_socket.accept()
            print("Connection accepted from:", client_addr)            
            command = client_socket.recv(2048).decode().lower().strip()
            if command == "generate":
                try: 
                    data = generate_data()
                    connection = self.db
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
                connection=self.db
                name=command.split(' ')[1]
                if search(name, connection):
                    public_key=get_public_key(name, connection)
                    client_socket.send(public_key.encode())
                else:
                    client_socket.send("No such psedunym/ip exists".encode())
                connection.close()
                client_socket.close()
            else:
                client_socket.send("Bye".encode())
                client_socket.close()  

def main():
    server=Server()
    server.run()
if __name__=="__main__":
    main()