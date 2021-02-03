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

import bpy
import sys
import traceback

from io_scene_halo.global_functions import global_functions

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

    def __init__(self, context, report, version, game_version, extension, custom_scale, biped_controller, vertex_group_sort):
        global_functions.unhide_all_collections()
        scene = bpy.context.scene
        view_layer = bpy.context.view_layer
        object_properties = []
        object_list = list(scene.objects)
        object_count = len(object_list)
        node_list = []
        armature = []
        armature_count = 0
        first_frame = scene.frame_start
        last_frame = scene.frame_end + 1
        total_frame_count = scene.frame_end - first_frame + 1
        for obj in object_list:
            object_properties.append([obj.hide_get(), obj.hide_viewport])
            if obj.type == 'ARMATURE':
                global_functions.unhide_object(obj)
                armature_count += 1
                armature = obj
                view_layer.objects.active = obj
                obj.select_set(True)
                node_list = list(obj.data.bones)

        self.transform_count = total_frame_count
        #actor related items are hardcoded due to them being an unused feature in tool. Do not attempt to do anything to write this out as it is a waste of time and will get you nothing.
        self.actor_names = ['unnamedActor']
        self.node_count = len(node_list)
        self.transforms = []
        self.biped_controller_transforms = []
        self.nodes = []
        root_node_count = global_functions.count_root_nodes(node_list)
        h2_extension_list = ['JRMX', 'JMH']
        dae_object = None
        if vertex_group_sort:
            for object in object_list:
                if object.type == 'MESH' and not object.name[0:1].lower() == '#' and not object in node_list:
                    if object.parent in node_list or object.parent == armature:
                        dae_object = object
                        break

        sorted_list = global_functions.sort_list(node_list, armature, game_version, version, False, vertex_group_sort, dae_object)
        joined_list = sorted_list[0]
        reversed_joined_list = sorted_list[1]

        if self.node_count == 0:
            raise global_functions.SceneParseError("No nodes in scene. Add an armature or object mesh named frame.")

        elif armature_count >= 2:
            raise global_functions.SceneParseError("More than one armature object. Please delete all but one.")

        elif root_node_count >= 2:
            raise global_functions.SceneParseError("More than one root node. Please remove or rename objects until you only have one root frame object.")

        elif len(object_list) == 0:
            raise global_functions.SceneParseError("No objects in scene.")

        elif extension in h2_extension_list and game_version == 'haloce':
            raise global_functions.SceneParseError("This extension is not used in Halo CE.")

        elif version >= 16393 and game_version == 'haloce':
            raise global_functions.SceneParseError("This version is not supported for Halo CE. Choose from 16390-16392 if you wish to export for Halo CE.")

        elif game_version == 'haloce' and self.node_count > 64:
            raise global_functions.SceneParseError("This model has more nodes than Halo CE supports. Please limit your node count to 64 nodes")

        elif game_version == 'halo2' and self.node_count > 255:
            raise global_functions.SceneParseError("This model has more nodes than Halo 2 supports. Please limit your node count to 255 nodes")

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

        self.node_checksum = global_functions.node_hierarchy_checksum(self.nodes, self.nodes[0], self.node_checksum)

        for frame in range(first_frame, last_frame):
            transforms_for_frame = []
            for node in joined_list:
                bpy.context.scene.frame_set(frame)
                is_bone = False
                if armature:
                    is_bone = True

                bone_matrix = global_functions.get_matrix(node, node, True, armature, joined_list, True, version, 'JMA', 0)
                mesh_dimensions = global_functions.get_dimensions(bone_matrix, node, None, None, custom_scale, version, None, False, is_bone, armature, 'JMA')
                vector = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
                rotation = (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a)
                scale = (mesh_dimensions.scale_x_a)

                transforms_for_frame.append(JMAScene.Transform(vector, rotation, scale))

            self.transforms.append(transforms_for_frame)

        #H2 specific biped controller data bool value.
        if version > 16394 and biped_controller:
            for frame in range(self.transform_count):
                bpy.context.scene.frame_set(frame)
                armature_matrix = global_functions.get_matrix(armature, armature, True, None, joined_list, False, version, 'JMA', 0)
                mesh_dimensions = global_functions.get_dimensions(armature_matrix, armature, None, None, custom_scale, version, None, False, False, armature, 'JMA')

                vector = (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
                rotation = (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a)
                scale = (mesh_dimensions.scale_x_a)

                self.biped_controller_transforms.append(JMAScene.Transform(vector, rotation, scale))

        scene.frame_set(1)
        for idx, obj in enumerate(object_list):
            property_value = object_properties[idx]
            obj.hide_set(property_value[0])
            obj.hide_viewport = property_value[1]

def write_file(context,
               filepath,
               report,
               extension,
               extension_ce,
               extension_h2,
               jma_version,
               jma_version_ce,
               jma_version_h2,
               custom_frame_rate,
               frame_rate_float,
               biped_controller,
               vertex_group_sort,
               scale_enum,
               scale_float,
               console,
               game_version,
               encoding
               ):

    version = global_functions.get_version(jma_version,
                                           jma_version_ce,
                                           jma_version_h2,
                                           game_version,
                                           console
                                           )

    extension = global_functions.get_extension(extension,
                                               extension_ce,
                                               extension_h2,
                                               game_version,
                                               console
                                               )

    custom_scale = global_functions.set_scale(scale_enum, scale_float)
    if custom_frame_rate == 'CUSTOM':
        frame_rate_value = frame_rate_float

    else:
        frame_rate_value = int(custom_frame_rate)


    jma_scene = JMAScene(context, report, version, game_version, extension, custom_scale, biped_controller, vertex_group_sort)

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

    file = open(filepath + global_functions.get_true_extension(filepath, extension, False), 'w', encoding=encoding)
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
