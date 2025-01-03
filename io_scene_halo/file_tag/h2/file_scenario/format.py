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

from ....file_tag.h2.file_functions.format import Function as ShaderFunction

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

class CommentTypeEnum(Enum):
    generic = 0

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

class TransformFlags(Flag):
    mirrored = auto()

class ObjectTypeFlags(Enum):
    biped = 0
    vehicle = auto()
    weapon = auto()
    equipment = auto()
    garbage = auto()
    projectile = auto()
    scenery = auto()
    machine = auto()
    control = auto()
    light_fixture = auto()
    sound_scenery = auto()
    crate = auto()
    creature = auto()

class ObjectSourceFlags(Enum):
    structure = 0
    editor = auto()
    dynamic = auto()
    legacy = auto()

class ObjectBSPPolicyFlags(Enum):
    default = 0
    always_placed = auto()
    manual_bsp_placement = auto()

class ObjectColorChangeFlags(Flag):
    primary = auto()
    secondary = auto()
    tertiary = auto()
    quaternary = auto()

class PathfindingPolicyEnum(Enum):
    tag_default = 0
    pathfinding_dynamic = auto()
    pathfinding_cut_out = auto()
    pathfinding_static = auto()
    pathfinding_none = auto()

class LightmappingPolicyEnum(Enum):
    tag_default = 0
    dynamic = auto()
    per_vertex = auto()

class ObjectGametypeEnum(Flag):
    ctf = 0
    slayer = auto()
    oddball = auto()
    king = auto()
    juggernaut = auto()
    territories = auto()
    assault = auto()
    medic = auto()
    vip = auto()
    infection = auto()
    headhunter = auto()

class UnitFlags(Flag):
    dead = auto()
    closed = auto()
    not_enterable_by_player = auto()

class ItemFlags(Flag):
    initially_at_rest = auto()
    obsolete = auto()
    does_accelerate = auto()

class DeviceGroupFlags(Flag):
    can_change_only_once = auto()

class DeviceFlags(Flag):
    initially_open = auto()
    initially_off = auto()
    can_change_only_once = auto()
    position_reversed = auto()
    not_usable_from_any_side = auto()

class MachineFlags(Flag):
    does_not_operate_automatically = auto()
    one_sided = auto()
    never_appears_locked = auto()
    opened_by_melee_attack = auto()
    one_sided_for_player = auto()
    does_not_close_automatically = auto()

class ControlFlags(Flag):
    usable_from_both_sides = auto()

class VolumeTypeEnum(Enum):
    sphere = 0
    vertical_cylinder = auto()

class ShapeTypeEnum(Enum):
    sphere = 0
    orthogonal = auto()
    projective = auto()
    pyramid = auto()

class LightFlags(Flag):
    custom_geometry = auto()
    unused = auto()
    cinematic_only = auto()

class LightmapTypeEnum(Enum):
    use_light_tag_settings = 0
    dynamic_only = auto()
    dynamic_with_lightmaps = auto()
    lightmaps_only = auto()

class LightmapFlags(Flag):
    unused = auto()

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

class SpawnTypeEnum(Enum):
    both = 0
    initial_spawn_only = auto()
    respawn_only = auto()

class CampaignPlayerTypeEnum(Enum):
    masterchief = 0
    dervish = auto()
    chief_multiplayer = auto()
    elite_multiplayer = auto()

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

class NetGameEquipmentFlags(Flag):
    levitate = auto()
    destroy_existing_on_new_spawn = auto()

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

class SquadFlags(Flag):
    unused = auto()
    never_search = auto()
    start_timer_immediately = auto()
    no_timer_delay_forever = auto()
    magic_sight_after_timer = auto()
    automatic_migration = auto()
    deprecated = auto()
    respawn_enabled = auto()
    blind = auto()
    deaf = auto()
    braindead = auto()
    _3d_firing_positions = auto()
    initially_placed = auto()
    units_not_enterable_by_player = auto()

class TeamEnum(Enum):
    default = 0
    player = auto()
    human = auto()
    covenant = auto()
    flood = auto()
    sentinel = auto()
    heretic = auto()
    prophet = auto()
    unused8 = auto()
    unused9 = auto()
    unused10 = auto()
    unused11 = auto()
    unused12 = auto()
    unused13 = auto()
    unused14 = auto()
    unused15 = auto()

class MajorUpgradeEnum(Enum):
    normal = 0
    few = auto()
    many = auto()
    none = auto()
    all = auto()

class GrenadeTypeEnum(Enum):
    none = 0
    human_grenade = auto()
    plasma_grenade = auto()

class StartingLocationFlags(Flag):
    initially_asleep = auto()
    infection_from_explode = auto()
    not_applicable = auto()
    always_place = auto()
    initially_hidden = auto()

class SeatTypeEnum(Enum):
    default = 0
    passenger = auto()
    gunner = auto()
    driver = 0
    small_cargo = auto()
    large_cargo = auto()
    no_driver = auto()
    no_vehicle = auto()

class InitialMovementModeEnum(Enum):
    default = 0
    climbing = auto()
    flying = auto()

class ZoneFlags(Flag):
    manual_bsp_index = auto()

class FiringPointFlags(Flag):
    open = auto()
    partial = auto()
    closed = auto()
    mobile = auto()
    wall_lean = auto()
    perch = auto()
    ground_point = auto()
    dynamic_cover_point = auto()

class AreaFlags(Flag):
    vehicle_area = auto()
    perch = auto()
    manual_reference_frame = auto()

class MissionSceneFlags(Flag):
    scene_can_play_multiple_times = auto()
    enable_combat_dialogue = auto()

class CombinationRuleEnum(Enum):
    _or = 0
    _and = auto()

class TriggerFlags(Flag):
    _not = auto()

class GroupEnum(Enum):
    group_1 = 0
    group_2 = auto()
    group_3 = auto()

class PathfindingSectorFlags(Flag):
    sector_walkable = auto()
    sector_breakable = auto()
    sector_mobile = auto()
    sector_bsp_source = auto()
    floor = auto()
    ceiling = auto()
    wall_north = auto()
    wall_south = auto()
    wall_east = auto()
    wall_west = auto()
    crouchable = auto()
    aligned = auto()
    sector_step = auto()
    sector_interior = auto()

class LinkFlags(Flag):
    sector_link_from_collision_edge = auto()
    sector_intersection_link = auto()
    sector_link_bsp2d_creation_error = auto()
    sector_link_topology_error = auto()
    sector_link_chain_error = auto()
    sector_link_both_sectors_walkable = auto()
    sector_link_magic_hanging_link = auto()
    sector_link_threshold = auto()
    sector_link_crouchable = auto()
    sector_link_wall_base = auto()
    sector_link_ledge = auto()
    sector_link_leanable = auto()
    sector_link_start_corner = auto()
    sector_link_end_corner = auto()

class ObjectRefFlags(Flag):
    mobile = auto()

class NodeFlags(Flag):
    projection_sign = auto()

class HintTypeEnum(Enum):
    intersection_link = 0
    jump_link = auto()
    climb_link = auto()
    vault_link = auto()
    mount_link = auto()
    hoist_link = auto()
    wall_jump_link = auto()
    breakable_floor = auto()

class GeometryFlags(Flag):
    bidirectional = auto()
    closed = auto()

class ForceJumpHeightEnum(Enum):
    none = 0
    down = auto()
    step = auto()
    crouch = auto()
    stand = auto()
    storey = auto()
    tower = auto()
    infinite = auto()

class JumpControlFlags(Flag):
    magic_lift = auto()

class HintFlags(Flag):
    bidirectional = auto()

class WellTypeEnum(Enum):
    jump = 0
    climb = auto()
    hoist = auto()

class AIConversationFlags(Flag):
    stop_if_death = auto()
    stop_if_damaged = auto()
    stop_if_visible_enemy = auto()
    stop_if_alerted_to_enemy = auto()
    player_must_be_visible = auto()
    stop_other_actions = auto()
    keep_trying_to_play = auto()
    player_must_be_looking = auto()

class LineFlags(Flag):
    addressee_look_at_speaker = auto()
    everyone_look_at_speaker = auto()
    everyone_look_at_addresse = auto()
    wait_after_until_told_to_advance = auto()
    wait_until_speaker_nearby = auto()
    wait_until_everyone_nearby = auto()

class AddresseeEnum(Enum):
    none = 0
    player = auto()
    participant = auto()

class ScriptTypeEnum(Enum):
    startup = 0
    dormant = auto()
    continuous = auto()
    static = auto()
    stub = auto()
    command_script = auto()

class ReturnTypeEnum(Enum):
    unparsed = 0
    special_form = auto()
    function_name = auto()
    passthrough = auto()
    void = auto()
    boolean = auto()
    real = auto()
    short = auto()
    long = auto()
    string = auto()
    script = auto()
    string_id = auto()
    unit_seat_mapping = auto()
    trigger_volume = auto()
    cutscene_flag = auto()
    cutscene_camera_point = auto()
    cutscene_title = auto()
    cutscene_recording = auto()
    device_group = auto()
    ai = auto()
    ai_command_list = auto()
    ai_command_script = auto()
    ai_behavior = auto()
    ai_orders = auto()
    starting_profile = auto()
    conversation = auto()
    structure_bsp = auto()
    navpoint = auto()
    point_reference = auto()
    style = auto()
    hud_message = auto()
    object_list = auto()
    sound = auto()
    effect = auto()
    damage = auto()
    looping_sound = auto()
    animation_graph = auto()
    damage_effect = auto()
    object_definition = auto()
    bitmap = auto()
    shader = auto()
    render_model = auto()
    structure_definition = auto()
    lightmap_definition = auto()
    game_difficulty = auto()
    team = auto()
    actor_type = auto()
    hud_corner = auto()
    model_state = auto()
    network_event = auto()
    object = auto()
    unit = auto()
    vehicle = auto()
    weapon = auto()
    device = auto()
    scenery = auto()
    object_name = auto()
    unit_name = auto()
    vehicle_name = auto()
    weapon_name = auto()
    device_name = auto()
    scenery_name = auto()

class PointSetFlags(Flag):
    manual_reference_frame = auto()
    turret_deployment = auto()

class CameraFlags(Flag):
    edit_as_relative = auto()

class CameraTypeEnum(Enum):
    normal = 0
    ignore_target_orientation = auto()
    dolly = auto()
    ignore_target_updates = auto()

class JustificationEnum(Enum):
    left = 0
    right = auto()
    center = auto()
    custom_text_entry = auto()

class FontEnum(Enum):
    terminal_font = 0
    body_text_font = auto()
    title_font = auto()
    super_large_font = auto()
    large_body_text_font = auto()
    split_screen_hud_message_font = auto()
    full_screen_hud_message_font = auto()
    english_body_text_font = auto()
    hud_number_font = auto()
    subtitle_font = auto()
    mainmenu_font = auto()
    text_chat_font = auto()

class StructureBSPFlags(Flag):
    default_sky_enabled = auto()

class OrderFlags(Flag):
    locked = auto()
    always_active = auto()
    debug_on = auto()
    strict_area_def = auto()
    follow_closest_player = auto()
    follow_squad = auto()
    active_camo = auto()
    suppress_combat_until_engaged = auto()
    inhibit_vehicle_use = auto()

class OrderEnum(Enum):
    none = 0
    asleep = auto()
    idle = auto()
    alert = auto()
    combat = auto()

class AreaTypeEnum(Enum):
    default = 0
    search = auto()
    goal = auto()

class DialogueTypeEnum(Enum):
    none = 0
    advance = auto()
    charge = auto()
    fall_back = auto()
    retreat = auto()
    move_one = auto()
    arrival = auto()
    enter_vehicle = auto()
    exit_vehicle = auto()
    follow_player = auto()
    leave_player = auto()
    support = auto()

class SpecialMovementFlags(Flag):
    jump = auto()
    climb = auto()
    vault = auto()
    mount = auto()
    hoist = auto()
    wall_jump = auto()
    not_applicable = auto()

class AITriggerFlags(Flag):
    latch_on_when_triggered = auto()

class RuleTypeEnum(Enum):
    a_or_greater_alive = 0
    a_or_fewer_alive = auto()
    x_or_greater_strength = auto()
    x_or_less_strength = auto()
    if_enemy_sighted = auto()
    after_a_ticks = auto()
    if_alerted_by_squad_a = auto()
    script_ref_true = auto()
    script_ref_false = auto()
    if_player_in_trigger_volume = auto()
    if_all_players_in_trigger_volume = auto()
    combat_status_a_or_more = auto()
    combat_status_a_or_less = auto()
    arrived = auto()
    in_vehicle = auto()
    sighted_player = auto()
    a_or_greater_fighting = auto()
    a_or_fewer_fighting = auto()
    player_within_x_world_units = auto()
    player_shot_more_than_x_seconds_ago = auto()
    game_safe_to_save = auto()

class ScaleFlags(Flag):
    override_default_scale = auto()
    use_adjacent_cluster_as_portal_scale = auto()
    use_adjacent_cluster_as_exterior_scale = auto()
    scale_with_weather_intensity = auto()

class OverloadTypeEnum(Enum):
    enemy = 0
    friend = auto()
    enemy_vehicle = auto()
    friendly_vehicle = auto()
    empty_vehicle = auto()
    oddball_inclusion = auto()
    oddball_exclusion = auto()
    hill_inclusion = auto()
    hill_exclusion = auto()
    last_race_flag = auto()
    dead_ally = auto()
    controlled_territory = auto()
    medic = auto()

class RelevantTeamFlags(Flag):
    alpha_team = auto()
    bravo_team = auto()
    charlie_team = auto()
    delta_team = auto()
    echo_team = auto()
    foxtrot_team = auto()
    golf_team = auto()
    hotel_team = auto()
    neutral = auto()

class RelevantGamesFlags(Flag):
    all_slayer = auto()
    all_oddball = auto()
    all_king = auto()
    all_ctf = auto()
    all_race = auto()
    all_headhunter = auto()
    all_juggernaut = auto()
    all_territories = auto()
    all_medic = auto()
    all_vip = auto()
    all_infection = auto()

class SpawnZoneFlags(Flag):
    disabled_if_flag_home = auto()
    disabled_if_flag_away = auto()
    disabled_if_bomb_home = auto()
    disabled_if_bomb_away = auto()

class CameraImmersionFlags(Flag):
    disable_atmospheric_fog = auto()
    disable_secondary_fog = auto()
    disable_planar_fog = auto()
    invert_planar_fog_priorities = auto()
    disable_water = auto()

class FlockFlags(Flag):
    hard_boundaries_on_volume = auto()
    flock_initially_stopped = auto()

class CacheResourceTypeEnum(Enum):
    tag_block = 0
    tag_data = auto()
    vertex_buffer = auto()

class DecoratorTypeEnum(Enum):
    model = 0
    floating_decal = auto()
    projected_decal = auto()
    screen_facing_quad = auto()
    axis_rotating_quad = auto()
    cross_quad = auto()

class MultiplayerLevelFlags(Flag):
    unlockable = auto()

class FunctionTypeEnum(Enum):
    identity = 0
    constant = auto()
    transition = auto()
    periodic = auto()
    linear = auto()
    linear_key = auto()
    multi_linear_key = auto()
    spline = auto()
    multi_spline = auto()
    exponent = auto()
    spline2 = auto()

class TransitionExponentEnum(Enum):
    linear = 0
    early = auto()
    very_early = auto()
    late = auto()
    very_late = auto()
    cosine = auto()
    one = auto()
    zero = auto()

class PeriodicExponentEnum(Enum):
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

class ScenarioAsset():
    def __init__(self, header=None, body_header=None, skies_header=None, skies=None, child_scenario_header=None, child_scenarios=None, predicted_resources_header=None, 
                 predicted_resources=None, functions_header=None, functions=None, editor_scenario_data=None, comment_header=None, comments=None, 
                 environment_objects_header=None, environment_objects=None, object_name_header=None, object_names=None, scenery_header=None, scenery=None, 
                 scenery_palette_header=None, scenery_palette=None, bipeds_header=None, bipeds=None, biped_palette_header=None, biped_palette=None, vehicles_header=None, 
                 vehicles=None, vehicle_palette_header=None, vehicle_palette=None, equipment_header=None, equipment=None, equipment_palette_header=None, 
                 equipment_palette=None, weapon_header=None, weapons=None, weapon_palette_header=None, weapon_palette=None, device_group_header=None, device_groups=None, 
                 device_machine_header=None, device_machines=None, device_machine_palette_header=None, device_machine_palette=None, device_control_header=None, 
                 device_controls=None, device_control_palette_header=None, device_control_palette=None, device_light_fixture_header=None, device_light_fixtures=None, 
                 device_light_fixture_palette_header=None, device_light_fixtures_palette=None, sound_scenery_header=None, sound_scenery=None, 
                 sound_scenery_palette_header=None, sound_scenery_palette=None, light_volume_header=None, light_volumes=None, light_volume_palette_header=None, 
                 light_volume_palette=None, player_starting_profile_header=None, player_starting_profiles=None, player_starting_location_header=None, 
                 player_starting_locations=None, trigger_volumes_header=None, trigger_volumes=None, recorded_animation_header=None, recorded_animations=None, 
                 netgame_flag_header=None, netgame_flags=None, netgame_equipment_header=None, netgame_equipment=None, starting_equipment_header=None, 
                 starting_equipment=None, bsp_switch_trigger_volumes_header=None, bsp_switch_trigger_volumes=None, decals_header=None, decals=None, 
                 decal_palette_header=None, decal_palette=None, detail_object_collection_palette_header=None, detail_object_collection_palette=None, 
                 style_palette_header=None, style_palette=None, squad_groups_header=None, squad_groups=None, squads_header=None, squads=None, zones_header=None, zones=None, 
                 mission_scenes_header=None, mission_scenes=None, character_palette_header=None, character_palette=None, ai_pathfinding_data_header=None, 
                 ai_pathfinding_data=None, ai_animation_references_header=None, ai_animation_references=None, ai_script_references_header=None, ai_script_references=None, 
                 ai_recording_references_header=None, ai_recording_references=None, ai_conversations_header=None, ai_conversations=None, script_syntax_data=None, 
                 script_string_data=None, scripts_header=None, scripts=None, globals_header=None, script_globals=None, references_header=None, references=None, 
                 source_files_header=None, source_files=None, scripting_data_header=None, scripting_data=None, cutscene_flags_header=None, cutscene_flags=None, 
                 cutscene_camera_points_header=None, cutscene_camera_points=None, cutscene_titles_header=None, cutscene_titles=None, structure_bsps_header=None, 
                 structure_bsps=None, scenario_resources_header=None, scenario_resources=None, old_structure_physics_header=None, old_structure_physics=None, 
                 hs_unit_seat_header=None, hs_unit_seats=None, scenario_kill_triggers_header=None, scenario_kill_triggers=None, hs_syntax_datums_header=None, 
                 hs_syntax_datums=None, orders_header=None, orders=None, triggers_header=None, triggers=None, background_sound_palette_header=None, 
                 background_sound_palette=None, sound_environment_palette_header=None, sound_environment_palette=None, weather_palette_header=None, weather_palette=None, 
                 unused_0_header=None, unused_0=None, unused_1_header=None, unused_1=None, unused_2_header=None, unused_2=None, unused_3_header=None, unused_3=None, 
                 scavenger_hunt_objects_header=None, scavenger_hunt_objects=None, scenario_cluster_data_header=None, scenario_cluster_data=None, spawn_data_header=None, 
                 spawn_data=None, crates_header=None, crates=None, crates_palette_header=None, crates_palette=None, atmospheric_fog_palette_header=None, 
                 atmospheric_fog_palette=None, planar_fog_palette_header=None, planar_fog_palette=None, flocks_header=None, flocks=None, decorators_header=None, 
                 decorators=None, creatures_header=None, creatures=None, creatures_palette_header=None, creatures_palette=None, decorator_palette_header=None, 
                 decorator_palette=None, bsp_transition_volumes_header=None, bsp_transition_volumes=None, structure_bsp_lighting_header=None, structure_bsp_lighting=None, 
                 editor_folders_header=None, editor_folders=None, level_data_header=None, level_data=None, mission_dialogue_header=None, mission_dialogue=None, 
                 interpolators_header=None, interpolators=None, shared_references_header=None, shared_references=None, screen_effect_references_header=None, 
                 screen_effect_references=None, simulation_definition_table_header=None, simulation_definition_table=None, unused_tag_ref=None, skies_tag_block=None, 
                 scenario_type=0, scenario_flags=0, child_scenarios_tag_block=None, local_north=0.0, predicted_resources_tag_block=None, functions_tag_block=None, 
                 comments_tag_block=None, environment_objects_tag_block=None, object_names_tag_block=None, scenery_tag_block=None, scenery_palette_tag_block=None, 
                 bipeds_tag_block=None, biped_palette_tag_block=None, vehicles_tag_block=None, vehicle_palette_tag_block=None, equipment_tag_block=None, 
                 equipment_palette_tag_block=None, weapons_tag_block=None, weapon_palette_tag_block=None, device_groups_tag_block=None, machines_tag_block=None, 
                 machine_palette_tag_block=None, controls_tag_block=None, control_palette_tag_block=None, light_fixtures_tag_block=None, 
                 light_fixtures_palette_tag_block=None, sound_scenery_tag_block=None, sound_scenery_palette_tag_block=None, light_volumes_tag_block=None, 
                 light_volume_palette_tag_block=None, player_starting_profile_tag_block=None, player_starting_locations_tag_block=None, trigger_volumes_tag_block=None, 
                 recorded_animations_tag_block=None, netgame_flags_tag_block=None, netgame_equipment_tag_block=None, starting_equipment_tag_block=None, 
                 bsp_switch_trigger_volumes_tag_block=None, decals_tag_block=None, decal_palette_tag_block=None, detail_object_collection_palette_tag_block=None, 
                 style_palette_tag_block=None, squad_groups_tag_block=None, squads_tag_block=None, zones_tag_block=None, mission_scenes_tag_block=None, 
                 character_palette_tag_block=None, ai_pathfinding_data_tag_block=None, ai_animation_references_tag_block=None, ai_script_references_tag_block=None, 
                 ai_recording_references_tag_block=None, ai_conversations_tag_block=None, script_syntax_data_tag_data=None, script_string_data_tag_data=None, 
                 scripts_tag_block=None, globals_tag_block=None, references_tag_block=None, source_files_tag_block=None, scripting_data_tag_block=None, 
                 cutscene_flags_tag_block=None, cutscene_camera_points_tag_block=None, cutscene_titles_tag_block=None, custom_object_names_tag_ref=None, 
                 chapter_title_text_tag_ref=None, hud_messages_tag_ref=None, structure_bsps_tag_block=None, scenario_resources_tag_block=None, 
                 old_structure_physics_tag_block=None, hs_unit_seats_tag_block=None, scenario_kill_triggers_tag_block=None, hs_syntax_datums_tag_block=None, 
                 orders_tag_block=None, triggers_tag_block=None, background_sound_palette_tag_block=None, sound_environment_palette_tag_block=None, 
                 weather_palette_tag_block=None, unused_0_tag_block=None, unused_1_tag_block=None, unused_2_tag_block=None, unused_3_tag_block=None, 
                 scavenger_hunt_objects_tag_block=None, scenario_cluster_data_tag_block=None, salt_array=None, spawn_data_tag_block=None, 
                 sound_effect_collection_tag_ref=None, crates_tag_block=None, crate_palette_tag_block=None, global_lighting_tag_ref=None, 
                 atmospheric_fog_palette_tag_block=None, planar_fog_palette_tag_block=None, flocks_tag_block=None, subtitles_tag_ref=None, decorators_tag_block=None, 
                 creatures_tag_block=None, creature_palette_tag_block=None, decorator_palette_tag_block=None, bsp_transition_volumes_tag_block=None, 
                 structure_bsp_lighting_tag_block=None, editor_folders_tag_block=None, level_data_tag_block=None, game_engine_strings_tag_ref=None, 
                 mission_dialogue_tag_block=None, objectives_tag_ref=None, interpolators_tag_block=None, shared_references_tag_block=None, 
                 screen_effect_references_tag_block=None, simulation_definition_table_tag_block=None):
        self.header = header
        self.body_header = body_header
        self.skies_header = skies_header
        self.skies = skies
        self.child_scenario_header = child_scenario_header
        self.child_scenarios = child_scenarios
        self.predicted_resources_header = predicted_resources_header
        self.predicted_resources = predicted_resources
        self.functions_header = functions_header
        self.functions = functions
        self.editor_scenario_data = editor_scenario_data
        self.comment_header = comment_header
        self.comments = comments
        self.environment_objects_header = environment_objects_header
        self.environment_objects = environment_objects
        self.object_name_header = object_name_header
        self.object_names = object_names
        self.scenery_header = scenery_header
        self.scenery = scenery
        self.scenery_palette_header = scenery_palette_header
        self.scenery_palette = scenery_palette
        self.bipeds_header = bipeds_header
        self.bipeds = bipeds
        self.biped_palette_header = biped_palette_header
        self.biped_palette = biped_palette
        self.vehicles_header = vehicles_header
        self.vehicles = vehicles
        self.vehicle_palette_header = vehicle_palette_header
        self.vehicle_palette = vehicle_palette
        self.equipment_header = equipment_header
        self.equipment = equipment
        self.equipment_palette_header = equipment_palette_header
        self.equipment_palette = equipment_palette
        self.weapon_header = weapon_header
        self.weapons = weapons
        self.weapon_palette_header = weapon_palette_header
        self.weapon_palette = weapon_palette
        self.device_group_header = device_group_header
        self.device_groups = device_groups
        self.device_machine_header = device_machine_header
        self.device_machines = device_machines
        self.device_machine_palette_header = device_machine_palette_header
        self.device_machine_palette = device_machine_palette
        self.device_control_header = device_control_header
        self.device_controls = device_controls
        self.device_control_palette_header = device_control_palette_header
        self.device_control_palette = device_control_palette
        self.device_light_fixture_header = device_light_fixture_header
        self.device_light_fixtures = device_light_fixtures
        self.device_light_fixture_palette_header = device_light_fixture_palette_header
        self.device_light_fixtures_palette = device_light_fixtures_palette
        self.sound_scenery_header = sound_scenery_header
        self.sound_scenery = sound_scenery
        self.sound_scenery_palette_header = sound_scenery_palette_header
        self.sound_scenery_palette = sound_scenery_palette
        self.light_volume_header = light_volume_header
        self.light_volumes = light_volumes
        self.light_volume_palette_header = light_volume_palette_header
        self.light_volume_palette = light_volume_palette
        self.player_starting_profile_header = player_starting_profile_header
        self.player_starting_profiles = player_starting_profiles
        self.player_starting_location_header = player_starting_location_header
        self.player_starting_locations = player_starting_locations
        self.trigger_volumes_header = trigger_volumes_header
        self.trigger_volumes = trigger_volumes
        self.recorded_animation_header = recorded_animation_header
        self.recorded_animations = recorded_animations
        self.netgame_flag_header = netgame_flag_header
        self.netgame_flags = netgame_flags
        self.netgame_equipment_header = netgame_equipment_header
        self.netgame_equipment = netgame_equipment
        self.starting_equipment_header = starting_equipment_header
        self.starting_equipment = starting_equipment
        self.bsp_switch_trigger_volumes_header = bsp_switch_trigger_volumes_header
        self.bsp_switch_trigger_volumes = bsp_switch_trigger_volumes
        self.decals_header = decals_header
        self.decals = decals
        self.decal_palette_header = decal_palette_header
        self.decal_palette = decal_palette
        self.detail_object_collection_palette_header = detail_object_collection_palette_header
        self.detail_object_collection_palette = detail_object_collection_palette
        self.style_palette_header = style_palette_header
        self.style_palette = style_palette
        self.squad_groups_header = squad_groups_header
        self.squad_groups = squad_groups
        self.squads_header = squads_header
        self.squads = squads
        self.zones_header = zones_header
        self.zones = zones
        self.mission_scenes_header = mission_scenes_header
        self.mission_scenes = mission_scenes
        self.character_palette_header = character_palette_header
        self.character_palette = character_palette
        self.ai_pathfinding_data_header = ai_pathfinding_data_header
        self.ai_pathfinding_data = ai_pathfinding_data
        self.ai_animation_references_header = ai_animation_references_header
        self.ai_animation_references = ai_animation_references
        self.ai_script_references_header = ai_script_references_header
        self.ai_script_references = ai_script_references
        self.ai_recording_references_header = ai_recording_references_header
        self.ai_recording_references = ai_recording_references
        self.ai_conversations_header = ai_conversations_header
        self.ai_conversations = ai_conversations
        self.script_syntax_data = script_syntax_data
        self.script_string_data = script_string_data
        self.scripts_header = scripts_header
        self.scripts = scripts
        self.globals_header = globals_header
        self.script_globals = script_globals
        self.references_header = references_header
        self.references = references
        self.source_files_header = source_files_header
        self.source_files = source_files
        self.scripting_data_header = scripting_data_header
        self.scripting_data = scripting_data
        self.cutscene_flags_header = cutscene_flags_header
        self.cutscene_flags = cutscene_flags
        self.cutscene_camera_points_header = cutscene_camera_points_header
        self.cutscene_camera_points = cutscene_camera_points
        self.cutscene_titles_header = cutscene_titles_header
        self.cutscene_titles = cutscene_titles
        self.structure_bsps_header = structure_bsps_header
        self.structure_bsps = structure_bsps
        self.scenario_resources_header = scenario_resources_header
        self.scenario_resources = scenario_resources
        self.old_structure_physics_header = old_structure_physics_header
        self.old_structure_physics = old_structure_physics
        self.hs_unit_seat_header = hs_unit_seat_header
        self.hs_unit_seats = hs_unit_seats
        self.scenario_kill_triggers_header = scenario_kill_triggers_header
        self.scenario_kill_triggers = scenario_kill_triggers
        self.hs_syntax_datums_header = hs_syntax_datums_header
        self.hs_syntax_datums = hs_syntax_datums
        self.orders_header = orders_header
        self.orders = orders
        self.triggers_header = triggers_header
        self.triggers = triggers
        self.background_sound_palette_header = background_sound_palette_header
        self.background_sound_palette = background_sound_palette
        self.sound_environment_palette_header = sound_environment_palette_header
        self.sound_environment_palette = sound_environment_palette
        self.weather_palette_header = weather_palette_header
        self.weather_palette = weather_palette
        self.unused_0_header = unused_0_header
        self.unused_0 = unused_0
        self.unused_1_header = unused_1_header
        self.unused_1 = unused_1
        self.unused_2_header = unused_2_header
        self.unused_2 = unused_2
        self.unused_3_header = unused_3_header
        self.unused_3 = unused_3
        self.scavenger_hunt_objects_header = scavenger_hunt_objects_header
        self.scavenger_hunt_objects = scavenger_hunt_objects
        self.scenario_cluster_data_header = scenario_cluster_data_header
        self.scenario_cluster_data = scenario_cluster_data
        self.spawn_data_header = spawn_data_header
        self.spawn_data = spawn_data
        self.crates_header = crates_header
        self.crates = crates
        self.crates_palette_header = crates_palette_header
        self.crates_palette = crates_palette
        self.atmospheric_fog_palette_header = atmospheric_fog_palette_header
        self.atmospheric_fog_palette = atmospheric_fog_palette
        self.planar_fog_palette_header = planar_fog_palette_header
        self.planar_fog_palette = planar_fog_palette
        self.flocks_header = flocks_header
        self.flocks = flocks
        self.decorators_header = decorators_header
        self.decorators = decorators
        self.creatures_header = creatures_header
        self.creatures = creatures
        self.creatures_palette_header = creatures_palette_header
        self.creatures_palette = creatures_palette
        self.decorator_palette_header = decorator_palette_header
        self.decorator_palette = decorator_palette
        self.bsp_transition_volumes_header = bsp_transition_volumes_header
        self.bsp_transition_volumes = bsp_transition_volumes
        self.structure_bsp_lighting_header = structure_bsp_lighting_header
        self.structure_bsp_lighting = structure_bsp_lighting
        self.editor_folders_header = editor_folders_header
        self.editor_folders = editor_folders
        self.level_data_header = level_data_header
        self.level_data = level_data
        self.mission_dialogue_header = mission_dialogue_header
        self.mission_dialogue = mission_dialogue
        self.interpolators_header = interpolators_header
        self.interpolators = interpolators
        self.shared_references_header = shared_references_header
        self.shared_references = shared_references
        self.screen_effect_references_header = screen_effect_references_header
        self.screen_effect_references = screen_effect_references
        self.simulation_definition_table_header = simulation_definition_table_header
        self.simulation_definition_table = simulation_definition_table
        self.unused_tag_ref = unused_tag_ref
        self.skies_tag_block = skies_tag_block
        self.scenario_type = scenario_type
        self.scenario_flags = scenario_flags
        self.child_scenarios_tag_block = child_scenarios_tag_block
        self.local_north = local_north
        self.predicted_resources_tag_block = predicted_resources_tag_block
        self.functions_tag_block = functions_tag_block
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

    class PredictedResource:
        def __init__(self, tag_type=0, resource_index=0, tag_index=0):
            self.tag_type = tag_type
            self.resource_index = resource_index
            self.tag_index = tag_index

    class Function:
        def __init__(self, flags=0, name="", period=0, scale_period_by=0, function_type=0, scale_function_by=0, wobble_function_type=0, wobble_period=0, wobble_magnitude=0,
                     square_wave_threshold=0, step_count=0, map_to=0, sawtooth_count=0, scale_result_by=0, bounds_mode=0, bounds=(0.0, 0.0), turn_off_with=0):
            self.flags = flags
            self.name = name
            self.period = period
            self.scale_period_by = scale_period_by
            self.function_type = function_type
            self.scale_function_by = scale_function_by
            self.wobble_function_type = wobble_function_type
            self.wobble_period = wobble_period
            self.wobble_magnitude = wobble_magnitude
            self.square_wave_threshold = square_wave_threshold
            self.step_count = step_count
            self.map_to = map_to
            self.sawtooth_count = sawtooth_count
            self.scale_result_by = scale_result_by
            self.bounds_mode = bounds_mode
            self.bounds = bounds
            self.turn_off_with = turn_off_with

    class Comment:
        def __init__(self, position=Vector(), type=0, name="", comment=""):
            self.position = position
            self.type = type
            self.name = name
            self.comment = comment

    class EnvironmentObject:
        def __init__(self, bsp_index=0, runtime_object_type=0, unique_id=0, object_definition_tag=0, environment_object=0):
            self.bsp_index = bsp_index
            self.runtime_object_type = runtime_object_type
            self.unique_id = unique_id
            self.object_definition_tag = object_definition_tag
            self.environment_object = environment_object

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
                     quaternary_color_BGRA=(0, 0, 0, 255), pathfinding_policy=0, lightmap_policy=0, pathfinding_references_header=None, pathfinding_references_tag_block=None,
                     valid_multiplayer_games=0, pathfinding_references=None):
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
            self.pathfinding_references_tag_block = pathfinding_references_tag_block
            self.valid_multiplayer_games = valid_multiplayer_games
            self.pathfinding_references = pathfinding_references

    class PathfindingReference:
        def __init__(self, bsp_index=0, pathfinding_object_index=0):
            self.bsp_index = bsp_index
            self.pathfinding_object_index = pathfinding_object_index

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
                     flags_1=0, pathfinding_references_header=None, pathfinding_references_tag_block=None, pathfinding_references=None):
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
            self.pathfinding_references_tag_block = pathfinding_references_tag_block
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

    class BSPSwitchTriggerVolume():
        def __init__(self, trigger_volume=0, source=0, destination=0):
            self.trigger_volume = trigger_volume
            self.source = source
            self.destination = destination

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
                     initial_order_index=0, vehicle_variant="", vehicle_variant_length=0, starting_locations_tag_block=None, placement_script="", starting_locations_header=None,
                     starting_locations=None):
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
            self.vehicle_variant_length = vehicle_variant_length
            self.starting_locations_tag_block = starting_locations_tag_block
            self.placement_script = placement_script
            self.starting_locations_header = starting_locations_header
            self.starting_locations = starting_locations

    class StartingLocation():
        def __init__(self, name="", name_length=0, position=Vector(), reference_frame=0, facing=(0.0, 0.0), flags=0, character_type_index=0,
                     initial_weapon_index=0, initial_secondary_weapon_index=0, vehicle_type_index=0, seat_type=0, grenade_type=0, swarm_count=0,
                     actor_variant="", actor_variant_length=0, vehicle_variant="", vehicle_variant_length=0, initial_movement_distance=0, emitter_vehicle_index=0,
                     initial_movement_mode=0, placement_script=""):
            self.name = name
            self.name_length = name_length
            self.position = position
            self.reference_frame = reference_frame
            self.facing = facing
            self.flags = flags
            self.character_type_index = character_type_index
            self.initial_weapon_index = initial_weapon_index
            self.initial_secondary_weapon_index = initial_secondary_weapon_index
            self.vehicle_type_index = vehicle_type_index
            self.seat_type = seat_type
            self.grenade_type = grenade_type
            self.swarm_count = swarm_count
            self.actor_variant = actor_variant
            self.actor_variant_length = actor_variant_length
            self.vehicle_variant = vehicle_variant
            self.vehicle_variant_length = vehicle_variant_length
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
        def __init__(self, position=Vector(), reference_frame=0, flags=0, area_index=0, cluster_index=0, normal=(0.0, 0.0)):
            self.position = position
            self.reference_frame = reference_frame
            self.flags = flags
            self.area_index = area_index
            self.cluster_index = cluster_index
            self.normal = normal

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

    class FlightHint():
        def __init__(self, flight_hint_index=0, point_index=0):
            self.flight_hint_index = flight_hint_index
            self.point_index = point_index

    class MissionScene():
        def __init__(self, name="", name_length=0, flags=0, trigger_conditions_tag_block=None, roles_tag_block=None, trigger_conditions_header=None, roles_header=None,
                     trigger_conditions=None, roles=None):
            self.name = name
            self.name_length = name_length
            self.flags = flags
            self.trigger_conditions_tag_block = trigger_conditions_tag_block
            self.roles_tag_block = roles_tag_block
            self.trigger_conditions_header = trigger_conditions_header
            self.roles_header = roles_header
            self.trigger_conditions = trigger_conditions
            self.roles = roles

    class TriggerCondition():
        def __init__(self, combination_rule=0, triggers_tag_block=None, triggers_header=None, triggers=None):
            self.combination_rule = combination_rule
            self.triggers_tag_block = triggers_tag_block
            self.triggers_header = triggers_header
            self.triggers = triggers

    class Trigger():
        def __init__(self, trigger_flags=0, trigger=0):
            self.trigger_flags = trigger_flags
            self.trigger = trigger

    class Role():
        def __init__(self, name="", name_length=0, group=0, role_variants_tag_block=None, role_variants_header=None, role_variants=None):
            self.name = name
            self.name_length = name_length
            self.group = group
            self.role_variants_tag_block = role_variants_tag_block
            self.role_variants_header = role_variants_header
            self.role_variants = role_variants

    class RoleVariant():
        def __init__(self, name="", name_length=0):
            self.name = name
            self.name_length = name_length

    class AIPathfindingData():
        def __init__(self, sectors_tag_block=None, sectors_header=None, sectors=None, links_tag_block=None, links_header=None, links=None, refs_tag_block=None, refs_header=None,
                     refs=None, bsp2d_nodes_tag_block=None, bsp2d_nodes_header=None, bsp2d_nodes=None, surface_flags_tag_block=None, surface_flags_header=None, surface_flags=None,
                     vertices_tag_block=None, vertices_header=None, vertices=None, object_refs_tag_block=None, object_refs_header=None, object_refs=None,
                     pathfinding_hints_tag_block=None, pathfinding_hints_header=None, pathfinding_hints=None, instanced_geometry_refs_tag_block=None,
                     instanced_geometry_refs_header=None, instanced_geometry_refs=None, structure_checksum=0, user_placed_hints_tag_block=None, user_placed_hints_header=None,
                     user_placed_hints=None):
            self.sectors_tag_block = sectors_tag_block
            self.sectors_header = sectors_header
            self.sectors = sectors
            self.links_tag_block = links_tag_block
            self.links_header = links_header
            self.links = links
            self.refs_tag_block = refs_tag_block
            self.refs_header = refs_header
            self.refs = refs
            self.bsp2d_nodes_tag_block = bsp2d_nodes_tag_block
            self.bsp2d_nodes_header = bsp2d_nodes_header
            self.bsp2d_nodes = bsp2d_nodes
            self.surface_flags_tag_block = surface_flags_tag_block
            self.surface_flags_header = surface_flags_header
            self.surface_flags = surface_flags
            self.vertices_tag_block = vertices_tag_block
            self.vertices_header = vertices_header
            self.vertices = vertices
            self.object_refs_tag_block = object_refs_tag_block
            self.object_refs_header = object_refs_header
            self.object_refs = object_refs
            self.pathfinding_hints_tag_block = pathfinding_hints_tag_block
            self.pathfinding_hints_header = pathfinding_hints_header
            self.pathfinding_hints = pathfinding_hints
            self.instanced_geometry_refs_tag_block = instanced_geometry_refs_tag_block
            self.instanced_geometry_refs_header = instanced_geometry_refs_header
            self.instanced_geometry_refs = instanced_geometry_refs
            self.structure_checksum = structure_checksum
            self.user_placed_hints_tag_block = user_placed_hints_tag_block
            self.user_placed_hints_header = user_placed_hints_header
            self.user_placed_hints = user_placed_hints

    class Sector():
        def __init__(self, pathfinding_sector_flags=0, hint_index=0, first_link=0):
            self.pathfinding_sector_flags = pathfinding_sector_flags
            self.hint_index = hint_index
            self.first_link = first_link

    class Link():
        def __init__(self, vertex_1=0, vertex_2=0, link_flags=0, hint_index=0, forward_link=0, reverse_link=0, left_sector=0, right_sector=0):
            self.vertex_1 = vertex_1
            self.vertex_2 = vertex_2
            self.link_flags = link_flags
            self.hint_index = hint_index
            self.forward_link = forward_link
            self.reverse_link = reverse_link
            self.left_sector = left_sector
            self.right_sector = right_sector

    class Bsp2DNode():
        def __init__(self, plane=None, left_child=0, right_child=0):
            self.plane = plane
            self.left_child = left_child
            self.right_child = right_child

    class ObjectRef():
        def __init__(self, flags=0, first_sector=0, last_sector=0, bsps_tag_block=None, bsps_header=None, bsps=None, nodes_tag_block=None, nodes_header=None, nodes=None):
            self.flags = flags
            self.first_sector = first_sector
            self.last_sector = last_sector
            self.bsps_tag_block = bsps_tag_block
            self.bsps_header = bsps_header
            self.bsps = bsps
            self.nodes_tag_block = nodes_tag_block
            self.nodes_header = nodes_header
            self.nodes = nodes

    class BSP():
        def __init__(self, bsp_reference=0, first_sector=0, last_sector=0, node_index=0):
            self.bsp_reference = bsp_reference
            self.first_sector = first_sector
            self.last_sector = last_sector
            self.node_index = node_index

    class Node():
        def __init__(self, reference_frame_index=0, projection_axis=0, projection_sign=0):
            self.reference_frame_index = reference_frame_index
            self.projection_axis = projection_axis
            self.projection_sign = projection_sign

    class PathfindingHint():
        def __init__(self, hint_type=0, next_hint_index=0, hint_data_0=0, hint_data_1=0, hint_data_2=0, hint_data_3=0, hint_data_4=0, hint_data_5=0, hint_data_6=0, hint_data_7=0):
            self.hint_type = hint_type
            self.next_hint_index = next_hint_index
            self.hint_data_0 = hint_data_0
            self.hint_data_1 = hint_data_1
            self.hint_data_2 = hint_data_2
            self.hint_data_3 = hint_data_3
            self.hint_data_4 = hint_data_4
            self.hint_data_5 = hint_data_5
            self.hint_data_6 = hint_data_6
            self.hint_data_7 = hint_data_7

    class UserPlacedHint():
        def __init__(self, point_geometry_tag_block=None, point_geometry_header=None, point_geometry=None, ray_geometry_tag_block=None, ray_geometry_header=None, ray_geometry=None,
                     line_segment_geometry_tag_block=None, line_segment_geometry_header=None, line_segment_geometry=None, parallelogram_geometry_tag_block=None,
                     parallelogram_geometry_header=None, parallelogram_geometry=None, polygon_geometry_tag_block=None, polygon_geometry_header=None, polygon_geometry=None,
                     jump_hints_tag_block=None, jump_hints_header=None, jump_hints=None, climb_hints_tag_block=None, climb_hints_header=None, climb_hints=None,
                     well_hints_tag_block=None, well_hints_header=None, well_hints=None, flight_hints_tag_block=None, flight_hints_header=None, flight_hints=None):
            self.point_geometry_tag_block = point_geometry_tag_block
            self.point_geometry_header = point_geometry_header
            self.point_geometry = point_geometry
            self.ray_geometry_tag_block = ray_geometry_tag_block
            self.ray_geometry_header = ray_geometry_header
            self.ray_geometry = ray_geometry
            self.line_segment_geometry_tag_block = line_segment_geometry_tag_block
            self.line_segment_geometry_header = line_segment_geometry_header
            self.line_segment_geometry = line_segment_geometry
            self.parallelogram_geometry_tag_block = parallelogram_geometry_tag_block
            self.parallelogram_geometry_header = parallelogram_geometry_header
            self.parallelogram_geometry = parallelogram_geometry
            self.polygon_geometry_tag_block = polygon_geometry_tag_block
            self.polygon_geometry_header = polygon_geometry_header
            self.polygon_geometry = polygon_geometry
            self.jump_hints_tag_block = jump_hints_tag_block
            self.jump_hints_header = jump_hints_header
            self.jump_hints = jump_hints
            self.climb_hints_tag_block = climb_hints_tag_block
            self.climb_hints_header = climb_hints_header
            self.climb_hints = climb_hints
            self.well_hints_tag_block = well_hints_tag_block
            self.well_hints_header = well_hints_header
            self.well_hints = well_hints
            self.flight_hints_tag_block = flight_hints_tag_block
            self.flight_hints_header = flight_hints_header
            self.flight_hints = flight_hints

    class PointGeometry():
        def __init__(self, point=Vector(), reference_frame=0):
            self.point = point
            self.reference_frame = reference_frame

    class RayGeometry():
        def __init__(self, point=Vector(), reference_frame=0, vector=Vector()):
            self.point = point
            self.reference_frame = reference_frame
            self.vector = vector

    class LineSegmentGeometry():
        def __init__(self, flags=0, point_0=Vector(), reference_frame_0=0, point_1=Vector(), reference_frame_1=0):
            self.flags = flags
            self.point_0 = point_0
            self.reference_frame_0 = reference_frame_0
            self.point_1 = point_1
            self.reference_frame_1 = reference_frame_1

    class ParallelogramGeometry():
        def __init__(self, flags=0, point_0=Vector(), reference_frame_0=0, point_1=Vector(), reference_frame_1=0, point_2=Vector(), reference_frame_2=0, point_3=Vector(),
                     reference_frame_3=0):
            self.flags = flags
            self.point_0 = point_0
            self.reference_frame_0 = reference_frame_0
            self.point_1 = point_1
            self.reference_frame_1 = reference_frame_1
            self.point_2 = point_2
            self.reference_frame_2 = reference_frame_2
            self.point_3 = point_3
            self.reference_frame_3 = reference_frame_3

    class Hint():
        def __init__(self, flags=0, points_tag_block=None, points_header=None, points=None):
            self.flags = flags
            self.points_tag_block = points_tag_block
            self.points_header = points_header
            self.points = points

    class JumpHint():
        def __init__(self, flags=0, geometry_index=0, force_jump_height=0, control_flags=0):
            self.flags = flags
            self.geometry_index = geometry_index
            self.force_jump_height = force_jump_height
            self.control_flags = control_flags

    class ClimbHint():
        def __init__(self, flags=0, geometry_index=0):
            self.flags = flags
            self.geometry_index = geometry_index

    class WellPoint():
        def __init__(self, type=0, point=Vector(), reference_frame=0, sector_index=0, normal=(0.0, 0.0)):
            self.type = type
            self.point = point
            self.reference_frame = reference_frame
            self.sector_index = sector_index
            self.normal = normal

    class FlightHint():
        def __init__(self, points_tag_block=None, points_header=None, points=None):
            self.points_tag_block = points_tag_block
            self.points_header = points_header
            self.points = points

    class AIAnimationReference():
        def __init__(self, animation_name="", animation_reference=None):
            self.animation_name = animation_name
            self.animation_reference = animation_reference

    class AIConversation():
        def __init__(self, name="", flags=0, trigger_distance=0.0, run_to_player_distance=0.0, participants_tag_block=None, lines_tag_block=None, unknown_tag_block=None, 
                     participants_header=None, lines_header=None, unknown_header=None , participants=None, lines=None, unknown=None):
            self.name = name
            self.flags = flags
            self.trigger_distance = trigger_distance
            self.run_to_player_distance = run_to_player_distance
            self.participants_tag_block = participants_tag_block
            self.lines_tag_block = lines_tag_block
            self.unknown_tag_block = unknown_tag_block
            self.participants_header = participants_header
            self.lines_header = lines_header
            self.unknown_header = unknown_header
            self.participants = participants
            self.lines = lines
            self.unknown = unknown

    class Participant():
        def __init__(self, use_this_object=0, set_new_name=0, encounter_name=""):
            self.use_this_object = use_this_object
            self.set_new_name = set_new_name
            self.encounter_name = encounter_name

    class Line():
        def __init__(self, flags=0, participant=0, addresses=0, addresse_participant=0, line_delay_time=0.0, variant_1=None, variant_2=None, variant_3=None, variant_4=None,
                     variant_5=None, variant_6=None):
            self.flags = flags
            self.participant = participant
            self.addresses = addresses
            self.addresse_participant = addresse_participant
            self.line_delay_time = line_delay_time
            self.variant_1 = variant_1
            self.variant_2 = variant_2
            self.variant_3 = variant_3
            self.variant_4 = variant_4
            self.variant_5 = variant_5
            self.variant_6 = variant_6

    class Script():
        def __init__(self, name="", script_type=0, return_type=0, root_expression_index=0):
            self.name = name
            self.script_type = script_type
            self.return_type = return_type
            self.root_expression_index = root_expression_index

    class ScriptGlobal():
        def __init__(self, name="", return_type=0, initialization_expression_index=0):
            self.name = name
            self.return_type = return_type
            self.initialization_expression_index = initialization_expression_index

    class SourceFile():
        def __init__(self, name="", source_tag_data=None, source=""):
            self.name = name
            self.source_tag_data = source_tag_data
            self.source = source

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
        def __init__(self, name="", position=Vector(), reference_frame=0, surface_index=0, facing_direction=(0.0, 0.0)):
            self.name = name
            self.position = position
            self.reference_frame = reference_frame
            self.surface_index = surface_index
            self.facing_direction = facing_direction

    class CutsceneFlag():
        def __init__(self, name="", position=Vector(), facing=(0.0, 0.0)):
            self.name = name
            self.position = position
            self.facing = facing

    class CutsceneCameraPoint():
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

    class ScenarioResource():
        def __init__(self, references_tag_block=None, references_header=None, references=None, script_source_tag_block=None, script_source_header=None, script_source=None,
                     ai_resources_tag_block=None, ai_resources_header=None, ai_resources=None):
            self.references_tag_block = references_tag_block
            self.references_header = references_header
            self.references = references
            self.script_source_tag_block = script_source_tag_block
            self.script_source_header = script_source_header
            self.script_source = script_source
            self.ai_resources_tag_block = ai_resources_tag_block
            self.ai_resources_header = ai_resources_header
            self.ai_resources = ai_resources

    class OldStructurePhysics():
        def __init__(self, physics_tag_data=None, physics_data=None, object_identifiers_tag_block=None, object_identifiers_header=None, mopp_bounds_min=Vector(),
                     mopp_bounds_max=Vector(), object_identifiers=None):
            self.physics_tag_data = physics_tag_data
            self.physics_data = physics_data
            self.object_identifiers_tag_block = object_identifiers_tag_block
            self.object_identifiers_header = object_identifiers_header
            self.mopp_bounds_min = mopp_bounds_min
            self.mopp_bounds_max = mopp_bounds_max
            self.object_identifiers = object_identifiers

    class ObjectIdentifier:
        def __init__(self, unique_id=0, origin_bsp_index=0, object_type=0, source=0, sobj_header=None):
            self.unique_id = unique_id
            self.origin_bsp_index = origin_bsp_index
            self.object_type = object_type
            self.source = source
            self.sobj_header = sobj_header

    class HSUnitSeat:
        def __init__(self, unit_definition_tag_index=0, unit_seats=0):
            self.unit_definition_tag_index = unit_definition_tag_index
            self.unit_seats = unit_seats

    class HSSyntaxDatum:
        def __init__(self, datum_header=0, script_index_function_index_con=0, datum_type=0, flags=0, next_node_index=0, data=0, source_offset=0):
            self.datum_header = datum_header
            self.script_index_function_index_con = script_index_function_index_con
            self.datum_type = datum_type
            self.flags = flags
            self.next_node_index = next_node_index
            self.data = data
            self.source_offset = source_offset

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

    class AreaSet():
        def __init__(self, area_type=0, zone_index=0, area_index=0):
            self.area_type = area_type
            self.zone_index = zone_index
            self.area_index = area_index

    class SetTrigger():
        def __init__(self, combination_rule=0, dialogue_type=0, triggers_tag_block=None, triggers_header=None, triggers=None):
            self.combination_rule = combination_rule
            self.dialogue_type = dialogue_type
            self.triggers_tag_block = triggers_tag_block
            self.triggers_header = triggers_header
            self.triggers = triggers

    class OrderEnding():
        def __init__(self, next_order_index=0, combination_rule=0, delay_time=0.0, dialogue_type=0, triggers_tag_block=None, triggers_header=None, triggers=None):
            self.next_order_index = next_order_index
            self.combination_rule = combination_rule
            self.delay_time = delay_time
            self.dialogue_type = dialogue_type
            self.triggers_tag_block = triggers_tag_block
            self.triggers_header = triggers_header
            self.triggers = triggers

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

    class WeatherPalette():
        def __init__(self, name="", weather_system=None, wind=None, wind_direction=Vector(), wind_magnitude=0.0, wind_scale_function=""):
            self.name = name
            self.weather_system = weather_system
            self.wind = wind
            self.wind_direction = wind_direction
            self.wind_magnitude = wind_magnitude
            self.wind_scale_function = wind_scale_function

    class ScavengerHuntObject:
        def __init__(self, exported_name="", scenario_object_name_index=0):
            self.exported_name = exported_name
            self.scenario_object_name_index = scenario_object_name_index

    class ScenarioClusterData():
        def __init__(self, bsp=None, background_sounds_tag_block=None, sound_environments_tag_block=None, bsp_checksum=0, cluster_centroids_tag_block=None,
                     weather_properties_tag_block=None, atmospheric_fog_properties_tag_block=None, background_sounds_header=None, sound_environments_header=None,
                     cluster_centroids_header=None, weather_properties_header=None, atmospheric_fog_properties_header=None, background_sounds=None, sound_environments=None,
                     cluster_centroids=None, weather_properties=None, atmospheric_fog_properties=None):
            self.bsp = bsp
            self.background_sounds_tag_block = background_sounds_tag_block
            self.sound_environments_tag_block = sound_environments_tag_block
            self.bsp_checksum = bsp_checksum
            self.cluster_centroids_tag_block = cluster_centroids_tag_block
            self.weather_properties_tag_block = weather_properties_tag_block
            self.atmospheric_fog_properties_tag_block = atmospheric_fog_properties_tag_block
            self.background_sounds_header = background_sounds_header
            self.sound_environments_header = sound_environments_header
            self.cluster_centroids_header = cluster_centroids_header
            self.weather_properties_header = weather_properties_header
            self.atmospheric_fog_properties_header = atmospheric_fog_properties_header
            self.background_sounds = background_sounds
            self.sound_environments = sound_environments
            self.cluster_centroids = cluster_centroids
            self.weather_properties = weather_properties
            self.atmospheric_fog_properties = atmospheric_fog_properties

    class SpawnData():
        def __init__(self, dynamic_spawn_lower_height=0.0, dynamic_spawn_upper_height=0.0, game_object_reset_height=0.0, dynamic_spawn_overloads_header=None, 
                     static_respawn_zones_header=None, static_initial_spawn_zones_header=None, dynamic_spawn_overloads_tag_block=None, static_respawn_zones_tag_block=None, 
                     static_initial_spawn_zones_tag_block=None, dynamic_spawn_overloads=None, static_respawn_zones=None, static_initial_spawn_zones=None):
            self.dynamic_spawn_lower_height = dynamic_spawn_lower_height
            self.dynamic_spawn_upper_height = dynamic_spawn_upper_height
            self.game_object_reset_height = game_object_reset_height
            self.dynamic_spawn_overloads_header = dynamic_spawn_overloads_header
            self.static_respawn_zones_header = static_respawn_zones_header
            self.static_initial_spawn_zones_header = static_initial_spawn_zones_header
            self.dynamic_spawn_overloads_tag_block = dynamic_spawn_overloads_tag_block
            self.static_respawn_zones_tag_block = static_respawn_zones_tag_block
            self.static_initial_spawn_zones_tag_block = static_initial_spawn_zones_tag_block
            self.dynamic_spawn_overloads = dynamic_spawn_overloads
            self.static_respawn_zones = static_respawn_zones
            self.static_initial_spawn_zones = static_initial_spawn_zones

    class DynamicSpawnOverload():
        def __init__(self, overload_type=0, inner_radius=0.0, outer_radius=0.0, weight=0.0):
            self.overload_type = overload_type
            self.inner_radius = inner_radius
            self.outer_radius = outer_radius
            self.weight = weight

    class StaticSpawnZone():
        def __init__(self, name="", name_length=0, relevant_teams=0, relevant_games=0, flags=0, position=Vector(), lower_height=0.0, upper_height=0.0, inner_radius=0.0, 
                     outer_radius=0.0, weight=0.0, sszd_header=None):
            self.name = name
            self.name_length = name_length
            self.relevant_teams = relevant_teams
            self.relevant_games = relevant_games
            self.flags = flags
            self.position = position
            self.lower_height = lower_height
            self.upper_height = upper_height
            self.inner_radius = inner_radius
            self.outer_radius = outer_radius
            self.weight = weight
            self.sszd_header = sszd_header

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

    class AtmosphericFogPalette():
        def __init__(self, name="", name_length=0, atmospheric_fog_color_RGBA=(0, 0, 0, 255), atmospheric_fog_spread_distance=0.0, atmospheric_fog_maximum_density=0.0, 
                     atmospheric_fog_start_distance=0.0, atmospheric_fog_opaque_distance=0.0, secondary_fog_color_RGBA=(0, 0, 0, 255), secondary_fog_maximum_density=0.0, 
                     secondary_fog_start_distance=0.0, secondary_fog_opaque_distance=0.0, planar_color_RGBA=(0, 0, 0, 255), planar_max_density=0.0, planar_override_amount=0.0, 
                     planar_min_distance_bias=0.0, patchy_color_RGBA=(0, 0, 0, 255), patchy_density=(0.0, 0.0), patchy_distance=(0.0, 0.0), patchy_fog=None, 
                     mixers_header=None, mixers_tag_block=None, mixers=None, amount=0.0, threshold=0.0, brightness=0.0, gamma_power=0.0, camera_immersion_flags=0):
            self.name = name
            self.name_length = name_length
            self.atmospheric_fog_color_RGBA = atmospheric_fog_color_RGBA
            self.atmospheric_fog_spread_distance = atmospheric_fog_spread_distance
            self.atmospheric_fog_maximum_density = atmospheric_fog_maximum_density
            self.atmospheric_fog_start_distance = atmospheric_fog_start_distance
            self.atmospheric_fog_opaque_distance = atmospheric_fog_opaque_distance
            self.secondary_fog_color_RGBA = secondary_fog_color_RGBA
            self.secondary_fog_maximum_density = secondary_fog_maximum_density
            self.secondary_fog_start_distance = secondary_fog_start_distance
            self.secondary_fog_opaque_distance = secondary_fog_opaque_distance
            self.planar_color_RGBA = planar_color_RGBA
            self.planar_max_density = planar_max_density
            self.planar_override_amount = planar_override_amount
            self.planar_min_distance_bias = planar_min_distance_bias
            self.patchy_color_RGBA = patchy_color_RGBA
            self.patchy_density = patchy_density
            self.patchy_distance = patchy_distance
            self.patchy_fog = patchy_fog
            self.mixers_header = mixers_header
            self.mixers_tag_block = mixers_tag_block
            self.mixers = mixers
            self.amount = amount
            self.threshold = threshold
            self.brightness = brightness
            self.gamma_power = gamma_power
            self.camera_immersion_flags = camera_immersion_flags

    class Mixer():
        def __init__(self, atmospheric_fog_source="", atmospheric_fog_source_length=0, interpolator="", interpolator_length=0):
            self.atmospheric_fog_source = atmospheric_fog_source
            self.atmospheric_fog_source_length = atmospheric_fog_source_length
            self.interpolator = interpolator
            self.interpolator_length = interpolator_length

    class PlanarFogPalette():
        def __init__(self, name="", name_length=0, planar_fog=None):
            self.name = name
            self.name_length = name_length
            self.planar_fog = planar_fog

    class Flock():
        def __init__(self, bsp=0, bounding_volume=0, flags=0, ecology_margin=0.0, sources_header=None, sources_tag_block=None, sources=None, sinks_header=None, sinks_tag_block=None, 
                     sinks=None, production_frequency=0.0, scale=(0.0, 0.0), creature=None, boid_count=(0, 0), neighborhood_radius=0.0, avoidance_radius=0.0, forward_scale=0.0, 
                     alignment_scale=0.0, avoidance_scale=0.0, leveling_force_scale=0.0, sink_scale=0.0, perception_angle=0.0, average_throttle=0.0, maximum_throttle=0.0, 
                     position_scale=0.0, position_min_radius=0.0, position_max_radius=0.0, movement_weight_threshold=0.0, danger_radius=0.0, danger_scale=0.0, random_offset_scale=0.0, 
                     random_offset_period=(0.0, 0.0), flock_name="", flock_name_length=0):
            self.bsp = bsp
            self.bounding_volume = bounding_volume
            self.flags = flags
            self.ecology_margin = ecology_margin
            self.sources_header = sources_header
            self.sources_tag_block = sources_tag_block
            self.sources = sources
            self.sinks_header = sinks_header
            self.sinks_tag_block = sinks_tag_block
            self.sinks = sinks
            self.production_frequency = production_frequency
            self.scale = scale
            self.creature = creature
            self.boid_count = boid_count
            self.neighborhood_radius = neighborhood_radius
            self.avoidance_radius = avoidance_radius
            self.forward_scale = forward_scale
            self.alignment_scale = alignment_scale
            self.avoidance_scale = avoidance_scale
            self.leveling_force_scale = leveling_force_scale
            self.sink_scale = sink_scale
            self.perception_angle = perception_angle
            self.average_throttle = average_throttle
            self.maximum_throttle = maximum_throttle
            self.position_scale = position_scale
            self.position_min_radius = position_min_radius
            self.position_max_radius = position_max_radius
            self.movement_weight_threshold = movement_weight_threshold
            self.danger_radius = danger_radius
            self.danger_scale = danger_scale
            self.random_offset_scale = random_offset_scale
            self.random_offset_period = random_offset_period
            self.flock_name = flock_name
            self.flock_name_length = flock_name_length

    class Source():
        def __init__(self, position=Vector(), starting_yaw_pitch=(0.0, 0.0), radius=0.0, weight=0.0):
            self.position = position
            self.starting_yaw_pitch = starting_yaw_pitch
            self.radius = radius
            self.weight = weight

    class Sink():
        def __init__(self, position=Vector(), radius=0.0):
            self.position = position
            self.radius = radius

    class Decorator():
        def __init__(self, grid_origin=Vector(), cell_count_per_dimension=0, cache_blocks_header=None, cache_blocks_tag_block=None, cache_blocks=None, groups_header=None, 
                     groups_tag_block=None, groups=None, cells_header=None, cells_tag_block=None, cells=None, decals_header=None, decals_tag_block=None, decals=None):
            self.grid_origin = grid_origin
            self.cell_count_per_dimension = cell_count_per_dimension
            self.cache_blocks_header = cache_blocks_header
            self.cache_blocks_tag_block = cache_blocks_tag_block
            self.cache_blocks = cache_blocks
            self.groups_header = groups_header
            self.groups_tag_block = groups_tag_block
            self.groups = groups
            self.cells_header = cells_header
            self.cells_tag_block = cells_tag_block
            self.cells = cells
            self.decals_header = decals_header
            self.decals_tag_block = decals_tag_block
            self.decals = decals

    class CacheBlock():
        def __init__(self, block_offset=0, block_size=0, section_data_size=0, resource_data_size=0, resources_header=None, resources_tag_block=None, resources=None, 
                     owner_tag_section_offset=0, cache_block_data_header=None, cache_block_data_tag_block=None, cache_block_data=None, blok_header=None):
            self.block_offset = block_offset
            self.block_size = block_size
            self.section_data_size = section_data_size
            self.resource_data_size = resource_data_size
            self.resources_header = resources_header
            self.resources_tag_block = resources_tag_block
            self.resources = resources
            self.owner_tag_section_offset = owner_tag_section_offset
            self.cache_block_data_header = cache_block_data_header
            self.cache_block_data_tag_block = cache_block_data_tag_block
            self.cache_block_data = cache_block_data
            self.blok_header = blok_header

    class Resource:
        def __init__(self, resource_type=0, primary_locator=0, secondary_locator=0, resource_data_size=0, resource_data_offset=0):
            self.resource_type = resource_type
            self.primary_locator = primary_locator
            self.secondary_locator = secondary_locator
            self.resource_data_size = resource_data_size
            self.resource_data_offset = resource_data_offset

    class CacheBlockData():
        def __init__(self, placements_header=None, placements_tag_block=None, placements=None, decal_vertices_header=None, decal_vertices_tag_block=None, decal_vertices=None, 
                     decal_indices_header=None, decal_indices_tag_block=None, decal_indices=None, sprite_vertices_header=None, sprite_vertices_tag_block=None, sprite_vertices=None, 
                     sprite_indices_header=None, sprite_indices_tag_block=None, sprite_indices=None):
            self.placements_header = placements_header
            self.placements_tag_block = placements_tag_block
            self.placements = placements
            self.decal_vertices_header = decal_vertices_header
            self.decal_vertices_tag_block = decal_vertices_tag_block
            self.decal_vertices = decal_vertices
            self.decal_indices_header = decal_indices_header
            self.decal_indices_tag_block = decal_indices_tag_block
            self.decal_indices = decal_indices
            self.sprite_vertices_header = sprite_vertices_header
            self.sprite_vertices_tag_block = sprite_vertices_tag_block
            self.sprite_vertices = sprite_vertices
            self.sprite_indices_header = sprite_indices_header
            self.sprite_indices_tag_block = sprite_indices_tag_block
            self.sprite_indices = sprite_indices

    class Placement():
        def __init__(self, internal_data_1=0, compressed_position=0, tint_color=(0, 0, 0, 255), lightmap_color=(0, 0, 0, 255), compressed_light_direction=0, 
                     compressed_light_2_direction=0):
            self.internal_data_1 = internal_data_1
            self.compressed_position = compressed_position
            self.tint_color = tint_color
            self.lightmap_color = lightmap_color
            self.compressed_light_direction = compressed_light_direction
            self.compressed_light_2_direction = compressed_light_2_direction

    class DecalVertex():
        def __init__(self, position=Vector(), texcoord_0=(0.0, 0.0), texcoord_1=(0.0, 0.0), color=(0, 0, 0, 255)):
            self.position = position
            self.texcoord_0 = texcoord_0
            self.texcoord_1 = texcoord_1
            self.color = color

    class SpriteVertex():
        def __init__(self, position=Vector(), offset=Vector(), axis=Vector(), texcoord=(0.0, 0.0), color=(0, 0, 0, 255)):
            self.position = position
            self.offset = offset
            self.axis = axis
            self.texcoord = texcoord
            self.color = color

    class Group():
        def __init__(self, decorator_set=0, decorator_type=0, shader_index=0, compressed_radius=0, cluster=0, cache_block=0, decorator_start_index=0, decorator_count=0, 
                     vertex_start_offset=0, vertex_count=0, index_start_offset=0, index_count=0, compressed_bounding_center=0):
            self.decorator_set = decorator_set
            self.decorator_type = decorator_type
            self.shader_index = shader_index
            self.compressed_radius = compressed_radius
            self.cluster = cluster
            self.cache_block = cache_block
            self.decorator_start_index = decorator_start_index
            self.decorator_count = decorator_count
            self.vertex_start_offset = vertex_start_offset
            self.vertex_count = vertex_count
            self.index_start_offset = index_start_offset
            self.index_count = index_count
            self.compressed_bounding_center = compressed_bounding_center

    class Cell():
        def __init__(self, child_index_0=0, child_index_1=0, child_index_2=0, child_index_3=0, child_index_4=0, child_index_5=0, child_index_6=0, child_index_7=0, 
                     cache_block_index=0, group_count=0, group_start_index=0):
            self.child_index_0 = child_index_0
            self.child_index_1 = child_index_1
            self.child_index_2 = child_index_2
            self.child_index_3 = child_index_3
            self.child_index_4 = child_index_4
            self.child_index_5 = child_index_5
            self.child_index_6 = child_index_6
            self.child_index_7 = child_index_7
            self.cache_block_index = cache_block_index
            self.group_count = group_count
            self.group_start_index = group_start_index

    class DecoratorDecal():
        def __init__(self, decorator_set=0, decorator_class=0, decorator_permutation=0, sprite_index=0, position=Vector(), left=Vector(), up=Vector(), extents=Vector(), 
                     previous_position=Vector()):
            self.decorator_set = decorator_set
            self.decorator_class = decorator_class
            self.decorator_permutation = decorator_permutation
            self.sprite_index = sprite_index
            self.position = position
            self.left = left
            self.up = up
            self.extents = extents
            self.previous_position = previous_position

    class Creature(Object):
        def __init__(self, sobj_header=None, obj0_header=None):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header

    class BSPTransitionVolume():
        def __init__(self, bsp_index_key=0, trigger_volume=0):
            self.bsp_index_key = bsp_index_key
            self.trigger_volume = trigger_volume

    class StructureBSPLighting():
        def __init__(self, bsp=None, lighting_points_header=None, lighting_points_tag_block=None, lighting_points=None):
            self.bsp = bsp
            self.lighting_points_header = lighting_points_header
            self.lighting_points_tag_block = lighting_points_tag_block
            self.lighting_points = lighting_points

    class EditorFolder():
        def __init__(self, parent_folder=0, name=""):
            self.parent_folder = parent_folder
            self.name = name

    class LevelData():
        def __init__(self, level_strings=None, campaign_level_data_header=None, campaign_level_data_tag_block=None, campaign_level_data=None, multiplayer_level_data_header=None, 
                     multiplayer_level_data_tag_block=None, multiplayer_level_data=None):
            self.level_strings = level_strings
            self.campaign_level_data_header = campaign_level_data_header
            self.campaign_level_data_tag_block = campaign_level_data_tag_block
            self.campaign_level_data = campaign_level_data
            self.multiplayer_level_data_header = multiplayer_level_data_header
            self.multiplayer_level_data_tag_block = multiplayer_level_data_tag_block
            self.multiplayer_level_data = multiplayer_level_data

    class CampaignLevelData():
        def __init__(self, campaign_id=0, map_id=0, bitmap=None):
            self.campaign_id = campaign_id
            self.map_id = map_id
            self.bitmap = bitmap

    class MultiplayerLevelData():
        def __init__(self, map_id=0, bitmap=None, path="", sort_order=0, flags=0, max_teams_none=0, max_teams_ctf=0, max_teams_slayer=0, max_teams_oddball=0, max_teams_king=0, 
                     max_teams_race=0, max_teams_head_hunter=0, max_teams_juggernaut=0, max_teams_territories=0, max_teams_assault=0, max_teams_10_stub=0, max_teams_medic=0, 
                     max_teams_vip=0, max_teams_infection=0, max_teams_14_stub=0, max_teams_15_stub=0):
            self.map_id = map_id
            self.bitmap = bitmap
            self.path = path
            self.sort_order = sort_order
            self.flags = flags
            self.max_teams_none = max_teams_none
            self.max_teams_ctf = max_teams_ctf
            self.max_teams_slayer = max_teams_slayer
            self.max_teams_oddball = max_teams_oddball
            self.max_teams_king = max_teams_king
            self.max_teams_race = max_teams_race
            self.max_teams_head_hunter = max_teams_head_hunter
            self.max_teams_juggernaut = max_teams_juggernaut
            self.max_teams_territories = max_teams_territories
            self.max_teams_assault = max_teams_assault
            self.max_teams_10_stub = max_teams_10_stub
            self.max_teams_medic = max_teams_medic
            self.max_teams_vip = max_teams_vip
            self.max_teams_infection = max_teams_infection
            self.max_teams_14_stub = max_teams_14_stub
            self.max_teams_15_stub = max_teams_15_stub

    class Interpolator(ShaderFunction):
        def __init__(self, name="", name_length=0, accelerator_name="", accelerator_name_length=0, multiplier_name="", multiplier_name_length=0):
            super().__init__()
            self.name = name
            self.name_length = name_length
            self.accelerator_name = accelerator_name
            self.accelerator_name_length = accelerator_name_length
            self.multiplier_name = multiplier_name
            self.multiplier_name_length = multiplier_name_length

    class ScreenEffectReference():
        def __init__(self, screen_effect=None, primary_input="", primary_input_name_length=0, secondary_input="", secondary_input_name_length=0):
            self.screen_effect = screen_effect
            self.primary_input = primary_input
            self.primary_input_name_length = primary_input_name_length
            self.secondary_input = secondary_input
            self.secondary_input_name_length = secondary_input_name_length
