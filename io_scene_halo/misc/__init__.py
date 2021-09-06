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

from bpy_extras.io_utils import ExportHelper

from bpy.types import (
        Operator,
        Panel,
        PropertyGroup
        )

from bpy.props import (
        IntProperty,
        EnumProperty,
        PointerProperty,
        StringProperty
        )

from ..global_functions import global_functions

class Halo_LightmapperPropertiesGroup(PropertyGroup):
    res_x: IntProperty(
        name="Image Width",
        description="Set the width for images created during bulk",
        default=256,
        min=2,
    )

    res_y: IntProperty(
        name="Image Height",
        description="Set the height for images created during bulk",
        default=256,
        min=2,
    )

class Halo_PrefixPropertiesGroup(PropertyGroup):
    prefix_string: StringProperty(
        name = "Prefix",
        default = "",
        description = "Set the new prefix for selected objects. Undo if you mess up cause you won't be able to try again!"
        )

class Scale_ModelPropertiesGroup(PropertyGroup):
    game_version: EnumProperty(
        name="Game:",
        description="What game will the scale models be from.",
        items=[ ('haloce', "Halo CE", "Models from CE only"),
                ('halo2', "Halo 2", "Models from Halo 2 only"),
                ('halo3', "Halo 3", "Models from Halo 3 only"),
               ]
        )

    unit_type: EnumProperty(
        name="Unit Type:",
        description="Is the unit a character or vehicle",
        items=[ ('character', "Character", "Only show characters"),
                ('vehicle', "Vehicle", "Only show vehicles"),
               ]
        )

    halo_one_scale_model_char: EnumProperty(
        name="Halo 1 Character Models:",
        description="What model to create",
        items=[
                ('captain', "Captain", "Captain Keyes Model"),
                ('cortana', "Cortana", "Cortana Model"),
                ('crewman', "Crewman", "Crewman Model"),
                ('spartan', "Cyborg", "Cyborg Model"),
                ('elite', "Elite", "Elite Model"),
                ('engineer', "Engineer", "Engineer Model"),
                ('flood_captain', "Flood Captain", "Flood Captain Model"),
                ('flood_infection', "Flood Infection", "Flood Infection Model"),
                ('flood_carrier', "Flood Carrier", "Flood Carrier Model"),
                ('floodcombat_elite', "Flood Combat Elite", "Flood Combat Elite Model"),
                ('floodcombat_human', "Flood Combat Human", "Flood Combat Human Model"),
                ('grunt', "Grunt", "Grunt Model"),
                ('hunter', "Hunter", "Hunter Model"),
                ('jackal', "Jackal", "Jackal Model"),
                ('marine', "Marine", "Marine Model"),
                ('marine_armored', "Marine Armored", "Marine Armored Model"),
                ('monitor', "Monitor", "Monitor Model"),
                ('pilot', "Pilot", "Pilot Model"),
                ('sentinel', "Sentinel", "Sentinel Model"),
               ]
        )

    halo_one_scale_model_vehi: EnumProperty(
        name="Halo 1 Vehicle Models:",
        description="What model to create",
        items=[
                ('banshee', "Banshee", "Banshee Model"),
                ('c_gun_turret', "Covenant Gun Turret", "Covenant Gun Turret Model"),
                ('c_dropship', "Covenant Dropship", "Covenant Dropship Model"),
                ('fighterbomber', "Fighter Bomber", "Fighter Bomber Model"),
                ('ghost', "Ghost", "Ghost Model"),
                ('lifepod', "Lifepod", "Lifepod Model"),
                ('lifepod_entry', "Lifepod Entry", "Lifepod Entry Model"),
                ('pelican', "Pelican", "Pelican Model"),
                ('rwarthog', "Rocket Warthog", "Rocket Warthog Model"),
                ('scorpion', "Scorpion", "Scorpion Model"),
                ('warthog', "Warthog", "Warthog Model"),
                ('wraith', "Wraith", "Wraith Model"),
               ]
        )

class Halo_Tools_Helper(Panel):
    """Tools to help automate Halo workflow"""
    bl_label = "Halo Tools Helper"
    bl_idname = "HALO_PT_AutoTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Halo Tools"

    def draw(self, context):
        scene = context.scene
        scene_halo_lightmapper = scene.halo_lightmapper
        scene_halo_prefix = scene.halo_prefix
        scene_scale_model = scene.scale_model

        layout = self.layout
        row = layout.row()

        box = layout.box()
        box.label(text="Lightmap Helper:")
        col = box.column(align=True)

        row = col.row()
        row.label(text='Image Width:')
        row.prop(scene_halo_lightmapper, "res_x", text='')
        row = col.row()
        row.label(text='Image Height:')
        row.prop(scene_halo_lightmapper, "res_y", text='')
        row = col.row()
        row.operator("halo_bulk.lightmapper_images", text="BULK!!!")

        box = layout.box()
        box.label(text="Bone Name Helper:")
        col = box.column(align=True)
        row = col.row()
        row.operator("halo_bulk.bulk_bone_names", text="BULK!!!")

        box = layout.box()
        box.label(text="Node Prefix Helper:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Prefix:')
        row.prop(scene_halo_prefix, "prefix_string", text='')
        row = col.row()
        row.operator("halo_bulk.bulk_node_prefix", text="BULK!!!")

        box = layout.box()
        box.label(text="Bone Rotation Helper:")
        col = box.column(align=True)
        row = col.row()
        row.operator("halo_bulk.bulk_bone_rotation", text="BULK!!!")
        row.operator("halo_bulk.bulk_bone_reset", text="BULK!!!")

        box = layout.box()
        box.label(text="Cull Materials:")
        col = box.column(align=True)
        row = col.row()
        row.operator("halo_bulk.cull_materials", text="BULK!!!")

        box = layout.box()
        box.label(text="Scale Model Helper:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Game:')
        row.prop(scene_scale_model, "game_version", text="")
        row = col.row()
        row.label(text='Unit Type:')
        row.prop(scene_scale_model, "unit_type", text="")
        row = col.row()
        row.label(text='Model:')
        if scene_scale_model.unit_type == "character":
            row.prop(scene_scale_model, "halo_one_scale_model_char", text="")
        else:
            row.prop(scene_scale_model, "halo_one_scale_model_vehi", text="")
        row = col.row()
        row.operator("halo_bulk.scale_model", text="BULK!!!")

class Bulk_Lightmap_Images(Operator):
    """Create image nodes with a set size for all materials in the scene"""
    bl_idname = 'halo_bulk.lightmapper_images'
    bl_label = 'Bulk Halo Images'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from io_scene_halo.misc import lightmapper_prep
        scene = context.scene
        scene_halo_lightmapper = scene.halo_lightmapper
        return global_functions.run_code("lightmapper_prep.lightmap_bulk(context, scene_halo_lightmapper.res_x, scene_halo_lightmapper.res_y)")

class Bulk_Rename_Bones(Operator):
    """Rename all bones in the scene to swap from Blender .L/.R to Halo l/r bone naming scheme and vice versa"""
    bl_idname = 'halo_bulk.bulk_bone_names'
    bl_label = 'Bulk Halo Bones Names'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from io_scene_halo.misc import rename_bones
        return global_functions.run_code("rename_bones.rename_bones()")

class Bulk_Rename_Prefix(Operator):
    """Rename prefixes for selected objects in the scene"""
    bl_idname = 'halo_bulk.bulk_node_prefix'
    bl_label = 'Bulk Halo Node Prefix'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from io_scene_halo.misc import rename_prefix
        scene = context.scene
        scene_halo_prefix = scene.halo_prefix
        return global_functions.run_code("rename_prefix.rename_prefix(scene_halo_prefix.prefix_string)")

class Bulk_Rotate_Bones(Operator):
    """Add -180 degrees for the roll of all selected bones in edit mode."""
    bl_idname = 'halo_bulk.bulk_bone_rotation'
    bl_label = 'Bulk Halo Bones Rotate'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from io_scene_halo.misc import rotate_bones
        return global_functions.run_code("rotate_bones.rotate_bones()")

class Bulk_Reset_Bones(Operator):
    """Resets bone rotation of all selected bones in edit mode."""
    bl_idname = 'halo_bulk.bulk_bone_reset'
    bl_label = 'Bulk Halo Bones Reset'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from io_scene_halo.misc import rotate_bones
        return global_functions.run_code("rotate_bones.reset_bones()")

class Cull_Materials(Operator):
    """Sets unused material slots to none for the selected object."""
    bl_idname = 'halo_bulk.cull_materials'
    bl_label = 'Cull Materials'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from io_scene_halo.misc import cull_materials
        return global_functions.run_code("cull_materials.cull_materials()")

class Scale_Model(Operator):
    """Creates a model that matches the ingame scale."""
    bl_idname = 'halo_bulk.scale_model'
    bl_label = 'Scale Model'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from io_scene_halo.misc import scale_models
        scene = context.scene
        scene_scale_model = scene.scale_model
        return global_functions.run_code("scale_models.create_model(scene_scale_model.game_version, scene_scale_model.unit_type, scene_scale_model.halo_one_scale_model_char, scene_scale_model.halo_one_scale_model_vehi)")

class ExportLightmap(Operator, ExportHelper):
    """Write a LUV file"""
    bl_idname = "export_luv.export"
    bl_label = "Export LUV"
    filename_ext = '.LUV'

    def execute(self, context):
        from io_scene_halo.misc import export_lightmap

        return global_functions.run_code("export_lightmap.write_file(context, self.filepath, self.report)")

def menu_func_export(self, context):
    self.layout.operator(ExportLightmap.bl_idname, text="Halo Lightmap UV (.luv)")

classeshalo = (
    ExportLightmap,
    Bulk_Lightmap_Images,
    Bulk_Rename_Bones,
    Bulk_Rename_Prefix,
    Bulk_Rotate_Bones,
    Bulk_Reset_Bones,
    Cull_Materials,
    Scale_Model,
    Halo_Tools_Helper,
    Halo_LightmapperPropertiesGroup,
    Scale_ModelPropertiesGroup,
    Halo_PrefixPropertiesGroup
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.Scene.halo_lightmapper = PointerProperty(type=Halo_LightmapperPropertiesGroup, name="Halo Lightmapper Helper", description="Set properties for the lightmapper")
    bpy.types.Scene.halo_prefix = PointerProperty(type=Halo_PrefixPropertiesGroup, name="Halo Prefix Helper", description="Set properties for node prefixes")
    bpy.types.Scene.scale_model = PointerProperty(type=Scale_ModelPropertiesGroup, name="Halo Scale Model Helper", description="Create meshes for scale")

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    del bpy.types.Scene.halo_lightmapper
    del bpy.types.Scene.halo_prefix
    del bpy.types.Scene.scale_model
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
