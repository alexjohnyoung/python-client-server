import socket
import threading
from util import get_valid_string, get_valid_int
HOST = '0.0.0.0'

ACTIVE_CONNECTION = False
SERVER_SOCK = None
SOCK_LIST = []
AUTHENTICATED_SOCKS = []
PASSWD = ""


# Used to close all sockets
def close_sockets():
    global AUTHENTICATED_SOCKS
    global ACTIVE_CONNECTION
    global SOCK_LIST
    global SERVER_SOCK

    print("Closing connections gracefully..")

    ACTIVE_CONNECTION = False

    for key, sock in enumerate(SOCK_LIST):
        print(f"Client socket {str(key+1)} closed.\n")
        sock.send("!close".encode())
        sock.close()

    AUTHENTICATED_SOCKS = []
    SOCK_LIST = []
    SERVER_SOCK.close()

# Used with multithreading to handle individual client connections
def handle_connection(sock, addr):

    global ACTIVE_CONNECTION
    global AUTHENTICATED_SOCKS
    global SERVER_SOCK

    while ACTIVE_CONNECTION:
        try:
            data = sock.recv(1024)

            if not data:
                break

            data = data.decode()

            if not addr[0] in AUTHENTICATED_SOCKS:
                if data != PASSWD:
                    print(f"Client connection {addr[0]} failed authentication.")
                    sock.send("!close".encode())
                    close_sockets()
                else:
                    print(f"Client connection {addr[0]} authenticated.")
                    AUTHENTICATED_SOCKS.append(addr[0])
                    sock.send("Authenticated.".encode())
            else:  # authenticated chat
                print(f"[{addr[0]}]: {data}")
                sock.sendall(data.encode())

        except ConnectionResetError:
            sock.close()
        except ConnectionAbortedError:
            sock.close()
        except OSError:
            print(f"Connection closed by client socket {addr[0]}")
            ACTIVE_CONNECTION = False
            SERVER_SOCK.close()


# Used with multithreading to handle user input
def handle_input(sock, addr):

    print(f"Connection established with {addr[0]}\n"
          f"Type 'exit' to end connection")

    print("Waiting for client to enter password..")

    while ACTIVE_CONNECTION:
        text = get_valid_string("")

        if text != "exit":
            if ACTIVE_CONNECTION:

                try:
                    sock.sendall(text.encode())
                except OSError:
                    pass
        else:
            close_sockets()


# Used to startup server
def start_server():

    global PASSWD

    port = get_valid_int("Enter port number", 80, 40000)
    pw = get_valid_string("Enter password")

    PASSWD = pw

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((HOST, port))

        s.listen(1)

        global SERVER_SOCK
        SERVER_SOCK = s

        print("Listening for connection..")

        conn, addr = s.accept()

        global ACTIVE_CONNECTION
        ACTIVE_CONNECTION = True

        handle_client = threading.Thread(target=handle_connection, args=(conn, addr))
        handle_client.start()

        handle_inc_data = threading.Thread(target=handle_input, args=(conn, addr))
        handle_inc_data.start()

        SOCK_LIST.append(conn)

        try:
            while ACTIVE_CONNECTION:
                pass
        except KeyboardInterrupt:
            close_sockets()

    except OSError:
        print("Socket already opened on this port - bug?")

