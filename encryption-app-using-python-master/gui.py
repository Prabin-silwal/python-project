from tkinter import * 
from tkinter import filedialog,messagebox
import database
from chiper import *
from file import *
def popup(flag):
    choice=0
    if flag==False:
        message="Your message is encryptd and store in 'chiper.txt'.To Preview click 'Ok'."
        choice=1
    else:
        message="You chiper is decrypted and store in 'message.txt'.To Preview click 'Ok'."
        choice=2
    response=messagebox.askokcancel("Chiper",message)
    if response==1:
        decode=file.datafromfile(choice)
        messagebox.showinfo("Preview",decode)

def decryption():
    flag=True
    if clicked2.get()=="Ceasar":
        chiper_txt=caesar_file.datafromfile2(home.filename)
        c1=caesar(chiper_txt,key.get())
        plain_txt=c1.decrypt()
        caesar_file.outputinfile(plain_txt)
    elif clicked2.get()=="Playfair":
        chiper_txt=playfair_file.datafromfile2(home.filename)
        p1=playfair(chiper_txt,key.get())
        plain_txt=p1.decrypt()
        playfair_file.outputinfile(plain_txt)
    elif clicked2.get()=="Raps alogrithm":
        chiper_txt,key_list,key_list2=raps_file.datafromfile(home.filename)
        r1=raps(chiper_txt,key.get())
        plain_txt=r1.decrypt(key_list,key_list2)
        raps_file.outputinfile(plain_txt)
    popup(flag)

def encryption():
    flag=False
    if clicked1.get()=="Ceasar":
        c1=caesar(plain_text.get(),key.get())
        chiper_txt=c1.encrypt() 
        print(chiper_txt)
        caesar_file.displayfile(chiper_txt)
    elif clicked1.get()=="Playfair":
        p1=playfair(plain_text.get(),key.get())
        chiper_txt=p1.encrypt()
        playfair_file.displayfile(chiper_txt)
    elif clicked2.get()=="Raps alogrithm":
        r1=raps(plain_text.get(),key.get())
        chiper_txt,key_list,key_list2=r1.encrypt()
        raps_file.displayfile(chiper_txt,key_list,key_list2)
    popup(flag)

def open(): 
    home.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("txt files", "*.txt"),("all files", "*.*")))

def tomainwindow():
    home.withdraw()
    main_window()

def home_gui():
    global home,clicked1,clicked2,key,plain_text
    clicked1,clicked2,key,plain_text=None,None,None,None
    home=Toplevel(window)                                                    
    home.title("Home")
    home.geometry("400x400")
    window.withdraw()
    
    option=[
        "Raps alogrithm",
        "Ceasar",
        "Playfair"
    ]
    clicked1=StringVar()
    clicked2=StringVar()
    key=StringVar()
    plain_text=StringVar()
    clicked1.set(option[0])
    clicked2.set(option[0])

    frame1=LabelFrame(home, text="To encrypt", padx=5,pady=5)
    frame1.pack(padx=0,pady=0)

    Label(frame1,text="Choose chiper :").grid(row=0)
    drop=OptionMenu(frame1, clicked1, *option)
    drop.grid(row=0,column=1)
    Label(frame1,text="Plain Text").grid(row=1)
    Entry(frame1,textvariable=plain_text).grid(row=1, column=1)
    Label(frame1,text="Keys").grid(row=2)
    Entry(frame1,textvariable=key).grid(row=2, column=1)

    Button(frame1,text="Encrypt",height="2",width="30", command=encryption).grid(row=3)

    frame2=LabelFrame(home, text="To decrypt", padx=5,pady=5)
    frame2.pack(padx=0,pady=0)
    
    Label(frame2,text="Choose chiper :").grid(row=0)
    drop=OptionMenu(frame2, clicked2, *option)
    drop.grid(row=0,column=1)
    Label(frame2,text="File :").grid(row=1)
    Button(frame2,text="Broswe file",height="2",width="10",command=open).grid(row=1,column=1)
    Label(frame2,text="Keys").grid(row=2)
    Entry(frame2,textvariable=key).grid(row=2, column=1)
    
    Button(frame2,text="Decrypt",height="2",width="30",command=decryption).grid(row=3)

    Button(home,text="Log out",height="1",width="5",command=tomainwindow).pack()
    home.mainloop()

def checkinglogin():
    val=database.dbvalue(usernameL.get(),passwordL.get())
    if val==True:
        home_gui()
    else:
        main_window(False)
        
def register_to_db():
    database.dbinsert(first_name.get(),last_name.get(),usernameS.get(),passwordS.get())
    screen1.withdraw()
    main_window()

def checkingpw():
    if not first_name.get().strip() or not last_name.get().strip() or not usernameS.get().strip() or not passwordS.get().strip():
        register(False)

    else:
        if passwordS.get()==con_passwordS.get():
            register_to_db()
        else:
            register("not_match")

def register(val=True):
    global screen1
    global first_name, last_name, usernameS, passwordS, con_passwordS
    first_name, last_name, usernameS, passwordS, con_passwordS=None,None,None,None,None
    screen1 =Toplevel(window)
    screen1.title("Register")
    screen1.geometry("300x300")
    window.withdraw()

    first_name=StringVar()
    last_name=StringVar()
    usernameS=StringVar()
    passwordS=StringVar()
    con_passwordS=StringVar()

    Label(screen1, text="First Name : ").grid(row=0)
    Entry(screen1,textvariable=first_name).grid(row=0, column=1)

    Label(screen1, text="Last Name : ").grid(row=2)
    Entry(screen1,textvariable=last_name).grid(row=2, column=1)

    Label(screen1,text="Username : ").grid(row=4)
    Entry(screen1,textvariable=usernameS).grid(row=4, column=1)

    Label(screen1,text="Password : ").grid(row=6)
    Entry(screen1,textvariable=passwordS,show="*").grid(row=6, column=1)

    Label(screen1,text="Confirm pw:").grid(row=8)
    Entry(screen1,textvariable=con_passwordS,show="*").grid(row=8, column=1)

    for i in range(1,11):
        if i%2!=0:
            Label(screen1,text="").grid(row=i)

    Button(screen1,text="Sign up",height="2",width="30",command=checkingpw).grid(rows=10,column=1)
    if val==False:
        Label(screen1,text="Note:The input is empty!!!\n Use 'string' as the input. ").grid(row=12 )
    elif val=="not_match":
        Label(screen1,text="Note:The password doesnot match!!!. ").grid(row=12 )

def main_window(val=True):
    global window, usernameL, passwordL
    usernameL, passwordL=None,None
    window=Tk()
    window.geometry("300x300")
    window.title("Log In")
    
    usernameL=StringVar()
    passwordL=StringVar()
    
    Label(window,text="Username:").pack()
    Entry(window,textvariable=usernameL).pack()
    Label(window,text="Password:").pack()
    Entry(window,textvariable=passwordL,show="*").pack()
   
    Button(window,text="Login",height="2",width="30",command=checkinglogin).pack()
    Button(window,text="Register",height="2",width="30",command=register).pack()
    Label(window,text="").pack()
    if val==False:
        Label(window,text="Invalid username or password. Try again with valid one.").pack()
        
    window.mainloop()
main_window() 