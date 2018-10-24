My attempts to import CityGML data into blender
===============================================

I tried importing cityGML data into blender.
Apparently this is possible, since I was able to find people on the internet who have done that.
But as I write this, I was not able to.
Here is what I tried, once I figure out what I did wrong/What to do, I can update this text.


ImportCityGML
-------------

Basically I do what they say in their [readme](https://github.com/mohamedmezlini/ImportCityGML).

```
$ git clone https://github.com/mohamedmezlini/ImportCityGML.git
```

Since I use fedora not ubuntu I have to put stuff here:
/usr/share/blender/scripts/addons/

Create package folder and copy package code:

```
$ mkdir /usr/share/blender/scripts/addons/import_citygml
$ cp ImportCityGML/*.py /usr/share/blender/scripts/addons/import_citygml
```

However when running blender, shift+F4 to start a python console, and importing the package I get this:

```
>>> import import_citygml
Traceback (most recent call last):
  File "<blender_console>", line 1, in <module>
  File "/usr/share/blender/scripts/addons/import_citygml/__init__.py", line 26, in <module>
    import lxml #traittement du fichier gml
ModuleNotFoundError: No module named 'lxml'
```

Apparently blender has its own python and I cant just simply install packages into that.
[This](https://blender.stackexchange.com/questions/5287/using-3rd-party-python-modules) says I can use another python e.g. the system python, which Im not using either!
What is easier, installing lxml into the blender python or making blender use my conda python?
Or install lxml into my system python and make blender use that? :D


io_cityGML_basic
----------------

I also tried out [this](https://github.com/zeffii/io_cityGML_basic) and couldn't make it work.
I probably have to learn more blender to solve this...

Again I put their code into a package in here:
/usr/share/blender/scripts/addons/io_cityGML_basic

But I cant make it do anything:

```
>>> import io_citygml_basic
>>> gmlfile = 'path/to/3890_5819.gml'
>>> io_citygml_basic.main(gmlfile)
```

This all runs without error, but to the best of my knowledge, nothing happens?!

Azul
----

This way feels a bit like cheating, but it works.
[Azul](https://itunes.apple.com/nl/app/azul/id1173239678?mt=12) is one of the softwares that are recommended by [cityGML](https://www.citygml.org/software/).
It can read the gml file and export it as a 3dsmax file (.3ds), which blender is able to read...

Getting mesh information
------------------------

For now we do this "by hand" but we are confident, we can turn this into a script :D
Once we imported the citygml 3ds model we can select meshes.
We load the 3D Print Toolbox

```
File -> User Preferences -> Addons -> Mesh: 3D Print Toolbox
```

Or

```
bpy.ops.wm.addon_enable(module="object_print3d_utils")
```

We switch to the 3D printing tab, where we can compute areas and volumes of meshes.
Checking the blender script log reveals that this command lets us compute the area through code:

```
bpy.ops.mesh.print3d_info_area()
```

I guess we have to write some sort of loop over the available meshes and compute all areas.
Also we have to identify the relevant meshes, e.g. roofs and outer walls.
Btw if the log does not show commands for 'everything' you do, here is how we can change that:

```
bpy.app.debug_wm = True
```

Note that the areas are computed using the models unit!
While you can change the unit in the units tab

```
Properties -> Scene -> Units
```

You still have to know the original unit of the model.
Maybe we can get that from the gml file? Let's find out :D


