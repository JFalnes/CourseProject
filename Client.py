# IMPORT
from tkinter import *
from tkinter import messagebox
import socket
import logging
import threading

# VARIABLES
HOST = "127.0.0.1"
PORT = 20049
BUFFER = 1024
ADDR = (HOST, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# LOGGING
logFormat = "%(asctime)s: %(message)s"
logging.basicConfig(format=logFormat, level=logging.INFO,
                    datefmt="%H:%M:%S")


def conn_recv():
    """for receiving buffer from server"""
    client_recv = client_socket.recv(BUFFER).decode('utf8')
    logging.info(client_recv)


def exit_def():
    """exits the program when the exit button is pressed"""
    exit()


def add_item():
    """Send """
    # Get the text from the entry fields
    a = codeVar.get()
    b = descVar.get()
    c = amountVar.get()
    logging.info("Item added")

    # Concatenate the text from the entry fields into a single variable
    abc = "{}:{}:{}".format(a, b, c)
    logging.info(abc + " sent to server")

    # Send abc to server,
    client_socket.send(bytes(abc, 'utf8'))

    # Messagebox showing which items were added
    messagebox.showinfo("Item Added", abc)





def tk_window():
    """function that displays a tkinter gui"""
    # Global variables
    global codeVar
    global descVar
    global amountVar

    # Creates the window object, adds a title, sets the size of the window
    # and makes it non-resizable
    window = Tk()
    window.title("Add a stock item to the server")
    window.geometry("500x500")
    window.resizable(False, False)

    # define StringVars for the Entry-fields
    codeVar = StringVar()
    descVar = StringVar()
    amountVar = StringVar()

    # create entry-fields
    entry_code = Entry(window, textvar=codeVar)
    entry_desc = Entry(window, textvar=descVar)
    entry_amount = Entry(window, textvar=amountVar)

    # create labels, define what text they have
    label_code = Label(window, text="Code: ")
    label_desc = Label(window, text="Description: ")
    label_amount = Label(window, text="Amount: ")

    #create buttons,
    add_btn = Button(window, text="Add", relief="raised", command=add_item)
    exit_btn = Button(window, text="Exit", relief="raised", command=exit_def)

    # place all the previously created objects on a grid
    label_code.grid(row=0, column=0)
    label_desc.grid(row=1, column=0)
    label_amount.grid(row=2, column=0)
    entry_code.grid(row=0, column=1)
    entry_desc.grid(row=1, column=1)
    entry_amount.grid(row=2, column=1)
    add_btn.grid(row=3, column=1)
    exit_btn.grid(row=3, column=2)

    # put the window object in the mainloop
    window.mainloop()

# Try to connect to the server, expect a Connection Refused Error if the server is unavailable
try:
    client_socket.connect(ADDR)

except ConnectionRefusedError:
    conn_ref = messagebox.showinfo("Connection Refused", "Connection Refused. Please try again.")

# Starting threads for conn_recv and tk_window, letting the two functions run in parallell
t3 = threading.Thread(target=conn_recv)
t3.start()
t4 = threading.Thread(target=tk_window)
t4.start()
