import socket
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox as mb
import threading

class client:
    def __init__(self, master):
        self.master = master
        self.master.title("الاتصال بالخادم")
        self.master.geometry("400x350+650+200")
        self.master.resizable(False, False)
        self.master.config(bg="#0B192C")
        self.master.columnconfigure(0, weight=1)

        header = tk.Label(master, text=" تطبيق دردشة ", bg="#0B192C", font=('thesans', 24), fg="#FF4C29")
        header.grid(row=0, column=0, padx=10, pady=10)

        username_label = tk.Label(master, text="اسم المستخدم", bg="#0B192C", fg="#41B06E", font=('thesans', 18))
        username_label.grid(row=1, column=0, padx=10, pady=10)

        self.master.username_var = tk.StringVar()
        username_entry = tk.Entry(master, textvariable=self.master.username_var, font=('thesans', 18))
        username_entry.grid(row=2, column=0)

        server_label = tk.Label(master, text="عنوان الخادم", bg="#0B192C", fg="#41B06E", font=('thesans', 18))
        server_label.grid(row=3, column=0)

        self.master.server_var = tk.StringVar()
        # self.master.server_var.set("172.20.10.3")
        server_entry = tk.Entry(master, textvariable=self.master.server_var, font=('thesans', 18))
        server_entry.grid(row=4, column=0)

        port_label = tk.Label(master, text="المنفذ", bg="#0B192C", fg="#41B06E", font=('thesans', 18))
        port_label.grid(row=5, column=0)

        self.master.port_var = tk.StringVar()
        self.master.port_var.set("8080")
        port_entry = tk.Entry(master, textvariable=self.master.port_var, font=('thesans', 18))
        port_entry.grid(row=6, column=0)

        self.master.connect_btn = tk.Button(master, command=self.connect, text="اتصال", font=('thesans', 18), fg="#fff", bg="#FF4C29", bd=0)
        self.master.connect_btn.grid(row=7, column=0, padx=10, pady=10)

    def connect(self):
        username = self.master.username_var.get()
        host = self.master.server_var.get()
        port = int(self.master.port_var.get())

        if not host or not port or not username:
            mb.showerror("خطأ", "رجاء قم بادخال اسمك و عنوان الخادم والمنفذ")
        else:
            try:
                self.master.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.master.client_socket.connect((host, port))
                self.master.client_socket.send(username.encode("utf-8"))
                self.message_window()
                receive_thread = threading.Thread(target=self.client_receive)
                receive_thread.start()
            except Exception as error:
                mb.showwarning("خطأ", error)

    def client_receive(self):
        while True:
            try:
                message = self.master.client_socket.recv(2048).decode('utf-8')
                if message:
                    self.master.message_text_box.config(state='normal')
                    self.master.message_text_box.insert("end", message + "\n")
                    self.master.message_text_box.config(state='disabled')
                    self.master.message_text_box.see("end")

            except:
                self.master.client_socket.close()
                break

    def client_send(self):
        if not self.master.client_message_var.get():
            mb.showerror("خطأ", "يرجى كتابة الرسالة")
            return
        message = f"{self.master.username_var.get()}: {self.master.client_message_var.get()}"
        self.master.client_socket.send(message.encode("utf-8"))
        self.master.client_message_var.set("")

    def message_window(self):
        self.master.withdraw()
        message_window = ctk.CTkToplevel()
        message_window.title("غرفة الدردشة")
        message_window.geometry("450x450+600+100")
        message_window.resizable(False, False)
        message_window.config(bg="#0B192C")
        message_window.columnconfigure(0, weight=1)

        header = tk.Label(message_window, text=" غرفة دردشة ", bg="#0B192C", font=('thesans', 24), fg="#FF4C29")
        header.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        user = tk.Label(message_window, text=f" Username: {self.master.username_var.get()}", bg="#0B192C", fg="#41B06E", font=('thesans', 18))
        user.grid(row=1, column=0, padx=10, pady=10, columnspan=2)


        self.master.message_text_box = tk.Text(message_window, fg="#000", font=('thesans', 18), height=10, state="disabled")
        self.master.message_text_box.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        self.master.client_message_var = tk.StringVar()
        self.master.client_message_entry = tk.Entry(message_window, width=20, textvariable=self.master.client_message_var, font=('thesans', 18))
        self.master.client_message_entry.grid(row=5, column=0, padx=10, pady=10)

        send_btn = tk.Button(message_window, command=self.client_send, text="ارسال", width=15, font=('thesans', 16), fg="#fff", bg="#FF4C29", bd=0)
        send_btn.grid(row=5, column=1, padx=10, pady=10)

if __name__ == "__main__":
    ctk.set_appearance_mode('dark')
    window = ctk.CTk()
    window.iconbitmap("icon.ico")
    client = client(window)
    window.mainloop()
