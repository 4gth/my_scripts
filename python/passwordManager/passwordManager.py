#!/usr/bin/env python
# passwordManager.py
# Date of development 11/09/2023

# This is a simple password manager written in python.
# It allows a user to create a login profile.
# Once logged in it allows the user to view and add passwords.

# Written by Justin Manners.

# I am sure there are many better ways of making this work.
# I have only just started using python, I wanted to make it all from
# native modules.

# Import modules needed for script.
import csv
import sys
import os.path
import hashlib
from getpass import getpass
from urllib.parse import urlparse
from time import sleep
from progress.bar import Bar


# Some global variables, this program needs only to create 2 extra files.
userdb = "user.db"
passdb = "passwd.db"


class PasswordEntry:  #   class for functions that deal with creating new
    #                           credentials.
    #                           cryptFile() is used to encrypt and decrypt the
    #                           passwd.db file
    #                           urlValidator() will check the URL if it is valid.
    #                           for this exercise we are looking to only store
    #                           valid URLs.
    #                           createEntry() will take user credentials and write
    #                           them to the passwd.db file.
    isCrypted = False

    # funcion for creating a PasswordEntry object.
    def __init__(self, url, user, passw, passfile):
        self.url = url
        self.user = user
        self.password = passw
        self.passfile = passfile
        self.cryptFile()

    # function for en/decrypting file, run=True will run encryption algorthim.
    def cryptFile(self, run=False, key="BAD_CRYPTO"):
        xorByte = key.encode("utf-8")
        # open passwd.db as bytes type
        # for each byte in passwd.db XOR it with key=
        if run:
            with open(passdb, "rb") as passwords:
                outXorList = []
                while True:  # if file still has bytes remaining.
                    byte = passwords.read(1)
                    if not byte:
                        break
                    outXor = bytes([byte[0] ^ xorByte[0]])
                    outXorList.append(outXor)
            # once all bytes are XORd write XORd bytes to passwd.db
            with open(passdb, "wb") as passwords:
                for xordbytes in outXorList:
                    passwords.write(xordbytes)
            PasswordEntry.isCrypted != PasswordEntry.isCrypted
        # check to see if the passwd.db file is decrypted or not using
        # a simple string match on 'http'.
        with open(passdb, "r") as passwords:
            # if http is in row checkurl += 1
            checkurl = [rows for rows in passwords if "http" in rows]
            if len(checkurl) > 0:  # if list is > 0 it contains plaintext
                # with http string meaning not crypted.
                PasswordEntry.isCrypted = False
                return False
            else:
                PasswordEntry.isCrypted = True
                return True

    # function for validating URL,this will ensure entries stay nice and formatted.
    def urlValidator(self):
        try:
            result = urlparse(self.url)  # this will return True of False.
            return all([result.scheme, result.netloc])
        except:
            return False

    # function for writing entry into the passwd.db file.
    def createEntry(self):
        # check to see if passwd.db is encrypted, decrypt if necessary

        if PasswordEntry.isCrypted:
            self.cryptFile(True)
            PasswordEntry.isCrypted = False
            # make sure entry contains valid URL,
        if self.urlValidator():  # if it does write CSV entry for credentials.
            with open(self.passfile, "a+") as f:
                dbWriter = csv.writer(f)
                dbWriter.writerow([self.url, self.user, self.password])
                print("New website credentials added successfully!")
                return True
        else:
            print("malformed URL")  # if URL is no good return False.
            return False


class Hashing:  #   class for creating pw manager user hashes, no user
    #                           credentials are stored in plain text.
    #                           createHash() will take username and password, salt
    #                           it and return the hash.
    #                           hashToFile() will take a hash and write it to the
    #                           user.db file.

    # function for creating a Hashing object.
    def __init__(self, username, password, userfile):
        self.username = username
        self.password = password
        self.userfile = userfile

    # function for creating a hash based on arguments username and password.
    def createHash(self, username, password):
        inputSalt = "This is not how you should hash passwords"
        dbPass = password + inputSalt + username
        hashed = hashlib.md5(dbPass.encode()).hexdigest()  # simple hashing of
        return hashed  # user/passwords

    # fucntion for writing login information to user.db file
    def hashToFile(self):
        with open(self.userfile, "a+") as userlist:  # open user.db and write hash
            userdbList = []
            userdbList.append(self.createHash(self.username, self.password))
            userlist.writelines(userdbList)
            userlist.writelines("\n")


class User:  #   class for functions that manager user credentials.
    # function for creating User object.
    def __init__(self, userhash, userfile):
        self.userhash = userhash
        self.userfile = userfile

    # function for checking user.db hashes against a userhash passed to the object.
    def validateUser(self):
        with open(self.userfile, "r") as userlist:  # open user.db
            row = []  # load hashes into row[]
            for rows in userlist:  # check userhash to see
                row.append(rows.strip("\n"))  # if it already exsist.
            for hash in row:  # in user.db
                if self.userhash == hash:
                    print("User exsists.")
                    return True
            else:
                return False


class Menus:  #   class for functions that create and format Menus.
    #                           mainMenu() allows user to create a new user or login.
    #                           loggedIn() allows loggined in user to view/create
    #                           passwd.db entries.
    #                           exit() function to kill program.

    # all functions in this class are the same, they create formatted strings
    # and print to terminal.

    # menu object initialiser.
    def __init__() -> None:
        pass

    # main menu for password manager
    def mainMenu():
        print(
            """
           
            ---------------------------------------------
            |   1: Create new user for password manager.|
            |   2: Login to password manager.           |
            |   3: Exit password manager.               |
            ---------------------------------------------   
                        """
        )

    # menu for when a user has sucessfully logged in.
    def loggedIn():
        print(
            """
           
            ---------------------------------------------
            |   1: List saved URLs.                     |
            |   2: Add new password.                    |
            |   3: Log out and exit to main menu.       |
            ---------------------------------------------   
                        """
        )

    # menu for displaying credentials stored in passwd.db
    def displayEntries(passfile):
        with Bar(
            "Fetching saved credentials...",
        ) as bar:
            for i in range(100):
                sleep(0.005)
                bar.next()
        with open(passfile, "r") as f:
            dbReader = csv.reader(f)
            number = 1
            
            for row in dbReader:
                with Bar(
                    "decrypting entry..."
                ) as bar:
                    for i in range(100):
                        sleep(0.005)
                        bar.next()
                try:
                    print(
                        f""" 
            ====
            |  | {number}:>
            |  | Website: {row[0]}
            |  | Username: {row[1]}
            |  | Password: {row[2]}
            ====
                """
                    )
                    number += 1
                    input(" Press any key for next entry.")
                except:
                    print("malformed entry")
            print(
                """
            =============================================
            ============================================="""
            )
            
            

    # function to kill program.
    def exit():
        print("exiting")
        with Bar(
            "cleaning up and securing...",
        ) as bar:
            for i in range(100):
                sleep(0.04)
                bar.next()
        sys.exit(0)


class UserInput:  #   class for handling user input via the terminal.
    #                           makeSelection() asks for input and returns int
    #                           type for selection.
    #                           login() asks for user and password, returns str
    #                           type for each.
    #                           getWebsite() asks user for URL, login name, and
    #                           password. reurns str type for each .
    #                           createUser() asks the user for new login details
    #                           returns str type for username and password.

    # initialise UserInput object.
    def __init__():
        pass

    # main function for asking for menu selections.
    def makeSelection():
        while True:
            userInput = input("Please make a selection: ")
            try:  # take userInput and check if it is int() between 1 -3
                userSelection = int(userInput)
                if 1 <= userSelection <= 3:
                    return userSelection
                else:  # if userInput > 3
                    print(
                        f"Invalid input: {userSelection},"
                        "input must be number between 1-3"
                    )
            except ValueError:  # if userInput not int()
                print("Invalid input: Input must be number between 1-3")

    # function for asking for login credentials
    def login():
        print("Please enter Username and Password.")
        userName = input("Username: ")
        passWord = getpass()

        return userName, passWord

    # function for asking for new website credentials
    def getWebsite():
        inputurl = input("Please input URL: ")
        inputuser = input("Please input website Username: ")
        inputpassword = getpass("Please input website password: ")
        return inputurl, inputuser, inputpassword

    # function for asking for new user credentials
    def createUser():
        newUser = input("Please input new username for password manager: ")
        newPassword = getpass("Please input new password for password manager: ")
        confirmNewPass = getpass("Please input password again to confirm: ")
        if newPassword == confirmNewPass and newUser:
            return newUser, newPassword
        else:
            print("Password mismatch please try again.")
            return False


def navigate():  # function for mainMenu logic.
    Menus.mainMenu()
    # call makeSelection() using match: case: determine what the user wants.
    match UserInput.makeSelection():
        # case 1 is create new user.
        case 1:
            print("Create new User Selected!")
            # get input from user, create hash and check if hash is in user.db
            while True:
                rawUser = UserInput.createUser()
                if rawUser:
                    hashedUser = Hashing.createHash("", *rawUser)
                    if not User(hashedUser, userdb).validateUser():
                        Hashing(*rawUser, userdb).hashToFile()
                        with Bar(
                            "Hashing User...",
                        ) as bar:
                            for i in range(100):
                                sleep(0.01)
                                bar.next()
                        print("New user created, you can now login!")
                        navigate()
                    else:
                        navigate()
        # case 2 is login to password manager.
        case 2:
            print("Login to password manager selected!")
            # get user login details, create hash check if hash is in user.db
            # if it is move to menuLoggedIn()
            attempts = 0
            while attempts < 3:
                userLogin = UserInput.login()
                hashedLogin = Hashing.createHash("", *userLogin)
                validateLoginAttempt = User(hashedLogin, userdb).validateUser()
                if validateLoginAttempt:
                    menuLoggedIn()
                else:
                    attempts += 1
                    print(f"Invalid login. {3 - attempts} attempts remaining.")
            if attempts == 3:
                navigate()
        # case 3 is to exit the program.
        case 3:
            # check if passwd.db is encrypted, if False: encrypt
            # if True: exit()
            if not PasswordEntry.isCrypted:
                PasswordEntry.cryptFile("", True)
            Menus.exit()


def menuLoggedIn():  # function for Menus logic when the user is logged in.
    Menus.loggedIn()
    # once logged in, check passwd.db if it is encrypted.
    # if True: de-crypt
    # if False ask for input
    if PasswordEntry.isCrypted:
        PasswordEntry.cryptFile("", True)
    # call makeSelection() using match: case: determine what the user wants.
    match UserInput.makeSelection():
        # case 1 is to display passwd.db entries
        case 1:
            Menus.displayEntries(passdb)
            menuLoggedIn()
        # case 2 is to create a new entry in passwd.db
        case 2:
            createNewCredential = UserInput.getWebsite()
            if PasswordEntry(*createNewCredential, passdb).createEntry():
                menuLoggedIn()
            else:
                menuLoggedIn()
        # case 3 is to return to the mainMenu.
        case 3:
            # if passwd.db is decrypted: encrypt
            # go to mainMenu via navigate()
            if not PasswordEntry.isCrypted:
                PasswordEntry.cryptFile("", True)
            navigate()


def main():  # function to run start of the program and check if
    # user.db and passwd.db exsist, and create if needed.

    # check if file exsists in directory, if not use w+ to create
    if not os.path.isfile(userdb):
        open(userdb, "w+").close()
    if not os.path.isfile(passdb):
        open(passdb, "w+").close()
    # check state of passwd.db
    if not PasswordEntry.isCrypted:
        PasswordEntry.cryptFile("")
    # call navigate to start main program.
    with Bar(
        "Initialising...",
    ) as bar:
        for i in range(100):
            sleep(0.01)
            bar.next()
    navigate()


# Start of program.
main()
