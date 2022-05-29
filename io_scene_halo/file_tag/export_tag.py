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

from ..file_tag.file_scenario.h2.build_asset import build_asset as build_scenario
from ..file_tag.file_scenario.h2.process_json import process_json
from ..global_functions import tag_format, mesh_processing, global_functions


def write_file(context, filepath, report):
    scenario_path = filepath.rsplit('.', 1)[0]
    input_stream = open(filepath, 'r')
    output_stream = open(scenario_path + ".scenario", 'wb')
    
    ASSET = process_json(input_stream, tag_format, report)

    build_scenario(output_stream, ASSET, report)
    output_stream.close()
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_scene.tag()
