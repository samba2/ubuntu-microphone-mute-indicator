#!/usr/bin/env python3

from tkinter import Tk, Canvas
import signal
from signal import SIGUSR1, SIGUSR2
from contextlib import contextmanager
import os
from pathlib import PosixPath
from abc import ABC, abstractmethod
import argparse


class OnAirMonitor:

    _PROGRAM_TITLE = "On-Air Monitor"
    _ALWAYS_ON_TOP_DEFAULT = True
    _OPACITY_DEFAULT = 0.6
    _OFF_AIR_SIGNAL = SIGUSR1
    _ON_AIR_SIGNAL = SIGUSR2
    _REFRESH_AFTER_MILLISECONDS = 200

    PID_FILE_LOCATION = "~/.on-air-monitor.pid"

    def __init__(self):
        self._root = Tk()
        self._startup_canvas = StartupCanvas(self._root)
        self._on_air_canvas = OnAirCanvas(self._root)
        self._off_air_canvas = OffAirCanvas(self._root)

    def run(self):
        with OnAirMonitor.pid_file():
            self._initialize()
            self._root.mainloop()

    @staticmethod
    @contextmanager
    def pid_file():
        _PID_FILE_LOCATION = PosixPath(OnAirMonitor.PID_FILE_LOCATION).expanduser()
        _pid_file = open(_PID_FILE_LOCATION, "w")

        try:
            _pid_file.write(str(os.getpid()))
            _pid_file.close()
            yield _pid_file
        finally:
            os.remove(_PID_FILE_LOCATION)

    def _initialize(self):
        args = self._parse_arguments()
        self._root.wait_visibility(self._root)
        self._root.attributes('-topmost',args.always_on_top)
        self._root.attributes('-alpha', args.opacity)
        self._root.resizable(False, False)
        self._root.title(self._PROGRAM_TITLE)

        self._root.after(self._REFRESH_AFTER_MILLISECONDS, self._refresh_application)
        self._setup_signal_handler()

        self._on_air_canvas.draw()
        self._off_air_canvas.draw()
        self._startup_canvas.draw()
        self._startup_canvas.show()

    def _setup_signal_handler(self):
        signal.signal(self._OFF_AIR_SIGNAL, self._handle_signal)
        signal.signal(self._ON_AIR_SIGNAL, self._handle_signal)

    # force refresh
    def _refresh_application(self):
        self._root.after(self._REFRESH_AFTER_MILLISECONDS, self._refresh_application)

    def _handle_signal(self, signum, unused):
        if signum == self._OFF_AIR_SIGNAL:
            self._startup_canvas.hide()
            self._on_air_canvas.hide()
            self._off_air_canvas.show()

        elif signum == self._ON_AIR_SIGNAL:
            self._startup_canvas.hide()
            self._off_air_canvas.hide()
            self._on_air_canvas.show()
    
    def _parse_arguments(self):
        parser.add_argument('--always-on-top', nargs='?', const=self._ALWAYS_ON_TOP_DEFAULT, default=self._ALWAYS_ON_TOP_DEFAULT, type=bool)
        parser.add_argument('--opacity', nargs='?', const=self._OPACITY_DEFAULT, default=self._OPACITY_DEFAULT, type=float)
        return parser.parse_args()


class BaseCanvas(ABC):
    
    def __init__(self, root):
        self._canvas = Canvas(root, width=100, height=100, highlightthickness=0)

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


class StartupCanvas(BaseCanvas):
    def draw(self):
        self._canvas.create_rectangle(0, 0, 100, 100, fill='gray40', outline='gray40')
        self._canvas.create_text(50, 50, fill="black", font=("Times", 9), text="Awaiting update")


class OnAirCanvas(BaseCanvas):
    _LED_LAYER_COLORS = [(5, 'red'), (4, 'goldenrod'), (3, 'yellow'), (2, 'linen')]

    def draw(self):
        self._canvas.create_rectangle(0, 0, 100, 100, fill='gray30', outline='gray30')
        self._canvas.create_oval(0,0,100,100, fill='red4', outline='red4')
    
        for (x, y) in self._LED_POSITIONS:
            self._draw_led(x, y)

    def _draw_led(self, x, y):
        for (layer_offset, color) in self._LED_LAYER_COLORS:
            self._canvas.create_oval(x-layer_offset,y-layer_offset,x+layer_offset,y+layer_offset, fill=color, outline=color)


class OffAirCanvas(BaseCanvas):
    def draw(self):
        self._canvas.create_rectangle(0, 0, 100, 100, fill='gray30', outline='gray30')
        self._canvas.create_oval(0,0,100,100, fill='brown4', outline='brown4')
        
        for (x, y) in self._LED_POSITIONS:
            self._draw_led(x, y)

    def _draw_led(self, x, y):
        self._canvas.create_oval(x-3, y-3, x+3, y+3, fill='gray30', outline='gray30')
        self._canvas.create_oval(x-2, y-2, x+2, y+2, fill='gray40', outline='gray40')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    OnAirMonitor().run()    
