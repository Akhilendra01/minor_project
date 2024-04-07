import socket 
import Helpers
import Constants

ip=Helpers.get_ip_address()
port=Constants.CLIENT_PORT


print(ip, port)
class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.bind((ip, port))
        self.client_socket.listen(1)

    # def send_message(self, target_ip, message, private_key):
    #     pass

    # def receive_message(self):
    #     pass

    # def initiate_handshake(self, target_ip):
    #     send_message(target_ip, "initiate handshake")
    #     response=receive_message()

    def run(self):
        pass

def main():
    client=Client()

if __name__=="main":
    main()