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

As an example they show a model trained on [German Fraktur text](tmbdev.net/ocropy/fraktur.pyrnn.gz)
Maybe that model works for us as well.


Postprocessing
--------------

The Postprocessing is about putting the recognised pieces back together as well as fixing the
mistakes.
Most of it has to be done manually by humans.

