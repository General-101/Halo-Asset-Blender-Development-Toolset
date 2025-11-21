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

import math

from .format import QUAAsset
from ..global_functions import global_functions

def parse_legacy_unit(QUA, unit_version):
    unit_count = int(QUA.next())
    for unit_idx in range(unit_count):
        qua_object = QUAAsset.Object()
        qua_object.export_name = QUA.next()
        qua_object.object_path = QUA.next()
        qua_object.bits = []
        if unit_version >= 3:
            bit_list = QUA.next().split()
            for bit in bit_list:
                # Inverting this here for Blender
                if bit == "0":
                    qua_object.bits.append(True)
                elif bit == "1":
                    qua_object.bits.append(False)

        QUA.units.append(qua_object)

def parse_legacy_scenery(QUA, scenery_version):
    scenery_count = int(QUA.next())
    for scenery_idx in range(scenery_count):
        qua_object = QUAAsset.Object()
        qua_object.export_name = QUA.next()
        qua_object.object_path = QUA.next()
        qua_object.bits = []
        if scenery_version >= 3:
            bit_list = QUA.next().split()
            for bit in bit_list:
                if bit == "0":
                    qua_object.bits.append(True)
                elif bit == "1":
                    qua_object.bits.append(False)

        QUA.scenery.append(qua_object)

def parse_legacy_effect_scenery(QUA):
    scenery_count = int(QUA.next())
    for scenery_idx in range(scenery_count):
        qua_object = QUAAsset.Object()
        qua_object.export_name = QUA.next()
        qua_object.object_path = QUA.next()
        qua_object.bits = []
        bit_list = QUA.next().split()
        for bit in bit_list:
            if bit == "0":
                qua_object.bits.append(True)
            elif bit == "1":
                qua_object.bits.append(False)

        QUA.scenery.append(qua_object)

def parse_legacy_shot(QUA, shot_count, shot_version):
    for shot_idx in range(shot_count):
        shot = QUAAsset.Shots()
        shot.audio_data_version = 0
        shot.custom_script_data_version = 0
        shot.effect_data_version = 0
        shot.frames = []
        shot.audio_data = []
        shot.custom_script_data = []
        shot.effect_data = []

        frame_count = int(QUA.next())
        for frame_idx in range(frame_count):
            frame = QUAAsset.Frames()
            frame.position = QUA.next_vector_space()
            frame.up = QUA.next_vector_space()
            frame.forward = QUA.next_vector_space()
            frame.fov = float(QUA.next())
            if shot_version >= 4:
                frame.aperture = float(QUA.next())

            frame.focal_length = float(QUA.next())
            frame.depth_of_field = bool(int(QUA.next()))
            frame.near_focal = float(QUA.next())
            frame.far_focal = float(QUA.next())
            frame.focal_depth = float(QUA.next())
            frame.blur_amount = float(QUA.next())

            shot.frames.append(frame)

        audio_count = int(QUA.next())
        for audio_idx in range(audio_count):
            audio = QUAAsset.AudioData()
            audio.audio_filename = QUA.next()
            audio.frame = int(QUA.next())
            audio.character = QUA.next()

            shot.audio_data.append(audio)

        QUA.shots.append(shot)

def parse_legacy_extra_cameras(QUA):
    extra_camera_count = int(QUA.next())
    for extra_camera_idx in range(extra_camera_count):
        extra_camera = QUAAsset.ExtraCamera()
        extra_camera.name = QUA.next()
        extra_camera.camera_type = QUA.next()
        extra_camera.extra_shots = []
        for shot in QUA.shots:
            extra_shot = QUAAsset.Shots()
            extra_shot.frames = []
            extra_shot.audio_data = []

            for frame in shot.frames:
                extra_frame = QUAAsset.Frames()
                camera_is_enabled = bool(int(QUA.next()))
                if camera_is_enabled:
                    extra_frame.camera_is_enabled = False
                else:
                    extra_frame.camera_is_enabled = True
                extra_frame.position = QUA.next_vector_space()
                extra_frame.up = QUA.next_vector_space()
                extra_frame.forward = QUA.next_vector_space()
                extra_frame.fov = float(QUA.next())
                extra_frame.focal_length = float(QUA.next())
                extra_frame.depth_of_field = bool(int(QUA.next()))
                extra_frame.near_focal = float(QUA.next())
                extra_frame.far_focal = float(QUA.next())
                extra_frame.focal_depth = float(QUA.next())
                extra_frame.blur_amount = float(QUA.next())

                extra_shot.frames.append(extra_frame)

            extra_camera.extra_shots.append(extra_shot)

        QUA.extra_cameras.append(extra_camera)

def parse_legacy_file(QUA, report):
    QUA.units = []
    QUA.scenery = []
    QUA.effects_scenery = []
    QUA.objects = []
    QUA.shots = []
    QUA.extra_cameras = []

    QUA.version = int(QUA.next())
    if QUA.version >= 5:
        QUA.scene_name = QUA.next()
        shot_count = int(QUA.next())
        parse_legacy_unit(QUA, 5)
        parse_legacy_scenery(QUA, 5)
        parse_legacy_effect_scenery(QUA)
        parse_legacy_shot(QUA, shot_count, 5)
        parse_legacy_extra_cameras(QUA)

    elif QUA.version == 4:
        QUA.scene_name = QUA.next()
        shot_count = int(QUA.next())
        parse_legacy_unit(QUA, 4)
        parse_legacy_scenery(QUA, 4)
        parse_legacy_shot(QUA, shot_count, 4)
        parse_legacy_extra_cameras(QUA)

    elif QUA.version >= 3:
        QUA.scene_name = QUA.next()
        shot_count = int(QUA.next())
        parse_legacy_unit(QUA, 3)
        parse_legacy_scenery(QUA, 3)
        parse_legacy_shot(QUA, shot_count, 3)
        parse_legacy_extra_cameras(QUA)

    elif QUA.version == 2:
        QUA.scene_name = QUA.next()
        parse_legacy_unit(QUA, 2)
        parse_legacy_scenery(QUA, 2)
        shot_count = int(QUA.next())
        parse_legacy_shot(QUA, shot_count, 2)
        parse_legacy_extra_cameras(QUA)

    elif QUA.version == 1:
        raise global_functions.ParseError("Importer does not support this %s version" % "QUA")

def parse_type_main_file(QUA):
    QUA.scene_version = int(QUA.next())
    QUA.scene_name = QUA.next()
    shot_count = int(QUA.next())
    object_count = int(QUA.next())
    for object_idx in range(object_count):
        qua_object = QUAAsset.Object()
        qua_object.export_name = QUA.next()
        qua_object.animation_id = QUA.next()
        qua_object.animation_path = QUA.next()
        qua_object.object_path = QUA.next()
        qua_object.bits = []
        bit_list = QUA.next().split()
        for bit in bit_list:
            # Inverting this here for Blender
            if bit == "0":
                qua_object.bits.append(True)
            elif bit == "1":
                qua_object.bits.append(False)

        QUA.objects.append(qua_object)

    for shot_idx in range(shot_count):
        shot = QUAAsset.Shots()
        shot.audio_data_version = 0
        shot.custom_script_data_version = 0
        shot.effect_data_version = 0
        shot.frames = []
        shot.audio_data = []
        shot.custom_script_data = []
        shot.effect_data = []

        frame_count = int(QUA.next())
        for frame_idx in range(frame_count):
            frame = QUAAsset.Frames()
            frame.position = QUA.next_vector_space()
            frame.up = QUA.next_vector_space()
            frame.forward = QUA.next_vector_space()
            frame.focal_length = float(QUA.next())
            frame.depth_of_field = bool(int(QUA.next()))
            frame.near_focal = float(QUA.next())
            frame.far_focal = float(QUA.next())
            frame.near_focal_depth = float(QUA.next())
            frame.far_focal_depth = float(QUA.next())
            frame.near_blur_amount = float(QUA.next())
            frame.far_blur_amount = float(QUA.next())

            shot.frames.append(frame)

        shot.audio_data_version = int(QUA.next())
        audio_count = int(QUA.next())
        for audio_idx in range(audio_count):
            audio = QUAAsset.AudioData()
            audio.sound_tag = QUA.next()
            audio.female_sound_tag = QUA.next()
            audio.audio_filename = QUA.next()
            audio.female_audio_filename = QUA.next()
            audio.frame = int(QUA.next())
            audio.character = QUA.next()
            audio.dialog_color = QUA.next()

            shot.audio_data.append(audio)

        shot.custom_script_data_version = int(QUA.next())
        custom_script_count = int(QUA.next())
        for custom_script_idx in range(custom_script_count):
            custom_script = QUAAsset.CustomScriptData()
            custom_script.node_id = int(QUA.next())
            custom_script.sequence_id = int(QUA.next())
            custom_script.script = QUA.next()
            custom_script.frame = int(QUA.next())

            shot.audio_data.append(custom_script)

        shot.effect_data_version = int(QUA.next())
        effect_count = int(QUA.next())
        for effect_idx in range(effect_count):
            effect = QUAAsset.EffectData()
            effect.node_id = int(QUA.next())
            effect.sequence_id = int(QUA.next())
            effect.effect = QUA.next()
            effect.marker_name = QUA.next()
            effect.marker_parent = QUA.next()
            effect.frame = int(QUA.next())
            effect.effect_state = int(QUA.next())
            effect.size_scale = float(QUA.next())
            effect.function_a = QUA.next()
            effect.function_b = QUA.next()
            effect.looping = int(QUA.next())

            shot.effect_data.append(effect)

        QUA.shots.append(shot)

    extra_camera_count = int(QUA.next())
    for extra_camera_idx in range(extra_camera_count):
        extra_camera = QUAAsset.ExtraCamera()
        extra_camera.name = QUA.next()
        extra_camera.camera_type = QUA.next()
        extra_camera.extra_shots = []
        for shot in QUA.shots:
            extra_shot = QUAAsset.Shots()
            extra_shot.frames = []
            extra_shot.audio_data = []

            for frame in shot.frames:
                extra_frame = QUAAsset.Frames()
                camera_is_enabled = bool(int(QUA.next()))
                if camera_is_enabled:
                    extra_frame.camera_is_enabled = False
                else:
                    extra_frame.camera_is_enabled = True
                extra_frame.position = QUA.next_vector_space()
                extra_frame.up = QUA.next_vector_space()
                extra_frame.forward = QUA.next_vector_space()
                extra_frame.focal_length = float(QUA.next())
                extra_frame.depth_of_field = bool(int(QUA.next()))
                extra_frame.near_focal = float(QUA.next())
                extra_frame.far_focal = float(QUA.next())
                extra_frame.near_focal_depth = float(QUA.next())
                extra_frame.far_focal_depth = float(QUA.next())
                extra_frame.near_blur_amount = float(QUA.next())
                extra_frame.far_blur_amount = float(QUA.next())

                extra_shot.frames.append(extra_frame)

            extra_camera.extra_shots.append(extra_shot)

        QUA.extra_cameras.append(extra_camera)

def parse_type_segment_file(QUA):
    QUA.scene_version = int(QUA.next())
    QUA.scene_name = QUA.next()
    shot_count = int(QUA.next())
    for shot_idx in range(shot_count):
        shot = QUAAsset.Shots()
        shot.audio_data_version = 0
        shot.custom_script_data_version = 0
        shot.effect_data_version = 0
        shot.frames = []
        shot.audio_data = []
        shot.custom_script_data = []
        shot.effect_data = []

        shot.custom_script_data_version = int(QUA.next())
        custom_script_count = int(QUA.next())
        for custom_script_idx in range(custom_script_count):
            custom_script = QUAAsset.CustomScriptData()
            custom_script.node_id = int(QUA.next())
            custom_script.sequence_id = int(QUA.next())
            custom_script.script = QUA.next()
            custom_script.frame = int(QUA.next())

            shot.audio_data.append(custom_script)

        shot.effect_data_version = int(QUA.next())
        effect_count = int(QUA.next())
        for effect_idx in range(effect_count):
            effect = QUAAsset.EffectData()
            effect.node_id = int(QUA.next())
            effect.sequence_id = int(QUA.next())
            effect.effect = QUA.next()
            effect.marker_name = QUA.next()
            effect.marker_parent = QUA.next()
            effect.frame = int(QUA.next())
            effect.effect_state = int(QUA.next())
            effect.size_scale = float(QUA.next())
            effect.function_a = QUA.next()
            effect.function_b = QUA.next()
            effect.looping = int(QUA.next())

            shot.effect_data.append(effect)

        QUA.shots.append(shot)

def parse_new_file(QUA, report):
    QUA.units = []
    QUA.scenery = []
    QUA.effects_scenery = []
    QUA.objects = []
    QUA.shots = []
    QUA.extra_cameras = []

    QUA.version = int(QUA.next())
    QUA.scene_type = QUA.next()

    if QUA.version >= 4:
        if QUA.scene_type == "main":
            parse_type_main_file(QUA)
        else:
            parse_type_segment_file(QUA)

    elif QUA.version >= 3:
        report({'WARNING'}, "QUA version 3 is not supported. Let General_101 know you found a file to look at.")

    if QUA.version >= 2:
        QUA.scene_name = QUA.next()
        shot_count = int(QUA.next())
        object_count = int(QUA.next())
        for object_idx in range(object_count):
            qua_object = QUAAsset.Object()
            qua_object.export_name = QUA.next()
            qua_object.animation_id = QUA.next()
            qua_object.animation_path = QUA.next()
            qua_object.object_path = QUA.next()
            qua_object.bits = []
            bit_list = QUA.next().split()
            for bit in bit_list:
                # Inverting this here for Blender
                if bit == "0":
                    qua_object.bits.append(True)
                elif bit == "1":
                    qua_object.bits.append(False)

            QUA.objects.append(qua_object)

        for shot_idx in range(shot_count):
            shot = QUAAsset.Shots()
            shot.audio_data_version = 0
            shot.custom_script_data_version = 0
            shot.effect_data_version = 0
            shot.frames = []
            shot.audio_data = []
            shot.custom_script_data = []
            shot.effect_data = []

            frame_count = int(QUA.next())
            for frame_idx in range(frame_count):
                frame = QUAAsset.Frames()
                frame.position = QUA.next_vector_space()
                frame.up = QUA.next_vector_space()
                frame.forward = QUA.next_vector_space()
                frame.fov = float(QUA.next())
                frame.aperture = float(QUA.next())
                frame.focal_length = float(QUA.next())
                frame.depth_of_field = bool(int(QUA.next()))
                frame.near_focal = float(QUA.next())
                frame.far_focal = float(QUA.next())
                frame.focal_depth = float(QUA.next())
                frame.blur_amount = float(QUA.next())

                shot.frames.append(frame)

            audio_count = int(QUA.next())
            for audio_idx in range(audio_count):
                audio = QUAAsset.AudioData()
                audio.audio_filename = QUA.next()
                audio.female_audio_filename = QUA.next()
                audio.frame = int(QUA.next())
                audio.character = QUA.next()
                audio.dialog_color = QUA.next()

                shot.audio_data.append(audio)

            custom_script_count = int(QUA.next())
            for custom_script_idx in range(custom_script_count):
                custom_script = QUAAsset.CustomScriptData()
                custom_script.node_id = int(QUA.next())
                custom_script.sequence_id = int(QUA.next())
                custom_script.script = QUA.next()
                custom_script.frame = int(QUA.next())

                shot.audio_data.append(custom_script)

            effect_count = int(QUA.next())
            for effect_idx in range(effect_count):
                effect = QUAAsset.EffectData()
                effect.node_id = int(QUA.next())
                effect.sequence_id = int(QUA.next())
                effect.effect = QUA.next()
                effect.marker_name = QUA.next()
                effect.marker_parent = QUA.next()
                effect.frame = int(QUA.next())

                shot.effect_data.append(effect)

            QUA.shots.append(shot)

        extra_camera_count = int(QUA.next())
        for extra_camera_idx in range(extra_camera_count):
            extra_camera = QUAAsset.ExtraCamera()
            extra_camera.name = QUA.next()
            extra_camera.camera_type = QUA.next()
            extra_camera.extra_shots = []
            for shot in QUA.shots:
                extra_shot = QUAAsset.Shots()
                extra_shot.frames = []
                extra_shot.audio_data = []

                for frame in shot.frames:
                    extra_frame = QUAAsset.Frames()
                    camera_is_enabled = bool(int(QUA.next()))
                    if camera_is_enabled:
                        extra_frame.camera_is_enabled = False
                    else:
                        extra_frame.camera_is_enabled = True
                    extra_frame.position = QUA.next_vector_space()
                    extra_frame.up = QUA.next_vector_space()
                    extra_frame.forward = QUA.next_vector_space()
                    extra_frame.fov = float(QUA.next())
                    extra_frame.focal_length = float(QUA.next())
                    extra_frame.depth_of_field = bool(int(QUA.next()))
                    extra_frame.near_focal = float(QUA.next())
                    extra_frame.far_focal = float(QUA.next())
                    extra_frame.focal_depth = float(QUA.next())
                    extra_frame.blur_amount = float(QUA.next())

                    extra_shot.frames.append(extra_frame)

                extra_camera.extra_shots.append(extra_shot)

            QUA.extra_cameras.append(extra_camera)

    elif QUA.version == 1:
        report({'WARNING'}, "QUA version 1 is not supported. Let General_101 know you found a file to look at.")

def parse_hr_file(QUA, report):
    QUA.units = []
    QUA.scenery = []
    QUA.effects_scenery = []
    QUA.objects = []
    QUA.shots = []
    QUA.extra_cameras = []

    QUA.version = int(QUA.next())
    if not QUA.version == 2:
        raise global_functions.ParseError("Importer does not support this %s version" % "QUA")

    if QUA.version >= 2:
        QUA.scene_name = QUA.next()
        shot_count = int(QUA.next())
        object_count = int(QUA.next())
        for object_idx in range(object_count):
            qua_object = QUAAsset.Object()
            qua_object.export_name = QUA.next()
            qua_object.animation_id = QUA.next()
            qua_object.animation_path = QUA.next()
            qua_object.object_path = QUA.next()
            qua_object.bits = []
            bit_list = QUA.next().split()
            for bit in bit_list:
                # Inverting this here for Blender
                if bit == "0":
                    qua_object.bits.append(True)
                elif bit == "1":
                    qua_object.bits.append(False)

            QUA.objects.append(qua_object)

        for shot_idx in range(shot_count):
            shot = QUAAsset.Shots()
            shot.audio_data_version = 0
            shot.custom_script_data_version = 0
            shot.effect_data_version = 0
            shot.frames = []
            shot.audio_data = []
            shot.custom_script_data = []
            shot.effect_data = []

            frame_count = int(QUA.next())
            for frame_idx in range(frame_count):
                frame = QUAAsset.Frames()
                frame.position = QUA.next_vector_space()
                frame.up = QUA.next_vector_space()
                frame.forward = QUA.next_vector_space()
                frame.fov = float(QUA.next())
                frame.aperture = float(QUA.next())
                frame.focal_length = float(QUA.next())
                frame.depth_of_field = bool(int(QUA.next()))
                frame.near_focal = float(QUA.next())
                frame.far_focal = float(QUA.next())
                frame.focal_depth = float(QUA.next())
                frame.blur_amount = float(QUA.next())

                shot.frames.append(frame)

            audio_count = int(QUA.next())
            for audio_idx in range(audio_count):
                audio = QUAAsset.AudioData()
                audio.audio_filename = QUA.next()
                audio.female_audio_filename = QUA.next()
                audio.frame = int(QUA.next())
                audio.character = QUA.next()
                audio.dialog_color = QUA.next()

                shot.audio_data.append(audio)

            custom_script_count = int(QUA.next())
            for custom_script_idx in range(custom_script_count):
                custom_script = QUAAsset.CustomScriptData()
                custom_script.node_id = int(QUA.next())
                custom_script.sequence_id = int(QUA.next())
                custom_script.script = QUA.next()
                custom_script.frame = int(QUA.next())

                shot.audio_data.append(custom_script)

            effect_count = int(QUA.next())
            for effect_idx in range(effect_count):
                effect = QUAAsset.EffectData()
                effect.node_id = int(QUA.next())
                effect.sequence_id = int(QUA.next())
                effect.effect = QUA.next()
                effect.marker_name = QUA.next()
                effect.marker_parent = QUA.next()
                effect.frame = int(QUA.next())

                shot.effect_data.append(effect)

            QUA.shots.append(shot)

        extra_camera_count = int(QUA.next())
        for extra_camera_idx in range(extra_camera_count):
            extra_camera = QUAAsset.ExtraCamera()
            extra_camera.name = QUA.next()
            extra_camera.camera_type = QUA.next()
            extra_camera.extra_shots = []
            for shot in QUA.shots:
                extra_shot = QUAAsset.Shots()
                extra_shot.frames = []
                extra_shot.audio_data = []

                for frame in shot.frames:
                    extra_frame = QUAAsset.Frames()
                    camera_is_enabled = bool(int(QUA.next()))
                    if camera_is_enabled:
                        extra_frame.camera_is_enabled = False
                    else:
                        extra_frame.camera_is_enabled = True
                    extra_frame.position = QUA.next_vector_space()
                    extra_frame.up = QUA.next_vector_space()
                    extra_frame.forward = QUA.next_vector_space()
                    extra_frame.fov = float(QUA.next())
                    extra_frame.focal_length = float(QUA.next())
                    extra_frame.depth_of_field = bool(int(QUA.next()))
                    extra_frame.near_focal = float(QUA.next())
                    extra_frame.far_focal = float(QUA.next())
                    extra_frame.focal_depth = float(QUA.next())
                    extra_frame.blur_amount = float(QUA.next())

                    extra_shot.frames.append(extra_frame)

                extra_camera.extra_shots.append(extra_shot)

            QUA.extra_cameras.append(extra_camera)

    elif QUA.version == 1:
        report({'WARNING'}, "QUA version 1 is not supported. Let General_101 know you found a file to look at.")

def process_file(game_title, QUA, report):
    if game_title == "halo3":
        parse_legacy_file(QUA, report)

    elif game_title == "halor" or game_title == "halo4":
        parse_new_file(QUA, report)

    if QUA.left() != 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % QUA.left())

    return QUA
