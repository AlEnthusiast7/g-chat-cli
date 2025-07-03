import json


class database_manager:
    def __init__(self):
        self.data = {}
        self.file = "database.json"

    def validator(self, name, password):
        if name in self.data:
            if self.data[name]["password"] == password:
                return True
        return False

    def load_data(self):
        try:
            with open(self.file, "r") as f:
                self.data = json.load(f)
        except Exception as e:
            print("Error loading data: ",e)

    def save_data(self):
        try:
            with open(self.file, "w") as f:
                json.dump(self.data,f)
        except Exception as e:
            print("Error saving server data: ", e)


    def update(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=2)

    def save_message(self, sender, receiver, message):
        if sender in self.data and receiver in self.data:
            if receiver in self.data[sender]["contacts"]:
                self.data[sender]["contacts"][receiver]["to"].append(message)
            if sender in self.data[receiver]["contacts"]:
                self.data[receiver]["contacts"][sender]["from"].append(message)

    def remove_contact(self, user, contact):
        del self.data[user]["contacts"][contact]

    def add_contact(self, user, contact):
        if contact not in self.data:
            return f"{contact} doesn't exist"
        if contact not in self.data[user]["contacts"]:
            self.data[user]["contacts"][contact] = {}
            self.data[user]["contacts"][contact] = {}
            self.data[user]["contacts"][contact]["to"] = []
            self.data[user]["contacts"][contact]["from"] = []
            return f"Successfully added {contact}!"
        return "Already added!"

    def new_user(self, name, password):
        if name not in self.data:
            self.data[name] = {"password": password, "contacts": {}}
            return True
        return False

    def retrieve_messages(self, user, contact):
        if contact in self.data[user]["contacts"]:
            return self.data[user]["contacts"][contact]
        else:
            return "Contact doesn't exist"


    def retrieve_contacts(self,user):
        try:
            contacts = [contact for contact in self.data[user]["contacts"]]
        except Exception as e:
            print("Error retrieving contacts: ", e)
        if len(contacts) == 0:
            return "No contacts"
        else:
            return contacts

    def retrieve_all_users(self):
        return [user for user in self.data]
