import tkinter as tk
from cryptography.fernet import Fernet

def check_user():
    pass

    

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
    
    formated_data = ""
    for line in dec_data:
        formated_data += line
    #print(formated_data)

data = {"name":[],
        "email":[],
        "password":[]} 
"""    
data = {"name":["jao","123"],
        "email":["bbb","123"],
        "password":["aaa","123"]}
"""

#widget = Entry(parent, show="*", width=15)

key= get_key()
#data_encrypt(key)
data_decrypt(key)


root = tk.Tk()

canvas = tk.Canvas(root)
canvas.pack()

#root.mainloop()