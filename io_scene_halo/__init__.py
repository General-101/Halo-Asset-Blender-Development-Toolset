# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2023 Steven Garcia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ##### END MIT LICENSE BLOCK #####

# Don't edit the version or build version here or it will break CI
# Need to do this because of Blender parsing the plugin init code instead of actually executing it when getting bl_info
bl_info = {
    "name": "Halo Asset Blender Development Toolset",
    "author": "General_101",
    "version": (117, 343, 65521),
    "blender": (4, 0, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Halo intermediate files Build: BUILD_VERSION_STR",
    "warning": "",
    "wiki_url": "https://c20.reclaimers.net/tools/jointed-model-blender-toolset/",
    "support": 'COMMUNITY',
    "category": "Import-Export"}

import bpy

from bpy.props import (
        IntProperty,
        BoolProperty,
        EnumProperty,
        FloatProperty,
        StringProperty,
        PointerProperty,
        FloatVectorProperty
        )

from . import global_ui
from . import file_ass
from . import file_jma
from . import file_jmi
from . import file_jms
from . import file_qua
from . import file_tag
from . import file_wrl
from . import misc

modules = [
    global_ui,
    file_ass,
    file_jma,
    file_jmi,
    file_jms,
    file_qua,
    file_tag,
    file_wrl,
    misc
]

class HaloAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__
    enable_debug: BoolProperty(
        name ="Enable Debug",
        description = "Enable debug when running a process",
        default = False,
    )

    enable_debugging_pm: BoolProperty(
        name ="Enable Debugging PM",
        description = "More detailed python exception",
        default = False,
    )

    enable_profiling: BoolProperty(
        name ="Enable Profiling",
        description = "Enable profiling to check how long a process is taking",
        default = False,
    )

    enable_crash_report: BoolProperty(
        name ="Enable Crash Report",
        description = "Write crash logs to the users Windows profile",
        default = True,
    )

    override_user_details: BoolProperty(
        name ="Override User Details",
        description = "Write the username and device name set in preferences instead of the hosts details",
        default = False,
    )

    username: StringProperty(
        name = "Username",
        default = "MissingString",
        description = "Set the override name for the user in the ASS file"
        )

    device_name: StringProperty(
        name = "Device Name",
        default = "HiddenIntentions",
        description = "Set the override name for the device in the ASS file"
        )

    shader_gen: EnumProperty(
        name="Shader Gen:",
        description="Setting for the shader generator",
        items=[ ('0', "NONE", "No shaders will be generated during import"),
                ('1', "Simple", "Only the base map or the first bitmap found will be used"),
                ('2', "Full", "Shaders will try to match ingame appearnce if supported"),
               ]
        )

    halo_1_data_path: StringProperty(
        name="Halo 1 Data Path",
        description="Path to the data directory",
        subtype="DIR_PATH"
    )

    halo_1_tag_path: StringProperty(
        name="Halo 1 Tag Path",
        description="Path to the tag directory",
        subtype="DIR_PATH"
    )

    halo_2_data_path: StringProperty(
        name="Halo 2 Data Path",
        description="Path to the data directory",
        subtype="DIR_PATH"
    )

    halo_2_tag_path: StringProperty(
        name="Halo 2 Tag Path",
        description="Path to the tag directory",
        subtype="DIR_PATH"
    )

    halo_3_data_path: StringProperty(
        name="Halo 3 Data Path",
        description="Path to the data directory",
        subtype="DIR_PATH"
    )

    halo_3_tag_path: StringProperty(
        name="Halo 3 Tag Path",
        description="Path to the tag directory",
        subtype="DIR_PATH"
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Debug Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Enable Debug:')
        row.prop(self, "enable_debug", text='')
        row = col.row()
        row.label(text='Enable Debugging PM:')
        row.prop(self, "enable_debugging_pm", text='')
        row = col.row()
        row.label(text='Enable Profiling:')
        row.prop(self, "enable_profiling", text='')
        row = col.row()
        row.label(text='Enable Crash Report:')
        row.prop(self, "enable_crash_report", text='')

        box = layout.box()
        box.label(text="User Detail Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Override User Details:')
        row.prop(self, "override_user_details", text='')
        row = col.row()
        row.label(text='Username:')
        row.prop(self, "username", text='')
        row = col.row()
        row.label(text='Device Name:')
        row.prop(self, "device_name", text='')

        box = layout.box()
        box.label(text="Tag Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Shader Gen:')
        row.prop(self, "shader_gen", text='')
        row = col.row()
        row.label(text='Halo 1 Data Path:')
        row.prop(self, "halo_1_data_path", text='')
        row = col.row()
        row.label(text='Halo 1 Tag Path:')
        row.prop(self, "halo_1_tag_path", text='')
        row = col.row()
        row.label(text='Halo 2 Data Path:')
        row.prop(self, "halo_2_data_path", text='')
        row = col.row()
        row.label(text='Halo 2 Tag Path:')
        row.prop(self, "halo_2_tag_path", text='')
        row = col.row()
        row.label(text='Halo 3 Data Path:')
        row.prop(self, "halo_3_data_path", text='')
        row = col.row()
        row.label(text='Halo 3 Tag Path:')
        row.prop(self, "halo_3_tag_path", text='')

def register():
    bpy.utils.register_class(HaloAddonPrefs)
    for module in modules:
        module.register()

def unregister():
    bpy.utils.unregister_class(HaloAddonPrefs)
    for module in reversed(modules):
        module.unregister()

if __name__ == '__main__':
    register()
