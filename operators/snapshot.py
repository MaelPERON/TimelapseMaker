import bpy
from bpy_extras.io_utils import ImportHelper
from re import sub
from ..utils.saving import save_fbx, get_datetime
from ..utils.importing import import_fbx, fbx_import_check

class CaptureWorkCollection(bpy.types.Operator):
    bl_idname = "scene.capture_work_collection"
    bl_label = "Capture Work Collection"

    @classmethod
    def poll(self, context):
        return context.scene.tm_work_collection is not None and context.scene.tm_save_filepath != ""
    
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
            if wrapper in bpy.app.handlers.save_post:
                bpy.app.handlers.save_post.remove(wrapper)
        
        # Saving the scene before exporting (in case of a crash)
        if not bpy.data.filepath: # File is not saved
            wrapper(None, None)
        else:
            bpy.app.handlers.save_post.append(wrapper)
            bpy.ops.wm.save_as_mainfile()
        return {"FINISHED"}
    
class ImportSnapshot(bpy.types.Operator, ImportHelper):
    bl_idname = "object.tm_import_snapshot"
    bl_label = "Import Snapshot File"
    bl_options = {"REGISTER","UNDO"}

    # filepath: bpy.props.StringProperty(subtype="FILE_PATH",default="//")

    filter_glob : bpy.props.StringProperty(default="*.fbx")
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
        l = len(self.files)
        new_objs = []
        
        ## Importing FBX files
        self.report({"INFO"}, "Importing FBX files ({}).".format(l))
        context.window_manager.progress_begin(1, l)

        for n, file in enumerate(self.files):
            context.window_manager.progress_update(n)
            filepath = self.directory + file.name
            check = fbx_import_check(filepath)
            if check<1:
                self.report({"ERROR_INVALID_INPUT"}, file.name + " " + ("is not an fbx file" if check == 0 else "doesn't exist"))
                continue

            obj = import_fbx(context, filepath)
            if obj is None:
                self.report({"WARNING"}, f'"{file.name}" is empty. no object found!')
                continue
            new_objs.append(obj)
        context.window_manager.progress_end()

        ## Processing all the imported snapshots
        self.report({"INFO"}, "Processing snapshots")
        context.window_manager.progress_begin(1, l)

        for n, obj in enumerate(new_objs):
            context.window_manager.progress_update(n)

            bool_expression = "custom_frames != self.tm_version"

            def set_driver(driver):
                driver.use_self = True
                # Custom Frames
                custom_frames = driver.variables.new()
                custom_frames.name = "custom_frames"
                custom_frames.type = "CONTEXT_PROP"
                target = custom_frames.targets[0]
                target.context_property = "ACTIVE_SCENE"
                target.data_path = "tm_timelapse_frame"
                # Display hidden
                display_hidden = driver.variables.new()
                display_hidden.name = "display_hidden"
                display_hidden.type = "CONTEXT_PROP"
                target = display_hidden.targets[0]
                target.context_property = "ACTIVE_SCENE"
                target.data_path = "tm_timelapse_display_hidden"

            # Hide render's driver
            hide_render = obj.driver_add("hide_render", -1).driver
            set_driver(hide_render)
            hide_render.expression = bool_expression
            # Hide viewport's driver
            hide_viewport = obj.driver_add("hide_viewport", -1).driver
            set_driver(hide_viewport)
            hide_viewport.expression = f'{bool_expression} if display_hidden == "hidden" else 0'
            # Display type's driver (2 = Wire | 5 = Textured)
            display_type = obj.driver_add("display_type", -1).driver
            set_driver(display_type)
            display_type.expression = f'display(display_hidden) if {bool_expression} else 5'

        context.window_manager.progress_end()
        self.report({"INFO"}, "Succesfully imported {} snapshots".format(l))
        return {"FINISHED"}