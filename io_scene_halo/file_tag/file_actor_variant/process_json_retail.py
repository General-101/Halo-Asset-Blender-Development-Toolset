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

import json

from .format_retail import (
        ActorVariantAsset,
        )

def process_json_retail(input_stream, tag_format, report):
    dump_dic = json.load(input_stream)

    TAG = tag_format.TagAsset()
    ACTORVARIANT = ActorVariantAsset()
    TAG.is_legacy = False

    ACTORVARIANT.header = TAG.Header()
    ACTORVARIANT.header.unk1 = 0
    ACTORVARIANT.header.flags = 0
    ACTORVARIANT.header.type = 0
    ACTORVARIANT.header.name = ""
    ACTORVARIANT.header.tag_group = "actv"
    ACTORVARIANT.header.checksum = 0
    ACTORVARIANT.header.data_offset = 64
    ACTORVARIANT.header.data_length = 0
    ACTORVARIANT.header.unk2 = 0
    ACTORVARIANT.header.version = 1
    ACTORVARIANT.header.destination = 0
    ACTORVARIANT.header.plugin_handle = -1
    ACTORVARIANT.header.engine_tag = "blam"

    ACTORVARIANT.actor_variant_body = ACTORVARIANT.ActorVariantBody()
    ACTORVARIANT.actor_variant_body.flags = dump_dic['Data']['Flags']
    actor_definition = dump_dic['Data']['Actor Definition']
    unit = dump_dic['Data']['Unit']
    major_variant = dump_dic['Data']['Major Variant']
    ACTORVARIANT.actor_variant_body.actor_definition = TAG.TagRef()
    ACTORVARIANT.actor_variant_body.unit = TAG.TagRef()
    ACTORVARIANT.actor_variant_body.major_variant = TAG.TagRef()
    if not actor_definition['GroupName'] == "NONE":
        ACTORVARIANT.actor_variant_body.actor_definition = TAG.TagRef(actor_definition['GroupName'], actor_definition['Path'], len(actor_definition['Path']))

    if not unit['GroupName'] == "NONE":
        ACTORVARIANT.actor_variant_body.unit = TAG.TagRef(unit['GroupName'], unit['Path'], len(unit['Path']))

    if not major_variant['GroupName'] == "NONE":
        ACTORVARIANT.actor_variant_body.major_variant = TAG.TagRef(major_variant['GroupName'], major_variant['Path'], len(major_variant['Path']))

    ACTORVARIANT.actor_variant_body.movement_type = dump_dic['Data']['Movement Type']['Value']
    ACTORVARIANT.actor_variant_body.initial_crouch_distance = dump_dic['Data']['Initial Crouch Chance']
    ACTORVARIANT.actor_variant_body.crouch_time = (dump_dic['Data']['Crouch Time']['Min'], dump_dic['Data']['Crouch Time']['Max'])
    ACTORVARIANT.actor_variant_body.run_time = (dump_dic['Data']['Run Time']['Min'], dump_dic['Data']['Run Time']['Max'])
    weapon = dump_dic['Data']['Weapon']
    ACTORVARIANT.actor_variant_body.weapon = TAG.TagRef()
    if not weapon['GroupName'] == "NONE":
        ACTORVARIANT.actor_variant_body.weapon = TAG.TagRef(weapon['GroupName'], weapon['Path'], len(weapon['Path']))

    ACTORVARIANT.actor_variant_body.maximum_firing_distance = dump_dic['Data']['Maximum Firing Distance']
    ACTORVARIANT.actor_variant_body.rate_of_Fire = dump_dic['Data']['Rate Of Fire']
    ACTORVARIANT.actor_variant_body.projectile_error = dump_dic['Data']['Projectile Error']
    ACTORVARIANT.actor_variant_body.first_burst_delay_time =  (dump_dic['Data']['First Burst Delay Time']['Min'], dump_dic['Data']['First Burst Delay Time']['Max'])
    ACTORVARIANT.actor_variant_body.new_target_firing_pattern_time = dump_dic['Data']['New-Target Firing Pattern Time']
    ACTORVARIANT.actor_variant_body.surprise_delay_time = dump_dic['Data']['Surprise Delay Time']

    return ACTORVARIANT
