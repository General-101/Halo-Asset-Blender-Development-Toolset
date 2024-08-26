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

import os
import bpy

from math import radians
from mathutils import Vector, Matrix, Euler
from .format import QUAAsset, UbercamObjectTypeEnum
from ..global_functions import global_functions, resource_management

def get_camera_frame(context, frame, camera, version):
    context.scene.frame_set(frame)

    camera_matrix = global_functions.get_matrix(camera, camera, False, None, None, False, version, 'QUA', False, 1, False)
    mesh_dimensions = global_functions.get_dimensions(camera_matrix, camera, version, False, 'QUA', 1)
    position = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])

    transposed_matrix = camera_matrix.transposed()
    up = transposed_matrix[1]
    forward = transposed_matrix[2] * -1

    is_enabled = True
    if camera.hide_render:
        is_enabled = False

    vfov = camera.data.angle
    aperture = camera.data.sensor_width 
    focal_length = camera.data.lens
    depth_of_field = int(camera.data.dof.use_dof)
    near_focal = camera.data.qua.near_focal_plane_distance
    far_focal = camera.data.qua.far_focal_plane_distance
    focal_depth = camera.data.dof.focus_distance
    blur_amount = camera.data.dof.aperture_ratio

    return QUAAsset.Frames(is_enabled, position, (up[0], up[1], up[2]), (forward[0], forward[1], forward[2]), vfov, aperture, focal_length, depth_of_field, near_focal, far_focal, focal_depth, blur_amount)

def process_scene(context, game_title, qua_version, strip_identifier, hidden_geo, nonrender_geo, report):
    QUA = QUAAsset()

    blend_filename = bpy.path.basename(context.blend_data.filepath)
    scene_name = 'default'
    if len(blend_filename) > 0:
        scene_name = blend_filename.rsplit('.', 1)[0]

    QUA.version = qua_version
    QUA.name = scene_name
    QUA.units = []
    QUA.scenery = []
    QUA.effects_scenery = []
    QUA.shots = []
    QUA.extra_cameras = []

    layer_collection_list = []
    object_list = []

    if not context.view_layer.objects.active == None:
        bpy.ops.object.mode_set(mode='OBJECT')

    # Gather all scene resources that fit export criteria
    resource_management.gather_scene_resources(context, layer_collection_list, object_list, hidden_geo, nonrender_geo)

    # Store visibility for all relevant resources
    stored_collection_visibility = resource_management.store_collection_visibility(layer_collection_list)
    stored_object_visibility = resource_management.store_object_visibility(object_list)
    stored_modifier_visibility = resource_management.store_modifier_visibility(object_list)

    # Unhide all relevant resources for exporting
    resource_management.unhide_relevant_resources(layer_collection_list, object_list)

    ubercam = None
    extra_cameras = []
    speakers = []
    armatures = []
    for obj in object_list:
        name = obj.name.lower()
        if obj.type == 'CAMERA':
            if name[0:1] == '&' and ubercam == None:
                ubercam = obj

            else:
                extra_cameras.append(obj)

        elif obj.type == 'SPEAKER':
            speakers.append(obj)

        elif obj.type == 'ARMATURE':
            armatures.append(obj)

    if ubercam:
        if ubercam.animation_data:
            for nla_track in ubercam.animation_data.nla_tracks:
                for strip in nla_track.strips:
                    action_tranforms = []
                    sound_data = []
                    first_frame = round(strip.frame_start)
                    last_frame = round(strip.frame_end + 1)
                    for frame in range(first_frame, last_frame):
                        action_tranforms.append(get_camera_frame(context, frame, ubercam, qua_version))

                    for speaker in speakers:
                        object_name = "none"
                        if speaker.parent and not global_functions.string_empty_check(speaker.parent.name):
                            object_name = speaker.parent.name

                        sound_path = "none"
                        if speaker.data.sound and not global_functions.string_empty_check(speaker.data.sound.filepath):
                            sound_path = os.path.abspath(bpy.path.abspath(speaker.data.sound.filepath))
                            for nla_track in speaker.animation_data.nla_tracks:
                                for strip in nla_track.strips:
                                    sound_initial_frame = round(strip.frame_start)
                                    if sound_initial_frame in range(first_frame, last_frame):
                                        sound_data.append(QUAAsset.AudioData(sound_path, sound_initial_frame, object_name))

                    QUA.shots.append(QUAAsset.Shots(action_tranforms, sound_data))

            for extra_camera_ob in extra_cameras:
                extra_shots = []
                for nla_track in ubercam.animation_data.nla_tracks:
                    for strip in nla_track.strips:
                        extra_action_tranforms = []
                        first_frame = round(strip.frame_start)
                        last_frame = round(strip.frame_end + 1)
                        for frame in range(first_frame, last_frame):
                            extra_action_tranforms.append(get_camera_frame(context, frame, extra_camera_ob, qua_version))

                        extra_shots.append(QUAAsset.Shots(extra_action_tranforms, []))

                    extra_camera_name = "none"
                    if not global_functions.string_empty_check(extra_camera_ob.name):
                        extra_camera_name = extra_camera_ob.name

                    extra_camera_type = "none"
                    if not global_functions.string_empty_check(extra_camera_ob.data.qua.ubercam_type):
                        extra_camera_type = extra_camera_ob.data.qua.ubercam_type

                    QUA.extra_cameras.append(QUAAsset.ExtraCamera(extra_camera_name, extra_camera_type, extra_shots))

            for armature in armatures:
                ubercam_object_type = UbercamObjectTypeEnum(int(armature.ass_jms.ubercam_object_type))
                qua_object = QUAAsset.Object()
                qua_object.name = "none"
                if not global_functions.string_empty_check(armature.name):
                    qua_object.name = armature.name

                qua_object.path = "none"
                if not global_functions.string_empty_check(armature.ass_jms.ubercam_object_animation):
                    qua_object.path = os.path.abspath(bpy.path.abspath(armature.ass_jms.ubercam_object_animation))
                    if strip_identifier:
                        results = qua_object.path.rsplit(".", 1)
                        if len(results) >= 2:
                            animation_path = results[0]
                            extension = results[1]
                            directory_path = os.path.dirname(animation_path)
                            file_name = os.path.basename(animation_path)
                            strip_keyword = ""
                            strip_valid = True
                            for char in reversed(file_name):
                                if char.isdigit():
                                    strip_keyword += char
                                else:
                                    if char == "_":
                                        strip_keyword += char
                                        break
                                    else:
                                        strip_valid = False
                                        break
                                    
                            strip_keyword = strip_keyword[::-1]
                            if strip_valid:
                                stripped_file_name = file_name.rsplit(strip_keyword, 1)[0]
                                qua_object.path = os.path.join(directory_path, "%s.%s" % (stripped_file_name, extension))

                qua_object.bits = []
                for nla_track in ubercam.animation_data.nla_tracks:
                    for strip in nla_track.strips:
                        first_frame = round(strip.frame_start)
                        context.scene.frame_set(first_frame)
                        visible_bit = 1
                        if armature.hide_render:
                            visible_bit = 0

                        qua_object.bits.append(visible_bit)

                if ubercam_object_type == UbercamObjectTypeEnum.unit:
                    QUA.units.append(qua_object)
                elif ubercam_object_type == UbercamObjectTypeEnum.scenery:
                    QUA.scenery.append(qua_object)
                elif ubercam_object_type == UbercamObjectTypeEnum.effect_scenery:
                    QUA.effects_scenery.append(qua_object)

    else:
        raise global_functions.ParseError("No uber camera in your scene. Create a camera and give it & as the prefix for the object name")
    
    resource_management.restore_collection_visibility(stored_collection_visibility)
    resource_management.restore_object_visibility(stored_object_visibility)
    resource_management.restore_modifier_visibility(stored_modifier_visibility)

    return QUA
