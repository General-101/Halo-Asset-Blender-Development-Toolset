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

from ..file_jma.format import JMAAsset
from ..global_functions import global_functions
from ..file_jma.process_file_retail import process_file_retail
from ..file_jma.build_asset import build_asset

def generate_jma_data(context, jma_version, game_version, imported_jma_file):
    JMA = JMAAsset()

    JMA.version = jma_version
    JMA.frame_rate = imported_jma_file.frame_rate
    JMA.frame_count = imported_jma_file.frame_count
    JMA.actor_names = ['unnamedActor'] # Actor values are hardcoded and unused as they are in the official exporter. Leave as is.
    JMA.broken_skeleton = imported_jma_file.broken_skeleton
    JMA.node_checksum = -1
    JMA.node_count = imported_jma_file.node_count
    JMA.biped_controller_frame_type = imported_jma_file.biped_controller_frame_type
    JMA.nodes = []
    JMA.transforms = []
    JMA.biped_controller_transforms = []

    sorted_list = global_functions.sort_list_batch(imported_jma_file.nodes, game_version, jma_version, True)
    joined_list = sorted_list[0]
    reversed_joined_list = sorted_list[1]

    JMA.node_checksum = 0
    for node in joined_list:
        name = node.name
        find_child_node = global_functions.get_child_batch(node, reversed_joined_list, imported_jma_file.nodes)
        find_sibling_node = global_functions.get_sibling_batch(node, reversed_joined_list)

        first_child_node = -1
        first_sibling_node = -1
        parent_node = -1
        if find_child_node and not find_child_node == -1:
            first_child_node = joined_list.index(find_child_node)

        if find_sibling_node and not find_sibling_node == -1:
            first_sibling_node = joined_list.index(find_sibling_node)

        if not node.parent == None and not node.parent == -1:
            parent_node = node.parent

        JMA.nodes.append(JMAAsset.Node(name, parent_node, first_child_node, first_sibling_node))

    JMA.node_checksum = global_functions.node_hierarchy_checksum(JMA.nodes, JMA.nodes[0], JMA.node_checksum)

    for frame in range(imported_jma_file.frame_count):
        transforms_for_frame = []
        for node_idx, node in enumerate(joined_list):
            absolute_matrix = []
            if imported_jma_file.version < 16394:
                absolute_matrix = global_functions.get_absolute_matrix(imported_jma_file.nodes, frame, imported_jma_file.transforms)

            transform = global_functions.get_transform(imported_jma_file.version, jma_version, node, frame, imported_jma_file.nodes, imported_jma_file.transforms, absolute_matrix)

            pos, rot, scale = transform.decompose()
            quat = rot.inverted()
            if jma_version >= 16394:
                quat = rot

            quaternion = (quat[1], quat[2], quat[3], quat[0])
            transforms_for_frame.append(JMAAsset.Transform(pos, quaternion, scale[0]))

        JMA.transforms.append(transforms_for_frame)

    #H2 specific biped controller data bool value.
    if jma_version == 16395 and len(imported_jma_file.biped_controller_transforms) > 0:
        for frame in range(JMA.frame_count):
            transform = imported_jma_file.biped_controller_transforms[frame]

            JMA.biped_controller_transforms.append(JMAAsset.Transform(transform.translation, transform.rotation, transform.scale))

    return JMA

def write_file(context, report, directory, jma_version, game_version):
    extension_list = ('.jma', '.jmm', '.jmt', '.jmo', '.jmr', '.jmrx', '.jmh', '.jmz', '.jmw')
    retail_version_list = (16390,16391,16392,16393,16394,16395)
    if not os.path.exists(bpy.path.abspath(directory)):
        report({'ERROR'}, "Invalid directory path")
        return {'CANCELLED'}

    for file_item in os.listdir(directory):
        if file_item.lower().endswith(extension_list):
            file_path = os.path.join(directory, file_item)
            extension = global_functions.get_true_extension(file_path, None, True)
            imported_jma_file = JMAAsset(file_path)
            JMA = process_file_retail(imported_jma_file, extension, game_version, retail_version_list, report)
            if not JMA.broken_skeleton:
                exported_jma_file = generate_jma_data(context, jma_version, game_version, JMA)
                build_asset(context, file_path.rsplit('.', 1)[0], report, ".%s" % extension.upper(), exported_jma_file.version, game_version, True, False, False, False, exported_jma_file.frame_rate, 1.0, exported_jma_file)

    report({'INFO'}, "Conversion completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_jma.export()
