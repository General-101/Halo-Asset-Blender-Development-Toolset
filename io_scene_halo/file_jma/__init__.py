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

def extension_settings_callback(self, context):
    items=[ ('.JMA', "JMA", "Jointed Model Animation CE/H2/H3"),
            ('.JMM', "JMM", "Jointed Model Moving CE/H2/H3"),
            ('.JMT', "JMT", "Jointed Model Turning CE/H2/H3"),
            ('.JMO', "JMO", "Jointed Model Overlay CE/H2/H3"),
            ('.JMR', "JMR", "Jointed Model Replacement CE/H2/H3"),
            ('.JMZ', "JMZ", "Jointed Model Height CE/H2/H3"),
            ('.JMW', "JMW", "Jointed Model World CE/H2/H3"),
        ]

    if not self.game_title == "halo1":
            items.insert(5, ('.JMRX', "JMRX", "Jointed Model Replacement Extended H2/H3"))
            items.insert(6, ('.JMH', "JMH", "Jointed Model Havok H2/H3"))

    return items

def version_settings_callback(self, context):
    items=[ ('16390', "16390", "CE/H2/H3"),
            ('16391', "16391", "CE/H2/H3"),
            ('16392', "16392", "CE/H2/H3"),
        ]

    if not self.game_title == "halo1":
            items.append(('16393', "16393", "H2/H3"))
            items.append(('16394', "16394", "H2/H3"))
            items.append(('16395', "16395", "H2/H3"))

    return items

def update_version(self, context):
    if self.game_title == "halo1":
        self.jma_version = '16392'

    else:
        self.jma_version = '16395'

class JMA_ScenePropertiesGroup(PropertyGroup):
    extension: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        options={'HIDDEN'},
        items=extension_settings_callback
        )

    jma_version: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        options={'HIDDEN'},
        items=version_settings_callback,
        default=2
        )

    game_title: EnumProperty(
        name="Game Title:",
        description="What game will the model file be used for",
        items=[ ('halo1', "Halo 1", "Export an animation intended for Halo 1"),
                ('halo2', "Halo 2", "Export an animation intended for Halo 2"),
                ('halo3', "Halo 3", "Export an animation intended for Halo 3"),
            ],
        update = update_version
        )

    generate_checksum: BoolProperty(
        name ="Generate Node Checksum",
        description = "Generates a checksum for the current node skeleton. Defaults to 0 if unchecked",
        default = True,
        )

    folder_structure: BoolProperty(
        name ="Generate Asset Subdirectories",
        description = "Generate folder subdirectories for exported assets",
        default = False,
        )

    fix_rotations: BoolProperty(
        name ="Fix Rotations",
        description = "Rotates bones by 90 degrees on a local Z axis",
        default = False,
        )

    use_maya_sorting: BoolProperty(
        name ="Use Maya Sorting",
        description = "Certain models have different checksums due to how the Maya bipeds worked. Try this if the checksum doesn't match as is.",
        default = False,
        )


    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
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
    bl_parent_id = "HALO_PT_ScenePropertiesPanel"

    def draw(self, context):
        scene = context.scene
        scene_jma = scene.jma
        scene_halo = scene.halo

        layout = self.layout

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.prop(scene_jma, "game_title", text='')
        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)
        if scene_halo.expert_mode:
            row = col.row()
            row.label(text='JMA Version:')
            row.prop(scene_jma, "jma_version", text='')

        row = col.row()
        row.label(text='Extension:')
        row.prop(scene_jma, "extension", text='')
        row = col.row()
        row.label(text='Generate Checksum:')
        row.prop(scene_jma, "generate_checksum", text='')
        row = col.row()
        row.label(text='Generate Asset Subdirectories:')
        row.prop(scene_jma, "folder_structure", text='')
        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Fix Rotation:')
        row.prop(scene_jma, "fix_rotations", text='')
        row = col.row()
        row.label(text='Use Maya Sorting:')
        row.prop(scene_jma, "use_maya_sorting", text='')
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
        items=extension_settings_callback
        )

    jma_version: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        options={'HIDDEN'},
        items=version_settings_callback,
        default=2
        )

    game_title: EnumProperty(
        name="Game Title:",
        description="What game will the model file be used for",
        items=[ ('halo1', "Halo 1", "Export an animation intended for Halo 1"),
                ('halo2', "Halo 2", "Export an animation intended for Halo 2"),
                ('halo3', "Halo 3", "Export an animation intended for Halo 3"),
            ],
        update = update_version
        )

    generate_checksum: BoolProperty(
        name ="Generate Node Checksum",
        description = "Generates a checksum for the current node skeleton. Defaults to 0 if unchecked",
        default = True,
        )

    folder_structure: BoolProperty(
        name ="Generate Asset Subdirectories",
        description = "Generate folder subdirectories for exported assets",
        default = False,
        )

    fix_rotations: BoolProperty(
        name ="Fix Rotations",
        description = "Rotates bones by 90 degrees on a local Z axis",
        default = False,
        )

    use_maya_sorting: BoolProperty(
        name ="Use Maya Sorting",
        description = "Certain models have different checksums due to how the Maya bipeds worked. Try this if the checksum doesn't match as is.",
        default = False,
        )

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

    frame_rate_enum: EnumProperty(
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

    filter_glob: StringProperty(
        default="*.jma;*.jmm;*.jmt;*.jmo;*.jmr;*.jmrx;*.jmh;*.jmz;*.jmw",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from ..file_jma import export_jma

        scale_value = global_functions.set_scale(self.scale_enum, self.scale_float)
        frame_rate_value = global_functions.set_framerate(self.frame_rate_enum, self.frame_rate_float)
        int_jma_version = int(self.jma_version)

        return global_functions.run_code("export_jma.write_file(context, self.filepath, self.report, self.extension, int_jma_version, self.game_title, self.generate_checksum, self.folder_structure, self.fix_rotations, self.use_maya_sorting, frame_rate_value, scale_value)")

    def draw(self, context):
        scene = context.scene
        scene_jma = scene.jma
        scene_halo = scene.halo

        layout = self.layout
        is_enabled = True
        if scene_jma.use_scene_properties:
            is_enabled = False

        if scene_jma.use_scene_properties:
            self.game_title = scene_jma.game_title
            self.jma_version = scene_jma.jma_version
            self.extension = scene_jma.extension
            self.generate_checksum = scene_jma.generate_checksum
            self.folder_structure = scene_jma.folder_structure
            self.fix_rotations = scene_jma.fix_rotations
            self.use_maya_sorting = scene_jma.use_maya_sorting
            self.scale_enum = scene_jma.scale_enum
            self.scale_float = scene_jma.scale_float
            frame_rate_string = str(scene.render.fps)
            if frame_rate_string not in self.rna_type.properties["frame_rate_enum"].enum_items.keys():
                self.frame_rate_enum = 'CUSTOM'
                self.frame_rate_float = scene.render.fps

            else:
                self.frame_rate_enum = frame_rate_string

        box = layout.box()
        box.label(text="Game Title:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.prop(self, "game_title", text='')
        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)
        if scene_halo.expert_mode:
            row = col.row()
            row.enabled = is_enabled
            row.label(text='JMA Version:')
            row.prop(self, "jma_version", text='')

        row = col.row()
        row.enabled = is_enabled
        row.label(text='Extension:')
        row.prop(self, "extension", text='')
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
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Fix Rotation:')
        row.prop(self, "fix_rotations", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Use Maya Sorting:')
        row.prop(self, "use_maya_sorting", text='')
        row = col.row()
        row.label(text='Use Scene Export Settings:')
        row.prop(scene_jma, "use_scene_properties", text='')
        if scene_halo.expert_mode:
            box = layout.box()
            box.label(text="Custom Frame Rate:")
            row = box.row()
            row.enabled = is_enabled
            row.prop(self, "frame_rate_enum", text='')
            if self.frame_rate_enum == 'CUSTOM':
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

    game_title: EnumProperty(
        name="Game Title:",
        description="What game was the model file made for",
        default="auto",
        items=[ ('auto', "Auto", "Attempt to guess the game this animation was intended for. Will default to Halo CE if this fails."),
                ('halo1', "Halo 1", "Import an animation intended for Halo 1"),
                ('halo2', "Halo 2", "Import an animation intended for Halo 2"),
                ('halo3', "Halo 3", "Import an animation intended for Halo 3"),
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

        return global_functions.run_code("import_jma.load_file(context, self.filepath, self.game_title, self.fix_parents, self.fix_rotations, self.jms_path_a, self.jms_path_b, self.report)")

    def draw(self, context):
        scene = context.scene
        scene_jma = scene.jma
        self.jms_path_a = scene_jma.jms_path_a
        self.jms_path_b = scene_jma.jms_path_b
        layout = self.layout

        box = layout.box()
        box.label(text="Version:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Game Title:')
        row.prop(self, "game_title", text='')
        if self.game_title == "halo1" or self.game_title == 'auto':
            row = col.row()
            row.label(text='Game Version:')
            row.prop(self, "game_version", text='')

        if not self.game_title == "halo1":
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
