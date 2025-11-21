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
import json

from mathutils import Vector
from enum import Flag, Enum, auto
from ....global_functions import tag_format, shader_processing
from ....file_tag.h2_20030504.file_object.format import upgrade_e3_object_flags
from ....file_tag.h2.file_projectile.format import ProjectileAsset, ResponseEnum
from ....file_tag.h2_20030504.file_object.upgrade_json import generate_attachments, generate_widgets, generate_change_colors, _20030504_ObjectFunctionsEnum

class _20030504_ProjectileFunctionsEnum(Enum):
    none = 0
    range_remaining = auto()
    time_remaining = auto()
    tracer = auto()

class _20030504_ResponseEnum(Enum):
    disappear = 0
    detonate = auto()
    reflect = auto()
    overpenetrate = auto()
    attach = auto()

def convert_legacy_response(response_index):
    h2_response_index = 0
    h1_response = _20030504_ResponseEnum(response_index)
    if h1_response == _20030504_ResponseEnum.disappear:
        h2_response_index = ResponseEnum.fizzle.value
    elif h1_response == _20030504_ResponseEnum.detonate:
        h2_response_index = ResponseEnum.impact_detonate.value
    elif h1_response == _20030504_ResponseEnum.reflect:
        h2_response_index = ResponseEnum.bounce.value
    elif h1_response == _20030504_ResponseEnum.overpenetrate:
        h2_response_index = ResponseEnum.overpenetrate.value
    elif h1_response == _20030504_ResponseEnum.attach:
        h2_response_index = ResponseEnum.attach.value
    return h2_response_index

def generate_material_responses(dump_dic, TAG, PROJECTILE):
    material_responses_tag_block = dump_dic['Data']['Material Responses']

    for material_response_element in material_responses_tag_block:
        between = material_response_element['Between']
        and_bounds = material_response_element['And']

        material_response = PROJECTILE.MaterialResponse()
        material_response.flags = material_response_element["Flags"]
        material_response.result_response = convert_legacy_response(material_response_element["Default Response"]['Value'])
        material_response.result_effect = TAG.TagRef().convert_from_json(material_response_element['Default Effect'])
        material_response.material_name = ""
        material_response.material_name_length = len(material_response.material_name)
        material_response.potential_result_response = convert_legacy_response(material_response_element["Potential Response"]['Value'])
        material_response.potential_result_flags = material_response_element["Potential Flags"]
        material_response.chance_fraction = material_response_element["Skip Fraction"]
        material_response.between = (between["Min"], between["Max"])
        material_response.and_bounds = (and_bounds["Min"] * 30, and_bounds["Max"] * 30)
        material_response.potential_result_effect = TAG.TagRef().convert_from_json(material_response_element['Potential Effect'])
        material_response.scale_effects_by = material_response_element["Scale Effects By"]['Value']
        material_response.angular_noise = material_response_element["Angular Noise"]
        material_response.velocity_noise = material_response_element["Velocity Noise"]
        material_response.detonation_effect = TAG.TagRef().convert_from_json(material_response_element['Detonation Effect'])
        material_response.initial_friction = material_response_element["Initial Friction"]
        material_response.maximum_distance = material_response_element["Maximum Distance"]
        material_response.parallel_friction = material_response_element["Parallel Friction"]
        material_response.perpendicular_friction = material_response_element["Perpendicular Friction"]

        PROJECTILE.material_responses.append(material_response)

    material_response_count = len(PROJECTILE.material_responses)
    PROJECTILE.material_responses_header = TAG.TagBlockHeader("tbfd", 0, material_response_count, 112)

    return TAG.TagBlock(material_response_count)

def upgrade_projectile(H2_ASSET, patch_txt_path, report):
    dump_dic = json.load(H2_ASSET)

    TAG = tag_format.TagAsset()
    PROJECTILE = ProjectileAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    PROJECTILE.header = TAG.Header()
    PROJECTILE.header.unk1 = 0
    PROJECTILE.header.flags = 0
    PROJECTILE.header.type = 0
    PROJECTILE.header.name = ""
    PROJECTILE.header.tag_group = "proj"
    PROJECTILE.header.checksum = 0
    PROJECTILE.header.data_offset = 64
    PROJECTILE.header.data_length = 0
    PROJECTILE.header.unk2 = 0
    PROJECTILE.header.version = 5
    PROJECTILE.header.destination = 0
    PROJECTILE.header.plugin_handle = -1
    PROJECTILE.header.engine_tag = "BLM!"

    PROJECTILE.ai_properties = []
    PROJECTILE.functions = []
    PROJECTILE.attachments = []
    PROJECTILE.widgets = []
    PROJECTILE.old_functions = []
    PROJECTILE.change_colors = []
    PROJECTILE.predicted_resources = []
    PROJECTILE.material_responses = []

    timer = dump_dic['Data']['Timer']
    air_damage_range = dump_dic['Data']['Air Damage Range']
    water_damage_range = dump_dic['Data']['Water Damage Range']

    function_keywords = [("Object", _20030504_ObjectFunctionsEnum), ("Projectile", _20030504_ProjectileFunctionsEnum)]

    PROJECTILE.body_header = TAG.TagBlockHeader("tbfd", 1, 1, 604)
    PROJECTILE.object_flags = upgrade_e3_object_flags(dump_dic['Data']['Flags'])
    PROJECTILE.bounding_radius = dump_dic['Data']['Bounding Radius']
    PROJECTILE.bounding_offset = dump_dic['Data']['Bounding Offset']
    PROJECTILE.acceleration_scale = dump_dic['Data']['Acceleration Scale']
    PROJECTILE.lightmap_shadow_mode = 0
    PROJECTILE.sweetner_size = 0
    PROJECTILE.dynamic_light_sphere_radius = 0.0
    PROJECTILE.dynamic_light_sphere_offset = Vector()
    PROJECTILE.default_model_variant = dump_dic['Data']['Default Model Variant']
    PROJECTILE.default_model_variant_length = len(dump_dic['Data']['Default Model Variant'])
    PROJECTILE.model = TAG.TagRef().convert_from_json(dump_dic['Data']['Model'])
    PROJECTILE.crate_object = TAG.TagRef()
    PROJECTILE.modifier_shader = TAG.TagRef()
    PROJECTILE.creation_effect = TAG.TagRef()
    PROJECTILE.material_effects = TAG.TagRef()
    PROJECTILE.ai_properties_tag_block = TAG.TagBlock()
    PROJECTILE.functions_tag_block = TAG.TagBlock()
    PROJECTILE.apply_collision_damage_scale = 0.0
    PROJECTILE.min_game_acc = 0.0
    PROJECTILE.max_game_acc = 0.0
    PROJECTILE.min_game_scale = 0.0
    PROJECTILE.max_game_scale = 0.0
    PROJECTILE.min_abs_acc = 0.0
    PROJECTILE.max_abs_acc = 0.0
    PROJECTILE.min_abs_scale = 0.0
    PROJECTILE.max_abs_scale = 0.0
    PROJECTILE.hud_text_message_index = dump_dic['Data']['Hud Text Message Index']
    PROJECTILE.attachments_tag_block = generate_attachments(dump_dic, TAG, PROJECTILE, function_keywords)
    PROJECTILE.widgets_tag_block = generate_widgets(dump_dic, TAG, PROJECTILE)
    PROJECTILE.old_functions_tag_block = TAG.TagBlock()
    PROJECTILE.change_colors_tag_block = generate_change_colors(dump_dic, TAG, PROJECTILE, function_keywords)
    PROJECTILE.predicted_resources_tag_block = TAG.TagBlock()
    PROJECTILE.projectile_flags = dump_dic['Data']['Projectile Flags']
    PROJECTILE.detonation_timer_starts = dump_dic['Data']['Detonation Timer Starts']['Value']
    PROJECTILE.impact_noise = dump_dic['Data']['Impact Noise']['Value']
    PROJECTILE.ai_perception_radius = dump_dic['Data']['Ai Perception Radius']
    PROJECTILE.collision_radius = dump_dic['Data']['Collision Radius']
    PROJECTILE.arming_time = dump_dic['Data']['Arming Time']
    PROJECTILE.danger_radius = dump_dic['Data']['Danger Radius']
    PROJECTILE.timer = (timer["Min"], timer["Max"])
    PROJECTILE.minimum_velocity = dump_dic['Data']['Minimum Velocity'] * 30
    PROJECTILE.maximum_range = dump_dic['Data']['Maximum Range']
    PROJECTILE.detonation_noise = dump_dic['Data']['Detonation Noise']['Value']
    PROJECTILE.super_detonation_projectile_count = 0
    PROJECTILE.detonation_started = TAG.TagRef().convert_from_json(dump_dic['Data']['Detonation Started'])
    PROJECTILE.detonation_effect_airborne = TAG.TagRef().convert_from_json(dump_dic['Data']['Effect'])
    PROJECTILE.detonation_effect_ground = TAG.TagRef().convert_from_json(dump_dic['Data']['Effect'])
    PROJECTILE.detonation_damage = TAG.TagRef()
    PROJECTILE.attached_detonation_damage = TAG.TagRef().convert_from_json(dump_dic['Data']['Attached Detonation Damage'])
    PROJECTILE.super_detonation = TAG.TagRef().convert_from_json(dump_dic['Data']['Super Detonation'])
    PROJECTILE.super_detonation_damage = TAG.TagRef()
    PROJECTILE.detonation_sound = TAG.TagRef()
    PROJECTILE.damage_reporting_type = 0
    PROJECTILE.super_attached_detonation_damage_effect = TAG.TagRef()
    PROJECTILE.material_effect_radius = 0.0
    PROJECTILE.flyby_sound = TAG.TagRef().convert_from_json(dump_dic['Data']['Flyby Sound'])
    PROJECTILE.impact_effect = TAG.TagRef()
    PROJECTILE.impact_damage = TAG.TagRef().convert_from_json(dump_dic['Data']['Impact Damage'])
    PROJECTILE.boarding_detonation_time = 0.0
    PROJECTILE.boarding_detonation_damage_effect = TAG.TagRef()
    PROJECTILE.boarding_attached_detonation_damage_effect = TAG.TagRef()
    PROJECTILE.air_gravity_scale = dump_dic['Data']['Air Gravity Scale']
    PROJECTILE.air_damage_range = (air_damage_range["Min"], air_damage_range["Max"])
    PROJECTILE.water_gravity_scale = dump_dic['Data']['Water Gravity Scale']
    PROJECTILE.water_damage_range = (water_damage_range["Min"], water_damage_range["Max"])
    PROJECTILE.initial_velocity = dump_dic['Data']['Initial Velocity'] * 30
    PROJECTILE.final_velocity = dump_dic['Data']['Final Velocity'] * 30
    PROJECTILE.guided_angular_velocity_lower = dump_dic['Data']['Guided Angular Velocity']
    PROJECTILE.guided_angular_velocity_upper = dump_dic['Data']['Guided Angular Velocity']
    PROJECTILE.acceleration_range = (0.0, 0.0)
    PROJECTILE.targeted_leading_fraction = 0.0
    PROJECTILE.material_responses_tag_block = generate_material_responses(dump_dic, TAG, PROJECTILE)

    return PROJECTILE
