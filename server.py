import socket
import threading
s = socket.socket()
HOST = ""
PORT = 4444
MSG_LENGTH = 1024*10
sock_address = (HOST,PORT)
s.bind(sock_address)
s.listen(5)

clients = {} 

print("Server listening ...")
def get_clients():
    pass

def transfer_msg(From,To):
    From_sock = clients[From]
    To_sock = clients[To]
    while True:
        msg = From_sock.recv(MSG_LENGTH).decode()
        msg = From+":"+msg
        To_sock.send(msg.encode())

def connection_request(From,To):
    From_sock = clients[From]
    To_sock = clients[To]
    To_sock.send(f"share to {From}".encode())
    response = From_sock.recv(MSG_LENGTH).decode()
    if response[:1].lower() =="y":
        screen_sender = threading.Thread(target=transfer_msg,args=(From,To,),daemon=True)
        screen_reciever = threading.Thread(target=transfer_msg,args=(To,From,),daemon=True)
        screen_sender.start()
        screen_reciever.start()
        screen_sender.join()
        screen_reciever.join()


def accept_clients():
    global clients
    while True:
        c,c_addr = s.accept()
        name = c.recv(1024).decode()
        print(f"Got connection from {name}")
        clients[name] = c

ac =  threading.Thread(target=accept_clients,daemon=True)
ac.start()
print("Server Started ...")
while True:
    if len(clients.keys())>1:
        From = list(clients.keys())[0]
        To = list(clients.keys())[1]
        screen_sender = threading.Thread(target=transfer_msg,args=(From,To,),daemon=True)
        screen_reciever = threading.Thread(target=transfer_msg,args=(To,From,),daemon=True)
        screen_sender.start()
        screen_reciever.start()
        screen_sender.join()
        screen_reciever.join()
        print("Main Finsihed")
        break