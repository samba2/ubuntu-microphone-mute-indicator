#!/usr/bin/env python3

from tkinter import Tk, Canvas
import signal
from signal import SIGUSR1, SIGUSR2
from contextlib import contextmanager
import os
from pathlib import PosixPath
from abc import ABC, abstractmethod


class MuteIndicator:

    _MUTE_SIGNAL = SIGUSR1
    _SPEAK_SIGNAL = SIGUSR2
    _REFRESH_AFTER_MILLISECONDS = 200

    def __init__(self):
        self._root = Tk()
        self._no_connection_canvas = NoConnectionCanvas(self._root)
        self._speak_canvas = SpeakCanvas(self._root)
        self._mute_canvas = MuteCanvas(self._root)

    def run(self):
        with MuteIndicator.pid_file():
            self._initialize()
            self._root.mainloop()

    @staticmethod
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

    def _initialize(self):
        # root.wait_visibility(root)
        self._root.attributes('-topmost',True)
        #self._root.attributes('-alpha', 0.8)
        # root.tk.call('tk', 'scaling', 1.0)
        self._speak_canvas.draw()
        self._mute_canvas.draw()
        self._no_connection_canvas.draw()
        self._no_connection_canvas.show()

        self._root.after(self._REFRESH_AFTER_MILLISECONDS, self._poll)
        signal.signal(self._MUTE_SIGNAL, self._handle_signal)
        signal.signal(self._SPEAK_SIGNAL, self._handle_signal)

    # force refresh
    def _poll(self):
        self._root.after(self._REFRESH_AFTER_MILLISECONDS, self._poll)

    def _handle_signal(self, signum, unused):
        if signum == self._MUTE_SIGNAL:
            self._no_connection_canvas.hide()
            self._speak_canvas.hide()
            self._mute_canvas.show()

        elif signum == self._SPEAK_SIGNAL:
            self._no_connection_canvas.hide()
            self._mute_canvas.hide()
            self._speak_canvas.show()


class IndicatorCanvas(ABC):
    
    def __init__(self, root):
        self._canvas = Canvas(root, width=100, height=100)

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

    @abstractmethod
    def draw(self):
        pass
    
    def show(self):
        self._canvas.pack()

    def hide(self):
        self._canvas.pack_forget()


class NoConnectionCanvas(IndicatorCanvas):
    def draw(self):
        self._canvas.create_rectangle(0, 0, 100, 100, fill='gray40', outline='gray40')
        self._canvas.create_text(50, 50, fill="black", font=("Times", 9),
                        text="Awaiting update")


class SpeakCanvas(IndicatorCanvas):
    _LED_LAYER_COLORS = [(5, 'red'), (4, 'goldenrod'), (3, 'yellow'), (2, 'linen')]

    def draw(self):
        self._canvas.create_rectangle(0, 0, 100, 100, fill='black', outline='black')
        self._canvas.create_oval(0,0,100,100, fill='red4', outline='red4')
    
        for (x, y) in self._LED_POSITIONS:
            self._draw_led(x, y)

    def _draw_led(self, x, y):
        for (layer_offset, color) in self._LED_LAYER_COLORS:
            self._canvas.create_oval(x-layer_offset,y-layer_offset,x+layer_offset,y+layer_offset, fill=color, outline=color)


class MuteCanvas(IndicatorCanvas):
    def draw(self):
        self._canvas.create_rectangle(0, 0, 100, 100, fill='black', outline='black')
        self._canvas.create_oval(0,0,100,100, fill='brown4', outline='brown4')
        
        for (x, y) in self._LED_POSITIONS:
            self._draw_led(x, y)

    def _draw_led(self, x, y):
        self._canvas.create_oval(x-3, y-3, x+3, y+3, fill='gray30', outline='gray30')
        self._canvas.create_oval(x-2, y-2, x+2, y+2, fill='gray40', outline='gray40')


if __name__ == "__main__":
    MuteIndicator().run()    
