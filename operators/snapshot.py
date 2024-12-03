import bpy
from ..utils.saving import save_fbx, get_datetime
from re import sub

class CaptureWorkCollection(bpy.types.Operator):
    bl_idname = "scene.capture_work_collection"
    bl_label = "Capture Work Collection"

    @classmethod
    def poll(self, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "tm_save_filepath")
        row.prop(context.scene, "tm_version")
        layout.prop(context.scene, "tm_work_collection")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):

        # Saving the FBX file
        replacement_map = {
            r"VERSION": f'v{context.scene.tm_version:04}',
            r"DATETIME": get_datetime()
        }
        pattern = '|'.join(f'({pattern})' for pattern in replacement_map.keys()) # Regex pattern from replacement map's keys
        new_filepath = sub(pattern, lambda match: replacement_map[match.group(0)], context.scene.tm_save_filepath)
        save_fbx(new_filepath, context.scene.tm_work_collection.name, {})
        
        # Incrementing the version
        context.scene.tm_version += 1
        return {"FINISHED"}