# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2020 Steven Garcia
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

from ..file_jma import import_jma
from ..global_functions import global_functions

class JMAFile(global_functions.HaloAsset):
    class Transform:
        def __init__(self, vector, rotation, scale):
            self.vector = vector
            self.rotation = rotation
            self.scale = scale

    class Node:
        def __init__(self, name, parent=None, child=None, sibling=None):
            self.name = name
            self.parent = parent
            self.child = child
            self.sibling = sibling

    def __init__(self, context, version, game_version, jma_asset):
        node_list = jma_asset.nodes

        #actor related items are hardcoded due to them being an unused feature in tool. Do not attempt to do anything to write this out as it is a waste of time and will get you nothing.
        self.actor_names = ['unnamedActor']
        self.node_count = len(node_list)
        self.transforms = []
        self.biped_controller_transforms = []
        self.nodes = []

        sorted_list = global_functions.sort_list_batch(node_list, game_version, version, True)
        joined_list = sorted_list[0]
        reversed_joined_list = sorted_list[1]

        self.node_checksum = 0
        for node in joined_list:
            name = node.name
            find_child_node = global_functions.get_child_batch(node, reversed_joined_list, node_list)
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

            self.nodes.append(JMAFile.Node(name, parent_node, first_child_node, first_sibling_node))

        self.node_checksum = global_functions.node_hierarchy_checksum(self.nodes, self.nodes[0], self.node_checksum)

        for frame in range(jma_asset.frame_count):
            transforms_for_frame = []
            for node_idx, node in enumerate(joined_list):
                absolute_matrix = []
                if jma_asset.version < 16394:
                    absolute_matrix = global_functions.get_absolute_matrix(node_list, frame, jma_asset.transforms)

                transform = global_functions.get_transform(jma_asset.version, version, node, frame, node_list, jma_asset.transforms, absolute_matrix)

                pos, rot, scale = transform.decompose()
                quat = rot.inverted()
                if version >= 16394:
                    quat = rot

                quaternion = (quat[1], quat[2], quat[3], quat[0])
                transforms_for_frame.append(JMAFile.Transform(pos, quaternion, scale[0]))

            self.transforms.append(transforms_for_frame)

        #H2 specific biped controller data bool value.
        if version == 16395 and len(jma_asset.biped_controller_transforms) > 0:
            for frame in range(self.transform_count):
                transform = jma_asset.biped_controller_transforms[frame]

                self.biped_controller_transforms.append(JMAFile.Transform(transform.vector, transform.rotation, transform.scale))


def write_file(context, report, directory, jma_version, jma_version_ce, jma_version_h2, jma_version_h3, game_version):
    version = global_functions.get_version(jma_version, jma_version_ce, jma_version_h2, jma_version_h3, game_version, False)
    extension_list = ('.jma', '.jmm', '.jmt', '.jmo', '.jmr', '.jmrx', '.jmh', '.jmz', '.jmw')
    if not os.path.exists(bpy.path.abspath(directory)):
        report({'ERROR'}, "Invalid directory path")
        return {'CANCELLED'}

    for file_item in os.listdir(directory):
        if file_item.lower().endswith(extension_list):
            imported_jma_file = import_jma.JMAAsset(os.path.join(directory, file_item), game_version, report)
            if not imported_jma_file.broken_skeleton:
                exported_jma_file = JMAFile(context, version, game_version, imported_jma_file)

                if version > 16394:
                    decimal_1 = '\n%0.10f'
                    decimal_2 = '\n%0.10f\t%0.10f'
                    decimal_3 = '\n%0.10f\t%0.10f\t%0.10f'
                    decimal_4 = '\n%0.10f\t%0.10f\t%0.10f\t%0.10f'

                else:
                    decimal_1 = '\n%0.6f'
                    decimal_2 = '\n%0.6f\t%0.6f'
                    decimal_3 = '\n%0.6f\t%0.6f\t%0.6f'
                    decimal_4 = '\n%0.6f\t%0.6f\t%0.6f\t%0.6f'

                filename = os.path.basename(file_item)

                file = open(os.path.join(directory, file_item), 'w', encoding='utf_8')

                #write header
                if version >= 16394:
                    file.write(
                        '%s' % (version) +
                        '\n%s' % (exported_jma_file.node_checksum) +
                        '\n%s' % (imported_jma_file.frame_count) +
                        '\n%s' % (int(imported_jma_file.frame_rate)) +
                        '\n%s' % (1) +
                        '\n%s' % (imported_jma_file.actor_name) +
                        '\n%s' % (len(imported_jma_file.nodes))
                        )

                else:
                    file.write(
                        '%s' % (version) +
                        '\n%s' % (imported_jma_file.frame_count) +
                        '\n%s' % (int(imported_jma_file.frame_rate)) +
                        '\n%s' % (1) +
                        '\n%s' % (imported_jma_file.actor_name) +
                        '\n%s' % (len(imported_jma_file.nodes)) +
                        '\n%s' % (exported_jma_file.node_checksum)
                        )

                if version >= 16391:
                        for node in exported_jma_file.nodes:
                            if version >= 16394:
                                file.write(
                                    '\n%s' % (node.name) +
                                    '\n%s' % (node.parent)
                                    )

                            else:
                                file.write('\n%s' % (node.name))
                                if version >= 16392:
                                    file.write(
                                        '\n%s' % (node.child) +
                                        '\n%s' % (node.sibling)
                                        )

                #write transforms
                for node_transform in exported_jma_file.transforms:
                    for node in node_transform:
                        file.write(
                            decimal_3 % (node.vector[0], node.vector[1], node.vector[2]) +
                            decimal_4 % (node.rotation[0], node.rotation[1], node.rotation[2], node.rotation[3]) +
                            decimal_1 % (node.scale)
                            )

                #H2 specific biped controller data bool value.
                if version > 16394:
                    file.write('\n%s' % (int(len(exported_jma_file.biped_controller_transforms) > 0)))
                    if len(exported_jma_file.biped_controller_transforms) > 0:
                        for biped_transform in exported_jma_file.biped_controller_transforms:
                            file.write(
                                decimal_3 % (biped_transform.vector[0], biped_transform.vector[1], biped_transform.vector[2]) +
                                decimal_4 % (biped_transform.rotation[0], biped_transform.rotation[1], biped_transform.rotation[2], biped_transform.rotation[3]) +
                                decimal_1 % (biped_transform.scale)
                                )

                file.write('\n')
                file.close()

    report({'INFO'}, "Conversion completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_jma.export()
