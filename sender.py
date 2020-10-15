import tkinter as tk
import socket
from tkinter import filedialog as tkFileDialog
import time
import nmap
import threading
import os
from tkinter.ttk import Style,Progressbar
'''
Scans network for hosts connected to same network
'''
class Sender(tk.Frame):
    '''
    Send page
    ---------
    add or remove files to send


    '''
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

        #List box to display files to be sent
        self.file_list_box = tk.Listbox(self,height = 15,  
                  width = 52,  
                  bg = "white", 
                  activestyle = 'dotbox',  
                  font = "Helvetica", 
                  fg = "black",selectmode = "multiple")
        self.file_list_box.insert(1, "/home/ram/s")
        self.file_list_box.insert(2, "/home/ram/Marksheet.pdf")
        self.file_list_box.insert(3, "/home/ram/Mywork/Python-Networking/SocketProgramming/Hack-Basic/pic1.jpg")
        self.file_list_box.place(x=12,y=150)
        print(self.file_list_box.get(0,tk.END))
        
        self.back =tk.Button(self,text="Back",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=lambda:self.root.show_frame("home_page"))
        self.back.pack(fill=tk.BOTH,side=tk.BOTTOM,padx=2,pady=25)

        self.send =tk.Button(self,text="Send",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=self.root.connect_to_send)
        self.send.pack(fill=tk.BOTH,side=tk.BOTTOM,padx=2,pady=10)

    def add_files_to_send(self):
        #to add files in the listbox to send
        files = tkFileDialog.askopenfilenames(parent=self,title='Choose a file')
        print(files)
        for file in files:
            self.file_list_box.insert(0,file.split("/")[-1])

    def remove_files(self):
        #to remove selected files in the listbox

        items = self.file_list_box.curselection()
        print(items)
        for index in items[::-1]:
            self.file_list_box.delete(index)
    def remove_all_files(self):
        #to remove all files in the listbox

        self.file_list_box.delete(0,tk.END)
class Network(object):
    def __init__(self, ip=''):
        self.ip = ip
    def scan_network(self):
        network=  self.ip +'/24'
        print("Scanning Please Wait ------>")
        nm=  nmap.PortScanner()
        nm.scan(hosts = network,arguments="-sn")
        self.host_list = [x for x in nm.all_hosts() if nm[x]['status']['state']=="up"]

class Sender_Connect(tk.Frame):
    '''
    -Create a socket connection
    -scans for recivers
    -select reciver
    -file transer
    -End of socket connection
    '''
    def __init__(self,parent,root,user_name,files):
        tk.Frame.__init__(self,parent)
        self.root = root 
        self.parent = parent
        self.files = files
        self.title = tk.Label(self,text="Sending Files Boss ",relief='solid',fg='blue',bg='red',font=("arial",16,"bold"))
        self.title.pack(fill=tk.BOTH,padx=2,pady=2)
        self.user_name = user_name
        self.sender_socket = socket.socket()             # Create a socket object
        self.port = 2500

        self.recievers = []
        #variable to check if something is still loading in page
        self.waiting = False

        #scan for recivers
        self.show_scanning()
        
    def show_scanning(self):
        #Show loading animation
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
        '''
        scan network and display who are all waiting to recive file
        -select reciver to send file
        '''


        #For testing
        self.recievers = [["Ram",'192.168.1.7'],["Sam",'192.168.1.7']]
        self.sender_socket.connect(('192.168.1.7', self.port))
        self.sender_socket.send(str("name").encode())
        data = self.sender_socket.recv(1024)        
        '''

        D = Network('192.168.1.1')
        D.scan_network()
        port = 2500
        for host in D.host_list:
            try:
                self.sender_socket.connect((host, self.port))
                self.sender_socket.send(str("name").encode())
                data = self.sender_socket.recv(1024)        
                self.recievers.append([str(data,"utf-8"),host])

            except:
                print("Something happend")
            
        print("Done checking")
        print("Recivers available ")
        print("------------------")
        '''

        for name,ip in self.recievers:
            print(name,'----->',ip)
        print()
        self.waiting = False
        self.title.configure(text="Please Select Reciver")
        self.recievers_list_frame = tk.Frame(self)
        
        for name,ip in self.recievers:
            tk.Button(self.recievers_list_frame,text=name,relief=tk.GROOVE,bg="lime",fg="blue",font=("arial",16,"bold"),command=lambda :self.send_files(name,ip)).pack(fill = tk.BOTH,pady=15,padx=10,side=tk.TOP)
  
        tk.Button(self.recievers_list_frame,text="Rescan",relief=tk.GROOVE,bg="orange",fg="red",font=("arial",16,"bold"),command=self.rescan).pack(fill = tk.BOTH,pady=15,padx=30,side=tk.TOP)
        
        self.recievers_list_frame.pack(fill=tk.BOTH, pady=30,expand=tk.YES)

    def rescan(self):
        self.recievers_list_frame.pack_forget()
        self.show_scanning()

    def get_file_names(self,files):
        files = [file_path.split("/")[-1] for file_path in files]
        return ' '.join(files)
    def send_files(self,name,ip):

        '''
        name -> username of reciver
        ip -> ip addr of reciver

        '''
        self.sender_socket = socket.socket() 
        self.sender_socket.connect((ip, self.port))
        self.sender_socket.send(self.user_name.encode())

        self.show_loading()

        self.sender_socket.send(self.get_file_names(self.files).encode())
        file_sizes = ' '.join([str(os.path.getsize(file_path)) for file_path in self.files])
        self.sender_socket.send(file_sizes.encode())
        print("Sending files")
        for file_name in self.files:
            print(file_name)
            with open(file_name,'rb') as f:
                chunk  = 1
                while(chunk):
                    chunk = f.read(1024*1024)
                    self.sender_socket.send(chunk)
    
            print('Done sending')
        
        self.sender_socket.close()
