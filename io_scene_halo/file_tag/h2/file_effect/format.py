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

class EffectFlags(Flag):
    deleted_when_attachment_deactivates = auto()

class EventFlags(Flag):
    disabled_for_debugging = auto()

class EnvironmentEnum(Enum):
    any_environment = 0
    air_only = auto()
    water_only = auto()
    space_only = auto()

class ModeEnum(Enum):
    either_mode = 0
    violent_mode_only = auto()
    nonviolent_mode_only = auto()

class PartFlags(Flag):
    face_down_regardless_of_location_decals = auto()
    offset_origin_away_from_geometry_lights = auto()
    never_attached_to_object = auto()
    disabled_for_debugging = auto()
    draw_regardless_of_distance = auto()

class ScaleFlags(Flag):
    velocity = auto()
    velocity_delta = auto()
    velocity_cone_angle = auto()
    angular_velocity = auto()
    angular_velocity_delta = auto()
    type_specific_scale = auto()

class CoordinateSystemEnum(Enum):
    world = 0
    local = auto()
    parent = auto()

class CameraModeEnum(Enum):
    independent_of_camera_mode = 0
    only_in_first_person = auto()
    only_in_third_person = auto()
    both_first_and_third = auto()

class ParticleSystemFlags(Flag):
    glow = auto()
    cinematics = auto()
    looping_particle = auto()
    disabled_for_debug = auto()
    inherit_effect_velocity = auto()
    dont_render_system = auto()
    render_when_zoomed = auto()
    spread_between_ticks = auto()
    persistent_particle = auto()
    expensive_visibility = auto()

class EffectAsset():
    def __init__(self, header=None, body_header=None, locations_header=None, locations=None, events_header=None, events=None, flags=0, loop_start_event=0, 
                 locations_tag_block=None, events_tag_block=None, looping_sound=None, location=0, always_play_distance=0.0, never_play_distance=0.0):
        self.header = header
        self.body_header = body_header
        self.locations_header = locations_header
        self.locations = locations
        self.events_header = events_header
        self.events = events
        self.flags = flags
        self.loop_start_event = loop_start_event
        self.locations_tag_block = locations_tag_block
        self.events_tag_block = events_tag_block
        self.looping_sound = looping_sound
        self.location = location
        self.always_play_distance = always_play_distance
        self.never_play_distance = never_play_distance

    class Location:
        def __init__(self, name="", name_length=0):
            self.name = name
            self.name_length = name_length

    class Event:
        def __init__(self, flags=0, skip_fraction=0.0, delay_bounds=(0.0, 0.0), duration_bounds=(0.0, 0.0), parts_tag_block=None, parts_header=None, parts=None,
                     beams_tag_block=None, beams_header=None, beams=None, accelerations_tag_block=None, accelerations_header=None, accelerations=None,
                     particle_systems_tag_block=None, particle_systems_header=None, particle_systems=None):
            self.flags = flags
            self.skip_fraction = skip_fraction
            self.delay_bounds = delay_bounds
            self.duration_bounds = duration_bounds
            self.parts_tag_block = parts_tag_block
            self.parts_header = parts_header
            self.parts = parts
            self.beams_tag_block = beams_tag_block
            self.beams_header = beams_header
            self.beams = beams
            self.accelerations_tag_block = accelerations_tag_block
            self.accelerations_header = accelerations_header
            self.accelerations = accelerations
            self.particle_systems_tag_block = particle_systems_tag_block
            self.particle_systems_header = particle_systems_header
            self.particle_systems = particle_systems

    class Part:
        def __init__(self, create_in_environment=0, create_in_mode=0, location=0, flags=0, object_type=None, velocity_bounds=(0.0, 0.0), velocity_cone_angle=0.0,
                     angular_velocity_bounds=(0.0, 0.0), radius_modifier_bounds=(0.0, 0.0), a_scales_value=0, b_scales_value=0):
            self.create_in_environment = create_in_environment
            self.create_in_mode = create_in_mode
            self.location = location
            self.flags = flags
            self.object_type = object_type
            self.velocity_bounds = velocity_bounds
            self.velocity_cone_angle = velocity_cone_angle
            self.angular_velocity_bounds = angular_velocity_bounds
            self.radius_modifier_bounds = radius_modifier_bounds
            self.a_scales_value = a_scales_value
            self.b_scales_value = b_scales_value

    class Beam:
        def __init__(self, shader=None, location=0, properties=None):
            self.shader = shader
            self.location = location
            self.properties = properties

    class Acceleration:
        def __init__(self, create_in_environment=0, create_in_mode=0, location=0, acceleration=0.0, inner_cone_angle=0.0, outer_cone_angle=0.0):
            self.create_in_environment = create_in_environment
            self.create_in_mode = create_in_mode
            self.location = location
            self.acceleration = acceleration
            self.inner_cone_angle = inner_cone_angle
            self.outer_cone_angle = outer_cone_angle

    class ParticleSystem:
        def __init__(self, particle=None, location=0, coordinate_system=0, environment=0, disposition=0, camera_mode=0, sort_bias=0, flags=0, lod_in_distance=0.0,
                     lod_feather_in_delta=0.0, lod_out_distance=0.0, lod_feather_out_delta=0.0, emitters_tag_block=None, emitters_header=None, emitters=None):
            self.particle = particle
            self.location = location
            self.coordinate_system = coordinate_system
            self.environment = environment
            self.disposition = disposition
            self.camera_mode = camera_mode
            self.sort_bias = sort_bias
            self.flags = flags
            self.lod_in_distance = lod_in_distance
            self.lod_feather_in_delta = lod_feather_in_delta
            self.lod_out_distance = lod_out_distance
            self.lod_feather_out_delta = lod_feather_out_delta
            self.emitters_tag_block = emitters_tag_block
            self.emitters_header = emitters_header
            self.emitters = emitters

    class Emitter:
        def __init__(self, particle_physics=None, particle_properties=None, emission_shape=0, emission_properties=None, translational_offset=Vector(), relative_direction=(0.0, 0.0)):
            self.particle_physics = particle_physics
            self.particle_properties = particle_properties
            self.emission_shape = emission_shape
            self.emission_properties = emission_properties
            self.translational_offset = translational_offset
            self.relative_direction = relative_direction
