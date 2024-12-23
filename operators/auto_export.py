import bpy
import time

last_export: float = float("-inf")
interval_check = 0.5
export_frequency = 25
session_state = False

def elapse_time_since_last_export() -> float:
	return time.time() - last_export

def get_modals() -> list:
	return [operator for operator in bpy.context.window.modal_operators]

def check_for_modal() -> bool:
	return len(get_modals())>0

def restart_timer() -> None:
	global last_export
	global session_state
	last_export = time.time()
	session_state = True

def update_interface() -> None:
	"""
	Refresh every interface where timer information is displayed (or used).
	"""
	for area in bpy.context.screen.areas:
		for region in area.regions:
			if region.type == "UI":
				region.tag_redraw()
	pass

def draw_panel(layout, context) -> None:
	box = layout.box()
	recording = is_registered()
	box.label(text="Recording..." if recording else "No recording", icon="RECORD_" + ("ON" if recording else "OFF"))
	box.prop(context.scene, "tm_work_collection")
	row = box.row()
	row.prop(context.scene, "tm_save_filepath")
	row.prop(context.scene, "tm_version")
	if recording:
		if check_for_modal():
			box.label(text=f"In pause. Wait for {','.join([op.name for op in get_modals()])} to finish.",icon="EVENT_PAUSE")
		box.label(text="Next export : " + time.strftime("%H:%M:%S (%d/%m/%Y)", next_export()))


def check_timer() -> None:
	if diff := elapse_time_since_last_export() > export_frequency:
		update_interface()
		if check_for_modal(): return interval_check
		bpy.ops.scene.capture_work_collection()
		restart_timer()
	return interval_check

def next_export() -> time.struct_time:
	_next_export = last_export + export_frequency
	return time.localtime(_next_export)

def unregister_timer() -> None:
	if is_registered(): # Session already started
		bpy.app.timers.unregister(check_timer)

def is_registered() -> bool:
	return bpy.app.timers.is_registered(check_timer)

def start_session() -> None:
	session_state = True
	unregister_timer()
	bpy.app.timers.register(check_timer, first_interval=0, persistent=False)

def stop_session() -> None:
	global session_state
	session_state = False
	unregister_timer()

class StartRecordingSession(bpy.types.Operator):
	bl_idname = "scene.tm_start_session"
	bl_label = "Start Recording Session"

	frequence: bpy.props.FloatProperty(name="Export Frequence",min=1,default=5)
	
	@classmethod
	def poll(self, context):
		return True
	
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
	
	def draw(self, context):
		layout = self.layout
		layout.prop(self, "frequency")
	
	def execute(self, context):
		start_session()
		return {"FINISHED"}
	
class StopRecordingSession(bpy.types.Operator):
	bl_idname = "scene.tm_stop_session"
	bl_label = "Stop Recording Session"

	@classmethod
	def poll(self, context):
		return session_state
	
	def execute(self, context):
		stop_session()
		return {"FINISHED"}