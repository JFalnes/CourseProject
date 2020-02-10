from tkinter import *
from tkinter import messagebox
import socket
import threading

HOST = "127.0.0.1"
PORT = 60000
BUFFER = 1024
ADDR = (HOST, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def add_item():
    print("Item added")
    a = codeVar.get(), descVar.get(), amountVar.get()
    a = "test"
    messagebox.showinfo("Item Added", a)
    client_socket.send(bytes(a, "utf8"))


def conn_recv():
    b = client_socket.recv(BUFFER).decode('utf8')
    print(b)


def exit_def():
    exit()


window = Tk()
window.title("Add a stock item to the server")
window.geometry("250x150")
window.resizable(False, False)

codeVar = StringVar()
descVar = StringVar()
amountVar = StringVar()

entryCode = Entry(window, textvar=codeVar)
entryDesc = Entry(window, textvar=descVar)
entryAmount = Entry(window, textvar=amountVar)

labelCode = Label(window, text="Code: ")
labelDesc = Label(window, text="Description: ")
labelAmount = Label(window, text="Amount: ")
addBtn = Button(window, text="Add", relief="raised", command=add_item)
exitBtn = Button(window, text="Exit", relief="raised", command=exit_def)

labelCode.grid(row=0, column=0)
labelDesc.grid(row=1, column=0)
labelAmount.grid(row=2, column=0)
entryCode.grid(row=0, column=1)
entryDesc.grid(row=1, column=1)
entryAmount.grid(row=2, column=1)

addBtn.grid(row=3, column=1)
exitBtn.grid(row=3, column=2)

try:
    client_socket.connect(ADDR)
except ConnectionRefusedError:
    print("Connection refused")

window.mainloop()
