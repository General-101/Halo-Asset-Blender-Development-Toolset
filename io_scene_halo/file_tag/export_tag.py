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
import json

from ..global_functions import global_functions
from ..file_tag.tag_interface.tag_definitions import h1, h2
from ..file_tag.tag_interface import tag_interface, tag_common
from .h1.file_scenario.process_scene import generate_scenario_scene

def write_file(context, file_path, report):
    donor_scnr = None
    game_title = "halo1"

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

    if tags_directory in file_path and os.path.isfile(file_path):
        if not global_functions.string_empty_check(tags_directory):
            result = file_path.split(tags_directory, 1)
            if len(result) > 1:
                local_path, tag_extension = result[1].rsplit(".", 1)
                tag_group = tag_extensions.get(tag_extension)
                tag_ref = {"group name": tag_group, "path": local_path}

                donor_scnr = tag_interface.read_tag(tag_ref, tags_directory, tag_groups, engine_tag, merged_defs)

            else:
                report({'ERROR'}, "Invalid input provided. Check your tag directory settings and make sure the file exists in your tag directory.")
        else:
            report({'ERROR'}, "Invalid tag directory path provided. Check your tag directory settings.")

    filename_no_ext = file_path.rsplit('.scenario', 1)[0]
    filepath = "%s%s" % (filename_no_ext, "_blender.scenario")

    scnr_dict = generate_scenario_scene(context, donor_scnr, file_path)
    with open(r"C:\Users\Steven\Desktop\shader_stuff.json", 'w', encoding='utf8') as json_file:
        json.dump(scnr_dict, json_file, ensure_ascii=True, indent=4)

    tag_interface.write_file(merged_defs, scnr_dict, tag_interface.obfuscation_buffer_prepare(), filepath, engine_tag)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_scene.scenario()
