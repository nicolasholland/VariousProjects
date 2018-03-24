# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 12:09:57 2018

@author: dutchman
"""
import numpy as np
import cv2
from matplotlib import pyplot as plt
import imageio
from io import BytesIO

vid = imageio.get_reader('Devil May Cry™ HD Collection_20180323205018.mp4')
fps = vid.get_meta_data()['fps']

SG = cv2.ximgproc.segmentation.createGraphSegmentation()

out = imageio.get_writer('GraphSegmentation may cry.mp4', fps=fps)

for frameid in range(0, vid.get_length()):
    print(frameid)
    frame = vid.get_data(frameid)
    seg = SG.processImage(frame)

    plt.subplots_adjust(0, 0, 1, 1)
    plt.imshow(seg)
    buf = BytesIO()
    plt.savefig(buf, format="png", bboxes_inches='tight', pad_inches=0)

    buf.seek(0)
    img = imageio.imread(buf)
    img = img[:, :, :3]
    img = cv2.resize(img, (frame.shape[1], frame.shape[0]))

    out.append_data(np.concatenate((frame, img), axis=1))
    plt.close()

out.close()
