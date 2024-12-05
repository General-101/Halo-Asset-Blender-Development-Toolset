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

class DataTypesEnum(Enum):
    none = 0
    clusters = auto()
    scenery = auto()
    bipeds = auto()
    vehicles = auto()
    equipment = auto()
    weapons = auto()
    machines = auto()
    controls = auto()
    light_fixtures = auto()
    sound_scenery = auto()
    player_starting_locations = auto()
    netgame_flags = auto()
    netgame_equipment = auto()
    decals = auto()
    encounters = auto()
    instances = auto()

class ScenarioTypeEnum(Enum):
    solo = 0
    multiplayer = auto()
    mainmenu = auto()

class ScenarioFlags(Flag):
    cortana_hack = auto()
    use_demo_ui = auto()
    color_correction_ntsc_srgb = auto()
    do_not_apply_bungie_campaign_patches = auto()

class ResourceTypeEnum(Enum):
    bitmap = 0
    sound = auto()

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

class BoundsModeEnum(Enum):
    clip = 0
    clip_and_normalize = auto()
    scale_to_fit = auto()

class ObjectFlags(Flag):
    automatically = auto()
    on_easy = auto()
    on_normal = auto()
    on_hard = auto()
    use_player_appearance = auto()

class UnitFlags(Flag):
    dead = auto()

class VehicleFlags(Flag):
    slayer_default = auto()
    ctf_default = auto()
    king_default = auto()
    oddball_default = auto()
    unused0 = auto()
    unused1 = auto()
    unused2 = auto()
    unused3 = auto()
    slayer_allowed = auto()
    ctf_allowed = auto()
    king_allowed = auto()
    oddball_allowed = auto()
    unused4 = auto()
    unused5 = auto()
    unused6 = auto()
    unused7 = auto()

class ItemFlags(Flag):
    initially_at_rest_doesnt_fall = auto()
    obsolete = auto()
    does_accelerate_moves_due_to_explosions = auto()

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

class ControlFlags(Flag):
    usable_from_both_sides = auto()

class GametypeEnum(Enum):
    none = 0
    ctf = auto()
    slayer = auto()
    oddball = auto()
    king_of_the_hill = auto()
    race = auto()
    terminator = auto()
    stub = auto()
    ignored1 = auto()
    ignored2 = auto()
    ignored3 = auto()
    ignored4 = auto()
    all_games = auto()
    all_except_ctf = auto()
    all_except_race_and_ctf = auto()

class NetGameEnum(Enum):
    ctf_flag = 0
    unused1 = auto()
    oddball_ball_spawn = auto()
    race_track = auto()
    race_vehicle = auto()
    unused5 = auto()
    teleport_from = auto()
    teleport_to = auto()
    hill_flag = auto()

class NetGameEquipment(Flag):
    levitate = auto()

class StartingEquipment(Flag):
    no_grenades = auto()
    plasma_grenades_only = auto()
    type2_grenades_only = auto()
    type3_grenades_only = auto()

class EncounterFlags(Flag):
    not_intially_created = auto()
    respawn_enabled = auto()
    initially_blind = auto()
    initially_deaf = auto()
    initially_braindead = auto()
    _3d_firing_positions = auto()
    manual_bsp_index_specified = auto()

class TeamEnum(Enum):
    default_by_unit = 0
    player = auto()
    human = auto()
    covenant = auto()
    flood = auto()
    sentinel = auto()
    unused6 = auto()
    unused7 = auto()
    unused8 = auto()
    unused9 = auto()

class SearchBehaviorEnum(Enum):
    normal = 0
    never = auto()
    tenacious = auto()

class StateEnum(Enum):
    none = 0
    sleeping = auto()
    alert = auto()
    moving_repeat_same_position = auto()
    moving_loop = auto()
    moving_loop_back_and_forth = auto()
    moving_loop_randomly = auto()
    moving_randomly = auto()
    guarding = auto()
    guarding_at_guard_position = auto()
    searching = auto()
    fleeing = auto()

class SquadFlags(Flag):
    unused = auto()
    never_search = auto()
    start_timer_immediately = auto()
    no_timer_delay_forever = auto()
    magic_sight_after_timer = auto()
    automatic_migration = auto()

class LeaderEnum(Enum):
    normal = 0
    none = auto()
    random = auto()
    sgt_johnson = auto()
    sgt_lehto = auto()

class GroupFlags(Flag):
    a = auto()
    b = auto()
    c = auto()
    d = auto()
    e = auto()
    f = auto()
    g = auto()
    h = auto()
    i = auto()
    j = auto()
    k = auto()
    l = auto()
    m = auto()
    n = auto()
    o = auto()
    p = auto()
    q = auto()
    r = auto()
    s = auto()
    t = auto()
    u = auto()
    v = auto()
    w = auto()
    x = auto()
    y = auto()
    z = auto()

class MajorUpgradeEnum(Enum):
    normal = 0
    few = auto()
    many = auto()
    none = auto()
    all = auto()

class PlatoonFlags(Flag):
    flee_when_maneuvering = auto()
    say_advancing_when_maneuver = auto()
    start_in_defending_state = auto()

class PlatoonStrengthEnum(Enum):
    never = 0
    less_75_percent_strength = auto()
    less_50_percent_strength = auto()
    less_25_percent_strength = auto()
    anybody_dead = auto()
    _25_percent_dead = auto()
    _50_percent_dead = auto()
    _75_percent_dead = auto()
    all_but_one_dead = auto()
    al_dead = auto()

class GroupEnum(Enum):
    a = 0
    b = auto()
    c = auto()
    d = auto()
    e = auto()
    f = auto()
    g = auto()
    h = auto()
    i = auto()
    j = auto()
    k = auto()
    l = auto()
    m = auto()
    n = auto()
    o = auto()
    p = auto()
    q = auto()
    r = auto()
    s = auto()
    t = auto()
    u = auto()
    v = auto()
    w = auto()
    x = auto()
    y = auto()
    z = auto()

class CommandListFlags(Flag):
    allow_initiative = auto()
    allow_targeting = auto()
    disable_looking = auto()
    disable_communication = auto()
    disable_falling_damage = auto()
    manual_bsp_index = auto()

class AtomTypeEnum(Enum):
    pause = 0
    go_to = auto()
    go_to_and_face = auto()
    move_in_direction = auto()
    look = auto()
    animation_mode = auto()
    crouch = auto()
    shoot = auto()
    grenade = auto()
    vehicle = auto()
    running_jump = auto()
    targeted_jump = auto()
    script = auto()
    animate = auto()
    recording = auto()
    action = auto()
    vocalize = auto()
    targeting = auto()
    initiative = auto()
    wait = auto()
    loop = auto()
    die = auto()
    move_immediate = auto()
    look_random = auto()
    look_player = auto()
    look_object = auto()
    set_radius = auto()
    teleport = auto()

class AIConversationFlags(Flag):
    stop_if_death = auto()
    stop_if_damaged = auto()
    stop_if_visible_enemy = auto()
    stop_if_alerted_to_enemy = auto()
    player_must_be_visible = auto()
    stop_other_actions = auto()
    keep_trying_to_play = auto()
    player_must_be_looking = auto()

class ParticipantFlags(Flag):
    optional = auto()
    has_alternate = auto()
    is_alternate = auto()

class SelectionTypeEnum(Enum):
    friendly_actor = 0
    disembodied = auto()
    in_players_vehicle = auto()
    not_in_a_vehicle = auto()
    prefer_sergeant = auto()
    any_actor = auto()
    radio_unit = auto()
    radio_sergeant = auto()

class ActorTypeEnum(Enum):
    elite = 0
    jackal = auto()
    grunt = auto()
    hunter = auto()
    engineer = auto()
    assassin = auto()
    player = auto()
    marine = auto()
    crew = auto()
    combat_form = auto()
    infection_form = auto()
    carrier_form = auto()
    monitor = auto()
    sentinel = auto()
    none = auto()
    mounted_weapon = auto()

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
    trigger_volume = auto()
    cutscene_flag = auto()
    cutscene_camera_point = auto()
    cutscene_title = auto()
    cutscene_recording = auto()
    device_group = auto()
    ai = auto()
    ai_command_list = auto()
    starting_profile = auto()
    conversation = auto()
    navpoint = auto()
    hud_message = auto()
    object_list = auto()
    sound = auto()
    effect = auto()
    damage = auto()
    looping_sound = auto()
    animation_graph = auto()
    actor_variant = auto()
    damage_effect = auto()
    object_definition = auto()
    game_difficulty = auto()
    team = auto()
    ai_default_state = auto()
    actor_type = auto()
    hud_corner = auto()
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

class StyleEnum(Enum):
    plain = 0
    bold = auto()
    italics = auto()
    condensed = auto()
    underlined = auto()

class JustificationEnum(Enum):
    left = 0
    right = auto()
    center = auto()

class TextFlags(Flag):
    wrap_horizontally = auto()
    wrap_vertically = auto()
    center_vertically = auto()
    bottom_justify = auto()

class ScenarioAsset():
    def __init__(self, header=None, skies=None, child_scenarios=None, predicted_resources=None, functions=None, editor_scenario_data=None, comments=None, 
                 scavenger_hunt_objects=None, object_names=None, scenery=None, scenery_palette=None, bipeds=None, biped_palette=None, vehicles=None, vehicle_palette=None, 
                 equipment=None, equipment_palette=None, weapons=None, weapon_palette=None, device_groups=None, device_machines=None, device_machine_palette=None, 
                 device_controls=None, device_control_palette=None, device_light_fixtures=None, device_light_fixtures_palette=None, sound_scenery=None, 
                 sound_scenery_palette=None, player_starting_profiles=None, player_starting_locations=None, trigger_volumes=None, recorded_animations=None, 
                 netgame_flags=None, netgame_equipment=None, starting_equipment=None, bsp_switch_trigger_volumes=None, decals=None, decal_palette=None, 
                 detail_object_collection_palette =None, actor_palette=None, encounters=None, command_lists=None, ai_animation_references=None, ai_script_references=None, 
                 ai_recording_references=None, ai_conversations=None, script_syntax_data=None, script_string_data=None, scripts=None, script_globals=None, references=None, 
                 source_files=None, cutscene_flags=None, cutscene_camera_points=None, cutscene_titles=None, structure_bsps=None, dont_use_tag_ref=None, 
                 wont_use_tag_ref=None, cant_use_tag_ref=None, skies_tag_block=None, scenario_type=0, scenario_flags=0, child_scenarios_tag_block=None, local_north=0.0, 
                 predicted_resources_tag_block=None, functions_tag_block=None, comments_tag_block=None, scavenger_hunt_objects_tag_block=None, 
                 object_names_tag_block=None, scenery_tag_block=None, scenery_palette_tag_block=None, bipeds_tag_block=None, biped_palette_tag_block=None, 
                 vehicles_tag_block=None, vehicle_palette_tag_block=None, equipment_tag_block=None, equipment_palette_tag_block=None, weapons_tag_block=None, 
                 weapon_palette_tag_block=None, device_groups_tag_block=None, machines_tag_block=None, machine_palette_tag_block=None, controls_tag_block=None, 
                 control_palette_tag_block=None, light_fixtures_tag_block=None, light_fixtures_palette_tag_block=None, sound_scenery_tag_block=None, 
                 sound_scenery_palette_tag_block=None, player_starting_profile_tag_block=None, player_starting_locations_tag_block=None, trigger_volumes_tag_block=None, 
                 recorded_animations_tag_block=None, netgame_flags_tag_block=None, netgame_equipment_tag_block=None, starting_equipment_tag_block=None, 
                 bsp_switch_trigger_volumes_tag_block=None, decals_tag_block=None, decal_palette_tag_block=None, detail_object_collection_palette_tag_block=None, 
                 actor_palette_tag_block=None, encounters_tag_block=None, command_lists_tag_block=None, ai_animation_references_tag_block=None, 
                 ai_script_references_tag_block=None, ai_recording_references_tag_block=None, ai_conversations_tag_block=None, script_syntax_data_tag_data=None, 
                 script_string_data_tag_data=None, scripts_tag_block=None, globals_tag_block=None, references_tag_block=None, source_files_tag_block=None, 
                 cutscene_flags_tag_block=None, cutscene_camera_points_tag_block=None, cutscene_titles_tag_block=None, custom_object_names_tag_ref=None, 
                 chapter_title_text_tag_ref=None, hud_messages_tag_ref=None, structure_bsps_tag_block=None):
        self.header = header
        self.skies = skies
        self.child_scenarios = child_scenarios
        self.predicted_resources = predicted_resources
        self.functions = functions
        self.editor_scenario_data = editor_scenario_data
        self.comments = comments
        self.scavenger_hunt_objects = scavenger_hunt_objects
        self.object_names = object_names
        self.scenery = scenery
        self.scenery_palette = scenery_palette
        self.bipeds = bipeds
        self.biped_palette = biped_palette
        self.vehicles = vehicles
        self.vehicle_palette = vehicle_palette
        self.equipment = equipment
        self.equipment_palette = equipment_palette
        self.weapons = weapons
        self.weapon_palette = weapon_palette
        self.device_groups = device_groups
        self.device_machines = device_machines
        self.device_machine_palette = device_machine_palette
        self.device_controls = device_controls
        self.device_control_palette = device_control_palette
        self.device_light_fixtures = device_light_fixtures
        self.device_light_fixtures_palette = device_light_fixtures_palette
        self.sound_scenery = sound_scenery
        self.sound_scenery_palette = sound_scenery_palette
        self.player_starting_profiles = player_starting_profiles
        self.player_starting_locations = player_starting_locations
        self.trigger_volumes = trigger_volumes
        self.recorded_animations = recorded_animations
        self.netgame_flags = netgame_flags
        self.netgame_equipment = netgame_equipment
        self.starting_equipment = starting_equipment
        self.bsp_switch_trigger_volumes = bsp_switch_trigger_volumes
        self.decals = decals
        self.decal_palette = decal_palette
        self.detail_object_collection_palette  = detail_object_collection_palette
        self.actor_palette = actor_palette
        self.encounters = encounters
        self.command_lists = command_lists
        self.ai_animation_references = ai_animation_references
        self.ai_script_references = ai_script_references
        self.ai_recording_references = ai_recording_references
        self.ai_conversations = ai_conversations
        self.script_syntax_data = script_syntax_data
        self.script_string_data = script_string_data
        self.scripts = scripts
        self.script_globals = script_globals
        self.references = references
        self.source_files = source_files
        self.cutscene_flags = cutscene_flags
        self.cutscene_camera_points = cutscene_camera_points
        self.cutscene_titles = cutscene_titles
        self.structure_bsps = structure_bsps
        self.dont_use_tag_ref = dont_use_tag_ref
        self.wont_use_tag_ref = wont_use_tag_ref
        self.cant_use_tag_ref = cant_use_tag_ref
        self.skies_tag_block = skies_tag_block
        self.scenario_type = scenario_type
        self.scenario_flags = scenario_flags
        self.child_scenarios_tag_block = child_scenarios_tag_block
        self.local_north = local_north
        self.predicted_resources_tag_block = predicted_resources_tag_block
        self.functions_tag_block = functions_tag_block
        self.editor_scenario_data = editor_scenario_data
        self.comments_tag_block = comments_tag_block
        self.scavenger_hunt_objects_tag_block = scavenger_hunt_objects_tag_block
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
        self.actor_palette_tag_block = actor_palette_tag_block
        self.encounters_tag_block = encounters_tag_block
        self.command_lists_tag_block = command_lists_tag_block
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
        self.cutscene_flags_tag_block = cutscene_flags_tag_block
        self.cutscene_camera_points_tag_block = cutscene_camera_points_tag_block
        self.cutscene_titles_tag_block = cutscene_titles_tag_block
        self.custom_object_names_tag_ref = custom_object_names_tag_ref
        self.chapter_title_text_tag_ref = chapter_title_text_tag_ref
        self.hud_messages_tag_ref = hud_messages_tag_ref
        self.structure_bsps_tag_block = structure_bsps_tag_block

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
        def __init__(self, position=Vector(), data=None, text=""):
            self.position = position
            self.data = data
            self.text = text

    class ScanvengerHuntObject:
        def __init__(self, exported_name="", scenario_object_name_index=0):
            self.exported_name = exported_name
            self.scenario_object_name_index = scenario_object_name_index

    class ObjectName:
        def __init__(self, name="", object_type=0, placement_index=0):
            self.name = name
            self.object_type = object_type
            self.placement_index = placement_index

    class Object:
        def __init__(self, type_index=0, name_index=0, placement_flags=0, desired_permutation=0, position=Vector(), rotation=Euler(), appearance_player_index=0):
            self.type_index = type_index
            self.name_index = name_index
            self.placement_flags = placement_flags
            self.desired_permutation = desired_permutation
            self.position = position
            self.rotation = rotation
            self.appearance_player_index = appearance_player_index

    class Unit(Object):
        def __init__(self, body_vitality=0.0, flags=0):
            super().__init__()
            self.body_vitality = body_vitality
            self.flags = flags

    class Vehicle(Unit):
        def __init__(self, multiplayer_team_index=0, multiplayer_spawn_flags=0):
            super().__init__()
            self.multiplayer_team_index = multiplayer_team_index
            self.multiplayer_spawn_flags = multiplayer_spawn_flags

    class Equipment(Object):
        def __init__(self, misc_flags=0):
            super().__init__()
            self.misc_flags = misc_flags

    class Weapon(Object):
        def __init__(self, rounds_left=0, rounds_loaded=0, flags=0):
            super().__init__()
            self.rounds_left = rounds_left
            self.rounds_loaded = rounds_loaded
            self.flags = flags

    class DeviceGroup():
        def __init__(self, name="", initial_value=0.0, flags=0):
            self.name = name
            self.initial_value = initial_value
            self.flags = flags

    class DeviceMachine(Object):
        def __init__(self, power_group_index=0, position_group_index=0, flags_0=0, flags_1=0):
            super().__init__()
            self.power_group_index = power_group_index
            self.position_group_index = position_group_index
            self.flags_0 = flags_0
            self.flags_1 = flags_1

    class DeviceControl(Object):
        def __init__(self, power_group_index=0, position_group_index=0, flags_0=0, flags_1=0, unknown=0):
            super().__init__()
            self.power_group_index = power_group_index
            self.position_group_index = position_group_index
            self.flags_0 = flags_0
            self.flags_1 = flags_1
            self.unknown = unknown

    class DeviceLightFixture(Object):
        def __init__(self, power_group_index=0, position_group_index=0, flags=0, color_RGBA=(0.0, 0.0, 0.0, 1.0), intensity=0.0, falloff_angle=0.0, cutoff_angle=0.0):
            super().__init__()
            self.power_group_index = power_group_index
            self.position_group_index = position_group_index
            self.flags = flags
            self.color_RGBA = color_RGBA
            self.intensity = intensity
            self.falloff_angle = falloff_angle
            self.cutoff_angle = cutoff_angle

    class PlayerStartingProfile():
        def __init__(self, name="", starting_health_damage=0.0, starting_shield_damage=0.0, primary_weapon_tag_ref=None, primary_rounds_loaded=0, primary_rounds_total=0,
                     secondary_weapon_tag_ref=None, secondary_rounds_loaded=0, secondary_rounds_total=0, starting_fragmentation_grenades_count=0,
                     starting_plasma_grenade_count=0, starting_grenade_type2_count=0, starting_grenade_type3_count=0):
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
            self.starting_grenade_type2_count = starting_grenade_type2_count
            self.starting_grenade_type3_count = starting_grenade_type3_count

    class PlayerStartingLocation():
        def __init__(self, position=Vector(), facing=0.0, team_index=0, bsp_index=0, type_0=0, type_1=0, type_2=0, type_3=0):
            self.position = position
            self.facing = facing
            self.team_index = team_index
            self.bsp_index = bsp_index
            self.type_0 = type_0
            self.type_1 = type_1
            self.type_2 = type_2
            self.type_3 = type_3

    class TriggerVolume():
        def __init__(self, name="", parameter=Vector(), forward=Vector(), up=Vector(), position=Vector(), extents=Vector()):
            self.name = name
            self.parameter = parameter
            self.forward = forward
            self.up = up
            self.position = position
            self.extents = extents

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
        def __init__(self, position=Vector(), facing=0, type=0, usage_id=0, weapon_group=None):
            self.position = position
            self.facing = facing
            self.type = type
            self.usage_id = usage_id
            self.weapon_group = weapon_group

    class NetGameEquipment():
        def __init__(self, flags=0, type_0=0, type_1=0, type_2=0, type_3=0, team_index=0, spawn_time=0, position=Vector(), facing=0.0, item_collection=None):
            self.flags = flags
            self.type_0 = type_0
            self.type_1 = type_1
            self.type_2 = type_2
            self.type_3 = type_3
            self.team_index = team_index
            self.spawn_time = spawn_time
            self.position = position
            self.facing = facing
            self.item_collection = item_collection

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

    class Encounter():
        def __init__(self, name="", flags=0, team_index=0, search_behavior=0, manual_bsp_index=0, respawn_delay=(0.0, 0.0), squads_tag_block=None, platoons_tag_block= None,
                     firing_positions_tag_block=None, player_starting_locations_tag_block=None, squads=None, platoons= None, firing_positions=None, player_starting_locations=None):
            self.name = name
            self.flags = flags
            self.team_index = team_index
            self.search_behavior = search_behavior
            self.manual_bsp_index = manual_bsp_index
            self.respawn_delay = respawn_delay
            self.squads_tag_block = squads_tag_block
            self.platoons_tag_block = platoons_tag_block
            self.firing_positions_tag_block = firing_positions_tag_block
            self.player_starting_locations_tag_block = player_starting_locations_tag_block
            self.squads = squads
            self.platoons = platoons
            self.firing_positions = firing_positions
            self.player_starting_locations = player_starting_locations

    class Squad():
        def __init__(self, name="", actor_type=0, platoon=0, initial_state=0, return_state=0, flags=0, unique_leader_type=0, maneuver_to_squad=0, squad_delay_time=0.0, attacking=0,
                     attacking_search=0, attacking_guard=0, defending=0, defending_search=0, defending_guard=0, pursuing=0, normal_diff_count=0, insane_diff_count=0, major_upgrade=0,
                     respawn_min_actors=0, respawn_max_actors=0, respawn_total=0, respawn_delay=(0.0, 0.0), move_positions_tag_block=None, starting_locations_tag_block=None,
                     move_positions=None, starting_locations=None):
            self.name = name
            self.actor_type = actor_type
            self.platoon = platoon
            self.initial_state = initial_state
            self.return_state = return_state
            self.flags = flags
            self.unique_leader_type = unique_leader_type
            self.maneuver_to_squad = maneuver_to_squad
            self.squad_delay_time = squad_delay_time
            self.attacking = attacking
            self.attacking_search = attacking_search
            self.attacking_guard = attacking_guard
            self.defending = defending
            self.defending_search = defending_search
            self.defending_guard = defending_guard
            self.pursuing = pursuing
            self.normal_diff_count = normal_diff_count
            self.insane_diff_count = insane_diff_count
            self.major_upgrade = major_upgrade
            self.respawn_min_actors = respawn_min_actors
            self.respawn_max_actors = respawn_max_actors
            self.respawn_total = respawn_total
            self.respawn_delay = respawn_delay
            self.move_positions_tag_block = move_positions_tag_block
            self.starting_locations_tag_block = starting_locations_tag_block
            self.move_positions = move_positions
            self.starting_locations = starting_locations

    class MovePosition():
        def __init__(self, position=Vector(), facing=0.0, weight=0.0, time=(0.0, 0.0), animation=0, sequence_id=0, surface_index=0):
            self.position = position
            self.facing = facing
            self.weight = weight
            self.time = time
            self.animation = animation
            self.sequence_id = sequence_id
            self.surface_index = surface_index

    class StartingLocation():
        def __init__(self, position=Vector(), facing=0.0, sequence_id=0, flags=0, return_state=0, initial_state=0, actor_type=0, command_list=0):
            self.position = position
            self.facing = facing
            self.sequence_id = sequence_id
            self.flags = flags
            self.return_state = return_state
            self.initial_state = initial_state
            self.actor_type = actor_type
            self.command_list = command_list

    class Platoon():
        def __init__(self, name="", flags=0, change_attacking_defending_state=0, happens_to_a=0, maneuver_when=0, happens_to_b=0):
            self.name = name
            self.flags = flags
            self.change_attacking_defending_state = change_attacking_defending_state
            self.happens_to_a = happens_to_a
            self.maneuver_when = maneuver_when
            self.happens_to_b = happens_to_b

    class FiringPosition():
        def __init__(self, position=Vector(), group_index=0):
            self.position = position
            self.group_index = group_index

    class CommandList():
        def __init__(self, name="", flags=0, manual_bsp_index=0, command_tag_block=None, points_tag_block=None, commands=None, points=None):
            self.name = name
            self.flags = flags
            self.manual_bsp_index = manual_bsp_index
            self.command_tag_block = command_tag_block
            self.points_tag_block = points_tag_block
            self.commands = commands
            self.points = points

    class Command():
        def __init__(self, atom_type=0, atom_modifier=0, parameter1=0.0, parameter2=0.0, point_1=0, point_2=0, animation=0, script=0, recording=0, command=0, object_name=0):
            self.atom_type = atom_type
            self.atom_modifier = atom_modifier
            self.parameter1 = parameter1
            self.parameter2 = parameter2
            self.point_1 = point_1
            self.point_2 = point_2
            self.animation = animation
            self.script = script
            self.recording = recording
            self.command = command
            self.object_name = object_name

    class AIAnimationReference():
        def __init__(self, animation_name="", animation_reference=None):
            self.animation_name = animation_name
            self.animation_reference = animation_reference

    class AIConversation():
        def __init__(self, name="", flags=0, trigger_distance=0.0, run_to_player_distance=0.0, participants_tag_block=None, lines_tag_block=None, participants=None, lines=None):
            self.name = name
            self.flags = flags
            self.trigger_distance = trigger_distance
            self.run_to_player_distance = run_to_player_distance
            self.participants_tag_block = participants_tag_block
            self.lines_tag_block = lines_tag_block
            self.participants = participants
            self.lines = lines

    class Participant():
        def __init__(self, flags=0, selection_type=0, actor_type=0, use_this_object=0, set_new_name=0, encounter_name=""):
            self.flags = flags
            self.selection_type = selection_type
            self.actor_type = actor_type
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
        def __init__(self, name="", script_type=0, return_type=0, root_expression_index=0, parameters_tag_block=None, parameters=None):
            self.name = name
            self.script_type = script_type
            self.return_type = return_type
            self.root_expression_index = root_expression_index
            self.parameters_tag_block = parameters_tag_block
            self.parameters = parameters

    class Parameter():
        def __init__(self, name="", return_type=0):
            self.name = name
            self.return_type = return_type

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

    class CutsceneFlag():
        def __init__(self, name="", position=Vector(), facing=(0.0, 0.0)):
            self.name = name
            self.position = position
            self.facing = facing

    class CutsceneCameraPoint():
        def __init__(self, name="", position=Vector(), orientation=Euler(), field_of_view=0.0):
            self.name = name
            self.position = position
            self.orientation = orientation
            self.field_of_view = field_of_view

    class CutsceneTitle():
        def __init__(self, name="", name_length=0, text_bounds=(0, 0, 0, 0), string_index=0, style=0, justification=0, text_flags=0, text_color=(0.0, 0.0, 0.0, 1.0),
                     shadow_color=(0.0, 0.0, 0.0, 1.0), fade_in_time=0.0, up_time=0.0, fade_out_time=0.0):
            self.name = name
            self.name_length = name_length
            self.text_bounds = text_bounds
            self.string_index = string_index
            self.style = style
            self.justification = justification
            self.text_flags = text_flags
            self.text_color = text_color
            self.shadow_color = shadow_color
            self.fade_in_time = fade_in_time
            self.up_time = up_time
            self.fade_out_time = fade_out_time
