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

import os

from .process_scene import process_scene
from ..global_functions import global_functions

def build_asset(context, blend_scene, filepath, version, game_version, generate_checksum, fix_rotations, folder_structure, folder_type, model_type, jmi, permutation_ce, level_of_detail_ce, custom_scale, report):
    JMS = process_scene(version, game_version, generate_checksum, fix_rotations, model_type, blend_scene, custom_scale)

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
            '\n%s' % (JMS.node_checksum)
            )

        if version >= 8203 and version <= 8204:
            file.write(
                '\n;' +
                '\n;###Frames###'
                )

        file.write(
            '\n%s' % (len(JMS.nodes))
            )

    if version >= 8205:
        file.write(
            '\n;### NODES ###' +
            '\n%s' % (len(JMS.nodes)) +
            '\n;\t<name>' +
            '\n;\t<parent node index>' +
            '\n;\t<default rotation <i,j,k,w>>' +
            '\n;\t<default translation <x,y,z>>\n'
        )

    for idx, node in enumerate(JMS.nodes):
        transform = JMS.transforms[idx]
        if version >= 8205:
            file.write(
                '\n;NODE %s' % (idx) +
                '\n%s' % (node.name) +
                '\n%s' % (node.parent) +
                decimal_4 % (transform.rotation) +
                decimal_3 % (transform.translation) +
                '\n'
            )

        else:
            file.write(
                '\n%s' % (node.name) +
                '\n%s' % (node.child) +
                '\n%s' % (node.sibling) +
                decimal_4 % (transform.rotation) +
                decimal_3 % (transform.translation)
            )

    if version >= 8205:
        file.write(
            '\n;### MATERIALS ###' +
            '\n%s' % (len(JMS.materials)) +
            '\n;\t<name>' +
            '\n;\t<(Material Slot Index) LOD Permutation Region>\n'
        )

    else:
        if version >= 8202 and version <= 8204:
            file.write(
                '\n;' +
                '\n;###Materials###'
                )

        file.write(
            '\n%s' % (len(JMS.materials))
        )

    for idx, material in enumerate(JMS.materials):
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
                if version >= 8202 and version <= 8204:
                    file.write('\n%s' % (material.texture_path))

                file.write('\n%s' % (material_definition))

    if version >= 8205:
        file.write(
            '\n;### MARKERS ###' +
            '\n%s' % (len(JMS.markers)) +
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
            '\n%s' % (len(JMS.markers))
        )

    for idx, marker in enumerate(JMS.markers):
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
            file.write(decimal_1 % (marker.radius))

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
                '\n%s' % (len(JMS.xref_instances)) +
                '\n;\t<path to asset file>' +
                '\n;\t<name>\n'
            )

        elif version == 8205:
            file.write(
                '\n;### INSTANCE XREF PATHS ###' +
                '\n%s' % (len(JMS.xref_instances)) +
                '\n;\t<name>\n'
            )

        elif version >= 8203 and version <= 8204:
            file.write(
                '\n;' +
                '\n;###Instance xref paths###' +
                '\n%s' % (len(JMS.xref_instances))
                )

        for idx, xref_instance in enumerate(JMS.xref_instances):
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
                '\n%s' % (len(JMS.xref_markers)) +
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
                '\n%s' % (len(JMS.xref_markers))
                )

        for idx, xref_marker in enumerate(JMS.xref_markers):
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
            '\n%s' % (len(JMS.regions))
        )

        for region in JMS.regions:
            file.write(
                '\n%s' % (region.name)
            )

    if version >= 8205:
        file.write(
            '\n;### VERTICES ###' +
            '\n%s' % (len(JMS.vertices)) +
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
            '\n%s' % (len(JMS.vertices))
        )

    for idx, vertex in enumerate(JMS.vertices):
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
                if version >= 8202 and version <= 8204:
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
            '\n%s' % (len(JMS.triangles)) +
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
            '\n%s' % (len(JMS.triangles))
        )

    for idx, triangle in enumerate(JMS.triangles):
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
            '\n%s' % (len(JMS.spheres)) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<radius>\n'
        )

        #write sphere
        for idx, sphere in enumerate(JMS.spheres):
            file.write(
                '\n;SPHERE %s' % (idx) +
                '\n%s' % (sphere.name) +
                '\n%s' % (sphere.parent_index) +
                '\n%s' % (sphere.material_index) +
                decimal_4 % (sphere.rotation) +
                decimal_3 % (sphere.translation) +
                decimal_1 % (sphere.radius) +
                '\n'
            )

        #write boxes
        file.write(
            '\n;### BOXES ###' +
            '\n%s' % (len(JMS.boxes)) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<width (x)>' +
            '\n;\t<length (y)>' +
            '\n;\t<height (z)>\n'
        )

        for idx, box in enumerate(JMS.boxes):
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
            '\n%s' % (len(JMS.capsules)) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<height>' +
            '\n;\t<radius>\n'
             )

        for idx, capsule in enumerate(JMS.capsules):
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
            '\n%s' % (len(JMS.convex_shapes)) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<vertex count>' +
            '\n;\t<...vertices>\n'
        )

        for idx, convex_shape in enumerate(JMS.convex_shapes):
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
            '\n%s' % (len(JMS.ragdolls)) +
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

        for idx, ragdoll in enumerate(JMS.ragdolls):
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
            '\n%s' % (len(JMS.hinges)) +
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

        for idx, hinge in enumerate(JMS.hinges):
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
                '\n%s' % (len(JMS.car_wheels)) +
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

            for idx, car_wheel in enumerate(JMS.car_wheels):
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
                '\n%s' % (len(JMS.point_to_points)) +
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

            for idx, point_to_point in enumerate(JMS.point_to_points):
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
                '\n%s' % (len(JMS.prismatics)) +
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

            for idx, prismatic in enumerate(JMS.prismatics):
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
                '\n%s' % (len(JMS.bounding_spheres)) +
                '\n;\t<translation <x,y,z>>' +
                '\n;\t<radius>\n'
            )

            for idx, bounding_sphere in enumerate(JMS.bounding_spheres):
                file.write(
                    '\n;BOUNDING SPHERE %s' % (idx) +
                    decimal_3 % (bounding_sphere.translation) +
                    decimal_1 % (bounding_sphere.radius) +
                    '\n'
                )

        if version >= 8212:
            #write skylight
            file.write(
                '\n;### SKYLIGHT ###' +
                '\n%s' % (len(JMS.skylights)) +
                '\n;\t<direction <x,y,z>>' +
                '\n;\t<radiant intensity <x,y,z>>' +
                '\n;\t<solid angle>\n'
            )

            for idx, light in enumerate(JMS.skylights):
                file.write(
                    '\n;SKYLIGHT %s' % (idx) +
                    decimal_3 % light.direction +
                    decimal_3 % light.radiant_intensity +
                    decimal_1 % light.solid_angle +
                    '\n'
                )
    report({'INFO'}, "Export completed successfully")
    file.close()
