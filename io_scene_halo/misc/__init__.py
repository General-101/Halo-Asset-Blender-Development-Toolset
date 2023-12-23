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

def version_settings_callback(self, context):
    items=[ ('16390', "16390", "CE/H2/H3"),
            ('16391', "16391", "CE/H2/H3"),
            ('16392', "16392", "CE/H2/H3"),
        ]

    if not self.game_title == "halo1":
            items.append(('16393', "16393", "H2/H3"))
            items.append(('16394', "16394", "H2/H3"))
            items.append(('16395', "16395", "H2/H3"))

    return items

def update_version(self, context):
    if self.game_title == "halo1":
        self.jma_version = '16392'

    else:
        self.jma_version = '16395'

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

class Generate_Tag_Dialog(Operator):
    """Select the source file to read data from"""
    bl_idname = "import_scene.generate_tag"
    bl_label = "Select Source"

    filepath: StringProperty(
        name="Upgrade Patches Filepath",
        description="The filepath to the patches we wish to use",
    )

    def execute(self, context):
        scene = context.scene
        scene_halo_scenario = scene.halo_scenario
        scene_halo_scenario.input_file = self.filepath
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class Generate_Tag_Patches_Dialog(Operator):
    """Select the upgrade patches file to use during the upgrade process"""
    bl_idname = "import_scene.generate_tag_patches"
    bl_label = "Select Patches"

    filter_glob: StringProperty(
        default="*.txt",
        options={'HIDDEN'},
        )

    filepath: StringProperty(
        name="Source Filepath",
        description="The filepath to the source we wish to use",
    )

    def execute(self, context):
        scene = context.scene
        scene_halo_scenario = scene.halo_scenario
        scene_halo_scenario.upgrade_patches = self.filepath
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class H3EK_PathDialog(Operator):
    """Set H3EK"""
    bl_idname = "import_scene.h3ek_path"
    bl_label = "Set H3EK Directory"

    filter_glob: StringProperty(
        default="*.exe",
        options={'HIDDEN'},
        )

    directory: StringProperty(
        name="Directory",
        description="The H3EK Directory",
    )

    def execute(self, context):
        scene = context.scene
        scene_halo_h3ek_path = scene.halo_h3ek_path
        scene_halo_h3ek_path.directory = self.directory
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class H3EK_DataPathDialog(Operator):
    """Set H3EK"""
    bl_idname = "import_scene.h3ek_data_path"
    bl_label = "Set H3EK Data Directory"

    filter_glob: StringProperty(
        default="*.exe",
        options={'HIDDEN'},
        )

    directory: StringProperty(
        name="Directory",
        description="The H3EK Data Directory",
    )

    def execute(self, context):
        scene = context.scene
        scene_halo_h3ek_data_path = scene.halo_h3ek_data_path
        scene_halo_h3ek_data_path.directory = self.directory
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class Halo_MaterialPropertiesGroup(PropertyGroup):
    set_mattype: BoolProperty(
        name ="Set Material Type",
        description = "Sets the material type of the materials in the selected object",
        default = False,
    )

    mat_types: EnumProperty(
        name="Material Types:",
        description="What material type to use for the materials in the object",
        items=[ ('two_sided', "Two Sided", "Two Sided"),
                ('render_only', "Render Only", "Render Only"),
                ('collision_only', "Collision Only", "Collision Only"),
                ('sphere_collision_only', "Large Collideable", "Large Collideable"),
                ('transparent_1_sided', "One-Sided Transparent", "One-Sided Transparent"),
                ('transparent_2_sided', "Two-Sided Transparent", "Two-Sided Transparent"),
                ('slip_surface', "Slip Surface", "Slip Surface"),
                ('group_transparents_by_plane', "Group Transparents by Plane", "Group Transparents by Plane"),
                ('fog_plane', "Fog Plane", "Fog Plane"),
                ('water_surface', "Water Surface", "Water Surface"),
                ('breakable', "Breakable", "Breakable"),
                ('conveyor', "Conveyor", "Conveyor"),
                ('ladder', "Ladder", "Ladder"),
                ('decal_offset', "Decal Offset", "Decal Offset"),
                ('ai_deafening', "AI Deafening", "AI Deafening"),
                ('blocks_sound', "Blocks Sound", "Blocks Sound"),
                ('no_shadow', "No Shadow", "No Shadow"),
                ('shadow_only', "Shadow Only", "Shadow Only"),
                ('lightmap_only', "Lightmap Only", "Lightmap Only"),
                ('ignored_by_lightmaps', "Ignored by Lightmaps", "Ignored by Lightmaps"),
                ('precise', "Precise", "Precise"),
                ('portal_exact', "Portal Exact", "Portal Exact"),
                ('portal_1_way', "One Way Portal", "One Way Portal"),
                ('portal_door', "Portal Door", "Portal Door"),
                ('portal_vis_blocker', "Portal Visibility Blocker", "Portal Visibility Blocker"),
               ]
        )

class JMA_BatchPropertiesGroup(PropertyGroup):
    jma_version: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        options={'HIDDEN'},
        items=version_settings_callback,
        default=2
        )

    game_title: EnumProperty(
        name="Game Title:",
        description="What game will the model file be used for",
        items=[ ('halo1', "Halo 1", "Export an animation intended for Halo 1"),
                ('halo2', "Halo 2", "Export an animation intended for Halo 2"),
                ('halo3', "Halo 3", "Export an animation intended for Halo 3"),
            ],
        update = update_version
        )

    directory: StringProperty(
        name="Directory",
        description="A directory containing animation source files to convert",
        )

class Source_PropertiesGroup(PropertyGroup):
    source_game_title: EnumProperty(
        name="Game:",
        description="What game to target",
        items=[ ('halo1', "Halo 1", "Source is from Halo 1 MCC"),
                ('halo2', "Halo 2", "Source is from Halo 2 MCC"),
                ('halo3', "Halo 3", "Source is from Halo 3 MCC"),
            ]
        )

    target_game_title: EnumProperty(
        name="Game:",
        description="What game to target",
        items=[ ('halo1', "Halo 1", "Generate a tag intended for Halo 1 MCC"),
                ('halo2', "Halo 2", "Generate a tag intended for Halo 2 MCC"),
                ('halo3', "Halo 3", "Generate a tag intended for Halo 3 MCC"),
            ]
        )

    input_file: StringProperty(
        name="Source",
        description="A source file to load and convert to a tag",
        )

    upgrade_patches: StringProperty(
        name="Upgrade Patches",
        description="A text file containing paths to replace during a scenario upgrade",
        )

class LevelProprtiesGroup(PropertyGroup):
    game_title: EnumProperty(
        name="Game:",
        description="What game to target",
        items=[ ('h1', "Halo 1", "Generate a tag intended for Halo 1 MCC"),
                ('h2', "Halo 2", "Generate a tag intended for Halo 2 MCC"),
            ]
        )

    level_seed: IntProperty(
        name="Seed",
        description="Set the seed for the generator. System time will be used if nothing is set",
    )

    level_theme: EnumProperty(
        name="Theme",
        description="What theme to use for the level geometry",
        items=[ ('human', "Human", "Generate a human themed level"),
                ('covenant', "Covenant", "Generate a Covenant themed level"),
                ('forerunner', "Forerunner", "Generate a Forerunner themed level"),
            ]
        )

    level_damage: EnumProperty(
        name="Level Damage",
        description="How much damage has the level gone through. Will determine decals and level pieces used",
        items=[ ('0', "None", "Pristine and ready for ruination"),
                ('1', "Small", "Someone might have had a heated argument in the breakroom"),
                ('2', "Medium", "Bit of a trash heap."),
                ('3', "Large", "Someone has been here before you and they most certainly had their fun."),
            ]
        )

    level_goal: EnumProperty(
        name="Goal",
        description="What are you trying to achieve? Where do you see yourself 5 years from now",
        items=[ ('0', "Reclaimer", "There's an artifact at the location. Recover it and use it against your foes"),
                ('1', "Defense", "There is a location or squad of great importance. Secure it"),
                ('2', "Attack", "There is a location or squad of great importance. Destroy it"),
            ]
        )

    player_biped: EnumProperty(
        name="Player Biped",
        description="Are we Master Chief or the Arbiter",
        items=[ ('0', "Masterchief", "We are allied with human and separatists characters"),
                ('1', "Arbiter", "We are allied with the Covenant or human and separatists"),
            ]
        )

    level_conflict: EnumProperty(
        name="Conflict",
        description="Who is our friend? Who is our foe?",
        items=[ ('0', "Standard", "Unified Covenant"),
                ('1', "Schism", "The Covenant are in a civil war. Brutes will be fighting elites"),
                ('2', "Separatists", "Humans and separatists against the Covenant"),
            ]
        )

    mutator_random_weapons: BoolProperty(
        name ="Mutator Random Weapons",
        description = "Recieve a random loadout every couple of seconds. Make due with what you get",
        default = False,
    )

    mutator_extended_family: BoolProperty(
        name ="Mutator Extended Family",
        description = "Only one unit. Will you get all hunters? I hope so",
        default = False,
    )

    maze_height: IntProperty(
        name="Maze Height",
        description="Set the height of the maze",
        default=8,
        min=4,
    )

    maze_width: IntProperty(
        name="Maze Height",
        description="Set the width of the maze",
        default=8,
        min=4,
    )

    output_directory: StringProperty(
            name = "Scenario Output",
            description="Where to place the generated scenario file for this level",
            default="",
            maxlen=1024,
            subtype='DIR_PATH'
    )

class Halo_H3EKPropertiesGroup(PropertyGroup):
    directory: StringProperty(
        name="Directory",
        description="The H3EK Directory",
        )
    datadirectory: StringProperty(
        name="Data Directory",
        description="The H3EK Data Directory",
        )

class Halo_ImportFixupPropertiesGroup(PropertyGroup):
    threshold: FloatProperty(
        name="Threshold",
        description="Maximum distance between elements to merge",
        default=0.0001,
        min=0.000001,
        max=50.0
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
        items=[ ('halo1', "Halo 1", "Models from CE only"),
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

class Halo_RandomMaterialColors(Panel):
    bl_label = "Random Material Colors"
    bl_idname = "HALO_PT_RandomMaterialColors"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        row = col.row()
        row.operator("halo_bulk.random_material_colors", text="Set Colors")

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
        if scene_scale_model.game_version == "halo1":
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
        row.prop(scene_halo_anim_batch, "game_title", text='')
        if scene_halo.expert_mode:
            row = col.row()
            row.label(text='JMA Version:')
            row.prop(scene_halo_anim_batch, "jma_version", text='')

        row = col.row()
        row.operator("halo_bulk.anim_convert", text="Convert Directory")

class Halo_GenerateTag(Panel):
    bl_label = "Generate Tag"
    bl_idname = "HALO_PT_GenerateTag"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo_scenario = scene.halo_scenario

        col = layout.column(align=True)
        row = col.row()
        row.operator(Generate_Tag_Dialog.bl_idname, text="Select Source")
        row.prop(scene_halo_scenario, "input_file", text='')

        row = col.row()
        row.operator(Generate_Tag_Patches_Dialog.bl_idname, text="Select Patches")
        row.prop(scene_halo_scenario, "upgrade_patches", text='')

        row = col.row()
        row.label(text="Source Game Title:")
        row.prop(scene_halo_scenario, "source_game_title", text='')

        row = col.row()
        row.label(text="Target Game Title:")
        row.prop(scene_halo_scenario, "target_game_title", text='')

        row = col.row()
        row.operator("halo_bulk.generate_tag", text="Generate Tag")

class Halo_GenerateLevel(Panel):
    bl_label = "Generate Level"
    bl_idname = "HALO_PT_GenerateLevel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo_maze = scene.halo_maze

        col = layout.column(align=True)
        row = col.row()
        row.label(text="Source Game Title:")
        row.prop(scene_halo_maze, "game_title", text='')
        row = col.row()
        row.label(text="Level Seed:")
        row.prop(scene_halo_maze, "level_seed", text='')
        row = col.row()
        row.label(text="Level Theme:")
        row.prop(scene_halo_maze, "level_theme", text='')
        row = col.row()
        row.label(text="Level Damage:")
        row.prop(scene_halo_maze, "level_damage", text='')
        row = col.row()
        row.label(text="Level Goal:")
        row.prop(scene_halo_maze, "level_goal", text='')
        row = col.row()
        row.label(text="Level Conflict:")
        row.prop(scene_halo_maze, "level_conflict", text='')
        row = col.row()
        row.label(text="Player Biped:")
        row.prop(scene_halo_maze, "player_biped", text='')
        row = col.row()
        row.label(text="Mutator Random Weapons:")
        row.prop(scene_halo_maze, "mutator_random_weapons", text='')
        row = col.row()
        row.label(text="Mutator Extended Family:")
        row.prop(scene_halo_maze, "mutator_extended_family", text='')
        row = col.row()
        row.label(text="Maze Height:")
        row.prop(scene_halo_maze, "maze_height", text='')
        row = col.row()
        row.label(text="Maze Width:")
        row.prop(scene_halo_maze, "maze_width", text='')
        row = col.row()
        row.label(text="Output Directory:")
        row.prop(scene_halo_maze, "output_directory", text='')

        row = col.row()
        row.operator("halo_bulk.generate_level", text="Generate Level")

class Halo_MatTools(Panel):
    bl_label = "Halo Material Tools"
    bl_idname = "HALO_PT_MatTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        from ..misc import mattools
        layout = self.layout
        scene = context.scene
        scene_halo = scene.halo
        scene_halo_h3ek_path = scene.halo_h3ek_path
        scene_halo_h3ek_data_path = scene.halo_h3ek_data_path
        scene_halo_mattype = scene.halo_mattype
        col = layout.column(align=True)
        row = col.row()
        row.operator(H3EK_PathDialog.bl_idname, text="Select H3EK Directory")
        row.prop(scene_halo_h3ek_path, "directory", text='')
        row = col.row()
        row.operator(H3EK_DataPathDialog.bl_idname, text="Select Data Directory")
        row.prop(scene_halo_h3ek_data_path, "directory", text='')
        row = col.row()
        row.operator(Export_Textures.bl_idname, text="Export Textures")
        row = col.row()
        row.operator(Make_Bitmaps.bl_idname, text="Make Bitmaps")
        row = col.row()
        row.label(text='Set Material Type')
        row.prop(scene_halo_mattype, "mat_types", text='')
        row = col.row()
        row.operator(Set_Material_Type.bl_idname, text='Apply Material Type')
        row = col.row()
        row.operator(Enable_Material_Type.bl_idname, text='Toggle Usage of Material Types')

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

class Random_Material_Colors(Operator):
    """Sets materials to use a random diffuse"""
    bl_idname = 'halo_bulk.random_material_colors'
    bl_label = 'Random Material Colors'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import random_material_colors
        return global_functions.run_code("random_material_colors.random_material_colors(context)")

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

        if scene_scale_model.game_version == "halo1":
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

class GenerateLevel(Operator):
    """Generates a level"""
    bl_idname = 'halo_bulk.generate_level'
    bl_label = 'Generate Level'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import generate_level
        scene_maze = context.scene.halo_maze

        return global_functions.run_code("generate_level.generate_level(context, scene_maze.game_title, scene_maze.level_seed, scene_maze.level_theme, scene_maze.level_damage, scene_maze.level_goal, scene_maze.player_biped, scene_maze.level_conflict, scene_maze.mutator_random_weapons, scene_maze.mutator_extended_family, scene_maze.maze_height, scene_maze.maze_width, scene_maze.output_directory, self.report)")

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
        jma_version = int(scene_halo_anim_batch.jma_version)

        return global_functions.run_code("batch_anims.write_file(context, self.report, scene_halo_anim_batch.directory, jma_version, scene_halo_anim_batch.game_title)")

class Export_Textures(Operator):
    """Exports Textures for the selected object"""
    bl_idname = 'halo_mattools.export_texture'
    bl_label = 'Export Textures'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import mattools
        scene = context.scene
        scene_halo_h3ek_data_path = scene.halo_h3ek_data_path

        return global_functions.run_code("mattools.export_texture(context, scene_halo_h3ek_data_path.directory)")

class Make_Bitmaps(Operator):
    """Make Bitmaps out of Tifs in Working Data Directory"""
    bl_idname = 'halo_mattools.make_bitmaps'
    bl_label = 'Make Bitmaps'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import mattools
        scene = context.scene
        scene_halo_h3ek_data_path = scene.halo_h3ek_data_path
        scene_halo_h3ek_path = context.scene.halo_h3ek_path

        return global_functions.run_code("mattools.make_bitmaps(context, scene_halo_h3ek_path.directory, scene_halo_h3ek_data_path.directory)")

class Set_Material_Type(Operator):
    """Set Material Type"""
    bl_idname = 'halo_mattools.set_material_type'
    bl_label = 'Set Material Type'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import mattools
        scene = context.scene
        scene_halo_mattype = scene.halo_mattype
        return global_functions.run_code("mattools.set_material_type(context, scene_halo_mattype.mat_types)")

class Enable_Material_Type(Operator):
    """Enables/Disables the usage of material types"""
    bl_idname = 'halo_mattools.enable_material_type'
    bl_label = 'Set Material Type'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import mattools
        scene = context.scene
        scene_halo_mattype = scene.halo_mattype
        return global_functions.run_code("mattools.enable_material_type(context)")

class GenerateTag(Operator):
    """Generate a Halo tag from JSON or older tags"""
    bl_idname = 'halo_bulk.generate_tag'
    bl_label = 'Generate Tag'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import generate_tag

        scene_halo_scenario = context.scene.halo_scenario

        return global_functions.run_code("generate_tag.convert_tag(context, scene_halo_scenario.input_file, scene_halo_scenario.source_game_title, scene_halo_scenario.target_game_title, scene_halo_scenario.upgrade_patches, self.report)")

class Halo_JoinObjectPanel(Panel):
    bl_label = "Halo Join Objects"
    bl_idname = "HALO_PT_JoinObjects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        row = col.row()
        row.operator(Halo_JoinObject.bl_idname, text='Joins Objects')

class Halo_JoinObject(Operator):
    """Joins objects while preserving region setup"""
    bl_idname = 'halo_bulk.join_objects'
    bl_label = 'Join selected objects into active object'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import join_objects
        return global_functions.run_code("join_objects.join_objects(context)")

class Halo_ConvertFacemapsPanel(Panel):
    bl_label = "Halo Convert Facemaps"
    bl_idname = "HALO_PT_ConvertFacemaps"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        row = col.row()
        row.operator(Halo_ConvertFacemaps.bl_idname, text='Convert Facemaps')

class Halo_ConvertFacemaps(Operator):
    """Converts facemaps to the custom region attribute system"""
    bl_idname = 'halo_bulk.convert_facemaps'
    bl_label = 'Convert facemaps of the active object'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import convert_facemaps
        return global_functions.run_code("convert_facemaps.convert_facemaps(context)")

class Scenario_SceneProps(Panel):
    bl_label = "Tag Scene Properties"
    bl_idname = "HALO_PT_ScenarioTag"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_ScenePropertiesPanel"

    def draw(self, context):
        layout = self.layout
        scene_halo_tag = context.scene.halo_tag

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Scenario Path:')
        row.prop(scene_halo_tag, "scenario_path", text='')

class ScenarioTagGroup(PropertyGroup):
    scenario_path: StringProperty(
            name = "Scenario Path",
            description="Where to place the generated scenario file for this level",
            default="",
            maxlen=1024,
            subtype='FILE_PATH'
    )

    image_multiplier: IntProperty(
        name="Image Multiplier",
        description="Takes image resolution and multiplies it by set value",
        default=1,
        min=1
    )

class Halo_LightmapBakingPanel(Panel):
    bl_label = "Halo Lightmap Baking"
    bl_idname = "HALO_PT_LightmapBaking"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_AutoTools"

    def draw(self, context):
        layout = self.layout
        scene_halo_tag = context.scene.halo_tag

        if global_functions.string_empty_check(scene_halo_tag.scenario_path):
            layout.enabled = False

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Image Multiplier:')
        row.prop(scene_halo_tag, "image_multiplier", text='')
        row = col.row()
        row.operator(LightmapBaking.bl_idname, text='Bake Lightmaps')

class LightmapBaking(Operator):
    """Bake lightmaps for all clusters in scene"""
    bl_idname = 'halo_bulk.bake_clusters'
    bl_label = 'Bake Clusters'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from ..misc import lightmap_baking
        scene_halo = context.scene.halo
        scene_halo_tag = context.scene.halo_tag

        return global_functions.run_code("lightmap_baking.bake_clusters(context, scene_halo.game_title, scene_halo_tag.scenario_path, scene_halo_tag.image_multiplier, self.report)")

classeshalo = (
    Halo_MaterialPropertiesGroup,
    JMA_BatchDialog,
    H3EK_PathDialog,
    H3EK_DataPathDialog,
    ExportLightmap,
    Bulk_Rename_Bones,
    Bulk_Rename_Prefix,
    Bulk_Rotate_Bones,
    Bulk_Reset_Bones,
    Cull_Materials,
    Random_Material_Colors,
    Scale_Model,
    GenerateSky,
    GenerateLevel,
    FaceSet,
    ImportFixup,
    Bulk_IK_Prep,
    Bulk_Anim_Convert,
    Bulk_Set_Transform,
    Halo_Tools_Helper,
    Halo_BoneNameHelper,
    Halo_NodePrefixHelper,
    Halo_BoneRotationHelper,
    Halo_CullMaterials,
    Halo_RandomMaterialColors,
    Halo_ScaleModelHelper,
    Halo_MaterialDefinitionHelper,
    Halo_ImportFixup,
    Halo_IKHelper,
    Halo_MultiUserHelper,
    Halo_BatchAnimConverter,
    Halo_MatTools,
    Export_Textures,
    Make_Bitmaps,
    Set_Material_Type,
    Enable_Material_Type,
    Halo_Sky_Tools_Helper,
    Halo_Sky_Dome,
    Halo_Sky_Light,
    Halo_Sky_Zenith_Color,
    Halo_Sky_Horizon_Color,
    Halo_Sky_Sun_Light,
    Halo_Sky_Sun_Color,
    Halo_Sky_Misc_Settings,
    JMA_BatchPropertiesGroup,
    Halo_H3EKPropertiesGroup,
    Halo_ImportFixupPropertiesGroup,
    Scale_ModelPropertiesGroup,
    SkyPropertiesGroup,
    Halo_PrefixPropertiesGroup,
    Face_SetPropertiesGroup,
    GenerateTag,
    Halo_GenerateTag,
    Source_PropertiesGroup,
    Halo_GenerateLevel,
    LevelProprtiesGroup,
    Generate_Tag_Dialog,
    Generate_Tag_Patches_Dialog,
    Halo_JoinObject,
    Halo_JoinObjectPanel,
    Halo_ConvertFacemapsPanel,
    Halo_ConvertFacemaps,
    ScenarioTagGroup,
    Halo_LightmapBakingPanel,
    LightmapBaking,
    Scenario_SceneProps
)

def menu_func_export(self, context):
    self.layout.operator(ExportLightmap.bl_idname, text="Halo Lightmap UV (.luv)")

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.Scene.halo_import_fixup = PointerProperty(type=Halo_ImportFixupPropertiesGroup, name="Halo Import Helper", description="Set properties for the import fixup helper")
    bpy.types.Scene.halo_prefix = PointerProperty(type=Halo_PrefixPropertiesGroup, name="Halo Prefix Helper", description="Set properties for node prefixes")
    bpy.types.Scene.scale_model = PointerProperty(type=Scale_ModelPropertiesGroup, name="Halo Scale Model Helper", description="Create meshes for scale")
    bpy.types.Scene.halo_scenario = PointerProperty(type=Source_PropertiesGroup, name="Halo Source Converter", description="Create tags from JSON or older tag versions")
    bpy.types.Scene.halo_sky = PointerProperty(type=SkyPropertiesGroup, name="Sky Helper", description="Generate a sky for Halo 3")
    bpy.types.Scene.halo_face_set = PointerProperty(type=Face_SetPropertiesGroup, name="Halo Face Set Helper", description="Creates a facemap with the exact name we need")
    bpy.types.Scene.halo_anim_batch = PointerProperty(type=JMA_BatchPropertiesGroup, name="Halo Batch Anims", description="Converts all animations in a specific directory to a different version.")
    bpy.types.Scene.halo_h3ek_path = PointerProperty(type=Halo_H3EKPropertiesGroup, name="H3EK Path", description="The H3EK Path")
    bpy.types.Scene.halo_h3ek_data_path = PointerProperty(type=Halo_H3EKPropertiesGroup, name="H3EK Path", description="The H3EK Data Path")
    bpy.types.Scene.halo_mattype = PointerProperty(type=Halo_MaterialPropertiesGroup, name ="Material Properties", description="Set the material properties of the active object")
    bpy.types.Scene.halo_maze = PointerProperty(type=LevelProprtiesGroup, name="Halo Level Properties", description="Create a Halo level using a maze layout")
    bpy.types.Scene.halo_tag = PointerProperty(type=ScenarioTagGroup, name="Scenario Tag", description="Store properties for a scenario tag")

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    del bpy.types.Scene.halo_import_fixup
    del bpy.types.Scene.halo_prefix
    del bpy.types.Scene.scale_model
    del bpy.types.Scene.halo_sky
    del bpy.types.Scene.halo_face_set
    del bpy.types.Scene.halo_anim_batch
    del bpy.types.Scene.halo_h3ek_path
    del bpy.types.Scene.halo_h3ek_data_path
    del bpy.types.Scene.halo_mattype
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
