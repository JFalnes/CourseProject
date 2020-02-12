import socket
import threading
import logging
import csv

HOST = "127.0.0.1"
PORT = 60000
BUFFER = 1024
addresses = {}
logFormat = "%(asctime)s: %(message)s"

logging.basicConfig(format=logFormat, level=logging.INFO,
                    datefmt="%H:%M:%S")


class StockTracker:
    def __init__(self, code, desc, amount):
        self.code = code
        self.desc = desc
        self.amount = amount

    def write_item(self, code, desc, amount):
        """Write items to stock.csv"""
        in_list = [self.code, self.desc, self.amount]
        with open('stock.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(in_list)

    def update_item(self, old_value, new_value):
        self.old_value = old_value
        self.new_value = new_value
        with open('stock.csv', 'a+', newline='') as csv_file:
            for row in csv_file:
                return row
        text = open("stock.csv", 'r')
        text = "".join([i for i in text]).replace(self.old_value, self.new_value)
        p = open('stock.csv', 'w')
        p.writelines(text)

    def show_item(self, choose_item):
        self.choose_item = choose_item
        with open('stock.csv', 'r', newline='') as csv_file:
            for row in csv_file.readlines():
                if self.choose_item in row:
                    return row

    def show_stock(self):
        """WIP"""
        with open('stock.csv', 'r', newline='') as csv_file:
            for row in csv_file.readlines():
                print(row.strip().replace(";", " "))


class StockItem(StockTracker):
    def __init__(self, code, description, amount):
        super().__init__(code, description, amount)



def command_line():
    run_cli = True
    tracker = StockTracker(1, 2, 3)

    while run_cli:
        print("What do you want to do?\n1.Add a stock item\n2.Update stock item\n3.Display details of item\n4.Display "
              "the entire stock list\n5.Exit")
        user_input = input("Please enter your selection: \n")
        if user_input == "1":
            code_input = input("Item Code: ")
            desc_input = input("Item Description: ")
            amount_input = input("Item Amount: ")
            tracker.write_item(code_input, desc_input, amount_input)
            print("\n{} | {} | {}| \nItem added to stock!\n".format(code_input,desc_input,amount_input))

        elif user_input == "2":
            old_value = input("Input the value you want to change: ")
            new_value = input("Input the new value: ")
            tracker.update_item(old_value, new_value)
            print(old_value, " changed to ", new_value)

        elif user_input == "3":
            choose_item = input("Enter code for the item you want to check: ")

            tracker.show_item(choose_item)
        elif user_input == "4":
            tracker.show_stock()
        elif user_input == "5":
            print("Exiting...")
            run_cli = False


def incoming_connection():
    global addr
    while True:
        conn, addr = socket_serv.accept()
        addresses[conn] = addr
        logging.info(f'Connection established with {str(addr)}')
        conn.sendall(bytes(('Connection Established with ' + str(addr)), 'utf8'))
        thread_handle = threading.Thread(target=handle_conn, args=(conn,))
        thread_handle.start()


def handle_conn(client):
    """Handles input from client to server"""
    while True:
        coderecv = client.recv(BUFFER).decode('utf8')
        csv_edit(coderecv)


def csv_edit(coderecv):
        x = coderecv.split(":")
        code = x[0]
        desc = x[1]
        amount = x[2]
        print(code)
        print(desc)
        print(amount)
        logging.info(str(addr) + " sent: " + coderecv)

        a = StockItem(code, desc, amount)
        a.write_item(code, desc, amount)


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
