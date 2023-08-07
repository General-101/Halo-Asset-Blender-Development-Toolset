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

from enum import Flag, Enum, auto
from mathutils import Vector, Euler

SALT_SIZE = 32

class ScenarioTypeEnum(Enum):
    solo = 0
    multiplayer = auto()
    mainmenu = auto()
    multiplayer_shared = auto()
    single_player_shared = auto()

class ScenarioFlags(Flag):
    cortana_hack = auto()
    always_draw_sky = auto()
    dont_strip_pathfinding = auto()
    symmetric_multiplayer_map = auto()
    quick_loading_cinematic_only_scenario = auto()
    characters_use_previous_mission_weapons = auto()
    lightmaps_smooth_palettes_with_neighbors = auto()
    snap_to_white_at_start = auto()
    do_not_apply_bungie_mp_tag_patches = auto()

class ResourceTypeEnum(Enum):
    bitmap = 0
    sound = auto()
    render_model_geometry = auto()
    cluster_geometry = auto()
    cluster_instanced_geometry = auto()
    lightmap_geometry_object_buckets = auto()
    lightmap_geometry_instance_buckets = auto()
    lightmap_cluster_bitmaps = auto()
    lightmap_instance_bitmaps = auto()

class FunctionFlags(Flag):
    scripted = auto()
    invert = auto()
    additive = auto()
    always_active = auto()

class FunctionEnum(Enum):
    one = 0
    zero = auto()
    cosine = auto()
    cosine_variable_period = auto()
    diagonal_wave = auto()
    diagonal_wave_variable_period = auto()
    slide = auto()
    slide_variable_period = auto()
    noise = auto()
    jitter = auto()
    wander = auto()
    spark = auto()

class MapEnum(Enum):
    linear = 0
    early = auto()
    very_early = auto()
    late = auto()
    very_late = auto()
    cosine = auto()
    one = auto()
    zero = auto()

class BoundsModeEnum(Enum):
    clip = 0
    clip_and_normalize = auto()
    scale_to_fit = auto()

class ObjectFlags(Flag):
    not_automatically = auto()
    unused_0 = auto()
    unused_1 = auto()
    unused_2 = auto()
    lock_type_to_env_object = auto()
    lock_transform_to_env_object = auto()
    never_placed = auto()
    lock_name_to_env_object = auto()
    create_at_rest = auto()

class TeamDesignatorEnum(Enum):
    alpha = 0
    bravo = auto()
    charlie = auto()
    delta = auto()
    echo = auto()
    foxtrot = auto()
    golf = auto()
    hotel = auto()
    neutral = auto()

class GametypeEnum(Enum):
    none = 0
    ctf = auto()
    slayer = auto()
    oddball = auto()
    king_of_the_hill = auto()
    race = auto()
    headhunter = auto()
    juggernaut = auto()
    territories = auto()
    assault = auto()
    stub = auto()
    ignored1 = auto()
    all_games = auto()
    all_except_ctf = auto()
    all_except_race_and_ctf = auto()
    medic = auto()
    vip = auto()
    infection = auto()

class NetGameEnum(Enum):
    ctf_flag_spawn = 0
    ctf_flag_return = auto()
    assault_bomb_spawn = auto()
    assault_bomb_return = auto()
    oddball_spawn = auto()
    unused = auto()
    race_checkpoint = auto()
    teleporter_src = auto()
    teleporter_dest = auto()
    headhunter_bin = auto()
    territories_flag = auto()
    king_of_the_hill_0 = auto()
    king_of_the_hill_1 = auto()
    king_of_the_hill_2 = auto()
    king_of_the_hill_3 = auto()
    king_of_the_hill_4 = auto()
    king_of_the_hill_5 = auto()
    king_of_the_hill_6 = auto()
    king_of_the_hill_7 = auto()

class NetGameFlags(Flag):
    multi_flag_bomb = auto()
    single_flag_bomb = auto()
    neutral_flag_bomb = auto()

class RespawnTimerStartsEnum(Enum):
    on_pick_up = 0
    on_body_depletion = auto()

class ClassificationEnum(Enum):
    weapon = 0
    primary_light_land = auto()
    secondary_light_land = auto()
    primary_heavy_land = auto()
    primary_flying = auto()
    secondary_heavy_land = auto()
    primary_turret = auto()
    secondary_turret = auto()
    grenade = auto()
    powerup = auto()

class StartingEquipment(Flag):
    no_grenades = auto()
    plasma_grenades = auto()

class ScenarioAsset():
    def __init__(self):
        self.header = None
        self.scenario_body_header = None
        self.scenario_body = None
        self.skies_header = None
        self.skies = None
        self.child_scenario_header = None
        self.child_scenarios = None
        self.comment_header = None
        self.comments = None
        self.object_name_header = None
        self.object_names = None
        self.scenery_header = None
        self.scenery = None
        self.scenery_palette_header = None
        self.scenery_palette = None
        self.bipeds_header = None
        self.bipeds = None
        self.biped_palette_header = None
        self.biped_palette = None
        self.vehicles_header = None
        self.vehicles = None
        self.vehicle_palette_header = None
        self.vehicle_palette = None
        self.equipment_header = None
        self.equipment = None
        self.equipment_palette_header = None
        self.equipment_palette = None
        self.weapon_header = None
        self.weapons = None
        self.weapon_palette_header = None
        self.weapon_palette = None
        self.device_group_header = None
        self.device_groups = None
        self.device_machine_header = None
        self.device_machines = None
        self.device_machine_palette_header = None
        self.device_machine_palette = None
        self.device_control_header = None
        self.device_controls = None
        self.device_control_palette_header = None
        self.device_control_palette = None
        self.light_fixture_header = None
        self.light_fixtures = None
        self.light_fixture_palette_header = None
        self.light_fixtures_palette = None
        self.sound_scenery_header = None
        self.sound_scenery = None
        self.sound_scenery_palette_header = None
        self.sound_scenery_palette = None
        self.light_volume_header = None
        self.light_volumes = None
        self.light_volume_palette_header = None
        self.light_volume_palette = None
        self.player_starting_profile_header = None
        self.player_starting_profiles = None
        self.player_starting_location_header = None
        self.player_starting_locations = None
        self.trigger_volumes_header = None
        self.trigger_volumes = None
        self.recorded_animation_header = None
        self.recorded_animations = None
        self.netgame_flag_header = None
        self.netgame_flags = None
        self.netgame_equipment_header = None
        self.netgame_equipment = None
        self.starting_equipment_header = None
        self.starting_equipment = None
        self.decals_header = None
        self.decals = None
        self.decal_palette_header = None
        self.decal_palette = None
        self.style_palette_header = None
        self.style_palette = None
        self.squad_groups_header = None
        self.squad_groups = None
        self.squads_header = None
        self.squads = None
        self.zones_header = None
        self.zones = None
        self.character_palette_header = None
        self.character_palette = None
        self.scripting_data_header = None
        self.scripting_data = None
        self.cutscene_flags_header = None
        self.cutscene_flags = None
        self.cutscene_camera_points_header = None
        self.cutscene_camera_points = None
        self.cutscene_titles_header = None
        self.cutscene_titles = None
        self.structure_bsp_header = None
        self.structure_bsp = None
        self.orders_header = None
        self.orders = None
        self.triggers_header = None
        self.triggers = None
        self.background_sound_palette_header = None
        self.background_sound_palette = None
        self.sound_environment_palette_header = None
        self.sound_environment_palette = None
        self.crates_header = None
        self.crates = None
        self.crates_palette_header = None
        self.crates_palette = None

    class ScenarioBody:
        def __init__(self, unused_tag_ref=None, skies_tag_block=None, scenario_type=0, scenario_flags=0, child_scenarios_tag_block=None, local_north=0.0,
                     predicted_resources_tag_block=None, functions_tag_block=None, editor_scenario_data=0, comments_tag_block=None, environment_objects_tag_block=None,
                     object_names_tag_block=None, scenery_tag_block=None, scenery_palette_tag_block=None, bipeds_tag_block=None, biped_palette_tag_block=None,
                     vehicles_tag_block=None, vehicle_palette_tag_block=None, equipment_tag_block=None, equipment_palette_tag_block=None, weapons_tag_block=None,
                     weapon_palette_tag_block=None, device_groups_tag_block=None, machines_tag_block=None, machine_palette_tag_block=None, controls_tag_block=None,
                     control_palette_tag_block=None, light_fixtures_tag_block=None, light_fixtures_palette_tag_block=None, sound_scenery_tag_block=None,
                     sound_scenery_palette_tag_block=None, light_volumes_tag_block=None, light_volume_palette_tag_block=None, player_starting_profile_tag_block=None,
                     player_starting_locations_tag_block=None, trigger_volumes_tag_block=None, recorded_animations_tag_block=None, netgame_flags_tag_block=None,
                     netgame_equipment_tag_block=None, starting_equipment_tag_block=None, bsp_switch_trigger_volumes_tag_block=None, decals_tag_block=None,
                     decal_palette_tag_block=None, detail_object_collection_palette_tag_block=None, style_palette_tag_block=None, squad_groups_tag_block=None,
                     squads_tag_block=None, zones_tag_block=None, mission_scenes_tag_block=None, character_palette_tag_block=None, ai_pathfinding_data_tag_block=None,
                     ai_animation_references_tag_block=None, ai_script_references_tag_block=None, ai_recording_references_tag_block=None, ai_conversations_tag_block=None,
                     script_syntax_data_tag_data=None, script_string_data_tag_data=None, scripts_tag_block=None, globals_tag_block=None, references_tag_block=None,
                     source_files_tag_block=None, scripting_data_tag_block=None, cutscene_flags_tag_block=None, cutscene_camera_points_tag_block=None,
                     cutscene_titles_tag_block=None, custom_object_names_tag_ref=None, chapter_title_text_tag_ref=None, hud_messages_tag_ref=None,
                     structure_bsps_tag_block=None, scenario_resources_tag_block=None, old_structure_physics_tag_block=None, hs_unit_seats_tag_block=None,
                     scenario_kill_triggers_tag_block=None, hs_syntax_datums_tag_block=None, orders_tag_block=None, triggers_tag_block=None,
                     background_sound_palette_tag_block=None, sound_environment_palette_tag_block=None, weather_palette_tag_block=None, unused_0_tag_block=None,
                     unused_1_tag_block=None, unused_2_tag_block=None, unused_3_tag_block=None, scavenger_hunt_objects_tag_block=None, scenario_cluster_data_tag_block=None,
                     salt_array=None, spawn_data_tag_block=None, sound_effect_collection_tag_ref=None, crates_tag_block=None, crate_palette_tag_block=None,
                     global_lighting_tag_ref=None, atmospheric_fog_palette_tag_block=None, planar_fog_palette_tag_block=None, flocks_tag_block=None, subtitles_tag_ref=None,
                     decorators_tag_block=None, creatures_tag_block=None, creature_palette_tag_block=None, decorator_palette_tag_block=None,
                     bsp_transition_volumes_tag_block=None, structure_bsp_lighting_tag_block=None, editor_folders_tag_block=None, level_data_tag_block=None,
                     game_engine_strings_tag_ref=None, mission_dialogue_tag_block=None, objectives_tag_ref=None, interpolators_tag_block=None, shared_references_tag_block=None,
                     screen_effect_references_tag_block=None, simulation_definition_table_tag_block=None):
            self.unused_tag_ref = unused_tag_ref
            self.skies_tag_block = skies_tag_block
            self.scenario_type = scenario_type
            self.scenario_flags = scenario_flags
            self.child_scenarios_tag_block = child_scenarios_tag_block
            self.local_north = local_north
            self.predicted_resources_tag_block = predicted_resources_tag_block
            self.functions_tag_block = functions_tag_block
            self.editor_scenario_data = editor_scenario_data
            self.comments_tag_block = comments_tag_block
            self.environment_objects_tag_block = environment_objects_tag_block
            self.object_names_tag_block = object_names_tag_block
            self.scenery_tag_block = scenery_tag_block
            self.scenery_palette_tag_block = scenery_palette_tag_block
            self.bipeds_tag_block = bipeds_tag_block
            self.biped_palette_tag_block = biped_palette_tag_block
            self.vehicles_tag_block = vehicles_tag_block
            self.vehicle_palette_tag_block = vehicle_palette_tag_block
            self.equipment_tag_block = equipment_tag_block
            self.equipment_palette_tag_block = equipment_palette_tag_block
            self.weapons_tag_block = weapons_tag_block
            self.weapon_palette_tag_block = weapon_palette_tag_block
            self.device_groups_tag_block = device_groups_tag_block
            self.machines_tag_block = machines_tag_block
            self.machine_palette_tag_block = machine_palette_tag_block
            self.controls_tag_block = controls_tag_block
            self.control_palette_tag_block = control_palette_tag_block
            self.light_fixtures_tag_block = light_fixtures_tag_block
            self.light_fixtures_palette_tag_block = light_fixtures_palette_tag_block
            self.sound_scenery_tag_block = sound_scenery_tag_block
            self.sound_scenery_palette_tag_block = sound_scenery_palette_tag_block
            self.light_volumes_tag_block = light_volumes_tag_block
            self.light_volume_palette_tag_block = light_volume_palette_tag_block
            self.player_starting_profile_tag_block = player_starting_profile_tag_block
            self.player_starting_locations_tag_block = player_starting_locations_tag_block
            self.trigger_volumes_tag_block = trigger_volumes_tag_block
            self.recorded_animations_tag_block = recorded_animations_tag_block
            self.netgame_flags_tag_block = netgame_flags_tag_block
            self.netgame_equipment_tag_block = netgame_equipment_tag_block
            self.starting_equipment_tag_block = starting_equipment_tag_block
            self.bsp_switch_trigger_volumes_tag_block = bsp_switch_trigger_volumes_tag_block
            self.decals_tag_block = decals_tag_block
            self.decal_palette_tag_block = decal_palette_tag_block
            self.detail_object_collection_palette_tag_block = detail_object_collection_palette_tag_block
            self.style_palette_tag_block = style_palette_tag_block
            self.squad_groups_tag_block = squad_groups_tag_block
            self.squads_tag_block = squads_tag_block
            self.zones_tag_block = zones_tag_block
            self.mission_scenes_tag_block = mission_scenes_tag_block
            self.character_palette_tag_block = character_palette_tag_block
            self.ai_pathfinding_data_tag_block = ai_pathfinding_data_tag_block
            self.ai_animation_references_tag_block = ai_animation_references_tag_block
            self.ai_script_references_tag_block = ai_script_references_tag_block
            self.ai_recording_references_tag_block = ai_recording_references_tag_block
            self.ai_conversations_tag_block = ai_conversations_tag_block
            self.script_syntax_data_tag_data = script_syntax_data_tag_data
            self.script_string_data_tag_data = script_string_data_tag_data
            self.scripts_tag_block = scripts_tag_block
            self.globals_tag_block = globals_tag_block
            self.references_tag_block = references_tag_block
            self.source_files_tag_block = source_files_tag_block
            self.scripting_data_tag_block = scripting_data_tag_block
            self.cutscene_flags_tag_block = cutscene_flags_tag_block
            self.cutscene_camera_points_tag_block = cutscene_camera_points_tag_block
            self.cutscene_titles_tag_block = cutscene_titles_tag_block
            self.custom_object_names_tag_ref = custom_object_names_tag_ref
            self.chapter_title_text_tag_ref = chapter_title_text_tag_ref
            self.hud_messages_tag_ref = hud_messages_tag_ref
            self.structure_bsps_tag_block = structure_bsps_tag_block
            self.scenario_resources_tag_block = scenario_resources_tag_block
            self.old_structure_physics_tag_block = old_structure_physics_tag_block
            self.hs_unit_seats_tag_block = hs_unit_seats_tag_block
            self.scenario_kill_triggers_tag_block = scenario_kill_triggers_tag_block
            self.hs_syntax_datums_tag_block = hs_syntax_datums_tag_block
            self.orders_tag_block = orders_tag_block
            self.triggers_tag_block = triggers_tag_block
            self.background_sound_palette_tag_block = background_sound_palette_tag_block
            self.sound_environment_palette_tag_block = sound_environment_palette_tag_block
            self.weather_palette_tag_block = weather_palette_tag_block
            self.unused_0_tag_block = unused_0_tag_block
            self.unused_1_tag_block = unused_1_tag_block
            self.unused_2_tag_block = unused_2_tag_block
            self.unused_3_tag_block = unused_3_tag_block
            self.scavenger_hunt_objects_tag_block = scavenger_hunt_objects_tag_block
            self.scenario_cluster_data_tag_block = scenario_cluster_data_tag_block
            self.salt_array = salt_array
            self.spawn_data_tag_block = spawn_data_tag_block
            self.sound_effect_collection_tag_ref = sound_effect_collection_tag_ref
            self.crates_tag_block = crates_tag_block
            self.crate_palette_tag_block = crate_palette_tag_block
            self.global_lighting_tag_ref = global_lighting_tag_ref
            self.atmospheric_fog_palette_tag_block = atmospheric_fog_palette_tag_block
            self.planar_fog_palette_tag_block = planar_fog_palette_tag_block
            self.flocks_tag_block = flocks_tag_block
            self.subtitles_tag_ref = subtitles_tag_ref
            self.decorators_tag_block = decorators_tag_block
            self.creatures_tag_block = creatures_tag_block
            self.creature_palette_tag_block = creature_palette_tag_block
            self.decorator_palette_tag_block = decorator_palette_tag_block
            self.bsp_transition_volumes_tag_block = bsp_transition_volumes_tag_block
            self.structure_bsp_lighting_tag_block = structure_bsp_lighting_tag_block
            self.editor_folders_tag_block = editor_folders_tag_block
            self.level_data_tag_block = level_data_tag_block
            self.game_engine_strings_tag_ref = game_engine_strings_tag_ref
            self.mission_dialogue_tag_block = mission_dialogue_tag_block
            self.objectives_tag_ref = objectives_tag_ref
            self.interpolators_tag_block = interpolators_tag_block
            self.shared_references_tag_block = shared_references_tag_block
            self.screen_effect_references_tag_block = screen_effect_references_tag_block
            self.simulation_definition_table_tag_block = simulation_definition_table_tag_block

    class Comment:
        def __init__(self, position=Vector(), type=0, name="", comment=""):
            self.position = position
            self.type = type
            self.name = name
            self.comment = comment

    class ObjectName:
        def __init__(self, name="", object_type=0, placement_index=0):
            self.name = name
            self.object_type = object_type
            self.placement_index = placement_index

    class Object:
        def __init__(self, palette_index=0, name_index=0, placement_flags=0, position=Vector(), rotation=Euler(), scale=0.0, transform_flags=0, manual_bsp_flags=0, unique_id=0,
                     origin_bsp_index=0, object_type=0, source=0, bsp_policy=0, editor_folder_index=0):
            self.palette_index = palette_index
            self.name_index = name_index
            self.placement_flags = placement_flags
            self.position = position
            self.rotation = rotation
            self.scale = scale
            self.transform_flags = transform_flags
            self.manual_bsp_flags = manual_bsp_flags
            self.unique_id = unique_id
            self.origin_bsp_index = origin_bsp_index
            self.object_type = object_type
            self.source = source
            self.bsp_policy = bsp_policy
            self.editor_folder_index = editor_folder_index

    class Scenery(Object):
        def __init__(self, sobj_header=None, obj0_header=None, sper_header=None, sct3_header=None, variant_name="", variant_name_length=0, active_change_colors=0,
                     primary_color_BGRA=(0, 0, 0, 255), secondary_color_BGRA=(0, 0, 0, 255), tertiary_color_BGRA=(0, 0, 0, 255),
                     quaternary_color_BGRA=(0, 0, 0, 255), pathfinding_policy=0, lightmap_policy=0, pathfinding_references_header=None, pathfinding_references=None,
                     valid_multiplayer_games=0):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.sper_header = sper_header
            self.sct3_header = sct3_header
            self.variant_name = variant_name
            self.variant_name_length = variant_name_length
            self.active_change_colors = active_change_colors
            self.primary_color_BGRA = primary_color_BGRA
            self.secondary_color_BGRA = secondary_color_BGRA
            self.tertiary_color_BGRA = tertiary_color_BGRA
            self.quaternary_color_BGRA = quaternary_color_BGRA
            self.pathfinding_policy = pathfinding_policy
            self.lightmap_policy = lightmap_policy
            self.pathfinding_references_header = pathfinding_references_header
            self.pathfinding_references = pathfinding_references
            self.valid_multiplayer_games = valid_multiplayer_games

    class Unit(Object):
        def __init__(self, sobj_header=None, obj0_header=None, sper_header=None, sunt_header=None, variant_name="", variant_name_length=0, active_change_colors=0,
                     primary_color_BGRA=(0, 0, 0, 255), secondary_color_BGRA=(0, 0, 0, 255), tertiary_color_BGRA=(0, 0, 0, 255),
                     quaternary_color_BGRA=(0, 0, 0, 255), body_vitality=0.0, flags=0):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.sper_header = sper_header
            self.sunt_header = sunt_header
            self.variant_name = variant_name
            self.variant_name_length = variant_name_length
            self.active_change_colors = active_change_colors
            self.primary_color_BGRA = primary_color_BGRA
            self.secondary_color_BGRA = secondary_color_BGRA
            self.tertiary_color_BGRA = tertiary_color_BGRA
            self.quaternary_color_BGRA = quaternary_color_BGRA
            self.body_vitality = body_vitality
            self.flags = flags

    class Equipment(Object):
        def __init__(self, sobj_header=None, obj0_header=None, seqt_header=None, flags=0):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.seqt_header = seqt_header
            self.flags = flags

    class Weapon(Object):
        def __init__(self, sobj_header=None, obj0_header=None, sper_header=None, swpt_header=None, variant_name="", variant_name_length=0, active_change_colors=0,
                     primary_color_BGRA=(0, 0, 0, 255), secondary_color_BGRA=(0, 0, 0, 255), tertiary_color_BGRA=(0, 0, 0, 255),
                     quaternary_color_BGRA=(0, 0, 0, 255), rounds_left=0, rounds_loaded=0, flags=0):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.sper_header = sper_header
            self.swpt_header = swpt_header
            self.variant_name = variant_name
            self.variant_name_length = variant_name_length
            self.active_change_colors = active_change_colors
            self.primary_color_BGRA = primary_color_BGRA
            self.secondary_color_BGRA = secondary_color_BGRA
            self.tertiary_color_BGRA = tertiary_color_BGRA
            self.quaternary_color_BGRA = quaternary_color_BGRA
            self.rounds_left = rounds_left
            self.rounds_loaded = rounds_loaded
            self.flags = flags

    class DeviceGroup():
        def __init__(self, name="", initial_value=0.0, flags=0):
            self.name = name
            self.initial_value = initial_value
            self.flags = flags

    class DeviceMachine(Object):
        def __init__(self, sobj_header=None, obj0_header=None, sdvt_header=None, smht_header=None, power_group_index=0, position_group_index=0, flags_0=0,
                     flags_1=0, pathfinding_references_header=None, pathfinding_references=None):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.sdvt_header = sdvt_header
            self.smht_header = smht_header
            self.power_group_index = power_group_index
            self.position_group_index = position_group_index
            self.flags_0 = flags_0
            self.flags_1 = flags_1
            self.pathfinding_references_header = pathfinding_references_header
            self.pathfinding_references = pathfinding_references

    class DeviceControl(Object):
        def __init__(self, sobj_header=None, obj0_header=None, sdvt_header=None, sctt_header=None, power_group_index=0, position_group_index=0, flags_0=0,
                     flags_1=0, unk=0):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.sdvt_header = sdvt_header
            self.sctt_header = sctt_header
            self.power_group_index = power_group_index
            self.position_group_index = position_group_index
            self.flags_0 = flags_0
            self.flags_1 = flags_1
            self.unk = unk

    class LightFixture(Object):
        def __init__(self, sobj_header=None, obj0_header=None, sdvt_header=None, slft_header=None, power_group_index=0, position_group_index=0, flags=0,
                     color_RGBA=(0, 0, 0, 255), intensity=0.0, falloff_angle=0.0, cutoff_angle=0.0):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.sdvt_header = sdvt_header
            self.slft_header = slft_header
            self.power_group_index = power_group_index
            self.position_group_index = position_group_index
            self.flags = flags
            self.color_RGBA = color_RGBA
            self.intensity = intensity
            self.falloff_angle = falloff_angle
            self.cutoff_angle = cutoff_angle

    class SoundScenery(Object):
        def __init__(self, sobj_header=None, obj0_header=None, _sc__header=None, volume_type=0, height=0.0, override_distance_bounds=(0.0, 0.0), override_core_angle_bounds=(0.0, 0.0),
                     override_outer_core_gain=0.0):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self._sc__header = _sc__header
            self.volume_type = volume_type
            self.height = height
            self.override_distance_bounds = override_distance_bounds
            self.override_core_angle_bounds = override_core_angle_bounds
            self.override_outer_core_gain = override_outer_core_gain

    class LightVolume(Object):
        def __init__(self, sobj_header=None, obj0_header=None, sdvt_header=None, slit_header=None, power_group_index=0, position_group_index=0, flags_0=0,
                     shape_type=0, flags_1=0, lightmap_type=0, lightmap_flags=0, lightmap_half_life=0.0, lightmap_light_scale=0.0, target_point=Vector(), width=0.0,
                     height_scale=0.0, field_of_view=0.0, falloff_distance=0.0, cutoff_distance=0.0):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.sdvt_header = sdvt_header
            self.slit_header = slit_header
            self.power_group_index = power_group_index
            self.position_group_index = position_group_index
            self.flags_0 = flags_0
            self.shape_type = shape_type
            self.flags_1 = flags_1
            self.lightmap_type = lightmap_type
            self.lightmap_flags = lightmap_flags
            self.lightmap_half_life = lightmap_half_life
            self.lightmap_light_scale = lightmap_light_scale
            self.target_point = target_point
            self.width = width
            self.height_scale = height_scale
            self.field_of_view = field_of_view
            self.falloff_distance = falloff_distance
            self.cutoff_distance = cutoff_distance

    class PlayerStartingProfile():
        def __init__(self, name="", starting_health_damage=0.0, starting_shield_damage=0.0, primary_weapon_tag_ref=None, primary_rounds_loaded=0, primary_rounds_total=0,
                     secondary_weapon_tag_ref=None, secondary_rounds_loaded=0, secondary_rounds_total=0, starting_fragmentation_grenades_count=0,
                     starting_plasma_grenade_count=0, starting_custom_2_grenade_count=0, starting_custom_3_grenade_count=0):
            super().__init__()
            self.name = name
            self.starting_health_damage = starting_health_damage
            self.starting_shield_damage = starting_shield_damage
            self.primary_weapon_tag_ref = primary_weapon_tag_ref
            self.primary_rounds_loaded = primary_rounds_loaded
            self.primary_rounds_total = primary_rounds_total
            self.secondary_weapon_tag_ref = secondary_weapon_tag_ref
            self.secondary_rounds_loaded = secondary_rounds_loaded
            self.secondary_rounds_total = secondary_rounds_total
            self.starting_fragmentation_grenades_count = starting_fragmentation_grenades_count
            self.starting_plasma_grenade_count = starting_plasma_grenade_count
            self.starting_custom_2_grenade_count = starting_custom_2_grenade_count
            self.starting_custom_3_grenade_count = starting_custom_3_grenade_count

    class PlayerStartingLocation():
        def __init__(self, position=Vector(), facing=0.0, team_designator=0, bsp_index=0, type_0=0, type_1=0, type_2=0, type_3=0, spawn_type_0=0, spawn_type_1=0,
                     spawn_type_2=0, spawn_type_3=0, unk_0="", unk_1="", unk_0_length=0, unk_1_length=0, campaign_player_type=0):
            super().__init__()
            self.position = position
            self.facing = facing
            self.team_designator = team_designator
            self.bsp_index = bsp_index
            self.type_0 = type_0
            self.type_1 = type_1
            self.type_2 = type_2
            self.type_3 = type_3
            self.spawn_type_0 = spawn_type_0
            self.spawn_type_1 = spawn_type_1
            self.spawn_type_2 = spawn_type_2
            self.spawn_type_3 = spawn_type_3
            self.unk_0 = unk_0
            self.unk_1 = unk_1
            self.unk_0_length = unk_0_length
            self.unk_1_length = unk_1_length
            self.campaign_player_type = campaign_player_type

    class TriggerVolume():
        def __init__(self, name="", name_length=0, object_name_index=0, node_name="", node_name_length=0, forward=Vector(), up=Vector(), position=Vector(), extents=Vector(),
                     kill_trigger_volume_index=0):
            self.name = name
            self.name_length = name_length
            self.object_name_index = object_name_index
            self.node_name = node_name
            self.node_name_length = node_name_length
            self.forward = forward
            self.up = up
            self.position = position
            self.extents = extents
            self.kill_trigger_volume_index = kill_trigger_volume_index

    class RecordedAnimation():
        def __init__(self, name="", version=0, raw_animation_data=0, unit_control_data_version=0, length_of_animation=0, recorded_animation_event_stream_tag_data=None,
                     recorded_animation_event_stream=None):
            self.name = name
            self.version = version
            self.raw_animation_data = raw_animation_data
            self.unit_control_data_version = unit_control_data_version
            self.length_of_animation = length_of_animation
            self.recorded_animation_event_stream_tag_data = recorded_animation_event_stream_tag_data
            self.recorded_animation_event_stream = recorded_animation_event_stream

    class NetGameFlag():
        def __init__(self, position=Vector(), facing=0.0, type=0, team_designator=0, identifer=0, flags=0, spawn_object_name="", spawn_object_name_length=0, spawn_marker_name="",
                     spawn_marker_name_length=0):
            self.position = position
            self.facing = facing
            self.type = type
            self.team_designator = team_designator
            self.identifer = identifer
            self.flags = flags
            self.spawn_object_name = spawn_object_name
            self.spawn_object_name_length = spawn_object_name_length
            self.spawn_marker_name = spawn_marker_name
            self.spawn_marker_name_length = spawn_marker_name_length

    class NetGameEquipment():
        def __init__(self, ntor_header=None, flags=0, type_0=0, type_1=0, type_2=0, type_3=0, spawn_time=0, respawn_on_empty_time=0, respawn_timer_starts=0, classification=0,
                     position=Vector(), orientation=Euler(), item_vehicle_collection=None):
            self.ntor_header = ntor_header
            self.flags = flags
            self.type_0 = type_0
            self.type_1 = type_1
            self.type_2 = type_2
            self.type_3 = type_3
            self.spawn_time = spawn_time
            self.respawn_on_empty_time = respawn_on_empty_time
            self.respawn_timer_starts = respawn_timer_starts
            self.classification = classification
            self.position = position
            self.orientation = orientation
            self.item_vehicle_collection = item_vehicle_collection

    class StartingEquipment():
        def __init__(self, flags=0, type_0=0, type_1=0, type_2=0, type_3=0, item_collection_1=None, item_collection_2=None, item_collection_3=None, item_collection_4=None,
                     item_collection_5=None, item_collection_6=None):
            self.flags = flags
            self.type_0 = type_0
            self.type_1 = type_1
            self.type_2 = type_2
            self.type_3 = type_3
            self.item_collection_1 = item_collection_1
            self.item_collection_2 = item_collection_2
            self.item_collection_3 = item_collection_3
            self.item_collection_4 = item_collection_4
            self.item_collection_5 = item_collection_5
            self.item_collection_6 = item_collection_6

    class Decal():
        def __init__(self, palette_index=0, yaw=0, pitch=0, position=Vector()):
            self.palette_index = palette_index
            self.yaw = yaw
            self.pitch = pitch
            self.position = position

    class SquadGroups():
        def __init__(self, name="", parent_index=0, initial_order_index=0):
            self.name = name
            self.parent_index = parent_index
            self.initial_order_index = initial_order_index

    class Squad():
        def __init__(self, name="", flags=0, team=0, parent_squad_group_index=0, squad_delay_time=0.0, normal_difficulty_count=0, insane_difficulty_count=0, major_upgrade=0,
                     vehicle_type_index=0, character_type_index=0, initial_zone_index=0, initial_weapon_index=0, initial_secondary_weapon_index=0, grenade_type=0,
                     initial_order_index=0, vehicle_variant="", starting_locations_tag_block=None, placement_script="", starting_locations_header=None, starting_locations=None):
            self.name = name
            self.flags = flags
            self.team = team
            self.parent_squad_group_index = parent_squad_group_index
            self.squad_delay_time = squad_delay_time
            self.normal_difficulty_count = normal_difficulty_count
            self.insane_difficulty_count = insane_difficulty_count
            self.major_upgrade = major_upgrade
            self.vehicle_type_index = vehicle_type_index
            self.character_type_index = character_type_index
            self.initial_zone_index = initial_zone_index
            self.initial_weapon_index = initial_weapon_index
            self.initial_secondary_weapon_index = initial_secondary_weapon_index
            self.grenade_type = grenade_type
            self.initial_order_index = initial_order_index
            self.vehicle_variant = vehicle_variant
            self.starting_locations_tag_block = starting_locations_tag_block
            self.placement_script = placement_script
            self.starting_locations_header = starting_locations_header
            self.starting_locations = starting_locations

    class StartingLocation():
        def __init__(self, name="", name_length=0, position=Vector(), reference_frame=0, facing_y=0.0, facing_p=0.0, flags=0, character_type_index=0,
                     initial_weapon_index=0, initial_secondary_weapon_index=0, vehicle_type_index=0, seat_type=0, grenade_type=0, swarm_count=0,
                     actor_variant="", vehicle_variant="", initial_movement_distance=0, emitter_vehicle_index=0, initial_movement_mode=0,
                     placement_script=""):
            self.name = name
            self.name_length = name_length
            self.position = position
            self.reference_frame = reference_frame
            self.facing_y = facing_y
            self.facing_p = facing_p
            self.flags = flags
            self.character_type_index = character_type_index
            self.initial_weapon_index = initial_weapon_index
            self.initial_secondary_weapon_index = initial_secondary_weapon_index
            self.vehicle_type_index = vehicle_type_index
            self.seat_type = seat_type
            self.grenade_type = grenade_type
            self.swarm_count = swarm_count
            self.actor_variant = actor_variant
            self.vehicle_variant = vehicle_variant
            self.initial_movement_distance = initial_movement_distance
            self.emitter_vehicle_index = emitter_vehicle_index
            self.initial_movement_mode = initial_movement_mode
            self.placement_script = placement_script

    class Zone():
        def __init__(self, name="", flags=0, manual_bsp_index=0, firing_positions_tag_block=None, areas_tag_block=None, firing_positions_header=None, areas_header=None,
                     firing_positions=None, areas=None):
            self.name = name
            self.flags = flags
            self.manual_bsp_index = manual_bsp_index
            self.firing_positions_tag_block = firing_positions_tag_block
            self.areas_tag_block = areas_tag_block
            self.firing_positions_header = firing_positions_header
            self.areas_header = areas_header
            self.firing_positions = firing_positions
            self.areas = areas

    class FiringPosition():
        def __init__(self, position=Vector(), reference_frame=0, flags=0, area_index=0, cluster_index=0, normal_y=0.0, normal_p=0.0):
            self.position = position
            self.reference_frame = reference_frame
            self.flags = flags
            self.area_index = area_index
            self.cluster_index = cluster_index
            self.normal_y = normal_y
            self.normal_p = normal_p

    class Area():
        def __init__(self, name="", flags=0, runtime_starting_index=0, runtime_count=0, manual_reference_frame=0, flight_hints_tag_block=None, flight_hints_header=None,
                     flight_hints=None):
            self.name = name
            self.flags = flags
            self.runtime_starting_index = runtime_starting_index
            self.runtime_count = runtime_count
            self.manual_reference_frame = manual_reference_frame
            self.flight_hints_tag_block = flight_hints_tag_block
            self.flight_hints_header = flight_hints_header
            self.flight_hints = flight_hints

    class ScriptingData():
        def __init__(self, point_sets_tag_block=None, point_sets_header=None, point_sets=None):
            self.point_sets_tag_block = point_sets_tag_block
            self.point_sets_header = point_sets_header
            self.point_sets = point_sets

    class PointSet():
        def __init__(self, name="", points_tag_block=None, bsp_index=0, manual_reference_frame=0, flags=0, points_header=None, points=None):
            self.name = name
            self.points_tag_block = points_tag_block
            self.bsp_index = bsp_index
            self.manual_reference_frame = manual_reference_frame
            self.flags = flags
            self.points_header = points_header
            self.points = points

    class Point():
        def __init__(self, name="", position=Vector(), reference_frame=0, surface_index=0, facing_direction_y=0.0, facing_direction_p=0.0):
            self.name = name
            self.position = position
            self.reference_frame = reference_frame
            self.surface_index = surface_index
            self.facing_direction_y = facing_direction_y
            self.facing_direction_p = facing_direction_p

    class CutsceneFlags():
        def __init__(self, name="", position=Vector(), facing_y=0.0, facing_p=0.0):
            self.name = name
            self.position = position
            self.facing_y = facing_y
            self.facing_p = facing_p

    class CutsceneCameraPoints():
        def __init__(self, flags=0, camera_type=0, name="", position=Vector(), orientation=Vector()):
            self.flags = flags
            self.camera_type = camera_type
            self.name = name
            self.position = position
            self.orientation = orientation

    class CutsceneTitle():
        def __init__(self, name="", name_length=0, text_bounds=(0, 0, 0, 0), justification=0, font=0, text_color=(0, 0, 0, 255),
                     shadow_color=(0, 0, 0, 255), fade_in_time=0.0, up_time=0.0, fade_out_time=0.0):
            self.name = name
            self.name_length = name_length
            self.text_bounds = text_bounds
            self.justification = justification
            self.font = font
            self.text_color = text_color
            self.shadow_color = shadow_color
            self.fade_in_time = fade_in_time
            self.up_time = up_time
            self.fade_out_time = fade_out_time

    class StructureBSP():
        def __init__(self, structure_bsp=None, structure_lightmap=None, unused_radiance_estimated_search_distance=0.0, unused_luminels_per_world_unit=0.0,
                     unused_output_white_reference=0.0, flags=0, default_sky=0):
            self.structure_bsp = structure_bsp
            self.structure_lightmap = structure_lightmap
            self.unused_radiance_estimated_search_distance = unused_radiance_estimated_search_distance
            self.unused_luminels_per_world_unit = unused_luminels_per_world_unit
            self.unused_output_white_reference = unused_output_white_reference
            self.flags = flags
            self.default_sky = default_sky

    class Order():
        def __init__(self, name="", style_index=0, flags=0, force_combat_status=0, entry_script="", follow_squad=0, follow_radius=0.0, primary_area_set_tag_block=None,
                     secondary_area_set_tag_block=None, secondary_set_trigger_tag_block=None, special_movement_tag_block=None, order_endings_tag_block=None,
                     primary_area_set_header=None, secondary_area_set_header=None, secondary_set_trigger_header=None, special_movement_header=None, order_endings_header=None,
                     primary_area_set=None, secondary_area_set=None, secondary_set_trigger=None, special_movement=None, order_endings=None):
            self.name = name
            self.style_index = style_index
            self.flags = flags
            self.force_combat_status = force_combat_status
            self.entry_script = entry_script
            self.follow_squad = follow_squad
            self.follow_radius = follow_radius
            self.primary_area_set_tag_block = primary_area_set_tag_block
            self.secondary_area_set_tag_block = secondary_area_set_tag_block
            self.secondary_set_trigger_tag_block = secondary_set_trigger_tag_block
            self.special_movement_tag_block = special_movement_tag_block
            self.order_endings_tag_block = order_endings_tag_block
            self.primary_area_set_header = primary_area_set_header
            self.secondary_area_set_header = secondary_area_set_header
            self.secondary_set_trigger_header = secondary_set_trigger_header
            self.special_movement_header = special_movement_header
            self.order_endings_header = order_endings_header
            self.primary_area_set = primary_area_set
            self.secondary_area_set = secondary_area_set
            self.secondary_set_trigger = secondary_set_trigger
            self.special_movement = special_movement
            self.order_endings = order_endings

    class PrimaryAreaSet():
        def __init__(self, area_type=0, zone_index=0, area_index=0):
            self.area_type = area_type
            self.zone_index = zone_index
            self.area_index = area_index

    class OrderEnding():
        def __init__(self, next_order_index=0, combination_rule=0, delay_time=0.0, dialogue_type=0, triggers_tag_block=None, triggers_header=None, triggers=None):
            self.next_order_index = next_order_index
            self.combination_rule = combination_rule
            self.delay_time = delay_time
            self.dialogue_type = dialogue_type
            self.triggers_tag_block = triggers_tag_block
            self.triggers_header = triggers_header
            self.triggers = triggers

    class Trigger():
        def __init__(self, trigger_flags=0, trigger_index=0):
            self.trigger_flags = trigger_flags
            self.trigger_index = trigger_index

    class AITrigger():
        def __init__(self, name="", trigger_flags=0, combination_rule=0, conditions_tag_block=None, conditions_header=None, conditions=None):
            self.name = name
            self.trigger_flags = trigger_flags
            self.combination_rule = combination_rule
            self.conditions_tag_block = conditions_tag_block
            self.conditions_header = conditions_header
            self.conditions = conditions

    class Condition():
        def __init__(self, rule_type=0, squad_index=0, squad_group_index=0, a=0, x=0.0, trigger_volume_index=0, exit_condition_script="", exit_condition_script_index=0,
                     flags=0):
            self.rule_type = rule_type
            self.squad_index = squad_index
            self.squad_group_index = squad_group_index
            self.a = a
            self.x = x
            self.trigger_volume_index = trigger_volume_index
            self.exit_condition_script = exit_condition_script
            self.exit_condition_script_index = exit_condition_script_index
            self.flags = flags

    class BackgroundSoundPalette():
        def __init__(self, name="", background_sound=None, inside_cluster_sound=None, cutoff_distance=0.0, scale_flags=0, interior_scale=0.0, portal_scale=0.0, exterior_scale=0.0,
                     interpolation_speed=0.0):
            self.name = name
            self.background_sound = background_sound
            self.inside_cluster_sound = inside_cluster_sound
            self.cutoff_distance = cutoff_distance
            self.scale_flags = scale_flags
            self.interior_scale = interior_scale
            self.portal_scale = portal_scale
            self.exterior_scale = exterior_scale
            self.interpolation_speed = interpolation_speed

    class SoundEnvironmentPalette():
        def __init__(self, name="", sound_environment=None, cutoff_distance=0.0, interpolation_speed=0.0):
            self.name = name
            self.sound_environment = sound_environment
            self.cutoff_distance = cutoff_distance
            self.interpolation_speed = interpolation_speed

    class Crate(Object):
        def __init__(self, sobj_header=None, obj0_header=None, sper_header=None, variant_name="", variant_name_length=0, active_change_colors=0,
                     primary_color_BGRA=(0, 0, 0, 255), secondary_color_BGRA=(0, 0, 0, 255), tertiary_color_BGRA=(0, 0, 0, 255),
                     quaternary_color_BGRA=(0, 0, 0, 255)):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.sper_header = sper_header
            self.variant_name = variant_name
            self.variant_name_length = variant_name_length
            self.active_change_colors = active_change_colors
            self.primary_color_BGRA = primary_color_BGRA
            self.secondary_color_BGRA = secondary_color_BGRA
            self.tertiary_color_BGRA = tertiary_color_BGRA
            self.quaternary_color_BGRA = quaternary_color_BGRA
