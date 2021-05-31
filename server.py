import socket
import threading
import pickle
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="port")
parser.add_argument(
    "-i", "--ip", help="ip address of server")
args = parser.parse_args()

if not (args.ip and args.port):
    print("Insufficient Arguments!")
    print("\u001b[31;1m\n")
    print(
        "USAGE:\tpython3 server.py -p PORT  -i IP_ADDRESS")
    print("\n\n\u001b[0m")
    sys.exit()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = int(args.port)
    SERVER = args.ip
except:
    print("Invalid Arguments!")
    print("\u001b[31;1m\n")
    print(
        "USAGE:\tpython3 server.py -p PORT  -i IP_ADDRESS")
    print("\n\n\u001b[0m")
    sys.exit()
s.bind((SERVER, PORT))
print('''\033[; 1m \033[1; 39m

╱╱╱╱╱╱╱╭━━━╮╱╱╱╱╱╭╮╱╱╱╱╭╮
╱╱╱╱╱╱╱┃╭━╮┃╱╱╱╱╱┃┃╱╱╱╭╯╰╮
╭━━┳╮╱╭┫╰━━┳━━┳━━┫┃╭┳━┻╮╭╯
┃╭╮┃┃╱┃┣━━╮┃╭╮┃╭━┫╰╯┫┃━┫┃
┃╰╯┃╰━╯┃╰━╯┃╰╯┃╰━┫╭╮┫┃━┫╰╮
┃╭━┻━╮╭┻━━━┻━━┻━━┻╯╰┻━━┻━╯
┃┃╱╭━╯┃         Developed By: Akarsh
╰╯╱╰━━╯   
\033[0; 0m''')
members = []

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


def client(client_socket, addr, USER):
    while True:
        try:
            msg = client_socket.recv(1024)
            user, message = pickle.loads(msg)
            msg = decrypt(message)
            if msg == "exit()":
                members.remove(client_socket)
                client_socket.close()
                print(f'[Active] {len(members)}')
                break

            else:
                for client in members:
                    # if (client != client_socket):
                    client.send(pickle.dumps((user, message)))

        except:
            print("Force Terminated!")
            print(f'[Active] {len(members)}')
            members.remove(client_socket)
            client_socket.close()
            break


def threads():
    s.listen()
    while True:
        try:
            client_socket, addr = s.accept()
            user = client_socket.recv(1024).decode('utf-8')
            for member in members:
                msg = encrypt("hopped in!".encode('utf-8'))
                member.send(pickle.dumps((user, msg)))

            members.append(client_socket)
            print(f'[Active] {len(members)}')

            thread = threading.Thread(
                target=client, args=(client_socket, addr, user))
            thread.start()

        except:
            s.close()
            break


print("\033[1;32m[STARTING] Server!\033[0m \033[;1m")
threads()
