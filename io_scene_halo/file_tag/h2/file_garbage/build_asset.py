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

def write_body(output_stream, TAG, GARBAGE):
    GARBAGE.body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<H', 4))
    output_stream.write(struct.pack('<H', GARBAGE.object_flags))
    output_stream.write(struct.pack('<f', GARBAGE.bounding_radius))
    output_stream.write(struct.pack('<fff', *GARBAGE.bounding_offset))
    output_stream.write(struct.pack('<f', GARBAGE.acceleration_scale))
    output_stream.write(struct.pack('<h', GARBAGE.lightmap_shadow_mode))
    output_stream.write(struct.pack('<h', GARBAGE.sweetner_size))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<f', GARBAGE.dynamic_light_sphere_radius))
    output_stream.write(struct.pack('<fff', *GARBAGE.dynamic_light_sphere_offset))
    output_stream.write(struct.pack('>I', len(GARBAGE.default_model_variant)))
    GARBAGE.model.write(output_stream, False, True)
    GARBAGE.crate_object.write(output_stream, False, True)
    GARBAGE.modifier_shader.write(output_stream, False, True)
    GARBAGE.creation_effect.write(output_stream, False, True)
    GARBAGE.material_effects.write(output_stream, False, True)
    GARBAGE.ai_properties_tag_block.write(output_stream, False)
    GARBAGE.functions_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', GARBAGE.apply_collision_damage_scale))
    output_stream.write(struct.pack('<f', GARBAGE.min_game_acc))
    output_stream.write(struct.pack('<f', GARBAGE.max_game_acc))
    output_stream.write(struct.pack('<f', GARBAGE.min_game_scale))
    output_stream.write(struct.pack('<f', GARBAGE.max_game_scale))
    output_stream.write(struct.pack('<f', GARBAGE.min_abs_acc))
    output_stream.write(struct.pack('<f', GARBAGE.max_abs_acc))
    output_stream.write(struct.pack('<f', GARBAGE.min_abs_scale))
    output_stream.write(struct.pack('<f', GARBAGE.max_abs_scale))
    output_stream.write(struct.pack('<H', GARBAGE.hud_text_message_index))
    output_stream.write(struct.pack('<2x'))
    GARBAGE.attachments_tag_block.write(output_stream, False)
    GARBAGE.widgets_tag_block.write(output_stream, False)
    GARBAGE.old_functions_tag_block.write(output_stream, False)
    GARBAGE.change_colors_tag_block.write(output_stream, False)
    GARBAGE.predicted_resources_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<I', GARBAGE.item_flags))
    output_stream.write(struct.pack('<h', GARBAGE.old_message_index))
    output_stream.write(struct.pack('<h', GARBAGE.sort_order))
    output_stream.write(struct.pack('<f', GARBAGE.multiplayer_on_ground_scale))
    output_stream.write(struct.pack('<f', GARBAGE.campaign_on_ground_scale))
    output_stream.write(struct.pack('>I', len(GARBAGE.pickup_message)))
    output_stream.write(struct.pack('>I', len(GARBAGE.swap_message)))
    output_stream.write(struct.pack('>I', len(GARBAGE.pickup_or_dual_msg)))
    output_stream.write(struct.pack('>I', len(GARBAGE.swap_or_dual_msg)))
    output_stream.write(struct.pack('>I', len(GARBAGE.dual_only_msg)))
    output_stream.write(struct.pack('>I', len(GARBAGE.picked_up_msg)))
    output_stream.write(struct.pack('>I', len(GARBAGE.singluar_quantity_msg)))
    output_stream.write(struct.pack('>I', len(GARBAGE.plural_quantity_msg)))
    output_stream.write(struct.pack('>I', len(GARBAGE.switch_to_msg)))
    output_stream.write(struct.pack('>I', len(GARBAGE.switch_to_from_ai_msg)))
    GARBAGE.unused.write(output_stream, False, True)
    GARBAGE.collision_sound.write(output_stream, False, True)
    GARBAGE.predicted_bitmaps_tag_block.write(output_stream, False)
    GARBAGE.detonation_damage_effect.write(output_stream, False, True)
    output_stream.write(struct.pack('<ff', *GARBAGE.detonation_delay))
    GARBAGE.detonating_effect.write(output_stream, False, True)
    GARBAGE.detonation_effect.write(output_stream, False, True)
    output_stream.write(struct.pack('<168x'))

def build_asset(output_stream, GARBAGE, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    GARBAGE.header.write(output_stream, False, True)
    write_body(output_stream, TAG, GARBAGE)

    default_model_variant_name_length = len(GARBAGE.default_model_variant)
    if default_model_variant_name_length > 0:
        output_stream.write(struct.pack('<%ss' % default_model_variant_name_length, TAG.string_to_bytes(GARBAGE.default_model_variant, False)))

    model_name_length = len(GARBAGE.model.name)
    if model_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % model_name_length, TAG.string_to_bytes(GARBAGE.model.name, False)))

    crate_object_name_length = len(GARBAGE.crate_object.name)
    if crate_object_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % crate_object_name_length, TAG.string_to_bytes(GARBAGE.crate_object.name, False)))

    modifier_shader_name_length = len(GARBAGE.modifier_shader.name)
    if modifier_shader_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % modifier_shader_name_length, TAG.string_to_bytes(GARBAGE.modifier_shader.name, False)))

    creation_effect_name_length = len(GARBAGE.creation_effect.name)
    if creation_effect_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % creation_effect_name_length, TAG.string_to_bytes(GARBAGE.creation_effect.name, False)))

    material_effects_name_length = len(GARBAGE.material_effects.name)
    if material_effects_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % material_effects_name_length, TAG.string_to_bytes(GARBAGE.material_effects.name, False)))

    write_ai_properties(output_stream, TAG, GARBAGE.ai_properties, GARBAGE.ai_properties_header)
    write_functions(output_stream, TAG, GARBAGE.functions, GARBAGE.functions_header)
    write_attachments(output_stream, TAG, GARBAGE.attachments, GARBAGE.attachments_header)
    write_tag_ref(output_stream, TAG, GARBAGE.widgets, GARBAGE.widgets_header)
    write_old_functions(output_stream, TAG, GARBAGE.old_functions, GARBAGE.old_functions_header)
    write_change_colors(output_stream, TAG, GARBAGE.change_colors, GARBAGE.change_colors_header)
    write_predicted_resources(output_stream, TAG, GARBAGE.predicted_resources, GARBAGE.predicted_resources_header)

    pickup_message_length = len(GARBAGE.pickup_message)
    if pickup_message_length > 0:
        output_stream.write(struct.pack('<%ss' % pickup_message_length, TAG.string_to_bytes(GARBAGE.pickup_message, False)))

    swap_message_length = len(GARBAGE.swap_message)
    if swap_message_length > 0:
        output_stream.write(struct.pack('<%ss' % swap_message_length, TAG.string_to_bytes(GARBAGE.swap_message, False)))

    pickup_or_dual_msg_length = len(GARBAGE.pickup_or_dual_msg)
    if pickup_or_dual_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % pickup_or_dual_msg_length, TAG.string_to_bytes(GARBAGE.pickup_or_dual_msg, False)))

    swap_or_dual_msg_length = len(GARBAGE.swap_or_dual_msg)
    if swap_or_dual_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % swap_or_dual_msg_length, TAG.string_to_bytes(GARBAGE.swap_or_dual_msg, False)))

    dual_only_msg_length = len(GARBAGE.dual_only_msg)
    if dual_only_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % dual_only_msg_length, TAG.string_to_bytes(GARBAGE.dual_only_msg, False)))

    picked_up_msg_length = len(GARBAGE.picked_up_msg)
    if picked_up_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % picked_up_msg_length, TAG.string_to_bytes(GARBAGE.picked_up_msg, False)))

    singluar_quantity_msg_length = len(GARBAGE.singluar_quantity_msg)
    if singluar_quantity_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % singluar_quantity_msg_length, TAG.string_to_bytes(GARBAGE.singluar_quantity_msg, False)))

    plural_quantity_msg_length = len(GARBAGE.plural_quantity_msg)
    if plural_quantity_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % plural_quantity_msg_length, TAG.string_to_bytes(GARBAGE.plural_quantity_msg, False)))

    switch_to_msg_length = len(GARBAGE.switch_to_msg)
    if switch_to_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % switch_to_msg_length, TAG.string_to_bytes(GARBAGE.switch_to_msg, False)))

    switch_to_from_ai_msg_length = len(GARBAGE.switch_to_from_ai_msg)
    if switch_to_from_ai_msg_length > 0:
        output_stream.write(struct.pack('<%ss' % switch_to_from_ai_msg_length, TAG.string_to_bytes(GARBAGE.switch_to_from_ai_msg, False)))

    unused_length = len(GARBAGE.unused.name)
    if unused_length > 0:
        output_stream.write(struct.pack('<%ssx' % unused_length, TAG.string_to_bytes(GARBAGE.unused.name, False)))

    collision_sound_length = len(GARBAGE.collision_sound.name)
    if collision_sound_length > 0:
        output_stream.write(struct.pack('<%ssx' % collision_sound_length, TAG.string_to_bytes(GARBAGE.collision_sound.name, False)))

    write_predicted_bitmaps(output_stream, TAG, GARBAGE.predicted_bitmaps, GARBAGE.predicted_bitmaps_header)

    detonation_damage_effect_length = len(GARBAGE.detonation_damage_effect.name)
    if detonation_damage_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonation_damage_effect_length, TAG.string_to_bytes(GARBAGE.detonation_damage_effect.name, False)))

    detonating_effect_length = len(GARBAGE.detonating_effect.name)
    if detonating_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonating_effect_length, TAG.string_to_bytes(GARBAGE.detonating_effect.name, False)))

    detonation_effect_length = len(GARBAGE.detonation_effect.name)
    if detonation_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % detonation_effect_length, TAG.string_to_bytes(GARBAGE.detonation_effect.name, False)))
