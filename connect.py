import socket
import threading
import defs
from util import get_valid_int, get_valid_string
from contacts import list_contacts

ACTIVE_CONNECTION = False
TARGET_IP = ""


# Used with multithreading to handle incoming data
def handle_connection(sock, addr):

    global ACTIVE_CONNECTION

    while True:
        try:
            data = sock.recv(1024)

            if not data:
                break

            data = data.decode()

            if addr[0] != TARGET_IP and data != "!close":
                print(f"[{addr}]: {data}")
            else:
                print("Connection closed by server.")
                sock.close()
                ACTIVE_CONNECTION = False

        except ConnectionResetError:
            sock.close()
        except OSError:
            pass

    sock.close()


# Used with multithreading to handle user input
def handle_input(sock, addr):

    global ACTIVE_CONNECTION

    print(f"Connected with {addr}")
    print("Enter password")

    while ACTIVE_CONNECTION:
        text = get_valid_string("")

        try:
            if ACTIVE_CONNECTION:
                sock.sendall(text.encode())
        except OSError:
            pass


# Used to connect to target address
def connect_to_target(contacts):

    if contacts == "":
        print(defs.EMPTY_CONTACTS + " connecting")
        return

    contacts, max_contacts = list_contacts(contacts)

    target_contact = get_valid_int(defs.ENTER_CONTACT, 1, max_contacts)
    target_port = get_valid_int(defs.ENTER_PORT, 80, 40000)

    target_contact = contacts[target_contact-1]
    print(f"Attempting to connect to contact {target_contact}:{str(target_port)}..")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((target_contact, target_port))

        global ACTIVE_CONNECTION
        global TARGET_IP

        ACTIVE_CONNECTION = True
        TARGET_IP = target_contact

        reader_thread = threading.Thread(target=handle_connection, args=(s, target_contact))
        input_thread = threading.Thread(target=handle_input, args=(s, target_contact))

        reader_thread.start()
        input_thread.start()

        try:
            while ACTIVE_CONNECTION:
                pass
        except KeyboardInterrupt:
            s.close()
    except ConnectionRefusedError:
        print(defs.UNABLE_CONNECT_REFUSED)
    except OSError:
        print(defs.UNABLE_CONNECT_UNREACHABLE)
