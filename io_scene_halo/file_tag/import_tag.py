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

from .build_scene import build_mesh
from .build_scene import build_physics
from .build_scene import build_animations
from .build_scene import build_collision
from .build_scene import build_bsp
from .build_scene import build_lightmap
from .build_scene import build_scenario
from .build_scene import build_camera_track
from .build_scene import build_shader

from ..global_functions import global_functions
from ..file_tag.tag_interface.tag_definitions import h1, h2
from ..file_tag.tag_interface import tag_interface, tag_common


def load_file(context, file_path, game_title, fix_rotations, empty_markers, report):
    with open(file_path, 'rb') as input_stream:
        asset_cache = {}

        if game_title == "auto":
            valid_header, tag_group, checksum, engine_tag = tag_interface.check_header(input_stream)
            if engine_tag == "blam":
                game_title = "halo1"
            else:
                game_title = "halo2"

        tag_groups = None
        tag_extensions = None
        engine_tag = None
        merged_defs = None
        tags_directory = ""
        
        if game_title == "halo1":
            output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h1_merged_output")
            tag_groups = tag_common.h1_tag_groups
            tag_extensions = tag_common.h1_tag_extensions
            engine_tag = tag_interface.EngineTag.H1Latest.value
            merged_defs = h1.generate_defs(tag_common.h1_defs_directory, output_dir)
            tags_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_tag_path
            
        elif game_title == "halo2":
            output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h2_merged_output")
            tag_groups = tag_common.h2_tag_groups
            tag_extensions = tag_common.h2_tag_extensions
            engine_tag = tag_interface.EngineTag.H2Latest.value
            merged_defs = h2.generate_defs(tag_common.h2_defs_directory, output_dir)
            tags_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path
        else:
            print("%s is not supported." % game_title)

        if not global_functions.string_empty_check(tags_directory):
            result = file_path.split(tags_directory, 1)
            if len(result) > 1:
                local_path, tag_extension = result[1].rsplit(".", 1)
                tag_group = tag_extensions.get(tag_extension)
                tag_ref = {"group name": tag_group, "path": local_path}

                tag_interface.generate_tag_dictionary(game_title, tag_ref, tags_directory, tag_groups, engine_tag, merged_defs, asset_cache)

                context.scene.halo.game_title = game_title
                
                if game_title == "halo1":
                    shader_groups = ("senv", "soso", "schi", "scex", "sotr", "sgla", "smet", "spla", "swat")

                elif game_title == "halo2":
                    shader_groups = ("shad")

                else:
                    input_stream.close()
                    report({'ERROR'}, "Not implemented")

                    return {'CANCELLED'}

                build_scene = None
                if tag_group == "mode" or tag_group == "mod2":
                    build_scene = build_mesh

                elif tag_group == "coll":
                    build_scene = build_collision

                elif tag_group == "phys":
                    build_scene = build_physics

                elif tag_group == "antr":
                    build_scene = build_animations

                elif tag_group == "sbsp":
                    build_scene = build_bsp

                elif tag_group == "ltmp":
                    build_scene = build_lightmap

                elif tag_group == "scnr":
                    context.scene.tag_scenario.scenario_path = file_path
                    build_scene = build_scenario

                elif tag_group == "trak":
                    build_scene = build_camera_track

                elif tag_group in shader_groups:
                    build_scene = build_shader

                input_stream.close()
                if build_scene:
                    build_scene.build_scene(context, tag_ref, asset_cache, game_title, fix_rotations, empty_markers, report)
                else:
                    report({'ERROR'}, "Tag file has no support. Contact the plugin author if it should.")

            else:
                report({'ERROR'}, "Invalid input provided. Check your tag directory settings and make sure the file exists in your tag directory.")
        else:
            report({'ERROR'}, "Invalid tag directory path provided. Check your tag directory settings.")