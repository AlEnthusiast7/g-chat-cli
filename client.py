import threading

from network import Network
import os
import time

programData = {"programState": 0, "programStateHistory": [0], "chosenContact": ""}
n = Network()


def switch (state):
    programData["programState"] = state
    programData["programStateHistory"].append(state)

def back():
    programData["programStateHistory"].pop()
    programData["programState"] = programData["programStateHistory"][-1]

def home():
    data = input("Login/Register? ")
    if data.lower() == "login":
        switch(1)
    elif data.lower() == "register":
        switch(2)
    elif data.lower() == "exit" or data.lower() == "back":
        switch(100)
    os.system('cls')


def login(network):
    userName = input("Enter your username ")

    if userName.lower() == "back":
        back()
        return
    elif userName.lower() == "exit":
        switch(100)
        return

    password = input("Enter your password ")

    if password.lower() == "back" :
        back()
        return
    elif password.lower() == "exit":
        switch(100)
        return


    stat = network.connect("login", userName, password)
    print(stat)
    if stat:
        switch(3)
        os.system('cls')
        return
    else:
        print("Wrong username/password")


def register(network):
    userName = input("Enter your desired username ")

    if userName.lower() == "back" :
        back()
        return
    elif userName.lower() == "exit":
        switch(100)
        return

    password = input("Enter your desired password ")

    if password.lower() == "back" :
        back()
        return
    elif password.lower() == "exit":
        switch(100)
        return


    stat = network.connect("register", userName, password)
    print(stat)
    if stat:
        switch(3)
        os.system('cls')
    else:
        print("Username already in use")

def contacts(network):
    contacts = network.send(["refresh"])
    print("Your contacts: ", contacts)
    choice = input("Would you like to add a contact or see a contact? | type 'add' or 'view'")

    if choice.lower() == "back" :
        back()
        return
    elif choice.lower() == "exit":
        switch(100)
        return
    elif choice.lower() == "add":
        new = input("Type in the username ")
        check = network.send(["add", new])
        print(check)
        return
    elif choice[0:4].lower() == "view":
        choice = input("Which contact would you like to view?")
        if network.send(["contact_check", choice]) is True:
            programData["chosenContact"] = choice
            switch(4)
        else:
            print("Contact doesn't exist")
            return
        os.system('cls')

def receive_messages(network, stop_event):
    last_messages_count = 0

    while not stop_event.is_set():
        messages = network.send(["retrieve", programData["chosenContact"]])

        if not isinstance(messages, dict):
            continue
        to = messages["to"]
        from_ = messages["from"]
        new_messages_count = len(to) + len(from_)

        if new_messages_count != last_messages_count:
            last_messages_count = new_messages_count

            i, j = 0, 0

            while i < len(to) and j < len(from_):
                if to[i + 1] <= from_[j + 1]:
                    print("Me: ", to[i])
                    i += 2
                else:
                    print(programData["chosenContact"] + ": ", from_[j])
                    j += 2

            while i < len(to):
                print("Me: ", to[i])
                i += 2
            while j < len(from_):
                print(programData["chosenContact"], ": ", from_[j])
                j += 2

            time.sleep(0.1)

def chatting(network):
    message = ""
    stop = threading.Event()
    refresher = threading.Thread(target=receive_messages, args = (network, stop), daemon=True)
    refresher.start()

    while message != "exit" and message != "back":
        message = input()

        if message.lower() == "back":
            stop.set()
            back()
            return
        if message.lower() == "exit":
            stop.set()
            switch(100)
            return
        data = ["message", programData["chosenContact"], message]
        network.send(data)




def switcher(network):

    match programData["programState"]:
        case 0:
            home()
        case 1:
            login(network)
        case 2:
            register(network)
        case 3:
            contacts(network)
        case 4:
            chatting(network)



while programData["programState"] != 100:
    switcher(n)
