import bpy
import os
from re import search

def fbx_import_check(filepath):
	if not filepath.endswith(".fbx"):
		print(f'"[TM:import_fbx]{filepath}" is not an fbx file.')
		return 0
	if not os.path.exists(filepath):
		print(f'"[TM:import_fbx]{filepath}" doesn\'t exist.')
		return -1
	return 1

def import_fbx(context, filepath):
	if fbx_import_check(filepath)<1:
		return None
	# Importing the object
	bpy.ops.import_scene.fbx(filepath=filepath)

	objs = context.selected_objects
	if len(objs) < 1:
		print("Empty")
		return None

	# Setting few things : joining objects
	context.view_layer.objects.active = objs[0]
	bpy.ops.object.join()
	bpy.ops.object.origin_set(type="ORIGIN_CURSOR")

	obj = context.active_object
	filename = os.path.basename(filepath).replace(".fbx", "")
	obj.name = filename
	obj.data['tm_is_snapshot'] = True
	match = search(r"v(\d{1,})", filename)
	if hasattr(match, "group"):
		obj.tm_version = int(match.group(1))

	return obj