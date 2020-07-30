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
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Export",
    "description": "Export Halo 2/CE Jointed Model Skeleton File (.jms)",
    "warning": "",
    "wiki_url": "https://num0005.github.io/h2codez_docs/w/H2Tool/Render_Model/render_model.html",
    "support": 'COMMUNITY',
    "category": "Import-Export"}

if "bpy" in locals():
    import importlib
    if "import_jms" in locals():
        importlib.reload(import_jms)
    if "export_jms" in locals():
        importlib.reload(export_jms)

import bpy
import sys
import argparse

from bpy_extras.io_utils import (
        ImportHelper,
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
        FloatProperty,
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

class JmsDimensions:
    quat_i_a = '0'
    quat_j_a = '0'
    quat_k_a = '0'
    quat_w_a = '0'
    pos_x_a = '0'
    pos_y_a = '0'
    pos_z_a = '0'
    scale_x_a = '0'
    scale_y_a = '0'
    scale_z_a = '0'
    radius_a = '0'
    pill_z_a = '0'
    quat_i_b = '0'
    quat_j_b = '0'
    quat_k_b = '0'
    quat_w_b = '0'
    pos_x_b = '0'
    pos_y_b = '0'
    pos_z_b = '0'
    scale_x_b = '0'
    scale_y_b = '0'
    scale_z_b = '0'
    radius_b = '0'
    pill_z_b = '0'

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
        row.prop(jms, "bounding_radius")

        row = layout.row()
        row.prop(jms, "Region")

        row = layout.row()
        row.prop(jms, "Permutation")

        row = layout.row()
        row.prop(jms, "level_of_detail")

        row = layout.row()
        row.prop(jms, "Object_Type")

        row = layout.row()
        row.prop(jms, "XREF_path")

class JMS_ObjectPropertiesGroup(PropertyGroup):
    bounding_radius: BoolProperty(
        name ="Bounding Radius",
        description = "Sets object as a bounding radius",
        default = False,
        )

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
        items=[ ('0', "NONE", ""),
                ('1', "L1", ""),
                ('2', "L2", ""),
                ('3', "L3", ""),
                ('4', "L4", ""),
                ('5', "L5", ""),
                ('6', "L6", ""),
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

    XREF_path: StringProperty(
        name="XREF Object",
        description="Select a path to a .MAX file",
        subtype="FILE_PATH"
    )

class ExportJMS(Operator, ExportHelper):
    """Write a JMS file"""
    bl_idname = "export_scene.jms"
    bl_label = "Export JMS"

    filename_ext = ''

    extension_ce: EnumProperty(
        name="Extension:",
        description="What extension to use for the model file",
        items=[ ('.JMS', "JMS", "Jointed Model Skeleton CE"),
                ('.JMP', "JMP", "Jointed Model Physics CE"),
               ]
        )

    extension_h2: EnumProperty(
        name="Extension:",
        description="What extension to use for the model file",
        items=[ ('.JMS', "JMS", "Jointed Model Skeleton H2"),
               ]
        )

    jms_version_ce: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8200",
        items=[ ('8197', "8197", "CE Non-functional"),
                ('8198', "8198", "CE Non-functional"),
                ('8199', "8199", "CE Non-functional"),
                ('8200', "8200", "CE"),
               ]
        )

    jms_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8210",
        items=[ ('8197', "8197", "H2 Non-functional"),
                ('8198', "8198", "H2 Non-functional"),
                ('8199', "8199", "H2 Non-functional"),
                ('8200', "8200", "H2"),
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

    scale_enum: EnumProperty(
    name="Scale",
        items=(
            ('0', "Default", "Export at 1:1"),
            ('1', "JMS",     "Export at x100"),
            ('2', "Custom",  "Set your own scaling multiplier."),
        )
    )
    scale_float: FloatProperty(
        name="Custom Scale",
        description="Choose a custom value to multiply position values by.",
        default=1.0,
        min=1.0,
    )

    filter_glob: StringProperty(
        default="*.jms;*.jmp",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from . import export_jms
        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            parser.add_argument('-arg2', '--extension_ce', dest='extension_ce', type=str, default=".JMS")
            parser.add_argument('-arg3', '--extension_h2', dest='extension_h2', type=str, default=".JMS")
            parser.add_argument('-arg4', '--jms_version_ce', dest='jms_version_ce', type=str, default="8200")
            parser.add_argument('-arg5', '--jms_version_h2', dest='jms_version_h2', type=str, default="8210")
            parser.add_argument('-arg6', '--game_version', dest='game_version', type=str, default="halo2")
            parser.add_argument('-arg7', '--triangulate_faces', dest='triangulate_faces', action='store_true')
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            print('extension_ce: ', args.extension_ce)
            print('extension_h2: ', args.extension_h2)
            print('jms_version_ce: ', args.jms_version_ce)
            print('jms_version_h2: ', args.jms_version_h2)
            print('game_version: ', args.game_version)
            print('triangulate_faces: ', args.triangulate_faces)
            self.filepath = args.filepath
            self.extension_ce = args.extension_ce
            self.extension_h2 = args.extension_h2
            self.jms_version_ce = args.jms_version_ce
            self.jms_version_h2 = args.jms_version_h2
            self.game_version = args.game_version
            self.triangulate_faces = args.triangulate_faces

        return export_jms.write_file(context, self.filepath, self.report, self.extension_ce, self.extension_h2, self.jms_version_ce, self.jms_version_h2, self.game_version, self.triangulate_faces, self.scale_enum, self.scale_float)

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="File Details:")
        row = box.row()
        row.prop(self, "game_version")

        if self.game_version == 'haloce':
            row = box.row()
            row.prop(self, "extension_ce")
            row = box.row()
            row.prop(self, "jms_version_ce")

        elif self.game_version == 'halo2':
            row = box.row()
            row.prop(self, "extension_h2")
            row = box.row()
            row.prop(self, "jms_version_h2")

        box = layout.box()
        box.label(text="Triangulate:")
        row = box.row()
        row.prop(self, "triangulate_faces")

        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.prop(self, "scale_enum", expand=True)

        if self.scale_enum == '2':
            row = box.row()
            row.prop(self, "scale_float")

class ImportJMS(Operator, ImportHelper):
    """Import a JMS file"""
    bl_idname = "import_scene.jms"
    bl_label = "Import JMS"

    filename_ext = '.JMS'

    filter_glob: StringProperty(
        default="*.jms;*.jmp",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from . import import_jms
        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)

        if len(self.filepath) == 0:
            self.filepath = args.filepath

        return import_jms.load_file(context, self.filepath, self.report)

def menu_func_export(self, context):
    self.layout.operator(ExportJMS.bl_idname, text="Halo Jointed Model Skeleton (.jms)")

def menu_func_import(self, context):
    self.layout.operator(ImportJMS.bl_idname, text="Halo Jointed Model Skeleton (.jms)")

classesjms = (
    JMS_ObjectPropertiesGroup,
    JMS_ObjectProps,
    ImportJMS,
    ExportJMS
)

def register():
    for clsjms in classesjms:
        bpy.utils.register_class(clsjms)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.Object.jms = PointerProperty(type=JMS_ObjectPropertiesGroup, name="JMS Object Properties", description="JMS Object properties")

def unregister():
    for clsjms in reversed(classesjms):
        bpy.utils.unregister_class(clsjms)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    del bpy.types.Object.jms

if __name__ == '__main__':
    register()
