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

from mathutils import Vector
from ....global_functions import tag_format
from ....file_tag.h2.file_sky.format import SkyAsset

def generate_atmospheric_fog(H1_ASSET, TAG, SKY):
    fog = SKY.Fog()
    fog.color = H1_ASSET.sky_body.outdoor_fog_color
    fog.maximum_density = H1_ASSET.sky_body.outdoor_fog_maximum_density
    fog.start_distance = H1_ASSET.sky_body.outdoor_fog_start_distance
    fog.opaque_distance = H1_ASSET.sky_body.outdoor_fog_opaque_distance

    SKY.atmospheric_fog.append(fog)

    atmospheric_fog_count = len(SKY.atmospheric_fog)
    SKY.atmospheric_fog_header = TAG.TagBlockHeader("tbfd", 0, atmospheric_fog_count, 24)

    return TAG.TagBlock(atmospheric_fog_count)

def generate_lights(H1_ASSET, TAG, SKY):
    for light_element in H1_ASSET.lights:
        light = SKY.Light()
        light.direction_vector = Vector()
        light.direction = light_element.direction
        light.lens_flare = light_element.lens_flare

        light.fog = []
        fog_count = len(light.fog)
        light.fog_header = TAG.TagBlockHeader("tbfd", 0, fog_count, 44)
        light.fog_tag_block = TAG.TagBlock(fog_count)

        light.fog_opposite = []
        fog_opposite_count = len(light.fog_opposite)
        light.fog_opposite_header = TAG.TagBlockHeader("tbfd", 0, fog_opposite_count, 44)
        light.fog_opposite_tag_block = TAG.TagBlock(fog_opposite_count)

        light.radiosity = []
        radiosity = SKY.Radiosity()
        radiosity.flags = light_element.flags
        radiosity.color = light_element.color
        radiosity.power = light_element.power / 1000
        radiosity.test_distance = light_element.test_distance
        radiosity.diameter = light_element.diameter

        light.radiosity.append(radiosity)

        radiosity_count = len(light.radiosity)
        light.radiosity_header = TAG.TagBlockHeader("tbfd", 0, radiosity_count, 40)
        light.radiosity_tag_block = TAG.TagBlock(radiosity_count)

        SKY.lights.append(light)

    lights_count = len(SKY.lights)
    SKY.lights_header = TAG.TagBlockHeader("tbfd", 0, lights_count, 72)

    return TAG.TagBlock(lights_count)

def upgrade_sky(H1_ASSET, patch_txt_path, report):
    TAG = tag_format.TagAsset()
    SKY = SkyAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    SKY.header = TAG.Header()
    SKY.header.unk1 = 0
    SKY.header.flags = 0
    SKY.header.type = 0
    SKY.header.name = ""
    SKY.header.tag_group = "sky "
    SKY.header.checksum = 0
    SKY.header.data_offset = 64
    SKY.header.data_length = 0
    SKY.header.unk2 = 0
    SKY.header.version = 1
    SKY.header.destination = 0
    SKY.header.plugin_handle = -1
    SKY.header.engine_tag = "BLM!"

    SKY.cubemap = []
    SKY.atmospheric_fog = []
    SKY.secondary_fog = []
    SKY.sky_fog = []
    SKY.patchy_fog = []
    SKY.lights = []
    SKY.shader_functions = []
    SKY.animations = []

    SKY.sky_body_header = TAG.TagBlockHeader("tbfd", 0, 1, 220)
    SKY.sky_body = SKY.SkyBody()
    SKY.sky_body.render_model = H1_ASSET.sky_body.model
    SKY.sky_body.animation_graph = H1_ASSET.sky_body.animation_graph
    SKY.sky_body.flags = 0
    SKY.sky_body.render_model_scale = 1
    SKY.sky_body.movement_scale = -1
    SKY.sky_body.cubemap_tag_block = TAG.TagBlock()
    SKY.sky_body.indoor_ambient_color = H1_ASSET.sky_body.indoor_ambient_radiosity_color
    SKY.sky_body.outdoor_ambient_color = H1_ASSET.sky_body.outdoor_ambient_radiosity_color
    SKY.sky_body.fog_spread_distance = 0.0
    SKY.sky_body.atmospheric_fog_tag_block = generate_atmospheric_fog(H1_ASSET, TAG, SKY)
    SKY.sky_body.secondary_fog_tag_block = TAG.TagBlock()
    SKY.sky_body.sky_fog_tag_block = TAG.TagBlock()
    SKY.sky_body.patchy_fog_tag_block = TAG.TagBlock()
    SKY.sky_body.amount = 0.0
    SKY.sky_body.threshold = 0.0
    SKY.sky_body.brightness = 0.0
    SKY.sky_body.gamma_power = 0.0
    SKY.sky_body.lights_tag_block = generate_lights(H1_ASSET, TAG, SKY)
    SKY.sky_body.global_sky_rotation = 0.0
    SKY.sky_body.shader_functions_tag_block = TAG.TagBlock()
    SKY.sky_body.animations_tag_block = TAG.TagBlock()
    SKY.sky_body.clear_color = (0.0, 0.0, 0.0, 1.0)

    return SKY
