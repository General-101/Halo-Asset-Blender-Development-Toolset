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
    PointerProperty,
    StringProperty
    )

def version_settings_callback(self, context):
    items=[ ('1', "1", "H2/H3"),
            ('2', "2", "H2/H3"),
        ]

    if not self.game_title == "halo2":
        items.append(('3', "3", "H3 Non-functional"))
        items.append(('4', "4", "H3 Non-functional"))
        items.append(('5', "5", "H3 Non-functional"))
        items.append(('6', "6", "H3 Non-functional"))
        items.append(('7', "7", "H3"))

    return items

def update_version(self, context):
    if self.game_title == "halo2":
        self.ass_version = '2'

    else:
        self.ass_version = '7'

class ASS_ScenePropertiesGroup(PropertyGroup):
    ass_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        items=version_settings_callback,
        default=1
        )

    game_title: EnumProperty(
        name="Game Title:",
        description="What game will the model file be used for",
        items=[ ('halo2', "Halo 2", "Export a level intended for Halo 2"),
                ('halo3', "Halo 3", "Export a level intended for Halo 3"),
            ],
        update = update_version
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

class ASS_SceneProps(Panel):
    bl_label = "ASS Scene Properties"
    bl_idname = "ASS_PT_GameVersionPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_ScenePropertiesPanel"
    def draw(self, context):
        scene = context.scene
        scene_ass = scene.ass
        scene_halo = scene.halo

        layout = self.layout

        box = layout.box()
        box.label(text="Game Title:")
        col = box.column(align=True)
        row = col.row()
        row.prop(scene_ass, "game_title", text='')
        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)
        if scene_halo.expert_mode:
            row = col.row()
            row.label(text='ASS Version:')
            row.prop(scene_ass, "ass_version", text='')

        row = col.row()
        row.label(text='Generate Asset Subdirectories:')
        row.prop(scene_ass, "folder_structure", text='')

        box = layout.box()
        box.label(text="Mask Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Export Hidden Geometry:')
        row.prop(scene_ass, "hidden_geo", text='')
        row = col.row()
        row.label(text='Export Non-render Geometry:')
        row.prop(scene_ass, "nonrender_geo", text='')

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
        row.label(text='Use Loop Normals:')
        row.prop(scene_ass, "loop_normals", text='')
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
        items=version_settings_callback,
        default=1
        )

    game_title: EnumProperty(
        name="Game Title:",
        description="What game will the model file be used for",
        items=[ ('halo2', "Halo 2", "Export a level intended for Halo 2"),
                ('halo3', "Halo 3", "Export a level intended for Halo 3"),
            ],
        update = update_version
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

    filter_glob: StringProperty(
        default="*.ass",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from ..file_ass import export_ass

        scale_value = global_functions.set_scale(self.scale_enum, self.scale_float)
        edge_split = global_functions.EdgeSplit(self.edge_split, self.use_edge_angle, self.split_angle, self.use_edge_sharp)
        int_ass_version = int(self.ass_version)

        return global_functions.run_code("export_ass.write_file(context, self.filepath, int_ass_version, self.game_title, self.folder_structure, self.hidden_geo, self.nonrender_geo, self.apply_modifiers, self.triangulate_faces, self.loop_normals, edge_split, self.clean_normalize_weights, scale_value, self.report)")

    def draw(self, context):
        scene = context.scene
        scene_ass = scene.ass
        scene_halo = scene.halo

        layout = self.layout
        is_enabled = True
        if scene_ass.use_scene_properties:
            is_enabled = False

        if scene_ass.use_scene_properties:
            self.game_title = scene_ass.game_title
            self.ass_version = scene_ass.ass_version
            self.folder_structure = scene_ass.folder_structure
            self.hidden_geo = scene_ass.hidden_geo
            self.nonrender_geo = scene_ass.nonrender_geo
            self.apply_modifiers = scene_ass.apply_modifiers
            self.triangulate_faces = scene_ass.triangulate_faces
            self.loop_normals = scene_ass.loop_normals
            self.clean_normalize_weights = scene_ass.clean_normalize_weights
            self.edge_split = scene_ass.edge_split
            self.use_edge_angle = scene_ass.use_edge_angle
            self.split_angle = scene_ass.split_angle
            self.use_edge_sharp = scene_ass.use_edge_sharp
            self.scale_enum = scene_ass.scale_enum
            self.scale_float = scene_ass.scale_float

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
            row.label(text='ASS Version:')
            row.prop(self, "ass_version", text='')

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
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Export Non-render Geometry:')
        row.prop(self, "nonrender_geo", text='')

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

try:
    from bpy.types import FileHandler

    class ImportASS(Operator, ImportHelper):
        """Import an ASS file"""
        bl_idname = "import_scene.ass"
        bl_label = "Import ASS"
        filename_ext = '.ASS'

        filter_glob: StringProperty(
            default="*.ass",
            options={'HIDDEN'},
            )

        filepath: StringProperty(
            subtype='FILE_PATH', 
            options={'SKIP_SAVE'}
            )

        def execute(self, context):
            from ..file_ass import import_ass

            return global_functions.run_code("import_ass.load_file(context, self.filepath, self.report)")

        def invoke(self, context, event):
            if self.filepath:
                return self.execute(context)
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}

    class ImportASS_FileHandler(FileHandler):
        bl_idname = "ASS_FH_import"
        bl_label = "File handler for ASS import"
        bl_import_operator = "import_scene.ass"
        bl_file_extensions = ".ASS"

        @classmethod
        def poll_drop(cls, context):
            return (context.area and context.area.type == 'VIEW_3D')

except ImportError:
    print("Blender is out of date. Drag and drop will not function")
    FileHandler = None
    class ImportASS(Operator, ImportHelper):
        """Import an ASS file"""
        bl_idname = "import_scene.ass"
        bl_label = "Import ASS"
        filename_ext = '.ASS'

        filter_glob: StringProperty(
            default="*.ass",
            options={'HIDDEN'},
            )

        filepath: StringProperty(
            subtype='FILE_PATH', 
            options={'SKIP_SAVE'}
            )

        def execute(self, context):
            from ..file_ass import import_ass

            return global_functions.run_code("import_ass.load_file(context, self.filepath, self.report)")

def menu_func_export(self, context):
    self.layout.operator(ExportASS.bl_idname, text='Halo Amalgam Scene Specification (.ass)')

def menu_func_import(self, context):
    self.layout.operator(ImportASS.bl_idname, text="Halo Amalgam Scene Specification (.ass)")

classeshalo = [
    ASS_ScenePropertiesGroup,
    ASS_SceneProps,
    ImportASS,
    ExportASS
]

if not FileHandler == None:
    classeshalo.append(ImportASS_FileHandler)

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
