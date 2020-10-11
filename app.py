
import tkinter as tk
import subprocess
from home import Home
from sender import Sender


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.geometry('500x600')
        self.title("File share")
        self.resizable(0, 0)
        self.container.pack(side="top",fill="both",expand=1)
        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)
        
        self.frames = {}
        self.user_name = str(subprocess.check_output("whoami",shell=True),"utf-8")
        
        self.create_frames()
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


        '''
        reciever_page = Reciever(self.container)
        self.frames.update({"reciever_page":reciever_page})
        '''


app = App() 

app.mainloop()

