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
from random import seed, randint
from mathutils import Vector, Matrix
from ..global_functions import mesh_processing, global_functions

class JMSScene(global_functions.HaloAsset):
    class Node:
        def __init__(self, name, children=None, child=-1, sibling=-1, parent=-1, rotation=None, translation=None):
            self.name = name
            self.children = children
            self.child = child
            self.sibling = sibling
            self.parent = parent
            self.rotation = rotation
            self.translation = translation

    class Material:
        def __init__(self, name, texture_path=None, slot=None, lod=None, permutation=None, region=None):
            self.name = name
            self.texture_path = texture_path
            self.slot = slot
            self.lod = lod
            self.permutation = permutation
            self.region = region

    class Marker:
        def __init__(self, name, region=-1, parent=-1, rotation=None, translation=None, scale=0.0):
            self.name = name
            self.region = region
            self.parent = parent
            self.rotation = rotation
            self.translation = translation
            self.scale = scale

    class XREF:
        def __init__(self, path, name):
            self.path = path
            self.name = name

    class XREF_Marker:
        def __init__(self, name, unique_identifier=-1, index=-1, rotation=None, translation=None):
            self.name = name
            self.unique_identifier = unique_identifier
            self.index = index
            self.rotation = rotation
            self.translation = translation

    class Region:
        def __init__(self, name):
            self.name = name

    class Vertex:
        def __init__(self,
                     node_influence_count=0,
                     node_set=None,
                     region=-1,
                     translation=None,
                     normal=None,
                     color=None,
                     uv_set=None
                     ):

            self.node_influence_count = node_influence_count
            self.node_set = node_set
            self.region = region
            self.translation = translation
            self.normal = normal
            self.color = color
            self.uv_set = uv_set

    class Triangle:
        def __init__(self, region=-1, material_index=-1, v0=-1, v1=-1, v2=-1):
            self.region = region
            self.material_index = material_index
            self.v0 = v0
            self.v1 = v1
            self.v2 = v2

    class Sphere:
        def __init__(self, name, parent_index=-1, material_index=-1, rotation=None, translation=None, scale=0.0):
            self.name = name
            self.parent_index = parent_index
            self.material_index = material_index
            self.rotation = rotation
            self.translation = translation
            self.scale = scale

    class Box:
        def __init__(self, name, parent_index=-1, material_index=-1, rotation=None, translation=None, width=0.0, length=0.0, height=0.0):
            self.name = name
            self.parent_index = parent_index
            self.material_index = material_index
            self.rotation = rotation
            self.translation = translation
            self.width = width
            self.length = length
            self.height = height

    class Capsule:
        def __init__(self, name, parent_index=-1, material_index=-1, rotation=None, translation=None, height=0.0, radius=0.0):
            self.name = name
            self.parent_index = parent_index
            self.material_index = material_index
            self.rotation = rotation
            self.translation = translation
            self.height = height
            self.radius = radius

    class Convex_Shape:
        def __init__(self, name, parent_index=-1, material_index=-1, rotation=None, translation=None, verts=None):
            self.name = name
            self.parent_index = parent_index
            self.material_index = material_index
            self.rotation = rotation
            self.translation = translation
            self.verts = verts

    class Ragdoll:
        def __init__(self,
                     name,
                     attached_index=-1,
                     referenced_index=-1,
                     attached_rotation=None,
                     attached_translation=None,
                     referenced_rotation=None,
                     referenced_translation=None,
                     min_twist=0.0,
                     max_twist=0.0,
                     min_cone=0.0,
                     max_cone=0.0,
                     min_plane=0.0,
                     max_plane=0.0,
                     friction_limit=0.0
                     ):

            self.name = name
            self.attached_index = attached_index
            self.referenced_index = referenced_index
            self.attached_rotation = attached_rotation
            self.attached_translation = attached_translation
            self.referenced_rotation = referenced_rotation
            self.referenced_translation = referenced_translation
            self.min_twist = min_twist
            self.max_twist = max_twist
            self.min_cone = min_cone
            self.max_cone = max_cone
            self.min_plane = min_plane
            self.max_plane = max_plane
            self.friction_limit = friction_limit

    class Hinge:
        def __init__(self, name, body_a_index=-1, body_b_index=-1, body_a_rotation=None, body_a_translation=None, body_b_rotation=None, body_b_translation=None, is_limited=0, friction_limit=0.0, min_angle=0.0, max_angle=0.0):
            self.name = name
            self.body_a_index = body_a_index
            self.body_b_index = body_b_index
            self.body_a_rotation = body_a_rotation
            self.body_a_translation = body_a_translation
            self.body_b_rotation = body_b_rotation
            self.body_b_translation = body_b_translation
            self.is_limited = is_limited
            self.friction_limit = friction_limit
            self.min_angle = min_angle
            self.max_angle = max_angle

    class Car_Wheel:
        def __init__(self, name, chassis_index=-1, wheel_index=-1, chassis_rotation=None, chassis_translation=None, wheel_rotation=None, wheel_translation=None, suspension_rotation=None, suspension_translation=None, suspension_min_limit=0.0, suspension_max_limit=0.0, friction_limit=0.0, velocity=0.0, gain=0.0):
            self.name = name
            self.chassis_index = chassis_index
            self.wheel_index = wheel_index
            self.chassis_rotation = chassis_rotation
            self.chassis_translation = chassis_translation
            self.wheel_rotation = wheel_rotation
            self.wheel_translation = wheel_translation
            self.suspension_rotation = suspension_rotation
            self.suspension_translation = suspension_translation
            self.suspension_min_limit = suspension_min_limit
            self.suspension_max_limit = suspension_max_limit
            self.friction_limit = friction_limit
            self.velocity = velocity
            self.gain = gain

    class Point_to_Point:
        def __init__(self, name, body_a_index=-1, body_b_index=-1, body_a_rotation=None, body_a_translation=None, body_b_rotation=None, body_b_translation=None, constraint_type=0, x_min_limit=0.0, x_max_limit=0.0, y_min_limit=0.0, y_max_limit=0.0, z_min_limit=0.0, z_max_limit=0.0, spring_length=0.0):
            self.name = name
            self.body_a_index = body_a_index
            self.body_b_index = body_b_index
            self.body_a_rotation = body_a_rotation
            self.body_a_translation = body_a_translation
            self.body_b_rotation = body_b_rotation
            self.body_b_translation = body_b_translation
            self.constraint_type = constraint_type
            self.x_min_limit = x_min_limit
            self.x_max_limit = x_max_limit
            self.y_min_limit = y_min_limit
            self.y_max_limit = y_max_limit
            self.z_min_limit = z_min_limit
            self.z_max_limit = z_max_limit
            self.spring_length = spring_length

    class Prismatic:
        def __init__(self, name, body_a_index=-1, body_b_index=-1, body_a_rotation=None, body_a_translation=None, body_b_rotation=None, body_b_translation=None, is_limited=0, suspension_max_limit=0.0, friction_limit=0.0, min_limit=0.0, max_limit=0.0):
            self.name = name
            self.body_a_index = body_a_index
            self.body_b_index = body_b_index
            self.body_a_rotation = body_a_rotation
            self.body_a_translation = body_a_translation
            self.body_b_rotation = body_b_rotation
            self.body_b_translation = body_b_translation
            self.is_limited = is_limited
            self.friction_limit = friction_limit
            self.min_limit = min_limit
            self.max_limit = max_limit

    class Bounding_Sphere:
        def __init__(self, translation=None, scale=0.0):
            self.translation = translation
            self.scale = scale

    class Skylight:
        def __init__(self, direction=None, radiant_intensity=None, solid_angle=0.0):
            self.direction = direction
            self.radiant_intensity = radiant_intensity
            self.solid_angle = solid_angle

    def __init__(self, version, game_version, generate_checksum, fix_rotations, model_type, blend_scene, custom_scale):
        default_region = mesh_processing.get_default_region_permutation_name(game_version)
        default_permutation = mesh_processing.get_default_region_permutation_name(game_version)
        region_list = ['unnamed']
        permutation_list = []
        self.nodes = []
        self.materials = []
        self.markers = []
        self.xref_instances = []
        self.xref_markers = []
        self.regions = []
        self.geometry_list = []
        self.original_geometry_list = []
        self.triangles = []
        self.vertices = []
        self.spheres = []
        self.boxes = []
        self.capsules = []
        self.convex_shapes = []
        self.ragdolls = []
        self.hinges = []
        self.car_wheels = []
        self.point_to_points = []
        self.prismatics = []
        self.bounding_spheres = []
        self.skylights = []

        material_list = []

        sorted_list = global_functions.sort_list(blend_scene.node_list, blend_scene.armature, game_version, version, False)
        joined_list = sorted_list[0]
        reversed_joined_list = sorted_list[1]
        self.node_checksum = 0
        for node in joined_list:
            is_bone = False
            if blend_scene.armature:
                is_bone = True

            find_child_node = global_functions.get_child(node, reversed_joined_list)
            find_sibling_node = global_functions.get_sibling(blend_scene.armature, node, reversed_joined_list)

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
            mesh_dimensions = global_functions.get_dimensions(bone_matrix, node, version, None, False, is_bone, 'JMS', custom_scale)

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

            self.nodes.append(JMSScene.Node(name, children, child, sibling, parent, rotation, translation))

        if generate_checksum:
            self.node_checksum = global_functions.node_hierarchy_checksum(self.nodes, self.nodes[0], self.node_checksum)

        all_marker_list = blend_scene.marker_list
        if model_type == "render":
            all_marker_list = blend_scene.marker_list + blend_scene.render_marker_list

        elif model_type == "collision":
            all_marker_list = blend_scene.marker_list + blend_scene.collision_marker_list

        else:
            all_marker_list = blend_scene.marker_list + blend_scene.physics_marker_list

        for marker in all_marker_list:
            marker_name = marker.name.split('#', 1)[1] #remove marker symbol from name
            if not global_functions.string_empty_check(marker.marker.name_override):
                marker_name = marker.marker.name_override

            region_idx = -1

            parent_idx = global_functions.get_parent(blend_scene.armature, marker, joined_list, 0)
            marker_matrix = global_functions.get_matrix(marker, marker, True, blend_scene.armature, joined_list, False, version, 'JMS', False, custom_scale, fix_rotations)
            mesh_dimensions = global_functions.get_dimensions(marker_matrix, marker, version, None, False, False, 'JMS', custom_scale)

            rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
            translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])
            scale = (mesh_dimensions.object_radius)

            if marker.type == 'EMPTY':
                scale = (mesh_dimensions.scale[0])
                if not marker.marker.marker_region == '':
                    if not marker.marker.marker_region in region_list:
                        region_list.append(marker.marker.marker_region)

                    region_idx = region_list.index(marker.marker.marker_region)

            elif marker.type == 'MESH':
                if marker.face_maps.active:
                    region_face_map_name = marker.face_maps[0].name
                    if not region_face_map_name in region_list:
                        region_list.append(region_face_map_name)

                    region_idx = region_list.index(region_face_map_name)

                elif not marker.marker.marker_region == '':
                    if not marker.marker.marker_region in region_list:
                        region_list.append(marker.marker.marker_region)

                    region_idx = region_list.index(marker.marker.marker_region)

            self.markers.append(JMSScene.Marker(marker_name, region_idx, parent_idx[0], rotation, translation, scale))

        if model_type == "render":
            for xref_path in blend_scene.instance_xref_paths:
                path = bpy.path.abspath(xref_path)
                name = os.path.basename(xref_path).rsplit('.', 1)[0]

                self.xref_instances.append(JMSScene.XREF(path, name))

            seed(1)
            starting_ID = -1 * (randint(0, 3000000000))
            for idx, int_markers in enumerate(blend_scene.instance_markers):
                name = int_markers.name
                unique_identifier = starting_ID - idx
                index = blend_scene.instance_xref_paths.index(int_markers.data.ass_jms.XREF_path)
                int_markers_matrix = global_functions.get_matrix(int_markers, int_markers, False, blend_scene.armature, joined_list, False, version, 'JMS', False, custom_scale, fix_rotations)
                mesh_dimensions = global_functions.get_dimensions(int_markers_matrix, int_markers, version, None, False, False, 'JMS', custom_scale)

                rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
                translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])

                self.xref_markers.append(JMSScene.XREF_Marker(name, unique_identifier, index, rotation, translation))

            for bound_sphere in blend_scene.bounding_sphere_list:
                bound_sphere_matrix = global_functions.get_matrix(bound_sphere, bound_sphere, False, blend_scene.armature, joined_list, False, version, 'JMS', False, custom_scale, fix_rotations)
                mesh_dimensions = global_functions.get_dimensions(bound_sphere_matrix, bound_sphere, version, None, False, False, 'JMS', custom_scale)
                translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])
                scale = mesh_dimensions.object_radius

                self.bounding_spheres.append(JMSScene.Bounding_Sphere(translation, scale))

            for light in blend_scene.skylight_list:
                down_vector = Vector((0, 0, -1))
                down_vector.rotate(light.rotation_euler)

                direction = (down_vector[0], down_vector[1], down_vector[2])
                radiant_intensity =  (light.data.color[0], light.data.color[1], light.data.color[2])
                solid_angle = light.data.energy

                self.skylights.append(JMSScene.Skylight(direction, radiant_intensity, solid_angle))

        if model_type == "render" or model_type == "collision":
            geometry_list = blend_scene.render_geometry_list
            if model_type == "collision":
                geometry_list = blend_scene.collision_geometry_list

            for idx, geometry in enumerate(geometry_list):
                evaluted_mesh = geometry[0]
                original_geo = geometry[1]
                vertex_groups = original_geo.vertex_groups.keys()
                original_geo_matrix = global_functions.get_matrix(original_geo, original_geo, False, blend_scene.armature, joined_list, False, version, "JMS", False, custom_scale, fix_rotations)
                for idx, face in enumerate(evaluted_mesh.polygons):
                    face_set = (None, default_permutation, default_region)
                    region_index = -1
                    if game_version == 'haloce':
                        region_index = region_list.index(default_region)

                    lod = face_set[0]
                    permutation = face_set[1]
                    region = face_set[2]
                    if evaluted_mesh.face_maps.active and len(original_geo.face_maps) > 0:
                        face_map_idx = evaluted_mesh.face_maps.active.data[idx].value
                        if not face_map_idx == -1:
                            face_set = mesh_processing.process_mesh_export_face_set(default_permutation, default_region, game_version, original_geo, face_map_idx)
                            lod = face_set[0]
                            permutation = face_set[1]
                            region = face_set[2]
                            if not region in region_list:
                                region_list.append(region)

                            region_index = region_list.index(region)
                            if not game_version == 'haloce':
                                if not permutation in permutation_list:
                                    permutation_list.append(permutation)

                    material = global_functions.get_material(game_version, original_geo, face, evaluted_mesh, lod, region, permutation)
                    material_index = -1
                    if not material == -1:
                        material_list = global_functions.gather_materials(game_version, material, material_list, "JMS")
                        material_index = material_list.index(material)

                    vert_count = len(self.vertices)
                    v0 = vert_count
                    v1 = vert_count + 1
                    v2 = vert_count + 2

                    self.triangles.append(JMSScene.Triangle(region_index, material_index, v0, v1, v2))
                    for loop_index in face.loop_indices:
                        vert = evaluted_mesh.vertices[evaluted_mesh.loops[loop_index].vertex_index]

                        region = region_index
                        scaled_translation, normal = mesh_processing.process_mesh_export_vert(vert, "JMS", original_geo_matrix, version, custom_scale)
                        uv_set = mesh_processing.process_mesh_export_uv(evaluted_mesh, "JMS", loop_index, version)
                        color = mesh_processing.process_mesh_export_color(evaluted_mesh, loop_index)
                        node_influence_count, node_set, node_index_list = mesh_processing.process_mesh_export_weights(vert, blend_scene.armature, original_geo, vertex_groups, joined_list, "JMS")

                        self.vertices.append(JMSScene.Vertex(node_influence_count, node_set, region, scaled_translation, normal, color, uv_set))

                original_geo.to_mesh_clear()

        if model_type == "physics":
            for spheres in blend_scene.sphere_list:
                name = spheres.name.split('$', 1)[1]
                mesh_sphere = spheres.to_mesh()
                face = mesh_sphere.polygons[0]

                region = default_region
                permutation = default_permutation
                if spheres.face_maps.active:
                    face_set = spheres.face_maps[0].name.split()
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
                mesh_dimensions = global_functions.get_dimensions(sphere_matrix, spheres, version, None, False, False, 'JMS', custom_scale)

                rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
                translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])
                scale = (mesh_dimensions.object_radius)

                self.spheres.append(JMSScene.Sphere(name, parent_index[0], material_index, rotation, translation, scale))
                spheres.to_mesh_clear()

            for boxes in blend_scene.box_list:
                name = boxes.name.split('$', 1)[1]
                mesh_boxes = boxes.to_mesh()
                face = mesh_boxes.polygons[0]

                lod = None
                region = default_region
                permutation = default_permutation
                if boxes.face_maps.active:
                    face_set = boxes.face_maps[0].name.split()
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
                mesh_dimensions = global_functions.get_dimensions(box_matrix, boxes, version, None, False, False, 'JMS', custom_scale)

                rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
                translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])
                width = (mesh_dimensions.dimension[0])
                length = (mesh_dimensions.dimension[1])
                height = (mesh_dimensions.dimension[2])

                self.boxes.append(JMSScene.Box(name, parent_index[0], material_index, rotation, translation, width, length, height))
                boxes.to_mesh_clear()

            for capsule in blend_scene.capsule_list:
                name = capsule.name.split('$', 1)[1]
                mesh_capsule = capsule.to_mesh()
                face = mesh_capsule.polygons[0]

                lod = None
                region = default_region
                permutation = default_permutation
                if capsule.face_maps.active:
                    face_set = capsule.face_maps[0].name.split()
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
                mesh_dimensions = global_functions.get_dimensions(capsule_matrix, capsule, version, None, False, False, 'JMS', custom_scale)

                rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
                translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])
                height = (mesh_dimensions.pill_height)
                scale = (mesh_dimensions.object_radius)

                self.capsules.append(JMSScene.Capsule(name, parent_index[0], material_index, rotation, translation, height, scale))
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
                if original_geo.face_maps.active:
                    face_set = original_geo.face_maps[0].name.split()
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
                mesh_dimensions = global_functions.get_dimensions(convex_matrix, original_geo, version, None, False, False, 'JMS', custom_scale)

                rotation = (mesh_dimensions.quaternion[0], mesh_dimensions.quaternion[1], mesh_dimensions.quaternion[2], mesh_dimensions.quaternion[3])
                translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])

                loc, rot, scale = convex_matrix.decompose()

                scale_x = Matrix.Scale(scale[0], 4, (1, 0, 0))
                scale_y = Matrix.Scale(scale[1], 4, (0, 1, 0))
                scale_z = Matrix.Scale(scale[2], 4, (0, 0, 1))

                scale_matrix = scale_x @ scale_y @ scale_z

                for vertex in evaluated_geo.vertices:
                    pos  = scale_matrix @ vertex.co
                    mesh_dimensions = global_functions.get_dimensions(None, None, version, pos, True, False, 'JMS', custom_scale)
                    vert_translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])

                    verts.append(JMSScene.Vertex(None, None, None, vert_translation, None, None, None))

                self.convex_shapes.append(JMSScene.Convex_Shape(name, parent_index[0], material_index, rotation, translation, verts))
                original_geo.to_mesh_clear()

            for ragdoll in blend_scene.ragdoll_list:
                body_a_obj = ragdoll.rigid_body_constraint.object1
                body_b_obj = ragdoll.rigid_body_constraint.object2
                body_a_name = 'Null'
                body_b_name = 'Null'
                if body_a_obj:
                    body_a_name = body_a_obj.name.split('$', 1)[1]

                if body_b_obj:
                    body_b_name = body_b_obj.name.split('$', 1)[1]

                name = 'ragdoll:%s:%s' % (body_a_name, body_b_name)
                attached_index = global_functions.get_parent(blend_scene.armature, body_a_obj, joined_list, -1)
                referenced_index = global_functions.get_parent(blend_scene.armature, body_b_obj, joined_list, -1)
                body_a_matrix = global_functions.get_matrix(ragdoll, body_a_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                body_b_matrix = global_functions.get_matrix(ragdoll, body_b_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                body_a_dimensions = global_functions.get_dimensions(body_a_matrix, body_a_obj, version, None, False, False, 'JMS', custom_scale)
                body_b_dimensions = global_functions.get_dimensions(body_b_matrix, body_b_obj, version, None, False, False, 'JMS', custom_scale)
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
                attached_rotation = (body_a_dimensions.quaternion[0], body_a_dimensions.quaternion[1], body_a_dimensions.quaternion[2], body_a_dimensions.quaternion[3])
                attached_translation = (body_a_dimensions.position[0], body_a_dimensions.position[1], body_a_dimensions.position[2])
                referenced_rotation = (body_b_dimensions.quaternion[0], body_b_dimensions.quaternion[1], body_b_dimensions.quaternion[2], body_b_dimensions.quaternion[3])
                referenced_translation = (body_b_dimensions.position[0], body_b_dimensions.position[1], body_b_dimensions.position[2])

                self.ragdolls.append(JMSScene.Ragdoll(name, attached_index[0], referenced_index[0], attached_rotation, attached_translation, referenced_rotation, referenced_translation, min_twist, max_twist, min_cone, max_cone, min_plane, max_plane, friction_limit))

            for hinge in blend_scene.hinge_list:
                body_a_obj = hinge.rigid_body_constraint.object1
                body_b_obj = hinge.rigid_body_constraint.object2
                body_a_name = 'Null'
                body_b_name = 'Null'
                if body_a_obj:
                    body_a_name = body_a_obj.name.split('$', 1)[1]

                if body_b_obj:
                    body_b_name = body_b_obj.name.split('$', 1)[1]

                name = 'hinge:%s:%s' % (body_a_name, body_b_name)
                body_a_index = global_functions.get_parent(blend_scene.armature, body_a_obj, joined_list, -1)
                body_b_index = global_functions.get_parent(blend_scene.armature, body_b_obj, joined_list, -1)
                body_a_matrix = global_functions.get_matrix(hinge, body_a_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                body_b_matrix = global_functions.get_matrix(hinge, body_b_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                body_a_dimensions = global_functions.get_dimensions(body_a_matrix, body_a_obj, version, None, False, False, 'JMS', custom_scale)
                body_b_dimensions = global_functions.get_dimensions(body_b_matrix, body_b_obj, version, None, False, False, 'JMS', custom_scale)
                friction_limit = 0
                if body_b_obj:
                    friction_limit = body_b_obj.rigid_body.angular_damping

                min_angle = 0
                max_angle = 0
                is_limited = int(hinge.rigid_body_constraint.use_limit_ang_z)
                if is_limited:
                    min_angle = degrees(hinge.rigid_body_constraint.limit_ang_z_lower)
                    max_angle = degrees(hinge.rigid_body_constraint.limit_ang_z_upper)

                body_a_rotation = (body_a_dimensions.quaternion[0], body_a_dimensions.quaternion[1], body_a_dimensions.quaternion[2], body_a_dimensions.quaternion[3])
                body_a_translation = (body_a_dimensions.position[0], body_a_dimensions.position[1], body_a_dimensions.position[2])
                body_b_rotation = (body_b_dimensions.quaternion[0], body_b_dimensions.quaternion[1], body_b_dimensions.quaternion[2], body_b_dimensions.quaternion[3])
                body_b_translation = (body_b_dimensions.position[0], body_b_dimensions.position[1], body_b_dimensions.position[2])

                self.hinges.append(JMSScene.Hinge(name, body_a_index[0], body_b_index[0], body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, is_limited, friction_limit, min_angle, max_angle))

            for car_wheel in blend_scene.car_wheel_list:
                chassis_obj = car_wheel.rigid_body_constraint.object1
                wheel_obj = car_wheel.rigid_body_constraint.object2
                chassis_name = 'Null'
                wheel_name = 'Null'
                if chassis_obj:
                    chassis_name = chassis_obj.name.split('$', 1)[1]

                if wheel_obj:
                    wheel_name = wheel_obj.name.split('$', 1)[1]

                name = 'hinge:%s:%s' % (chassis_name, wheel_name)
                chassis_index = global_functions.get_parent(blend_scene.armature, chassis_obj, joined_list, -1)
                wheel_index = global_functions.get_parent(blend_scene.armature, wheel_obj, joined_list, -1)
                chassis_matrix = global_functions.get_matrix(hinge, chassis_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                wheel_matrix = global_functions.get_matrix(hinge, wheel_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                chassis_dimensions = global_functions.get_dimensions(chassis_matrix, chassis_obj, version, None, False, False, 'JMS', custom_scale)
                wheel_dimensions = global_functions.get_dimensions(wheel_matrix, wheel_obj, version, None, False, False, 'JMS', custom_scale)
                suspension_min_limit = 0
                suspension_max_limit = 0
                if wheel_obj:
                    suspension_min_limit = 0
                    suspension_max_limit = 0

                friction_limit = 0
                velocity = 0
                gain = 0

                chassis_rotation = (chassis_dimensions.quaternion[0], chassis_dimensions.quaternion[1], chassis_dimensions.quaternion[2], chassis_dimensions.quaternion[3])
                chassis_translation = (chassis_dimensions.position[0], chassis_dimensions.position[1], chassis_dimensions.position[2])
                wheel_rotation = (wheel_dimensions.quaternion[0], wheel_dimensions.quaternion[1], wheel_dimensions.quaternion[2], wheel_dimensions.quaternion[3])
                wheel_translation = (wheel_dimensions.position[0], wheel_dimensions.position[1], wheel_dimensions.position[2])
                suspension_rotation = (wheel_dimensions.quaternion[0], wheel_dimensions.quaternion[1], wheel_dimensions.quaternion[2], wheel_dimensions.quaternion[3])
                suspension_translation = (wheel_dimensions.position[0], wheel_dimensions.position[1], wheel_dimensions.position[2])

                self.car_wheels.append(JMSScene.Car_Wheel(name, chassis_index[0], wheel_index[0], chassis_rotation, chassis_translation, wheel_rotation, wheel_translation, suspension_rotation, suspension_translation, suspension_min_limit, suspension_max_limit, friction_limit, velocity, gain))

            for point_to_point in blend_scene.point_to_point_list:
                body_a_obj = point_to_point.rigid_body_constraint.object1
                body_b_obj = point_to_point.rigid_body_constraint.object2
                body_a_name = 'Null'
                body_b_name = 'Null'
                body_a_matrix = Matrix.Translation((0, 0, 0))
                body_b_matrix = Matrix.Translation((0, 0, 0))
                if body_a_obj:
                    body_a_name = body_a_obj.name.split('$', 1)[1]
                    body_a_matrix = global_functions.get_matrix(point_to_point, body_a_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)

                if body_b_obj:
                    body_b_name = body_b_obj.name.split('$', 1)[1]
                    body_b_matrix = global_functions.get_matrix(point_to_point, body_b_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)

                name = 'point_to_point:%s:%s' % (body_a_name, body_b_name)
                body_a_index = global_functions.get_parent(blend_scene.armature, body_a_obj, joined_list, -1)
                body_b_index = global_functions.get_parent(blend_scene.armature, body_b_obj, joined_list, -1)
                body_a_dimensions = global_functions.get_dimensions(body_a_matrix, point_to_point, version, None, False, False, 'JMS', custom_scale)
                body_b_dimensions = global_functions.get_dimensions(body_b_matrix, point_to_point, version, None, False, False, 'JMS', custom_scale)
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

                body_a_rotation = (body_a_dimensions.quaternion[0], body_a_dimensions.quaternion[1], body_a_dimensions.quaternion[2], body_a_dimensions.quaternion[3])
                body_a_translation = (body_a_dimensions.position[0], body_a_dimensions.position[1], body_a_dimensions.position[2])
                body_b_rotation = (body_b_dimensions.quaternion[0], body_b_dimensions.quaternion[1], body_b_dimensions.quaternion[2], body_b_dimensions.quaternion[3])
                body_b_translation = (body_b_dimensions.position[0], body_b_dimensions.position[1], body_b_dimensions.position[2])

                self.point_to_points.append(JMSScene.Point_to_Point(name, body_a_index[0], body_b_index[0], body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, constraint_type, x_min_limit, x_max_limit, y_min_limit, y_max_limit, z_min_limit, z_max_limit, spring_length))

            for prismatic in blend_scene.prismatic_list:
                body_a_obj = prismatic.rigid_body_constraint.object1
                body_b_obj = prismatic.rigid_body_constraint.object2
                body_a_name = 'Null'
                body_b_name = 'Null'
                if body_a_obj:
                    body_a_name = chassis_obj.name.split('$', 1)[1]

                if body_b_obj:
                    body_b_name = wheel_obj.name.split('$', 1)[1]

                name = 'hinge:%s:%s' % (body_a_name, body_b_name)
                body_a_index = global_functions.get_parent(blend_scene.armature, body_a_obj, joined_list, -1)
                body_b_index = global_functions.get_parent(blend_scene.armature, body_b_obj, joined_list, -1)
                body_a_matrix = global_functions.get_matrix(prismatic, body_a_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                body_b_matrix = global_functions.get_matrix(prismatic, body_b_obj, True, blend_scene.armature, joined_list, False, version, 'JMS', True, custom_scale, fix_rotations)
                body_a_dimensions = global_functions.get_dimensions(body_a_matrix, body_a_obj, version, None, False, False, 'JMS', custom_scale)
                body_b_dimensions = global_functions.get_dimensions(body_b_matrix, body_b_obj, version, None, False, False, 'JMS', custom_scale)
                is_limited = 0
                friction_limit = 0
                min_limit = 0
                max_limit = 0
                if wheel_obj:
                    min_limit = 0
                    max_limit = 0

                body_a_rotation = (body_a_dimensions.quaternion[0], body_a_dimensions.quaternion[1], body_a_dimensions.quaternion[2], body_a_dimensions.quaternion[3])
                body_a_translation = (body_a_dimensions.position[0], body_a_dimensions.position[1], body_a_dimensions.position[2])
                body_b_rotation = (body_b_dimensions.quaternion[0], body_b_dimensions.quaternion[1], body_b_dimensions.quaternion[2], body_b_dimensions.quaternion[3])
                body_b_translation = (body_b_dimensions.position[0], body_b_dimensions.position[1], body_b_dimensions.position[2])

                self.prismatics.append(JMSScene.Prismatic(name, body_a_index[0], body_b_index[0], body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, is_limited, friction_limit, min_limit, max_limit))

        for region in region_list:
            name = region

            self.regions.append(JMSScene.Region(name))

        for material in material_list:
            name = None
            texture_path = None
            slot = None
            lod = None
            permutation = default_permutation
            region = default_region
            if game_version == 'haloce':
                name = '<none>'
                texture_path = '<none>'
                if not material == None:
                    name = mesh_processing.append_material_symbols(material, game_version)
                    if not material.node_tree == None:
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
                name = mesh_processing.append_material_symbols(material[0], game_version)
                slot = bpy.data.materials.find(material[0].name)
                lod = mesh_processing.get_lod(material[1], game_version)
                #This doesn't matter for CE but for Halo 2/3 the region or permutation names can't have any whitespace.
                #Lets fix that here to make sure nothing goes wrong.
                if len(material[2]) != 0:
                    region = material[2].replace(' ', '_').replace('\t', '_')

                if len(material[3]) != 0:
                    permutation = material[3].replace(' ', '_').replace('\t', '_')

            self.materials.append(JMSScene.Material(name, texture_path, slot, lod, permutation, region))

def write_file(context, filepath, report, version, game_version, generate_checksum, fix_rotations, folder_structure, folder_type, permutation_ce, level_of_detail_ce, model_type, blend_scene, jmi, custom_scale):
    jms_scene = JMSScene(version, game_version, generate_checksum, fix_rotations, model_type, blend_scene, custom_scale)

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

    filename = global_functions.get_filename(game_version, permutation_ce, level_of_detail_ce, folder_structure, model_type, False, filepath)
    root_directory = global_functions.get_directory(context, game_version, model_type, folder_structure, folder_type, jmi, filepath)

    print(root_directory)
    print(filename)
    file = open(root_directory + os.sep + filename, 'w', encoding='utf_8')

    if version >= 8205:
        version_bounds = '8197-8210'
        if game_version == 'halo3mcc':
            version_bounds = '8197-8213'

        file.write(
            ';### VERSION ###' +
            '\n%s' % (version) +
            '\n;\t<%s>\n' % (version_bounds)
            )

    else:
        file.write(
            '%s' % (version) +
            '\n%s' % (jms_scene.node_checksum)
            )

        if version >= 8203 and version <= 8204:
            file.write(
                '\n;' +
                '\n;###Frames###'
                )

        file.write(
            '\n%s' % (len(jms_scene.nodes))
            )

    if version >= 8205:
        file.write(
            '\n;### NODES ###' +
            '\n%s' % (len(jms_scene.nodes)) +
            '\n;\t<name>' +
            '\n;\t<parent node index>' +
            '\n;\t<default rotation <i,j,k,w>>' +
            '\n;\t<default translation <x,y,z>>\n'
        )

    for idx, node in enumerate(jms_scene.nodes):
        if version >= 8205:
            file.write(
                '\n;NODE %s' % (idx) +
                '\n%s' % (node.name) +
                '\n%s' % (node.parent) +
                decimal_4 % (node.rotation) +
                decimal_3 % (node.translation) +
                '\n'
            )

        else:
            file.write(
                '\n%s' % (node.name) +
                '\n%s' % (node.child) +
                '\n%s' % (node.sibling) +
                decimal_4 % (node.rotation) +
                decimal_3 % (node.translation)
            )

    if version >= 8205:
        file.write(
            '\n;### MATERIALS ###' +
            '\n%s' % (len(jms_scene.materials)) +
            '\n;\t<name>' +
            '\n;\t<(Material Slot Index) LOD Permutation Region>\n'
        )

    else:
        if version >= 8203 and version <= 8204:
            file.write(
                '\n;' +
                '\n;###Materials###'
                )

        file.write(
            '\n%s' % (len(jms_scene.materials))
        )

    for idx, material in enumerate(jms_scene.materials):
        if game_version == 'haloce':
            file.write(
                '\n%s' % (material.name) +
                '\n%s' % (material.texture_path)
            )

        else:
            material_definition = '(%s)' % (material.slot)
            if not material.lod == None:
                material_definition += ' %s' % (material.lod)
            if not material.permutation == '':
                material_definition += ' %s' % (material.permutation)
            if not material.region == '':
                material_definition += ' %s' % (material.region)
            if version >= 8205:
                file.write(
                    '\n;MATERIAL %s' % (idx) +
                    '\n%s' % (material.name) +
                    '\n%s\n' % (material_definition)
                )

            else:
                file.write('\n%s' % (material.name))
                if version >= 8203 and version <= 8204:
                    file.write('\n%s' % (material.texture_path))
                file.write('\n%s' % (material_definition))

    if version >= 8205:
        file.write(
            '\n;### MARKERS ###' +
            '\n%s' % (len(jms_scene.markers)) +
            '\n;\t<name>' +
            '\n;\t<node index>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<radius>\n'
        )

    else:
        if version >= 8203 and version <= 8204:
            file.write(
                '\n;' +
                '\n;###Markers###'
                )

        file.write(
            '\n%s' % (len(jms_scene.markers))
        )

    for idx, marker in enumerate(jms_scene.markers):
        if version >= 8205:
            file.write(
                '\n;MARKER %s' % (idx)
            )

        file.write('\n%s' % (marker.name))

        if version >= 8198 and version <= 8204:
            file.write('\n%s' % (marker.region))

        file.write(
            '\n%s' % (marker.parent) +
            decimal_4 % (marker.rotation) +
            decimal_3 % (marker.translation)
        )

        if version >= 8200:
            file.write(decimal_1 % (marker.scale))

        if version >= 8205:
            file.write('\n')

    if version >= 8203 and version <= 8204:
        file.write(
            '\n;' +
            '\n;###Instances###'
            )

    if version >= 8203:
        if version >= 8206:
            file.write(
                '\n;### INSTANCE XREF PATHS ###' +
                '\n%s' % (len(jms_scene.xref_instances)) +
                '\n;\t<path to asset file>' +
                '\n;\t<name>\n'
            )

        elif version == 8205:
            file.write(
                '\n;### INSTANCE XREF PATHS ###' +
                '\n%s' % (len(jms_scene.xref_instances)) +
                '\n;\t<name>\n'
            )

        elif version >= 8203 and version <= 8204:
            file.write(
                '\n;' +
                '\n;###Instance xref paths###' +
                '\n%s' % (len(jms_scene.xref_instances))
                )

        for idx, xref_instance in enumerate(jms_scene.xref_instances):
            if version >= 8205:
                file.write(
                    '\n;XREF %s' % (idx) +
                    '\n%s' % (xref_instance.path) +
                    '\n%s\n' % (xref_instance.name)
                )
            else:
                file.write(
                    '\n%s' % (xref_instance.path) +
                    '\n%s\n' % (xref_instance.name)
                )

        if version >= 8205:
            file.write(
                '\n;### INSTANCE MARKERS ###' +
                '\n%s' % (len(jms_scene.xref_markers)) +
                '\n;\t<name>' +
                '\n;\t<unique identifier>' +
                '\n;\t<path index>' +
                '\n;\t<rotation <i,j,k,w>>' +
                '\n;\t<translation <x,y,z>>\n'
            )

        elif version >= 8203 and version <= 8204:
            file.write(
                '\n;' +
                '\n;###Instance markers###' +
                '\n%s' % (len(jms_scene.xref_markers))
                )

        for idx, xref_marker in enumerate(jms_scene.xref_markers):
            if version >= 8205:
                file.write(
                    '\n;XREF OBJECT %s' % (idx) +
                    '\n%s' % (xref_marker.name) +
                    '\n%s' % (xref_marker.unique_identifier) +
                    '\n%s' % (xref_marker.index) +
                    decimal_4 % (xref_marker.rotation) +
                    decimal_3 % (xref_marker.translation) +
                    '\n'
                )
            else:
                file.write(
                    '\n%s' % (xref_marker.name) +
                    '\n%s' % (xref_marker.unique_identifier) +
                    '\n%s' % (xref_marker.index) +
                    decimal_4 % (xref_marker.rotation) +
                    decimal_3 % (xref_marker.translation) +
                    '\n'
                )

    if version >= 8203 and version <= 8204:
        file.write(
            '\n;' +
            '\n;###Skin data###'
            )

    if version <= 8204:
        if version >= 8203 and version <= 8204:
            file.write(
                '\n;' +
                '\n;###Regions###'
                )

        file.write(
            '\n%s' % (len(jms_scene.regions))
        )

        for region in jms_scene.regions:
            file.write(
                '\n%s' % (region.name)
            )

    if version >= 8205:
        file.write(
            '\n;### VERTICES ###' +
            '\n%s' % (len(jms_scene.vertices)) +
            '\n;\t<position>' +
            '\n;\t<normal>' +
            '\n;\t<node influences count>' +
            '\n;\t\t<index>' +
            '\n;\t\t<weight>' +
            '\n;\t<texture coordinate count>' +
            '\n;\t\t<texture coordinates <u,v>>\n'
        )

        if version >= 8211:
            file.write(
                ';\t<vertex color <r,g,b>>\n'
            )
    else:
        if version >= 8203 and version <= 8204:
            file.write(
                '\n;' +
                '\n;###Vertices###'
                )

        file.write(
            '\n%s' % (len(jms_scene.vertices))
        )

    for idx, vertex in enumerate(jms_scene.vertices):
        if version >= 8205:
            file.write(
                '\n;VERTEX %s' % (idx) +
                decimal_3 % (vertex.translation[0], vertex.translation[1], vertex.translation[2]) +
                decimal_3 % (vertex.normal[0], vertex.normal[1], vertex.normal[2]) +
                '\n%s' % (len(vertex.node_set))
            )
            for node in vertex.node_set:
                node_index = node[0]
                node_weight = node[1]
                file.write(
                    '\n%s' % (node_index) +
                    decimal_1 % (node_weight)
                )

            file.write('\n%s' % (len(vertex.uv_set)))

            for uv in vertex.uv_set:
                tex_u = uv[0]
                tex_v = uv[1]
                file.write(decimal_2 % (tex_u, tex_v))

            if version >= 8211:
                file.write(
                    decimal_3 % (vertex.color[0], vertex.color[1], vertex.color[2])
                )
            file.write('\n')

        else:
            uv_0 = vertex.uv_set[0]
            tex_u_0 = uv_0[0]
            tex_v_0 = uv_0[1]

            uv_1 = None
            tex_u_1 = 0.0
            tex_v_1 = 0.0
            if len(vertex.uv_set) > 1:
                uv_1 = vertex.uv_set[1]
                tex_u_1 = uv_1[0]
                tex_v_1 = uv_1[1]

            uv_2 = None
            tex_u_2 = 0.0
            tex_v_2 = 0.0
            if len(vertex.uv_set) > 2:
                uv_2 = vertex.uv_set[2]
                tex_u_2 = uv_2[0]
                tex_v_2 = uv_2[1]

            uv_3 = None
            tex_u_3 = 0.0
            tex_v_3 = 0.0
            if len(vertex.uv_set) > 3:
                uv_3 = vertex.uv_set[3]
                tex_u_3 = uv_3[0]
                tex_v_3 = uv_3[1]

            if version < 8198:
                file.write(
                    '\n%s' % (vertex.region)
                )

            node0 = (int(-1), float(0.0))
            if len(vertex.node_set) > 0:
                node0 = vertex.node_set[0]

            node1 = (int(-1), float(0.0))
            if len(vertex.node_set) > 1:
                node1 = vertex.node_set[1]

            node2 = (int(-1), float(0.0))
            if len(vertex.node_set) > 2:
                node2 = vertex.node_set[2]

            node3 = (int(-1), float(0.0))
            if len(vertex.node_set) > 3:
                node3 = vertex.node_set[3]

            node0_index = node0[0]
            node0_weight = node0[1]

            node1_index = node1[0]
            node1_weight = node1[1]

            node2_index = node2[0]
            node2_weight = node2[1]

            node3_index = node3[0]
            node3_weight = node3[1]

            if version < 8202:
                if not node1_index == -1:
                    node1_weight = 1.0 - node0_weight

                if node1_weight == 0:
                    node1_index = -1

                if node1_weight == 1:
                    node0_index = node1[0]
                    node1_index = -1
                    node1_weight = 0.0

            if version >= 8204:
                file.write(
                    '\n%s' % (node0_index) +
                    decimal_1 % (node0_weight) +
                    decimal_3 % (vertex.translation[0], vertex.translation[1], vertex.translation[2]) +
                    decimal_3 % (vertex.normal[0], vertex.normal[1], vertex.normal[2]) +
                    '\n%s' % (node1_index) +
                    decimal_1 % (node1_weight) +
                    '\n%s' % (node2_index) +
                    decimal_1 % (node2_weight) +
                    '\n%s' % (node3_index) +
                    decimal_1 % (node3_weight)
                )
            else:
                file.write(
                    '\n%s' % (node0_index) +
                    decimal_3 % (vertex.translation[0], vertex.translation[1], vertex.translation[2]) +
                    decimal_3 % (vertex.normal[0], vertex.normal[1], vertex.normal[2]) +
                    '\n%s' % (node1_index) +
                    decimal_1 % (node1_weight)
                )

            if version >= 8200:
                if version >= 8203 and version <= 8204:
                    file.write(
                        decimal_2 % (tex_u_0, tex_v_0) +
                        decimal_2 % (tex_u_1, tex_v_1) +
                        decimal_2 % (tex_u_2, tex_v_2) +
                        decimal_2 % (tex_u_3, tex_v_3)
                    )

                else:
                    file.write(
                        decimal_1 % (tex_u_0) +
                        decimal_1 % (tex_v_0)
                    )

            else:
                file.write(decimal_2 % (tex_u_0, tex_v_0))

            if version >= 8199:
                unused_flag = 0
                file.write('\n%s' % (unused_flag))

    if version >= 8205:
        file.write(
            '\n;### TRIANGLES ###' +
            '\n%s' % (len(jms_scene.triangles)) +
            '\n;\t<material index>' +
            '\n;\t<vertex indices <v0,v1,v2>>\n'
        )

    else:
        if version >= 8203 and version <= 8204:
            file.write(
                '\n;' +
                '\n;###Faces###'
                )

        file.write(
            '\n%s' % (len(jms_scene.triangles))
        )

    for idx, triangle in enumerate(jms_scene.triangles):
        if version >= 8205:
            file.write(
                '\n;TRIANGLE %s' % (idx) +
                '\n%s' % (triangle.material_index) +
                '\n%s\t%s\t%s\n' % (triangle.v0, triangle.v1, triangle.v2)
            )

        else:
            if version >= 8198:
                file.write('\n%s' % (triangle.region))

            file.write(
                '\n%s' % (triangle.material_index) +
                '\n%s\t%s\t%s' % (triangle.v0, triangle.v1, triangle.v2)
            )

    if version <= 8204:
        file.write('\n')

    if version >= 8206:
        file.write(
            '\n;### SPHERES ###' +
            '\n%s' % (len(jms_scene.spheres)) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<radius>\n'
        )

        #write sphere
        for idx, sphere in enumerate(jms_scene.spheres):
            file.write(
                '\n;SPHERE %s' % (idx) +
                '\n%s' % (sphere.name) +
                '\n%s' % (sphere.parent_index) +
                '\n%s' % (sphere.material_index) +
                decimal_4 % (sphere.rotation) +
                decimal_3 % (sphere.translation) +
                decimal_1 % (sphere.scale) +
                '\n'
            )

        #write boxes
        file.write(
            '\n;### BOXES ###' +
            '\n%s' % (len(jms_scene.boxes)) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<width (x)>' +
            '\n;\t<length (y)>' +
            '\n;\t<height (z)>\n'
        )

        for idx, box in enumerate(jms_scene.boxes):
            file.write(
                '\n;BOXES %s' % (idx) +
                '\n%s' % (box.name) +
                '\n%s' % (box.parent_index) +
                '\n%s' % (box.material_index) +
                decimal_4 % (box.rotation) +
                decimal_3 % (box.translation) +
                decimal_1 % (box.width) +
                decimal_1 % (box.length) +
                decimal_1 % (box.height) +
                '\n'
            )

        #write capsules
        file.write(
            '\n;### CAPSULES ###' +
            '\n%s' % (len(jms_scene.capsules)) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<height>' +
            '\n;\t<radius>\n'
             )

        for idx, capsule in enumerate(jms_scene.capsules):
            file.write(
                '\n;CAPSULES %s' % (idx) +
                '\n%s' % (capsule.name) +
                '\n%s' % (capsule.parent_index) +
                '\n%s' % (capsule.material_index) +
                decimal_4 % (capsule.rotation) +
                decimal_3 % (capsule.translation) +
                decimal_1 % (capsule.height) +
                decimal_1 % (capsule.radius) +
                '\n'
            )

        #write convex shapes
        file.write(
            '\n;### CONVEX SHAPES ###' +
            '\n%s' % (len(jms_scene.convex_shapes)) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<vertex count>' +
            '\n;\t<...vertices>\n'
        )

        for idx, convex_shape in enumerate(jms_scene.convex_shapes):
            file.write(
                '\n;CONVEX %s' % (idx) +
                '\n%s' % (convex_shape.name) +
                '\n%s' % (convex_shape.parent_index) +
                '\n%s' % (convex_shape.material_index) +
                decimal_4 % (convex_shape.rotation) +
                decimal_3 % (convex_shape.translation) +
                '\n%s' % (len(convex_shape.verts))
            )

            for vertex in convex_shape.verts:
                file.write(decimal_3 % (vertex.translation))

            file.write('\n')

        #write rag dolls
        file.write(
            '\n;### RAGDOLLS ###' +
            '\n%s' % (len(jms_scene.ragdolls)) +
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

        if version == 8213:
            file.write(';\t<friction limit>\n')
        for idx, ragdoll in enumerate(jms_scene.ragdolls):
            file.write(
                '\n;RAGDOLL %s' % (idx) +
                '\n%s' % (ragdoll.name) +
                '\n%s' % (ragdoll.attached_index) +
                '\n%s' % (ragdoll.referenced_index) +
                decimal_4 % (ragdoll.attached_rotation) +
                decimal_3 % (ragdoll.attached_translation) +
                decimal_4 % (ragdoll.referenced_rotation) +
                decimal_3 % (ragdoll.referenced_translation) +
                decimal_1 % (ragdoll.min_twist) +
                decimal_1 % (ragdoll.max_twist) +
                decimal_1 % (ragdoll.min_cone) +
                decimal_1 % (ragdoll.max_cone) +
                decimal_1 % (ragdoll.min_plane) +
                decimal_1 % (ragdoll.max_plane)
            )

            if version == 8213:
                file.write(decimal_1 % (ragdoll.friction_limit))
            file.write('\n')

        #write hinges
        file.write(
            '\n;### HINGES ###' +
            '\n%s' % (len(jms_scene.hinges)) +
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

        for idx, hinge in enumerate(jms_scene.hinges):
            file.write(
                '\n;HINGE %s' % (idx) +
                '\n%s' % (hinge.name) +
                '\n%s' % (hinge.body_a_index) +
                '\n%s' % (hinge.body_b_index) +
                decimal_4 % (hinge.body_a_rotation) +
                decimal_3 % (hinge.body_a_translation) +
                decimal_4 % (hinge.body_b_rotation) +
                decimal_3 % (hinge.body_b_translation) +
                '\n%s' % (hinge.is_limited) +
                decimal_1 % (hinge.friction_limit) +
                decimal_1 % (hinge.min_angle) +
                decimal_1 % (hinge.max_angle) +
                '\n'
            )

        if version > 8209:
            #write car wheel
            file.write(
                '\n;### CAR WHEEL ###' +
                '\n%s' % (len(jms_scene.car_wheels)) +
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

            for idx, car_wheel in enumerate(jms_scene.car_wheels):
                file.write(
                    '\n;CAR WHEEL %s' % (idx) +
                    '\n%s' % (car_wheel.name) +
                    '\n%s' % (car_wheel.chassis_index) +
                    '\n%s' % (car_wheel.wheel_index) +
                    decimal_4 % (car_wheel.chassis_rotation) +
                    decimal_3 % (car_wheel.chassis_translation) +
                    decimal_4 % (car_wheel.wheel_rotation) +
                    decimal_3 % (car_wheel.wheel_translation) +
                    decimal_4 % (car_wheel.suspension_rotation) +
                    decimal_3 % (car_wheel.suspension_translation) +
                    decimal_1 % (car_wheel.suspension_min_limit) +
                    decimal_1 % (car_wheel.suspension_max_limit) +
                    decimal_1 % (car_wheel.friction_limit) +
                    decimal_1 % (car_wheel.velocity) +
                    decimal_1 % (car_wheel.gain) +
                    '\n'
                )

            #write point to point
            file.write(
                '\n;### POINT TO POINT ###' +
                '\n%s' % (len(jms_scene.point_to_points)) +
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

            for idx, point_to_point in enumerate(jms_scene.point_to_points):
                file.write(
                    '\n;POINT_TO_POINT %s' % (idx) +
                    '\n%s' % (point_to_point.name) +
                    '\n%s' % (point_to_point.body_a_index) +
                    '\n%s' % (point_to_point.body_b_index) +
                    decimal_4 % (point_to_point.body_b_rotation) +
                    decimal_3 % (point_to_point.body_b_translation) +
                    decimal_4 % (point_to_point.body_a_rotation) +
                    decimal_3 % (point_to_point.body_a_translation) +
                    '\n%s' % (point_to_point.constraint_type) +
                    decimal_1 % (point_to_point.x_min_limit) +
                    decimal_1 % (point_to_point.x_max_limit) +
                    decimal_1 % (point_to_point.y_min_limit) +
                    decimal_1 % (point_to_point.y_max_limit) +
                    decimal_1 % (point_to_point.z_min_limit) +
                    decimal_1 % (point_to_point.z_max_limit) +
                    decimal_1 % (point_to_point.spring_length) +
                    '\n'
                )

            #write prismatic
            file.write(
                '\n;### PRISMATIC ###' +
                '\n%s' % (len(jms_scene.prismatics)) +
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

            for idx, prismatic in enumerate(jms_scene.prismatics):
                file.write(
                    '\n;PRISMATIC %s' % (idx) +
                    '\n%s' % (prismatic.name) +
                    '\n%s' % (prismatic.body_a_index) +
                    '\n%s' % (prismatic.body_b_index) +
                    decimal_4 % (prismatic.body_a_rotation) +
                    decimal_3 % (prismatic.body_a_translation) +
                    decimal_4 % (prismatic.body_b_rotation) +
                    decimal_3 % (prismatic.body_b_translation) +
                    '\n%s' % (prismatic.is_limited) +
                    decimal_1 % (prismatic.friction_limit) +
                    decimal_1 % (prismatic.min_limit) +
                    decimal_1 % (prismatic.max_limit) +
                    '\n'
                )

        if version >= 8209:
            #write bounding sphere
            file.write(
                '\n;### BOUNDING SPHERE ###' +
                '\n%s' % (len(jms_scene.bounding_spheres)) +
                '\n;\t<translation <x,y,z>>' +
                '\n;\t<radius>\n'
            )

            for idx, bounding_sphere in enumerate(jms_scene.bounding_spheres):
                file.write(
                    '\n;BOUNDING SPHERE %s' % (idx) +
                    decimal_3 % (bounding_sphere.translation) +
                    decimal_1 % (bounding_sphere.scale) +
                    '\n'
                )

        if version >= 8212:
            #write skylight
            file.write(
                '\n;### SKYLIGHT ###' +
                '\n%s' % (len(jms_scene.skylights)) +
                '\n;\t<direction <x,y,z>>' +
                '\n;\t<radiant intensity <x,y,z>>' +
                '\n;\t<solid angle>\n'
            )

            for idx, light in enumerate(jms_scene.skylights):
                file.write(
                    '\n;SKYLIGHT %s' % (idx) +
                    decimal_3 % light.direction +
                    decimal_3 % light.radiant_intensity +
                    decimal_1 % light.solid_angle +
                    '\n'
                )
    report({'INFO'}, "Export completed successfully")
    file.close()

def command_queue(context, filepath, report, jms_version, jms_version_ce, jms_version_h2, jms_version_h3, generate_checksum, folder_structure, folder_type, apply_modifiers, triangulate_faces, fix_rotations, edge_split, use_edge_angle, use_edge_sharp, split_angle, clean_normalize_weights, scale_enum, scale_float, console, permutation_ce, level_of_detail_ce, hidden_geo, export_render, export_collision, export_physics, game_version, world_nodes):
    object_properties = []
    node_prefix_tuple = ('b ', 'b_', 'bone', 'frame', 'bip01')
    limit_value = 0.001

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

    object_list = list(scene.objects)

    global_functions.unhide_all_collections(context)

    jmi = False
    if not world_nodes == None:
        jmi = True
        object_list = world_nodes

    edge_split = global_functions.EdgeSplit(edge_split, use_edge_angle, split_angle, use_edge_sharp)

    version = global_functions.get_version(jms_version, jms_version_ce, jms_version_h2, jms_version_h3, game_version, console)
    level_of_detail_ce = mesh_processing.get_lod(level_of_detail_ce, game_version)
    custom_scale = global_functions.set_scale(scale_enum, scale_float)

    for obj in object_list:
        if obj.type== 'MESH':
            if clean_normalize_weights:
                mesh_processing.vertex_group_clean_normalize(context, obj, limit_value)

            if apply_modifiers:
                mesh_processing.add_modifier(context, obj, triangulate_faces, edge_split, None)

    depsgraph = context.evaluated_depsgraph_get()
    for obj in object_list:
        object_properties.append((obj.hide_get(), obj.hide_viewport))
        if hidden_geo:
            mesh_processing.unhide_object(obj)

        name = obj.name.lower()
        parent_name = None
        if obj.parent:
            parent_name = obj.parent.name.lower()

        if name[0:1] == '!':
            world_node_count += 1

        elif obj.type == 'ARMATURE':
            mesh_processing.unhide_object(obj)
            armature = obj
            armature_bones = obj.data.bones
            armature_count += 1
            node_list = list(armature_bones)

        elif name.startswith(node_prefix_tuple):
            mesh_processing.unhide_object(obj)
            mesh_frame_count += 1
            node_list.append(obj)

        elif name[0:1] == '#':
            if mesh_processing.set_ignore(obj) == False or hidden_geo:
                if not obj.parent == None:
                    if obj.parent.type == 'ARMATURE' or parent_name.startswith(node_prefix_tuple):
                        if export_render and obj.marker.marker_mask_type =='0':
                            render_marker_list.append(obj)
                            render_count += 1

                        elif export_collision and obj.marker.marker_mask_type =='1':
                            collision_marker_list.append(obj)
                            collision_count += 1

                        elif export_physics and obj.marker.marker_mask_type =='2':
                            physics_marker_list.append(obj)
                            physics_count += 1

                        elif obj.marker.marker_mask_type =='3':
                            marker_list.append(obj)
                            render_count += 1
                            collision_count += 1
                            physics_count += 1

        elif name[0:1] == '@' and len(obj.data.polygons) > 0:
            if mesh_processing.set_ignore(obj) == False or hidden_geo:
                if export_collision:
                    if not obj.parent == None:
                        if obj.parent.type == 'ARMATURE' or parent_name.startswith(node_prefix_tuple):
                            collision_count += 1
                            if apply_modifiers:
                                obj_for_convert = obj.evaluated_get(depsgraph)
                                evaluted_mesh = obj_for_convert.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
                                collision_geometry_list.append((evaluted_mesh, obj))

                            else:
                                evaluted_mesh = obj.to_mesh(preserve_all_data_layers=True)
                                collision_geometry_list.append((evaluted_mesh, obj))

        elif name[0:1] == '$' and not game_version == "haloce" and version > 8205:
            if mesh_processing.set_ignore(obj) == False or hidden_geo:
                if export_physics:
                    physics_count += 1
                    if not obj.rigid_body_constraint == None:
                        if obj.rigid_body_constraint.type == 'HINGE':
                            hinge_list.append(obj)

                        elif obj.rigid_body_constraint.type == 'GENERIC':
                            ragdoll_list.append(obj)

                        elif obj.rigid_body_constraint.type == 'GENERIC_SPRING':
                            point_to_point_list.append(obj)

                    else:
                        if obj.type == 'MESH':
                            phy_material = global_functions.get_face_material(obj, obj.data.polygons[0])
                            if not phy_material == -1:
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
                                        convex_shape_list.append((evaluted_mesh, obj))

                                    else:
                                        evaluted_mesh = obj.to_mesh(preserve_all_data_layers=True)
                                        convex_shape_list.append((evaluted_mesh, obj))

        elif obj.type== 'MESH' and not len(obj.data.ass_jms.XREF_path) == 0 and version > 8205:
            if mesh_processing.set_ignore(obj) == False or hidden_geo:
                if export_render:
                    instance_markers.append(obj)
                    if not obj.data.ass_jms.XREF_path in instance_xref_paths:
                        instance_xref_paths.append(obj.data.ass_jms.XREF_path)


        elif obj.type== 'MESH' and obj.data.ass_jms.bounding_radius and version >= 8209:
            if mesh_processing.set_ignore(obj) == False or hidden_geo:
                if export_render:
                    bounding_sphere_list.append(obj)

        elif obj.type == 'LIGHT' and version > 8212:
            if mesh_processing.set_ignore(obj) == False or hidden_geo:
                if obj.data.type == 'SUN':
                    if export_render:
                        skylight_list.append(obj)

        elif obj.type== 'MESH' and len(obj.data.polygons) > 0:
            if mesh_processing.set_ignore(obj) == False or hidden_geo:
                if export_render:
                    if not obj.parent == None:
                        if obj.parent.type == 'ARMATURE' or parent_name.startswith(node_prefix_tuple):
                            render_count += 1
                            if apply_modifiers:
                                obj_for_convert = obj.evaluated_get(depsgraph)
                                evaluted_mesh = obj_for_convert.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
                                render_geometry_list.append((evaluted_mesh, obj))

                            else:
                                evaluted_mesh = obj.to_mesh(preserve_all_data_layers=True)
                                render_geometry_list.append((evaluted_mesh, obj))

    blend_scene = global_functions.BlendScene(world_node_count, armature_count, mesh_frame_count, render_count, collision_count, physics_count, armature, node_list, render_marker_list, collision_marker_list, physics_marker_list, marker_list, instance_xref_paths, instance_markers, render_geometry_list, collision_geometry_list, sphere_list, box_list, capsule_list, convex_shape_list, ragdoll_list, hinge_list, car_wheel_list, point_to_point_list, prismatic_list, bounding_sphere_list, skylight_list)

    global_functions.validate_halo_jms_scene(game_version, version, blend_scene, object_list, jmi)

    if export_render and blend_scene.render_count > 0:
        model_type = "render"

        write_file(context, filepath, report, version, game_version, generate_checksum, fix_rotations, folder_structure, folder_type, permutation_ce, level_of_detail_ce, model_type, blend_scene, jmi, custom_scale)

    if export_collision and blend_scene.collision_count > 0:
        model_type = "collision"

        write_file(context, filepath, report, version, game_version, generate_checksum, fix_rotations, folder_structure, folder_type, permutation_ce, level_of_detail_ce, model_type, blend_scene, jmi, custom_scale)

    if export_physics and blend_scene.physics_count > 0:
        model_type = "physics"

        write_file(context, filepath, report, version, game_version, generate_checksum, fix_rotations, folder_structure, folder_type, permutation_ce, level_of_detail_ce, model_type, blend_scene, jmi, custom_scale)

    for idx, obj in enumerate(object_list):
        property_value = object_properties[idx]
        obj.hide_set(property_value[0])
        obj.hide_viewport = property_value[1]

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_scene.jms()
