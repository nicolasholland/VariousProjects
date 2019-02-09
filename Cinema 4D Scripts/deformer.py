import c4d
from c4d import documents, plugins

### Helper functions ###

def object():
    """ return active object """
    return doc.GetActiveObject()

def parent_child_relationship(order):
    """
    Last two created objects become parent and child.
    
    Parameters
    ----------
    order : int,
        0 ~ first object parent, second object child
        1 ~ second object parent, first object child        
    """
    ActiveObject = object()
    NextObject = ActiveObject.GetNext()

    if order == 0:
        MakeObjectChild(ActiveObject, NextObject)
    else:
        MakeObjectChild(NextObject, ActiveObject)

def MakeObjectChild(parent, child):
    """ Hierachy Functions """
     # Make the following removal of the object reversible
    doc.AddUndo(c4d.UNDOTYPE_DELETE, child)
    child.Remove()
    
    # Make the following insertion of the object reversible
    doc.AddUndo(c4d.UNDOTYPE_CHANGE,child)
    
    child.InsertUnder(parent)
    doc.EndUndo() 
    c4d.EventAdd()

### modelling functions ###

def ring(ring_radius=250,
         ring_segments=70,
         pipe_radius=50,
         pipe_segments=150):
    """ Create a custom ring """
    c4d.CallCommand(5163) # Ring
    object()[c4d.PRIM_TORUS_OUTERRAD] = ring_radius
    object()[c4d.PRIM_TORUS_SEG] = ring_segments
    object()[c4d.PRIM_TORUS_INNERRAD] = pipe_radius
    object()[c4d.PRIM_TORUS_CSUB] = pipe_segments


def create_graph(rotation_z=0.2,
                 graph_radius=1,
                 node_radius=1):
    """ Creates a torus shaped graph of connected nodes """
    c4d.CallCommand(1018685) # Displacer
    ring(ring_segments=40, pipe_segments=50)
    parent_child_relationship(0)
    
    c4d.CallCommand(1001253) # Polygonreduktion
    parent_child_relationship(1)
    
    c4d.CallCommand(1001002) # Atom Array
    object()[c4d.ATOMARRAYOBJECT_CRAD]=graph_radius
    object()[c4d.ATOMARRAYOBJECT_SRAD]=node_radius
    object()[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Z]=rotation_z
    parent_child_relationship(0)

def create_cloth(displacer_heigh=150,
                 subdivision_render=4,
                 rotation_z=0.2):
    """ Create a flower shaped cloth like structure
    
    Parameters
    ----------
    displacer_heigh : int,
        This is the most important parameter as is has the biggest
        effect on how the noise will affect the ring object.
    subdivision_render : int
    rotation_z : float
    """
    c4d.CallCommand(1018685) # Displacer
    object()[c4d.MGDISPLACER_DISPLACEMENT_HEIGHT]=displacer_heigh

    #TODO not working yet
    noise = c4d.BaseShader(1011116)
    object()[c4d.ID_MG_SHADER_SHADER] = noise

    ring()
    parent_child_relationship(0)
    
    c4d.CallCommand(1007455) # HyperNURBS
    object()[c4d.SDSOBJECT_SUBRAY_CM] = subdivision_render
    object()[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Z]=rotation_z
    parent_child_relationship(0)

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


def main():
    # Create some materials
    matlist = setup_materials()
    
    # Create a graph
    create_graph()

    # Create a ring with deformers
    create_cloth()
    
    # And create a sphere
    c4d.CallCommand(5160) # Kugel



if __name__=='__main__':
    main()