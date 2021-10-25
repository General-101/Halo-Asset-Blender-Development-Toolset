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
import sys
import argparse

from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper
from ..global_functions import global_functions

class ImportWRL(Operator, ImportHelper):
    """Import a Halo WRL file"""
    bl_idname = "import_scene.wrl"
    bl_label = "Import WRL"
    filename_ext = '.WRL'

    filter_glob: StringProperty(
        default="*.wrl",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from io_scene_halo.file_wrl import import_wrl
        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            self.filepath = args.filepath

        return global_functions.run_code("import_wrl.convert_wrl_to_blend(context, self.filepath, self.report)")

def menu_func_import(self, context):
    self.layout.operator(ImportWRL.bl_idname, text="Halo WRL Debug Geometry (.wrl)")

def register():
    bpy.utils.register_class(ImportWRL)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(ImportWRL)

if __name__ == '__main__':
    register()
