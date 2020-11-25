#!/usr/bin/env python3

from tkinter import Tk, Canvas
from abc import ABC, abstractmethod
import argparse
import subprocess
import re
from queue import Queue, Empty
from threading  import Thread


class MicrophoneMonitor:

    _PROGRAM_TITLE = "Microphone Monitor"
    _ALWAYS_ON_TOP_DEFAULT = True
    _OPACITY_DEFAULT = 0.6
    _REFRESH_AFTER_MILLISECONDS = 250


    def __init__(self):
        self._root = Tk()
        self._unmuted_canvas = UnmutedCanvas(self._root)
        self._muted_canvas = MutedCanvas(self._root)
        self._queue = Queue()


    def run(self):
        self._initialize()
        self._root.mainloop()


    def _initialize(self):
        args = self._parse_arguments()
        self._root.wait_visibility(self._root)
        self._root.attributes('-topmost',args.always_on_top)
        self._root.attributes('-alpha', args.opacity)
        self._root.resizable(False, False)
        self._root.title(self._PROGRAM_TITLE)

        self._unmuted_canvas.draw()
        self._muted_canvas.draw()
        self._update_canvas()

        self._start_pulseaudio_change_listener()
        self._root.after(self._REFRESH_AFTER_MILLISECONDS, self._refresh_application)


    def _parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--always-on-top', nargs='?', const=self._ALWAYS_ON_TOP_DEFAULT, default=self._ALWAYS_ON_TOP_DEFAULT, type=bool)
        parser.add_argument('--opacity', nargs='?', const=self._OPACITY_DEFAULT, default=self._OPACITY_DEFAULT, type=float)
        return parser.parse_args()


    def _update_canvas(self):
        source_to_mute_state = self._get_pulseaudio_sources_mute_state()
        mute_state = source_to_mute_state[self._get_current_mic_name()]

        if mute_state == "yes":
            self._unmuted_canvas.hide()
            self._muted_canvas.show()

        elif mute_state == "no":
            self._muted_canvas.hide()
            self._unmuted_canvas.show()


    def _get_pulseaudio_sources_mute_state(self):
        source_to_mute_state = {}
        last_seen_name = None

        for line in self._run_command(["pactl", "list", "sources"]):
            if '\tName:' in line:
                last_seen_name = re.sub('^\tName: ', '', line)
            elif '\tMute:' in line:
                mute_state = re.sub('^\tMute: ', '', line)
                source_to_mute_state[last_seen_name] = mute_state
        
        return source_to_mute_state


    def _get_current_mic_name(self):
        return [ re.sub('^Default source name: ', '', line) 
                for line in self._run_command(["pacmd", "info"]) 
                if line.startswith("Default source name: ") ][0]


    def _run_command(self, command_list):
        out = subprocess.run(command_list, capture_output=True)
        return str(out.stdout, 'utf-8').splitlines()


    def _refresh_application(self):
        if self._pulseaudio_change_happend() == True:
            self._update_canvas()

        self._root.after(self._REFRESH_AFTER_MILLISECONDS, self._refresh_application)


    def _pulseaudio_change_happend(self):
        try:  
            self._queue.get_nowait() 
        except Empty:
            return False
        else: 
            return True


    def _start_pulseaudio_change_listener(self):
        proc = subprocess.Popen(['pactl', 'subscribe'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
        t = Thread(target=self._enqueue_output, args=(proc.stdout, self._queue))
        t.daemon = True 
        t.start()


    def _enqueue_output(self, out, queue):
        for raw_line in iter(out.readline, b''):
            line = str(raw_line, 'utf-8')
            if "Event 'change' on source" in line:
                queue.put(line)
        out.close()


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


class UnmutedCanvas(BaseCanvas):
    _LED_LAYER_COLORS = [(5, 'red'), (4, 'goldenrod'), (3, 'yellow'), (2, 'linen')]

    def draw(self):
        self._canvas.create_rectangle(0, 0, 100, 100, fill='gray30', outline='gray30')
        self._canvas.create_oval(0,0,100,100, fill='red4', outline='red4')
    
        for (x, y) in self._LED_POSITIONS:
            self._draw_led(x, y)

    def _draw_led(self, x, y):
        for (layer_offset, color) in self._LED_LAYER_COLORS:
            self._canvas.create_oval(x-layer_offset,y-layer_offset,x+layer_offset,y+layer_offset, fill=color, outline=color)


class MutedCanvas(BaseCanvas):
    def draw(self):
        self._canvas.create_rectangle(0, 0, 100, 100, fill='gray30', outline='gray30')
        self._canvas.create_oval(0,0,100,100, fill='brown4', outline='brown4')
        
        for (x, y) in self._LED_POSITIONS:
            self._draw_led(x, y)

    def _draw_led(self, x, y):
        self._canvas.create_oval(x-3, y-3, x+3, y+3, fill='gray30', outline='gray30')
        self._canvas.create_oval(x-2, y-2, x+2, y+2, fill='gray40', outline='gray40')


if __name__ == "__main__":
    MicrophoneMonitor().run()    