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

from enum import Flag, Enum, auto

SALT_SIZE = 64

class ShadowFadeDistance(Enum):
    fade_at_super_high_detail_level = 0
    fade_at_high_detail_level = auto()
    fade_at_medium_detail_level = auto()
    fade_at_low_detail_level = auto()
    fade_at_super_low_detail_level = auto()
    afde_never = auto()

class ModelFlags(Flag):
    active_camo_always_on = auto()
    active_camo_always_merge = auto()
    active_camo_never_merge = auto()

class RuntimeFlags(Flag):
    contains_runtime_nodes = auto()

class ModelAsset():
    def __init__(self):
        self.header = None
        self.model_body_header = None
        self.model_body = None
        self.variants_header = None
        self.variants = None
        self.materials_header = None
        self.materials = None
        self.new_damage_info_header = None
        self.new_damage_info = None
        self.targets_header = None
        self.targets = None
        self.runtime_regions_header = None
        self.runtime_regions = None
        self.runtime_nodes_header = None
        self.runtime_nodes = None
        self.model_object_data_header = None
        self.model_object_data = None
        self.scenario_load_parameters_header = None
        self.scenario_load_parameters = None

    class ModelBody:
        def __init__(self, render_model=None, collision_model=None, animation=None, physics=None, physics_model=None, disappear_distance=0.0, begin_fade_distance=0.0, 
                     reduce_to_l1=0.0, reduce_to_l2=0.0, reduce_to_l3=0.0, reduce_to_l4=0.0, reduce_to_l5=0.0, shadow_fade_distance=0, variants_tag_block=None, 
                     materials_tag_block=None, new_damage_info_tag_block=None, targets_tag_block=None, runtime_regions_tag_block=None, runtime_nodes_tag_block=None, 
                     model_object_data_tag_block=None, default_dialogue=None, unused=None, flags=0, default_dialogue_effect="", default_dialogue_effect_length=0, 
                     salt_array=None, runtime_flags=0, scenario_load_parameters_tag_block=None, hologram_shader=None, hologram_control_function="", 
                     hologram_control_function_length=0):
            self.render_model = render_model
            self.collision_model = collision_model
            self.animation = animation
            self.physics = physics
            self.physics_model = physics_model
            self.disappear_distance = disappear_distance
            self.begin_fade_distance = begin_fade_distance
            self.reduce_to_l1 = reduce_to_l1
            self.reduce_to_l2 = reduce_to_l2
            self.reduce_to_l3 = reduce_to_l3
            self.reduce_to_l4 = reduce_to_l4
            self.reduce_to_l5 = reduce_to_l5
            self.shadow_fade_distance = shadow_fade_distance
            self.variants_tag_block = variants_tag_block
            self.materials_tag_block = materials_tag_block
            self.new_damage_info_tag_block = new_damage_info_tag_block
            self.targets_tag_block = targets_tag_block
            self.runtime_regions_tag_block = runtime_regions_tag_block
            self.runtime_nodes_tag_block = runtime_nodes_tag_block
            self.model_object_data_tag_block = model_object_data_tag_block
            self.default_dialogue = default_dialogue
            self.unused = unused
            self.flags = flags
            self.default_dialogue_effect = default_dialogue_effect
            self.default_dialogue_effect_length = default_dialogue_effect_length
            self.salt_array = salt_array
            self.runtime_flags = runtime_flags
            self.scenario_load_parameters_tag_block = scenario_load_parameters_tag_block
            self.hologram_shader = hologram_shader
            self.hologram_control_function = hologram_control_function
            self.hologram_control_function_length = hologram_control_function_length
