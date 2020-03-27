# ##### BEGIN UNLICENSED BLOCK #####
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>
#
# ##### END UNLICENSED BLOCK #####

import os
import bpy

from decimal import *
from random import seed
from math import degrees
from random import randint

def unhide_all_collections():
    for collection_viewport in bpy.context.view_layer.layer_collection.children:
        collection_viewport.hide_viewport = False

    for collection_hide in bpy.data.collections:
        collection_hide.hide_select = False
        collection_hide.hide_viewport = False
        collection_hide.hide_render = False

def unhide_all_objects():
    for obj in bpy.context.view_layer.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False
        obj.hide_render = False

def get_child(bone, bone_list = [], *args):
    for node in bone_list:
        if bone == node.parent:
            return node

def get_sibling(armature, bone, bone_list = [], *args):
    sibling_list = []
    for node in bone_list:
        if bone.parent == node.parent:
            sibling_list.append(node)

    if len(sibling_list) <= 1:
        return None

    else:
        sibling_node = sibling_list.index(bone)
        next_sibling_node = sibling_node + 1
        if next_sibling_node >= len(sibling_list):
            sibling = None

        else:
            if not armature:
                sibling = bpy.data.objects['%s' % sibling_list[next_sibling_node].name]

            else:
                sibling = armature.data.bones['%s' % sibling_list[next_sibling_node].name]

        return sibling

def get_region(default_region, region):
    if not len(region) == 0:
        return region

    else:
        return default_region

def get_permutation(default_permutation, permutation):
    if not len(permutation) == 0:
        return permutation

    else:
        return default_permutation

def get_default_region_permutation_name(game_version):
    if game_version == 'haloce':
        default_name = 'unnamed'

    elif game_version == 'halo2':
        default_name = 'Default'

    return default_name

def get_lod(lod_setting):
    if lod_setting == '0':
        LOD_name = 'L1'

    elif lod_setting == '1':
        LOD_name = 'L2'

    elif lod_setting == '2':
        LOD_name = 'L3'

    elif lod_setting == '3':
        LOD_name = 'L4'

    elif lod_setting == '4':
        LOD_name = 'L5'

    elif lod_setting == '5':
        LOD_name = 'L6'

    else:
        LOD_name = ''

    return LOD_name

def get_encoding(game_version):
    if game_version == 'haloce':
        encoding = 'utf_8'

    elif game_version == 'halo2':
        encoding = 'utf-16le'

    else:
        encoding = 'utf_8'

    return encoding

def error_pass(armature_count, report, game_version, node_count, version, extension, geometry_list, marker_list):
    if armature_count >= 2:
        report({'ERROR'}, 'More than one armature object. Please delete all but one.')
        return {'CANCELLED'}

    elif game_version == 'haloce' and node_count == 0: #JMSv2 files can have JMS files without a node for physics.
        report({'ERROR'}, 'No nodes in scene. Add an armature or object mesh named frame')
        return {'CANCELLED'}

    elif game_version == 'haloce' and len(geometry_list) == 0 and len(marker_list) == 0:
        report({'ERROR'}, 'No geometry in scene.')
        return {'CANCELLED'}

    elif version >= 8201 and game_version == 'haloce':
        report({'ERROR'}, 'This version is not supported for CE. Choose from 8197-8200 if you wish to export for CE.')
        return {'CANCELLED'}

    elif extension == '.JMP' and game_version == 'halo2':
        report({'ERROR'}, 'This extension is not used in Halo 2 Vista')
        return {'CANCELLED'}

def write_file(context, filepath, report, extension, jms_version, game_version, triangulate_faces):
    from . import JmsVertex
    from . import JmsTriangle

    unhide_all_collections()
    unhide_all_objects()

    object_list = list(bpy.context.scene.objects)

    node_list = []
    layer_count = []
    layer_root = []
    root_list = []
    children_list = []
    reversed_children_list = []
    joined_list = []
    reversed_joined_list = []
    sort_list = []
    reversed_sort_list = []
    armature = []
    armature_count = 0
    mesh_frame_count = 0

    material_list = []
    marker_list = []
    instance_xref_paths = []
    instance_markers = []
    geometry_list = []
    original_geometry_list = []
    triangles = []
    vertices = []
    sphere_list = []
    box_list = []
    capsule_list = []
    convex_shape_list = []
    ragdoll_list = []
    hinge_list = []
    car_wheel_list = []
    point_to_point_list = []
    prismatic_list = []
    bounding_sphere = []

    region_list = []
    permutation_list = []
    default_region = get_default_region_permutation_name(game_version)
    default_permutation = get_default_region_permutation_name(game_version)

    version = int(jms_version)
    node_checksum = 0

    if len(object_list) == 0:
        report({'ERROR'}, 'No objects in scene.')
        return {'CANCELLED'}

    bpy.context.view_layer.objects.active = object_list[0]
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    for obj in object_list:
        assigned_materials_list = []
        find_region = get_region(default_region, obj.jms.Region)
        find_permutation = get_permutation(default_permutation, obj.jms.Permutation)
        if obj.type == 'ARMATURE':
            armature_count += 1
            armature = obj
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            node_list = list(obj.data.bones)
            if mesh_frame_count > 0:
                report({'ERROR'}, "Using both armature and object mesh node setup. Choose one or the other.")
                return {'CANCELLED'}

        elif obj.name[0:2].lower() == 'b_' or obj.name[0:5].lower() == 'frame':
            node_list.append(obj)
            mesh_frame_count += 1
            if armature_count > 0:
                report({'ERROR'}, "Using both armature and object mesh node setup. Choose one or the other.")
                return {'CANCELLED'}

        elif obj.name[0:1].lower() == '#':
            if game_version == 'haloce':
                if not obj.parent == None:
                    if obj.parent.type == 'ARMATURE' or obj.parent.name[0:2].lower() == 'b_' or obj.parent.name[0:5].lower() == 'frame':
                        marker_list.append(obj)
                        region_list.append(find_region)

            elif game_version == 'halo2':
                marker_list.append(obj)
                region_list.append(find_region)

            else:
                report({'ERROR'}, "How did you even choose an option that doesn't exist?")
                return {'CANCELLED'}

        elif obj.name[0:1].lower() == '$':
            if version >= 8205:
                if not obj.rigid_body_constraint == None:
                    if obj.rigid_body_constraint.type == 'HINGE':
                        hinge_list.append(obj)

                elif obj.jms.Object_Type == 'SPHERE':
                    sphere_list.append(obj)
                    region_list.append(find_region)
                    permutation_list.append(find_permutation)

                elif obj.jms.Object_Type == 'BOX':
                    box_list.append(obj)
                    region_list.append(find_region)
                    permutation_list.append(find_permutation)

                elif obj.jms.Object_Type == 'CAPSULES':
                    capsule_list.append(obj)
                    region_list.append(find_region)
                    permutation_list.append(find_permutation)

                elif obj.jms.Object_Type == 'CONVEX SHAPES':
                    convex_shape_list.append(obj)
                    region_list.append(find_region)
                    permutation_list.append(find_permutation)

                else:
                    report({'ERROR'}, "How did you even choose an option that doesn't exist?")
                    return {'CANCELLED'}

        elif not len(obj.jms.XREF_path) == 0:
            instance_markers.append(obj)
            if not obj.jms.XREF_path in instance_xref_paths:
                instance_xref_paths.append(obj.jms.XREF_path)

        elif obj.name[0:1].lower() == ',':
            bounding_sphere.append(obj)

        elif obj.type== 'MESH':
            if game_version == 'haloce':
                if not obj.parent == None:
                    if obj.parent.type == 'ARMATURE' or obj.parent.name[0:2].lower() == 'b_' or obj.parent.name[0:5].lower() == 'frame':
                        modifier_list = []
                        if triangulate_faces:
                            for modifier in obj.modifiers:
                                modifier.show_render = True
                                modifier.show_viewport = True
                                modifier.show_in_editmode = True
                                modifier_list.append(modifier.type)

                            if not 'TRIANGULATE' in modifier_list:
                                obj.modifiers.new("Triangulate", type='TRIANGULATE')

                            depsgraph = context.evaluated_depsgraph_get()
                            obj_for_convert = obj.evaluated_get(depsgraph)
                            me = obj_for_convert.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
                            geometry_list.append(me)
                            original_geometry_list.append(obj)

                        else:
                            geometry_list.append(obj.to_mesh(preserve_all_data_layers=True))
                            original_geometry_list.append(obj)

                        region_list.append(find_region)
                        permutation_list.append(find_permutation)

            elif game_version == 'halo2':
                modifier_list = []
                if triangulate_faces:
                    for modifier in obj.modifiers:
                        modifier.show_render = True
                        modifier.show_viewport = True
                        modifier.show_in_editmode = True
                        modifier_list.append(modifier.type)

                    if not 'TRIANGULATE' in modifier_list:
                        obj.modifiers.new("Triangulate", type='TRIANGULATE')

                    depsgraph = context.evaluated_depsgraph_get()
                    obj_for_convert = obj.evaluated_get(depsgraph)
                    me = obj_for_convert.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
                    geometry_list.append(me)
                    original_geometry_list.append(obj)

                else:
                    geometry_list.append(obj.to_mesh(preserve_all_data_layers=True))
                    original_geometry_list.append(obj)

                region_list.append(find_region)
                permutation_list.append(find_permutation)

            else:
                report({'ERROR'}, "How did you even choose an option that doesn't exist?")
                return {'CANCELLED'}

        if len(obj.material_slots)!= 0 and len(obj.jms.XREF_path) == 0 and not obj.name[0:1].lower() == '#' and not obj.name[0:2].lower() == 'b_' and not obj.name[0:5].lower() == 'frame':
            for f in obj.data.polygons:
                slot = obj.material_slots[f.material_index]
                mat = slot.material
                if mat is not None:
                    if mat not in assigned_materials_list:
                        assigned_materials_list.append(mat)

            for slot in obj.material_slots:
                if game_version == 'halo2':
                    if obj.name[0:1].lower() == '$':
                        if [slot.material, obj.jms.level_of_detail, obj.jms.Region, obj.jms.Permutation] not in material_list and slot.material in assigned_materials_list and version >= 8205:
                            material_list.append([slot.material, obj.jms.level_of_detail, obj.jms.Region, obj.jms.Permutation])

                    elif obj.type== 'MESH':
                        if [slot.material, obj.jms.level_of_detail, obj.jms.Region, obj.jms.Permutation] not in material_list and slot.material in assigned_materials_list:
                            material_list.append([slot.material, obj.jms.level_of_detail, obj.jms.Region, obj.jms.Permutation])

                elif game_version == 'haloce':
                    if slot.material not in material_list and not obj.name[0:1].lower() == '$':
                        material_list.append(slot.material)

                else:
                    report({'ERROR'}, "How did you even choose an option that doesn't exist?")
                    return {'CANCELLED'}

        else:
            if game_version == 'haloce':
                if None not in material_list and not obj.name[0:1].lower() == '$' and not obj.name[0:1].lower() == '#' and not obj.name[0:2].lower() == 'b_' and not obj.name[0:5].lower() == 'frame':
                    material_list.append(None)

    region_list = list(dict.fromkeys(region_list))
    permutation_list = list(dict.fromkeys(permutation_list))
    node_count = len(node_list)
    material_count = len(material_list)
    marker_count = len(marker_list)
    region_count = len(region_list)
    instance_xref_paths_count = len(instance_xref_paths)
    instance_markers_count = len(instance_markers)
    bounding_sphere_count = len(bounding_sphere)
    ragdoll_count = len(ragdoll_list)
    hinge_count = len(hinge_list)
    car_wheel_count = len(car_wheel_list)
    point_to_point_count = len(point_to_point_list)
    prismatic_count = len(prismatic_list)

    for node in node_list:
        if node.parent == None:
            layer_count.append(None)
            layer_root.append(node)

        else:
            if not node.parent in layer_count:
                layer_count.append(node.parent)

    for layer in layer_count:
        joined_list = root_list + children_list
        reversed_joined_list = root_list + reversed_children_list
        layer_index = layer_count.index(layer)
        if layer_index == 0:
            if armature_count == 0:
                root_list.append(layer_root[0])

            else:
                root_list.append(armature.data.bones[0])

        else:
            for node in node_list:
                if armature_count == 0:
                    if node.parent != None:
                        if node.parent in joined_list and not node in children_list:
                            sort_list.append(node.name)
                            reversed_sort_list.append(node.name)

                else:
                    if node.parent != None:
                        if armature.data.bones['%s' % node.parent.name] in joined_list and not node in children_list:
                            sort_list.append(node.name)
                            reversed_sort_list.append(node.name)

            sort_list.sort()
            reversed_sort_list.sort()
            reversed_sort_list.reverse()
            for sort in sort_list:
                if armature_count == 0:
                    if not bpy.data.objects[sort] in children_list:
                        children_list.append(bpy.data.objects[sort])

                else:
                    if not armature.data.bones['%s' % sort] in children_list:
                        children_list.append(armature.data.bones['%s' % sort])

            for sort in reversed_sort_list:
                if armature_count == 0:
                    if not bpy.data.objects[sort] in reversed_children_list:
                        reversed_children_list.append(bpy.data.objects[sort])

                else:
                    if not armature.data.bones['%s' % sort] in reversed_children_list:
                        reversed_children_list.append(armature.data.bones['%s' % sort])

        joined_list = root_list + children_list
        reversed_joined_list = root_list + reversed_children_list

    if version > 8209:
        decimal_1 = '\n%0.10f'
        decimal_2 = '\n%0.10f\t%0.10f'
        decimal_3 = '\n%0.10f\t%0.10f\t%0.10f'
        decimal_4 = '\n%0.10f\t%0.10f\t%0.10f\t%0.10f'

    else:
        decimal_1 = '\n%0.6f'
        decimal_2 = '\n%0.6f\t%0.6f'
        decimal_3 = '\n%0.6f\t%0.6f\t%0.6f'
        decimal_4 = '\n%0.6f\t%0.6f\t%0.6f\t%0.6f'

    error_pass(armature_count, report, game_version, node_count, version, extension, geometry_list, marker_list)

    file = open(filepath + extension, 'w', encoding='%s' % get_encoding(game_version))

    #write header
    if version >= 8205:
        file.write(
            ';### VERSION ###' +
            '\n%s' % (version) +
            '\n;\t<8197-8210>\n'
            )

    else:
        file.write(
            '%s' % (version) +
            '\n%s' % (node_checksum) +
            '\n%s' % (node_count)
            )

    #write nodes
    if version >= 8205:
        file.write(
            '\n;### NODES ###' +
            '\n%s' % (node_count) +
            '\n;\t<name>' +
            '\n;\t<parent node index>' +
            '\n;\t<default rotation <i,j,k,w>>' +
            '\n;\t<default translation <x,y,z>>\n'
        )

    for node in joined_list:
        find_child_node = get_child(node, reversed_joined_list)
        find_sibling_node = get_sibling(armature, node, reversed_joined_list)
        first_child_node = -1
        first_sibling_node = -1
        parent_node = -1
        if not find_child_node == None:
            first_child_node = joined_list.index(find_child_node)

        if not find_sibling_node == None:
            first_sibling_node = joined_list.index(find_sibling_node)

        if not node.parent == None:
            parent_node = joined_list.index(node.parent)

        if armature_count == 0:
            bone_matrix = node.matrix_world

            if node.parent and not version >= 8205:
                bone_matrix = node.parent.matrix_local @ node.matrix_world

        else:
            pose_bone = armature.pose.bones['%s' % (node.name)]

            bone_matrix = pose_bone.matrix
            if pose_bone.parent and not version >= 8205:
                bone_matrix = pose_bone.parent.matrix.inverted() @ pose_bone.matrix

        pos  = bone_matrix.translation
        quat = bone_matrix.to_quaternion().inverted()
        if version >= 8205:
            quat = bone_matrix.to_quaternion()

        quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
        quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
        quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
        quat_w = Decimal(-quat[0]).quantize(Decimal('1.0000000000'))
        pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))
        pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))
        pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))

        if version >= 8205:
            file.write(
                '\n;NODE %s' % (joined_list.index(node)) +
                '\n%s' % (node.name) +
                '\n%s' % (parent_node) +
                decimal_4 % (quat_i, quat_j, quat_k, quat_w) +
                decimal_3 % (pos_x, pos_y, pos_z) +
                '\n'
            )

        else:
            file.write(
                '\n%s' % (node.name) +
                '\n%s' % (first_child_node) +
                '\n%s' % (first_sibling_node) +
                decimal_4 % (quat_i, quat_j, quat_k, quat_w) +
                decimal_3 % (pos_x, pos_y, pos_z)
            )

    #write materials
    if version >= 8205:
        file.write(
            '\n;### MATERIALS ###' +
            '\n%s' % (material_count) +
            '\n;\t<name>' +
            '\n;\t<(?Material ID?) LOD Permutation Region>\n'
        )

    else:
        file.write(
            '\n%s' % (material_count)
        )

    for material in material_list:
        if game_version == 'halo2':
            untouched_lod = material[1]
            untouched_region = material[2]
            untouched_permutation = material[3]
            LOD = get_lod(material[1])
            Permutation = default_permutation
            Region = default_region
            '''
            This doesn't matter for CE but for Halo 2 the region or permutation names can't have any whitespace.
            Lets fix that here to make sure nothing goes wrong.
            '''
            if len(material[3]) != 0:
                safe_permutation = material[3].replace(' ', '_').replace('\t', '_')
                Permutation = safe_permutation

            if len(material[2]) != 0:
                safe_region = material[2].replace(' ', '_').replace('\t', '_')
                Region = safe_region

            if version >= 8205:
                file.write(
                    '\n;MATERIAL %s' % (material_list.index([material[0], untouched_lod, untouched_region, untouched_permutation])) +
                    '\n%s' % material[0].name +
                    '\n%s %s %s\n' % (LOD, Permutation, Region)
                )

            else:
                file.write(
                    '\n%s' % (material[0].name) +
                    '\n%s %s %s' % (LOD, Permutation, Region)
                )

        elif game_version == 'haloce':
            material_name = '<none>'
            texture_path = '<none>'
            if not material == None:
                material_name = material.name
                for node in material.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        image_filepath = node.image.filepath
                        image_extension = image_filepath.rsplit('.', 1)[1]
                        image_path = image_filepath.rsplit('.', 1)[0]
                        if image_extension.lower() == 'tif' and os.path.exists(image_filepath):
                            texture_path = image_path

            file.write(
                '\n%s' % (material_name) +
                '\n%s' % (texture_path)
            )

        else:
            report({'ERROR'}, "How did you even choose an option that doesn't exist?")
            file.close()
            return {'CANCELLED'}

    #write markers
    if version >= 8205:
        file.write(
            '\n;### MARKERS ###' +
            '\n%s' % (marker_count) +
            '\n;\t<name>' +
            '\n;\t<node index>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<radius>\n'
        )

    else:
        file.write(
            '\n%s' % (marker_count)
        )

    for marker in marker_list:
        name = marker.name.split('#', 1)[1] #remove marker symbol from name
        fixed_name = name.rsplit('.', 1)[0] #remove name change from duplicating objects in Blender
        region = -1
        if len(marker.jms.Region) != 0:
            region = region_list.index(marker.jms.Region)

        parent_index = 0
        if armature_count == 0:
            if marker.parent:
                parent_bone = bpy.data.objects[marker.parent.name]
                parent_index = joined_list.index(parent_bone)

        else:
            if marker.parent_bone:
                parent_bone = armature.data.bones[marker.parent_bone]
                parent_index = joined_list.index(parent_bone)

        radius = marker.dimensions[0]/2
        marker_matrix = marker.matrix_world
        if marker.parent:
            marker_matrix = parent_bone.matrix_local.inverted() @ marker.matrix_world

        pos  = marker_matrix.translation
        quat = marker_matrix.to_quaternion().inverted()

        quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
        quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
        quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
        quat_w = Decimal(quat[0]).quantize(Decimal('1.0000000000'))
        pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))
        pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))
        pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))

        if version >= 8205:
            file.write(
                '\n;MARKER %s' % (marker_list.index(marker)) +
                '\n%s' % (fixed_name) +
                '\n%s' % (parent_index) +
                decimal_4 % (quat_i, quat_j, quat_k, quat_w) +
                decimal_3 % (pos_x, pos_y, pos_z) +
                decimal_1 % (radius) +
                '\n'
            )

        else:
            file.write(
                '\n%s' % (fixed_name) +
                '\n%s' % (region) +
                '\n%s' % (parent_index) +
                decimal_4 % (quat_i, quat_j, quat_k, quat_w) +
                decimal_3 % (pos_x, pos_y, pos_z) +
                decimal_1 % (radius)
            )

    #write regions
    if version <= 8204:
        file.write(
            '\n%s' % (region_count)
        )

        for region in region_list:
            file.write(
                '\n%s' % (region)
            )

    if version >= 8205:
        #write instance xref paths
        file.write(
            '\n;### INSTANCE XREF PATHS ###' +
            '\n%s' % (instance_xref_paths_count) +
            '\n;\t<path to .MAX file>' +
            '\n;\t<name>\n'
        )

        for int_xref_path in instance_xref_paths:
            file.write(
                '\n;XREF %s' % (instance_xref_paths.index(int_xref_path)) +
                '\n%s' % (bpy.path.abspath(int_xref_path)) +
                '\n%s\n' % (os.path.basename(int_xref_path).rsplit('.', 1)[0])
            )

        #write instance markers
        file.write(
            '\n;### INSTANCE MARKERS ###' +
            '\n%s' % (instance_markers_count) +
            '\n;\t<name>' +
            '\n;\t<unique identifier>' +
            '\n;\t<path index>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>\n'
        )

        seed(1)
        for int_markers in instance_markers:
            unique_identifier = -1 * (randint(0, 3000000000))

            pos  = int_markers.matrix_world.translation
            quat = int_markers.matrix_world.to_quaternion().inverted()

            quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
            quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
            quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
            quat_w = Decimal(quat[0]).quantize(Decimal('1.0000000000'))
            pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))
            pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))
            pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))

            file.write(
                '\n;XREF OBJECT %s' % (instance_markers.index(int_markers)) +
                '\n%s' % (int_markers.name) +
                '\n%s' % (unique_identifier) +
                '\n%s' % (instance_xref_paths.index(int_markers.jms.XREF_path)) +
                decimal_4 % (quat_i, quat_j, quat_k, quat_w) +
                decimal_3 % (pos_x, pos_y, pos_z) +
                '\n'
            )

    #write vertices
    for geometry in geometry_list:
        item_index = int(geometry_list.index(geometry))
        original_geo = original_geometry_list[item_index]
        vertex_groups = original_geo.vertex_groups.keys()

        matrix = original_geo.matrix_world

        region_name = original_geo.jms.Region

        uv_layer = geometry.uv_layers.active.data[:]
        mesh_loops = geometry.loops
        mesh_verts = geometry.vertices[:]

        for face in geometry.polygons:
            jms_triangle = JmsTriangle()
            triangles.append(jms_triangle)

            if len(region_name) != 0:
                region_index = region_list.index(region_name)

            else:
                region_index = region_list.index(default_region)

            jms_triangle.v0 = len(vertices)
            jms_triangle.v1 = len(vertices) + 1
            jms_triangle.v2 = len(vertices) + 2
            jms_triangle.region = region_index
            if game_version == 'halo2':
                jms_triangle.material = -1
                if len(original_geo.material_slots) != 0:
                    jms_triangle.material = material_list.index([bpy.data.materials[geometry.materials[face.material_index].name], original_geo.jms.level_of_detail, original_geo.jms.Region, original_geo.jms.Permutation])

            elif game_version == 'haloce':
                jms_triangle.material = material_list.index(None)
                if len(original_geo.material_slots) != 0:
                    jms_triangle.material = material_list.index(bpy.data.materials[geometry.materials[face.material_index].name])

            else:
                report({'ERROR'}, "How did you even choose an option that doesn't exist?")
                file.close()
                return {'CANCELLED'}

            for loop_index in face.loop_indices:
                vert = mesh_verts[mesh_loops[loop_index].vertex_index]
                uv = uv_layer[loop_index].uv

                jms_vertex = JmsVertex()
                vertices.append(jms_vertex)

                pos  = matrix @ vert.co
                norm = matrix @ (vert.co + vert.normal) - pos

                jms_vertex.pos = pos
                jms_vertex.norm = norm
                jms_vertex.uv = uv

                if len(vert.groups) != 0:
                    value = len(vert.groups)
                    if value > 4:
                        value = 4

                    jms_vertex.node_influence_count = value
                    for group_index in range(len(vert.groups)):
                        vertex_group = vert.groups[group_index].group
                        object_vertex_group = vertex_groups[vertex_group]
                        if armature_count == 0:
                            node_obj = bpy.data.objects[object_vertex_group]

                        else:
                            node_obj = armature.data.bones[object_vertex_group]

                        if group_index == 0:
                            jms_vertex.node0 = joined_list.index(node_obj)
                            jms_vertex.node0_weight = '%0.10f' % vert.groups[0].weight

                        if group_index == 1:
                            jms_vertex.node1 = joined_list.index(node_obj)
                            jms_vertex.node1_weight = '%0.10f' % vert.groups[1].weight

                        if group_index == 2:
                            jms_vertex.node2 = joined_list.index(node_obj)
                            jms_vertex.node2_weight = '%0.10f' % vert.groups[2].weight

                        if group_index == 3:
                            jms_vertex.node3 = joined_list.index(node_obj)
                            jms_vertex.node3_weight = '%0.10f' % vert.groups[3].weight

                else:
                    parent_index = 0
                    if armature_count == 0:
                        if geometry.parent:
                            parent_bone = bpy.data.objects[geometry.parent.name]
                            parent_index = joined_list.index(parent_bone)

                    else:
                        if geometry.parent_bone:
                            parent_bone = armature.data.bones[geometry.parent_bone]
                            parent_index = joined_list.index(parent_bone)

                    jms_vertex.node_influence_count = '1'
                    jms_vertex.node0 = parent_index
                    jms_vertex.node0_weight = '1.0000000000'

    if version >= 8205:
        file.write(
            '\n;### VERTICES ###' +
            '\n%s' % len(vertices) +
            '\n;\t<position>' +
            '\n;\t<normal>' +
            '\n;\t<node influences count>' +
            '\n;\t\t<index>' +
            '\n;\t\t<weight>' +
            '\n;\t<texture coordinate count>' +
            '\n;\t\t<texture coordinates <u,v>>\n'
        )

    else:
        file.write(
            '\n%s' % (len(vertices))
        )

    for jms_vertex in vertices:
        pos  = jms_vertex.pos
        norm = jms_vertex.norm
        uv   = jms_vertex.uv

        pos_x = Decimal(pos[0]).quantize(Decimal('1.000000'))
        pos_y = Decimal(pos[1]).quantize(Decimal('1.000000'))
        pos_z = Decimal(pos[2]).quantize(Decimal('1.000000'))

        norm_i = Decimal(norm[0]).quantize(Decimal('1.000000'))
        norm_j = Decimal(norm[1]).quantize(Decimal('1.000000'))
        norm_k = Decimal(norm[2]).quantize(Decimal('1.000000'))

        for node_influence_index in range(int(jms_vertex.node_influence_count)):
            if node_influence_index == 0:
                jms_node = '\n%s%s' % (jms_vertex.node0, decimal_1 % float(jms_vertex.node0_weight))
            elif node_influence_index == 1:
                jms_node += '\n%s%s' % (jms_vertex.node1, decimal_1 % float(jms_vertex.node1_weight))
            elif node_influence_index == 2:
                jms_node += '\n%s%s' % (jms_vertex.node2, decimal_1 % float(jms_vertex.node2_weight))
            elif node_influence_index == 3:
                jms_node += '\n%s%s' % (jms_vertex.node3, decimal_1 % float(jms_vertex.node3_weight))

        tex_coord_count = 1

        tex_u = Decimal(uv[0]).quantize(Decimal('1.000000'))
        tex_v = Decimal(uv[1]).quantize(Decimal('1.000000'))
        tex_w = 0

        if version >= 8205:
            file.write(
                '\n;VERTEX %s' % (vertices.index(jms_vertex)) +
                decimal_3 % (pos_x, pos_y, pos_z) +
                decimal_3 % (norm_i, norm_j, norm_k) +
                '\n%s' % (jms_vertex.node_influence_count) +
                (jms_node) +
                '\n%s' % (tex_coord_count) +
                decimal_2 % (tex_u, tex_v) +
                '\n'
            )

        else:
            file.write(
                '\n%s' % (jms_vertex.node0) +
                decimal_3 % (pos_x, pos_y, pos_z) +
                decimal_3 % (norm_i, norm_j, norm_k) +
                '\n%s' % (jms_vertex.node1) +
                decimal_1 % float(jms_vertex.node1_weight) +
                decimal_1 % float(tex_u) +
                decimal_1 % float(tex_v) +
                decimal_1 % float(tex_w)
            )

    if version >= 8205:
        file.write(
            '\n;### TRIANGLES ###' +
            '\n%s' % len(triangles) +
            '\n;\t<material index>' +
            '\n;\t<vertex indices <v0,v1,v2>>\n'
        )

    else:
        file.write(
            '\n%s' % (len(triangles))
        )

    for tri in triangles:
        if version >= 8205:
            file.write(
                '\n;TRIANGLE %s' % (triangles.index(tri)) +
                '\n%s' % (tri.material) +
                '\n%s\t%s\t%s\n' % (tri.v0, tri.v1, tri.v2)
            )

        else:
            file.write(
                '\n%s' % (tri.region) +
                '\n%s' % (tri.material) +
                '\n%s\t%s\t%s' % (tri.v0, tri.v1, tri.v2)
            )

    if version <= 8204:
        file.write(
            '\n'
        )

    if version >= 8206:
        file.write(
            '\n;### SPHERES ###' +
            '\n%s' % len(sphere_list) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<radius>\n'
        )

        #write sphere
        for spheres in sphere_list:
            assigned_sphere_materials_list = []
            name = spheres.name.split('$', 1)[1]
            sphere_material_index = -1
            sphere_materials = spheres.data.materials
            if len(sphere_materials) != 0:
                for f in spheres.data.polygons:
                    slot = spheres.material_slots[f.material_index]
                    mat = slot.material
                    if mat is not None:
                        if mat not in assigned_sphere_materials_list:
                            assigned_sphere_materials_list.append(mat)

            if len(assigned_sphere_materials_list) > 1:
                report({'WARNING'}, "Physics object %s has more than one material assigned to it's faces. Please use only one material." % (spheres.name))

            if len(assigned_sphere_materials_list) != 0:
                sphere_material_index = material_list.index([assigned_sphere_materials_list[0], spheres.jms.level_of_detail, spheres.jms.Region, spheres.jms.Permutation])

            parent_index = -1
            if armature_count == 0:
                if spheres.parent:
                    parent_bone = bpy.data.objects[spheres.parent.name]
                    parent_index = joined_list.index(parent_bone)

            else:
                if spheres.parent_bone:
                    parent_bone = armature.data.bones[spheres.parent_bone]
                    parent_index = joined_list.index(parent_bone)

            radius = spheres.dimensions[0]/2
            sphere_matrix = spheres.matrix_world
            if spheres.parent:
                sphere_matrix = parent_bone.matrix_local.inverted() @ spheres.matrix_world

            pos  = sphere_matrix.translation
            quat = sphere_matrix.to_quaternion().inverted()

            quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
            quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
            quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
            quat_w = Decimal(quat[0]).quantize(Decimal('1.0000000000'))
            pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))
            pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))
            pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))

            file.write(
                '\n;SPHERE %s' % (sphere_list.index(spheres)) +
                '\n%s' % name +
                '\n%s' % parent_index +
                '\n%s' % sphere_material_index +
                decimal_4 % (quat_i, quat_j, quat_k, quat_w) +
                decimal_3 % (pos_x, pos_y, pos_z) +
                decimal_1 % radius +
                '\n'
            )

        #write boxes
        file.write(
            '\n;### BOXES ###' +
            '\n%s' % len(box_list) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<width (x)>' +
            '\n;\t<length (y)>' +
            '\n;\t<height (z)>\n'
        )

        for boxes in box_list:
            assigned_boxes_materials_list = []
            name = boxes.name.split('$', 1)[1]
            boxes_material_index = -1
            box_materials = boxes.data.materials
            if len(box_materials) != 0:
                for f in boxes.data.polygons:
                    slot = boxes.material_slots[f.material_index]
                    mat = slot.material
                    if mat is not None:
                        if mat not in assigned_boxes_materials_list:
                            assigned_boxes_materials_list.append(mat)

            if len(assigned_boxes_materials_list) > 1:
                report({'WARNING'}, "Physics object %s has more than one material assigned to it's faces. Please use only one material." % (boxes.name))

            if len(assigned_boxes_materials_list) != 0:
                boxes_material_index = material_list.index([assigned_boxes_materials_list[0], boxes.jms.level_of_detail, boxes.jms.Region, boxes.jms.Permutation])

            parent_index = -1
            if armature_count == 0:
                if boxes.parent:
                    parent_bone = bpy.data.objects[boxes.parent.name]
                    parent_index = joined_list.index(parent_bone)

            else:
                if boxes.parent_bone:
                    parent_bone = armature.data.bones[boxes.parent_bone]
                    parent_index = joined_list.index(parent_bone)

            dimension_x = boxes.dimensions[0]/2
            dimension_y = boxes.dimensions[1]/2
            dimension_z = boxes.dimensions[2]/2
            box_matrix = boxes.matrix_world
            if boxes.parent:
                box_matrix = parent_bone.matrix_local.inverted() @ boxes.matrix_world

            pos  = box_matrix.translation
            quat = box_matrix.to_quaternion().inverted()

            quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
            quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
            quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
            quat_w = Decimal(quat[0]).quantize(Decimal('1.0000000000'))
            pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))
            pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))
            pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))

            file.write(
                '\n;BOXES %s' % (box_list.index(boxes)) +
                '\n%s' % name +
                '\n%s' % parent_index +
                '\n%s' % boxes_material_index +
                decimal_4 % (quat_i, quat_j, quat_k, quat_w) +
                decimal_3 % (pos_x, pos_y, pos_z) +
                decimal_1 % dimension_x +
                decimal_1 % dimension_y +
                decimal_1 % dimension_z +
                '\n'
            )

        #write capsules
        file.write(
            '\n;### CAPSULES ###' +
            '\n%s' % len(capsule_list) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<height>' +
            '\n;\t<radius>\n'
             )

        for capsule in capsule_list:
            assigned_capsule_materials_list = []
            name = capsule.name.split('$', 1)[1]
            capsule_material_index = -1
            capsule_materials = capsule.data.materials
            if len(capsule_materials) != 0:
                for f in capsule.data.polygons:
                    slot = capsule.material_slots[f.material_index]
                    mat = slot.material
                    if mat is not None:
                        if mat not in assigned_capsule_materials_list:
                            assigned_capsule_materials_list.append(mat)

            if len(assigned_capsule_materials_list) > 1:
                report({'WARNING'}, "Physics object %s has more than one material assigned to it's faces. Please use only one material." % (capsule.name))

            if len(assigned_capsule_materials_list) != 0:
                capsule_material_index = material_list.index([assigned_capsule_materials_list[0], capsule.jms.level_of_detail, capsule.jms.Region, capsule.jms.Permutation])

            parent_index = -1
            if armature_count == 0:
                if capsule.parent:
                    parent_bone = bpy.data.objects[capsule.parent.name]
                    parent_index = joined_list.index(parent_bone)

            else:
                if capsule.parent_bone:
                    parent_bone = armature.data.bones[capsule.parent_bone]
                    parent_index = joined_list.index(parent_bone)

            capsule_matrix = capsule.matrix_world
            if capsule.parent:
                capsule_matrix = parent_bone.matrix_local.inverted() @ capsule.matrix_world

            pos  = capsule_matrix.translation
            quat = capsule_matrix.to_quaternion().inverted()

            quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
            quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
            quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
            quat_w = Decimal(quat[0]).quantize(Decimal('1.0000000000'))
            pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))
            pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))
            pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))
            scale_x = capsule.dimensions[0]
            scale_y = capsule.dimensions[1]
            scale_z = capsule.dimensions[2]

            radius = scale_y/2
            pill_height_math = scale_z - scale_x
            if pill_height_math < 0:
                pill_height = 0

            else:
                pill_height = pill_height_math

            file.write(
                '\n;CAPSULES %s' % (capsule_list.index(capsule)) +
                '\n%s' % name +
                '\n%s' % parent_index +
                '\n%s' % capsule_material_index +
                decimal_4 % (quat_i, quat_j, quat_k, quat_w) +
                decimal_3 % (pos_x, pos_y, pos_z) +
                decimal_1 % pill_height +
                decimal_1 % radius +
                '\n'
            )

        #write convex shapes
        file.write(
            '\n;### CONVEX SHAPES ###' +
            '\n%s' % len(convex_shape_list) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<vertex count>' +
            '\n;\t<...vertices>\n'
        )

        for convex_shape in convex_shape_list:
            assigned_convex_shape_materials_list = []
            name = convex_shape.name.split('$', 1)[1]
            convex_shape_materials = convex_shape.data.materials
            convex_shape_material_index = -1
            if len(convex_shape_materials) != 0:
                for f in convex_shape.data.polygons:
                    slot = convex_shape.material_slots[f.material_index]
                    mat = slot.material
                    if mat is not None:
                        if mat not in assigned_convex_shape_materials_list:
                            assigned_convex_shape_materials_list.append(mat)

            if len(assigned_convex_shape_materials_list) > 1:
                report({'WARNING'}, "Physics object %s has more than one material assigned to it's faces. Please use only one material." % (convex_shape.name))

            if len(assigned_convex_shape_materials_list) != 0:
                convex_shape_material_index = material_list.index([assigned_convex_shape_materials_list[0], convex_shape.jms.level_of_detail, convex_shape.jms.Region, convex_shape.jms.Permutation])

            parent_index = -1
            if armature_count == 0:
                if convex_shape.parent:
                    parent_bone = bpy.data.objects[convex_shape.parent.name]
                    parent_index = joined_list.index(parent_bone)

            else:
                if convex_shape.parent_bone:
                    parent_bone = armature.data.bones[convex_shape.parent_bone]
                    parent_index = joined_list.index(parent_bone)

            convex_matrix = convex_shape.matrix_world
            if convex_shape.parent:
                convex_matrix = parent_bone.matrix_local.inverted() @ convex_shape.matrix_world

            pos  = convex_matrix.translation
            quat = convex_matrix.to_quaternion().inverted()

            quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
            quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
            quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
            quat_w = Decimal(quat[0]).quantize(Decimal('1.0000000000'))
            pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))
            pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))
            pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))

            file.write(
                '\n;CONVEX %s' % (convex_shape_list.index(convex_shape)) +
                '\n%s' % name +
                '\n%s' % parent_index +
                '\n%s' % convex_shape_material_index +
                decimal_4 % (quat_i, quat_j, quat_k, quat_w) +
                decimal_3 % (pos_x, pos_y, pos_z) +
                '\n%s' % len(convex_shape.data.vertices)
            )

            for vertex in convex_shape.data.vertices:
                file.write(
                    decimal_3 % (vertex.co[0], vertex.co[1], vertex.co[2])
                )

            file.write('\n')

        #write rag dolls
        file.write(
            '\n;### RAGDOLLS ###' +
            '\n%s' % (ragdoll_count) +
            '\n;\t<name>' +
            '\n;\t<attached index>' +
            '\n;\t<referenced index>' +
            '\n;\t<attached transform>' +
            '\n;\t<reference transform>' +
            '\n;\t<min twist>' +
            '\n;\t<max twist>' +
            '\n;\t<min cone>' +
            '\n;\t<max cone>' +
            '\n;\t<min plane>' +
            '\n;\t<max plane>\n'
        )

        #write hinges
        file.write(
            '\n;### HINGES ###' +
            '\n%s' % (hinge_count) +
            '\n;\t<name>' +
            '\n;\t<body A index>' +
            '\n;\t<body B index>' +
            '\n;\t<body A transform>' +
            '\n;\t<body B transform>' +
            '\n;\t<is limited>' +
            '\n;\t<friction limit>' +
            '\n;\t<min angle>' +
            '\n;\t<max angle>\n'
        )

        for hinge in hinge_list:
            name = hinge.name.split('$', 1)[1]
            body_a_obj = hinge.rigid_body_constraint.object1
            body_b_obj = hinge.rigid_body_constraint.object2
            body_a_index = -1
            body_b_index = -1
            if armature_count == 0:
                if body_a_obj:
                    if body_a_obj.parent:
                        parent_bone_a = bpy.data.objects[body_a_obj.parent.name]
                        parent_index = joined_list.index(parent_bone_a)
                        body_a_index = parent_index

                if body_b_obj:
                    if body_b_obj.parent:
                        parent_bone_b = bpy.data.objects[body_b_obj.parent.name]
                        parent_index = joined_list.index(parent_bone_b)
                        body_b_index = parent_index

            else:
                if body_a_obj:
                    if body_a_obj.parent_bone:
                        parent_bone_a = armature.data.bones[body_a_obj.parent_bone]
                        parent_index = joined_list.index(parent_bone_a)
                        body_a_index = parent_index

                if body_b_obj:
                    if body_b_obj.parent_bone:
                        parent_bone_b = armature.data.bones[body_b_obj.parent_bone]
                        parent_index = joined_list.index(parent_bone_b)
                        body_b_index = parent_index

            body_a_matrix = hinge.matrix_world
            if body_a_obj.parent:
                body_a_matrix = parent_bone_a.matrix_local.inverted() @ hinge.matrix_world

            body_b_matrix = hinge.matrix_world
            if body_b_obj.parent:
                body_b_matrix = parent_bone_b.matrix_local.inverted() @ hinge.matrix_world

            pos  = body_a_matrix.translation
            quat = body_a_matrix.to_quaternion().inverted()
            pos2  = body_b_matrix.translation
            quat2 = body_b_matrix.to_quaternion().inverted()

            is_limited = int(hinge.rigid_body_constraint.use_limit_ang_z)
            friction_limit = 0
            if body_b_obj:
                friction_limit = body_b_obj.rigid_body.angular_damping

            min_angle = 0
            max_angle = 0
            if is_limited:
                min_angle = degrees(hinge.rigid_body_constraint.limit_ang_z_lower)
                max_angle = degrees(hinge.rigid_body_constraint.limit_ang_z_upper)

            quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
            quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
            quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
            quat_w = Decimal(quat[0]).quantize(Decimal('1.0000000000'))
            pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))
            pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))
            pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))

            quat_i2 = Decimal(quat2[1]).quantize(Decimal('1.0000000000'))
            quat_j2 = Decimal(quat2[2]).quantize(Decimal('1.0000000000'))
            quat_k2 = Decimal(quat2[3]).quantize(Decimal('1.0000000000'))
            quat_w2 = Decimal(quat2[0]).quantize(Decimal('1.0000000000'))
            pos_x2 = Decimal(pos2[0]).quantize(Decimal('1.0000000000'))
            pos_y2 = Decimal(pos2[1]).quantize(Decimal('1.0000000000'))
            pos_z2 = Decimal(pos2[2]).quantize(Decimal('1.0000000000'))

            file.write(
                '\n;HINGE %s' % (hinge_list.index(hinge)) +
                '\n%s' % name +
                '\n%s' % body_a_index +
                '\n%s' % body_b_index +
                decimal_4 % (quat_i, quat_j, quat_k, quat_w) +
                decimal_3 % (pos_x, pos_y, pos_z) +
                decimal_4 % (quat_i2, quat_j2, quat_k2, quat_w2) +
                decimal_3 % (pos_x2, pos_y2, pos_z2) +
                '\n%s' % (is_limited) +
                decimal_1 % (friction_limit) +
                decimal_1 % (min_angle) +
                decimal_1 % (max_angle) +
                '\n'
            )

        if version > 8209:
            #write car wheel
            file.write(
                '\n;### CAR WHEEL ###' +
                '\n%s' % (car_wheel_count) +
                '\n;\t<name>' +
                '\n;\t<chassis index>' +
                '\n;\t<wheel index>' +
                '\n;\t<chassis transform>' +
                '\n;\t<wheel transform>' +
                '\n;\t<suspension transform>' +
                '\n;\t<suspension min limit>' +
                '\n;\t<suspension max limit>' +
                '\n;\t<friction limit>' +
                '\n;\t<velocity>' +
                '\n;\t<gain>\n'
            )

            #write point to point
            file.write(
                '\n;### POINT TO POINT ###' +
                '\n%s' % (point_to_point_count) +
                '\n;\t<name>' +
                '\n;\t<body A index>' +
                '\n;\t<body B index>' +
                '\n;\t<body A transform>' +
                '\n;\t<body B transform>' +
                '\n;\t<constraint type>' +
                '\n;\t<x min limit>' +
                '\n;\t<x max limit>' +
                '\n;\t<y min limit>' +
                '\n;\t<y max limit>' +
                '\n;\t<z min limit>' +
                '\n;\t<z max limit>' +
                '\n;\t<spring length>\n'
            )

            #write prismatic
            file.write(
                '\n;### PRISMATIC ###' +
                '\n%s' % (prismatic_count) +
                '\n;\t<name>' +
                '\n;\t<body A index>' +
                '\n;\t<body B index>' +
                '\n;\t<body A transform>' +
                '\n;\t<body B transform>' +
                '\n;\t<is limited>' +
                '\n;\t<friction limit>' +
                '\n;\t<min limit>' +
                '\n;\t<max limit>\n'
            )

        #write bounding sphere
        file.write(
            '\n;### BOUNDING SPHERE ###' +
            '\n%s' % (bounding_sphere_count) +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<radius>\n'
        )

        for bound_sphere in bounding_sphere:
            radius = bound_sphere.dimensions[0]/2

            pos  = bound_sphere.matrix_world.translation

            pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))
            pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))
            pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))

            file.write(
                '\n;BOUNDING SPHERE %s' % (bounding_sphere.index(bound_sphere)) +
                decimal_3 % (pos_x, pos_y, pos_z) +
                decimal_1 % radius +
                '\n'
            )

    file.close()
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_scene.jms()
