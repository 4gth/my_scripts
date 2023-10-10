import passwordManager as pm
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
userdb = 'user.db'


def makeNewUser(iusername, ipassword):
    messagebox.showinfo(title='hurray', message=f'parameters sent {iusername}, {ipassword}')
    return


def createUserFrame():
    mainFrame.grid_forget()
    newUserFrame = ttk.Frame(root)
    newUserFrame.grid(row=0,column=0)
    newUsername = tk.Entry(newUserFrame)
    newPassword = tk.Entry(newUserFrame)
    userLabel = tk.Label(newUserFrame, text='New Username')
    passwordLabel = tk.Label( newUserFrame, text='New Password')
    creatUserButton = tk.Button(newUserFrame, width='25', text='Create User', command=makeNewUser(newUsername.get(), newUsername.get()))
    
    
    userLabel.grid(row=0, column=0)
    passwordLabel.grid(row=1, column=0)
    newUsername.grid(row=0, column=1)
    newPassword.grid(row=1, column=1)
    creatUserButton.grid(row=2, columnspan=2)


def userLogin():
    return

def onclick():
    ttk.Label(text='Hello world!').grid(row=1, columnspan=3)

    
root = tk.Tk()
root.title('Password Manager')
root.geometry('400x150')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainFrame = ttk.Frame(root)
mainFrame.grid(row=0,column=0)
Login = tk.Button(mainFrame, width=25, text='Login', command=userLogin)
newUser = tk.Button(mainFrame, width=25, text=' New User', command=createUserFrame)
Login.grid(row=0,column=0)
newUser.grid(row=1,column=0)





root.mainloop()

