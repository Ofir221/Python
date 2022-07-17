## Assignment 1
# Course: Server side
# Server side: server.py
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
import threading
import time
import string
import random
import sys


## Class of object Server
class Server:
    ## Constructor - defined by two given arguments ('self' is like 'this' in Java)  
    def __init__(self, ip, port):
        self.__SERVER_PORT = int(port)  # Cast the port number from string to integer
        self.__SERVER_IP = ip  # Local IP address given by router (string)
        self.__ADDR = (self.__SERVER_IP, self.__SERVER_PORT)
        self.BUFFER_SIZE = 1024
        self.__DIS_CONN_MSG = "exit"
        self.__clients_count = 0

        ## Create the socket
        self.server = socket.socket()

        # Binding the socket server to the right address and port
        self.server.bind(self.__ADDR)
        self.server.listen()
        print("[LISTENING] Server started listening...")

    ## Function that receive massage from Client and send back upper case string to Client
    def sequential(self, conn, addr):
        print("[CONNECTED] Server connected to Client")
        connected = True
        msg = ' '

        # Assigns unique id the each Client after connection was made
        client_id = "".join([random.choice(string.ascii_letters + string.digits) for n in range(8)])

        # Get massage from Client
        while connected and msg:
            msg = conn.recv(self.BUFFER_SIZE)
            msg = msg.decode()
            print(f"[Reading] Server read: \n[Client-{client_id}] {msg}")
            if msg == self.__DIS_CONN_MSG:
                connected = False

            # Send massage back to Client
            msg = msg.upper()
            conn.sendall(msg.encode())
            print(f"[WRITING] Server sent to Client: {msg}")

        # Close connection with current Client
        conn.close()
        print("[DISCONNECT] Client disconnected")

        # Update amount of Clients after the current Client has disconnected
        if self.__clients_count > 0:
            self.__clients_count  = self.__clients_count - 1
            print(f"[ACTIVE CONNECTIONS] There are {self.__clients_count} Clients connected at this moment")

    ##  Deals the accept attribute of socket 
    def accept(self):
        return self.server.accept()

    ## Setter to manage properly the amount of Clients at a moment
    def set_amount_of_clients(self, count):
        self.__clients_count = count

    ## Function 
    def http_server(self, conn ,addr):
        msg  = "HTTP/1.1 200 OK\n"\
                   +"Content-Type: text/html\n"\
                   +"\n"\
                   +"<html><body>WOW</body></html>\n"
        conn.sendall(msg.encode())
        conn.close()
        print("[DISCONNECT] Client disconnected")


## Main function
if __name__ == '__main__':
    # Error in command typing run command at the Terminal
    if len(sys.argv) != 4:
        print('Error! call server.py with <IP_ADDRESS> <PORT#> <function>')
        exit(-1)

    # The arguments specified in the terminal (invoke Server)
    IP_ADDRESS = sys.argv[1]
    PORT = sys.argv[2]
    method = sys.argv[3]

    # Init the object server - the socket to communication with Client
    server = Server(IP_ADDRESS, PORT)
    
    ## Type 1 (for details see Description above) 
    if method == 'sequential':
        conn, addr = server.accept()  # Listen and waiting for the Client to connect
        server.sequential(conn, addr)

    ## Type 2 (for details see Description above)
    elif method == 'concurrently':
        while True:
            conn, addr = server.accept()  # Listen and waiting for a Client to connect
            thread = threading.Thread(target=server.sequential, args=(conn, addr))  # Each thread handle a signle Client (infinite requests)
            time.sleep(0.5)  # Solution for the optional race condition (between the threads)
            thread.start()  # Start the thread activity
            server.set_amount_of_clients(threading.active_count() - 1)  # Update the number of Clients 
            print(f"[ACTIVE CONNECTIONS] There are {threading.active_count() - 1} Clients connected at this moment")

    ## Type 3 (for details see Description above)
    elif method == 'httpServer':
        connHTTP, addrHTTP = server.accept()  # Listen and waiting for the Client to connect
        server.http_server(connHTTP, addrHTTP)
    
    print("Server ended")