import tkinter as tk
from tkinter import Label
import threading
import time


cnt = 0

root = tk.Tk()
w = Label(root, text="Hello. Count is " + str(cnt))

def counter():
    global cnt 
    print("in counter, cnt is " + str(cnt))
    cnt += 1
    time.sleep(1)
    counter()

def refresh():
    print("refresh, cnt is " + str(cnt))
    root.after(500, refresh)

def pack_label():
    w = Label(root, text="Hello. Count is " + str(cnt))
    w.pack()

def unpack_label():
    w.pack_forget()

x = threading.Thread(target=counter)
x.start()

w = Label(root, text="Hello. Count is " + str(cnt))
w.pack()
root.after(500, refresh)


root.mainloop()