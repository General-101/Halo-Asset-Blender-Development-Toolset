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

class LensFlareAsset():
    def __init__(self, header=None, body_header=None, reflections_header=None, reflections=None, brightness_header=None, brightness=None, color_header=None, color=None, 
                 rotation_header=None, rotation=None, falloff_angle=0.0, cutoff_angle=0.0, occlusion_radius=0.05, occlusion_offset_direction=0, 
                 occlusion_inner_radius_scale=0, near_fade_distance=90.0, far_fade_distance=100.0, bitmap=None, occlusion_flags=0, rotation_function=None, 
                 rotation_function_scale=0.0, corona_scale=(1.0, 1.0), falloff_function=0, reflections_tag_block=None, flags=0, brightness_tag_block=None, 
                 color_tag_block=None, rotation_tag_block=None):
        self.header = header
        self.body_header = body_header
        self.reflections_header = reflections_header
        self.reflections = reflections
        self.brightness_header = brightness_header
        self.brightness = brightness
        self.color_header = color_header
        self.color = color
        self.rotation_header = rotation_header
        self.rotation = rotation
        self.falloff_angle = falloff_angle
        self.cutoff_angle = cutoff_angle
        self.occlusion_radius = occlusion_radius
        self.occlusion_offset_direction = occlusion_offset_direction
        self.occlusion_inner_radius_scale = occlusion_inner_radius_scale
        self.near_fade_distance = near_fade_distance
        self.far_fade_distance = far_fade_distance
        self.bitmap = bitmap
        self.occlusion_flags = occlusion_flags
        self.rotation_function = rotation_function
        self.rotation_function_scale = rotation_function_scale
        self.corona_scale = corona_scale
        self.falloff_function = falloff_function
        self.reflections_tag_block = reflections_tag_block
        self.flags = flags
        self.brightness_tag_block = brightness_tag_block
        self.color_tag_block = color_tag_block
        self.rotation_tag_block = rotation_tag_block

    class Reflection:
        def __init__(self, flags=0, bitmap_index=0, position=0.0, rotation_offset=0.0, radius=(0.0, 0.1), brightness=(0.0, 1.0), modulation_factor=0.0, color=(1.0, 1.0, 1.0, 1.0)):
            self.flags = flags
            self.bitmap_index = bitmap_index
            self.position = position
            self.rotation_offset = rotation_offset
            self.radius = radius
            self.brightness = brightness
            self.modulation_factor = modulation_factor
            self.color = color
