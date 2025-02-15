#! /usr/bin/env python
# IMPORTS
import socket
import threading
import logging
import json

# VARIABLES
HOST = '127.0.0.1'
PORT = 20049
BUFFER = 1024
addresses = {}

# LOGGING
logFormat = '%(asctime)s: %(message)s'
logging.basicConfig(format=logFormat, level=logging.INFO,
                    datefmt="%H:%M:%S")


# class StockItem holds all the variables which are used by StockTracker
class StockItem:
    def __init__(self, code, desc, amount, old_value, new_value, choose_item):
        self.code = code
        self.desc = desc
        self.amount = amount
        self.old_value = old_value
        self.new_value = new_value
        self.choose_item = choose_item

    def __str__(self):
        return 'This is an overridden built-in python function'


# class StockTracker derives from class StockItem
class StockTracker(StockItem):
    def __init__(self, code, desc, amount, old_value, new_value, choose_item):
        super().__init__(code, desc, amount, old_value, new_value, choose_item)

    # overridden built-in python function
    def __repr__(self):
        return 'This is an overridden built-in python function'

    def write_item(self):
        """Write items to data_file.json, takes three parameters (code, desc, amount)
        for appending a new row for stock item in data_file.json"""

        # save the users input in a dictionary inside a dictionary
        # the key in the first dictionary is the item-code, the values are the description
        # and amount

        json_data = {self.code: {
                         "desc": self.desc,
                         "amount": self.amount}
        }

        # opens data_file.json for append + binary + update
        with open('data_file.json', 'ab+') as json_f:
            # Go to the end of file
            json_f.seek(0, 2)
            # Check if file is empty
            if json_f.tell() == 0:
                # If empty, write an array
                json_f.write(json.dumps([json_data], indent=2).encode())
            else:
                json_f.seek(-1, 2)
                # Remove the last character, open the array
                json_f.truncate()
                # separate json objects
                json_f.write(' , '.encode())
                # dump dictionary to json_data
                json_f.write(json.dumps(json_data, indent=2).encode())
                json_f.write(']'.encode())

    def update_item(self):
        # First, read in the file and convert JSON -> python objects
        with open('data_file.json', 'r') as f:
            json_file = json.load(f)
        # Check to see if self.code is in data_file, if it is then replace the "amount" keys value to be the new_value
        for each_dict in json_file:
            if self.code in each_dict:
                each_dict[self.code]['amount'] = self.new_value

        # Write out data by converting objects -> JSON and
        # writing it to disk
        with open('data_file.json', 'w') as f:
            json.dump(json_file, f, indent=2)

    def show_item(self):
        # Reads file and converts to JSON
        with open('data_file.json', 'r') as f:
            json_file = json.load(f)
            # Scans each dictionary in json_file
            for each_dict in json_file:
                # Scans each dictionary in each_dict
                for k, v in each_dict.items():
                    # If the key == user input, print the key and value pair
                    if k == self.choose_item:
                        print(k, v)

    def show_stock(self):
        """show key, value in datafile.json"""
        with open('data_file.json', 'r') as f:
            json_data = json.load(f)
            for each_dict in json_data:
                print(each_dict)


def command_line():
    """chooses what methods to use depending on user input"""
    # create StockTracker object
    tracker = StockTracker(1, 2, 3, 4, 5, 6)

    # set run_cli to true
    run_cli = True
    # while run_cli = true, run the CLI
    while run_cli:
        # display options to user
        print('What do you want to do?\n1.Add a stock item\n2.Update stock item\n3.Display details of item\n4.Display '
              'the entire stock list\n5.Exit')
        # ask user for input
        user_input = input('Please enter your selection: \n')
        if user_input == '1':
            # variables for code, desc and amount
            code_input = input('Item Code: ')
            desc_input = input('Item Description: ')
            amount_input = input('Item Amount: ')
            # create new StockTracker object and start method
            add_tracker = StockTracker(code_input, desc_input, amount_input, 4, 5, 6)
            add_tracker.write_item()
            # assure the user the stock has been added
            print('\n{} | {} | {}| \nItem added to stock!\n'.format(code_input, desc_input, amount_input))

        elif user_input == '2':
            # code of item to change
            code = input('Input code of the item: ')
            # new amount, replaces the old one
            new_value = input('Input the new stock amount:' )
            # new StockTracker object
            change_tracker = StockTracker(code, 2, 3, 4, new_value, 4)
            change_tracker.update_item()
            print(code, ' changed the stock on hand to ', new_value)

        elif user_input == '3':
            # ask user which item to display
            choose_item = input('Enter code for the item you want to check: ')
            # display selcted item
            track_item = StockTracker(1, 2, 3, 4, 5, choose_item)
            track_item.show_item()
        elif user_input == '4':
            # show entire stock
            tracker.show_stock()
        elif user_input == '5':
            # set run_cli to false and exit
            print('Exiting...')
            run_cli = False


def incoming_connection():
    """Function for handling incoming connections from a client starts a new thread for function handle_conn"""
    # GLOBAL VARIABLES
    global addr
    global conn
    # While loop
    while True:
        # client
        conn, addr = socket_serv.accept()
        # add address to list
        addresses[conn] = addr
        # when a client connects, display a log msg with IP of client
        logging.info(f'Connection established with {str(addr)}')
        # send message to all clients when client connects
        conn.sendall(bytes(('Connection Established with ' + str(addr)), 'utf8'))
        # start handle_conn in a thread, pass the argument conn
        thread_handle = threading.Thread(target=handle_conn, args=(conn,))
        # start the thread
        thread_handle.start()


def handle_conn(client):
    """Handles input from client to server, takes 1 parameter (client) for receiving BUFFER,
    after buffer is received it initializes json_add function"""
    while True:
        coderecv = client.recv(BUFFER).decode('utf8')
        json_add(coderecv)


def json_add(coderecv):
        x = coderecv.split(':')
        code = x[0]
        desc = x[1]
        amount = x[2]
        logging.info(str(addr) + ' sent: ' + coderecv)

        a = StockTracker(code, desc, amount, 1, 2, 3)
        a.write_item()


socket_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 / TCP
socket_serv.bind((HOST, PORT))
socket_serv.listen(5)
logging.info('Waiting for connection...')

thread_cli = threading.Thread(target=command_line)
thread_cli.daemon = True
thread_cli.start()
thread_serv = threading.Thread(target=incoming_connection)
thread_serv.start()
thread_serv.join()
socket_serv.close()
