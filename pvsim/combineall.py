#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os.path import join, dirname
import imageio
import numpy as np
import cv2


envsim = imageio.get_reader(join(dirname(__file__), "plant_at_26_8.avi"))
powersim = imageio.get_reader(join(dirname(__file__), "powermovie.mp4"))
cellsim = imageio.get_reader(join(dirname(__file__), "cell.mp4"))

def combine(frameid):
    retval = np.zeros((768, 1024+410, 3)).astype(np.uint8)
    
    env = envsim.get_data(min(frameid + 25 * 5, 1500))
    power = powersim.get_data(min(frameid, 1440))
    cell = cellsim.get_data(min(frameid + 25 * 4, 1440))
    
    powert = cv2.resize(power, (410, 384))
    cellt = cv2.resize(cell, (410, 384))
    
    retval[:768, :1024] = env
    retval[:384, 1024:] = powert
    retval[384:, 1024:] = cellt

    return retval

def main():
    output = imageio.get_writer('combine.mp4', fps=25)

    for frameid in range(0, 25 * 57):
        print(frameid)
        img = combine(frameid)

        output.append_data(img)

    output.close()

main()


envsim.close()
powersim.close()
cellsim.close()
