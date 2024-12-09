import bpy

def name() -> str:
    return __package__.replace(".utils", '')

def preferences():
    return bpy.context.preferences.addons[name()].preferences