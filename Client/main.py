import socket 
import Helpers
import Constants

ip=Helpers.get_ip_address()
port=Constants.CLIENT_PORT

print(ip, port)
class Client:
    def __init__(self):
        pass



def main():
    client=Client()

if __name__=="main":
    main()