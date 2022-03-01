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

from .format import JMSAsset
from ..global_functions import global_functions

def process_file_retail(JMS, game_version, extension, version_list, default_region, default_permutation):
    JMS.version = int(JMS.next())
    JMS.game_version = game_version
    if game_version == 'auto':
        JMS.game_version = global_functions.get_game_version(JMS.version, 'JMS')

    if not JMS.version in version_list:
        raise global_functions.AssetParseError("Importer does not support this " + extension + " version")

    if JMS.version < 8205:
        JMS.skip(1) # skip the node checksum

    node_count = int(JMS.next())
    transforms_for_frame = []

    if JMS.version >= 8205:
        for node_idx in range(node_count):
            name = JMS.next()
            parent = int(JMS.next())
            JMS.nodes.append(JMSAsset.Node(name, parent=parent))
            transforms_for_frame.append(JMS.next_transform())

    else:
        for node_idx in range(node_count):
            name = JMS.next()
            child = int(JMS.next())
            sibling = int(JMS.next())
            JMS.nodes.append(JMSAsset.Node(name, child=child, sibling=sibling))
            transforms_for_frame.append(JMS.next_transform())

    JMS.transforms.append(transforms_for_frame)
    material_count = int(JMS.next())
    for material in range(material_count):
        name = JMS.next()
        if JMS.version >= 8203 and JMS.version <= 8204:
            texture_definition = JMS.next()

        material_definition = JMS.next()
        if JMS.game_version == 'haloce':
            JMS.materials.append(JMSAsset.Material(name, material_definition, None, None, None, None))

        elif JMS.game_version == 'halo2' or JMS.game_version == 'halo3':
            material_definition_items = material_definition.split()
            lod, permutation, region = global_functions.material_definition_parser(True, material_definition_items, default_region, default_permutation)

            JMS.materials.append(JMSAsset.Material(name, None, material, lod, permutation, region))

    marker_count = int(JMS.next())
    for marker in range(marker_count):
        name = JMS.next()
        region = -1
        if JMS.version >= 8198 and JMS.version < 8205:
            region = int(JMS.next())

        parent = int(JMS.next())
        rotation = JMS.next_quaternion()
        translation = JMS.next_vector()
        radius = 1
        if JMS.version >= 8200:
            radius = float(JMS.next())

        JMS.markers.append(JMSAsset.Marker(name, region, parent, rotation, translation, radius))

    if JMS.version >= 8201:
        xref_instance_count = int(JMS.next())
        for xref_idx in range(xref_instance_count):
            xref_path = JMS.next()
            xref_name = None
            if JMS.version >= 8208:
                xref_name = JMS.next()

            JMS.xref_instances.append(JMSAsset.XREF(xref_path, xref_name))

        xref_markers_count = int(JMS.next())
        for xref_marker_idx in range(xref_markers_count):
            name = JMS.next()
            unique_identifier = None
            if JMS.version >= 8203:
                unique_identifier = int(JMS.next())

            path_index = int(JMS.next())
            rotation = JMS.next_quaternion()
            translation = JMS.next_vector()
            JMS.xref_markers.append(JMSAsset.XREF_Marker(name, unique_identifier, path_index, rotation, translation))

    if JMS.version < 8205:
        region_count = int(JMS.next())
        for region in range(region_count):
            name = JMS.next()
            if name == "__unnamed":
                name = "unnamed"

            JMS.regions.append(JMSAsset.Region(name))

    vertex_count = int(JMS.next())
    for vertex in range(vertex_count):
        node_set = []
        uv_set = []
        region = None
        color = None
        if JMS.version >= 8205:
            translation = JMS.next_vector()
            normal = JMS.next_vector()
            node_influence_count = int(JMS.next())
            for node in range(node_influence_count):
                node_index = int(JMS.next())
                node_weight = float(JMS.next())
                node_set.append([node_index, node_weight])

            uv_count = int(JMS.next())
            for uv in range(uv_count):
                tex_u_value   = JMS.next()
                tex_v_value   = JMS.next()
                try:
                    tex_u = float(tex_u_value)

                except ValueError:
                    tex_u = float(tex_u_value.rsplit('.', 1)[0])

                try:
                    tex_v = float(tex_v_value)

                except ValueError:
                    tex_v = float(tex_v_value.rsplit('.', 1)[0])

                u = tex_u
                v = tex_v
                uv_set.append([u, v])
            if JMS.version >= 8211:
                color = JMS.next_vector()

        else:
            node_influence_count = 0
            if JMS.version == 8197:
                region = int(JMS.next())
                JMS.active_regions.append(region)

            node_0_index = int(JMS.next())
            if JMS.version == 8204:
                node_0_weight = float(JMS.next())

            translation = JMS.next_vector()
            normal = JMS.next_vector()
            node_1_index = int(JMS.next())
            node_1_weight = float(JMS.next())
            node_2_index = -1
            node_3_index = -1
            if JMS.version == 8204:
                node_2_index = int(JMS.next())
                node_2_weight = float(JMS.next())
                node_3_index = int(JMS.next())
                node_3_weight = float(JMS.next())

            if JMS.version >= 8204:
                node_set.append([node_0_index, node_0_weight])

            else:
                node_set.append([node_0_index, 1])

            node_set.append([node_1_index, node_1_weight])
            if JMS.version >= 8204:
                node_set.append([node_2_index, node_2_weight])
                node_set.append([node_3_index, node_3_weight])

            if not node_0_index == -1:
                node_influence_count += 1

            if not node_1_index == -1:
                node_influence_count += 1

            if not node_2_index == -1:
                node_influence_count += 1

            if not node_3_index == -1:
                node_influence_count += 1

            if JMS.version >= 8205:
                uv_count = int(JMS.next())
                for uv in range(uv_count):
                    tex_u_value   = JMS.next()
                    tex_v_value   = JMS.next()
                    try:
                        tex_u = float(tex_u_value)

                    except ValueError:
                        tex_u = float(tex_u_value.rsplit('.', 1)[0])

                    try:
                        tex_v = float(tex_v_value)

                    except ValueError:
                        tex_v = float(tex_v_value.rsplit('.', 1)[0])

                    u = tex_u
                    v = tex_v
                    uv_set.append([u, v])

            else:
                tex_0_u_value = JMS.next()
                tex_0_v_value = JMS.next()
                if JMS.version >= 8203:
                    tex_1_u_value = JMS.next()
                    tex_1_v_value = JMS.next()
                    tex_2_u_value = JMS.next()
                    tex_2_v_value = JMS.next()
                    tex_3_u_value = JMS.next()
                    tex_3_v_value = JMS.next()

                try:
                    tex_0_u = float(tex_0_u_value)

                except ValueError:
                    tex_0_u = float(tex_0_u_value.rsplit('.', 1)[0])

                try:
                    tex_0_v = float(tex_0_v_value)

                except ValueError:
                    tex_0_v = float(tex_0_v_value.rsplit('.', 1)[0])

                if JMS.version >= 8203:
                    try:
                        tex_1_u = float(tex_1_u_value)

                    except ValueError:
                        tex_1_u = float(tex_1_u_value.rsplit('.', 1)[0])

                    try:
                        tex_1_v = float(tex_1_v_value)

                    except ValueError:
                        tex_1_v = float(tex_1_v_value.rsplit('.', 1)[0])

                    try:
                        tex_2_u = float(tex_2_u_value)

                    except ValueError:
                        tex_2_u = float(tex_2_u_value.rsplit('.', 1)[0])

                    try:
                        tex_2_v = float(tex_2_v_value)

                    except ValueError:
                        tex_2_v = float(tex_2_v_value.rsplit('.', 1)[0])

                    try:
                        tex_3_u = float(tex_3_u_value)

                    except ValueError:
                        tex_3_u = float(tex_3_u_value.rsplit('.', 1)[0])

                    try:
                        tex_3_v = float(tex_3_v_value)

                    except ValueError:
                        tex_3_v = float(tex_3_v_value.rsplit('.', 1)[0])

                if JMS.version >= 8203:
                    uv_set.append([tex_0_u, tex_0_v])
                    uv_set.append([tex_1_u, tex_1_v])
                    uv_set.append([tex_2_u, tex_2_v])
                    uv_set.append([tex_3_u, tex_3_v])

                else:
                    uv_set.append([tex_0_u, tex_0_v])

            flags = None
            if JMS.version >= 8199:
                flags = JMS.skip(1) #Unused int or boolean value. Don't know which but definitely not a float

        JMS.vertices.append(JMSAsset.Vertex(node_influence_count, node_set, region, translation, normal, color, uv_set))

    triangle_count = int(JMS.next())
    for triangle in range(triangle_count):
        region = None
        if JMS.version >= 8198 and JMS.version < 8205:
            region = int(JMS.next())
            JMS.active_regions.append(region)

        material_index = int(JMS.next())
        v0 = int(JMS.next())
        v1 = int(JMS.next())
        v2 = int(JMS.next())
        JMS.triangles.append(JMSAsset.Triangle(region, material_index, v0, v1, v2))

    if JMS.version >= 8206:
        sphere_count = int(JMS.next())
        for sphere in range(sphere_count):
            name = JMS.next()
            parent_index = int(JMS.next())
            material_index = None
            if JMS.version >= 8207:
                material_index = int(JMS.next())

            rotation = JMS.next_quaternion()
            translation = JMS.next_vector()
            radius = float(JMS.next())
            JMS.spheres.append(JMSAsset.Sphere(name, parent_index, material_index, rotation, translation, radius))

        boxes_count = int(JMS.next())
        for box in range(boxes_count):
            name = JMS.next()
            parent_index = int(JMS.next())
            material_index = None
            if JMS.version >= 8207:
                material_index = int(JMS.next())

            rotation = JMS.next_quaternion()
            translation = JMS.next_vector()
            width = float(JMS.next())
            length = float(JMS.next())
            height = float(JMS.next())
            JMS.boxes.append(JMSAsset.Box(name, parent_index, material_index, rotation, translation, width, length, height))

        capsules_count = int(JMS.next())
        for capsules in range(capsules_count):
            name = JMS.next()
            parent_index = int(JMS.next())
            material_index = None
            if JMS.version >= 8207:
                material_index = int(JMS.next())

            rotation = JMS.next_quaternion()
            translation = JMS.next_vector()
            height = float(JMS.next())
            radius = float(JMS.next())
            JMS.capsules.append(JMSAsset.Capsule(name, parent_index, material_index, rotation, translation, height, radius))

        convex_shape_count = int(JMS.next())
        for convex_shape in range(convex_shape_count):
            vert = []
            name = JMS.next()
            parent_index = int(JMS.next())
            material_index = None
            if JMS.version >= 8207:
                material_index = int(JMS.next())

            rotation = JMS.next_quaternion()
            translation = JMS.next_vector()
            vertex_count = int(JMS.next())
            for vertex in range(vertex_count):
                vert.append(JMS.next_vector())

            JMS.convex_shapes.append(JMSAsset.Convex_Shape(name, parent_index, material_index, rotation, translation, vert))

        ragdoll_count  = int(JMS.next())
        for ragdoll in range(ragdoll_count):
            name = JMS.next()
            attached_index = int(JMS.next())
            referenced_index = int(JMS.next())
            attached_rotation = JMS.next_quaternion()
            attached_translation = JMS.next_vector()
            referenced_rotation = JMS.next_quaternion()
            referenced_translation = JMS.next_vector()
            min_twist = float(JMS.next())
            max_twist = float(JMS.next())
            min_cone = float(JMS.next())
            max_cone = float(JMS.next())
            min_plane = float(JMS.next())
            max_plane = float(JMS.next())
            friction_limit = 0.0
            if JMS.version >= 8213:
                friction_limit = float(JMS.next())

            JMS.ragdolls.append(JMSAsset.Ragdoll(name, attached_index, referenced_index, attached_rotation, attached_translation, referenced_rotation, referenced_translation, min_twist, max_twist, min_cone, max_cone, min_plane, max_plane, friction_limit))

        hinge_count  = int(JMS.next())
        for hinge in range(hinge_count):
            name = JMS.next()
            body_a_index = int(JMS.next())
            body_b_index = int(JMS.next())
            body_a_rotation = JMS.next_quaternion()
            body_a_translation = JMS.next_vector()
            body_b_rotation = JMS.next_quaternion()
            body_b_translation = JMS.next_vector()
            is_limited = int(JMS.next())
            friction_limit = float(JMS.next())
            min_angle = float(JMS.next())
            max_angle = float(JMS.next())

            JMS.hinges.append(JMSAsset.Hinge(name, body_a_index, body_b_index, body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, is_limited, friction_limit, min_angle, max_angle))

    if JMS.version >= 8210:
        car_wheel_count  = int(JMS.next())
        for car_wheel in range(car_wheel_count):
            name = JMS.next()
            chassis_index = int(JMS.next())
            wheel_index = int(JMS.next())
            wheel_rotation = JMS.next_quaternion()
            wheel_translation = JMS.next_vector()
            suspension_rotation = JMS.next_quaternion()
            suspension_translation = JMS.next_vector()
            suspension_min_limit = float(JMS.next())
            suspension_max_limit = float(JMS.next())
            friction_limit = float(JMS.next())
            velocity = float(JMS.next())
            gain = float(JMS.next())

            JMS.car_wheels.append(JMSAsset.Car_Wheel(name, chassis_index, wheel_index, wheel_rotation, wheel_translation, suspension_rotation, suspension_translation, suspension_min_limit, suspension_max_limit, friction_limit, velocity, gain))

        point_to_point_count = int(JMS.next())
        for point_to_point in range(point_to_point_count):
            name = JMS.next()
            body_a_index = int(JMS.next())
            body_b_index = int(JMS.next())
            body_a_rotation = JMS.next_quaternion()
            body_a_translation = JMS.next_vector()
            body_b_rotation = JMS.next_quaternion()
            body_b_translation = JMS.next_vector()
            constraint_type = int(JMS.next())
            x_min_limit = float(JMS.next())
            x_max_limit = float(JMS.next())
            y_min_limit = float(JMS.next())
            y_max_limit = float(JMS.next())
            z_min_limit = float(JMS.next())
            z_max_limit = float(JMS.next())
            spring_length = float(JMS.next())

            JMS.point_to_points.append(JMSAsset.Point_to_Point(name, body_a_index, body_b_index, body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, constraint_type, x_min_limit, x_max_limit, y_min_limit, y_max_limit, z_min_limit, z_max_limit, spring_length))

        prismatic_count = int(JMS.next())
        for prismatic in range(prismatic_count):
            name = JMS.next()
            body_a_index = int(JMS.next())
            body_b_index = int(JMS.next())
            body_a_rotation = JMS.next_quaternion()
            body_a_translation = JMS.next_vector()
            body_b_rotation = JMS.next_quaternion()
            body_b_translation = JMS.next_vector()
            is_limited = int(JMS.next())
            friction_limit = float(JMS.next())
            min_limit = float(JMS.next())
            max_limit = float(JMS.next())

            JMS.prismatics.append(JMSAsset.Prismatic(name, body_a_index, body_b_index, body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, is_limited, friction_limit, min_limit, max_limit))

    if JMS.version >= 8209:
        bounding_sphere_count = int(JMS.next())
        for bounding_sphere in range(bounding_sphere_count):
            translation = JMS.next_vector()
            radius = float(JMS.next())

            JMS.bounding_spheres.append(JMSAsset.Bounding_Sphere(translation, radius))

    if JMS.version >= 8212:
        skylight_count = int(JMS.next())
        for skylight in range(skylight_count):
            direction = JMS.next_vector()
            radiant_intensity = JMS.next_vector()
            solid_angle = float(JMS.next())

            JMS.skylights.append(JMSAsset.Skylight(direction, radiant_intensity, solid_angle))

    if JMS.left() != 0: # is something wrong with the parser?
        raise RuntimeError("%s elements left after parse end" % JMS.left())

    # update node graph
    if JMS.version >= 8205:
        # loop over nodes and
        for node_idx in range(node_count):
            node = JMS.nodes[node_idx]
            if node.parent == -1:
                continue # this is a root node, nothing to update

            if node.parent >= len(JMS.nodes) or node.parent == node_idx:
                raise global_functions.AssetParseError("Malformed node graph (bad parent index)")

            parent_node = JMS.nodes[node.parent]
            if parent_node.child:
                node.sibling = parent_node.child

            else:
                node.sibling = -1

            if node.sibling >= len(JMS.nodes):
                raise global_functions.AssetParseError("Malformed node graph (sibling index out of range)")

            parent_node.child = node_idx
    else:
        for node_idx in range(node_count):
            node = JMS.nodes[node_idx]
            if node.child == -1:
                continue # no child nodes, nothing to update

            if node.child >= len(JMS.nodes) or node.child == node_idx:
                raise global_functions.AssetParseError("Malformed node graph (bad child index)")

            child_node = JMS.nodes[node.child]
            while child_node != None:
                child_node.parent = node_idx
                if child_node.visited:
                    raise global_functions.AssetParseError("Malformed node graph (circular reference)")

                child_node.visited = True
                if child_node.sibling >= len(JMS.nodes):
                    raise global_functions.AssetParseError("Malformed node graph (sibling index out of range)")

                if child_node.sibling != -1:
                    child_node = JMS.nodes[child_node.sibling]

                else:
                    child_node = None

    return JMS
