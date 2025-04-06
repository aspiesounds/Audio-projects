#piano de 3 oitavas com samples do steinway & sons (B) de cauda. samples gratuitos disponibilizados em https://theremin.music.uiowa.edu/
#3 octaves piano with free samples recorded from a grand steinway & sons (model B) avaiable on https://theremin.music.uiowa.edu/

import tkinter as tk
import pygame.mixer
import os
import threading
import time

class Piano:
    def _init_(self):
        self.root = tk.Tk()
        self.root.title("3 Octave Piano")
        
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        pygame.mixer.set_num_channels(32)
        
        self.sound_cache = {}
        self.active_sounds = {}
        
        self.notes = {
            'z': 'C4', 's': 'Db4', 'x': 'D4', 'd': 'Eb4', 'c': 'E4', 'v': 'F4',
            'g': 'Gb4', 'b': 'G4', 'h': 'Ab4', 'n': 'A4', 'j': 'Bb4', 'm': 'B4',
            'q': 'C5', '2': 'Db5', 'w': 'D5', '3': 'Eb5', 'e': 'E5', 'r': 'F5',
            '5': 'Gb5', 't': 'G5', '6': 'Ab5', 'y': 'A5', '7': 'Bb5', 'u': 'B5',
            'i': 'C6', '9': 'Db6', 'o': 'D6', '0': 'Eb6', 'p': 'E6', '[': 'F6',
            '=': 'Gb6', ']': 'G6', '\\': 'Ab6', 'a': 'A6', 'k': 'Bb6', 'l': 'B6'
        }
        
        self.canvas = tk.Canvas(self.root, width=850, height=250, bg="gray")
        self.canvas.pack()
        
        self.create_piano()
        
        self.root.bind('<KeyPress>', self.key_press)
        self.root.bind('<KeyRelease>', self.key_release)

    def create_piano(self):
        white_keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        black_keys = {'Db': 0.7, 'Eb': 1.7, 'Gb': 3.7, 'Ab': 4.7, 'Bb': 5.7}

        white_key_width = 52
        white_key_height = 200
        black_key_width = 32
        black_key_height = 120
        
        self.white_key_rects = {}
        self.black_key_rects = {}

        for octave in range(4, 7):
            x_offset = (octave - 4) * (white_key_width * 7)

            #white keys
            for i, note in enumerate(white_keys):
                x = x_offset + i * white_key_width
                rect = self.canvas.create_rectangle(x, 0, x + white_key_width, white_key_height, fill="white", outline="black")
                self.white_key_rects[rect] = f"{note}{octave}"
            
            #black keys 
            for note, position in black_keys.items():
                black_x = x_offset + (position * white_key_width)
                rect = self.canvas.create_rectangle(black_x, 0, black_x + black_key_width, black_key_height, fill="black", outline="black")
                self.black_key_rects[rect] = f"{note}{octave}"

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        clicked_note = None

        
        for rect, note in self.black_key_rects.items():
            x1, y1, x2, y2 = self.canvas.coords(rect)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                clicked_note = note
                self.highlight_key(rect, "darkgray")
                break

       
        if not clicked_note:
            for rect, note in self.white_key_rects.items():
                x1, y1, x2, y2 = self.canvas.coords(rect)
                if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                    clicked_note = note
                    self.highlight_key(rect, "lightgray")
                    break

        if clicked_note:
            self.play_note(clicked_note)
            self.root.after(200, lambda: self.reset_key_color(rect))  # Reset after 200ms

    def highlight_key(self, rect, color):
        self.canvas.itemconfig(rect, fill=color)

    def reset_key_color(self, rect):
        if rect in self.white_key_rects:
            self.canvas.itemconfig(rect, fill="white")
        elif rect in self.black_key_rects:
            self.canvas.itemconfig(rect, fill="black")

    def play_note(self, note):
        file_path = f'{note}.wav'
        if not os.path.exists(file_path):
            print(f"Sound file missing: {file_path}")
            return
        try:
            if note not in self.sound_cache:
                self.sound_cache[note] = pygame.mixer.Sound(file_path)
            
            channel = pygame.mixer.find_channel()
            channel.play(self.sound_cache[note])
            self.active_sounds[note] = channel
            threading.Thread(target=self.fade_out_note, args=(note,), daemon=True).start()
            
        except Exception as e:
            print(f"Could not play sound for note {note}: {e}")
    
    def fade_out_note(self, note):
        time.sleep(5)
        if note in self.active_sounds:
            self.active_sounds[note].fadeout(1000)
            del self.active_sounds[note]

    def key_press(self, event):
        if event.char in self.notes:
            note = self.notes[event.char]

           
            for rect, n in self.black_key_rects.items():
                if n == note:
                    self.highlight_key(rect, "darkgray")
                    break

            for rect, n in self.white_key_rects.items():
                if n == note:
                    self.highlight_key(rect, "lightgray")
                    break
            
            self.play_note(note)

    def key_release(self, event):
        if event.char in self.notes:
            note = self.notes[event.char]

            
            for rect, n in self.black_key_rects.items():
                if n == note:
                    self.reset_key_color(rect)
                    break

            for rect, n in self.white_key_rects.items():
                if n == note:
                    self.reset_key_color(rect)
                    break
    
    def run(self):
        self.root.geometry("850x250")
        self.root.mainloop()

if _name_ == "_main_":
    piano = Piano()
    piano.run()