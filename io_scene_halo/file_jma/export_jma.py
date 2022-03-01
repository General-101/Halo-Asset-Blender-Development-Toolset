# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2021 Steven Garcia
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

from .build_asset import build_asset
from ..global_functions import global_functions

def write_file(context, filepath, report, extension, extension_ce, extension_h2, extension_h3, jma_version, jma_version_ce, jma_version_h2, jma_version_h3, generate_checksum, custom_frame_rate, frame_rate_float, biped_controller, folder_structure, scale_enum, scale_float, console, game_version, fix_rotations):
    version = global_functions.get_version(jma_version, jma_version_ce, jma_version_h2, jma_version_h3, game_version, console)
    extension = global_functions.get_extension(extension, extension_ce, extension_h2, extension_h3, game_version, console)
    custom_scale = global_functions.set_scale(scale_enum, scale_float)
    if custom_frame_rate == 'CUSTOM':
        frame_rate_value = frame_rate_float

    else:
        frame_rate_value = int(custom_frame_rate)

    build_asset(context, filepath, extension, version, game_version, generate_checksum, frame_rate_value, fix_rotations, folder_structure, biped_controller, custom_scale)

    report({'INFO'}, "Export completed successfully")

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_jma.export()
