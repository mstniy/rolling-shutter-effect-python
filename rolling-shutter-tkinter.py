#!/usr/bin/env python3

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk # pillow fork of PIL

root = tk.Tk()
label = tk.Label(root)
label.pack()
height = 600
x, y = np.ogrid[-height/2: height/2, -height/2: height/2]
plane = x + 1j * y
plane_abs = abs(plane)
bentprop = np.zeros_like(plane, dtype=np.bool)
propeller_angular_speed=1
animation_speed=3

propeller_cache = {}

for frame in range(height):
    base_angle = 2 * np.pi * ( propeller_angular_speed * frame / height + 1/12)
    base_angle %= np.pi/3
    base_angle = round(base_angle, 3)
    if base_angle in propeller_cache:
        propellors = propeller_cache[base_angle]
    else:
        propellors = np.zeros_like(plane, dtype=np.bool)
        for blade in range(6):
            this_angle = base_angle + blade * np.pi/3
            phase = np.exp( 1j * this_angle)
            ellipse = abs(plane - 0.49 * height * phase) + plane_abs
            this_propellor = ellipse < 0.5 * height
            propellors |= this_propellor
        propeller_cache[base_angle] = propellors

    bentprop[frame] = propellors[frame]
    if frame % animation_speed == 0:
        greenbar = list(range(frame, min(frame + 3, height -3)))
        colors = ("white","lightblue","red","green")
        rgbcolors = np.array(list(map(root.winfo_rgb, colors))) / 256
        composite = np.maximum.reduce((propellors*1, bentprop*2))
        composite[greenbar] = 3
        rgb = rgbcolors.astype(np.uint8)[composite]
        image = ImageTk.PhotoImage(Image.fromarray(rgb, mode="RGB"))
        label.config(image=image)
        root.update()

root.mainloop()

