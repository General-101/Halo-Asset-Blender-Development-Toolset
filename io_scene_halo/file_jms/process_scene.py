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

from math import degrees
from .format import JMSAsset
from random import seed, randint
from mathutils import Vector, Matrix
from ..global_functions import mesh_processing, global_functions

def process_scene(context, version, game_version, generate_checksum, fix_rotations, use_maya_sorting, model_type, blend_scene, custom_scale, loop_normals, write_textures):
    JMS = JMSAsset()
    JMS.node_checksum = 0

    default_region = mesh_processing.get_default_region_permutation_name(game_version)
    default_permutation = mesh_processing.get_default_region_permutation_name(game_version)

    region_list = ['unnamed']
    permutation_list = []
    material_list = []

    sorted_list = global_functions.sort_list(blend_scene.node_list, blend_scene.armature, game_version, version, False)
    joined_list = sorted_list[0]
    reversed_joined_list = sorted_list[1]

    for node in joined_list:
        is_bone = False
        if blend_scene.armature:
            is_bone = True

        find_child_node = global_functions.get_child(node, reversed_joined_list, game_version, use_maya_sorting)
        find_sibling_node = global_functions.get_sibling(blend_scene.armature, node, reversed_joined_list, game_version, use_maya_sorting)

        first_child_node = -1
        first_sibling_node = -1
        parent_node = -1

        if not find_child_node == None:
            first_child_node = joined_list.index(find_child_node)
        if not find_sibling_node == None:
            first_sibling_node = joined_list.index(find_sibling_node)
        if not node.parent == None and not node.parent.name.startswith('!'):
            parent_node = joined_list.index(node.parent)

        bone_matrix = global_functions.get_matrix(node, node, True, blend_scene.armature, joined_list, True, version, 'JMS', False, custom_scale, fix_rotations)
        mesh_dimensions = global_functions.get_dimensions(bone_matrix, node, version, is_bone, 'JMS', custom_scale)

        name = node.name
        child = first_child_node
        sibling = first_sibling_node
        parent = parent_node

        current_node_children = []
        children = []
        for child_node in node.children:
            if child_node in joined_list:
                current_node_children.append(child_node.name)

        current_node_children.sort()

        if is_bone:
            for child_node in current_node_children:
                children.append(joined_list.index(blend_scene.armature.data.bones[child_node]))

        else:
            for child_node in current_node_children:
                children.append(joined_list.index(bpy.data.objects[child_node]))

        rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
        translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])

        JMS.nodes.append(JMSAsset.Node(name, children, child, sibling, parent))
        JMS.transforms.append(JMSAsset.Transform(translation, rotation))

    if generate_checksum:
        JMS.node_checksum = global_functions.node_hierarchy_checksum(JMS.nodes, JMS.nodes[0], JMS.node_checksum)

    all_marker_list = blend_scene.marker_list
    if model_type == global_functions.ModelTypeEnum.render:
        all_marker_list = blend_scene.marker_list + blend_scene.render_marker_list

    elif model_type == global_functions.ModelTypeEnum.collision:
        all_marker_list = blend_scene.marker_list + blend_scene.collision_marker_list

    else:
        all_marker_list = blend_scene.marker_list + blend_scene.physics_marker_list

    for marker in all_marker_list:
        marker_name = marker.name
        if not global_functions.string_empty_check(marker.ass_jms.name_override):
            marker_name = marker.ass_jms.name_override

        if marker_name.startswith('#'):
            marker_name = marker_name.split('#', 1)[1] #remove marker symbol from name in case someone thinks they still need it here.

        region_idx = -1

        parent_idx = global_functions.get_parent(blend_scene.armature, marker, joined_list, 0)
        marker_matrix = global_functions.get_matrix(marker, marker, True, blend_scene.armature, joined_list, False, version, 'JMS', False, custom_scale, fix_rotations, 0)
        mesh_dimensions = global_functions.get_dimensions(marker_matrix, marker, version, False, 'JMS', custom_scale)

        rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
        translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])
        scale = (mesh_dimensions.object_radius)

        if marker.type == 'EMPTY':
            scale = (mesh_dimensions.scale[0])
            if not marker.ass_jms.marker_region == '':
                if not marker.ass_jms.marker_region in region_list:
                    region_list.append(marker.ass_jms.marker_region)

                region_idx = region_list.index(marker.ass_jms.marker_region)

        elif marker.type == 'MESH':
            if not marker.active_region == -1:
                region_name = marker.region_list[marker.active_region].name
                if not region_name in region_list:
                    region_list.append(region_name)

                region_idx = region_list.index(region_name)

            elif not marker.ass_jms.marker_region == '':
                if not marker.ass_jms.marker_region in region_list:
                    region_list.append(marker.ass_jms.marker_region)

                region_idx = region_list.index(marker.ass_jms.marker_region)

        JMS.markers.append(JMSAsset.Marker(marker_name, region_idx, parent_idx[0], rotation, translation, scale))

    if model_type == global_functions.ModelTypeEnum.render:
        for xref_instance in blend_scene.xref_instances:
            xref_path = xref_instance[0]
            xref_name = xref_instance[1]

            JMS.xref_instances.append(JMSAsset.XREF(xref_path, xref_name))

        seed(1)
        starting_ID = -1 * (randint(0, 3000000000))
        for idx, int_markers in enumerate(blend_scene.instance_markers):
            name = int_markers.name
            unique_identifier = starting_ID - idx

            xref_path = int_markers.data.ass_jms.XREF_path
            xref_name = int_markers.data.ass_jms.XREF_name
            if global_functions.string_empty_check(xref_name):
                xref_name = os.path.basename(xref_path).rsplit('.', 1)[0]

            xref_tuple = (xref_path, xref_name)

            index = blend_scene.xref_instances.index(xref_tuple)
            int_markers_matrix = global_functions.get_matrix(int_markers, int_markers, False, blend_scene.armature, joined_list, False, version, 'JMS', False, custom_scale, fix_rotations)
            mesh_dimensions = global_functions.get_dimensions(int_markers_matrix, int_markers, version, False, 'JMS', custom_scale)

            rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
            translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])

            JMS.xref_markers.append(JMSAsset.XREF_Marker(name, unique_identifier, index, rotation, translation))

        for bound_sphere in blend_scene.bounding_sphere_list:
            bound_sphere_matrix = global_functions.get_matrix(bound_sphere, bound_sphere, False, blend_scene.armature, joined_list, False, version, 'JMS', False, custom_scale, fix_rotations)
            mesh_dimensions = global_functions.get_dimensions(bound_sphere_matrix, bound_sphere, version, False, 'JMS', custom_scale)
            translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])
            scale = mesh_dimensions.object_radius

            JMS.bounding_spheres.append(JMSAsset.Bounding_Sphere(translation, scale))

        for light in blend_scene.skylight_list:
            down_vector = Vector((0, 0, -1))
            down_vector.rotate(light.rotation_euler)

            direction = (down_vector[0], down_vector[1], down_vector[2])
            radiant_intensity =  (light.data.color[0], light.data.color[1], light.data.color[2])
            solid_angle = light.data.energy
            skylight = JMSAsset.Skylight(direction, radiant_intensity, solid_angle)
            JMS.skylights.append(skylight)

    if model_type == global_functions.ModelTypeEnum.render or model_type == global_functions.ModelTypeEnum.collision:
        geometry_list = blend_scene.render_geometry_list
        if model_type == global_functions.ModelTypeEnum.collision:
            geometry_list = blend_scene.collision_geometry_list

        for idx, geometry in enumerate(geometry_list):
            evaluted_mesh = geometry[0]
            original_geo = geometry[1]
            vertex_groups = original_geo.vertex_groups.keys()
            original_geo_matrix = global_functions.get_matrix(original_geo, original_geo, False, blend_scene.armature, joined_list, False, version, "JMS", False, custom_scale, fix_rotations)
            region_count = len(original_geo.region_list)
            for idx, face in enumerate(evaluted_mesh.polygons):
                face_set = (None, default_permutation, default_region)
                region_index = -1
                if game_version == "halo1":
                    region_index = region_list.index(default_region)

                lod = face_set[0]
                permutation = face_set[1]
                region = face_set[2]
                if not original_geo.active_region == -1 and region_count > 0:
                    region_idx = evaluted_mesh.get_custom_attribute().data[idx].value - 1
                    if not region_idx == -1 and not region_idx >= region_count:
                        face_set = mesh_processing.process_mesh_export_face_set(default_permutation, default_region, game_version, original_geo, region_idx)
                        lod = face_set[0]
                        permutation = face_set[1]
                        region = face_set[2]
                        if not region in region_list:
                            region_list.append(region)

                        region_index = region_list.index(region)
                        if not game_version == "halo1":
                            if not permutation in permutation_list:
                                permutation_list.append(permutation)

                material = global_functions.get_material(game_version, original_geo, face, evaluted_mesh, lod, region, permutation)
                material_index = -1
                if not material == -1:
                    material_list = global_functions.gather_materials(game_version, material, material_list, "JMS")
                    material_index = material_list.index(material)

                vert_count = len(JMS.vertices)
                v0 = vert_count
                v1 = vert_count + 1
                v2 = vert_count + 2
                if original_geo_matrix.determinant() < 0.0:
                    v0 = vert_count + 2
                    v1 = vert_count + 1
                    v2 = vert_count

                JMS.triangles.append(JMSAsset.Triangle(region_index, material_index, v0, v1, v2))
                for loop_index in face.loop_indices:
                    point_idx = evaluted_mesh.loops[loop_index].vertex_index
                    loop_data = evaluted_mesh.loops[loop_index]
                    vertex_data = evaluted_mesh.vertices[loop_data.vertex_index]

                    region = region_index
                    normal = evaluted_mesh.corner_normals[loop_index].vector.normalized()
                    scaled_translation, normal = mesh_processing.process_mesh_export_vert(vertex_data, "JMS", original_geo_matrix, custom_scale)
                    uv_set = mesh_processing.process_mesh_export_uv(evaluted_mesh, "JMS", loop_index, version)
                    color = mesh_processing.process_mesh_export_color(evaluted_mesh, loop_index, point_idx)
                    node_influence_count, node_set = mesh_processing.process_mesh_export_weights(vertex_data, blend_scene.armature, original_geo, vertex_groups, joined_list, "JMS")

                    JMS.vertices.append(JMSAsset.Vertex(node_influence_count, node_set, region, scaled_translation, normal, color, uv_set))

            original_geo.to_mesh_clear()

    if model_type == global_functions.ModelTypeEnum.physics:
        for spheres in blend_scene.sphere_list:
            name = spheres.name.split('$', 1)[1]
            mesh_sphere = spheres.to_mesh()
            face = mesh_sphere.polygons[0]

            lod = None
            region = default_region
            permutation = default_permutation
            if not spheres.active_region == -1:
                face_set = spheres.region_list[spheres.active_region].name.split()
                lod, permutation, region = global_functions.material_definition_parser(False, face_set, default_region, default_permutation)

                if not permutation in permutation_list:
                    permutation_list.append(permutation)

                if not region in region_list:
                    region_list.append(region)

            material = global_functions.get_material(game_version, spheres, face, mesh_sphere, lod, region, permutation)
            material_index = -1
            if not material == -1:
                material_list = global_functions.gather_materials(game_version, material, material_list, 'JMS')
                material_index = material_list.index(material)

            parent_index = global_functions.get_parent(blend_scene.armature, spheres, joined_list, -1)
            sphere_matrix = global_functions.get_matrix(spheres, spheres, True, blend_scene.armature, joined_list, False, version, 'JMS', False, custom_scale, fix_rotations)
            mesh_dimensions = global_functions.get_dimensions(sphere_matrix, spheres, version, False, 'JMS', custom_scale)

            rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
            translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])
            scale = (mesh_dimensions.object_radius)

            JMS.spheres.append(JMSAsset.Sphere(name, parent_index[0], material_index, rotation, translation, scale))
            spheres.to_mesh_clear()

        for boxes in blend_scene.box_list:
            name = boxes.name.split('$', 1)[1]
            mesh_boxes = boxes.to_mesh()
            face = mesh_boxes.polygons[0]

            lod = None
            region = default_region
            permutation = default_permutation
            if not boxes.active_region == -1:
                face_set = boxes.region_list[boxes.active_region].name.split()
                lod, permutation, region = global_functions.material_definition_parser(False, face_set, default_region, default_permutation)

                if not permutation in permutation_list:
                    permutation_list.append(permutation)

                if not region in region_list:
                    region_list.append(region)

            material = global_functions.get_material(game_version, boxes, face, mesh_boxes, lod, region, permutation)
            material_index = -1
            if not material == -1:
                material_list = global_functions.gather_materials(game_version, material, material_list, 'JMS')
                material_index = material_list.index(material)

            parent_index = global_functions.get_parent(blend_scene.armature, boxes, joined_list, -1)
            box_matrix = global_functions.get_matrix(boxes, boxes, True, blend_scene.armature, joined_list, False, version, 'JMS', False, custom_scale, fix_rotations)
            mesh_dimensions = global_functions.get_dimensions(box_matrix, boxes, version, False, 'JMS', custom_scale)

            rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
            translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])
            width = (mesh_dimensions.dimension[0])
            length = (mesh_dimensions.dimension[1])
            height = (mesh_dimensions.dimension[2])

            JMS.boxes.append(JMSAsset.Box(name, parent_index[0], material_index, rotation, translation, width, length, height))
            boxes.to_mesh_clear()

        for capsule in blend_scene.capsule_list:
            name = capsule.name.split('$', 1)[1]
            mesh_capsule = capsule.to_mesh()
            face = mesh_capsule.polygons[0]

            lod = None
            region = default_region
            permutation = default_permutation
            if not capsule.active_region == -1:
                face_set = capsule.region_list[capsule.active_region].name.split()
                lod, permutation, region = global_functions.material_definition_parser(False, face_set, default_region, default_permutation)

                if not permutation in permutation_list:
                    permutation_list.append(permutation)

                if not region in region_list:
                    region_list.append(region)

            material = global_functions.get_material(game_version, capsule, face, mesh_capsule, lod, region, permutation)
            material_index = -1
            if not material == -1:
                material_list = global_functions.gather_materials(game_version, material, material_list, 'JMS')
                material_index = material_list.index(material)

            parent_index = global_functions.get_parent(blend_scene.armature, capsule, joined_list, -1)
            capsule_matrix = global_functions.get_matrix(capsule, capsule, True, blend_scene.armature, joined_list, False, version, 'JMS', False, custom_scale, fix_rotations)
            mesh_dimensions = global_functions.get_dimensions(capsule_matrix, capsule, version, False, 'JMS', custom_scale)

            rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
            translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])
            height = (mesh_dimensions.pill_height)
            scale = (mesh_dimensions.object_radius)

            JMS.capsules.append(JMSAsset.Capsule(name, parent_index[0], material_index, rotation, translation, height, scale))
            capsule.to_mesh_clear()

        for convex_shape in blend_scene.convex_shape_list:
            verts = []
            evaluated_geo = convex_shape[0]
            original_geo = convex_shape[1]
            name = original_geo.name.split('$', 1)[1]

            face = evaluated_geo.polygons[0]

            lod = None
            region = default_region
            permutation = default_permutation
            if not original_geo.active_region == -1:
                face_set = original_geo.region_list[original_geo.active_region].name.split()
                lod, permutation, region = global_functions.material_definition_parser(False, face_set, default_region, default_permutation)

                if not permutation in permutation_list:
                    permutation_list.append(permutation)

                if not region in region_list:
                    region_list.append(region)

            material = global_functions.get_material(game_version, original_geo, face, evaluated_geo, lod, region, permutation)
            material_index = -1
            if not material == -1:
                material_list = global_functions.gather_materials(game_version, material, material_list, 'JMS')
                material_index = material_list.index(material)

            parent_index = global_functions.get_parent(blend_scene.armature, original_geo, joined_list, -1)
            convex_matrix = global_functions.get_matrix(original_geo, original_geo, True, blend_scene.armature, joined_list, False, version, 'JMS', False, custom_scale, fix_rotations)
            mesh_dimensions = global_functions.get_dimensions(convex_matrix, original_geo, version, False, 'JMS', custom_scale)

            rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
            translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])

            loc, rot, scale = convex_matrix.decompose()

            scale_x = Matrix.Scale(scale[0], 4, (1, 0, 0))
            scale_y = Matrix.Scale(scale[1], 4, (0, 1, 0))
            scale_z = Matrix.Scale(scale[2], 4, (0, 0, 1))

            scale_matrix = scale_x @ scale_y @ scale_z

            for vertex in evaluated_geo.vertices:
                pos  = scale_matrix @ vertex.co
                vert_translation = (pos[0], pos[1], pos[2])

                verts.append(JMSAsset.Vertex(None, None, None, vert_translation, None, None, None))

            JMS.convex_shapes.append(JMSAsset.Convex_Shape(name, parent_index[0], material_index, rotation, translation, verts))
            original_geo.to_mesh_clear()

        for ragdoll in blend_scene.ragdoll_list:
            body_a_obj = ragdoll.rigid_body_constraint.object1
            body_b_obj = ragdoll.rigid_body_constraint.object2
            body_a_name = 'Null'
            attached_index = -1
            attached_rotation = (0.0, 0.0, 0.0, 1.0)
            attached_translation = (0.0, 0.0, 0.0)
            body_b_name = 'Null'
            referenced_index = -1
            referenced_rotation = (0.0, 0.0, 0.0, 1.0)
            referenced_translation = (0.0, 0.0, 0.0)
            if body_a_obj:
                body_a_name = body_a_obj.name.split('$', 1)[1]
                attached_index = global_functions.get_parent(blend_scene.armature, body_a_obj, joined_list, -1)[0]
                body_a_matrix = global_functions.get_matrix(ragdoll, body_a_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                body_a_dimensions = global_functions.get_dimensions(body_a_matrix, body_a_obj, version, False, 'JMS', custom_scale)
                attached_rotation = (body_a_dimensions.quaternion[0], body_a_dimensions.quaternion[1], body_a_dimensions.quaternion[2], body_a_dimensions.quaternion[3])
                attached_translation = (body_a_dimensions.position[0], body_a_dimensions.position[1], body_a_dimensions.position[2])

            if body_b_obj:
                body_b_name = body_b_obj.name.split('$', 1)[1]
                referenced_index = global_functions.get_parent(blend_scene.armature, body_b_obj, joined_list, -1)[0]
                body_b_matrix = global_functions.get_matrix(ragdoll, body_b_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                body_b_dimensions = global_functions.get_dimensions(body_b_matrix, body_b_obj, version, False, 'JMS', custom_scale)
                referenced_rotation = (body_b_dimensions.quaternion[0], body_b_dimensions.quaternion[1], body_b_dimensions.quaternion[2], body_b_dimensions.quaternion[3])
                referenced_translation = (body_b_dimensions.position[0], body_b_dimensions.position[1], body_b_dimensions.position[2])

            name = 'ragdoll:%s:%s' % (body_a_name, body_b_name)
            is_limited_x = int(ragdoll.rigid_body_constraint.use_limit_ang_x)
            is_limited_y = int(ragdoll.rigid_body_constraint.use_limit_ang_y)
            is_limited_z = int(ragdoll.rigid_body_constraint.use_limit_ang_z)
            min_twist = 0
            max_twist = 0
            if is_limited_x:
                min_twist = degrees(ragdoll.rigid_body_constraint.limit_ang_x_lower)
                max_twist = degrees(ragdoll.rigid_body_constraint.limit_ang_x_upper)

            min_cone = 0
            max_cone = 0
            if is_limited_y:
                min_cone = degrees(ragdoll.rigid_body_constraint.limit_ang_y_lower)
                max_cone = degrees(ragdoll.rigid_body_constraint.limit_ang_y_upper)

            min_plane = 0
            max_plane = 0
            if is_limited_z:
                min_plane = degrees(ragdoll.rigid_body_constraint.limit_ang_z_lower)
                max_plane = degrees(ragdoll.rigid_body_constraint.limit_ang_z_upper)

            friction_limit = 0

            JMS.ragdolls.append(JMSAsset.Ragdoll(name, attached_index, referenced_index, attached_rotation, attached_translation, referenced_rotation, referenced_translation, min_twist, max_twist, min_cone, max_cone, min_plane, max_plane, friction_limit))

        for hinge in blend_scene.hinge_list:
            body_a_obj = hinge.rigid_body_constraint.object1
            body_b_obj = hinge.rigid_body_constraint.object2
            body_a_name = 'Null'
            body_a_parent = -1
            body_a_rotation = (0.0, 0.0, 0.0, 1.0)
            body_a_translation = (0.0, 0.0, 0.0)
            body_b_name = 'Null'
            body_b_parent = -1
            body_b_rotation = (0.0, 0.0, 0.0, 1.0)
            body_b_translation = (0.0, 0.0, 0.0)
            if body_a_obj:
                body_a_name = body_a_obj.name.split('$', 1)[1]
                body_a_parent = global_functions.get_parent(blend_scene.armature, body_a_obj, joined_list, -1)[0]
                body_a_matrix = global_functions.get_matrix(hinge, body_a_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                body_a_dimensions = global_functions.get_dimensions(body_a_matrix, body_a_obj, version, False, 'JMS', custom_scale)
                body_a_rotation = (body_a_dimensions.quaternion[0], body_a_dimensions.quaternion[1], body_a_dimensions.quaternion[2], body_a_dimensions.quaternion[3])
                body_a_translation = (body_a_dimensions.position[0], body_a_dimensions.position[1], body_a_dimensions.position[2])

            if body_b_obj:
                body_b_name = body_b_obj.name.split('$', 1)[1]
                body_b_parent = global_functions.get_parent(blend_scene.armature, body_b_obj, joined_list, -1)[0]
                body_b_matrix = global_functions.get_matrix(hinge, body_b_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                body_b_dimensions = global_functions.get_dimensions(body_b_matrix, body_b_obj, version, False, 'JMS', custom_scale)
                body_b_rotation = (body_b_dimensions.quaternion[0], body_b_dimensions.quaternion[1], body_b_dimensions.quaternion[2], body_b_dimensions.quaternion[3])
                body_b_translation = (body_b_dimensions.position[0], body_b_dimensions.position[1], body_b_dimensions.position[2])

            name = 'hinge:%s:%s' % (body_a_name, body_b_name)
            friction_limit = 0
            if body_b_obj and body_b_obj.rigid_body:
                friction_limit = body_b_obj.rigid_body.angular_damping

            min_angle = 0
            max_angle = 0
            is_limited = int(hinge.rigid_body_constraint.use_limit_ang_z)
            if is_limited:
                min_angle = degrees(hinge.rigid_body_constraint.limit_ang_z_lower)
                max_angle = degrees(hinge.rigid_body_constraint.limit_ang_z_upper)

            JMS.hinges.append(JMSAsset.Hinge(name, body_a_parent, body_b_parent, body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, is_limited, friction_limit, min_angle, max_angle))

        for car_wheel in blend_scene.car_wheel_list:
            chassis_obj = car_wheel.rigid_body_constraint.object1
            wheel_obj = car_wheel.rigid_body_constraint.object2
            chassis_name = 'Null'
            chassis_index = -1
            chassis_rotation = (0.0, 0.0, 0.0, 1.0)
            chassis_translation = (0.0, 0.0, 0.0)
            wheel_name = 'Null'
            wheel_index = -1
            wheel_rotation = (0.0, 0.0, 0.0, 1.0)
            wheel_translation = (0.0, 0.0, 0.0)
            suspension_rotation = (0.0, 0.0, 0.0, 1.0)
            suspension_translation = (0.0, 0.0, 0.0)
            if chassis_obj:
                chassis_name = chassis_obj.name.split('$', 1)[1]
                chassis_index = global_functions.get_parent(blend_scene.armature, chassis_obj, joined_list, -1)[0]
                chassis_matrix = global_functions.get_matrix(hinge, chassis_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                chassis_dimensions = global_functions.get_dimensions(chassis_matrix, chassis_obj, version, False, 'JMS', custom_scale)
                chassis_rotation = (chassis_dimensions.quaternion[0], chassis_dimensions.quaternion[1], chassis_dimensions.quaternion[2], chassis_dimensions.quaternion[3])
                chassis_translation = (chassis_dimensions.position[0], chassis_dimensions.position[1], chassis_dimensions.position[2])

            if wheel_obj:
                wheel_name = wheel_obj.name.split('$', 1)[1]
                wheel_index = global_functions.get_parent(blend_scene.armature, wheel_obj, joined_list, -1)[0]
                wheel_matrix = global_functions.get_matrix(hinge, wheel_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                wheel_dimensions = global_functions.get_dimensions(wheel_matrix, wheel_obj, version, False, 'JMS', custom_scale)
                wheel_rotation = (wheel_dimensions.quaternion[0], wheel_dimensions.quaternion[1], wheel_dimensions.quaternion[2], wheel_dimensions.quaternion[3])
                wheel_translation = (wheel_dimensions.position[0], wheel_dimensions.position[1], wheel_dimensions.position[2])
                suspension_rotation = (wheel_dimensions.quaternion[0], wheel_dimensions.quaternion[1], wheel_dimensions.quaternion[2], wheel_dimensions.quaternion[3])
                suspension_translation = (wheel_dimensions.position[0], wheel_dimensions.position[1], wheel_dimensions.position[2])

            name = 'hinge:%s:%s' % (chassis_name, wheel_name)
            suspension_min_limit = 0
            suspension_max_limit = 0
            if wheel_obj:
                suspension_min_limit = 0
                suspension_max_limit = 0

            friction_limit = 0
            velocity = 0
            gain = 0

            JMS.car_wheels.append(JMSAsset.Car_Wheel(name, chassis_index, wheel_index, chassis_rotation, chassis_translation, wheel_rotation, wheel_translation, suspension_rotation, suspension_translation, suspension_min_limit, suspension_max_limit, friction_limit, velocity, gain))

        for point_to_point in blend_scene.point_to_point_list:
            body_a_obj = point_to_point.rigid_body_constraint.object1
            body_b_obj = point_to_point.rigid_body_constraint.object2
            body_a_name = 'Null'
            body_a_index = -1
            body_a_rotation = (0.0, 0.0, 0.0, 1.0)
            body_a_translation = (0.0, 0.0, 0.0)
            body_b_name = 'Null'
            body_b_index = -1
            body_b_rotation = (0.0, 0.0, 0.0, 1.0)
            body_b_translation = (0.0, 0.0, 0.0)
            if body_a_obj:
                body_a_name = body_a_obj.name.split('$', 1)[1]
                body_a_matrix = global_functions.get_matrix(point_to_point, body_a_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                body_a_index = global_functions.get_parent(blend_scene.armature, body_a_obj, joined_list, -1)[0]
                body_a_dimensions = global_functions.get_dimensions(body_a_matrix, point_to_point, version, False, 'JMS', custom_scale)
                body_a_rotation = (body_a_dimensions.quaternion[0], body_a_dimensions.quaternion[1], body_a_dimensions.quaternion[2], body_a_dimensions.quaternion[3])
                body_a_translation = (body_a_dimensions.position[0], body_a_dimensions.position[1], body_a_dimensions.position[2])

            if body_b_obj:
                body_b_name = body_b_obj.name.split('$', 1)[1]
                body_b_matrix = global_functions.get_matrix(point_to_point, body_b_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                body_b_index = global_functions.get_parent(blend_scene.armature, body_b_obj, joined_list, -1)[0]
                body_b_dimensions = global_functions.get_dimensions(body_b_matrix, point_to_point, version, False, 'JMS', custom_scale)
                body_b_rotation = (body_b_dimensions.quaternion[0], body_b_dimensions.quaternion[1], body_b_dimensions.quaternion[2], body_b_dimensions.quaternion[3])
                body_b_translation = (body_b_dimensions.position[0], body_b_dimensions.position[1], body_b_dimensions.position[2])

            name = 'point_to_point:%s:%s' % (body_a_name, body_b_name)
            constraint_type = int(point_to_point.jms.jms_spring_type)
            x_min_limit = degrees(-45.0)
            x_max_limit = degrees(45.0)
            if point_to_point.rigid_body_constraint.use_limit_ang_x is True and constraint_type == 1:
                x_min_limit = degrees(point_to_point.rigid_body_constraint.limit_ang_x_lower)
                x_max_limit = degrees(point_to_point.rigid_body_constraint.limit_ang_x_upper)

            y_min_limit = degrees(-45.0)
            y_max_limit = degrees(45.0)
            if point_to_point.rigid_body_constraint.use_limit_ang_y is True and constraint_type == 1:
                y_min_limit = degrees(point_to_point.rigid_body_constraint.limit_ang_y_lower)
                y_max_limit = degrees(point_to_point.rigid_body_constraint.limit_ang_y_upper)

            z_min_limit = degrees(-45.0)
            z_max_limit = degrees(45.0)
            if point_to_point.rigid_body_constraint.use_limit_ang_z is True and constraint_type == 1:
                z_min_limit = degrees(point_to_point.rigid_body_constraint.limit_ang_z_lower)
                z_max_limit = degrees(point_to_point.rigid_body_constraint.limit_ang_z_upper)

            spring_length = float(0.0)
            if point_to_point.rigid_body_constraint.use_limit_lin_z is True and constraint_type == 2:
                spring_length = float(point_to_point.rigid_body_constraint.limit_lin_z_upper)

            JMS.point_to_points.append(JMSAsset.Point_to_Point(name, body_a_index, body_b_index, body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, constraint_type, x_min_limit, x_max_limit, y_min_limit, y_max_limit, z_min_limit, z_max_limit, spring_length))

        for prismatic in blend_scene.prismatic_list:
            body_a_obj = prismatic.rigid_body_constraint.object1
            body_b_obj = prismatic.rigid_body_constraint.object2
            body_a_name = 'Null'
            body_a_index = -1
            body_a_rotation = (0.0, 0.0, 0.0, 1.0)
            body_a_translation = (0.0, 0.0, 0.0)
            body_b_name = 'Null'
            body_b_index = -1
            body_b_rotation = (0.0, 0.0, 0.0, 1.0)
            body_b_translation = (0.0, 0.0, 0.0)
            if body_a_obj:
                body_a_name = chassis_obj.name.split('$', 1)[1]
                body_a_index = global_functions.get_parent(blend_scene.armature, body_a_obj, joined_list, -1)[0]
                body_a_matrix = global_functions.get_matrix(prismatic, body_a_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                body_a_dimensions = global_functions.get_dimensions(body_a_matrix, body_a_obj, version, False, 'JMS', custom_scale)
                body_a_rotation = (body_a_dimensions.quaternion[0], body_a_dimensions.quaternion[1], body_a_dimensions.quaternion[2], body_a_dimensions.quaternion[3])
                body_a_translation = (body_a_dimensions.position[0], body_a_dimensions.position[1], body_a_dimensions.position[2])

            if body_b_obj:
                body_b_name = wheel_obj.name.split('$', 1)[1]
                body_b_index = global_functions.get_parent(blend_scene.armature, body_b_obj, joined_list, -1)[0]
                body_b_matrix = global_functions.get_matrix(prismatic, body_b_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                body_b_dimensions = global_functions.get_dimensions(body_b_matrix, body_b_obj, version, False, 'JMS', custom_scale)
                body_b_rotation = (body_b_dimensions.quaternion[0], body_b_dimensions.quaternion[1], body_b_dimensions.quaternion[2], body_b_dimensions.quaternion[3])
                body_b_translation = (body_b_dimensions.position[0], body_b_dimensions.position[1], body_b_dimensions.position[2])

            name = 'hinge:%s:%s' % (body_a_name, body_b_name)
            is_limited = 0
            friction_limit = 0
            min_limit = 0
            max_limit = 0
            if wheel_obj:
                min_limit = 0
                max_limit = 0

            JMS.prismatics.append(JMSAsset.Prismatic(name, body_a_index, body_b_index, body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, is_limited, friction_limit, min_limit, max_limit))

    for region in region_list:
        name = region
        JMS.regions.append(JMSAsset.Region(name))

    for material in material_list:
        name = None
        texture_path = None
        slot = None
        lod = None
        permutation = default_permutation
        region = default_region
        if game_version == "halo1":
            name = '<none>'
            texture_path = '<none>'
            if not material == None:
                name = mesh_processing.append_material_symbols(material, game_version, False)
                if not material.node_tree == None and write_textures:
                    for node in material.node_tree.nodes:
                        if node.type == 'TEX_IMAGE':
                            if not node.image == None:
                                if node.image.source == "FILE" and not node.image.packed_file:
                                    image_filepath = bpy.path.abspath(node.image.filepath)
                                    image_path = image_filepath.rsplit('.', 1)[0]
                                    image_name = bpy.path.basename(image_path)
                                    tex = image_name
                                    if version >= 8200:
                                        tex = image_path

                                else:
                                    tex = node.image.name.rsplit('.', 1)[0]

                                texture_path = tex
                                break

        else:
            texture_path = '<none>'
            if not material[0] == None:
                name = mesh_processing.append_material_symbols(material[0], game_version, False)
                if not material[0].node_tree == None and write_textures:
                    for node in material[0].node_tree.nodes:
                        if node.type == 'TEX_IMAGE':
                            if not node.image == None:
                                if node.image.source == "FILE" and not node.image.packed_file:
                                    image_filepath = bpy.path.abspath(node.image.filepath)
                                    image_path = image_filepath.rsplit('.', 1)[0]
                                    image_name = bpy.path.basename(image_path)
                                    tex = image_name
                                    if version >= 8200:
                                        tex = image_path

                                else:
                                    tex = node.image.name.rsplit('.', 1)[0]

                                texture_path = tex
                                break

            name = mesh_processing.append_material_symbols(material[0], game_version, False)
            slot = bpy.data.materials.find(material[0].name)
            lod = mesh_processing.get_lod(material[1], game_version)
            #This doesn't matter for CE but for Halo 2/3 the region or permutation names can't have any whitespace.
            #Lets fix that here to make sure nothing goes wrong.
            if len(material[2]) != 0 and not game_version == "halo1":
                region = material[2].replace(' ', '_').replace('\t', '_')

            if len(material[3]) != 0 and not game_version == "halo1":
                permutation = material[3].replace(' ', '_').replace('\t', '_')

        JMS.materials.append(JMSAsset.Material(name, texture_path, slot, lod, permutation, region))

    return JMS
