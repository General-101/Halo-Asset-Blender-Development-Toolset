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

class ExportGR2(Operator, ExportHelper):
    """Write a Granny file"""
    bl_idname = "export_scene.gr2"
    bl_label = "Export GR2"
    filename_ext = '.GR2'

    filter_glob: StringProperty(
        default="*.gr2",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from ..file_gr2 import export_gr2

        return global_functions.run_code("export_gr2.write_file(context, self.filepath, self.report)")

class ImportGR2(Operator, ImportHelper):
    """Import a Granny file"""
    bl_idname = "import_scene.gr2"
    bl_label = "Import GR2"
    filename_ext = '.GR2'

    filter_glob: StringProperty(
        default="*.gr2",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from ..file_gr2 import import_gr2

        return global_functions.run_code("import_gr2.load_file(context, self.filepath, self.report)")

def menu_func_export(self, context):
    self.layout.operator(ExportGR2.bl_idname, text="Halo Granny V2 (.GR2)")

def menu_func_import(self, context):
    self.layout.operator(ImportGR2.bl_idname, text="Halo Granny V2 (.GR2)")

classeshalo = (
    ExportGR2,
    ImportGR2,
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    #bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    #bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    #bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    #bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
