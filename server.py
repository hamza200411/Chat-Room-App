import socket
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox as mb
import threading

class Server:
    def __init__(self, master):
        self.master = master
        self.master.title("الخادم")
        self.master.geometry("450x450+600+120")
        self.master.resizable(False, False)
        self.master.config(bg="#0B192C")
        self.master.columnconfigure((0, 1), weight=1)
        # self.master.rowconfigure(0, weight=1)
        self.master.host = socket.gethostbyname(socket.gethostname())
        self.master.clients = []
        self.master.usernames = []

        header = tk.Label(master, text="خادم الدردشة ", bg="#0B192C", font=('thesans', 24), fg="#FF4C29")
        header.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        server_label = tk.Label(master, text="عنوان الخادم", bg="#0B192C", fg="#41B06E", font=('thesans', 16))
        server_label.grid(row=1, column=0)

        self.master.server_var = tk.StringVar()
        self.master.server_var.set(self.master.host)
        server_entry = tk.Entry(master, state="disabled", textvariable=self.master.server_var, font=('thesans', 16))
        server_entry.grid(row=2, column=0)

        port_label = tk.Label(master, text="المنفذ", bg="#0B192C", fg="#41B06E", font=('thesans', 16))
        port_label.grid(row=1, column=1)

        self.master.port_var = tk.StringVar()
        self.master.port_var.set(8080)
        port_entry = tk.Entry(master, textvariable=self.master.port_var, font=('thesans', 16))
        port_entry.grid(row=2, column=1)

        self.master.server_start_btn = tk.Button(master, text="تشغيل الخادم", width=15,  font=('thesans', 16), fg="#fff", bg="#FF4C29", bd=0)
        self.master.server_start_btn.grid(row=3, column=0, padx=10, pady=10)
        self.master.server_start_btn.config(command=self.start_server)

        self.master.clients_btn = tk.Button(master, text="عرض المتصلين", width=15, font=('thesans', 16), fg="#fff", bg="#FF4C29", bd=0)
        self.master.clients_btn.grid(row=3, column=1, padx=10, pady=10)
        self.master.clients_btn.config(command=self.connected_client)

        self.master.message_text_box = tk.Text(master, fg="#000", font=('thesans', 18), height=10, state="disabled")
        self.master.message_text_box.grid(row=4, column=0, padx=10, pady=10, columnspan=2)


    def connected_client(self):
            mb.showinfo("clients", self.master.usernames)

    def broadcast(self, message):
        for client in self.master.clients:
            client.send(message)

    def handle_client(self, client):
        clients = self.master.clients
        usernames = self.master.usernames
        while True:
            try:
                message = client.recv(2048)
                self.broadcast(message)

            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                username = usernames[index]
                self.broadcast(f"{username} غادر الدردشة ".encode("utf-8"))
                usernames.remove(username)
                break

    def start_server(self):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()

    def run_server(self):
        usernames = self.master.usernames
        clients = self.master.clients
        port = int(self.master.port_var.get())
        if not port:
            mb.showwarning("خطأ", "يجب ادخال المنفذ")
            return

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.master.host, port))
        server_socket.listen()
        mb.showinfo("تم", "تم تشغيل الخادم بنجاح")
        while True:
                client, addr = server_socket.accept()
                username = client.recv(1024).decode("utf-8")
                usernames.append(username)
                clients.append(client)

                self.broadcast(f"{username} اتصل بالمحادثة ".encode("utf-8"))
                self.master.message_text_box.config(state='normal')
                self.master.message_text_box.insert("end", f"{username} اتصل بالمحادثة " + "\n")
                self.master.message_text_box.config(state='disabled')
                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.start()

if __name__ == "__main__":
    ctk.set_appearance_mode('dark')
    window = ctk.CTk()
    window.iconbitmap('icon.ico')
    server = Server(window)
    window.mainloop()
