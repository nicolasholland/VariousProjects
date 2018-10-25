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

Lets assume we have a 3d model of some buildings. 
We already converted them from citygml to 3ds and now we want to compute areas of their roofs.

Here is how our model could look like:

![](https://raw.githubusercontent.com/nicolasholland/VariousProjects/master/citygml/images/singlebuilding.png)

In order to compute the total roof area we can loop over all roof meshes and sum up their areas.
Our area compute [script](https://github.com/nicolasholland/VariousProjects/blob/master/citygml/area_compute.py) contains a simple function for selecting meshes by their name and computing their area.
How to know what meshes are part of the roof however is a bit tricky.
We found the easiest way is to remove all non roof meshes and than simply loop over all meshes that are left :D

![](https://raw.githubusercontent.com/nicolasholland/VariousProjects/master/citygml/images/justroof.png)

The original citygml file (which is just an XML file) has every meshed labeled as RoofSurfaces.
So we could simply loop over every entry in the GML file, extract only roof meshes and convert them to our blender input.

```
<bldg:RoofSurface gml:id="GEOM_447005">
    <bldg:lod2MultiSurface>
        <gml:MultiSurface srsName="EPSG:25833" srsDimension="3">
            <gml:surfaceMember>
                <gml:Polygon gml:id="fme-gen-bec0fcbd-d143-11e8-b354-026a9c381164">
                    <gml:exterior>
                        <gml:LinearRing gml:id="fme-gen-bec0fcbd-d143-11e8-b354-026a9c381164_0">
                            <gml:posList> *List of points* </gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </gml:surfaceMember>
        </gml:MultiSurface>
    </bldg:lod2MultiSurface>
</bldg:RoofSurface>
```

Note that the areas are computed using the models unit!
While you can change the unit in the units tab

```
Properties -> Scene -> Units
```

You still have to know the original unit of the model.



