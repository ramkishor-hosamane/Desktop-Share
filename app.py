
import tkinter as tk
import subprocess

root = tk.Tk() 
root.geometry('400x500')
root.title("File share") 
user_name = str(subprocess.check_output("whoami",shell=True),"utf-8")


title =tk.Label(root,text="Welcome to File share "+user_name.capitalize(),relief='solid',fg='blue',bg='red',font=("arial",16,"bold"))
title.pack(fill=tk.BOTH,padx=2,pady=2)
image = tk.PhotoImage(file = "logo.png")

photo = tk.Label(image=image,width="400")
photo.pack(fill=tk.BOTH,padx=2,pady=2)




send = tk.Button(root,text="Send",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=print)
send.pack(fill=tk.BOTH,padx=2,pady=20)


recieve = tk.Button(root,text="Recieve",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=print)
recieve.pack(fill=tk.BOTH,padx=2,pady=10)


root.mainloop()

