"""
Compute optical flow using OpenCV's Deepflow implementation for
video files.

This script is called secret_of_deepflow because we first applied it
on secret of mana footage.
"""
import sys
import numpy as np
import imageio
import cv2
from multiprocessing import Pool

retval = cv2.optflow.createOptFlow_DeepFlow()

f = lambda f1,f2: retval.calc(cv2.cvtColor(f1, cv2.COLOR_RGB2GRAY),
                              cv2.cvtColor(f2, cv2.COLOR_RGB2GRAY),
                              np.zeros((f1.shape[:2]), dtype=np.float32))

def draw(flow, frame):
    hsv = np.zeros_like(frame)
    hsv[...,1] = 255
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    return cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB)


def total(fr1, fr2):
    """
    CPU times: user 20 ms, sys: 12 ms, total: 32 ms
    Wall time: 19.2 s
    """
    flow = f(fr1, fr2)
    rgb = draw(flow, fr1)
    return np.concatenate((fr1, rgb), axis=1)

def total2(args):
    """
    For use with multiprocessing.Pool
    """
    flow = f(args[0], args[1])
    rgb = draw(flow, args[0])
    return np.concatenate((args[0], rgb), axis=1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Use with %s <video>' % (sys.argv[0]))
    vid = imageio.get_reader(sys.argv[1],  'ffmpeg')
    out = imageio.get_writer('%s_flow.mp4' % (sys.argv[1]), 'ffmpeg')
    p = Pool(4)
    N = vid.get_length() - 1
    print(N)
    for n in range(1, N/4):
        print("FRAME: ", 4*n)
        idx = 4 * (n - 1)
        res = p.map(total2, [[vid.get_data(idx + 1), vid.get_data(idx + 2)],
                             [vid.get_data(idx + 2), vid.get_data(idx + 3)],
                             [vid.get_data(idx + 3), vid.get_data(idx + 4)],
                             [vid.get_data(idx + 4), vid.get_data(idx + 5)]])
        out.append_data(res[0])
        out.append_data(res[1])
        out.append_data(res[2])
        out.append_data(res[3])
    out.close()

