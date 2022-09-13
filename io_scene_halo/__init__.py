# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2020 Steven Garcia
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
import bpy
from bpy.types import Operator, AddonPreferences, PropertyGroup
from bpy.props import StringProperty, IntProperty, BoolProperty, PointerProperty

bl_info = {
    "name": "Halo Asset Blender Development Toolset",
    "author": "General_101",
    "version": (117, 343, 65521),
    "blender": (3, 0, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Halo intermediate files Build: BUILD_VERSION_STR",
    "warning": "",
    "wiki_url": "https://c20.reclaimers.net/tools/jointed-model-blender-toolset/",
    "support": 'COMMUNITY',
    "category": "Import-Export"}

from . import global_ui
from . import file_ass
from . import file_jma
from . import file_jmi
from . import file_jms
from . import file_qua
from . import file_tag
from . import file_wrl
from . import file_fbx
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
    file_fbx,
    misc
]

class HREKLocation(bpy.types.Operator):
    bl_idname = 'hrek.path'
    bl_label = 'HREK Path'
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences

        info = ("Path: %s" %
                (addon_prefs.hrek_path))

        self.report({'INFO'}, info)
        print(info)
        return {"FINISHED"}
 
 
class HREKLocationPanel(bpy.types.Panel):
    bl_idname = 'toolpref.panel'
    bl_label = 'TOOL_LOCATION'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TEST'
 
    def draw(self, context):
        self.layout.operator("hrek.path", icon=None, text="Specify HREK Path")
 
 
class HREKLocationPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    hrek_path: bpy.props.StringProperty(
        name="HREK Path",
        description="Specify path to your HREK tools",
        default="",
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, 'hrek_path', expand=True)

def register():
    bpy.utils.register_class(HREKLocation)
    bpy.utils.register_class(HREKLocationPanel)
    bpy.utils.register_class(HREKLocationPreferences)
    bpy.types.AddonPreferences.toolpath = StringProperty(type=HREKLocationPreferences, name="HREK Path", description="Set path of Halo Reach mod tools folder")
    for module in modules:
        module.register()

def unregister():
    bpy.utils.unregister_class(HREKLocationPreferences)
    bpy.utils.unregister_class(HREKLocationPanel)
    bpy.utils.unregister_class(HREKLocation)
    for module in reversed(modules):
        module.unregister()

if __name__ == '__main__':
    register()
