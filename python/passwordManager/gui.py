import passwordManager as pm
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import pyautogui

userdb = "user.db"
passdb = "passwd.db"

isLoggedIn = False

if not os.path.isfile(userdb):
    open(userdb, "w+").close()
if not os.path.isfile(passdb):
    open(passdb, "w+").close()

def makeNewCredential(iusername, ipassword, iwebsite):
    pm.PasswordEntry.cryptFile('', True)
    pm.PasswordEntry(iwebsite, iusername, ipassword, passdb).createEntry()
    pm.PasswordEntry.cryptFile('', True)
    return

def clearFrame():
    
    currentChild = (root.winfo_children())
    if len(currentChild) >= 2:
        currentChild[len(currentChild) - 1].destroy()

def validateUser(iusername, ipassword):

    global isLoggedIn
    userHash = pm.Hashing.createHash('', iusername, ipassword)
    loginAttempt = pm.User(userHash, userdb).validateUser()
    if loginAttempt == True:
        isLoggedIn = True    
        messagebox.showinfo(
        title=f"{pm.Hashing.createHash('',iusername,ipassword)}", message="Login success, please use Functions menu to continue"
        )
        menuBar.entryconfigure('Functions', state='normal')
        clearFrame()

def makeNewUser(iusername, ipassword):
    
    hashNewUser = pm.Hashing(iusername, ipassword, userdb)
    hashNewUser.hashToFile()
        
    messagebox.showinfo(
        title="hurray", message=f"new User: {pm.Hashing.createHash('',iusername,ipassword)}"
    )
    return

def loginFrame(): 

    clearFrame()
    newLoginFrame = ttk.Frame(root)
    newLoginFrame.grid(row=0, column=0)
    username = tk.Entry(newLoginFrame)
    password = tk.Entry(newLoginFrame, show="\u2022")
    userLabel = tk.Label(newLoginFrame, text="Username")
    passwordLabel = tk.Label(newLoginFrame, text="Password")
    createUserButton = tk.Button(
        newLoginFrame,
        width="25",
        text="Login",
        command= lambda: validateUser(username.get(), password.get())
    )

    userLabel.grid(row=0, column=0)
    passwordLabel.grid(row=1, column=0)
    username.grid(row=0, column=1)
    password.grid(row=1, column=1)
    createUserButton.grid(row=2, columnspan=2)

def createUserFrame():
        
    clearFrame()
    newUserFrame = ttk.Frame(root)
    newUserFrame.grid(row=0, column=0)
    newUsername = tk.Entry(newUserFrame)
    newPassword = tk.Entry(newUserFrame)
    userLabel = tk.Label(newUserFrame, text="New Username")
    passwordLabel = tk.Label(newUserFrame, text="New Password")
    createUserButton = tk.Button(
        newUserFrame,
        width="25",
        text="Create User",
        command= lambda: makeNewUser(newUsername.get(), newPassword.get())
    )


    userLabel.grid(row=0, column=0)
    passwordLabel.grid(row=1, column=0)
    newUsername.grid(row=0, column=1)
    newPassword.grid(row=1, column=1)
    createUserButton.grid(row=2, columnspan=2)

def addWebsiteFrame():
    clearFrame()
    newCredentialFrame = ttk.Frame(root)
    newCredentialFrame.grid(row=0, column=0)
    newUsername = tk.Entry(newCredentialFrame)
    newPassword = tk.Entry(newCredentialFrame)
    newWebsite = tk.Entry(newCredentialFrame)
    userLabel = tk.Label(newCredentialFrame, text="Username")
    passwordLabel = tk.Label(newCredentialFrame, text="Password")
    websiteLabel = tk.Label(newCredentialFrame, text="Website")
    createUserButton = tk.Button(
        newCredentialFrame,
        width="25",
        text="Create new record",
        command= lambda: makeNewCredential(newUsername.get(), newPassword.get(), newWebsite.get())
    )
    userLabel.grid(row=0, column=0)
    passwordLabel.grid(row=1, column=0)
    websiteLabel.grid(row=2, column=0)
    newUsername.grid(row=0, column=1)
    newPassword.grid(row=1, column=1)
    newWebsite.grid(row=2, column=1)
    createUserButton.grid(row=3, columnspan=2)

def listWebsiteFrame():
    clearFrame()


root = tk.Tk()
root.title("Password Manager")

x, y = pyautogui.position()
fx = 600
fy = 400


root.geometry("%dx%d+%d+%d"%(fx, fy, x-fx/2, y-fy/2))

menuBar = tk.Menu(root)

fileMenu = tk.Menu(menuBar, tearoff=0)
loginMenu = tk.Menu(menuBar, tearoff=0)

menuBar.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Login", command=loginFrame)
fileMenu.add_command(label="Create User", command=createUserFrame)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.destroy)

menuBar.add_cascade(label="Functions", menu=loginMenu)
loginMenu.add_command(label="Add website Login", command=addWebsiteFrame)
loginMenu.add_command(label="List logins", command=listWebsiteFrame)
loginMenu.add_separator()
loginMenu.add_command(label="Logout", command= lambda: [menuBar.entryconfigure('Functions', state= 'disabled'), clearFrame()])

root.config(menu = menuBar)
menuBar.entryconfigure('Functions', state='disabled')
root.mainloop()