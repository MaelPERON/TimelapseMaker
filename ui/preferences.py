import bpy
from ..utils.addon import *

class TM_Preferences(bpy.types.AddonPreferences):
    bl_idname = name()

    # RECORDING PREFERENCES

    default_directory: bpy.props.StringProperty(
        subtype="DIR_PATH",default="C:/tmp/snapshots/",
        name="Default save directory",
        description="Default place to save your files"
    )

    frequency: bpy.props.FloatProperty(
        subtype="TIME",min=1,default=10,
        name="Saving Frequency",
        description="In recording, sets the time where every x seconds it takes a snapshot of your work.\nLow values create a lot of snapshots, while high values store less files."
    )

    start_on_load: bpy.props.BoolProperty(
        default=False,
        name="Start Record on Load",
        description="Starts the recording session everytime you load the file"
    )

    padding_number: bpy.props.IntProperty(min=1,default=3,name="VERSION padding number")

    def draw(self, layout):
        layout = self.layout
        # Recording Session
        layout.label(text="Recording",icon="RECORD_ON")
        box = layout.box()
        box.prop(self, "default_directory", icon="FOLDER_REDIRECT")
        box.prop(self, "frequency")
        row = box.row(align=True)
        row.prop(self, "start_on_load")
        if getattr(self, "start_on_load", False):
            row.label(text="",icon="ERROR")

        layout.separator()
        # Timelapse Creation
        layout.label(text="Timelapse Creation",icon="CAMERA_DATA")
        box = layout.box()


# TODO:
# Version padding number
# Filename suffix and prefix
# Start on loading file
# Save before exporting