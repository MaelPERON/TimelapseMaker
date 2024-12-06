from bpy.app import driver_namespace

def timelapse_bool_expression(frame, version, offset, duration, use_custom_frames=False, custom_frames=1):
	_in = version*duration+offset
	_out = (version+1)*duration+offset
	return _in <= (frame if not use_custom_frames else custom_frames) < _out

def register():
	driver_namespace["timelapse_bool"] = timelapse_bool_expression