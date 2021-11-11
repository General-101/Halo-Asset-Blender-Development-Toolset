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
        IntProperty,
        PointerProperty,
        StringProperty
        )

class JMS_RestPositionsADialog(Operator):
    """Set rest positions from a JMS file"""
    bl_idname = "import_scene.jms_rest_a"
    bl_label = "Import JMS"
    filename_ext = '.JMS'

    filter_glob: StringProperty(
        default="*.jms;*.jmp",
        options={'HIDDEN'},
        )

    filepath: StringProperty(
        name="JMS",
        description="Select a path to a JMS containing a skeleton. Will be used for rest position",
        subtype="FILE_PATH"
    )

    def execute(self, context):
        scene = context.scene
        scene_jma = scene.jma
        scene_jma.jms_path_a = self.filepath
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class JMS_RestPositionsBDialog(Operator):
    """Set rest positions from a JMS file"""
    bl_idname = "import_scene.jms_rest_b"
    bl_label = "Import JMS"
    filename_ext = '.JMS'

    filter_glob: StringProperty(
        default="*.jms;*.jmp",
        options={'HIDDEN'},
        )

    filepath: StringProperty(
        name="JMS",
        description="Select a path to a JMS containing a skeleton. Will be used for rest position",
        subtype="FILE_PATH"
    )

    def execute(self, context):
        scene = context.scene
        scene_jma = scene.jma
        scene_jma.jms_path_b = self.filepath
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class JMA_ScenePropertiesGroup(PropertyGroup):
    extension: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        options={'HIDDEN'},
        items=[ ('.JMA', "JMA", "Jointed Model Animation CE/H2/H3"),
                ('.JMM', "JMM", "Jointed Model Moving CE/H2/H3"),
                ('.JMT', "JMT", "Jointed Model Turning CE/H2/H3"),
                ('.JMO', "JMO", "Jointed Model Overlay CE/H2/H3"),
                ('.JMR', "JMR", "Jointed Model Replacement CE/H2/H3"),
                ('.JMRX', "JMRX", "Jointed Model Replacement Extended H2/H3"),
                ('.JMH', "JMH", "Jointed Model Havok H2/H3"),
                ('.JMZ', "JMZ", "Jointed Model Height CE/H2/H3"),
                ('.JMW', "JMW", "Jointed Model World CE/H2/H3"),
            ]
        )

    extension_ce: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        items=[ ('.JMA', "JMA", "Jointed Model Animation CE"),
                ('.JMM', "JMM", "Jointed Model Moving CE"),
                ('.JMT', "JMT", "Jointed Model Turning CE"),
                ('.JMO', "JMO", "Jointed Model Overlay CE"),
                ('.JMR', "JMR", "Jointed Model Replacement CE"),
                ('.JMZ', "JMZ", "Jointed Model Height CE"),
                ('.JMW', "JMW", "Jointed Model World CE"),
            ]
        )

    extension_h2: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        items=[ ('.JMA', "JMA", "Jointed Model Animation H2"),
                ('.JMM', "JMM", "Jointed Model Moving H2"),
                ('.JMT', "JMT", "Jointed Model Turning H2"),
                ('.JMO', "JMO", "Jointed Model Overlay H2"),
                ('.JMR', "JMR", "Jointed Model Replacement H2"),
                ('.JMRX', "JMRX", "Jointed Model Replacement Extended H2"),
                ('.JMH', "JMH", "Jointed Model Havok H2"),
                ('.JMZ', "JMZ", "Jointed Model Height H2"),
                ('.JMW', "JMW", "Jointed Model World H2"),
            ]
        )

    extension_h3: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        items=[ ('.JMA', "JMA", "Jointed Model Animation H3"),
                ('.JMM', "JMM", "Jointed Model Moving H3"),
                ('.JMT', "JMT", "Jointed Model Turning H3"),
                ('.JMO', "JMO", "Jointed Model Overlay H3"),
                ('.JMR', "JMR", "Jointed Model Replacement H3"),
                ('.JMRX', "JMRX", "Jointed Model Replacement Extended H3"),
                ('.JMH', "JMH", "Jointed Model Havok H3"),
                ('.JMZ', "JMZ", "Jointed Model Height H3"),
                ('.JMW', "JMW", "Jointed Model World H3"),
            ]
        )

    jma_version: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16392",
        options={'HIDDEN'},
        items=[ ('16390', "16390", "CE/H2/H3"),
                ('16391', "16391", "CE/H2/H3"),
                ('16392', "16392", "CE/H2/H3"),
                ('16393', "16393", "H2/H3"),
                ('16394', "16394", "H2/H3"),
                ('16395', "16395", "H2/H3"),
            ]
        )

    jma_version_ce: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16392",
        items=[ ('16390', "16390", "CE"),
                ('16391', "16391", "CE"),
                ('16392', "16392", "CE"),
            ]
        )

    jma_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16395",
        items=[ ('16390', "16390", "H2"),
                ('16391', "16391", "H2"),
                ('16392', "16392", "H2"),
                ('16393', "16393", "H2"),
                ('16394', "16394", "H2"),
                ('16395', "16395", "H2"),
            ]
        )

    jma_version_h3: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16395",
        items=[ ('16390', "16390", "H3"),
                ('16391', "16391", "H3"),
                ('16392', "16392", "H3"),
                ('16393', "16393", "H3"),
                ('16394', "16394", "H3"),
                ('16395', "16395", "H3"),
            ]
        )

    generate_checksum: BoolProperty(
        name ="Generate Node Checksum",
        description = "Generates a checksum for the current node skeleton. Defaults to 0 if unchecked",
        default = True,
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        items=[ ('haloce', "Halo CE", "Export an animation intended for Halo Custom Edition or Halo 1 MCC"),
                ('halo2', "Halo 2", "Export an animation intended for Halo 2 Vista or Halo 2 MCC"),
                ('halo3mcc', "Halo 3 MCC", "Export an animation intended for Halo 3 MCC"),
            ]
        )

    custom_frame_rate: EnumProperty(
        name="Framerate:",
        description="Set the framerate this animation will run at",
        default="30",
        items=[ ("23.98", "23.98", ""),
                ("24", "24", ""),
                ("25", "25", ""),
                ("29.97", "29.97", ""),
                ("30", "30", ""),
                ("50", "50", ""),
                ("59.94", "59.94", ""),
                ("60", "60", ""),
                ("CUSTOM", "CUSTOM", ""),
            ]
        )

    frame_rate_float: IntProperty(
        name="Custom Framerate",
        description="Set your own framerate",
        default=30,
        min=1,
        )

    biped_controller: BoolProperty(
        name ="Biped Controller",
        description = "Transform values for armature object",
        default = False,
        options={'HIDDEN'},
        )

    fix_rotations: BoolProperty(
        name ="Fix Rotations",
        description = "Rotates bones by 90 degrees on a local Z axis",
        default = False,
        )

    folder_structure: BoolProperty(
        name ="Generate Asset Subdirectories",
        description = "Generate folder subdirectories for exported assets",
        default = False,
        )

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

    scale_enum: EnumProperty(
        name="Scale",
        description="Choose a preset value to multiply position values by",
        items=( ('0', "Default(JMA)", "Export as is"),
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

    jms_path_a: StringProperty(
        name="Primary JMS",
        description="A path to a JMS containing the primary skeleton. Will be used for rest position",
        )

    jms_path_b: StringProperty(
        name="Secondary JMS",
        description="A path to a JMS containing the secondary skeleton. Will be used for rest position",
        )

class JMA_SceneProps(Panel):
    bl_label = "JMA Scene Properties"
    bl_idname = "JMA_PT_GameVersionPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GameVersionPanel"
    def draw(self, context):
        scene = context.scene
        scene_jma = scene.jma
        scene_halo = scene.halo

        layout = self.layout

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.prop(scene_jma, "game_version", text='')
        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)
        if scene_halo.expert_mode:
            row = col.row()
            row.label(text='JMA Version:')
            if scene_jma.game_version == 'haloce':
                row.prop(scene_jma, "jma_version_ce", text='')

            elif scene_jma.game_version == 'halo2':
                row.prop(scene_jma, "jma_version_h2", text='')

            elif scene_jma.game_version == 'halo3mcc':
                row.prop(scene_jma, "jma_version_h3", text='')

        row = col.row()
        row.label(text='Extension:')
        if scene_jma.game_version == 'haloce':
            row.prop(scene_jma, "extension_ce", text='')

        elif scene_jma.game_version == 'halo2':
            row.prop(scene_jma, "extension_h2", text='')

        elif scene_jma.game_version == 'halo3mcc':
            row.prop(scene_jma, "extension_h3", text='')

        row = col.row()
        row.label(text='Generate Checksum:')
        row.prop(scene_jma, "generate_checksum", text='')
        row = col.row()
        row.label(text='Generate Asset Subdirectories:')
        row.prop(scene_jma, "folder_structure", text='')
        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        if scene_jma.jma_version_h2 == '16395' or scene_jma.jma_version_h3 == '16395':
            if not scene_jma.game_version == 'haloce':
                row = col.row()
                row.label(text='Biped Controller:')
                row.prop(scene_jma, "biped_controller", text='')

        row = col.row()
        row.label(text='Fix Rotation:')
        row.prop(scene_jma, "fix_rotations", text='')
        row = col.row()
        row.label(text='Use As Default Export Settings:')
        row.prop(scene_jma, "use_scene_properties", text='')
        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.prop(scene_jma, "scale_enum", expand=True)
        if scene_jma.scale_enum == '2':
            row = box.row()
            row.prop(scene_jma, "scale_float")

        box = layout.box()
        box.label(text="Import:")
        col = box.column(align=True)
        row = col.row()
        row.operator(JMS_RestPositionsADialog.bl_idname, text="JMS Rest Positions A")
        row.prop(scene_jma, "jms_path_a", text='')
        if ".jms" in scene_jma.jms_path_a.lower():
            row = col.row()
            row.operator(JMS_RestPositionsBDialog.bl_idname, text="JMS Rest Positions B")
            row.prop(scene_jma, "jms_path_b", text='')

class ExportJMA(Operator, ExportHelper):
    """Write a JMA file"""
    bl_idname = "export_jma.export"
    bl_label = "Export Animation"
    filename_ext = ''
    extension: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        options={'HIDDEN'},
        items=[ ('.JMA', "JMA", "Jointed Model Animation CE/H2/H3"),
                ('.JMM', "JMM", "Jointed Model Moving CE/H2/H3"),
                ('.JMT', "JMT", "Jointed Model Turning CE/H2/H3"),
                ('.JMO', "JMO", "Jointed Model Overlay CE/H2/H3"),
                ('.JMR', "JMR", "Jointed Model Replacement CE/H2/H3"),
                ('.JMRX', "JMRX", "Jointed Model Replacement Extended H2/H3"),
                ('.JMH', "JMH", "Jointed Model Havok H2/H3"),
                ('.JMZ', "JMZ", "Jointed Model Height CE/H2/H3"),
                ('.JMW', "JMW", "Jointed Model World CE/H2/H3"),
            ]
        )

    extension_ce: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        items=[ ('.JMA', "JMA", "Jointed Model Animation CE"),
                ('.JMM', "JMM", "Jointed Model Moving CE"),
                ('.JMT', "JMT", "Jointed Model Turning CE"),
                ('.JMO', "JMO", "Jointed Model Overlay CE"),
                ('.JMR', "JMR", "Jointed Model Replacement CE"),
                ('.JMZ', "JMZ", "Jointed Model Height CE"),
                ('.JMW', "JMW", "Jointed Model World CE"),
            ]
        )

    extension_h2: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        items=[ ('.JMA', "JMA", "Jointed Model Animation H2"),
                ('.JMM', "JMM", "Jointed Model Moving H2"),
                ('.JMT', "JMT", "Jointed Model Turning H2"),
                ('.JMO', "JMO", "Jointed Model Overlay H2"),
                ('.JMR', "JMR", "Jointed Model Replacement H2"),
                ('.JMRX', "JMRX", "Jointed Model Replacement Extended H2"),
                ('.JMH', "JMH", "Jointed Model Havok H2"),
                ('.JMZ', "JMZ", "Jointed Model Height H2"),
                ('.JMW', "JMW", "Jointed Model World H2"),
            ]
        )

    extension_h3: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        items=[ ('.JMA', "JMA", "Jointed Model Animation H3"),
                ('.JMM', "JMM", "Jointed Model Moving H3"),
                ('.JMT', "JMT", "Jointed Model Turning H3"),
                ('.JMO', "JMO", "Jointed Model Overlay H3"),
                ('.JMR', "JMR", "Jointed Model Replacement H3"),
                ('.JMRX', "JMRX", "Jointed Model Replacement Extended H3"),
                ('.JMH', "JMH", "Jointed Model Havok H3"),
                ('.JMZ', "JMZ", "Jointed Model Height H3"),
                ('.JMW', "JMW", "Jointed Model World H3"),
            ]
        )

    jma_version: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16392",
        options={'HIDDEN'},
        items=[ ('16390', "16390", "CE/H2/H3"),
                ('16391', "16391", "CE/H2/H3"),
                ('16392', "16392", "CE/H2/H3"),
                ('16393', "16393", "H2/H3"),
                ('16394', "16394", "H2/H3"),
                ('16395', "16395", "H2/H3"),
            ]
        )

    jma_version_ce: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16392",
        items=[ ('16390', "16390", "CE"),
                ('16391', "16391", "CE"),
                ('16392', "16392", "CE"),
            ]
        )

    jma_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16395",
        items=[ ('16390', "16390", "H2"),
                ('16391', "16391", "H2"),
                ('16392', "16392", "H2"),
                ('16393', "16393", "H2"),
                ('16394', "16394", "H2"),
                ('16395', "16395", "H2"),
            ]
        )

    jma_version_h3: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16395",
        items=[ ('16390', "16390", "H3"),
                ('16391', "16391", "H3"),
                ('16392', "16392", "H3"),
                ('16393', "16393", "H3"),
                ('16394', "16394", "H3"),
                ('16395', "16395", "H3"),
            ]
        )

    generate_checksum: BoolProperty(
        name ="Generate Node Checksum",
        description = "Generates a checksum for the current node skeleton. Defaults to 0 if unchecked",
        default = True,
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        items=[ ('haloce', "Halo CE", "Export an animation intended for Halo Custom Edition or Halo 1 MCC"),
                ('halo2', "Halo 2", "Export an animation intended for Halo 2 Vista or Halo 2 MCC"),
                ('halo3mcc', "Halo 3 MCC", "Export an animation intended for Halo 3 MCC"),
            ]
        )

    custom_frame_rate: EnumProperty(
        name="Framerate:",
        description="Set the framerate this animation will run at",
        default="30",
        items=[ ("23.98", "23.98", ""),
                ("24", "24", ""),
                ("25", "25", ""),
                ("29.97", "29.97", ""),
                ("30", "30", ""),
                ("50", "50", ""),
                ("59.94", "59.94", ""),
                ("60", "60", ""),
                ("CUSTOM", "CUSTOM", ""),
            ]
        )

    frame_rate_float: IntProperty(
        name="Custom Framerate",
        description="Set your own framerate",
        default=30,
        min=1,
        )

    biped_controller: BoolProperty(
        name ="Biped Controller",
        description = "Transform values for armature object",
        default = False,
        options={'HIDDEN'},
        )

    fix_rotations: BoolProperty(
        name ="Fix Rotations",
        description = "Rotates bones by 90 degrees on a local Z axis",
        default = False,
        )

    folder_structure: BoolProperty(
        name ="Generate Asset Subdirectories",
        description = "Generate folder subdirectories for exported assets",
        default = False,
        )

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

    scale_enum: EnumProperty(
        name="Scale",
        description="Choose a preset value to multiply position values by",
        items=( ('0', "Default(JMA)", "Export as is"),
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

    jms_path_a: StringProperty(
        name="Primary JMS",
        description="Select a path to a JMS containing the primary skeleton. Will be used for rest position",
        subtype="FILE_PATH"
        )

    jms_path_b: StringProperty(
        name="Secondary JMS",
        description="Select a path to a JMS containing the secondary skeleton. Will be used for rest position",
        subtype="FILE_PATH"
        )

    filter_glob: StringProperty(
        default="*.jma;*.jmm;*.jmt;*.jmo;*.jmr;*.jmrx;*.jmh;*.jmz;*.jmw",
        options={'HIDDEN'},
        )

    console: BoolProperty(
        name ="Console",
        description = "Is your console running",
        default = False,
        options={'HIDDEN'},
        )

    def execute(self, context):
        from ..file_jma import export_jma
        keywords = [context,
                    self.filepath,
                    self.report,
                    self.extension,
                    self.extension_ce,
                    self.extension_h2,
                    self.extension_h3,
                    self.jma_version,
                    self.jma_version_ce,
                    self.jma_version_h2,
                    self.jma_version_h3,
                    self.generate_checksum,
                    self.custom_frame_rate,
                    self.frame_rate_float,
                    self.biped_controller,
                    self.folder_structure,
                    self.scale_enum,
                    self.scale_float,
                    self.console]

        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            parser.add_argument('-arg2', '--game_version', dest='game_version', type=str, default="halo2")
            parser.add_argument('-arg3', '--jma_version', dest='jma_version', type=str, default="16392")
            parser.add_argument('-arg4', '--extension', dest='extension', type=str, default=".JMA")
            parser.add_argument('-arg5', '--generate_checksum', dest='generate_checksum', action='store_true')
            parser.add_argument('-arg6', '--folder_structure', dest='folder_structure', action='store_true')
            parser.add_argument('-arg7', '--biped_controller', dest='biped_controller', action='store_true')
            parser.add_argument('-arg8', '--fix_rotations', dest='fix_rotations', action='store_true')
            parser.add_argument('-arg9', '--custom_frame_rate', dest='custom_frame_rate', type=str, default="30")
            parser.add_argument('-arg10', '--frame_rate_float', dest='frame_rate_float', type=str, default=30)
            parser.add_argument('-arg11', '--scale_enum', dest='scale_enum', type=str, default="0")
            parser.add_argument('-arg12', '--scale_float', dest='scale_float', type=float, default=1.0)
            parser.add_argument('-arg13', '--console', dest='console', action='store_true', default=True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            print('game_version: ', args.game_version)
            print('jma_version: ', args.jma_version)
            print('extension: ', args.extension)
            print('generate_checksum: ', args.generate_checksum)
            print('folder_structure: ', args.folder_structure)
            print('biped_controller: ', args.biped_controller)
            print('fix_rotations: ', args.fix_rotations)
            print('custom_frame_rate: ', args.custom_frame_rate)
            print('frame_rate_float: ', args.frame_rate_float)
            print('scale_enum: ', args.scale_enum)
            print('scale_float: ', args.scale_float)
            print('console: ', args.console)
            self.filepath = args.filepath
            self.game_version = args.game_version
            self.jma_version = args.jma_version
            self.extension = args.extension
            self.generate_checksum = args.generate_checksum
            self.folder_structure = args.folder_structure
            self.biped_controller = args.biped_controller
            self.fix_rotations = args.fix_rotations
            self.custom_frame_rate = args.custom_frame_rate
            self.frame_rate_float = args.frame_rate_float
            self.scale_enum = args.scale_enum
            self.scale_float = args.scale_float
            self.console = args.console

        return export_jma.write_file(*keywords, self.game_version, self.fix_rotations)

    def draw(self, context):
        fps_options = [23.98, 24, 25, 29.97, 30, 50, 59.94, 60]
        scene = context.scene
        scene_jma = scene.jma
        scene_halo = scene.halo

        layout = self.layout
        is_enabled = True
        if scene_jma.use_scene_properties:
            is_enabled = False

        if scene_jma.use_scene_properties:
            self.game_version = scene_jma.game_version
            self.jma_version_ce = scene_jma.jma_version_ce
            self.jma_version_h2 = scene_jma.jma_version_h2
            self.jma_version_h3 = scene_jma.jma_version_h3
            self.extension_ce = scene_jma.extension_ce
            self.extension_h2 = scene_jma.extension_h2
            self.extension_h3 = scene_jma.extension_h3
            self.generate_checksum = scene_jma.generate_checksum
            self.biped_controller = scene_jma.biped_controller
            self.fix_rotations = scene_jma.fix_rotations
            self.folder_structure = scene_jma.folder_structure
            self.scale_enum = scene_jma.scale_enum
            self.scale_float = scene_jma.scale_float
            if scene.render.fps not in fps_options:
                self.custom_frame_rate = 'CUSTOM'
                self.frame_rate_float = scene.render.fps

            else:
                self.custom_frame_rate = '%s' % (scene.render.fps)

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
            row.label(text='JMA Version:')
            if self.game_version == 'haloce':
                 row.prop(self, "jma_version_ce", text='')

            elif self.game_version == 'halo2':
                row.prop(self, "jma_version_h2", text='')

            elif self.game_version == 'halo3mcc':
                row.prop(self, "jma_version_h3", text='')

        row = col.row()
        row.enabled = is_enabled
        row.label(text='Extension:')
        if self.game_version == 'haloce':
            row.prop(self, "extension_ce", text='')

        elif self.game_version == 'halo2':
            row.prop(self, "extension_h2", text='')

        elif self.game_version == 'halo3mcc':
            row.prop(self, "extension_h3", text='')

        row = col.row()
        row.enabled = is_enabled
        row.label(text='Generate Checksum:')
        row.prop(self, "generate_checksum", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Generate Asset Subdirectories:')
        row.prop(self, "folder_structure", text='')
        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        if self.jma_version_h2 == '16395' or self.jma_version_h3 == '16395':
            if not self.game_version == 'haloce':
                row = col.row()
                row.enabled = is_enabled
                row.label(text='Biped Controller:')
                row.prop(self, "biped_controller", text='')

        row = col.row()
        row.enabled = is_enabled
        row.label(text='Fix Rotation:')
        row.prop(self, "fix_rotations", text='')
        row = col.row()
        row.label(text='Use Scene Export Settings:')
        row.prop(scene_jma, "use_scene_properties", text='')
        if scene_halo.expert_mode:
            box = layout.box()
            box.label(text="Custom Frame Rate:")
            row = box.row()
            row.enabled = is_enabled
            row.prop(self, "custom_frame_rate", text='')
            if self.custom_frame_rate == 'CUSTOM':
                row = box.row()
                row.enabled = is_enabled
                row.prop(self, "frame_rate_float")

        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.enabled = is_enabled
        row.prop(self, "scale_enum", expand=True)
        if self.scale_enum == '2':
            row = box.row()
            row.enabled = is_enabled
            row.prop(self, "scale_float")

class ImportJMA(Operator, ImportHelper):
    """Import a JMA file"""
    bl_idname = "import_scene.jma"
    bl_label = "Import JMA"
    filename_ext = '.JMA'

    game_version: EnumProperty(
        name="Game:",
        description="What game was the model file made for",
        default="auto",
        items=[ ('auto', "Auto", "Attempt to guess the game this animation was intended for. Will default to Halo CE if this fails."),
                ('haloce', "Halo CE", "Import an animation intended for Halo Custom Edition or Halo 1 MCC"),
                ('halo2', "Halo 2", "Import an animation intended for Halo 2 Vista or Halo 2 MCC"),
                ('halo3', "Halo 3", "Import an animation intended for Halo 3 MCC"),
            ]
        )

    fix_parents: BoolProperty(
        name ="Force node parents",
        description = "Force thigh bones to use pelvis and clavicles to use spine1. Used to match node import behavior used by Halo 2, Halo 3, and Halo 3 ODST",
        default = True,
        )

    fix_rotations: BoolProperty(
        name ="Fix Rotations",
        description = "Set rotations to match what you would visually see in 3DS Max. Rotates bones by 90 degrees on a local Z axis to match how Blender handles rotations",
        default = False,
        )

    jms_path_a: StringProperty(
        name="Primary JMS",
        description="Select a path to a JMS containing the primary skeleton. Will be used for rest position",
        )

    jms_path_b: StringProperty(
        name="Secondary JMS",
        description="Select a path to a JMS containing the secondary skeleton. Will be used for rest position",
        )

    filter_glob: StringProperty(
        default="*.jma;*.jmm;*.jmt;*.jmo;*.jmr;*.jmrx;*.jmh;*.jmz;*.jmw",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from ..file_jma import import_jma
        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            parser.add_argument('-arg2', '--game_version', dest='game_version', type=str, default="auto")
            parser.add_argument('-arg3', '--fix_parents', dest='fix_parents', action='store_true')
            parser.add_argument('-arg4', '--fix_rotations', dest='fix_rotations', action='store_true')
            parser.add_argument('-arg5', '--jms_path_a', dest='jms_path_a', type=str, default="")
            parser.add_argument('-arg6', '--jms_path_b', dest='jms_path_b', type=str, default="")
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            print('game_version: ', args.game_version)
            print('fix_parents: ', args.fix_parents)
            print('fix_rotations: ', args.fix_rotations)
            print('jms_path_a: ', args.jms_path_a)
            print('jms_path_b: ', args.jms_path_b)
            self.filepath = args.filepath
            self.game_version = args.game_version
            self.fix_parents = args.fix_parents
            self.fix_rotations = args.fix_rotations
            self.jms_path_a = args.jms_path_a
            self.jms_path_b = args.jms_path_b

        return global_functions.run_code("import_jma.load_file(context, self.filepath, self.report, self.fix_parents, self.game_version, self.jms_path_a, self.jms_path_b, self.fix_rotations)")

    def draw(self, context):
        scene = context.scene
        scene_jma = scene.jma
        self.jms_path_a = scene_jma.jms_path_a
        self.jms_path_b = scene_jma.jms_path_b
        layout = self.layout

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.prop(self, "game_version", text='')
        if not self.game_version == 'haloce':
            box = layout.box()
            box.label(text="Import Options:")
            col = box.column(align=True)
            row = col.row()
            row.label(text='Force node parents:')
            row.prop(self, "fix_parents", text='')

        row = col.row()
        row.label(text='Fix Rotations:')
        row.prop(self, "fix_rotations", text='')

        box = layout.box()
        box.label(text="Import:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Primary JMS:')
        row.prop(self, "jms_path_a", text='')
        if ".jms" in self.jms_path_a.lower():
            row = col.row()
            row.label(text='Secondary JMS:')
            row.prop(self, "jms_path_b", text='')

def menu_func_export(self, context):
    self.layout.operator(ExportJMA.bl_idname, text="Halo Jointed Model Animation (.jma)")

def menu_func_import(self, context):
    self.layout.operator(ImportJMA.bl_idname, text="Halo Jointed Model Animation (.jma)")

classeshalo = (
    JMA_ScenePropertiesGroup,
    JMA_SceneProps,
    ImportJMA,
    ExportJMA,
    JMS_RestPositionsADialog,
    JMS_RestPositionsBDialog,
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.Scene.jma = PointerProperty(type=JMA_ScenePropertiesGroup, name="JMA Scene Properties", description="Set properties for the JMA exporter")

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    del bpy.types.Scene.jma
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
