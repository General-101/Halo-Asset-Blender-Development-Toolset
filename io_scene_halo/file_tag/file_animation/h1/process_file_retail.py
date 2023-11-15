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

import io
import bpy
import copy
import struct
import binascii

from xml.dom import minidom
from math import degrees, sqrt
from mathutils import Vector, Matrix, Quaternion, Euler
from .format_retail import AnimationAsset, AnimationTagFlags, FunctionEnum, FunctionControlsEnum, NodeJointFlags, AnimationTypeEnum, AnimationFrameInfoTypeEnum, AnimationFlags

XML_OUTPUT = False
XML_RAW_DATA_OUTPUT = False

def get_anim_flags(anim):
    rot_flags   = anim.rot_flags0 | anim.rot_flags1 << 32
    trans_flags = anim.trans_flags0 | anim.trans_flags1 << 32
    scale_flags = anim.scale_flags0 | anim.scale_flags1 << 32

    rot_flags   = [bool(rot_flags   & (1 << i)) for i in range(anim.node_count)]
    trans_flags = [bool(trans_flags & (1 << i)) for i in range(anim.node_count)]
    scale_flags = [bool(scale_flags & (1 << i)) for i in range(anim.node_count)]

    return rot_flags, trans_flags, scale_flags

def deserialize_frame_info(frame_info, frame_info_node, ANIMATION, animation_element, TAG, tag_format):
    dx = dy = dz = dyaw = x = y = z = yaw = 0.0

    root_node_info = []

    # write to the data
    if AnimationFrameInfoTypeEnum(animation_element.frame_info_type) == AnimationFrameInfoTypeEnum.dx_dy_dz_dyaw:
        for frame_idx in range(animation_element.frame_count):
            frame_element_node = None
            if XML_RAW_DATA_OUTPUT:
                frame_element_node = TAG.xml_doc.createElement('element')
                frame_element_node.setAttribute('index', str(frame_idx))
                frame_info_node.appendChild(frame_element_node)

            info = ANIMATION.FrameTransform()

            dx = TAG.read_float(frame_info, TAG, tag_format.XMLData(frame_element_node, "dx"), True)
            dy = TAG.read_float(frame_info, TAG, tag_format.XMLData(frame_element_node, "dy"), True)
            dz = TAG.read_float(frame_info, TAG, tag_format.XMLData(frame_element_node, "dz"), True)
            dyaw = TAG.read_float(frame_info, TAG, tag_format.XMLData(frame_element_node, "dyaw"))

            info.translation = Vector((x, y, z))
            info.yaw = yaw
            info.delta = (dx, dy, dz, dyaw)

            x += dx
            y += dy
            z += dz
            yaw += dyaw

            root_node_info.append(info)

    elif AnimationFrameInfoTypeEnum(animation_element.frame_info_type) == AnimationFrameInfoTypeEnum.dx_dy_dyaw:
        for frame_idx in range(animation_element.frame_count):
            frame_element_node = None
            if XML_RAW_DATA_OUTPUT:
                frame_element_node = TAG.xml_doc.createElement('element')
                frame_element_node.setAttribute('index', str(frame_idx))
                frame_info_node.appendChild(frame_element_node)

            info = ANIMATION.FrameTransform()

            dx = TAG.read_float(frame_info, TAG, tag_format.XMLData(frame_element_node, "dx"), True)
            dy = TAG.read_float(frame_info, TAG, tag_format.XMLData(frame_element_node, "dy"), True)
            dyaw = TAG.read_float(frame_info, TAG, tag_format.XMLData(frame_element_node, "dyaw"))

            info.translation = Vector((x, y, 0.0))
            info.yaw = yaw
            info.delta = (dx, dy, 0.0, dyaw)

            x += dx
            y += dy
            yaw += dyaw

            root_node_info.append(info)

    elif AnimationFrameInfoTypeEnum(animation_element.frame_info_type) == AnimationFrameInfoTypeEnum.dx_dy:
        for frame_idx in range(animation_element.frame_count):
            frame_element_node = None
            if XML_RAW_DATA_OUTPUT:
                frame_element_node = TAG.xml_doc.createElement('element')
                frame_element_node.setAttribute('index', str(frame_idx))
                frame_info_node.appendChild(frame_element_node)

            info = ANIMATION.FrameTransform()

            dx = TAG.read_float(frame_info, TAG, tag_format.XMLData(frame_element_node, "dx"), True)
            dy = TAG.read_float(frame_info, TAG, tag_format.XMLData(frame_element_node, "dy"), True)

            info.translation = Vector((x, y, 0.0))
            info.delta = (dx, dy, 0.0, 0.0)

            x += dx
            y += dy

            root_node_info.append(info)

    else:
        for frame_idx in range(animation_element.frame_count):
            info = ANIMATION.FrameTransform()

            root_node_info.append(info)

    if root_node_info:
        # duplicate the last frame and apply the change
        # that frame to the total change at that frame.

        duped_frame = copy.deepcopy(root_node_info[-1])

        duped_frame.translation = Vector((duped_frame.translation[0] + duped_frame.delta[0], duped_frame.translation[1] + duped_frame.delta[1] , duped_frame.translation[2] + duped_frame.delta[2]))
        duped_frame.yaw += duped_frame.delta[3]

        # no delta on last frame. zero it out
        duped_frame.delta = (0.0, 0.0, 0.0, 0.0)

        root_node_info.append(duped_frame)


    return root_node_info

def read_animation_data(ANIMATION, animation_element, data_steam, data_node, get_default_data, def_node_states, transforms, TAG, tag_format):
    rot_flags, trans_flags, scale_flags = get_anim_flags(animation_element)

    if get_default_data:
        store = False
        stored_frame_count = 1
    else:
        store = True
        stored_frame_count = animation_element.frame_count

    all_node_states = [[ANIMATION.FrameTransform() for n in range(animation_element.node_count)]
                       for f in range(stored_frame_count)]

    if get_default_data:
        def_node_states = all_node_states[0]

    assert len(def_node_states) == animation_element.node_count

    for frame_idx in range(stored_frame_count):
        frame_element_node = None
        if XML_RAW_DATA_OUTPUT:
            frame_element_node = TAG.xml_doc.createElement('element')
            frame_element_node.setAttribute('index', str(frame_idx))
            data_node.appendChild(frame_element_node)

        node_states = all_node_states[frame_idx]

        for node_idx in range(animation_element.node_count):
            node_element_node = None
            if XML_RAW_DATA_OUTPUT:
                node_element_node = TAG.xml_doc.createElement('element')
                node_element_node.setAttribute('index', str(node_idx))
                frame_element_node.appendChild(node_element_node)

            def_node_state = def_node_states[node_idx]
            state = node_states[node_idx]

            if AnimationTypeEnum(animation_element.type) == AnimationTypeEnum.base:
                if rot_flags[node_idx] == store:
                    rotation = TAG.read_quaternion_squared(data_steam, TAG, tag_format.XMLData(node_element_node, "rotation"))

                else:
                    rotation = def_node_state.rotation

                if trans_flags[node_idx] == store:
                    translation = TAG.read_point_3d(data_steam, TAG, tag_format.XMLData(node_element_node, "translation"), True)

                else:
                    translation = def_node_state.translation


                if scale_flags[node_idx] == store:
                    scale = TAG.read_float(data_steam, TAG, tag_format.XMLData(node_element_node, "scale"))

                else:
                    scale = def_node_state.scale

            else:
                if not transforms == None:
                    pos, rot, sca = transforms[node_idx].decompose()

                else:
                    pos = Vector()
                    rot = Quaternion()
                    sca = 1.0

                original_rotation = def_node_state.rotation
                if rot_flags[node_idx] == store:
                    if not get_default_data:
                        original_rotation = rot

                    rotation = (TAG.read_quaternion_squared(data_steam, TAG, tag_format.XMLData(node_element_node, "rotation")).to_matrix() @ original_rotation.to_matrix()).to_quaternion()

                else:
                    if get_default_data:
                        original_rotation = rot

                    rotation = original_rotation

                original_translation = def_node_state.translation
                if trans_flags[node_idx] == store:
                    if not get_default_data:
                        original_translation = pos

                    translation = original_translation + TAG.read_point_3d(data_steam, TAG, tag_format.XMLData(node_element_node, "translation"), True)

                else:
                    if get_default_data:
                        original_translation = pos

                    translation = original_translation

                original_scale = def_node_state.scale
                if scale_flags[node_idx] == store:
                    if not get_default_data:
                        original_scale = sca

                    scale = TAG.read_float(data_steam, TAG, tag_format.XMLData(node_element_node, "scale"))

                else:
                    if get_default_data:
                        original_scale = sca

                    scale = def_node_state.scale

            state.translation = translation
            state.rotation = rotation
            state.scale = scale

    return all_node_states

def build_frame_data(default_data, frame_data, default_data_node, frame_data_node, ANIMATION, animation_element, transforms, TAG, tag_format):
    def_node_states = read_animation_data(ANIMATION, animation_element, default_data, default_data_node, True, None, transforms, TAG, tag_format)[0]
    frame_data = read_animation_data(ANIMATION, animation_element, frame_data, frame_data_node, False, def_node_states, transforms, TAG, tag_format)

    if not AnimationTypeEnum(animation_element.type) == AnimationTypeEnum.overlay:
        # duplicate the first frame to the last frame for non-overlays
        duplicate_frame = copy.deepcopy(frame_data[0])
        frame_data.append(duplicate_frame)

    else:
        # overlay animations start with frame 0 being
        # in the same state as the default node states
        frame_data.insert(0, def_node_states)

    return frame_data

def apply_root_node_info_to_states(animation_element, undo=False):
    if animation_element.frame_info_applied == (not undo):
        # do nothing if the root node info is already applied
        # and we are being told to apply it, or its not applied
        # and we are being told to undo its application.
        return

    if not AnimationFrameInfoTypeEnum(animation_element.frame_info_type) == AnimationFrameInfoTypeEnum.none:
        delta = -1 if undo else 1
        for frame_idx in range(animation_element.frame_count + 1):
            # apply the total change in the root nodes
            # frame_info for this frame to the frame_data
            node_info = animation_element.frame_info[frame_idx]
            node_state = animation_element.frame_data[frame_idx][0]

            matrix0 = Euler((0, 0, -node_info.yaw * delta)).to_quaternion().normalized().to_matrix()
            matrix1 = node_state.rotation.normalized().to_matrix()

            final_rotation = (matrix0 @ matrix1).to_quaternion().normalized()
            final_translation = node_info.translation * delta

            animation_element.frame_data[frame_idx][0].rotation = final_rotation
            animation_element.frame_data[frame_idx][0].translation = final_translation + animation_element.frame_data[frame_idx][0].translation

    animation_element.frame_info_applied = not undo

def decompress_quaternion48(word_0, word_1, word_2):
    '''Decompress a ones-signed 6byte quaternion to floats'''
    comp_rot = (word_2 & 0xFFff) | ((word_1 & 0xFFff)<<16) | ((word_0 & 0xFFff)<<32)
    w =  comp_rot & 4095
    k = (comp_rot >> 12) & 4095
    j = (comp_rot >> 24) & 4095
    i = (comp_rot >> 36) & 4095
    # avoid division by zero
    if i | j | k | w:
        if i & 0x800: i -= 4095
        if j & 0x800: j -= 4095
        if k & 0x800: k -= 4095
        if w & 0x800: w -= 4095
        length = 1.0 / sqrt(i**2 + j**2 + k**2 + w**2)
        return i * length, j * length, k * length, w * length
    return 0.0, 0.0, 0.0, 1.0

def lerp_blend_vectors(v0, v1, ratio):
    r1 = max(0.0, min(1.0, ratio))
    r0 = 1.0 - r1
    return [a*r0 + b*r1 for a, b in zip(v0, v1)]


def nlerp_blend_quaternions(q0, q1, ratio):
    r1 = max(0.0, min(1.0, ratio))
    r0 = 1.0 - ratio

    i0, j0, k0, w0 = q0
    i1, j1, k1, w1 = q1

    cos_half_theta = i0*i1 + j0*j1 + k0*k1 + w0*w1
    if cos_half_theta < 0:
        # need to change the vector rotations to be 2pi - rot
        r1 = -r1

    return [i0*r0 + i1*r1, j0*r0 + j1*r1, k0*r0 + k1*r1, w0*r0 + w1*r1]

def get_keyframe_index_of_frame(frame, keyframes,
keyframe_count=None, offset=0):
    if keyframe_count is None:
        keyframe_count = len(keyframes) - offset

    # TODO: make this more efficent using a binary search
    for i in range(offset, offset + keyframe_count - 1):
        if keyframes[i] <= frame and frame < keyframes[i + 1]:
            return i

    raise ValueError(
        "No keyframes pairs containing frame %s" % frame)

def deserialize_compressed_frame_data(animation_element, frame_data):
    rot_keyframes_by_nodes = []
    trans_keyframes_by_nodes = []
    scale_keyframes_by_nodes = []

    keyframes = (rot_keyframes_by_nodes,
                 trans_keyframes_by_nodes,
                 scale_keyframes_by_nodes)

    # make a bunch of frames we can fill in below
    frames = [[AnimationAsset.FrameTransform() for n in range(animation_element.node_count)]
              for f in range(animation_element.frame_count + 1)]

    rot_flags, trans_flags, scale_flags = get_anim_flags(animation_element)

    # get the keyframe counts and keyframe offsets
    frame_data.seek(animation_element.offset_to_compressed_data, 0)
    translation_keyframe_offset, scale_keyframe_offset = struct.unpack('<12xI12xI12x', frame_data.read(44))

    data_size = animation_element.frame_data_tag_data.size

    rot_keyframes = []
    trans_keyframes = []
    scale_keyframes = []

    rot_def_data = []
    trans_def_data = []
    scale_def_data = [1.0 for node_idx in range(animation_element.node_count)]

    rot_keyframe_data = []
    trans_keyframe_data = []
    scale_keyframe_data = []

    rot_keyframe_headers   = []
    trans_keyframe_headers = []
    scale_keyframe_headers = []

    rotation_offset = animation_element.offset_to_compressed_data + 44
    if data_size > rotation_offset:
        frame_data.seek(rotation_offset, 0)
        for node_idx in range(animation_element.node_count):
            if rot_flags[node_idx] == True:
                rotation_keyframe_count = struct.unpack('<I', frame_data.read(4))[0]
                header = (rotation_keyframe_count & 4095, rotation_keyframe_count >> 12)
                rot_keyframe_headers.append(header)

        index = 0
        for node_idx in range(animation_element.node_count):
            if rot_flags[node_idx] == True:
                rotation_keyframe_count = rot_keyframe_headers[index][0]
                for rotation_frame in range(rotation_keyframe_count):
                    rot_keyframes.append(struct.unpack('<H', frame_data.read(2))[0])

                index += 1

        for node_idx in range(animation_element.node_count):
            default_x, default_y, default_z = struct.unpack('<HHH', frame_data.read(6))
            rot_def_data.append(default_x)
            rot_def_data.append(default_y)
            rot_def_data.append(default_z)

        index = 0
        for node_idx in range(animation_element.node_count):
            if rot_flags[node_idx] == True:
                rotation_keyframe_count = rot_keyframe_headers[index][0]
                for rotation_frame in range(rotation_keyframe_count):
                    x, y, z = struct.unpack('<HHH', frame_data.read(6))
                    rot_keyframe_data.append(x)
                    rot_keyframe_data.append(y)
                    rot_keyframe_data.append(z)

                index += 1

    translation_offset = animation_element.offset_to_compressed_data + translation_keyframe_offset
    if data_size > translation_offset:
        frame_data.seek(translation_offset, 0)
        for node_idx in range(animation_element.node_count):
            if trans_flags[node_idx] == True:
                translation_keyframe_count = struct.unpack('<I', frame_data.read(4))[0]
                header = (translation_keyframe_count & 4095, translation_keyframe_count >> 12)
                trans_keyframe_headers.append(header)

        index = 0
        for node_idx in range(animation_element.node_count):
            if trans_flags[node_idx] == True:
                translation_keyframe_count = trans_keyframe_headers[index][0]
                for translation_frame in range(translation_keyframe_count):
                    trans_keyframes.append(struct.unpack('<H', frame_data.read(2))[0])

                index += 1

        for node_idx in range(animation_element.node_count):
            default_x, default_y, default_z = struct.unpack('<fff', frame_data.read(12))
            trans_def_data.append(default_x)
            trans_def_data.append(default_y)
            trans_def_data.append(default_z)

        index = 0
        for node_idx in range(animation_element.node_count):
            if trans_flags[node_idx] == True:
                translation_keyframe_count = trans_keyframe_headers[index][0]
                for translation_frame in range(translation_keyframe_count):
                    x, y, z = struct.unpack('<fff', frame_data.read(12))
                    trans_keyframe_data.append(x)
                    trans_keyframe_data.append(y)
                    trans_keyframe_data.append(z)

                index += 1
                    
    scale_offset = animation_element.offset_to_compressed_data + scale_keyframe_offset
    if data_size > scale_offset:
        frame_data.seek(scale_offset, 0)
        for node_idx in range(animation_element.node_count):
            if scale_flags[node_idx] == True:
                scale_keyframe_count = struct.unpack('<I', frame_data.read(4))[0]
                header = (scale_keyframe_count & 4095, scale_keyframe_count >> 12)
                scale_keyframe_headers.append(header)
        index = 0
        for node_idx in range(animation_element.node_count):
            if scale_flags[node_idx] == True:
                scale_keyframe_count = scale_keyframe_headers[index][0]
                for scale_frame in range(scale_keyframe_count):
                    scale_keyframes.append(struct.unpack('<H', frame_data.read(2))[0])

                index += 1

        for node_idx in range(animation_element.node_count):
            if scale_flags[node_idx] == True:
                default_scale = struct.unpack('<f', frame_data.read(4))[0]
                scale_def_data[node_idx] = default_scale

        index = 0
        for node_idx in range(animation_element.node_count):
            if scale_flags[node_idx] == True:
                scale_keyframe_count = scale_keyframe_headers[index][0]
                for scale_frame in range(scale_keyframe_count):
                    scale = struct.unpack('<f', frame_data.read(4))[0]
                    scale_keyframe_data.append(scale)

                index += 1

    decomp_quat = decompress_quaternion48
    blend_trans = lerp_blend_vectors
    blend_quats = nlerp_blend_quaternions

    ri = ti = si = 0
    for ni in range(animation_element.node_count):
        rot_kf_ct  = trans_kf_ct  = scale_kf_ct  = 0
        rot_kf_off = trans_kf_off = scale_kf_off = 0

        rot_def = decomp_quat(*rot_def_data[3 * ni: 3 * (ni + 1)])
        trans_def = trans_def_data[3 * ni: 3 * (ni + 1)]
        scale_def = 1.0

        if rot_flags[ni]:
            rot_kf_ct, rot_kf_off = rot_keyframe_headers[ri]
            ri += 1

        if trans_flags[ni]:
            trans_kf_ct, trans_kf_off = trans_keyframe_headers[ti]
            ti += 1

        if scale_flags[ni]:
            scale_kf_ct, scale_kf_off = scale_keyframe_headers[si]
            si += 1
            scale_def = scale_def_data[ni]

        # add this nodes keyframes to the keyframe lists in the jma_anim
        for kf_ct, kf_off, all_kfs, kfs_by_nodes in (
                (rot_kf_ct, rot_kf_off, rot_keyframes,
                 rot_keyframes_by_nodes),
                (trans_kf_ct, trans_kf_off, trans_keyframes,
                 trans_keyframes_by_nodes),
                (scale_kf_ct, scale_kf_off, scale_keyframes,
                 scale_keyframes_by_nodes)):
            kfs_by_nodes.append(list(all_kfs[kf_off: kf_off + kf_ct]))


        if rot_kf_ct:
            rot_first_kf = rot_keyframes[rot_kf_off]
            rot_last_kf  = rot_keyframes[rot_kf_off + rot_kf_ct - 1]
            rot_first = decomp_quat(*rot_keyframe_data[
                3 * rot_kf_off:
                3 * (rot_kf_off + 1)])
            rot_last = decomp_quat(*rot_keyframe_data[
                3 * (rot_kf_off + rot_kf_ct - 1):
                3 * (rot_kf_off + rot_kf_ct)])

        if trans_kf_ct:
            trans_first_kf = trans_keyframes[trans_kf_off]
            trans_last_kf  = trans_keyframes[trans_kf_off + trans_kf_ct - 1]
            trans_first = trans_keyframe_data[
                3 * trans_kf_off:
                3 * (trans_kf_off + 1)]
            trans_last = trans_keyframe_data[
                3 * (trans_kf_off + trans_kf_ct - 1):
                3 * (trans_kf_off + trans_kf_ct)]

        if scale_kf_ct:
            scale_first_kf = scale_keyframes[scale_kf_off]
            scale_last_kf  = scale_keyframes[scale_kf_off + scale_kf_ct - 1]
            scale_first = scale_keyframe_data[scale_kf_off]
            scale_last  = scale_keyframe_data[scale_kf_off + scale_kf_ct - 1]

        for fi in range(animation_element.frame_count):
            node_frame = frames[fi][ni]

            if not rot_kf_ct or fi == 0:
                # first frame OR only default data stored for this node
                i, j, k, w = rot_def
            elif fi == rot_last_kf:
                # frame is the last keyframe. repeat it to the end
                i, j, k, w = rot_last
            elif fi < rot_first_kf:
                # frame is before the first stored keyframe.
                # blend from default data to first keyframe.
                i, j, k, w = blend_quats(
                    rot_def, rot_first, fi / rot_first_kf)
            else:
                # frame is at/past the first stored keyframe.
                # don't need to use default data at all.
                kf_i = get_keyframe_index_of_frame(
                    fi, rot_keyframes, rot_kf_ct, rot_kf_off)
                kf0 = rot_keyframes[kf_i]
                q0 = decomp_quat(
                    *rot_keyframe_data[kf_i * 3: (kf_i + 1) * 3])

                if fi == kf0:
                    # this keyframe is the frame we want.
                    # no blending required
                    i, j, k, w = q0
                else:
                    kf1 = rot_keyframes[kf_i + 1]
                    ratio = (fi - kf0) / (kf1 - kf0)
                    kf_i += 1
                    q1 = decomp_quat(
                        *rot_keyframe_data[kf_i * 3: (kf_i + 1) * 3])
                    i, j, k, w = blend_quats(q0, q1, ratio)


            if not trans_kf_ct or fi == 0:
                # first frame OR only default data stored for this node
                x, y, z = trans_def
            elif fi == trans_last_kf:
                # frame is the last keyframe. repeat it to the end
                x, y, z = trans_last
            elif fi < trans_first_kf:
                # frame is before the first stored keyframe.
                # blend from default data to first keyframe.
                x, y, z = blend_trans(
                    trans_def, trans_first, fi / trans_first_kf)
            else:
                # frame is at/past the first stored keyframe.
                # don't need to use default data at all.
                kf_i = get_keyframe_index_of_frame(
                    fi, trans_keyframes, trans_kf_ct, trans_kf_off)
                kf0 = trans_keyframes[kf_i]
                p0 = trans_keyframe_data[kf_i * 3: (kf_i + 1) * 3]

                if fi == kf0:
                    # this keyframe is the frame we want.
                    # no blending required
                    x, y, z = p0
                else:
                    kf1 = trans_keyframes[kf_i + 1]
                    ratio = (fi - kf0) / (kf1 - kf0)

                    kf_i += 1
                    p1 = trans_keyframe_data[kf_i * 3: (kf_i + 1) * 3]
                    x, y, z = blend_trans(p0, p1, ratio)


            if not scale_kf_ct or fi == 0:
                # first frame OR only default data stored for this node
                scale = scale_def
            elif fi == scale_last_kf:
                # frame is the last keyframe. repeat it to the end
                scale = scale_last
            elif fi < scale_first_kf:
                # frame is before the first stored keyframe.
                # blend from default data to first keyframe.
                ratio = fi / scale_first_kf
                scale = scale_def * (1 - ratio) + scale_first * ratio
            else:
                # frame is at/past the first stored keyframe.
                # don't need to use default data at all.
                kf_i = get_keyframe_index_of_frame(
                    fi, scale_keyframes, scale_kf_ct, scale_kf_off)

                if fi == kf0:
                    # this keyframe is the frame we want.
                    # no blending required
                    scale = scale_keyframes[kf_i]
                else:
                    ratio = ((fi - scale_keyframes[kf_i]) /
                             (scale_keyframes[kf_i + 1] -
                              scale_keyframes[kf_i]))
                    scale = (
                        scale_keyframe_data[kf_i] * (1 - ratio) +
                        scale_keyframe_data[kf_i + 1] * ratio)


            nmag = i**2 + j**2 + k**2 + w**2
            if nmag:
                nmag = 1 / sqrt(nmag)
                i = i * nmag
                j = j * nmag
                k = k * nmag
                w = w * nmag
                node_frame.rotation = Quaternion((w, i, j, k))

            node_frame.translation = Vector((x, y, z)) * 100
            node_frame.scale = scale

    if not AnimationTypeEnum(animation_element.type) == AnimationTypeEnum.overlay:
        # duplicate the first frame to the last frame for non-overlays
        frames[-1] = copy.deepcopy(frames[-2])

    return frames

def process_file_retail(input_stream, global_functions, tag_format, report):
    TAG = tag_format.TagAsset()
    ANIMATION = AnimationAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    ANIMATION.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    ANIMATION.antr_body = ANIMATION.AntrBody()
    ANIMATION.antr_body.objects_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "objects"))
    ANIMATION.antr_body.units_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "units"))
    ANIMATION.antr_body.weapons_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapons"))
    ANIMATION.antr_body.vehicles_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "vehicles"))
    ANIMATION.antr_body.devices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "devices"))
    ANIMATION.antr_body.unit_damage_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "unit damage"))
    ANIMATION.antr_body.first_person_weapons_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "first person weapons"))
    ANIMATION.antr_body.sound_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sound references"))
    ANIMATION.antr_body.limp_body_node_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "limp body node radius"))
    ANIMATION.antr_body.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", AnimationTagFlags))
    input_stream.read(2) # Padding?
    ANIMATION.antr_body.nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "nodes"))
    ANIMATION.antr_body.animations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "animations"))

    ANIMATION.objects = []
    object_node = tag_format.get_xml_node(XML_OUTPUT, ANIMATION.antr_body.objects_tag_block.count, tag_node, "name", "objects")
    for objects_idx in range(ANIMATION.antr_body.objects_tag_block.count):
        object_element_node = None
        if XML_OUTPUT:
            object_element_node = TAG.xml_doc.createElement('element')
            object_element_node.setAttribute('index', str(objects_idx))
            object_node.appendChild(object_element_node)

        object = ANIMATION.Objects()
        object.animation = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(object_element_node, "animation", None, ANIMATION.antr_body.animations_tag_block.count, "animation_block"))
        object.function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(object_element_node, "function", FunctionEnum))
        object.function_controls = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(object_element_node, "function controls", FunctionControlsEnum))
        input_stream.read(14) # Padding?

        ANIMATION.objects.append(object)

    ANIMATION.units = []
    unit_node = tag_format.get_xml_node(XML_OUTPUT, ANIMATION.antr_body.units_tag_block.count, tag_node, "name", "units")
    for unit_idx in range(ANIMATION.antr_body.units_tag_block.count):
        unit_element_node = None
        if XML_OUTPUT:
            unit_element_node = TAG.xml_doc.createElement('element')
            unit_element_node.setAttribute('index', str(unit_idx))
            unit_node.appendChild(unit_element_node)

        unit = ANIMATION.AnimationBehavior()
        unit.label = TAG.read_string32(input_stream, TAG, tag_format.XMLData(unit_element_node, "label"))
        unit.right_yaw_per_frame = TAG.read_degree(input_stream, TAG, tag_format.XMLData(unit_element_node, "right yaw per frame"))
        unit.left_yaw_per_frame = TAG.read_degree(input_stream, TAG, tag_format.XMLData(unit_element_node, "left yaw per frame"))
        unit.right_frame_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(unit_element_node, "right frame count"))
        unit.left_frame_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(unit_element_node, "left frame count"))
        unit.down_pitch_per_frame = TAG.read_degree(input_stream, TAG, tag_format.XMLData(unit_element_node, "down pitch per frame"))
        unit.up_pitch_per_frame = TAG.read_degree(input_stream, TAG, tag_format.XMLData(unit_element_node, "up pitch per frame"))
        unit.down_pitch_frame_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(unit_element_node, "down pitch frame count"))
        unit.up_pitch_frame_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(unit_element_node, "up pitch frame count"))
        input_stream.read(8) # Padding?
        unit.animations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(unit_element_node, "animations"))
        unit.ik_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(unit_element_node, "ik points"))
        unit.weapons_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(unit_element_node, "weapons"))

        ANIMATION.units.append(unit)

    for unit_idx, unit in enumerate(ANIMATION.units):
        unit_element_node = None
        if XML_OUTPUT:
            unit_element_node = unit_node.childNodes[unit_idx]

        unit.animations = []
        unit.ik_points = []
        unit.weapons = []
        animation_node = tag_format.get_xml_node(XML_OUTPUT, unit.animations_tag_block.count, unit_element_node, "name", "animations")
        ik_point_node = tag_format.get_xml_node(XML_OUTPUT, unit.ik_points_tag_block.count, unit_element_node, "name", "ik points")
        weapon_node = tag_format.get_xml_node(XML_OUTPUT, unit.weapons_tag_block.count, unit_element_node, "name", "weapons")
        for unit_animation_idx in range(unit.animations_tag_block.count):
            unit_animation_element_node = None
            if XML_OUTPUT:
                unit_animation_element_node = TAG.xml_doc.createElement('element')
                unit_animation_element_node.setAttribute('index', str(unit_animation_idx))
                animation_node.appendChild(unit_animation_element_node)

            unit.animations.append(TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(unit_animation_element_node, "animation", None, ANIMATION.antr_body.animations_tag_block.count, "animation_block")))

        for unit_ik_point_idx in range(unit.ik_points_tag_block.count):
            ik_point_element_node = None
            if XML_OUTPUT:
                ik_point_element_node = TAG.xml_doc.createElement('element')
                ik_point_element_node.setAttribute('index', str(unit_ik_point_idx))
                ik_point_node.appendChild(ik_point_element_node)

            ik_point = ANIMATION.IKPoints()
            ik_point.marker = TAG.read_string32(input_stream, TAG, tag_format.XMLData(ik_point_element_node, "marker"))
            ik_point.attach_to_marker = TAG.read_string32(input_stream, TAG, tag_format.XMLData(ik_point_element_node, "attach to marker"))

            unit.ik_points.append(ik_point)

        for unit_weapon_idx in range(unit.weapons_tag_block.count):
            unit_weapon_element_node = None
            if XML_OUTPUT:
                unit_weapon_element_node = TAG.xml_doc.createElement('element')
                unit_weapon_element_node.setAttribute('index', str(unit_weapon_idx))
                weapon_node.appendChild(unit_weapon_element_node)

            weapon_type = ANIMATION.AnimationBehavior()
            weapon_type.label = TAG.read_string32(input_stream, TAG, tag_format.XMLData(unit_weapon_element_node, "name"))
            weapon_type.grip_marker = TAG.read_string32(input_stream, TAG, tag_format.XMLData(unit_weapon_element_node, "grip marker"))
            weapon_type.hand_marker = TAG.read_string32(input_stream, TAG, tag_format.XMLData(unit_weapon_element_node, "hand marker"))
            weapon_type.right_yaw_per_frame = TAG.read_degree(input_stream, TAG, tag_format.XMLData(unit_weapon_element_node, "right yaw per frame"))
            weapon_type.left_yaw_per_frame = TAG.read_degree(input_stream, TAG, tag_format.XMLData(unit_weapon_element_node, "left yaw per frame"))
            weapon_type.right_frame_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(unit_weapon_element_node, "right frame count"))
            weapon_type.left_frame_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(unit_weapon_element_node, "left frame count"))
            weapon_type.down_pitch_per_frame = TAG.read_degree(input_stream, TAG, tag_format.XMLData(unit_weapon_element_node, "down pitch per frame"))
            weapon_type.up_pitch_per_frame = TAG.read_degree(input_stream, TAG, tag_format.XMLData(unit_weapon_element_node, "up pitch per frame"))
            weapon_type.down_pitch_frame_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(unit_weapon_element_node, "down pitch frame count"))
            weapon_type.up_pitch_frame_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(unit_weapon_element_node, "up pitch frame count"))
            input_stream.read(32) # Padding?
            weapon_type.animations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(unit_weapon_element_node, "animations"))
            weapon_type.ik_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(unit_weapon_element_node, "ik points"))
            weapon_type.weapons_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(unit_weapon_element_node, "weapons types"))

            unit.weapons.append(weapon_type)

        for unit_weapon_idx, unit_weapon in enumerate(unit.weapons):
            unit_weapon_element_node = None
            if XML_OUTPUT:
                unit_weapon_element_node = weapon_node.childNodes[unit_weapon_idx]

            unit_weapon.animations = []
            unit_weapon.ik_points = []
            unit_weapon.weapons = []
            animation_node = tag_format.get_xml_node(XML_OUTPUT, unit_weapon.animations_tag_block.count, unit_weapon_element_node, "name", "animations")
            ik_point_node = tag_format.get_xml_node(XML_OUTPUT, unit_weapon.ik_points_tag_block.count, unit_weapon_element_node, "name", "ik points")
            weapon_type_node = tag_format.get_xml_node(XML_OUTPUT, unit_weapon.weapons_tag_block.count, unit_weapon_element_node, "name", "weapons types")
            for weapon_animation_idx in range(unit_weapon.animations_tag_block.count):
                weapon_animation_element_node = None
                if XML_OUTPUT:
                    weapon_animation_element_node = TAG.xml_doc.createElement('element')
                    weapon_animation_element_node.setAttribute('index', str(weapon_animation_idx))
                    animation_node.appendChild(weapon_animation_element_node)

                unit_weapon.animations.append(TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(weapon_animation_element_node, "animation", None, ANIMATION.antr_body.animations_tag_block.count, "animation_block")))

            for weapon_ik_point_idx in range(unit_weapon.ik_points_tag_block.count):
                weapon_ik_point_element_node = None
                if XML_OUTPUT:
                    weapon_ik_point_element_node = TAG.xml_doc.createElement('element')
                    weapon_ik_point_element_node.setAttribute('index', str(weapon_ik_point_idx))
                    ik_point_node.appendChild(weapon_ik_point_element_node)

                ik_point = ANIMATION.IKPoints()
                ik_point.marker = TAG.read_string32(input_stream, TAG, tag_format.XMLData(weapon_ik_point_element_node, "marker"))
                ik_point.attach_to_marker = TAG.read_string32(input_stream, TAG, tag_format.XMLData(weapon_ik_point_element_node, "attach to marker"))

                unit_weapon.ik_points.append(ik_point)

            for weapon_type_idx in range(unit_weapon.weapons_tag_block.count):
                weapon_type_element_node = None
                if XML_OUTPUT:
                    weapon_type_element_node = TAG.xml_doc.createElement('element')
                    weapon_type_element_node.setAttribute('index', str(weapon_type_idx))
                    weapon_type_node.appendChild(weapon_type_element_node)

                weapon_type = ANIMATION.AnimationBehavior()
                weapon_type.label = TAG.read_string32(input_stream, TAG, tag_format.XMLData(weapon_type_element_node, "label"))
                input_stream.read(16) # Padding?
                weapon_type.animations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(weapon_type_element_node, "animations"))

                unit_weapon.weapons.append(weapon_type)

            for weapon_type_idx, weapon_type in enumerate(unit_weapon.weapons):
                weapon_type_element_node = None
                if XML_OUTPUT:
                    weapon_type_element_node = weapon_type_node.childNodes[weapon_type_idx]

                weapon_type.animations = []
                animation_node = tag_format.get_xml_node(XML_OUTPUT, weapon_type.animations_tag_block.count, weapon_type_element_node, "name", "animations")
                for weapon_type_animation_idx in range(weapon_type.animations_tag_block.count):
                    weapon_type_animation_element_node = None
                    if XML_OUTPUT:
                        weapon_type_animation_element_node = TAG.xml_doc.createElement('element')
                        weapon_type_animation_element_node.setAttribute('index', str(weapon_type_animation_idx))
                        animation_node.appendChild(weapon_type_animation_element_node)

                    weapon_type.animations.append(TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(weapon_type_animation_element_node, "animation", None, ANIMATION.antr_body.animations_tag_block.count, "animation_block")))

    ANIMATION.weapons = []
    weapon_node = tag_format.get_xml_node(XML_OUTPUT, ANIMATION.antr_body.weapons_tag_block.count, tag_node, "name", "weapons")
    for weapon_idx in range(ANIMATION.antr_body.weapons_tag_block.count):
        weapon_element_node = None
        if XML_OUTPUT:
            weapon_element_node = TAG.xml_doc.createElement('element')
            weapon_element_node.setAttribute('index', str(weapon_idx))
            weapon_node.appendChild(weapon_element_node)

        weapon = ANIMATION.AnimationGroups()
        input_stream.read(16) # Padding?
        weapon.animations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "animations"))

        ANIMATION.weapons.append(weapon)

    for weapon_idx, weapon in enumerate(ANIMATION.weapons):
        weapon_element_node = None
        if XML_OUTPUT:
            weapon_element_node = weapon_node.childNodes[weapon_idx]

        weapon.animations = []
        animation_node = tag_format.get_xml_node(XML_OUTPUT, weapon.animations_tag_block.count, weapon_element_node, "name", "animations")
        for weapon_animation_idx in range(weapon.animations_tag_block.count):
            weapon_animation_element_node = None
            if XML_OUTPUT:
                weapon_animation_element_node = TAG.xml_doc.createElement('element')
                weapon_animation_element_node.setAttribute('index', str(weapon_animation_idx))
                animation_node.appendChild(weapon_animation_element_node)

            weapon.animations.append(TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(weapon_animation_element_node, "animation", None, ANIMATION.antr_body.animations_tag_block.count, "animation_block")))

    ANIMATION.vehicles = []
    vehicle_node = tag_format.get_xml_node(XML_OUTPUT, ANIMATION.antr_body.vehicles_tag_block.count, tag_node, "name", "vehicles")
    for vehicle_idx in range(ANIMATION.antr_body.vehicles_tag_block.count):
        vehicle_element_node = None
        if XML_OUTPUT:
            vehicle_element_node = TAG.xml_doc.createElement('element')
            vehicle_element_node.setAttribute('index', str(vehicle_idx))
            vehicle_node.appendChild(vehicle_element_node)

        vehicle = ANIMATION.AnimationGroups()
        vehicle.right_yaw_per_frame = TAG.read_degree(input_stream, TAG, tag_format.XMLData(vehicle_element_node, "right yaw per frame"))
        vehicle.left_yaw_per_frame = TAG.read_degree(input_stream, TAG, tag_format.XMLData(vehicle_element_node, "left yaw per frame"))
        vehicle.right_frame_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(vehicle_element_node, "right frame count"))
        vehicle.left_frame_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(vehicle_element_node, "left frame count"))
        vehicle.down_pitch_per_frame = TAG.read_degree(input_stream, TAG, tag_format.XMLData(vehicle_element_node, "down pitch per frame"))
        vehicle.up_pitch_per_frame = TAG.read_degree(input_stream, TAG, tag_format.XMLData(vehicle_element_node, "up pitch per frame"))
        vehicle.down_pitch_frame_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(vehicle_element_node, "down pitch frame count"))
        vehicle.up_pitch_frame_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(vehicle_element_node, "up pitch frame count"))
        input_stream.read(68) # Padding?
        vehicle.animations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(vehicle_element_node, "animations"))
        vehicle.suspension_animations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(vehicle_element_node, "suspension animations"))

        ANIMATION.vehicles.append(vehicle)

    for vehicle_idx, vehicle in enumerate(ANIMATION.vehicles):
        vehicle_element_node = None
        if XML_OUTPUT:
            vehicle_element_node = vehicle_node.childNodes[vehicle_idx]

        vehicle.animations = []
        vehicle.suspension_animations = []
        animation_node = tag_format.get_xml_node(XML_OUTPUT, vehicle.animations_tag_block.count, vehicle_element_node, "name", "animations")
        suspension_animation_node = tag_format.get_xml_node(XML_OUTPUT, vehicle.suspension_animations_tag_block.count, vehicle_element_node, "name", "suspension animations")
        for vehicle_animation_idx in range(vehicle.animations_tag_block.count):
            vehicle_animation_element_node = None
            if XML_OUTPUT:
                vehicle_animation_element_node = TAG.xml_doc.createElement('element')
                vehicle_animation_element_node.setAttribute('index', str(vehicle_animation_idx))
                animation_node.appendChild(vehicle_animation_element_node)

            vehicle.animations.append(TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(vehicle_animation_element_node, "animation", None, ANIMATION.antr_body.animations_tag_block.count, "animation_block")))

        for vehicle_suspension_animation_idx in range(vehicle.suspension_animations_tag_block.count):
            vehicle_suspension_animation_element_node = None
            if XML_OUTPUT:
                vehicle_suspension_animation_element_node = TAG.xml_doc.createElement('element')
                vehicle_suspension_animation_element_node.setAttribute('index', str(vehicle_suspension_animation_idx))
                suspension_animation_node.appendChild(vehicle_suspension_animation_element_node)

            vehicle_suspension = ANIMATION.AnimationSuspension()
            vehicle_suspension.mass_point_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(vehicle_suspension_animation_element_node, "mass point index"))
            vehicle_suspension.animation = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(vehicle_suspension_animation_element_node, "animation", None, ANIMATION.antr_body.animations_tag_block.count, "animation_block"))
            vehicle_suspension.full_extension_ground_depth = TAG.read_float(input_stream, TAG, tag_format.XMLData(vehicle_suspension_animation_element_node, "full extension ground_depth"))
            vehicle_suspension.full_compression_ground_depth = TAG.read_float(input_stream, TAG, tag_format.XMLData(vehicle_suspension_animation_element_node, "full compression ground_depth"))
            input_stream.read(8) # Padding?

            vehicle.suspension_animations.append(vehicle_suspension)

    ANIMATION.devices = []
    device_node = tag_format.get_xml_node(XML_OUTPUT, ANIMATION.antr_body.devices_tag_block.count, tag_node, "name", "devices")
    for devices_idx in range(ANIMATION.antr_body.devices_tag_block.count):
        device_element_node = None
        if XML_OUTPUT:
            device_element_node = TAG.xml_doc.createElement('element')
            device_element_node.setAttribute('index', str(devices_idx))
            device_node.appendChild(device_element_node)

        device = ANIMATION.AnimationGroups()
        input_stream.read(84) # Padding?
        device.animations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(device_element_node, "animations"))

        ANIMATION.devices.append(device)

    for device_idx, device in enumerate(ANIMATION.devices):
        device_element_node = None
        if XML_OUTPUT:
            device_element_node = device_node.childNodes[device_idx]

        device.animations = []
        animation_node = tag_format.get_xml_node(XML_OUTPUT, device.animations_tag_block.count, device_element_node, "name", "animations")
        for device_animation_idx in range(device.animations_tag_block.count):
            device_animation_element_node = None
            if XML_OUTPUT:
                device_animation_element_node = TAG.xml_doc.createElement('element')
                device_animation_element_node.setAttribute('index', str(device_animation_idx))
                animation_node.appendChild(device_animation_element_node)

            device.animations.append(TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(device_animation_element_node, "animation", None, ANIMATION.antr_body.animations_tag_block.count, "animation_block")))

    ANIMATION.unit_damages = []
    unit_damage_node = tag_format.get_xml_node(XML_OUTPUT, ANIMATION.antr_body.unit_damage_tag_block.count, tag_node, "name", "unit damage")
    for unit_damage_idx in range(ANIMATION.antr_body.unit_damage_tag_block.count):
        unit_damage_element_node = None
        if XML_OUTPUT:
            unit_damage_element_node = TAG.xml_doc.createElement('element')
            unit_damage_element_node.setAttribute('index', str(unit_damage_idx))
            unit_damage_node.appendChild(unit_damage_element_node)

        ANIMATION.unit_damages.append(TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(unit_damage_element_node, "animation", None, ANIMATION.antr_body.animations_tag_block.count, "animation_block")))

    ANIMATION.first_person_weapons = []
    first_person_weapon_node = tag_format.get_xml_node(XML_OUTPUT, ANIMATION.antr_body.first_person_weapons_tag_block.count, tag_node, "name", "first person weapons")
    for first_person_weapon_idx in range(ANIMATION.antr_body.first_person_weapons_tag_block.count):
        first_person_weapon_element_node = None
        if XML_OUTPUT:
            first_person_weapon_element_node = TAG.xml_doc.createElement('element')
            first_person_weapon_element_node.setAttribute('index', str(first_person_weapon_idx))
            first_person_weapon_node.appendChild(first_person_weapon_element_node)

        first_person = ANIMATION.AnimationGroups()
        input_stream.read(16) # Padding?
        first_person.animations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(first_person_weapon_element_node, "animations"))

        ANIMATION.first_person_weapons.append(first_person)

    for first_person_weapon_idx, first_person_weapon in enumerate(ANIMATION.first_person_weapons):
        first_person_weapon_element_node = None
        if XML_OUTPUT:
            first_person_weapon_element_node = first_person_weapon_node.childNodes[first_person_weapon_idx]

        first_person_weapon.animations = []
        animation_node = tag_format.get_xml_node(XML_OUTPUT, first_person_weapon.animations_tag_block.count, first_person_weapon_element_node, "name", "animations")
        for first_person_weapon_animation_idx in range(first_person_weapon.animations_tag_block.count):
            first_person_weapon_animation_element_node = None
            if XML_OUTPUT:
                first_person_weapon_animation_element_node = TAG.xml_doc.createElement('element')
                first_person_weapon_animation_element_node.setAttribute('index', str(first_person_weapon_animation_idx))
                animation_node.appendChild(first_person_weapon_animation_element_node)

            first_person_weapon.animations.append(TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(first_person_weapon_animation_element_node, "animation", None, ANIMATION.antr_body.animations_tag_block.count, "animation_block")))

    ANIMATION.sound_references = []
    sound_reference_node = tag_format.get_xml_node(XML_OUTPUT, ANIMATION.antr_body.sound_references_tag_block.count, tag_node, "name", "sound references")
    for sound_reference_idx in range(ANIMATION.antr_body.sound_references_tag_block.count):
        sound_reference_element_node = None
        if XML_OUTPUT:
            sound_reference_element_node = TAG.xml_doc.createElement('element')
            sound_reference_element_node.setAttribute('index', str(sound_reference_idx))
            sound_reference_node.appendChild(sound_reference_element_node)

        tag_ref = TAG.TagRef().read(input_stream, TAG)
        input_stream.read(4) # Padding?

        ANIMATION.sound_references.append(tag_ref)

    for sound_reference_idx, sound_reference in enumerate(ANIMATION.sound_references):
        if sound_reference.name_length > 0:
            sound_reference.name = TAG.read_variable_string(input_stream, sound_reference.name_length, TAG)

        if XML_OUTPUT:
            sound_reference_element_node = sound_reference_node.childNodes[sound_reference_idx]

            sound_reference.create_xml_node(tag_format.XMLData(sound_reference_element_node, "sound"))

    ANIMATION.nodes = []
    bone_node = tag_format.get_xml_node(XML_OUTPUT, ANIMATION.antr_body.nodes_tag_block.count, tag_node, "name", "nodes")
    for node_idx in range(ANIMATION.antr_body.nodes_tag_block.count):
        node_element_node = None
        if XML_OUTPUT:
            node_element_node = TAG.xml_doc.createElement('element')
            node_element_node.setAttribute('index', str(node_idx))
            bone_node.appendChild(node_element_node)

        node = ANIMATION.Nodes()
        node.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element_node, "name"))
        node.sibling = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "next sibling node index", None, ANIMATION.antr_body.nodes_tag_block.count, "animation_graph_node_block"))
        node.child = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "first child node index", None, ANIMATION.antr_body.nodes_tag_block.count, "animation_graph_node_block"))
        node.parent = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "parent node index", None, ANIMATION.antr_body.nodes_tag_block.count, "animation_graph_node_block"))
        input_stream.read(2) # Padding?
        node.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element_node, "node joint flags", NodeJointFlags))
        node.base_vector = TAG.read_vector(input_stream, TAG, tag_format.XMLData(node_element_node, "base vector"))
        node.vector_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element_node, "vector range"))
        input_stream.read(4) # Padding?

        ANIMATION.nodes.append(node)

    ANIMATION.animations = []
    animation_node = tag_format.get_xml_node(XML_OUTPUT, ANIMATION.antr_body.animations_tag_block.count, tag_node, "name", "animations")
    for animation_idx in range(ANIMATION.antr_body.animations_tag_block.count):
        animation_element_node = None
        if XML_OUTPUT:
            animation_element_node = TAG.xml_doc.createElement('element')
            animation_element_node.setAttribute('index', str(animation_idx))
            animation_node.appendChild(animation_element_node)

        animation = ANIMATION.Animation()
        animation.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(animation_element_node, "name"))
        animation.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "type", AnimationTypeEnum))
        animation.frame_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "frame count"))
        animation.frame_size = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "frame size"))
        animation.frame_info_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "frame info type", AnimationFrameInfoTypeEnum))
        animation.node_list_checksum = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(animation_element_node, "node list checksum"))
        animation.node_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "node count"))
        animation.loop_frame_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "loop frame index"))
        animation.weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_element_node, "weight"))
        animation.key_frame_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "key frame index"))
        animation.second_key_frame_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "second key frame index"))
        animation.next_animation = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "next animation", None, ANIMATION.antr_body.animations_tag_block.count, "animation_block"))
        animation.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "flags", AnimationFlags))
        animation.sound = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "sound", None, ANIMATION.antr_body.sound_references_tag_block.count, "animation_graph_sound_reference_block"))
        animation.sound_frame_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "sound frame index"))
        animation.left_foot_frame_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(animation_element_node, "left foot frame index"))
        animation.right_foot_frame_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(animation_element_node, "right foot frame index"))
        animation.first_permutation_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "first permutation index"))
        animation.chance_to_play = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_element_node, "chance to play"))
        animation.frame_info_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(animation_element_node, "frame info"))
        animation.trans_flags0 = TAG.read_unsigned_integer(input_stream, TAG, tag_format.XMLData(animation_element_node, "translation flags0"))
        animation.trans_flags1 = TAG.read_unsigned_integer(input_stream, TAG, tag_format.XMLData(animation_element_node, "translation flags1"))
        input_stream.read(8) # Padding?
        animation.rot_flags0 = TAG.read_unsigned_integer(input_stream, TAG, tag_format.XMLData(animation_element_node, "rotation flags0"))
        animation.rot_flags1 = TAG.read_unsigned_integer(input_stream, TAG, tag_format.XMLData(animation_element_node, "rotation flags1"))
        input_stream.read(8) # Padding?
        animation.scale_flags0 = TAG.read_unsigned_integer(input_stream, TAG, tag_format.XMLData(animation_element_node, "scale flags0"))
        animation.scale_flags1 = TAG.read_unsigned_integer(input_stream, TAG, tag_format.XMLData(animation_element_node, "scale flags1"))
        input_stream.read(4) # Padding?
        animation.offset_to_compressed_data = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(animation_element_node, "offset to compressed data"))
        animation.default_data_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(animation_element_node, "default data"))
        animation.frame_data_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(animation_element_node, "frame data"))

        ANIMATION.animations.append(animation)

    armature = bpy.context.object
    transforms = None
    if armature and armature.type == "ARMATURE":
        sorted_list = global_functions.sort_list(list(armature.data.bones), armature, "halo1", 8200, False)
        joined_list = sorted_list[0]

        transforms = []
        for node in joined_list:
            pose_bone = armature.pose.bones[node.name]
            object_matrix = pose_bone.matrix
            if pose_bone.parent:
                #Files at or above 8205 use absolute transform instead of local transform for nodes
                object_matrix = pose_bone.parent.matrix.inverted() @ pose_bone.matrix

            pos, rot, scale = object_matrix.decompose()

            default_matrix_scale = Matrix.Scale(scale[0], 4)
            default_matrix_rotation = rot.inverted().to_matrix().to_4x4()
            default_matrix_translation = Matrix.Translation(pos)
            transform_matrix = default_matrix_translation @ default_matrix_rotation @ default_matrix_scale

            transforms.append(transform_matrix)

    for animation_idx, animation_element in enumerate(ANIMATION.animations):
        animation_element_node = None
        if XML_OUTPUT:
            animation_element_node = animation_node.childNodes[animation_idx]

        animation_element.frame_info = []
        animation_element.default_data = []
        animation_element.frame_data = []
        animation_element.frame_info_tag_data.data = input_stream.read(animation_element.frame_info_tag_data.size)
        animation_element.default_data_tag_data.data = input_stream.read(animation_element.default_data_tag_data.size)
        animation_element.frame_data_tag_data.data = input_stream.read(animation_element.frame_data_tag_data.size)
        frame_info_crc32 = binascii.crc32(animation_element.frame_info_tag_data.data)
        default_data_crc32 = binascii.crc32(animation_element.default_data_tag_data.data)
        frame_data_crc32 = binascii.crc32(animation_element.frame_data_tag_data.data)
        frame_info_node = tag_format.get_xml_node(XML_OUTPUT, animation_element.frame_count, animation_element_node, "name", "frame info")
        default_data_node = tag_format.get_xml_node(XML_OUTPUT, animation_element.frame_count, animation_element_node, "name", "default data")
        frame_data_node = tag_format.get_xml_node(XML_OUTPUT, animation_element.frame_count, animation_element_node, "name", "frame data")
        if XML_OUTPUT:
            frame_info_field_text = minidom.Document().createTextNode("checksum: %s" % str(hex(frame_info_crc32)).split("0x", 1)[1])
            default_field_text = minidom.Document().createTextNode("checksum: %s" % str(hex(default_data_crc32)).split("0x", 1)[1])
            frame_field_text = minidom.Document().createTextNode("checksum: %s" % str(hex(frame_data_crc32)).split("0x", 1)[1])
            frame_info_node.appendChild(frame_info_field_text)
            default_data_node.appendChild(default_field_text)
            frame_data_node.appendChild(frame_field_text)

        frame_info = io.BytesIO(animation_element.frame_info_tag_data.data)
        default_data = io.BytesIO(animation_element.default_data_tag_data.data)
        frame_data = io.BytesIO(animation_element.frame_data_tag_data.data)

        # sum the frame info changes for each frame from the frame_info
        animation_element.frame_info = deserialize_frame_info(frame_info, frame_info_node, ANIMATION, animation_element, TAG, tag_format)

        if AnimationFlags.compressed_data in AnimationFlags(animation_element.flags):
            # decompress compressed animations
            animation.frame_data = deserialize_compressed_frame_data(animation_element, frame_data)

        else:
            # create the node states from the frame_data and default_data
            animation_element.frame_data = build_frame_data(default_data, frame_data, default_data_node, frame_data_node, ANIMATION, animation_element, transforms, TAG, tag_format)

        if not AnimationTypeEnum(animation_element.type) == AnimationTypeEnum.overlay:
            # this is set to True on instantiation.
            # Set it to False since we had to provide root node info
            animation_element.frame_info_applied = False
            apply_root_node_info_to_states(animation_element)

    unit_node = tag_format.get_xml_node(XML_OUTPUT, ANIMATION.antr_body.units_tag_block.count, tag_node, "name", "units")
    for unit_idx, unit in enumerate(ANIMATION.units):
        unit_element_node = None
        if XML_OUTPUT:
            unit_element_node = unit_node.childNodes[unit_idx]

        animation_node = tag_format.get_xml_node(XML_OUTPUT, unit.animations_tag_block.count, unit_element_node, "name", "animations")
        weapon_node = tag_format.get_xml_node(XML_OUTPUT, unit.weapons_tag_block.count, unit_element_node, "name", "weapons")
        for unit_animation_idx, unit_animation in enumerate(unit.animations):
            unit_animation_element_node = None
            if XML_OUTPUT:
                unit_animation_element_node = animation_node.childNodes[unit_animation_idx]

            name = "none"
            if not unit_animation == -1:
                name = ANIMATION.animations[unit_animation].name

            if XML_OUTPUT:
                tag_format.append_xml_attributes(unit_animation_element_node, [("name", name)])

        for unit_weapon_idx, unit_weapon in enumerate(unit.weapons):
            unit_weapon_element_node = None
            if XML_OUTPUT:
                unit_weapon_element_node = weapon_node.childNodes[unit_weapon_idx]

            animation_node = tag_format.get_xml_node(XML_OUTPUT, unit_weapon.animations_tag_block.count, unit_weapon_element_node, "name", "animations")
            weapon_type_node = tag_format.get_xml_node(XML_OUTPUT, unit_weapon.weapons_tag_block.count, unit_weapon_element_node, "name", "weapons types")
            for weapon_animation_idx, weapon_animation in enumerate(unit_weapon.animations):
                weapon_animation_element_node = None
                if XML_OUTPUT:
                    weapon_animation_element_node = animation_node.childNodes[weapon_animation_idx]

                name = "none"
                if not weapon_animation == -1:
                    name = ANIMATION.animations[weapon_animation].name

                if XML_OUTPUT:
                    tag_format.append_xml_attributes(weapon_animation_element_node, [("name", name)])

            for weapon_type_idx, weapon_type in enumerate(unit_weapon.weapons):
                weapon_type_element_node = None
                if XML_OUTPUT:
                    weapon_type_element_node = weapon_type_node.childNodes[weapon_type_idx]

                animation_node = tag_format.get_xml_node(XML_OUTPUT, weapon_type.animations_tag_block.count, weapon_type_element_node, "name", "animations")
                for weapon_type_animation_idx, weapon_type_animation in enumerate(weapon_type.animations):
                    weapon_type_animation_element_node = None
                    if XML_OUTPUT:
                        weapon_type_animation_element_node = animation_node.childNodes[weapon_type_animation_idx]

                    name = "none"
                    if not weapon_type_animation == -1:
                        name = ANIMATION.animations[weapon_type_animation].name

                    if XML_OUTPUT:
                        tag_format.append_xml_attributes(weapon_type_animation_element_node, [("name", name)])

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, ANIMATION.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return ANIMATION
