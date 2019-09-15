#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os.path import join, dirname
import imageio
import numpy as np

IMGS = []

def load_images():
    path = join(dirname(__file__), "cell")
    names = ["dv%d.jpg" % (n) for n in [0, 100, 500, 600, 650, 660,
             665, 670, 680, 690, 700, 800, 900, 1000]]
    
    for name in names:
        IMGS.append(imageio.imread(join(path, name))[73:800, 156:980])


def _sec2id(sec):
    f = lambda x: x-17 - (x%30)*2
    if sec > 17 and sec <= 30:
        return sec - 17
    if sec > 30:
        return f(sec)

def cell(cellid):
    retval = IMGS[0]
    
    sec = round(cellid / 25)
    
    
    if sec >= 43 or sec <= 17:
        return retval
    
    currentr = IMGS[_sec2id(sec)]
    nextr = IMGS[_sec2id(sec+1)]

    weight1 = (cellid % 25) / 24
    weight2 = 1 - weight1
    retval = weight2 * currentr + weight1 * nextr

    return retval.astype(np.uint8)

def process_video():
    """ docstring """
    output = imageio.get_writer('cell.mp4', fps=25)

    for frameid in range(0, 25 * 60):
    #for frameid in range(0, 300):
        print(frameid)
        img = cell(frameid)

        output.append_data(img)

    output.close()


if __name__ == '__main__':
    load_images()
    process_video()