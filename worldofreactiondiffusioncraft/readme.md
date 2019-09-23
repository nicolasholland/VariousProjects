World of Nonlinear Reaction Diffusion
=====================================

The idea is to use the Nonlinear reaction diffusion cnn and run it on frames of a video.
The results would be the final smoothed frames as well as the intermediate results from different
convolution layers.
We want to compile them all into a single video showing the convolution results all at once.
But first we had to find a implementation of the network. (That's not using caffe that is...)


Tensorflow
----------

There's a Tensorflow implementation of the cnn we were looking for [here](https://github.com/VLOGroup/denoising-variationalnetwork).

It needs a specifiv tensorflow implementation from [here](https://github.com/VLOGroup/tensorflow-icg.git)

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

We know this exists but right now we're to tired to look for it.
This section right now is a placeholder until we continued working on this.

