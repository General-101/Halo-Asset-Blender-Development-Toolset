# ##### BEGIN UNLICENSED BLOCK #####
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>
#
# ##### END UNLICENSED BLOCK #####

bl_info = {
    "name": "Blend2Halo2 JMS",
    "author": "Cyboryxmen, modified by Fulsy + MosesofEgypt + General_101",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "File > Export",
    "description": "Export Halo 2/CE Jointed Model Skeleton File (.jms)",
    "warning": "",
    "wiki_url": "https://num0005.github.io/h2codez_docs/w/H2Tool/Render_Model/render_model.html",
    "support": 'COMMUNITY',
    "category": "Import-Export"}

import bpy
import sys
import argparse
import io_scene_jms.export_jms as halo

from bpy_extras.io_utils import (
        ExportHelper,
        )

from bpy.types import (
        Operator,
        Panel,
        PropertyGroup,
        )

from bpy.props import (
        BoolProperty,
        EnumProperty,
        PointerProperty,
        StringProperty,
        )

class JmsVertex:
    node_influence_count = '0'
    node0 = '-1'
    node1 = '-1'
    node2 = '-1'
    node3 = '-1'
    node0_weight = '0.0000000000'
    node1_weight = '0.0000000000'
    node2_weight = '0.0000000000'
    node3_weight = '0.0000000000'
    pos = None
    norm = None
    uv = None

class JmsTriangle:
    v0 = 0
    v1 = 0
    v2 = 0
    region = 0
    material = 0

class JMS_ObjectProps(Panel):
    bl_label = "JMS Object Properties"
    bl_idname = "JMS_PT_RegionPermutationPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        obj = context.object
        jms = obj.jms

        row = layout.row()
        row.prop(jms, "Region")

        row = layout.row()
        row.prop(jms, "Permutation")

        row = layout.row()
        row.prop(jms, "level_of_detail")

        row = layout.row()
        row.prop(jms, "Object_Type")

class JMS_ObjectPropertiesGroup(PropertyGroup):
    Region : StringProperty(
        name = "Region",
        default = "",
        description = "Set region name."
        )

    Permutation : StringProperty(
        name = "Permutation",
        default = "",
        description = "Set permutation name."
        )

    level_of_detail: EnumProperty(
        name="LOD:",
        description="What LOD to use for the object",
        items=[ ('0', "L1", ""),
                ('1', "L2", ""),
                ('2', "L3", ""),
                ('3', "L4", ""),
                ('4', "L5", ""),
                ('5', "L6", ""),
               ]
        )

    Object_Type : EnumProperty(
        name="Object Type",
        description="Select object type to write mesh as",
        default = "CONVEX SHAPES",
        items=[ ('SPHERE', "Sphere", ""),
                ('BOX', "Box", ""),
                ('CAPSULES', "Pill", ""),
                ('CONVEX SHAPES', "Convex Shape", ""),
               ]
        )

class ExportJMS(Operator, ExportHelper):
    """Write a JMS file"""
    bl_idname = "export_jms.export"
    bl_label = "Export JMS"

    filename_ext = ''

    encoding: EnumProperty(
        name="Encoding:",
        description="What encoding to use for the model file",
        default="UTF-16LE",
        items=[ ('utf_8', "UTF-8", "For CE"),
                ('UTF-16LE', "UTF-16", "For H2"),
               ]
        )

    extension: EnumProperty(
        name="Extension:",
        description="What extension to use for the model file",
        items=[ ('.JMS', "JMS", "Jointed Model Skeleton CE/H2"),
                ('.JMP', "JMP", "Jointed Model Physics CE"),
               ]
        )

    jms_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8200",
        items=[ ('8197', "8197", "CE/H2 Non-functional"),
                ('8198', "8198", "CE/H2 Non-functional"),
                ('8199', "8199", "CE/H2 Non-functional"),
                ('8200', "8200", "CE/H2"),
                ('8201', "8201", "H2 Non-functional"),
                ('8202', "8202", "H2 Non-functional"),
                ('8203', "8203", "H2 Non-functional"),
                ('8204', "8204", "H2 Non-functional"),
                ('8205', "8205", "H2"),
                ('8206', "8206", "H2 Non-functional"),
                ('8207', "8207", "H2 Non-functional"),
                ('8208', "8208", "H2 Non-functional"),
                ('8209', "8209", "H2"),
                ('8210', "8210", "H2"),
               ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        default="halo2",
        items=[ ('haloce', "Halo CE", "Export a JMS intended for Halo Custom Edition"),
                ('halo2', "Halo 2", "Export a JMS intended for Halo 2 Vista"),
               ]
        )

    triangulate_faces: BoolProperty(
        name ="Triangulate faces",
        description = "Automatically triangulate all faces (recommended)",
        default = True,
        )

    filter_glob: StringProperty(
        default="*.jms;*.jmp",
        options={'HIDDEN'},
        )

    def execute(self, context):
        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            parser.add_argument('-arg2', '--encoding', dest='encoding', type=str, default="UTF-16LE")
            parser.add_argument('-arg3', '--extension', dest='extension', type=str, default=".JMS")
            parser.add_argument('-arg4', '--jms_version', dest='jms_version', type=str, default="8200")
            parser.add_argument('-arg5', '--game_version', dest='game_version', type=str, default="halo2")
            parser.add_argument('-arg6', '--triangulate_faces', dest='triangulate_faces', action='store_true')
            args = parser.parse_known_args(argv)[0]
            # print parameters
            print('filepath: ', args.filepath)
            print('encoding: ', args.encoding)
            print('extension: ', args.extension)
            print('jms_version: ', args.jms_version)
            print('game_version: ', args.game_version)
            print('triangulate_faces: ', args.triangulate_faces)

        if len(self.filepath) == 0:
            self.filepath = args.filepath
            self.encoding = args.encoding
            self.extension = args.extension
            self.jms_version = args.jms_version
            self.game_version = args.game_version
            self.triangulate_faces = args.triangulate_faces

        return halo.export_jms(context, self.filepath, self.report, self.encoding, self.extension, self.jms_version, self.game_version, self.triangulate_faces)

def menu_func_export(self, context):
    self.layout.operator(ExportJMS.bl_idname, text="Halo Jointed Model Skeleton (.jms)")

classesjms = (
    JMS_ObjectPropertiesGroup,
    JMS_ObjectProps,
    ExportJMS
)

def register():
    for clsjms in classesjms:
        bpy.utils.register_class(clsjms)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.Object.jms = PointerProperty(type=JMS_ObjectPropertiesGroup, name="JMS Object Properties", description="JMS Object properties")

def unregister():
    for clsjms in reversed(classesjms):
        bpy.utils.unregister_class(clsjms)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    del bpy.types.Object.jms

if __name__ == '__main__':
    register()
