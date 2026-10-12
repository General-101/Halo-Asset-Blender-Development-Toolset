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

from ..file_tag.tag_interface import tag_interface, tag_common

def convert_tag(context, input_file, source_game_title, target_game_title, tag_action, patch_txt_path, donor_tag, report):
    path_basename = os.path.basename(input_file)
    path_dirname = os.path.dirname(input_file)
    filename_no_ext = path_basename.rsplit('.', 1)[0]
    file_path = os.path.join(path_dirname, filename_no_ext)

    read_engine = tag_common.EngineTag.H1Latest.value
    tag_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_tag_path
    if source_game_title != "halo1":
        read_engine = tag_common.EngineTag.H2Latest.value
        tag_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path

    write_engine = tag_common.EngineTag.H1Latest.value
    if target_game_title != "halo1":
        write_engine = tag_common.EngineTag.H2Latest.value

    tag_interface.process_tag(input_file, tag_directory, read_engine, write_engine)

    return {'FINISHED'}
