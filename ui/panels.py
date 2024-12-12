import bpy
from time import strftime
from ..operators.auto_export import draw_panel

class SimplePanel(bpy.types.Panel):
    bl_idname = "SCENE_PT_SimplePanel"
    bl_label = "Simple Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Timelapse Maker"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Hello World")
        layout.operator_context = "EXEC_DEFAULT"
        op = layout.operator(operator="scene.capture_work_collection")
        layout.operator_context = "INVOKE_DEFAULT"
        op = layout.operator(operator="object.tm_import_snapshot")
        row = layout.row()
        row.operator(operator="scene.tm_start_session")
        row.operator(operator="scene.tm_stop_session")
        # op.test = bpy.data.collections.get("WorkCollection")
        draw_panel(layout, context)

        if obj := context.active_object:
            if obj.type == "MESH" and hasattr(obj, "tm_version"):
                layout.prop(obj, "tm_version")

        layout.prop(context.scene, "tm_timelapse_frame")
        layout.prop(context.scene, "tm_timelapse_display_hidden")
        layout.separator()
        layout.operator("scene.tm_test")