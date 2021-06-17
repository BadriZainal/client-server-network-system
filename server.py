import os
import socket
import pickle
import threading

# get the ip address of the computer
SERVER = socket.gethostbyname(socket.gethostname())

# declaration of the port number,address for the connection, byte format and header
PORT = 9999
HEADER = 10000
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# create socket for the server and client communication path, and bind the address
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


# function block to handle the client connection
def handle_client(conn, addr):
    print(f"\n \n[NEW CONNECTION] {addr} connected.")
    count = 1
    connected = True
    while connected:
        msg_length = conn.recv(HEADER)  # blocking command for the stream protocol,cannot exceed the HEADER bytes
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)  # receive the message from client
            if msg == DISCONNECT_MESSAGE.encode(FORMAT):  # check if receive disconnect message
                connected = False  # to break the loop and stop connection
                msg = msg.decode(FORMAT)  # decode the data without deserialized it
                print(f"\nConnection from {addr} is {msg}")  # notify the disconnection

            if isinstance(msg, bytes):    # check if the data is still in byte type
                tuple1 = pickle.loads(msg)  # deserialize the tuple sent from the client
                print(f"\nINPUT {count} from Client {addr}")  # print the source of the data
                count += 1
                print(f"The input floats are {tuple1} in tuple form")  # print the tuple data
                diff1 = float(tuple1[0]) - float(tuple1[1])  # calculate the differences between both floats (diff1)
                diff2 = float(tuple1[1]) - float(tuple1[0])  # same process but float2-float1 (diff2)
                base = {'A': 329.0525, 'C': 305.0413, 'G': 345.0474, 'U': 306.0253}  # list the given dictionary
                keys = base.keys()
                base_check = True

                for key in keys:   # loop for checking any presence of the base
                    if abs(diff1-base[key]) <= 1E-6:  # calculate the approximate equality between the data and diff1
                        base_send1 = key
                        tuple_with_base1 = (tuple1[0], tuple1[1], base_send1)  # create new tuple that include the base
                        base_check = False
                        print(f"The base exists for this tuple and it is {base_send1}.")  # print the base and new tuple
                        print(f"The tuple form to be sent to the client is {tuple_with_base1}.")
                        found_base1 = pickle.dumps(tuple_with_base1)  # serialized the tuple to be sent to client
                        conn.send(found_base1)  # send the pickled tuple to the client

                    if abs(diff2-base[key]) <= 1E-6:  # repeat the same case like above but for diff2
                        base_send2 = key
                        tuple_with_base2 = (tuple1[1], tuple1[0], base_send2)
                        base_check = False
                        print(f"The base exists for this tuple and it is {base_send2}.")
                        print(f"The tuple form to be sent to the client is {tuple_with_base2}.")
                        found_base2 = pickle.dumps(tuple_with_base2)
                        conn.send(found_base2)

                if base_check:  # if statement for the tuple does not have base
                    print(f"This tuple does not have any base")
                    conn.send("No base".encode(FORMAT))  # inform the client the absence of the base
    conn.close()  # to close the connection


# function block to start the server and allow multiple client client access server at once
def start():
    server.listen()  # server ready to be connected
    print(f"[LISTENING] Server is listening on {SERVER}")  # display server startup status
    while True:
       conn, addr = server.accept()  # server ready to accept connection
       thread = threading.Thread(target=handle_client, args=(conn, addr))  # allow threading for multiple client at once
       thread.start()
       print(f"\n[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")  # display server startup status
       print(f"\n[WAITING INPUT FROM CLIENT] The inputs and their base will be listed below...")


os.system('cls')  # clear the cmd display before starting the server
print(f"[STARTING] Server is starting on the local host {PORT}...")  # display server startup status

start()

