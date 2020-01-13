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
    propellors = np.zeros_like(plane, dtype=np.bool)
    angle = 2 * np.pi * ( propeller_angular_speed * frame / height + 1/12)
    for blade in range(6):
        phase = np.exp( 1j * (angle + blade * np.pi/3))
        if phase in propeller_cache:
            this_propellor = propeller_cache[phase]
        else:
            ellipse = abs(plane - 0.49 * height * phase) + plane_abs
            this_propellor = ellipse < 0.5 * height
            propeller_cache[phase] = this_propellor
        propellors |= this_propellor

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

