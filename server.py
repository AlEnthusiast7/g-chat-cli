import socket
from _thread import *
import socket
import sys
import json
from records import database_manager
import pygame

pygame.init()


def threaded_client(conn):
    name = None
    password = None

    clock = pygame.time.Clock()
    try:
        while True:
            clock.tick()
            data = json.loads(conn.recv(4096).decode())
            print("message: ", data)

            if data[0].lower() == "login":
                check = records.validator(data[1],data[2])
                if check:
                    name = data[1]
                    password = data[2]
                conn.send(json.dumps(check).encode())
            elif data[0].lower() == "register":
                check = records.new_user(data[1],data[2])
                if check:
                    name = data[1]
                    password = data[2]
                conn.send(json.dumps(check).encode())
            elif data[0].lower() == "refresh":
                conn.send(json.dumps(records.retrieve_contacts(name)).encode())
            elif data[0].lower() == "message":
                print("MATCHED")
                conn.send(json.dumps(records.save_message(name, data[1], data[2:])).encode())
            elif data[0].lower() == "retrieve":
                conn.send(json.dumps(records.retrieve_messages(name,data[1])).encode())
            elif data[0].lower() == "add":
                conn.send(json.dumps(records.add_contact(name, data[1])).encode())
            print("current database: ", records.data)



    except Exception as e:
        print(e)

    finally:
        print(f"{name} has disconnected")
        conn.close()


server = "127.0.0.1"
port = 64340

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((server,port))
except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for a connection, Server started")

records = database_manager()
records.load_data()
while True:
    conn,addr = s.accept()
    print(f"connected to{conn}:{addr}")


    start_new_thread(threaded_client, (conn,))




