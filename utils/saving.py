from bpy.ops import export_scene
from bpy.path import abspath
from datetime import datetime as date
from os import path, makedirs
from re import sub

def save_fbx(filepath, collection, options={}):
    op_options = {"use_selection": False,"use_active_collection": True,"object_types": {"MESH"},"use_mesh_modifiers": True,"use_subsurf": False,"use_custom_props": True,"bake_anim": False,"path_mode": "AUTO","batch_mode": "OFF"}
    op_options.update(options)

    # Create directory if needed
    filepath = abspath(filepath)
    directory = path.dirname(filepath)
    if not path.exists(directory):
        makedirs(directory, exist_ok=True)
    
    datetime = date.now().strftime("%Y_%m_%d-%H_%M_%S")

    export_scene.fbx(filepath=sub(r"DATETIME", datetime, filepath), collection=collection,**op_options)