import tkinter as tk
import socket
from tkinter import filedialog as tkFileDialog
import time
import nmap
import threading
from tkinter.ttk import Style,Progressbar
class Network(object):
	def __init__(self, ip=''):
		self.ip = ip
        
	def scan_network(self):

		network=  self.ip +'/24'

		print("Scanning Please Wait ------>")

		nm=  nmap.PortScanner()
		nm.scan(hosts = network,arguments="-sn")
		self.host_list = [x for x in nm.all_hosts() if nm[x]['status']['state']=="up"]

class Sender(tk.Frame):
    def __init__(self,parent,root,user_name):
        tk.Frame.__init__(self,parent)   
        self.root = root 
        self.parent = parent
        self.user_name = user_name
        self.title = tk.Label(self,text="Select Files ",relief='solid',fg='blue',bg='red',font=("arial",16,"bold"))
        self.title.pack(fill=tk.BOTH,padx=2,pady=2)
        self.files = []


        self.add_files = tk.Button(self,text="Add",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=self.add_files_to_send,padx=20)
        self.add_files.place(x=10,y=100)

        self.remove_file = tk.Button(self,text="Remove",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=self.remove_files,padx=20)
        self.remove_file.place(x=150,y=100)

        self.remove_all_file = tk.Button(self,text="Remove All",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=self.remove_all_files,padx=20)
        self.remove_all_file.place(x=330,y=100)


        self.file_list_box = tk.Listbox(self,height = 15,  
                  width = 52,  
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
        self.file_list_box.place(x=12,y=150)

        
        self.back =tk.Button(self,text="Back",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=lambda:self.root.show_frame("home_page"))
        self.back.pack(fill=tk.BOTH,side=tk.BOTTOM,padx=2,pady=25)

        self.send =tk.Button(self,text="Send",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=self.root.connect_to_send)
        self.send.pack(fill=tk.BOTH,side=tk.BOTTOM,padx=2,pady=10)

    def add_files_to_send(self):
        files = tkFileDialog.askopenfilenames(parent=self,title='Choose a file')
        print(files)
        for file in files:
            self.file_list_box.insert(0,file.split("/")[-1])
            #self.files = []

    def remove_files(self):
        items = self.file_list_box.curselection()
        print(items)
        for index in items[::-1]:
            self.file_list_box.delete(index)
    def remove_all_files(self):
        self.file_list_box.delete(0,tk.END)

class Sender_Connect(tk.Frame):
    def __init__(self,parent,root,user_name):
        tk.Frame.__init__(self,parent)
        self.root = root 
        self.parent = parent
        self.title = tk.Label(self,text="Sending Files Boss ",relief='solid',fg='blue',bg='red',font=("arial",16,"bold"))
        self.title.pack(fill=tk.BOTH,padx=2,pady=2)
        self.sender_socket = socket.socket()             # Create a socket object
        self.recievers = []
        self.waiting = False

        
        self.show_scanning()
        
    def show_scanning(self):
        self.show_loading()

        self.s = threading.Thread(target=self.create_connection,daemon=True)
        self.s.start()
        self.title.configure(text="Searching for recivers")

    def show_loading(self):
        self.waiting = True
        #Loading animation GUI
        self.update()

        theme = Style()
        theme.theme_use("default")
        theme.configure("green.Horizontal.TProgressbar",background="green",thickness=100)

        #progress bar
        self.bar = Progressbar(self,style="blue.Horizontal.TProgressbar",
        orient="horizontal",mode="indeterminate",length=300)
        self.bar.pack(fill=tk.BOTH,pady=30,padx=10)
        self.loading_anim = threading.Thread(target=self.loading,daemon=True)
        self.loading_anim.start()

    def loading(self):
        while self.waiting:
            self.bar['value']+=1
            self.update_idletasks()
            time.sleep(0.01)
        self.bar.pack_forget()

        

    def create_connection(self):
        self.get_recivers()

    def get_recivers(self):
        D = Network('192.168.1.1')
        D.scan_network()
        port = 2500
        for host in D.host_list:
            try:
                self.sender_socket.connect((host, port))
                self.sender_socket.send(str("name").encode())
                data = self.sender_socket.recv(1024)        
                self.recievers.append([str(data,"utf-8"),host])

            except:
                print("Something happend")
            
        print("Done checking")
        print("Recivers available ")
        print("------------------")
        '''
        self.recievers = [["Ram",'192.168.1.7'],["Sam",'192.168.1.7']]
        '''
        for name,ip in self.recievers:
            print(name,'----->',ip)
        print()
        self.waiting = False
        self.title.configure(text="Please Select Reciver")
        #tk.Label(self,text="Please Select Reciver",relief='solid',fg='blue',bg='red',font=("arial",16,"bold")).pack(fill=tk.BOTH,padx=2,pady=20)
        self.recievers_list_frame = tk.Frame(self)
        
        for name,ip in self.recievers:
            tk.Button(self.recievers_list_frame,text=name,relief=tk.GROOVE,bg="lime",fg="blue",font=("arial",16,"bold")).pack(fill = tk.BOTH,pady=15,padx=10,side=tk.TOP)
  
        tk.Button(self.recievers_list_frame,text="Rescan",relief=tk.GROOVE,bg="orange",fg="red",font=("arial",16,"bold"),command=self.rescan).pack(fill = tk.BOTH,pady=15,padx=30,side=tk.TOP)
        
        self.recievers_list_frame.pack(fill=tk.BOTH, pady=30,expand=tk.YES)

    def rescan(self):
        self.recievers_list_frame.pack_forget()
        self.show_scanning()

