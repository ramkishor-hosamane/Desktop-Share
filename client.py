import socket
import threading
def recv_msg(s):
    while True:
        print(s.recv(1024).decode())

def send_msg(s):
    while True:
        cmd = input()
            
        s.send(cmd.encode())
s = socket.socket()
HOST = "127.0.0.1"
PORT = 4444
sock_address = (HOST,PORT)
s.connect(sock_address)
name = input("Enter your name : ")
s.send(name.encode())
sm = threading.Thread(target=send_msg,args=(s,),daemon = True)
rm = threading.Thread(target=recv_msg,args=(s,),daemon = True)

sm.start()
rm.start()

sm.join()
rm.join()

print("Main finshed")