#import passwordManager as pm
import tkinter as tk
from tkinter import ttk
userdb = 'user.db'



def onclick():
    ttk.Label(text='Hello world!').grid(row=1, columnspan=3)

    
root = tk.Tk()
root.title('Password Manager')
root.geometry('400x150')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe = ttk.Frame(root)

tk.Button(mainframe, width=25, text='Hello, please click', command=onclick).grid(row=0,column=0)




root.mainloop()

