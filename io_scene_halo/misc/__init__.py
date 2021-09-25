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
        Panel,
        Operator,
        PropertyGroup
        )

from bpy.props import (
        IntProperty,
        BoolProperty,
        EnumProperty,
        FloatProperty,
        StringProperty,
        PointerProperty,
        FloatVectorProperty
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

class Perm_RegionPropertiesGroup(PropertyGroup):
    permutation_string: StringProperty(
        name = "Permutation",
        default = "",
        description = "Set the permutation for your model"
        )
    region_string: StringProperty(
        name = "Region",
        default = "",
        description = "Set the region for your model"
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

class SkyPropertiesGroup(PropertyGroup):
    longitude_slices: IntProperty(
        name="Longitude Slices",
        description="How tessellated the dome is along the longitude line",
        default=8,
        min=8,
        max=64,
    )

    lattitude_slices: IntProperty(
        name="Lattitude Slices",
        description="How tessellated the dome is along the lattitude line",
        default=8,
        min=8,
        max=64,
    )

    dome_radius: FloatProperty(
        name="Radius",
        description="The radius of our dome object",
        default=8000.0,
        min=100.0,
        max=16000.0
    )

    horizontal_fov: FloatProperty(
        name="Horizontal FOV",
        description="How much of the dome to render horizontal",
        default=360.0,
        min=10.0,
        max=360.0
    )

    vertical_fov: FloatProperty(
        name="Vertical FOV",
        description="How much of the dome to render vertically",
        default=90.0,
        min=10.0,
        max=90.0
    )

    sky_type: EnumProperty(
        name="Sky",
        description="Choose what type of sky to use",
        items=( ('0', "Standard", "Standard"),
                ('1', "CIE",      "CIE"),
                ('2', "Night",    "Night"),
                ('3', "Custom",   "Custom"),
                ('4', "HDR",      "HDR"),
        )
    )

    cie_sky_number: IntProperty(
        name="CIE Sky Number",
        description="I don't even know",
        default=0,
        min=0,
        max=12,
    )

    hdr_map: StringProperty(
        name="HDR Map",
        description="I don't even know. Something about a .PFM file",
        subtype="FILE_PATH"
    )

    override_zenith_color: BoolProperty(
        name ="Override Zenith Color",
        description = "Override the color set for the zenith section of the dome",
        default = False,
    )

    zenith_color: FloatVectorProperty(
        name = "Zenith Color",
        description = "Set the color around the bottom rim of the hemisphere",
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        max = 1.0,
        min = 0.0,
    )

    override_horizon_color: BoolProperty(
        name ="Override Horizon Color",
        description = "Override the color set for the horizon section of the dome",
        default = False,
    )

    horizon_color: FloatVectorProperty(
        name = "Horizon Color",
        description = "Set the color for the upper area of the hemisphere",
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        max = 1.0,
        min = 0.0,
    )

    haze_height: FloatProperty(
        name="Haze Height",
        description="I don't even know",
        default=2.0,
        min=2.0,
        max=15.0
    )

    luminance_only: BoolProperty(
        name ="Luminance Only",
        description = "I don't even know",
        default = False,
    )

    dome_intensity: FloatProperty(
        name="Dome Intensity",
        description="I don't even know",
        default=1.0,
        min=0.0,
        max=2.0
    )

    sun_altittude: FloatProperty(
        name="Sun Altittude",
        description="Set the altittude for the sun.",
        default=10.0,
        min=0.0,
        max=90.0
    )

    sun_heading: FloatProperty(
        name="Sun Heading",
        description="Set the heading for the sun.",
        default=0.0,
        min=0.0,
        max=360.0
    )

    override_sun_color: BoolProperty(
        name ="Use Custom Color",
        description = "Override the color set vertex colors of the sun disk mesh",
        default = False,
    )

    sun_color: FloatVectorProperty(
        name = "Sun Color",
        description = "Set the vertex colors of the sun disk mesh",
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        max = 1.0,
        min = 0.0,
    )

    sun_intensity: FloatProperty(
        name="Sun Intensity",
        description="I don't even know",
        default=1.0,
        min=0.0,
        max=30.0
    )

    sun_disc_size: FloatProperty(
        name="Sun Disc Size",
        description="The size of the disk used for our sun",
        default=0.25,
        min=0.01,
        max=5.0
    )

    windowing: FloatProperty(
        name="Windowing",
        description="I don't even know",
        default=0.9,
        min=0.3,
        max=1.0
    )

    air_cleaness: FloatProperty(
        name="Air Cleaness",
        description="I don't even know",
        default=2.0,
        min=1.67,
        max=10.0
    )

    exposure: FloatProperty(
        name="Exposure",
        description="I don't even know",
        default=0.0,
        min=-30.0,
        max=30.0
    )

    clamp_colors: BoolProperty(
        name ="Clamp Colors",
        description = "I don't even know",
        default = False,
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
        scene_perm_region = scene.set_perm_region

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
        row.operator("halo_bulk.lightmapper_images", text="Generate Lightmap Images")

        box = layout.box()
        box.label(text="Bone Name Helper:")
        col = box.column(align=True)
        row = col.row()
        row.operator("halo_bulk.bulk_bone_names", text="Rename Bones Halo/Blender Style")

        box = layout.box()
        box.label(text="Node Prefix Helper:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Prefix:')
        row.prop(scene_halo_prefix, "prefix_string", text='')
        row = col.row()
        row.operator("halo_bulk.bulk_node_prefix", text="Set Halo Node Pefix")

        box = layout.box()
        box.label(text="Bone Rotation Helper:")
        col = box.column(align=True)
        row = col.row()
        row.operator("halo_bulk.bulk_bone_rotation", text="Invert Bone Roll")
        row.operator("halo_bulk.bulk_bone_reset", text="Reset Bone Rotation")

        box = layout.box()
        box.label(text="Cull Materials:")
        col = box.column(align=True)
        row = col.row()
        row.operator("halo_bulk.cull_materials", text="Cull Materials")

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
        row.operator("halo_bulk.scale_model", text="Generate Scale Model")

        box = layout.box()
        box.label(text="Permutation Region Helper:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Permutation:')
        row.prop(scene_perm_region, "permutation_string", text='')
        row = col.row()
        row.label(text='Region:')
        row.prop(scene_perm_region, "region_string", text='')
        row = col.row()
        row.operator("halo_bulk.perm_region_set", text="Generate Facemap")

class Halo_Sky_Tools_Helper(Panel):
    """Tools to help automate Halo workflow"""
    bl_label = "Halo Sky Tools Helper"
    bl_idname = "HALO_PT_SkyTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Halo Sky Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("halo_bulk.generate_hemisphere", text="Generate Sky")

class Halo_Sky_Dome(Panel):
    bl_label = "Sky Dome"
    bl_idname = "HALO_PT_SkyDome"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_SkyTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo_sky = scene.halo_sky

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Longitude Slices:')
        row.prop(scene_halo_sky, "longitude_slices", text='')
        row = col.row()
        row.label(text='Lattitude Slices:')
        row.prop(scene_halo_sky, "lattitude_slices", text='')
        row = col.row()
        row.label(text='Radius:')
        row.prop(scene_halo_sky, "dome_radius", text='')
        row = col.row()
        row.label(text='Horizontal FOV:')
        row.prop(scene_halo_sky, "horizontal_fov", text='')
        row = col.row()
        row.label(text='Vertical FOV:')
        row.prop(scene_halo_sky, "vertical_fov", text='')
        row = col.row()

class Halo_Sky_Light(Panel):
    bl_label = "Sky Light"
    bl_idname = "HALO_PT_SkyLight"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_SkyTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo_sky = scene.halo_sky

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Sky:')
        row.prop(scene_halo_sky, "sky_type", expand=True)
        if scene_halo_sky.sky_type == '1':
            row = col.row()
            row.label(text='CIE Sky Number:')
            row.prop(scene_halo_sky, "cie_sky_number", text='')

        elif scene_halo_sky.sky_type == '4':
            row = col.row()
            row.label(text='HDR Map:')
            row.prop(scene_halo_sky, "hdr_map", text='')

        row = col.row()
        row.label(text='Haze Height:')
        row.prop(scene_halo_sky, "haze_height", text='', slider=True)
        row = col.row()
        row.label(text='Luminance Only:')
        row.prop(scene_halo_sky, "luminance_only", text='')
        row = col.row()
        row.label(text='Dome Intensity:')
        row.prop(scene_halo_sky, "dome_intensity", text='', slider=True)

class Halo_Sky_Zenith_Color(Panel):
    bl_label = "Zenith Color"
    bl_idname = "HALO_PT_SkyZenithColor"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_SkyLight"

    def draw_header(self, context):
        scene = context.scene
        scene_halo_sky = scene.halo_sky
        self.layout.prop(scene_halo_sky, "override_zenith_color", text='')

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo_sky = scene.halo_sky
        if not scene_halo_sky.override_zenith_color:
            layout.enabled = False

        col = layout.column(align=True)
        row = col.row()
        row.prop(scene_halo_sky, "zenith_color", text='')

class Halo_Sky_Horizon_Color(Panel):
    bl_label = "Horizon Color"
    bl_idname = "HALO_PT_SkyHorizonColor"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_SkyLight"

    def draw_header(self, context):
        scene = context.scene
        scene_halo_sky = scene.halo_sky
        self.layout.prop(scene_halo_sky, "override_horizon_color", text='')

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo_sky = scene.halo_sky
        if not scene_halo_sky.override_horizon_color:
            layout.enabled = False

        col = layout.column(align=True)
        row = col.row()
        row.prop(scene_halo_sky, "horizon_color", text='')

class Halo_Sky_Sun_Light(Panel):
    bl_label = "Sun Light"
    bl_idname = "HALO_PT_SunLight"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_SkyTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo_sky = scene.halo_sky

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Sun Altittude:')
        row.prop(scene_halo_sky, "sun_altittude", text='')
        row = col.row()
        row.label(text='Sun Heading:')
        row.prop(scene_halo_sky, "sun_heading", text='')
        row = col.row()
        row.label(text='Sun Intensity:')
        row.prop(scene_halo_sky, "sun_intensity", text='', slider=True)
        row = col.row()
        row.label(text='Sun Disc Size:')
        row.prop(scene_halo_sky, "sun_disc_size", text='')
        row = col.row()
        row.label(text='Windowing:')
        row.prop(scene_halo_sky, "windowing", text='')
        row = col.row()

class Halo_Sky_Sun_Color(Panel):
    bl_label = "Sun Color"
    bl_idname = "HALO_PT_SkySunColor"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_SunLight"

    def draw_header(self, context):
        scene = context.scene
        scene_halo_sky = scene.halo_sky
        self.layout.prop(scene_halo_sky, "override_sun_color", text='')

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo_sky = scene.halo_sky
        if not scene_halo_sky.override_sun_color:
            layout.enabled = False

        col = layout.column(align=True)
        row = col.row()
        row.prop(scene_halo_sky, "sun_color", text='')

class Halo_Sky_Misc_Settings(Panel):
    bl_label = "Misc Settings"
    bl_idname = "HALO_PT_SkyMiscSettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_SkyTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo_sky = scene.halo_sky

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Air Cleaness:')
        row.prop(scene_halo_sky, "air_cleaness", text='')
        row = col.row()
        row.label(text='Exposure:')
        row.prop(scene_halo_sky, "exposure", text='')
        row = col.row()
        row.label(text='Clamp Colors:')
        row.prop(scene_halo_sky, "clamp_colors", text='')

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

class GenerateHemisphere(Operator):
    """Generates a hemisphere shaped set of skylights for Halo 3 sky models"""
    bl_idname = 'halo_bulk.generate_hemisphere'
    bl_label = 'Sun Strength'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from io_scene_halo.misc import generate_hemisphere
        scene = context.scene
        scene_halo_sky = scene.halo_sky
        return global_functions.run_code("generate_hemisphere.generate_hemisphere(self.report, scene_halo_sky.longitude_slices, scene_halo_sky.lattitude_slices, scene_halo_sky.dome_radius, scene_halo_sky.horizontal_fov, scene_halo_sky.vertical_fov, scene_halo_sky.sky_type, scene_halo_sky.cie_sky_number, scene_halo_sky.hdr_map, scene_halo_sky.haze_height, scene_halo_sky.luminance_only, scene_halo_sky.dome_intensity, scene_halo_sky.override_zenith_color, scene_halo_sky.zenith_color, scene_halo_sky.override_horizon_color, scene_halo_sky.horizon_color, scene_halo_sky.sun_altittude, scene_halo_sky.sun_heading, scene_halo_sky.sun_intensity, scene_halo_sky.sun_disc_size, scene_halo_sky.windowing, scene_halo_sky.override_sun_color, scene_halo_sky.sun_color, scene_halo_sky.air_cleaness, scene_halo_sky.exposure, scene_halo_sky.clamp_colors)")

class ExportLightmap(Operator, ExportHelper):
    """Write a LUV file"""
    bl_idname = "export_luv.export"
    bl_label = "Export LUV"
    filename_ext = '.LUV'

    def execute(self, context):
        from io_scene_halo.misc import export_lightmap

        return global_functions.run_code("export_lightmap.write_file(context, self.filepath, self.report)")

class PermRegionSet(Operator):
    """Create a facemap with a permutation and a region"""
    bl_idname = "halo_bulk.perm_region_set"
    bl_label = "Create a Facemap"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        scene_perm_region = scene.set_perm_region
        from io_scene_halo.misc import region_perm_prep

        return global_functions.run_code("region_perm_prep.create_facemap(scene_perm_region.permutation_string, scene_perm_region.region_string)")

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
    GenerateHemisphere,
    PermRegionSet,
    Halo_Tools_Helper,
    Halo_Sky_Tools_Helper,
    Halo_Sky_Dome,
    Halo_Sky_Light,
    Halo_Sky_Zenith_Color,
    Halo_Sky_Horizon_Color,
    Halo_Sky_Sun_Light,
    Halo_Sky_Sun_Color,
    Halo_Sky_Misc_Settings,
    Halo_LightmapperPropertiesGroup,
    Scale_ModelPropertiesGroup,
    SkyPropertiesGroup,
    Halo_PrefixPropertiesGroup,
    Perm_RegionPropertiesGroup
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.Scene.halo_lightmapper = PointerProperty(type=Halo_LightmapperPropertiesGroup, name="Halo Lightmapper Helper", description="Set properties for the lightmapper")
    bpy.types.Scene.halo_prefix = PointerProperty(type=Halo_PrefixPropertiesGroup, name="Halo Prefix Helper", description="Set properties for node prefixes")
    bpy.types.Scene.scale_model = PointerProperty(type=Scale_ModelPropertiesGroup, name="Halo Scale Model Helper", description="Create meshes for scale")
    bpy.types.Scene.halo_sky = PointerProperty(type=SkyPropertiesGroup, name="Sky Helper", description="Generate a sky for Halo 3")
    bpy.types.Scene.set_perm_region = PointerProperty(type=Perm_RegionPropertiesGroup, name="Halo Permutation Region Helper", description="Creates a facemap with the exact name we need")

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    del bpy.types.Scene.halo_lightmapper
    del bpy.types.Scene.halo_prefix
    del bpy.types.Scene.halo_sky
    del bpy.types.Scene.sun_strength
    del bpy.types.Scene.set_perm_region
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
