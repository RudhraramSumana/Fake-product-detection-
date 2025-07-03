import tkinter
from tkinter import messagebox
from tkinter import *
from hashlib import sha256
import os
import datetime
import qrcode
import random
from PIL import ImageTk, Image
import pickle

from Blockchain import Blockchain  # Ensure Blockchain.py is in the same directory as this script

# Initialize main window
main = tkinter.Tk()
main.title("Authentication of Products - Counterfeit Elimination Using Blockchain")
main.attributes('-fullscreen', True)
main.config(bg="lightblue")  # Set background to light blue

# Global variables
global qr_render

# Blockchain initialization
blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)

# Add product functionality
def addProduct():
    text.delete('1.0', END)
    pid = tf1.get()
    name = tf2.get()
    user = tf3.get()
    address = tf4.get()

    if not (pid.strip() and name.strip() and user.strip() and address.strip()):
        messagebox.showerror("Error", "All fields are required. Please fill them out.")
        return

    digital_signature = sha256(hex(random.getrandbits(128)).encode('utf-8')).hexdigest()

    try:
        qr_path = f'original_barcodes/{pid}productQR.png'
        QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        QRcode.add_data(digital_signature)
        QRcode.make(fit=True)
        QRimg = QRcode.make_image().convert('RGB')
        QRimg.save(qr_path)
    except Exception as e:
        messagebox.showerror("Error", f"QR Code generation failed: {e}")
        return

    try:
        current_time = datetime.datetime.now()
        data = f"{pid}#{name}#{user}#{address}#{current_time}#{digital_signature}"
        blockchain.add_new_transaction(data)
        blockchain.mine()
        blockchain.save_object(blockchain, 'blockchain_contract.txt')

        # Insert product details into the text box
        text.insert(END, f"Product ID: {pid}\n")
        text.insert(END, f"Product Name: {name}\n")
        text.insert(END, f"Company/User Details: {user}\n")
        text.insert(END, f"Address Details: {address}\n")
        text.insert(END, f"Registered Date & Time: {current_time}\n")
        text.insert(END, f"Digital Signature: {digital_signature}\n\n")

        # Load and display the QR code at the extreme right inside the text box
        img = Image.open(qr_path).resize((150, 150))  # Resize for better fit
        qr_render = ImageTk.PhotoImage(img)

        canvas = Canvas(text, width=150, height=150, bg="white", highlightthickness=0)
        canvas.create_image(0, 0, anchor=NW, image=qr_render)

        # Place the canvas to the extreme right inside the text widget
        text.insert(END, "\n")  # Add a new line before placing the QR code
        text.window_create(END, window=canvas)
        text.insert(END, "\n")  # Ensure spacing after the QR code

        tf1.delete(0, 'end')
        tf2.delete(0, 'end')
        tf3.delete(0, 'end')
        tf4.delete(0, 'end')

        messagebox.showinfo("Success", "Product saved successfully with Blockchain entry!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save product: {e}")

# Search product functionality
def searchProduct():
    text.delete('1.0', END)
    pid = tf1.get()
    flag = True

    if len(pid) > 0:
        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                arr = data.split("#")
                if arr[0] == pid:
                    text.insert(END, "Product Details extracted from Blockchain using Product ID : " + pid + "\n\n")
                    text.insert(END, f"Product ID: {arr[0]}\n")
                    text.insert(END, f"Product Name: {arr[1]}\n")
                    text.insert(END, f"Company/User Details: {arr[2]}\n")
                    text.insert(END, f"Address Details: {arr[3]}\n")
                    text.insert(END, f"Product Registered Date & Time: {arr[4]}\n")
                    text.insert(END, f"Product Qr Code: {arr[5]}\n")
                    flag = False
                    break
    if flag:
        text.insert(END, "Given product ID does not exist")

# Navigation to home page
def run13():
    main.destroy()
    import Main

# UI Components
font = ('times', 30, 'bold')
title = Label(main, text='Authentication of Products - Counterfeit Elimination Using Blockchain', bg="green", fg='black')
title.config(font=font)
title.place(x=300, y=10)

font1 = ('times', 13, 'bold')

l1 = Label(main, text='Product ID:', font=font1, bg="lightblue", fg="black")
l1.place(x=300, y=150)

tf1 = Entry(main, width=50)
tf1.config(font=font1)
tf1.place(x=500, y=150)

l2 = Label(main, text='Product Name:', font=font1, bg="lightblue", fg="black")
l2.place(x=300, y=200)

tf2 = Entry(main, width=50)
tf2.config(font=font1)
tf2.place(x=500, y=200)

l3 = Label(main, text='Company/User Details:', font=font1, bg="lightblue", fg="black")
l3.place(x=300, y=250)

tf3 = Entry(main, width=50)
tf3.config(font=font1)
tf3.place(x=500, y=250)

l4 = Label(main, text='Address Details:', font=font1, bg="lightblue", fg="black")
l4.place(x=300, y=300)

tf4 = Entry(main, width=50)
tf4.config(font=font1)
tf4.place(x=500, y=300)

font2 = ('times', 15, 'bold')

# Larger buttons
saveButton = Button(main, text="Save Product with Blockchain Entry", font=font2, width=25, height=2, command=addProduct, bg="lightgreen")
saveButton.place(x=400, y=400)

searchButton = Button(main, text="Retrieve Product Data", font=font2, width=25, height=2, command=searchProduct, bg="lightblue")
searchButton.place(x=800, y=400)

# Reduced size for text box
text = Text(main, height=15, width=80, bg="white", fg="black")
text.place(relx=0.5, rely=0.75, anchor="center")  # Position below buttons
text.config(font=font2)

scanButton = Button(main, text="Home Page", bg="dark orange", font=font2, width=15, height=2, command=run13)
scanButton.place(x=1300, y=150)

main.mainloop()