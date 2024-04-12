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

class ParticleFlags(Flag):
    spins = auto()
    random_u_mirror = auto()
    random_v_mirror = auto()
    frame_animation_one_shot = auto()
    select_random_sequence = auto()
    disable_frame_blending = auto()
    can_animate_backwards = auto()
    receive_lightmap_lighting = auto()
    tint_from_diffuse_texture = auto()
    dies_at_rest = auto()
    dies_on_structure_collision = auto()
    dies_in_media = auto()
    dies_in_air = auto()
    bitmap_authored_vertically = auto()
    has_sweetener = auto()

class ParticleBillboardStyleEnum(Enum):
    screen_facing = 0
    parallel_to_direction = auto()
    perpendicular_to_direction = auto()
    vertical = auto()
    horizontal = auto()

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

class OutputModifierInputEnum(Enum):
    particle_age = 0
    particle_emit_time = auto()
    particle_random_1 = auto()
    particle_random_2 = auto()
    emitter_age = auto()
    emitter_random_1 = auto()
    emitter_random_2 = auto()
    system_lod = auto()
    game_time = auto()
    effect_a_scale = auto()
    effect_b_scale = auto()
    particle_rotation = auto()
    explosion_animation = auto()
    explosion_rotation = auto()
    particle_random_3 = auto()
    particle_random_4 = auto()
    location_random = auto()

class OutputModifierEnum(Enum):
    none = 0
    plus = auto()
    times = auto()

class CoordinateSystemEnum(Enum):
    world = 0
    local = auto()
    parent = auto()

class CameraModeEnum(Enum):
    independent_of_camera_mode = 0
    only_in_first_person = auto()
    only_in_third_person = auto()
    both_first_and_third = auto()

class AttachedParticleSystemFlags(Flag):
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

class ParticleAsset():
    def __init__(self):
        self.header = None
        self.particle_body_header = None
        self.particle_body = None
        self.parameters_header = None
        self.parameters = None
        self.locations_header = None
        self.locations = None
        self.attached_particle_systems_header = None
        self.attached_particle_systems = None
        self.shader_postprocess_definitions_header = None
        self.shader_postprocess_definitions = None

    class ParticleBody:
        def __init__(self, flags=0, particle_billboard_style=0, first_sequence_index=0, sequence_count=0, shader_template=None, parameters_tag_block=None, properties=None, 
                     collision_effect=None, death_effect=None, locations_tag_block=None, attached_particle_systems_tag_block=None, shader_postprocess_definitions_tag_block=None):
            self.flags = flags
            self.particle_billboard_style = particle_billboard_style
            self.first_sequence_index = first_sequence_index
            self.sequence_count = sequence_count
            self.shader_template = shader_template
            self.parameters_tag_block = parameters_tag_block
            self.properties = properties
            self.collision_effect = collision_effect
            self.death_effect = death_effect
            self.locations_tag_block = locations_tag_block
            self.attached_particle_systems_tag_block = attached_particle_systems_tag_block
            self.shader_postprocess_definitions_tag_block = shader_postprocess_definitions_tag_block

    class Location:
        def __init__(self, name="", name_length=0):
            self.name = name
            self.name_length = name_length

    class AttachedParticleSystem:
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
