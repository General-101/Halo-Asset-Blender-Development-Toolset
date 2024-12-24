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

from bpy.types import (
        PropertyGroup,
        Panel
        )

from bpy.props import (
        IntProperty,
        BoolProperty,
        EnumProperty,
        PointerProperty,
        CollectionProperty
        )

from .region_ui import (
    Halo_RegionsPanel,
    Halo_OT_RegionMove,
    Halo_OT_RegionRemove,
    Halo_OT_RegionAdd,
    REGION_UL_List,
    RegionItem,
    Halo_OT_RegionAssign,
    Halo_OT_RegionRemoveFrom,
    Halo_OT_RegionSelect,
    Halo_OT_RegionDeselect,
    Halo_OT_RegionRemoveUnused,
    REGION_MT_context_menu,
    region_add,
    get_custom_attribute
)

from .material_ui import (
    ASS_JMS_MaterialPropertiesGroup,
    ASS_LightPropertiesGroup,
    ASS_LightProps,
    ASS_LightSpot,
    ASS_LightNearAtten,
    ASS_LightFarAtten,
    ASS_JMS_MaterialProps,
    ASS_JMS_MaterialFlagsProps,
    ASS_JMS_MaterialLightmapProps,
    ASS_JMS_MaterialBasicProps,
    ASS_JMS_MaterialAttenuationProps,
    ASS_JMS_MaterialFrustumProps
)

from .maze_ui import (
    set_surface_usage,
    get_surface_usage,
    set_character_usage,
    get_character_usage,
    set_marine_usage,
    get_marine_usage,
    set_elite_usage,
    get_elite_usage,
    set_grunt_usage,
    get_grunt_usage,
    set_hunter_usage,
    get_hunter_usage,
    set_jackal_usage,
    get_jackal_usage,
    set_floodcarrier_usage,
    get_floodcarrier_usage,
    set_floodcombat_elite_usage,
    get_floodcombat_elite_usage,
    set_floodcombat_human_usage,
    get_floodcombat_human_usage,
    set_flood_infection_usage,
    get_flood_infection_usage,
    set_sentinel_usage,
    get_sentinel_usage,
    set_drinol_usage,
    get_drinol_usage,
    set_slug_man_usage,
    get_slug_man_usage
)

from .object_ui import (
    ASS_JMS_ObjectPropertiesGroup,
    ASS_JMS_MeshPropertiesGroup,
    QUA_ObjectPropertiesGroup,
    QUA_SpeakerPropertiesGroup,
    QUA_ScriptPropertiesGroup,
    QUA_EffectPropertiesGroup,
    Halo_ObjectProps,
    Halo_BoneProps,
    Halo_MeshProps,
    Halo_XREFPath,
    Halo_CameraProps,
    Halo_ScriptProps,
    Halo_EffectProps
)

from .tag_view import (
    Halo_ObjectTagView,
    Halo_CollectionTagView,
    HaloSkyPropertiesGroup,
    HaloObjectPropertiesGroup,
    HaloUnitPropertiesGroup,
    HaloItemPropertiesGroup,
    HaloWeaponPropertiesGroup,
    HaloDevicePropertiesGroup,
    HaloMachinePropertiesGroup,
    HaloControlPropertiesGroup,
    HaloLightFixturePropertiesGroup,
    HaloPlayerStartingLocationPropertiesGroup,
    HaloNetgameFlagsPropertiesGroup,
    HaloNetgameEquipmentPropertiesGroup,
    HaloCollectionPropertiesGroup,
    HaloEncounterPropertiesGroup,
    HaloSquadPropertiesGroup,
    HaloMovePositionPropertiesGroup,
    HaloStartingLocationPropertiesGroup,
    HaloPlatoonPropertiesGroup,
    HaloFiringPositionPropertiesGroup,
    HaloDecalPropertiesGroup,
    HaloCommandListPropertiesGroup,
    HaloCommandPropertiesGroup,
    HaloCutsceneFlagGroup,
    HaloCutsceneCameraGroup,
    Scenario_SceneProps,
    HaloScenarioPropertiesGroup,
    HaloGeometryPropertiesGroup,
)

from ..global_ui.tag_fields.object_names import (
    object_name_add,
    ObjectNameItem,
    OBJECTNAME_UL_List,
    Halo_OT_ObjectNameAdd,
    Halo_OT_ObjectNameRemove,
    Halo_OT_ObjectNameMove,
    Halo_ObjectNamePanel
    )

from .tag_fields.tag_palette import (
    tag_add,
    TagItem,
    TAG_UL_List,
    Halo_OT_TagAdd,
    Halo_OT_TagRemove,
    Halo_OT_TagMove,
    Halo_TagPanel
    )

class Halo_SceneProps(Panel):
    bl_label = "Halo Scene Properties"
    bl_idname = "HALO_PT_ScenePropertiesPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

class Halo_GlobalSettings(Panel):
    bl_label = "Global Settings"
    bl_idname = "HALO_PT_GlobalSettings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_ScenePropertiesPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo = scene.halo

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Scene Game Title:')
        row.prop(scene_halo, "game_title", text='')
        row = col.row()
        row.label(text='Expert Mode:')
        row.prop(scene_halo, "expert_mode", text='')

class Halo_ScenePropertiesGroup(PropertyGroup):
    game_title: EnumProperty(
        name="Game:",
        description="What game will you be exporting for",
        items=[ ('halo1', "Halo 1", "Show properties for Halo Custom Edition Or Halo CE MCC"),
                ('halo2', "Halo 2", "Show properties for Halo 2 Vista or Halo 2 MCC"),
                ('halo3', "Halo 3", "Show properties for Halo 3 MCC"),
                ('halor', "Halo Reach", "Show properties for Halo Reach MCC"),
                ('halo4', "Halo 4", "Show properties for Halo 4 MCC"),
               ]
        )

    expert_mode: BoolProperty(
        name ="Expert Mode",
        description = "Reveal hidden options. If you're not a developer or know what you're doing then you probably shouldn't be messing with this.",
        default = False,
        )

classeshalo = (
    ASS_JMS_ObjectPropertiesGroup,
    ASS_JMS_MeshPropertiesGroup,
    ASS_JMS_MaterialPropertiesGroup,
    QUA_ObjectPropertiesGroup,
    QUA_SpeakerPropertiesGroup,
    QUA_ScriptPropertiesGroup,
    QUA_EffectPropertiesGroup,
    Halo_ObjectProps,
    Halo_BoneProps,
    Halo_MeshProps,
    ASS_LightPropertiesGroup,
    ASS_LightProps,
    ASS_LightSpot,
    ASS_LightNearAtten,
    ASS_LightFarAtten,
    ASS_JMS_MaterialProps,
    ASS_JMS_MaterialFlagsProps,
    ASS_JMS_MaterialLightmapProps,
    ASS_JMS_MaterialBasicProps,
    ASS_JMS_MaterialAttenuationProps,
    ASS_JMS_MaterialFrustumProps,
    Halo_CameraProps,
    Halo_ScriptProps,
    Halo_EffectProps,
    Halo_ScenePropertiesGroup,
    Halo_SceneProps,
    Halo_GlobalSettings,
    Halo_XREFPath,
    Halo_RegionsPanel,
    Halo_OT_RegionMove,
    Halo_OT_RegionRemove,
    Halo_OT_RegionAdd,
    REGION_UL_List,
    RegionItem,
    Halo_OT_RegionAssign,
    Halo_OT_RegionRemoveFrom,
    Halo_OT_RegionSelect,
    Halo_OT_RegionDeselect,
    Halo_OT_RegionRemoveUnused,
    REGION_MT_context_menu,
    Halo_ObjectTagView,
    Halo_CollectionTagView,
    HaloSkyPropertiesGroup,
    HaloObjectPropertiesGroup,
    HaloUnitPropertiesGroup,
    HaloItemPropertiesGroup,
    HaloWeaponPropertiesGroup,
    HaloDevicePropertiesGroup,
    HaloMachinePropertiesGroup,
    HaloControlPropertiesGroup,
    HaloLightFixturePropertiesGroup,
    HaloPlayerStartingLocationPropertiesGroup,
    HaloNetgameFlagsPropertiesGroup,
    HaloNetgameEquipmentPropertiesGroup,
    HaloCollectionPropertiesGroup,
    HaloEncounterPropertiesGroup,
    HaloSquadPropertiesGroup,
    HaloMovePositionPropertiesGroup,
    HaloStartingLocationPropertiesGroup,
    HaloPlatoonPropertiesGroup,
    HaloFiringPositionPropertiesGroup,
    HaloDecalPropertiesGroup,
    HaloCommandListPropertiesGroup,
    HaloCommandPropertiesGroup,
    HaloCutsceneFlagGroup,
    HaloCutsceneCameraGroup,
    Scenario_SceneProps,
    HaloScenarioPropertiesGroup,
    HaloGeometryPropertiesGroup,
    ObjectNameItem,
    OBJECTNAME_UL_List,
    Halo_OT_ObjectNameAdd,
    Halo_OT_ObjectNameRemove,
    Halo_OT_ObjectNameMove,
    Halo_ObjectNamePanel, 
    TagItem,
    TAG_UL_List,
    Halo_OT_TagAdd,
    Halo_OT_TagRemove,
    Halo_OT_TagMove,
    Halo_TagPanel
    )

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.Light.halo_light = PointerProperty(type=ASS_LightPropertiesGroup, name="ASS Properties", description="Set properties for your light")
    bpy.types.Scene.tag_scenario = PointerProperty(type=HaloScenarioPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_mesh = PointerProperty(type=HaloGeometryPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_sky = PointerProperty(type=HaloSkyPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_object = PointerProperty(type=HaloObjectPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_unit = PointerProperty(type=HaloUnitPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_item = PointerProperty(type=HaloItemPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_weapon = PointerProperty(type=HaloWeaponPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_device = PointerProperty(type=HaloDevicePropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_machine = PointerProperty(type=HaloMachinePropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_control = PointerProperty(type=HaloControlPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_light_fixture = PointerProperty(type=HaloLightFixturePropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_player_starting_location = PointerProperty(type=HaloPlayerStartingLocationPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_netgame_flag = PointerProperty(type=HaloNetgameFlagsPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_netgame_equipment = PointerProperty(type=HaloNetgameEquipmentPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_encounter = PointerProperty(type=HaloEncounterPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_squad = PointerProperty(type=HaloSquadPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_move_position = PointerProperty(type=HaloMovePositionPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_starting_location = PointerProperty(type=HaloStartingLocationPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_platoon = PointerProperty(type=HaloPlatoonPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_firing_position = PointerProperty(type=HaloFiringPositionPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_decal = PointerProperty(type=HaloDecalPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_command_list = PointerProperty(type=HaloCommandListPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_command = PointerProperty(type=HaloCommandPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_cutscene_flag = PointerProperty(type=HaloCutsceneFlagGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.tag_cutscene_camera = PointerProperty(type=HaloCutsceneCameraGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_mesh = PointerProperty(type=HaloGeometryPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_sky = PointerProperty(type=HaloSkyPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_object = PointerProperty(type=HaloObjectPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_unit = PointerProperty(type=HaloUnitPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_item = PointerProperty(type=HaloItemPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_weapon = PointerProperty(type=HaloWeaponPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_device = PointerProperty(type=HaloDevicePropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_machine = PointerProperty(type=HaloMachinePropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_control = PointerProperty(type=HaloControlPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_light_fixture = PointerProperty(type=HaloLightFixturePropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_player_starting_location = PointerProperty(type=HaloPlayerStartingLocationPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_netgame_flag = PointerProperty(type=HaloNetgameFlagsPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_netgame_equipment = PointerProperty(type=HaloNetgameEquipmentPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_encounter = PointerProperty(type=HaloEncounterPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_squad = PointerProperty(type=HaloSquadPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_move_position = PointerProperty(type=HaloMovePositionPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_starting_location = PointerProperty(type=HaloStartingLocationPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_platoon = PointerProperty(type=HaloPlatoonPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_firing_position = PointerProperty(type=HaloFiringPositionPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_decal = PointerProperty(type=HaloDecalPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_command_list = PointerProperty(type=HaloCommandListPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_command = PointerProperty(type=HaloCommandPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_cutscene_flag = PointerProperty(type=HaloCutsceneFlagGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Light.tag_cutscene_camera = PointerProperty(type=HaloCutsceneCameraGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_collection = PointerProperty(type=HaloCollectionPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_mesh = PointerProperty(type=HaloGeometryPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_sky = PointerProperty(type=HaloSkyPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_object = PointerProperty(type=HaloObjectPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_unit = PointerProperty(type=HaloUnitPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_item = PointerProperty(type=HaloItemPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_weapon = PointerProperty(type=HaloWeaponPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_device = PointerProperty(type=HaloDevicePropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_machine = PointerProperty(type=HaloMachinePropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_control = PointerProperty(type=HaloControlPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_light_fixture = PointerProperty(type=HaloLightFixturePropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_player_starting_location = PointerProperty(type=HaloPlayerStartingLocationPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_netgame_flag = PointerProperty(type=HaloNetgameFlagsPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_netgame_equipment = PointerProperty(type=HaloNetgameEquipmentPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_encounter = PointerProperty(type=HaloEncounterPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_squad = PointerProperty(type=HaloSquadPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_move_position = PointerProperty(type=HaloMovePositionPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_starting_location = PointerProperty(type=HaloStartingLocationPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_platoon = PointerProperty(type=HaloPlatoonPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_firing_position = PointerProperty(type=HaloFiringPositionPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_decal = PointerProperty(type=HaloDecalPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_command_list = PointerProperty(type=HaloCommandListPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_command = PointerProperty(type=HaloCommandPropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_cutscene_flag = PointerProperty(type=HaloCutsceneFlagGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Collection.tag_cutscene_camera = PointerProperty(type=HaloCutsceneCameraGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.ass_jms = PointerProperty(type=ASS_JMS_ObjectPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your object")
    bpy.types.Armature.ass_jms = PointerProperty(type=ASS_JMS_ObjectPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your object")
    bpy.types.Bone.ass_jms = PointerProperty(type=ASS_JMS_ObjectPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your Bone")
    bpy.types.Mesh.ass_jms = PointerProperty(type=ASS_JMS_MeshPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your mesh")
    bpy.types.Material.ass_jms = PointerProperty(type=ASS_JMS_MaterialPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your materials")
    bpy.types.Scene.halo = PointerProperty(type=Halo_ScenePropertiesGroup, name="Halo Scene Properties", description="Set properties for your scene")
    bpy.types.Camera.qua = PointerProperty(type=QUA_ObjectPropertiesGroup, name="Halo Camera Properties", description="Set properties for your camera")
    bpy.types.Mesh.halo_valid_surface = BoolProperty(name="Valid Surface", get=get_surface_usage, set=set_surface_usage)
    bpy.types.Mesh.halo_valid_characters = IntProperty(name="Valid Characters Flag", get=get_character_usage, set=set_character_usage)
    bpy.types.Mesh.halo_marine = BoolProperty(name="Marine", get=get_marine_usage, set=set_marine_usage)
    bpy.types.Mesh.halo_elite = BoolProperty(name="Elite", get=get_elite_usage, set=set_elite_usage)
    bpy.types.Mesh.halo_grunt = BoolProperty(name="Grunt", get=get_grunt_usage, set=set_grunt_usage)
    bpy.types.Mesh.halo_hunter = BoolProperty(name="Hunter", get=get_hunter_usage, set=set_hunter_usage)
    bpy.types.Mesh.halo_jackal = BoolProperty(name="Jackal", get=get_jackal_usage, set=set_jackal_usage)
    bpy.types.Mesh.halo_floodcarrier = BoolProperty(name="Flood Carrier", get=get_floodcarrier_usage, set=set_floodcarrier_usage)
    bpy.types.Mesh.halo_floodcombat_elite = BoolProperty(name="Floodcombat Elite", get=get_floodcombat_elite_usage, set=set_floodcombat_elite_usage)
    bpy.types.Mesh.halo_floodcombat_human = BoolProperty(name="Floodcombat Human", get=get_floodcombat_human_usage, set=set_floodcombat_human_usage)
    bpy.types.Mesh.halo_flood_infection = BoolProperty(name="Flood Infection", get=get_flood_infection_usage, set=set_flood_infection_usage)
    bpy.types.Mesh.halo_sentinel = BoolProperty(name="Sentinel", get=get_sentinel_usage, set=set_sentinel_usage)
    bpy.types.Mesh.halo_drinol = BoolProperty(name="Drinol", get=get_drinol_usage, set=set_drinol_usage)
    bpy.types.Mesh.halo_slug_man = BoolProperty(name="Slug Man", get=get_slug_man_usage, set=set_slug_man_usage)
    bpy.types.Object.region_list = CollectionProperty(type = RegionItem)
    bpy.types.Object.active_region = IntProperty(name = "Active region index", description="Active index in the region array", default = -1)
    bpy.types.Scene.active_region_list = []
    bpy.types.Object.region_add = region_add
    bpy.types.Mesh.get_custom_attribute = get_custom_attribute
    bpy.types.Speaker.qua = PointerProperty(type=QUA_SpeakerPropertiesGroup, name="Halo Camera Audio Properties", description="Set sound properties for your speaker")
    bpy.types.Text.qua = PointerProperty(type=QUA_ScriptPropertiesGroup, name="Halo Script Properties", description="Set script properties for your scene")
    bpy.types.Object.qua = PointerProperty(type=QUA_EffectPropertiesGroup, name="Halo Camera Effect Properties", description="Set properties for your effect")
    bpy.types.Scene.object_names = CollectionProperty(type = ObjectNameItem)
    bpy.types.Scene.active_object_name = IntProperty(name = "Active object name index", description="Active index in the object name array", default = -1)
    bpy.types.Scene.object_name_add = object_name_add
    bpy.types.Scene.tag_palatte = CollectionProperty(type = TagItem)
    bpy.types.Scene.active_tag = IntProperty(name = "Active tag index", description="Active index in the tag array", default = -1)
    bpy.types.Scene.tag_add = tag_add

def unregister():
    del bpy.types.Light.halo_light
    del bpy.types.Scene.tag_scenario
    del bpy.types.Object.tag_mesh
    del bpy.types.Object.tag_sky
    del bpy.types.Object.tag_object
    del bpy.types.Object.tag_unit
    del bpy.types.Object.tag_item
    del bpy.types.Object.tag_weapon
    del bpy.types.Object.tag_device
    del bpy.types.Object.tag_machine
    del bpy.types.Object.tag_control
    del bpy.types.Object.tag_light_fixture
    del bpy.types.Object.tag_player_starting_location
    del bpy.types.Object.tag_netgame_flag
    del bpy.types.Object.tag_netgame_equipment
    del bpy.types.Object.tag_encounter
    del bpy.types.Object.tag_squad
    del bpy.types.Object.tag_move_position
    del bpy.types.Object.tag_starting_location
    del bpy.types.Object.tag_platoon
    del bpy.types.Object.tag_firing_position
    del bpy.types.Light.tag_mesh
    del bpy.types.Light.tag_sky
    del bpy.types.Light.tag_object
    del bpy.types.Light.tag_unit
    del bpy.types.Light.tag_item
    del bpy.types.Light.tag_weapon
    del bpy.types.Light.tag_device
    del bpy.types.Light.tag_machine
    del bpy.types.Light.tag_control
    del bpy.types.Light.tag_light_fixture
    del bpy.types.Light.tag_player_starting_location
    del bpy.types.Light.tag_netgame_flag
    del bpy.types.Light.tag_netgame_equipment
    del bpy.types.Light.tag_encounter
    del bpy.types.Light.tag_squad
    del bpy.types.Light.tag_move_position
    del bpy.types.Light.tag_starting_location
    del bpy.types.Light.tag_platoon
    del bpy.types.Light.tag_firing_position
    del bpy.types.Collection.tag_mesh
    del bpy.types.Collection.tag_sky
    del bpy.types.Collection.tag_object
    del bpy.types.Collection.tag_unit
    del bpy.types.Collection.tag_item
    del bpy.types.Collection.tag_weapon
    del bpy.types.Collection.tag_device
    del bpy.types.Collection.tag_machine
    del bpy.types.Collection.tag_control
    del bpy.types.Collection.tag_light_fixture
    del bpy.types.Collection.tag_player_starting_location
    del bpy.types.Collection.tag_netgame_flag
    del bpy.types.Collection.tag_netgame_equipment
    del bpy.types.Collection.tag_encounter
    del bpy.types.Collection.tag_squad
    del bpy.types.Collection.tag_move_position
    del bpy.types.Collection.tag_starting_location
    del bpy.types.Collection.tag_platoon
    del bpy.types.Collection.tag_firing_position
    del bpy.types.Object.ass_jms
    del bpy.types.Armature.ass_jms
    del bpy.types.Bone.ass_jms
    del bpy.types.Mesh.ass_jms
    del bpy.types.Material.ass_jms
    del bpy.types.Scene.halo
    del bpy.types.Camera.qua
    del bpy.types.Mesh.halo_valid_surface
    del bpy.types.Mesh.halo_valid_characters
    del bpy.types.Mesh.halo_marine
    del bpy.types.Mesh.halo_elite
    del bpy.types.Mesh.halo_grunt
    del bpy.types.Mesh.halo_hunter
    del bpy.types.Mesh.halo_jackal
    del bpy.types.Mesh.halo_floodcarrier
    del bpy.types.Mesh.halo_floodcombat_elite
    del bpy.types.Mesh.halo_floodcombat_human
    del bpy.types.Mesh.halo_flood_infection
    del bpy.types.Mesh.halo_sentinel
    del bpy.types.Mesh.halo_drinol
    del bpy.types.Mesh.halo_slug_man
    del bpy.types.Object.region_list
    del bpy.types.Object.active_region
    del bpy.types.Scene.active_region_list
    del bpy.types.Object.region_add
    del bpy.types.Mesh.get_custom_attribute
    del bpy.types.Speaker.qua
    del bpy.types.Text.qua
    del bpy.types.Object.qua
    del bpy.types.Scene.object_names
    del bpy.types.Scene.active_object_name
    del bpy.types.Scene.object_name_add
    del bpy.types.Scene.tag_palatte
    del bpy.types.Scene.active_tag
    del bpy.types.Scene.tag_add
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
