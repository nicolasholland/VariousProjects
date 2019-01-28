Optical Character Recognition
=============================

We have a PDF of handwritten text that we would like to digitalize.
This document contains our thoughts and results in doing so.

First we looked into how OCR is typically done and found some information
from a lecture by the [University Trier](https://www.uni-trier.de/index.php?id=1175).
In order to digitalize text there are basically four steps that need to happen:

* Preprocessing
* Segmentation
* Recognition
* Postprocessing

In our problem we have a PDF of handwritten text.
And the only background we have so far in OCR is the famous [MNIST challange](http://yann.lecun.com/exdb/mnist/), which is about recognising handwritten digits.
(It's basically the 'Hello World' of machine learning by now)

We are aware of some existing software for OCR namely [OCRopus](https://developers.googleblog.com/2007/04/announcing-ocropus-open-source-ocr.html) (by Google) and [OCR4all](https://gitlab2.informatik.uni-wuerzburg.de/chr58bk/OCR4all_Web) (by University Wuerzburg).
We try to use OCRopus as there is a python client for it [ocropy](https://github.com/tmbdev/ocropy)

Preprocessing
-------------

The text recognition tools we found take images as input, so we start by extracting
our handwritten text into image files.
In our case the entire PDF contained scanned images.
Therefore extracting the text into image files was very easy using [pdfimages](https://www.systutorials.com/docs/linux/man/1-pdfimages/)

```
$ pdfimages handwritten.pdf path/to/images -png
```

Overall our PDF had 699 pages resulting in 699 png image files.

![](https://raw.githubusercontent.com/nicolasholland/VariousProjects/master/ocr/_images/a_page.png)

And while we're at it a simple command for resizing/converting images is [convert](https://linux.die.net/man/1/convert)

```
$ convert -resize 20% input.png output.png
```

The OCRopus input resolution should be about 300 dpi (dots-per-inch).
We also found ocropus gives us a warning when the image is white text on black background instead of vice versa.

```
ERROR:  input.pngSKIPPEDimage may be inverted
```

This can also be fixed using convert:

```
$ convert -negate input.png output.png
```

Processing
----------

We choose to install ocropus using conda (as described in their github readme).


OCRopus states that in order to recognize pages we need to run three steps:

* binarization
* page layout analysis
* text line recognition

We tried out their first example.

Here is a page that we ran ocropus on:

![](https://raw.githubusercontent.com/nicolasholland/VariousProjects/master/ocr/_images/page.png)

It went from line to line segmenting text lines and recognised them:

![](https://raw.githubusercontent.com/nicolasholland/VariousProjects/master/ocr/_images/line.png)

```
The importance oflibraries is evident in the oft-quoted
```

The OCRopus readme "warns" us that we may need to train our own recogintion model.
They even provide tools for ground truth editing.
However we hope that we can apply a pre trained model for now.

When working on our own data we follow the described steps from ocropus test code.

Binarization:

```
$ ocropus-nlbin input.png -o temp
```

Page Segmentation:

```
$ ocropus-gpageseg 'temp/????.bin.png'
```

Text line recognition:

```
$ ocropus-rpred -n 'temp/????/??????.bin.png'
```

OCRopus also offers a tool to combine the results of those three steps in a HTML file using the [hOCR format](https://en.wikipedia.org/wiki/HOCR).

```
$ ocropus-hocr 'temp/????.bin.png' -o temp.html
```

Results (So far)
----------------

The segmentation worked well, most lines were correctly identified even though it was handwritten
and we had mixed characters. Here is an example of a line that was segmented:

![](https://raw.githubusercontent.com/nicolasholland/VariousProjects/master/ocr/_images/aline.png)

The recognition however did not work.
We tried out both the default and [German Fraktur text](tmbdev.net/ocropy/fraktur.pyrnn.gz) models.
Since neither of them were trained on the kind of text we were analysing, we didn't expect them to have good results.
However we hoped that at least some of the german words could be recognised.
Sadly most results were gibberish and the best cases looked more like this, e.g. "entschieden" becomes "enhAreaen".


Postprocessing
--------------

The Postprocessing is about putting the recognised pieces back together as well as fixing the
mistakes.
Most of it has to be done manually by humans.

