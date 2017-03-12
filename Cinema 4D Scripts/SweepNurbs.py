import c4d
from c4d import gui

""" PARAMETERS:
    The following parameters are used for generating Sweep Nurbs.
    Change the parameters to create different Sweep Nurbs.
"""
birth_rate_editor = 2
birth_rate_render = 1

cogwheel_teeth = 20
cogwheel_inner_radius = 0.5
cogwheel_middle_radius = 0
cogwheel_outer_radius = 22
cogwheel_base_level = 0.6

rotation_strength = 25
turbolence_strength = 10
turbolence_scale = 3
friction_strength = 15



""" Hierachy Functions
"""
def MakeObjectChild(parent, child):
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

""" Selection Functions
"""
def SelectNext(ActiveObject):
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
   


def main(): 
    def object():
        return doc.GetActiveObject()

    # Create Objects    
    c4d.CallCommand(5109) # Emitter
    
    object()[c4d.PARTICLEOBJECT_BIRTHEDITOR]= birth_rate_editor
    object()[c4d.PARTICLEOBJECT_BIRTHRAYTRACER]= birth_rate_render
    object()[c4d.PARTICLEOBJECT_SHOWOBJECTS]=True
    
    c4d.CallCommand(5160) # Sphere
    object()[c4d.PRIM_SPHERE_RAD]=5

    # Create Hierachy
    ActiveObject = object()
    NextObject = ActiveObject.GetNext()
    MakeObjectChild(NextObject, ActiveObject)
    
    # Create Tracer
    ActiveObject = object()
    SelectParent(ActiveObject)
    c4d.CallCommand(1018655) # Tracer
    
    # Create cogwheel and sweep-nurbs
    c4d.CallCommand(5188) # cogwheel
    object()[c4d.PRIM_COGWHEEL_TEETH]=cogwheel_teeth
    object()[c4d.PRIM_COGWHEEL_IRAD]=cogwheel_inner_radius
    object()[c4d.PRIM_COGWHEEL_MRAD]=cogwheel_middle_radius
    object()[c4d.PRIM_COGWHEEL_ORAD]=cogwheel_outer_radius
    object()[c4d.PRIM_COGWHEEL_BEVEL]=cogwheel_base_level
    c4d.CallCommand(5118) # Sweep-NURBS
    
    # Put tracer and cogwheel below sweep-nurbs
    MakeObjectChild(object(), object().GetNext() )
    MakeObjectChild(object(), object().GetNext() )
    
    SelectChild(object())
    MoveDown(object())
    
    # rotation, turbolance and friction
    c4d.CallCommand(5112) # Rotation
    object()[c4d.ROTATIONOBJECT_STRENGTH]=rotation_strength
    
    c4d.CallCommand(5115) # Turbulence
    object()[c4d.TURBULENCEOBJECT_STRENGTH]=turbolence_strength
    object()[c4d.TURBULENCEOBJECT_SCALE]=turbolence_scale
    
    c4d.CallCommand(5114) # Friction
    object()[c4d.FRICTIONOBJECT_STRENGTH]=friction_strength


    # Attach material
    SelectNext(object())
    SelectNext(object())
    SelectNext(object())

    
    # If there is no material, create one
    if len(doc.GetMaterials()) < 1:
        c4d.CallCommand(13015)

    textag = c4d.TextureTag()
    textag.SetMaterial(doc.GetMaterials()[0])    
    object().InsertTag(textag)
    
    # Background
    c4d.CallCommand(5122)
    
    # If there is no background material, create one
    if len(doc.GetMaterials()) < 2:
        c4d.CallCommand(13015)

    textag = c4d.TextureTag()
    textag.SetMaterial(doc.GetMaterials()[1])    
    object().InsertTag(textag)


if __name__=='__main__':
    main()
