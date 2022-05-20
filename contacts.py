import defs
from util import get_valid_string, get_valid_int
from os.path import isfile
from os import remove


# Used to retrieve number of contacts
def get_num_contacts():

    contacts_handle = open("contacts.txt", "r")
    contacts_data = contacts_handle.read()
    contacts_data = contacts_data.split('\n')

    return len(contacts_data)


# Used to add contacts to file
def add_contacts_to_file(contacts, overwrite_contacts=None):

    if overwrite_contacts == 'y':
        overwrite_contacts = 'w'
    else:
        overwrite_contacts = 'a'

    contacts_handle = open("contacts.txt", overwrite_contacts)
    contacts_handle.write(contacts)
    contacts_handle.close()


# Used to clear all saved contacts
def clear_contacts():

    try:
        remove("contacts.txt")
        print("Contacts cleared")
    except FileNotFoundError:
        print(defs.ERROR_NO_CONTACTS)


# Used to list all saved contacts
def list_contacts(contacts):

    if contacts == "":
        print(defs.EMPTY_CONTACTS + " listing")
        return

    contacts = contacts.split('\n')

    for key, contact in enumerate(contacts):
        print(f"{str(key+1)}. {contact}")

    return contacts, len(contacts)


# Used to create and add new contacts
def create_contacts(empty=False):

    contacts = ''
    add_str = defs.ADD_CONTACTS
    num_contacts = 0
    overwrite_contacts = ''

    if not empty:
        overwrite_contacts = get_valid_string("Overwrite contacts? (Y/N)").lower()

        if overwrite_contacts != 'y':
            num_contacts = get_num_contacts()

    contact_ip = ''

    while contact_ip != 'exit':

        contact_ip = get_valid_string(add_str).lower()
        add_str = "Contact added"

        if contact_ip != "exit":

            if num_contacts >= 1:
                contacts += '\n'

            contacts += contact_ip

        num_contacts += 1

    if contacts != '':
        add_contacts_to_file(contacts)
    else:
        create_contacts(True)

    return contacts


# Used to read contacts from file (creates if does not exist)
def read_contacts():

    if not isfile("contacts.txt"):
        print(defs.NO_CONTACTS_ADDING)
        create_contacts(True)

    contacts_handle = open("contacts.txt", "r")
    contacts_data = contacts_handle.read()
    contacts_handle.close()

    return contacts_data
