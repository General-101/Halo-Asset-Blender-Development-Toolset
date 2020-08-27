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

bl_info = {
    "name": "Halo Jointed Model Exporter",
    "author": "General_101",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Export Halo 2/CE Jointed Model Skeleton File (.jms) and Halo 2/CE Jointed Model Animation File (.jma) with basic support for H2 Jointed Model Skeleton File importing. Originally by Cyboryxmen with changes by Fulsy + MosesofEgypt + con",
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
    if "export_jma" in locals():
        importlib.reload(export_jma)
    if "import_jma" in locals():
        importlib.reload(import_jma)
    if "global_functions" in locals():
        importlib.reload(global_functions)

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
        IntProperty,
        PointerProperty,
        StringProperty,
        )

class JMA_SceneProps(Panel):
    bl_label = "JMA Scene Properties"
    bl_idname = "JMA_PT_GameVersionPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        scene_jma = scene.jma
        layout = self.layout

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)

        row = col.row()
        row.prop(scene_jma, "game_version", text='')

        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)

        if scene_jma.game_version == 'haloce':
            row = col.row()
            row.label(text='Extension:')
            row.prop(scene_jma, "extension_ce", text='')
            row = col.row()
            row.label(text='JMA Version:')
            row.prop(scene_jma, "jma_version_ce", text='')

        elif scene_jma.game_version == 'halo2':
            row = col.row()
            row.label(text='Extension:')
            row.prop(scene_jma, "extension_h2", text='')
            row = col.row()
            row.label(text='JMA Version:')
            row.prop(scene_jma, "jma_version_h2", text='')

        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
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

class JMA_ScenePropertiesGroup(PropertyGroup):
    extension: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        options={'HIDDEN'},
        items=[ ('.JMA', "JMA", "Jointed Model Animation CE/H2"),
                ('.JMM', "JMM", "Jointed Model Moving CE/H2"),
                ('.JMT', "JMT", "Jointed Model Turning CE/H2"),
                ('.JMO', "JMO", "Jointed Model Overlay CE/H2"),
                ('.JMR', "JMR", "Jointed Model Replacement CE/H2"),
                ('.JMRX', "JMRX", "Jointed Model Replacement Extended H2"),
                ('.JMH', "JMH", "Jointed Model Havok H2"),
                ('.JMZ', "JMZ", "Jointed Model Height CE/H2"),
                ('.JMW', "JMW", "Jointed Model World CE/H2"),
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

    jma_version: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16395",
        options={'HIDDEN'},
        items=[ ('16390', "16390", "CE/H2 Non-functional"),
                ('16391', "16391", "CE/H2 Non-functional"),
                ('16392', "16392", "CE/H2"),
                ('16393', "16393", "H2"),
                ('16394', "16394", "H2"),
                ('16395', "16395", "H2"),
               ]
        )

    jma_version_ce: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16392",
        items=[ ('16390', "16390", "CE Non-functional"),
                ('16391', "16391", "CE Non-functional"),
                ('16392', "16392", "CE"),
               ]
        )

    jma_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16395",
        items=[ ('16390', "16390", "H2 Non-functional"),
                ('16391', "16391", "H2 Non-functional"),
                ('16392', "16392", "H2"),
                ('16393', "16393", "H2"),
                ('16394', "16394", "H2"),
                ('16395', "16395", "H2"),
               ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        default="halo2",
        items=[ ('haloce', "Halo CE", "Export an animation intended for Halo CE"),
                ('halo2', "Halo 2", "Export an animation intended for Halo 2"),
               ]
        )

    biped_controller: BoolProperty(
        name ="Biped Controller",
        description = "For Testing",
        default = False,
        options={'HIDDEN'},
        )

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

    scale_enum: EnumProperty(
    name="Scale",
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

class JMS_SceneProps(Panel):
    bl_label = "JMS Scene Properties"
    bl_idname = "JMS_PT_GameVersionPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        scene_jms = scene.jms
        layout = self.layout

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)

        row = col.row()
        row.prop(scene_jms, "game_version", text='')

        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)

        if scene_jms.game_version == 'haloce':
            row = col.row()
            row.label(text='Extension:')
            row.prop(scene_jms, "extension_ce", text='')
            row = col.row()
            row.label(text='JMS Version:')
            row.prop(scene_jms, "jms_version_ce", text='')
            row = col.row()
            row.label(text='Permutation:')
            row.prop(scene_jms, "permutation_ce", text='')
            row = col.row()
            row.label(text='LOD:')
            row.prop(scene_jms, "level_of_detail_ce", text='')

        elif scene_jms.game_version == 'halo2':
            row = col.row()
            row.label(text='Extension:')
            row.prop(scene_jms, "extension_h2", text='')
            row = col.row()
            row.label(text='JMS Version:')
            row.prop(scene_jms, "jms_version_h2", text='')

        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Triangulate:')
        row.prop(scene_jms, "triangulate_faces", text='')
        row = col.row()
        row.label(text='Export Hidden Geometry:')
        row.prop(scene_jms, "hidden_geo", text='')
        if scene_jms.game_version == 'halo2':
            row = col.row()
            row.label(text='Export Render Geometry:')
            row.prop(scene_jms, "export_render", text='')
            row = col.row()
            row.label(text='Export Collision Geometry:')
            row.prop(scene_jms, "export_collision", text='')
            row = col.row()
            row.label(text='Export Physics Geometry:')
            row.prop(scene_jms, "export_physics", text='')

        row = col.row()
        row.label(text='Use As Default Export Settings:')
        row.prop(scene_jms, "use_scene_properties", text='')

        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.prop(scene_jms, "scale_enum", expand=True)

        if scene_jms.scale_enum == '2':
            row = box.row()
            row.prop(scene_jms, "scale_float")

class JMS_ScenePropertiesGroup(PropertyGroup):
    permutation_ce: StringProperty(
        name="Permutation",
        description="Permutation for a JMS file",
        subtype="FILE_NAME"
    )

    level_of_detail_ce: EnumProperty(
        name="LOD:",
        description="What LOD to use for the JMS file",
        items=[ ('0', "NONE", ""),
                ('1', "SuperLow", ""),
                ('2', "Low", ""),
                ('3', "Medium", ""),
                ('4', "High", ""),
                ('5', "SuperHigh", ""),
               ]
        )

    extension: EnumProperty(
        name="Extension:",
        description="What extension to use for the model file",
        options={'HIDDEN'},
        items=[ ('.JMS', "JMS", "Jointed Model Skeleton CE"),
                ('.JMP', "JMP", "Jointed Model Physics CE"),
               ]
        )

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

    jms_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8200",
        options={'HIDDEN'},
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

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

    hidden_geo: BoolProperty(
        name ="Export hidden geometry",
        description = "Whether or not we ignore geometry that is hidden",
        default = True,
        )

    export_render: BoolProperty(
        name ="Export render geometry",
        description = "Export render geometry",
        default = True,
        )

    export_collision: BoolProperty(
        name ="Export collision geometry",
        description = "Export collision geometry",
        default = True,
        )

    export_physics: BoolProperty(
        name ="Export physics geometry",
        description = "Export physics geometry",
        default = True,
        )

    scale_enum: EnumProperty(
    name="Scale",
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
        obj_jms = obj.jms
        scene = context.scene
        scene_jms = scene.jms

        box = layout.box()
        box.label(text="Object Details:")

        col = box.column(align=True)

        if scene_jms.game_version == 'haloce':
            row = col.row()
            row.label(text='Region:')
            row.prop(obj_jms, "Region", text='')

        elif scene_jms.game_version == 'halo2':
            row = col.row()
            row.label(text='Bounding Radius:')
            row.prop(obj_jms, "bounding_radius", text='')
            row = col.row()
            row.label(text='Region:')
            row.prop(obj_jms, "Region", text='')
            row = col.row()
            row.label(text='Permutation:')
            row.prop(obj_jms, "Permutation", text='')
            row = col.row()
            row.label(text='LOD:')
            row.prop(obj_jms, "level_of_detail", text='')
            row = col.row()
            row.label(text='Object Type:')
            row.prop(obj_jms, "Object_Type", text='')
            row = col.row()
            row.label(text='XREF Path:')
            row.prop(obj_jms, "XREF_path", text='')

class JMS_ObjectPropertiesGroup(PropertyGroup):
    bounding_radius: BoolProperty(
        name ="Bounding Radius",
        description = "Sets object as a bounding radius",
        default = False,
        )

    Region : StringProperty(
        name = "Region",
        default = "",
        description = "Set region name"
        )

    Permutation : StringProperty(
        name = "Permutation",
        default = "",
        description = "Set permutation name"
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

    permutation_ce: StringProperty(
        name="Permutation",
        description="Permutation for a JMS file",
        subtype="FILE_NAME"
    )

    level_of_detail_ce: EnumProperty(
        name="LOD:",
        description="What LOD to use for the JMS file",
        items=[ ('0', "NONE", ""),
                ('1', "SuperLow", ""),
                ('2', "Low", ""),
                ('3', "Medium", ""),
                ('4', "High", ""),
                ('5', "SuperHigh", ""),
               ]
        )

    extension: EnumProperty(
        name="Extension:",
        description="What extension to use for the model file",
        options={'HIDDEN'},
        items=[ ('.JMS', "JMS", "Jointed Model Skeleton CE"),
                ('.JMP', "JMP", "Jointed Model Physics CE"),
               ]
        )

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

    jms_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8200",
        options={'HIDDEN'},
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

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

    hidden_geo: BoolProperty(
        name ="Export hidden geometry",
        description = "Whether or not we ignore geometry that has scene options that make exporting it complicated",
        default = True,
        )

    export_render: BoolProperty(
        name ="Export render geometry",
        description = "Export render geometry",
        default = True,
        )

    export_collision: BoolProperty(
        name ="Export collision geometry",
        description = "Export collision geometry",
        default = True,
        )

    export_physics: BoolProperty(
        name ="Export physics geometry",
        description = "Export physics geometry",
        default = True,
        )

    scale_enum: EnumProperty(
    name="Scale",
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
        from .file_jms import export_jms
        keywords = [context,
                    self.filepath,
                    self.report,
                    self.extension,
                    self.extension_ce,
                    self.extension_h2,
                    self.jms_version,
                    self.jms_version_ce,
                    self.jms_version_h2,
                    self.game_version,
                    self.triangulate_faces,
                    self.scale_enum,
                    self.scale_float,
                    self.console,
                    self.permutation_ce,
                    self.level_of_detail_ce,
                    self.hidden_geo,
                    self.export_render,
                    self.export_collision,
                    self.export_physics]

        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            parser.add_argument('-arg2', '--extension', dest='extension', type=str, default=".JMS")
            parser.add_argument('-arg3', '--jms_version', dest='jms_version', type=str, default="8200")
            parser.add_argument('-arg4', '--game_version', dest='game_version', type=str, default="halo2")
            parser.add_argument('-arg5', '--triangulate_faces', dest='triangulate_faces', action='store_true')
            parser.add_argument('-arg6', '--hidden_geo', dest='hidden_geo', action='store_true')
            parser.add_argument('-arg7', '--permutation', dest='permutation_ce', type=str, default="")
            parser.add_argument('-arg8', '--lod', dest='level_of_detail_ce', type=str, default="0")
            parser.add_argument('-arg9', '--scale_enum', dest='scale_enum', type=str, default="0")
            parser.add_argument('-arg10', '--scale_float', dest='scale_float', type=float, default=1.0)
            parser.add_argument('-arg11', '--console', dest='console', action='store_true', default=True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            print('extension: ', args.extension)
            print('jms_version: ', args.jms_version)
            print('game_version: ', args.game_version)
            print('triangulate_faces: ', args.triangulate_faces)
            print('hidden_geo: ', args.hidden_geo)
            print('permutation_ce: ', args.permutation_ce)
            print('level_of_detail_ce: ', args.level_of_detail_ce)
            print('scale_enum: ', args.scale_enum)
            print('scale_float: ', args.scale_float)
            print('console: ', args.console)
            self.filepath = args.filepath
            self.extension = args.extension
            self.jms_version = args.jms_version
            self.game_version = args.game_version
            self.triangulate_faces = args.triangulate_faces
            self.hidden_geo = args.hidden_geo
            self.permutation_ce = args.permutation_ce
            self.level_of_detail_ce = args.level_of_detail_ce
            self.scale_enum = args.scale_enum
            self.scale_float = args.scale_float
            self.console = args.console

        return export_jms.write_file(*keywords)

    def draw(self, context):
        scene = context.scene
        scene_jms = scene.jms
        layout = self.layout
        is_enabled = True
        if scene_jms.use_scene_properties:
            is_enabled = False

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)

        row = col.row()
        row.enabled = is_enabled
        row.prop(self, "game_version", text='')

        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)

        if scene_jms.use_scene_properties:
            self.game_version = scene_jms.game_version
            self.extension_ce = scene_jms.extension_ce
            self.jms_version_ce = scene_jms.jms_version_ce
            self.permutation_ce = scene_jms.permutation_ce
            self.level_of_detail_ce = scene_jms.level_of_detail_ce
            self.extension_h2 = scene_jms.extension_h2
            self.jms_version_h2 = scene_jms.jms_version_h2
            self.triangulate_faces = scene_jms.triangulate_faces
            self.hidden_geo = scene_jms.hidden_geo
            self.export_render = scene_jms.export_render
            self.export_collision = scene_jms.export_collision
            self.export_physics = scene_jms.export_physics
            self.scale_enum = scene_jms.scale_enum
            self.scale_float = scene_jms.scale_float

        if self.game_version == 'haloce':
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Extension:')
            row.prop(self, "extension_ce", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='JMS Version:')
            row.prop(self, "jms_version_ce", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Permutation:')
            row.prop(self, "permutation_ce", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='LOD:')
            row.prop(self, "level_of_detail_ce", text='')

        elif self.game_version == 'halo2':
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Extension:')
            row.prop(self, "extension_h2", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='JMS Version:')
            row.prop(self, "jms_version_h2", text='')

        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Triangulate:')
        row.prop(self, "triangulate_faces", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Export Hidden Geometry:')
        row.prop(self, "hidden_geo", text='')
        if self.game_version == 'halo2':
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

        row = col.row()
        row.label(text='Use Scene Export Settings:')
        row.prop(scene_jms, "use_scene_properties", text='')

        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.enabled = is_enabled
        row.prop(self, "scale_enum", expand=True)

        if self.scale_enum == '2':
            row = box.row()
            row.enabled = is_enabled
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
        from .file_jms import import_jms
        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            self.filepath = args.filepath

        return import_jms.load_file(context, self.filepath, self.report)

class ExportJMA(Operator, ExportHelper):
    """Write a JMA file"""
    bl_idname = "export_jma.export"
    bl_label = "Export Animation"

    filename_ext = ''

    extension: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        options={'HIDDEN'},
        items=[ ('.JMA', "JMA", "Jointed Model Animation CE/H2"),
                ('.JMM', "JMM", "Jointed Model Moving CE/H2"),
                ('.JMT', "JMT", "Jointed Model Turning CE/H2"),
                ('.JMO', "JMO", "Jointed Model Overlay CE/H2"),
                ('.JMR', "JMR", "Jointed Model Replacement CE/H2"),
                ('.JMRX', "JMRX", "Jointed Model Replacement Extended H2"),
                ('.JMH', "JMH", "Jointed Model Havok H2"),
                ('.JMZ', "JMZ", "Jointed Model Height CE/H2"),
                ('.JMW', "JMW", "Jointed Model World CE/H2"),
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

    jma_version: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16395",
        options={'HIDDEN'},
        items=[ ('16390', "16390", "CE/H2 Non-functional"),
                ('16391', "16391", "CE/H2 Non-functional"),
                ('16392', "16392", "CE/H2"),
                ('16393', "16393", "H2"),
                ('16394', "16394", "H2"),
                ('16395', "16395", "H2"),
               ]
        )

    jma_version_ce: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16392",
        items=[ ('16390', "16390", "CE Non-functional"),
                ('16391', "16391", "CE Non-functional"),
                ('16392', "16392", "CE"),
               ]
        )

    jma_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16395",
        items=[ ('16390', "16390", "H2 Non-functional"),
                ('16391', "16391", "H2 Non-functional"),
                ('16392', "16392", "H2"),
                ('16393', "16393", "H2"),
                ('16394', "16394", "H2"),
                ('16395', "16395", "H2"),
               ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        default="halo2",
        items=[ ('haloce', "Halo CE", "Export an animation intended for Halo CE"),
                ('halo2', "Halo 2", "Export an animation intended for Halo 2"),
               ]
        )

    custom_frame_rate: EnumProperty(
        name="Framerate:",
        description="Set the framerate this animation will run at.",
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
        description="Set your own framerate.",
        default=30,
        min=1,
    )

    biped_controller: BoolProperty(
        name ="Biped Controller",
        description = "For Testing",
        default = False,
        options={'HIDDEN'},
        )

    scale_enum: EnumProperty(
    name="Scale",
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
        default="*.jma;*.jmm;*.jmt;*.jmo;*.jmr;*.jmrx;*.jmh;*.jmz;*.jmw",
        options={'HIDDEN'},
        )

    console: BoolProperty(
        name ="Console",
        description = "Is your console running?",
        default = False,
        options={'HIDDEN'},
        )

    def execute(self, context):
        from .file_jma import export_jma
        keywords = [context,
                    self.filepath,
                    self.report,
                    self.extension,
                    self.extension_ce,
                    self.extension_h2,
                    self.jma_version,
                    self.jma_version_ce,
                    self.jma_version_h2,
                    self.game_version,
                    self.custom_frame_rate,
                    self.frame_rate_float,
                    self.biped_controller,
                    self.scale_enum,
                    self.scale_float,
                    self.console]

        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            parser.add_argument('-arg2', '--extension', dest='extension', type=str, default=".JMA")
            parser.add_argument('-arg3', '--jma_version', dest='jma_version', type=str, default="16392")
            parser.add_argument('-arg4', '--game_version', dest='game_version', type=str, default="halo2")
            parser.add_argument('-arg5', '--custom_frame_rate', dest='custom_frame_rate', type=str, default="30")
            parser.add_argument('-arg6', '--frame_rate_float', dest='frame_rate_float', type=str, default=30)
            parser.add_argument('-arg7', '--biped_controller', dest='biped_controller', action='store_true')
            parser.add_argument('-arg8', '--scale_enum', dest='scale_enum', type=str, default="0")
            parser.add_argument('-arg9', '--scale_float', dest='scale_float', type=float, default=1.0)
            parser.add_argument('-arg10', '--console', dest='console', action='store_true', default=True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            print('extension: ', args.extension)
            print('jma_version: ', args.jma_version)
            print('game_version: ', args.game_version)
            print('custom_frame_rate: ', args.custom_frame_rate)
            print('frame_rate_float: ', args.frame_rate_float)
            print('biped_controller: ', args.biped_controller)
            print('scale_enum: ', args.scale_enum)
            print('scale_float: ', args.scale_float)
            print('console: ', args.console)
            self.filepath = args.filepath
            self.extension = args.extension
            self.jma_version = args.jma_version
            self.game_version = args.game_version
            self.custom_frame_rate = args.custom_frame_rate
            self.frame_rate_float = args.frame_rate_float
            self.biped_controller = args.biped_controller
            self.scale_enum = args.scale_enum
            self.scale_float = args.scale_float
            self.console = args.console

        return export_jma.write_file(*keywords)

    def draw(self, context):
        fps_options = [23.98, 24, 25, 29.97, 30, 50, 59.94, 60]
        scene = context.scene
        scene_jma = scene.jma
        layout = self.layout
        is_enabled = True
        if scene_jma.use_scene_properties:
            is_enabled = False

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)

        row = col.row()
        row.enabled = is_enabled
        row.prop(self, "game_version", text='')

        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)

        if scene_jma.use_scene_properties:
            self.game_version = scene_jma.game_version
            self.extension_ce = scene_jma.extension_ce
            self.jma_version_ce = scene_jma.jma_version_ce
            self.extension_h2 = scene_jma.extension_h2
            self.jma_version_h2 = scene_jma.jma_version_h2
            if scene.render.fps not in fps_options:
                self.custom_frame_rate = 'CUSTOM'
                self.frame_rate_float = scene.render.fps

            else:
                self.custom_frame_rate = '%s' % (scene.render.fps)

        if self.game_version == 'haloce':
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Extension:')
            row.prop(self, "extension_ce", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='JMA Version:')
            row.prop(self, "jma_version_ce", text='')

        elif self.game_version == 'halo2':
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Extension:')
            row.prop(self, "extension_h2", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='JMA Version:')
            row.prop(self, "jma_version_h2", text='')

        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Use Scene Export Settings:')
        row.prop(scene_jma, "use_scene_properties", text='')

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

    filter_glob: StringProperty(
        default="*.jma;*.jmm;*.jmt;*.jmo;*.jmr;*.jmrx;*.jmh;*.jmz;*.jmw",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from .file_jma import import_jma
        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            self.filepath = args.filepath

        return import_jma.load_file(context, self.filepath, self.report)

def menu_func_export(self, context):
    self.layout.operator(ExportJMS.bl_idname, text="Halo Jointed Model Skeleton (.jms)")
    self.layout.operator(ExportJMA.bl_idname, text="Halo Jointed Model Animation (.jma)")

def menu_func_import(self, context):
    self.layout.operator(ImportJMS.bl_idname, text="Halo Jointed Model Skeleton (.jms)")
    self.layout.operator(ImportJMA.bl_idname, text="Halo Jointed Model Animation (.jma)")

classeshalo = (
    JMS_ObjectPropertiesGroup,
    JMS_ScenePropertiesGroup,
    JMA_ScenePropertiesGroup,
    JMS_ObjectProps,
    JMS_SceneProps,
    JMA_SceneProps,
    ImportJMS,
    ImportJMA,
    ExportJMS,
    ExportJMA
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.Object.jms = PointerProperty(type=JMS_ObjectPropertiesGroup, name="JMS Object Properties", description="JMS Object properties")
    bpy.types.Scene.jms = PointerProperty(type=JMS_ScenePropertiesGroup, name="JMS Scene Properties", description="JMS Scene properties")
    bpy.types.Scene.jma = PointerProperty(type=JMA_ScenePropertiesGroup, name="JMA Scene Properties", description="JMA Scene properties")

def unregister():
    for clshalo in reversed(classeshalo):
        bpy.utils.unregister_class(clshalo)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    del bpy.types.Object.jms
    del bpy.types.Scene.jms
    del bpy.types.Scene.jma

if __name__ == '__main__':
    register()
