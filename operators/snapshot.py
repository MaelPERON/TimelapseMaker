import bpy
from ..utils.saving import save_fbx


class CaptureWorkCollection(bpy.types.Operator):
    bl_idname = "scene.capture_work_collection"
    bl_label = "Capture Work Collection"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(self, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "filepath")
        layout.prop(context.scene, "tm_work_collection")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        save_fbx(self.filepath, context.scene.tm_work_collection.name, {})
        return {"FINISHED"}