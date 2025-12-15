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
from ....file_tag.h2.file_sound_environment.format import SoundEnvironmentAsset

def upgrade_sound_environment(H2_ASSET, patch_txt_path, report):
    dump_dic = json.load(H2_ASSET)

    TAG = tag_format.TagAsset()
    SOUNDENV = SoundEnvironmentAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    SOUNDENV.header = TAG.Header()
    SOUNDENV.header.unk1 = 0
    SOUNDENV.header.flags = 0
    SOUNDENV.header.type = 0
    SOUNDENV.header.name = ""
    SOUNDENV.header.tag_group = "snde"
    SOUNDENV.header.checksum = 0
    SOUNDENV.header.data_offset = 64
    SOUNDENV.header.data_length = 0
    SOUNDENV.header.unk2 = 0
    SOUNDENV.header.version = 1
    SOUNDENV.header.destination = 0
    SOUNDENV.header.plugin_handle = -1
    SOUNDENV.header.engine_tag = "BLM!"

    SOUNDENV.body_header = TAG.TagBlockHeader("tbfd", 1, 1, 72)
    SOUNDENV.priority = dump_dic['Data']['Priority']
    SOUNDENV.room_intensity = dump_dic['Data']['Room Intensity']
    SOUNDENV.room_intensity_hf = dump_dic['Data']['Room Intensity Hf']
    SOUNDENV.room_rolloff = dump_dic['Data']['Room Rolloff (0 To 10)']
    SOUNDENV.decay_time = dump_dic['Data']['Decay Time (.1 To 20)']
    SOUNDENV.decay_hf_ratio = dump_dic['Data']['Decay Hf Ratio (.1 To 2)']
    SOUNDENV.reflections_intensity = dump_dic['Data']['Reflections Intensity']
    SOUNDENV.reflections_delay = dump_dic['Data']['Reflections Delay (0 To .3)']
    SOUNDENV.reverb_intensity = dump_dic['Data']['Reverb Intensity']
    SOUNDENV.reverb_delay = dump_dic['Data']['Reverb Delay (0 To .1)']
    SOUNDENV.diffusion = dump_dic['Data']['Diffusion']
    SOUNDENV.density = dump_dic['Data']['Density']
    SOUNDENV.hf_reference = dump_dic['Data']['Hf Reference(20 To 20,000)']
    SOUNDENV.reflection_type = ""
    SOUNDENV.reflection_type_length = 0

    return SOUNDENV
