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
import sys
import argparse

from ..global_functions import global_functions

from bpy_extras.io_utils import ExportHelper

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

class JMI_FilePropertiesGroup(PropertyGroup):
    permutation_ce: StringProperty(
        name="Permutation",
        description="Permutation for the JMS file",
        subtype="FILE_NAME"
        )

    level_of_detail_ce: EnumProperty(
        name="LOD:",
        description="What LOD to use for the JMS file",
        items=[ ('0', "NONE", ""),
                ('1', "Super Low", ""),
                ('2', "Low", ""),
                ('3', "Medium", ""),
                ('4', "High", ""),
                ('5', "Super High", ""),
            ]
        )

class JMI_FileProps(Panel):
    bl_label = "JMI Properties"
    bl_idname = "JMI_PT_FilePanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "HALO_PT_MeshDetailsPanel"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        scene_halo = scene.halo

        obj = context.object
        is_ce_world_node = None
        if hasattr(obj, 'jmi') and obj.name[0:1].lower() == '!' and scene_halo.game_version == 'haloce':
            is_ce_world_node = True

        return is_ce_world_node

    def draw(self, context):
        layout = self.layout

        obj = context.object
        obj_jmi = obj.jmi

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Permutation:')
        row.prop(obj_jmi, "permutation_ce", text='')
        row = col.row()
        row.label(text='LOD:')
        row.prop(obj_jmi, "level_of_detail_ce", text='')

class JMI_ScenePropertiesGroup(PropertyGroup):
    jmi_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file. Versions below 8207 will not have a JMI file",
        default="8210",
        options={'HIDDEN'},
        items=[ ('8197', "8197", "CE/H2/H3"),
                ('8198', "8198", "CE/H2/H3"),
                ('8199', "8199", "CE/H2/H3"),
                ('8200', "8200", "CE/H2/H3"),
                ('8201', "8201", "H2/H3 Non-functional"),
                ('8202', "8202", "H2/H3 Non-functional"),
                ('8203', "8203", "H2/H3 Non-functional"),
                ('8204', "8204", "H2/H3 Non-functional"),
                ('8205', "8205", "H2/H3"),
                ('8206', "8206", "H2/H3 Non-functional"),
                ('8207', "8207", "H2/H3 Non-functional"),
                ('8208', "8208", "H2/H3 Non-functional"),
                ('8209', "8209", "H2/H3"),
                ('8210', "8210", "H2/H3"),
                ('8211', "8211", "H3 Non-functional"),
                ('8212', "8212", "H3 Non-functional"),
                ('8213', "8213", "H3"),
            ]
        )

    jmi_version_ce: EnumProperty(
        name="Version:",
        description="What version to use for the model file. No JMI file will be written",
        default="8200",
        items=[ ('8197', "8197", "CE"),
                ('8198', "8198", "CE"),
                ('8199', "8199", "CE"),
                ('8200', "8200", "CE"),
            ]
        )

    jmi_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the model file. Versions below 8207 will not have a JMI file",
        default="8210",
        items=[ ('8197', "8197", "CE/H2"),
                ('8198', "8198", "CE/H2"),
                ('8199', "8199", "CE/H2"),
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

    jmi_version_h3: EnumProperty(
        name="Version:",
        description="What version to use for the model file. Versions below 8207 will not have a JMI file",
        default="8213",
        items=[ ('8197', "8197", "CE/H2/H3"),
                ('8198', "8198", "CE/H2/H3"),
                ('8199', "8199", "CE/H2/H3"),
                ('8200', "8200", "CE/H2/H3"),
                ('8201', "8201", "H2/H3 Non-functional"),
                ('8202', "8202", "H2/H3 Non-functional"),
                ('8203', "8203", "H2/H3 Non-functional"),
                ('8204', "8204", "H2/H3 Non-functional"),
                ('8205', "8205", "H2/H3"),
                ('8206', "8206", "H2/H3 Non-functional"),
                ('8207', "8207", "H2/H3 Non-functional"),
                ('8208', "8208", "H2/H3 Non-functional"),
                ('8209', "8209", "H2/H3"),
                ('8210', "8210", "H2/H3"),
                ('8211', "8211", "H3 Non-functional"),
                ('8212', "8212", "H3 Non-functional"),
                ('8213', "8213", "H3"),
            ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        items=[ ('haloce', "Halo CE", "Export a JMS set intended for Halo Custom Edition or Halo 1 MCC"),
                ('halo2', "Halo 2", "Export a JMS set intended for Halo 2 Vista or Halo 2 MCC"),
                ('halo3mcc', "Halo 3 MCC", "Export a JMS set intended for Halo 3 MCC"),
            ]
        )

    folder_type: EnumProperty(
        name="Model Type:",
        description="What type to use for the model file",
        default="0",
        items=[ ('0', "Structure", "Asset subdirectory intended for levels"),
                ('1', "Render", "Asset subdirectory intended for models"),
            ]
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

    loop_normals: BoolProperty(
        name ="Use Loop Normals",
        description = "Use loop data for normals instead of vertex. May not match original 3DS Max output at the moment.",
        default = True,
        )

    clean_normalize_weights: BoolProperty(
        name ="Clean and Normalize Weights",
        description = "Remove unused vertex groups and normalize weights before export. Permanently affects scene",
        default = True,
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

    nonrender_geo: BoolProperty(
        name ="Export non-render geometry",
        description = "Whether or not we ignore geometry that has scene options that hides it from the render output",
        default = True,
        )

    export_render: BoolProperty(
        name ="Export render geometry",
        description = "Whether or not we ignore geometry that is marked as render",
        default = True,
        )

    export_collision: BoolProperty(
        name ="Export collision geometry",
        description = "Whether or not we ignore geometry that is marked as collision",
        default = True,
        )

    export_physics: BoolProperty(
        name ="Export physics geometry",
        description = "Whether or not we ignore geometry that is marked as physics",
        default = True,
        )

    write_textures: BoolProperty(
        name ="Write textures",
        description = "Whether or not we write texture paths for materials",
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
        items=( ('0', "Default(JMS)", "Export as is"),
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

class JMI_SceneProps(Panel):
    bl_label = "JMI Scene Properties"
    bl_idname = "JMI_PT_GameVersionPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_ScenePropertiesPanel"
    def draw(self, context):
        scene = context.scene
        scene_jmi = scene.jmi
        scene_halo = scene.halo

        layout = self.layout

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.prop(scene_jmi, "game_version", text='')
        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)
        if scene_halo.expert_mode:
            row = col.row()
            row.label(text='JMI Version:')
            if scene_jmi.game_version == 'haloce':
                row.prop(scene_jmi, "jmi_version_ce", text='')

            elif scene_jmi.game_version == 'halo2mcc':
                row.prop(scene_jmi, "jmi_version_h2", text='')

            elif scene_jmi.game_version == 'halo3mcc':
                row.prop(scene_jmi, "jmi_version_h3", text='')

        row = col.row()
        row.label(text='Write Texture Paths:')
        row.prop(scene_jmi, "write_textures", text='')

        box = layout.box()
        box.label(text="Mask Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Export Hidden Geometry:')
        row.prop(scene_jmi, "hidden_geo", text='')
        row = col.row()
        row.label(text='Export Non-render Geometry:')
        row.prop(scene_jmi, "nonrender_geo", text='')

        row = col.row()
        row.label(text='Export Render Geometry:')
        row.prop(scene_jmi, "export_render", text='')
        row = col.row()
        row.label(text='Export Collision Geometry:')
        row.prop(scene_jmi, "export_collision", text='')
        row = col.row()
        row.label(text='Export Physics Geometry:')
        row.prop(scene_jmi, "export_physics", text='')

        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Apply Modifiers:')
        row.prop(scene_jmi, "apply_modifiers", text='')
        row = col.row()
        row.label(text='Triangulate:')
        row.prop(scene_jmi, "triangulate_faces", text='')
        row = col.row()
        row.label(text='Use Loop Normals:')
        row.prop(scene_jmi, "loop_normals", text='')
        row = col.row()
        row.label(text='Clean and Normalize Weights:')
        row.prop(scene_jmi, "clean_normalize_weights", text='')
        row = col.row()
        row.label(text='Use Edge Split:')
        row.prop(scene_jmi, "edge_split", text='')
        row = col.row()
        row.label(text='Use As Default Export Settings:')
        row.prop(scene_jmi, "use_scene_properties", text='')

        if not scene_jmi.game_version == 'haloce':
            box = layout.box()
            box.label(text="Subdirectory Type:")
            col = box.column(align=True)
            row = col.row()
            row.label(text='Model Type:')
            row.prop(scene_jmi, "folder_type", text='')

        if scene_jmi.edge_split == True:
            box = layout.box()
            box.label(text="Edge Split:")
            col = box.column(align=True)
            row = col.row()
            row.label(text='Edge Angle:')
            row.prop(scene_jmi, "use_edge_angle", text='')
            row.active = scene_jmi.use_edge_angle
            row.prop(scene_jmi, "split_angle", text='')
            row = col.row()
            row.label(text='Sharp Edges:')
            row.prop(scene_jmi, "use_edge_sharp", text='')

        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.prop(scene_jmi, "scale_enum", expand=True)
        if scene_jmi.scale_enum == '2':
            row = box.row()
            row.prop(scene_jmi, "scale_float")

class ExportJMI(Operator, ExportHelper):
    """Write a JMI file"""
    bl_idname = "export_jmi.export"
    bl_label = "Export JMI"
    filename_ext = ''

    jmi_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file. Versions below 8207 will not have a JMI file",
        default="8210",
        options={'HIDDEN'},
        items=[ ('8197', "8197", "CE/H2/H3"),
                ('8198', "8198", "CE/H2/H3"),
                ('8199', "8199", "CE/H2/H3"),
                ('8200', "8200", "CE/H2/H3"),
                ('8201', "8201", "H2/H3 Non-functional"),
                ('8202', "8202", "H2/H3 Non-functional"),
                ('8203', "8203", "H2/H3 Non-functional"),
                ('8204', "8204", "H2/H3 Non-functional"),
                ('8205', "8205", "H2/H3"),
                ('8206', "8206", "H2/H3 Non-functional"),
                ('8207', "8207", "H2/H3 Non-functional"),
                ('8208', "8208", "H2/H3 Non-functional"),
                ('8209', "8209", "H2/H3"),
                ('8210', "8210", "H2/H3"),
                ('8211', "8211", "H3 Non-functional"),
                ('8212', "8212", "H3 Non-functional"),
                ('8213', "8213", "H3"),
            ]
        )

    jmi_version_ce: EnumProperty(
        name="Version:",
        description="What version to use for the model file. No JMI file will be written",
        default="8200",
        items=[ ('8197', "8197", "CE"),
                ('8198', "8198", "CE"),
                ('8199', "8199", "CE"),
                ('8200', "8200", "CE"),
            ]
        )

    jmi_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the model file. Versions below 8207 will not have a JMI file",
        default="8210",
        items=[ ('8197', "8197", "CE/H2"),
                ('8198', "8198", "CE/H2"),
                ('8199', "8199", "CE/H2"),
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

    jmi_version_h3: EnumProperty(
        name="Version:",
        description="What version to use for the model file. Versions below 8207 will not have a JMI file",
        default="8213",
        items=[ ('8197', "8197", "CE/H2/H3"),
                ('8198', "8198", "CE/H2/H3"),
                ('8199', "8199", "CE/H2/H3"),
                ('8200', "8200", "CE/H2/H3"),
                ('8201', "8201", "H2/H3 Non-functional"),
                ('8202', "8202", "H2/H3 Non-functional"),
                ('8203', "8203", "H2/H3 Non-functional"),
                ('8204', "8204", "H2/H3 Non-functional"),
                ('8205', "8205", "H2/H3"),
                ('8206', "8206", "H2/H3 Non-functional"),
                ('8207', "8207", "H2/H3 Non-functional"),
                ('8208', "8208", "H2/H3 Non-functional"),
                ('8209', "8209", "H2/H3"),
                ('8210', "8210", "H2/H3"),
                ('8211', "8211", "H3 Non-functional"),
                ('8212', "8212", "H3 Non-functional"),
                ('8213', "8213", "H3"),
            ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        items=[ ('haloce', "Halo CE", "Export a JMS set intended for Halo Custom Edition or Halo 1 MCC"),
                ('halo2', "Halo 2 MCC", "Export a JMS set intended for Halo 2 Vista or Halo 2 MCC"),
                ('halo3mcc', "Halo 3 MCC", "Export a JMS set intended for Halo 3 MCC"),
            ]
        )

    folder_type: EnumProperty(
        name="Model Type:",
        description="What type to use for the model file",
        default="0",
        items=[ ('0', "Structure", "Asset subdirectory intended for levels"),
                ('1', "Render", "Asset subdirectory intended for models"),
            ]
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

    loop_normals: BoolProperty(
        name ="Use Loop Normals",
        description = "Use loop data for normals instead of vertex. May not match original 3DS Max output at the moment.",
        default = True,
        )

    clean_normalize_weights: BoolProperty(
        name ="Clean and Normalize Weights",
        description = "Remove unused vertex groups and normalize weights before export. Permanently affects scene",
        default = True,
        )

    fix_rotations: BoolProperty(
        name ="Fix Rotations",
        description = "Rotates bones by 90 degrees on a local Z axis",
        default = False,
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

    nonrender_geo: BoolProperty(
        name ="Export non-render geometry",
        description = "Whether or not we ignore geometry that has scene options that hides it from the render output",
        default = True,
        )

    export_render: BoolProperty(
        name ="Export render geometry",
        description = "Whether or not we ignore geometry that is marked as render",
        default = True,
        )

    export_collision: BoolProperty(
        name ="Export collision geometry",
        description = "Whether or not we ignore geometry that is marked as collision",
        default = True,
        )

    export_physics: BoolProperty(
        name ="Export physics geometry",
        description = "Whether or not we ignore geometry that is marked as physics",
        default = True,
        )

    write_textures: BoolProperty(
        name ="Write textures",
        description = "Whether or not we write texture paths for materials",
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
        items=(
            ('0', "Default(JMS)", "Export as is"),
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

    filter_glob: StringProperty(
        default="*.jms;*.jmp",
        options={'HIDDEN'},
        )

    console: BoolProperty(
        name ="Console",
        description = "Is your console running",
        default = False,
        options={'HIDDEN'},
        )

    def execute(self, context):
        from ..file_jmi import export_jmi
        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            parser.add_argument('-arg2', '--game_version', dest='game_version', type=str, default="halo2")
            parser.add_argument('-arg3', '--jmi_version', dest='jmi_version', type=str, default="8210")
            parser.add_argument('-arg4', '--hidden_geo', dest='hidden_geo', action='store_true')
            parser.add_argument('-arg5', '--nonrender_geo', dest='nonrender_geo', action='store_true')
            parser.add_argument('-arg6', '--export_render', dest='export_render', action='store_true')
            parser.add_argument('-arg7', '--export_collision', dest='export_collision', action='store_true')
            parser.add_argument('-arg8', '--export_physics', dest='export_physics', action='store_true')
            parser.add_argument('-arg9', '--write_textures', dest='write_textures', action='store_true')
            parser.add_argument('-arg10', '--apply_modifiers', dest='apply_modifiers', action='store_true')
            parser.add_argument('-arg11', '--triangulate_faces', dest='triangulate_faces', action='store_true')
            parser.add_argument('-arg12', '--loop_normals', dest='loop_normals', action='store_true')
            parser.add_argument('-arg13', '--clean_normalize_weights', dest='clean_normalize_weights', action='store_true')
            parser.add_argument('-arg14', '--fix_rotations', dest='fix_rotations', action='store_true')
            parser.add_argument('-arg15', '--edge_split', dest='edge_split', action='store_true')
            parser.add_argument('-arg16', '--folder_type', dest='folder_type', action='store_true')
            parser.add_argument('-arg17', '--use_edge_angle', dest='use_edge_angle', action='store_true')
            parser.add_argument('-arg18', '--split_angle', dest='split_angle', type=float, default=1.0)
            parser.add_argument('-arg19', '--use_edge_sharp', dest='use_edge_sharp', action='store_true')
            parser.add_argument('-arg20', '--scale_enum', dest='scale_enum', type=str, default="0")
            parser.add_argument('-arg21', '--scale_float', dest='scale_float', type=float, default=1.0)
            parser.add_argument('-arg22', '--console', dest='console', action='store_true', default=True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            print('game_version: ', args.game_version)
            print('jmi_version: ', args.jmi_version)
            print('hidden_geo: ', args.hidden_geo)
            print('nonrender_geo: ', args.nonrender_geo)
            print('export_render: ', args.export_render)
            print('export_collision: ', args.export_collision)
            print('export_physics: ', args.export_physics)
            print('write_textures: ', args.write_textures)
            print('apply_modifiers: ', args.apply_modifiers)
            print('triangulate_faces: ', args.triangulate_faces)
            print('loop_normals: ', args.loop_normals)
            print('clean_normalize_weights: ', args.clean_normalize_weights)
            print('fix_rotations: ', args.fix_rotations)
            print('edge_split: ', args.edge_split)
            print('folder_type: ', args.folder_type)
            print('use_edge_angle: ', args.use_edge_angle)
            print('split_angle: ', args.split_angle)
            print('use_edge_sharp: ', args.use_edge_sharp)
            print('scale_enum: ', args.scale_enum)
            print('scale_float: ', args.scale_float)
            print('console: ', args.console)
            self.filepath = args.filepath
            self.game_version = args.game_version
            self.jmi_version = args.jmi_version
            self.hidden_geo = args.hidden_geo
            self.nonrender_geo = args.nonrender_geo
            self.export_render = args.export_render
            self.export_collision = args.export_collision
            self.export_physics = args.export_physics
            self.write_textures = args.write_textures
            self.apply_modifiers = args.apply_modifiers
            self.triangulate_faces = args.triangulate_faces
            self.loop_normals = args.loop_normals
            self.clean_normalize_weights = args.clean_normalize_weights
            self.fix_rotations = args.fix_rotations
            self.edge_split = args.edge_split
            self.folder_type = args.folder_type
            self.use_edge_angle = args.use_edge_angle
            self.split_angle = args.split_angle
            self.use_edge_sharp = args.use_edge_sharp
            self.scale_enum = args.scale_enum
            self.scale_float = args.scale_float
            self.console = args.console

        return global_functions.run_code("export_jmi.write_file(context, self.filepath, self.report, self.jmi_version, self.jmi_version_ce, self.jmi_version_h2, self.jmi_version_h3, self.apply_modifiers, self.triangulate_faces, self.loop_normals, self.folder_type, self.edge_split, self.use_edge_angle, self.use_edge_sharp, self.split_angle, self.clean_normalize_weights, self.scale_enum, self.scale_float, self.console, self.hidden_geo, self.nonrender_geo, self.export_render, self.export_collision, self.export_physics, self.write_textures, self.game_version, self.fix_rotations)")

    def draw(self, context):
        scene = context.scene
        scene_jmi = scene.jmi
        scene_halo = scene.halo

        layout = self.layout

        is_enabled = True
        if scene_jmi.use_scene_properties:
            is_enabled = False

        if scene_jmi.use_scene_properties:
            self.game_version = scene_jmi.game_version
            self.jmi_version_ce = scene_jmi.jmi_version_ce
            self.jmi_version_h2 = scene_jmi.jmi_version_h2
            self.jmi_version_h3 = scene_jmi.jmi_version_h3
            self.hidden_geo = scene_jmi.hidden_geo
            self.nonrender_geo = scene_jmi.nonrender_geo
            self.export_render = scene_jmi.export_render
            self.export_collision = scene_jmi.export_collision
            self.export_physics = scene_jmi.export_physics
            self.write_textures = scene_jmi.write_textures
            self.apply_modifiers = scene_jmi.apply_modifiers
            self.triangulate_faces = scene_jmi.triangulate_faces
            self.loop_normals = scene_jmi.loop_normals
            self.clean_normalize_weights = scene_jmi.clean_normalize_weights
            self.edge_split = scene_jmi.edge_split
            self.folder_type = scene_jmi.folder_type
            self.use_edge_angle = scene_jmi.use_edge_angle
            self.split_angle = scene_jmi.split_angle
            self.use_edge_sharp = scene_jmi.use_edge_sharp
            self.scale_enum = scene_jmi.scale_enum
            self.scale_float = scene_jmi.scale_float

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
            row.label(text='JMI Version:')
            if self.game_version == 'haloce':
                row.prop(scene_jmi, "jmi_version_ce", text='')

            elif self.game_version == 'halo2mcc':
                row.prop(scene_jmi, "jmi_version_h2", text='')

            elif self.game_version == 'halo3mcc':
                row.prop(scene_jmi, "jmi_version_h3", text='')

        row = col.row()
        row.enabled = is_enabled
        row.label(text='Write Texture Paths:')
        row.prop(self, "write_textures", text='')

        box = layout.box()
        box.label(text="Mask Options:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Export Hidden Geometry:')
        row.prop(self, "hidden_geo", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Export Non-render Geometry:')
        row.prop(self, "nonrender_geo", text='')

        row = col.row()
        row.enabled = is_enabled
        row.label(text='Export Render Geometry:')
        row.prop(self, "export_render", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Export Collision Geometry:')
        row.prop(self, "export_collision", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Export Physics Geometry:')
        row.prop(self, "export_physics", text='')

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
        row.label(text='Use Loop Normals:')
        row.prop(self, "loop_normals", text='')
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
        row.prop(scene_jmi, "use_scene_properties", text='')

        if not self.game_version == 'haloce':
            box = layout.box()
            box.label(text="Subdirectory Type:")
            col = box.column(align=True)
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Model Type:')
            row.prop(self, "folder_type", text='')

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

def menu_func_export(self, context):
    self.layout.operator(ExportJMI.bl_idname, text="Halo Jointed Model Instance (.jmi)")

classeshalo = (
    JMI_FileProps,
    JMI_FilePropertiesGroup,
    JMI_ScenePropertiesGroup,
    JMI_SceneProps,
    ExportJMI,
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.Scene.jmi = PointerProperty(type=JMI_ScenePropertiesGroup, name="JMI Scene Properties", description="Set properties for the JMI exporter")
    bpy.types.Object.jmi = PointerProperty(type=JMI_FilePropertiesGroup, name="JMI File Properties", description="Set properties for world nodes")

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    del bpy.types.Scene.jmi
    del bpy.types.Object.jmi
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
