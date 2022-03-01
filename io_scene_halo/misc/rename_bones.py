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

import re
import bpy

def rename_bones(context):
    node_prefix_tuple = ('b ', 'b_', 'bone ','bone_', 'frame ','frame_', 'bip01 ', 'bip01_')
    blender_style = (".l", ".r")
    halo_style = ("l ", "r ", "l_", "r_")

    active_object = context.view_layer.objects.active

    if not active_object == None and active_object.type == 'ARMATURE':
        style_type = 1
        for bone in active_object.data.bones:
            if bone.name.lower().endswith(blender_style):
                style_type = 0

        for bone in active_object.data.bones:
            prefix_index = 6
            bone_side_index = None
            bone_name = bone.name
            if style_type == 0:
                if bone.name.lower().startswith(node_prefix_tuple):
                    for prefix in node_prefix_tuple:
                        if bone.name.lower().startswith(prefix):
                            prefix_index = node_prefix_tuple.index(prefix)
                            prefix_letter_list = list(prefix)
                            prefix_limiter = ''
                            for letter in prefix_letter_list:
                                prefix_limiter += ("[{}]".format(letter))
                            bone_name = re.split(prefix_limiter, bone.name, flags=re.IGNORECASE)[1]
                            for style in blender_style:
                                if bone_name.lower().endswith(style):
                                    style_letter_list = list(style)
                                    style_limiter = ''
                                    for letter in style_letter_list:
                                        style_limiter += ("[{}]".format(letter))
                                    bone_name = re.split(style_limiter, bone_name, flags=re.IGNORECASE)[0]
                                    bone_side_index = blender_style.index(style)
                else:
                    for style in blender_style:
                        if bone.name.lower().endswith(style):
                            style_letter_list = list(style)
                            style_limiter = ''
                            for letter in style_letter_list:
                                style_limiter += ("[{}]".format(letter))
                            bone_name = re.split(style_limiter, bone.name, flags=re.IGNORECASE)[0]
                            bone_side_index = blender_style.index(style)

                if not bone_side_index == None:
                    bone.name = node_prefix_tuple[prefix_index] + halo_style[bone_side_index] + bone_name

            elif style_type == 1:
                if bone.name.lower().startswith(node_prefix_tuple):
                    for prefix in node_prefix_tuple:
                        if bone.name.lower().startswith(prefix):
                            prefix_index = node_prefix_tuple.index(prefix)
                            prefix_letter_list = list(prefix)
                            prefix_limiter = ''
                            for letter in prefix_letter_list:
                                prefix_limiter += ("[{}]".format(letter))
                            bone_name = re.split(prefix_limiter, bone.name, flags=re.IGNORECASE)[-1]
                            for style in halo_style:
                                if bone_name.lower().startswith(style):
                                    bone_name = re.split(style, bone_name, flags=re.IGNORECASE)[-1]
                                    bone_side_index = halo_style.index(style)
                else:
                    for style in halo_style:
                        if bone_name.lower().startswith(style):
                            style_letter_list = list(style)
                            style_limiter = ''
                            for letter in style_letter_list:
                                style_limiter += ("[{}]".format(letter))
                            bone_name = re.split(style_limiter, bone.name, flags=re.IGNORECASE)[-1]
                            bone_side_index = halo_style.index(style)

                if not bone_side_index == None:
                    if bone_side_index > 1:
                        bone_side_index = bone_side_index - 2

                    bone.name = node_prefix_tuple[prefix_index] + bone_name + blender_style[bone_side_index]

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.bulk_bone_names()
