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
        self.jmi_version = '8200'

    elif self.game_title == "halo2":
        self.jmi_version = '8210'

    else:
        self.jmi_version = '8213'

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
        if hasattr(obj, 'jmi') and obj.name[0:1].lower() == '!' and scene_halo.game_title == "halo1":
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
        box.label(text="Game Title:")
        col = box.column(align=True)
        row = col.row()
        row.prop(scene_jmi, "game_title", text='')
        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)
        if scene_halo.expert_mode:
            row = col.row()
            row.label(text='JMI Version:')
            row.prop(scene_jmi, "jmi_version", text='')

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
        row.label(text='Fix Rotations:')
        row.prop(scene_jmi, "fix_rotations", text='')
        row = col.row()
        row.label(text='Use Maya Sorting:')
        row.prop(scene_jmi, "use_maya_sorting", text='')
        row = col.row()
        row.label(text='Use As Default Export Settings:')
        row.prop(scene_jmi, "use_scene_properties", text='')

        if not scene_jmi.game_title == "halo1":
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
        options={'HIDDEN'},
        items=version_settings_callback,
        update = version_settings_callback,
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
        description = "Use loop data for normals instead of vertex. May not match original 3DS Max output.",
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

    def execute(self, context):
        from ..file_jmi import export_jmi

        jmi_version = int(self.jmi_version)
        folder_type = bool(int(self.folder_type))
        scale_value = global_functions.set_scale(self.scale_enum, self.scale_float)
        edge_split = global_functions.EdgeSplit(self.edge_split, self.use_edge_angle, self.split_angle, self.use_edge_sharp)

        return global_functions.run_code("export_jmi.write_file(context, self.filepath, self.report, jmi_version, self.apply_modifiers, self.triangulate_faces, self.loop_normals, folder_type, edge_split, self.clean_normalize_weights, scale_value, self.hidden_geo, self.nonrender_geo, self.export_render, self.export_collision, self.export_physics, self.write_textures, self.game_title, self.fix_rotations, self.use_maya_sorting)")

    def draw(self, context):
        scene = context.scene
        scene_jmi = scene.jmi
        scene_halo = scene.halo

        layout = self.layout

        is_enabled = True
        if scene_jmi.use_scene_properties:
            is_enabled = False

        if scene_jmi.use_scene_properties:
            self.game_title = scene_jmi.game_title
            self.jmi_version = scene_jmi.jmi_version
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
            self.fix_rotations = scene_jmi.fix_rotations
            self.use_maya_sorting = scene_jmi.use_maya_sorting
            self.folder_type = scene_jmi.folder_type
            self.use_edge_angle = scene_jmi.use_edge_angle
            self.split_angle = scene_jmi.split_angle
            self.use_edge_sharp = scene_jmi.use_edge_sharp
            self.scale_enum = scene_jmi.scale_enum
            self.scale_float = scene_jmi.scale_float

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
            row.label(text='JMI Version:')
            row.prop(self, "jmi_version", text='')

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
        row.prop(scene_jmi, "use_scene_properties", text='')

        if not self.game_title == "halo1":
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
