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

import json

from ....global_functions import tag_format, shader_processing
from ....file_tag.h2.file_contrail.format import ContrailAsset

def generate_point_states(dump_dic, TAG, CONTRAIL):
    point_states_tag_block = dump_dic['Data']['Point States']

    for point_state_element in point_states_tag_block:
        duration = point_state_element['Duration']
        transition_duration = point_state_element['Transition Duration']

        point_state = CONTRAIL.PointState()
        point_state.duration = (duration["Min"], duration["Max"])
        point_state.transition_duration = (transition_duration["Min"], transition_duration["Max"])
        point_state.physics = TAG.TagRef().convert_from_json(point_state_element['Physics'])
        point_state.width = point_state_element['Width']
        point_state.color_lower_bound = shader_processing.get_rgb_percentage(point_state_element["Color Lower Bound"])
        point_state.color_upper_bound = shader_processing.get_rgb_percentage(point_state_element["Color Upper Bound"])
        point_state.scale_flags = point_state_element['Scale Flags']

        CONTRAIL.point_states.append(point_state)

    point_state_count = len(CONTRAIL.point_states)
    CONTRAIL.point_states_header = TAG.TagBlockHeader("tbfd", 0, point_state_count, 72)

    return TAG.TagBlock(point_state_count)

def upgrade_contrail(H2_ASSET, patch_txt_path, report):
    dump_dic = json.load(H2_ASSET)

    TAG = tag_format.TagAsset()
    CONTRAIL = ContrailAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    CONTRAIL.header = TAG.Header()
    CONTRAIL.header.unk1 = 0
    CONTRAIL.header.flags = 0
    CONTRAIL.header.type = 0
    CONTRAIL.header.name = ""
    CONTRAIL.header.tag_group = "cont"
    CONTRAIL.header.checksum = 0
    CONTRAIL.header.data_offset = 64
    CONTRAIL.header.data_length = 0
    CONTRAIL.header.unk2 = 0
    CONTRAIL.header.version = 3
    CONTRAIL.header.destination = 0
    CONTRAIL.header.plugin_handle = -1
    CONTRAIL.header.engine_tag = "BLM!"

    CONTRAIL.point_states = []

    point_velocity = dump_dic['Data']['Point Velocity']

    CONTRAIL.body_header = TAG.TagBlockHeader("tbfd", 0, 1, 260)
    CONTRAIL.flags = dump_dic['Data']['Flags']
    CONTRAIL.scale_flags = dump_dic['Data']['Scale Flags']
    CONTRAIL.point_generation_rate = dump_dic['Data']['Point Generation Rate']
    CONTRAIL.point_velocity = (point_velocity["Min"], point_velocity["Max"])
    CONTRAIL.point_velocity_cone_angle = dump_dic['Data']['Point Velocity Cone Angle']
    CONTRAIL.inherited_velocity_fraction = dump_dic['Data']['Inherited Velocity Fraction']
    CONTRAIL.render_type = dump_dic['Data']['Render Type']['Value']
    CONTRAIL.texture_repeats_u = dump_dic['Data']['Texture Repeats U']
    CONTRAIL.texture_repeats_v = dump_dic['Data']['Texture Repeats V']
    CONTRAIL.texture_animation_u = dump_dic['Data']['Texture Animation U']
    CONTRAIL.texture_animation_v = dump_dic['Data']['Texture Animation V']
    CONTRAIL.animation_rate = dump_dic['Data']['Animation Rate']
    CONTRAIL.render_bitmap = TAG.TagRef().convert_from_json(dump_dic['Data']['Bitmap'])
    CONTRAIL.first_sequence_index = dump_dic['Data']['First Sequence Index']
    CONTRAIL.sequence_count = dump_dic['Data']['Sequence Count']
    CONTRAIL.shader_flags = dump_dic['Data']['Shader Flags']
    CONTRAIL.framebuffer_blend_function = dump_dic['Data']['Framebuffer Blend Function']['Value']
    CONTRAIL.framebuffer_fade_mode = dump_dic['Data']['Framebuffer Fade Mode']['Value']
    CONTRAIL.map_flags = dump_dic['Data']['Map Flags']
    CONTRAIL.secondary_bitmap = TAG.TagRef().convert_from_json(dump_dic['Data']['Secondary Bitmap'])
    CONTRAIL.anchor = dump_dic['Data']['Anchor']['Value']
    CONTRAIL.secondary_flags = dump_dic['Data']['Secondary Flags']
    CONTRAIL.u_animation_function = dump_dic['Data']['U-Animation Function']['Value']
    CONTRAIL.u_animation_period = dump_dic['Data']['U-Animation Period']
    CONTRAIL.u_animation_phase = dump_dic['Data']['U-Animation Phase']
    CONTRAIL.u_animation_scale = dump_dic['Data']['U-Animation Scale']
    CONTRAIL.v_animation_function = dump_dic['Data']['V-Animation Function']['Value']
    CONTRAIL.v_animation_period = dump_dic['Data']['V-Animation Period']
    CONTRAIL.v_animation_phase = dump_dic['Data']['V-Animation Phase']
    CONTRAIL.v_animation_scale = dump_dic['Data']['V-Animation Scale']
    CONTRAIL.rotation_animation_function = dump_dic['Data']['Rotation-Animation Function']['Value']
    CONTRAIL.rotation_animation_period = dump_dic['Data']['Rotation-Animation Period']
    CONTRAIL.rotation_animation_phase = dump_dic['Data']['Rotation-Animation Phase']
    CONTRAIL.rotation_animation_scale = dump_dic['Data']['Rotation-Animation Scale']
    CONTRAIL.rotation_animation_center = dump_dic['Data']['Rotation-Animation Center']
    CONTRAIL.zsprite_radius_scale = dump_dic['Data']['Zsprite Radius Scale']
    CONTRAIL.point_states_tag_block = generate_point_states(dump_dic, TAG, CONTRAIL)

    return CONTRAIL
