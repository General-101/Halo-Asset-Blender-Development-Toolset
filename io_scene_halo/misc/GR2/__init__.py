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

import bpy

from bpy.types import (
        Panel,
        Operator,
        PropertyGroup
        )

from bpy.props import (
        StringProperty,
        PointerProperty
        )

class GR2_Tools_Helper(Panel):
    """Tools to help automate Halo GR2 workflow"""
    bl_label = "Halo GR2 Tools Helper"
    bl_idname = "HALO_PT_GR2_AutoTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Halo GR2 Tools"

    def draw(self, context):
        layout = self.layout


#######################################
# FRAME IDS TOOL
class GR2_SetFrameIDs(Panel):
    bl_label = "Set Frame IDs"
    bl_idname = "HALO_PT_GR2_SetFrameIDs"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GR2_AutoTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_gr2_frame_ids = scene.gr2_frame_ids

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()
        col = layout.column(heading="Animation Graph Path")
        sub = col.column(align=True)
        sub.prop(scene_gr2_frame_ids, "anim_tag_path", text='')
        sub.separator()
        sub.operator("halo_gr2.set_frame_ids", text="Set Frame IDs")
        sub.separator()
        sub.operator("halo_gr2.reset_frame_ids", text="Reset Frame IDs")

class GR2_SetFrameIDsOp(Operator):
    bl_idname = 'halo_gr2.set_frame_ids'
    bl_label = 'Set Frame IDs'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from .set_frame_ids import set_frame_ids
        return set_frame_ids(context, self.report)

class GR2_ResetFrameIDsOp(Operator):
    bl_idname = 'halo_gr2.reset_frame_ids'
    bl_label = 'Reset Frame IDs'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from .set_frame_ids import reset_frame_ids
        return reset_frame_ids(context, self.report)

class GR2_SetFrameIDsPropertiesGroup(PropertyGroup):
    anim_tag_path: StringProperty(
        name="Path to Animation Tag",
        description="Specify the full or relative path to a model animation graph",
        default='',
    )

#######################################
# HALO MANAGER TOOL

class GR2_HaloLauncher(Panel):
    bl_label = "Halo Launcher"
    bl_idname = "HALO_PT_GR2_HaloLauncher"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "HALO_PT_GR2_AutoTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_gr2_halo_launcher = scene.gr2_halo_launcher

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()
        col.scale_y = 1.5
        col.operator('halo_gr2.launch_foundation')
        col.separator()
        split = layout.split()
        col = split.column()
        col.operator('halo_gr2.launch_data')
        col = split.column(align=True)
        col.operator('halo_gr2.launch_tags')
        if scene_gr2_halo_launcher.sidecar_path != '':
            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
            col = flow.column()
            col.separator()
            col.operator('halo_gr2.launch_source')

class GR2_HaloLauncher_Foundation(Operator):
    bl_idname = 'halo_gr2.launch_foundation'
    bl_label = 'Launch Foundation'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from .halo_launcher import LaunchFoundation
        return LaunchFoundation()

class GR2_HaloLauncher_Data(Operator):
    bl_idname = 'halo_gr2.launch_data'
    bl_label = 'Data Folder'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from .halo_launcher import LaunchData
        return LaunchData()

class GR2_HaloLauncher_Tags(Operator):
    bl_idname = 'halo_gr2.launch_tags'
    bl_label = 'Tags Folder'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from .halo_launcher import LaunchTags
        return LaunchTags()

class GR2_HaloLauncher_Source(Operator):
    bl_idname = 'halo_gr2.launch_source'
    bl_label = 'Source Files'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        scene_gr2_halo_launcher = scene.gr2_halo_launcher
        from .halo_launcher import LaunchSource
        return LaunchSource(scene_gr2_halo_launcher.sidecar_path)

class GR2_HaloLauncherPropertiesGroup(PropertyGroup):
    sidecar_path: StringProperty(
        name="",
        description="",
        default='',
    )
    asset_name: StringProperty(
        name="",
        description="",
        default='',
    )

#######################################
# SHADER FINDER TOOL

class GR2_ShaderFinder(Panel):
    bl_label = "Update Materials by Shader"
    bl_idname = "HALO_PT_GR2_ShaderFinder"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GR2_AutoTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_gr2_shader_finder = scene.gr2_shader_finder

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()
        col = layout.column(heading="Shaders Directory")
        col.prop(scene_gr2_shader_finder, 'shaders_dir', text='')
        col = col.row()
        col.scale_y = 1.5
        col.operator('halo_gr2.shader_finder')

class GR2_ShaderFinder_Find(Operator):
    bl_idname = 'halo_gr2.shader_finder'
    bl_label = 'Update Shader Paths'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        scene_gr2_shader_finder = scene.gr2_shader_finder
        from .shader_finder import FindShaders
        return FindShaders(context, scene_gr2_shader_finder.shaders_dir, self.report)

class GR2_HaloShaderFinderPropertiesGroup(PropertyGroup):
    shaders_dir: StringProperty(
        name="Shaders Directory",
        description="Leave blank to search the entire tags folder for shaders or input a directory path to specify the folder (and sub-folders) to search for shaders",
        default='',
    )

#######################################
# HALO EXPORT TOOL

class GR2_HaloExport(Panel):
    bl_label = "Halo Export"
    bl_idname = "HALO_PT_GR2_HaloExport"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_icon = 'EXPORT'
    bl_parent_id = "HALO_PT_GR2_AutoTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_gr2_halo_launcher = scene.gr2_halo_launcher

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()
        col.scale_y = 1.5
        col.operator('halo_gr2.export', text='Export', icon='EXPORT')
        if scene_gr2_halo_launcher.sidecar_path != '':
            col.separator()
            col.operator('halo_gr2.export_quick', text='Quick Export', icon='EMPTY_SINGLE_ARROW')

class GR2_HaloExport_Export(Operator):
    bl_idname = 'halo_gr2.export'
    bl_label = 'Export'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from .halo_export import Export
        return Export(bpy.ops.export_scene.gr2)

class GR2_HaloExport_ExportQuick(Operator):
    bl_idname = 'halo_gr2.export_quick'
    bl_label = 'Quick Export'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from .halo_export import ExportQuick
        return ExportQuick(bpy.ops.export_scene.gr2, self.report, context)

class GR2_HaloExportFinderPropertiesGroup(PropertyGroup):
    final_report: StringProperty(
        name="",
        description="",
        default='',
    )

classeshalo = (
    GR2_Tools_Helper,
    GR2_HaloExport,
    GR2_HaloExport_Export,
    GR2_HaloExport_ExportQuick,
    GR2_HaloExportFinderPropertiesGroup,
    GR2_HaloLauncher,
    GR2_HaloLauncher_Foundation,
    GR2_HaloLauncher_Data,
    GR2_HaloLauncher_Tags,
    GR2_HaloLauncher_Source,
    GR2_HaloLauncherPropertiesGroup,
    GR2_ShaderFinder,
    GR2_ShaderFinder_Find,
    GR2_HaloShaderFinderPropertiesGroup,
    GR2_SetFrameIDs,
    GR2_SetFrameIDsOp,
    GR2_ResetFrameIDsOp,
    GR2_SetFrameIDsPropertiesGroup,
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.Scene.gr2_frame_ids = PointerProperty(type=GR2_SetFrameIDsPropertiesGroup, name="Halo Frame ID Getter", description="Gets Frame IDs")
    bpy.types.Scene.gr2_halo_launcher = PointerProperty(type=GR2_HaloLauncherPropertiesGroup, name="Halo Launcher", description="Launches stuff")
    bpy.types.Scene.gr2_shader_finder = PointerProperty(type=GR2_HaloShaderFinderPropertiesGroup, name="Shader Finder", description="Find Shaders")
    bpy.types.Scene.gr2_export = PointerProperty(type=GR2_HaloExportFinderPropertiesGroup, name="Halo Export", description="")

    
def unregister():
    del bpy.types.Scene.halo_import_fixup
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
    
