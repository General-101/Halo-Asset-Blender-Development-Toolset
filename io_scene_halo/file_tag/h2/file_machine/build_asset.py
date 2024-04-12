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

def write_body(output_stream, TAG, MACHINE):
    MACHINE.machine_body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<H', 7))
    output_stream.write(struct.pack('<H', MACHINE.machine_body.object_flags))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.bounding_radius))
    output_stream.write(struct.pack('<fff', *MACHINE.machine_body.bounding_offset))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.acceleration_scale))
    output_stream.write(struct.pack('<h', MACHINE.machine_body.lightmap_shadow_mode))
    output_stream.write(struct.pack('<h', MACHINE.machine_body.sweetner_size))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.dynamic_light_sphere_radius))
    output_stream.write(struct.pack('<fff', *MACHINE.machine_body.dynamic_light_sphere_offset))
    output_stream.write(struct.pack('>I', len(MACHINE.machine_body.default_model_variant)))
    MACHINE.machine_body.model.write(output_stream, False, True)
    MACHINE.machine_body.crate_object.write(output_stream, False, True)
    MACHINE.machine_body.modifier_shader.write(output_stream, False, True)
    MACHINE.machine_body.creation_effect.write(output_stream, False, True)
    MACHINE.machine_body.material_effects.write(output_stream, False, True)
    MACHINE.machine_body.ai_properties_tag_block.write(output_stream, False)
    MACHINE.machine_body.functions_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', MACHINE.machine_body.apply_collision_damage_scale))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.min_game_acc))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.max_game_acc))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.min_game_scale))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.max_game_scale))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.min_abs_acc))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.max_abs_acc))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.min_abs_scale))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.max_abs_scale))
    output_stream.write(struct.pack('<H', MACHINE.machine_body.hud_text_message_index))
    output_stream.write(struct.pack('<2x'))
    MACHINE.machine_body.attachments_tag_block.write(output_stream, False)
    MACHINE.machine_body.widgets_tag_block.write(output_stream, False)
    MACHINE.machine_body.old_functions_tag_block.write(output_stream, False)
    MACHINE.machine_body.change_colors_tag_block.write(output_stream, False)
    MACHINE.machine_body.predicted_resources_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<I', MACHINE.machine_body.device_flags))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.power_transition_time))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.power_acceleration_time))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.position_transition_time))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.position_acceleration_time))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.depowered_position_transition_time))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.depowered_position_acceleration_time))
    output_stream.write(struct.pack('<H', MACHINE.machine_body.lightmap_flags))
    output_stream.write(struct.pack('<2x'))
    MACHINE.machine_body.open_up.write(output_stream, False, True)
    MACHINE.machine_body.close_down.write(output_stream, False, True)
    MACHINE.machine_body.opened.write(output_stream, False, True)
    MACHINE.machine_body.closed.write(output_stream, False, True)
    MACHINE.machine_body.depowered.write(output_stream, False, True)
    MACHINE.machine_body.repowered.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', MACHINE.machine_body.delay_time))
    MACHINE.machine_body.delay_effect.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', MACHINE.machine_body.automatic_activation_radius))
    output_stream.write(struct.pack('<H', MACHINE.machine_body.machine_type))
    output_stream.write(struct.pack('<H', MACHINE.machine_body.machine_flags))
    output_stream.write(struct.pack('<f', MACHINE.machine_body.door_open_time))
    output_stream.write(struct.pack('<ff', *MACHINE.machine_body.door_occlusion_time))
    output_stream.write(struct.pack('<H', MACHINE.machine_body.collision_response))
    output_stream.write(struct.pack('<h', MACHINE.machine_body.elevator_node))
    output_stream.write(struct.pack('<H', MACHINE.machine_body.pathfinding_policy))
    output_stream.write(struct.pack('<2x'))

def build_asset(output_stream, MACHINE, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    MACHINE.header.write(output_stream, False, True)
    write_body(output_stream, TAG, MACHINE)

    default_model_variant_name_length = len(MACHINE.machine_body.default_model_variant)
    if default_model_variant_name_length > 0:
        output_stream.write(struct.pack('<%ss' % default_model_variant_name_length, TAG.string_to_bytes(MACHINE.machine_body.default_model_variant, False)))

    model_name_length = len(MACHINE.machine_body.model.name)
    if model_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % model_name_length, TAG.string_to_bytes(MACHINE.machine_body.model.name, False)))

    crate_object_name_length = len(MACHINE.machine_body.crate_object.name)
    if crate_object_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % crate_object_name_length, TAG.string_to_bytes(MACHINE.machine_body.crate_object.name, False)))

    modifier_shader_name_length = len(MACHINE.machine_body.modifier_shader.name)
    if modifier_shader_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % modifier_shader_name_length, TAG.string_to_bytes(MACHINE.machine_body.modifier_shader.name, False)))

    creation_effect_name_length = len(MACHINE.machine_body.creation_effect.name)
    if creation_effect_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % creation_effect_name_length, TAG.string_to_bytes(MACHINE.machine_body.creation_effect.name, False)))

    material_effects_name_length = len(MACHINE.machine_body.material_effects.name)
    if material_effects_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % material_effects_name_length, TAG.string_to_bytes(MACHINE.machine_body.material_effects.name, False)))

    write_ai_properties(output_stream, TAG, MACHINE.ai_properties, MACHINE.ai_properties_header)
    write_functions(output_stream, TAG, MACHINE.functions, MACHINE.functions_header)
    write_attachments(output_stream, TAG, MACHINE.attachments, MACHINE.attachments_header)
    write_tag_ref(output_stream, TAG, MACHINE.widgets, MACHINE.widgets_header)
    write_old_functions(output_stream, TAG, MACHINE.old_functions, MACHINE.old_functions_header)
    write_change_colors(output_stream, TAG, MACHINE.change_colors, MACHINE.change_colors_header)
    write_predicted_resources(output_stream, TAG, MACHINE.predicted_resources, MACHINE.predicted_resources_header)

    open_up_length = len(MACHINE.machine_body.open_up.name)
    if open_up_length > 0:
        output_stream.write(struct.pack('<%ssx' % open_up_length, TAG.string_to_bytes(MACHINE.machine_body.open_up.name, False)))

    close_down_length = len(MACHINE.machine_body.close_down.name)
    if close_down_length > 0:
        output_stream.write(struct.pack('<%ssx' % close_down_length, TAG.string_to_bytes(MACHINE.machine_body.close_down.name, False)))

    opened_length = len(MACHINE.machine_body.opened.name)
    if opened_length > 0:
        output_stream.write(struct.pack('<%ssx' % opened_length, TAG.string_to_bytes(MACHINE.machine_body.opened.name, False)))

    closed_length = len(MACHINE.machine_body.closed.name)
    if closed_length > 0:
        output_stream.write(struct.pack('<%ssx' % closed_length, TAG.string_to_bytes(MACHINE.machine_body.closed.name, False)))

    depowered_length = len(MACHINE.machine_body.depowered.name)
    if depowered_length > 0:
        output_stream.write(struct.pack('<%ssx' % depowered_length, TAG.string_to_bytes(MACHINE.machine_body.depowered.name, False)))

    repowered_length = len(MACHINE.machine_body.repowered.name)
    if repowered_length > 0:
        output_stream.write(struct.pack('<%ssx' % repowered_length, TAG.string_to_bytes(MACHINE.machine_body.repowered.name, False)))

    delay_effect_length = len(MACHINE.machine_body.delay_effect.name)
    if delay_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % delay_effect_length, TAG.string_to_bytes(MACHINE.machine_body.delay_effect.name, False)))
