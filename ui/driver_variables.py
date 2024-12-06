from bpy.app import driver_namespace

def timelapse_bool_expression(frame, version):
	return version == frame

def display_hidden(identifier):
	match identifier:
		case 0: return 0 # Hidden
		case 1: return 2 # Wire
		case 2: return 5 # Textured
	return 5
def register():
	driver_namespace["timelapse_bool"] = timelapse_bool_expression
	driver_namespace["display"] = display_hidden