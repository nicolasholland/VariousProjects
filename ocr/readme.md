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

Training
--------

Since we could not find any pre trained model that yielded good results, we looked into training a custom model ourselves.
We found a lot of information about the training process [here](http://www.danvk.org/2015/01/11/training-an-ocropus-ocr-model.htm).

Since we were happy with our segmentation, we keept it and created a '.gt.txt' file for every segmented '.png' file.
Our text contains both latin and non-latin characters.
As we personally don't know about the non-latin characters we labeled them as '?'.
A model that knows how to mark all non-latin characters is also of value to us.
As a start we created ground truth data for one page and trained on that.

```
$ ocropus-rtrain -o mymodel temp/????/*.bin.png
```

One page gave us about 40 samples, which is not enough to train a proper model.
The tutorial we saw started with about 400 training samples.
However we were concerned with the non-latin characters and wanted to see if it was possible at all to train a model on them even if it ends up overfitted.

This is how the output of the training process can look like.

```
24827 71.72 (1649, 48) temp/0001/010003.bin.png
   TRU: u'(im heil. Buche), so spricht (der heil. Lehrer). (Ich habe dieses Wort nach dem Vorgange west'
   ALN: u'(im heil. Buuche), so spricht (der heil. Lehrer). (Ich habe dieses Wort ach dem VVorgange west'
   OUT: u'(inm hel. Buuche), s gricht (der heil. Lchrer. ch hbe dieses Wort ah. denmm ?rgnnge est'
```

For every iteration we can see the ground truth label (TRU) the output of the current state of the model (OUT) and a variant ot the model output which is used for the training (ALN).
The tutorial we learned from suggested having about 30,000 iterations, which even tough we had much fewer training samples we still decided to do.

Here's an example of what our model learned:

![](https://raw.githubusercontent.com/nicolasholland/VariousProjects/master/ocr/_images/recline_sample.png)

```
die ondern sind ???? heil chriten, utras, sowie ??????? für oos, nd es würde-
```

Other Problems
--------------

As we continued working on this we stumbled upon more problems.
I try to keep a list here for future reference.

Encoding:
We got some gt.txt files from project partners which were written on windows or something.
They're not utf8 which makes ocropus lose its shit.

```
UnicodeDecodeError: 'utf8' codec can't decode byte 0xff in position 0: invalid start byte
```

A lot of things that should have helped didn't (maybe because Im fedora an most of linux advice
on the internet appears to be for ubuntu etc.?)

E.g.

```
$ file -i mytextfile.gt.txt
```

would just tell me the charset of a file is us-ascii which is not helpful in any way.
There's a tool iconv that apparently can change encodings but wouldn't do anything for me.
I mean, maybe Im using all these things wrong but if so, the [tutorials](https://www.tecmint.com/convert-files-to-utf-8-encoding-in-linux/) I've been reading weren't helpful either. 

One really good tool was dos2unix. It helped us fix file encodings a lot.

```
$ dos2unix *gt.txt
```

Filenames:

Nothing's more annyoing than writing files and then noticing their name pattern is wrong.
Here's how to fix that:

```
$ rename '.txt' '.gt.txt' *.txt
```

Ground truth labeling:

Very useful tool ba ocropus is ocropus-gtedit.
First you need a model that you apply on all images you want to label.
The resulting .txt files can be gathered in a html file.
That file can then manually be edited before extracting the labels as .gt.txt files.

```
$ ocropus-gtedit html datafolder/????/??????.bin.png -o label.html
$ ocropus-gtedit extract label.html
```


Postprocessing
--------------

The Postprocessing is about putting the recognised pieces back together as well as fixing the
mistakes.
Most of it has to be done manually by humans.

