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

from decimal import *
from math import degrees
from bpy_extras import io_utils
from random import seed, randint
from io_scene_halo.global_functions import global_functions
from io_scene_halo.global_functions.global_functions import JmsVertex
from io_scene_halo.global_functions.global_functions import JmsTriangle
from io_scene_halo.global_functions.global_functions import JmsDimensions

def get_region(default_region, region):
    set_region = None
    if not len(region) == 0:
        set_region = region

    else:
        set_region = default_region

    return set_region

def get_permutation(default_permutation, permutation):
    set_permutation = None
    if not len(permutation) == 0:
        set_permutation = permutation

    else:
        set_permutation = default_permutation

    return set_permutation

def get_default_region_permutation_name(game_version):
    default_name = None
    if game_version == 'haloce':
        default_name = 'unnamed'

    elif game_version == 'halo2':
        default_name = 'Default'

    return default_name

def get_lod(lod_setting, game_version):
    LOD_name = None
    if game_version == 'haloce':
        if lod_setting == '1':
            LOD_name = 'superlow'

        elif lod_setting == '2':
            LOD_name = 'low'

        elif lod_setting == '3':
            LOD_name = 'medium'

        elif lod_setting == '4':
            LOD_name = 'high'

        elif lod_setting == '5':
            LOD_name = 'superhigh'

    elif game_version == 'halo2':
        if lod_setting == '1':
            LOD_name = 'L1'

        elif lod_setting == '2':
            LOD_name = 'L2'

        elif lod_setting == '3':
            LOD_name = 'L3'

        elif lod_setting == '4':
            LOD_name = 'L4'

        elif lod_setting == '5':
            LOD_name = 'L5'

        elif lod_setting == '6':
            LOD_name = 'L6'

    return LOD_name

def get_material(game_version, original_geo, face, geometry, material_list):
    object_materials = len(original_geo.material_slots) - 1
    assigned_material = None
    if game_version == 'haloce':
        if len(original_geo.material_slots) != 0:
            if not face.material_index > object_materials:
                if geometry.materials[face.material_index] is not None:
                    assigned_material = material_list.index(bpy.data.materials[geometry.materials[face.material_index].name])

                else:
                    assigned_material = material_list.index(None)

            else:
                assigned_material = material_list.index(None)

        else:
            assigned_material = material_list.index(None)

    elif game_version == 'halo2':
        assigned_material = -1
        if len(original_geo.material_slots) != 0:
            if not face.material_index > object_materials:
                if geometry.materials[face.material_index] is not None:
                    assigned_material = material_list.index([bpy.data.materials[geometry.materials[face.material_index].name], original_geo.jms.level_of_detail, original_geo.jms.Region, original_geo.jms.Permutation])

    return assigned_material

def set_ignore(mesh):
    collection_list = mesh.users_collection
    ignore = False
    if mesh.hide_viewport or mesh.hide_get():
        ignore = True

    for collection in collection_list:
        if not collection.name == 'Master Collection':
            access_collection = bpy.data.collections[collection.name]
            if access_collection.hide_viewport:
                ignore = True

    return ignore

def gather_materials(obj, version, game_version, material_list):
    assigned_materials_list = []
    if len(obj.material_slots) != 0:
        for face in obj.data.polygons:
            object_materials = len(obj.material_slots) - 1
            if not face.material_index > object_materials:
                slot = obj.material_slots[face.material_index]
                mat = slot.material
                if mat is not None:
                    if mat not in assigned_materials_list:
                        assigned_materials_list.append(mat)

            else:
                if game_version == 'haloce' and not None in material_list:
                    material_list.append(None)

        for slot in obj.material_slots:
            if game_version == 'haloce':
                if slot.material not in material_list:
                    material_list.append(slot.material)

            elif game_version == 'halo2':
                if [slot.material, obj.jms.level_of_detail, obj.jms.Region, obj.jms.Permutation] not in material_list and slot.material in assigned_materials_list:
                    material_list.append([slot.material, obj.jms.level_of_detail, obj.jms.Region, obj.jms.Permutation])

            else:
                report({'ERROR'}, "How did you even choose an option that doesn't exist?")
                return {'CANCELLED'}

    else:
        if game_version == 'haloce' and not None in material_list:
            material_list.append(None)

    return material_list

def file_layout(context,
                filepath,
                report,
                extension,
                extension_ce,
                extension_h2,
                jms_version,
                jms_version_ce,
                jms_version_h2,
                game_version,
                triangulate_faces,
                scale_enum,
                scale_float,
                console,
                permutation_ce,
                level_of_detail_ce,
                hidden_geo,
                object_list,
                export_render,
                export_collision,
                export_physics,
                model_type):

    object_properties = []
    node_list = []
    armature = None
    armature_count = 0
    mesh_frame_count = 0
    object_count = len(object_list)
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
    level_of_detail_ce = get_lod(level_of_detail_ce, game_version)
    version = global_functions.get_version(jms_version, jms_version_ce, jms_version_h2, game_version, console)
    extension = global_functions.get_extension(extension, extension_ce, extension_h2, game_version, console)
    node_checksum = 0
    scale = global_functions.set_scale(scale_enum, scale_float)
    for obj in object_list:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode = 'OBJECT')

    depsgraph = context.evaluated_depsgraph_get()

    for obj in object_list:
        object_properties.append([obj.hide_get(), obj.hide_viewport])
        if hidden_geo:
            global_functions.unhide_object(obj)

        find_region = get_region(default_region, obj.jms.Region)
        find_permutation = get_permutation(default_permutation, obj.jms.Permutation)
        if obj.type == 'ARMATURE':
            global_functions.unhide_object(obj)
            armature_count += 1
            armature = obj
            obj.select_set(True)
            node_list = list(obj.data.bones)

        elif obj.name[0:2].lower() == 'b_' or obj.name[0:4].lower() == 'bone' or obj.name[0:5].lower() == 'frame':
            global_functions.unhide_object(obj)
            node_list.append(obj)
            mesh_frame_count += 1

        elif obj.name[0:1].lower() == '#':
            if set_ignore(obj) == False or hidden_geo:
                if game_version == 'haloce':
                    if not obj.parent == None:
                        if obj.parent.type == 'ARMATURE' or obj.parent.name[0:2].lower() == 'b_' or obj.name[0:4].lower() == 'bone' or obj.parent.name[0:5].lower() == 'frame':
                            marker_list.append(obj)
                            region_list.append(find_region)

                elif game_version == 'halo2':
                    if not export_physics:
                        marker_list.append(obj)
                        region_list.append(find_region)

                else:
                    report({'ERROR'}, "How did you even choose an option that doesn't exist?")
                    return {'CANCELLED'}

        elif obj.name[0:1].lower() == '@' and game_version == 'halo2':
            if set_ignore(obj) == False or hidden_geo:
                if export_collision:
                    if obj.data.uv_layers:
                        material_list = gather_materials(obj, version, game_version, material_list)
                        modifier_list = []
                        if triangulate_faces:
                            for modifier in obj.modifiers:
                                modifier.show_render = True
                                modifier.show_viewport = True
                                modifier.show_in_editmode = True
                                modifier_list.append(modifier.type)

                            if not 'TRIANGULATE' in modifier_list:
                                obj.modifiers.new("Triangulate", type='TRIANGULATE')

                            obj_for_convert = obj.evaluated_get(depsgraph)
                            me = obj_for_convert.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
                            geometry_list.append(me)
                            original_geometry_list.append(obj)

                        else:
                            geometry_list.append(obj.to_mesh(preserve_all_data_layers=True))
                            original_geometry_list.append(obj)

                        region_list.append(find_region)
                        permutation_list.append(find_permutation)

        elif obj.name[0:1].lower() == '$' and game_version == 'halo2':
            if set_ignore(obj) == False or hidden_geo:
                if export_physics:
                    material_list = gather_materials(obj, version, game_version, material_list)
                    if not obj.rigid_body_constraint == None:
                        if obj.rigid_body_constraint.type == 'HINGE':
                            hinge_list.append(obj)

                        elif obj.rigid_body_constraint.type == 'GENERIC':
                            ragdoll_list.append(obj)

                        elif obj.rigid_body_constraint.type == 'GENERIC_SPRING':
                            point_to_point_list.append(obj)

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

        elif not len(obj.jms.XREF_path) == 0 and game_version == 'halo2':
            if set_ignore(obj) == False or hidden_geo:
                instance_markers.append(obj)
                if not obj.jms.XREF_path in instance_xref_paths:
                    instance_xref_paths.append(obj.jms.XREF_path)

        elif obj.jms.bounding_radius == True and game_version == 'halo2':
            if set_ignore(obj) == False or hidden_geo:
                bounding_sphere.append(obj)

        elif obj.type == 'MESH':
            if set_ignore(obj) == False or hidden_geo:
                if obj.data.uv_layers:
                    if game_version == 'haloce':
                        if not obj.parent == None:
                            if obj.parent.type == 'ARMATURE' or obj.parent.name[0:2].lower() == 'b_' or obj.name[0:4].lower() == 'bone' or obj.parent.name[0:5].lower() == 'frame':
                                material_list = gather_materials(obj, version, game_version, material_list)
                                modifier_list = []
                                if triangulate_faces:
                                    for modifier in obj.modifiers:
                                        modifier.show_render = True
                                        modifier.show_viewport = True
                                        modifier.show_in_editmode = True
                                        modifier_list.append(modifier.type)

                                    if not 'TRIANGULATE' in modifier_list:
                                        obj.modifiers.new("Triangulate", type='TRIANGULATE')

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
                        if export_render:
                            material_list = gather_materials(obj, version, game_version, material_list)
                            modifier_list = []
                            if triangulate_faces:
                                for modifier in obj.modifiers:
                                    modifier.show_render = True
                                    modifier.show_viewport = True
                                    modifier.show_in_editmode = True
                                    modifier_list.append(modifier.type)

                                if not 'TRIANGULATE' in modifier_list:
                                    obj.modifiers.new("Triangulate", type='TRIANGULATE')

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
    root_node_count = global_functions.count_root_nodes(node_list)
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

    if global_functions.error_pass(armature_count, report, game_version, node_count, version, extension, geometry_list, marker_count, root_node_count, False, mesh_frame_count, object_count):
        return {'CANCELLED'}

    joined_list = global_functions.sort_list(node_list, armature, False, game_version, version, True)
    reversed_joined_list = global_functions.sort_list(node_list, armature, True, game_version, version, True)
    ce_settings = ''
    directory = filepath.rsplit(os.sep, 1)[0]
    filename = filepath.rsplit(os.sep, 1)[1]
    if game_version == 'haloce':
        if not permutation_ce == '':
            ce_settings += '%s ' % (permutation_ce.replace(' ', '_').replace('\t', '_'))

            if level_of_detail_ce == None:
                ce_settings += '%s ' % ('superhigh')

        if not level_of_detail_ce == None:
            if permutation_ce == '':
                ce_settings += '%s ' % ('unnamed')

            ce_settings += '%s ' % (level_of_detail_ce)

        if not permutation_ce == '' or not level_of_detail_ce == None:
            filename = ''

    file = open(directory + os.sep + ce_settings + filename + model_type + global_functions.get_true_extension(filepath, extension, False), 'w', encoding='%s' % global_functions.get_encoding(game_version))
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

        is_bone = False
        if armature:
            is_bone = True

        bone_matrix = global_functions.get_matrix(node, node, True, armature, joined_list, True, version, False)
        mesh_dimensions = global_functions.get_dimensions(bone_matrix, node, None, None, -1, scale, version, None, False, is_bone, armature, False)
        if version >= 8205:
            file.write(
                '\n;NODE %s' % (joined_list.index(node)) +
                '\n%s' % (node.name) +
                '\n%s' % (parent_node) +
                decimal_4 % (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a) +
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
                '\n'
            )

        else:
            file.write(
                '\n%s' % (node.name) +
                '\n%s' % (first_child_node) +
                '\n%s' % (first_sibling_node) +
                decimal_4 % (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a) +
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
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
        if game_version == 'haloce':
            material_name = '<none>'
            texture_path = '<none>'
            if not material == None:
                material_name = material.name
                if not material.node_tree == None:
                    for node in material.node_tree.nodes:
                        if node.type == 'TEX_IMAGE':
                            if not node.image == None:
                                image_filepath = io_utils.path_reference(node.image.filepath, directory, directory, mode='AUTO', copy_subdir='', copy_set=None, library=None)
                                image_extension = image_filepath.rsplit('.', 1)[1]
                                image_path = image_filepath.rsplit('.', 1)[0]
                                if image_extension.lower() == 'tif' and os.path.exists(image_filepath):
                                    texture_path = image_path

            file.write(
                '\n%s' % (material_name) +
                '\n%s' % (texture_path)
            )

        elif game_version == 'halo2':
            untouched_lod = material[1]
            untouched_region = material[2]
            untouched_permutation = material[3]
            LOD = get_lod(material[1], game_version)
            Permutation = default_permutation
            Region = default_region
            #This doesn't matter for CE but for Halo 2 the region or permutation names can't have any whitespace.
            #Lets fix that here to make sure nothing goes wrong.
            if len(material[3]) != 0:
                safe_permutation = material[3].replace(' ', '_').replace('\t', '_')
                Permutation = safe_permutation

            if len(material[2]) != 0:
                safe_region = material[2].replace(' ', '_').replace('\t', '_')
                Region = safe_region

            material_definition = '(%s)' % (bpy.data.materials.find(material[0].name))
            if not LOD == None:
                material_definition += ' %s' % (LOD)

            if not Permutation == '':
                material_definition += ' %s' % (Permutation)

            if not Region == '':
                material_definition += ' %s' % (Region)

            if version >= 8205:
                file.write(
                    '\n;MATERIAL %s' % (material_list.index([material[0], untouched_lod, untouched_region, untouched_permutation])) +
                    '\n%s' % material[0].name +
                    '\n%s\n' % (material_definition)
                )

            else:
                file.write(
                    '\n%s' % (material[0].name) +
                    '\n%s' % (material_definition)
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

        parent_index = global_functions.get_parent(armature, marker, joined_list, 0, True)
        marker_matrix = global_functions.get_matrix(marker, marker, True, armature, joined_list, False, version, False)
        mesh_dimensions = global_functions.get_dimensions(marker_matrix, marker, None, None, -1, scale, version, None, False, False, armature, False)

        if version >= 8205:
            file.write(
                '\n;MARKER %s' % (marker_list.index(marker)) +
                '\n%s' % (fixed_name) +
                '\n%s' % (parent_index) +
                decimal_4 % (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a) +
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
                decimal_1 % (mesh_dimensions.radius_a) +
                '\n'
            )

        else:
            file.write(
                '\n%s' % (fixed_name) +
                '\n%s' % (region) +
                '\n%s' % (parent_index) +
                decimal_4 % (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a) +
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
                decimal_1 % (mesh_dimensions.radius_a)
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
        starting_ID = -1 * (randint(0, 3000000000))
        for int_markers in instance_markers:
            unique_identifier = starting_ID + (-1 * instance_markers.index(int_markers))
            int_markers_matrix = global_functions.get_matrix(int_markers, int_markers, False, armature, joined_list, False, version, False)
            mesh_dimensions = global_functions.get_dimensions(int_markers_matrix, int_markers, None, None, -1, scale, version, None, False, False, armature, False)
            file.write(
                '\n;XREF OBJECT %s' % (instance_markers.index(int_markers)) +
                '\n%s' % (int_markers.name) +
                '\n%s' % (unique_identifier) +
                '\n%s' % (instance_xref_paths.index(int_markers.jms.XREF_path)) +
                decimal_4 % (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a) +
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
                '\n'
            )

    #write vertices
    for geometry in geometry_list:
        item_index = int(geometry_list.index(geometry))
        original_geo = original_geometry_list[item_index]
        vertex_groups = original_geo.vertex_groups.keys()
        original_geo_matrix = global_functions.get_matrix(original_geo, original_geo, False, armature, joined_list, False, version, False)
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
            jms_triangle.material = get_material(game_version, original_geo, face, geometry, material_list)
            for loop_index in face.loop_indices:
                vert = mesh_verts[mesh_loops[loop_index].vertex_index]
                uv = uv_layer[loop_index].uv
                jms_vertex = JmsVertex()
                vertices.append(jms_vertex)
                pos  = original_geo_matrix @ vert.co
                norm = original_geo_matrix @ (vert.co + vert.normal) - pos
                jms_vertex.pos = pos
                jms_vertex.norm = norm
                jms_vertex.uv = uv
                if len(vert.groups) != 0:
                    object_vert_group_list = []
                    vertex_vert_group_list = []
                    for group_index in range(len(vert.groups)):
                        vert_group = vert.groups[group_index].group
                        object_vertex_group = vertex_groups[vert_group]
                        if armature:
                            if object_vertex_group in armature.data.bones:
                                vertex_vert_group_list.append(group_index)
                                if armature.data.bones[object_vertex_group] in joined_list:
                                    object_vert_group_list.append(vert_group)

                        else:
                            if object_vertex_group in bpy.data.objects:
                                vertex_vert_group_list.append(group_index)
                                if bpy.data.objects[object_vertex_group] in joined_list:
                                    object_vert_group_list.append(vert_group)

                    value = len(object_vert_group_list)
                    if value > 4:
                        value = 4

                    jms_vertex.node_influence_count = value
                    if len(object_vert_group_list) != 0:
                        for group_index in object_vert_group_list:
                            item_index = int(object_vert_group_list.index(group_index))
                            vert_index = int(vertex_vert_group_list[item_index])
                            vert_group = vert.groups[vert_index].group
                            object_vertex_group = vertex_groups[vert_group]
                            if armature:
                                node_obj = armature.data.bones[object_vertex_group]

                            else:
                                node_obj = bpy.data.objects[object_vertex_group]

                            if item_index == 0:
                                jms_vertex.node0 = joined_list.index(node_obj)
                                jms_vertex.node0_weight = '%0.10f' % vert.groups[vert_index].weight

                            if item_index == 1:
                                jms_vertex.node1 = joined_list.index(node_obj)
                                jms_vertex.node1_weight = '%0.10f' % vert.groups[vert_index].weight

                            if item_index == 2:
                                jms_vertex.node2 = joined_list.index(node_obj)
                                jms_vertex.node2_weight = '%0.10f' % vert.groups[vert_index].weight

                            if item_index == 3:
                                jms_vertex.node3 = joined_list.index(node_obj)
                                jms_vertex.node3_weight = '%0.10f' % vert.groups[vert_index].weight

                    else:
                        parent_index = global_functions.get_parent(armature, original_geo, joined_list, 0, True)
                        jms_vertex.node_influence_count = '1'
                        jms_vertex.node0 = parent_index
                        jms_vertex.node0_weight = '1.0000000000'

                else:
                    parent_index = global_functions.get_parent(armature, original_geo, joined_list, 0, True)
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
        norm = jms_vertex.norm
        uv   = jms_vertex.uv
        mesh_dimensions = global_functions.get_dimensions(None, None, None, None, -1, scale, version, jms_vertex, True, False, armature, False)
        norm_i = Decimal(norm[0]).quantize(Decimal('1.0000000000'))
        norm_j = Decimal(norm[1]).quantize(Decimal('1.0000000000'))
        norm_k = Decimal(norm[2]).quantize(Decimal('1.0000000000'))
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
        tex_u = Decimal(uv[0]).quantize(Decimal('1.0000000000'))
        tex_v = Decimal(uv[1]).quantize(Decimal('1.0000000000'))
        tex_w = 0
        if version >= 8205:
            file.write(
                '\n;VERTEX %s' % (vertices.index(jms_vertex)) +
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
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
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
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
            name = spheres.name.split('$', 1)[1]
            mesh_sphere = spheres.to_mesh()
            face = mesh_sphere.polygons[0]
            sphere_material_index = get_material(game_version, spheres, face, mesh_sphere, material_list)
            parent_index = global_functions.get_parent(armature, spheres, joined_list, -1, True)
            sphere_matrix = global_functions.get_matrix(spheres, spheres, True, armature, joined_list, False, version, False)
            mesh_dimensions = global_functions.get_dimensions(sphere_matrix, spheres, None, None, -1, scale, version, None, False, False, armature, False)
            file.write(
                '\n;SPHERE %s' % (sphere_list.index(spheres)) +
                '\n%s' % name +
                '\n%s' % parent_index +
                '\n%s' % sphere_material_index +
                decimal_4 % (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a) +
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
                decimal_1 % mesh_dimensions.radius_a +
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
            name = boxes.name.split('$', 1)[1]
            mesh_boxes = boxes.to_mesh()
            face = mesh_boxes.polygons[0]
            boxes_material_index = get_material(game_version, boxes, face, mesh_boxes, material_list)
            parent_index = global_functions.get_parent(armature, boxes, joined_list, -1, True)
            box_matrix = global_functions.get_matrix(boxes, boxes, True, armature, joined_list, False, version, False)
            mesh_dimensions = global_functions.get_dimensions(box_matrix, boxes, None, None, -1, scale, version, None, False, False, armature, False)
            file.write(
                '\n;BOXES %s' % (box_list.index(boxes)) +
                '\n%s' % name +
                '\n%s' % parent_index +
                '\n%s' % boxes_material_index +
                decimal_4 % (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a) +
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
                decimal_1 % mesh_dimensions.dimension_x_a +
                decimal_1 % mesh_dimensions.dimension_y_a +
                decimal_1 % mesh_dimensions.dimension_z_a +
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
            name = capsule.name.split('$', 1)[1]
            mesh_capsule = capsule.to_mesh()
            face = mesh_capsule.polygons[0]
            capsule_material_index = get_material(game_version, capsule, face, mesh_capsule, material_list)
            parent_index = global_functions.get_parent(armature, capsule, joined_list, -1, True)
            capsule_matrix = global_functions.get_matrix(capsule, capsule, True, armature, joined_list, False, version, False)
            mesh_dimensions = global_functions.get_dimensions(capsule_matrix, capsule, None, None, -1, scale, version, None, False, False, armature, False)
            file.write(
                '\n;CAPSULES %s' % (capsule_list.index(capsule)) +
                '\n%s' % name +
                '\n%s' % parent_index +
                '\n%s' % capsule_material_index +
                decimal_4 % (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a) +
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
                decimal_1 % mesh_dimensions.pill_z_a +
                decimal_1 % mesh_dimensions.radius_a +
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
            name = convex_shape.name.split('$', 1)[1]
            modifier_list = []
            if triangulate_faces:
                for modifier in convex_shape.modifiers:
                    modifier.show_render = True
                    modifier.show_viewport = True
                    modifier.show_in_editmode = True
                    modifier_list.append(modifier.type)

                if not 'TRIANGULATE' in modifier_list:
                    convex_shape.modifiers.new("Triangulate", type='TRIANGULATE')

                convex_shape_for_convert = convex_shape.evaluated_get(depsgraph)
                mesh_convex_shape = convex_shape_for_convert.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)

            else:
                mesh_convex_shape = convex_shape.to_mesh(preserve_all_data_layers=True)

            convex_shape_vert_count = len(mesh_convex_shape.vertices)
            face = mesh_convex_shape.polygons[0]
            convex_shape_material_index = get_material(game_version, convex_shape, face, mesh_convex_shape, material_list)
            parent_index = global_functions.get_parent(armature, convex_shape, joined_list, -1, True)
            convex_matrix = global_functions.get_matrix(convex_shape, convex_shape, True, armature, joined_list, False, version, False)
            mesh_dimensions = global_functions.get_dimensions(convex_matrix, convex_shape, None, None, -1, scale, version, None, False, False, armature, False)
            file.write(
                '\n;CONVEX %s' % (convex_shape_list.index(convex_shape)) +
                '\n%s' % name +
                '\n%s' % parent_index +
                '\n%s' % convex_shape_material_index +
                decimal_4 % (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a) +
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
                '\n%s' % convex_shape_vert_count
            )

            for vertex in mesh_convex_shape.vertices:
                pos  = vertex.co
                jms_vertex = JmsVertex()
                jms_vertex.pos = pos
                mesh_dimensions = global_functions.get_dimensions(None, None, None, None, -1, scale, version, jms_vertex, True, False, armature, False)
                file.write(
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a)
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

        for ragdoll in ragdoll_list:
            name = ragdoll.name.split('$', 1)[1]
            body_a_obj = ragdoll.rigid_body_constraint.object1
            body_b_obj = ragdoll.rigid_body_constraint.object2
            body_a_index = global_functions.get_parent(armature, body_a_obj, joined_list, -1, True)
            body_b_index = global_functions.get_parent(armature, body_b_obj, joined_list, -1, True)
            body_a_matrix = global_functions.get_matrix(ragdoll, body_a_obj, True, armature, joined_list, False, version, False)
            body_b_matrix = global_functions.get_matrix(ragdoll, body_b_obj, True, armature, joined_list, False, version, False)
            mesh_dimensions = global_functions.get_dimensions(body_a_matrix, body_a_obj, body_b_matrix, body_b_obj, -1, scale, version, None, False, False, armature, False)
            min_angle_x = 0
            max_angle_x = 0
            min_angle_y = 0
            max_angle_y = 0
            min_angle_z = 0
            max_angle_z = 0
            is_limited_x = int(ragdoll.rigid_body_constraint.use_limit_ang_x)
            is_limited_y = int(ragdoll.rigid_body_constraint.use_limit_ang_y)
            is_limited_z = int(ragdoll.rigid_body_constraint.use_limit_ang_z)
            if is_limited_x:
                min_angle_x = degrees(ragdoll.rigid_body_constraint.limit_ang_x_lower)
                max_angle_x = degrees(ragdoll.rigid_body_constraint.limit_ang_x_upper)

            if is_limited_y:
                min_angle_y = degrees(ragdoll.rigid_body_constraint.limit_ang_y_lower)
                max_angle_y = degrees(ragdoll.rigid_body_constraint.limit_ang_y_upper)

            if is_limited_z:
                min_angle_z = degrees(ragdoll.rigid_body_constraint.limit_ang_z_lower)
                max_angle_z = degrees(ragdoll.rigid_body_constraint.limit_ang_z_upper)

            file.write(
                '\n;RAGDOLL %s' % (ragdoll_list.index(ragdoll)) +
                '\n%s' % name +
                '\n%s' % body_a_index +
                '\n%s' % body_b_index +
                decimal_4 % (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a) +
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
                decimal_4 % (mesh_dimensions.quat_i_b, mesh_dimensions.quat_j_b, mesh_dimensions.quat_k_b, mesh_dimensions.quat_w_b) +
                decimal_3 % (mesh_dimensions.pos_x_b, mesh_dimensions.pos_y_b, mesh_dimensions.pos_z_b) +
                decimal_1 % (min_angle_x) +
                decimal_1 % (max_angle_x) +
                decimal_1 % (min_angle_y) +
                decimal_1 % (max_angle_y) +
                decimal_1 % (min_angle_z) +
                decimal_1 % (max_angle_z) +
                '\n'
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
            body_a_index = global_functions.get_parent(armature, body_a_obj, joined_list, -1, True)
            body_b_index = global_functions.get_parent(armature, body_b_obj, joined_list, -1, True)
            body_a_matrix = global_functions.get_matrix(hinge, body_a_obj, True, armature, joined_list, False, version, False)
            body_b_matrix = global_functions.get_matrix(hinge, body_b_obj, True, armature, joined_list, False, version, False)
            mesh_dimensions = global_functions.get_dimensions(body_a_matrix, body_a_obj, body_b_matrix, body_b_obj, -1, scale, version, None, False, False, armature, False)
            is_limited = int(hinge.rigid_body_constraint.use_limit_ang_z)
            friction_limit = 0
            min_angle = 0
            max_angle = 0
            if body_b_obj:
                friction_limit = body_b_obj.rigid_body.angular_damping

            if is_limited:
                min_angle = degrees(hinge.rigid_body_constraint.limit_ang_z_lower)
                max_angle = degrees(hinge.rigid_body_constraint.limit_ang_z_upper)

            file.write(
                '\n;HINGE %s' % (hinge_list.index(hinge)) +
                '\n%s' % name +
                '\n%s' % body_a_index +
                '\n%s' % body_b_index +
                decimal_4 % (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a) +
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
                decimal_4 % (mesh_dimensions.quat_i_b, mesh_dimensions.quat_j_b, mesh_dimensions.quat_k_b, mesh_dimensions.quat_w_b) +
                decimal_3 % (mesh_dimensions.pos_x_b, mesh_dimensions.pos_y_b, mesh_dimensions.pos_z_b) +
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

            for point_to_point in point_to_point_list:
                name = point_to_point.name.split('$', 1)[1]
                body_a_obj = point_to_point.rigid_body_constraint.object1
                body_b_obj = point_to_point.rigid_body_constraint.object2
                body_a_index = global_functions.get_parent(armature, body_a_obj, joined_list, -1, True)
                body_b_index = global_functions.get_parent(armature, body_b_obj, joined_list, -1, True)
                body_a_matrix = global_functions.get_matrix(body_a_obj, point_to_point, True, armature, joined_list, False, version, False)
                body_b_matrix = global_functions.get_matrix(body_b_obj, point_to_point, True, armature, joined_list, False, version, False)
                mesh_dimensions = global_functions.get_dimensions(body_a_matrix, body_a_obj, body_b_matrix, body_b_obj, -1, scale, version, None, False, False, armature, False)
                is_limited_x = int(point_to_point.rigid_body_constraint.use_limit_ang_x)
                is_limited_y = int(point_to_point.rigid_body_constraint.use_limit_ang_y)
                is_limited_z = int(point_to_point.rigid_body_constraint.use_limit_ang_z)
                is_spring_z = int(point_to_point.rigid_body_constraint.use_limit_lin_z)
                constraint_type = 0
                min_angle_x = degrees(0)
                max_angle_x = degrees(0)
                min_angle_y = degrees(0)
                max_angle_y = degrees(0)
                min_angle_z = degrees(0)
                max_angle_z = degrees(0)
                spring_length = degrees(0)
                if is_limited_x == False and is_limited_y == False and is_limited_z == False and is_spring_z == False:
                    constraint_type = 0
                    min_angle_x = degrees(point_to_point.rigid_body_constraint.limit_ang_x_lower)
                    max_angle_x = degrees(point_to_point.rigid_body_constraint.limit_ang_x_upper)
                    min_angle_y = degrees(point_to_point.rigid_body_constraint.limit_ang_y_lower)
                    max_angle_y = degrees(point_to_point.rigid_body_constraint.limit_ang_y_upper)
                    min_angle_z = degrees(point_to_point.rigid_body_constraint.limit_ang_z_lower)
                    max_angle_z = degrees(point_to_point.rigid_body_constraint.limit_ang_z_upper)
                    spring_length = degrees(0)

                elif is_limited_x == True and is_limited_y == True and is_limited_z == True and is_spring_z == False:
                    constraint_type = 1
                    min_angle_x = degrees(point_to_point.rigid_body_constraint.limit_ang_x_lower)
                    max_angle_x = degrees(point_to_point.rigid_body_constraint.limit_ang_x_upper)
                    min_angle_y = degrees(point_to_point.rigid_body_constraint.limit_ang_y_lower)
                    max_angle_y = degrees(point_to_point.rigid_body_constraint.limit_ang_y_upper)
                    min_angle_z = degrees(point_to_point.rigid_body_constraint.limit_ang_z_lower)
                    max_angle_z = degrees(point_to_point.rigid_body_constraint.limit_ang_z_upper)
                    spring_length = degrees(0)

                elif is_limited_x == False and is_limited_y == False and is_limited_z == False and is_spring_z == True:
                    constraint_type = 2
                    min_angle_x = degrees(point_to_point.rigid_body_constraint.limit_ang_x_lower)
                    max_angle_x = degrees(point_to_point.rigid_body_constraint.limit_ang_x_upper)
                    min_angle_y = degrees(point_to_point.rigid_body_constraint.limit_ang_y_lower)
                    max_angle_y = degrees(point_to_point.rigid_body_constraint.limit_ang_y_upper)
                    min_angle_z = degrees(point_to_point.rigid_body_constraint.limit_ang_z_lower)
                    max_angle_z = degrees(point_to_point.rigid_body_constraint.limit_ang_z_upper)
                    spring_length = degrees(point_to_point.rigid_body_constraint.limit_lin_z_upper)

                else:
                    report({'WARNING'}, 'Improper point to point.')

                file.write(
                    '\n;POINT_TO_POINT %s' % (point_to_point_list.index(point_to_point)) +
                    '\n%s' % name +
                    '\n%s' % body_a_index +
                    '\n%s' % body_b_index +
                    decimal_4 % (mesh_dimensions.quat_i_a, mesh_dimensions.quat_j_a, mesh_dimensions.quat_k_a, mesh_dimensions.quat_w_a) +
                    decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
                    decimal_4 % (mesh_dimensions.quat_i_b, mesh_dimensions.quat_j_b, mesh_dimensions.quat_k_b, mesh_dimensions.quat_w_b) +
                    decimal_3 % (mesh_dimensions.pos_x_b, mesh_dimensions.pos_y_b, mesh_dimensions.pos_z_b) +
                    '\n%s' % (constraint_type) +
                    decimal_1 % (min_angle_x) +
                    decimal_1 % (max_angle_x) +
                    decimal_1 % (min_angle_y) +
                    decimal_1 % (max_angle_y) +
                    decimal_1 % (min_angle_z) +
                    decimal_1 % (max_angle_z) +
                    decimal_1 % (spring_length) +
                    '\n'
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
            bound_sphere_matrix = global_functions.get_matrix(bound_sphere, bound_sphere, False, armature, joined_list, False, version, False)
            mesh_dimensions = global_functions.get_dimensions(bound_sphere_matrix, bound_sphere, None, None, -1, scale, version, None, False, False, armature, False)
            file.write(
                '\n;BOUNDING SPHERE %s' % (bounding_sphere.index(bound_sphere)) +
                decimal_3 % (mesh_dimensions.pos_x_a, mesh_dimensions.pos_y_a, mesh_dimensions.pos_z_a) +
                decimal_1 % mesh_dimensions.radius_a +
                '\n'
            )

    file.close()
    for obj in object_list:
        item_index = object_list.index(obj)
        property_value = object_properties[item_index]
        obj.hide_set(property_value[0])
        obj.hide_viewport = property_value[1]

    report({'INFO'}, "Export completed successfully")

def write_file(context,
               filepath,
               report,
               extension,
               extension_ce,
               extension_h2,
               jms_version,
               jms_version_ce,
               jms_version_h2,
               game_version,
               triangulate_faces,
               scale_enum,
               scale_float,
               console,
               permutation_ce,
               level_of_detail_ce,
               hidden_geo,
               export_render,
               export_collision,
               export_physics):

    global_functions.unhide_all_collections()

    object_list = list(bpy.context.scene.objects)
    node_count = 0
    marker_count = 0
    collision_count = 0
    physics_count = 0
    xref_count = 0
    bounding_radius_count = 0
    render_count = 0
    for obj in object_list:
        if obj.type == 'ARMATURE':
            node_count += 1

        elif obj.name[0:2].lower() == 'b_' or obj.name[0:4].lower() == 'bone' or obj.name[0:5].lower() == 'frame':
            node_count += 1

        elif obj.name[0:1].lower() == '#':
            if set_ignore(obj) == False or hidden_geo:
                marker_count += 1

        elif obj.name[0:1].lower() == '@':
            if set_ignore(obj) == False or hidden_geo:
                collision_count += 1

        elif obj.name[0:1].lower() == '$':
            if set_ignore(obj) == False or hidden_geo:
                physics_count += 1

        elif not len(obj.jms.XREF_path) == 0:
            if set_ignore(obj) == False or hidden_geo:
                xref_count += 1

        elif obj.jms.bounding_radius:
            if set_ignore(obj) == False or hidden_geo:
                bounding_radius_count += 1

        elif obj.type== 'MESH':
            if set_ignore(obj) == False or hidden_geo:
                render_count += 1

    keywords = [context,
                filepath,
                report,
                extension,
                extension_ce,
                extension_h2,
                jms_version,
                jms_version_ce,
                jms_version_h2,
                game_version,
                triangulate_faces,
                scale_enum,
                scale_float,
                console,
                permutation_ce,
                level_of_detail_ce,
                hidden_geo,
                object_list]

    if render_count == 0 and collision_count == 0 and physics_count == 0 and marker_count == 0:
        report({'ERROR'}, "No objects in scene")
        return {'CANCELLED'}

    if game_version == 'haloce':
        model_type = ""
        file_layout(*keywords, True, True, True, model_type)

    elif game_version == 'halo2':
        if export_render and render_count > 0:
            model_type = ""
            file_layout(*keywords, export_render, False, False, model_type)

        if export_collision and collision_count > 0:
            model_type = "_collision"
            file_layout(*keywords, False, export_collision, False, model_type)

        if export_physics and physics_count > 0:
            model_type = "_physics"
            file_layout(*keywords, False, False, export_physics, model_type)

    else:
        report({'ERROR'}, "How did you even choose an option that doesn't exist?")
        return {'CANCELLED'}

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_scene.jms()
