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

import struct

from ....global_functions import tag_format, shader_processing
from ..file_object.build_asset import (
    write_ai_properties,
    write_functions,
    write_attachments,
    write_tag_ref,
    write_old_functions,
    write_change_colors,
    write_predicted_resources
    )
from ..file_item.build_asset import write_predicted_bitmaps

def write_body(output_stream, TAG, EQUIPMENT):
    EQUIPMENT.body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<H', 3))
    output_stream.write(struct.pack('<H', EQUIPMENT.object_flags))
    output_stream.write(struct.pack('<f', EQUIPMENT.bounding_radius))
    output_stream.write(struct.pack('<fff', *EQUIPMENT.bounding_offset))
    output_stream.write(struct.pack('<f', EQUIPMENT.acceleration_scale))
    output_stream.write(struct.pack('<h', EQUIPMENT.lightmap_shadow_mode))
    output_stream.write(struct.pack('<h', EQUIPMENT.sweetner_size))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<f', EQUIPMENT.dynamic_light_sphere_radius))
    output_stream.write(struct.pack('<fff', *EQUIPMENT.dynamic_light_sphere_offset))
    output_stream.write(struct.pack('>I', len(EQUIPMENT.default_model_variant)))
    EQUIPMENT.model.write(output_stream, False, True)
    EQUIPMENT.crate_object.write(output_stream, False, True)
    EQUIPMENT.modifier_shader.write(output_stream, False, True)
    EQUIPMENT.creation_effect.write(output_stream, False, True)
    EQUIPMENT.material_effects.write(output_stream, False, True)
    EQUIPMENT.ai_properties_tag_block.write(output_stream, False)
    EQUIPMENT.functions_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', EQUIPMENT.apply_collision_damage_scale))
    output_stream.write(struct.pack('<f', EQUIPMENT.min_game_acc))
    output_stream.write(struct.pack('<f', EQUIPMENT.max_game_acc))
    output_stream.write(struct.pack('<f', EQUIPMENT.min_game_scale))
    output_stream.write(struct.pack('<f', EQUIPMENT.max_game_scale))
    output_stream.write(struct.pack('<f', EQUIPMENT.min_abs_acc))
    output_stream.write(struct.pack('<f', EQUIPMENT.max_abs_acc))
    output_stream.write(struct.pack('<f', EQUIPMENT.min_abs_scale))
    output_stream.write(struct.pack('<f', EQUIPMENT.max_abs_scale))
    output_stream.write(struct.pack('<H', EQUIPMENT.hud_text_message_index))
    output_stream.write(struct.pack('<2x'))
    EQUIPMENT.attachments_tag_block.write(output_stream, False)
    EQUIPMENT.widgets_tag_block.write(output_stream, False)
    EQUIPMENT.old_functions_tag_block.write(output_stream, False)
    EQUIPMENT.change_colors_tag_block.write(output_stream, False)
    EQUIPMENT.predicted_resources_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<I', EQUIPMENT.item_flags))
    output_stream.write(struct.pack('<h', EQUIPMENT.old_message_index))
    output_stream.write(struct.pack('<h', EQUIPMENT.sort_order))
    output_stream.write(struct.pack('<f', EQUIPMENT.multiplayer_on_ground_scale))
    output_stream.write(struct.pack('<f', EQUIPMENT.campaign_on_ground_scale))
    output_stream.write(struct.pack('>I', len(EQUIPMENT.pickup_message)))
    output_stream.write(struct.pack('>I', len(EQUIPMENT.swap_message)))
    output_stream.write(struct.pack('>I', len(EQUIPMENT.pickup_or_dual_msg)))
    output_stream.write(struct.pack('>I', len(EQUIPMENT.swap_or_dual_msg)))
    output_stream.write(struct.pack('>I', len(EQUIPMENT.dual_only_msg)))
    output_stream.write(struct.pack('>I', len(EQUIPMENT.picked_up_msg)))
    output_stream.write(struct.pack('>I', len(EQUIPMENT.singluar_quantity_msg)))
    output_stream.write(struct.pack('>I', len(EQUIPMENT.plural_quantity_msg)))
    output_stream.write(struct.pack('>I', len(EQUIPMENT.switch_to_msg)))
    output_stream.write(struct.pack('>I', len(EQUIPMENT.switch_to_from_ai_msg)))
    EQUIPMENT.unused.write(output_stream, False, True)
    EQUIPMENT.collision_sound.write(output_stream, False, True)
    EQUIPMENT.predicted_bitmaps_tag_block.write(output_stream, False)
    EQUIPMENT.detonation_damage_effect.write(output_stream, False, True)
    output_stream.write(struct.pack('<ff', *EQUIPMENT.detonation_delay))
    EQUIPMENT.detonating_effect.write(output_stream, False, True)
    EQUIPMENT.detonation_effect.write(output_stream, False, True)
    output_stream.write(struct.pack('<H', EQUIPMENT.powerup_type))
    output_stream.write(struct.pack('<H', EQUIPMENT.grenade_type))
    output_stream.write(struct.pack('<f', EQUIPMENT.powerup_time))
    EQUIPMENT.pickup_sound.write(output_stream, False, True)

def build_asset(output_stream, EQUIPMENT, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    EQUIPMENT.header.write(output_stream, False, True)
    write_body(output_stream, TAG, EQUIPMENT)

    default_model_variant_name_length = len(EQUIPMENT.default_model_variant)
    if default_model_variant_name_length > 0:
        output_stream.write(struct.pack('<%ss' % default_model_variant_name_length, TAG.string_to_bytes(EQUIPMENT.default_model_variant, False)))

    model_name_length = len(EQUIPMENT.model.name)
    if model_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % model_name_length, TAG.string_to_bytes(EQUIPMENT.model.name, False)))

    crate_object_name_length = len(EQUIPMENT.crate_object.name)
    if crate_object_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % crate_object_name_length, TAG.string_to_bytes(EQUIPMENT.crate_object.name, False)))

    modifier_shader_name_length = len(EQUIPMENT.modifier_shader.name)
    if modifier_shader_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % modifier_shader_name_length, TAG.string_to_bytes(EQUIPMENT.modifier_shader.name, False)))

    creation_effect_name_length = len(EQUIPMENT.creation_effect.name)
    if creation_effect_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % creation_effect_name_length, TAG.string_to_bytes(EQUIPMENT.creation_effect.name, False)))

    material_effects_name_length = len(EQUIPMENT.material_effects.name)
    if material_effects_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % material_effects_name_length, TAG.string_to_bytes(EQUIPMENT.material_effects.name, False)))

    write_ai_properties(output_stream, TAG, EQUIPMENT.ai_properties, EQUIPMENT.ai_properties_header)
    write_functions(output_stream, TAG, EQUIPMENT.functions, EQUIPMENT.functions_header)
    write_attachments(output_stream, TAG, EQUIPMENT.attachments, EQUIPMENT.attachments_header)
    write_tag_ref(output_stream, TAG, EQUIPMENT.widgets, EQUIPMENT.widgets_header)
    write_old_functions(output_stream, TAG, EQUIPMENT.old_functions, EQUIPMENT.old_functions_header)
    write_change_colors(output_stream, TAG, EQUIPMENT.change_colors, EQUIPMENT.change_colors_header)
    write_predicted_resources(output_stream, TAG, EQUIPMENT.predicted_resources, EQUIPMENT.predicted_resources_header)

    pickup_message_length = len(EQUIPMENT.pickup_message)
    if pickup_message_length > 0:
        output_stream.write(struct.pack('<%ss' % pickup_message_length, TAG.string_to_bytes(EQUIPMENT.pickup_message, False)))

    swap_message_length = len(EQUIPMENT.swap_message)
    if swap_message_length > 0:
        output_stream.write(struct.pack('<%ss' % swap_message_length, TAG.string_to_bytes(EQUIPMENT.swap_message, False)))

    pickup_or_dual_msg_length = len(EQUIPMENT.pickup_or_dual_msg)
    if pickup_or_dual_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % pickup_or_dual_msg_length, TAG.string_to_bytes(EQUIPMENT.pickup_or_dual_msg, False)))

    swap_or_dual_msg_length = len(EQUIPMENT.swap_or_dual_msg)
    if swap_or_dual_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % swap_or_dual_msg_length, TAG.string_to_bytes(EQUIPMENT.swap_or_dual_msg, False)))

    dual_only_msg_length = len(EQUIPMENT.dual_only_msg)
    if dual_only_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % dual_only_msg_length, TAG.string_to_bytes(EQUIPMENT.dual_only_msg, False)))

    picked_up_msg_length = len(EQUIPMENT.picked_up_msg)
    if picked_up_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % picked_up_msg_length, TAG.string_to_bytes(EQUIPMENT.picked_up_msg, False)))

    singluar_quantity_msg_length = len(EQUIPMENT.singluar_quantity_msg)
    if singluar_quantity_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % singluar_quantity_msg_length, TAG.string_to_bytes(EQUIPMENT.singluar_quantity_msg, False)))

    plural_quantity_msg_length = len(EQUIPMENT.plural_quantity_msg)
    if plural_quantity_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % plural_quantity_msg_length, TAG.string_to_bytes(EQUIPMENT.plural_quantity_msg, False)))

    switch_to_msg_length = len(EQUIPMENT.switch_to_msg)
    if switch_to_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % switch_to_msg_length, TAG.string_to_bytes(EQUIPMENT.switch_to_msg, False)))

    switch_to_from_ai_msg_length = len(EQUIPMENT.switch_to_from_ai_msg)
    if switch_to_from_ai_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % switch_to_from_ai_msg_length, TAG.string_to_bytes(EQUIPMENT.switch_to_from_ai_msg, False)))

    unused_length = len(EQUIPMENT.unused.name)
    if unused_length > 0:
        output_stream.write(struct.pack('<%ssx' % unused_length, TAG.string_to_bytes(EQUIPMENT.unused.name, False)))

    collision_sound_length = len(EQUIPMENT.collision_sound.name)
    if collision_sound_length > 0:
        output_stream.write(struct.pack('<%ssx' % collision_sound_length, TAG.string_to_bytes(EQUIPMENT.collision_sound.name, False)))

    write_predicted_bitmaps(output_stream, TAG, EQUIPMENT.predicted_bitmaps, EQUIPMENT.predicted_bitmaps_header)

    detonation_damage_effect_length = len(EQUIPMENT.detonation_damage_effect.name)
    if detonation_damage_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonation_damage_effect_length, TAG.string_to_bytes(EQUIPMENT.detonation_damage_effect.name, False)))

    detonating_effect_length = len(EQUIPMENT.detonating_effect.name)
    if detonating_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonating_effect_length, TAG.string_to_bytes(EQUIPMENT.detonating_effect.name, False)))

    detonation_effect_length = len(EQUIPMENT.detonation_effect.name)
    if detonation_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonation_effect_length, TAG.string_to_bytes(EQUIPMENT.detonation_effect.name, False)))

    pickup_sound_length = len(EQUIPMENT.pickup_sound.name)
    if pickup_sound_length > 0:
        output_stream.write(struct.pack('<%ssx' % pickup_sound_length, TAG.string_to_bytes(EQUIPMENT.pickup_sound.name, False)))
