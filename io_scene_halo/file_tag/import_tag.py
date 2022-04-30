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

import bpy

from ..global_functions import tag_format, mesh_processing, global_functions

from ..file_tag.file_model import build_scene as build_scene_model
from ..file_tag.file_physics import build_scene as build_scene_physics
from ..file_tag.file_animation import build_scene as build_scene_animation
from ..file_tag.file_collision import build_scene as build_scene_collision
from ..file_tag.file_structure_bsp import build_scene as build_scene_level
from ..file_tag.file_scenario import build_scene as build_scenario
from ..file_tag.file_camera_track import build_scene as build_camera_track

from ..file_tag.file_model.process_file_mode_retail import process_file_mode_retail as process_mode
from ..file_tag.file_model.process_file_mod2_retail import process_file_mod2_retail as process_mod2

from ..file_tag.file_collision.h1.process_file_retail import process_file_retail as process_collision_retail
from ..file_tag.file_collision.h2.process_file import process_file as process_h2_collision

from ..file_tag.file_physics.process_file_retail import process_file_retail as process_physics_retail

from ..file_tag.file_animation.process_file_retail import process_file_retail as process_animation_retail

from ..file_tag.file_structure_bsp.h1.process_file_retail import process_file_retail as process_level_retail
from ..file_tag.file_structure_bsp.h2.process_file import process_file_retail as process_h2_level

from ..file_tag.file_scenario.h2.process_file import process_file as process_scenario

from ..file_tag.file_camera_track.process_file_retail import process_file_retail as process_camera_track_retail

def load_file(context, file_path, fix_rotations, report):
    input_stream = open(file_path, "rb")
    if tag_format.check_file_size(input_stream) < 64: # Size of the header for all tags
        input_stream.close()
        report({'ERROR'}, "File size does not meet the minimum amount required. File is either not a tag or corrupted")

        return {'CANCELLED'}

    tag_group, group_is_valid = tag_format.check_group(input_stream)
    if not group_is_valid:
        input_stream.close()
        report({'ERROR'}, "File does not have a valid tag class. Make sure you are importing a tag supported by the toolset")

        return {'CANCELLED'}

    if tag_group == "mode" or tag_group == "mod2":
        build_scene = build_scene_model
        if tag_group == "mode":
            ASSET = process_mode(input_stream, tag_format, report)

        else:
            ASSET = process_mod2(input_stream, tag_format, report)

    elif tag_group == "coll":
        build_scene = build_scene_collision
        ASSET = process_collision_retail(input_stream, tag_format, report)

    elif tag_group == "lloc":
        build_scene = build_scene_collision
        ASSET = process_h2_collision(input_stream, tag_format, report)

    elif tag_group == "phys":
        build_scene = build_scene_physics
        ASSET = process_physics_retail(input_stream, tag_format, report)

    elif tag_group == "antr":
        build_scene = build_scene_animation
        ASSET = process_animation_retail(input_stream, tag_format, report)

    elif tag_group == "sbsp":
        build_scene = build_scene_level
        ASSET = process_level_retail(input_stream, tag_format, report)

    elif tag_group == "psbs":
        build_scene = build_scene_level
        ASSET = process_h2_level(input_stream, tag_format, report)

    elif tag_group == "trak":
        build_scene = build_camera_track
        ASSET = process_camera_track_retail(input_stream, tag_format, report)

    else:
        input_stream.close()
        report({'ERROR'}, "Not implemented")

        return {'CANCELLED'}

    input_stream.close()
    build_scene.build_scene(context, ASSET, fix_rotations, report, mesh_processing, global_functions)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.model()
