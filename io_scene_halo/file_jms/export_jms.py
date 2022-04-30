# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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
from ..global_functions import mesh_processing, global_functions

def command_queue(context, filepath, report, jms_version, jms_version_ce, jms_version_h2, jms_version_h3, generate_checksum, folder_structure, folder_type, apply_modifiers, triangulate_faces, fix_rotations, edge_split, use_edge_angle, use_edge_sharp, split_angle, clean_normalize_weights, scale_enum, scale_float, console, permutation_ce, level_of_detail_ce, hidden_geo, export_render, export_collision, export_physics, game_version, world_nodes):
    object_properties = []
    node_prefix_tuple = ('b ', 'b_', 'bone', 'frame', 'bip01')
    limit_value = 0.00000000009

    world_node_count = 0
    armature_count = 0
    mesh_frame_count = 0
    render_count = 0
    collision_count = 0
    physics_count = 0
    armature = None
    node_list = []
    render_marker_list = []
    collision_marker_list = []
    physics_marker_list = []
    marker_list = []
    instance_xref_paths = []
    instance_markers = []
    render_geometry_list = []
    collision_geometry_list = []
    sphere_list = []
    box_list = []
    capsule_list = []
    convex_shape_list = []
    ragdoll_list = []
    hinge_list = []
    car_wheel_list = []
    point_to_point_list = []
    prismatic_list = []
    bounding_sphere_list = []
    skylight_list = []

    scene = context.scene

    collections = []
    layer_collections = list(context.view_layer.layer_collection.children)

    while len(layer_collections) > 0:
        collection_batch = layer_collections
        layer_collections = []
        for collection in collection_batch:
            collections.append(collection)
            for collection_child in collection.children:
                layer_collections.append(collection_child)

    jmi = False
    if not world_nodes == None:
        jmi = True
        object_list = world_nodes

    else:
        object_list = list(scene.objects)

    edge_split = global_functions.EdgeSplit(edge_split, use_edge_angle, split_angle, use_edge_sharp)

    version = global_functions.get_version(jms_version, jms_version_ce, jms_version_h2, jms_version_h3, game_version, console)
    level_of_detail_ce = mesh_processing.get_lod(level_of_detail_ce, game_version)
    custom_scale = global_functions.set_scale(scale_enum, scale_float)

    for obj in object_list:
        if obj.type== 'MESH' and mesh_processing.set_ignore(collections, obj) == False:
            if clean_normalize_weights:
                mesh_processing.vertex_group_clean_normalize(context, obj, limit_value)

            if apply_modifiers:
                mesh_processing.add_modifier(context, obj, triangulate_faces, edge_split, None)

    depsgraph = context.evaluated_depsgraph_get()
    for obj in object_list:
        object_properties.append((obj.hide_get(), obj.hide_viewport))
        if hidden_geo:
            mesh_processing.unhide_object(collections, obj)

        name = obj.name.lower()
        parent_name = None
        if obj.parent:
            parent_name = obj.parent.name.lower()

        if name[0:1] == '!':
            world_node_count += 1

        elif obj.type == 'ARMATURE':
            mesh_processing.unhide_object(collections, obj)
            armature = obj
            armature_bones = obj.data.bones
            armature_count += 1
            node_list = list(armature_bones)

        elif name.startswith(node_prefix_tuple):
            mesh_processing.unhide_object(collections, obj)
            mesh_frame_count += 1
            node_list.append(obj)

        elif name[0:1] == '#':
            if mesh_processing.set_ignore(collections, obj) == False or hidden_geo:
                if obj.parent and (obj.parent.type == 'ARMATURE' or parent_name.startswith(node_prefix_tuple)):
                    mask_type = obj.marker.marker_mask_type
                    if export_render and mask_type =='0':
                        render_marker_list.append(obj)
                        render_count += 1

                    elif export_collision and mask_type =='1':
                        collision_marker_list.append(obj)
                        collision_count += 1

                    elif export_physics and mask_type =='2':
                        physics_marker_list.append(obj)
                        physics_count += 1

                    elif mask_type =='3':
                        marker_list.append(obj)
                        render_count += 1
                        collision_count += 1
                        physics_count += 1

        elif name[0:1] == '@' and len(obj.data.polygons) > 0:
            if export_collision and (not mesh_processing.set_ignore(collections, obj) or hidden_geo):
                if obj.parent and (obj.parent.type == 'ARMATURE' or parent_name.startswith(node_prefix_tuple)):
                    collision_count += 1
                    if apply_modifiers:
                        obj_for_convert = obj.evaluated_get(depsgraph)
                        evaluted_mesh = obj_for_convert.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)

                    else:
                        evaluted_mesh = obj.to_mesh(preserve_all_data_layers=True)

                    collision_geometry_list.append((evaluted_mesh, obj))

        elif name[0:1] == '$' and not game_version == "haloce" and version > 8205:
            if export_physics and (not mesh_processing.set_ignore(collections, obj) or hidden_geo):
                physics_count += 1
                if obj.rigid_body_constraint:
                    if obj.rigid_body_constraint.type == 'HINGE':
                        hinge_list.append(obj)

                    elif obj.rigid_body_constraint.type == 'GENERIC':
                        ragdoll_list.append(obj)

                    elif obj.rigid_body_constraint.type == 'GENERIC_SPRING':
                        point_to_point_list.append(obj)

                else:
                    if obj.type == 'MESH':
                        if obj.data.ass_jms.Object_Type == 'SPHERE':
                            sphere_list.append(obj)

                        elif obj.data.ass_jms.Object_Type == 'BOX':
                            box_list.append(obj)

                        elif obj.data.ass_jms.Object_Type == 'CAPSULES':
                            capsule_list.append(obj)

                        elif obj.data.ass_jms.Object_Type == 'CONVEX SHAPES':
                            if apply_modifiers:
                                obj_for_convert = obj.evaluated_get(depsgraph)
                                evaluted_mesh = obj_for_convert.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)

                            else:
                                evaluted_mesh = obj.to_mesh(preserve_all_data_layers=True)

                            convex_shape_list.append((evaluted_mesh, obj))

        elif obj.type == 'LIGHT' and obj.data.type == 'SUN' and version > 8212:
            if mesh_processing.set_ignore(collections, obj) == False or hidden_geo:
                if export_render:
                    skylight_list.append(obj)

        elif obj.type== 'MESH':
            if export_render and (not mesh_processing.set_ignore(collections, obj) or hidden_geo):
                if not global_functions.string_empty_check(obj.data.ass_jms.XREF_path) and version > 8205:
                    instance_markers.append(obj)
                    if not obj.data.ass_jms.XREF_path in instance_xref_paths:
                        instance_xref_paths.append(obj.data.ass_jms.XREF_path)

                elif obj.data.ass_jms.bounding_radius and version >= 8209:
                    bounding_sphere_list.append(obj)

                elif len(obj.data.polygons) > 0:
                    if obj.parent and (obj.parent.type == 'ARMATURE' or parent_name.startswith(node_prefix_tuple)):
                        render_count += 1
                        if apply_modifiers:
                            obj_for_convert = obj.evaluated_get(depsgraph)
                            evaluted_mesh = obj_for_convert.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)

                        else:
                            evaluted_mesh = obj.to_mesh(preserve_all_data_layers=True)

                        render_geometry_list.append((evaluted_mesh, obj))

    blend_scene = global_functions.BlendScene(world_node_count, armature_count, mesh_frame_count, render_count, collision_count, physics_count, armature, node_list, render_marker_list, collision_marker_list, physics_marker_list, marker_list, instance_xref_paths, instance_markers, render_geometry_list, collision_geometry_list, sphere_list, box_list, capsule_list, convex_shape_list, ragdoll_list, hinge_list, car_wheel_list, point_to_point_list, prismatic_list, bounding_sphere_list, skylight_list)

    global_functions.validate_halo_jms_scene(game_version, version, blend_scene, object_list, jmi)

    if export_render and blend_scene.render_count > 0:
        model_type = "render"

        build_asset(context, blend_scene, filepath, version, game_version, generate_checksum, fix_rotations, folder_structure, folder_type, model_type, jmi, permutation_ce, level_of_detail_ce, custom_scale, report)

    if export_collision and blend_scene.collision_count > 0:
        model_type = "collision"

        build_asset(context, blend_scene, filepath, version, game_version, generate_checksum, fix_rotations, folder_structure, folder_type, model_type, jmi, permutation_ce, level_of_detail_ce, custom_scale, report)

    if export_physics and blend_scene.physics_count > 0:
        model_type = "physics"

        build_asset(context, blend_scene, filepath, version, game_version, generate_checksum, fix_rotations, folder_structure, folder_type, model_type, jmi, permutation_ce, level_of_detail_ce, custom_scale, report)

    for idx, obj in enumerate(object_list):
        property_value = object_properties[idx]
        obj.hide_set(property_value[0])
        obj.hide_viewport = property_value[1]

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_scene.jms()
