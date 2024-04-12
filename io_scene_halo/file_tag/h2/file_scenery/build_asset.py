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
from ....file_tag.h2.file_shader.format import FunctionTypeEnum
from ..file_object.build_asset import (
    write_ai_properties, 
    write_functions, 
    write_attachments, 
    write_tag_ref, 
    write_old_functions, 
    write_change_colors, 
    write_predicted_resources
    )

def write_body(output_stream, TAG, SCENERY):
    SCENERY.scenery_body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<H', 6))
    output_stream.write(struct.pack('<H', SCENERY.scenery_body.object_flags))
    output_stream.write(struct.pack('<f', SCENERY.scenery_body.bounding_radius))
    output_stream.write(struct.pack('<fff', *SCENERY.scenery_body.bounding_offset))
    output_stream.write(struct.pack('<f', SCENERY.scenery_body.acceleration_scale))
    output_stream.write(struct.pack('<h', SCENERY.scenery_body.lightmap_shadow_mode))
    output_stream.write(struct.pack('<h', SCENERY.scenery_body.sweetner_size))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<f', SCENERY.scenery_body.dynamic_light_sphere_radius))
    output_stream.write(struct.pack('<fff', *SCENERY.scenery_body.dynamic_light_sphere_offset))
    output_stream.write(struct.pack('>I', len(SCENERY.scenery_body.default_model_variant)))
    SCENERY.scenery_body.model.write(output_stream, False, True)
    SCENERY.scenery_body.crate_object.write(output_stream, False, True)
    SCENERY.scenery_body.modifier_shader.write(output_stream, False, True)
    SCENERY.scenery_body.creation_effect.write(output_stream, False, True)
    SCENERY.scenery_body.material_effects.write(output_stream, False, True)
    SCENERY.scenery_body.ai_properties_tag_block.write(output_stream, False)
    SCENERY.scenery_body.functions_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', SCENERY.scenery_body.apply_collision_damage_scale))
    output_stream.write(struct.pack('<f', SCENERY.scenery_body.min_game_acc))
    output_stream.write(struct.pack('<f', SCENERY.scenery_body.max_game_acc))
    output_stream.write(struct.pack('<f', SCENERY.scenery_body.min_game_scale))
    output_stream.write(struct.pack('<f', SCENERY.scenery_body.max_game_scale))
    output_stream.write(struct.pack('<f', SCENERY.scenery_body.min_abs_acc))
    output_stream.write(struct.pack('<f', SCENERY.scenery_body.max_abs_acc))
    output_stream.write(struct.pack('<f', SCENERY.scenery_body.min_abs_scale))
    output_stream.write(struct.pack('<f', SCENERY.scenery_body.max_abs_scale))
    output_stream.write(struct.pack('<H', SCENERY.scenery_body.hud_text_message_index))
    output_stream.write(struct.pack('<2x'))
    SCENERY.scenery_body.attachments_tag_block.write(output_stream, False)
    SCENERY.scenery_body.widgets_tag_block.write(output_stream, False)
    SCENERY.scenery_body.old_functions_tag_block.write(output_stream, False)
    SCENERY.scenery_body.change_colors_tag_block.write(output_stream, False)
    SCENERY.scenery_body.predicted_resources_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<H', SCENERY.scenery_body.pathfinding_policy))
    output_stream.write(struct.pack('<H', SCENERY.scenery_body.scenery_flags))
    output_stream.write(struct.pack('<H', SCENERY.scenery_body.lightmapping_policy))
    output_stream.write(struct.pack('<2x'))

def build_asset(output_stream, SCENERY, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    SCENERY.header.write(output_stream, False, True)
    write_body(output_stream, TAG, SCENERY)

    default_model_variant_name_length = len(SCENERY.scenery_body.default_model_variant)
    if default_model_variant_name_length > 0:
        output_stream.write(struct.pack('<%ss' % default_model_variant_name_length, TAG.string_to_bytes(SCENERY.scenery_body.default_model_variant, False)))

    model_name_length = len(SCENERY.scenery_body.model.name)
    if model_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % model_name_length, TAG.string_to_bytes(SCENERY.scenery_body.model.name, False)))

    crate_object_name_length = len(SCENERY.scenery_body.crate_object.name)
    if crate_object_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % crate_object_name_length, TAG.string_to_bytes(SCENERY.scenery_body.crate_object.name, False)))

    modifier_shader_name_length = len(SCENERY.scenery_body.modifier_shader.name)
    if modifier_shader_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % modifier_shader_name_length, TAG.string_to_bytes(SCENERY.scenery_body.modifier_shader.name, False)))

    creation_effect_name_length = len(SCENERY.scenery_body.creation_effect.name)
    if creation_effect_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % creation_effect_name_length, TAG.string_to_bytes(SCENERY.scenery_body.creation_effect.name, False)))

    material_effects_name_length = len(SCENERY.scenery_body.material_effects.name)
    if material_effects_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % material_effects_name_length, TAG.string_to_bytes(SCENERY.scenery_body.material_effects.name, False)))

    write_ai_properties(output_stream, TAG, SCENERY.ai_properties, SCENERY.ai_properties_header)
    write_functions(output_stream, TAG, SCENERY.functions, SCENERY.functions_header)
    write_attachments(output_stream, TAG, SCENERY.attachments, SCENERY.attachments_header)
    write_tag_ref(output_stream, TAG, SCENERY.widgets, SCENERY.widgets_header)
    write_old_functions(output_stream, TAG, SCENERY.old_functions, SCENERY.old_functions_header)
    write_change_colors(output_stream, TAG, SCENERY.change_colors, SCENERY.change_colors_header)
    write_predicted_resources(output_stream, TAG, SCENERY.predicted_resources, SCENERY.predicted_resources_header)

