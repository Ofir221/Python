## Assignment 1
# Course: Server side
# Client side: client.py
# Submitters: Ofir Nahshoni 204616718, Ori Tsemach 205927775
#
## Description:
# Client Server system (one Client) 2 directional communication, using TCP (Transfer Control Protocol).
# This system can open 3 different types of servers:
# 1) Server that handles a single Client, but can reply to infinite number of requests, send the string exit.
# 2) Server that handles multiple Clients (at the same time) and can reply to infinite number of requests.
#    Each new Client that succeeded to connect to this Server (port number 5050 - free use port), would be handled
#    by different thread.
# 3) Server that handles a single Client and a single HTTP request. 
#    HTTP actually is used to get the translation of the string address of the Web, specified in the browser.
#    The local DNS is responsible to do this action.


## Libraries
import socket
import sys
import threading


## Main function
if __name__ == '__main__':
    # Error in command typing run command at the Terminal
    if len(sys.argv) != 3:
            print('Error! call client.py with <IP_ADDRESS> <PORT#>')
            exit(-1)

    # Initiate the communication with the Server using socket
    else:
        BUFFER_SIZE = 1024  # Size of the buffer that reads the massages sent through the socket
        # The arguments specified in the terminal (invoke Server)
        SERVER_IP = sys.argv[1]  # Local IP address given by the router of LAN (WiFi)
        SERVER_PORT = int(sys.argv[2])
        ADDR = (SERVER_IP, SERVER_PORT)
        DIS_CONN_MSG = "exit"  # Massage to disconnect the socket - send also to the Server

        ## Create the socket
        client = socket.socket()
        print(f"Client created a socket to: addr={SERVER_IP} port={SERVER_PORT}.")

        ## Connect to socket
        client.connect(ADDR)
        print("Client connected to Server")
        
        # Send infinite number of requests to Server, until Client entered exit (to disconnect)
        msg = " "
        print("Hello new Client :)")
        if SERVER_PORT == 5050:
            while msg:
                userInput = input("Enter string string (enter exit for end for disconnect): ")
                client.sendall(userInput.encode())
                # Exit loop if Client entered exit to disconnect
                if userInput == DIS_CONN_MSG:
                    break
                msg = client.recv(BUFFER_SIZE).decode()
                print(f"Client read from Server: {msg}")
        
        # Send single HTTP request and get the answer from the Server
        # HTTP is used for converting string URL to numeric - answer from Local DNS
        elif SERVER_PORT == 80:
            msg = client.recv(BUFFER_SIZE).decode()
            print(f"Client read from Server: {msg}")
        else:
            print("Wrong Port number, initiate process again please.")

    ## End of program - main process of Client shut down
    client.close()
    print("Client finished")