import socket
import defs
from util import get_valid_string, get_valid_int

from contacts import read_contacts, create_contacts, clear_contacts, list_contacts, add_contacts_to_file
from connect import connect_to_target
from server import start_server


# Entry point to our program
def main():

    contacts = read_contacts()

    ans = 0

    while ans != 6:

        ans = get_valid_int(defs.BUFFER_CHAT + '\n', 1, 6)

        if ans == 1:
            connect_to_target(contacts)
        elif ans == 2:
            start_server()
        elif ans == 3:

            if contacts != "":
                contacts = create_contacts(False)
            else:
                contacts = create_contacts(True)

        elif ans == 4:
            list_contacts(contacts)
        elif ans == 5:
            contacts = ""
            clear_contacts()
        else:
            break


main()
