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

def process_file(QUA, report):
    QUA.version = int(QUA.next())
    if not QUA.version == 5:
        raise global_functions.ParseError("Importer does not support this %s version" % "QUA")

    if QUA.version >= 5:
        QUA.name = QUA.next()
        shot_count = int(QUA.next())
        unit_count = int(QUA.next())
        for unit_idx in range(unit_count):
            qua_object = QUAAsset.Object()
            qua_object.name = QUA.next()
            qua_object.path = QUA.next()
            qua_object.bits = []
            bit_list = QUA.next().split()
            for bit in bit_list:
                # Inverting this here for Blender
                if bit == "0":
                    qua_object.bits.append(True)
                elif bit == "1":
                    qua_object.bits.append(False)

            QUA.units.append(qua_object)

        scenery_count = int(QUA.next())
        for scenery_idx in range(scenery_count):
            qua_object = QUAAsset.Object()
            qua_object.name = QUA.next()
            qua_object.path = QUA.next()
            qua_object.bits = []
            bit_list = QUA.next().split()
            for bit in bit_list:
                if bit == "0":
                    qua_object.bits.append(True)
                elif bit == "1":
                    qua_object.bits.append(False)

            QUA.scenery.append(qua_object)

        effect_scenery_count = int(QUA.next())
        for effect_scenery_idx in range(effect_scenery_count):
            qua_object = QUAAsset.Object()
            qua_object.name = QUA.next()
            qua_object.path = QUA.next()
            qua_object.bits = []
            bit_list = QUA.next().split()
            for bit in bit_list:
                if bit == "0":
                    qua_object.bits.append(True)
                elif bit == "1":
                    qua_object.bits.append(False)

            QUA.effects_scenery.append(qua_object)

        for shot_idx in range(shot_count):
            shot = QUAAsset.Shots()
            shot.frames = []
            shot.audio_data = []

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
                audio.filepath = QUA.next()
                audio.frame = int(QUA.next())
                audio.name = QUA.next()

                shot.audio_data.append(audio)

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

    elif QUA.version == 4:
        print("Not Implemented")

    elif QUA.version >= 3:
        print("Not Implemented")

    elif QUA.version == 2:
        print("Not Implemented")

    elif QUA.version == 1:
        print("Not Implemented")

    if QUA.left() != 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % QUA.left())

    return QUA
