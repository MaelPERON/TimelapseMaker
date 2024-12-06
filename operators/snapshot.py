import bpy
from bpy_extras.io_utils import ImportHelper
from re import sub
from ..utils.saving import save_fbx, get_datetime

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
        def wrapper(_, __):
            # Saving the FBX file
            replacement_map = {
                r"VERSION": f'v{context.scene.tm_version:04}',
                r"DATETIME": get_datetime()
            }
            pattern = '|'.join(f'({pattern})' for pattern in replacement_map.keys()) # Regex pattern from replacement map's keys
            new_filepath = sub(pattern, lambda match: replacement_map[match.group(0)], context.scene.tm_save_filepath)
            save_fbx(new_filepath, context.scene.tm_work_collection.name, {"use_active_collection":True})
            self.report({"INFO"}, f'[{replacement_map[r"DATETIME"]}] Saved "{new_filepath}"')

            # Incrementing the version
            context.scene.tm_version += 1
            bpy.app.handlers.save_post.remove(wrapper)
        
        # Saving the scene before exporting (in case of a crash)
        bpy.app.handlers.save_post.append(wrapper)
        bpy.ops.wm.save_as_mainfile()
        return {"FINISHED"}
    
class ImportSnapshot(bpy.types.Operator, ImportHelper):
    bl_idname = "object.tm_import_snapshot"
    bl_label = "Import Snapshot File"
    bl_options = {"REGISTER","UNDO"}

    # filepath: bpy.props.StringProperty(subtype="FILE_PATH",default="//")

    directory : bpy.props.StringProperty(subtype="DIR_PATH")
    filename : bpy.props.StringProperty(subtype="FILE_NAME")

    files: bpy.props.CollectionProperty(type=bpy.types.OperatorFileListElement)

    @classmethod
    def poll(self, context):
        return True
    
    def draw(self, context):
        self.layout.prop(self, "filepath")

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}
    
    def execute(self, context):
        # Checking for errors
        if not self.filepath.endswith(".fbx"): 
            self.report({"ERROR"}, f'"{self.filepath}" is not an fbx file.')
            return {"CANCELLED"}
        if not os.path.exists(self.filepath):
            self.report({"ERROR"}, f'"{self.filepath}" doesn\'t exist.')
            return {"CANCELLED"}
        
        # Importing the object
        bpy.ops.import_scene.fbx(filepath=self.filepath)

        # Setting few things : joining objects
        context.view_layer.objects.active = context.selected_objects[0]
        bpy.ops.object.join()
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR")

        obj = context.active_object
        filename = os.path.basename(self.filepath).replace(".fbx", "")
        obj.name = filename
        obj.data['tm_is_snapshot'] = True
        match = search(r"v(\d{1,})", filename)
        if hasattr(match, "group"):
            obj.tm_version = int(match.group(1))

        return {"FINISHED"}