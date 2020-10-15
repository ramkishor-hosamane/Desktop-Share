
import tkinter as tk
import subprocess
from home import Home
from sender import Sender,Sender_Connect
from receiver import Receiver_Connect

class App(tk.Tk):
    '''
    Main control of the app
    '''
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.geometry('500x600')
        self.title("File share")
        self.resizable(0, 0)
        
        #Main container inside root 
        self.container = tk.Frame(self)
        self.container.pack(side="top",fill="both",expand=1)
        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)

        self.frames = {}

        #getting username of the user
        self.user_name = str(subprocess.check_output("whoami",shell=True),"utf-8").capitalize()

        #Creating frames (Scenes eg -->home,send,recieve)        
        self.create_frames()
        #show home frame at the top
        self.show_frame("home_page")


    
    def hide_all_frames(self):
        pass
    
    def show_frame(self,frame):
        frame = self.frames[frame]
        frame.tkraise()

    def create_frames(self):
        sender_page = Sender(self.container,self,self.user_name)
        self.frames.update({"sender_page":sender_page})
        sender_page.grid(row=0,column=0,sticky="nsew")

        home_page = Home(self.container,self,self.user_name)
        self.frames["home_page"]=home_page
        home_page.grid(row=0,column=0,sticky="nsew")



    def connect_to_send(self):
        #Creating frame to connect sockets and send files
        sender_connect = Sender_Connect(self.container,self,self.user_name,self.frames["sender_page"].file_list_box.get(0,tk.END))
        sender_connect.grid(row=0,column=0,sticky="nsew")
        self.frames["sender_connect_page"] = sender_connect
        self.show_frame("sender_connect_page")
        
    def connect_to_recieve(self):
        #Creating frame to connect sockets and recieve files

        receiver_connect = Receiver_Connect(self.container,self,self.user_name)
        receiver_connect.grid(row=0,column=0,sticky="nsew")
        self.frames["receiver_connect_page"] = receiver_connect
        self.show_frame("receiver_connect_page")



app = App() 

app.mainloop()

