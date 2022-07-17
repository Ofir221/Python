## Version of optional assignment - Client

## Assignment 1 - Server side course
# Client side: client.py
# Submitters: Ofir Nahshoni 204616718, Ori Tsemach 205927775
# Description:
# Client Server system (one Client) 2 directional communication, using TCP (Transfer Control Protocol).

## Libraries
import socket
import sys
import threading


# Function that thread is running
def sendMsg(client, lock, i):
    lock.acquire()
    ## Critical code section
    client.sendall(str(i).encode())
    msg = client.recv(1024).decode()
    print(msg)
    ## End critical code
    lock.release()


if __name__ == '__main__':
    if (len(sys.argv) != 3) and (len(sys.argv) != 4):
            print('call client.py with <IP_ADDRESS> <PORT#>\nor call client.py with <IP_ADDRESS> <PORT#> idRequest')
            exit(-1)
    else:
        BUFFER_SIZE = 1024
        SERVER_IP = sys.argv[1]  # Local IP address given by the router of LAN (WiFi)
        SERVER_PORT = int(sys.argv[2])

        ADDR = (SERVER_IP, SERVER_PORT)

        ## Create the socket
        client = socket.socket()
        print(f"Client created a socket to: addr={SERVER_IP} port={SERVER_PORT}.")
        ## Connect to socket TCP connection
        client.connect(ADDR)
        print("Client connected to Server")

        if len(sys.argv) == 4:
            if sys.argv[3] == 'idRequest':
                lock = threading.Lock()
                # Generate 100 requests for this Client
                for i in range(100):
                    thread = threading.Thread(target=sendMsg, args=(client, lock, i))
                    thread.start()
            else:
                print('call client.py with <IP_ADDRESS> <PORT#> idRequest')
                exit(-1)
        else: 
            msg = " "
            if SERVER_PORT == 5050:
                while msg:
                    x = input("Hello Client, Enter string to send to Server: ")
                    client.sendall(x.encode())
                    if x == "exit":
                        break
                    msg = client.recv(BUFFER_SIZE).decode()
                    print(f"Client read from Server: {msg}")

            elif SERVER_PORT == 80:
                msg = client.recv(BUFFER_SIZE).decode()
                print(f"Client read from Server: {msg}")

            else:
                print("Wrong Port number, initiate process again please.")


    client.close()
    print("Client finished")
