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

def process_scene(context, game_title, qua_version, qua_type, qua_revision, strip_identifier, hidden_geo, nonrender_geo, report):
    QUA = QUAAsset()

    blend_filename = bpy.path.basename(context.blend_data.filepath)
    scene_name = 'default'
    if len(blend_filename) > 0:
        scene_name = blend_filename.rsplit('.', 1)[0]

    QUA.version = qua_version
    QUA.scene_type = qua_type
    QUA.scene_version = qua_revision
    QUA.scene_name = scene_name
    QUA.units = []
    QUA.scenery = []
    QUA.effects_scenery = []
    QUA.objects = []
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

    data_key = "data%s" % os.sep
    tags_key = "tags%s" % os.sep

    ubercam = None
    extra_cameras = []
    speakers = []
    armatures = []
    effects = []
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

        elif obj.qua.ubercam_halo_effect:
            effects.append(obj)

    if ubercam:
        if ubercam.animation_data:
            for nla_track in ubercam.animation_data.nla_tracks:
                for strip in nla_track.strips:
                    action_tranforms = []
                    sound_data = []
                    custom_scripts = []
                    shot_effects = []
                    first_frame = round(strip.frame_start)
                    last_frame = round(strip.frame_end + 1)
                    for frame in range(first_frame, last_frame):
                        action_tranforms.append(get_camera_frame(context, frame, ubercam, qua_version))

                    for speaker in speakers:
                        sound_tag = "none"
                        female_sound_tag = "none"
                        audio_filename = "none"
                        female_audio_filename = "none"
                        character = "none"
                        dialog_color = "none"
                        if speaker.parent and not global_functions.string_empty_check(speaker.parent.name):
                            character = speaker.parent.name

                        if not global_functions.string_empty_check(speaker.data.qua.ubercam_sound_tag_reference):
                            sound_tag = os.path.abspath(bpy.path.abspath(speaker.data.qua.ubercam_sound_tag_reference))
                            if tags_key in sound_tag:
                                sound_tag_string = sound_tag.split(tags_key, 1)[1]
                                sound_tag = "%s%s" % (tags_key, sound_tag_string)

                        if not global_functions.string_empty_check(speaker.data.qua.ubercam_female_sound_tag_reference):
                            female_sound_tag = os.path.abspath(bpy.path.abspath(speaker.data.qua.ubercam_female_sound_tag_reference))
                            if tags_key in female_sound_tag:
                                female_sound_tag_string = female_sound_tag.split(tags_key, 1)[1]
                                female_sound_tag = "%s%s" % (tags_key, female_sound_tag_string)

                        else:
                            female_sound_tag = sound_tag

                        if not global_functions.string_empty_check(speaker.data.qua.ubercam_female_sound_file_reference):
                            female_audio_filename = os.path.abspath(bpy.path.abspath(speaker.data.qua.ubercam_female_sound_file_reference))
                            if data_key in female_audio_filename:
                                female_audio_string = female_audio_filename.split(data_key, 1)[1]
                                female_audio_filename = "%s%s" % (data_key, female_audio_string)

                        if not global_functions.string_empty_check(speaker.data.qua.ubercam_dialog_color):
                            dialog_color = speaker.data.qua.ubercam_dialog_color

                        if speaker.data.sound and not global_functions.string_empty_check(speaker.data.sound.filepath):
                            audio_filename = os.path.abspath(bpy.path.abspath(speaker.data.sound.filepath))
                            if data_key in audio_filename:
                                audio_filename_string = audio_filename.split(data_key, 1)[1]
                                audio_filename = "%s%s" % (data_key, audio_filename_string)

                            if female_audio_filename == "none":
                                female_audio_filename = audio_filename

                            for nla_track in speaker.animation_data.nla_tracks:
                                for strip in nla_track.strips:
                                    sound_initial_frame = round(strip.frame_start)
                                    if sound_initial_frame in range(first_frame, last_frame):
                                        sound_data.append(QUAAsset.AudioData(sound_tag, female_sound_tag, audio_filename, female_audio_filename, sound_initial_frame, character, 
                                                                             dialog_color))

                    for text in bpy.data.texts:
                        if text.qua.ubercam_halo_script:
                            ubercam_frame_number = round(text.qua.ubercam_frame_number)
                            if ubercam_frame_number in range(first_frame, last_frame):
                                script = QUAAsset.CustomScriptData()
                                script.node_id = text.qua.ubercam_node_id
                                script.sequence_id = text.qua.ubercam_sequence_id
                                script.script = text.as_string().replace("\n", " ")
                                script.frame = text.qua.ubercam_frame_number

                                custom_scripts.append(script)

                    for effect in effects:
                        ubercam_frame_number = round(effect.qua.ubercam_frame_number)
                        if ubercam_frame_number in range(first_frame, last_frame):
                            effect_string = "none"
                            marker_name_string = "none"
                            marker_parent_string = "none"
                            function_a_string = "none"
                            function_b_string = "none"
                            if not global_functions.string_empty_check(effect.qua.ubercam_effect):
                                effect_string = os.path.abspath(bpy.path.abspath(effect.qua.ubercam_effect))
                                if tags_key in effect_string:
                                    effect_string = effect_string.split(tags_key, 1)[1]
        
                            if not global_functions.string_empty_check(effect.name):
                                marker_name_string = effect.name

                            if effect.parent:
                                marker_parent_string = effect.parent.name

                            if not global_functions.string_empty_check(effect.qua.ubercam_function_a):
                                function_a_string = effect.qua.ubercam_function_a

                            if not global_functions.string_empty_check(effect.qua.ubercam_function_b):
                                function_b_string = effect.qua.ubercam_function_b

                            effect_data = QUAAsset.EffectData()
                            effect_data.node_id = effect.qua.ubercam_node_id
                            effect_data.sequence_id = effect.qua.ubercam_sequence_id
                            effect_data.effect = effect_string
                            effect_data.marker_name = marker_name_string
                            effect_data.marker_parent = marker_parent_string
                            effect_data.frame = effect.qua.ubercam_frame_number
                            effect_data.effect_state = effect.qua.ubercam_effect_state
                            effect_data.size_scale = effect.scale[0]
                            effect_data.function_a = function_a_string
                            effect_data.function_b = function_b_string
                            effect_data.looping = effect.qua.ubercam_looping

                            shot_effects.append(effect_data)

                    QUA.shots.append(QUAAsset.Shots(frames=action_tranforms, audio_data_version=3, audio_data=sound_data, custom_script_data_version=1, 
                                                    custom_script_data=custom_scripts, effect_data_version=4, effect_data=shot_effects))

            for extra_camera_ob in extra_cameras:
                extra_shots = []
                for nla_track in ubercam.animation_data.nla_tracks:
                    for strip in nla_track.strips:
                        extra_action_tranforms = []
                        first_frame = round(strip.frame_start)
                        last_frame = round(strip.frame_end + 1)
                        for frame in range(first_frame, last_frame):
                            extra_action_tranforms.append(get_camera_frame(context, frame, extra_camera_ob, qua_version))

                        extra_shots.append(QUAAsset.Shots(frames=extra_action_tranforms, audio_data=[]))

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
                qua_object.export_name = "none"
                qua_object.animation_id = "none"
                qua_object.animation_path = "none"
                qua_object.object_path = "none"
                if not global_functions.string_empty_check(armature.name):
                    qua_object.export_name = armature.name

                if game_title == "halo3":
                    if not global_functions.string_empty_check(armature.ass_jms.ubercam_object_animation):
                        qua_object.object_path = os.path.abspath(bpy.path.abspath(armature.ass_jms.ubercam_object_animation))
                        if strip_identifier:
                            results = qua_object.object_path.rsplit(".", 1)
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
                                    qua_object.object_path = os.path.join(directory_path, "%s.%s" % (stripped_file_name, extension))
                else:
                    if not global_functions.string_empty_check(armature.ass_jms.ubercam_animation_name):
                        qua_object.animation_id = os.path.abspath(bpy.path.abspath(armature.ass_jms.ubercam_animation_name))

                    if not global_functions.string_empty_check(armature.ass_jms.ubercam_object_animation):
                        ubercam_object_animation_string = os.path.abspath(bpy.path.abspath(armature.ass_jms.ubercam_object_animation))
                        qua_object.animation_path = ubercam_object_animation_string
                        if tags_key in ubercam_object_animation_string:
                            object_animation_string = ubercam_object_animation_string.split(tags_key, 1)[1]
                            qua_object.animation_path = "%s%s" % (tags_key, object_animation_string)

                    if not global_functions.string_empty_check(armature.ass_jms.ubercam_object_reference):
                        ubercam_object_reference_string = os.path.abspath(bpy.path.abspath(armature.ass_jms.ubercam_object_reference))
                        qua_object.object_path = ubercam_object_reference_string
                        if tags_key in ubercam_object_reference_string:
                            object_reference_string = ubercam_object_reference_string.split(tags_key, 1)[1]
                            qua_object.object_path = "%s%s" % (tags_key, object_reference_string)

                qua_object.bits = []
                for nla_track in ubercam.animation_data.nla_tracks:
                    for strip in nla_track.strips:
                        first_frame = round(strip.frame_start)
                        context.scene.frame_set(first_frame)
                        visible_bit = 1
                        if armature.hide_render:
                            visible_bit = 0

                        qua_object.bits.append(visible_bit)

                if game_title == "halo3":
                    if ubercam_object_type == UbercamObjectTypeEnum.unit:
                        QUA.units.append(qua_object)
                    elif ubercam_object_type == UbercamObjectTypeEnum.scenery:
                        QUA.scenery.append(qua_object)
                    elif ubercam_object_type == UbercamObjectTypeEnum.effect_scenery:
                        QUA.effects_scenery.append(qua_object)
                else:
                    QUA.objects.append(qua_object)

    else:
        raise global_functions.ParseError("No uber camera in your scene. Create a camera and give it & as the prefix for the object name")
    
    resource_management.restore_collection_visibility(stored_collection_visibility)
    resource_management.restore_object_visibility(stored_object_visibility)
    resource_management.restore_modifier_visibility(stored_modifier_visibility)

    return QUA
