import pickle
import random

try:
	import c4d
	from c4d import gui
	
	MODE = "C4D Mode"
except ImportError:
	pass
	
try:
	import imageio
	import numpy as np
	import pickle
	from sklearn.cluster import KMeans
	from sklearn.utils import shuffle
	from numba import jit
	import cv2
	
	MODE = "IMGAGE PROCESS Mode"
except ImportError:
	pass


@jit
def recreate(labels, cc):
    image = np.zeros((w, h, d))
    labels = labels.reshape((w,h))
    for x in range(w):
        for y in range(h):
            image[x,y,:] = cc[labels[x,y]] * 255
    return image.astype(np.uint8)


def image_process_main():
	raw = imageio.imread("John_Martin_Le_Pandemonium_Louvre.jfif")
	
	k = 20
	divide = 80

	img = np.array(raw, dtype=np.float64) / 255

	w, h, d = tuple(img.shape)

	image_array = np.reshape(img, (w * h, d))
	image_array_sample = shuffle(image_array, random_state=0)[:1000]

	kmeans = KMeans(n_clusters=k, random_state=0).fit(image_array_sample)

	resraw = cv2.resize(raw, (round(raw.shape[1] / divide),
		round(raw.shape[0] / divide)))
	img2 = np.array(resraw, dtype=np.float64) / 255
	w, h, d = tuple(img2.shape)
	image_array = np.reshape(img2, (w * h, d))

	labels = kmeans.predict(image_array)
	image = recreate(labels, kmeans.cluster_centers_)

	colorlist = kmeans.cluster_centers_.tolist()
	with open("colorlist.bin", "w") as f:
		f.write("cl="+str(colorlist))
	lablist = labimg.tolist()
	with open("labels.bin", "w") as f:
		f.write("labels="+str(lablist))


def object():
    return doc.GetActiveObject()

def MakeObjectChild(parent, child):
    """ Hierachy Functions
    """
     # Make the following removal of the object reversible
    doc.AddUndo(c4d.UNDOTYPE_DELETE, child)
    child.Remove()
    
    # Make the following insertion of the object reversible
    doc.AddUndo(c4d.UNDOTYPE_CHANGE,child)
    
    child.InsertUnder(parent)
    doc.EndUndo() 
    c4d.EventAdd()

def createmats(vec):
    """ Creates materials """
    c4d.CallCommand(13015)
    
    mat = doc.GetMaterials()[0]
    mat[c4d.MATERIAL_USE_COLOR]=False
    mat[c4d.MATERIAL_USE_LUMINANCE]=True
    mat[c4d.MATERIAL_LUMINANCE_COLOR]=c4d.Vector(vec[0], vec[1], vec[2])
    mat[c4d.MATERIAL_USE_REFLECTION]=False
    mat[c4d.MATERIAL_REFLECTION_BRIGHTNESS]=0.3    
    mat[c4d.MATERIAL_USE_SPECULAR]=False
    mattag = c4d.TextureTag()
    mattag.SetMaterial(mat)


def sphere(posx, posz, height, radius, lab):
    """ Create a sphere """
    c4d.CallCommand(5159) # Cube
    object()[c4d.PRIM_CUBE_LEN,c4d.VECTOR_X]=10
    object()[c4d.PRIM_CUBE_LEN,c4d.VECTOR_Y]=10
    object()[c4d.PRIM_CUBE_LEN,c4d.VECTOR_Z]=10
    object()[c4d.ID_BASEOBJECT_REL_POSITION]=c4d.Vector(posx, height, posz)
    
    textag = c4d.TextureTag()
    textag.SetMaterial(doc.GetMaterials()[lab])
    object().InsertTag(textag)

    c4d.CallCommand(1018791) # Fracture
    
    ActiveObject = object()
    NextObject = ActiveObject.GetNext()
    MakeObjectChild(ActiveObject, NextObject)
    c4d.CallCommand(180000041)

def pandemonium(ll):
    """ create spheres """
    heights = gen_heights(ll)
    x = len(ll)
    y = len(ll[0])
    mult = 10
    for idx in range(x):
        for idy in range(y):
            sphere(mult * idx, mult * idy, 0+heights[ll[idx][idy]],
                    5, ll[idx][idy])
            print(idx, idy, x, y)

def gen_heights(ll, scale=5):
    """ generate random heights mapped to labels """
    x = len(ll)
    y = len(ll[0])
    retval = {}
    for idx in range(x):
        for idy in range(y):
            retval[ll[idx][idy]] = random.random()*scale
                 
    return retval

def main():
    with open("colorlist.bin", "r") as f:
        exec(f.read())
    for vec in cl[::-1]:
        createmats(vec)
    with open("labels.bin", "r") as f:
        exec(f.read())
    pandemonium(labels)


if __name__=='__main__':
    main()
