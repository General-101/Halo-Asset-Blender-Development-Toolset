# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Generalkidd & Crisp
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
    "name": "Halo GR2 Export",
    "author": "Generalkidd, Crisp",
    "version": (1.0),
    "blender": (3, 3, 0),
    "location": "File > Export",
    "category": "Export",
    "description": "Halo Granny File and Sidecar exporter",
}
import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

import os
t = os.getcwd()
t += "\\scripts\\addons\\io_scene_fbx"
print(t)
import sys
path = sys.modules[bpy.types.IMPORT_SCENE_OT_fbx.__module__].__file__
from subprocess import run
run('python ' + path)
print("HERE!!!")
#bpy.ops.IMPORT_SCENE_OT_fbx.FBX_PT_import_transform(bpy.types.Panel)

class Export_Halo_GR2(Operator, ExportHelper):
    """Writes a Halo Reach GR2 File using your Halo Editing Kit"""
    bl_idname = "export_halo.gr2"
    bl_label = "Export"

    filename_ext = ".gr2"
    filter_glob: StringProperty(
        default="*.gr2",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    export_gr2: BoolProperty(
            name="Export To GR2",
            description="Uses the exported FBX and JSON files to generate a GR2 File",
            default=True,
            )
    delete_fbx: BoolProperty(
            name="FBX",
            description="Delete the source FBX file after GR2 conversion",
            default=False,
            )
    delete_json: BoolProperty(
            name="JSON",
            description="Delete the source JSON file after GR2 conversion",
            default=False,
            )
    export_sidecar: BoolProperty(
            name="Export Sidecar",
            description="",
            default=True,
            )
    sidecar_type: EnumProperty(
            name='Asset Type',
            description='',
            default='MODEL',
            items=[ ('MODEL', "Model", ""),
                ('SCENARIO', "Scenario", ""),
                ('DECORATOR', "Decorator", ""),
                ('PARTICLE MODEL', "Particle Model", ""),
               ]
        )
    asset_path: StringProperty(
            name="Asset Folder Path",
            description="",
            )

    def execute(self, context):
        import sys
        sys.path.insert(0,t)

        from io_scene_fbx import export_fbx_bin
        from . import export_gr2, export_sidecar_xml
        export_fbx_bin.save(self, context, **keywords)
        export_gr2.save(self, context, self.report, **keywords)
        return export_sidecar_xml.save(self, context, self.report, **keywords)

    def draw(self, context):
        pass

def menu_func_export(self, context):
    self.layout.operator(Export_Halo_GR2.bl_idname, text="Halo Granny File (.gr2)")

class Halo_GR2_Settings(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Generate GR2 File"
    bl_parent_id = "FILE_PT_operator"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_HALO_OT_gr2"

    def draw_header(self, context):
        sfile = context.space_data
        operator = sfile.active_operator

        self.layout.prop(operator, "export_gr2", text='')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        sfile = context.space_data
        operator = sfile.active_operator

        layout.enabled = operator.export_gr2

        sublayout = layout.column(heading="Clean Up Files")
        sublayout.prop(operator, "delete_fbx")
        sublayout.prop(operator, "delete_json")

class Halo_Sidecar_Settings(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Generate Sidecar"
    bl_parent_id = "FILE_PT_operator"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_HALO_OT_gr2"

    def draw_header(self, context):
        file = context.space_data
        operator = file.active_operator

        self.layout.prop(operator, "export_sidecar", text='')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        sfile = context.space_data
        operator = sfile.active_operator

        layout.enabled = operator.export_sidecar

        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()

        col.prop(operator, "sidecar_type", text='Asset Type')
        col.prop(operator, 'asset_path', text='Asset Folder')

classes = (
    Export_Halo_GR2,
    Halo_GR2_Settings,
    Halo_Sidecar_Settings,
    #bpy.ops.IMPORT_SCENE_OT_fbx.FBX_PT_import_transform,
    #bpy.ops.IMPORT_SCENE_OT_fbx.FBX_PT_import_include,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
