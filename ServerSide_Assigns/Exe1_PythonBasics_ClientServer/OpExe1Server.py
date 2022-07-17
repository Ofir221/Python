## Version of optional assignment - Server

## Assignment 1 - Server side course
# Server side: server.py
# Submitters: Ofir Nahshoni 204616718, Ori Tsemach 205927775
# Description:
# Client Server system (one Client) 2 directional communication, using TCP (Transfer Control Protocol).

## Libraries
import socket
import threading
import time
import string
import random
import sys

class Server:
    
    def __init__(self, ip, port):
        ## Global Variables
        self.__SERVER_PORT = int(port)  # 5050
        self.__SERVER_IP = ip  # Local IP address given by router
        self.__ADDR = (self.__SERVER_IP, self.__SERVER_PORT)
        self.BUFFER_SIZE = 1024
        self.__DIS_CONN_MSG = "exit"
        self.__clients_count = 0
        # self.HTTP_SERVER = 'httpServer'

        ## Create the socket
        self.server = socket.socket()
        ## Binding the socket server to address and port
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
            if msg == "exit":
                connected = False

            # Send massage back to Client
            msg = msg.upper()
            conn.sendall(msg.encode())
            print(f"[WRITING] Server sent to Client: {msg}")

        # Close connection with current Client
        conn.close()
        print("[DISCONNECT] Client disconnected")

        # Update amount of Clients after the current Client has disconnected
        self.__clients_count  = self.__clients_count - 1
        print(f"[ACTIVE CONNECTIONS] There are {self.__clients_count} Clients connected at this moment")
        
    def accept(self):
        return self.server.accept()

    def set_amount_of_clients(self, count):
        self.__clients_count = count

    def http_server(self, conn ,addr):
        msg  = "HTTP/1.1 200 OK\n"\
                   +"Content-Type: text/html\n"\
                   +"\n"\
                   +"<html><body>WOW</body></html>\n"
        conn.sendall(msg.encode())
        conn.close()
        print("[DISCONNECT] Client disconnected")


def thread_acc(conn, lock):
    lock.acquire()
    ## Critical code section
    msg = conn.recv(1024).decode()
    print(msg)
    # The ID of the Request in the Server
    msg = str(int(msg) * 8)  # The first byte of request = ID of the Request
    conn.sendall(msg.encode())
    ## End critical code
    lock.release()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('call server.py with <IP_ADDRESS> <PORT#> <function>')
        exit(-1)

    IP_ADDRESS = sys.argv[1]
    PORT = sys.argv[2]
    method = sys.argv[3]
    
    server = Server(IP_ADDRESS, PORT)
    
    if method == 'sequential':
        conn, addr = server.accept()  # Listen and waiting for a Client to connect
        server.sequential(conn, addr)

    elif method == 'concurrently':
        while True:
            conn, addr = server.accept()  # Listen and waiting for a Client to connect
            thread = threading.Thread(target=server.sequential, args=(conn, addr))
            time.sleep(0.5)
            thread.start()  # Start the thread activity to control the threads made
            server.set_amount_of_clients(threading.active_count() - 1)
            print(f"[ACTIVE CONNECTIONS] There are {threading.active_count() - 1} Clients connected at this moment")

    elif method == 'httpServer':
        connHTTP, addrHTTP = server.accept()  # Listen and waiting for a Client to connect
        server.http_server(connHTTP, addrHTTP)

    elif method == 'idRequest':
        print("Server starting idRequest process:")
        # count = 0
        lock = threading.Lock()
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=thread_acc, args=(conn, lock))
            thread.start()
            
            # count = count + 1
    
    print("Server ended")