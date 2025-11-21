# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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

import os

from mathutils import Vector
from enum import Flag, Enum, auto

class H1BipedFlags(Flag):
    turns_without_animating = auto()
    passes_through_other_bipeds = auto()
    immune_for_falling_damage = auto()
    rotate_while_airborne = auto()
    uses_limp_body_physics = auto()
    unused_5 = auto()
    random_speed_increase = auto()
    unused_7 = auto()
    spawn_death_children_on_destroy = auto()
    stunned_by_emp_damage = auto()
    dead_physics_when_stunned = auto()
    always_ragdoll_when_dead = auto()

class H2BipedFlags(Flag):
    turns_without_animating = auto()
    passes_through_other_bipeds = auto()
    immune_for_falling_damage = auto()
    rotate_while_airborne = auto()
    uses_limp_body_physics = auto()
    unused_5 = auto()
    random_speed_increase = auto()
    unused_7 = auto()
    spawn_death_children_on_destroy = auto()
    stunned_by_emp_damage = auto()
    dead_physics_when_stunned = auto()
    always_ragdoll_when_dead = auto()

def generate_contact_points(dump_dic, TAG, ASSET):
    contact_points_tag_block = dump_dic['Data']['Contact Points']

    for contact_point_element in contact_points_tag_block:
        contact_point = ASSET.StringEntry()
        contact_point.name = contact_point_element['Marker Name']
        contact_point.name_length = len(contact_point.name)

        ASSET.contact_points.append(contact_point)

    contact_point_count = len(ASSET.contact_points)
    ASSET.contact_points_header = TAG.TagBlockHeader("tbfd", 0, contact_point_count, 4)

    return TAG.TagBlock(contact_point_count)

def generate_ai_properties(dump_dic, TAG, BIPED):
    tag_file_name = os.path.basename(dump_dic['TagName']).lower().replace(" ", "_")
    if "brute" in tag_file_name:
        ai_property = BIPED.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = ""
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.large.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        BIPED.ai_properties.append(ai_property)
    elif "elite" in tag_file_name:
        ai_property = BIPED.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = ""
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.large.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        BIPED.ai_properties.append(ai_property)
    elif "grunt" in tag_file_name:
        ai_property = BIPED.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = ""
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.medium.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        BIPED.ai_properties.append(ai_property)
    elif "jackal" in tag_file_name:
        ai_property = BIPED.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = ""
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.medium.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        BIPED.ai_properties.append(ai_property)
    elif "marine" in tag_file_name:
        ai_property = BIPED.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = ""
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.medium.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        BIPED.ai_properties.append(ai_property)
    elif "masterchief" in tag_file_name:
        ai_property = BIPED.AIProperty()
        ai_property.ai_flags = 0
        ai_property.ai_type_name = ""
        ai_property.ai_type_name_length = len(ai_property.ai_type_name)
        ai_property.ai_size = AISizeEnum.large.value
        ai_property.leap_jump_speed = LeapJumpSpeedEnum.none.value
        BIPED.ai_properties.append(ai_property)

    ai_property_count = len(BIPED.ai_properties)
    BIPED.ai_properties_header = TAG.TagBlockHeader("tbfd", 0, ai_property_count, 16)

    return TAG.TagBlock(ai_property_count)

def get_hand_defaults(dump_dic):
    right_hand_node = ""
    left_hand_node = ""
    preferred_gun_node = ""
    tag_file_name = os.path.basename(dump_dic['TagName']).lower().replace(" ", "_")
    if "brute" in tag_file_name:
        right_hand_node = "right_hand"
        left_hand_node = "left_hand"
        preferred_gun_node = "right_hand_brute"
    elif "elite" in tag_file_name:
        right_hand_node = "right_hand_elite"
        left_hand_node = "left_hand_elite"
    elif "grunt" in tag_file_name:
        right_hand_node = "right_hand"
        left_hand_node = "left_hand"
    elif "jackal" in tag_file_name:
        right_hand_node = "left_hand_jackal"
        left_hand_node = "left_hand"
        preferred_gun_node = "left_hand_jackal"
    elif "marine" in tag_file_name:
        right_hand_node = "right_hand"
        left_hand_node = "left_hand"
        preferred_gun_node = "left_hand_marine"
    elif "masterchief" in tag_file_name:
        right_hand_node = "right_hand"
        left_hand_node = "left_hand"
        preferred_gun_node = "right_hand_mc"

    return right_hand_node, left_hand_node, preferred_gun_node

def get_camera_defaults(dump_dic):
    camera_interpolation_start = 0.0
    camera_interpolation_end = 0.0
    camera_forward_movement_scale = 0.0
    camera_side_movement_scale = 0.0
    camera_vertical_movement_scale = 0.0
    camera_exclusion_distance = 0.0
    tag_file_name = os.path.basename(dump_dic['TagName']).lower().replace(" ", "_")
    if "masterchief" in tag_file_name:
        camera_interpolation_start = 15
        camera_interpolation_end = 90
        camera_forward_movement_scale = 0.75
        camera_side_movement_scale = 0.5
        camera_vertical_movement_scale = 0.5
        camera_exclusion_distance = 0.13

    return camera_interpolation_start, camera_interpolation_end, camera_forward_movement_scale, camera_side_movement_scale, camera_vertical_movement_scale, camera_exclusion_distance

def get_lock_on_defaults(dump_dic, TAG):
    lock_on_flags = 0
    lock_on_distance = 0.0
    head_shot_acceleration_scale = 0.0
    area_damage_effect = TAG.TagRef()
    collision_flags = 0
    mass = 0.0
    living_material_name = ""
    dead_material_name = ""
    tag_file_name = os.path.basename(dump_dic['TagName']).lower().replace(" ", "_")
    if "brute" in tag_file_name:
        area_damage_effect = TAG.TagRef("effe", r"effects\contact\collision\blood_aoe\blood_aoe_brute", len(r"effects\contact\collision\blood_aoe\blood_aoe_brute"))
        mass = 200
        living_material_name = "tough_organic_flesh_brute"
        dead_material_name = "tough_organic_flesh_brute"
    elif "elite" in tag_file_name:
        lock_on_flags = LockOnFlags.locked_by_plasma_targeting.value
        lock_on_distance = 15
        area_damage_effect = TAG.TagRef("effe", r"effects\contact\collision\blood_aoe\blood_aoe_elite", len(r"effects\contact\collision\blood_aoe\blood_aoe_elite"))
        mass = 125
        living_material_name = "hard_metal_thin_cov_elite"
        dead_material_name = "hard_metal_thin_cov_elite"
    elif "grunt" in tag_file_name:
        area_damage_effect = TAG.TagRef("effe", r"effects\contact\collision\blood_aoe\blood_aoe_grunt", len(r"effects\contact\collision\blood_aoe\blood_aoe_grunt"))
        mass = 90
        living_material_name = "soft_organic_flesh_grunt"
        dead_material_name = "soft_organic_flesh_grunt"
    elif "jackal" in tag_file_name:
        area_damage_effect = TAG.TagRef("effe", r"effects\contact\collision\blood_aoe\blood_aoe_jackal", len(r"effects\contact\collision\blood_aoe\blood_aoe_jackal"))
        mass = 75
        living_material_name = "soft_organic_flesh_jackal"
        dead_material_name = "soft_organic_flesh_jackal"
    elif "marine" in tag_file_name:
        area_damage_effect = TAG.TagRef("effe", r"effects\contact\collision\blood_aoe\blood_aoe_human", len(r"effects\contact\collision\blood_aoe\blood_aoe_human"))
        mass = 75
        living_material_name = "soft_organic_flesh_human"
        dead_material_name = "soft_organic_flesh_human"
    elif "masterchief" in tag_file_name:
        lock_on_flags = LockOnFlags.locked_by_plasma_targeting.value
        lock_on_distance = 15
        area_damage_effect = TAG.TagRef("effe", r"effects\contact\collision\blood_aoe\blood_aoe_human_masterchief", len(r"effects\contact\collision\blood_aoe\blood_aoe_human_masterchief"))
        collision_flags = CollisionFlags.uses_player_physics.value
        mass = 125
        living_material_name = "hard_metal_thin_hum_masterchief"
        dead_material_name = "hard_metal_thin_hum_masterchief"

    return lock_on_flags, lock_on_distance, head_shot_acceleration_scale, area_damage_effect, collision_flags, mass, living_material_name, dead_material_name

def upgrade_biped(dict_asset, report):

    pitch_range = dump_dic['Data']['Pitch Range']
    seat_acceleration_scale = dump_dic['Data']['Seat Acceleration Scale']
    spawned_actor_count = dump_dic['Data']['Spawned Actor Count']

    unit_type, unit_class = get_metagame_data(dump_dic)
    right_hand_node, left_hand_node, preferred_gun_node = get_hand_defaults(dump_dic)
    camera_interpolation_start, camera_interpolation_end, camera_forward_movement_scale, camera_side_movement_scale, camera_vertical_movement_scale, camera_exclusion_distance = get_camera_defaults(dump_dic)
    lock_on_flags, lock_on_distance, head_shot_acceleration_scale, area_damage_effect, collision_flags, mass, living_material_name, dead_material_name = get_lock_on_defaults(dump_dic, TAG)

    function_keywords = [("Object", _20030504_ObjectFunctionsEnum), ("Unit", _20030504_UnitFunctionsEnum), ("Biped", _20030504_BipedFunctionsEnum)]

    BIPED.body_header = TAG.TagBlockHeader("tbfd", 1, 1, 988)
    BIPED.object_flags = upgrade_e3_object_flags(dump_dic['Data']['Flags'])
    BIPED.bounding_radius = dump_dic['Data']['Bounding Radius']
    BIPED.bounding_offset = dump_dic['Data']['Bounding Offset']
    BIPED.acceleration_scale = dump_dic['Data']['Acceleration Scale']
    BIPED.lightmap_shadow_mode = 0
    BIPED.sweetner_size = 0
    BIPED.dynamic_light_sphere_radius = 0.0
    BIPED.dynamic_light_sphere_offset = Vector()
    BIPED.default_model_variant = dump_dic['Data']['Default Model Variant']
    BIPED.default_model_variant_length = len(dump_dic['Data']['Default Model Variant'])
    BIPED.model = TAG.TagRef().convert_from_json(dump_dic['Data']['Model'])
    BIPED.crate_object = TAG.TagRef()
    BIPED.modifier_shader = TAG.TagRef()
    BIPED.creation_effect = TAG.TagRef()
    BIPED.material_effects = TAG.TagRef()
    BIPED.ai_properties_tag_block = generate_ai_properties(dump_dic, TAG, BIPED)
    BIPED.functions_tag_block = TAG.TagBlock()
    BIPED.apply_collision_damage_scale = 0.0
    BIPED.min_game_acc = 0.0
    BIPED.max_game_acc = 0.0
    BIPED.min_game_scale = 0.0
    BIPED.max_game_scale = 0.0
    BIPED.min_abs_acc = 0.0
    BIPED.max_abs_acc = 0.0
    BIPED.min_abs_scale = 0.0
    BIPED.max_abs_scale = 0.0
    BIPED.hud_text_message_index = dump_dic['Data']['Hud Text Message Index']
    BIPED.attachments_tag_block = generate_attachments(dump_dic, TAG, BIPED, function_keywords)
    BIPED.widgets_tag_block = generate_widgets(dump_dic, TAG, BIPED)
    BIPED.old_functions_tag_block = TAG.TagBlock()
    BIPED.change_colors_tag_block = generate_change_colors(dump_dic, TAG, BIPED, function_keywords)
    BIPED.predicted_resources_tag_block = TAG.TagBlock()
    BIPED.unit_flags = dump_dic['Data']['Unit Flags']
    BIPED.default_team = dump_dic['Data']['Default Team']['Value']
    BIPED.constant_sound_volume = dump_dic['Data']['Constant Sound Volume']['Value']
    BIPED.integrated_light_toggle = TAG.TagRef().convert_from_json(dump_dic['Data']['Integrated Light Toggle'])
    BIPED.camera_field_of_view = dump_dic['Data']['Camera Field Of View']
    BIPED.camera_stiffness = dump_dic['Data']['Camera Stiffness']
    BIPED.camera_marker_name = dump_dic['Data']['Camera Marker Name']
    BIPED.camera_marker_name_length = len(BIPED.camera_marker_name)
    BIPED.camera_submerged_marker_name = dump_dic['Data']['Camera Submerged Marker Name']
    BIPED.camera_submerged_marker_name_length = len(BIPED.camera_submerged_marker_name)
    BIPED.pitch_auto_level = dump_dic['Data']['Pitch Auto-Level']
    BIPED.pitch_range = (pitch_range["Min"], pitch_range["Max"])
    BIPED.camera_tracks_tag_block = generate_camera_tracks(dump_dic, TAG, BIPED)
    BIPED.acceleration_range = Vector((seat_acceleration_scale[0], seat_acceleration_scale[1], seat_acceleration_scale[2])) * 30
    BIPED.acceleration_action_scale = 0.0
    BIPED.acceleration_attach_scale = 0.0
    BIPED.soft_ping_threshold = dump_dic['Data']['Soft Ping Threshold']
    BIPED.soft_ping_interrupt_time = dump_dic['Data']['Soft Ping Interrupt Time']
    BIPED.hard_ping_threshold = dump_dic['Data']['Hard Ping Threshold']
    BIPED.hard_ping_interrupt_time = dump_dic['Data']['Hard Ping Interrupt Time']
    BIPED.hard_death_threshold = dump_dic['Data']['Hard Death Threshold']
    BIPED.feign_death_threshold = dump_dic['Data']['Feign Death Threshold']
    BIPED.feign_death_time = dump_dic['Data']['Feign Death Time']
    BIPED.distance_of_evade_anim = dump_dic['Data']['Distance Of Evade Anim']
    BIPED.distance_of_dive_anim = dump_dic['Data']['Distance Of Dive Anim']
    BIPED.stunned_movement_threshold = dump_dic['Data']['Stunned Movement Threshold']
    BIPED.feign_death_chance = dump_dic['Data']['Feign Death Chance']
    BIPED.feign_repeat_chance = dump_dic['Data']['Feign Repeat Chance']
    BIPED.spawned_turret_actor = TAG.TagRef().convert_from_json(dump_dic['Data']['Spawned Actor'], "char")
    BIPED.spawned_actor_count = (spawned_actor_count["Min"], spawned_actor_count["Max"])
    BIPED.spawned_velocity = dump_dic['Data']['Spawned Velocity']
    BIPED.aiming_velocity_maximum = dump_dic['Data']['Aiming Velocity Maximum']
    BIPED.aiming_acceleration_maximum = dump_dic['Data']['Aiming Acceleration Maximum']
    BIPED.casual_aiming_modifier = dump_dic['Data']['Casual Aiming Modifier']
    BIPED.looking_velocity_maximum = dump_dic['Data']['Looking Velocity Maximum']
    BIPED.looking_acceleration_maximum = dump_dic['Data']['Looking Acceleration Maximum']
    BIPED.right_hand_node = right_hand_node
    BIPED.left_hand_node = left_hand_node
    BIPED.preferred_gun_node = preferred_gun_node
    BIPED.right_hand_node_length = len(BIPED.right_hand_node)
    BIPED.left_hand_node_length = len(BIPED.left_hand_node)
    BIPED.preferred_gun_node_length = len(BIPED.preferred_gun_node)
    BIPED.melee_damage = TAG.TagRef().convert_from_json(dump_dic['Data']['Melee Damage'])
    BIPED.boarding_melee_damage = TAG.TagRef()
    BIPED.boarding_melee_response = TAG.TagRef()
    BIPED.landing_melee_damage = TAG.TagRef()
    BIPED.flurry_melee_damage = TAG.TagRef()
    BIPED.obstacle_smash_damage = TAG.TagRef()
    BIPED.motion_sensor_blip_size = dump_dic['Data']['Motion Sensor Blip Size']['Value']
    BIPED.unit_type = unit_type
    BIPED.unit_class = unit_class
    BIPED.postures_tag_block = TAG.TagBlock()
    BIPED.new_hud_interfaces_tag_block = generate_new_hud_interface(dump_dic, TAG, BIPED)
    BIPED.dialogue_variants_tag_block = generate_dialogue_variants(dump_dic, TAG, BIPED)
    BIPED.grenade_velocity = dump_dic['Data']['Grenade Velocity']
    BIPED.grenade_type = dump_dic['Data']['Grenade Type']['Value']
    BIPED.grenade_count = dump_dic['Data']['Grenade Count']
    BIPED.powered_seats_tag_block = generate_powered_seats(dump_dic, TAG, BIPED)
    BIPED.weapons_tag_block = generate_weapons(dump_dic, TAG, BIPED)
    BIPED.seats_tag_block = generate_seats(dump_dic, TAG, BIPED)
    BIPED.boost_peak_power = 0.0
    BIPED.boost_rise_power = 0.0
    BIPED.boost_peak_time = 0.0
    BIPED.boost_fall_power = 0.0
    BIPED.dead_time = 0.0
    BIPED.attack_weight = 0.0
    BIPED.decay_weight = 0.0
    BIPED.moving_turning_speed = dump_dic['Data']['Moving Turning Speed']
    BIPED.biped_flags = dump_dic['Data']['Biped Flags']
    if not BipedFlags.uses_limp_body_physics in BipedFlags(BIPED.biped_flags):
        BIPED.biped_flags += BipedFlags.uses_limp_body_physics.value
    if BipedFlags.passes_through_other_bipeds in BipedFlags(BIPED.biped_flags):
        BIPED.biped_flags -= BipedFlags.passes_through_other_bipeds.value

    BIPED.stationary_turning_threshold = dump_dic['Data']['Stationary Turning Threshold']
    BIPED.jump_velocity = dump_dic['Data']['Jump Velocity'] * 30
    BIPED.maximum_soft_landing_time = dump_dic['Data']['Maximum Soft Landing Time']
    BIPED.maximum_hard_landing_time = dump_dic['Data']['Maximum Hard Landing Time']
    BIPED.minimum_soft_landing_velocity = dump_dic['Data']['Minimum Soft Landing Velocity']
    BIPED.minimum_hard_landing_velocity = dump_dic['Data']['Minimum Hard Landing Velocity']
    BIPED.maximum_hard_landing_velocity = dump_dic['Data']['Maximum Hard Landing Velocity']
    BIPED.death_hard_landing_velocity = dump_dic['Data']['Death Hard Landing Velocity']
    BIPED.stun_duration = 0.0
    BIPED.standing_camera_height = dump_dic['Data']['Standing Camera Height']
    BIPED.crouching_camera_height = dump_dic['Data']['Crouching Camera Height']
    BIPED.crouching_transition_time = dump_dic['Data']['Crouch Transition Time']
    BIPED.camera_interpolation_start = camera_interpolation_start
    BIPED.camera_interpolation_end = camera_interpolation_end
    BIPED.camera_forward_movement_scale = camera_forward_movement_scale
    BIPED.camera_side_movement_scale = camera_side_movement_scale
    BIPED.camera_vertical_movement_scale = camera_vertical_movement_scale
    BIPED.camera_exclusion_distance = camera_exclusion_distance
    BIPED.autoaim_width = dump_dic['Data']['Autoaim Width']
    BIPED.lock_on_flags = lock_on_flags
    BIPED.lock_on_distance = lock_on_distance
    BIPED.head_shot_acceleration_scale = head_shot_acceleration_scale
    BIPED.area_damage_effect = area_damage_effect
    BIPED.collision_flags = collision_flags
    BIPED.height_standing = dump_dic['Data']['Standing Camera Height']
    BIPED.height_crouching = dump_dic['Data']['Crouching Camera Height']
    BIPED.radius = dump_dic['Data']['Collision Radius']
    BIPED.mass = mass
    BIPED.living_material_name = living_material_name
    BIPED.dead_material_name = dead_material_name
    BIPED.living_material_name_length = len(BIPED.living_material_name)
    BIPED.dead_material_name_length = len(BIPED.dead_material_name)
    BIPED.dead_sphere_shapes_tag_block = TAG.TagBlock()
    BIPED.pill_shapes_tag_block = TAG.TagBlock()
    BIPED.sphere_shapes_tag_block = TAG.TagBlock()
    BIPED.maximum_slope_angle = dump_dic['Data']['Maximum Slope Angle']
    BIPED.downhill_falloff_angle = dump_dic['Data']['Downhill Falloff Angle']
    BIPED.downhill_cuttoff_angle = dump_dic['Data']['Downhill Cutoff Angle']
    BIPED.uphill_falloff_angle = dump_dic['Data']['Uphill Falloff Angle']
    BIPED.uphill_cuttoff_angle = dump_dic['Data']['Uphill Cutoff Angle']
    BIPED.downhill_velocity_scale = dump_dic['Data']['Downhill Velocity Scale']
    BIPED.uphill_velocity_scale = dump_dic['Data']['Uphill Velocity Scale']
    BIPED.bank_angle = dump_dic['Data']['Bank Angle']
    BIPED.bank_apply_time = dump_dic['Data']['Bank Apply Time']
    BIPED.bank_decay_time = dump_dic['Data']['Bank Decay Time']
    BIPED.pitch_ratio = dump_dic['Data']['Pitch Ratio']
    BIPED.max_velocity = dump_dic['Data']['Max Velocity']
    BIPED.max_sidestep_velocity = dump_dic['Data']['Max Sidestep Velocity']
    BIPED.acceleration = dump_dic['Data']['Acceleration']
    BIPED.deceleration = dump_dic['Data']['Deceleration']
    BIPED.angular_velocity_maximum = dump_dic['Data']['Angular Velocity Maximum']
    BIPED.angular_acceleration_maximum = dump_dic['Data']['Angular Acceleration Maximum']
    BIPED.crouch_velocity_modifier = dump_dic['Data']['Crouch Velocity Modifier']
    BIPED.contact_points_tag_block = generate_contact_points(dump_dic, TAG, BIPED)
    BIPED.reanimation_character = TAG.TagRef()
    BIPED.death_spawn_character = TAG.TagRef()
    BIPED.death_spawn_count = 0

    h2_biped_asset = {
        "Data": {
            "flags": dict_asset,
            "bounding radius": 0.0,
            "bounding offset": [
                0.0,
                0.0,
                0.0
            ],
            "acceleration scale": 0.0,
            "lightmap shadow mode": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "sweetener size": {
                "type": "CharEnum",
                "value": 0,
                "value name": ""
            },
            "dynamic light sphere radius": 0.0,
            "dynamic light sphere offset": [
                0.0,
                0.0,
                0.0
            ],
            "default model variant": "",
            "default model variant_pad": 0,
            "model": {
                "group name": "hlmt",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "crate object": {
                "group name": "bloc",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "modifier shader": {
                "group name": "shad",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "creation effect": {
                "group name": "effe",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "material effects": {
                "group name": "foot",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "TagBlock_ai properties": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_ai properties": {
                "name": "tbfd",
                "version": 0,
                "size": 16
            },
            "ai properties": [
                {
                    "ai flags": 0,
                    "ai type name": "",
                    "ai type name_pad": 0,
                    "ai size": {
                        "type": "ShortEnum",
                        "value": 0,
                        "value name": ""
                    },
                    "leap jump speed": {
                        "type": "ShortEnum",
                        "value": 0,
                        "value name": ""
                    }
                }
            ],
            "TagBlock_functions": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_functions": {
                "name": "tbfd",
                "version": 0,
                "size": 36
            },
            "functions": [
                {
                    "flags": 0,
                    "import name": "",
                    "import name_pad": 0,
                    "export name": "",
                    "export name_pad": 0,
                    "turn off with": "",
                    "turn off with_pad": 0,
                    "min value": 0.0,
                    "StructHeader_default function": {
                        "name": "MAPP",
                        "version": 1,
                        "size": 12
                    },
                    "TagBlock_data": {
                        "unk1": 0,
                        "unk2": 0
                    },
                    "TagBlockHeader_data": {
                        "name": "tbfd",
                        "version": 0,
                        "size": 1
                    },
                    "data": [
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": -128
                        },
                        {
                            "Value": 63
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        },
                        {
                            "Value": 0
                        }
                    ],
                    "scale by": "",
                    "scale by_pad": 0
                }
            ],
            "Apply collision damage scale": 0.0,
            "min game acc (default)": 0.0,
            "max game acc (default)": 0.0,
            "min game scale (default)": 0.0,
            "max game scale (default)": 0.0,
            "min abs acc (default)": 0.0,
            "max abs acc (default)": 0.0,
            "min abs scale (default)": 0.0,
            "max abs scale (default)": 0.0,
            "hud text message index": 0,
            "TagBlock_attachments": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_attachments": {
                "name": "tbfd",
                "version": 0,
                "size": 32
            },
            "attachments": [
                {
                    "type": {
                        "group name": null,
                        "unk1": 0,
                        "length": 0,
                        "unk2": -1,
                        "path": ""
                    },
                    "marker": "",
                    "marker_pad": 0,
                    "change color": {
                        "type": "ShortEnum",
                        "value": 0,
                        "value name": ""
                    },
                    "primary scale": "",
                    "primary scale_pad": 0,
                    "secondary scale": "",
                    "secondary scale_pad": 0
                }
            ],
            "TagBlock_widgets": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_widgets": {
                "name": "tbfd",
                "version": 0,
                "size": 16
            },
            "widgets": [
                {
                    "type": {
                        "group name": null,
                        "unk1": 0,
                        "length": 0,
                        "unk2": -1,
                        "path": ""
                    }
                }
            ],
            "TagBlock_old functions": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_old functions": {
                "name": "tbfd",
                "version": 0,
                "size": 0
            },
            "old functions": [],
            "TagBlock_change colors": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_change colors": {
                "name": "tbfd",
                "version": 0,
                "size": 24
            },
            "change colors": [
                {
                    "TagBlock_initial permutations": {
                        "unk1": 0,
                        "unk2": 0
                    },
                    "TagBlockHeader_initial permutations": {
                        "name": "tbfd",
                        "version": 0,
                        "size": 32
                    },
                    "initial permutations": [
                        {
                            "weight": 0.0,
                            "color lower bound": {
                                "R": 0.0,
                                "G": 0.0,
                                "B": 0.0
                            },
                            "color upper bound": {
                                "R": 0.0,
                                "G": 0.0,
                                "B": 0.0
                            },
                            "variant name": "",
                            "variant name_pad": 0
                        }
                    ],
                    "TagBlock_functions": {
                        "unk1": 0,
                        "unk2": 0
                    },
                    "TagBlockHeader_functions": {
                        "name": "tbfd",
                        "version": 0,
                        "size": 40
                    },
                    "functions": [
                        {
                            "scale flags": 0,
                            "color lower bound": {
                                "R": 0.0,
                                "G": 0.0,
                                "B": 0.0
                            },
                            "color upper bound": {
                                "R": 0.0,
                                "G": 0.0,
                                "B": 0.0
                            },
                            "darken by": "",
                            "darken by_pad": 0,
                            "scale by": "",
                            "scale by_pad": 0
                        }
                    ]
                }
            ],
            "TagBlock_predicted resources": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_predicted resources": {
                "name": "tbfd",
                "version": 0,
                "size": 0
            },
            "predicted resources": [],
            "flags_1": 0,
            "default team": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "constant sound volume": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "integrated light toggle": {
                "group name": "effe",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "camera field of view": 0.0,
            "camera stiffness": 0.0,
            "StructHeader_unit camera": {
                "name": "uncs",
                "version": 0,
                "size": 32
            },
            "camera marker name": "",
            "camera marker name_pad": 0,
            "camera submerged marker name": "",
            "camera submerged marker name_pad": 0,
            "pitch auto-level": 0.0,
            "pitch range": {
                "Min": 0.0,
                "Max": 0.0
            },
            "TagBlock_camera tracks": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_camera tracks": {
                "name": "tbfd",
                "version": 0,
                "size": 16
            },
            "camera tracks": [
                {
                    "track": {
                        "group name": "trak",
                        "unk1": 0,
                        "length": 0,
                        "unk2": -1,
                        "path": ""
                    }
                }
            ],
            "StructHeader_acceleration": {
                "name": "usas",
                "version": 0,
                "size": 20
            },
            "acceleration range": [
                0.0,
                0.0,
                0.0
            ],
            "accel action scale": 0.0,
            "accel attach scale": 0.0,
            "soft ping threshold": 0.0,
            "soft ping interrupt time": 0.0,
            "hard ping threshold": 0.0,
            "hard ping interrupt time": 0.0,
            "hard death threshold": 0.0,
            "feign death threshold": 0.0,
            "feign death time": 0.0,
            "distance of evade anim": 0.0,
            "distance of dive anim": 0.0,
            "stunned movement threshold": 0.0,
            "feign death chance": 0.0,
            "feign repeat chance": 0.0,
            "spawned turret character": {
                "group name": "char",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "spawned actor count": {
                "Min": 0,
                "Max": 0
            },
            "spawned velocity": 0.0,
            "aiming velocity maximum": 0.0,
            "aiming acceleration maximum": 0.0,
            "casual aiming modifier": 0.0,
            "looking velocity maximum": 0.0,
            "looking acceleration maximum": 0.0,
            "right_hand_node": "",
            "right_hand_node_pad": 0,
            "left_hand_node": "",
            "left_hand_node_pad": 0,
            "StructHeader_more damn nodes": {
                "name": "uHnd",
                "version": 1,
                "size": 4
            },
            "preferred_gun_node": "",
            "preferred_gun_node_pad": 0,
            "melee damage": {
                "group name": "jpt!",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "StructHeader_your momma": {
                "name": "ubms",
                "version": 1,
                "size": 80
            },
            "boarding melee damage": {
                "group name": "jpt!",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "boarding melee response": {
                "group name": "jpt!",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "landing melee damage": {
                "group name": "jpt!",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "flurry melee damage": {
                "group name": "jpt!",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "obstacle smash damage": {
                "group name": "jpt!",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "motion sensor blip size": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "StructHeader_campaign metagame bucket": {
                "name": "cmtb",
                "version": 0,
                "size": 2
            },
            "type": {
                "type": "CharEnum",
                "value": 0,
                "value name": ""
            },
            "class": {
                "type": "CharEnum",
                "value": 0,
                "value name": ""
            },
            "TagBlock_postures": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_postures": {
                "name": "tbfd",
                "version": 0,
                "size": 16
            },
            "postures": [
                {
                    "name": "",
                    "name_pad": 0,
                    "pill offset": [
                        0.0,
                        0.0,
                        0.0
                    ]
                }
            ],
            "TagBlock_NEW HUD INTERFACES": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_NEW HUD INTERFACES": {
                "name": "tbfd",
                "version": 0,
                "size": 16
            },
            "NEW HUD INTERFACES": [
                {
                    "new unit hud interface": {
                        "group name": "nhdt",
                        "unk1": 0,
                        "length": 0,
                        "unk2": -1,
                        "path": ""
                    }
                }
            ],
            "TagBlock_dialogue variants": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_dialogue variants": {
                "name": "tbfd",
                "version": 0,
                "size": 20
            },
            "dialogue variants": [
                {
                    "variant number": 0,
                    "dialogue": {
                        "group name": "udlg",
                        "unk1": 0,
                        "length": 0,
                        "unk2": -1,
                        "path": ""
                    }
                }
            ],
            "grenade velocity": 0.0,
            "grenade type": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "grenade count": 0,
            "TagBlock_powered seats": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_powered seats": {
                "name": "tbfd",
                "version": 0,
                "size": 8
            },
            "powered seats": [
                {
                    "driver powerup time": 0.0,
                    "driver powerdown time": 0.0
                }
            ],
            "TagBlock_weapons": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_weapons": {
                "name": "tbfd",
                "version": 0,
                "size": 16
            },
            "weapons": [
                {
                    "weapon": {
                        "group name": "weap",
                        "unk1": 0,
                        "length": 0,
                        "unk2": -1,
                        "path": ""
                    }
                }
            ],
            "TagBlock_seats": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_seats": {
                "name": "tbfd",
                "version": 3,
                "size": 192
            },
            "seats": [
                {
                    "flags": 0,
                    "label": "",
                    "label_pad": 0,
                    "marker name": "",
                    "marker name_pad": 0,
                    "entry marker(s) name": "",
                    "entry marker(s) name_pad": 0,
                    "boarding grenade marker": "",
                    "boarding grenade marker_pad": 0,
                    "boarding grenade string": "",
                    "boarding grenade string_pad": 0,
                    "boarding melee string": "",
                    "boarding melee string_pad": 0,
                    "ping scale": 0.0,
                    "turnover time": 0.0,
                    "StructHeader_acceleration": {
                        "name": "usas",
                        "version": 0,
                        "size": 20
                    },
                    "acceleration range": [
                        0.0,
                        0.0,
                        0.0
                    ],
                    "accel action scale": 0.0,
                    "accel attach scale": 0.0,
                    "AI scariness": 0.0,
                    "ai seat type": {
                        "type": "ShortEnum",
                        "value": 0,
                        "value name": ""
                    },
                    "boarding seat": -1,
                    "listener interpolation factor": 0.0,
                    "yaw rate bounds": {
                        "Min": 0.0,
                        "Max": 0.0
                    },
                    "pitch rate bounds": {
                        "Min": 0.0,
                        "Max": 0.0
                    },
                    "min speed reference": 0.0,
                    "max speed reference": 0.0,
                    "speed exponent": 0.0,
                    "StructHeader_unit camera": {
                        "name": "uncs",
                        "version": 0,
                        "size": 32
                    },
                    "camera marker name": "",
                    "camera marker name_pad": 0,
                    "camera submerged marker name": "",
                    "camera submerged marker name_pad": 0,
                    "pitch auto-level": 0.0,
                    "pitch range": {
                        "Min": 0.0,
                        "Max": 0.0
                    },
                    "TagBlock_camera tracks": {
                        "unk1": 0,
                        "unk2": 0
                    },
                    "TagBlockHeader_camera tracks": {
                        "name": "tbfd",
                        "version": 0,
                        "size": 16
                    },
                    "camera tracks": [
                        {
                            "track": {
                                "group name": "trak",
                                "unk1": 0,
                                "length": 0,
                                "unk2": -1,
                                "path": ""
                            }
                        }
                    ],
                    "TagBlock_unit hud interface": {
                        "unk1": 0,
                        "unk2": 0
                    },
                    "TagBlockHeader_unit hud interface": {
                        "name": "tbfd",
                        "version": 0,
                        "size": 16
                    },
                    "unit hud interface": [
                        {
                            "new unit hud interface": {
                                "group name": "nhdt",
                                "unk1": 0,
                                "length": 0,
                                "unk2": -1,
                                "path": ""
                            }
                        }
                    ],
                    "enter seat string": "",
                    "enter seat string_pad": 0,
                    "yaw minimum": 0.0,
                    "yaw maximum": 0.0,
                    "built-in gunner": {
                        "group name": "char",
                        "unk1": 0,
                        "length": 0,
                        "unk2": -1,
                        "path": ""
                    },
                    "entry radius": 0.0,
                    "entry marker cone angle": 0.0,
                    "entry marker facing angle": 0.0,
                    "maximum relative velocity": 0.0,
                    "invisible seat region": "",
                    "invisible seat region_pad": 0,
                    "runtime invisible seat region index": 0
                }
            ],
            "StructHeader_boost": {
                "name": "!@#$",
                "version": 0,
                "size": 20
            },
            "boost peak power": 0.0,
            "boost rise power": 0.0,
            "boost peak time": 0.0,
            "boost fall power": 0.0,
            "dead time": 0.0,
            "StructHeader_lipsync": {
                "name": "ulYc",
                "version": 1,
                "size": 8
            },
            "attack weight": 0.0,
            "decay weight": 0.0,
            "moving turning speed": 0.0,
            "flags_2": 0,
            "stationary turning threshold": 0.0,
            "jump velocity": 0.0,
            "maximum soft landing time": 0.0,
            "maximum hard landing time": 0.0,
            "minimum soft landing velocity": 0.0,
            "minimum hard landing velocity": 0.0,
            "maximum hard landing velocity": 0.0,
            "death hard landing velocity": 0.0,
            "stun duration": 0.0,
            "standing camera height": 0.0,
            "crouching camera height": 0.0,
            "crouch transition time": 0.0,
            "camera interpolation start": 0.0,
            "camera interpolation end": 0.0,
            "camera forward movement scale": 0.0,
            "camera side movement scale": 0.0,
            "camera vertical movement scale": 0.0,
            "camera exclusion distance": 0.0,
            "autoaim width": 0.0,
            "StructHeader_lock-on data": {
                "name": "blod",
                "version": 1,
                "size": 8
            },
            "flags_3": 0,
            "lock on distance": 0.0,
            "head shot acc scale": 0.0,
            "area damage effect": {
                "group name": "effe",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "StructHeader_physics": {
                "name": "chpy",
                "version": 0,
                "size": 160
            },
            "flags_4": 0,
            "height standing": 0.0,
            "height crouching": 0.0,
            "radius": 0.0,
            "mass": 0.0,
            "living material name": "",
            "living material name_pad": 0,
            "dead material name": "",
            "dead material name_pad": 0,
            "TagBlock_dead sphere shapes": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_dead sphere shapes": {
                "name": "tbfd",
                "version": 0,
                "size": 128
            },
            "dead sphere shapes": [
                {
                    "name": "",
                    "name_pad": 0,
                    "material": -1,
                    "flags": 0,
                    "relative mass scale": 0.0,
                    "friction": 0.0,
                    "restitution": 0.0,
                    "volume": 0.0,
                    "mass": 0.0,
                    "Skip": "AAA=",
                    "phantom": -1,
                    "Ptr": "AAAAAA==",
                    "size": 0,
                    "count": 0,
                    "Skip_1": "AAAAAA==",
                    "radius": 0.0,
                    "Ptr_1": "AAAAAA==",
                    "size_1": 0,
                    "count_1": 0,
                    "Skip_2": "AAAAAA==",
                    "Ptr_2": "AAAAAA==",
                    "rotation i": [
                        0.0,
                        0.0,
                        0.0
                    ],
                    "Skip_3": "AAAAAA==",
                    "rotation j": [
                        0.0,
                        0.0,
                        0.0
                    ],
                    "Skip_4": "AAAAAA==",
                    "rotation k": [
                        0.0,
                        0.0,
                        0.0
                    ],
                    "Skip_5": "AAAAAA==",
                    "translation": [
                        0.0,
                        0.0,
                        0.0
                    ],
                    "Skip_6": "AAAAAA=="
                }
            ],
            "TagBlock_pill shapes": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_pill shapes": {
                "name": "tbfd",
                "version": 0,
                "size": 80
            },
            "pill shapes": [
                {
                    "name": "",
                    "name_pad": 0,
                    "material": -1,
                    "flags": 0,
                    "relative mass scale": 0.0,
                    "friction": 0.0,
                    "restitution": 0.0,
                    "volume": 0.0,
                    "mass": 0.0,
                    "Skip": "AAA=",
                    "phantom": -1,
                    "Ptr": "AAAAAA==",
                    "size": 0,
                    "count": 0,
                    "Skip_1": "AAAAAA==",
                    "radius": 0.0,
                    "bottom": [
                        0.0,
                        0.0,
                        0.0
                    ],
                    "Skip_2": "AAAAAA==",
                    "top": [
                        0.0,
                        0.0,
                        0.0
                    ],
                    "Skip_3": "AAAAAA=="
                }
            ],
            "TagBlock_sphere shapes": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_sphere shapes": {
                "name": "tbfd",
                "version": 0,
                "size": 128
            },
            "sphere shapes": [
                {
                    "name": "",
                    "name_pad": 0,
                    "material": -1,
                    "flags": 0,
                    "relative mass scale": 0.0,
                    "friction": 0.0,
                    "restitution": 0.0,
                    "volume": 0.0,
                    "mass": 0.0,
                    "Skip": "AAA=",
                    "phantom": -1,
                    "Ptr": "AAAAAA==",
                    "size": 0,
                    "count": 0,
                    "Skip_1": "AAAAAA==",
                    "radius": 0.0,
                    "Ptr_1": "AAAAAA==",
                    "size_1": 0,
                    "count_1": 0,
                    "Skip_2": "AAAAAA==",
                    "Ptr_2": "AAAAAA==",
                    "rotation i": [
                        0.0,
                        0.0,
                        0.0
                    ],
                    "Skip_3": "AAAAAA==",
                    "rotation j": [
                        0.0,
                        0.0,
                        0.0
                    ],
                    "Skip_4": "AAAAAA==",
                    "rotation k": [
                        0.0,
                        0.0,
                        0.0
                    ],
                    "Skip_5": "AAAAAA==",
                    "translation": [
                        0.0,
                        0.0,
                        0.0
                    ],
                    "Skip_6": "AAAAAA=="
                }
            ],
            "StructHeader_ground physics": {
                "name": "chgr",
                "version": 0,
                "size": 48
            },
            "maximum slope angle": 0.0,
            "downhill falloff angle": 0.0,
            "downhill cutoff angle": 0.0,
            "uphill falloff angle": 0.0,
            "uphill cutoff angle": 0.0,
            "downhill velocity scale": 0.0,
            "uphill velocity scale": 0.0,
            "StructHeader_flying physics": {
                "name": "chfl",
                "version": 0,
                "size": 44
            },
            "bank angle": 0.0,
            "bank apply time": 0.0,
            "bank decay time": 0.0,
            "pitch ratio": 0.0,
            "max velocity": 0.0,
            "max sidestep velocity": 0.0,
            "acceleration": 0.0,
            "deceleration": 0.0,
            "angular velocity maximum": 0.0,
            "angular acceleration maximum": 0.0,
            "crouch velocity modifier": 0.0,
            "StructHeader_dead physics": {
                "name": "chdd",
                "version": 0,
                "size": 0
            },
            "StructHeader_sentinel physics": {
                "name": "chsn",
                "version": 0,
                "size": 0
            },
            "TagBlock_contact points": {
                "unk1": 0,
                "unk2": 0
            },
            "TagBlockHeader_contact points": {
                "name": "tbfd",
                "version": 0,
                "size": 4
            },
            "contact points": [
                {
                    "marker name": "",
                    "marker name_pad": 0
                }
            ],
            "reanimation character": {
                "group name": "char",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "death spawn character": {
                "group name": "char",
                "unk1": 0,
                "length": 0,
                "unk2": -1,
                "path": ""
            },
            "death spawn count": 0
        }
    }

    return BIPED
