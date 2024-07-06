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

from ..global_functions import global_functions
from bpy.props import (
        EnumProperty,
        StringProperty,
        BoolProperty
        )
from bpy.types import Operator
from bpy_extras.io_utils import (
    ImportHelper,
    ExportHelper
    )

try:
    from bpy.types import (
        FileHandler,
        OperatorFileListElement
        )
except ImportError:
    print("Blender is out of date. Drag and drop will not function")
    FileHandler = None
    OperatorFileListElement = None


class ExportQUA(Operator, ExportHelper):
    """Write a QUA file"""
    bl_idname = 'export_scene.qua'
    bl_label = 'Export QUA'
    filename_ext = '.QUA'

    game_title: EnumProperty(
        name="Game Title:",
        description="What game will the Ubercam file be used for",
        items=[ ('halo3', "Halo 3", "Export a QUA intended for Halo 3"),
                ('halor', "Halo Reach", "Export a QUA intended for Halo Reach"),
                ('halo4', "Halo 4", "Export a QUA intended for Halo 4"),
            ]
        )

    qua_version: EnumProperty(
        name="Version:",
        description="What version to use for the Ubercam file",
        default="5",
        items=[ ('1', "1", "Non-functional"),
                ('2', "2", "Non-functional"),
                ('3', "3", "Non-functional"),
                ('4', "4", "Non-functional"),
                ('5', "5", "Retail"),
            ]
        )

    strip_identifier: BoolProperty(
        name ="Strip Identifier",
        description = "Strip identifier from filename of animation paths",
        default = True,
        )

    filter_glob: StringProperty(
        default="*.qua",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from ..file_qua import export_qua

        return global_functions.run_code("export_qua.write_file(context, self.filepath, self.game_title, int(self.qua_version), self.strip_identifier, self.report)")

    def draw(self, context):
        scene = context.scene
        scene_halo = scene.halo

        layout = self.layout

        box = layout.box()
        box.label(text="Game Title:")
        col = box.column(align=True)
        row = col.row()
        row.prop(self, "game_title", text='')
        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)
        if scene_halo.expert_mode:
            row = col.row()
            row.label(text='QUA Version:')
            row.prop(self, "qua_version", text='')

        row = col.row()
        row.label(text='Strip Identifier:')
        row.prop(self, "strip_identifier", text='')

class ImportQUA(Operator, ImportHelper):
    """Import a QUA file"""
    bl_idname = "import_scene.qua"
    bl_label = "Import QUA"
    filename_ext = '.QUA'

    game_title: EnumProperty(
        name="Game Title:",
        description="What game was the cinematic file made for",
        default="auto",
        items=[ ('auto', "Auto", "Attempt to guess the game this animation was intended for. Will default to Halo CE if this fails."),
                ('halo1', "Halo 1", "Import an animation intended for Halo 1"),
                ('halo2', "Halo 2", "Import an animation intended for Halo 2"),
                ('halo3', "Halo 3", "Import an animation intended for Halo 3"),
            ]
        )

    filter_glob: StringProperty(
        default="*.qua",
        options={'HIDDEN'},
        )

    filepath: StringProperty(
        subtype='FILE_PATH', 
        options={'SKIP_SAVE'}
        )

    def execute(self, context):
        from ..file_qua import import_qua

        return global_functions.run_code("import_qua.load_file(context, self.filepath, self.report)")

    def invoke(self, context, event):
        if self.filepath:
            return self.execute(context)
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class ImportQUA_FileHandler(FileHandler):
    bl_idname = "QUA_FH_import"
    bl_label = "File handler for QUA import"
    bl_import_operator = "import_scene.qua"
    bl_file_extensions = ".QUA"

    @classmethod
    def poll_drop(cls, context):
        return (context.area and context.area.type == 'VIEW_3D')

def menu_func_export(self, context):
    self.layout.operator(ExportQUA.bl_idname, text='Halo Ubercam Animation (.qua)')

def menu_func_import(self, context):
    self.layout.operator(ImportQUA.bl_idname, text="Halo Ubercam Animation (.qua)")

classeshalo = (
    ImportQUA,
    ImportQUA_FileHandler,
    ExportQUA
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
