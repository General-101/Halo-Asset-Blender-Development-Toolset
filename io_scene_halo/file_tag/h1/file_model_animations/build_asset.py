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

import struct

from math import radians

def write_body(output_stream, ANIMATION):
    ANIMATION.antr_body.objects_tag_block.write(output_stream, True)
    ANIMATION.antr_body.units_tag_block.write(output_stream, True)
    ANIMATION.antr_body.weapons_tag_block.write(output_stream, True)
    ANIMATION.antr_body.vehicles_tag_block.write(output_stream, True)
    ANIMATION.antr_body.devices_tag_block.write(output_stream, True)
    ANIMATION.antr_body.unit_damage_tag_block.write(output_stream, True)
    ANIMATION.antr_body.first_person_weapons_tag_block.write(output_stream, True)
    ANIMATION.antr_body.sound_references_tag_block.write(output_stream, True)
    output_stream.write(struct.pack('>f', ANIMATION.antr_body.limp_body_node_radius))
    output_stream.write(struct.pack('>H',ANIMATION.antr_body.flags))
    output_stream.write(struct.pack('>2x'))
    ANIMATION.antr_body.nodes_tag_block.write(output_stream, True)
    ANIMATION.antr_body.animations_tag_block.write(output_stream, True)

def write_objects(output_stream, ANIMATION):
    for object_element in ANIMATION.objects:
        output_stream.write(struct.pack('>H', object_element.animation))
        output_stream.write(struct.pack('>H', object_element.function))
        output_stream.write(struct.pack('>H', object_element.function_controls))
        output_stream.write(struct.pack('>14x'))

def write_units(output_stream, ANIMATION, TAG):
    for unit in ANIMATION.units:
        output_stream.write(struct.pack('>31sx', TAG.string_to_bytes(unit.label, False)))
        output_stream.write(struct.pack('>f', radians(unit.right_yaw_per_frame)))
        output_stream.write(struct.pack('>f', radians(unit.left_yaw_per_frame)))
        output_stream.write(struct.pack('>h', unit.right_frame_count))
        output_stream.write(struct.pack('>h', unit.left_frame_count))
        output_stream.write(struct.pack('>f', radians(unit.down_pitch_per_frame)))
        output_stream.write(struct.pack('>f', radians(unit.up_pitch_per_frame)))
        output_stream.write(struct.pack('>h', unit.down_pitch_frame_count))
        output_stream.write(struct.pack('>h', unit.up_pitch_frame_count))
        output_stream.write(struct.pack('>8x'))
        unit.animations_tag_block.write(output_stream, True)
        unit.ik_points_tag_block.write(output_stream, True)
        unit.weapons_tag_block.write(output_stream, True)

    for unit in ANIMATION.units:
        for unit_animation in unit.animations:
            output_stream.write(struct.pack('>h', unit_animation))

        for unit_ik_point in unit.ik_points:
            output_stream.write(struct.pack('>31sx', TAG.string_to_bytes(unit_ik_point.marker, False)))
            output_stream.write(struct.pack('>31sx', TAG.string_to_bytes(unit_ik_point.attach_to_marker, False)))

        for unit_weapon in unit.weapons:
            output_stream.write(struct.pack('>31sx', TAG.string_to_bytes(unit_weapon.label, False)))
            output_stream.write(struct.pack('>31sx', TAG.string_to_bytes(unit_weapon.grip_marker, False)))
            output_stream.write(struct.pack('>31sx', TAG.string_to_bytes(unit_weapon.hand_marker, False)))
            output_stream.write(struct.pack('>f', radians(unit_weapon.right_yaw_per_frame)))
            output_stream.write(struct.pack('>f', radians(unit_weapon.left_yaw_per_frame)))
            output_stream.write(struct.pack('>h', unit_weapon.right_frame_count))
            output_stream.write(struct.pack('>h', unit_weapon.left_frame_count))
            output_stream.write(struct.pack('>f', radians(unit_weapon.down_pitch_per_frame)))
            output_stream.write(struct.pack('>f', radians(unit_weapon.up_pitch_per_frame)))
            output_stream.write(struct.pack('>h', unit_weapon.down_pitch_frame_count))
            output_stream.write(struct.pack('>h', unit_weapon.up_pitch_frame_count))
            output_stream.write(struct.pack('>32x'))
            unit_weapon.animations_tag_block.write(output_stream, True)
            unit_weapon.ik_points_tag_block.write(output_stream, True)
            unit_weapon.weapons_tag_block.write(output_stream, True)

        for unit_weapon in unit.weapons:
            for weapon_animation in unit_weapon.animations:
                output_stream.write(struct.pack('>h', weapon_animation))

            for weapon_ik_point in unit_weapon.ik_points:
                output_stream.write(struct.pack('>31sx', TAG.string_to_bytes(weapon_ik_point.marker, False)))
                output_stream.write(struct.pack('>31sx', TAG.string_to_bytes(weapon_ik_point.attach_to_marker, False)))

            for weapon_type in unit_weapon.weapons:
                output_stream.write(struct.pack('>31sx', TAG.string_to_bytes(weapon_type.label, False)))
                output_stream.write(struct.pack('>16x'))
                weapon_type.animations_tag_block.write(output_stream, True)

            for weapon_type in unit_weapon.weapons:
                for weapon_type_animation in weapon_type.animations:
                    output_stream.write(struct.pack('>h', weapon_type_animation))

def write_weapons(output_stream, ANIMATION):
    for weapon in ANIMATION.weapons:
        output_stream.write(struct.pack('>16x'))
        weapon.animations_tag_block.write(output_stream, True)

    for weapon in ANIMATION.weapons:
        for weapon_animation in weapon.animations:
            output_stream.write(struct.pack('>h', weapon_animation))

def write_vehicles(output_stream, ANIMATION):
    for vehicle in ANIMATION.vehicles:
        output_stream.write(struct.pack('>f', radians(vehicle.right_yaw_per_frame)))
        output_stream.write(struct.pack('>f', radians(vehicle.left_yaw_per_frame)))
        output_stream.write(struct.pack('>h', vehicle.right_frame_count))
        output_stream.write(struct.pack('>h', vehicle.left_frame_count))
        output_stream.write(struct.pack('>f', radians(vehicle.down_pitch_per_frame)))
        output_stream.write(struct.pack('>f', radians(vehicle.up_pitch_per_frame)))
        output_stream.write(struct.pack('>h', vehicle.down_pitch_frame_count))
        output_stream.write(struct.pack('>h', vehicle.up_pitch_frame_count))
        output_stream.write(struct.pack('>68x'))
        vehicle.animations_tag_block.write(output_stream, True)
        vehicle.suspension_animations_tag_block.write(output_stream, True)

    for vehicle in ANIMATION.vehicles:
        for vehicle_animation in vehicle.animations:
            output_stream.write(struct.pack('>h', vehicle_animation))

        for vehicle_suspension_animation in vehicle.suspension_animations:
            output_stream.write(struct.pack('>h', vehicle_suspension_animation.mass_point_index))
            output_stream.write(struct.pack('>h', vehicle_suspension_animation.animation))
            output_stream.write(struct.pack('>f', vehicle_suspension_animation.full_extension_ground_depth))
            output_stream.write(struct.pack('>f', vehicle_suspension_animation.full_compression_ground_depth))
            output_stream.write(struct.pack('>8x'))

def write_devices(output_stream, ANIMATION):
    for device in ANIMATION.devices:
        output_stream.write(struct.pack('>84x'))
        device.animations_tag_block.write(output_stream, True)

    for device in ANIMATION.devices:
        for device_animation in device.animations:
            output_stream.write(struct.pack('>h', device_animation))

def write_unit_damages(output_stream, ANIMATION):
    for unit_damage in ANIMATION.unit_damages:
        output_stream.write(struct.pack('>h', unit_damage))

def write_first_person_weapons(output_stream, ANIMATION):
    for first_person_weapon in ANIMATION.first_person_weapons:
        output_stream.write(struct.pack('>16x'))
        first_person_weapon.animations_tag_block.write(output_stream, True)

    for first_person_weapon in ANIMATION.first_person_weapons:
        for first_person_weapon_animation in first_person_weapon.animations:
            output_stream.write(struct.pack('>h', first_person_weapon_animation))

def write_sound_references(output_stream, ANIMATION, TAG):
    for sound_reference in ANIMATION.sound_references:
        sound_reference.write(output_stream, True)
        output_stream.write(struct.pack('>4x'))

    for sound_reference in ANIMATION.sound_references:
        output_stream.write(struct.pack('>%ssx' % len(sound_reference.name), TAG.string_to_bytes(sound_reference.name, False)))

def write_nodes(output_stream, ANIMATION, TAG):
    for node in ANIMATION.nodes:
        output_stream.write(struct.pack('>31sx', TAG.string_to_bytes(node.name, False)))
        output_stream.write(struct.pack('>h', node.sibling))
        output_stream.write(struct.pack('>h', node.child))
        output_stream.write(struct.pack('>h', node.parent))
        output_stream.write(struct.pack('>2x'))
        output_stream.write(struct.pack('>I', node.flags))
        output_stream.write(struct.pack('>fff', node.base_vector[0], node.base_vector[1], node.base_vector[2]))
        output_stream.write(struct.pack('>f', node.vector_range))
        output_stream.write(struct.pack('>4x'))

def write_animations(output_stream, ANIMATION, TAG):
    for animation in ANIMATION.animations:
        output_stream.write(struct.pack('>31sx', TAG.string_to_bytes(animation.name, False)))
        output_stream.write(struct.pack('>H', animation.type))
        output_stream.write(struct.pack('>h', animation.frame_count))
        output_stream.write(struct.pack('>h', animation.frame_size))
        output_stream.write(struct.pack('>H', animation.frame_info_type))
        output_stream.write(struct.pack('>i', animation.node_list_checksum))
        output_stream.write(struct.pack('>h', animation.node_count))
        output_stream.write(struct.pack('>h', animation.loop_frame_index))
        output_stream.write(struct.pack('>f', animation.weight))
        output_stream.write(struct.pack('>h', animation.key_frame_index))
        output_stream.write(struct.pack('>h', animation.second_key_frame_index))
        output_stream.write(struct.pack('>h', animation.next_animation))
        output_stream.write(struct.pack('>h', animation.flags))
        output_stream.write(struct.pack('>h', animation.sound))
        output_stream.write(struct.pack('>h', animation.sound_frame_index))
        output_stream.write(struct.pack('>b', animation.left_foot_frame_index))
        output_stream.write(struct.pack('>b', animation.right_foot_frame_index))
        output_stream.write(struct.pack('>h', animation.first_permutation_index))
        output_stream.write(struct.pack('>f', animation.chance_to_play))
        animation.frame_info_tag_data.write(output_stream, True)
        output_stream.write(struct.pack('>I', animation.trans_flags0))
        output_stream.write(struct.pack('>I', animation.trans_flags1))
        output_stream.write(struct.pack('>8x'))
        output_stream.write(struct.pack('>I', animation.rot_flags0))
        output_stream.write(struct.pack('>I', animation.rot_flags1))
        output_stream.write(struct.pack('>8x'))
        output_stream.write(struct.pack('>I', animation.scale_flags0))
        output_stream.write(struct.pack('>I', animation.scale_flags1))
        output_stream.write(struct.pack('>4x'))
        output_stream.write(struct.pack('>i', animation.offset_to_compressed_data))
        animation.default_data_tag_data.write(output_stream, True)
        animation.frame_data_tag_data.write(output_stream, True)

    for animation in ANIMATION.animations:
        output_stream.write(animation.frame_info_tag_data.data)
        output_stream.write(animation.default_data_tag_data.data)
        output_stream.write(animation.frame_data_tag_data.data)

def build_asset(output_stream, ANIMATION, TAG, report):
    ANIMATION.header.write(output_stream, True)
    write_body(output_stream, ANIMATION)

    write_objects(output_stream, ANIMATION)
    write_units(output_stream, ANIMATION, TAG)
    write_weapons(output_stream, ANIMATION)
    write_vehicles(output_stream, ANIMATION)
    write_devices(output_stream, ANIMATION)
    write_unit_damages(output_stream, ANIMATION)
    write_first_person_weapons(output_stream, ANIMATION)
    write_sound_references(output_stream, ANIMATION, TAG)
    write_nodes(output_stream, ANIMATION, TAG)
    write_animations(output_stream, ANIMATION, TAG)
