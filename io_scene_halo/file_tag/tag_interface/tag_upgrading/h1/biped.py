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

class H1ObjectFlags(Flag):
    does_not_cast_shadow = auto()
    transparent_self_occlusion = auto()
    brighter_than_it_should_be = auto()
    not_a_pathfinding_obstacle = auto()
    extension_of_parent = auto()
    cast_shadow_by_default = auto()
    does_not_have_anniversary_geometry = auto()

class H2ObjectFlags(Flag):
    does_not_cast_shadow = auto()
    search_cardinal_direction_lightmaps_on_failure = auto()
    unused2 = auto()
    not_a_pathfinding_obstacle = auto()
    extension_of_parent = auto()
    does_not_cause_collision_damage = auto()
    early_mover = auto()
    early_mover_localized_physics = auto()
    use_static_massive_lightmap_sample = auto()
    object_scales_attachments = auto()
    inherits_players_appearance = auto()
    dead_bipeds_cant_localize = auto()
    attach_to_clusters_by_dynamic_sphere = auto()
    effects_created_by_this_object_do_not_spawn_objects_in_multiplayer = auto()
    prophet_is_not_displayed_in_pegasus_builds = auto()

def convert_object_flags(object_flags):
    flags = 0
    active_h1_flags = H1ObjectFlags(object_flags)
    if H1ObjectFlags.does_not_cast_shadow in active_h1_flags:
        flags += H2ObjectFlags.does_not_cast_shadow.value

    if H1ObjectFlags.not_a_pathfinding_obstacle in active_h1_flags:
        flags += H2ObjectFlags.not_a_pathfinding_obstacle.value

    if H1ObjectFlags.extension_of_parent in active_h1_flags:
        flags += H2ObjectFlags.extension_of_parent.value

    return flags


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
    ai_property_element = {
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
    ai_properties_block = [ai_property_element]


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

def upgrade_biped(h1_biped_asset, report):
    h2_biped_asset = {
        "Data": {
            "flags": convert_object_flags(h1_biped_asset["Data"]["flags"]),
            "bounding radius": h1_biped_asset["Data"]["bounding radius"],
            "bounding offset": h1_biped_asset["Data"]["bounding offset"],
            "acceleration scale": h1_biped_asset["Data"]["acceleration scale"],
            "model": {"group name": "hlmt", "path": ""},
            "ai properties": generate_ai_properties(h1_biped_asset),
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
