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

name = "Assault Android Cactus_20190201170107.mp4"

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
    fps = video.get_meta_data()['fps']

    output = imageio.get_writer(out_name, fps=fps)

    for frameid in range(0, video.get_length()):
    #for frameid in range(0, 300):
        print(frameid)
        frame = video.get_data(frameid)

        img = function(frame)

        output.append_data(np.concatenate((frame, img), axis=1))

    output.close()

#process_video(vid, out, util.invert)
process_video(name, 'result.mp4', laplacian)

    