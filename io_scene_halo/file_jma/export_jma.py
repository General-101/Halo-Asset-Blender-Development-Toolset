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

from io_scene_halo.global_functions import global_functions

def write_file(context,
               filepath,
               report,
               extension,
               extension_ce,
               extension_h2,
               jma_version,
               jma_version_ce,
               jma_version_h2,
               game_version,
               custom_frame_rate,
               frame_rate_float,
               biped_controller,
               scale_enum,
               scale_float,
               console):

    global_functions.unhide_all_collections()
    scene = bpy.context.scene
    view_layer = bpy.context.view_layer
    object_properties = []
    object_list = list(scene.objects)
    object_count = len(object_list)
    node_list = []
    armature = []
    armature_count = 0
    root_node_count = 0
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

    version = global_functions.get_version(jma_version, jma_version_ce, jma_version_h2, game_version, console)
    node_checksum = 0
    scale = global_functions.set_scale(scale_enum, scale_float)
    transform_count = total_frame_count
    if custom_frame_rate == 'CUSTOM':
        frame_rate_value = frame_rate_float

    else:
        frame_rate_value = int(custom_frame_rate)

    frame_rate = frame_rate_value
    #actor related items are hardcoded due to them being an unused feature in tool. Do not attempt to do anything to write this out as it is a waste of time and will get you nothing.
    actor_count = 1
    actor_name = 'unnamedActor'
    node_count = len(node_list)
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

    if global_functions.error_pass(armature_count, report, game_version, node_count, version, extension, None, None, root_node_count, True, None, object_count):
        return {'CANCELLED'}

    joined_list = global_functions.sort_list(node_list, armature, False, game_version, version, True)
    reversed_joined_list = global_functions.sort_list(node_list, armature, True, game_version, version, True)
    file = open(filepath + global_functions.get_true_extension(filepath, extension, False), 'w', encoding='%s' % global_functions.get_encoding(game_version))
    #write header
    if version >= 16394:
        file.write(
            '%s' % (version) +
            '\n%s' % (node_checksum) +
            '\n%s' % (transform_count) +
            '\n%s' % (frame_rate) +
            '\n%s' % (actor_count) +
            '\n%s' % (actor_name) +
            '\n%s' % (node_count)
            )

    else:
        file.write(
            '%s' % (version) +
            '\n%s' % (transform_count) +
            '\n%s' % (frame_rate) +
            '\n%s' % (actor_count) +
            '\n%s' % (actor_name) +
            '\n%s' % (node_count) +
            '\n%s' % (node_checksum)
            )

    #write nodes
    for node in joined_list:
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

        if version >= 16394:
            file.write(
                '\n%s' % (node.name) +
                '\n%s' % (parent_node)
                )

        else:
            file.write(
                '\n%s' % (node.name) +
                '\n%s' % (first_child_node) +
                '\n%s' % (first_sibling_node)
                )

    #write transforms
    for frame in range(first_frame, last_frame):
        for node in joined_list:
            bpy.context.scene.frame_set(frame)
            is_bone = False
            if armature:
                is_bone = True

            bone_matrix = global_functions.get_matrix(node, node, True, armature, joined_list, True, version, True)
            mesh_dimensions = global_functions.get_dimensions(bone_matrix, node, None, None, -1, scale, version, None, False, is_bone, armature, True)
            file.write(
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
                decimal_4 % (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a) +
                decimal_1 % (mesh_dimensions.scale_x_a)
                )

    #H2 specific biped controller data bool value.
    if version > 16394:
        biped_controller_attached = 0
        if biped_controller:
            biped_controller_attached = 1

        file.write(
            '\n%s' % (biped_controller_attached)
            )

        #Explanation for this found in closed issue #15 on the Git. Seems to do nothing in our toolset so no way to test this to properly port.
        if biped_controller:
            for i in range(transform_count):
                file.write(
                    decimal_3 % (0, 0, 0) +
                    decimal_4 % (0, 0, 0, 1) +
                    decimal_1 % (1)
                    )

    file.write(
        '\n'
        )

    scene.frame_set(1)
    file.close()
    for obj in object_list:
        item_index = object_list.index(obj)
        property_value = object_properties[item_index]
        obj.hide_set(property_value[0])
        obj.hide_viewport = property_value[1]

    report({'INFO'}, "Export completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_jma.export()
