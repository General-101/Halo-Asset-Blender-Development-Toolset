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
from ..file_unit.format import UnitAsset

class BipedFlags(Flag):
    turns_without_animating = auto()
    passes_through_other_bipeds = auto()
    immune_for_falling_damage = auto()
    rotate_while_airborne = auto()
    uses_limp_body_physics = auto()
    unused_5 = auto()
    random_speed_increase = auto()
    unused_7 = auto()
    spawn_death_children_on_destroy = auto()
    stunned_by_emp_damage = auto()
    dead_physics_when_stunned = auto()
    always_ragdoll_when_dead = auto()

class LockOnFlags(Flag):
    locked_by_human_targeting = auto()
    locked_by_plasma_targeting = auto()
    always_locked_by_plasma_targeting = auto()

class CollisionFlags(Flag):
    centered_at_origin = auto()
    shape_spherical = auto()
    uses_player_physics = auto()
    climb_any_surface = auto()
    flying = auto()
    not_physical = auto()
    dead_character_collision_group = auto()

class BipedAsset(UnitAsset):
    def __init__(self):
        super().__init__()
        self.header = None
        self.biped_body_header = None
        self.biped_body = None
        self.dead_sphere_shapes_header = None
        self.dead_sphere_shapes = None
        self.pill_shapes_header = None
        self.pill_shapes = None
        self.sphere_shapes_header = None
        self.sphere_shapes = None
        self.contact_points_header = None
        self.contact_points = None

    class BipedBody(UnitAsset.UnitBody):
        def __init__(self, moving_turning_speed=0.0, biped_flags=0, stationary_turning_threshold=0.0, jump_velocity=0.0, maximum_soft_landing_time=0.0, 
                     maximum_hard_landing_time=0.0, minimum_soft_landing_velocity=0.0, minimum_hard_landing_velocity=0.0, maximum_hard_landing_velocity=0.0, 
                     death_hard_landing_velocity=0.0, stun_duration=0.0, standing_camera_height=0.0, crouching_camera_height=0.0, crouching_transition_time=0.0, 
                     camera_interpolation_start=0.0, camera_interpolation_end=0.0, camera_forward_movement_scale=0.0, camera_side_movement_scale=0.0, 
                     camera_vertical_movement_scale=0.0, camera_exclusion_distance=0.0, autoaim_width=0.0, lock_on_flags=0, lock_on_distance=0.0, head_shot_acceleration_scale=0.0, 
                     area_damage_effect=None, collision_flags=0, height_standing=0.0, height_crouching=0.0, radius=0.0, mass=0.0, living_material_name="", 
                     living_material_name_length=0, dead_material_name="", dead_material_name_length=0, dead_sphere_shapes_tag_block=None, pill_shapes_tag_block=None, 
                     sphere_shapes_tag_block=None, maximum_slope_angle=0.0, downhill_falloff_angle=0.0, downhill_cuttoff_angle=0.0, uphill_falloff_angle=0.0, 
                     uphill_cuttoff_angle=0.0, downhill_velocity_scale=0.0, uphill_velocity_scale=0.0, bank_angle=0.0, bank_apply_time=0.0, bank_decay_time=0.0, pitch_ratio=0.0, 
                     max_velocity=0.0, max_sidestep_velocity=0.0, acceleration=0.0, deceleration=0.0, angular_velocity_maximum=0.0, angular_acceleration_maximum=0.0, 
                     crouch_velocity_modifier=0.0, contact_points_tag_block=None, reanimation_character=None, death_spawn_character=None, death_spawn_count=0):
            super().__init__()
            self.moving_turning_speed = moving_turning_speed
            self.biped_flags = biped_flags
            self.stationary_turning_threshold = stationary_turning_threshold
            self.jump_velocity = jump_velocity
            self.maximum_soft_landing_time = maximum_soft_landing_time
            self.maximum_hard_landing_time = maximum_hard_landing_time
            self.minimum_soft_landing_velocity = minimum_soft_landing_velocity
            self.minimum_hard_landing_velocity = minimum_hard_landing_velocity
            self.maximum_hard_landing_velocity = maximum_hard_landing_velocity
            self.death_hard_landing_velocity = death_hard_landing_velocity
            self.stun_duration = stun_duration
            self.standing_camera_height = standing_camera_height
            self.crouching_camera_height = crouching_camera_height
            self.crouching_transition_time = crouching_transition_time
            self.camera_interpolation_start = camera_interpolation_start
            self.camera_interpolation_end = camera_interpolation_end
            self.camera_forward_movement_scale = camera_forward_movement_scale
            self.camera_side_movement_scale = camera_side_movement_scale
            self.camera_vertical_movement_scale = camera_vertical_movement_scale
            self.camera_exclusion_distance = camera_exclusion_distance
            self.autoaim_width = autoaim_width
            self.lock_on_flags = lock_on_flags
            self.lock_on_distance = lock_on_distance
            self.head_shot_acceleration_scale = head_shot_acceleration_scale
            self.area_damage_effect = area_damage_effect
            self.collision_flags = collision_flags
            self.height_standing = height_standing
            self.height_crouching = height_crouching
            self.radius = radius
            self.mass = mass
            self.living_material_name = living_material_name
            self.living_material_name_length = living_material_name_length
            self.dead_material_name = dead_material_name
            self.dead_material_name_length = dead_material_name_length
            self.dead_sphere_shapes_tag_block = dead_sphere_shapes_tag_block
            self.pill_shapes_tag_block = pill_shapes_tag_block
            self.sphere_shapes_tag_block = sphere_shapes_tag_block
            self.maximum_slope_angle = maximum_slope_angle
            self.downhill_falloff_angle = downhill_falloff_angle
            self.downhill_cuttoff_angle = downhill_cuttoff_angle
            self.uphill_falloff_angle = uphill_falloff_angle
            self.uphill_cuttoff_angle = uphill_cuttoff_angle
            self.downhill_velocity_scale = downhill_velocity_scale
            self.uphill_velocity_scale = uphill_velocity_scale
            self.bank_angle = bank_angle
            self.bank_apply_time = bank_apply_time
            self.bank_decay_time = bank_decay_time
            self.pitch_ratio = pitch_ratio
            self.max_velocity = max_velocity
            self.max_sidestep_velocity = max_sidestep_velocity
            self.acceleration = acceleration
            self.deceleration = deceleration
            self.angular_velocity_maximum = angular_velocity_maximum
            self.angular_acceleration_maximum = angular_acceleration_maximum
            self.crouch_velocity_modifier = crouch_velocity_modifier
            self.contact_points_tag_block = contact_points_tag_block
            self.reanimation_character = reanimation_character
            self.death_spawn_character = death_spawn_character
            self.death_spawn_count = death_spawn_count

    class Shape:
        def __init__(self, name="", name_length=0, material=-1, flags=0, relative_mass_scale=0.0, friction=0.0, restitution=0.0, volume=0.0, mass=0.0, phantom=-1, size_a=0, 
                     count_a=0, radius=0.0, size_b=0, count_b=0, rotation_i=Vector(), rotation_j=Vector(), rotation_k=Vector(), translation=Vector(), bottom=Vector(), top=Vector()):
            self.name = name
            self.name_length = name_length
            self.material = material
            self.flags = flags
            self.relative_mass_scale = relative_mass_scale
            self.friction = friction
            self.restitution = restitution
            self.volume = volume
            self.mass = mass
            self.phantom = phantom
            self.size_a = size_a
            self.count_a = count_a
            self.radius = radius
            self.size_b = size_b
            self.count_b = count_b
            self.rotation_i = rotation_i
            self.rotation_j = rotation_j
            self.rotation_k = rotation_k
            self.translation = translation
            self.bottom = bottom
            self.top = top


