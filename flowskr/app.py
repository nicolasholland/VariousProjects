import os
from flask import Flask, render_template, request, redirect, url_for, \
                  make_response
from werkzeug import secure_filename

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO

from imageio import imread
import numpy as np
import cv2

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_file():
   return render_template('app.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      file1 = request.files['file1']
      file2 = request.files['file2']

      if not (file1 and file2):
          return redirect(url_for('upload_file'))

      if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
          return redirect(url_for('upload_file'))

      file1.save(os.path.join('frames', secure_filename('frame1.png')))
      file2.save(os.path.join('frames', secure_filename('frame2.png')))
      return redirect(url_for('plot_result'))

@app.route('/result.png')
def plot_result():
    frame1 = imread(os.path.join('frames', 'frame1.png'))
    frame2 = imread(os.path.join('frames', 'frame2.png'))

    os.remove(os.path.join('frames', 'frame1.png'))
    os.remove(os.path.join('frames', 'frame2.png'))

    hsv = np.zeros_like(frame1)
    prvs = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
    sucs = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs, sucs, None, 0.5, 3, 15, 3, 5,
                                        1.2, 0)

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB)

    fig=Figure()
    ax=fig.add_subplot(111)
    ax.axis('off')
    ax.imshow(bgr)

    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)
