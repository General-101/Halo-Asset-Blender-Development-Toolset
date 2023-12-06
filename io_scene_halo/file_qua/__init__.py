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

import bpy

from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from ..global_functions import global_functions
from bpy.props import (
        EnumProperty,
        StringProperty
        )

class ExportQUA(Operator, ExportHelper):
    """Write a QUA file"""
    bl_idname = 'export_scene.qua'
    bl_label = 'Export QUA'
    filename_ext = '.QUA'

    qua_version: EnumProperty(
        name="Version:",
        description="What version to use for the Ubercam file",
        default="5",
        items=[ ('1', "1", "Non-functional"),
                ('2', "2", "Non-functional"),
                ('3', "3", "Non-functional"),
                ('4', "4", "Non-functional"),
                ('5', "5", "Non-functional"),
            ]
        )

    filter_glob: StringProperty(
        default="*.qua",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from ..file_qua import export_qua

        return global_functions.run_code("export_qua.write_file(context, self.filepath, self.report, self.qua_version)")

def menu_func_export(self, context):
    self.layout.operator(ExportQUA.bl_idname, text='Halo Ubercam Animation (.qua)')

def register():
    bpy.utils.register_class(ExportQUA)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(ExportQUA)

if __name__ == '__main__':
    register()
