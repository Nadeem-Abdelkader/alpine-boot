"""
ALPINE BOOT SCREEN Application
- Reads user data from .txt file then allows user to edit and writes back updated data to .txt file

Created by: Nadeem Abdelkader on 9/4/2022
Last updated by Nadeem Abdelkader on 10/4/2022

GUI framework = Tkinter

This file contains the helper function to be called from main.py
"""

# importing the necessary libraries for working with json
from tkinter import Frame, Label, Entry, X, LEFT, RIGHT, YES, messagebox, Button, Tk, TOP

# declaring the constants to be used everywhere in the module
FIELDS = ('KEYMAPOPTS', 'HOSTNAMEOPTS', 'INTERFACESOPTS', 'DNSOPTS', 'TIMEZONEOPTS', 'PROXYOPTS',
          'APKREPOSOPTS', 'SSHDOPTS', 'NTPOPTS', 'DISKOPTS', 'LBUOPTS', 'APKCACHEOPTS')

DISPlAY_FIELDS = ('Keyboard Layout', 'Host Name', 'Network Interface', 'DNS and Domain', 'Timezone', 'Proxy',
                  'Repository', 'SSH Server', 'NTP Service', 'DISKOPTS', 'LBUOPTS', 'APKCACHEOPTS')

BASE_DIR = "/usr/local/KC"

ANSWERS_FILE = BASE_DIR + "/config/answers.txt"
HOST_FILE = BASE_DIR + "/etc/hostname.txt"
INTERFACES_FILE = BASE_DIR + "/etc/network/interfaces.txt"
RESOLVE_FILE = BASE_DIR + "/etc/resolve.conf"

global txt_result
global my_ents

data_dict = {
    FIELDS[0]: None,
    FIELDS[1]: None,
    FIELDS[2]: None,
    FIELDS[3]: None,
    FIELDS[4]: None,
    FIELDS[5]: None,
    FIELDS[6]: None,
    FIELDS[7]: None,
    FIELDS[8]: None,
    FIELDS[9]: None,
    FIELDS[10]: None,
    FIELDS[11]: None,
}


def read_to_dict(filename):
    """
    This function reads data from a txt file to a dictionary
    :param filename: file to read from
    :return: dictionary contining read data
    """
    f = open(filename, 'r')
    f = f.read()
    f = f.split('\"')
    for i in range(len(f)):
        for j in range(len(FIELDS)):
            if f[i].endswith(FIELDS[j] + "="):
                data_dict[FIELDS[j]] = f[i + 1]
    return data_dict


def read_txt_to_lst(filename):
    """
    This function reads the data from .txt file to a list
    :param filename: txt file to read from
    :return: list containing the data
    """
    mylines = []
    with open(filename, 'rt') as myfile:
        for myline in myfile:
            if myline.startswith(FIELDS[0]) or myline.startswith(FIELDS[1]) or myline.startswith(
                    FIELDS[2]) or \
                    myline.startswith(FIELDS[3]) or myline.startswith(FIELDS[4]) or myline.startswith(FIELDS[5]) \
                    or myline.startswith(FIELDS[6]) or myline.startswith(FIELDS[7]) or \
                    myline.startswith(FIELDS[8]) or myline.startswith(FIELDS[9]) or \
                    myline.startswith(FIELDS[10]) or \
                    myline.startswith(FIELDS[11]):
                start = myline.find("\"")
                end = myline.rfind("\"")
                if myline[start + 1:end].startswith("-"):
                    mylines.append(myline[start + 4:end])
                else:
                    mylines.append(myline[start + 1:end])
    return mylines


def make_form(root, fields):
    """
    This function created the actual GUI form using Tkinter Entry, Label, and Frames
    :param root: root Tkinter window
    :param fields: array of strings that include the field names to createb the form according to
    :return: an array of Tkinter entries
    """
    make_label(root)
    entries = {}
    i = 0
    data = read_to_dict(ANSWERS_FILE)
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=22, text=DISPlAY_FIELDS[i] + ": ", anchor='w')
        if field == "Password" or field == "Re-enter Password":
            ent = Entry(row, show="*")
        else:
            ent = Entry(row)
            if data[field].startswith("-"):
                ent.insert(0, data[field][3:])
            else:
                ent.insert(0, data[field])
        ent.insert(0, "")
        row.pack(side=TOP, fill=X, padx=25, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries[field] = ent
        i += 1
    return entries


def read(ents):
    """
    This function re reads data from .txt file and re populates the entries
    :param ents: entries to re populate
    :return: void
    """
    data = read_to_dict(ANSWERS_FILE)
    for i in range(len(FIELDS)):
        ents[FIELDS[i]].delete(0, 'end')
        if data[FIELDS[i]].startswith("-"):
            ents[FIELDS[i]].insert(0, data[FIELDS[i]][3:])
        else:
            ents[FIELDS[i]].insert(0, data[FIELDS[i]])
    txt_result.config(text="Successfully read data!", fg="green")
    return


def make_label(root):
    """
    This function adds the GUI heading
    :param root: root Tkinter window
    :return: void
    """
    txt_title = Label(root, width=0, font=(
        'arial', 24), text="Khwarizm Consulting")
    txt_title.pack(side=TOP, padx=5, pady=5)
    return


def submit(entries):
    """
    This function is executed when the user fills in all the inforamtion and clicks submit.
    It takes all the entered information an writes it to a .json file (users.json)
    :param entries: an array of entries that contain the entered information
    :return: void
    """
    cont = True

    if cont:
        my_dict = {}
        for i in range(len(entries)):
            my_dict[FIELDS[i]] = entries[FIELDS[i]].get()

        filename = ANSWERS_FILE
        comments = ["# Example answer file for setup-alpine script\n"
                    "# If you don't want to use a certain option, then comment it out\n\n"
                    "# Use US layout with US variant\n",
                    "\n# Set hostname to alpine-test\n",
                    "\n# Contents of /etc/network/interfaces\n",
                    "\n# Search domain of example.com, Google public nameserver\n",
                    "\n# Set timezone to UTC\n",
                    "\n# set http/ftp proxy\n",
                    "\n# Add a random mirror\n",
                    "\n# Install Openssh\n",
                    "\n# Use openntpd\n",
                    "\n# Use /dev/sda as a data disk\n",
                    "\n# Setup in /media/sdb1\n"
                    ]
        with open(filename, 'w') as file:
            for i in range(len(FIELDS)):
                if i < len(comments):
                    file.write(comments[i])
                if i == 1:
                    file.write(FIELDS[i] + "=\"-n " + my_dict[FIELDS[i]] + "\"")
                elif i == 3:
                    file.write(FIELDS[i] + "=\"-d " + my_dict[FIELDS[i]] + "\"")
                elif i == 4:
                    file.write(FIELDS[i] + "=\"-z " + my_dict[FIELDS[i]] + "\"")
                elif i == 6:
                    file.write(FIELDS[i] + "=\"-r" + my_dict[FIELDS[i]] + "\"")
                elif i == 7:
                    file.write(FIELDS[i] + "=\"-c " + my_dict[FIELDS[i]] + "\"")
                elif i == 8:
                    file.write(FIELDS[i] + "=\"-c " + my_dict[FIELDS[i]] + "\"")
                elif i == 9:
                    file.write(FIELDS[i] + "=\"-m " + my_dict[FIELDS[i]] + "\"")
                else:
                    file.write(FIELDS[i] + "=\"" + my_dict[FIELDS[i]] + "\"")
                file.write("\n")
            file.write("\n")

        txt_result.config(text="Successfully submitted data!", fg="green")

        clear(entries, True)

    return


def clear(entries, on_submit=False):
    """
    This function is executed when the users clicks the "clear" button.
    It resets the entire form
    :param entries: an array of entries to clear
    :param on_submit: indicates whether on submit or not to in order to display correct message
    :return: void
    """
    for i in range(len(FIELDS)):
        entries[FIELDS[i]].delete(0, 'end')
    if not on_submit:
        txt_result.config(text="Cleared form!", fg="green")
    return


def quit_app():
    """
    This function is executed when the users clicks the "quit" button.
    It quits the entire application
    :return: void
    """
    result = messagebox.askquestion(
        'Khwarizm Consulting', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        my_root.destroy()
    return


def text_alert():
    """
    This function creates the label where we will later add some alerts to the user like
    "please complete the required field" or "Submitted data successfully"
    :return: void
    """
    global txt_result
    txt_result = Label(my_root)
    txt_result.pack()
    return


def create_buttons():
    """
    This function creates 3 buttons (submit, clear, and quit) and associates them with the appropriate methods
    :return: void
    """
    top = Frame(my_root)
    top.pack(side=TOP)
    submit_button = Button(my_root, text="Submit", command=lambda: submit(my_ents))
    read_button = Button(my_root, text="Read", command=lambda: read(my_ents))
    clear_button = Button(my_root, text="Clear", command=lambda: clear(my_ents))
    quit_button = Button(my_root, text="Quit", command=quit_app)
    submit_button.pack(in_=top, side=LEFT)
    read_button.pack(in_=top, side=LEFT)
    clear_button.pack(in_=top, side=LEFT)
    quit_button.pack(in_=top, side=LEFT)
    return


def initialise_window():
    """
    This function initialises the Tkinter GUI window
    :return: root Tkinter window
    """
    global my_root, my_ents
    my_root = Tk()
    my_ents = make_form(my_root, FIELDS)
    my_root.geometry("800x600")
    my_root.title("Khwarizm Consulting")
    return my_root


# calling function to initialise the GUI window
my_root = initialise_window()
