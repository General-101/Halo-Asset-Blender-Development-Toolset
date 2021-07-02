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

class JMI_ScenePropertiesGroup(PropertyGroup):
    jmi_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8210",
        options={'HIDDEN'},
        items=[ ('8207', "8207", "H2/H3 Non-functional"),
                ('8208', "8208", "H2/H3 Non-functional"),
                ('8209', "8209", "H2/H3"),
                ('8210', "8210", "H2/H3"),
                ('8211', "8211", "H3 Non-functional"),
                ('8212', "8212", "H3 Non-functional"),
                ('8213', "8213", "H3"),
               ]
        )

    jmi_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8210",
        items=[ ('8207', "8207", "H2 Non-functional"),
                ('8208', "8208", "H2 Non-functional"),
                ('8209', "8209", "H2"),
                ('8210', "8210", "H2"),
               ]
        )

    jmi_version_h3: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8213",
        items=[ ('8207', "8207", "H3 Non-functional"),
                ('8208', "8208", "H3 Non-functional"),
                ('8209', "8209", "H3"),
                ('8210', "8210", "H3"),
                ('8211', "8211", "H3 Non-functional"),
                ('8212', "8212", "H3 Non-functional"),
                ('8213', "8213", "H3"),
               ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        items=[ ('halo2mcc', "Halo 2 MCC", "Export a JMS set intended for Halo 2 MCC"),
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
    description="Choose a preset value to multiply position values by.",
        items=(
            ('0', "Default(JMS)", "Export as is"),
            ('1', "World Units",  "Multiply position values by 100 units"),
            ('2', "Custom",       "Set your own scale multiplier."),
        )
    )

    scale_float: FloatProperty(
        name="Custom Scale",
        description="Choose a custom value to multiply position values by.",
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
    bl_parent_id = "HALO_PT_GameVersionPanel"
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
        if scene_jmi.game_version == 'halo2mcc':
            if scene_halo.expert_mode:
                box = layout.box()
                box.label(text="File Details:")
                col = box.column(align=True)
                row = col.row()
                row.label(text='JMI Version:')
                row.prop(scene_jmi, "jmi_version_h2", text='')

        elif scene_jmi.game_version == 'halo3mcc':
            if scene_halo.expert_mode:
                box = layout.box()
                box.label(text="File Details:")
                col = box.column(align=True)
                row = col.row()
                row.label(text='JMI Version:')
                row.prop(scene_jmi, "jmi_version_h3", text='')

        box = layout.box()
        box.label(text="Mask Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Export Hidden Geometry:')
        row.prop(scene_jmi, "hidden_geo", text='')
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
        row.label(text='Clean and Normalize Weights:')
        row.prop(scene_jmi, "clean_normalize_weights", text='')
        row = col.row()
        row.label(text='Use Edge Split:')
        row.prop(scene_jmi, "edge_split", text='')
        row = col.row()
        row.label(text='Use As Default Export Settings:')
        row.prop(scene_jmi, "use_scene_properties", text='')

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
        description="What version to use for the model file",
        default="8210",
        options={'HIDDEN'},
        items=[ ('8207', "8207", "H2/H3 Non-functional"),
                ('8208', "8208", "H2/H3 Non-functional"),
                ('8209', "8209", "H2/H3"),
                ('8210', "8210", "H2/H3"),
                ('8211', "8211", "H3 Non-functional"),
                ('8212', "8212", "H3 Non-functional"),
                ('8213', "8213", "H3"),
               ]
        )

    jmi_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8210",
        items=[ ('8207', "8207", "H2 Non-functional"),
                ('8208', "8208", "H2 Non-functional"),
                ('8209', "8209", "H2"),
                ('8210', "8210", "H2"),
               ]
        )

    jmi_version_h3: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8213",
        items=[ ('8207', "8207", "H3 Non-functional"),
                ('8208', "8208", "H3 Non-functional"),
                ('8209', "8209", "H3"),
                ('8210', "8210", "H3"),
                ('8211', "8211", "H3 Non-functional"),
                ('8212', "8212", "H3 Non-functional"),
                ('8213', "8213", "H3"),
               ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        items=[ ('halo2mcc', "Halo 2 MCC", "Export a JMS set intended for Halo 2 MCC"),
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
    description="Choose a preset value to multiply position values by.",
        items=(
            ('0', "Default(JMS)", "Export as is"),
            ('1', "World Units",  "Multiply position values by 100 units"),
            ('2', "Custom",       "Set your own scale multiplier."),
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

    console: BoolProperty(
        name ="Console",
        description = "Is your console running?",
        default = False,
        options={'HIDDEN'},
        )

    def execute(self, context):
        from io_scene_halo.file_jmi import export_jmi
        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            parser.add_argument('-arg2', '--use_scene_properties', dest='use_scene_properties', action='store_true')
            parser.add_argument('-arg3', '--jms_version', dest='jms_version', type=str, default="8200")
            parser.add_argument('-arg4', '--game_version', dest='game_version', type=str, default="halo2mcc")
            parser.add_argument('-arg5', '--folder_type', dest='folder_type', action='store_true')
            parser.add_argument('-arg6', '--apply_modifiers', dest='apply_modifiers', action='store_true')
            parser.add_argument('-arg7', '--triangulate_faces', dest='triangulate_faces', action='store_true')
            parser.add_argument('-arg8', '--clean_normalize_weights', dest='clean_normalize_weights', action='store_true')
            parser.add_argument('-arg9', '--hidden_geo', dest='hidden_geo', action='store_true')
            parser.add_argument('-arg10', '--edge_split', dest='edge_split', action='store_true')
            parser.add_argument('-arg11', '--use_edge_angle', dest='use_edge_angle', action='store_true')
            parser.add_argument('-arg12', '--use_edge_sharp', dest='use_edge_sharp', action='store_true')
            parser.add_argument('-arg13', '--split_angle', dest='split_angle', type=float, default=1.0)
            parser.add_argument('-arg14', '--scale_enum', dest='scale_enum', type=str, default="0")
            parser.add_argument('-arg15', '--scale_float', dest='scale_float', type=float, default=1.0)
            parser.add_argument('-arg16', '--console', dest='console', action='store_true', default=True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            print('use_scene_properties: ', args.use_scene_properties)
            print('jms_version: ', args.jms_version)
            print('game_version: ', args.game_version)
            print('folder_type: ', args.folder_type)
            print('apply_modifiers: ', args.apply_modifiers)
            print('triangulate_faces: ', args.triangulate_faces)
            print('clean_normalize_weights: ', args.clean_normalize_weights)
            print('hidden_geo: ', args.hidden_geo)
            print('edge_split: ', args.edge_split)
            print('use_edge_angle: ', args.use_edge_angle)
            print('use_edge_sharp: ', args.use_edge_sharp)
            print('split_angle: ', args.split_angle)
            print('scale_enum: ', args.scale_enum)
            print('scale_float: ', args.scale_float)
            print('console: ', args.console)
            self.filepath = args.filepath
            self.use_scene_properties = args.use_scene_properties
            self.jms_version = args.jms_version
            self.game_version = args.game_version
            self.folder_type = args.folder_type
            self.apply_modifiers = args.apply_modifiers
            self.triangulate_faces = args.triangulate_faces
            self.clean_normalize_weights = args.clean_normalize_weights
            self.hidden_geo = args.hidden_geo
            self.edge_split = args.edge_split
            self.use_edge_angle = args.use_edge_angle
            self.use_edge_sharp = args.use_edge_sharp
            self.split_angle = args.split_angle
            self.scale_enum = args.scale_enum
            self.scale_float = args.scale_float
            self.console = args.console

        encoding = global_functions.get_encoding(self.game_version)
        game_version = self.game_version
        if self.game_version == 'halo2mcc':
            game_version = 'halo2'

        return global_functions.run_code("export_jmi.write_file(context, self.filepath, self.report, self.jmi_version, self.jmi_version_h2, self.jmi_version_h3, self.apply_modifiers, self.triangulate_faces, self.folder_type, self.edge_split, self.use_edge_angle, self.use_edge_sharp, self.split_angle, self.clean_normalize_weights, self.scale_enum, self.scale_float, self.console, self.hidden_geo, self.export_render, self.export_collision, self.export_physics, game_version, encoding)")

    def draw(self, context):
        scene = context.scene
        scene_jmi = scene.jmi
        scene_halo = scene.halo

        layout = self.layout

        is_enabled = True
        if scene_jmi.use_scene_properties:
            is_enabled = False

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.prop(self, "game_version", text='')
        if scene_jmi.use_scene_properties:
            self.game_version = scene_jmi.game_version
            self.jmi_version_h2 = scene_jmi.jmi_version_h2
            self.jmi_version_h3 = scene_jmi.jmi_version_h3
            self.apply_modifiers = scene_jmi.apply_modifiers
            self.triangulate_faces = scene_jmi.triangulate_faces
            self.clean_normalize_weights = scene_jmi.clean_normalize_weights
            self.hidden_geo = scene_jmi.hidden_geo
            self.export_render = scene_jmi.export_render
            self.export_collision = scene_jmi.export_collision
            self.export_physics = scene_jmi.export_physics
            self.edge_split = scene_jmi.edge_split
            self.folder_type = scene_jmi.folder_type
            self.use_edge_angle = scene_jmi.use_edge_angle
            self.split_angle = scene_jmi.split_angle
            self.use_edge_sharp = scene_jmi.use_edge_sharp
            self.scale_enum = scene_jmi.scale_enum
            self.scale_float = scene_jmi.scale_float

        if self.game_version == 'halo2mcc':
            if scene_halo.expert_mode:
                box = layout.box()
                box.label(text="File Details:")
                col = box.column(align=True)
                row = col.row()
                row.enabled = is_enabled
                row.label(text='JMI Version:')
                row.prop(self, "jmi_version_h2", text='')

        elif self.game_version == 'halo3mcc':
            if scene_halo.expert_mode:
                box = layout.box()
                box.label(text="File Details:")
                col = box.column(align=True)
                row = col.row()
                row.enabled = is_enabled
                row.label(text='JMI Version:')
                row.prop(self, "jmi_version_h3", text='')

        box = layout.box()
        box.label(text="Mask Options:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Export Hidden Geometry:')
        row.prop(self, "hidden_geo", text='')
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
        row.label(text='Clean and Normalize Weights:')
        row.prop(self, "clean_normalize_weights", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Use Edge Split:')
        row.prop(self, "edge_split", text='')
        row = col.row()
        row.label(text='Use Scene Export Settings:')
        row.prop(scene_jmi, "use_scene_properties", text='')

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
    JMI_ScenePropertiesGroup,
    JMI_SceneProps,
    ExportJMI,
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.Scene.jmi = PointerProperty(type=JMI_ScenePropertiesGroup, name="JMI Scene Properties", description="Set properties for the JMI exporter")

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    del bpy.types.Scene.jmi
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
