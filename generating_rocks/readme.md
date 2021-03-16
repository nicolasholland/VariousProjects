产生人工岩石
============

在这个项目我们打算安装[Proc-Rock](https://github.com/acfaruk/proc-rock),产生一些岩石。
Proc-Rock的docs说安装很简单，不过我们有很多的问题。


vcpkg
-----

Proc-Rock用microsoft的vcpkg为加载需要的软件。
不过在Fedora我们有一些问题安装vcpkg。
错误是vcpkg/cmake不可以找到bzlib2,不过电脑有那个。
因为我们不认识vcpkg,所以我们不知道怎么说"bzlib2在那儿!"。

Proc-Rock的setup.sh不用最新的vcpkg，我们认为也许最新的可以用，所以我们试了。
不过那有其他的错误。



Fedora -> Ubuntu (Docker)
-------------------------

也许在Fedora我们不可以用vcpkg，因此我们试了ubuntu，不过因为我们的电脑没有ubuntu，
所以我们用ubuntu在docker图片。
开始新鲜ubuntu的时候我们先必须安装一些软件:

```
$ docker run -it -v /home/dutchman/stuff/产生人工岩石/docker:/scratch ubuntu bash

$ apt-get update

$ apt-get install -y git curl unzip tar cmake yasm automake build-essential pkg-config autogen autoconf libtool

$ git clone https://github.com/acfaruk/proc-rock.git

$ cd proc-rock

$ sh setup.sh
```

OPENGL_opengl_LIBRARY OPENGL_glx_LIBRARY
  OPENGL_INCLUDE_DIR

-> $ apt-get install libgl1-mesa-dev


错误
----

一些小时以后我们觉得错误太多了，所以我们停。
Fedora和Ubuntu都有一样的错误:

```
configure:11008: error: possibly undefined macro: AC_PROG_NM
      If this token and others are legitimate, please use m4_pattern_allow.
      See the Autoconf documentation.
configure:14506: error: possibly undefined macro: AC_LIBTOOL_PROG_COMPILER_PIC
configure:14601: error: possibly undefined macro: AC_ENABLE_SHARED
configure:14602: error: possibly undefined macro: AC_PROG_LIBTOOL
autoreconf: /usr/bin/autoconf failed with exit status: 1
```
我们的autoconf不认识很多的macro,不过我们不知道怎么找到软件有那macro!

-> 找到了: autogen autoconf libtool autoconf-archive

在Fedora我们试安装这软件:

```
$ sudo yum install autogen autoconf libtool autoconf-archive

$ sudo yum install libXrandr-devel libXinerama-devel libXcursor-devel libXi-devel
```

在ubuntu软件的名字是:


```
$ apt-get install -y libxrandr-dev libxinerama-dev libxcursor-dev libxi-dev

```

有fatal error: GL/glu.h: No such file or directory 

-> $ apt-get install libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev


CMake
-----

用vcpkg以后我们试做Proc-Rock软件用:

```
$ cmake .
$ make
```

(Fedora)

```
/usr/bin/ld: cannot find -lglm

-> sudo yum install glm-devel (还不好)
```

(Ubuntu)

```
/usr/include/c++/9/thread:126: undefined reference to `pthread_create'

```

如果Linker不可以找到"-lpthread"，我们觉得这个Makefile很坏。
我们三个小时试了,不过不可以。
虽然我们也有Windows，但是那里也有错误，我们知道windows没有linux好。

