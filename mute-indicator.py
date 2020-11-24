#!/usr/bin/env python3

import tkinter as tk
from tkinter import Canvas, Image
from tkinter import PhotoImage
from tkinter import NW, Label, Frame
import signal
from signal import SIGUSR1, SIGUSR2
from typing import NamedTuple
from contextlib import contextmanager
import os
from pathlib import PosixPath
from os.path import expanduser


@contextmanager
def pid_file():
    _PID_FILE_PATH = PosixPath("~/.mute-indicator.pid").expanduser()
    _pid_file = open(_PID_FILE_PATH, "w")

    try:
        _pid_file.write(str(os.getpid()))
        _pid_file.close()
        yield _pid_file
    finally:
        os.remove(_PID_FILE_PATH)


class MuteIndicator:
    _root = tk.Tk()
    # root.wait_visibility(root)
    _root.attributes('-topmost',True)
    # root.attributes('-alpha', 0.8)

    # root.tk.call('tk', 'scaling', 1.0)
    _speak_canvas = tk.Canvas(_root, width=100, height=100)
    _mute_canvas = tk.Canvas(_root, width=100, height=100)
    _no_connection_canvas = tk.Canvas(_root, width=100, height=100)

    _LED_POSITIONS=[
        (28, 14), (40, 12), (60, 12), (72, 14), # line 1
        (16, 26), (28, 26), (40, 26), (60, 26), (72, 26), (84, 26), # line 2
        (12, 38), (25, 38), (38, 38), (63, 38), (75, 38), (88, 38), #line 3
        (7, 50), (18, 50), (30, 50), (42, 50), (58, 50), (70, 50), (82, 50), (93, 50), #line (middle)
        (12, 62), (25, 62), (38, 62), (63, 62), (75, 62), (88, 62), # line 5
        (16, 74), (28, 74), (40, 74), (60, 74), (72, 74), (84, 74), # line 6
        (28, 86), (40, 88), (60, 88), (72, 86), # line 7
        (50, 7), (50, 18), (50, 30), (50, 42), (50, 58), (50, 70), (50, 82), (50, 93) # middle y-axis
    ]

    SPEAK_LED_LAYER_COLORS = [(5, 'red'), (4, 'goldenrod'), (3, 'yellow'), (2, 'linen')]
    
    def run(self):
        with pid_file():
            self._draw_speak_canvas()
            self._draw_mute_canvas()
            self._draw_no_connection_canvas()

            self._no_connection_canvas.pack()

            self._root.after(500, self._poll)
            # mute 
            signal.signal(SIGUSR1, self._handle_signal)
            # speak
            signal.signal(SIGUSR2, self._handle_signal)

            self._root.mainloop()

    def _draw_speak_canvas(self):
        self._speak_canvas.create_rectangle(0, 0, 100, 100, fill='black', outline='black')
        self._speak_canvas.create_oval(0,0,100,100, fill='red4', outline='red4')
    
        for (x, y) in self._LED_POSITIONS:
            self._draw_speak_led(x, y)

    def _draw_speak_led(self, x, y):
        for (layer_offset, color) in self.SPEAK_LED_LAYER_COLORS:
            self._speak_canvas.create_oval(x-layer_offset,y-layer_offset,x+layer_offset,y+layer_offset, fill=color, outline=color)
    
    def _draw_mute_canvas(self):
        self._mute_canvas.create_rectangle(0, 0, 100, 100, fill='black', outline='black')
        self._mute_canvas.create_oval(0,0,100,100, fill='brown4', outline='brown4')
        
        for (x, y) in self._LED_POSITIONS:
            self._draw_mute_led(x, y)

    def _draw_mute_led(self, x, y):
        self._mute_canvas.create_oval(x-3, y-3, x+3, y+3, fill='gray30', outline='gray30')
        self._mute_canvas.create_oval(x-2, y-2, x+2, y+2, fill='gray40', outline='gray40')


    def _draw_no_connection_canvas(self):
        self._no_connection_canvas.create_rectangle(0, 0, 100, 100, fill='gray40', outline='gray40')
        self._no_connection_canvas.create_text(50, 50, fill="black", font=("Times", 9),
                        text="Awaiting update")

    # force refresh
    def _poll(self):
        self._root.after(500, self._poll)

    def _handle_signal(self, signum, unused):
        if signum == SIGUSR1:
            self._no_connection_canvas.pack_forget()
            self._speak_canvas.pack_forget()
            self._mute_canvas.pack()

        elif signum == SIGUSR2:
            self._no_connection_canvas.pack_forget()
            self._mute_canvas.pack_forget()
            self._speak_canvas.pack()
    

if __name__ == "__main__":
    MuteIndicator().run()    
