import bpy

def register():
    bpy.types.Scene.tm_work_collection = bpy.props.PointerProperty(type=bpy.types.Collection, name="Work Collection")
    bpy.types.Scene.tm_save_filepath = bpy.props.StringProperty(subtype="FILE_PATH",name="Snapshot filepath",description='File directory and name to store snapshots. (Variables available: VERSION, DATETIME).')
    bpy.types.Scene.tm_version = bpy.props.IntProperty(min=0,name="Version")
    bpy.types.Scene.tm_timelapse_frame = bpy.props.IntProperty(min=1,default=1,name="Timelapse Frame Version")
    enum_items = [
        ('HIDDEN', "Hidden", "Object isn't show in the viewport","",0),
        ('WIRE', "Wire", "Only wireframe is visible","",1),
        ('SHOW', "Shown", "Object is displayed as usual","",2),
    ]
    bpy.types.Scene.tm_timelapse_display_hidden = bpy.props.EnumProperty(items=enum_items,name="Display Hidden Snapshots")


    bpy.types.Object.tm_version = bpy.props.IntProperty(min=0,name="Version")