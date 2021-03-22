音乐和人工神经网络梦
===================

一些星期前我们在[reddit](https://www.reddit.com/r/MachineLearning/comments/m554cq/project_new_python_package_sync_gan_art_to_music/)发现一个软件，用人工神经网络拿音乐产生梦视频。
因为我们觉得这很有意思，所以我们要自己试。
我们常常用图片数据，不过还没用音数据。

先我们加载代码在[github](https://github.com/mikaelalafriz/lucid-sonic-dreams)。
那里说安装很简单，不过我们有一些问题。
试一些小时以后我们停试安装，我们写了错误列表，放[这里](https://github.com/nicolasholland/VariousProjects/tree/master/luciddream)。
因为我们不可以用github的代码，所以我们用[colab](https://colab.research.google.com/drive/1Y5i50xSFIuN3V4Md8TB30_GOAtts7RQD?usp=sharing#scrollTo=Ldjd9LiHxZNG)。
这用得不错。

这神经网络的本来是[StyleGAN2](https://github.com/NVlabs/stylegan2-ada),很有名的神经网络，NVIDIA开发的。
二〇一九年我们已经有[项目](https://somefunwithdata.blogspot.com/2019/10/world-of-gan-craft.html)用GAN产生电脑游戏的图片。这个GAN看了很多的图片，有一些[模型](https://github.com/justinpinkney/awesome-pretrained-stylegan2)。
lucidsonicdreams软件让我们选择模型为产生视频。
软件也让选择神经网络用多少图片，更多图片会做视频更快,少图片做视频更慢，如果只用一个图片，视频可能一点儿无聊。


我们想知道音乐的影响为产生的视频，所以我们试很多不同的音乐。
一些成果在我们的youtube。


错误列表
--------

试用lucidsonicdreams的时候，我们有一些错误安装软件:

* enum (python > 3.6) 错误

```
$ pip install lucidsonicdreams

 AttributeError: module 'enum' has no attribute 'IntFlag'
  ----------------------------------------
```

```
$ pip uninstall -y enum34
```

* 没有 libsndfile 错误

```
>>> import lucidsonicdreams
OSError: sndfile library not found
```

```
$ conda install -c conda-forge libsndfile
```

* 不会找到 libsndfile 错误


```
$ vim miniconda3/lib/python3.7/site-packages/soundfile.py
```

-> 换代码

```
_libname = _find_library('sndfile')
_libname = "/scratch/mini_tmp/miniconda3/envs/tf/lib/libsndfile.so.1"
```

* 不会加载 git 错误

因为我们在proxy的后面，所以我们觉得pygit2不可以加载github.

_pygit2.GitError: failed to connect to github.com: Connection refused

$ git clone  https://github.com/NVlabs/stylegan2-ada.git
$ mv stylegan2-ada stylegan2


* tensorflow 错误

tensorflow.python.framework.errors_impl.InvalidArgumentError: Conv2DCustomBackpropInputOp only supports NHWC

NHWC (number, height, width, channel)是图片的dims。
如果软件不可以用，也许tensorflow在我们的电脑有不对的config。

-> 因为我们用CPU ?

-> 在reddit也有其他的人，有一样的错误，所以我们觉得错误在代码里。


* Colab demo

一些小时试以后，我们决定用colab。

有[colab](https://colab.research.google.com/drive/1Y5i50xSFIuN3V4Md8TB30_GOAtts7RQD?usp=sharing#scrollTo=Ldjd9LiHxZNG), 用得很棒!


用JS和Canvas产生音乐视频
------------------------

在[reddit](https://www.reddit.com/r/proceduralgeneration/comments/m8thb9/my_handmade_html_canvas_javascript_sound/)我们也发现了JS代码用Canvas产生音乐视频。
因为一些月前我们也有Canvas项目，这个项目也产生视频，所以我们觉得那个软件也很有意思。
如果我们有够的时间，可能也试那个软件。


