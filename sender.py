import tkinter as tk
from tkinter import filedialog as tkFileDialog

class Sender(tk.Frame):
    def __init__(self,parent,root,user_name):
        tk.Frame.__init__(self,parent)   
        self.root = root 
        self.user_name = user_name
        self.title = tk.Label(self,text="Send Files ",relief='solid',fg='blue',bg='red',font=("arial",16,"bold"))
        self.title.pack(fill=tk.BOTH,padx=2,pady=2)
        self.files = []
        self.back_icon = tk.PhotoImage(file = "back.png")
        self.back = tk.Button(self, image = self.back_icon,padx=10,bg="black",command=lambda:self.root.show_frame("home_page"))
        self.back.place(x=10,y=80)

        self.add_files = tk.Button(self,text="Add",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=self.add_files_to_send,padx=20)
        self.remove_file = tk.Button(self,text="Remove",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=self.remove_files)

        self.add_files.place(x=200,y=100)
        #self.add_files.pack(pady=50,side=tk.LEFT)
        self.remove_file.place(x=300,y=100)


        self.file_list_box = tk.Listbox(self,height = 15,  
                  width = 40,  
                  bg = "white", 
                  activestyle = 'dotbox',  
                  font = "Helvetica", 
                  fg = "black",selectmode = "multiple")
        self.file_list_box.insert(1, "Python")
        self.file_list_box.insert(2, "Perl")
        self.file_list_box.insert(3, "C")
        self.file_list_box.insert(4, "PHP")
        self.file_list_box.insert(5, "JSP")
        self.file_list_box.insert(6, "Ruby")
        self.file_list_box.place(x=100,y=200)




    def add_files_to_send(self):
        files = tkFileDialog.askopenfilenames(parent=self,title='Choose a file')
        print(files)
        for file in files:
            self.file_list_box.insert(0,file.split("/")[-1])
            #self.files = []

    def remove_files(self):
        items = self.file_list_box.curselection()
        for item in items:
            self.file_list_box.delete(item)