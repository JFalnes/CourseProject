from tkinter import *
from tkinter import messagebox
import socket
import logging
import threading

HOST = "127.0.0.1"
PORT = 60000
BUFFER = 1024
ADDR = (HOST, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def add_item():
    logging.info("Item added")
    a = codeVar.get()
    b = descVar.get()
    c = amountVar.get()
    abc = "{}:{}:{}".format(a, b, c)
    logging.info(abc + " sent to server")
    client_socket.send(bytes(abc, 'utf8'))
    messagebox.showinfo("Item Added", abc)




def conn_recv():
    b = client_socket.recv(BUFFER).decode('utf8')
    logging.info(b)


def exit_def():
    exit()


logFormat = "%(asctime)s: %(message)s"
logging.basicConfig(format=logFormat, level=logging.INFO,
                    datefmt="%H:%M:%S")


def tk_window():
    global codeVar
    global descVar
    global amountVar
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
    window.mainloop()


try:
    client_socket.connect(ADDR)

except ConnectionRefusedError:
    conn_ref = messagebox.showinfo("Connection Refused", "Connection Refused. Please try again.")
t3 = threading.Thread(target=conn_recv)
t3.start()
t4 = threading.Thread(target=tk_window)
t4.start()
