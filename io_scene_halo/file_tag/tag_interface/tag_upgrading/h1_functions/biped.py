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

from enum import Flag, Enum, auto

from ..h1_functions.object import (
    convert_object_flags, 
    generate_ai_properties, 
    generate_attachments, 
    generate_widgets, 
    generate_change_colors, 
    FunctionEnum as ObjectFunctionsEnum
    )
from ..h1_functions.unit import (
    get_hand_defaults,
    generate_new_hud_interface,
    generate_dialogue_variants,
    generate_powered_seats,
    generate_weapons,
    generate_seats,
    FunctionEnum as UnitFunctionsEnum,
    get_metagame_data
    )

class BipedFunctionEnum(Enum):
    none = 0
    flying_velocity = auto()

class H1BipedFlags(Flag):
    turns_without_animating = auto()
    uses_player_physics = auto()
    flying = auto()
    physics_pill_centered_at_origin = auto()
    spherical = auto()
    passes_through_other_bipeds = auto()
    can_climb_any_surface = auto()
    immune_to_falling_damage = auto()
    rotate_while_airborne = auto()
    uses_limp_body_physics = auto()
    has_no_dying_airborne = auto()
    random_speed_increase = auto()
    unit_uses_old_ntsc_player_physics = auto()

class H2BipedFlags(Flag):
    turns_without_animating = auto()
    passes_through_other_bipeds = auto()
    immune_to_falling_damage = auto()
    rotate_while_airborne = auto()
    uses_limp_body_physics = auto()
    unused5 = auto()
    random_speed_increase = auto()
    unused7 = auto()
    spawn_death_children_on_destroy = auto()
    stunned_by_emp_damage = auto()
    dead_physics_when_stunned = auto()
    always_ragdoll_when_dead = auto()

class LockOnFlags(Flag):
    locked_by_human_targeting = auto()
    locked_by_plasma_targeting = auto()
    always_locked_by_plasma_targeting = auto()

class CollisionFlags(Flag):
    centered_at_origin = auto()
    shape_spherical = auto()
    uses_player_physics = auto()
    climb_any_surface = auto()
    flying = auto()
    not_physical = auto()
    dead_character_collision_group = auto()

def convert_biped_flags(object_flags):
    flags = 0
    active_h1_flags = H1BipedFlags(object_flags)
    if H1BipedFlags.turns_without_animating in active_h1_flags:
        flags += H2BipedFlags.turns_without_animating.value

    if H1BipedFlags.passes_through_other_bipeds in active_h1_flags:
        flags += H2BipedFlags.passes_through_other_bipeds.value

    if H1BipedFlags.immune_to_falling_damage in active_h1_flags:
        flags += H2BipedFlags.immune_to_falling_damage.value

    if H1BipedFlags.rotate_while_airborne in active_h1_flags:
        flags += H2BipedFlags.rotate_while_airborne.value

    if H1BipedFlags.uses_limp_body_physics in active_h1_flags:
        flags += H2BipedFlags.uses_limp_body_physics.value

    if H1BipedFlags.random_speed_increase in active_h1_flags:
        flags += H2BipedFlags.random_speed_increase.value

    return flags

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

def get_lock_on_defaults(dump_dic):
    lock_on_flags = 0
    lock_on_distance = 0.0
    head_shot_acceleration_scale = 0.0
    area_damage_effect = {"group name": "effe","path": ""}
    collision_flags = 0
    mass = 0.0
    living_material_name = ""
    dead_material_name = ""
    tag_file_name = os.path.basename(dump_dic["TagName"]).lower().replace(" ", "_")
    if "brute" in tag_file_name:
        area_damage_effect = {"group name": "effe","path": r"effects\contact\collision\blood_aoe\blood_aoe_brute"}
        mass = 200
        living_material_name = "tough_organic_flesh_brute"
        dead_material_name = "tough_organic_flesh_brute"
    elif "elite" in tag_file_name:
        lock_on_flags = LockOnFlags.locked_by_plasma_targeting.value
        lock_on_distance = 15
        area_damage_effect = {"group name": "effe","path": r"effects\contact\collision\blood_aoe\blood_aoe_elite"}
        mass = 125
        living_material_name = "hard_metal_thin_cov_elite"
        dead_material_name = "hard_metal_thin_cov_elite"
    elif "grunt" in tag_file_name:
        area_damage_effect = {"group name": "effe","path": r"effects\contact\collision\blood_aoe\blood_aoe_grunt"}
        mass = 90
        living_material_name = "soft_organic_flesh_grunt"
        dead_material_name = "soft_organic_flesh_grunt"
    elif "jackal" in tag_file_name:
        area_damage_effect = {"group name": "effe","path": r"effects\contact\collision\blood_aoe\blood_aoe_jackal"}
        mass = 75
        living_material_name = "soft_organic_flesh_jackal"
        dead_material_name = "soft_organic_flesh_jackal"
    elif "marine" in tag_file_name:
        area_damage_effect = {"group name": "effe","path": r"effects\contact\collision\blood_aoe\blood_aoe_human"}
        mass = 75
        living_material_name = "soft_organic_flesh_human"
        dead_material_name = "soft_organic_flesh_human"
    elif "masterchief" in tag_file_name:
        lock_on_flags = LockOnFlags.locked_by_plasma_targeting.value
        lock_on_distance = 15
        area_damage_effect = {"group name": "effe","path": r"effects\contact\collision\blood_aoe\blood_aoe_human_masterchief"}
        collision_flags = CollisionFlags.uses_player_physics.value
        mass = 125
        living_material_name = "hard_metal_thin_hum_masterchief"
        dead_material_name = "hard_metal_thin_hum_masterchief"

    return lock_on_flags, lock_on_distance, head_shot_acceleration_scale, area_damage_effect, collision_flags, mass, living_material_name, dead_material_name

def generate_contact_points(dump_dic):
    contact_points_block = []
    for contact_point_element in dump_dic["Data"]["contact point"]:
        contact_point_dict = {
            "marker name": contact_point_element["marker name"],
        }

        contact_points_block.append(contact_point_dict)

    return contact_points_block

def get_flood_defaults(dump_dic):
    reanimation_character = {"group name": "char", "path": ""}
    death_spawn_character = {"group name": "char", "path": dump_dic["Data"]["spawned actor"]["path"]}
    min_value, max_value = dump_dic["Data"]["spawned actor count"].values()
    death_spawn_count = (min_value + max_value) // 2
    tag_file_name = os.path.basename(dump_dic["TagName"]).lower().replace(" ", "_")
    if "floodcarrier" in tag_file_name:
        reanimation_character = {"group name": "char", "path": ""}
        death_spawn_character = {"group name": "char", "path": r"objects\characters\flood_infection\ai\flood_infection"}
        death_spawn_count = 5
    elif "floodcombat elite" in tag_file_name:
        reanimation_character = {"group name": "char", "path": r"objects\characters\floodcombat_elite\ai\floodcombat_elite"}
        death_spawn_character = {"group name": "char", "path": r"objects\characters\flood_infection\ai\flood_infection"}
        death_spawn_count = 1
    elif "floodcombat_human" in tag_file_name:
        reanimation_character = {"group name": "char", "path": r"objects\characters\floodcombat_human\ai\flood_combat_human"}
        death_spawn_character = {"group name": "char", "path": r""}
        death_spawn_count = 0

    return reanimation_character, death_spawn_character, death_spawn_count

def upgrade_biped(h1_biped_asset, EngineTag):
    h1_biped_data = h1_biped_asset["Data"]

    right_hand_node, left_hand_node, preferred_gun_node = get_hand_defaults(h1_biped_asset)
    unit_type, unit_class = get_metagame_data(h1_biped_asset)
    camera_interpolation_start, camera_interpolation_end, camera_forward_movement_scale, camera_side_movement_scale, camera_vertical_movement_scale, camera_exclusion_distance = get_camera_defaults(h1_biped_asset)
    lock_on_flags, lock_on_distance, head_shot_acceleration_scale, area_damage_effect, collision_flags, mass, living_material_name, dead_material_name = get_lock_on_defaults(h1_biped_asset)
    reanimation_character, death_spawn_character, death_spawn_count = get_flood_defaults(h1_biped_asset)

    function_keywords = [("Object", ObjectFunctionsEnum), ("Unit", UnitFunctionsEnum), ("Biped", BipedFunctionEnum)]
    i, j, k = h1_biped_data["seat acceleration scale"]

    h2_biped_asset = {
        "TagName": h1_biped_asset["TagName"],
        "Header": {
            "unk1": 0, 
            "flags": 0, 
            "tag type": 0, 
            "name": "", 
            "tag group": "bipd", 
            "checksum": 0, 
            "data offset": 64, 
            "data length": 0, 
            "unk2": 0, 
            "version": 3, 
            "destination": 0, 
            "plugin handle": -1, 
            "engine tag": EngineTag.H2Latest.value
        },
        "Data": {
            "flags": convert_object_flags(h1_biped_data["flags"]),
            "bounding radius": h1_biped_data["bounding radius"],
            "bounding offset": h1_biped_data["bounding offset"],
            "acceleration scale": h1_biped_data["acceleration scale"],
            "model": {"group name": "hlmt", "path": ""},
            "ai properties": generate_ai_properties(h1_biped_asset),
            "hud text message index": h1_biped_data["hud text message index"],
            "attachments": generate_attachments(h1_biped_asset, function_keywords),
            "widgets": generate_widgets(h1_biped_asset),
            "change colors": generate_change_colors(h1_biped_asset, function_keywords),
            "flags_1": h1_biped_data["flags_1"],
            "default team": {
                "type": "ShortEnum",
                "value": h1_biped_data["default team"]["value"],
                "value name": ""
            },
            "constant sound volume": {
                "type": "ShortEnum",
                "value": h1_biped_data["constant sound volume"]["value"],
                "value name": ""
            },
            "integrated light toggle": h1_biped_data["integrated light toggle"],
            "camera field of view": h1_biped_data["camera field of view"],
            "camera stiffness": h1_biped_data["camera stiffness"],
            "camera marker name": h1_biped_data["camera marker name"],
            "camera submerged marker name": h1_biped_data["camera submerged marker name"],
            "pitch auto-level": h1_biped_data["pitch auto level"],
            "pitch range": h1_biped_data["pitch range"],
            "camera tracks": h1_biped_data["camera tracks"],
            
            "acceleration range": [(i * 30), (j * 30), (k * 30)],
            "accel action scale": 0.0,
            "accel attach scale": 0.0,
            "soft ping threshold": h1_biped_data["soft ping threshold"],
            "soft ping interrupt time": h1_biped_data["soft ping interrupt time"],
            "hard ping threshold": h1_biped_data["hard ping threshold"],
            "hard ping interrupt time": h1_biped_data["hard ping interrupt time"],
            "hard death threshold": h1_biped_data["hard death threshold"],
            "feign death threshold": h1_biped_data["feign death threshold"],
            "feign death time": h1_biped_data["feign death time"],
            "distance of evade anim": h1_biped_data["distance of evade anim"],
            "distance of dive anim": h1_biped_data["distance of dive anim"],
            "stunned movement threshold": h1_biped_data["stunned movement threshold"],
            "feign death chance": h1_biped_data["feign death chance"],
            "feign repeat chance": h1_biped_data["feign repeat chance"],
            "spawned velocity": h1_biped_data["spawned velocity"],
            "aiming velocity maximum": h1_biped_data["aiming velocity maximum"],
            "aiming acceleration maximum": h1_biped_data["aiming acceleration maximum"],
            "casual aiming modifier": h1_biped_data["casual aiming modifier"],
            "looking velocity maximum": h1_biped_data["looking velocity maximum"],
            "looking acceleration maximum": h1_biped_data["looking acceleration maximum"],
            "right_hand_node": right_hand_node,
            "left_hand_node": left_hand_node,
            "preferred_gun_node": preferred_gun_node,
            "melee damage": h1_biped_data["melee damage"],
            "motion sensor blip size": {
                "type": "ShortEnum",
                "value": h1_biped_data["motion sensor blip size"]["value"],
                "value name": ""
            },
            "type": {
                "type": "CharEnum",
                "value": unit_type,
                "value name": ""
            },
            "class": {
                "type": "CharEnum",
                "value": unit_class,
                "value name": ""
            },
            "NEW HUD INTERFACES": generate_new_hud_interface(h1_biped_asset),
            "dialogue variants": generate_dialogue_variants(h1_biped_asset),
            "grenade velocity": h1_biped_data["grenade velocity"],
            "grenade type": {
                "type": "ShortEnum",
                "value": h1_biped_data["grenade type"]["value"],
                "value name": ""
            },
            "grenade count": h1_biped_data["grenade count"],
            "powered seats": generate_powered_seats(h1_biped_asset),
            "weapons": generate_weapons(h1_biped_asset),
            "seats": generate_seats(h1_biped_asset),
            "moving turning speed": h1_biped_data["moving turning speed"],
            "flags_2": convert_biped_flags(h1_biped_data["flags_2"]),
            "stationary turning threshold": h1_biped_data["stationary turning threshold"],
            "jump velocity": h1_biped_data["jump velocity"] * 30,
            "maximum soft landing time": h1_biped_data["maximum soft landing time"],
            "maximum hard landing time": h1_biped_data["maximum hard landing time"],
            "minimum soft landing velocity": h1_biped_data["minimum soft landing velocity"],
            "minimum hard landing velocity": h1_biped_data["minimum hard landing velocity"],
            "maximum hard landing velocity": h1_biped_data["maximum hard landing velocity"],
            "death hard landing velocity": h1_biped_data["death hard landing velocity"],
            "stun duration": 0.0,
            "standing camera height": h1_biped_data["standing camera height"],
            "crouching camera height": h1_biped_data["crouching camera height"],
            "crouch transition time": h1_biped_data["crouch transition time"],
            "camera interpolation start": camera_interpolation_start,
            "camera interpolation end": camera_interpolation_end,
            "camera forward movement scale": camera_forward_movement_scale,
            "camera side movement scale": camera_side_movement_scale,
            "camera vertical movement scale": camera_vertical_movement_scale,
            "camera exclusion distance": camera_exclusion_distance,
            "autoaim width": h1_biped_data["autoaim width"],
            "flags_3": lock_on_flags,
            "lock on distance": lock_on_distance,
            "head shot acc scale": head_shot_acceleration_scale,
            "area damage effect": area_damage_effect,
            "flags_4": collision_flags,
            "height standing": h1_biped_data["standing collision height"],
            "height crouching": h1_biped_data["crouching collision height"],
            "radius": h1_biped_data["collision radius"],
            "mass": mass,
            "living material name": living_material_name,
            "dead material name": dead_material_name,
            "maximum slope angle": h1_biped_data["maximum slope angle"],
            "downhill falloff angle": h1_biped_data["downhill falloff angle"],
            "downhill cutoff angle": h1_biped_data["downhill cutoff angle"],
            "uphill falloff angle": h1_biped_data["uphill falloff angle"],
            "uphill cutoff angle": h1_biped_data["uphill cutoff angle"],
            "downhill velocity scale": h1_biped_data["downhill velocity scale"],
            "uphill velocity scale": h1_biped_data["uphill velocity scale"],
            "bank angle": h1_biped_data["bank angle"],
            "bank apply time": h1_biped_data["bank apply time"],
            "bank decay time": h1_biped_data["bank decay time"],
            "pitch ratio": h1_biped_data["pitch ratio"],
            "max velocity": h1_biped_data["max velocity"],
            "max sidestep velocity": h1_biped_data["max sidestep velocity"],
            "acceleration": h1_biped_data["acceleration"],
            "deceleration": h1_biped_data["deceleration"],
            "angular velocity maximum": h1_biped_data["angular velocity maximum"],
            "angular acceleration maximum": h1_biped_data["angular acceleration maximum"],
            "crouch velocity modifier": h1_biped_data["crouch velocity modifier"],
            "contact points": generate_contact_points(h1_biped_asset),
            "reanimation character": reanimation_character,
            "death spawn character": death_spawn_character,
            "death spawn count": death_spawn_count
        }
    }

    return h2_biped_asset
