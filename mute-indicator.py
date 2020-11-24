#!/usr/bin/env python3

import tkinter as tk
from tkinter import Canvas, Image
from tkinter import PhotoImage
from tkinter import NW, Label, Frame
import signal

root = tk.Tk()
# root.wait_visibility(root)
root.attributes('-topmost',True)
# root.attributes('-alpha', 0.8)

# root.tk.call('tk', 'scaling', 1.0)



# mute = PhotoImage(file="icon/noun_Mute_905696.gif")
# speak = PhotoImage(file="icon/noun_shock_905701.gif")


# does not work
canvas = tk.Canvas(root, width=100, height=100)
canvas.pack()
# canvas.create_rectangle(0, 0, 100, 100, fill='IndianRed3', outline='IndianRed4')
# canvas.create_rectangle(10, 10, 90, 90, fill='IndianRed2', outline='IndianRed4')
# canvas.create_rectangle(20, 20, 80, 80, fill='IndianRed1', outline='IndianRed4')
# canvas.create_rectangle(30, 30, 70, 70, fill='IndianRed1', outline='IndianRed4')

# canvas.create_rectangle(0, 0, 100, 100, fill='GoldenRod3', outline='GoldenRod3')
# canvas.create_oval(20,20,80,80, fill='GoldenRod2', outline='GoldenRod2')
# canvas.create_rectangle(0, 0, 10, 100, fill='IndianRed3', outline='IndianRed4', stipple='gray50')
# canvas.create_rectangle(10, 0, 20, 100, fill='IndianRed3', outline='IndianRed4', stipple='gray50')
# canvas.create_rectangle(20, 0, 30, 100, fill='IndianRed3', outline='IndianRed4', stipple='gray50')
# canvas.create_rectangle(30, 0, 40, 100, fill='IndianRed3', outline='IndianRed4', stipple='gray50')
# canvas.create_rectangle(40, 0, 50, 100, fill='IndianRed3', outline='IndianRed4', stipple='gray50')
# canvas.create_rectangle(50, 0, 60, 100, fill='IndianRed3', outline='IndianRed4', stipple='gray50')
# canvas.create_rectangle(60, 0, 70, 100, fill='IndianRed3', outline='IndianRed4', stipple='gray50')
# canvas.create_rectangle(70, 0, 80, 100, fill='IndianRed3', outline='IndianRed4', stipple='gray50')
# canvas.create_rectangle(80, 0, 90, 100, fill='IndianRed3', outline='IndianRed4', stipple='gray50')
# canvas.create_rectangle(90, 0, 100, 100, fill='IndianRed3', outline='IndianRed4', stipple='gray50')


canvas.create_rectangle(0, 0, 100, 100, fill='black', outline='black')
canvas.create_oval(0,0,100,100, fill='red4', outline='red4')

def create_led(x, y):
    canvas.create_oval(x-6,y-6,x+6,y+6, fill='red3', outline='red3')
    canvas.create_oval(x-5,y-5,x+5,y+5, fill='red3', outline='red3')
    canvas.create_oval(x-4,y-4,x+4,y+4, fill='goldenrod', outline='goldenrod')
    canvas.create_oval(x-3,y-3,x+3,y+3, fill='yellow', outline='yellow')
    canvas.create_oval(x-2,y-2,x+2,y+2, fill='linen', outline='linen')

create_led(28, 14)
create_led(40, 12)
create_led(60, 12)
create_led(72, 14)

create_led(16, 26)
create_led(28, 26)
create_led(40, 26)
create_led(60, 26)
create_led(72, 26)
create_led(84, 26)

create_led(12, 38)
create_led(25, 38)
create_led(38, 38)
create_led(63, 38)
create_led(75, 38)
create_led(88, 38)

create_led(7, 50)
create_led(18, 50)
create_led(30, 50)
create_led(42, 50)
create_led(58, 50)
create_led(70, 50)
create_led(82, 50)
create_led(93, 50)

create_led(12, 62)
create_led(25, 62)
create_led(38, 62)
create_led(63, 62)
create_led(75, 62)
create_led(88, 62)

create_led(16, 74)
create_led(28, 74)
create_led(40, 74)
create_led(60, 74)
create_led(72, 74)
create_led(84, 74)

create_led(28, 86)
create_led(40, 88)
create_led(60, 88)
create_led(72, 86)

create_led(50, 7)
create_led(50, 18)
create_led(50, 30)
create_led(50, 42)
create_led(50, 58)
create_led(50, 70)
create_led(50, 82)
create_led(50, 93)


# canvas._image = img
# canvas.create_image(700,700, anchor=NW, image=img)

# speak_label = Label(image=speak)
# speak_label.image = speak 
# speak_label.pack()

# mute_label = Label(image=mute)
# mute_label.image = mute 
# mute_label.pack()

# force refresh
def poll():
    root.after(500, poll)
root.after(500, poll)

def handle_signal(signum, frame):
    print(f"caught " + str(signum))
    if signum == 10:
        speak_label.pack_forget()
        mute_label.pack()

    elif signum == 12:
        mute_label.pack_forget()
        speak_label.pack()

# mute
signal.signal(10, handle_signal)
# speak
signal.signal(12, handle_signal)

root.mainloop()

# TODO refreshes only when mouse focus