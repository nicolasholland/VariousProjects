import c4d
from c4d import gui
import random

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

def MoveDown(ActiveObject):
    if ActiveObject == None: return
    
    NextObject = ActiveObject.GetNext()
    if NextObject == None: return
    
    # Make the following section of code reversible
    doc.StartUndo() 
    doc.AddUndo(c4d.UNDOTYPE_DELETE, ActiveObject)
    ActiveObject.Remove()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE,ActiveObject)
    ActiveObject.InsertAfter(NextObject)
    doc.EndUndo()
    c4d.EventAdd()

def SelectNext(ActiveObject):
    """ Selection Functions
    """
    if ActiveObject == None: return
    
    NextObject = ActiveObject.GetNext()
    if NextObject == None: return

    # Marks the beginning of a range of code that should be reversible
    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_BITS, ActiveObject) 
    ActiveObject.DelBit(c4d.BIT_ACTIVE)
    doc.AddUndo(c4d.UNDOTYPE_BITS, NextObject)
    NextObject.SetBit(c4d.BIT_ACTIVE)
    doc.EndUndo()
    c4d.EventAdd()
    
def SelectParent(ActiveObject):
    if ActiveObject == None: return 

    ParentObject = ActiveObject.GetUp()
    if ParentObject == None: return

    # Marks the beginning of a range of code that should be reversible
    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_BITS, ActiveObject) 
    ActiveObject.DelBit(c4d.BIT_ACTIVE) 
    doc.AddUndo(c4d.UNDOTYPE_BITS, ParentObject)
    ParentObject.SetBit(c4d.BIT_ACTIVE)
    doc.EndUndo() 
    c4d.EventAdd()    
    
def SelectChild(ActiveObject):
    if ActiveObject == None: return
     
    ChildObject = ActiveObject.GetDown()
    if ChildObject == None: return
    
    # Marks the beginning of a range of code that should be reversible
    doc.StartUndo() 
    doc.AddUndo(c4d.UNDOTYPE_BITS, ActiveObject)
    ActiveObject.DelBit(c4d.BIT_ACTIVE)
    doc.AddUndo(c4d.UNDOTYPE_BITS, ChildObject)
    ChildObject.SetBit(c4d.BIT_ACTIVE)
    doc.EndUndo() 
    c4d.EventAdd()
   
def rectangle(width=200, height=200, radius=10):
    """ Creates a rectangle object.
    """
    def object():
        return doc.GetActiveObject()

    c4d.CallCommand(5186) # Rectangle
    object()[c4d.PRIM_PLANE]=2
    object()[c4d.PRIM_RECTANGLE_WIDTH]=width
    object()[c4d.PRIM_RECTANGLE_HEIGHT]=height
    object()[c4d.PRIM_RECTANGLE_ROUNDING]=True
    object()[c4d.PRIM_RECTANGLE_RADIUS]=radius
    
def extrude(name="Extrude-NURB", height=20, steps=5, radius=1, mat=0):
    """ Creates an extrude object.
    """
    def object():
        return doc.GetActiveObject()
    
    c4d.CallCommand(5116) # Extrude-NURBS
    object()[c4d.EXTRUDEOBJECT_MOVE]=c4d.Vector(0, height ,0)
    object()[c4d.CAP_START]=3
    object()[c4d.CAP_END]=3
    object()[c4d.CAP_STARTSTEPS]=steps
    object()[c4d.CAP_STARTRADIUS]=radius
    object()[c4d.CAP_ENDSTEPS]=steps
    object()[c4d.CAP_ENDRADIUS]=radius
    object()[c4d.ID_BASELIST_NAME]=name
    
    textag = c4d.TextureTag()
    textag.SetMaterial(doc.GetMaterials()[mat])
    object().InsertTag(textag)
    
def cloner(count=9, name="Cloner"):
    """ Creates a cloner object.
    """
    def object():
        return doc.GetActiveObject()
    
    c4d.CallCommand(1018544) # Klon

    object()[c4d.MG_LINEAR_COUNT]=count
    object()[c4d.ID_BASELIST_NAME]=name
    
def house(width=200, height=200, count=9):
    """ Builds a house.
    
        Creates rectangles, extrudes them and puts them into a cloner object.
        In order to get interesting buildings you have to adjust the 
        cloner options by hand.

    """
    def object():
        return doc.GetActiveObject()

    # small rectangle is 10% smaller
    rectangle(width=width - width/10, height=height - height/10)
    extrude(name="Small_Rectangle", height=height/10, mat=1)

    ActiveObject = object()
    NextObject = ActiveObject.GetNext()
    MakeObjectChild(ActiveObject, NextObject)
    
    rectangle(width=width, height=height)
    extrude(name="Big_Rectangle", height=height/10)
    ActiveObject = object()
    NextObject = ActiveObject.GetNext()
    MakeObjectChild(ActiveObject, NextObject)
    
    rectangle(width=width, height=height)    
    extrude(name="Big_Rectangle", height=height/10)
    ActiveObject = object()
    NextObject = ActiveObject.GetNext()
    MakeObjectChild(ActiveObject, NextObject)
    
    cloner(count=count)
    ActiveObject = object()
    NextObject = ActiveObject.GetNext()
    MakeObjectChild(ActiveObject, NextObject)

    ActiveObject = object()
    NextObject = ActiveObject.GetNext()
    MakeObjectChild(ActiveObject, NextObject)

    ActiveObject = object()
    NextObject = ActiveObject.GetNext()
    MakeObjectChild(ActiveObject, NextObject)

    
def build_base(xpos, ypos, zpos, width=220, height=220, radius=50):
    """ Builds a base of buildings.
    
        Creates a rectangle and extrudes it by calling rectangle().
        
        Parameters
        ----------
        xpos : position of center on x axis
        ypos : position of center on z axis
        zpos : position of center on y axis
    """
    def object():
        return doc.GetActiveObject()
    
    rectangle(width=width, height=height, radius=radius)
    object()[c4d.ID_BASEOBJECT_REL_POSITION]=c4d.Vector(xpos, ypos, zpos)
    

def city_map(areax=1000, areaz=1000, step=300, radius=50):
    """ Creates a city map.
    
        Creates a renctangle as the base of the city and extrudes it.
        Creates nine bases for houses as rectangles and extrudes them.
        
        Parameters
        ----------
            areax : size of city base on x axis.
            areaz : size of city base on z axis.
            step : distance between base centers.
            radius : radius of rounded rectangle corners. 
        
        Returns
        -------
        list of tuples
    """
    def object():
        return doc.GetActiveObject()
    

    rectangle(width=areax, height=areaz, radius=radius)
    extrude(name="Base", height=20, steps=5, radius=1, mat=2)
        
    ActiveObject = object()
    NextObject = ActiveObject.GetNext()
    MakeObjectChild(ActiveObject, NextObject)
    object()[c4d.ID_BASEOBJECT_REL_POSITION]=c4d.Vector(0, -5, 0)
    
    # Build the grid
    base_centers = []
    for x in xrange(-1,2):
        for z in xrange(-1,2):
            build_base(x*step, 0, z*step)
            extrude(name="Block", height=20, steps=5, radius=1, mat=2)

            ActiveObject = object()
            NextObject = ActiveObject.GetNext()
            MakeObjectChild(ActiveObject, NextObject)
            base_centers.append((x*step, z*step))

    # Store blocks in Null object
    c4d.CallCommand(5140) # Null
    object()[c4d.ID_BASELIST_NAME] = "Blocks"
    
    for c in xrange(len(base_centers)):
        ActiveObject = object()
        NextObject = ActiveObject.GetNext()
        MakeObjectChild(ActiveObject, NextObject)
    
    return base_centers

def setup_materials():
    """ Creates materials.
    
        Call this function first, so that all models can be applied with
        materials after they are created.
        Materials can later be changed in the editor.
    """
    def object():
        return doc.GetActiveObject()
    
    ret = []

    c4d.CallCommand(13015)
    c4d.CallCommand(13015)
    c4d.CallCommand(13015)
    
    # street mat
    mat = doc.GetMaterials()[0]
    mat[c4d.MATERIAL_COLOR_COLOR]=c4d.Vector(0.19, 0.15, 0.15)
    mat[c4d.MATERIAL_USE_REFLECTION]=True
    mat[c4d.MATERIAL_REFLECTION_BRIGHTNESS]=0.3    
    mattag = c4d.TextureTag()
    mattag.SetMaterial(mat)
    ret.append(mattag)
    
    # lumi mat
    mat = doc.GetMaterials()[1]
    mat[c4d.MATERIAL_USE_COLOR]=False
    mat[c4d.MATERIAL_USE_LUMINANCE]=True
    mat[c4d.MATERIAL_LUMINANCE_COLOR]=c4d.Vector(0, 0.62, 0.25)
    mat[c4d.MATERIAL_USE_REFLECTION]=True
    mat[c4d.MATERIAL_REFLECTION_BRIGHTNESS]=0.3    
    mattag = c4d.TextureTag()
    mattag.SetMaterial(mat)
    ret.append(mattag)
    
    # building mat
    mat = doc.GetMaterials()[2]
    mat[c4d.MATERIAL_COLOR_COLOR]=c4d.Vector(0.15, 0.19, 0.11)
    mat[c4d.MATERIAL_USE_REFLECTION]=True
    mat[c4d.MATERIAL_REFLECTION_BRIGHTNESS]=0.3    
    mattag = c4d.TextureTag()
    mattag.SetMaterial(mat)
    ret.append(mattag)
    
    return ret

def build_house(posx, posz, scaling, count, height=80, width=80):
    """ Builds a house.
    
        Parameters
        ----------
        posx: position of house on x axis
        posy: position of house on y axis
        scaling: sclaing of house size
        count :  number of segments of the house
    """
    def object():
        return doc.GetActiveObject()
    
    house(width=80, height=80, count=count)
    object()[c4d.MG_LINEAR_OBJECT_POSITION]=c4d.Vector(0, scaling, 0)
    object()[c4d.ID_BASEOBJECT_REL_POSITION]=c4d.Vector(posx, 0, posz)
    
def build_houses(base_centers, minh=10, maxh=30, scaling=11):
    """ Builds four houses on every block base of the city.
    
        Parameters
        ----------
        base_centers : list of tuples with coordinates
        minh : minimal building height
        maxh : maximal building height
        scaling : scaling of building size
    """
    def object():
        return doc.GetActiveObject()
    
    for center in base_centers:
        cx = center[0]
        cz = center[1]

        cc = house_count(minh, maxh)
        build_house(cx-50, cz-50, scaling, cc)

        cc = house_count(minh,maxh)
        build_house(cx-50, cz+50, scaling, cc)
        
        cc = house_count(minh,maxh)
        build_house(cx+50, cz-50, scaling, cc)
        
        cc = house_count(minh,maxh)
        build_house(cx+50, cz+50, scaling, cc)

        
        c4d.CallCommand(5140) # Null
        object()[c4d.ID_BASELIST_NAME] = "BuildingBlock"
        
        # Store buildings in Null object for better readability
        # This for loop assumes assumes buildings per block.
        for c in xrange(4):
            ActiveObject = object()
            NextObject = ActiveObject.GetNext()
            MakeObjectChild(ActiveObject, NextObject)

    c4d.CallCommand(5140) # Null
    object()[c4d.ID_BASELIST_NAME] = "Buildings"        
    # Store blocks of buildings in Null object for better readability
    for c in xrange(len(base_centers)):
        ActiveObject = object()
        NextObject = ActiveObject.GetNext()
        MakeObjectChild(ActiveObject, NextObject)

def house_count(minh, maxh):
    """ Create a random number for house heights.
    
        Random number is between minh and maxh.
        House height is set in a way that the top of a house is always
        a roof and not a luminescent floor.
    """
    ret = random.randint(minh,maxh)
    if (ret - 1) % 3 == 0:
        return ret + 1
    return ret

def street_lamp(x=0, z=0, y=40):
    """ Creates street lamps.
    
        Creates two half spheres and a light for a lamp.
        Those three parts are combined and placed in a cloner.
        This functions also sets a color of the lamps.
    """
    def object():
        return doc.GetActiveObject()
    
    # outer part
    c4d.CallCommand(5160) # Kugel
    object()[c4d.PRIM_SPHERE_TYPE]=5
    object()[c4d.PRIM_SPHERE_RAD]=5
    object()[c4d.ID_BASEOBJECT_REL_POSITION]=c4d.Vector(x, y, z)    
    textag = c4d.TextureTag()
    textag.SetMaterial(doc.GetMaterials()[0])
    object().InsertTag(textag)
    

    # inner part
    c4d.CallCommand(5160) # Kugel
    object()[c4d.PRIM_SPHERE_TYPE]=5
    object()[c4d.PRIM_SPHERE_RAD]=4.5
    object()[c4d.ID_BASEOBJECT_REL_ROTATION]=c4d.Vector(0, 3.14, 0)
    object()[c4d.ID_BASEOBJECT_REL_POSITION]=c4d.Vector(x, y + 1, z)
    textag = c4d.TextureTag()
    textag.SetMaterial(doc.GetMaterials()[1])
    object().InsertTag(textag)
    
    # light
    c4d.CallCommand(5102) # Licht
    object()[c4d.ID_BASEOBJECT_REL_POSITION]=c4d.Vector(x, y, z)
    object()[c4d.LIGHT_DETAILS_FALLOFF]=10
    object()[c4d.LIGHT_DETAILS_OUTERDISTANCE]=50
    object()[c4d.LIGHT_COLOR]=c4d.Vector(0, 0.62, 0.25) # color
    
    # grouping
    c4d.CallCommand(5140) # Null
    object()[c4d.ID_BASELIST_NAME] = "lamp"
    # Store blocks of buildings in Null object for better readability
    for c in xrange(3):
        ActiveObject = object()
        NextObject = ActiveObject.GetNext()
        MakeObjectChild(ActiveObject, NextObject)

    # clone lamps
    c4d.CallCommand(1018544) # Klon
    ActiveObject = object()
    NextObject = ActiveObject.GetNext()
    MakeObjectChild(ActiveObject, NextObject)
    object()[c4d.ID_MG_MOTIONGENERATOR_MODE]=3
    object()[c4d.MG_GRID_RESOLUTION]=c4d.Vector(4, 1, 5)
    object()[c4d.MG_GRID_SIZE]=c4d.Vector(800, 200, 800)


def main():
    def object():
        return doc.GetActiveObject()

    def tag():
        return doc.GetActiveTag()

    def renderdata():
        return doc.GetActiveRenderData()

    def prefs(id):
        return plugins.FindPlugin(id, c4d.PLUGINTYPE_PREFS)
    
    # Create base materials in order to assign them to objects
    matlist = setup_materials()

    # Create layout of the city
    base_centers = city_map()
    
    # Create buildings
    build_houses(base_centers)
    
    # Create street lights
    street_lamp()
   

if __name__=='__main__':
    main()
