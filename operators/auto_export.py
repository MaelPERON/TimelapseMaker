import bpy
import time

last_export: float = float("-inf")
interval_check = 0.5
export_frequence = 0.5
session_state = False

def elapse_time_since_last_export() -> float:
	return time.monotonic() - last_export

def restart_timer() -> None:
	global last_export
	global session_state
	last_export = time.monotonic()
	session_state = True

def check_timer() -> None:
	if diff := elapse_time_since_last_export() > export_frequence:
		restart_timer()
		print("Export !")
	return interval_check

def unregister_timer() -> None:
	if bpy.app.timers.is_registered(check_timer): # Session already started
		bpy.app.timers.unregister(check_timer)

def start_session() -> None:
	session_state = True
	unregister_timer()
	bpy.app.timers.register(check_timer, first_interval=1, persistent=False)

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
		layout.prop(self, "frequence")
	
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