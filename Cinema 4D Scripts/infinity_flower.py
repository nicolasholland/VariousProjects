import c4d
from c4d import gui

def object():
    return doc.GetActiveObject()

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
    
def group_null(target_object, name):
    """ Puts object in a null object and names it.
    
    Parameters
    ----------
    target_object : null object
    name : string
    
    Returns
    -------
    ActiveObject : null object
    """
    c4d.CallCommand(5140) # Null
    object()[c4d.ID_BASELIST_NAME]=name
    
    ActiveObject = object()
    MakeObjectChild(ActiveObject, target_object)
    
    return ActiveObject
    

def pedal():
    """ Creates a pedal as a plane with a correction object inside a
        HyperNURBS object grouped in a null object.
        
    Returns
    -------
    pedal : null object
    """
    c4d.CallCommand(5168) # Ebene
    object()[c4d.PRIM_PLANE_SUBW]=2
    object()[c4d.PRIM_PLANE_SUBH]=1
    c4d.CallCommand(1024542) # Korrektur
    
    ActiveObject = object()
    NextObject = ActiveObject.GetNext()
    MakeObjectChild(NextObject, ActiveObject)
    
    c4d.CallCommand(12139) # Punkte
    c4d.CallCommand(1007455) # HyperNURBS
    
    ActiveObject = object()
    NextObject = ActiveObject.GetNext()
    MakeObjectChild(ActiveObject, NextObject)
    
    object()[c4d.SDSOBJECT_SUBRAY_CM]=2

    c4d.CallCommand(5140) # Null
    ActiveObject = object()
    NextObject = ActiveObject.GetNext()
    MakeObjectChild(ActiveObject, NextObject)
    
    object()[c4d.ID_BASELIST_NAME]="Pedal"
    
    return object()

def pedal_setting(keyframe):
    """ Bend strengths for certain key frames.
    
    Parameters
    ----------
    keyframe : int
    
    Examples
    --------
    >>> h, bend = pedal_setting(0)
    >>> bend
    1.745
    >>> h
    2.182
    """
    bend_strength = 0
    h_strength = 0
    
    if keyframe == 0:
        bend_strength = 1.745
        h_strength = 2.182
        
    return bend_strength, h_strength


def bend_pedal(pedal, name, rot_x, rot_z, move_x, size_x, size_y, size_z,
               strength):
    """ Adds bend objects to the current pedal.
    
    Parameters
    ----------
    pedal : null object
    name : string
    rot_x : float
    rot_z : float
    move_x : float
    size_x : float
    size_y : float
    size_z : float
    strength : float
    
    Returns
    -------
    ActiveObject : null object
    """
    c4d.CallCommand(5128) # Bend

    object()[c4d.ID_BASELIST_NAME]=name


    ActiveObject = object()
    NextObject = ActiveObject.GetNext()
    MakeObjectChild( NextObject, ActiveObject)
    
    # rotate bend object and change size
    object()[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X]=rot_x
    object()[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Z]=rot_z
    object()[c4d.DEFORMOBJECT_SIZE,c4d.VECTOR_X]=size_x
    object()[c4d.DEFORMOBJECT_SIZE,c4d.VECTOR_Y]=size_y
    object()[c4d.DEFORMOBJECT_SIZE,c4d.VECTOR_Z]=size_z
    
    # Bend both halfs of the pedal
    object()[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X]=move_x
    object()[c4d.DEFORMOBJECT_MODE]=2
    object()[c4d.BENDOBJECT_KEEPYAXIS]=True
    object()[c4d.DEFORMOBJECT_STRENGTH]=strength
    
    return SelectParent(object())

def clone_pedals(pedal, count, amount, rotation):
    """ Creates a clone object and puts the pedal inside.
    
    Parameters
    ----------
    pedal : null object
    count : int
    amount : float
    rotation : float
    
    Returns
    -------
    ActiveObject : Cloner object
    """
    c4d.CallCommand(1018544) # Cloner
    
    ActiveObject = object()
    MakeObjectChild(ActiveObject, pedal)
    
    object()[c4d.MG_LINEAR_COUNT]=count
    object()[c4d.MG_LINEAR_MODE]=0
    object()[c4d.MG_LINEAR_OBJECT_POSITION,c4d.VECTOR_Y]=0
    object()[c4d.MG_LINEAR_OBJECT_AMOUNT]=amount
    object()[c4d.MG_LINEAR_OBJECT_ROTATION,c4d.VECTOR_X]=rotation
    
    return object()

def time_offset():
    """ Creates a step object.
    """
    c4d.CallCommand(1018881) # step
    object()[c4d.ID_MG_BASEEFFECTOR_SCALE_ACTIVE]=False
    object()[c4d.ID_MG_BASEEFFECTOR_TIME]=100

def main():
    # Create a pedal
    p = pedal()

    # create bend pedal
    h, bend = pedal_setting(0)
    p = bend_pedal(p, "h", 1.571, -1.571, 0, 10, 400, 350, h)
    p = bend_pedal(p, "Bend", 0, -1.571, -100, 10, 200, 350, bend)

    # move pedal
    object()[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z]=-200
    
    # put in null and clone
    p = group_null(object(), "pedal")
    p = clone_pedals(p, 40, 1.5, 62.832)
    
    # Create a time offset
    time_offset()
    


if __name__=='__main__':
    main()
