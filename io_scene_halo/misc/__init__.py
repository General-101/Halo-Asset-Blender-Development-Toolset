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

class JMA_BatchDialog(Operator):
    """Convert multiple animation source files for a specific game"""
    bl_idname = "import_scene.jma_batch"
    bl_label = "Convert JMA"

    filter_glob: StringProperty(
        default="*.jma;*.jmm;*.jmt;*.jmo;*.jmr;*.jmrx;*.jmh;*.jmz;*.jmw",
        options={'HIDDEN'},
        )

    directory: StringProperty(
        name="Directory",
        description="A directory containing animation source files to convert",
    )

    def execute(self, context):
        scene = context.scene
        scene_halo_anim_batch = scene.halo_anim_batch
        scene_halo_anim_batch.directory = self.directory
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class JMA_BatchPropertiesGroup(PropertyGroup):
    jma_version: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16392",
        options={'HIDDEN'},
        items=[ ('16390', "16390", "CE/H2/H3"),
                ('16391', "16391", "CE/H2/H3"),
                ('16392', "16392", "CE/H2/H3"),
                ('16393', "16393", "H2/H3"),
                ('16394', "16394", "H2/H3"),
                ('16395', "16395", "H2/H3"),
            ]
        )

    jma_version_ce: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16392",
        items=[ ('16390', "16390", "CE"),
                ('16391', "16391", "CE"),
                ('16392', "16392", "CE"),
            ]
        )

    jma_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16395",
        items=[ ('16390', "16390", "H2"),
                ('16391', "16391", "H2"),
                ('16392', "16392", "H2"),
                ('16393', "16393", "H2"),
                ('16394', "16394", "H2"),
                ('16395', "16395", "H2"),
            ]
        )

    jma_version_h3: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16395",
        items=[ ('16390', "16390", "H3"),
                ('16391', "16391", "H3"),
                ('16392', "16392", "H3"),
                ('16393', "16393", "H3"),
                ('16394', "16394", "H3"),
                ('16395', "16395", "H3"),
            ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        items=[ ('haloce', "Halo CE", "Export an animation intended for Halo Custom Edition or Halo 1 MCC"),
                ('halo2', "Halo 2", "Export an animation intended for Halo 2 Vista or Halo 2 MCC"),
                ('halo3mcc', "Halo 3 MCC", "Export an animation intended for Halo 3 MCC"),
            ]
        )

    directory: StringProperty(
        name="Directory",
        description="A directory containing animation source files to convert",
        )

class Halo_ImportFixupPropertiesGroup(PropertyGroup):
    threshold: FloatProperty(
        name="Threshold",
        description="Maximum distance between elements to merge",
        default=0.0001,
        min=0.000001,
        max=50.0
    )

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
        description = "Set the new prefix for selected objects. Undo if you mess up cause you won't be able to try again"
        )

class Face_SetPropertiesGroup(PropertyGroup):
    set_facemap: BoolProperty(
        name ="Set Face Map",
        description = "Sets all faces in the active object to use the newly created face map.",
        default = False,
    )

    level_of_detail: EnumProperty(
        name="LOD:",
        description="What LOD to use for the object",
        items=[ ('NONE', "NONE", "No level of detail set"),
                ('L1', "L1", "Super Low"),
                ('L2', "L2", "Low"),
                ('L3', "L3", "Medium"),
                ('L4', "L4", "High"),
                ('L5', "L5", "Super High"),
                ('L6', "L6", "Hollywood"),
               ]
        )

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
                ('0', "Captain", "Captain Keyes Model"),
                ('1', "Cortana", "Cortana Model"),
                ('2', "Crewman", "Crewman Model"),
                ('3', "Cyborg", "Cyborg Model"),
                ('4', "Elite", "Elite Model"),
                ('5', "Engineer", "Engineer Model"),
                ('6', "Flood Captain", "Flood Captain Model"),
                ('7', "Flood Carrier", "Flood Carrier Model"),
                ('8', "Flood Combat Elite", "Flood Combat Elite Model"),
                ('9', "Flood Combat Human", "Flood Combat Human Model"),
                ('10', "Flood Infection", "Flood Infection Model"),
                ('11', "Grunt", "Grunt Model"),
                ('12', "Hunter", "Hunter Model"),
                ('13', "Jackal", "Jackal Model"),
                ('14', "Marine", "Marine Model"),
                ('15', "Marine Armored", "Marine Armored Model"),
                ('16', "Monitor", "Monitor Model"),
                ('17', "Pilot", "Pilot Model"),
                ('18', "Sentinel", "Sentinel Model"),
               ]
        )

    halo_one_scale_model_vehi: EnumProperty(
        name="Halo 1 Vehicle Models:",
        description="What model to create",
        items=[
                ('19', "Banshee", "Banshee Model"),
                ('20', "Covenant Gun Turret", "Covenant Gun Turret Model"),
                ('21', "Covenant Dropship", "Covenant Dropship Model"),
                ('22', "Fighter Bomber", "Fighter Bomber Model"),
                ('23', "Ghost", "Ghost Model"),
                ('24', "Lifepod", "Lifepod Model"),
                ('25', "Lifepod Entry", "Lifepod Entry Model"),
                ('26', "Pelican", "Pelican Model"),
                ('27', "Rocket Warthog", "Rocket Warthog Model"),
                ('28', "Scorpion", "Scorpion Model"),
                ('29', "Warthog", "Warthog Model"),
                ('30', "Wraith", "Wraith Model"),
               ]
        )

    halo_two_scale_model_char: EnumProperty(
        name="Halo 2 Character Models:",
        description="What model to create",
        items=[
                ('0', "Arbiter", "Arbiter Model"),
                ('1', "Brute", "Brute Model"),
                ('2', "Bugger", "Bugger Model"),
                ('3', "Cortana", "Cortana Model"),
                ('4', "Elite", "Elite Model"),
                ('5', "Elite Heretic", "Elite Heretic Model"),
                ('6', "Elite Ranger", "Elite Ranger Model"),
                ('7', "Flood Carrier", "Flood Carrier Model"),
                ('8', "Flood Combat Elite", "Flood Combat Elite Model"),
                ('9', "Flood Combat Human", "Flood Combat Human Model"),
                ('10', "Flood Infection", "Flood Infection Model"),
                ('11', "Flood Juggernaut", "Flood Juggernaut Model"),
                ('12', "Gravemind", "Gravemind Model"),
                ('13', "Grunt", "Grunt Model"),
                ('14', "Grunt Heretic", "Grunt Heretic Model"),
                ('15', "Hunter", "Hunter Model"),
                ('16', "Jackal", "Jackal Model"),
                ('17', "Lord Hood", "Lord Hood Model"),
                ('18', "Master Chief", "Master Chief Model"),
                ('19', "Marine", "Marine Model"),
                ('20', "Marine ODST", "Marine ODST Model"),
                ('21', "Miranda", "Miranda Model"),
                ('22', "Monitor", "Monitor Model"),
                ('23', "Prophet Mercy", "Prophet Mercy Model"),
                ('24', "Prophet Minor", "Prophet Minor Model"),
                ('25', "Prophet Regret", "Prophet Regret Model"),
                ('26', "Prophet Truth", "Prophet Truth Model"),
                ('27', "Sentinel Aggressor", "Sentinel Aggressor Model"),
                ('28', "Sentinel Constructor", "Sentinel Constructor Model"),
                ('29', "Sentinel Enforcer", "Sentinel Enforcer Model"),
               ]
        )

    halo_two_scale_model_vehi: EnumProperty(
        name="Halo 2 Vehicle Models:",
        description="What model to create",
        items=[
                ('30', "Banshee", "Banshee Model"),
                ('31', "Covenant AP Turret", "Covenant AP Turret Model"),
                ('32', "Falcon", "Falcon Model"),
                ('33', "Ghost", "Ghost Model"),
                ('34', "Gravity Throne", "Gravity Throne Model"),
                ('35', "Human AP Turret", "Human AP Turret Model"),
                ('36', "Insertion Pod", "Insertion Pod Model"),
                ('37', "Longsword", "Longsword Model"),
                ('38', "Pelican", "Pelican Model"),
                ('39', "Phantom", "Phantom Model"),
                ('40', "Scorpion", "Scorpion Model"),
                ('41', "Shadow", "Shadow Model"),
                ('42', "Spectre", "Spectre Model"),
                ('43', "Warthog", "Warthog Model"),
                ('44', "Wraith", "Wraith Model"),
               ]
        )

    halo_three_scale_model_char: EnumProperty(
        name="Halo 3 Character Models:",
        description="What model to create",
        items=[
                ('0', "Arbiter", "Arbiter Model"),
                ('1', "Brute", "Brute Model"),
                ('2', "Bugger", "Bugger Model"),
                ('3', "Cortana", "Cortana Model"),
                ('4', "Elite", "Elite Model"),
                ('5', "Flood Carrier", "Flood Carrier Model"),
                ('6', "Flood Combat Brute", "Flood Combat Brute Model"),
                ('7', "Flood Combat Elite", "Flood Combat Elite Model"),
                ('8', "Flood Combat Human", "Flood Combat Human Model"),
                ('9', "Flood Infection", "Flood Infection Model"),
                ('10', "Flood Ranged", "Flood Ranged Model"),
                ('11', "Flood Stalker", "Flood Stalker Model"),
                ('12', "Flood Tank", "Flood Tank Model"),
                ('13', "Grunt", "Grunt Model"),
                ('14', "Hunter", "Hunter Model"),
                ('15', "Jackal", "Jackal Model"),
                ('16', "Lord Hood", "Lord Hood Model"),
                ('17', "Master Chief", "Master Chief Model"),
                ('18', "Marine", "Marine Model"),
                ('19', "Marine ODST", "Marine ODST Model"),
                ('20', "Miranda", "Miranda Model"),
                ('21', "Monitor", "Monitor Model"),
                ('22', "Prophet Truth", "Prophet Truth Model"),
                ('23', "Sentinel Aggressor", "Sentinel Aggressor Model"),
                ('24', "Sentinel Constructor", "Sentinel Constructor Model"),
                ('25', "Worker", "Worker Model"),
               ]
        )

    halo_three_scale_model_vehi: EnumProperty(
        name="Halo 3 Vehicle Models:",
        description="What model to create",
        items=[
                ('26', "Banshee", "Banshee Model"),
                ('27', "Chopper", "Chopper Model"),
                ('28', "Covenant Capital Ship", "Covenant Capital Ship Model"),
                ('29', "Covenant Cruiser", "Covenant Cruiser Model"),
                ('30', "Flood Cruiser", "Flood Cruiser Model"),
                ('31', "Ghost", "Ghost Model"),
                ('32', "Gravity Throne", "Gravity Throne Model"),
                ('33', "Hornet", "Hornet Model"),
                ('34', "Insertion Pod", "Insertion Pod Model"),
                ('35', "Longsword", "Longsword Model"),
                ('36', "Prowler", "Prowler Model"),
                ('37', "Mongoose", "Mongoose Model"),
                ('38', "Pelican", "Pelican Model"),
                ('39', "Phantom", "Phantom Model"),
                ('40', "Scorpion", "Scorpion Model"),
                ('41', "Shade", "Shade Model"),
                ('42', "Warthog", "Warthog Model"),
                ('43', "Wraith", "Wraith Model"),
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
        layout = self.layout

class Halo_Lightmapper(Panel):
    bl_label = "Lightmap Helper"
    bl_idname = "HALO_PT_Lightmapper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo_lightmapper = scene.halo_lightmapper

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Image Width:')
        row.prop(scene_halo_lightmapper, "res_x", text='')
        row = col.row()
        row.label(text='Image Height:')
        row.prop(scene_halo_lightmapper, "res_y", text='')
        row = col.row()
        row.operator("halo_bulk.lightmapper_images", text="Generate Lightmap Images")

class Halo_BoneNameHelper(Panel):
    bl_label = "Bone Name Helper"
    bl_idname = "HALO_PT_BoneNameHelper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        row = col.row()
        row.operator("halo_bulk.bulk_bone_names", text="Rename Bones Halo/Blender Style")

class Halo_NodePrefixHelper(Panel):
    bl_label = "Node Prefix Helper"
    bl_idname = "HALO_PT_NodePrefixHelper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo_prefix = scene.halo_prefix

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Prefix:')
        row.prop(scene_halo_prefix, "prefix_string", text='')
        row = col.row()
        row.operator("halo_bulk.bulk_node_prefix", text="Set Halo Node Pefix")

class Halo_BoneRotationHelper(Panel):
    bl_label = "Bone Rotation Helper"
    bl_idname = "HALO_PT_BoneRotationHelper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        row = col.row()
        row.operator("halo_bulk.bulk_bone_rotation", text="Invert Bone Roll")
        row = col.row()
        row.operator("halo_bulk.bulk_bone_reset", text="Reset Bone Rotation")

class Halo_CullMaterials(Panel):
    bl_label = "Cull Materials"
    bl_idname = "HALO_PT_CullMaterials"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        row = col.row()
        row.operator("halo_bulk.cull_materials", text="Cull Materials")

class Halo_ScaleModelHelper(Panel):
    bl_label = "Scale Model Helper"
    bl_idname = "HALO_PT_ScaleModelHelper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_scale_model = scene.scale_model

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Game:')
        row.prop(scene_scale_model, "game_version", text="")
        row = col.row()
        row.label(text='Unit Type:')
        row.prop(scene_scale_model, "unit_type", text="")
        row = col.row()
        row.label(text='Model:')
        if scene_scale_model.game_version == "haloce":
            if scene_scale_model.unit_type == "character":
                row.prop(scene_scale_model, "halo_one_scale_model_char", text="")

            else:
                row.prop(scene_scale_model, "halo_one_scale_model_vehi", text="")

        elif scene_scale_model.game_version == "halo2":
            if scene_scale_model.unit_type == "character":
                row.prop(scene_scale_model, "halo_two_scale_model_char", text="")

            else:
                row.prop(scene_scale_model, "halo_two_scale_model_vehi", text="")

        else:
            if scene_scale_model.unit_type == "character":
                row.prop(scene_scale_model, "halo_three_scale_model_char", text="")

            else:
                row.prop(scene_scale_model, "halo_three_scale_model_vehi", text="")

        row = col.row()
        row.operator("halo_bulk.scale_model", text="Generate Scale Model")

class Halo_MaterialDefinitionHelper(Panel):
    bl_label = "Material Definition Helper"
    bl_idname = "HALO_PT_MaterialDefinitionHelper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo_face_set = scene.halo_face_set

        col = layout.column(align=True)
        row = col.row()
        row.label(text='LOD:')
        row.prop(scene_halo_face_set, "level_of_detail", text='')
        row = col.row()
        row.label(text='Permutation:')
        row.prop(scene_halo_face_set, "permutation_string", text='')
        row = col.row()
        row.label(text='Region:')
        row.prop(scene_halo_face_set, "region_string", text='')
        row = col.row()
        row.label(text='Apply to active object:')
        row.prop(scene_halo_face_set, "set_facemap", text='')
        row = col.row()
        row.operator("halo_bulk.face_set", text="Generate Facemap")

class Halo_ImportFixup(Panel):
    bl_label = "Import Fixup"
    bl_idname = "HALO_PT_ImportFixup"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo_fixup = scene.halo_import_fixup

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Merge Distance:')
        row.prop(scene_halo_fixup, "threshold", text='')
        row = col.row()
        row.operator("halo_bulk.import_fixup", text="Import Fixup")

class Halo_IKHelper(Panel):
    bl_label = "IK Helper"
    bl_idname = "HALO_PT_IKHelper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        row = col.row()
        row.operator("ik_prep.move_objects", text="IK prep")

class Halo_MultiUserHelper(Panel):
    bl_label = "Multi User Helper"
    bl_idname = "HALO_PT_MultiUserHelper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        row = col.row()
        row.operator("apply_instance_transform.set_transform", text="Set Transform")

class Halo_BatchAnimConverter(Panel):
    bl_label = "Batch Anim Converter"
    bl_idname = "HALO_PT_BatchAnimConverter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo = scene.halo
        scene_halo_anim_batch = scene.halo_anim_batch

        col = layout.column(align=True)
        row = col.row()
        row.operator(JMA_BatchDialog.bl_idname, text="Select Directory")
        row.prop(scene_halo_anim_batch, "directory", text='')
        row = col.row()
        row.label(text="Game Version:")
        row.prop(scene_halo_anim_batch, "game_version", text='')
        if scene_halo.expert_mode:
            row = col.row()
            row.label(text='JMA Version:')
            if scene_halo_anim_batch.game_version == 'haloce':
                row.prop(scene_halo_anim_batch, "jma_version_ce", text='')

            elif scene_halo_anim_batch.game_version == 'halo2':
                row.prop(scene_halo_anim_batch, "jma_version_h2", text='')

            elif scene_halo_anim_batch.game_version == 'halo3mcc':
                row.prop(scene_halo_anim_batch, "jma_version_h3", text='')

        row = col.row()
        row.operator("halo_bulk.anim_convert", text="Convert Directory")

class Halo_Sky_Tools_Helper(Panel):
    """Tools to help automate Halo workflow"""
    bl_label = "Halo Sky Tools Helper"
    bl_idname = "HALO_PT_SkyTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Halo Sky Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("halo_bulk.generate_sky", text="Generate Sky")

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
        from ..misc import lightmapper_prep
        scene_halo_lightmapper = context.scene.halo_lightmapper
        return global_functions.run_code("lightmapper_prep.lightmap_bulk(context, scene_halo_lightmapper.res_x, scene_halo_lightmapper.res_y)")

class Bulk_Rename_Bones(Operator):
    """Rename all bones in the scene to swap from Blender .L/.R to Halo l/r bone naming scheme and vice versa"""
    bl_idname = 'halo_bulk.bulk_bone_names'
    bl_label = 'Bulk Halo Bones Names'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import rename_bones
        return global_functions.run_code("rename_bones.rename_bones(context)")

class Bulk_Rename_Prefix(Operator):
    """Rename prefixes for selected objects in the scene"""
    bl_idname = 'halo_bulk.bulk_node_prefix'
    bl_label = 'Bulk Halo Node Prefix'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import rename_prefix
        scene_halo_prefix = context.scene.halo_prefix
        return global_functions.run_code("rename_prefix.rename_prefix(context, scene_halo_prefix.prefix_string)")

class Bulk_Rotate_Bones(Operator):
    """Add -180 degrees for the roll of all selected bones in edit mode"""
    bl_idname = 'halo_bulk.bulk_bone_rotation'
    bl_label = 'Bulk Halo Bones Rotate'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import rotate_bones
        return global_functions.run_code("rotate_bones.rotate_bones(context)")

class Bulk_Reset_Bones(Operator):
    """Resets bone rotation of all selected bones in edit mode"""
    bl_idname = 'halo_bulk.bulk_bone_reset'
    bl_label = 'Bulk Halo Bones Reset'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import rotate_bones
        return global_functions.run_code("rotate_bones.reset_bones(context)")

class Cull_Materials(Operator):
    """Sets unused material slots to none for the selected object"""
    bl_idname = 'halo_bulk.cull_materials'
    bl_label = 'Cull Materials'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import cull_materials
        return global_functions.run_code("cull_materials.cull_materials(context)")

class Scale_Model(Operator):
    """Creates a model that matches the ingame scale"""
    bl_idname = 'halo_bulk.scale_model'
    bl_label = 'Scale Model'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import scale_models
        scene = context.scene
        scene_scale_model = scene.scale_model
        halo_1_unit_index = 0
        halo_2_unit_index = 0
        halo_3_unit_index = 0

        if scene_scale_model.game_version == "haloce":
            if scene_scale_model.unit_type == "character":
                halo_1_unit_index = scene_scale_model.halo_one_scale_model_char
            else:
                halo_1_unit_index = scene_scale_model.halo_one_scale_model_vehi


        elif scene_scale_model.game_version == "halo2":
            if scene_scale_model.unit_type == "character":
                halo_2_unit_index = scene_scale_model.halo_two_scale_model_char
            else:
                halo_2_unit_index = scene_scale_model.halo_two_scale_model_vehi

        elif scene_scale_model.game_version == "halo3":
            if scene_scale_model.unit_type == "character":
                halo_3_unit_index = scene_scale_model.halo_three_scale_model_char
            else:
                halo_3_unit_index = scene_scale_model.halo_three_scale_model_vehi

        return global_functions.run_code("scale_models.create_model(context, scene_scale_model.game_version, halo_1_unit_index, halo_2_unit_index, halo_3_unit_index)")

class GenerateSky(Operator):
    """Generates a hemisphere shaped set of skylights for Halo 3 sky models"""
    bl_idname = 'halo_bulk.generate_sky'
    bl_label = 'Sky'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import generate_sky
        scene_halo_sky = context.scene.halo_sky
        return global_functions.run_code("generate_sky.generate_sky(context, self.report, scene_halo_sky.longitude_slices, scene_halo_sky.lattitude_slices, scene_halo_sky.dome_radius, scene_halo_sky.horizontal_fov, scene_halo_sky.vertical_fov, scene_halo_sky.sky_type, scene_halo_sky.cie_sky_number, scene_halo_sky.hdr_map, scene_halo_sky.haze_height, scene_halo_sky.luminance_only, scene_halo_sky.dome_intensity, scene_halo_sky.override_zenith_color, scene_halo_sky.zenith_color, scene_halo_sky.override_horizon_color, scene_halo_sky.horizon_color, scene_halo_sky.sun_altittude, scene_halo_sky.sun_heading, scene_halo_sky.sun_intensity, scene_halo_sky.sun_disc_size, scene_halo_sky.windowing, scene_halo_sky.override_sun_color, scene_halo_sky.sun_color, scene_halo_sky.air_cleaness, scene_halo_sky.exposure, scene_halo_sky.clamp_colors)")

class ExportLightmap(Operator, ExportHelper):
    """Write a LUV file"""
    bl_idname = "export_luv.export"
    bl_label = "Export LUV"
    filename_ext = '.LUV'

    def execute(self, context):
        from ..misc import export_lightmap

        return global_functions.run_code("export_lightmap.write_file(self.filepath, self.report)")

class FaceSet(Operator):
    """Create a facemap with a permutation and a region"""
    bl_idname = "halo_bulk.face_set"
    bl_label = "Create a Facemap"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import face_set
        scene_face_set = context.scene.halo_face_set

        return global_functions.run_code("face_set.create_facemap(context, scene_face_set.level_of_detail, scene_face_set.permutation_string, scene_face_set.region_string, scene_face_set.set_facemap)")

class ImportFixup(Operator):
    """Attempt to automatically convert custom normals to sharp edges. Will probably need some manual cleanup afterwards"""
    bl_idname = "halo_bulk.import_fixup"
    bl_label = "Convert custom normals to sharp edges"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import import_fixup
        scene_halo_fixup = context.scene.halo_import_fixup
        return global_functions.run_code("import_fixup.model_fixup(context, scene_halo_fixup.threshold)")

class Bulk_IK_Prep(Operator):
    """Moves selected objects to the head position of a bone with the same object name in a selected armature"""
    bl_idname = 'ik_prep.move_objects'
    bl_label = 'Bulk Halo IK Prep'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import ik_prep
        return global_functions.run_code("ik_prep.move_objects(context)")

class Bulk_Set_Transform(Operator):
    """Apply scale on multi user objects"""
    bl_idname = 'apply_instance_transform.set_transform'
    bl_label = 'Bulk Set Transform'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import apply_instance_transform
        return global_functions.run_code("apply_instance_transform.set_transform(context)")

class Bulk_Anim_Convert(Operator):
    """Convert a whole directory of animation source files from one game to another"""
    bl_idname = 'halo_bulk.anim_convert'
    bl_label = 'Bulk Anim Convert'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import batch_anims
        scene_halo_anim_batch = context.scene.halo_anim_batch

        return global_functions.run_code("batch_anims.write_file(context, self.report, scene_halo_anim_batch.directory, scene_halo_anim_batch.jma_version, scene_halo_anim_batch.jma_version_ce, scene_halo_anim_batch.jma_version_h2, scene_halo_anim_batch.jma_version_h3, scene_halo_anim_batch.game_version)")

def menu_func_export(self, context):
    self.layout.operator(ExportLightmap.bl_idname, text="Halo Lightmap UV (.luv)")

classeshalo = (
    JMA_BatchDialog,
    ExportLightmap,
    Bulk_Lightmap_Images,
    Bulk_Rename_Bones,
    Bulk_Rename_Prefix,
    Bulk_Rotate_Bones,
    Bulk_Reset_Bones,
    Cull_Materials,
    Scale_Model,
    GenerateSky,
    FaceSet,
    ImportFixup,
    Bulk_IK_Prep,
    Bulk_Anim_Convert,
    Bulk_Set_Transform,
    Halo_Tools_Helper,
    Halo_Lightmapper,
    Halo_BoneNameHelper,
    Halo_NodePrefixHelper,
    Halo_BoneRotationHelper,
    Halo_CullMaterials,
    Halo_ScaleModelHelper,
    Halo_MaterialDefinitionHelper,
    Halo_ImportFixup,
    Halo_IKHelper,
    Halo_MultiUserHelper,
    Halo_BatchAnimConverter,
    Halo_Sky_Tools_Helper,
    Halo_Sky_Dome,
    Halo_Sky_Light,
    Halo_Sky_Zenith_Color,
    Halo_Sky_Horizon_Color,
    Halo_Sky_Sun_Light,
    Halo_Sky_Sun_Color,
    Halo_Sky_Misc_Settings,
    JMA_BatchPropertiesGroup,
    Halo_ImportFixupPropertiesGroup,
    Halo_LightmapperPropertiesGroup,
    Scale_ModelPropertiesGroup,
    SkyPropertiesGroup,
    Halo_PrefixPropertiesGroup,
    Face_SetPropertiesGroup
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.Scene.halo_import_fixup = PointerProperty(type=Halo_ImportFixupPropertiesGroup, name="Halo Import Helper", description="Set properties for the import fixup helper")
    bpy.types.Scene.halo_lightmapper = PointerProperty(type=Halo_LightmapperPropertiesGroup, name="Halo Lightmapper Helper", description="Set properties for the lightmapper")
    bpy.types.Scene.halo_prefix = PointerProperty(type=Halo_PrefixPropertiesGroup, name="Halo Prefix Helper", description="Set properties for node prefixes")
    bpy.types.Scene.scale_model = PointerProperty(type=Scale_ModelPropertiesGroup, name="Halo Scale Model Helper", description="Create meshes for scale")
    bpy.types.Scene.halo_sky = PointerProperty(type=SkyPropertiesGroup, name="Sky Helper", description="Generate a sky for Halo 3")
    bpy.types.Scene.halo_face_set = PointerProperty(type=Face_SetPropertiesGroup, name="Halo Face Set Helper", description="Creates a facemap with the exact name we need")
    bpy.types.Scene.halo_anim_batch = PointerProperty(type=JMA_BatchPropertiesGroup, name="Halo Batch Anims", description="Converts all animations in a specific directory to a different version.")

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    del bpy.types.Scene.halo_import_fixup
    del bpy.types.Scene.halo_lightmapper
    del bpy.types.Scene.halo_prefix
    del bpy.types.Scene.scale_model
    del bpy.types.Scene.halo_sky
    del bpy.types.Scene.halo_face_set
    del bpy.types.Scene.halo_anim_batch
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
