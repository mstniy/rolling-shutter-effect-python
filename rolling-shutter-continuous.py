#!/usr/bin/env python3

import tkinter as tk
import numpy as np
import time
from PIL import Image, ImageTk # pillow fork of PIL

root = tk.Tk()
label = tk.Label(root)
label.pack()
height = 600
x, y = np.ogrid[-height/2: height/2, -height/2: height/2]
plane = x + 1j * y
plane_abs = abs(plane)
propeller_angular_speed=1

frame_cache = {}
propeller_cache = {}
frame = 0

while True:
    frame_base_angle = 2 * np.pi * ( propeller_angular_speed * frame / height + 1/12)
    frame_base_angle %= np.pi/3
    frame_base_angle = round(frame_base_angle, 3)
    if frame_base_angle in frame_cache:
        print('frame hit')
        image = frame_cache[frame_base_angle]
        time.sleep(1/500)
    else:
        print('frame miss')
        bentprop = np.zeros_like(plane, dtype=np.bool)
        for line in range(height):
            line_base_angle = 2 * np.pi * ( propeller_angular_speed * (frame+line) / height + 1/12)
            line_base_angle %= np.pi/3
            line_base_angle = round(line_base_angle, 3)
            if line_base_angle in propeller_cache:
                propellors = propeller_cache[line_base_angle]
            else:
                propellors = np.zeros_like(plane, dtype=np.bool)
                for blade in range(6):
                    this_angle = line_base_angle + blade * np.pi/3
                    phase = np.exp( 1j * this_angle)
                    ellipse = abs(plane - 0.49 * height * phase) + plane_abs
                    this_propellor = ellipse < 0.5 * height
                    propellors |= this_propellor
                propeller_cache[line_base_angle] = propellors

            bentprop[line] = propellors[line]
        #greenbar = list(range(frame, min(frame + 3, height -3)))
        colors = ("white","lightblue","red","green")
        rgbcolors = np.array(list(map(root.winfo_rgb, colors))) / 256
        composite = bentprop*2
        #composite[greenbar] = 3
        rgb = rgbcolors.astype(np.uint8)[composite]
        image = ImageTk.PhotoImage(Image.fromarray(rgb, mode="RGB"))
        frame_cache[frame_base_angle] = image
    label.config(image=image)
    root.update()
    frame += 1

root.mainloop()

