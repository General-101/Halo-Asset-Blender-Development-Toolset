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

class ASS_ScenePropertiesGroup(PropertyGroup):
    ass_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="2",
        items=[ ('1', "1", "H2/H3"),
                ('2', "2", "H2/H3"),
                ('3', "3", "H3 Non-functional"),
                ('4', "4", "H3 Non-functional"),
                ('5', "5", "H3 Non-functional"),
                ('6', "6", "H3 Non-functional"),
                ('7', "7", "H3"),
            ]
        )

    ass_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="2",
        items=[ ('1', "1", "H2"),
                ('2', "2", "H2"),
            ]
        )

    ass_version_h3: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="7",
        items=[ ('1', "1", "H3"),
                ('2', "2", "H3"),
                ('3', "3", "H3 Non-functional"),
                ('4', "4", "H3 Non-functional"),
                ('5', "5", "H3 Non-functional"),
                ('6', "6", "H3 Non-functional"),
                ('7', "7", "H3"),
            ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        items=[ ('halo2', "Halo 2", "Export a level intended for Halo 2 Vista or Halo 2 MCC"),
                ('halo3mcc', "Halo 3 MCC", "Export a level intended for Halo 3 MCC"),
            ]
        )

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

    hidden_geo: BoolProperty(
        name ="Export hidden geometry",
        description = "Whether or not we ignore geometry that has scene options that hides it from the viewport",
        default = True,
        )

    folder_structure: BoolProperty(
        name ="Generate Asset Subdirectories",
        description = "Generate folder subdirectories for exported assets",
        default = False,
        )

    apply_modifiers: BoolProperty(
        name ="Apply Modifiers",
        description = "Automatically apply modifiers. Does not permanently affect scene",
        default = True,
        )

    triangulate_faces: BoolProperty(
        name ="Triangulate faces",
        description = "Automatically triangulate all faces. Does not permanently affect scene",
        default = True,
        )

    clean_normalize_weights: BoolProperty(
        name ="Clean and Normalize Weights",
        description = "Remove unused vertex groups and normalize weights before export. Permanently affects scene",
        default = True,
        )

    edge_split: BoolProperty(
        name ="Edge Split",
        description = "Apply a edge split modifier",
        default = True,
        )

    use_edge_angle: BoolProperty(
        name ="Use Edge Angle",
        description = "Split edges with high angle between faces",
        default = False,
        )

    use_edge_sharp: BoolProperty(
        name ="Use Edge Sharp",
        description = "Split edges that are marked as sharp",
        default = True,
        )

    split_angle: FloatProperty(
        name="Split Angle",
        description="Angle above which to split edges",
        subtype='ANGLE',
        default=0.523599,
        min=0.0,
        max=3.141593,
        )

    scale_enum: EnumProperty(
        name="Scale",
        description="Choose a preset value to multiply position values by",
        items=( ('0', "Default(ASS)", "Export as is"),
                ('1', "World Units",  "Multiply position values by 100 units"),
                ('2', "Custom",       "Set your own scale multiplier"),
            )
        )

    scale_float: FloatProperty(
        name="Custom Scale",
        description="Choose a custom value to multiply position values by",
        default=1.0,
        min=1.0,
        )

    console: BoolProperty(
        name ="Console",
        description = "Is your console running",
        default = False,
        options={'HIDDEN'},
        )

class ASS_SceneProps(Panel):
    bl_label = "ASS Scene Properties"
    bl_idname = "ASS_PT_GameVersionPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GameVersionPanel"
    def draw(self, context):
        scene = context.scene
        scene_ass = scene.ass
        scene_halo = scene.halo

        layout = self.layout

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.prop(scene_ass, "game_version", text='')
        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)
        if scene_halo.expert_mode:
            row = col.row()
            row.label(text='ASS Version:')
            if scene_ass.game_version == 'halo2':
                row.prop(scene_ass, "ass_version_h2", text='')

            elif scene_ass.game_version == 'halo3mcc':
                row.prop(scene_ass, "ass_version_h3", text='')

        row = col.row()
        row.label(text='Generate Asset Subdirectories:')
        row.prop(scene_ass, "folder_structure", text='')

        box = layout.box()
        box.label(text="Mask Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Export Hidden Geometry:')
        row.prop(scene_ass, "hidden_geo", text='')

        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Apply Modifiers:')
        row.prop(scene_ass, "apply_modifiers", text='')
        row = col.row()
        row.label(text='Triangulate:')
        row.prop(scene_ass, "triangulate_faces", text='')
        row = col.row()
        row.label(text='Clean and Normalize Weights:')
        row.prop(scene_ass, "clean_normalize_weights", text='')
        row = col.row()
        row.label(text='Use Edge Split:')
        row.prop(scene_ass, "edge_split", text='')
        row = col.row()
        row.label(text='Use As Default Export Settings:')
        row.prop(scene_ass, "use_scene_properties", text='')
        if scene_ass.edge_split == True:
            box = layout.box()
            box.label(text="Edge Split:")
            col = box.column(align=True)
            row = col.row()
            row.label(text='Edge Angle:')
            row.prop(scene_ass, "use_edge_angle", text='')
            row.active = scene_ass.use_edge_angle
            row.prop(scene_ass, "split_angle", text='')
            row = col.row()
            row.label(text='Sharp Edges:')
            row.prop(scene_ass, "use_edge_sharp", text='')

        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.prop(scene_ass, "scale_enum", expand=True)
        if scene_ass.scale_enum == '2':
            row = box.row()
            row.prop(scene_ass, "scale_float")

class ExportASS(Operator, ExportHelper):
    """Write an ASS file"""
    bl_idname = 'export_scene.ass'
    bl_label = 'Export ASS'
    filename_ext = '.ASS'
    ass_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="2",
        items=[ ('1', "1", "H2/H3"),
                ('2', "2", "H2/H3"),
                ('3', "3", "H3 Non-functional"),
                ('4', "4", "H3 Non-functional"),
                ('5', "5", "H3 Non-functional"),
                ('6', "6", "H3 Non-functional"),
                ('7', "7", "H3"),
            ]
        )

    ass_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="2",
        items=[ ('1', "1", "H2"),
                ('2', "2", "H2"),
            ]
        )

    ass_version_h3: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="7",
        items=[ ('1', "1", "H3"),
                ('2', "2", "H3"),
                ('3', "3", "H3 Non-functional"),
                ('4', "4", "H3 Non-functional"),
                ('5', "5", "H3 Non-functional"),
                ('6', "6", "H3 Non-functional"),
                ('7', "7", "H3"),
            ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        items=[ ('halo2', "Halo 2", "Export a level intended for Halo 2 Vista or Halo 2 MCC"),
                ('halo3mcc', "Halo 3 MCC", "Export a level intended for Halo 3 MCC"),
            ]
        )

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

    hidden_geo: BoolProperty(
        name ="Export hidden geometry",
        description = "Whether or not we ignore geometry that has scene options that hides it from the viewport",
        default = True,
        )

    folder_structure: BoolProperty(
        name ="Generate Asset Subdirectories",
        description = "Generate folder subdirectories for exported assets",
        default = False,
        )

    apply_modifiers: BoolProperty(
        name ="Apply Modifiers",
        description = "Automatically apply modifiers. Does not permanently affect scene",
        default = True,
        )

    triangulate_faces: BoolProperty(
        name ="Triangulate faces",
        description = "Automatically triangulate all faces. Does not permanently affect scene",
        default = True,
        )

    clean_normalize_weights: BoolProperty(
        name ="Clean and Normalize Weights",
        description = "Remove unused vertex groups and normalize weights before export. Permanently affects scene",
        default = True,
        )

    edge_split: BoolProperty(
        name ="Edge Split",
        description = "Apply a edge split modifier.",
        default = True,
        )

    use_edge_angle: BoolProperty(
        name ="Use Edge Angle",
        description = "Split edges with high angle between faces.",
        default = False,
        )

    use_edge_sharp: BoolProperty(
        name ="Use Edge Sharp",
        description = "Split edges that are marked as sharp.",
        default = True,
        )

    split_angle: FloatProperty(
        name="Split Angle",
        description="Angle above which to split edges.",
        subtype='ANGLE',
        default=0.523599,
        min=0.0,
        max=3.141593,
        )

    scale_enum: EnumProperty(
        name="Scale",
        description="Choose a preset value to multiply position values by",
        items=( ('0', "Default(ASS)", "Export as is"),
                ('1', "World Units",  "Multiply position values by 100 units"),
                ('2', "Custom",       "Set your own scale multiplier"),
            )
        )

    scale_float: FloatProperty(
        name="Custom Scale",
        description="Choose a custom value to multiply position values by",
        default=1.0,
        min=1.0,
        )

    console: BoolProperty(
        name ="Console",
        description = "Is your console running",
        default = False,
        options={'HIDDEN'},
        )

    filter_glob: StringProperty(
        default="*.ass",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from ..file_ass import export_ass
        keywords = [context,
                    self.filepath,
                    self.report,
                    self.ass_version,
                    self.ass_version_h2,
                    self.ass_version_h3,
                    self.hidden_geo,
                    self.folder_structure,
                    self.apply_modifiers,
                    self.triangulate_faces,
                    self.edge_split,
                    self.use_edge_angle,
                    self.use_edge_sharp,
                    self.split_angle,
                    self.clean_normalize_weights,
                    self.scale_enum,
                    self.scale_float,
                    self.console]

        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            parser.add_argument('-arg2', '--ass_version', dest='ass_version', type=str, default="2")
            parser.add_argument('-arg3', '--game_version', dest='game_version', type=str, default="halo2")
            parser.add_argument('-arg4', '--folder_structure', dest='folder_structure', action='store_true')
            parser.add_argument('-arg5', '--hidden_geo', dest='hidden_geo', action='store_true')
            parser.add_argument('-arg6', '--apply_modifiers', dest='apply_modifiers', action='store_true')
            parser.add_argument('-arg7', '--triangulate_faces', dest='triangulate_faces', action='store_true')
            parser.add_argument('-arg8', '--clean_normalize_weights', dest='clean_normalize_weights', action='store_true')
            parser.add_argument('-arg9', '--edge_split', dest='edge_split', action='store_true')
            parser.add_argument('-arg10', '--use_edge_angle', dest='use_edge_angle', action='store_true')
            parser.add_argument('-arg11', '--split_angle', dest='split_angle', type=float, default=1.0)
            parser.add_argument('-arg12', '--use_edge_sharp', dest='use_edge_sharp', action='store_true')
            parser.add_argument('-arg13', '--scale_enum', dest='scale_enum', type=str, default="0")
            parser.add_argument('-arg14', '--scale_float', dest='scale_float', type=float, default=1.0)
            parser.add_argument('-arg15', '--console', dest='console', action='store_true', default=True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            print('ass_version: ', args.ass_version)
            print('game_version: ', args.game_version)
            print('folder_structure: ', args.folder_structure)
            print('hidden_geo: ', args.hidden_geo)
            print('apply_modifiers: ', args.apply_modifiers)
            print('triangulate_faces: ', args.triangulate_faces)
            print('clean_normalize_weights: ', args.clean_normalize_weights)
            print('edge_split: ', args.edge_split)
            print('use_edge_angle: ', args.use_edge_angle)
            print('split_angle: ', args.split_angle)
            print('use_edge_sharp: ', args.use_edge_sharp)
            print('scale_enum: ', args.scale_enum)
            print('scale_float: ', args.scale_float)
            print('console: ', args.console)
            self.filepath = args.filepath
            self.ass_version = args.ass_version
            self.game_version = args.game_version
            self.folder_structure = args.folder_structure
            self.hidden_geo = args.hidden_geo
            self.apply_modifiers = args.apply_modifiers
            self.triangulate_faces = args.triangulate_faces
            self.clean_normalize_weights = args.clean_normalize_weights
            self.edge_split = args.edge_split
            self.use_edge_angle = args.use_edge_angle
            self.split_angle = args.split_angle
            self.use_edge_sharp = args.use_edge_sharp
            self.scale_enum = args.scale_enum
            self.scale_float = args.scale_float
            self.console = args.console

        return global_functions.run_code("export_ass.write_file(*keywords, self.game_version, get_encoding(self.game_version))")

    def draw(self, context):
        scene = context.scene
        scene_ass = scene.ass
        scene_halo = scene.halo

        layout = self.layout
        is_enabled = True
        if scene_ass.use_scene_properties:
            is_enabled = False

        if scene_ass.use_scene_properties:
            self.game_version = scene_ass.game_version
            self.ass_version_h2 = scene_ass.ass_version_h2
            self.ass_version_h3 = scene_ass.ass_version_h3
            self.folder_structure = scene_ass.folder_structure
            self.hidden_geo = scene_ass.hidden_geo
            self.apply_modifiers = scene_ass.apply_modifiers
            self.triangulate_faces = scene_ass.triangulate_faces
            self.clean_normalize_weights = scene_ass.clean_normalize_weights
            self.edge_split = scene_ass.edge_split
            self.use_edge_angle = scene_ass.use_edge_angle
            self.split_angle = scene_ass.split_angle
            self.use_edge_sharp = scene_ass.use_edge_sharp
            self.scale_enum = scene_ass.scale_enum
            self.scale_float = scene_ass.scale_float

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.prop(self, "game_version", text='')
        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)
        if scene_halo.expert_mode:
            row = col.row()
            row.enabled = is_enabled
            row.label(text='ASS Version:')
            if self.game_version == 'halo2':
                row.prop(self, "ass_version_h2", text='')

            elif self.game_version == 'halo3mcc':
                row.prop(self, "ass_version_h3", text='')

        row = col.row()
        row.enabled = is_enabled
        row.label(text='Generate Asset Subdirectories:')
        row.prop(self, "folder_structure", text='')
        box = layout.box()
        box.label(text="Mask Options:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Export Hidden Geometry:')
        row.prop(self, "hidden_geo", text='')

        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Apply Modifiers:')
        row.prop(self, "apply_modifiers", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Triangulate:')
        row.prop(self, "triangulate_faces", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Clean and Normalize Weights:')
        row.prop(self, "clean_normalize_weights", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Use Edge Split:')
        row.prop(self, "edge_split", text='')
        row = col.row()
        row.label(text='Use Scene Export Settings:')
        row.prop(scene_ass, "use_scene_properties", text='')
        if self.edge_split == True:
            box = layout.box()
            box.label(text="Edge Split:")
            col = box.column(align=True)
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Edge Angle:')
            row.prop(self, "use_edge_angle", text='')
            row.active = self.use_edge_angle
            row.prop(self, "split_angle", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Sharp Edges:')
            row.prop(self, "use_edge_sharp", text='')

        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.enabled = is_enabled
        row.prop(self, "scale_enum", expand=True)
        if self.scale_enum == '2':
            row = box.row()
            row.enabled = is_enabled
            row.prop(self, "scale_float")

class ImportASS(Operator, ImportHelper):
    """Import an ASS file"""
    bl_idname = "import_scene.ass"
    bl_label = "Import ASS"
    filename_ext = '.ASS'

    filter_glob: StringProperty(
        default="*.ass",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from ..file_ass import import_ass
        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            self.filepath = args.filepath

        return global_functions.run_code("import_ass.load_file(context, self.filepath, self.report)")

def menu_func_export(self, context):
    self.layout.operator(ExportASS.bl_idname, text='Halo Amalgam Scene Specification (.ass)')

def menu_func_import(self, context):
    self.layout.operator(ImportASS.bl_idname, text="Halo Amalgam Scene Specification (.ass)")

classeshalo = (
    ASS_ScenePropertiesGroup,
    ASS_SceneProps,
    ImportASS,
    ExportASS,
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.Scene.ass = PointerProperty(type=ASS_ScenePropertiesGroup, name="ASS Scene Properties", description="Set properties for the ASS exporter")

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    del bpy.types.Scene.ass
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
