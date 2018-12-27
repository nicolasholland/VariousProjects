import os
from flask import Flask, render_template, request, redirect, url_for, \
    make_response
from io import BytesIO

from werkzeug import secure_filename

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from merrychristmas.style_transfer import run_style_transfer

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['jpg'])
NUM_ITERATIONS = 1

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

      file1.save(os.path.join(secure_filename('frame1.jpg')))
      file2.save(os.path.join(secure_filename('frame2.jpg')))
      return redirect(url_for('plot_result'))

@app.route('/result.png')
def plot_result():
    content_path = 'frame1.jpg'
    style_path = 'frame2.jpg'

    best, best_loss = run_style_transfer(content_path,
                                     style_path, num_iterations=NUM_ITERATIONS)
    os.remove('frame1.jpg')
    os.remove('frame2.jpg')

    fig=Figure()
    ax=fig.add_subplot(111)
    ax.axis('off')
    ax.imshow(best)

    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)
