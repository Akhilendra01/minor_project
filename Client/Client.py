import socket 
import Helpers
import Constants
import Utils
import json
import threading
from plyer import notification

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.data = self.load_client_data('./Client/data.json')
        except:
            print("Not registered")
        self.ip=Helpers.get_ip_address()

    def load_client_data(self, file):
        with open(file, 'r') as file:
            data = json.load(file)
            return data
        
    def get_public_key(self, target):
        message=f"get {target}"
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_socket.connect((Constants.CENTRAL_IP, Constants.CENTRAL_PORT))
        send_socket.send(message.encode())
        pub_key=send_socket.recv(2048).decode()
        send_socket.close()
        return pub_key

    def getip(self, target):
        message=f"getip {target}"
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_socket.connect((Constants.CENTRAL_IP, Constants.CENTRAL_PORT))
        send_socket.send(message.encode())
        ip=send_socket.recv(2048).decode()
        send_socket.close()
        return ip
    
    def send_message(self, target_ip, message, port=Constants.CLIENT_PORT):
        target_pub_key = self.get_public_key(target_ip)
        if len(target_ip)==6:
            target_ip=self.getip(target_ip)
        encrypted_message = Helpers.encrypt_message(target_pub_key, message)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_socket.connect((target_ip, Constants.CLIENT_PORT_RECV))
        send_socket.send(encrypted_message)
        send_socket.close()
    
    def decrypt(self, message):
        decrypted_message = Helpers.decrypt_message(self.data['private_key'], message)
        return decrypted_message

    def sender(self):
        while True:
            target_ip = input("Enter target IPv4\n")
            message = "handshake start"
            self.send_message(target_ip, message)
            print(f"Sent = {message}")
    
    def get_pseudonym(self, ip):
        message=f"getnym {ip}"
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_socket.connect((Constants.CENTRAL_IP, Constants.CENTRAL_PORT))
        send_socket.send(message.encode())
        pseudonym=send_socket.recv(2048).decode()
        send_socket.close()
        if pseudonym is None:
            pseudonym='None'
        notification_title = f"Pseudonym Search"
        notification_message = f"Pseudonym Received for {ip} is {pseudonym}"
        notification.notify(title=notification_title, message=notification_message)
        return pseudonym
    
    def receiver(self):
        print(f"Client Waiting to Connect [{self.ip}]")
        self.client_socket.bind((self.ip, Constants.CLIENT_PORT_RECV))
        self.client_socket.listen(1)
        while True:
            client_socket, client_addr = self.client_socket.accept()
            print("Connection accepted from:", client_addr)            
            message = client_socket.recv(4096)
            decrypted_message=self.decrypt(message)
            print(f"Received = {decrypted_message}")
            notification_title = "New Message Received"
            notification_message = f"From: {client_addr[0]}\nMessage: {decrypted_message}"
            notification.notify(title=notification_title, message=notification_message)

    def run(self):
        # thread1=threading.Thread(target=self.sender)
        thread2=threading.Thread(target=self.receiver)
        # thread1.start()
        thread2.start()