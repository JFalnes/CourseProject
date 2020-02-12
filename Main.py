import socket
import threading
import logging
import csv


class StockItem:
    def __init__(self, code, description, amount):
        self.code = code
        self.description = description
        self.amount = amount


class StockTracker(StockItem):
    def __init__(self, code, description, amount):
        super().__init__(code, description, amount)
        self.amount = amount


def write_item(code, desc, amount):
    in_list = [code, desc, amount]
    with open('stock.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(in_list)


def command_line():
    """Work in progress"""
    while True:
        print("What do you want to do?\n1.Add a stock item\n2.Update stock item\n3.Display details of item\n4.Display "
              "the entire stock list\n5.Exit")
        user_input = input("Please enter your selection: \n")
        if user_input == "1":
            print("Stock item added.")


HOST = "127.0.0.1"
PORT = 60000
BUFFER = 1024
addresses = {}

a = StockItem(1, 2, 3)
logFormat = "%(asctime)s: %(message)s"
logging.basicConfig(format=logFormat, level=logging.INFO,
                    datefmt="%H:%M:%S")


def incoming_connection():
    global addr
    while True:
        conn, addr = socket_serv.accept()
        addresses[conn] = addr
        logging.info(f'Connection established with {str(conn)}')
        conn.sendall(bytes(('Connection Established with ' + str(addr)), 'utf8'))
        thread_handle = threading.Thread(target=handle_conn, args=(conn,))
        thread_handle.start()


def csv_edit(coderecv):
    """manipulates stocks.csv depending on the buffer sent from the client"""
    r = csv.reader(open('stock.csv', ), delimiter=";")
    lines = list(r)
    if "@@updateitem?" in coderecv:
        y = coderecv.split("?")
        item = y[1]
        print(item)
        item.split(":")
        new_code = item[0]
        new_desc = item[1]
        new_amount = item[2]
        print(new_code, new_desc, new_amount)
        for line_number in range(len(lines)):
            csvList = lines[line_number]
            if csvList[0] == item:
                print(lines[line_number])

    elif "@@showstock:" in coderecv:
        y = coderecv.split(":")
        item = y[1]
        for line_number in range(len(lines)):
            csvList = lines[line_number]
            if csvList[0] == item:
                print(lines[line_number])
    else:
        x = coderecv.split(":")
        code = x[0]
        desc = x[1]
        amount = x[2]

        logging.info(str(addr) + " sent: " + coderecv)

        write_item(code, desc, amount)


def handle_conn(client):
    """Handles input from client to server"""

    while True:
        coderecv = client.recv(BUFFER).decode('utf8')
        csv_edit(coderecv)


socket_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 / TCP
socket_serv.bind((HOST, PORT))
socket_serv.listen(5)
logging.info("Waiting for connection...")

thread_cli = threading.Thread(target=command_line)
thread_cli.start()
thread_serv = threading.Thread(target=incoming_connection)
thread_serv.start()
thread_serv.join()
socket_serv.close()
