import tkinter
from tkinter import filedialog as tkFileDialog

root = tkinter.Tk()
filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')
print(root.tk.splitlist(filez))