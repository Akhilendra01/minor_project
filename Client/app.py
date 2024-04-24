import socket 
import Helpers
import Constants
import Utils
import json
import threading
import tkinter as tk
from .Client import Client

class ClientGUI:
    def __init__(self, root, client):
        self.root = root
        self.root.title("Client GUI")

        self.client = client
        self.create_widgets()

    def create_widgets(self):
        self.target_ip_label = tk.Label(self.root, text="Enter Target IP / Pseudonym:")
        self.target_ip_label.pack()

        self.target_ip_entry = tk.Entry(self.root)
        self.target_ip_entry.pack()

        self.message_label = tk.Label(self.root, text="Enter Message:")
        self.message_label.pack()

        self.message_entry = tk.Entry(self.root)
        self.message_entry.pack()

        self.send_button = tk.Button(self.root, text="Send Message", command=self.send_message)
        self.send_button.pack()

    def send_message(self):
        target_ip = self.target_ip_entry.get()
        message = self.message_entry.get()
        print(target_ip, message)
        if message!='':
            self.client.send_message(target_ip, message)
        else:
            self.client.get_pseudonym(target_ip)

def main():
    root = tk.Tk()

    client = Client()
    client_gui = ClientGUI(root, client)

    client.run()

    root.mainloop()

if __name__ == "__main__":
    main()
