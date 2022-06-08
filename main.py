import tkinter
import tkinter.messagebox
import json
from cryptography.fernet import Fernet
import os
import sys

config = {
  "title": "Kakobubba",
  "key": b"e3eJttDz2_N2dnVFvaOeQbhZyceSP-tTxMxDwGD8idc=",
  "baseAccountSystem": "gAAAAABin8VnZXmOl-Hr2zMF9SpSSPFUuG3VSXRyYtve8hOzJvBXlPkDjyBmg2qMaZN3dgABB4RN0rFTdmKmBzVGxDbQn-jvfA=="
}

if not os.path.exists("accountSystem"):
  with open("accountSystem", "w+") as f:
    f.write(config["baseAccountSystem"])
fernet = Fernet(config["key"])
with open('accountSystem', 'rb') as enc_file:
  encrypted = enc_file.read()
decrypted = fernet.decrypt(encrypted)
accountSystem = json.loads(decrypted)


class App:
  def __init__(self):
    self.temp = True
    self.authkey = None
    self.root = tkinter.Tk()
    self.root.title(config["title"])
    self.root.geometry("426x240")
    self.root.resizable(0, 0)
    self.menuBarItems = [
      ["Home", lambda:self.openScreen("homeScreen")],
      ["About", lambda:self.openScreen("aboutScreen")],
      ["Stuff", lambda:self.openScreen("stuffScreen")],
      ["ASys", lambda:self.openScreen("aSysScreen")],
      ["Sign In", lambda:self.openScreen("loginScreen")],
      ["Sign Up", lambda:self.openScreen("signupScreen")]
    ]
    
    self.titleBar = tkinter.Frame(width=426)
    self.title = tkinter.Label(self.titleBar, text=config["title"], font='Helvetica 18 bold')
    self.title.pack()
    self.titleBar.pack()

    self.menuBar = tkinter.Frame()
    self.menuBarItemsCode = []
    for i in range(len(self.menuBarItems)):
      self.menuBarItemsCode.append(tkinter.Button(self.menuBar, text=self.menuBarItems[i][0], borderwidth = 0, command=self.menuBarItems[i][1]))
    for i in range(len(self.menuBarItemsCode)):
      self.menuBarItemsCode[i].grid(column = i, row = 0)
    self.menuBar.pack()
    
    self.content = tkinter.Frame(self.root)

    self.screens = [
      ["homeScreen", tkinter.Frame(self.content)],
      ["aboutScreen", tkinter.Frame(self.content)],
      ["stuffScreen", tkinter.Frame(self.content)],
      ["aSysScreen", tkinter.Frame(self.content)],
      ["loginScreen", tkinter.Frame(self.content)],
      ["signupScreen", tkinter.Frame(self.content)]
    ]

    tkinter.Button(self.screens[3][1], text="Erase Account System", borderwidth = 0, command = self.eraseAccountSystem).grid(row = 0, column = 0)
    
    tkinter.Label(self.screens[4][1], text="Username: ").grid(row = 0, column = 0)
    self.username = tkinter.Entry(self.screens[4][1], borderwidth = 0)
    self.username.grid(row = 0, column = 1)
    tkinter.Label(self.screens[4][1], text="Password: ").grid(row = 1, column = 0)
    self.password = tkinter.Entry(self.screens[4][1], show="*", borderwidth = 0)
    self.password.grid(row = 1, column = 1)
    tkinter.Button(self.screens[4][1], text="Sign In", borderwidth = 0, command = self.signIn).grid(row = 2, column = 0)
    
    tkinter.Label(self.screens[5][1], text="Username: ").grid(row = 1, column = 0)
    self.suUsername = tkinter.Entry(self.screens[5][1], borderwidth = 0)
    self.suUsername.grid(row = 1, column = 1)
    tkinter.Label(self.screens[5][1], text="Password: ").grid(row = 2, column = 0)
    self.suPassword = tkinter.Entry(self.screens[5][1], show="*", borderwidth = 0)
    self.suPassword.grid(row = 2, column = 1)
    tkinter.Label(self.screens[5][1], text="Confirm Password: ").grid(row = 3, column = 0)
    self.suConfirmPassword = tkinter.Entry(self.screens[5][1], show="*", borderwidth = 0)
    self.suConfirmPassword.grid(row = 3, column = 1)
    tkinter.Button(self.screens[5][1], text="Sign Up", borderwidth = 0, command = self.signUp).grid(row = 4, column = 0)
    self.openScreen("homeScreen")

    self.content.pack()
  def openScreen(self, screenName):
    for i in range(len(self.screens)):
      if self.screens[i][0] == screenName:
        self.screens[i][1].grid()
      else:
        self.screens[i][1].grid_forget()
  def signUp(self):
    if self.suConfirmPassword.get() == "" or self.suPassword.get() == "" or self.suUsername.get() == "":
      tkinter.messagebox.showwarning(config["title"], "Required field(s) are blank")
    elif self.suPassword.get() != self.suConfirmPassword.get():
      tkinter.messagebox.showwarning(config["title"], "Passwords do not match.")
    elif self.suUsername.get() == self.suPassword.get():
      tkinter.messagebox.showwarning(config["title"], "Password and username cannot match.")
    else:
      self.temp = True
      for i in range(len(accountSystem)):
        if accountSystem[i][0] == self.suUsername.get():
          if tkinter.messagebox.askokcancel(config["title"], "This account already exists. Go to login?"):
            self.openScreen("loginScreen")
          self.temp = False
          break
      if self.temp == True:
        accountSystem.append([self.suUsername.get(), self.suPassword.get()])
        tkinter.messagebox.showinfo(config["title"], "Sucess!")
        self.openScreen("loginScreen")
        self.username.insert(0, self.suUsername.get())
        self.password.insert(0, self.suPassword.get())
  def signIn(self):
    self.temp == False
    for i in range(len(accountSystem)):
      if accountSystem[i][0] == self.username.get():
        if accountSystem[i][1] == self.password.get():
          tkinter.messagebox.showinfo(config["title"], "Sucess!")
          self.temp == True
          break
    if self.temp == False:
      tkinter.messagebox.showwarning(config["title"], "Incorrect username or password.")
  
  def eraseAccountSystem(self):
    if tkinter.messagebox.askokcancel(config["title"], "Are you sure you want to erase the account system?"):
      self.root.quit()
      os.remove("accountSystem")
      with open("accountSystem", "w+") as f:
        f.write(config["baseAccountSystem"])
      tkinter.messagebox.showinfo(config["title"], "Sucessfully erased the account system. The application will now quit.")
      sys.exit()
          
  def go(self):
    self.root.mainloop()
    
App().go()

with open('accountSystem', 'w', encoding='utf-8') as f:
    json.dump(accountSystem, f, ensure_ascii = False, indent = 4)
fernet = Fernet(config["key"])
with open('accountSystem', 'rb') as file:
    original = file.read()
encrypted = fernet.encrypt(original)
with open('accountSystem', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)
