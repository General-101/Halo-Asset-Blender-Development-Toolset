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

from ..global_functions import tag_format, mesh_processing, global_functions

from ..file_tag.file_model import build_scene as build_scene_model
from ..file_tag.file_physics import build_scene as build_scene_physics
from ..file_tag.file_animation import build_scene as build_scene_animation
from ..file_tag.file_collision import build_scene as build_scene_collision
from ..file_tag.file_structure_bsp import build_scene as build_scene_level
from ..file_tag.file_structure_lightmap import build_scene as build_scene_lightmap
from ..file_tag.file_scenario import build_scene as build_scenario
from ..file_tag.file_camera_track import build_scene as build_camera_track
from ..file_tag.file_model.h1.process_file_mode_retail import process_file_mode_retail as process_mode
from ..file_tag.file_model.h1.process_file_mod2_retail import process_file_mod2_retail as process_mod2
from ..file_tag.file_collision.h1.process_file_retail import process_file_retail as process_collision_retail
from ..file_tag.file_collision.h2.process_file import process_file as process_h2_collision
from ..file_tag.file_physics.process_file_retail import process_file_retail as process_physics_retail
from ..file_tag.file_animation.h1.process_file_retail import process_file_retail as process_h1_animation_retail
from ..file_tag.file_structure_bsp.h1.process_file_retail import process_file_retail as process_level_retail
from .file_structure_bsp.h2.process_file_retail import process_file_retail as process_h2_level
from ..file_tag.file_structure_lightmap.h2.process_file_retail import process_file_retail as process_h2_lightmap

from .file_scenario.h1.process_file_retail import process_file_retail as process_h1_scenario
from .file_scenario.h2.process_file_retail import process_file as process_h2_scenario
from ..file_tag.file_camera_track.process_file_retail import process_file_retail as process_camera_track_retail

def load_file(context, file_path, game_title, fix_rotations, empty_markers, report):
    input_stream = open(file_path, "rb")
    if tag_format.check_file_size(input_stream) < 64: # Size of the header for all tags
        input_stream.close()
        report({'ERROR'}, "File size does not meet the minimum amount required. File is either not a tag or corrupted")

        return {'CANCELLED'}

    is_big_endian = True
    if not game_title == "halo1":
        is_big_endian = False

    tag_group, group_is_valid = tag_format.check_group(input_stream, is_big_endian)
    if not group_is_valid:
        input_stream.close()
        print(file_path)
        print(tag_group)
        report({'ERROR'}, "File does not have a valid tag class. Make sure you are importing a tag supported by the toolset")

        return {'CANCELLED'}

    if tag_group == "mode" or tag_group == "mod2":
        build_scene = build_scene_model
        if game_title == "halo1":
            if tag_group == "mode":
                ASSET = process_mode(input_stream, tag_format, report)

            else:
                ASSET = process_mod2(input_stream, tag_format, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}

    elif tag_group == "coll" or tag_group == "col2":
        build_scene = build_scene_collision
        if game_title == "halo1":
            ASSET = process_collision_retail(input_stream, tag_format, report)

        elif game_title == "halo2":
            ASSET = process_h2_collision(input_stream, tag_format, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}

    elif tag_group == "phys":
        build_scene = build_scene_physics
        if game_title == "halo1":
            ASSET = process_physics_retail(input_stream, tag_format, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}

    elif tag_group == "antr":
        build_scene = build_scene_animation
        if game_title == "halo1":
            ASSET = process_h1_animation_retail(input_stream, global_functions, tag_format, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}


    elif tag_group == "sbsp":
        build_scene = build_scene_level
        if game_title == "halo1":
            ASSET = process_level_retail(input_stream, tag_format, report)

        elif game_title == "halo2":
            ASSET = process_h2_level(input_stream, tag_format, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}

    elif tag_group == "ltmp":
        build_scene = build_scene_lightmap
        ASSET = process_h2_lightmap(input_stream, tag_format, report)


    elif tag_group == "scnr":
        context.scene.halo_tag.game_title = game_title
        context.scene.halo_tag.scenario_path = file_path
        build_scene = build_scenario
        if game_title == "halo1":
            ASSET = process_h1_scenario(input_stream, tag_format, report)

        elif game_title == "halo2":
            ASSET = process_h2_scenario(input_stream, tag_format, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}

    elif tag_group == "trak":
        build_scene = build_camera_track
        if game_title == "halo1":
            ASSET = process_camera_track_retail(input_stream, tag_format, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}

    else:
        input_stream.close()
        report({'ERROR'}, "Not implemented")

        return {'CANCELLED'}

    input_stream.close()
    build_scene.build_scene(context, ASSET, "retail", game_title, 0, fix_rotations, empty_markers, report, mesh_processing, global_functions, tag_format)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.model()
