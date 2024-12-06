import bpy

def register():
    bpy.types.Scene.tm_work_collection = bpy.props.PointerProperty(type=bpy.types.Collection, name="Work Collection")
    bpy.types.Scene.tm_save_filepath = bpy.props.StringProperty(subtype="FILE_PATH",name="Snapshot filepath",description='File directory and name to store snapshots. (Variables available: VERSION, DATETIME).')
    bpy.types.Scene.tm_version = bpy.props.IntProperty(min=0,name="Version")
    bpy.types.Scene.tm_timelapse_offset = bpy.props.IntProperty(min=1,default=1,name="Timelapse Offset")
    bpy.types.Scene.tm_timelapse_clip_duration = bpy.props.IntProperty(min=1,default=24,name="Snapshot Duration")
    bpy.types.Scene.tm_timelapse_frame = bpy.props.IntProperty(min=1,default=1,name="Custom Frames")
    bpy.types.Scene.tm_timelapse_use_frame = bpy.props.BoolProperty(default=False)

    bpy.types.Object.tm_version = bpy.props.IntProperty(min=0,name="Version")