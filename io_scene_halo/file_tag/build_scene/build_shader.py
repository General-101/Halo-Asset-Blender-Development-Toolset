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

from ...global_functions.shader_generation import halo_2_shader
from ...global_functions import shader_processing
from ...global_functions.shader_generation.shader_model import generate_shader_model
from ...global_functions.shader_generation.shader_environment import generate_shader_environment
from ...file_tag.tag_interface import tag_interface
from ...file_tag.tag_interface.tag_common import h1_tag_groups, h2_tag_groups

def build_scene(context, tag_ref, asset_cache, game_title, fix_rotations, empty_markers, report):
    tag_name = tag_ref["path"]
    tag_group = tag_ref["group name"]
    material_name = os.path.basename(tag_name)
    permutation_index = 0
    if game_title == "halo1":
        if tag_group == "senv":
            shader_asset = tag_interface.get_disk_asset(tag_name, h1_tag_groups.get(tag_group))
            mat = bpy.data.materials.new(name=material_name)
            if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                shader_processing.generate_shader_environment_simple(mat, shader_asset, permutation_index, asset_cache, report)
            else:
                generate_shader_environment(mat, shader_asset, permutation_index, asset_cache, report)

        elif tag_group == "soso":
            shader_asset = tag_interface.get_disk_asset(tag_name, h1_tag_groups.get(tag_group))
            mat = bpy.data.materials.new(name=material_name)
            if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                shader_processing.generate_shader_model_simple(mat, shader_asset, permutation_index, asset_cache, report)
            else:
                generate_shader_model(mat, shader_asset, permutation_index, asset_cache, report)

        elif tag_group == "schi":
            shader_asset = tag_interface.get_disk_asset(tag_name, h1_tag_groups.get(tag_group))
            mat = bpy.data.materials.new(name=material_name)
            if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                shader_processing.generate_shader_transparent_chicago_simple(mat, shader_asset, permutation_index, asset_cache, report)
            else:
                shader_processing.generate_shader_transparent_chicago_simple(mat, shader_asset, permutation_index, asset_cache, report)

        elif tag_group == "scex":
            shader_asset = tag_interface.get_disk_asset(tag_name, h1_tag_groups.get(tag_group))
            mat = bpy.data.materials.new(name=material_name)
            if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                shader_processing.generate_shader_transparent_chicago_extended_simple(mat, shader_asset, permutation_index, asset_cache, report)
            else:
                shader_processing.generate_shader_transparent_chicago_extended_simple(mat, shader_asset, permutation_index, asset_cache, report)

        elif tag_group == "sotr":
            shader_asset = tag_interface.get_disk_asset(tag_name, h1_tag_groups.get(tag_group))
            mat = bpy.data.materials.new(name=material_name)
            if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                shader_processing.generate_shader_transparent_generic_simple(mat, shader_asset, permutation_index, asset_cache, report)
            else:
                shader_processing.generate_shader_transparent_generic(mat, shader_asset, permutation_index, asset_cache, report)

        elif tag_group == "sgla":
            shader_asset = tag_interface.get_disk_asset(tag_name, h1_tag_groups.get(tag_group))
            mat = bpy.data.materials.new(name=material_name)
            if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                shader_processing.generate_shader_transparent_glass_simple(mat, shader_asset, permutation_index, asset_cache, report)
            else:
                shader_processing.generate_shader_transparent_glass(mat, shader_asset, permutation_index, asset_cache, report)

        elif tag_group == "smet":
            shader_asset = tag_interface.get_disk_asset(tag_name, h1_tag_groups.get(tag_group))
            mat = bpy.data.materials.new(name=material_name)
            if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                shader_processing.generate_shader_transparent_meter_simple(mat, shader_asset, permutation_index, asset_cache, report)
            else:
                shader_processing.generate_shader_transparent_meter(mat, shader_asset, permutation_index, asset_cache, report)

        elif tag_group == "spla":
            shader_asset = tag_interface.get_disk_asset(tag_name, h1_tag_groups.get(tag_group))
            mat = bpy.data.materials.new(name=material_name)
            if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                shader_processing.generate_shader_transparent_plasma_simple(mat, shader_asset, permutation_index, asset_cache, report)
            else:
                shader_processing.generate_shader_transparent_plasma_simple(mat, shader_asset, permutation_index, asset_cache, report)

        elif tag_group == "swat":
            shader_asset = tag_interface.get_disk_asset(tag_name, h1_tag_groups.get(tag_group))
            mat = bpy.data.materials.new(name=material_name)
            if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                shader_processing.generate_shader_transparent_water_simple(mat, shader_asset, permutation_index, asset_cache, report)
            else:
                shader_processing.generate_shader_transparent_water_simple(mat, shader_asset, permutation_index, asset_cache, report)

    else:
        if tag_group == "shad":
            shader_asset = tag_interface.get_disk_asset(tag_name, h2_tag_groups.get(tag_group))
            template_asset = tag_interface.get_disk_asset(shader_asset["Data"]["template"]["path"], h2_tag_groups.get(shader_asset["Data"]["template"]["group name"]))
            mat = bpy.data.materials.new(name=material_name)
            if int(bpy.context.preferences.addons["io_scene_halo"].preferences.shader_gen) == 1:
                halo_2_shader.generate_shader_simple(mat, shader_asset, asset_cache, report)
            else:
                halo_2_shader.generate_shader(mat, shader_asset, template_asset, asset_cache, report)
