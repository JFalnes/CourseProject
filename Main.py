import socket
import threading


class StockItem:
    def __init__(self, code, description, amount):
        self.code = code
        self.description = description
        self.amount = amount
        self.itemDesc = "{}, {}, {}".format(self.code, self.description, self.amount)

    def return_item(self):
        pass


class StockTracker(StockItem):
    def __init__(self,  code, description, amount):
        super().__init__(code, description, amount)
        self.amount = amount


HOST = "127.0.0.1"
PORT = 60000
BUFFER = 1024
addresses = {}


a = StockItem(1, 2, 3)
a.return_item()
print(a.itemDesc)


def incoming_connection():
    while True:
        conn, addr = serv_socket.accept()
        addresses[conn] = addr
        print("Connection established", conn)
        t3 = threading.Thread(target=handle_conn, args=(conn,))


def handle_conn(client):
    while True:
        a = client.recv(BUFFER).decode('utf8')
        print(a.decode('utf8'))
        client.send(a, 'utf8')


serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 / TCP
print(serv_socket)
serv_socket.bind((HOST, PORT))
serv_socket.listen(5)
print("Waiting for connection...")

serv_thread = threading.Thread(target=incoming_connection)
serv_thread.start()
serv_thread.join()
serv_socket.close()