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
DECIMAL_1 = '\n%s'
DECIMAL_2 = '\n%s %s'
DECIMAL_3 = '\n%s %s %s'
DECIMAL_4 = '\n%s %s %s %s'

def write_legacy_header(file, QUA):
    file.write(
        ';### VERSION ###' +
        '\n%s\n' % (QUA.version)
    )

    file.write(
        '\n;### SCENE ###' +
        '\n;      <scene name (string)>' +
        '\n%s\n' % (QUA.scene_name)
    )

def write_header(file, QUA):
    file.write(
        ';### VERSION ###' +
        '\n%s\n' % (QUA.version)
    )

    file.write(
        '\n;### SCENE TYPE ###' +
        '\n%s\n' % (QUA.scene_type)
    )

    file.write(
        '\n;### MAIN SCENE VERSION ###' +
        '\n%s\n' % (QUA.scene_version)
    )

    file.write(
        '\n;### SCENE ###' +
        '\n;      <scene name (string)>' +
        '\n%s\n' % (QUA.scene_name)
    )

def write_shots(file, QUA):
    file.write(
        '\n;### SHOTS ###' +
        '\n%s\n' % (len(QUA.shots))
    )

def write_legacy_objects(file, QUA):
    file.write(
        '\n;### UNITS ###' +
        '\n%s' % (len(QUA.units)) +
        '\n;      <export name (string)>' +
        '\n;      <export path (string)>' +
        '\n;      <shots visible (bit mask - sorta)>\n'
    )

    for unit_idx, unit in enumerate(QUA.units):
        file.write(
            '\n; UNIT %s' % (unit_idx) +
            '\n%s' % (unit.export_name) +
            '\n%s' % (unit.object_path)
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

    for scenery_idx, scenery in enumerate(QUA.scenery):
        file.write(
            '\n; SCENERY %s' % (scenery_idx) +
            '\n%s' % (scenery.export_name) +
            '\n%s' % (scenery.object_path)
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

    for effect_scenery_idx, effect_scenery in enumerate(QUA.effects_scenery):
        file.write(
            '\n; EFFECTS_SCENERY %s' % (effect_scenery_idx) +
            '\n%s' % (effect_scenery.export_name) +
            '\n%s' % (effect_scenery.object_path)
        )
        bit_string = ""
        for bit in effect_scenery.bits:
            bit_string += "%s " % int(bit)

        file.write('\n%s' % (bit_string))
        file.write('\n')

def write_objects(file, QUA):
    file.write(
        '\n;### OBJECTS ###' +
        '\n%s' % (len(QUA.objects)) +
        '\n;      <export name (string)>' +
        '\n;      <animation id (string)>' +
        '\n;      <animation graph tag path>' +
        '\n;      <object type tag path>' +
        '\n;      <shots visible (bit mask - sorta)>\n'
    )

    for ob_idx, ob in enumerate(QUA.objects):
        file.write(
            '\n; OBJECT %s' % (ob.export_name) +
            '\n%s' % (ob.export_name) +
            '\n%s' % (ob.animation_id) +
            '\n%s' % (ob.animation_path) +
            '\n%s' % (ob.object_path)
        )
        bit_string = ""
        for bit in ob.bits:
            bit_string += "%s " % int(bit)

        file.write('\n%s' % (bit_string))
        file.write('\n')

def write_h3_frames(file, QUA):
    for shot_idx, shot in enumerate(QUA.shots):
        file.write(
            '\n; ### SHOT %s ###' % (shot_idx + 1) +
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

        for frame_idx, frame in enumerate(shot.frames):
            file.write(
                '\n; FRAME %s' % (frame_idx + 1) +
                DECIMAL_3 % (frame.position) +
                DECIMAL_3 % (frame.up) +
                DECIMAL_3 % (frame.forward) +
                DECIMAL_1 % (frame.fov) +
                DECIMAL_1 % (frame.aperture) +
                DECIMAL_1 % (frame.focal_length) +
                '\n%s' % (frame.depth_of_field) +
                DECIMAL_1 % (frame.near_focal) +
                DECIMAL_1 % (frame.far_focal) +
                DECIMAL_1 % (frame.focal_depth) +
                DECIMAL_1 % (frame.blur_amount) +
                '\n'
            )

        file.write(
            '\n;*** SHOT %s AUDIO DATA ***' % (shot_idx + 1) +
            '\n%s' % (len(shot.audio_data)) +
            '\n;          <Audio filename (string)>' +
            '\n;          <Frame number (int)>' +
            '\n;          <Character (string)>\n'
        )

        for audio_idx, audio in enumerate(shot.audio_data):
            file.write(
                '\n; AUDIO %s' % (audio_idx) +
                '\n%s' % (audio.audio_filename) +
                '\n%s' % (audio.frame) +
                '\n%s\n' % (audio.character)
            )

    file.write(
        '\n;### EXTRA CAMERAS ###' +
        '\n%s' % (len(QUA.extra_cameras)) +
        '\n;          <Camera name (string)>' +
        '\n;          <Camera type (string)>\n'
    )

    for extra_camera_idx, extra_camera in enumerate(QUA.extra_cameras):
        file.write(
            '\n;### CAMERA %s ###' % (extra_camera_idx) +
            '\n%s' % (extra_camera.name) +
            '\n%s\n' % (extra_camera.camera_type)
        )

        for extra_shot_idx, extra_shot in enumerate(extra_camera.extra_shots):
            file.write(
                '\n; ### SHOT %s ###' % (extra_shot_idx + 1) +
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

            for frame_idx, frame in enumerate(extra_shot.frames):
                file.write(
                    '\n; FRAME %s' % (frame_idx + 1) +
                    '\n%s' % (int(frame.camera_is_enabled)) +
                    DECIMAL_3 % (frame.position) +
                    DECIMAL_3 % (frame.up) +
                    DECIMAL_3 % (frame.forward) +
                    DECIMAL_1 % (frame.fov) +
                    DECIMAL_1 % (frame.focal_length) +
                    '\n%s' % (frame.depth_of_field) +
                    DECIMAL_1 % (frame.near_focal) +
                    DECIMAL_1 % (frame.far_focal) +
                    DECIMAL_1 % (frame.focal_depth) +
                    DECIMAL_1 % (frame.blur_amount) +
                    '\n'
                )

def write_hr_frames(file, QUA):
    for shot_idx, shot in enumerate(QUA.shots):
        file.write(
            '\n; ### SHOT %s ###' % (shot_idx + 1) +
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

        for frame_idx, frame in enumerate(shot.frames):
            file.write(
                '\n; FRAME %s' % (frame_idx + 1) +
                DECIMAL_3 % (frame.position) +
                DECIMAL_3 % (frame.up) +
                DECIMAL_3 % (frame.forward) +
                DECIMAL_1 % (frame.fov) +
                DECIMAL_1 % (frame.aperture) +
                DECIMAL_1 % (frame.focal_length) +
                '\n%s' % (frame.depth_of_field) +
                DECIMAL_1 % (frame.near_focal) +
                DECIMAL_1 % (frame.far_focal) +
                DECIMAL_1 % (frame.focal_depth) +
                DECIMAL_1 % (frame.blur_amount) +
                '\n'
            )

        file.write(
            '\n;*** SHOT %s AUDIO DATA ***' % (shot_idx + 1) +
            '\n%s' % (len(shot.audio_data)) +
            '\n;          <Audio filename (string)>' +
            '\n;          <Female audio filename (string)>' +
            '\n;          <Frame number (int)>' +
            '\n;          <Character (string)>' +
            '\n;          <Dialog Color (string)>\n'
        )

        for audio_idx, audio in enumerate(shot.audio_data):
            file.write(
                '\n; AUDIO %s' % (audio_idx) +
                '\n%s' % (audio.audio_filename) +
                '\n%s' % (audio.female_audio_filename) +
                '\n%s' % (audio.frame) +
                '\n%s' % (audio.character) +
                '\n%s\n' % (audio.dialog_color)
            )

        file.write(
            '\n;*** SHOT %s CUSTOM SCRIPT DATA ***' % (shot_idx + 1) +
            '\n%s' % (len(shot.custom_script_data)) +
            '\n;          <Node ID (long)>' +
            '\n;          <Sequence ID (long)>' +
            '\n;          <Script (string)>' +
            '\n;          <Frame number (int)>\n'
        )

        for custom_script_idx, custom_script in enumerate(shot.custom_script_data):
            file.write(
                '\n%s' % (custom_script.node_id) +
                '\n%s' % (custom_script.sequence_id) +
                '\n%s' % (custom_script.script) +
                '\n%s' % (custom_script.frame)
            )

        file.write(
            '\n;*** SHOT %s EFFECT DATA ***' % (shot_idx + 1) +
            '\n%s' % (len(shot.effect_data)) +
            '\n;          <Node ID (long)>' +
            '\n;          <Sequence ID (long)>' +
            '\n;          <Effect (string)>' +
            '\n;          <Marker Name (string)>' +
            '\n;          <Marker Parent (string)>' +
            '\n;          <Frame number (int)>\n'
        )

        for effect_idx, effect in enumerate(shot.effect_data):
            file.write(
                '\n; EFFECT %s' % (effect_idx) +
                '\n%s' % (effect.node_id) +
                '\n%s' % (effect.sequence_id) +
                '\n%s' % (effect.effect) +
                '\n%s' % (effect.marker_name) +
                '\n%s' % (effect.marker_parent) +
                '\n%s\n' % (effect.frame)
            )

    file.write(
        '\n;### EXTRA CAMERAS ###' +
        '\n%s' % (len(QUA.extra_cameras)) +
        '\n;          <Camera name (string)>' +
        '\n;          <Camera type (string)>\n'
    )

    for extra_camera_idx, extra_camera in enumerate(QUA.extra_cameras):
        file.write(
            '\n;### CAMERA %s ###' % (extra_camera_idx) +
            '\n%s' % (extra_camera.name) +
            '\n%s\n' % (extra_camera.camera_type)
        )

        for extra_shot_idx, extra_shot in enumerate(extra_camera.extra_shots):
            file.write(
                '\n; ### SHOT %s ###' % (extra_shot_idx + 1) +
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

            for frame_idx, frame in enumerate(extra_shot.frames):
                file.write(
                    '\n; FRAME %s' % (frame_idx + 1) +
                    '\n%s' % (int(frame.camera_is_enabled)) +
                    DECIMAL_3 % (frame.position) +
                    DECIMAL_3 % (frame.up) +
                    DECIMAL_3 % (frame.forward) +
                    DECIMAL_1 % (frame.fov) +
                    DECIMAL_1 % (frame.focal_length) +
                    '\n%s' % (frame.depth_of_field) +
                    DECIMAL_1 % (frame.near_focal) +
                    DECIMAL_1 % (frame.far_focal) +
                    DECIMAL_1 % (frame.focal_depth) +
                    DECIMAL_1 % (frame.blur_amount) +
                    '\n'
                )

def write_h4_frames(file, QUA, is_segment=False):
    for shot_idx, shot in enumerate(QUA.shots):
        if not is_segment:
            file.write(
                '\n; ### SHOT %s ###' % (shot_idx + 1) +
                '\n;          <Ubercam position (vector)>' +
                '\n;          <Ubercam up (vector)>' +
                '\n;          <Ubercam forward (vector)>' +
                '\n;          <Focal Length (float)>' +
                '\n;          <Depth of Field (bool)>' +
                '\n;          <Near Focal Plane Distance (float)>' +
                '\n;          <Far Focal Plane Distance (float)>' +
                '\n;          <Near Focal Depth (float)>' +
                '\n;          <Far Focal Depth (float)>' +
                '\n;          <Near Blur Amount (float)>' +
                '\n;          <Far Blur Amount (float)>' +
                '\n%s' % (len(shot.frames))
            )

            for frame_idx, frame in enumerate(shot.frames):
                file.write(
                    '\n; FRAME %s' % (frame_idx + 1) +
                    DECIMAL_3 % (frame.position) +
                    DECIMAL_3 % (frame.up) +
                    DECIMAL_3 % (frame.forward) +
                    DECIMAL_1 % (frame.focal_length) +
                    '\n%s' % (frame.depth_of_field) +
                    DECIMAL_1 % (frame.near_focal) +
                    DECIMAL_1 % (frame.far_focal) +
                    DECIMAL_1 % (frame.near_focal_depth) +
                    DECIMAL_1 % (frame.far_focal_depth) +
                    DECIMAL_1 % (frame.near_blur_amount) +
                    DECIMAL_1 % (frame.far_blur_amount) +
                    '\n'
                )

            file.write(
                '\n;*** SHOT %s AUDIO DATA ***' % (shot_idx + 1) +
                '\n%s' % (len(shot.audio_data)) +
                '\n;          <Sound tag (string)>' +
                '\n;          <Female sound tag (string)>' +
                '\n;          <Audio filename (string)>' +
                '\n;          <Female audio filename (string)>' +
                '\n;          <Frame number (int)>' +
                '\n;          <Character (string)>' +
                '\n;          <Dialog Color (string)>\n'
            )

            for audio_idx, audio in enumerate(shot.audio_data):
                file.write(
                    '\n; AUDIO %s' % (audio_idx) +
                    '\n%s' % (audio.sound_tag) +
                    '\n%s' % (audio.female_sound_tag) +
                    '\n%s' % (audio.audio_filename) +
                    '\n%s' % (audio.female_audio_filename) +
                    '\n%s' % (audio.frame) +
                    '\n%s' % (audio.character) +
                    '\n%s\n' % (audio.dialog_color)
                )

        file.write(
            '\n;*** SHOT %s CUSTOM SCRIPT DATA ***' % (shot_idx + 1) +
            '\n%s' % (len(shot.custom_script_data)) +
            '\n;          <Node ID (long)>' +
            '\n;          <Sequence ID (long)>' +
            '\n;          <Script (string)>' +
            '\n;          <Frame number (int)>\n'
        )

        for custom_script_idx, custom_script in enumerate(shot.custom_script_data):
            file.write(
                '\n; CUSTOM SCRIPT %s' % (custom_script_idx) +
                '\n%s' % (custom_script.node_id) +
                '\n%s' % (custom_script.sequence_id) +
                '\n%s' % (custom_script.script) +
                '\n%s\n' % (custom_script.frame)
            )

        file.write(
            '\n;*** SHOT %s EFFECT DATA ***' % (shot_idx + 1) +
            '\n%s' % (len(shot.effect_data)) +
            '\n;          <Node ID (long)>' +
            '\n;          <Sequence ID (long)>' +
            '\n;          <Effect (string)>' +
            '\n;          <Marker Name (string)>' +
            '\n;          <Marker Parent (string)>' +
            '\n;          <Frame number (int)>' +
            '\n;          <Effect State (int)>' +
            '\n;          <Size Scale (float)>' +
            '\n;          <Function A (string)>' +
            '\n;          <Function B (string)>' +
            '\n;          <Looping (long)>\n'
        )

        for effect_idx, effect in enumerate(shot.effect_data):
            file.write(
                '\n; EFFECT %s' % (effect_idx) +
                '\n%s' % (effect.node_id) +
                '\n%s' % (effect.sequence_id) +
                '\n%s' % (effect.effect) +
                '\n%s' % (effect.marker_name) +
                '\n%s' % (effect.marker_parent) +
                '\n%s' % (effect.frame) +
                '\n%s' % (effect.effect_state) +
                '\n%s' % (effect.size_scale) +
                '\n%s' % (effect.function_a) +
                '\n%s' % (effect.function_b) +
                '\n%s\n' % (effect.looping)
            )

    if not is_segment:
        file.write(
            '\n;### EXTRA CAMERAS ###' +
            '\n%s' % (len(QUA.extra_cameras)) +
            '\n;          <Camera name (string)>' +
            '\n;          <Camera type (string)>\n'
        )

        for extra_camera_idx, extra_camera in enumerate(QUA.extra_cameras):
            file.write(
                '\n;### CAMERA %s ###' % (extra_camera_idx) +
                '\n%s' % (extra_camera.name) +
                '\n%s\n' % (extra_camera.camera_type)
            )

            for extra_shot_idx, extra_shot in enumerate(extra_camera.extra_shots):
                file.write(
                    '\n; ### SHOT %s ###' % (extra_shot_idx + 1) +
                    '\n;          <Camera enabled (bool)>' +
                    '\n;          <Camera position (vector)>' +
                    '\n;          <Camera up (vector)>' +
                    '\n;          <Camera forward (vector)>' +
                    '\n;          <Focal Length (float)>' +
                    '\n;          <Depth of Field (bool)>' +
                    '\n;          <Near Focal Plane Distance (float)>' +
                    '\n;          <Far Focal Plane Distance (float)>' +
                    '\n;          <Near Focal Depth (float)>' +
                    '\n;          <Far Focal Depth (float)>' +
                    '\n;          <Near Blur Amount (float)>' +
                    '\n;          <Far Blur Amount (float)>'
                )

                for frame_idx, frame in enumerate(extra_shot.frames):
                    file.write(
                        '\n; FRAME %s' % (frame_idx + 1) +
                        '\n%s' % (int(frame.camera_is_enabled)) +
                        DECIMAL_3 % (frame.position) +
                        DECIMAL_3 % (frame.up) +
                        DECIMAL_3 % (frame.forward) +
                        DECIMAL_1 % (frame.focal_length) +
                        '\n%s' % (frame.depth_of_field) +
                        DECIMAL_1 % (frame.near_focal) +
                        DECIMAL_1 % (frame.far_focal) +
                        DECIMAL_1 % (frame.near_focal_depth) +
                        DECIMAL_1 % (frame.far_focal_depth) +
                        DECIMAL_1 % (frame.near_blur_amount) +
                        DECIMAL_1 % (frame.far_blur_amount) +
                        '\n'
                    )

def build_asset(context, filepath, game_title, qua_version, qua_type, qua_revision, strip_identifier, hidden_geo, nonrender_geo, report):
    QUA = process_scene(context, game_title, qua_version, qua_type, qua_revision, strip_identifier, hidden_geo, nonrender_geo, report)

    file = open(filepath, 'w', encoding="utf-8")

    if game_title == "halo3":
        write_legacy_header(file, QUA)
        write_shots(file, QUA)
        write_legacy_objects(file, QUA)
        write_h3_frames(file, QUA)
    
    elif game_title == "halor":
        write_legacy_header(file, QUA)
        write_shots(file, QUA)
        write_objects(file, QUA)
        write_hr_frames(file, QUA)

    elif game_title == "halo4":
        if qua_type == "main":
            write_header(file, QUA)
            write_shots(file, QUA)
            write_objects(file, QUA)
            write_h4_frames(file, QUA)
        else:
            write_header(file, QUA)
            write_shots(file, QUA)
            write_h4_frames(file, QUA, True)

    report({'INFO'}, "Export completed successfully")
    file.close()
