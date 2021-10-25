# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2021 Steven Garcia
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

from ..global_functions import global_functions

from bpy_extras.io_utils import (
        ImportHelper,
        ExportHelper
        )

from bpy.types import (
        Operator,
        Panel,
        PropertyGroup
        )

from bpy.props import (
        BoolProperty,
        EnumProperty,
        FloatProperty,
        PointerProperty,
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

class ImportQUA(Operator, ImportHelper):
    """Import a QUA file"""
    bl_idname = "import_scene.qua"
    bl_label = "Import QUA"
    filename_ext = '.QUA'

    filter_glob: StringProperty(
        default="*.qua",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from ..file_qua import import_qua

        return global_functions.run_code("import_qua.load_file(context, self.filepath, self.report)")

def menu_func_export(self, context):
    self.layout.operator(ExportQUA.bl_idname, text='Halo Ubercam Animation (.qua)')

def menu_func_import(self, context):
    self.layout.operator(ImportQUA.bl_idname, text="Halo Ubercam Animation (.qua)")

classeshalo = (
    ImportQUA,
    ExportQUA,
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
