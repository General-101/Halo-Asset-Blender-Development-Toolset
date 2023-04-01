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
from os.path import exists as file_exists
from os.path import join as path_join

from bpy.types import (
        Panel,
        Operator,
        PropertyGroup
        )

from bpy.props import (
        StringProperty,
        BoolProperty,
        IntProperty,
        EnumProperty,
        PointerProperty,
        FloatProperty,
        )

from ...file_gr2.nwo_utils import clean_tag_path, get_tags_path, get_data_path, not_bungie_game, nwo_asset_type, valid_nwo_asset

is_blender_startup = True

class GR2_Tools_Helper(Panel):
    """Tools to help automate Halo GR2 workflow"""
    bl_label = "Halo GR2 Tools"
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

        row = layout.row()
        row.label(text='Animation Graph Path')
        row = layout.row()
        row.prop(scene_gr2_frame_ids, "anim_tag_path", text='')
        row.scale_x = 0.25
        row.operator('halo_gr2.graph_path')
        row = layout.row()
        row.scale_y = 1.5
        row.operator("halo_gr2.set_frame_ids", text="Set Frame IDs")
        row = layout.row()
        row.scale_y = 1.5
        row.operator("halo_gr2.reset_frame_ids", text="Reset Frame IDs")


class GR2_GraphPath(Operator):
    """Set the path to a model animation graph tag"""
    bl_idname = "halo_gr2.graph_path"
    bl_label = "Find"

    filter_glob: StringProperty(
        default="*.model_*",
        options={'HIDDEN'},
        )

    filepath: StringProperty(
        name="graph_path",
        description="Set the path to the tag",
        subtype="FILE_PATH"
    )

    def execute(self, context):
        context.scene.gr2_frame_ids.anim_tag_path = self.filepath

        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = get_tags_path()
        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}

class GR2_SetFrameIDsOp(Operator):
    bl_idname = 'halo_gr2.set_frame_ids'
    bl_label = 'Set Frame IDs'
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return len(context.scene.gr2_frame_ids.anim_tag_path) > 0

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

    def graph_clean_tag_path(self, context):
        self['anim_tag_path'] = clean_tag_path(self['anim_tag_path']).strip('"')

    anim_tag_path: StringProperty(
        name="Path to Animation Tag",
        description="Specify the full or relative path to a model animation graph",
        default='',
        update=graph_clean_tag_path,
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
        row = col.row(align=False)
        row.scale_y = 1.25
        row.operator('halo_gr2.launch_data')
        row.operator('halo_gr2.launch_tags')
        row = col.row(align=False)
        row.scale_y = 1.5
        row.operator('halo_gr2.launch_foundation')
        row = col.row(align=False)
        row.scale_y = 1.25
        row.operator('halo_gr2.launch_sapien')
        row.scale_y = 1.25
        row.operator('halo_gr2.launch_tagtest')
        # if scene_gr2_halo_launcher.sidecar_path != '' and file_exists(path_join(get_data_path(), scene_gr2_halo_launcher.sidecar_path)):
        #     flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        #     col = flow.column()
        #     col.scale_y = 1.5
        #     col.operator('halo_gr2.launch_source')

class GR2_HaloLauncherExplorerSettings(Panel):
    bl_label = "Explorer Settings"
    bl_idname = "HALO_PT_GR2_HaloLauncherExplorerSettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "HALO_PT_GR2_HaloLauncher"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return valid_nwo_asset(context)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_gr2_halo_launcher = scene.gr2_halo_launcher

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        col = flow.column()
        row = col.row()
        row.prop(scene_gr2_halo_launcher, "explorer_default", expand=True)

    
class GR2_HaloLauncherGameSettings(Panel):
    bl_label = "Game Settings"
    bl_idname = "HALO_PT_GR2_HaloLauncherGameSettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "HALO_PT_GR2_HaloLauncher"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return valid_nwo_asset(context)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_gr2_halo_launcher = scene.gr2_halo_launcher

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        col = flow.column()
        row = col.row()
        row.prop(scene_gr2_halo_launcher, "game_default", expand=True)
        col.prop(scene_gr2_halo_launcher, "initial_zone_set")
        if not_bungie_game():
            col.prop(scene_gr2_halo_launcher, "initial_bsp")
        col.prop(scene_gr2_halo_launcher, "insertion_point_index")
        col.prop(scene_gr2_halo_launcher, 'custom_functions')

        col.prop(scene_gr2_halo_launcher, "run_game_scripts")
        if not_bungie_game():
            col.prop(scene_gr2_halo_launcher, "enable_firefight")
            if scene_gr2_halo_launcher.enable_firefight:
                col.prop(scene_gr2_halo_launcher, "firefight_mission")

class GR2_HaloLauncherGamePruneSettings(Panel):
    bl_label = "Pruning"
    bl_idname = "HALO_PT_GR2_HaloLauncherGamePruneSettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "HALO_PT_GR2_HaloLauncherGameSettings"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_gr2_halo_launcher = scene.gr2_halo_launcher

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        col = flow.column()
        col.prop(scene_gr2_halo_launcher, "prune_globals")
        col.prop(scene_gr2_halo_launcher, "prune_globals_keep_playable")
        if not_bungie_game():
            col.prop(scene_gr2_halo_launcher, "prune_globals_use_empty")
            col.prop(scene_gr2_halo_launcher, "prune_models_enable_alternate_render_models")
            col.prop(scene_gr2_halo_launcher, "prune_scenario_keep_scriptable_objects")
        col.prop(scene_gr2_halo_launcher, "prune_scenario_all_lightmaps")
        col.prop(scene_gr2_halo_launcher, "prune_all_materials_use_gray_shader")
        if not_bungie_game():
            col.prop(scene_gr2_halo_launcher, "prune_all_materials_use_default_textures")
            col.prop(scene_gr2_halo_launcher, "prune_all_materials_use_default_textures_fx_textures")
        col.prop(scene_gr2_halo_launcher, "prune_all_material_effects")
        col.prop(scene_gr2_halo_launcher, "prune_all_dialog_sounds")
        col.prop(scene_gr2_halo_launcher, "prune_all_error_geometry")
        if not_bungie_game():
            col.prop(scene_gr2_halo_launcher, "prune_facial_animations")
            col.prop(scene_gr2_halo_launcher, "prune_first_person_animations")
            col.prop(scene_gr2_halo_launcher, "prune_low_quality_animations")
            col.prop(scene_gr2_halo_launcher, "prune_use_imposters")
            col.prop(scene_gr2_halo_launcher, "prune_cinematic_effects")
        else:
            col.prop(scene_gr2_halo_launcher, "prune_scenario_force_solo_mode")
            col.prop(scene_gr2_halo_launcher, "prune_scenario_force_single_bsp_zone_set")
            col.prop(scene_gr2_halo_launcher, "prune_scenario_force_single_bsp_zones")
            col.prop(scene_gr2_halo_launcher, "prune_keep_scripts")
        col.prop(scene_gr2_halo_launcher, "prune_scenario_for_environment_editing")
        if scene_gr2_halo_launcher.prune_scenario_for_environment_editing:
            col.prop(scene_gr2_halo_launcher, "prune_scenario_for_environment_editing_keep_cinematics")
            col.prop(scene_gr2_halo_launcher, "prune_scenario_for_environment_editing_keep_scenery")
            if not_bungie_game():
                col.prop(scene_gr2_halo_launcher, "prune_scenario_for_environment_editing_keep_decals")
                col.prop(scene_gr2_halo_launcher, "prune_scenario_for_environment_editing_keep_crates")
                col.prop(scene_gr2_halo_launcher, "prune_scenario_for_environment_editing_keep_creatures")
                col.prop(scene_gr2_halo_launcher, "prune_scenario_for_environment_editing_keep_pathfinding")
                col.prop(scene_gr2_halo_launcher, "prune_scenario_for_environment_editing_keep_new_decorator_block")
            else:
                col.prop(scene_gr2_halo_launcher, "prune_scenario_for_environment_finishing")

class GR2_HaloLauncherFoundationSettings(Panel):
    bl_label = "Foundation Settings"
    bl_idname = "HALO_PT_GR2_HaloLauncherFoundationSettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "HALO_PT_GR2_HaloLauncher"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return valid_nwo_asset(context)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_gr2_halo_launcher = scene.gr2_halo_launcher

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        col = flow.column()
        row = col.row()
        row.prop(scene_gr2_halo_launcher, "foundation_default", expand=True)
        col = layout.column(heading="Open")
        if scene_gr2_halo_launcher.foundation_default == 'asset':
            if nwo_asset_type() == 'MODEL':
                col.prop(scene_gr2_halo_launcher, "open_model")
                col.prop(scene_gr2_halo_launcher, "open_render_model")
                col.prop(scene_gr2_halo_launcher, "open_collision_model")
                col.prop(scene_gr2_halo_launcher, "open_physics_model")
                if len(bpy.data.actions) > 0:
                    col.prop(scene_gr2_halo_launcher, "open_model_animation_graph")
                    col.prop(scene_gr2_halo_launcher, "open_frame_event_list")
                col.separator()
                if scene.gr2.output_biped:
                    col.prop(scene_gr2_halo_launcher, "open_biped")
                if scene.gr2.output_crate:
                    col.prop(scene_gr2_halo_launcher, "open_crate")
                if scene.gr2.output_creature:
                    col.prop(scene_gr2_halo_launcher, "open_creature")
                if scene.gr2.output_device_control:
                    col.prop(scene_gr2_halo_launcher, "open_device_control")
                if scene.gr2.output_device_dispenser:
                    col.prop(scene_gr2_halo_launcher, "open_device_dispenser")
                if scene.gr2.output_device_machine:
                    col.prop(scene_gr2_halo_launcher, "open_device_machine")
                if scene.gr2.output_device_terminal:
                    col.prop(scene_gr2_halo_launcher, "open_device_terminal")
                if scene.gr2.output_effect_scenery:
                    col.prop(scene_gr2_halo_launcher, "open_effect_scenery")
                if scene.gr2.output_equipment:
                    col.prop(scene_gr2_halo_launcher, "open_equipment")
                if scene.gr2.output_giant:
                    col.prop(scene_gr2_halo_launcher, "open_giant")
                if scene.gr2.output_scenery:
                    col.prop(scene_gr2_halo_launcher, "open_scenery")
                if scene.gr2.output_vehicle:
                    col.prop(scene_gr2_halo_launcher, "open_vehicle")
                if scene.gr2.output_weapon:
                    col.prop(scene_gr2_halo_launcher, "open_weapon")
            elif nwo_asset_type() == 'SCENARIO':
                col.prop(scene_gr2_halo_launcher, "open_scenario")
                col.prop(scene_gr2_halo_launcher, "open_scenario_structure_bsp")
                col.prop(scene_gr2_halo_launcher, "open_scenario_lightmap_bsp_data")
                col.prop(scene_gr2_halo_launcher, "open_scenario_structure_lighting_info")
                if any([scene_gr2_halo_launcher.open_scenario_structure_bsp, scene_gr2_halo_launcher.open_scenario_lightmap_bsp_data,scene_gr2_halo_launcher.open_scenario_structure_lighting_info]):
                    col.prop(scene_gr2_halo_launcher, "bsp_name")
            elif nwo_asset_type() == 'SKY':
                col.prop(scene_gr2_halo_launcher, "open_model")
                col.prop(scene_gr2_halo_launcher, "open_render_model")
                col.prop(scene_gr2_halo_launcher, "open_scenery")
            elif nwo_asset_type() == 'DECORATOR SET':
                col.prop(scene_gr2_halo_launcher, "open_decorator_set")
            elif nwo_asset_type() == 'PARTICLE MODEL':
                col.prop(scene_gr2_halo_launcher, "open_particle_model")
            elif nwo_asset_type() == 'PREFAB':
                col.prop(scene_gr2_halo_launcher, "open_prefab")
                col.prop(scene_gr2_halo_launcher, "open_scenario_structure_bsp")
                col.prop(scene_gr2_halo_launcher, "open_scenario_structure_lighting_info")

class GR2_HaloLauncher_Foundation(Operator):
    """Launches Foundation"""
    bl_idname = 'halo_gr2.launch_foundation'
    bl_label = 'Foundation'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from .halo_launcher import LaunchFoundation
        return LaunchFoundation(context.scene.gr2_halo_launcher, context)

class GR2_HaloLauncher_Data(Operator):
    """Opens the Data Folder"""
    bl_idname = 'halo_gr2.launch_data'
    bl_label = 'Data'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        scene_gr2_halo_launcher = scene.gr2_halo_launcher
        from .halo_launcher import open_file_explorer
        return open_file_explorer(scene_gr2_halo_launcher.sidecar_path, scene_gr2_halo_launcher.explorer_default == 'asset' and valid_nwo_asset(context), False)

class GR2_HaloLauncher_Tags(Operator):
    """Opens the Tags Folder"""
    bl_idname = 'halo_gr2.launch_tags'
    bl_label = 'Tags'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        scene_gr2_halo_launcher = scene.gr2_halo_launcher
        from .halo_launcher import open_file_explorer
        return open_file_explorer(scene_gr2_halo_launcher.sidecar_path, scene_gr2_halo_launcher.explorer_default == 'asset' and valid_nwo_asset(context), True)

class GR2_HaloLauncher_Sapien(Operator):
    """Opens Sapien"""
    bl_idname = 'halo_gr2.launch_sapien'
    bl_label = 'Sapien   '
    bl_options = {"REGISTER", "UNDO"}

    filter_glob: StringProperty(
        default="*.scenario",
        options={'HIDDEN'},
        )

    filepath: StringProperty(
        name="filepath",
        description="Set path for the scenario",
        subtype="FILE_PATH"
    )

    def execute(self, context):
        scene = context.scene
        scene_gr2_halo_launcher = scene.gr2_halo_launcher
        from .halo_launcher import launch_game
        return launch_game(True, scene_gr2_halo_launcher, self.filepath)
    
    def invoke(self, context, event):
        scene = context.scene
        scene_gr2_halo_launcher = scene.gr2_halo_launcher
        if scene_gr2_halo_launcher.game_default == 'default' or not valid_nwo_asset(context) or nwo_asset_type() != 'SCENARIO':
            self.filepath = get_tags_path()
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.filepath = ''
            return self.execute(context)
    
class GR2_HaloLauncher_TagTest(Operator):
    """Opens Tag Test"""
    bl_idname = 'halo_gr2.launch_tagtest'
    bl_label = 'Tag Test'
    bl_options = {"REGISTER", "UNDO"}

    filter_glob: StringProperty(
        default="*.scenario",
        options={'HIDDEN'},
        )

    filepath: StringProperty(
        name="filepath",
        description="Set path for the scenario",
        subtype="FILE_PATH"
    )

    def execute(self, context):
        scene = context.scene
        scene_gr2_halo_launcher = scene.gr2_halo_launcher
        from .halo_launcher import launch_game
        return launch_game(False, scene_gr2_halo_launcher, self.filepath)
    
    def invoke(self, context, event):
        scene = context.scene
        scene_gr2_halo_launcher = scene.gr2_halo_launcher
        if scene_gr2_halo_launcher.game_default == 'default' or not valid_nwo_asset(context) or nwo_asset_type() != 'SCENARIO':
            self.filepath = get_tags_path()
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.filepath = ''
            return self.execute(context)
        

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

    explorer_default: EnumProperty(
        name="Folder",
        description="Select whether to open the root data / tags folder or the one for your asset. When no asset is found, defaults to root",
        default="asset",
        options=set(),
        items=[('default', 'Default', ''), ('asset', 'Asset', '')]
    )

    foundation_default: EnumProperty(
        name="Tags",
        description="Select whether Foundation should open with the last opended windows, or open to the selected asset tags",
        default="asset",
        options=set(),
        items=[('last', 'Default', ''), ('asset', 'Asset', '')]
    )

    game_default: EnumProperty(
        name="Scenario",
        description="Select whether to open Sapien / Tag Test and select a scenario, or open the current scenario asset if it exists",
        default="asset",
        options=set(),
        items=[('default', 'Default', ''), ('asset', 'Asset', '')]
    )

    open_model: BoolProperty(
        name='Model',
        default=True,
        options=set(),
    )

    open_render_model: BoolProperty(
        options=set(),
        name='Render Model'
    )
    
    open_collision_model: BoolProperty(
        options=set(),
        name='Collision Model'
    )

    open_physics_model: BoolProperty(
        options=set(),
        name='Physics Model'
    )

    open_model_animation_graph: BoolProperty(
        options=set(),
        name='Model Animation Graph'
    )

    open_frame_event_list: BoolProperty(
        options=set(),
        name='Frame Event List'
    )

    open_biped: BoolProperty(
        options=set(),
        name='Biped'
    )

    open_crate: BoolProperty(
        options=set(),
        name='Crate'
    )

    open_creature: BoolProperty(
        options=set(),
        name='Creature'
    )

    open_device_control: BoolProperty(
        options=set(),
        name='Device Control'
    )

    open_device_dispenser: BoolProperty(
        options=set(),
        name='Device Dispenser'
    )

    open_device_machine: BoolProperty(
        options=set(),
        name='Device Machine'
    )

    open_device_terminal: BoolProperty(
        options=set(),
        name='Device Terminal'
    )

    open_effect_scenery: BoolProperty(
        options=set(),
        name='Effect Scenery'
    )

    open_equipment: BoolProperty(
        options=set(),
        name='Equipment'
    )

    open_giant: BoolProperty(
        options=set(),
        name='Giant'
    )

    open_scenery: BoolProperty(
        options=set(),
        name='Scenery'
    )

    open_vehicle: BoolProperty(
        options=set(),
        name='Vehicle'
    )

    open_weapon: BoolProperty(
        options=set(),
        name='Weapon'
    )

    open_scenario: BoolProperty(
        options=set(),
        name='Scenario',
        default=True
    )

    open_prefab: BoolProperty(
        options=set(),
        name='Prefab',
        default=True
    )

    open_particle_model: BoolProperty(
        options=set(),
        name='Particle Model',
        default=True
    )

    open_decorator_set: BoolProperty(
        options=set(),
        name='Decorator Set',
        default=True
    )

    bsp_name: StringProperty(
        options=set(),
        name='BSP Name(s)',
        description="Input the bsps to open. Comma delimited for multiple bsps. Leave blank to open all bsps",
        default=''
    )

    open_scenario_structure_bsp: BoolProperty(
        options=set(),
        name='BSP',
    )

    open_scenario_lightmap_bsp_data: BoolProperty(
        options=set(),
        name='Lightmap Data',
    )

    open_scenario_structure_lighting_info: BoolProperty(
        options=set(),
        name='Lightmap Info',
    )

    ##### game launch #####

    run_game_scripts: BoolProperty(
        options=set(),
        description="Strips all player information, global materials, grenades and powerups from the globals tag, as well as interface global tags. Don't use this if you need the game to be playable",
        name='Run Game Scripts'
    )

    prune_globals: BoolProperty(
        options=set(),
        name='Globals'
    )

    prune_globals_keep_playable: BoolProperty(
        options=set(),
        name='Globals (Keep Playable)'
    )

    prune_globals_use_empty: BoolProperty(
        options=set(),
        name='Globals Use Empty'
    )

    prune_models_enable_alternate_render_models: BoolProperty(
        options=set(),
        name='Allow Alternate Render Models'
    )

    prune_scenario_keep_scriptable_objects: BoolProperty(
        options=set(),
        name='Keep Scriptable Objects'
    )

    prune_scenario_for_environment_editing: BoolProperty(
        options=set(),
        name='Prune for Environment Editing'
    )

    prune_scenario_for_environment_editing_keep_cinematics: BoolProperty(
        options=set(),
        name='Keep Cinematics'
    )

    prune_scenario_for_environment_editing_keep_scenery: BoolProperty(
        options=set(),
        name='Keep Scenery'
    )

    prune_scenario_for_environment_editing_keep_decals: BoolProperty(
        options=set(),
        name='Keep Decals'
    )

    prune_scenario_for_environment_editing_keep_crates: BoolProperty(
        options=set(),
        name='Keep Crates'
    )

    prune_scenario_for_environment_editing_keep_creatures: BoolProperty(
        options=set(),
        name='Keep Creatures'
    )

    prune_scenario_for_environment_editing_keep_pathfinding: BoolProperty(
        options=set(),
        name='Keep Pathfinding'
    )

    prune_scenario_for_environment_editing_keep_new_decorator_block: BoolProperty(
        options=set(),
        name='Keep Decorators'
    )

    prune_scenario_all_lightmaps: BoolProperty(
        options=set(),
        name='Prune Lightmaps'
    )

    prune_all_materials_use_gray_shader: BoolProperty(
        options=set(),
        name='Use Gray Shader'
    )

    prune_all_materials_use_default_textures: BoolProperty(
        options=set(),
        name='Use Default Textures'
    )

    prune_all_materials_use_default_textures_fx_textures: BoolProperty(
        options=set(),
        name='Include FX materials'
    )

    prune_all_material_effects: BoolProperty(
        options=set(),
        name='Prune Material Effects'
    )

    prune_all_dialog_sounds: BoolProperty(
        options=set(),
        name='Prune Material Effects'
    )

    prune_all_error_geometry: BoolProperty(
        options=set(),
        name='Prune Error Geometry'
    )

    prune_facial_animations: BoolProperty(
        options=set(),
        name='Prune Facial Animations'
    )

    prune_first_person_animations: BoolProperty(
        options=set(),
        name='Prune First Person Animations'
    )

    prune_low_quality_animations: BoolProperty(
        options=set(),
        name='Use Low Quality Animations'
    )

    prune_use_imposters: BoolProperty(
        options=set(),
        name='Use Imposters only'
    )

    prune_cinematic_effects: BoolProperty(
        options=set(),
        name='Prune Cinematic Effects'
    )
    # REACH Only prunes
    prune_scenario_force_solo_mode: BoolProperty(
        options=set(),
        name='Force Solo Mode'
    )

    prune_scenario_for_environment_finishing: BoolProperty(
        options=set(),
        name='Prune Finishing'
    )   

    prune_scenario_force_single_bsp_zone_set: BoolProperty(
        options=set(),
        name='Prune Zone Sets'
    )   

    prune_scenario_force_single_bsp_zones: BoolProperty(
        options=set(),
        name='Single BSP zone sets'
    )   

    prune_keep_scripts: BoolProperty(
        options=set(),
        name='Keep Scripts'
    )   
    # Other
    enable_firefight: BoolProperty(
        options=set(),
        name='Enable Spartan Ops'
    )

    firefight_mission: StringProperty(
        options=set(),
        name='Spartan Ops Mission',
        default=''
    )
    
    insertion_point_index: IntProperty(
        options=set(),
        name='Insertion Point Index',
        default=-1,
        min=-1,
        soft_max=4
    )

    initial_zone_set: StringProperty(
        options=set(),
        name='Initial Zone Set',
    )

    initial_bsp: StringProperty(
        options=set(),
        name='Initial BSP',
    )

    custom_functions: StringProperty(
        options=set(),
        name='Custom',
        description="Name of Blender blender text editor file to get custom init lines from. If no such text exists, instead looks in the root editing kit for an init with this name. If this doesn't exist, then the actual text is added to the init",
        default=''
    )

    


#######################################
# SHADER FINDER TOOL

class GR2_ShaderFinder(Panel):
    bl_label = "Shader Finder"
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
        col = layout.column(heading="Overwrite")
        sub = col.column(align=True)
        sub.prop(scene_gr2_shader_finder, "overwrite_existing", text='Existing')
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
        return FindShaders(context, scene_gr2_shader_finder.shaders_dir, self.report, scene_gr2_shader_finder.overwrite_existing)

class GR2_HaloShaderFinderPropertiesGroup(PropertyGroup):
    shaders_dir: StringProperty(
        name="Shaders Directory",
        description="Leave blank to search the entire tags folder for shaders or input a directory path to specify the folder (and sub-folders) to search for shaders",
        default='',
    )
    overwrite_existing: BoolProperty(
        name='Overwrite Shader Paths',
        options=set(),
        description="Overwrite material shader paths even if they're not blank",
        default=False,
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
        col.operator('halo_gr2.export', text='Export', icon='SETTINGS') 
        if scene_gr2_halo_launcher.sidecar_path != '' and file_exists(path_join(get_data_path(), scene_gr2_halo_launcher.sidecar_path)):
            col.separator()
            col.operator('halo_gr2.export_quick', text='Quick Export', icon='EXPORT')

class GR2_HaloExportSettings(Panel):
    bl_label = "Quick Export Settings"
    bl_idname = "HALO_PT_GR2_HaloExportSettings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_icon = 'EXPORT'
    bl_parent_id = "HALO_PT_GR2_HaloExport"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_gr2_export = scene.gr2_export

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()
        col = layout.column(heading="Toggle")
        col.prop(scene_gr2_export, 'show_output', text='Output')
        col = layout.column(heading="Export")
        col.prop(scene_gr2_export, 'export_gr2_files', text='GR2')
        if scene_gr2_export.export_gr2_files:
            col.prop(scene_gr2_export, "export_hidden", text='Hidden')
            col.prop(scene_gr2_export, 'export_all_bsps', expand=True)
            col.prop(scene_gr2_export, 'export_all_perms', expand=True)
        col.separator()
        col = layout.column(heading="Build")
        col.prop(scene_gr2_export, "export_sidecar_xml", text='Sidecar')
        col.separator()
        col = layout.column(heading="Import")
        col.prop(scene_gr2_export, "import_to_game", text='To Game')
        if scene_gr2_export.import_to_game:
            col.prop(scene_gr2_export, "import_draft", text='As draft')
        col.separator()
        col = layout.column(heading="Run")
        col.prop(scene_gr2_export, "lightmap_structure", text='Lightmap')
        if scene_gr2_export.lightmap_structure:
            if context.scene.halo.game_version in ('h4', 'h2a'):
                col.prop(scene_gr2_export, "lightmap_quality_h4")
                col.prop(scene_gr2_export, "lightmap_quality_custom")
            else:
                col.prop(scene_gr2_export, "lightmap_quality")
            if not scene_gr2_export.lightmap_all_bsps:
                col.prop(scene_gr2_export, 'lightmap_specific_bsp')
            col.prop(scene_gr2_export, 'lightmap_all_bsps')

class GR2_HaloExportSettingsExtended(Panel):
    bl_label = "Extended"
    bl_idname = "HALO_PT_GR2_HaloExportSettingsExtended"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_icon = 'EXPORT'
    bl_parent_id = "HALO_PT_GR2_HaloExportSettings"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_gr2_export = scene.gr2_export

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()
        col = layout.column(heading="Keep")
        col.prop(scene_gr2_export, 'keep_fbx')
        col.prop(scene_gr2_export, 'keep_json')
        col = layout.column(heading="Include")
        col.prop(scene_gr2_export, 'export_render')
        col.prop(scene_gr2_export, 'export_collision')
        col.prop(scene_gr2_export, 'export_physics')
        col.prop(scene_gr2_export, 'export_markers')
        col.prop(scene_gr2_export, 'export_structure')
        col.prop(scene_gr2_export, 'export_design')
        col.prop(scene_gr2_export, 'export_animations', expand=True)

        col.separator()

        col = layout.column(heading="Scene")
        col.prop(scene_gr2_export, 'use_mesh_modifiers')
        col.prop(scene_gr2_export, 'use_triangles')
        col.prop(scene_gr2_export, 'use_armature_deform_only')
        col.prop(scene_gr2_export, 'meshes_to_empties')
        col.prop(scene_gr2_export, 'global_scale')
        

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
        scene = context.scene
        scene_gr2_export = scene.gr2_export
        return ExportQuick(bpy.ops.export_scene.gr2, self.report, context, scene_gr2_export.export_gr2_files, scene_gr2_export.export_hidden, scene_gr2_export.export_all_bsps, scene_gr2_export.export_all_perms, scene_gr2_export.export_sidecar_xml, scene_gr2_export.import_to_game, scene_gr2_export.import_draft, scene_gr2_export.lightmap_structure, scene_gr2_export.lightmap_quality_h4, scene_gr2_export.lightmap_quality_custom, scene_gr2_export.lightmap_quality, scene_gr2_export.lightmap_specific_bsp, scene_gr2_export.lightmap_all_bsps, scene_gr2_export.export_animations, scene_gr2_export.export_render, scene_gr2_export.export_collision, scene_gr2_export.export_physics, scene_gr2_export.export_markers, scene_gr2_export.export_structure, scene_gr2_export.export_design, scene_gr2_export.use_mesh_modifiers, scene_gr2_export.use_triangles, scene_gr2_export.global_scale, scene_gr2_export.use_armature_deform_only, scene_gr2_export.meshes_to_empties, scene_gr2_export.show_output, scene_gr2_export.keep_fbx, scene_gr2_export.keep_json)

class GR2_HaloExportPropertiesGroup(PropertyGroup):
    final_report: StringProperty(
        name="",
        description="",
        default='',
    )
    export_gr2_files: BoolProperty(
        name='Export GR2 Files',
        default=True,
        options=set(),
    )
    export_hidden: BoolProperty(
        name="Hidden",
        description="Export visible objects only",
        default=True,
        options=set(),
    )
    export_all_bsps: EnumProperty(
        name='BSPs',
        description='Specify whether to export all BSPs, or just those selected',
        default='all',
        items=[('all', 'All', ''), ('selected', 'Selected', '')],
        options=set(),
    )
    export_all_perms: EnumProperty(
        name='Perms',
        description='Specify whether to export all permutations, or just those selected',
        default='all',
        items=[('all', 'All', ''), ('selected', 'Selected', '')],
        options=set(),
    )
    export_sidecar_xml: BoolProperty(
        name="Build Sidecar",
        description="",
        default=True,
        options=set(),
    )
    import_to_game: BoolProperty(
        name='Import to Game',
        description='',
        default=True,
        options=set(),
    )
    import_draft: BoolProperty(
        name='Draft',
        description="Skip generating PRT data. Faster speed, lower quality",
        default=False,
        options=set(),
    )
    lightmap_structure: BoolProperty(
        name='Run Lightmapper',
        default=False,
        options=set(),
    )
    lightmap_quality_h4: EnumProperty(
        name='Quality',
        items=(('default_new', "Default New", ""),
                ('farm_draft_quality', "Draft", ""),
                ('neutral_lighting_enc', "Neutral", ""),
                ('mp_medium', "Medium", ""),
                ('farm_high_quality', "High", ""),
                ('farm_high_quality_two_bounce', "High Two Bounce", ""),
                ('high_direct_sun', "High Direct Sun", ""),
                ('high_direct_sun_sky', "High Direct Sun Sky", ""),
                ('high_indirect_ao', "High Indirect AO", ""),
                ('farm_uber_quality', "Uber", ""),
                ),
        default='default_new',
        options=set(),
        description="Define the lightmap quality you wish to use",
    )
    lightmap_quality_custom: StringProperty(
        name='Custom Quality',
        default='',
        description="Define the custom lightmap quality you wish to use (must be defined in globals\lightmapper_settings). This will override the drop down list.",
    )
    lightmap_quality: EnumProperty(
        name='Quality',
        items=(('DIRECT', "Direct", ""),
                ('DRAFT', "Draft", ""),
                ('LOW', "Low", ""),
                ('MEDIUM', "Medium", ""),
                ('HIGH', "High", ""),
                ('SUPER', "Super (very slow)", ""),
                ),
        default='DIRECT',
        options=set(),
        description="Define the lightmap quality you wish to use",
    )
    lightmap_all_bsps: BoolProperty(
        name='All BSPs',
        default=True,
        options=set(),
    )
    lightmap_specific_bsp: StringProperty(
        name='Specific BSP',
        default='',
        options=set(),
    )
    ################################
    # Detailed settings
    ###############################
    export_animations: EnumProperty(
        name='Animations',
        description='',
        default='ALL',
        items=[ ('ALL', "All", ""), ('ACTIVE', "Active", ""), ('NONE', 'None', '')],
        options=set(),
    )
    export_render: BoolProperty(
        name='Render Models',
        description='',
        default=True,
        options=set(),
    )
    export_collision: BoolProperty(
        name='Collision Models',
        description='',
        default=True,
        options=set(),
    )
    export_physics: BoolProperty(
        name='Physics Models',
        description='',
        default=True,
        options=set(),
    )
    export_markers: BoolProperty(
        name='Markers',
        description='',
        default=True,
        options=set(),
    )
    export_structure: BoolProperty(
        name='Structure',
        description='',
        default=True,
        options=set(),
    )
    export_design: BoolProperty(
        name='Structure Design',
        description='',
        default=True,
        options=set(),
    )
    use_mesh_modifiers: BoolProperty(
        name='Apply Modifiers',
        description='',
        default=True,
        options=set(),
    )
    use_triangles: BoolProperty(
        name='Triangulate',
        description='',
        default=True,
        options=set(),
    )
    global_scale: FloatProperty(
        name='Scale',
        description='',
        default=1.0,
        options=set(), 
    )
    use_armature_deform_only: BoolProperty( 
        name='Deform Bones Only',
        description='Only export bones with the deform property ticked',
        default=True,
        options=set(),
    )
    meshes_to_empties: BoolProperty(
        name='Markers as Empties',
        description='Export all mesh Halo markers as empties. Helps save on export / import time and file size',
        default=True,
        options=set(),
    )

    def get_show_output(self):
        global is_blender_startup
        if is_blender_startup:
            is_blender_startup = False
            self["show_output"] = True
            return True
        else:
            return self["show_output"]
    
    def set_show_output(self, value):
        self["show_output"] = value

    show_output: BoolProperty(
        name='Show Output',
        description='',
        default=True,
        options=set(),
        get=get_show_output,
        set=set_show_output,
    )
    keep_fbx: BoolProperty(
        name="FBX",
        description="Keep the source FBX file after GR2 conversion",
        default=True,
        options=set(),
    )
    keep_json: BoolProperty(
        name="JSON",
        description="Keep the source JSON file after GR2 conversion",
        default=True,
        options=set(),
    )


#######################################
# PROPERTIES MANAGER TOOL

class GR2_PropertiesManager(Panel):
    bl_label = "Properties Manager"
    bl_idname = "HALO_PT_GR2_PropertiesManager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GR2_AutoTools"

    def draw(self, context):
        layout = self.layout

class GR2_CollectionManager(Panel):
    bl_label = "Collection Manager"
    bl_idname = "HALO_PT_GR2_CollectionManager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GR2_PropertiesManager"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_gr2_collection_manager = scene.gr2_collection_manager

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()
        col.prop(scene_gr2_collection_manager, 'collection_name', text='Name')
        col.prop(scene_gr2_collection_manager, 'collection_type', text='Type')
        col = col.row()
        col.scale_y = 1.5
        col.operator('halo_gr2.collection_create')

class GR2_CollectionManager_Create(Operator):
    bl_idname = 'halo_gr2.collection_create'
    bl_label = 'Create New Collection'
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        scene_gr2_collection_manager = scene.gr2_collection_manager
        return scene_gr2_collection_manager.collection_name != '' and not scene_gr2_collection_manager.collection_name.isspace()

    def execute(self, context):
        scene = context.scene
        scene_gr2_collection_manager = scene.gr2_collection_manager
        from .collection_manager import CreateCollections
        return CreateCollections(context, bpy.ops, bpy.data, scene_gr2_collection_manager.collection_type, scene_gr2_collection_manager.collection_name)

class GR2_HaloCollectionManagerPropertiesGroup(PropertyGroup):
    collection_type: EnumProperty(
        name="Collection Type",
        options=set(),
        description="Select the collection property you wish to apply to the selected objects",
        default='PERMUTATION',
        items=[
            ('BSP', 'BSP / Design', ''),
            ('REGION', 'Region', ''),
            ('PERMUTATION', 'Permutation', ''),
            ('EXCLUDE', 'Exclude', ''),
        ]
    )
    collection_name: StringProperty(
        name="Collection Name",
        description="Select the collection name you wish to apply to the selected objects",
        default='',
    )
    collection_special: BoolProperty(
        name="",
        description="Enable this property",
        default=False,
    )

class GR2_ArmatureCreator(Panel):
    bl_label = "Armature Creator"
    bl_idname = "HALO_PT_GR2_ArmatureCreator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GR2_AnimationTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_gr2_armature_creator = scene.gr2_armature_creator

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()
        col.prop(scene_gr2_armature_creator, 'armature_type', text='Type', expand=True)
        col = layout.column(heading="Include")
        sub = col.column(align=True)
        sub.prop(scene_gr2_armature_creator, 'control_rig', text='Control Rig')
        col = col.row()
        col.scale_y = 1.5
        col.operator('halo_gr2.armature_create')

class GR2_ArmatureCreator_Create(Operator):
    bl_idname = 'halo_gr2.armature_create'
    bl_label = 'Create Armature'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        scene_gr2_armature_creator = scene.gr2_armature_creator
        from .armature_creator import ArmatureCreate
        return ArmatureCreate(context, scene_gr2_armature_creator.armature_type, scene_gr2_armature_creator.control_rig)

class GR2_ArmatureCreatorPropertiesGroup(PropertyGroup):
    armature_type: EnumProperty(
        name="Armature Type",
        options=set(),
        description="",
        default='PEDESTAL',
        items=[
            ('PEDESTAL', 'Pedestal', ''),
            ('UNIT', 'Unit', ''),
        ]
    )
    control_rig: BoolProperty(
        name="Use Control Rig",
        description="",
        default=True,
        options=set()
    )

class GR2_CopyHaloProps(Panel):
    bl_label = "Copy Halo Properties"
    bl_idname = "HALO_PT_GR2_CopyHaloProps"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GR2_PropertiesManager"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()
        col.scale_y = 1.5
        col.operator('halo_gr2.props_copy')

class GR2_CopyHaloProps_Copy(Operator):
    bl_idname = 'halo_gr2.props_copy'
    bl_label = 'Copy Properties'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Copy Halo Properties from the active object to selected objects"

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 1

    def execute(self, context):
        from .copy_props import CopyProps
        return CopyProps(self.report, context.view_layer.objects.active, context.selected_objects)

class GR2_AMFHelper(Panel):
    bl_label = "AMF Helper"
    bl_idname = "HALO_PT_GR2_AMFHelper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GR2_PropertiesManager"

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()
        col.operator('halo_gr2.amf_assign')

class GR2_AMFHelper_Assign(Operator):
    bl_idname = 'halo_gr2.amf_assign'
    bl_label = 'Set Regions/Perms'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Sets regions and permutations for all scene objects which use the AMF naming convention [region:permutation]"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.object.type == 'MESH' and context.object.mode == 'OBJECT'

    def execute(self, context):
        from .amf_helper import amf_assign
        return amf_assign(context, self.report)

class GR2_JMSHelper(Panel):
    bl_label = "JMS Helper"
    bl_idname = "HALO_PT_GR2_JMSHelper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GR2_PropertiesManager"

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()
        col.operator('halo_gr2.jms_assign')

class GR2_JMSHelper_Assign(Operator):
    bl_idname = 'halo_gr2.jms_assign'
    bl_label = 'JMS -> GR2'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Splits the active object into it's face maps and assigns a new name for each new object to match the AMF naming convention, as well as setting the proper region & permutation. Collision and physics prefixes are retained"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.object.type == 'MESH' and context.object.mode == 'OBJECT'

    def execute(self, context):
        from .jms_helper import jms_assign
        return jms_assign(context, self.report)

class GR2_AnimationTools(Panel):
    bl_label = "Halo Animation Tools"
    bl_idname = "HALO_PT_GR2_AnimationTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GR2_AutoTools"

    def draw(self, context):
        layout = self.layout

class GR2_AnimationExportManager(Panel):
    bl_label = "Export Manager"
    bl_idname = "HALO_PT_GR2_AnimationExportManager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GR2_AnimationTools"

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()
        col.operator('halo_gr2.export_none')
        col.operator('halo_gr2.export_all')
        col.operator('halo_gr2.export_active')

class GR2_AnimationExport_None(Operator):
    bl_idname = 'halo_gr2.export_none'
    bl_label = 'None'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Turn off the export flag for every action in the scene"

    def execute(self, context):
        from .export_manager import set_export
        return set_export(context, self.report, 'none')

class GR2_AnimationExport_All(Operator):
    bl_idname = 'halo_gr2.export_all'
    bl_label = 'All'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Turn on the export flag for every action in the scene"

    def execute(self, context):
        from .export_manager import set_export
        return set_export(context, self.report, 'all')

class GR2_AnimationExport_Active(Operator):
    bl_idname = 'halo_gr2.export_active'
    bl_label = 'Only Active'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Enable the export flag for the current active active and toggle off the export flag for every other action in the scene"

    def execute(self, context):
        from .export_manager import set_export
        return set_export(context, self.report, 'active')

classeshalo = (
    GR2_Tools_Helper,
    GR2_HaloExport,
    GR2_HaloExport_Export,
    GR2_HaloExport_ExportQuick,
    GR2_HaloExportSettings,
    GR2_HaloExportSettingsExtended,
    GR2_HaloExportPropertiesGroup,
    GR2_HaloLauncher,
    GR2_HaloLauncherExplorerSettings,
    GR2_HaloLauncherGameSettings,
    GR2_HaloLauncherGamePruneSettings,
    GR2_HaloLauncherFoundationSettings,
    GR2_HaloLauncher_Foundation,
    GR2_HaloLauncher_Data,
    GR2_HaloLauncher_Tags,
    GR2_HaloLauncher_Sapien,
    GR2_HaloLauncher_TagTest,
    GR2_HaloLauncherPropertiesGroup,
    GR2_PropertiesManager,
    GR2_CollectionManager,
    GR2_CollectionManager_Create,
    GR2_HaloCollectionManagerPropertiesGroup,
    GR2_CopyHaloProps,
    GR2_CopyHaloProps_Copy,
    GR2_ShaderFinder,
    GR2_ShaderFinder_Find,
    GR2_HaloShaderFinderPropertiesGroup,
    GR2_GraphPath,
    GR2_SetFrameIDs,
    GR2_SetFrameIDsOp,
    GR2_ResetFrameIDsOp,
    GR2_SetFrameIDsPropertiesGroup,
    GR2_AMFHelper,
    GR2_AMFHelper_Assign,
    GR2_JMSHelper,
    GR2_JMSHelper_Assign,
    GR2_AnimationTools,
    GR2_ArmatureCreator,
    GR2_ArmatureCreator_Create,
    GR2_ArmatureCreatorPropertiesGroup,
    # GR2_AnimationExportManager,
    # GR2_AnimationExport_None,
    # GR2_AnimationExport_All,
    # GR2_AnimationExport_Active,
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.Scene.gr2_frame_ids = PointerProperty(type=GR2_SetFrameIDsPropertiesGroup, name="Halo Frame ID Getter", description="Gets Frame IDs")
    bpy.types.Scene.gr2_halo_launcher = PointerProperty(type=GR2_HaloLauncherPropertiesGroup, name="Halo Launcher", description="Launches stuff")
    bpy.types.Scene.gr2_shader_finder = PointerProperty(type=GR2_HaloShaderFinderPropertiesGroup, name="Shader Finder", description="Find Shaders")
    bpy.types.Scene.gr2_export = PointerProperty(type=GR2_HaloExportPropertiesGroup, name="Halo Export", description="")
    bpy.types.Scene.gr2_collection_manager = PointerProperty(type=GR2_HaloCollectionManagerPropertiesGroup, name="Collection Manager", description="")
    bpy.types.Scene.gr2_armature_creator = PointerProperty(type=GR2_ArmatureCreatorPropertiesGroup, name="Halo Armature", description="")
    
def unregister():
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
    
