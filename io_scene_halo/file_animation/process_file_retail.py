# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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

from math import degrees, sqrt
from mathutils import Vector, Quaternion, Euler
from ..global_functions.tag_format import TagAsset
from .format_retail import AnimationAsset, AnimationFlags

DEBUG_PARSER = False
DEBUG_HEADER = True
DEBUG_BODY = True
DEBUG_OBJECTS = True
DEBUG_UNITS = True
DEBUG_UNITS_ANIMATIONS = True
DEBUG_UNITS_IK_POINTS = True
DEBUG_UNITS_WEAPONS = True
DEBUG_WEAPONS_ANIMATIONS = True
DEBUG_WEAPONS_IK_POINTS = True
DEBUG_WEAPONS_TYPES = True
DEBUG_WEAPONS_TYPES_ANIMATIONS = True
DEBUG_WEAPONS = True
DEBUG_WEAPON_ANIMATIONS = True
DEBUG_VEHICLE = True
DEBUG_VEHICLE_ANIMATIONS = True
DEBUG_VEHICLE_SUSPENSION_ANIMATIONS = True
DEBUG_DEVICES = True
DEBUG_DEVICE_ANIMATIONS = True
DEBUG_UNIT_DAMAGES = True
DEBUG_FIRST_PERSON_WEAPONS = True
DEBUG_FIRST_PERSON_WEAPON_ANIMATIONS = True
DEBUG_SOUND_REFERENCES = True
DEBUG_NODES = True
DEBUG_ANIMATIONS= True
DEBUG_FRAMES = True

def get_anim_flags(anim):
    rot_flags   = anim.rot_flags0   | (anim.rot_flags1 << 32)
    trans_flags = anim.trans_flags0 | (anim.trans_flags1 << 32)
    scale_flags = anim.scale_flags0 | (anim.scale_flags1 << 32)

    rot_flags   = [bool(rot_flags   & (1 << i)) for i in range(anim.node_count)]
    trans_flags = [bool(trans_flags & (1 << i)) for i in range(anim.node_count)]
    scale_flags = [bool(scale_flags & (1 << i)) for i in range(anim.node_count)]
    return rot_flags, trans_flags, scale_flags

def deserialize_frame_info(anim, input_stream, include_extra_base_frame=False):
    dx = dy = dz = dyaw = x = y = z = yaw = 0.0

    root_node_info = [AnimationAsset.FrameTransform() for i in range(anim.frame_count)]

    # write to the data
    if anim.frame_info_type == 3:
        for f in range(anim.frame_count):
            dx, dy, dz, dyaw = struct.unpack('>ffff', input_stream.read(16))
            dx *= 100; dy *= 100; dz *= 100

            info = root_node_info[f]

            info.translation = Vector((x, y, z))
            info.yaw = yaw
            info.delta = (dx, dy, dz, dyaw)

            x += dx; y += dy; z += dz; yaw += dyaw

    elif anim.frame_info_type == 2:
        for f in range(anim.frame_count):
            dx, dy, dyaw = struct.unpack('>fff', input_stream.read(12))
            dx *= 100; dy *= 100

            info = root_node_info[f]

            info.translation = Vector((x, y, 0.0))
            info.yaw = yaw
            info.delta = (dx, dy, 0.0, dyaw)

            x += dx; y += dy; yaw += dyaw

    elif anim.frame_info_type == 1:
        for f in range(anim.frame_count):
            dx, dy = struct.unpack('>ff', input_stream.read(8))
            dx *= 100; dy *= 100

            info = root_node_info[f]
            info.translation = Vector((x, y, 0.0))
            info.delta = (dx, dy, 0.0, 0.0)

            x += dx; y += dy

    if include_extra_base_frame and root_node_info:
        # duplicate the last frame and apply the change
        # that frame to the total change at that frame.

        duped_frame = AnimationAsset.FrameTransform()
        duped_frame.delta = root_node_info[-1].delta
        duped_frame.rotation = root_node_info[-1].rotation
        duped_frame.translation = root_node_info[-1].translation
        duped_frame.scale = root_node_info[-1].scale
        duped_frame.yaw = root_node_info[-1].yaw

        duped_frame.translation = Vector((duped_frame.translation[0] + duped_frame.delta[0], duped_frame.translation[1] + duped_frame.delta[1] , duped_frame.translation[2] + duped_frame.delta[2]))
        duped_frame.yaw += duped_frame.delta[3]

        # no delta on last frame. zero it out
        duped_frame.delta = (0.0, 0.0, 0.0, 0.0)

        root_node_info.append(duped_frame)


    return root_node_info

def _deserialize_frame_data(anim, input_stream, get_default_data, def_node_states, endian):
    rot_flags, trans_flags, scale_flags = get_anim_flags(anim)

    if get_default_data:
        store = False
        stored_frame_count = 1
    else:
        store = True
        stored_frame_count = anim.frame_count

    all_node_states = [[AnimationAsset.FrameTransform() for n in range(anim.node_count)]
                       for f in range(stored_frame_count)]

    if get_default_data:
        def_node_states = all_node_states[0]

    assert len(def_node_states) == anim.node_count

    for f in range(stored_frame_count):
        node_states = all_node_states[f]

        for n in range(anim.node_count):
            def_node_state = def_node_states[n]
            state = node_states[n]

            qi = qj = qk = x = y = z = 0.0
            qw = scale = 1.0
            if rot_flags[n] == store:
                qi, qj, qk, qw = struct.unpack('>hhhh', input_stream.read(8))

                rot_len = qi**2 + qj**2 + qk**2 + qw**2
                if rot_len:
                    rot_len = 1 / sqrt(rot_len)
                    qi *= rot_len
                    qj *= rot_len
                    qk *= rot_len
                    qw *= rot_len
                else:
                    qi = qj = qk = 0.0
                    qw = 1.0
            else:
                qi = def_node_state.rotation[1]
                qj = def_node_state.rotation[2]
                qk = def_node_state.rotation[3]
                qw = def_node_state.rotation[0]

            if trans_flags[n] == store:
                x, y, z = struct.unpack('>fff', input_stream.read(12))
                x *= 100
                y *= 100
                z *= 100
            else:
                x = def_node_state.translation[0]
                y = def_node_state.translation[1]
                z = def_node_state.translation[2]

            if scale_flags[n] == store:
                scale = struct.unpack('>f', input_stream.read(4))
                scale = scale[0]
            else:
                scale = def_node_state.scale

            state.translation = Vector((x, y, z))
            state.rotation = Quaternion((qw, qi, qj, qk))
            state.scale = scale

    return all_node_states

def deserialize_default_data(anim, input_stream, endian=">"):
    return _deserialize_frame_data(anim, input_stream, True, (), endian)[0]

def deserialize_frame_data(anim, input_stream, def_node_states=None, include_extra_base_frame=False, endian=">"):
    if def_node_states is None:
        def_node_states = deserialize_default_data(anim, input_stream, endian)

    frame_data = _deserialize_frame_data(anim, input_stream, False, def_node_states, endian)

    if not include_extra_base_frame:
        pass
    if anim.type != 1:
        # duplicate the first frame to the last frame for non-overlays
        duplicate_frame = []
        for transforms in frame_data[0]:
            duplicate_node = AnimationAsset.FrameTransform()
            duplicate_node.delta = transforms.delta
            duplicate_node.rotation = transforms.rotation
            duplicate_node.translation = transforms.translation
            duplicate_node.scale = transforms.scale
            duplicate_node.yaw = transforms.yaw
            duplicate_frame.append(duplicate_node)

        frame_data.append(duplicate_frame)
    else:
        # overlay animations start with frame 0 being
        # in the same state as the default node states
        frame_data.insert(0, def_node_states)

    return frame_data

def apply_root_node_info_to_states(anim, undo=False):
    if anim.frame_info_applied == (not undo):
        # do nothing if the root node info is already applied
        # and we are being told to apply it, or its not applied
        # and we are being told to undo its application.
        return

    if anim.frame_info_type != 0:
        delta = -1 if undo else 1
        for f in range(anim.frame_count + 1):
            # apply the total change in the root nodes
            # frame_info for this frame to the frame_data
            node_info = anim.frame_info[f]
            node_state = anim.frame_data[f][0]

            matrix0 = Euler((0, 0, -node_info.yaw * delta)).to_quaternion().normalized().to_matrix()
            matrix1 = node_state.rotation.normalized().to_matrix()

            final_rotation = (matrix0 @ matrix1).to_quaternion().normalized()
            final_translation = node_info.translation * delta

            anim.frame_data[f][0].rotation = final_rotation
            anim.frame_data[f][0].translation = final_translation + anim.frame_data[f][0].translation

    anim.frame_info_applied = not undo

def process_file_retail(input_stream, report):
    TAG = TagAsset()
    ANIMATION = AnimationAsset()

    header_struct = struct.unpack('>hbb32s4sIIIIHbb4s', input_stream.read(64))
    ANIMATION.header = TAG.Header()
    ANIMATION.header.unk1 = header_struct[0]
    ANIMATION.header.flags = header_struct[1]
    ANIMATION.header.type = header_struct[2]
    ANIMATION.header.name = header_struct[3].decode().rstrip('\x00')
    ANIMATION.header.tag_group = header_struct[4].decode().rstrip('\x00')
    ANIMATION.header.checksum = header_struct[5]
    ANIMATION.header.data_offset = header_struct[6]
    ANIMATION.header.data_length = header_struct[7]
    ANIMATION.header.unk2 = header_struct[8]
    ANIMATION.header.version = header_struct[9]
    ANIMATION.header.destination = header_struct[10]
    ANIMATION.header.plugin_handle = header_struct[11]
    ANIMATION.header.engine_tag = header_struct[12].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_HEADER:
        print(" ===== Tag Header ===== ")
        print("Unknown Value: ", ANIMATION.header.unk1)
        print("Flags: ", ANIMATION.header.flags)
        print("Type: ", ANIMATION.header.type)
        print("Name: ", ANIMATION.header.name)
        print("Tag Group: ", ANIMATION.header.tag_group)
        print("Checksum: ", ANIMATION.header.checksum)
        print("Data Offset: ", ANIMATION.header.data_offset)
        print("Data Length:", ANIMATION.header.data_length)
        print("Unknown Value: ", ANIMATION.header.unk2)
        print("Version: ", ANIMATION.header.version)
        print("Destination: ", ANIMATION.header.destination)
        print("Plugin Handle: ", ANIMATION.header.plugin_handle)
        print("Engine Tag: ", ANIMATION.header.engine_tag)
        print(" ")

    body_struct = struct.unpack('>iIIiIIiIIiIIiIIiIIiIIiIIfh2xiIIiII', input_stream.read(128))
    ANIMATION.antr_body = ANIMATION.AntrBody()
    ANIMATION.antr_body.objects_tag_block = TAG.TagBlock(body_struct[0], 4, body_struct[1], body_struct[2])
    ANIMATION.antr_body.units_tag_block = TAG.TagBlock(body_struct[3], 32, body_struct[4], body_struct[5])
    ANIMATION.antr_body.weapons_tag_block = TAG.TagBlock(body_struct[6], 1, body_struct[7], body_struct[8])
    ANIMATION.antr_body.vehicles_tag_block = TAG.TagBlock(body_struct[9], 1, body_struct[10], body_struct[11])
    ANIMATION.antr_body.devices_tag_block = TAG.TagBlock(body_struct[12], 1, body_struct[13], body_struct[14])
    ANIMATION.antr_body.unit_damage_tag_block = TAG.TagBlock(body_struct[15], 176, body_struct[16], body_struct[17])
    ANIMATION.antr_body.first_person_weapons_tag_block = TAG.TagBlock(body_struct[18], 1, body_struct[19], body_struct[20])
    ANIMATION.antr_body.sound_references_tag_block = TAG.TagBlock(body_struct[21], 257, body_struct[22], body_struct[23])
    ANIMATION.antr_body.limp_body_node_radius = body_struct[24]
    ANIMATION.antr_body.flags = body_struct[25]
    ANIMATION.antr_body.nodes_tag_block = TAG.TagBlock(body_struct[26], 64, body_struct[27], body_struct[28])
    ANIMATION.antr_body.animations_tag_block = TAG.TagBlock(body_struct[29], 256, body_struct[30], body_struct[31])

    if DEBUG_PARSER and DEBUG_BODY:
        print(" ===== Antr Body ===== ")
        print("Objects Tag Block Count: ", ANIMATION.antr_body.objects_tag_block.count)
        print("Objects Tag Block Maximum Count: ", ANIMATION.antr_body.objects_tag_block.maximum_count)
        print("Objects Tag Block Address: ", ANIMATION.antr_body.objects_tag_block.address)
        print("Objects Tag Block Definition: ", ANIMATION.antr_body.objects_tag_block.definition)
        print("Units Tag Block Count: ", ANIMATION.antr_body.units_tag_block.count)
        print("Units Tag Block Maximum Count: ", ANIMATION.antr_body.units_tag_block.maximum_count)
        print("Units Tag Block Address: ", ANIMATION.antr_body.units_tag_block.address)
        print("Units Tag Block Definition: ", ANIMATION.antr_body.units_tag_block.definition)
        print("Weapons Tag Block Count: ", ANIMATION.antr_body.weapons_tag_block.count)
        print("Weapons Tag Block Maximum Count: ", ANIMATION.antr_body.weapons_tag_block.maximum_count)
        print("Weapons Tag Block Address: ", ANIMATION.antr_body.weapons_tag_block.address)
        print("Weapons Tag Block Definition: ", ANIMATION.antr_body.weapons_tag_block.definition)
        print("Vehicle Tag Block Count: ", ANIMATION.antr_body.vehicles_tag_block.count)
        print("Vehicle Tag Block Maximum Count: ", ANIMATION.antr_body.vehicles_tag_block.maximum_count)
        print("Vehicle Tag Block Address: ", ANIMATION.antr_body.vehicles_tag_block.address)
        print("Vehicle Tag Block Definition: ", ANIMATION.antr_body.vehicles_tag_block.definition)
        print("Devices Tag Block Count: ", ANIMATION.antr_body.devices_tag_block.count)
        print("Devices Tag Block Maximum Count: ", ANIMATION.antr_body.devices_tag_block.maximum_count)
        print("Devices Tag Block Address: ", ANIMATION.antr_body.devices_tag_block.address)
        print("Devices Tag Block Definition: ", ANIMATION.antr_body.devices_tag_block.definition)
        print("Unit Damage Tag Block Count: ", ANIMATION.antr_body.unit_damage_tag_block.count)
        print("Unit Damage Tag Block Maximum Count: ", ANIMATION.antr_body.unit_damage_tag_block.maximum_count)
        print("Unit Damage Tag Block Address: ", ANIMATION.antr_body.unit_damage_tag_block.address)
        print("Unit Damage Tag Block Definition: ", ANIMATION.antr_body.unit_damage_tag_block.definition)
        print("First Person Weapons Tag Block Count: ", ANIMATION.antr_body.first_person_weapons_tag_block.count)
        print("First Person Weapons Tag Block Maximum Count: ", ANIMATION.antr_body.first_person_weapons_tag_block.maximum_count)
        print("First Person Weapons Tag Block Address: ", ANIMATION.antr_body.first_person_weapons_tag_block.address)
        print("First Person Weapons Tag Block Definition: ", ANIMATION.antr_body.first_person_weapons_tag_block.definition)
        print("Sound References Tag Block Count: ", ANIMATION.antr_body.sound_references_tag_block.count)
        print("Sound References Tag Block Maximum Count: ", ANIMATION.antr_body.sound_references_tag_block.maximum_count)
        print("Sound References Tag Block Address: ", ANIMATION.antr_body.sound_references_tag_block.address)
        print("Sound References Tag Block Definition: ", ANIMATION.antr_body.sound_references_tag_block.definition)
        print("Limp Body Node Radius: ", ANIMATION.antr_body.limp_body_node_radius)
        print("Flags: ", ANIMATION.antr_body.flags)
        print("Nodes Tag Block Count: ", ANIMATION.antr_body.nodes_tag_block.count)
        print("Nodes Tag Block Maximum Count: ", ANIMATION.antr_body.nodes_tag_block.maximum_count)
        print("Nodes Tag Block Address: ", ANIMATION.antr_body.nodes_tag_block.address)
        print("Nodes Tag Block Definition: ", ANIMATION.antr_body.nodes_tag_block.definition)
        print("Animations Tag Block Count: ", ANIMATION.antr_body.animations_tag_block.count)
        print("Animations Tag Block Maximum Count: ", ANIMATION.antr_body.animations_tag_block.maximum_count)
        print("Animations Tag Block Address: ", ANIMATION.antr_body.animations_tag_block.address)
        print("Animations Tag Block Definition: ", ANIMATION.antr_body.animations_tag_block.definition)
        print(" ")

    for objects_idx in range(ANIMATION.antr_body.objects_tag_block.count):
        object_struct = struct.unpack('>hhh14x', input_stream.read(20))
        object = ANIMATION.Objects()
        object.animation = object_struct[0]
        object.function = object_struct[1]
        object.function_controls = object_struct[2]

        ANIMATION.objects.append(object)

    if DEBUG_PARSER and DEBUG_OBJECTS:
        print(" ===== Objects ===== ")
        for objects_idx, object in enumerate(ANIMATION.objects):
            print(" ===== Object %s ===== " % objects_idx)
            print("Animation: ", object.animation)
            print("Function: ", object.function)
            print("Function Controls: ", object.function_controls)
            print(" ")

    for unit_idx in range(ANIMATION.antr_body.units_tag_block.count):
        unit_struct = struct.unpack('>32sffhhffhh8xiIIiIIiII', input_stream.read(100))
        unit = ANIMATION.AnimationBehavior()
        unit.label = unit_struct[0].decode().rstrip('\x00')
        unit.right_yaw_per_frame = degrees(unit_struct[1])
        unit.left_yaw_per_frame = degrees(unit_struct[2])
        unit.right_frame_count = unit_struct[3]
        unit.left_frame_count = unit_struct[4]
        unit.down_pitch_per_frame = degrees(unit_struct[5])
        unit.up_pitch_per_frame = degrees(unit_struct[6])
        unit.down_pitch_frame_count = unit_struct[7]
        unit.up_pitch_frame_count = unit_struct[8]
        unit.animations_tag_block = TAG.TagBlock(unit_struct[9], 30, unit_struct[10], unit_struct[11])
        unit.ik_points_tag_block = TAG.TagBlock(unit_struct[12], 4, unit_struct[13], unit_struct[14])
        unit.weapons_tag_block = TAG.TagBlock(unit_struct[15], 16, unit_struct[16], unit_struct[17])

        ANIMATION.units.append(unit)

    for unit in ANIMATION.units:
        unit_animation_indices = []
        unit_ik_points = []
        unit_weapons = []
        for unit_animation_idx in range(unit.animations_tag_block.count):
            unit_animation = struct.unpack('>h', input_stream.read(2))

            unit_animation_indices.append(unit_animation[0])

        for unit_ik_point_idx in range(unit.ik_points_tag_block.count):
            ik_point_struct = struct.unpack('>32s32s', input_stream.read(64))
            ik_point = ANIMATION.IKPoints()
            ik_point.marker = ik_point_struct[0].decode().rstrip('\x00')
            ik_point.attach_to_marker = ik_point_struct[1].decode().rstrip('\x00')

            unit_ik_points.append(ik_point)

        for unit_weapon_idx in range(unit.weapons_tag_block.count):
            weapon_type_struct = struct.unpack('>32s32s32sffhhffhh32xiIIiIIiII', input_stream.read(188))
            weapon_type = ANIMATION.AnimationBehavior()
            weapon_type.label = weapon_type_struct[0].decode().rstrip('\x00')
            weapon_type.grip_marker = weapon_type_struct[1].decode().rstrip('\x00')
            weapon_type.hand_marker = weapon_type_struct[2].decode().rstrip('\x00')
            weapon_type.right_yaw_per_frame = degrees(weapon_type_struct[3])
            weapon_type.left_yaw_per_frame = degrees(weapon_type_struct[4])
            weapon_type.right_frame_count = weapon_type_struct[5]
            weapon_type.left_frame_count = weapon_type_struct[6]
            weapon_type.down_pitch_per_frame = degrees(weapon_type_struct[7])
            weapon_type.up_pitch_per_frame = degrees(weapon_type_struct[8])
            weapon_type.down_pitch_frame_count = weapon_type_struct[9]
            weapon_type.up_pitch_frame_count = weapon_type_struct[10]
            weapon_type.animations_tag_block = TAG.TagBlock(weapon_type_struct[11], 55, weapon_type_struct[12], weapon_type_struct[13])
            weapon_type.ik_points_tag_block = TAG.TagBlock(weapon_type_struct[14], 4, weapon_type_struct[15], weapon_type_struct[16])
            weapon_type.weapons_tag_block = TAG.TagBlock(weapon_type_struct[17], 10, weapon_type_struct[18], weapon_type_struct[19])

            unit_weapons.append(weapon_type)

        for unit_weapon in unit_weapons:
            weapon_type_animation_indices = []
            weapon_type_ik_points = []
            weapon_type_weapons = []
            for weapon_animation_idx in range(unit_weapon.animations_tag_block.count):
                animation = struct.unpack('>h', input_stream.read(2))
                weapon_type_animation_indices.append(animation[0])

            for weapon_ik_point_idx in range(unit_weapon.ik_points_tag_block.count):
                ik_point_struct = struct.unpack('>32s32s', input_stream.read(64))
                ik_point = ANIMATION.IKPoints()
                ik_point.marker = ik_point_struct[0].decode().rstrip('\x00')
                ik_point.attach_to_marker = ik_point_struct[1].decode().rstrip('\x00')

                weapon_type_ik_points.append(ik_point)

            for weapon_type_idx in range(unit_weapon.weapons_tag_block.count):
                weapon_type_struct = struct.unpack('>32s16xiII', input_stream.read(60))
                weapon_type = ANIMATION.AnimationBehavior()
                weapon_type.label = weapon_type_struct[0].decode().rstrip('\x00')
                weapon_type.animations_tag_block = TAG.TagBlock(weapon_type_struct[1], 10, weapon_type_struct[2], weapon_type_struct[3])

                weapon_type_weapons.append(weapon_type)

            for weapon_type in weapon_type_weapons:
                animation_indices = []
                for weapon_type_animation_idx in range(weapon_type.animations_tag_block.count):
                    animation = struct.unpack('>h', input_stream.read(2))

                    animation_indices.append(animation[0])

                weapon_type.animations = animation_indices

            unit_weapon.animations = weapon_type_animation_indices
            unit_weapon.ik_points = weapon_type_ik_points
            unit_weapon.weapons = weapon_type_weapons

        unit.animations = unit_animation_indices
        unit.ik_points = unit_ik_points
        unit.weapons = unit_weapons

    if DEBUG_PARSER and DEBUG_UNITS:
        print(" ===== Units ===== ")
        for unit_idx, unit in enumerate(ANIMATION.units):
            print(" ===== Unit %s ===== " % unit_idx)
            print("Label: ", unit.label)
            print("Right Yaw Per Frame: ", unit.right_yaw_per_frame)
            print("Left Yaw Per Frame: ", unit.left_yaw_per_frame)
            print("Right Frame Count: ", unit.right_frame_count)
            print("Left Frame Count: ", unit.left_frame_count)
            print("Down Pitch Per Frame: ", unit.down_pitch_per_frame)
            print("Up Pitch Per Frame: ", unit.up_pitch_per_frame)
            print("Down Pitch Frame Count: ", unit.down_pitch_frame_count)
            print("Up Pitch Frame_Count: ", unit.up_pitch_frame_count)
            print("Unit Animations Tag Block Count: ", unit.animations_tag_block.count)
            print("Unit Animations Tag Block Maximum Count: ", unit.animations_tag_block.maximum_count)
            print("Unit Animations Tag Block Address: ", unit.animations_tag_block.address)
            print("Unit Animations Tag Block Definition: ", unit.animations_tag_block.definition)
            print("IK Points Tag Block Count: ", unit.ik_points_tag_block.count)
            print("IK Points Tag Block Maximum Count: ", unit.ik_points_tag_block.maximum_count)
            print("IK Points Tag Block Address: ", unit.ik_points_tag_block.address)
            print("IK Points Tag Block Definition: ", unit.ik_points_tag_block.definition)
            print("Weapons Tag Block Count: ", unit.weapons_tag_block.count)
            print("Weapons Tag Block Maximum Count: ", unit.weapons_tag_block.maximum_count)
            print("Weapons Tag Block Address: ", unit.weapons_tag_block.address)
            print("Weapons Tag Block Definition: ", unit.weapons_tag_block.definition)
            print(" ")
            if DEBUG_UNITS_ANIMATIONS:
                for animation_idx, animation in enumerate(unit.animations):
                    print(" ===== Animation %s ===== " % animation_idx)
                    print("Animation Index: ", animation)
                    print(" ")

            if DEBUG_UNITS_IK_POINTS:
                for ik_point_idx, ik_point in enumerate(unit.ik_points):
                    print(" ===== IK Point %s ===== " % ik_point_idx)
                    print("IK Point Marker: ", ik_point.marker)
                    print("IK Point Attach to Marker: ", ik_point.attach_to_marker)
                    print(" ")

            if DEBUG_UNITS_WEAPONS:
                for weapon_idx, weapon in enumerate(unit.weapons):
                    print(" ===== Weapon %s ===== " % weapon_idx)
                    print("Name: ", weapon.label)
                    print("Grip Marker: ", weapon.grip_marker)
                    print("Hand Marker: ", weapon.hand_marker)
                    print("Right Yaw Per Frame: ", weapon.right_yaw_per_frame)
                    print("Left Yaw Per Frame: ", weapon.left_yaw_per_frame)
                    print("Right Frame Count: ", weapon.right_frame_count)
                    print("Left Frame Count: ", weapon.left_frame_count)
                    print("Down Pitch Per Frame: ", weapon.down_pitch_per_frame)
                    print("Up Pitch Per Frame: ", weapon.up_pitch_per_frame)
                    print("Down Pitch Frame Count: ", weapon.down_pitch_frame_count)
                    print("Up Pitch Frame_Count: ", weapon.up_pitch_frame_count)
                    print("Weapon Type Animations Tag Block Count: ", weapon.animations_tag_block.count)
                    print("Weapon Type Animations Tag Block Maximum Count: ", weapon.animations_tag_block.maximum_count)
                    print("Weapon Type Animations Tag Block Address: ", weapon.animations_tag_block.address)
                    print("Weapon Type Animations Tag Block Definition: ", weapon.animations_tag_block.definition)
                    print("IK Points Tag Block Count: ", weapon.ik_points_tag_block.count)
                    print("IK Points Tag Block Maximum Count: ", weapon.ik_points_tag_block.maximum_count)
                    print("IK Points Tag Block Address: ", weapon.ik_points_tag_block.address)
                    print("IK Points Tag Block Definition: ", weapon.ik_points_tag_block.definition)
                    print("Weapons Tag Block Count: ", weapon.weapons_tag_block.count)
                    print("Weapons Tag Block Maximum Count: ", weapon.weapons_tag_block.maximum_count)
                    print("Weapons Tag Block Address: ", weapon.weapons_tag_block.address)
                    print("Weapons Tag Block Definition: ", weapon.weapons_tag_block.definition)
                    print(" ")

                    if DEBUG_WEAPONS_ANIMATIONS:
                        for animation_idx, animation in enumerate(weapon.animations):
                            print(" ===== Animation %s ===== " % animation_idx)
                            print("Animation Index: ", animation)
                            print(" ")

                    if DEBUG_WEAPONS_IK_POINTS:
                        for ik_point_idx, ik_point in enumerate(weapon.ik_points):
                            print(" ===== IK Point %s ===== " % ik_point_idx)
                            print("IK Point Marker: ", ik_point.marker)
                            print("IK Point Attach to Marker: ", ik_point.attach_to_marker)
                            print(" ")

                    if DEBUG_WEAPONS_TYPES:
                        for weapon_idx, weapon_type in enumerate(weapon.weapons):
                            print(" ===== Weapon Type %s ===== " % weapon_idx)
                            print("Label: ", weapon.label)
                            print(" ")
                            if DEBUG_WEAPONS_TYPES_ANIMATIONS:
                                for weapon_type_animation_idx, weapon_type_animation in enumerate(weapon_type.animations):
                                    print(" ===== Weapon Type Animation %s ===== " % weapon_type_animation_idx)
                                    print("Animation Index: ", weapon_type_animation)
                                    print(" ")

    for weapon_idx in range(ANIMATION.antr_body.weapons_tag_block.count):
        weapon_struct = struct.unpack('>16xiII', input_stream.read(28))
        weapon = ANIMATION.AnimationGroups()
        weapon.animations_tag_block = TAG.TagBlock(weapon_struct[0], 11, weapon_struct[1], weapon_struct[2])

        ANIMATION.weapons.append(weapon)

    for weapon in ANIMATION.weapons:
        animation_indices = []
        for weapon_animation_idx in range(weapon.animations_tag_block.count):
            animation = struct.unpack('>h', input_stream.read(2))

            animation_indices.append(animation[0])

        weapon.animations = animation_indices

    if DEBUG_PARSER and DEBUG_WEAPONS:
        print(" ===== Weapons ===== ")
        for weapon_idx, weapon in enumerate(ANIMATION.weapons):
            print(" ===== Weapon %s ===== " % weapon_idx)
            print("Weapons Tag Block Count: ", weapon.animations_tag_block.count)
            print("Weapons Tag Block Maximum Count: ", weapon.animations_tag_block.maximum_count)
            print("Weapons Tag Block Address: ", weapon.animations_tag_block.address)
            print("Weapons Tag Block Definition: ", weapon.animations_tag_block.definition)
            print(" ")
            if DEBUG_WEAPON_ANIMATIONS:
                for animation_idx, animation in enumerate(weapon.animations):
                    print(" ===== Animation %s ===== " % animation_idx)
                    print("Animation Index: ", animation)
                    print(" ")

    for vehicle_idx in range(ANIMATION.antr_body.vehicles_tag_block.count):
        vehicle_struct = struct.unpack('>ffhhffhh68xiIIiII', input_stream.read(116))
        vehicle = ANIMATION.AnimationGroups()
        vehicle.right_yaw_per_frame = degrees(vehicle_struct[0])
        vehicle.left_yaw_per_frame = degrees(vehicle_struct[1])
        vehicle.right_frame_count = vehicle_struct[2]
        vehicle.left_frame_count = vehicle_struct[3]
        vehicle.down_pitch_per_frame = degrees(vehicle_struct[4])
        vehicle.up_pitch_per_frame =  degrees(vehicle_struct[5])
        vehicle.down_pitch_frame_count = vehicle_struct[6]
        vehicle.up_pitch_frame_count = vehicle_struct[7]
        vehicle.animations_tag_block = TAG.TagBlock(vehicle_struct[8], 8, vehicle_struct[9], vehicle_struct[10])
        vehicle.suspension_animations_tag_block = TAG.TagBlock(vehicle_struct[11], 8, vehicle_struct[12], vehicle_struct[13])

        ANIMATION.vehicles.append(vehicle)

    for vehicle in ANIMATION.vehicles:
        animation_indices = []
        suspension_animations = []
        for vehicle_animation_idx in range(vehicle.animations_tag_block.count):
            animation = struct.unpack('>h', input_stream.read(2))

            animation_indices.append(animation[0])

        for vehicle_suspension_animation_idx in range(vehicle.suspension_animations_tag_block.count):
            vehicle_suspension_struct = struct.unpack('>hhff8x', input_stream.read(20))
            vehicle_suspension = ANIMATION.AnimationSuspension()
            vehicle_suspension.mass_point_index = vehicle_suspension_struct[0]
            vehicle_suspension.animation = vehicle_suspension_struct[1]
            vehicle_suspension.full_extension_ground_depth = vehicle_suspension_struct[2]
            vehicle_suspension.full_compression_ground_depth = vehicle_suspension_struct[3]

            suspension_animations.append(vehicle_suspension)

        vehicle.animations = animation_indices
        vehicle.suspension_animations = suspension_animations

    if DEBUG_PARSER and DEBUG_VEHICLE:
        print(" ===== Vehicles ===== ")
        for vehicle_idx, vehicle in enumerate(ANIMATION.vehicles):
            print(" ===== Vehicle %s ===== " % vehicle_idx)
            print("Right Yaw Per Frame: ", vehicle.right_yaw_per_frame)
            print("Left Yaw Per Frame: ", vehicle.left_yaw_per_frame)
            print("Right Frame Count: ", vehicle.right_frame_count)
            print("Left Frame Count: ", vehicle.left_frame_count)
            print("Down Pitch Per Frame: ", vehicle.down_pitch_per_frame)
            print("Up Pitch Per Frame: ", vehicle.up_pitch_per_frame)
            print("Down Pitch Frame Count: ", vehicle.down_pitch_frame_count)
            print("Up Pitch Frame_Count: ", vehicle.up_pitch_frame_count)
            print("Animations Tag Block Count: ", vehicle.animations_tag_block.count)
            print("Animations Tag Block Maximum Count: ", vehicle.animations_tag_block.maximum_count)
            print("Animations Tag Block Address: ", vehicle.animations_tag_block.address)
            print("Animations Tag Block Definition: ", vehicle.animations_tag_block.definition)
            print("Suspension Animations Tag Block Count: ", vehicle.suspension_animations_tag_block.count)
            print("Suspension Animations Tag Block Maximum Count: ", vehicle.suspension_animations_tag_block.maximum_count)
            print("Suspension Animations Tag Block Address: ", vehicle.suspension_animations_tag_block.address)
            print("Suspension Animations Tag Block Definition: ", vehicle.suspension_animations_tag_block.definition)
            print(" ")
            if DEBUG_VEHICLE_ANIMATIONS:
                for animation_idx, animation in enumerate(vehicle.animations):
                    print(" ===== Animation %s ===== " % animation_idx)
                    print("Animation Index: ", animation)
                    print(" ")

            if DEBUG_VEHICLE_SUSPENSION_ANIMATIONS:
                for suspension_animation_idx, suspension_animation in enumerate(vehicle.suspension_animations):
                    print(" ===== Suspension Animation %s ===== " % suspension_animation_idx)
                    print("Mass Point Index: ", suspension_animation.mass_point_index)
                    print("Suspension Animation Index: ", suspension_animation.animation)
                    print("full Extension Ground Depth: ", suspension_animation.full_extension_ground_depth)
                    print("Full Compression Ground Depth: ", suspension_animation.full_compression_ground_depth)
                    print(" ")

    for devices_idx in range(ANIMATION.antr_body.devices_tag_block.count):
        device_struct = struct.unpack('>84xiII', input_stream.read(96))
        device = ANIMATION.AnimationGroups()
        device.animations_tag_block = TAG.TagBlock(device_struct[0], 2, device_struct[1], device_struct[2])

        ANIMATION.devices.append(device)

    for device in ANIMATION.devices:
        animation_indices = []
        for device_animation_idx in range(device.animations_tag_block.count):
            animation = struct.unpack('>h', input_stream.read(2))

            animation_indices.append(animation[0])

        device.animations = animation_indices

    if DEBUG_PARSER and DEBUG_DEVICES:
        print(" ===== Devices ===== ")
        for device_idx, device in enumerate(ANIMATION.devices):
            print(" ===== Device %s ===== " % device_idx)
            print("Animation Tag Block Count: ", device.animations_tag_block.count)
            print("Animation Tag Block Maximum Count: ", device.animations_tag_block.maximum_count)
            print("Animation Tag Block Address: ", device.animations_tag_block.address)
            print("Animation Tag Block Definition: ", device.animations_tag_block.definition)
            print(" ")
            if DEBUG_DEVICE_ANIMATIONS:
                for animation_idx, animation in enumerate(device.animations):
                    print(" ===== Animation %s ===== " % animation_idx)
                    print("Animation Index: ", animation)
                    print(" ")

    animation_indices = []
    for unit_damage_idx in range(ANIMATION.antr_body.unit_damage_tag_block.count):
        animation = struct.unpack('>h', input_stream.read(2))

        animation_indices.append(animation[0])

    ANIMATION.unit_damages = animation_indices

    if DEBUG_PARSER and DEBUG_UNIT_DAMAGES:
        print(" ===== Unit Damages ===== ")
        for unit_damage_idx, unit_damage in enumerate(ANIMATION.unit_damages):
            print(" ===== Unit Damage %s ===== " % unit_damage_idx)
            print("Animation Index: ", unit_damage)
            print(" ")

    for first_person_weapons_idx in range(ANIMATION.antr_body.first_person_weapons_tag_block.count):
        first_person_struct = struct.unpack('>16xiII', input_stream.read(28))
        first_person = ANIMATION.AnimationGroups()
        first_person.animations_tag_block = TAG.TagBlock(first_person_struct[0], 28, first_person_struct[1], first_person_struct[2])

        ANIMATION.first_person_weapons.append(first_person)

    for first_person_weapon in ANIMATION.first_person_weapons:
        animation_indices = []
        for first_person_weapon_animation_idx in range(first_person_weapon.animations_tag_block.count):
            animation = struct.unpack('>h', input_stream.read(2))

            animation_indices.append(animation[0])

        first_person_weapon.animations = animation_indices

    if DEBUG_PARSER and DEBUG_FIRST_PERSON_WEAPONS:
        print(" ===== First Person Weapons ===== ")
        for first_person_weapon_idx, first_person_weapon in enumerate(ANIMATION.first_person_weapons):
            print(" ===== First Person Weapon %s ===== " % first_person_weapon_idx)
            print("Animation Tag Block Count: ", first_person_weapon.animations_tag_block.count)
            print("Animation Tag Block Maximum Count: ", first_person_weapon.animations_tag_block.maximum_count)
            print("Animation Tag Block Address: ", first_person_weapon.animations_tag_block.address)
            print("Animation Tag Block Definition: ", first_person_weapon.animations_tag_block.definition)
            print(" ")
            if DEBUG_FIRST_PERSON_WEAPON_ANIMATIONS:
                for animation_idx, animation in enumerate(first_person_weapon.animations):
                    print(" ===== Animation %s ===== " % animation_idx)
                    print("Animation Index: ", animation)
                    print(" ")

    for sound_reference_idx in range(ANIMATION.antr_body.sound_references_tag_block.count):
        sound_struct  = struct.unpack('>4siiI4x', input_stream.read(20))

        ANIMATION.sound_references.append(TAG.TagRef(sound_struct[0].decode().rstrip('\x00'), "", sound_struct[2] + 1, sound_struct[1], sound_struct[3]))

    for sound_reference in ANIMATION.sound_references:
        tag_path = struct.unpack('>%ss' % sound_reference.name_length, input_stream.read(sound_reference.name_length))
        sound_reference.name = tag_path[0].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_SOUND_REFERENCES:
        print(" ===== Sound References ===== ")
        for sound_reference_idx, sound_reference in enumerate(ANIMATION.sound_references):
            print(" ===== Sound Reference %s ===== " % sound_reference_idx)
            print("Tag Reference Group: ", sound_reference.tag_group)
            print("Tag Reference Name: ", sound_reference.name)
            print("Tag Reference Length: ", sound_reference.name_length)
            print("Tag Reference Salt: ", sound_reference.salt)
            print("Tag Reference Index: ", sound_reference.index)
            print(" ")

    for node_idx in range(ANIMATION.antr_body.nodes_tag_block.count):
        node_struct = struct.unpack('>32shhh2xiffff4x', input_stream.read(64))
        node = ANIMATION.Nodes()
        node.name = node_struct[0].decode().rstrip('\x00')
        node.sibling = node_struct[1]
        node.child = node_struct[2]
        node.parent = node_struct[3]
        node.flags = node_struct[4]
        node.base_vector = Vector((node_struct[5], node_struct[6], node_struct[7])) * 100
        node.vector_range = node_struct[8] * 100

        ANIMATION.nodes.append(node)

    if DEBUG_PARSER and DEBUG_NODES:
        print(" ===== Nodes ===== ")
        for node_idx, node in enumerate(ANIMATION.nodes):
            print(" ===== Node %s ===== " % node_idx)
            print("Name: ", node.name)
            print("Sibling Index: ", node.sibling)
            print("Child Index: ", node.child)
            print("Parent Index: ", node.parent)
            print("Flags: ", node.flags)
            print("Base Vector: ", node.base_vector)
            print("Vector Range: ", node.vector_range)
            print(" ")

    for animation_idx in range(ANIMATION.antr_body.animations_tag_block.count):
        animation_struct  = struct.unpack('>32shhhhihhfhhhhhhbbhfiiIIIII8xII8xII4xiiiIIIiiIII', input_stream.read(180))
        animation = ANIMATION.Animation()
        animation.name = animation_struct[0].decode().rstrip('\x00')
        animation.type = animation_struct[1]
        animation.frame_count = animation_struct[2]
        animation.frame_size = animation_struct[3]
        animation.frame_info_type = animation_struct[4]
        animation.node_list_checksum = animation_struct[5]
        animation.node_count = animation_struct[6]
        animation.loop_frame_index = animation_struct[7]
        animation.weight = animation_struct[8]
        animation.key_frame_index = animation_struct[9]
        animation.second_key_frame_index = animation_struct[10]
        animation.next_animation = animation_struct[11]
        animation.flags = animation_struct[12]
        animation.sound = animation_struct[13]
        animation.sound_frame_index = animation_struct[14]
        animation.left_foot_frame_index = animation_struct[15]
        animation.right_foot_frame_index = animation_struct[16]
        animation.first_permutation_index = animation_struct[17]
        animation.chance_to_play = animation_struct[18]
        animation.frame_info = TAG.RawData(animation_struct[19], animation_struct[20], animation_struct[21], animation_struct[22], animation_struct[23])
        animation.trans_flags0 = animation_struct[24]
        animation.trans_flags1 = animation_struct[25]
        animation.rot_flags0 = animation_struct[26]
        animation.rot_flags1 = animation_struct[27]
        animation.scale_flags0 = animation_struct[28]
        animation.scale_flags1 = animation_struct[29]
        animation.offset_to_compressed_data = animation_struct[30]
        animation.default_data = TAG.RawData(animation_struct[31], animation_struct[32], animation_struct[33], animation_struct[34], animation_struct[35])
        animation.frame_data = TAG.RawData(animation_struct[36], animation_struct[37], animation_struct[38], animation_struct[39], animation_struct[40])

        ANIMATION.animations.append(animation)

    if DEBUG_PARSER and DEBUG_ANIMATIONS:
        print(" ===== Animations ===== ")
        for animation_idx, animation in enumerate(ANIMATION.animations):
            print(" ===== Animation %s ===== " % animation_idx)
            print("Name: ", animation.name)
            print("Type: ", animation.type)
            print("Frame Count: ", animation.frame_count)
            print("Frame Size: ", animation.frame_size)
            print("Frame Info Type: ", animation.frame_info_type)
            print("Node List Checksum: ", animation.node_list_checksum)
            print("Node Count: ", animation.node_count)
            print("Loop Frame Index: ", animation.loop_frame_index)
            print("Weight: ", animation.weight)
            print("Key Frame Index: ", animation.key_frame_index)
            print("Second Key Frame Index: ", animation.second_key_frame_index)
            print("Next Animation: ", animation.next_animation)
            print("Flags: ", animation.flags)
            print("Sound: ", animation.sound)
            print("Sound Frame Index: ", animation.sound_frame_index)
            print("Left Foot Frame Index: ", animation.left_foot_frame_index)
            print("Right Foot Frame Index: ", animation.right_foot_frame_index)
            print("First Permutation Index: ", animation.first_permutation_index)
            print("Chance To Play: ", animation.chance_to_play)
            print("Frame Info Size: ", animation.frame_info.size)
            print("Frame Info Flags: ", animation.frame_info.flags)
            print("Frame Info Raw Pointer: ", animation.frame_info.raw_pointer)
            print("Frame Info Pointer: ", animation.frame_info.pointer)
            print("Frame Info ID: ", animation.frame_info.id)
            print("Translation Flag 0: ", animation.trans_flags0)
            print("Translation Flag 1: ", animation.trans_flags1)
            print("Rotation Flag 0: ", animation.rot_flags0)
            print("Rotation Flag 1: ", animation.rot_flags1)
            print("Scale Flag 0: ", animation.scale_flags0)
            print("Scale Flag 1: ", animation.scale_flags1)
            print("Offset To Compressed Data: ", animation.offset_to_compressed_data)
            print("Default Data Size: ", animation.default_data.size)
            print("Default Data Flags: ", animation.default_data.flags)
            print("Default Data Raw Pointer: ", animation.default_data.raw_pointer)
            print("Default Data Pointer: ", animation.default_data.pointer)
            print("Default Data ID: ", animation.default_data.id)
            print("Frame Data Size: ", animation.frame_data.size)
            print("Frame Data Flags: ", animation.frame_data.flags)
            print("Frame Data Raw Pointer: ", animation.frame_data.raw_pointer)
            print("Frame Data Pointer: ", animation.frame_data.pointer)
            print("Frame Data ID: ", animation.frame_data.id)
            print(" ")

    for animation in ANIMATION.animations:
        # sum the frame info changes for each frame from the frame_info
        animation.frame_info = deserialize_frame_info(animation, input_stream, True)

        if AnimationFlags.Compressed_Data in AnimationFlags(animation.flags):
            raise Exception("Not Implmented")
            # decompress compressed animations
            #keyframes, animation.frame_data = deserialize_compressed_frame_data(animation)
            #jma_anim.rot_keyframes   = keyframes[0]
            #jma_anim.trans_keyframes = keyframes[1]
            #jma_anim.scale_keyframes = keyframes[2]

        else:
            # create the node states from the frame_data and default_data
            animation.frame_data = deserialize_frame_data(animation, input_stream, None, True)

        if animation.type != 1:
            # this is set to True on instantiation.
            # Set it to False since we had to provide root node info
            animation.frame_info_applied = False
            apply_root_node_info_to_states(animation)

    if DEBUG_PARSER and DEBUG_FRAMES:
        print(" ===== Frames ===== ")
        for animation_idx, animation in enumerate(ANIMATION.animations):
            print(" ===== Animation %s ===== " % animation_idx)
            for transform_idx, transform in enumerate(animation.frame_data):
                print(" ===== Frame %s ===== " % transform_idx)
                for node_idx, node in enumerate(transform):
                    print(" ===== Node %s ===== " % node_idx)
                    print("Rotation: ", node.rotation)
                    print("Translation: ", node.translation)
                    print("Scale: ", node.scale)
                    print(" ")

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    return ANIMATION
