import tkinter as tk
import socket
import threading
class Receiver_Connect(tk.Frame):
    def __init__(self,parent,root,user_name):
        tk.Frame.__init__(self,parent)
        self.root = root 
        self.parent = parent
        self.path = "Data"
        self.user_name = user_name
        self.port = 2500
        self.my_ip = self.get_my_ip()
        self.title = tk.Label(self,text="Receiving Files ",relief='solid',fg='blue',bg='red',font=("arial",16,"bold"))
        self.title.pack(fill=tk.BOTH,padx=2,pady=2)
        self.s = threading.Thread(target=self.create_connection)
        self.s.start()
    

    def create_connection(self):
        self.create_socket()
        self.get_sender()
        self.receive()

    def get_my_ip(self):
        return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

    def create_socket(self):
        self.receiver_socket = socket.socket()
        self.receiver_socket.bind((self.my_ip, self.port))
        self.receiver_socket.listen(5)
        print ('Receiver listening....')
    def get_sender(self):
        self.sender_socket, self.sender_addr = self.receiver_socket.accept() 
        print ('Got connection from', self.sender_addr)
        data = self.sender_socket.recv(1024)
        self.sender_socket.send(self.user_name.encode())
        self.sender_socket.close()

        
    def receive(self):
        self.receiver_socket.settimeout(60)
        try:
            self.sender_socket, self.sender_addr = self.receiver_socket.accept() 
            data = str(self.sender_socket.recv(1024),"utf-8")
            self.sender_name = data
            print("Got sender",self.sender_name)
            file_names = str(self.sender_socket.recv(1024),"utf-8")
            file_names = file_names.split()
            print(file_names)
            file_sizes = str(self.sender_socket.recv(1024),"utf-8")
            file_sizes = file_sizes.split() 
            print(file_sizes)

            self.sender_socket.settimeout(10)
            for file_name,file_size in zip(file_names,file_sizes):
                with open(self.path+'/'+file_name, 'wb') as f:
                    file_size=  int(file_size)
                    size = 0
                    print("image size is ",file_size)
                    while(True):
                        #print("Boom..")
                        try:
                            chunk = self.sender_socket.recv(1024)
                            f.write(chunk)
                        except:
                            pass


                        #print("Drugs dho")
                        size+=len(chunk)
                        if  size >= file_size:
                            break
                    
                    print("Done with writing File")
        except:
            pass
        self.sender_socket.settimeout(0)

        self.receiver_socket.close()
        self.sender_socket.close()
