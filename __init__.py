# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy
from .operators.snapshot import *
from .operators.auto_export import *
from .operators import auto_export as AUTO_EXPORT
from .app import props as PROPS
from .app import driver_variables as VARS
from .ui.panels import *
from .ui.preferences import *

classes = (
    # OPERATORS
    CaptureWorkCollection,
    ImportSnapshot,
    StartRecordingSession,
    StopRecordingSession,

    # UI
    SimplePanel,

    # PREFERENCES
    TM_Preferences
)

modules = (
    PROPS,
    VARS,
    AUTO_EXPORT
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    for module in modules:
        if hasattr(module, "register"):
            module.register()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for module in modules:
        if hasattr(module, "unregister"):
            module.unregister()

if __name__ == "__main__":
    register()