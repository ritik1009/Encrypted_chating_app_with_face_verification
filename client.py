import socket
import cv2
import os
import math
import tkinter as tk
from threading import Thread
from Crypto.Cipher import AES
#
#from Login_Page import login_page
current = os.getcwd()


def capture():
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0

    while img_counter < 1:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            scale_height = 30
            scale_width = 30

            #calculate the 50 percent of original dimensions
            print("Width:- ",frame.shape[1])
            print("Width:- ",frame.shape[0])
            width = int(frame.shape[1] * scale_width / 100)
            print("Width after:- ",width)
            height = int(frame.shape[0] * scale_height / 100)
            print("Height after:- ",height)
            capture.img_name = "opencv_frame_{}.png".format(img_counter)
            frame = cv2.resize(frame, (width, height))
            cv2.imwrite(os.path.join('D:\projects\SocketProgramming', capture.img_name), frame)
            print("{} written!".format(capture.img_name))
            img_counter += 1
    cam.release()
    cv2.destroyAllWindows()


def send_capture():
    file = open('D:\projects\SocketProgramming\{}'.format(
        capture.img_name), 'rb')
    file_size = os.path.getsize(
        'D:\projects\SocketProgramming\{}'.format(capture.img_name))
    print(file_size)
    resu = math.ceil(file_size/1024)
    print(resu)
    #c.send(bytes('Length {}'.format(resu),'utf-8'))
    c.send(bytes(str(resu), 'utf8'))
    image_data = file.read(1024)
    print("the File Has been opened")
    while image_data:
        print("it is in while loop")
        c.send(image_data)
        image_data = file.read(1024)
    print("Out of while Loop")
    file.close()
    print("the file has been closed")
    os.remove(os.path.join('D:\projects\SocketProgramming', capture.img_name))
    print("end of th function")
    # c.send(bytes("End","utf-8"))


c = socket.socket()

c.connect(('localhost', 9999))  # for connecting to the server


class Client:
    def sing_up(self, username, password):
        c_name = username
        c_password = password
        option = "sing_up"
        print("singup")
        c.send(bytes("\n".join([c_name, c_password, option]), 'utf8'))
        result = c.recv(10).decode()
        print(result)
        send_capture()
        return result

    def login(self, username, password):
        ver_name = username
        ver_pass = password
        option = "login"
        c.send(bytes("\n".join([ver_name, ver_pass, option]), 'utf8'))
        send_capture()
        user_exist = c.recv(5).decode()
        if user_exist:
            face_found = c.recv(5).decode()
            if face_found == "True":
                result = c.recv(5).decode()
                print("face_found", face_found)
                print("result", result)
                return result, face_found
            else:
                result = "False"
                print(face_found)
                return result, face_found
        else:
            print("user dont exist")

    def exit(self):
        c_name = "  "
        c_password = "  "
        option = "exit"
        c.send(bytes("\n".join([c_name, c_password, option]), 'utf8'))
        c.close()
        tk.destroy()

    def do_encrypt(self, message):
        obj = AES.new(b'This is a key123', AES.MODE_CBC, b'This is an IV456')
        message = bytes(message, 'utf8')
        ciphertext = obj.encrypt(message)
        print(ciphertext)
        return ciphertext

    def receive(self, msg_list):
        """Handles receiving of messages."""
        while True:
            try:
                msg = c.recv(1024).decode()
                print(msg)
                msg_list.insert(tk.END, msg)
                if msg == "{quit}":
                    c.close()
                    # top.quit()
            except OSError:  # Possibly client has left the chat.
                break

    def lenstr(self, msg):
        size = len(msg)
        if size % 16 != 0:
            for i in range(size, 600):
                if i % 16 == 0:
                    return msg
                else:
                    msg = msg+" "
        else:
            return msg

    def send(self, my_msg, event=None):  # event is passed by binders.
        """Handles sending of messages."""
        self.my_msg = my_msg
        msg = my_msg.get()
        print("msg = ", msg)
        my_msg.set("")  # Clears input field.
        c.send(self.do_encrypt(self.lenstr(msg)))

    def on_closing(self, event=None):
        """This function is to be called when the window is closed."""
        self.my_msg.set("{quit}")
        self.send(self.my_msg)

