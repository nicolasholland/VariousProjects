World of GAN craft
==================

The idea is to train a generative adversarial network on world of warcraft footage
in order to create a neural network that can generate images that look like they are
from the game.

How we learned about GANs
-------------------------

We learned how to build a basic GAN from [this](https://machinelearningmastery.com/how-to-develop-a-generative-adversarial-network-for-a-cifar-10-small-object-photographs-from-scratch/) tutorial using the cifar-10 dataset.

We created our own dataset by playing and recording the game.
The cifar-10 dataset contained about 60k images, where 50k were used for training and 10k for testing.
We recorded the game with 24 frames per second. That way we had to record about 3 hours of gameplay in order to create a dataset of the similar size as cifar-10.

Training a GAN on 32x32 images worked well.
We got to over 50 epochs in one night on our computer.

However our goal was images with a resolution of about 256x256.
We simply tried adding some convolution layers to the original gan and trained it on larger images.

Here are some difficulties with that:
* larger images/networks need more memory, while 50k 32x32 images fit easily in our memory, the 256x256 did not
* we lowered the batch size and loaded only parts of the dataset into memory, after each iteration, which slowed down the learning process.
* The results we got were dissapointing, which made us believe that we might need a more sophisticated network architecture

We found [this](https://github.com/t0nberryking/DCGAN256) gan for 256x256 images.
In addition to the conv and relu layers they also use batch normalization and upsampling layers for the generator and pooling layers for the discriminator.


How we recorded data
--------------------

Using [this](https://www.apowersoft.com/free-online-screen-recorder).

We extract image data from the videos using imageo and imageio-ffmpeg.

Instead of storing raw image files or some hdf5 format we simply kept the frames in an mp4 file.
When training on them, we loaded random frames from that file, which in itself consists of 3min video samples randomly stacked together.
And since it is a valid video file we could publish our dataset on youtube!


Results
-------

Here are some 32x32 results:

![](https://raw.githubusercontent.com/nicolasholland/VariousProjects/master/world_of_gan_craft/_images/generated_plot_e010.png)

World of Nonlinear Reaction Diffusion (abandoned project)
=========================================================

Note: We had the idea for this project before we made the "switch" to using GANs.
We keep what we had so far in this readme.md in case we ever want to try it again.
If anyone reading this knows a "good" implementation of the Trainable onlinear reaction
diffusion network (using either regular tensorflow or not depending on expensice matlab license)
please reach out, we find it amazing!
(Also we implemented that thing once ourselves using caffe ... not doing that again)

Idea
----

The idea is to use the Nonlinear reaction diffusion cnn and run it on frames of a video.
The results would be the final smoothed frames as well as the intermediate results from different
convolution layers.
We want to compile them all into a single video showing the convolution results all at once.
But first we had to find a implementation of the network. (That's not using caffe that is...)


Tensorflow
----------

There's a Tensorflow implementation of the cnn we were looking for [here](https://github.com/VLOGroup/denoising-variationalnetwork).

It needs a specific tensorflow implementation from [here](https://github.com/VLOGroup/tensorflow-icg.git)

We couldn't find any conda packages or docker images, so we tried building it ourself.
It is recommended to be used with ubuntu and we currently have fedora installed on our machine.
Thefore we used a gcp instance using this images:

```
Deep Learning Image: Base m35 (with CUDA 10.0)
A Debian based image with CUDA 10.0. 
```

The vm instance comes with cuda toolkit and cuDNN pre installed so there was no need to install it
from e.g. [here](https://developer.nvidia.com/cuda-90-download-archive)

However we had to install bazel.
The fedora version would be [here](https://docs.bazel.build/versions/master/install-redhat.html)
And the debian version we installed was [here](https://docs.bazel.build/versions/master/install-ubuntu.html)

Here's the catch, we dont know what bazel is. And it does not work for us...

We followed the instructions as we understood them, which were

```
$ sh tf_exports.sh
$ ./configure
$ sh build.sh
```

Up until the last command everything was going mostly fine.
The configure script was looking for libcudart.so.10 and the system had a library link named
libcudart.so.10.0.
We solved that by adding another symlink and that was it.

The build script however failed and we couldn't find enough information on stackoverflow to fix it:

```
ERROR: Config value cuda is not defined in any .rc file
build.sh: 24: build.sh: [[: not found
build.sh: 30: build.sh: bazel-bin/tensorflow/tools/pip_package/build_pip_package: not found
ls: cannot access '/tmp/tensorflow_pkg': No such file or directory
```

Matlab
------

We found [this](https://github.com/google/RED/blob/master/README.md).
Now we don't have matlab installed, so instead we tried octave.

First we need the octave image package.
And before we can install that, we need octave-devel (most tutorials are not meant for fedora?)

So here is what we do:

```
$ sudo dnf install octave-devel
```

Here's the octave command to install the package:

```
>> pkg -forge install image
```

Now while the image install command would work, running ReactionDiffusion.m would still result in this error:

```
warning: the 'idct2' function belongs to the image package from Octave Forge but
has not yet been implemented.
```

We assume this has to do with us using fedora somehow, so the next idea was using a docker image
from [here](https://hub.docker.com/r/openmicroscopy/octave)

```
$ docker run --rm -it openmicroscopy/octave  
```

