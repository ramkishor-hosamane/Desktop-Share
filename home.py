import tkinter as tk

class Home(tk.Frame):

    def __init__(self,parent,root,user_name):
        tk.Frame.__init__(self,parent)

        self.root = root 
        self.user_name = user_name

        #Title
        self.title = tk.Label(self,text="Welcome to File share "+user_name.capitalize(),relief='solid',fg='blue',bg='red',font=("arial",16,"bold"))
        self.title.pack(fill=tk.BOTH,padx=2,pady=2)

        #logo
        self.logo_icon = tk.PhotoImage(file = "images/logo.png")
        self.logo = tk.Label(self,image=self.logo_icon,width="400")
        self.logo.pack(fill=tk.BOTH,padx=2,pady=2)

    
        self.send = tk.Button(self,text="Send",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=lambda:self.root.show_frame("sender_page"))
        self.send.pack(fill=tk.BOTH,padx=2,pady=20)


        self.recieve = tk.Button(self,text="Recieve",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=lambda:self.root.connect_to_recieve())
        self.recieve.pack(fill=tk.BOTH,padx=2,pady=10)


        self.settings_icon = tk.PhotoImage(file ="images/setting.png")
        self.settings = tk.Button(self, image = self.settings_icon,bg='black')
        self.settings.pack(side = tk.LEFT,padx=20)

        self.about_icon = tk.PhotoImage(file = "images/about.png")
        self.about = tk.Button(self, image = self.about_icon,bg="black")
        self.about.pack(side = tk.RIGHT,padx=20)
