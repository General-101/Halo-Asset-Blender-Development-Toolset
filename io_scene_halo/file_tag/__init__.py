# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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
from bpy.props import (
        BoolProperty,
        EnumProperty
        )

from bpy_extras.io_utils import ImportHelper

from ..global_functions import global_functions

class ImportTag(Operator, ImportHelper):
    """Import a tag for various Halo titles"""
    bl_idname = "import_scene.tag"
    bl_label = "Import Tag"

    fix_rotations: BoolProperty(
        name ="Fix Rotations",
        description = "Set rotations to match what you would visually see in 3DS Max. Rotates bones by 90 degrees on a local Z axis to match how Blender handles rotations",
        default = False,
        )

    def execute(self, context):
        from ..file_tag import import_tag

        return global_functions.run_code("import_tag.load_file(context, self.filepath, self.fix_rotations, self.report)")

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Import Options:")
        col = box.column(align=True)

        row = col.row()
        row.label(text='Fix Rotations:')
        row.prop(self, "fix_rotations", text='')

def menu_func_import(self, context):
    self.layout.operator(ImportTag.bl_idname, text="Halo Tag (mode/mod2/coll/phys/antr/sbsp)")

def register():
    bpy.utils.register_class(ImportTag)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(ImportTag)

if __name__ == '__main__':
    register()
