import tkinter as tk
import Client

class GUI:
    def __init__(self, root):
        self.root=root
        self.root.title("Client Application")
        self.client=Client()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Enter pseudonym or IP:")
        self.label.pack()

        self.ip_field = tk.Entry(self.root, width=30)
        self.ip_field.pack(pady=10)


        self.label = tk.Label(self.root, text="Enter Message:")
        self.label.pack()
        self.message_field = tk.Entry(self.root, width=30)
        self.message_field.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack()

    def submit(self):
        print(f"{self.ip_field.get(), self.message_field.get()}")

def main():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()