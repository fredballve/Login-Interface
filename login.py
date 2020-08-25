import tkinter as tk
from cryptography.fernet import Fernet


def clear_entries():
    name_entry.delete(0,"end")
    email_entry.delete(0,"end")
    password_entry.delete(0,"end")

def login(name,email,password):
    if check_name(name,email,password)==0:
        label_warning["text"]="Login successful"
    elif check_name(name,email,password)==1:
        label_warning["text"]="User not found"
    elif check_name(name,email,password)==2:
        label_warning["text"]="Wrong Password"
    clear_entries()
    
def register(name,email,password):
    if check_name(name,email,password) == 3:
        label_warning["text"]="User already registered"
    elif check_name(name,email,password) == 4:
        label_warning["text"]="Invalid Email"
    elif check_name(name,email,password) == 5:
        label_warning["text"]="Password must be at least 8 characters"
    elif check_name(name,email,password) == 6:
        data["name"].append(name)
        data["email"].append(email)
        data["password"].append(password)
        label_warning["text"]="Register successful"
        clear_entries()
    
def check_name(name,email,password):
    """
        0 = Login successful
        1 = User not found
        2 = Wrong Password
        3 = User already registered
        4 = Invalid Email
        5 = Password must be at least 8 characters
        6 = OK to register
    """
    return 6

    

def get_key():
    try:
        r_file = open("secret.key","rb")
        key = r_file.read()
        key = Fernet(key)
        return key
    except FileNotFoundError:
        print("key not found, generating other...")
        key = Fernet.generate_key()
        with open("secret.key", "wb") as w_file:
            w_file.write(key)
            key = Fernet(key)
            return key
        print("error")
    except:
        print("error")
        
def data_encrypt(key):
    formated_data = ""
    for i in range(len(data["name"])):
        formated_data += data["name"][i]+ "," + data["email"][i] + "," + data["password"][i] + ";"
    print(formated_data)
    enc_data = key.encrypt(formated_data.encode())
    with open("data.txt","wb") as w_file:
        w_file.write(enc_data)

def data_decrypt(key):
    try:
        with open("data.txt","rb") as r_file:
            enc_data= r_file.read()
        dec_data = key.decrypt(enc_data)
        dec_data= dec_data.decode()
        data_tuple = tuple(map(str,dec_data.split(';')))
        for line in range(len(data_tuple)-1):
            aux_tuple = str(data_tuple[line])
            i,j,k = tuple(map(str,aux_tuple.split(',')))
            data["name"].append(i)
            data["email"].append(j)
            data["password"].append(k)
        print(data)
    except:
        print("Error")

data = {"name":[],
        "email":[],
        "password":[]} 
"""    

data = {"name":["jao","123"],
        "email":["bbb","123"],
        "password":["aaa","123"]}
"""

key= get_key()
#data_encrypt(key)
data_decrypt(key)


root = tk.Tk()

canvas = tk.Canvas(root)
canvas.pack()

frame = tk.Frame(root)
frame.place(relwidth=1,relheight=1)


label_name = tk.Label(frame,text="Username:",font=("Courier",10))
label_name.place(relx=0.2,rely=0,relwidth=0.6,relheight=0.05)
name_entry = tk.Entry(frame,font="Courier",bd=2,justify="center")
name_entry.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.125)

label_email = tk.Label(frame,text="Email:",font=("Courier",10))
label_email.place(relx=0.2,rely=0.25,relwidth=0.6,relheight=0.05)
email_entry = tk.Entry(frame,font="Courier",bd=2,justify="center")
email_entry.place(relx=0.2,rely=0.35,relwidth=0.6,relheight=0.125)

label_password = tk.Label(frame,text="Password:",font=("Courier",10))
label_password.place(relx=0.2,rely=0.5,relwidth=0.6,relheight=0.05)
password_entry = tk.Entry(frame,show="*",font="Courier",bd=2,justify="center")
password_entry.place(relx=0.2,rely=0.6,relwidth=0.6,relheight=0.125)

Login_button = tk.Button(frame, text="Login",font="Courier",  fg = 'red',bd=4, command=lambda:login(name_entry.get(),email_entry.get(),password_entry.get()))
Login_button.place(relx=0,rely=0.8,relwidth=.5,relheight=0.2)

Register_button = tk.Button(frame, text="Register",font="Courier",  fg = 'red',bd=4, command=lambda:register(name_entry.get(),email_entry.get(),password_entry.get()))
Register_button.place(relx=0.5,rely=0.8,relwidth=.5,relheight=0.2)

label_warning = tk.Label(frame,text="",font=("Courier",10),fg='red')
label_warning.place(relx=0,rely=0.725,relwidth=1,relheight=0.075)
root.mainloop()
