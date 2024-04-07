import socket 
import Helpers
import Constants
import Utils
import json
import threading

ip=Helpers.get_ip_address()

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = self.load_client_data('./Client/data.json')

    def load_client_data(self, file):
        with open(file, 'r') as file:
            data = json.load(file)
            return data

    def get_pub_key(self, target_ip):
        self.client_socket.connect((Constants.CENTRAL_IP, Constants.CENTRAL_PORT))
        self.client_socket.send(f"get {target_ip}".encode())
        response = self.client_socket.recv(2048).decode()
        return response

    def send_message(self, target_ip, message, port=Constants.CLIENT_PORT_RECV):
        target_pub_key = self.get_pub_key(target_ip)
        encrypted_message = Helpers.encrypt_message(target_pub_key, message)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_socket.connect((target_ip, Constants.CLIENT_PORT_RECV))
        send_socket.send(encrypted_message)
        send_socket.close()

    def decrypt(self, message):
        decrypted_message = Helpers.decrypt_message(self.data['private_key'], message)
        return decrypted_message

    def run_sender(self):
        while True:
            target_ip = input("Enter target IPv4\n")
            message = "handshake start"
            self.send_message(target_ip, message)
            recv_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            recv_socket.bind((ip, Constants.CLIENT_PORT_SEND))
            client_socket, client_addr=recv_socket.accept()
            if client_addr[0]!=target_ip:
                recv_socket.close()
                client_socket.close()
                continue
            message=recv_socket.recv(2048)
            message=Helpers.decrypt_message(self.data['private_key'], message)
            if message=="handshake done":
                self.send_message(target_ip, "handhshake done")

    def run_receiver(self):
        self.server_socket.bind((ip, Constants.CLIENT_PORT_RECV))
        print(f"RECV on port [{Constants.CLIENT_PORT_RECV}]")
        self.server_socket.listen(1)
        while True:
            client_socket, client_addr = self.server_socket.accept()
            message = client_socket.recv(2048)
            decrypted_message = self.decrypt(message)
            print("Received:", decrypted_message, client_addr)
            if(decrypted_message=="hanshake start"):
                target_pub_key=self.get_pub_key(client_addr[0])
                client_socket.send(Helpers.encrypt_message(target_pub_key, "handshake done"))
                message=client_socket.recv(2048)
                decrypted_message=Helpers.decrypt_message(self.data['private_key'], message)

            client_socket.close()
client=Client()

thread1 = threading.Thread(target=client.run_receiver)
thread2 = threading.Thread(target=client.run_sender)

thread1.start()
thread2.start()

thread1.join()
thread2.join()