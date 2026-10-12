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

from enum import Flag, Enum, auto
from ....global_functions import tag_format, shader_processing
from ....file_tag.h2.file_particle.format import ParticleAsset, ParticleFlags, OutputModifierInputEnum, OutputModifierEnum
from ....file_tag.h2.file_shader.format import FunctionTypeEnum, OutputTypeFlags
from ...h2.file_bitmap.format import ImportTypeEnum

class _20030504_ParticleOldFlags(Flag):
    can_animate_backwards = auto()
    animation_stops_at_rest = auto()
    animation_starts_on_random_frame = auto()
    animate_once_per_frame = auto()
    dies_at_rest = auto()
    dies_on_contact_with_structure = auto()
    tint_from_diffuse_texture = auto()
    dies_on_contact_with_water = auto()
    dies_on_contact_with_air = auto()
    self_illuminated = auto()
    random_horizontal_mirroring = auto()
    random_vertical_mirroring = auto()

class _20030504_ShaderFlags(Flag):
    sort_bias = auto()
    nonlinear_tint = auto()
    dont_overdraw_fp_weapon = auto()

class _20030504_FramebufferBlendFunctionEnum(Enum):
    alpha_blend = 0
    multiply = auto()
    double_multiply = auto()
    add = auto()
    subtract = auto()
    component_min = auto()
    component_max = auto()
    alpha_multiply_add = auto()

def convert_particle_old_flags(particle_old_flags):
    flags = 0
    active_h1_flags = [flag.name for flag in _20030504_ParticleOldFlags if flag in _20030504_ParticleOldFlags(particle_old_flags)]
    if "can_animate_backwards" in active_h1_flags:
        flags += ParticleFlags.can_animate_backwards.value
    if "animation_starts_on_random_frame" in active_h1_flags:
        flags += ParticleFlags.select_random_sequence.value
    if "animate_once_per_frame" in active_h1_flags:
        flags += ParticleFlags.select_random_sequence.value
    if "dies_at_rest" in active_h1_flags:
        flags += ParticleFlags.dies_at_rest.value
    if "dies_on_contact_with_structure" in active_h1_flags:
        flags += ParticleFlags.dies_on_structure_collision.value
    if "tint_from_diffuse_texture" in active_h1_flags:
        flags += ParticleFlags.tint_from_diffuse_texture.value
    if "dies_on_contact_with_water" in active_h1_flags:
        flags += ParticleFlags.dies_in_media.value
    if "dies_on_contact_with_air" in active_h1_flags:
        flags += ParticleFlags.dies_in_air.value
    if "random_horizontal_mirroring" in active_h1_flags:
        flags += ParticleFlags.random_u_mirror.value
    if "random_vertical_mirroring" in active_h1_flags:
        flags += ParticleFlags.random_v_mirror.value

    return flags

def get_template(dump_dic):
    framebuffer_blend_function = _20030504_FramebufferBlendFunctionEnum(dump_dic['Data']['Framebuffer Blend Function']['Value']).name
    is_nonlinear_tint = _20030504_ShaderFlags.nonlinear_tint in _20030504_ShaderFlags(dump_dic['Data']['Shader Flags'])

    shader_template = shader_processing.convert_legacy_particle(framebuffer_blend_function, is_nonlinear_tint)

    return shader_template

def upgrade_particle_old(dump_dic, patch_txt_path, report, json_directory=None):
    TAG = tag_format.TagAsset()
    PARTICLE = ParticleAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    PARTICLE.header = TAG.Header()
    PARTICLE.header.unk1 = 0
    PARTICLE.header.flags = 0
    PARTICLE.header.type = 0
    PARTICLE.header.name = ""
    PARTICLE.header.tag_group = "prt3"
    PARTICLE.header.checksum = 0
    PARTICLE.header.data_offset = 64
    PARTICLE.header.data_length = 0
    PARTICLE.header.unk2 = 0
    PARTICLE.header.version = 1
    PARTICLE.header.destination = 0
    PARTICLE.header.plugin_handle = -1
    PARTICLE.header.engine_tag = "BLM!"

    PARTICLE.parameters = []
    PARTICLE.locations = []
    PARTICLE.attached_particle_systems = []
    PARTICLE.shader_postprocess_definitions = []

    template_enum = get_template(dump_dic)

    bitmap_tag = TAG.TagRef().convert_from_json(dump_dic['Data']["Bitmap"])
    bitm_dic = None
    if not json_directory == None:
        bitm_path = "%s[%s].json" % (os.path.join(json_directory, bitmap_tag.name), bitmap_tag.tag_group)
        if os.path.isfile(bitm_path):
            input_stream = open(bitm_path, 'r')
            bitm_dic = json.load(input_stream)
            input_stream.close()

    sprite_count = 1
    frame_index_function = FunctionTypeEnum.constant
    particle_flags = convert_particle_old_flags(dump_dic['Data']['Flags'])
    if bitm_dic:
        if ImportTypeEnum.sprites == ImportTypeEnum(bitm_dic['Data']["Type"]["Value"]):
            bitmap_vertical = True
            frame_index_function = FunctionTypeEnum.identity
            sprite_count = 0
            sequences_tag_block = bitm_dic['Data']['Sequences']
            for sequence_element in sequences_tag_block:
                sprites_tag_block = sequence_element['Sprites']
                for sprite_element in sprites_tag_block:
                    sprite_count += 1

            first_sequence_index = dump_dic['Data']["First Sequence Index"]
            for sequence_element in sequences_tag_block[first_sequence_index:(first_sequence_index+1)]:
                sprites_tag_block = sequence_element['Sprites']
                for sprite_element in sprites_tag_block[0:1]:
                    sprite_left = sprite_element['Left']
                    sprite_right = sprite_element['Right']
                    sprite_top = sprite_element['Top']
                    sprite_bottom = sprite_element['Bottom']
                    if (sprite_right - sprite_left) > (sprite_bottom - sprite_top):
                        bitmap_vertical = False

            if bitmap_vertical:
                particle_flags += ParticleFlags.bitmap_authored_vertically.value

    frame_index_input_function = OutputModifierInputEnum.particle_age.value
    if _20030504_ParticleOldFlags.animation_starts_on_random_frame in _20030504_ParticleOldFlags(dump_dic['Data']['Flags']):
        frame_index_input_function = OutputModifierInputEnum.particle_random_1.value

    PARTICLE.body_header = TAG.TagBlockHeader("tbfd", 0, 1, 248)
    PARTICLE.flags = particle_flags
    PARTICLE.particle_billboard_style = dump_dic['Data']['Orientation']['Value']
    PARTICLE.first_sequence_index = dump_dic['Data']["First Sequence Index"]
    PARTICLE.sequence_count = dump_dic['Data']["Initial Sequence Count"]
    PARTICLE.shader_template = TAG.TagRef("stem", template_enum.value, len(template_enum.value))

    parameter = shader_processing.add_parameter(PARTICLE, TAG, parameter_name="alpha_map_texture", bitmap_name=dump_dic['Data']["Bitmap"]["Path"], float_value=0.0)

    parameter.animation_properties = []
    animation_property_count = len(parameter.animation_properties)
    parameter.animation_properties_header = TAG.TagBlockHeader("tbfd", 0, animation_property_count, 28)
    parameter.animation_properties_tag_block = TAG.TagBlock(animation_property_count)

    PARTICLE.parameters.append(parameter)

    parameter_count = len(PARTICLE.parameters)
    PARTICLE.parameters_header = TAG.TagBlockHeader("tbfd", 0, parameter_count, 52)
    PARTICLE.parameters_tag_block = TAG.TagBlock(parameter_count)

    PARTICLE.properties = []
    shader_processing.convert_legacy_function(PARTICLE, TAG, PARTICLE.properties, function_type=FunctionTypeEnum.constant, flag_value=OutputTypeFlags._2_color.value, output_modifier=OutputModifierEnum.none.value, output_modifier_input=OutputModifierInputEnum.particle_age.value, input_type=OutputModifierInputEnum.particle_age.value, range_type=OutputModifierInputEnum.particle_random_1.value, function_header=TAG.TagBlockHeader("PRPC", 0, 1, 20))
    shader_processing.convert_legacy_function(PARTICLE, TAG, PARTICLE.properties, function_type=FunctionTypeEnum.constant, output_modifier=OutputModifierEnum.none.value, output_modifier_input=OutputModifierInputEnum.particle_age.value, value_0=1.0, value_1=1.0, input_type=OutputModifierInputEnum.particle_age.value, range_type=OutputModifierInputEnum.particle_random_1.value, function_header=TAG.TagBlockHeader("PRPS", 0, 1, 20))
    shader_processing.convert_legacy_function(PARTICLE, TAG, PARTICLE.properties, function_type=FunctionTypeEnum.constant, output_modifier=OutputModifierEnum.none.value, output_modifier_input=OutputModifierInputEnum.particle_age.value, value_0=1.0, value_1=1.0, input_type=OutputModifierInputEnum.particle_age.value, range_type=OutputModifierInputEnum.particle_random_1.value, function_header=TAG.TagBlockHeader("PRPS", 0, 1, 20))
    shader_processing.convert_legacy_function(PARTICLE, TAG, PARTICLE.properties, function_type=FunctionTypeEnum.constant, output_modifier=OutputModifierEnum.none.value, output_modifier_input=OutputModifierInputEnum.particle_age.value, value_0=1.0, value_1=0.0, input_type=OutputModifierInputEnum.particle_rotation.value, range_type=OutputModifierInputEnum.particle_random_1.value, function_header=TAG.TagBlockHeader("PRPS", 0, 1, 20))
    shader_processing.convert_legacy_function(PARTICLE, TAG, PARTICLE.properties, function_type=frame_index_function, output_modifier=OutputModifierEnum.none.value, output_modifier_input=OutputModifierInputEnum.particle_age.value, value_0=0.0, value_1=sprite_count, input_type=frame_index_input_function, range_type=OutputModifierInputEnum.particle_age.value, function_header=TAG.TagBlockHeader("PRPS", 0, 1, 20))

    PARTICLE.collision_effect = TAG.TagRef().convert_from_json(dump_dic['Data']["Collision Effect"])
    PARTICLE.death_effect = TAG.TagRef().convert_from_json(dump_dic['Data']["Death Effect"])
    PARTICLE.locations_tag_block = TAG.TagBlock()
    PARTICLE.attached_particle_systems_tag_block = TAG.TagBlock()
    PARTICLE.shader_postprocess_definitions_tag_block = TAG.TagBlock()

    return PARTICLE
