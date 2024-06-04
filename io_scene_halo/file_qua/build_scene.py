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

import numpy as np
from math import radians
from mathutils import Matrix, Euler
from ..global_functions.mesh_processing import deselect_objects

def build_object(context):
    armdata = bpy.data.armatures.new('Armature')
    armature = bpy.data.objects.new('Armature', armdata)
    context.collection.objects.link(armature)

    armature.select_set(True)
    context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode = 'EDIT')
    current_bone = armature.data.edit_bones.new("b_root")
    current_bone.tail[2] = 5
    current_bone.matrix = Matrix().to_4x4()
    armature.select_set(False)
    context.view_layer.objects.active = None

    return armature

def build_camera(context, report, scene, view_layer, shots, camera_name, camera_type="", is_extra_camera=False, armatures=[]):
    camera_data = bpy.data.cameras.new(name=camera_name)
    ob = bpy.data.objects.new(camera_name, camera_data)
    camera_data.qua.ubercam_type = camera_type
    context.collection.objects.link(ob)

    ob.animation_data_create()
    nla_track = ob.animation_data.nla_tracks.new()

    camera_data.animation_data_create()
    nla_track_data = camera_data.animation_data.nla_tracks.new()

    nla_track.name = "shots"
    starting_frame = 1
    for shot_idx, shot in enumerate(shots):
        shot_name = "shot_%s" % shot_idx
        shot_data_name = "data_shot_%s" % (shot_idx)
        if is_extra_camera:
            shot_name = "%s_shot_%s" % (camera_name, shot_idx)
            shot_data_name = "%s_data_shot_%s" % (camera_name, shot_idx)

        action = bpy.data.actions.new(name=shot_name)
        action_data = bpy.data.actions.new(name=shot_data_name)

        ob.animation_data.action = action
        ob.data.animation_data.action = action_data
        shot_frame_count = len(shot.frames) - 1
        for frame_idx, frame in enumerate(shot.frames):
            scene.frame_set(frame_idx + 1)

            right = np.cross(frame.up, frame.forward)
            matrix_rotation = Matrix((frame.forward, right, frame.up)).transposed() @ Euler((radians(90), 0, radians(-90))).to_matrix()
            matrix_translate = Matrix.Translation(frame.position)
            transform_matrix = matrix_translate @ matrix_rotation.to_4x4()

            ob.matrix_world = transform_matrix

            if is_extra_camera:
                ob.hide_render = frame.camera_is_enabled

            camera_data.angle = radians(frame.fov)
            camera_data.sensor_width = frame.aperture
            camera_data.dof.use_dof = frame.depth_of_field
            camera_data.qua.near_focal_plane_distance = frame.near_focal
            camera_data.qua.far_focal_plane_distance = frame.far_focal
            camera_data.dof.focus_distance = frame.focal_depth
            camera_data.dof.aperture_ratio = frame.blur_amount

            view_layer.update()

            ob.keyframe_insert(data_path='location', group="Object Transforms")
            ob.keyframe_insert(data_path='rotation_euler', group="Object Transforms")
            ob.keyframe_insert(data_path='rotation_quaternion', group="Object Transforms")
            ob.keyframe_insert(data_path='scale', group="Object Transforms")
            camera_data.keyframe_insert(data_path='lens')
            camera_data.keyframe_insert(data_path='sensor_width')
            camera_data.keyframe_insert(data_path='dof.use_dof')
            camera_data.keyframe_insert(data_path='qua.near_focal_plane_distance')
            camera_data.keyframe_insert(data_path='qua.far_focal_plane_distance')
            camera_data.keyframe_insert(data_path='dof.focus_distance')
            camera_data.keyframe_insert(data_path='dof.aperture_ratio')

            if is_extra_camera:
                ob.keyframe_insert(data_path='hide_render')

        nla_track.strips.new(shot_name, start=starting_frame, action=action)
        nla_track_data.strips.new(shot_name, start=starting_frame, action=action_data)
        starting_frame += shot_frame_count
        
        ob.animation_data.action = None
        ob.data.animation_data.action = None
        for audio_idx, audio in enumerate(shot.audio_data):
            speaker_name = "shot_%s_speaker_%s" % (shot_idx, audio_idx)
            speaker_data = bpy.data.speakers.new(name=speaker_name)
            speaker = bpy.data.objects.new(speaker_name, speaker_data)
            context.collection.objects.link(speaker)
            for armature in armatures:
                if armature.name == audio.name:
                    speaker.parent = armature

            speaker.animation_data_create()
            speaker_nla_track = speaker.animation_data.nla_tracks.new()
            speaker_nla_track.name="SoundTrack"

            try:
                area = next(a for a in bpy.context.screen.areas if a.type == 'NLA_EDITOR')
                speaker.select_set(True)
                context.view_layer.objects.active = speaker

                context.scene.frame_set(audio.frame)

                area = next(a for a in bpy.context.screen.areas if a.type == 'NLA_EDITOR')
                with context.temp_override(area=area):
                    bpy.ops.nla.soundclip_add()

                speaker.select_set(False)
                context.view_layer.objects.active = None

                speaker.data.sound = bpy.data.sounds.load(audio.filepath)
            except:
                report({'WARNING'}, "No NLA window found. Reimport with the NLA window open or set the details printed to the console manually")
                print("Object Name: ", speaker_name)
                print("Starting Frame: ", audio.frame)
                print("Sound Filepath: ",audio.filepath)
                print(" ")

def build_scene(context, QUA, report):
    deselect_objects(context)

    scene = context.scene
    view_layer = context.view_layer
    if len(QUA.shots) > 0:
        frame_count = 0
        for shot_idx, shot in enumerate(QUA.shots):
            shot_frame_count = len(shot.frames)
            if shot_idx > 0:
                shot_frame_count -= 1
            frame_count += shot_frame_count

        scene.frame_start = 1
        scene.frame_end = frame_count

        armatures = []
        for unit in QUA.units:
            armature = build_object(context)
            armature.name = unit.name
            armature.ass_jms.ubercam_object_type = "0"
            armature.ass_jms.ubercam_object_animation = unit.path
            armatures.append(armature)

        for unit in QUA.scenery:
            armature = build_object(context)
            armature.name = unit.name
            armature.ass_jms.ubercam_object_type = "1"
            armature.ass_jms.ubercam_object_animation = unit.path
            armatures.append(armature)

        for unit in QUA.effects_scenery:
            armature = build_object(context)
            armature.name = unit.name
            armature.ass_jms.ubercam_object_type = "2"
            armature.ass_jms.ubercam_object_animation = unit.path
            armatures.append(armature)

        build_camera(context, report, scene, view_layer, QUA.shots, "&ubercam", armatures=armatures)
        for extra_camera in QUA.extra_cameras:
            build_camera(context, report, scene, view_layer, extra_camera.extra_shots, extra_camera.name, extra_camera.camera_type, True)

    report({'INFO'}, "Import completed successfully")

    return {'FINISHED'}
