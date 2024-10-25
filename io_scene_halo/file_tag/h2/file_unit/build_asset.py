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
from ..file_object.build_asset import write_tag_ref

def write_postures(output_stream, TAG, postures, postures_header):
    if len(postures) > 0:
        postures_header.write(output_stream, TAG, True)
        for posture_element in postures:
            output_stream.write(struct.pack('>I', len(posture_element.name)))
            output_stream.write(struct.pack('<fff', *posture_element.pill_offset))

        for posture_element in postures:
            name_length = len(posture_element.name)
            if name_length > 0:
                output_stream.write(struct.pack('<%ss' % name_length, TAG.string_to_bytes(posture_element.name, False)))

def write_dialogue_variant(output_stream, TAG, dialogue_variants, dialogue_variants_header):
    if len(dialogue_variants) > 0:
        dialogue_variants_header.write(output_stream, TAG, True)
        for dialogue_variant_element in dialogue_variants:
            output_stream.write(struct.pack('<h', dialogue_variant_element.variant_number))
            output_stream.write(struct.pack('<2x'))
            dialogue_variant_element.dialogue.write(output_stream, False, True)

        for dialogue_variant_element in dialogue_variants:
            dialogue_length = len(dialogue_variant_element.dialogue.name)
            if dialogue_length > 0:
                output_stream.write(struct.pack('<%ssx' % dialogue_length, TAG.string_to_bytes(dialogue_variant_element.dialogue.name, False)))

def write_powered_seats(output_stream, TAG, powered_seats, powered_seats_header):
    if len(powered_seats) > 0:
        powered_seats_header.write(output_stream, TAG, True)
        for powered_seat_element in powered_seats:
            output_stream.write(struct.pack('<f', powered_seat_element.driver_powerup_time))
            output_stream.write(struct.pack('<f', powered_seat_element.driver_powerdown_time))

def write_seats(output_stream, TAG, seats, seats_header):
    if len(seats) > 0:
        seats_header.write(output_stream, TAG, True)
        for seat_element in seats:
            output_stream.write(struct.pack('<I', seat_element.flags))
            output_stream.write(struct.pack('>I', len(seat_element.label)))
            output_stream.write(struct.pack('>I', len(seat_element.marker_name)))
            output_stream.write(struct.pack('>I', len(seat_element.entry_marker_name)))
            output_stream.write(struct.pack('>I', len(seat_element.boarding_grenade_marker)))
            output_stream.write(struct.pack('>I', len(seat_element.boarding_grenade_string)))
            output_stream.write(struct.pack('>I', len(seat_element.boarding_melee_string)))
            output_stream.write(struct.pack('<f', seat_element.ping_scale))
            output_stream.write(struct.pack('<f', seat_element.turnover_time))
            output_stream.write(struct.pack('<fff', *seat_element.acceleration_range))
            output_stream.write(struct.pack('<f', seat_element.acceleration_action_scale))
            output_stream.write(struct.pack('<f', seat_element.acceleration_attach_scale))
            output_stream.write(struct.pack('<f', seat_element.ai_scariness))
            output_stream.write(struct.pack('<H', seat_element.ai_seat_type))
            output_stream.write(struct.pack('<h', seat_element.boarding_seat))
            output_stream.write(struct.pack('<f', seat_element.listener_interpolation_factor))
            output_stream.write(struct.pack('<ff', *seat_element.yaw_rate_bounds))
            output_stream.write(struct.pack('<ff', *seat_element.pitch_rate_bounds))
            output_stream.write(struct.pack('<f', seat_element.min_speed_reference))
            output_stream.write(struct.pack('<f', seat_element.max_speed_reference))
            output_stream.write(struct.pack('<f', seat_element.speed_exponent))
            output_stream.write(struct.pack('>I', len(seat_element.camera_marker_name)))
            output_stream.write(struct.pack('>I', len(seat_element.camera_submerged_marker_name)))
            output_stream.write(struct.pack('<f', radians(seat_element.pitch_auto_level)))
            output_stream.write(struct.pack('<ff', radians(seat_element.pitch_range[0]), radians(seat_element.pitch_range[1])))
            seat_element.camera_tracks_tag_block.write(output_stream, False)
            seat_element.unit_hud_interface_tag_block.write(output_stream, False)
            output_stream.write(struct.pack('>I', len(seat_element.enter_seat_string)))
            output_stream.write(struct.pack('<f', radians(seat_element.yaw_minimum)))
            output_stream.write(struct.pack('<f', radians(seat_element.yaw_maximum)))
            seat_element.built_in_gunner.write(output_stream, False, True)
            output_stream.write(struct.pack('<f', seat_element.entry_radius))
            output_stream.write(struct.pack('<f', radians(seat_element.entry_marker_cone_angle)))
            output_stream.write(struct.pack('<f', radians(seat_element.entry_marker_facing_angle)))
            output_stream.write(struct.pack('<f', seat_element.maximum_relative_velocity))
            output_stream.write(struct.pack('>I', len(seat_element.invisible_seat_region)))
            output_stream.write(struct.pack('<i', seat_element.runtime_invisible_seat_region_index))

        for seat_element in seats:
            label_length = len(seat_element.label)
            if label_length > 0:
                output_stream.write(struct.pack('<%ss' % label_length, TAG.string_to_bytes(seat_element.label, False)))

            marker_name_length = len(seat_element.marker_name)
            if marker_name_length > 0:
                output_stream.write(struct.pack('<%ss' % marker_name_length, TAG.string_to_bytes(seat_element.marker_name, False)))

            entry_marker_name_length = len(seat_element.entry_marker_name)
            if entry_marker_name_length > 0:
                output_stream.write(struct.pack('<%ss' % entry_marker_name_length, TAG.string_to_bytes(seat_element.entry_marker_name, False)))

            boarding_grenade_marker_length = len(seat_element.boarding_grenade_marker)
            if boarding_grenade_marker_length > 0:
                output_stream.write(struct.pack('<%ss' % boarding_grenade_marker_length, TAG.string_to_bytes(seat_element.boarding_grenade_marker, False)))

            boarding_grenade_string_length = len(seat_element.boarding_grenade_string)
            if boarding_grenade_string_length > 0:
                output_stream.write(struct.pack('<%ss' % boarding_grenade_string_length, TAG.string_to_bytes(seat_element.boarding_grenade_string, False)))

            boarding_melee_string_length = len(seat_element.boarding_melee_string)
            if boarding_melee_string_length > 0:
                output_stream.write(struct.pack('<%ss' % boarding_melee_string_length, TAG.string_to_bytes(seat_element.boarding_melee_string, False)))

            output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("usas", True), 0, 1, 20))
            output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("uncs", True), 0, 1, 32))

            camera_marker_name_length = len(seat_element.camera_marker_name)
            if camera_marker_name_length > 0:
                output_stream.write(struct.pack('<%ss' % camera_marker_name_length, TAG.string_to_bytes(seat_element.camera_marker_name, False)))

            camera_submerged_marker_name_length = len(seat_element.camera_submerged_marker_name)
            if camera_submerged_marker_name_length > 0:
                output_stream.write(struct.pack('<%ss' % camera_submerged_marker_name_length, TAG.string_to_bytes(seat_element.camera_submerged_marker_name, False)))

            write_tag_ref(output_stream, TAG, seat_element.camera_tracks, seat_element.camera_tracks_header)
            write_tag_ref(output_stream, TAG, seat_element.unit_hud_interface, seat_element.unit_hud_interface_header)

            enter_seat_string_length = len(seat_element.enter_seat_string)
            if enter_seat_string_length > 0:
                output_stream.write(struct.pack('<%ss' % enter_seat_string_length, TAG.string_to_bytes(seat_element.enter_seat_string, False)))

            built_in_gunner_length = len(seat_element.built_in_gunner.name)
            if built_in_gunner_length > 0:
                output_stream.write(struct.pack('<%ssx' % built_in_gunner_length, TAG.string_to_bytes(seat_element.built_in_gunner.name, False)))

            invisible_seat_region_length = len(seat_element.invisible_seat_region)
            if invisible_seat_region_length > 0:
                output_stream.write(struct.pack('<%ss' % invisible_seat_region_length, TAG.string_to_bytes(seat_element.invisible_seat_region, False)))
