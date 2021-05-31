import socket
import threading
import pickle
from Crypto import Random
from Crypto.Cipher import AES

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 7654
SERVER = socket.gethostbyname(socket.gethostname())
s.bind((SERVER, PORT))
print('''\033[;1m \033[1;39m
               _________              __           __   
______ ___.__./   _____/ ____   ____ |  | __ _____/  |_ 
\____ <   |  |\_____  \ /  _ \_/ ___\|  |/ // __ \   __\
|  |_> >___  |/        (  <_> )  \___|    <\  ___/|  |  
|   __// ____/_______  /\____/ \___  >__|_ \\___  >__|  
|__|   \/            \/            \/     \/    \/  
                        Developed by:- Akarsh  
\033[0;0m''')
members = []
messages = []


def client(client_socket, addr, USER):
    while True:
        try:
            msg = client_socket.recv(1024)
            user, message = pickle.loads(msg)
            if message == "exit()":
                members.remove(client_socket)
                client_socket.close()
                break

            else:
                messages.append(f"{user}: {message}\n")
                for client in members:
                    # if (client != client_socket):
                    client.send(pickle.dumps((user, message)))

        except:
            print("Force Terminated!")
            members.remove(client_socket)
            client_socket.close()
            break


def threads():
    s.listen()
    while True:
        try:
            client_socket, addr = s.accept()
            user = client_socket.recv(1024).decode('utf-8')
            for client in members:
                client.send(f"{user} joined!".encode('utf-8'))

            members.append(client_socket)
            for message in messages:
                client_socket.send(message.encode('utf-8'))

            thread = threading.Thread(
                target=client, args=(client_socket, addr, user))
            thread.start()
            client_socket.send("jibrish".encode('utf-8'))

        except:
            s.close()
            break


print("\033[1;32m[STARTING] Server!\033[0m \033[;1m")
threads()
