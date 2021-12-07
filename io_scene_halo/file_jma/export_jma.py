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

from ..global_functions import mesh_processing
from ..global_functions import global_functions

class JMAScene(global_functions.HaloAsset):
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

    def __init__(self, context, report, version, generate_checksum, game_version, extension, custom_scale, biped_controller, fix_rotations):
        global_functions.unhide_all_collections(context)
        object_properties = []
        object_list = list(context.scene.objects)
        node_list = []
        armature = []
        armature_count = 0
        first_frame = context.scene.frame_start
        last_frame = context.scene.frame_end + 1
        total_frame_count = context.scene.frame_end - first_frame + 1
        for obj in object_list:
            object_properties.append([obj.hide_get(), obj.hide_viewport])
            if obj.type == 'ARMATURE' and mesh_processing.set_ignore(obj) == False:
                mesh_processing.unhide_object(obj)
                armature_count += 1
                armature = obj
                mesh_processing.select_object(context, obj)
                node_list = list(obj.data.bones)

        self.transform_count = total_frame_count
        #actor related items are hardcoded due to them being an unused feature in tool. Do not attempt to do anything to write this out as it is a waste of time and will get you nothing.
        self.actor_names = ['unnamedActor']
        self.node_count = len(node_list)
        self.transforms = []
        self.biped_controller_transforms = []
        self.nodes = []

        sorted_list = global_functions.sort_list(node_list, armature, game_version, version, False)
        joined_list = sorted_list[0]
        reversed_joined_list = sorted_list[1]

        blend_scene = global_functions.BlendScene(0, armature_count, 0, 0, 0, 0, armature, node_list, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
        global_functions.validate_halo_jma_scene(game_version, version, blend_scene, object_list, extension)

        self.node_checksum = 0
        for node in joined_list:
            name = node.name
            find_child_node = global_functions.get_child(node, reversed_joined_list)
            find_sibling_node = global_functions.get_sibling(armature, node, reversed_joined_list)
            first_child_node = -1
            first_sibling_node = -1
            parent_node = -1
            if not find_child_node == None:
                first_child_node = joined_list.index(find_child_node)

            if not find_sibling_node == None:
                first_sibling_node = joined_list.index(find_sibling_node)

            if not node.parent == None:
                parent_node = joined_list.index(node.parent)

            self.nodes.append(JMAScene.Node(name, parent_node, first_child_node, first_sibling_node))

        if generate_checksum:
            self.node_checksum = global_functions.node_hierarchy_checksum(self.nodes, self.nodes[0], self.node_checksum)

        for frame in range(first_frame, last_frame):
            transforms_for_frame = []
            for node in joined_list:
                context.scene.frame_set(frame)
                is_bone = False
                if armature:
                    is_bone = True

                bone_matrix = global_functions.get_matrix(node, node, True, armature, joined_list, True, version, 'JMA', False, custom_scale, fix_rotations)
                mesh_dimensions = global_functions.get_dimensions(bone_matrix, node, version, is_bone, 'JMA', custom_scale)
                rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
                translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])
                scale = (mesh_dimensions.scale[0])

                transforms_for_frame.append(JMAScene.Transform(translation, rotation, scale))

            self.transforms.append(transforms_for_frame)

        #H2 specific biped controller data bool value.
        if version > 16394 and biped_controller:
            for frame in range(self.transform_count):
                context.scene.frame_set(frame)
                armature_matrix = global_functions.get_matrix(armature, armature, True, None, joined_list, False, version, 'JMA', False, custom_scale, fix_rotations)
                mesh_dimensions = global_functions.get_dimensions(armature_matrix, armature, version, False, 'JMA', custom_scale)

                rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
                translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])
                scale = (mesh_dimensions.scale[0])

                self.biped_controller_transforms.append(JMAScene.Transform(translation, rotation, scale))

        context.scene.frame_set(1)
        for idx, obj in enumerate(object_list):
            property_value = object_properties[idx]
            obj.hide_set(property_value[0])
            obj.hide_viewport = property_value[1]

def write_file(context, filepath, report, extension, extension_ce, extension_h2, extension_h3, jma_version, jma_version_ce, jma_version_h2, jma_version_h3, generate_checksum, custom_frame_rate, frame_rate_float, biped_controller, folder_structure, scale_enum, scale_float, console, game_version, fix_rotations):
    version = global_functions.get_version(jma_version, jma_version_ce, jma_version_h2, jma_version_h3, game_version, console)
    extension = global_functions.get_extension(extension, extension_ce, extension_h2, extension_h3, game_version, console)
    custom_scale = global_functions.set_scale(scale_enum, scale_float)
    if custom_frame_rate == 'CUSTOM':
        frame_rate_value = frame_rate_float

    else:
        frame_rate_value = int(custom_frame_rate)


    jma_scene = JMAScene(context, report, version, generate_checksum, game_version, extension, custom_scale, biped_controller, fix_rotations)

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

    filename = os.path.basename(filepath)

    root_directory = global_functions.get_directory(context, game_version, "animations", folder_structure, "0", False, filepath)

    file = open(root_directory + os.sep + filename + global_functions.get_true_extension(filepath, extension, False), 'w', encoding='utf_8')

    #write header
    if version >= 16394:
        file.write(
            '%s' % (version) +
            '\n%s' % (jma_scene.node_checksum) +
            '\n%s' % (jma_scene.transform_count) +
            '\n%s' % (frame_rate_value) +
            '\n%s' % (len(jma_scene.actor_names)) +
            '\n%s' % (jma_scene.actor_names[0]) +
            '\n%s' % (jma_scene.node_count)
            )

    else:
        file.write(
            '%s' % (version) +
            '\n%s' % (jma_scene.transform_count) +
            '\n%s' % (frame_rate_value) +
            '\n%s' % (len(jma_scene.actor_names)) +
            '\n%s' % (jma_scene.actor_names[0]) +
            '\n%s' % (jma_scene.node_count) +
            '\n%s' % (jma_scene.node_checksum)
            )

    if version >= 16391:
            for node in jma_scene.nodes:
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
    for node_transform in jma_scene.transforms:
        for node in node_transform:
            file.write(
                decimal_3 % (node.vector[0], node.vector[1], node.vector[2]) +
                decimal_4 % (node.rotation[0], node.rotation[1], node.rotation[2], node.rotation[3]) +
                decimal_1 % (node.scale)
                )

    #H2 specific biped controller data bool value.
    if version > 16394:
        file.write('\n%s' % (int(biped_controller)))
        if biped_controller:
            for biped_transform in jma_scene.biped_controller_transforms:
                file.write(
                    decimal_3 % (biped_transform.vector[0], biped_transform.vector[1], biped_transform.vector[2]) +
                    decimal_4 % (biped_transform.rotation[0], biped_transform.rotation[1], biped_transform.rotation[2], biped_transform.rotation[3]) +
                    decimal_1 % (biped_transform.scale)
                    )

    file.write('\n')
    file.close()
    report({'INFO'}, "Export completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_jma.export()
