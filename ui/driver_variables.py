from bpy.app import driver_namespace

def timelapse_bool_expression(frame, version, offset, duration):
	_in = version*duration+offset
	_out = (version+1)*duration+offset
	return _in <= frame < _out

def register():
	driver_namespace["timelapse_bool"] = timelapse_bool_expression