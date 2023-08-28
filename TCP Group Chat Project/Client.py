# Imports
import socket
import threading

# Define constants
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5555  # The port used by the server
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT


def start_client():
    client_socket.connect(ADDR)  # Connecting to server's socket
    # creating a thread:
    thread = threading.Thread(target=receive)
    thread.start()

    while (True):
        # Get the client msg
        msg = input()
        client_socket.send(msg.encode(FORMAT))

def receive(): #Recieve message from server:
    while True:
        # Receive Message From Server
        msg = client_socket.recv(1024).decode(FORMAT)
        if msg:
            print(msg)

if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[CLIENT] Started running")
    start_client()
    print("Goodbye client:)")
