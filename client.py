import socket
import sys
import threading
import getpass
import os
import pickle


os.system('clear')
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 7654
SERVER = socket.gethostbyname(socket.gethostname())
c.connect((SERVER, PORT))
# user = getpass.getuser()
user = input("Enter your username: ")

c.send(user.encode('utf-8'))

print('''\033[1;36m
Developed by:-\033[0;0m''')
print('''\033[;1m \033[1;39m 
               _________              __           __   
______ ___.__./   _____/ ____   ____ |  | __ _____/  |_ 
\____ <   |  |\_____  \ /  _ \_/ ___\|  |/ // __ \   __\
|  |_> >___  |/        (  <_> )  \___|    <\  ___/|  |  
|   __// ____/_______  /\____/ \___  >__|_ \\___  >__|  
|__|   \/            \/            \/     \/    \/  
                        Developed by:- Akarsh    
\033[0;0m''')
print("\033[1;36mType 'exit()' to end the chat!\033[0;0m \n")
msg = ''
while True:
    message = c.recv(7).decode('utf-8')
    if message == "jibrish":
        break
    else:
        msg += message
        if len(message) == 0:
            break
print(msg)


def receive():
    while True:
        try:
            msg = c.recv(1024)
            USER, MESSAGE = pickle.loads(msg)
            if (USER != user):
                print(f"\n{USER}: {MESSAGE}")
                sys.stdout.write(f"\033[1;32m{user} (me): \033[0m \033[;1m")
                sys.stdout.flush()

        except:
            break


def send():
    while True:
        try:
            sys.stdout.write(f"\033[1;32m{user} (me): \033[0m \033[;1m")
            sys.stdout.flush()
            message = input()

            if message == "exit()":
                c.send(pickle.dumps((user, message)))
                c.close()
                break

            else:
                c.send(pickle.dumps((user, message)))
        except:
            print("Error while Sending!")
            sys.exit()


send_thread = threading.Thread(target=send)
receive_thread = threading.Thread(target=receive)


send_thread.start()
receive_thread.start()
