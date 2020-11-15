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
from numba import jit

name = "0001-7469.mkv"


class Wave(object):
    field = None
    counter = 0
    t = 0

    def __init__(self, w, h, function, update_rate=5, gray=True,
            nonumba=False):
        """
        Parameters
        ----------
        w : int, width
        h : int, height
        function : function x,y,t -> v, should be numba compiled
        update_rate : int, update wave attern every n-th frame.
        gray : bool, grayscale or color output
        nonumba : bool, must be true if function is not compiled.
            will make things slow, defaut False

        Examples
        --------
        >>> @jit
        ... def func(x, y, t):
        ...     return 15 * np.sin((x/50 + y/50) / (1/(t+1)))
        >>> wave =  Wave(1080, 1920, func, update_rate=4)
        >>> process_video(name, 'result.mp4', wave.__call__)

        Notes
        -----
        Here's some functions, inspired by this:
        https://tixy.land/

        * 30 * np.cos(((x/50)-7.5)*((y/50)-7.5)*(t/12))
        * 30 * (1-((t+x+np.sin(t+(x/50))/2)-(y/50)/30)%1)/3
        * 10 * np.cos(((y/300)**(x/300))+t)**np.cos((x>y)+t)
        * 10 * np.tan(2*t/(1+x*(y>=x)))+np.tan(2*t/(1+y*(x>=y)))
        * 15 * np.cos(((x-800)^(y-800))/1000.*t)
        * 10 * np.tan(t / (y+1) * x)
        * 10 * np.sin(((x-500)**2 + (y-500)**2)/10000. + t)
        """
        self.gray = gray
        self.w = w
        self.h = h
        self.field = np.zeros((w, h))
        self.update_rate = update_rate
        self.function = function
        self.nonumba = nonumba

    @staticmethod
    @jit
    def _static_update_field(w, h, field, t, f):
        for x in range(w):
            for y in range(h):
                field[x, y] = f(x, y, t)
        return field

    def _update_field(self, t):
        if self.nonumba:
            for x in range(self.w):
                for y in range(self.h):
                    self.field[x, y] = self.function(x, y, t)
        else:
            self.field = self._static_update_field(
                self.w, self.h, self.field, t, self.function)


    def _apply_field(self, img):
        if self.gray:
            retval = cv2.cvtColor(img,
                cv2.COLOR_RGB2GRAY).astype(np.float64)
            retval += self.field
            retval[retval < 0] = 0
            retval[retval > 254] = 254
            return np.stack([retval, retval, retval],
                axis=2).astype(np.uint8)
        else:
            raise NotImplementedError

    def __call__(self, img):
        if self.counter % self.update_rate == 0:
            self._update_field(self.t)
            self.t += 1

        self.counter += 1
        return self._apply_field(img)


class SlitSlider(object):
    """
    Examples
    --------
    >>> slitslider = SlitSlider(720, 4)
    >>> process_video(name, 'result.mp4', slitslider.__call__)
    """

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
slitslider = SlitSlider(720, 4)
def process_video(in_name, out_name, function):
    """ docstring """
    video = imageio.get_reader(name)
    #fps = video.get_meta_data()['fps']
    fps = 30

    output = imageio.get_writer(out_name, fps=fps)

    #for frameid in range(0, video.get_length()):
    for frameid in range(0, 7468):
        print(frameid)
        frame = video.get_data(frameid)

        img = function(frame)

        output.append_data(np.concatenate((frame, img), axis=1))

    output.close()

#process_video(vid, out, util.invert)
if __name__ == '__main__':

    @jit
    def func(x, y, t):
        return 15 * np.sin((x/50 + y/50) / (1/(t+1)))

    wave =  Wave(1080, 1920, func, update_rate=30)
    process_video(name, 'result.mp4', wave.__call__)

