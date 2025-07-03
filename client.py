from network import Network

def home():
    data = input("Login/Register? ")
    if data.lower() == "login":
        programData["programState"] = 1
    elif data.lower() == "register":
        programData["programState"] = 2
    elif data.lower() == "exit" or data.lower() == "back":
        programData["programState"] = 100
        return

def login(network):
    userName = input("Enter your username ")

    if userName.lower() == "back":
        programData["programState"] = 0
        return
    elif userName.lower() == "exit":
        programData["programState"] = 100
        return

    password = input("Enter your password ")

    if password.lower() == "back" :
        programData["programState"] = 0
        return
    elif password.lower() == "exit":
        programData["programState"] = 100
        return


    stat = network.connect("login", userName, password)
    print(stat)
    if stat:
        programData["programState"] = 3
    else:
        print("Wrong username/password")


def register(network):
    userName = input("Enter your desired username ")

    if userName.lower() == "back" :
        programData["programState"] = 0
        return
    elif userName.lower() == "exit":
        programData["programState"] = 100
        return

    password = input("Enter your desired password ")

    if password.lower() == "back" :
        programData["programState"] = 0
        return
    elif password.lower() == "exit":
        programData["programState"] = 100
        return


    stat = network.connect("register", userName, password)
    if stat:
        programData["programState"] = 3
    else:
        print("Username already in use")


def contacts(network):
    contacts = network.send(["refresh"])
    print("Your contacts: ", contacts)
    choice = input("Would you like to add a contact or see a contact? | type 'add' or 'view'")

    if choice.lower() == "back" :
        programData["programState"] = 0
        return
    elif choice.lower() == "exit":
        programData["programState"] = 100
        return
    elif choice.lower() == "add":
        new = input("Type in the username ")
        check = network.send(["add", new])
        print(check)
    elif choice[0:4].lower() == "view":
        programData["programState"] = 4

def chatting(network):
    contacts = network.send(["refresh"])
    print("Your contacts: ", contacts)
    con = input("Which contact would you like to view?")

    messages = network.send(["retrieve", con])
    if isinstance(messages, str):
        print(messages)
    else:
        to = messages["to"]
        from_ = messages["from"]

elif
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


programData = {"programState": 0}
n = Network()


while programData["programState"] != 100:
    switcher(n)
