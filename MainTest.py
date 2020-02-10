# Author:        Johannes R. Falnes
# Created:       31/01/2020
import socket
import threading

HOST = '127.0.0.1'
PORT = 1337
BUFFER = 1024
clients = {}
addresses = {}


def incoming():
    """Handles incoming connection from clients"""
    while True:
        conn, addr = my_socket.accept()
        conn.send(bytes("What is your name?", 'utf8'))
        addresses[conn] = addr
        t3 = threading.Thread(target=handle, args=(conn,))
        t3.start()


def handle(conn):
    nick = conn.recv(BUFFER)
    clients[conn] = nick.decode('utf8')
    welcome_msg = ("{} just joined!".format(nick.decode('utf8')))
    broadcast(welcome_msg)
    while True:
        msg = conn.recv(BUFFER)
        if msg == "quit":
            del clients[conn]
            conn.close()
        else:
            full_msg = str(nick.decode('utf8')) + ": " + str(msg.decode('utf8'))

            broadcast(full_msg)


def broadcast(msg):
    """Go through each value in dict address"""

    for a in addresses:

        a.send(bytes(msg, 'utf8'))


def receive(conn):
    """Handles a client connection"""
    while True:
        receive_msg = conn.recv(BUFFER)
        print(receive_msg)


my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 / TCP

print(my_socket)
my_socket.bind((HOST, PORT))

my_socket.listen(5)

print("Listening...")

t1 = threading.Thread(target=incoming)
t1.start()
t1.join()
my_socket.close()