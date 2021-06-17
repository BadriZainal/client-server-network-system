import os
import sys
import socket
import pickle

# get the ip address of the computer
SERVER = socket.gethostbyname(socket.gethostname())

# declaration of the port number,address for the connection, byte format and header
PORT = 9999
HEADER = 10000
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# declaration of the variable to control the cursor movement on console, and erase line
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

# create socket for the server and client communication path, and connect the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


# function block to delete multiple lines on the cmd display for client interface
def delete_multiple_lines(line_amount_up):
    for t in range(line_amount_up):   # loop to delete multiple lines based on the function input
        sys.stdout.write(CURSOR_UP_ONE)  # to move up a cursor
        sys.stdout.write(ERASE_LINE)     # to erase a line


# function block to send the message to the server with compliance to the stream protocol
def send(msg):
    message = msg
    msg_length = len(message)  # check the length of the message
    send_length = str(msg_length).encode(FORMAT)  # change the datatype of the message length to string
    send_length += b'' * (HEADER - len(send_length))  # padded the message to make its length == HEADER
    client.send(send_length)  # send the data of the message length to the server
    client.send(message)  # send the message to the server


def request_input():
    global result, delete_check  # declare these variables globally
    connection = True  # the switch for the connection
    delete_line = 1  # switch for the delete line if statement later
    dc = 0   # switch for print previous result and inputs in the if statement later
    while connection:  # loop for the client-server connection
        values = input(" \n Input two comma separated numbers : ")  # request float input from user
        list1 = values.split(",")  # separate both numbers
        tuple1 = tuple(list1)  # transform list into tuple of the floats
        if len(tuple1) == 2:  # check the length of the tuple, allow if it is only 2 numbers
            lowercase1 = tuple1[0].replace('.', '')  # remove any '.'' in the number if presence
            lowercase2 = tuple1[1].replace('.', '')  # remove any '.' in the number if presence
            contain_letter1 = lowercase1.isdecimal()  # apply the isdecimal Boolean to each tuple's elements
            contain_letter2 = lowercase2.isdecimal()  # apply the isdecimal Boolean to each tuple's elements
            if not contain_letter1 or not contain_letter2:  # to allow only number pass this line
                # request input to decide either to try again or disconnect
                c = input(" The input were not numbers, enter Y to try again or N to disconnect :")
                delete_check = False  # switch to not display the previous inputs and result
                if c == 'N' or c == 'n':  # if statement to disconnect the client
                    dc = 0
                    print("\n You are disconnected.")  # print out the connection status
                    connection = False   # switch for the client-server connection loop
                    send(DISCONNECT_MESSAGE.encode(FORMAT))
                elif c == 'Y' or c == 'y':   # if statement to return the client to the initial phase of the basecalling
                    dc = 1
                    pass  # to bypass the if-else statement
                else:   # if statement to disconnect the client for invalid input
                    dc = 0
                    print("\n Invalid input and you are disconnected.")  # print out the connection status
                    connection = False   # switch for the client-server connection loop
                    send(DISCONNECT_MESSAGE.encode(FORMAT))  # send the disconnection message
            else:
                delete_check = True  # switch to display the previous inputs and result
                mesej = pickle.dumps(tuple1)  # serialize the tuple input by the user
                send(mesej)  # send the tuple to the server to be further processed
                feedback = client.recv(9999)  # received result from the server
                if feedback == ("No base".encode(FORMAT)):  # if statement for the tuple without base
                    result = str(" The floats do not have a base.")
                    print(result)
                else:   # if statement for the tuple with base
                    tuple_with_base = pickle.loads(feedback)   # deserialize the tuple from the server
                    result = str(f" The floats have a base and it is denoted in this tuple : {tuple_with_base}.")
                    print(result)  # print out the result of the basecalling
        else:
            # request input to decide either to try again or disconnect
            b = input(" The input were not exactly two numbers, enter Y to try again or N to disconnect :")
            delete_check = False   # switch to not display the previous inputs and result
            if b == 'N' or b == 'n':   # if statement to disconnect the client
                dc = 0
                print("\n You are disconnected.")  # print out the connection status
                connection = False   # switch for the client-server connection loop
                send(DISCONNECT_MESSAGE.encode(FORMAT))
            elif b == 'Y' or b == 'y':  # if statement to return the client to the initial phase of the basecalling
                dc = 1
                pass  # to bypass the if-else statement
            else:   # if statement to disconnect the client for invalid input
                dc = 0
                print("\n Invalid input and you are disconnected.")  # print out the connection status
                connection = False   # switch for the client-server connection loop
                send(DISCONNECT_MESSAGE.encode(FORMAT))   # send the disconnection message

        delete_line += 1  # counter for deleting the line for client interface
        if delete_line >= 3:  # if statement to delete previous display and rewrite the new line
            if delete_check:  # if statement for valid previous input
                delete_multiple_lines(5)  # erase the previous line to prevent repetitive output on cmd
                print(f" The previous input numbers are : {tuple1[0]},{tuple1[1]}")  # display previous inputs
                print(" Result:" + result)  # display previous result

            elif dc == 1:    # if statement for invalid previous input
                delete_multiple_lines(6)  # erase the previous line to prevent repetitive output on cmd
                print("\n The previous input were not valid.")  # display previous inputs
                print(" Result: Invalid inputs will not give any result")  # display previous result


os.system('cls')  # clear the cmd before start the client-server connection
print("\n You are connected to the Basecalling Finder server!")  # display this right after client connected
print("\n\n INSTRUCTION: "
      "\n Insert two floats at a time and the base will be displayed if it exists."
      "\n If nothing is displayed, then the base does not exist between the floats.")
a = input("\n Input Y to continue or N to disconnect : ")
delete_multiple_lines(2)   # delete the unwanted line after request the input above
if a == 'N' or a == 'n':  # if statement when user want to disconnect
    print(" \n You are disconnected.")
    send(DISCONNECT_MESSAGE.encode(FORMAT))
elif a == 'Y' or a == 'y':  # if statement when user want to try again
    request_input()   # process the whole input and sending data stream to the server
else:    # if statement when user inset invalid input
    print("\n Invalid input and you are disconnected.")
    send(DISCONNECT_MESSAGE.encode(FORMAT))  # send disconect message to server for disconnection