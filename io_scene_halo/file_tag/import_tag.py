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
from .h2.file_render_model.process_file import process_file as process_h2_mode

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
from .h2.file_camera_track.process_file import process_file as process_h2_camera_track

from ..file_tag.h1.file_shader_environment.process_file import process_file as process_shader_environment
from ..file_tag.h1.file_shader_model.process_file import process_file as process_shader_model
from ..file_tag.h1.file_shader_transparent_chicago.process_file import process_file as process_shader_transparent_chicago
from ..file_tag.h1.file_shader_transparent_chicago_extended.process_file import process_file as process_shader_transparent_chicago_extended
from ..file_tag.h1.file_shader_transparent_generic.process_file import process_file as process_shader_transparent_generic
from ..file_tag.h1.file_shader_transparent_glass.process_file import process_file as process_shader_transparent_glass
from ..file_tag.h1.file_shader_transparent_meter.process_file import process_file as process_shader_transparent_meter
from ..file_tag.h1.file_shader_transparent_plasma.process_file import process_file as process_shader_transparent_plasma
from ..file_tag.h1.file_shader_transparent_water.process_file import process_file as process_shader_transparent_water

from ..global_functions.shader_processing import generate_shader_transparent_glass
from ..global_functions.shader_processing import generate_shader_transparent_meter
from ..global_functions.shader_generation.shader_environment import generate_shader_environment
from ..global_functions.shader_generation.shader_model import generate_shader_model

def load_file(context, file_path, game_title, fix_rotations, empty_markers, report):
    tag_name = os.path.basename(file_path).rsplit(".", 1)[0]
    input_stream = open(file_path, "rb")
    if tag_format.check_file_size(input_stream) < 64: # Size of the header for all tags
        input_stream.close()
        report({'ERROR'}, "File size does not meet the minimum amount required. File is either not a tag or corrupted")

        return {'CANCELLED'}

    if game_title == "auto":
        tag_group, group_is_valid, engine_tag = tag_format.check_group(input_stream, True)
        if engine_tag == "blam":
            game_title = "halo1"
        else:
            game_title = "halo2"

    is_big_endian = True
    if not game_title == "halo1":
        is_big_endian = False

    tag_group, group_is_valid, engine_tag = tag_format.check_group(input_stream, is_big_endian)
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

        elif game_title == "halo2":
            ASSET = process_h2_mode(input_stream, report)

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
            ASSET = process_h2_camera_track(input_stream, report)

    elif tag_group == "senv":
        build_scene = None
        ASSET = process_shader_environment(input_stream, report)
        mat = bpy.data.materials.new(name=tag_name)
        generate_shader_environment(mat, ASSET, 0, report)

    elif tag_group == "soso":
        build_scene = None
        ASSET = process_shader_model(input_stream, report)
        mat = bpy.data.materials.new(name=tag_name)
        generate_shader_model(mat, ASSET, report)

    #elif tag_group == "schi":
        #generate_shader_transparent_chicago(mat, shader, report)

    #elif tag_group == "scex":
        #generate_shader_transparent_chicago_extended(mat, shader, report)

    #elif tag_group == "sotr":
        #generate_shader_transparent_generic(mat, shader, report)

    elif tag_group == "sgla":
        build_scene = None
        ASSET = process_shader_transparent_glass(input_stream, report)
        mat = bpy.data.materials.new(name=tag_name)
        generate_shader_transparent_glass(mat, ASSET, report)

    elif tag_group == "smet":
        build_scene = None
        ASSET = process_shader_transparent_meter(input_stream, report)
        mat = bpy.data.materials.new(name=tag_name)
        generate_shader_transparent_meter(mat, ASSET, report)

    #elif tag_group == "spla":
        #generate_shader_transparent_plasma(mat, shader, report)

    #elif tag_group == "swat":
        #generate_shader_transparent_water(mat, shader, report)

    else:
        input_stream.close()
        report({'ERROR'}, "Not implemented")

        return {'CANCELLED'}

    input_stream.close()
    if build_scene:
        build_scene.build_scene(context, ASSET, "retail", game_title, 0, fix_rotations, empty_markers, report)

if __name__ == '__main__':
    bpy.ops.import_scene.model()
