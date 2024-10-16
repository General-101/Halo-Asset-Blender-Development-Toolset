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

import os
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
        PointerProperty,
        StringProperty,
        CollectionProperty
        )

class JMS_PhysicsPropertiesGroup(PropertyGroup):
    jms_spring_type: EnumProperty(
        name="Spring Type",
        description="Choose spring type. This option does nothing in your Blender physics simulation",
        items=( ('0', "Standard", "Standard spring"),
                ('1', "Limited",  "Limited spring"),
                ('2', "Stiff",    "Stiff spring"),
            )
        )

class JMS_PhysicsProps(Panel):
    bl_label = "Halo Physics Properties"
    bl_idname = "JMS_PT_PhysicsPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "physics"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "PHYSICS_PT_rigid_body_constraint"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        rbc = ob.rigid_body_constraint

        scene = context.scene
        scene_halo = scene.halo

        if not scene_halo.game_title == "halo1":
            return (ob and rbc and (rbc.type in {'GENERIC_SPRING'})
                    and context.engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        scene_halo = scene.halo

        ob = context.object
        obj_jms = ob.jms

        if not scene_halo.game_title == "halo1":
            box = layout.box()
            box.label(text="Spring Type:")
            col = box.column(align=True)
            row = col.row()
            row.prop(obj_jms, "jms_spring_type", text='')

class JMS_SceneProps(Panel):
    bl_label = "JMS Scene Properties"
    bl_idname = "JMS_PT_GameVersionPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_ScenePropertiesPanel"
    def draw(self, context):
        scene = context.scene
        scene_jms = scene.jms
        scene_halo = scene.halo

        layout = self.layout

        box = layout.box()
        box.label(text="Game Title:")
        col = box.column(align=True)
        row = col.row()
        row.prop(scene_jms, "game_title", text='')
        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)
        if scene_halo.expert_mode:
            row = col.row()
            row.label(text='JMS Version:')
            row.prop(scene_jms, "jms_version", text='')

        if scene_jms.game_title == "halo1":
            row = col.row()
            row.label(text='Permutation:')
            row.prop(scene_jms, "permutation_ce", text='')
            row = col.row()
            row.label(text='LOD:')
            row.prop(scene_jms, "level_of_detail_ce", text='')
            row = col.row()
            row.label(text='Generate Checksum:')
            row.prop(scene_jms, "generate_checksum", text='')

        row = col.row()
        row.label(text='Generate Asset Subdirectories:')
        row.prop(scene_jms, "folder_structure", text='')
        row = col.row()
        row.label(text='Write Texture Paths:')
        row.prop(scene_jms, "write_textures", text='')

        box = layout.box()
        box.label(text="Mask Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Export Hidden Geometry:')
        row.prop(scene_jms, "hidden_geo", text='')
        row = col.row()
        row.label(text='Export Non-render Geometry:')
        row.prop(scene_jms, "nonrender_geo", text='')
        row = col.row()
        row.label(text='Export Render Geometry:')
        row.prop(scene_jms, "export_render", text='')
        row = col.row()
        row.label(text='Export Collision Geometry:')
        row.prop(scene_jms, "export_collision", text='')
        row = col.row()
        row.label(text='Export Physics Geometry:')
        row.prop(scene_jms, "export_physics", text='')
        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Apply Modifiers:')
        row.prop(scene_jms, "apply_modifiers", text='')
        row = col.row()
        row.label(text='Triangulate:')
        row.prop(scene_jms, "triangulate_faces", text='')
        row = col.row()
        row.label(text='Use Loop Normals:')
        row.prop(scene_jms, "loop_normals", text='')
        row = col.row()
        row.label(text='Clean and Normalize Weights:')
        row.prop(scene_jms, "clean_normalize_weights", text='')
        row = col.row()
        row.label(text='Use Edge Split:')
        row.prop(scene_jms, "edge_split", text='')
        row = col.row()
        row.label(text='Fix Rotations:')
        row.prop(scene_jms, "fix_rotations", text='')
        row = col.row()
        row.label(text='Use Maya Sorting:')
        row.prop(scene_jms, "use_maya_sorting", text='')
        row = col.row()
        row.label(text='Use As Default Export Settings:')
        row.prop(scene_jms, "use_scene_properties", text='')
        if scene_jms.folder_structure == True and not scene_jms.game_title == "halo1":
            box = layout.box()
            box.label(text="Subdirectory Type:")
            col = box.column(align=True)
            row = col.row()
            row.label(text='Model Type:')
            row.prop(scene_jms, "folder_type", text='')

        if scene_jms.edge_split == True:
            box = layout.box()
            box.label(text="Edge Split:")
            col = box.column(align=True)
            row = col.row()
            row.label(text='Edge Angle:')
            row.prop(scene_jms, "use_edge_angle", text='')
            row.active = scene_jms.use_edge_angle
            row.prop(scene_jms, "split_angle", text='')
            row = col.row()
            row.label(text='Sharp Edges:')
            row.prop(scene_jms, "use_edge_sharp", text='')

        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.prop(scene_jms, "scale_enum", expand=True)
        if scene_jms.scale_enum == '2':
            row = box.row()
            row.prop(scene_jms, "scale_float")

def version_settings_callback(self, context):
    items=[ ('8197', "8197", "CE/H2/H3"),
            ('8198', "8198", "CE/H2/H3"),
            ('8199', "8199", "CE/H2/H3"),
            ('8200', "8200", "CE/H2/H3"),
        ]

    if self.game_title == "halo2":
            items.append(('8201', "8201", "H2/H3 Non-functional"))
            items.append(('8202', "8202", "H2/H3 Non-functional"))
            items.append(('8203', "8203", "H2/H3 Non-functional"))
            items.append(('8204', "8204", "H2/H3 Non-functional"))
            items.append(('8205', "8205", "H2/H3"))
            items.append(('8206', "8206", "H2/H3 Non-functional"))
            items.append(('8207', "8207", "H2/H3 Non-functional"))
            items.append(('8208', "8208", "H2/H3 Non-functional"))
            items.append(('8209', "8209", "H2/H3"))
            items.append(('8210', "8210", "H2/H3"))

    elif self.game_title == "halo3":
            items.append(('8201', "8201", "H2/H3 Non-functional"))
            items.append(('8202', "8202", "H2/H3 Non-functional"))
            items.append(('8203', "8203", "H2/H3 Non-functional"))
            items.append(('8204', "8204", "H2/H3 Non-functional"))
            items.append(('8205', "8205", "H2/H3"))
            items.append(('8206', "8206", "H2/H3 Non-functional"))
            items.append(('8207', "8207", "H2/H3 Non-functional"))
            items.append(('8208', "8208", "H2/H3 Non-functional"))
            items.append(('8209', "8209", "H2/H3"))
            items.append(('8210', "8210", "H2/H3"))
            items.append(('8211', "8211", "H3 Non-functional"))
            items.append(('8212', "8212", "H3 Non-functional"))
            items.append(('8213', "8213", "H3"))

    return items

def update_version(self, context):
    if self.game_title == "halo1":
        self.jms_version = '8200'

    elif self.game_title == "halo2":
        self.jms_version = '8210'

    else:
        self.jms_version = '8213'

class JMS_ScenePropertiesGroup(PropertyGroup):
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

    jms_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        options={'HIDDEN'},
        items=version_settings_callback,
        default=3
        )

    game_title: EnumProperty(
        name="Game Title:",
        description="What game will the model file be used for",
        items=[ ('halo1', "Halo 1", "Export a JMS intended for Halo 1"),
                ('halo2', "Halo 2", "Export a JMS intended for Halo 2"),
                ('halo3', "Halo 3", "Export a JMS intended for Halo 3"),
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

    folder_type: EnumProperty(
        name="Model Type:",
        description="What type to use for the model file",
        default="0",
        items=[ ('0', "Render", "Asset subdirectory intended for models"),
                ('1', "Structure", "Asset subdirectory intended for levels"),
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
        description = "Apply an edge split modifier",
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
                ('1', "Super Low", ""),
                ('2', "Low", ""),
                ('3', "Medium", ""),
                ('4', "High", ""),
                ('5', "Super High", ""),
            ]
        )

    jms_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        options={'HIDDEN'},
        items=version_settings_callback,
        default=3
        )

    game_title: EnumProperty(
        name="Game Title:",
        description="What game will the model file be used for",
        items=[ ('halo1', "Halo 1", "Export a JMS intended for Halo 1"),
                ('halo2', "Halo 2", "Export a JMS intended for Halo 2"),
                ('halo3', "Halo 3", "Export a JMS intended for Halo 3"),
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

    folder_type: EnumProperty(
        name="Model Type:",
        description="What type to use for the model file",
        default="0",
        items=[ ('0', "Render", "Asset subdirectory intended for models"),
                ('1', "Structure", "Asset subdirectory intended for levels"),
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
        description = "Use loop data for normals instead of vertex. May not match original 3DS Max output",
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
        description = "Apply an edge split modifier",
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

    filter_glob: StringProperty(
        default="*.jms;*.jmp",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from . import export_jms

        jms_version = int(self.jms_version)
        folder_type = bool(int(self.folder_type))
        scale_value = global_functions.set_scale(self.scale_enum, self.scale_float)
        edge_split = global_functions.EdgeSplit(self.edge_split, self.use_edge_angle, self.split_angle, self.use_edge_sharp)

        return global_functions.run_code("export_jms.write_file(context, self.filepath, self.game_title, jms_version, self.permutation_ce, self.level_of_detail_ce, self.generate_checksum, self.folder_structure, self.write_textures, self.hidden_geo, self.nonrender_geo, self.export_render, self.export_collision, self.export_physics, self.apply_modifiers, self.triangulate_faces, self.loop_normals, self.clean_normalize_weights, edge_split, self.fix_rotations, self.use_maya_sorting, folder_type, scale_value, self.report)")

    def draw(self, context):
        scene = context.scene
        scene_jms = scene.jms
        scene_halo = scene.halo

        layout = self.layout

        is_enabled = True
        if scene_jms.use_scene_properties:
            is_enabled = False

        if scene_jms.use_scene_properties:
            self.game_title = scene_jms.game_title
            self.jms_version = scene_jms.jms_version
            self.permutation_ce = scene_jms.permutation_ce
            self.level_of_detail_ce = scene_jms.level_of_detail_ce
            self.generate_checksum = scene_jms.generate_checksum
            self.folder_structure = scene_jms.folder_structure
            self.hidden_geo = scene_jms.hidden_geo
            self.nonrender_geo = scene_jms.nonrender_geo
            self.export_render = scene_jms.export_render
            self.export_collision = scene_jms.export_collision
            self.export_physics = scene_jms.export_physics
            self.write_textures = scene_jms.write_textures
            self.apply_modifiers = scene_jms.apply_modifiers
            self.triangulate_faces = scene_jms.triangulate_faces
            self.loop_normals = scene_jms.loop_normals
            self.clean_normalize_weights = scene_jms.clean_normalize_weights
            self.edge_split = scene_jms.edge_split
            self.fix_rotations = scene_jms.fix_rotations
            self.use_maya_sorting = scene_jms.use_maya_sorting
            self.folder_type = scene_jms.folder_type
            self.use_edge_angle = scene_jms.use_edge_angle
            self.split_angle = scene_jms.split_angle
            self.use_edge_sharp = scene_jms.use_edge_sharp
            self.scale_enum = scene_jms.scale_enum
            self.scale_float = scene_jms.scale_float

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
            row.label(text='JMS Version:')
            row.prop(self, "jms_version", text='')

        if self.game_title == "halo1":
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Permutation:')
            row.prop(self, "permutation_ce", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='LOD:')
            row.prop(self, "level_of_detail_ce", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Generate Checksum:')
            row.prop(self, "generate_checksum", text='')

        row = col.row()
        row.enabled = is_enabled
        row.label(text='Generate Asset Subdirectories:')
        row.prop(self, "folder_structure", text='')
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
        row.enabled = is_enabled
        row.label(text='Fix Rotation:')
        row.prop(self, "fix_rotations", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Use Maya Sorting:')
        row.prop(self, "use_maya_sorting", text='')
        row = col.row()
        row.label(text='Use Scene Export Settings:')
        row.prop(scene_jms, "use_scene_properties", text='')
        if self.folder_structure == True and not self.game_title == "halo1":
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

if (4, 1, 0) <= bpy.app.version:
    from bpy.types import (
        FileHandler,
        OperatorFileListElement
        )

class ImportJMS(Operator, ImportHelper):
    """Import a JMS file"""
    bl_idname = "import_scene.jms"
    bl_label = "Import JMS"
    filename_ext = '.JMS'
    game_title: EnumProperty(
        name="Game Title:",
        description="What game was the model file made for",
        default="auto",
        items=[ ('auto', "Auto", "Attempt to guess the game this JMS was intended for. Will default to Halo CE if this fails"),
                ('halo1', "Halo 1", "Import a JMS intended for Halo Custom Edition or Halo 1 MCC"),
                ('halo2', "Halo 2", "Import a JMS intended for Halo 2 Vista or Halo 2 MCC"),
                ('halo3', "Halo 3", "Import a JMS intended for Halo 3 MCC"),
            ]
        )

    reuse_armature: BoolProperty(
        name ="Reuse Armature",
        description = "Reuse a preexisting armature in the scene if it matches what is in the JMS file",
        default = True,
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

    empty_markers: BoolProperty(
        name ="Generate Empty Markers",
        description = "Generate empty markers instead of UV spheres",
        default = True,
        )

    filter_glob: StringProperty(
        default="*.jms;*.jmp",
        options={'HIDDEN'},
        )

    if (4, 1, 0) <= bpy.app.version:
        directory: StringProperty(
            subtype='FILE_PATH', 
            options={'SKIP_SAVE', 'HIDDEN'}
            )

        files: CollectionProperty(
            type=OperatorFileListElement, 
            options={'SKIP_SAVE', 'HIDDEN'}
            )

    def __init__(self):
        scene = bpy.context.scene
        scene_jms = scene.jms
        self.jma_path = scene_jms.jma_path

    def execute(self, context):
        if (4, 1, 0) <= bpy.app.version:
            if not self.directory:
                return {'CANCELLED'}
            
            for file in self.files:
                if file.name.lower().endswith(".jms"):
                    filepath = os.path.join(self.directory, file.name)
                    self.run_jms_code(filepath, context)

        else:
            self.run_jms_code(self.filepath, context)

        return {'FINISHED'}
    
    def run_jms_code(self, filepath, context):
        from . import import_jms
        global_functions.run_code("import_jms.load_file(context, filepath, self.game_title, self.reuse_armature, self.fix_parents, self.fix_rotations, self.empty_markers, self.report)")

    if (4, 1, 0) <= bpy.app.version:
        def invoke(self, context, event):
            if (4, 2, 0) <= bpy.app.version:
                return self.invoke_popup(context)
            else:
                if self.directory:
                    return self.execute(context)
                context.window_manager.fileselect_add(self)
                return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Version:")
        col = box.column(align=True)
        row = col.row()
        box.label(text="Game Version:")
        row.prop(self, "game_title", text='')
        box = layout.box()
        box.label(text="Import Options:")
        col = box.column(align=True)

        row = col.row()
        row.label(text='Reuse Armature:')
        row.prop(self, "reuse_armature", text='')
        if self.game_title == 'auto' or self.game_title == "halo2" or self.game_title == "halo3":
            row = col.row()
            row.label(text='Force node parents:')
            row.prop(self, "fix_parents", text='')

        row = col.row()
        row.label(text='Fix Rotations:')
        row.prop(self, "fix_rotations", text='')
        row = col.row()
        row.label(text='Use Empties For Markers:')
        row.prop(self, "empty_markers", text='')

if (4, 1, 0) <= bpy.app.version:
    class ImportJMS_FileHandler(FileHandler):
        bl_idname = "JMS_FH_import"
        bl_label = "File handler for JMS import"
        bl_import_operator = "import_scene.jms"
        bl_file_extensions = ".JMS"

        @classmethod
        def poll_drop(cls, context):
            return (context.area and context.area.type == 'VIEW_3D')

def menu_func_export(self, context):
    self.layout.operator(ExportJMS.bl_idname, text="Halo Jointed Model Skeleton (.jms)")

def menu_func_import(self, context):
    self.layout.operator(ImportJMS.bl_idname, text="Halo Jointed Model Skeleton (.jms)")

classeshalo = [
    JMS_ScenePropertiesGroup,
    JMS_SceneProps,
    JMS_PhysicsPropertiesGroup,
    JMS_PhysicsProps,
    ImportJMS,
    ExportJMS
]

if (4, 1, 0) <= bpy.app.version:
    classeshalo.append(ImportJMS_FileHandler)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.Scene.jms = PointerProperty(type=JMS_ScenePropertiesGroup, name="JMS Scene Properties", description="Set properties for the JMS exporter")
    bpy.types.Object.jms = PointerProperty(type=JMS_PhysicsPropertiesGroup, name="JMS Physics Properties", description="Set properties for your constraints")

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    del bpy.types.Scene.jms
    del bpy.types.Object.jms
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
