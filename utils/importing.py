import bpy
def fbx_import_check(filepath):
	if not filepath.endswith(".fbx"):
		print(f'"[TM:import_fbx]{filepath}" is not an fbx file.')
		return 0
	if not os.path.exists(filepath):
		print(f'"[TM:import_fbx]{filepath}" doesn\'t exist.')
		return -1
	return 1
