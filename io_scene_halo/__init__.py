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
from bpy.types import AddonPreferences, Operator
from bpy.props import StringProperty, EnumProperty

bl_info = {
    "name": "Halo Asset Blender Development Toolset",
    "author": "General_101, Crisp, GeneralKidd",
    "version": (117, 343, 65521),
    "blender": (3, 3, 0),
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
from . import file_gr2
from . import misc
from .misc import GR2

modules = [
    global_ui,
    file_ass,
    file_jma,
    file_jmi,
    file_jms,
    file_qua,
    file_tag,
    file_wrl,
    file_gr2,
    misc,
    GR2
]
 
class ToolkitLocationPreferences(AddonPreferences):
    bl_idname = __package__
    
    hrek_path: StringProperty(
        name="HREK Path",
        description="Specify the path to your Halo Reach Editing Kit folder containing tool / tool_fast",
        default="",
    )

    h4ek_path: StringProperty(
        name="HREK Path",
        description="Specify the path to your Halo 4 Editing Kit folder containing tool / tool_fast",
        default="",
    )

    h2aek_path: StringProperty(
        name="H2AEK Path",
        description="Specify the path to your Halo 2 Anniversary MP Editing Kit folder containing tool / tool_fast",
        default="",
    )

    tool_type: EnumProperty(
        name="Tool Type",
        description="Specify whether the add on should use Tool or Tool Fast",
        default="tool_fast",
        items=[('tool_fast', 'Tool Fast', ''), ('tool', 'Tool', '')]
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text='HREK Path')
        row = layout.row()
        row.prop(self, 'hrek_path', text='')
        row = layout.row()
        row.label(text='H4EK Path')
        row = layout.row()
        row.prop(self, 'h4ek_path', text='')
        row = layout.row()
        row.label(text='H2AEK Path')
        row = layout.row()
        row.prop(self, 'h2aek_path', text='')
        row = layout.row()
        row.label(text='Tool Type')
        row.prop(self, 'tool_type', expand=True)

def register():
    bpy.utils.register_class(ToolkitLocationPreferences)
    for module in modules:
        module.register()

def unregister():
    bpy.utils.unregister_class(ToolkitLocationPreferences)
    for module in reversed(modules):
        module.unregister()

if __name__ == '__main__':
    register()
