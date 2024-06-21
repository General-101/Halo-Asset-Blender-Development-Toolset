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

from .process_scene import process_scene

def build_asset(context, filepath, game_title, qua_version, strip_identifier, report):
    decimal_1 = '\n%s'
    decimal_2 = '\n%s %s'
    decimal_3 = '\n%s %s %s'
    decimal_4 = '\n%s %s %s %s'

    QUA = process_scene(context, game_title, qua_version, strip_identifier, report)

    file = open(filepath, 'w', encoding="utf-8")

    file.write(
        ';### VERSION ###' +
        '\n%s\n' % (QUA.version)
    )

    file.write(
        '\n;### SCENE ###' +
        '\n;      <scene name (string)>' +
        '\n%s\n' % (QUA.name)
    )

    file.write(
        '\n;### SHOTS ###' +
        '\n%s\n' % (len(QUA.shots))
    )

    file.write(
        '\n;### UNITS ###' +
        '\n%s' % (len(QUA.units)) +
        '\n;      <export name (string)>' +
        '\n;      <export path (string)>' +
        '\n;      <shots visible (bit mask - sorta)>\n'
    )

    for idx, unit in enumerate(QUA.units):
        file.write(
            '\n; UNIT %s' % (idx) +
            '\n%s' % (unit.name) +
            '\n%s' % (unit.path)
        )
        bit_string = ""
        for bit in unit.bits:
            bit_string += "%s " % int(bit)

        file.write('\n%s' % (bit_string))
        file.write('\n')

    file.write(
        '\n;### SCENERY ###' +
        '\n%s' % (len(QUA.scenery)) +
        '\n;      <export name (string)>' +
        '\n;      <export path (string)>' +
        '\n;      <shots visible (bit mask - sorta)>\n'
    )

    for idx, scenery in enumerate(QUA.scenery):
        file.write(
            '\n; SCENERY %s' % (idx) +
            '\n%s' % (scenery.name) +
            '\n%s' % (scenery.path)
        )
        bit_string = ""
        for bit in scenery.bits:
            bit_string += "%s " % int(bit)

        file.write('\n%s' % (bit_string))
        file.write('\n')

    file.write(
        '\n;### EFFECTS_SCENERY ###' +
        '\n%s' % (len(QUA.effects_scenery)) +
        '\n;      <export name (string)>' +
        '\n;      <export path (string)>' +
        '\n;      <shots visible (bit mask - sorta)>\n'
    )

    for idx, effect_scenery in enumerate(QUA.effects_scenery):
        file.write(
            '\n; EFFECTS_SCENERY %s' % (idx) +
            '\n%s' % (effect_scenery.name) +
            '\n%s' % (effect_scenery.path)
        )
        bit_string = ""
        for bit in effect_scenery.bits:
            bit_string += "%s " % int(bit)

        file.write('\n%s' % (bit_string))
        file.write('\n')

    for idx, shot in enumerate(QUA.shots):
        file.write(
            '\n; ### SHOT %s ###' % (idx + 1) +
            '\n;          <Ubercam position (vector)>' +
            '\n;          <Ubercam up (vector)>' +
            '\n;          <Ubercam forward (vector)>' +
            '\n;          <Horizontal field of view (float)>' +
            '\n;          <Horizontal film aperture (float, millimeters)>' +
            '\n;          <Focal Length (float)>' +
            '\n;          <Depth of Field (bool)>' +
            '\n;          <Near Focal Plane Distance (float)>' +
            '\n;          <Far Focal Plane Distance (float)>' +
            '\n;          <Focal Depth (float)>' +
            '\n;          <Blur Amount (float)>' +
            '\n%s' % (len(shot.frames))
        )

        for idx, frame in enumerate(shot.frames):
            file.write(
                '\n; FRAME %s' % (idx + 1) +
                decimal_3 % (frame.position) +
                decimal_3 % (frame.up) +
                decimal_3 % (frame.forward) +
                decimal_1 % (frame.fov) +
                decimal_1 % (frame.aperture) +
                decimal_1 % (frame.focal_length) +
                '\n%s' % (frame.depth_of_field) +
                decimal_1 % (frame.near_focal) +
                decimal_1 % (frame.far_focal) +
                decimal_1 % (frame.focal_depth) +
                decimal_1 % (frame.blur_amount) +
                '\n'
            )

        file.write(
            '\n;*** SHOT %s AUDIO DATA ***' % (idx + 1) +
            '\n%s' % (len(shot.audio_data)) +
            '\n;          <Audio filename (string)>' +
            '\n;          <Frame number (int)>' +
            '\n;          <Character (string)>\n'
        )

        for idx, audio in enumerate(shot.audio_data):
            file.write(
                '\n; AUDIO %s' % (idx) +
                '\n%s' % (audio.filepath) +
                '\n%s' % (audio.frame) +
                '\n%s\n' % (audio.name)
            )

    file.write(
        '\n;### EXTRA CAMERAS ###' +
        '\n%s' % (len(QUA.extra_cameras)) +
        '\n;          <Camera name (string)>' +
        '\n;          <Camera type (string)>\n'
    )

    for idx, extra_camera in enumerate(QUA.extra_cameras):
        file.write(
            '\n;### CAMERA %s ###' % (idx) +
            '\n%s' % (extra_camera.name) +
            '\n%s\n' % (extra_camera.camera_type)
        )

        for idx, extra_shot in enumerate(extra_camera.extra_shots):
            file.write(
                '\n; ### SHOT %s ###' % (idx + 1) +
                '\n;          <Camera enabled (bool)>' +
                '\n;          <Camera position (vector)>' +
                '\n;          <Camera up (vector)>' +
                '\n;          <Camera forward (vector)>' +
                '\n;          <Horizontal field of view (float)>' +
                '\n;          <Focal Length (float)>' +
                '\n;          <Depth of Field (bool)>' +
                '\n;          <Near Focal Plane Distance (float)>' +
                '\n;          <Far Focal Plane Distance (float)>' +
                '\n;          <Focal Depth (float)>' +
                '\n;          <Blur Amount (float)>'
            )

            for idx, frame in enumerate(extra_shot.frames):
                file.write(
                    '\n; FRAME %s' % (idx + 1) +
                    '\n%s' % (int(frame.camera_is_enabled)) +
                    decimal_3 % (frame.position) +
                    decimal_3 % (frame.up) +
                    decimal_3 % (frame.forward) +
                    decimal_1 % (frame.fov) +
                    decimal_1 % (frame.focal_length) +
                    '\n%s' % (frame.depth_of_field) +
                    decimal_1 % (frame.near_focal) +
                    decimal_1 % (frame.far_focal) +
                    decimal_1 % (frame.focal_depth) +
                    decimal_1 % (frame.blur_amount) +
                    '\n'
                )

    report({'INFO'}, "Export completed successfully")
    file.close()
