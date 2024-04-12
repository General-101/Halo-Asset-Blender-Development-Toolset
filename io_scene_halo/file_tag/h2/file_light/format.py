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

from mathutils import Vector
from enum import Flag, Enum, auto

class LightFlags(Flag):
    no_illumination = auto()
    no_specular = auto()
    force_cast_environment_shadows_through_portals = auto()
    no_shadow = auto()
    force_frustum_visibility_on_small_light = auto()
    only_render_in_first_person = auto()
    only_render_in_third_person = auto()
    dont_fade_when_invisible = auto()
    multiplayer_override = auto()
    animated_gel = auto()
    only_in_dynamic_envmap = auto()
    ignore_parent_object = auto()
    dont_shadow_parent = auto()
    ignore_all_parents = auto()
    march_milestone_hack = auto()
    force_light_inside_world = auto()
    environment_doesnt_cast_stencil_shadows = auto()
    objects_dont_cast_stencil_shadows = auto()
    first_person_from_camera = auto()
    texture_camera_gel = auto()
    light_framerate_killer = auto()
    allowed_in_split_screen = auto()
    only_on_parent_bipeds = auto()

class ShapeTypeEnum(Enum):
    sphere = 0
    orthogonal = auto()
    projective = auto()
    pyramid = auto()

class ShadowTapBiasEnum(Enum):
    _3_tap = 0
    unused = auto()
    _1_tap = auto()

class InterpolationFlags(Flag):
    blend_in_hsv = auto()
    more_colors = auto()

class SpecularMaskEnum(Enum):
    default = 0
    none_no_mask = auto()
    gel_alpha = auto()
    gel_color = auto()

class FalloffFunctionEnum(Enum):
    default = 0
    narrow = auto()
    broad = auto()
    very_broad = auto()

class DiffuseContrastEnum(Enum):
    default_linear = 0
    high = auto()
    low = auto()
    very_low = auto()

class SpecularContrastEnum(Enum):
    default_one = 0
    high_linear = auto()
    low = auto()
    very_low = auto()

class FalloffGeometryEnum(Enum):
    default = 0
    directional = auto()
    spherical = auto()

class DefaultLightmapSettingEnum(Enum):
    dynamic_only = 0
    dynamic_with_lightmaps = auto()
    lightmaps_only = auto()

class EffectFalloffFunctionEnum(Enum):
    linear = 0
    late = auto()
    very_late = auto()
    early = auto()
    very_early = auto()
    cosine = auto()
    zero = auto()
    one = auto()

class EffectFalloffFunctionEnum(Enum):
    linear = 0
    late = auto()
    very_late = auto()
    early = auto()
    very_early = auto()
    cosine = auto()
    zero = auto()
    one = auto()

class FadeEnum(Enum):
    fade_very_far = 0
    fade_far = auto()
    fade_medium = auto()
    fade_close = auto()
    fade_very_close = auto()

class AnimationFlags(Flag):
    synchronized = auto()

class LightAsset():
    def __init__(self):
        self.header = None
        self.light_body_header = None
        self.light_body = None
        self.brightness_animation_header = None
        self.brightness_animation = None
        self.color_animation_header = None
        self.color_animation = None
        self.gel_animation_header = None
        self.gel_animation = None

    class LightBody:
        def __init__(self, flags=0, shape_type=0, size_modifier=(0.0, 0.0), shadow_quality_bias=0.0, shadow_tap_bias=0, radius=0.0, specular_radius=0.0, near_width=0.0, 
                     height_stretch=0.0, field_of_view=0.0, falloff_distance=0.0, cutoff_distance=0.0, interpolation_flags=0, bloom_bounds=(0.0, 0.0), 
                     specular_lower_bound=(0.0, 0.0, 0.0, 1.0), specular_upper_bound=(0.0, 0.0, 0.0, 1.0), diffuse_lower_bound=(0.0, 0.0, 0.0, 1.0), 
                     diffuse_upper_bound=(0.0, 0.0, 0.0, 1.0), brightness_bounds=(0.0, 0.0), gel_map=None, specular_mask=0, falloff_function=0, diffuse_contrast=0, 
                     specular_contrast=0, falloff_geometry=0, lens_flare=None, bounding_radius=0.0, light_volume=None, default_lightmap_setting=0, lightmap_half_life=0.0, 
                     lightmap_light_scale=0.0, duration=0.0, effect_falloff_function=0, illumination_fade=0, shadow_fade=0, specular_fade=0, animation_flags=0, 
                     brightness_animation_tag_block=None, color_animation_tag_block=None, gel_animation_tag_block=None, shader=None):
            self.flags = flags
            self.shape_type = shape_type
            self.size_modifier = size_modifier
            self.shadow_quality_bias = shadow_quality_bias
            self.shadow_tap_bias = shadow_tap_bias
            self.radius = radius
            self.specular_radius = specular_radius
            self.near_width = near_width
            self.height_stretch = height_stretch
            self.field_of_view = field_of_view
            self.falloff_distance = falloff_distance
            self.cutoff_distance = cutoff_distance
            self.interpolation_flags = interpolation_flags
            self.bloom_bounds = bloom_bounds
            self.specular_lower_bound = specular_lower_bound
            self.specular_upper_bound = specular_upper_bound
            self.diffuse_lower_bound = diffuse_lower_bound
            self.diffuse_upper_bound = diffuse_upper_bound
            self.brightness_bounds = brightness_bounds
            self.gel_map = gel_map
            self.specular_mask = specular_mask
            self.falloff_function = falloff_function
            self.diffuse_contrast = diffuse_contrast
            self.specular_contrast = specular_contrast
            self.falloff_geometry = falloff_geometry
            self.lens_flare = lens_flare
            self.bounding_radius = bounding_radius
            self.light_volume = light_volume
            self.default_lightmap_setting = default_lightmap_setting
            self.lightmap_half_life = lightmap_half_life
            self.lightmap_light_scale = lightmap_light_scale
            self.duration = duration
            self.effect_falloff_function = effect_falloff_function
            self.illumination_fade = illumination_fade
            self.shadow_fade = shadow_fade
            self.specular_fade = specular_fade
            self.animation_flags = animation_flags
            self.brightness_animation_tag_block = brightness_animation_tag_block
            self.color_animation_tag_block = color_animation_tag_block
            self.gel_animation_tag_block = gel_animation_tag_block
            self.shader = shader
