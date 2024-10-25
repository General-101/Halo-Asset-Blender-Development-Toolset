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

from enum import Flag, auto

class LightFlags(Flag):
    affects_exteriors = auto()
    affects_interiors = auto()

class SkyAsset():
    def __init__(self, header=None, shader_functions=None, animations=None, lights=None, model=None, animation_graph=None, 
                 indoor_ambient_radiosity_color=(0.0, 0.0, 0.0, 1.0), indoor_ambient_radiosity_power=0.0, outdoor_ambient_radiosity_color=(0.0, 0.0, 0.0, 1.0), 
                 outdoor_ambient_radiosity_power=0.0, outdoor_fog_color=(0.0, 0.0, 0.0, 1.0), outdoor_fog_maximum_density=0.0, outdoor_fog_start_distance=0.0, 
                 outdoor_fog_opaque_distance=0.0, indoor_fog_color=(0.0, 0.0, 0.0, 1.0), indoor_fog_maximum_density=0.0, indoor_fog_start_distance=0.0, 
                 indoor_fog_opaque_distance=0.0, indoor_fog_screen=None, shader_functions_tag_block=None, animations_tag_block=None, lights_tag_block=None):
        self.header = header
        self.shader_functions = shader_functions
        self.animations = animations
        self.lights = lights
        self.model = model
        self.animation_graph = animation_graph
        self.indoor_ambient_radiosity_color = indoor_ambient_radiosity_color
        self.indoor_ambient_radiosity_power = indoor_ambient_radiosity_power
        self.outdoor_ambient_radiosity_color = outdoor_ambient_radiosity_color
        self.outdoor_ambient_radiosity_power = outdoor_ambient_radiosity_power
        self.outdoor_fog_color = outdoor_fog_color
        self.outdoor_fog_maximum_density = outdoor_fog_maximum_density
        self.outdoor_fog_start_distance = outdoor_fog_start_distance
        self.outdoor_fog_opaque_distance = outdoor_fog_opaque_distance
        self.indoor_fog_color = indoor_fog_color
        self.indoor_fog_maximum_density = indoor_fog_maximum_density
        self.indoor_fog_start_distance = indoor_fog_start_distance
        self.indoor_fog_opaque_distance = indoor_fog_opaque_distance
        self.indoor_fog_screen = indoor_fog_screen
        self.shader_functions_tag_block = shader_functions_tag_block
        self.animations_tag_block = animations_tag_block
        self.lights_tag_block = lights_tag_block

    class Animation:
        def __init__(self, animation_index=0, period=0.0):
            self.animation_index = animation_index
            self.period = period

    class Light:
        def __init__(self, lens_flare=None, lens_flare_marker_name="", flags=0, color=(0.0, 0.0, 0.0, 1.0), power=0.0, test_distance=0.0, direction=(0.0, 0.0), diameter=0.0):
            self.lens_flare = lens_flare
            self.lens_flare_marker_name = lens_flare_marker_name
            self.flags = flags
            self.color = color
            self.power = power
            self.test_distance = test_distance
            self.direction = direction
            self.diameter = diameter
