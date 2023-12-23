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
    Halo_ObjectProps,
    Halo_BoneProps,
    Halo_MeshProps,
    Halo_XREFPath
)

from .tag_view import (
    Halo_TagView,
    HALO_PropertiesGroup
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
    Halo_TagView,
    HALO_PropertiesGroup
    )

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.Light.halo_light = PointerProperty(type=ASS_LightPropertiesGroup, name="ASS Properties", description="Set properties for your light")
    bpy.types.Object.tag_view = PointerProperty(type=HALO_PropertiesGroup, name="Tag Properties", description="Set properties for your tags")
    bpy.types.Object.ass_jms = PointerProperty(type=ASS_JMS_ObjectPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your object")
    bpy.types.Armature.ass_jms = PointerProperty(type=ASS_JMS_ObjectPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your object")
    bpy.types.Bone.ass_jms = PointerProperty(type=ASS_JMS_ObjectPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your Bone")
    bpy.types.Mesh.ass_jms = PointerProperty(type=ASS_JMS_MeshPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your mesh")
    bpy.types.Material.ass_jms = PointerProperty(type=ASS_JMS_MaterialPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your materials")
    bpy.types.Scene.halo = PointerProperty(type=Halo_ScenePropertiesGroup, name="Halo Scene Properties", description="Set properties for your scene")
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

def unregister():
    del bpy.types.Light.halo_light
    del bpy.types.Object.ass_jms
    del bpy.types.Armature.ass_jms
    del bpy.types.Mesh.ass_jms
    del bpy.types.Material.ass_jms
    del bpy.types.Scene.halo
    del bpy.types.Object.region_list
    del bpy.types.Object.active_region
    del bpy.types.Scene.active_region_list
    del bpy.types.Object.region_add
    del bpy.types.Mesh.get_custom_attribute
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
