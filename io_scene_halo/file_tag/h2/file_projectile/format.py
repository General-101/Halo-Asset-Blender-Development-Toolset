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
from ..file_object.format import ObjectAsset

class ResponseEnum(Enum):
    impact_detonate = 0
    fizzle = auto()
    overpenetrate = auto()
    attach = auto()
    bounce = auto()
    bounce_dud = auto()
    fizzle_ricochet = auto()

class ProjectileAsset(ObjectAsset):
    def __init__(self):
        super().__init__()
        self.header = None
        self.projectile_body_header = None
        self.projectile_body = None
        self.material_responses_header = None
        self.material_responses = None

    class ProjectileBody(ObjectAsset.ObjectBody):
        def __init__(self, projectile_flags=0, detonation_timer_starts=0, impact_noise=0, ai_perception_radius=0.0, collision_radius=0.0, arming_time=0.0, danger_radius=0.0,
                     timer=(0.0, 0.0), minimum_velocity=0.0, maximum_range=0.0, detonation_noise=0, super_detonation_projectile_count=0, detonation_started=None,
                     detonation_effect_airborne=None, detonation_effect_ground=None, detonation_damage=None, attached_detonation_damage=None, super_detonation=None,
                     super_detonation_damage=None, detonation_sound=None, damage_reporting_type=0, super_attached_detonation_damage_effect=None, material_effect_radius=0.0,
                     flyby_sound=None, impact_effect=None, impact_damage=None, boarding_detonation_time=0.0, boarding_detonation_damage_effect=None,
                     boarding_attached_detonation_damage_effect=None, air_gravity_scale=0.0, air_damage_range=(0.0, 0.0), water_gravity_scale=0.0, water_damage_range=(0.0, 0.0),
                     initial_velocity=0.0, final_velocity=0.0, guided_angular_velocity_lower=0.0, guided_angular_velocity_upper=0.0, acceleration_range=(0.0, 0.0),
                     targeted_leading_fraction=0.0, material_responses_tag_block=None):
            super().__init__()
            self.projectile_flags = projectile_flags
            self.detonation_timer_starts = detonation_timer_starts
            self.impact_noise = impact_noise
            self.ai_perception_radius = ai_perception_radius
            self.collision_radius = collision_radius
            self.arming_time = arming_time
            self.danger_radius = danger_radius
            self.timer = timer
            self.minimum_velocity = minimum_velocity
            self.maximum_range = maximum_range
            self.detonation_noise = detonation_noise
            self.super_detonation_projectile_count = super_detonation_projectile_count
            self.detonation_started = detonation_started
            self.detonation_effect_airborne = detonation_effect_airborne
            self.detonation_effect_ground = detonation_effect_ground
            self.detonation_damage = detonation_damage
            self.attached_detonation_damage = attached_detonation_damage
            self.super_detonation = super_detonation
            self.super_detonation_damage = super_detonation_damage
            self.detonation_sound = detonation_sound
            self.damage_reporting_type = damage_reporting_type
            self.super_attached_detonation_damage_effect = super_attached_detonation_damage_effect
            self.material_effect_radius = material_effect_radius
            self.flyby_sound = flyby_sound
            self.impact_effect = impact_effect
            self.impact_damage = impact_damage
            self.boarding_detonation_time = boarding_detonation_time
            self.boarding_detonation_damage_effect = boarding_detonation_damage_effect
            self.boarding_attached_detonation_damage_effect = boarding_attached_detonation_damage_effect
            self.air_gravity_scale = air_gravity_scale
            self.air_damage_range = air_damage_range
            self.water_gravity_scale = water_gravity_scale
            self.water_damage_range = water_damage_range
            self.initial_velocity = initial_velocity
            self.final_velocity = final_velocity
            self.guided_angular_velocity_lower = guided_angular_velocity_lower
            self.guided_angular_velocity_upper = guided_angular_velocity_upper
            self.acceleration_range = acceleration_range
            self.targeted_leading_fraction = targeted_leading_fraction
            self.material_responses_tag_block = material_responses_tag_block

    class MaterialResponse:
        def __init__(self, flags=0, result_response=0, result_effect=None, material_name="", material_name_length=0, potential_result_response=0, potential_result_flags=0,
                     chance_fraction=0.0, between=(0.0, 0.0), and_bounds=(0.0, 0.0), potential_result_effect=None, scale_effects_by=0, angular_noise=0.0, velocity_noise=0.0,
                     detonation_effect=None, initial_friction=0.0, maximum_distance=0.0, parallel_friction=0.0, perpendicular_friction=0.0):
            self.flags = flags
            self.result_response = result_response
            self.result_effect = result_effect
            self.material_name = material_name
            self.material_name_length = material_name_length
            self.potential_result_response = potential_result_response
            self.potential_result_flags = potential_result_flags
            self.chance_fraction = chance_fraction
            self.between = between
            self.and_bounds = and_bounds
            self.potential_result_effect = potential_result_effect
            self.scale_effects_by = scale_effects_by
            self.angular_noise = angular_noise
            self.velocity_noise = velocity_noise
            self.detonation_effect = detonation_effect
            self.initial_friction = initial_friction
            self.maximum_distance = maximum_distance
            self.parallel_friction = parallel_friction
            self.perpendicular_friction = perpendicular_friction
