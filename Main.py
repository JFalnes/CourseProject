import socket
import threading
import logging
import struct

class StockItem:
    def __init__(self, code, description, amount):
        self.code = code
        self.description = description
        self.amount = amount

    def return_item(self):
        self.itemDesc = "{}, {}, {}".format(self.code, self.description, self.amount)



class StockTracker(StockItem):
    def __init__(self,  code, description, amount):
        super().__init__(code, description, amount)
        self.amount = amount


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
        conn, addr = serv_socket.accept()
        addresses[conn] = addr
        logging.info(f'Connection established with {str(conn)}')
        conn.sendall(bytes(('Connection Established with ' + str(addr)),  'utf8'))
        t3 = threading.Thread(target=handle_conn, args=(conn,))
        t3.start()


def handle_conn(client):
    while True:
        coderecv = client.recv(BUFFER).decode('utf8')
        x = coderecv.split(":")
        code = x[0]
        desc = x[1]
        amount = x[2]
        print(code, desc, amount)

        logging.info(str(addr) + " sent: " + code, desc, amount)
        with open('sample.txt', 'a+') as file:
            file.write(coderecv)
            file.write('\n')


serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 / TCP
serv_socket.bind((HOST, PORT))
serv_socket.listen(5)
logging.info("Waiting for connection...")

serv_thread = threading.Thread(target=incoming_connection)
serv_thread.start()
serv_thread.join()
serv_socket.close()
