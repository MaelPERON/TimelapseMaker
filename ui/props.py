import bpy

def register():
    bpy.types.Scene.tm_work_collection = bpy.props.PointerProperty(type=bpy.types.Collection, name="Work Collection")