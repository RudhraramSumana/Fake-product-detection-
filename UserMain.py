import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
import os
import datetime
import webbrowser
import random
import threading
import pickle
from Blockchain import Blockchain
import PIL.Image
from PIL import ImageTk
from tkinter.filedialog import askopenfilename
import imageio  # Add this import to fix the issue


main = tk.Tk()
main.title("Authentication of products-Counterfeit Elimination Using BlockChain")
main.attributes('-fullscreen', True)

video_name = "C:/Users/SUMANA/OneDrive/Desktop/fake-product-detection-by-qr-using-blockchain/bg/hii.jpg"  # This is your video file path
video = imageio.get_reader(video_name)

def stream(label):
    for image in video.iter_data():
        frame_image = ImageTk.PhotoImage(PIL.Image.fromarray(image))
        label.config(image=frame_image)
        label.image = frame_image

my_label = tk.Label(main)
my_label.pack()
thread = threading.Thread(target=stream, args=(my_label,))
thread.daemon = 1
thread.start()

global filename
blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)

def authenticateProduct():
    text.delete('1.0', tk.END)
    filename_ = filedialog.askopenfilename(initialdir="original_barcodes")

    # Use OpenCV to read the QR code
    image = cv2.imread(filename_)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(image)
    if data:
        digital_signature = data
    else:
        text.insert(tk.END, "QR Code not detected!\n")
        return

    flag = True
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            arr = data.split("#")
            if arr[5] == digital_signature:
                output = ''
                text.insert(tk.END, "Uploaded Product Barcode Authentication Successful\n")
                text.insert(tk.END, "Details extracted from Blockchain after Validation\n\n")
                text.insert(tk.END, "Product ID: " + arr[0] + "\n")
                text.insert(tk.END, "Product Name: " + arr[1] + "\n")
                text.insert(tk.END, "Company/User Details: " + arr[2] + "\n")
                text.insert(tk.END, "Address Details: " + arr[3] + "\n")
                text.insert(tk.END, "Product Registered Date & Time: " + arr[4] + "\n")
                text.insert(tk.END, "Product QR-Code: " + str(digital_signature) + "\n")

                output = '<html><body><table border=1>'
                output += '<tr><th>Block No</th><th>Product ID</th><th>Product Name</th><th>Company/User Details</th><th>Address Details</th><th>Scan Date & Time</th><th>Product QR-Code No</th></tr>'
                output += '<tr><td>' + str(i) + '</td><td>' + arr[0] + '</td><td>' + arr[1] + '</td><td>' + arr[2] + '</td><td>' + arr[3] + '</td><td>' + arr[4] + '</td><td>' + str(digital_signature) + '</td></tr>'
                with open("output.html", "w") as f:
                    f.write(output)
                webbrowser.open("output.html", new=1)
                flag = False
                break
    if flag:
        text.insert(tk.END, str(digital_signature) + ", this hash is not present in the blockchain\n")
        text.insert(tk.END, "Uploaded Product Barcode Authentication Failed: FAKE")
        o1 = '<html><body><link rel="stylesheet" href="styles.css">'
        o1 += '<h1>FAKE PRODUCT!!</h1>'
        o1 += '</body></html>'
        with open("o1.html", "w") as f:
            f.write(o1)
        webbrowser.open("o1.html", new=1)

def authenticateProductWeb():
    text.delete('1.0', tk.END)
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, frame = cap.read()
        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            digital_signature = data
            break
        cv2.imshow("QR-Code scanner", frame)
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

    flag = True
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            arr = data.split("#")
            if arr[5] == digital_signature:
                output = ''
                text.insert(tk.END, "Uploaded Product Barcode Authentication Successful\n")
                text.insert(tk.END, "Details extracted from Blockchain after Validation\n\n")
                text.insert(tk.END, "Product ID: " + arr[0] + "\n")
                text.insert(tk.END, "Product Name: " + arr[1] + "\n")
                text.insert(tk.END, "Company/User Details: " + arr[2] + "\n")
                text.insert(tk.END, "Address Details: " + arr[3] + "\n")
                text.insert(tk.END, "Scan Date & Time: " + arr[4] + "\n")
                text.insert(tk.END, "Product QR-Code: " + str(digital_signature) + "\n")

                output = '<html><body><table border=1>'
                output += '<tr><th>Block No</th><th>Product ID</th><th>Product Name</th><th>Company/User Details</th><th>Address Details</th><th>Scan Date & Time</th><th>Product Digital Signature</th></tr>'
                output += '<tr><td>' + str(i) + '</td><td>' + arr[0] + '</td><td>' + arr[1] + '</td><td>' + arr[2] + '</td><td>' + arr[3] + '</td><td>' + arr[4] + '</td><td>' + str(digital_signature) + '</td></tr>'
                with open("output.html", "w") as f:
                    f.write(output)
                webbrowser.open("output.html", new=1)
                flag = False
                break
    if flag:
        text.insert(tk.END, str(digital_signature) + ", this hash is not present in the blockchain\n")
        text.insert(tk.END, "Uploaded Product Barcode Authentication Failed: FAKE")
        o1 = '<html><body><link rel="stylesheet" href="styles.css">'
        o1 += '<h1>FAKE PRODUCT!!</h1>'
        o1 += '</body></html>'
        with open("o1.html", "w") as f:
            f.write(o1)
        webbrowser.open("o1.html", new=1)

def run12():
    main.destroy()
    import Main

scanButton = tk.Button(main, text="Home Page", bg="white", command=run12)
scanButton.place(x=1400, y=200)
scanButton.config(font=('times', 13, 'bold'))

scanButton = tk.Button(main, text="Authenticate Scan", command=authenticateProduct)
scanButton.place(x=420, y=300)
scanButton.config(font=('times', 13, 'bold'))

scanButton = tk.Button(main, text="Authenticate web Scan", command=authenticateProductWeb)
scanButton.place(x=850, y=300)
scanButton.config(font=('times', 13, 'bold'))

text = tk.Text(main, height=15, width=100)
scroll = tk.Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=300, y=450)
text.config(font=('times', 13, 'bold'))

main.config(bg='cornflower blue')
main.mainloop()