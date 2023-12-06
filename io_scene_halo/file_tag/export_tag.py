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
from .h1.file_scenario.process_scene import generate_scenario_scene
from .h1.file_scenario.build_asset import build_asset as build_h1_scenario
from .h1.file_scenario.process_file import process_file as process_h1_scenario

def write_file(context, file_path, report):
    DONOR_ASSET = None
    if os.path.isfile(file_path):
        input_stream = open(file_path, "rb")
        if tag_format.check_file_size(input_stream) < 64: # Size of the header for all tags
            input_stream.close()
            report({'ERROR'}, "File size does not meet the minimum amount required. File is either not a tag or corrupted")

            return {'CANCELLED'}

        is_big_endian = True

        tag_group, group_is_valid = tag_format.check_group(input_stream, is_big_endian)
        if not group_is_valid:
            input_stream.close()
            report({'ERROR'}, "File does not have a valid tag class. Make sure you are importing a tag supported by the toolset")

            return {'CANCELLED'}

        DONOR_ASSET = process_h1_scenario(input_stream, report)

    filename_no_ext = file_path.rsplit('.scenario', 1)[0]
    filepath = "%s%s" % (filename_no_ext, "_blender.scenario")
    output_stream = open(filepath, 'wb')
    BLENDER_ASSET = generate_scenario_scene(DONOR_ASSET)
    build_h1_scenario(output_stream, BLENDER_ASSET, report)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_scene.scenario()
