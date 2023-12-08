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

from ..global_functions import tag_format

from .build_scene import build_mesh as build_scene_model
from .build_scene import build_physics as build_scene_physics
from .build_scene import build_animations as build_scene_animation
from .build_scene import build_collision as build_scene_collision
from .build_scene import build_bsp as build_scene_level
from .build_scene import build_lightmap as build_scene_lightmap
from .build_scene import build_scenario as build_scenario
from .build_scene import build_camera_track as build_camera_track

from .h1.file_model.process_file import process_file as process_mode
from .h1.file_gbxmodel.process_file import process_file as process_mod2

from .h1.file_model_collision_geometry.process_file import process_file as process_collision
from .h2.file_collision_model.process_file import process_file as process_h2_collision

from .h1.file_physics.process_file import process_file as process_physics
from .h1.file_model_animations.process_file import process_file as process_h1_animation

from .h1.file_scenario_structure_bsp.process_file import process_file as process_level
from .h2.file_scenario_structure_bsp.process_file import process_file as process_h2_level
from .h2.file_scenario_structure_lightmap.process_file import process_file as process_h2_lightmap

from .h1.file_scenario.process_file import process_file as process_h1_scenario
from .h2.file_scenario.process_file import process_file as process_h2_scenario

from .h1.file_camera_track.process_file import process_file as process_camera_track

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
                ASSET = process_mode(input_stream, report)

            else:
                ASSET = process_mod2(input_stream, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}

    elif tag_group == "coll":
        build_scene = build_scene_collision
        if game_title == "halo1":
            ASSET = process_collision(input_stream, report)

        elif game_title == "halo2":
            ASSET = process_h2_collision(input_stream, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}

    elif tag_group == "phys":
        build_scene = build_scene_physics
        if game_title == "halo1":
            ASSET = process_physics(input_stream, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}

    elif tag_group == "antr":
        build_scene = build_scene_animation
        if game_title == "halo1":
            ASSET = process_h1_animation(input_stream, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}

    elif tag_group == "sbsp":
        build_scene = build_scene_level
        if game_title == "halo1":
            ASSET = process_level(input_stream, report)

        elif game_title == "halo2":
            ASSET = process_h2_level(input_stream, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}

    elif tag_group == "ltmp":
        build_scene = build_scene_lightmap
        if game_title == "halo2":
            ASSET = process_h2_lightmap(input_stream, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}

    elif tag_group == "scnr":
        context.scene.halo.game_title = game_title
        context.scene.halo_tag.scenario_path = file_path
        build_scene = build_scenario
        if game_title == "halo1":
            ASSET = process_h1_scenario(input_stream, report)

        elif game_title == "halo2":
            ASSET = process_h2_scenario(input_stream, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}

    elif tag_group == "trak":
        build_scene = build_camera_track
        if game_title == "halo1":
            ASSET = process_camera_track(input_stream, report)

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

            return {'CANCELLED'}

    else:
        input_stream.close()
        report({'ERROR'}, "Not implemented")

        return {'CANCELLED'}

    input_stream.close()
    build_scene.build_scene(context, ASSET, "retail", game_title, 0, fix_rotations, empty_markers, report)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.model()
