# Imports
import socket
import threading

# Define constants
import time

HOST = '127.0.0.1'  # Standard loopback IP address (localhost)
PORT = 5555  # Port to listen on (non-privileged ports are > 1023)
FORMAT = 'utf-8'  # Define the encoding format of messages from client-server
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT
group_id_counter = 1
clients_in_groups=[[]]
groups_id_list=[]
password_groups=[]

# Function that handles a single client connection
# Operates like an echo-server
def handle_client1(conn, addr):
    global group_id_counter
    global groups_id_list
    global password_groups
    global clients_in_groups

    print('[CLIENT CONNECTED] on address: ', addr)  # Printing connection address
    # total_messages = conn.recv(1024).decode(FORMAT)  # Receiving from client # of messages to expect
    # received = 0
    conn.send("Hello client, please choose an option: \n "
              "1. Connect to a group chat. \n 2. Create a group chat. \n "
              "3. Exit the server. \n ".encode(FORMAT))
    msg = conn.recv(1024).decode(FORMAT)
    if msg == "1":
        conn.send("Enter your name: \n".encode(FORMAT))
        name = conn.recv(1024).decode(FORMAT)
        # getting the group id:
        conn.send("Enter group ID: \n".encode(FORMAT))
        gro_id = conn.recv(1024).decode(FORMAT)
        while int(gro_id) not in list(groups_id_list):
            conn.send("There is no group id like this,try again".encode(FORMAT))
            conn.send("Enter group ID: \n".encode(FORMAT))
            gro_id = conn.recv(1024).decode(FORMAT)
        # here the group id is okay
        conn.send("Enter password: \n".encode(FORMAT))
        pass1 = conn.recv(1024).decode(FORMAT)
        while int(pass1) not in list(password_groups):
            conn.send("There is no group password like this,try again".encode(FORMAT))
            conn.send("Enter password: \n".encode(FORMAT))
            pass1 = conn.recv(1024).decode(FORMAT)
        # here the group id and the password is okay
        conn.send(("You’re connected to group chat #" + gro_id + "\n").encode(FORMAT))
        # adding the new client to the chat:
        clients_in_groups[int(gro_id) - 1].append(conn)
        # starting the conversation
        handle_conv(conn, gro_id, name)

    elif msg == "2":
        conn.send("Enter your name: \n".encode(FORMAT))
        name = conn.recv(1024).decode(FORMAT)

        conn.send("Enter password for the group: \n".encode(FORMAT))
        password = conn.recv(1024).decode(FORMAT)
        password_groups.append(int(password))

        the_group_id = group_id_counter
        group_id_counter += 1 # for the next group
        groups_id_list.append(int(the_group_id))

        conn.send(("The id of the group is:" + str(the_group_id) +
                   "\nYou’re connected to group chat #" + str(the_group_id) + "\n" +
                   "You can start to talk!").encode(FORMAT))
        # starting the conversation
        clients_in_groups[int(the_group_id) - 1].append(conn)
        handle_conv(conn, the_group_id, name)

    elif msg == "3":
        conn.send("Exit the chat \n".encode(FORMAT))
        print("[CLIENT DISCONNECTED]")
        conn.close()
        exit()
    else:
        conn.send("You chose an invalid option... \n".encode(FORMAT))

# Function that starts the conversation
def handle_conv(conn, gro_id, name):
    global group_id_counter
    global groups_id_list
    global password_groups
    global clients_in_groups
    time.sleep(0.1)
    for client in clients_in_groups:
        # Start Handling Thread For Client
        thread = threading.Thread(target=handle_msg, args=(conn, gro_id, name))  # Create a new thread to every Client on SERVER side
        thread.start()

# Function that handles the msg
def handle_msg(conn, gro_id, name):
    global group_id_counter
    global groups_id_list
    global password_groups
    global clients_in_groups
    while len(list(clients_in_groups[int(gro_id) - 1])) >= 1:
        msg = conn.recv(1024).decode(FORMAT)
        index = 0  # the index of the client in the group
        while (clients_in_groups[int(gro_id) - 1][int(index)] != conn):
            index += 1
        # checking the msg:
        if msg == "Exit":
            # we want to remove this client from the group
            clients_in_groups[int(gro_id) - 1][index] = -1# convert to some int
            clients_in_groups[int(gro_id) - 1].remove(-1)
            conn.send("You chose exit so you removed from the group. \n".encode(FORMAT))
            # printing a msg for everybody that the client has left:
            # print to the server:
            print(f'{name} has removed from the group: {gro_id} \n')
            # print to all the clients in the group:
            for client in list(clients_in_groups[int(gro_id) - 1]):
                if(client != conn):
                    client.send(f'{name} has removed from the group \n'.encode(FORMAT))
            print("[CLIENT DISCONNECTED]")
            conn.close()
            # checking if the group has 0 clients:
            if len(list(clients_in_groups[int(gro_id) - 1])) == 0:
                group_id_counter -= 1
                groups_id_list.remove(groups_id_list[int(gro_id) - 1])
                password_groups.remove(password_groups[int(gro_id) - 1])
                print(f'Group number: {gro_id} has deleted!\n')
            # closing the thread
            return
        # now we check if it's a regular msg:
        if msg != '':
            for client in list(clients_in_groups[int(gro_id) - 1]):
                if(client != conn):
                    client.send(f'{name}: {msg}'.encode(FORMAT))

# Function that starts the server
def start_server():
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(ADDR)  # binding socket with specified IP+PORT tuple
    print(f"[LISTENING] server is listening on {HOST}")
    server_socket.listen()  # Server is open for connections
    while True:
        connection, address = server_socket.accept()  # Waiting for client to connect to server (blocking call)
        thread = threading.Thread(target=handle_client1, args=(connection, address))  # Creating new Thread object.
        # Passing the handle func and full address to thread constructor
        thread.start()  # Starting the new thread (<=> handling new client)
    # when all end we want to close the server socket:
    server_socket.close()


# Main
if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())  # finding your current IP address
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening Server socket
    print("[STARTING] server is starting...")
    start_server()
    print("THE END!")

