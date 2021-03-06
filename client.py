import socket
import sys
import threading
import getpass
import os
import pickle
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import argparse

# Change it to any value of 16 byte length (should be same for client and server)
key = '1234567891234567'.encode('utf-8')


def encrypt(message):
    iv = get_random_bytes(16)
    cipher1 = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher1.encrypt(pad(message, 16))
    return base64.b64encode(iv+ct)


def decrypt(enc):
    ct = base64.b64decode(enc)
    iv = ct[:16]
    ct = ct[16:]
    cipher2 = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher2.decrypt(ct), 16)
    return pt.decode('utf-8')


os.system('clear')
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="port")
parser.add_argument(
    "-i", "--ip", help="ip address of server")
parser.add_argument("-u", "--user", help="username")
args = parser.parse_args()

if not (args.ip and args.port and args.user):
    print("Insufficient Arguments!")
    print("\u001b[31;1m\n")
    print(
        "USAGE:\tpython3 client.py -p PORT  -i IP_ADDRESS_OF_SERVER -u USER")
    print("\n\n\u001b[0m")
    sys.exit()

try:
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = int(args.port)
    SERVER = args.ip
    c.connect((SERVER, PORT))
    # user = getpass.getuser()
    user = str(args.user)
    c.send(user.encode('utf-8'))
except:
    print("Invalid Arguments!")
    print("\u001b[31;1m\n")
    print(
        "USAGE:\tpython3 client.py -p PORT  -i IP_ADDRESS_OF_SERVER -u USER")
    print("\n\n\u001b[0m")
    sys.exit()

print('''\033[;1m \033[1;39m 

╱╱╱╱╱╱╱╭━━━╮╱╱╱╱╱╭╮╱╱╱╱╭╮
╱╱╱╱╱╱╱┃╭━╮┃╱╱╱╱╱┃┃╱╱╱╭╯╰╮
╭━━┳╮╱╭┫╰━━┳━━┳━━┫┃╭┳━┻╮╭╯
┃╭╮┃┃╱┃┣━━╮┃╭╮┃╭━┫╰╯┫┃━┫┃
┃╰╯┃╰━╯┃╰━╯┃╰╯┃╰━┫╭╮┫┃━┫╰╮
┃╭━┻━╮╭┻━━━┻━━┻━━┻╯╰┻━━┻━╯
┃┃╱╭━╯┃         Developed By: Akarsh
╰╯╱╰━━╯   
\033[0;0m''')
print("\033[1;36mType 'exit()' to end the chat!\033[0;0m \n")


def receive():
    while True:
        try:
            msg = c.recv(1024)
            USER, MESSAGE = pickle.loads(msg)
            MESSAGE = decrypt(MESSAGE)
            if (USER != user):
                if (MESSAGE == 'hopped in!'):
                    print(f"\n\033[1;34m{USER} {MESSAGE}\033[0;0m ")
                    sys.stdout.write(
                        f"\033[1;32m{user} (me): \033[0m \033[;1m")
                    sys.stdout.flush()
                elif (USER == 'past'):
                    print(f"\n{MESSAGE}")
                else:
                    print(f"\n{USER}: {MESSAGE}")
                    sys.stdout.write(
                        f"\033[1;32m{user} (me): \033[0m \033[;1m")
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
                message = encrypt(message.encode("utf-8"))
                c.send(pickle.dumps((user, message)))
                c.close()
                break

            else:
                message = encrypt(message.encode("utf-8"))
                c.send(pickle.dumps((user, message)))
        except:
            print("Error while Sending!")
            sys.exit()


send_thread = threading.Thread(target=send)
receive_thread = threading.Thread(target=receive)


send_thread.start()
receive_thread.start()
