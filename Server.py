from base64 import decode
import socket
from deepface import DeepFace
import os
from login import Credential
from threading import Thread
from Crypto.Cipher import AES
credential = Credential()
credential.create_database()

# it is used to create a socket variable that will use ipv4 and the TCP protocol for connection
s = socket.socket()
print("socket created")
# used for binding an ipaddress and port for accepting the connection
s.bind(('localhost', 9999))
# it is used to set the buffer for connection how many user can connect to the
s.listen(4)
print("waiting for connection")


class Server:
    def lenstr(self, msg):
        size = len(msg)
        if size % 16 != 0:
            for i in range(size, 200):
                if i % 16 == 0:
                    return msg
                else:
                    msg = msg+" "
        else:
            return msg

    def do_decrypt(self, ciphertext):
        obj2 = AES.new(b'This is a key123', AES.MODE_CBC, b'This is an IV456')
        message = obj2.decrypt(ciphertext)
        return message

    def sing_up(self, username, password, c):
        credential.add_new_user(username, password)
        print("user has been created")
        parent_dir = "D:/projects/SocketProgramming/"
        parent_dir = os.getcwd()
        path = os.path.join(parent_dir, username)
        if os.path.isdir(path) == True:
            c.send(bytes("True", 'utf8'))
            return
        else:
            os.mkdir(path)
            c.send(bytes("False", "utf8"))
        os.chdir(path)
        i = c.recv(3)
        num = int(i)
        file = open("%s.jpg" % username, 'wb')
        while num != 0:
            image_chunk = c.recv(1024)
            if not image_chunk:
                break
            else:
                file.write(image_chunk)
            num -= 1
        file.close()
        os.chdir(parent_dir)
        return

    def login(self, user_name, password, c, addr):
        while True:
            print("login_page")
            re = credential.check_user(user_name, password)
            parent_dir = os.getcwd()
            path = os.path.join(parent_dir, user_name)
            if os.path.isdir(path) == True:
                print("user exist")
                c.send(bytes("True", 'utf-8'))
            else:
                print("User Dont Exist")
                c.send(bytes("False", 'utf-8'))
            os.chdir(path)
            try:
                os.remove('verification.jpg')
            except:
                print("the file doesn't exist")
            i = c.recv(3)
            num = int(i)
            file = open("verification.jpg", 'wb')
            while num != 0:
                image_chunk = c.recv(1024)
                if not image_chunk:
                    break
                else:
                    file.write(image_chunk)
                num -= 1
            file.close()
            try:
                resp = DeepFace.verify(img1_path="{}.jpg".format(
                    user_name), img2_path="verification.jpg")
                resp = list(resp.values())[0]
                c.send(bytes("True", 'utf-8'))
            except:
                print("no face found in the image")
                os.remove('verification.jpg')
                c.send(bytes("False", 'utf-8'))
                return
            os.remove('verification.jpg')
            os.chdir(parent_dir)
            if re == "pass" or resp == True:
                addresses[c] = addr
                c.send(bytes("True", 'utf-8'))
                Thread(target=server.handle_client,
                       args=(c, user_name)).start()
                return True
            else:
                c.send(bytes("False", 'utf-8'))
                return False

    # Takes client socket as argument.
    def handle_client(self, client, user_name):
        """Handles a single client connection."""
        name = user_name
        welcome = 'Welcome %s! To quit chat: type {quit} and send.' % name
        client.send(bytes(welcome, 'utf8'))
        name = name.encode()
        print("name", name)
        msg = b"%s has joined the chat!" % name
        print("msg", msg)
        self.broadcast(msg, name)
        clients[client] = name
        while True:
            msg = (self.do_decrypt(client.recv(100))).rstrip(b' ')
            print(msg)
            if msg != bytes("{quit}", 'utf8'):
                self.broadcast(msg, name + b": ")
            else:
                client.send(bytes("{quit}", 'utf8'))
                client.close()
                del clients[client]
                self.broadcast(bytes("%s has left the chat." % name, 'utf8'))
                break

    def broadcast(self, msg, prefix=""):  # prefix is for name identification.
        """Broadcasts a message to all the clients."""
        for sock in clients:
            sock.send(prefix + msg)


server = Server()
clients = {}
addresses = {}


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        c, client_address = s.accept()
        print("%s:%s has connected to" % client_address,)
        Thread(target=user_login, args=(c, client_address)).start()


def user_login(c, client_address):
    while True:
        c_name, c_pass, option = [i for i in c.recv(
            2048).decode('utf-8').split('\n')]
        print(c_name, c_pass, " ", option)
        if option == "sing_up":
            server.sing_up(c_name, c_pass, c)
            print("ended")
        elif option == "login":
            ans = server.login(c_name, c_pass, c, client_address)
            if ans:
                break
        else:
            print("else")
            # s.shutdown(socket.SHUT_RDWR)
            c.close()
            break


ACCEPT_THREAD = Thread(target=accept_incoming_connections)
ACCEPT_THREAD.start()  # Starts the infinite loop.
ACCEPT_THREAD.join()
s.close()
#Thread(target=server.handle_client, args=(c,user_name,)).start()
