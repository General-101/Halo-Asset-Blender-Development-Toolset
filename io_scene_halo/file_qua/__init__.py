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
from bpy.props import (
        EnumProperty,
        StringProperty,
        BoolProperty,
        PointerProperty,
        IntProperty
        )

from bpy.types import (
    Panel,
    Operator,
    PropertyGroup
    )

from bpy_extras.io_utils import (
    ImportHelper,
    ExportHelper
    )

class QUA_SceneProps(Panel):
    bl_label = "QUA Scene Properties"
    bl_idname = "QUA_PT_GameVersionPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_ScenePropertiesPanel"
    def draw(self, context):
        scene = context.scene
        scene_qua = scene.qua
        scene_halo = scene.halo

        layout = self.layout

        box = layout.box()
        box.label(text="Game Title:")
        col = box.column(align=True)
        row = col.row()
        row.prop(scene_qua, "game_title", text='')
        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)
        if scene_halo.expert_mode:
            row = col.row()
            row.label(text='QUA Version:')
            row.prop(scene_qua, "qua_version", text='')

        if scene_qua.game_title == "halo4":
            row = col.row()
            row.label(text='QUA Type:')
            row.prop(scene_qua, "qua_type", text='')
            row = col.row()
            row.label(text='QUA Revision:')
            row.prop(scene_qua, "qua_revision", text='')

        row = col.row()
        row.label(text='Strip Identifier:')
        row.prop(scene_qua, "strip_identifier", text='')

        box = layout.box()
        box.label(text="Mask Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Export Hidden Geometry:')
        row.prop(scene_qua, "hidden_geo", text='')
        row = col.row()
        row.label(text='Export Non-render Geometry:')
        row.prop(scene_qua, "nonrender_geo", text='')

        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Use As Default Export Settings:')
        row.prop(scene_qua, "use_scene_properties", text='')

def version_settings_callback(self, context):
    items=[('1', "1", "Non-functional")]

    print(self.game_title)
    if self.game_title == "halo3":
        items.append(('2', "2", "Non-functional"))
        items.append(('3', "3", "Non-functional"))
        items.append(('4', "4", "Non-functional"))
        items.append(('5', "5", "Retail"))

    elif self.game_title == "halor":
        items.append(('2', "2", "Retail"))

    elif self.game_title == "halo4":
        items.append(('2', "2", "Non-functional"))
        items.append(('3', "3", "Non-functional"))
        items.append(('4', "4", "Retail"))

    return items

def update_version(self, context):
    if self.game_title == "halo3":
        self.qua_version = '5'

    elif self.game_title == "halor":
        self.qua_version = '2'

    else:
        self.qua_version = '4'

class QUA_ScenePropertiesGroup(PropertyGroup):
    game_title: EnumProperty(
        name="Game Title:",
        description="What game will the Ubercam file be used for",
        items=[ ('halo3', "Halo 3", "Export a QUA intended for Halo 3"),
                ('halor', "Halo Reach", "Export a QUA intended for Halo Reach"),
                ('halo4', "Halo 4", "Export a QUA intended for Halo 4"),
            ],
        update = update_version
        )

    qua_version: EnumProperty(
        name="Version:",
        description="What version to use for the Ubercam file",
        options={'HIDDEN'},
        items=version_settings_callback,
        default=4
        )

    qua_type: EnumProperty(
        name="Scene Type:",
        description="What type of scene is the QUA file intended to be",
        items=[ ('main', "Main", "Export a standard QUA scene"),
                ('segment', "Segment", "Export a segment QUA scene")
            ]
        )

    qua_revision: IntProperty(
        name="Revision",
        description="Set the file revision for the QUA",
        default = 0,
        )

    strip_identifier: BoolProperty(
        name ="Strip Identifier",
        description = "Strip identifier from filename of animation paths",
        default = True,
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

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

class ExportQUA(Operator, ExportHelper):
    """Write a QUA file"""
    bl_idname = 'export_scene.qua'
    bl_label = 'Export QUA'
    filename_ext = '.QUA'

    game_title: EnumProperty(
        name="Game Title:",
        description="What game will the Ubercam file be used for",
        items=[ ('halo3', "Halo 3", "Export a QUA intended for Halo 3"),
                ('halor', "Halo Reach", "Export a QUA intended for Halo Reach"),
                ('halo4', "Halo 4", "Export a QUA intended for Halo 4"),
            ],
        update = update_version
        )

    qua_version: EnumProperty(
        name="Version:",
        description="What version to use for the Ubercam file",
        options={'HIDDEN'},
        items=version_settings_callback,
        default=4
        )

    qua_type: EnumProperty(
        name="Scene Type:",
        description="What type of scene is the QUA file intended to be",
        items=[ ('main', "Main", "Export a standard QUA scene"),
                ('segment', "Segment", "Export a segment QUA scene")
            ]
        )

    qua_revision: IntProperty(
        name="Revision",
        description="Set the file revision for the QUA",
        default = 0,
        )

    strip_identifier: BoolProperty(
        name ="Strip Identifier",
        description = "Strip identifier from filename of animation paths",
        default = True,
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

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

    filter_glob: StringProperty(
        default="*.qua",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from ..file_qua import export_qua

        return global_functions.run_code("export_qua.write_file(context, self.filepath, self.game_title, int(self.qua_version), self.qua_type, self.qua_revision, self.strip_identifier, self.hidden_geo, self.nonrender_geo, self.report)")

    def draw(self, context):
        scene = context.scene
        scene_halo = scene.halo
        scene_qua = scene.qua

        layout = self.layout

        is_enabled = True
        if scene_qua.use_scene_properties:
            is_enabled = False

        if scene_qua.use_scene_properties:
            self.game_title = scene_qua.game_title
            self.qua_version = scene_qua.qua_version
            self.strip_identifier = scene_qua.strip_identifier
            self.hidden_geo = scene_qua.hidden_geo
            self.nonrender_geo = scene_qua.nonrender_geo

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
            row.label(text='QUA Version:')
            row.prop(self, "qua_version", text='')

        if self.game_title == "halo4":
            row = col.row()
            row.label(text='QUA Type:')
            row.prop(self, "qua_type", text='')
            row = col.row()
            row.label(text='QUA Revision:')
            row.prop(self, "qua_revision", text='')

        row = col.row()
        row.enabled = is_enabled
        row.label(text='Strip Identifier:')
        row.prop(self, "strip_identifier", text='')

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
        row.label(text='Use Scene Export Settings:')
        row.prop(scene_qua, "use_scene_properties", text='')

if (4, 1, 0) <= bpy.app.version:
    from bpy.types import FileHandler

class ImportQUA(Operator, ImportHelper):
    """Import a QUA file"""
    bl_idname = "import_scene.qua"
    bl_label = "Import QUA"
    filename_ext = '.QUA'

    game_title: EnumProperty(
        name="Game Title:",
        description="What game was the cinematic file made for",
        items=[ ('halo3', "Halo 3", "Export a QUA intended for Halo 3"),
                ('halor', "Halo Reach", "Export a QUA intended for Halo Reach"),
                ('halo4', "Halo 4", "Export a QUA intended for Halo 4"),
            ]
        )

    filter_glob: StringProperty(
        default="*.qua",
        options={'HIDDEN'},
        )

    filepath: StringProperty(
        subtype='FILE_PATH', 
        options={'SKIP_SAVE'}
        )

    def execute(self, context):
        from ..file_qua import import_qua

        return global_functions.run_code("import_qua.load_file(context, self.game_title, self.filepath, self.report)")

    if (4, 1, 0) <= bpy.app.version:
        def invoke(self, context, event):
            if self.filepath:
                return self.execute(context)
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}
        
if (4, 1, 0) <= bpy.app.version:
    class ImportQUA_FileHandler(FileHandler):
        bl_idname = "QUA_FH_import"
        bl_label = "File handler for QUA import"
        bl_import_operator = "import_scene.qua"
        bl_file_extensions = ".QUA"

        @classmethod
        def poll_drop(cls, context):
            return (context.area and context.area.type == 'VIEW_3D')

def menu_func_export(self, context):
    self.layout.operator(ExportQUA.bl_idname, text='Halo Ubercam Animation (.qua)')

def menu_func_import(self, context):
    self.layout.operator(ImportQUA.bl_idname, text="Halo Ubercam Animation (.qua)")

classeshalo = [
    ImportQUA,
    ExportQUA,
    QUA_SceneProps,
    QUA_ScenePropertiesGroup
]

if (4, 1, 0) <= bpy.app.version:
    classeshalo.append(ImportQUA_FileHandler)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.Scene.qua = PointerProperty(type=QUA_ScenePropertiesGroup, name="QUA Scene Properties", description="Set properties for the QUA exporter")

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
