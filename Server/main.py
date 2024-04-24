import Constants
import Helpers
import socket
import Utils
from .processor import *

class Server:
    def __init__(self):
        self.host=Helpers.get_ip_address()
        self.port=Constants.CENTRAL_PORT
        self.db=Utils.connect_db()
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
                response=generate(self.db, client_addr)
                client_socket.send(response.encode())
                client_socket.close()

            elif command[: 5].lower()=="getip":
                name=command.split(' ')[1]
                client_socket.send(getip(name, self.db).encode())
                client_socket.close()

            elif command[: 6].lower()=="getnym":
                name=command.split(' ')[1]
                client_socket.send(getnym(name, self.db).encode())
                client_socket.close()

            elif command[: 3].lower()=="get":
                name=command.split(' ')[1]
                client_socket.send(get_pub_key(name, self.db).encode())
                client_socket.close()

            else:
                client_socket.send("Bye".encode())
                client_socket.close()  

def main():
    server=Server()
    server.run()
if __name__=="__main__":
    main()