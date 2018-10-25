"""
area_compute.py
---------------

Loop over roof tops, compute areas and write into file.
Use with:

$ blender -b -P area_compute.py
"""
import bpy
import bmesh
import numpy as np

# Load addons
bpy.ops.wm.addon_enable(module="object_print3d_utils")

# Import 3ds file
filepath = "/home/dutchman/stuff/citygml_stuff/3DS_ELEM.3ds"
bpy.ops.import_scene.autodesk_3ds(filepath = filepath)

# Loop over meshes and compute their areas.
meshlist = ['1', '2', '3', '4']

def meshid2area(mid):
    """
    Compute area of mesh as sum of its faces.

    Parameters
    ----------
    mid : str, name of mesh

    Returns
    -------
    area : float, area of mesh
    """
    obj = bpy.data.objects[mid]
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    area = sum(f.calc_area() for f in bm.faces)
    return area

areas = np.array([meshid2area(mid) for mid in meshlist])
print(areas) # Do something more usefull than printing.

print("Done")

