import bpy

def register():
    bpy.types.Scene.tm_work_collection = bpy.props.PointerProperty(type=bpy.types.Collection, name="Work Collection")
    bpy.types.Scene.tm_save_filepath = bpy.props.StringProperty(subtype="FILE_PATH",name="Snapshot filepath",description='File directory and name to store snapshots. (Variables available: VERSION, DATETIME).')
    bpy.types.Scene.tm_version = bpy.props.IntProperty(min=0,name="Version")