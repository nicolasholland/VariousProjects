"""
I try to collect all my video processing 'effects' in this script.
Hopefully I can make this into some kind of package in the future
that allows users to apply lots of effects on videos.
"""
import numpy as np
import cv2
from matplotlib import pyplot as plt
import imageio
from io import BytesIO
from scipy.ndimage.filters import gaussian_filter
from scipy import ndimage
from skimage import util
import seaborn as sns

name = "FINAL FANTASY VII REMAKE_20201101124152.mp4"


class SlitSlider(object):

    framebuffer = None

    def __init__(self, dimy, slitsize=1):
        self.slitsize = slitsize
        self.dimy = dimy

        self.nofslits = int(self.dimy / self.slitsize)
        if self.dimy / self.slitsize != self.nofslits:
            raise "number of rows must be divisible by slit size!"

    def _init_framebuffer(self, frame):
        self.framebuffer = [frame for _ in range(self.nofslits)]

    def _update(self, frame):
        self.framebuffer.pop(0)
        self.framebuffer.append(frame)

    def _traverse(self):
        retval = self.framebuffer[-1].copy()

        count = 1
        for slit_id in range(len(self.framebuffer) - 1, 0, -1):
            y_start = count * self.slitsize
            y_end = y_start + self.slitsize
            retval[y_start:y_end, :, :] = self.framebuffer[slit_id][y_start:y_end, :, :]

            count += 1

        return retval

    def __call__(self, frame):
        if self.framebuffer is None:
            self._init_framebuffer(frame)

        self._update(frame)

        return self._traverse()



def plot_resize(func):
    def wrapper(frame):
        img = func(frame)
        img = img[:, :, :3]
        img = cv2.resize(img, (frame.shape[1], frame.shape[0]))
        return img
    return wrapper

@plot_resize
def graph_seg(frame):
    """ OpenCV Graph Segmentation plot (plot needs improvement) """
    SG = cv2.ximgproc.segmentation.createGraphSegmentation()
    seg = SG.processImage(frame)

    plt.subplots_adjust(0, 0, 1, 1)
    plt.imshow(seg)
    buf = BytesIO()
    plt.savefig(buf, format="png", bboxes_inches='tight', pad_inches=0)
    plt.close()

    buf.seek(0)
    return imageio.imread(buf)

@plot_resize
def rgb_hist(frame):
    """ RGB dist plots """
    rgb = [frame[:, :, ind].flatten() for ind in range(3)]

    plt.figure()
    for plt_ind in range(3):
        plt.subplot(3, 1, plt_ind)
        plt.ylim(0, .05)
        plt.xlim(0, 255)
        plt.xticks([])
        plt.yticks([])
        sns.distplot(rgb[plt_ind], color=['red', 'green', 'blue'][plt_ind])

    buf = BytesIO()
    plt.savefig(buf, format="png", bboxes_inches='tight', pad_inches=0)
    plt.close()
    buf.seek(0)
    return imageio.imread(buf)

gblur = lambda frame : gaussian_filter(frame, [5, 5, 5])

laplacian = ndimage.laplace

def process_video(in_name, out_name, function):
    """ docstring """
    video = imageio.get_reader(name)
    #fps = video.get_meta_data()['fps']
    fps = 30

    output = imageio.get_writer(out_name, fps=fps)

    #for frameid in range(0, video.get_length()):
    for frameid in range(0, 3599):
        print(frameid)
        frame = video.get_data(frameid)

        img = function(frame)

        output.append_data(np.concatenate((frame, img), axis=1))

    output.close()

#process_video(vid, out, util.invert)
if __name__ == '__main__':
    slitslider = SlitSlider(720, 4)
    process_video(name, 'result.mp4', slitslider.__call__)

