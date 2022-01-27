
import tkinter as tk                # python 3
from tkinter import font as tkfont
from typing import Container
import client  # python 3
from threading import Thread

cl = client.Client()

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=2)
        container.grid_columnconfigure(0, weight=2)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, ThirdPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to the Chatting App", font=controller.title_font)
        label.pack(side="top", fill="x", pady=50)
        self.controller.geometry("400x400")
        button_font = tkfont.Font(size = 20)
        button1 = tk.Button(self, text="Sign Up",height=1 ,width=7 ,font = button_font,
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Login",height=1, width=7,font= button_font,
                            command=lambda: controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Exit",height=1, width=7,font= button_font,
                            command=parent.destroy)            
        button1.pack()
        button2.pack()
        #button3.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Sing Up", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        user_name_label = tk.Label(self,text="Enter the UserName You Want?")
        user_name_label.pack()
        self.user_name = tk.Entry(self,width=30)
        self.user_name.pack()
        password_label = tk.Label(self,text="Enter the Password You Want?")
        password_label.pack()
        self.password = tk.Entry(self,width=30)
        self.password.pack()
        face_button = tk.Button(self, text="Face Capture",
                           command= client.capture)
        face_button.pack()

        sing_up_button = tk.Button(self, text="Sing Up ",
                           command=self.sing)
        sing_up_button.pack()

        button = tk.Button(self, text="Go Back ",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

    def sing(self):
        print("the button is clicked")
        user_names = self.user_name.get()
        passwords =  self.password.get()
        check = cl.sing_up(user_names,passwords)
        #label2 = tkinter.Label(out)
        #label2.grid(column=1,row=4) 
        self.password.delete(0,'end')
        self.user_name.delete(0,'end')
        if check == "False":
            print("go to the login Page")
            label_re = tk.Label(self,text="Account Created Succesfully!!")
            label_re.pack()
        else:
            print("user already exist")
            label_re = tk.Label(self,text="Account Already Exist or taken!!")
            label_re.pack()



class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Login", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        user_name_label = tk.Label(self,text="Enter the UserName ?")
        user_name_label.pack()
        self.user_name = tk.Entry(self,width=30)
        self.user_name.pack()
        password_label = tk.Label(self,text="Enter the Password ?")
        password_label.pack()
        self.password = tk.Entry(self,width=30)
        self.password.pack()
        face_button = tk.Button(self, text="Face Verification",
                           command=client.capture)
        face_button.pack()
        login_button = tk.Button(self, text="Login",
                           command=self.login)
        login_button.pack()

        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
    
    def login(self):
        print("the button is clicked")
        user_names = self.user_name.get()
        passwords =  self.password.get()
        result,face_found = cl.login(user_names,passwords)
        #label2 = tkinter.Label(out)
        #label2.grid(column=1,row=4) 
        self.password.delete(0,'end')
        self.user_name.delete(0,'end')
        print("result",type(result))
        print("face_fund",face_found)
        if result == "True":
            print("Authorized")
            label_auth = tk.Label(self,text="You Are Authorized")
            label_auth.pack()
            self.controller.show_frame("ThirdPage")
        elif result == "False" and face_found =="True" :
            print("Not Authorized")
        else:
            print("Face not found")



class ThirdPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to the Chatting App", font=controller.title_font)
        label.pack(side="top", fill="x", pady=50)
        messages_frame = tk.Frame(self)
        my_msg = tk.StringVar()  # For the messages to be sent.
        my_msg.set("This is the Message ")
        scrollbar = tk.Scrollbar(messages_frame)  # To navigate through past messages.
        # Following will contain the messages.
        self.msg_list = tk.Listbox(messages_frame, height=10, width=80, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.msg_list.pack()
        messages_frame.pack()

        entry_field = tk.Entry(self, textvariable=my_msg)
        entry_field.bind("<Return>", lambda: cl.send(my_msg))
        entry_field.pack()
        send_button = tk.Button(self, text="Send", command=lambda: cl.send(my_msg))
        send_button.pack()
        recive_button = tk.Button(self, text="Recive_on", command =self.recive_msg)
        recive_button.pack()
        
    def recive_msg(self):
        receive_thread = Thread(target=cl.receive,args=(self.msg_list,))
        receive_thread.start()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()