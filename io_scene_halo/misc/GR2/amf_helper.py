# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Crisp
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
from ...file_gr2.nwo_utils import dot_partition

def amf_assign(context, report):
    # Loop through scene objects and apply appropriate perm / region names
    loop_count = 0
    for ob in context.view_layer.objects:
        true_name = dot_partition(ob.name)
        if not true_name.startswith(('+', ':')) and ':' in true_name:
            if true_name.rpartition(':')[0] != '':
                ob.nwo.Region_Name = true_name.rpartition(':')[0]
            if true_name.rpartition(':')[2] != '':
                ob.nwo.Permutation_Name = true_name.rpartition(':')[2]
            loop_count += 1

    report({'INFO'},f"Updated regions & permutations for {loop_count} AMF objects")

    return {'FINISHED'}

