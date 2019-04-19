Robot Project
=============

General idea: build a robot like one from star wars using ROS/urdf.

There is a tutorial on how to do this which I tried to follow: [link](http://wiki.ros.org/urdf/Tutorials/Building%20a%20Visual%20Robot%20Model%20with%20URDF%20from%20Scratch)

Installation tutorial is [here](http://wiki.ros.org/Installation/Source):

```
$ sudo dnf install gcc-c++ python-rosdep python3-rosinstall_generator python-wstool python-rosinstall @buildsys-build
$ sudo pip install -U rosdep rosinstall_generator wstool rosinstall
$ sudo pip install --upgrade setuptools
$ rosdep update
```

Created a new folder.

```
$ rosinstall_generator desktop_full --rosdistro melodic --deps > melodic-desktop-full.rosinstall
$ wstool init -j8 src melodic-desktop-full.rosinstall
```

choose ROS Kinetic Kame

Note: I had a problem when using '--tar' that had to do with vcstools.


Also I had problems with the em package.
pip install em will install the em package but put the executable em into condas bin folder.
the cmake file will look for it in the sitepackages/em folder where it is not.

As it turned out that problem was not fixable for me.
CMake kept telling me it cant find em, empty or python-empty.
I dont even know what that is :( and google wont help you either.
Even after I made CMake find em, it didn't recognize the command parameters it was called with.

At least for me it looks like installing ros on fedora while having a conda environment is not possible.
Instead I'm using the ros docker image:

```
$ docker run -it ros
```

Or more precise:


```
$ docker run -v path/to/urdf:urdf -it ros
```

Turns out that's not easy either...

I found [this](https://github.com/ros-ukraine/leobot/issues/83) and tried it.
But that also failed with an dbus.exceptions.DBusException.

Unfortunately I dont know enough about this to fix it myself...
There goes my dream of building a robot :(

I leave this file here in case I want to try again in the future.
