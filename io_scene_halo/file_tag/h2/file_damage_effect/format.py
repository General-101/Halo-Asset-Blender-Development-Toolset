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

class FunctionTypeEnum(Enum):
    linear = 0
    late = auto()
    very_late = auto()
    early = auto()
    very_early = auto()
    cosine = auto()
    zero = auto()
    one = auto()

class DamageEffectAsset():
    def __init__(self, header=None, body_header=None, player_response_header=None, player_responses=None, radius=(0.0, 0.0), cutoff_scale=0.0, flags=0, side_effect=0, 
                 category=0, damage_flags=0, aoe_core_radius=0.0, damage_lower_bound=0.0, damage_upper_bound=(0.0, 0.0), dmg_inner_cone_angle=0.0, dmg_outer_cone_angle=0.0, 
                 active_camouflage_damage=0.0, stun=0.0, maximum_stun=0.0, stun_time=0.0, instantaneous_acceleration=0.0, rider_direct_damage_scale=0.0, 
                 rider_maximum_transfer_damage_scale=0.0, rider_minimum_transfer_damage_scale=0.0, general_damage="", general_damage_length=0, specific_damage="", 
                 specific_damage_length=0, ai_stun_radius=0.0, ai_stun_bounds=(0.0, 0.0), shake_radius=0.0, emp_radius=0, player_responses_tag_block=None, 
                 impulse_duration=0.0, fade_function=0, rotation=0, pushback=0.0, jitter=(0.0, 0.0), shaking_duration=0.0, falloff_function=0, random_translation=0.0, 
                 random_rotation=0.0, wobble_function=0, wobble_function_period=0.0, wobble_weight=0.0, sound=None, forward_velocity=0.0, forward_radius=0.0, 
                 forward_exponent=0.0, outward_velocity=0.0, outward_radius=0.0, outward_exponent=0.0):
        self.header = header
        self.body_header = body_header
        self.player_response_header = player_response_header
        self.player_responses = player_responses
        self.radius = radius
        self.cutoff_scale = cutoff_scale
        self.flags = flags
        self.side_effect = side_effect
        self.category = category
        self.damage_flags = damage_flags
        self.aoe_core_radius = aoe_core_radius
        self.damage_lower_bound = damage_lower_bound
        self.damage_upper_bound = damage_upper_bound
        self.dmg_inner_cone_angle = dmg_inner_cone_angle
        self.dmg_outer_cone_angle = dmg_outer_cone_angle
        self.active_camouflage_damage = active_camouflage_damage
        self.stun = stun
        self.maximum_stun = maximum_stun
        self.stun_time = stun_time
        self.instantaneous_acceleration = instantaneous_acceleration
        self.rider_direct_damage_scale = rider_direct_damage_scale
        self.rider_maximum_transfer_damage_scale = rider_maximum_transfer_damage_scale
        self.rider_minimum_transfer_damage_scale = rider_minimum_transfer_damage_scale
        self.general_damage = general_damage
        self.general_damage_length = general_damage_length
        self.specific_damage = specific_damage
        self.specific_damage_length = specific_damage_length
        self.ai_stun_radius = ai_stun_radius
        self.ai_stun_bounds = ai_stun_bounds
        self.shake_radius = shake_radius
        self.emp_radius = emp_radius
        self.player_responses_tag_block = player_responses_tag_block
        self.impulse_duration = impulse_duration
        self.fade_function = fade_function
        self.rotation = rotation
        self.pushback = pushback
        self.jitter = jitter
        self.shaking_duration = shaking_duration
        self.falloff_function = falloff_function
        self.random_translation = random_translation
        self.random_rotation = random_rotation
        self.wobble_function = wobble_function
        self.wobble_function_period = wobble_function_period
        self.wobble_weight = wobble_weight
        self.sound = sound
        self.forward_velocity = forward_velocity
        self.forward_radius = forward_radius
        self.forward_exponent = forward_exponent
        self.outward_velocity = outward_velocity
        self.outward_radius = outward_radius
        self.outward_exponent = outward_exponent

    class PlayerResponse:
        def __init__(self, response_type=0, flash_type=0, priority=0, flash_duration=0.0, fade_function=0, maximum_intensity=0.0, color=(0.0, 0.0, 0.0, 0.0), low_vibration_duration=0.0,
                     high_vibration_duration=0.0, effect_name="", effect_name_length=0, sound_duration=0.0, functions=[]):
            self.response_type = response_type
            self.flash_type = flash_type
            self.priority = priority
            self.flash_duration = flash_duration
            self.fade_function = fade_function
            self.maximum_intensity = maximum_intensity
            self.color = color
            self.low_vibration_duration = low_vibration_duration
            self.high_vibration_duration = high_vibration_duration
            self.effect_name = effect_name
            self.effect_name_length = effect_name_length
            self.sound_duration = sound_duration
            self.functions = functions
