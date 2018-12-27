Style Transfer with Tensorflow as a Christmas Service
-----------------------------------------------------

Install dependencies (pillow, flask, matplotlib, tensorflow)

Setup the merrychristmas package:

```
$ pip install -e .
```

You can start the service like this.
Default is port 5000.

```
$ FLASK_APP=merrychristmas flask run
```
Number of iterations for style transfer is defined in a global variable in the beginning of __init__.py
If you have a gpu, configure tensor flow to use that (otherwise it will be slow).

Transfer style code was taken from [here](https://colab.research.google.com/github/tensorflow/models/blob/master/research/nst_blogpost/4_Neural_Style_Transfer_with_Eager_Execution.ipynb)

The whole service was used at christmas to show the kids some cool "machine learning stuff".

