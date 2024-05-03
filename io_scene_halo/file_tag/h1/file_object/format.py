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
from ....file_tag.h2.file_object.format import ObjectFlags as H2ObjectFlags

class ObjectFlags(Flag):
    does_not_cast_shadow = auto()
    transparent_self_occlusion = auto()
    brighter_than_it_should_be = auto()
    not_a_pathfinding_obstacle = auto()
    extension_of_parent = auto()
    cast_shadow_by_default = auto()
    does_not_have_remastered_geometry = auto()

class ObjectFunctionEnum(Enum):
    none = 0
    body_vitality = auto()
    shield_vitality = auto()
    recent_body_damage = auto()
    recent_shield_damage = auto()
    random_constant = auto()
    umbrella_shield_vitality = auto()
    shield_stun = auto()
    recent_umbrella_shield_vitality = auto()
    umbrella_shield_stun = auto()
    region_00_damage = auto()
    region_01_damage = auto()
    region_02_damage = auto()
    region_03_damage = auto()
    region_04_damage = auto()
    region_05_damage = auto()
    region_06_damage = auto()
    region_07_damage = auto()
    alive = auto()
    compass = auto()

class ScaleEnum(Enum):
    none = 0
    a_out = auto()
    b_out = auto()
    c_out = auto()
    d_out = auto()

class ColorEnum(Enum):
    none = 0
    a = auto()
    b = auto()
    c = auto()
    d = auto()

class FunctionFlags(Flag):
    invert = auto()
    additive = auto()
    always_active = auto()

class FunctionScaleEnum(Enum):
    none = 0
    a_in = auto()
    b_in = auto()
    c_in = auto()
    d_in = auto()
    a_out = auto()
    b_out = auto()
    c_out = auto()
    d_out = auto()

class FunctionEnum(Enum):
    one = 0
    zero = auto()
    cosine = auto()
    cosine_variable_period = auto()
    diagonal_wave = auto()
    diagonal_wave_variable_period = auto()
    slide = auto()
    slide_variable_period = auto()
    noise = auto()
    jitter = auto()
    wander = auto()
    spark = auto()

class MapEnum(Enum):
    linear = 0
    early = auto()
    very_early = auto()
    late = auto()
    very_late = auto()
    cosine = auto()

class BoundsModeEnum(Enum):
    clip = 0
    clip_and_normalize = auto()
    scale_to_fit = auto()

class ColorChangeFlags(Flag):
    blend_in_hsv = auto()
    more_colors = auto()

class ResourceTypeEnum(Enum):
    bitmap = 0
    sound = auto()

def upgrade_h1_object_flags(object_flags):
    flags = 0
    active_h1_flags = [flag.name for flag in ObjectFlags if flag in ObjectFlags(object_flags)]
    if "does_not_cast_shadow" in active_h1_flags:
        flags += H2ObjectFlags.does_not_cast_shadow.value
    if "not_a_pathfinding_obstacle" in active_h1_flags:
        flags += H2ObjectFlags.not_a_pathfinding_obstacle.value
    if "extension_of_parent" in active_h1_flags:
        flags += H2ObjectFlags.extension_of_parent.value

    return flags

def get_valid_h1_object_functions(function_name):
    valid_function_name = ""
    if function_name == "body_vitality":
        valid_function_name = "body_vitality"
    elif function_name == "shield_vitality":
        valid_function_name = "shield_vitality"
    elif function_name == "alive":
        valid_function_name = "alive"
    elif function_name == "compass":
        valid_function_name = "compass"

    return valid_function_name

class ObjectAsset():
    def __init__(self, object_flags=0, bounding_radius=0.0, bounding_offset=Vector(), origin_offset=Vector(), acceleration_scale=0.0, model=None, animation_graph=None,
                 collision_model=None, physics=None, modifier_shader=None, creation_effect=None, render_bounding_radius=0.0, object_a_in=0, object_b_in=0, object_c_in=0,
                 object_d_in=0, hud_text_message_index=0, forced_shader_permutation_index=0, attachments_tag_block=None, widgets_tag_block=None, functions_tag_block=None,
                 change_colors_tag_block=None, predicted_resources_tag_block=None, attachments=None, widgets=None, functions=None, change_colors=None, predicted_resources=None):
        self.header = None
        self.object_flags = object_flags
        self.bounding_radius = bounding_radius
        self.bounding_offset = bounding_offset
        self.origin_offset = origin_offset
        self.acceleration_scale = acceleration_scale
        self.model = model
        self.animation_graph = animation_graph
        self.collision_model = collision_model
        self.physics = physics
        self.modifier_shader = modifier_shader
        self.creation_effect = creation_effect
        self.render_bounding_radius = render_bounding_radius
        self.object_a_in = object_a_in
        self.object_b_in = object_b_in
        self.object_c_in = object_c_in
        self.object_d_in = object_d_in
        self.hud_text_message_index = hud_text_message_index
        self.forced_shader_permutation_index = forced_shader_permutation_index
        self.attachments_tag_block = attachments_tag_block
        self.widgets_tag_block = widgets_tag_block
        self.functions_tag_block = functions_tag_block
        self.change_colors_tag_block = change_colors_tag_block
        self.predicted_resources_tag_block = predicted_resources_tag_block
        self.attachments = attachments
        self.widgets = widgets
        self.functions = functions
        self.change_colors = change_colors
        self.predicted_resources = predicted_resources

    class Attachment:
        def __init__(self, attachment_type=None, marker="", primary_scale=0, secondary_scale=0, change_color=0):
            self.attachment_type = attachment_type
            self.marker = marker
            self.primary_scale = primary_scale
            self.secondary_scale = secondary_scale
            self.change_color = change_color

    class Function:
        def __init__(self, flags=0, period=0, scale_period_by=0, function_type=0, scale_function_by=0, wobble_function_type=0, wobble_period=0, wobble_magnitude=0,
                     square_wave_threshold=0, step_count=0, map_to=0, sawtooth_count=0, add_by=0, scale_result_by=0, bounds_mode=0, bounds=(0.0, 0.0), turn_off_with=0,
                     scale_by=0, usage=""):
            self.flags = flags
            self.period = period
            self.scale_period_by = scale_period_by
            self.function_type = function_type
            self.scale_function_by = scale_function_by
            self.wobble_function_type = wobble_function_type
            self.wobble_period = wobble_period
            self.wobble_magnitude = wobble_magnitude
            self.square_wave_threshold = square_wave_threshold
            self.step_count = step_count
            self.map_to = map_to
            self.sawtooth_count = sawtooth_count
            self.add_by = add_by
            self.scale_result_by = scale_result_by
            self.bounds_mode = bounds_mode
            self.bounds = bounds
            self.turn_off_with = turn_off_with
            self.scale_by = scale_by
            self.usage = usage

    class ChangeColor:
        def __init__(self, darken_by=0, scale_by=0, scale_flags=0, color_lower_bound=(0, 0, 0, 0), color_upper_bound=(0, 0, 0, 0), permutations_tag_block=None,
                     permutations=None):
            self.darken_by = darken_by
            self.scale_by = scale_by
            self.scale_flags = scale_flags
            self.color_lower_bound = color_lower_bound
            self.color_upper_bound = color_upper_bound
            self.permutations_tag_block = permutations_tag_block
            self.permutations = permutations

    class Permutation:
        def __init__(self, weight=0.0, color_lower_bound=(0, 0, 0, 0), color_upper_bound=(0, 0, 0, 0)):
            self.weight = weight
            self.color_lower_bound = color_lower_bound
            self.color_upper_bound = color_upper_bound

    class PredictedResource:
        def __init__(self, predicted_resources_type=0, resource_index=0, tag_index=0):
            self.predicted_resources_type = predicted_resources_type
            self.resource_index = resource_index
            self.tag_index = tag_index
