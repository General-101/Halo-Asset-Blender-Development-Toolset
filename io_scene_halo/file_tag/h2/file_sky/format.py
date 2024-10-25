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
from mathutils import Vector

class SkyFlags(Flag):
    fixed_in_worldspace = auto()
    deprecated = auto()
    sky_casts_light_from_below = auto()
    disable_sky_in_lightmaps = auto()
    fog_only_affects_containing_clusters = auto()
    use_clear_color = auto()

class LightFlags(Flag):
    affects_exteriors = auto()
    affects_interiors = auto()
    direct_illumination_in_lightmaps = auto()
    indirect_illumination_in_lightmaps = auto()

class SkyAsset():
    def __init__(self, header=None, body_header=None, cubemap_header=None, cubemap=None, atmospheric_fog_header=None, atmospheric_fog=None, secondary_fog_header=None, 
                 secondary_fog=None, sky_fog_header=None, sky_fog=None, patchy_fog_header=None, patchy_fog=None, lights_header=None, lights=None, 
                 shader_functions_header=None, shader_functions=None, animations_header=None, animations=None, render_model=None, animation_graph=None, flags=0, 
                 render_model_scale=0.0, movement_scale=0.0, cubemap_tag_block=None, indoor_ambient_color=(0.0, 0.0, 0.0, 1.0), outdoor_ambient_color=(0.0, 0.0, 0.0, 1.0), 
                 fog_spread_distance=0.0, atmospheric_fog_tag_block=None, secondary_fog_tag_block=None, sky_fog_tag_block=None, patchy_fog_tag_block=None, amount=0.0, 
                 threshold=0.0, brightness=0.0, gamma_power=0.0, lights_tag_block=None, global_sky_rotation=0.0, shader_functions_tag_block=None, animations_tag_block=None, 
                 clear_color=(0.0, 0.0, 0.0, 1.0)):
        self.header = header
        self.body_header = body_header
        self.cubemap_header = cubemap_header
        self.cubemap = cubemap
        self.atmospheric_fog_header = atmospheric_fog_header
        self.atmospheric_fog = atmospheric_fog
        self.secondary_fog_header = secondary_fog_header
        self.secondary_fog = secondary_fog
        self.sky_fog_header = sky_fog_header
        self.sky_fog = sky_fog
        self.patchy_fog_header = patchy_fog_header
        self.patchy_fog = patchy_fog
        self.lights_header = lights_header
        self.lights = lights
        self.shader_functions_header = shader_functions_header
        self.shader_functions = shader_functions
        self.animations_header = animations_header
        self.animations = animations
        self.render_model = render_model
        self.animation_graph = animation_graph
        self.flags = flags
        self.render_model_scale = render_model_scale
        self.movement_scale = movement_scale
        self.cubemap_tag_block = cubemap_tag_block
        self.indoor_ambient_color = indoor_ambient_color
        self.outdoor_ambient_color = outdoor_ambient_color
        self.fog_spread_distance = fog_spread_distance
        self.atmospheric_fog_tag_block = atmospheric_fog_tag_block
        self.secondary_fog_tag_block = secondary_fog_tag_block
        self.sky_fog_tag_block = sky_fog_tag_block
        self.patchy_fog_tag_block = patchy_fog_tag_block
        self.amount = amount
        self.threshold = threshold
        self.brightness = brightness
        self.gamma_power = gamma_power
        self.lights_tag_block = lights_tag_block
        self.global_sky_rotation = global_sky_rotation
        self.shader_functions_tag_block = shader_functions_tag_block
        self.animations_tag_block = animations_tag_block
        self.clear_color = clear_color

    class Cubemap:
        def __init__(self, cubemap_reference=None, power_scale=0.0):
            self.cubemap_reference = cubemap_reference
            self.power_scale = power_scale

    class Fog:
        def __init__(self, color=(0.0, 0.0, 0.0, 1.0), maximum_density=0.0, start_distance=0.0, opaque_distance=0.0):
            self.color = color
            self.maximum_density = maximum_density
            self.start_distance = start_distance
            self.opaque_distance = opaque_distance

    class PatchyFog:
        def __init__(self, color=(0.0, 0.0, 0.0, 1.0), density=(0.0, 0.0), distance=(0.0, 0.0), patchy_fog=None):
            self.color = color
            self.density = density
            self.distance = distance
            self.patchy_fog = patchy_fog

    class Light:
        def __init__(self, direction_vector=Vector(), direction=(0.0, 0.0), lens_flare=None, fog_tag_block=None, fog_header=None, fog=None, fog_opposite_tag_block=None,
                     fog_opposite_header=None, fog_opposite=None, radiosity_tag_block=None, radiosity_header=None, radiosity=None):
            self.direction_vector = direction_vector
            self.direction = direction
            self.lens_flare = lens_flare
            self.fog_tag_block = fog_tag_block
            self.fog_header = fog_header
            self.fog = fog
            self.fog_opposite_tag_block = fog_opposite_tag_block
            self.fog_opposite_header = fog_opposite_header
            self.fog_opposite = fog_opposite
            self.radiosity_tag_block = radiosity_tag_block
            self.radiosity_header = radiosity_header
            self.radiosity = radiosity

    class LightFog:
        def __init__(self, color=(0.0, 0.0, 0.0, 1.0), maximum_density=0.0, start_distance=0.0, opaque_distance=0.0, cone=(0.0, 0.0), atmospheric_fog_influence=0.0,
                     secondary_fog_influence=0.0, sky_fog_influence=0.0):
            self.color = color
            self.maximum_density = maximum_density
            self.start_distance = start_distance
            self.opaque_distance = opaque_distance
            self.cone = cone
            self.atmospheric_fog_influence = atmospheric_fog_influence
            self.secondary_fog_influence = secondary_fog_influence
            self.sky_fog_influence = sky_fog_influence

    class Radiosity:
        def __init__(self, flags=0, color=(0.0, 0.0, 0.0, 1.0), power=0.0, test_distance=0.0, diameter=0.0):
            self.flags = flags
            self.color = color
            self.power = power
            self.test_distance = test_distance
            self.diameter = diameter

    class Animation:
        def __init__(self, animation_index=0, period=0.0):
            self.animation_index = animation_index
            self.period = period
