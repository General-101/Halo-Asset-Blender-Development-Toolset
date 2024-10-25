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
from mathutils import Vector, Quaternion

class AnimationTagFlags(Flag):
    compress_all_animations = auto()
    force_idle_compression = auto()

class FunctionEnum(Enum):
    a_out = 0
    b_out = auto()
    c_out = auto()
    d_out = auto()

class FunctionControlsEnum(Enum):
    frame = 0
    scale = auto()

class NodeJointFlags(Flag):
    ball_socket = auto()
    hinge = auto()
    no_movement = auto()

class AnimationTypeEnum(Enum):
    base = 0
    overlay = auto()
    replacement = auto()

class AnimationFrameInfoTypeEnum(Enum):
    none = 0
    dx_dy = auto()
    dx_dy_dyaw = auto()
    dx_dy_dz_dyaw = auto()

class AnimationFlags(Flag):
    compressed_data = auto()
    world_relative = auto()
    pal_25hz = auto()

class AnimationAsset():
    def __init__(self, header=None, objects=None, units=None, weapons=None, vehicles=None, devices=None, unit_damages=None, first_person_weapons=None, sound_references=None, 
                 nodes=None, animations=None, objects_tag_block=None, units_tag_block=None, weapons_tag_block=None, vehicles_tag_block=None, devices_tag_block=None, 
                 unit_damage_tag_block=None, first_person_weapons_tag_block=None, sound_references_tag_block=None, limp_body_node_radius=0.0, flags=0, nodes_tag_block=None, 
                 animations_tag_block=None):
        self.header = header
        self.objects = objects
        self.units = units
        self.weapons = weapons
        self.vehicles = vehicles
        self.devices = devices
        self.unit_damages = unit_damages
        self.first_person_weapons = first_person_weapons
        self.sound_references = sound_references
        self.nodes = nodes
        self.animations = animations
        self.objects_tag_block = objects_tag_block
        self.units_tag_block = units_tag_block
        self.weapons_tag_block = weapons_tag_block
        self.vehicles_tag_block = vehicles_tag_block
        self.devices_tag_block = devices_tag_block
        self.unit_damage_tag_block = unit_damage_tag_block
        self.first_person_weapons_tag_block = first_person_weapons_tag_block
        self.sound_references_tag_block = sound_references_tag_block
        self.limp_body_node_radius = limp_body_node_radius
        self.flags = flags
        self.nodes_tag_block = nodes_tag_block
        self.animations_tag_block = animations_tag_block

    class Objects:
        def __init__(self, animation=0, function=0, function_controls=0):
            self.animation = animation
            self.function = function
            self.function_controls = function_controls

    class AnimationBehavior:
        def __init__(self, label="", grip_marker="", hand_marker="", right_yaw_per_frame=0, left_yaw_per_frame=0, right_frame_count=0, left_frame_count=0, down_pitch_per_frame=0, up_pitch_per_frame=0,
                     down_pitch_frame_count=0, up_pitch_frame_count=0, animations_tag_block=None, ik_points_tag_block=None, weapons_tag_block=None, animations=None,
                     ik_points=None, weapons=None):
            self.label = label
            self.grip_marker = grip_marker
            self.hand_marker = hand_marker
            self.right_yaw_per_frame = right_yaw_per_frame
            self.left_yaw_per_frame = left_yaw_per_frame
            self.right_frame_count = right_frame_count
            self.left_frame_count = left_frame_count
            self.down_pitch_per_frame = down_pitch_per_frame
            self.up_pitch_per_frame = up_pitch_per_frame
            self.down_pitch_frame_count = down_pitch_frame_count
            self.up_pitch_frame_count = up_pitch_frame_count
            self.animations_tag_block = animations_tag_block
            self.ik_points_tag_block = ik_points_tag_block
            self.weapons_tag_block = weapons_tag_block
            self.animations = animations
            self.ik_points = ik_points
            self.weapons = weapons

    class IKPoints:
        def __init__(self, marker="", attach_to_marker=""):
            self.marker = marker
            self.attach_to_marker = attach_to_marker

    class AnimationGroups:
        def __init__(self, label="", right_yaw_per_frame=0.0, left_yaw_per_frame=0.0, right_frame_count=0, left_frame_count=0, down_pitch_per_frame=0.0, up_pitch_per_frame=0.0,
                     down_pitch_frame_count=0, up_pitch_frame_count=0, animations_tag_block=None, suspension_animations_tag_block=None, animations=None,
                     suspension_animations=None):
            self.label = label
            self.right_yaw_per_frame = right_yaw_per_frame
            self.left_yaw_per_frame = left_yaw_per_frame
            self.right_frame_count = right_frame_count
            self.left_frame_count = left_frame_count
            self.down_pitch_per_frame = down_pitch_per_frame
            self.up_pitch_per_frame = up_pitch_per_frame
            self.down_pitch_frame_count = down_pitch_frame_count
            self.up_pitch_frame_count = up_pitch_frame_count
            self.animations_tag_block = animations_tag_block
            self.suspension_animations_tag_block = suspension_animations_tag_block
            self.animations = animations
            self.suspension_animations = suspension_animations

    class AnimationSuspension:
        def __init__(self, mass_point_index=0, animation=0, full_extension_ground_depth=0.0, full_compression_ground_depth=0.0):
            self.mass_point_index = mass_point_index
            self.animation = animation
            self.full_extension_ground_depth = full_extension_ground_depth
            self.full_compression_ground_depth = full_compression_ground_depth

    class Nodes:
        def __init__(self, name="", sibling=0, child=0, parent=0, flags=0, base_vector=Vector(), vector_range=0.0):
            self.name = name
            self.sibling = sibling
            self.child = child
            self.parent = parent
            self.flags = flags
            self.base_vector = base_vector
            self.vector_range = vector_range

    class Animation:
        def __init__(self, name="", type=0, frame_count=0, frame_size=0, frame_info_type=0, node_list_checksum=0, node_count=0, loop_frame_index=0, weight=0.0,
                     key_frame_index=0, second_key_frame_index=0, next_animation=0, flags=0, sound=0, sound_frame_index=0, left_foot_frame_index=0, right_foot_frame_index=0,
                     first_permutation_index=0, chance_to_play=0.0, frame_info_tag_data=None, trans_flags0=0, trans_flags1=0, rot_flags0=0, rot_flags1=0, scale_flags0=0,
                     scale_flags1=0, offset_to_compressed_data=0, default_data_tag_data=None, frame_data_tag_data=None, frame_info=None, default_data=None, frame_data=None,
                     frame_info_applied=False):
            self.name = name
            self.type = type
            self.frame_count = frame_count
            self.frame_size = frame_size
            self.frame_info_type = frame_info_type
            self.node_list_checksum = node_list_checksum
            self.node_count = node_count
            self.loop_frame_index = loop_frame_index
            self.weight = weight
            self.key_frame_index = key_frame_index
            self.second_key_frame_index = second_key_frame_index
            self.next_animation = next_animation
            self.flags = flags
            self.sound = sound
            self.sound_frame_index = sound_frame_index
            self.left_foot_frame_index = left_foot_frame_index
            self.right_foot_frame_index = right_foot_frame_index
            self.first_permutation_index = first_permutation_index
            self.chance_to_play = chance_to_play
            self.frame_info_tag_data = frame_info_tag_data
            self.trans_flags0 = trans_flags0
            self.trans_flags1 = trans_flags1
            self.rot_flags0 = rot_flags0
            self.rot_flags1 = rot_flags1
            self.scale_flags0 = scale_flags0
            self.scale_flags1 = scale_flags1
            self.offset_to_compressed_data = offset_to_compressed_data
            self.default_data_tag_data = default_data_tag_data
            self.frame_data_tag_data = frame_data_tag_data
            self.frame_info = frame_info
            self.default_data = default_data
            self.frame_data = frame_data
            self.frame_info_applied = frame_info_applied

    class FrameTransform:
        def __init__(self, delta= (0.0, 0.0, 0.0, 0.0),  rotation=Quaternion(), translation=Vector(), scale=1.0, yaw=0.0):
            self.delta = delta
            self.rotation = rotation
            self.translation = translation
            self.scale = scale
            self.yaw = yaw
