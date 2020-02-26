bl_info = {
    "name": "Blend2Halo2 JMS",
    "author": "Cyboryxmen, Modified by Fulsy + MosesofEgypt + General_101",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "File > Export",
    "description": "Import-Export Halo 2/CE Jointed Model Skeleton File (.jms)",
    "wiki_url": "https://num0005.github.io/h2codez_docs/w/H2Tool/Render_Model/render_model.html",
    "category": "Import-Export"}

import bpy
import bmesh
import math

from math import ceil
from decimal import *
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty

class JmsVertex:
    node_influence_count = '0'
    node0 = '-1'
    node1 = '-1'
    node2 = '-1'
    node3 = '-1'
    node0_weight = '0.0000000000'
    node1_weight = '0.0000000000'
    node2_weight = '0.0000000000'
    node3_weight = '0.0000000000'
    pos = None
    norm = None
    uv = None

class JmsTriangle:
    v0 = 0
    v1 = 0
    v2 = 0
    region = 0
    material = 0

def triangulate_object(obj):
    me = obj.data
    # Get a BMesh representation
    bm = bmesh.new()
    bm.from_mesh(me)

    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')

    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(me)
    bm.free()

def unhide_all_collections():
    for collection_viewport in bpy.context.view_layer.layer_collection.children:
        collection_viewport.hide_viewport = False

    for collection_hide in bpy.data.collections:
        collection_hide.hide_select = False
        collection_hide.hide_viewport = False
        collection_hide.hide_render = False

def unhide_all_objects():
    context = bpy.context
    for obj in context.view_layer.objects:
        if obj.hide_set:
            obj.hide_set(False)

        if obj.hide_select:
            obj.hide_select = False

        if obj.hide_viewport:
            obj.hide_viewport = False

        if obj.hide_render:
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

def export_jms(context, filepath, report, encoding, extension, jms_version, game_version, triangulate_faces):

    unhide_all_collections()
    unhide_all_objects()
    file = open(filepath + extension, 'w', encoding='%s' % encoding)

    object_list = list(bpy.context.scene.objects)
    node_list = []
    layer_count = []
    root_list = []
    children_list = []
    reversed_children_list = []
    joined_list = []
    reversed_joined_list = []
    sort_list = []
    reversed_sort_list = []
    keyframes = []
    armature = []
    armature_count = 0
    material_list = []
    marker_list = []
    geometry_list = []
    sphere_list = []
    box_list = []
    capsule_list = []
    convex_shape_list = []
    region_list = []
    permutation_list = []
    triangles = []
    vertices = []
    vertexgroups = []

    bpy.context.view_layer.objects.active = object_list[0]
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    for obj in object_list:
        if obj.type == 'ARMATURE':
            armature_count += 1
            armature = obj
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            node_list = list(obj.data.bones)

        elif obj.name[0:2].lower() == 'b_' or obj.name[0:5].lower() == "frame":
            node_list.append(obj)

        elif obj.name[0:1].lower() == '#':
            marker_list.append(obj)
            if not obj.jms.Region in region_list:
                if obj.jms.Region == " " and not 'unnamed' in region_list:
                    region_list.append('unnamed')

                if not obj.jms.Region == " ":
                    region_list.append(obj.jms.Region)

            if not obj.jms.Permutation in permutation_list:
                if obj.jms.Permutation == " " and not 'unnamed' in permutation_list:
                    permutation_list.append('unnamed')

                if not obj.jms.Permutation == " ":
                    permutation_list.append(obj.jms.Permutation)

        elif obj.name[0:1].lower() == '$':
            if obj.jms.Object_Type == 'SPHERE':
                sphere_list.append(obj)

            if obj.jms.Object_Type == 'BOX':
                box_list.append(obj)

            if obj.jms.Object_Type == 'CAPSULES':
                capsule_list.append(obj)

            if obj.jms.Object_Type == 'CONVEX SHAPES':
                convex_shape_list.append(obj)

        elif obj.type== 'MESH':
            geometry_list.append(obj)
            if not obj.jms.Region in region_list:
                if obj.jms.Region == " " and not 'unnamed' in region_list:
                    region_list.append('unnamed')

                if not obj.jms.Region == " ":
                    region_list.append(obj.jms.Region)

            if not obj.jms.Permutation in permutation_list:
                if obj.jms.Permutation == " " and not 'unnamed' in permutation_list:
                    permutation_list.append('unnamed')

                if not obj.jms.Permutation == " ":
                    permutation_list.append(obj.jms.Permutation)

        if len(obj.material_slots)!=0:
            for slot in obj.material_slots:
                if slot.material not in material_list:
                    material_list.append(slot.material)

        if armature_count >= 2:
            report({'ERROR'}, "More than one armature object. Please delete all but one.")
            file.close()
            return {'CANCELLED'}

    for node in node_list:
        if node.parent == None:
            layer_count.append(node)

        else:
            if not node.parent.name in layer_count:
                layer_count.append(node.parent.name)

    for layer in layer_count:
        joined_list = root_list + children_list
        reversed_joined_list = root_list + reversed_children_list
        layer_index = layer_count.index(layer)
        if layer_index == 0:
            if armature_count == 0:
                root_list.append(bpy.data.objects[layer_count[0]])

            else:
                root_list.append(armature.data.bones[0])

        else:
            for node in node_list:
                if armature_count == 0:
                    if node.parent != None:
                        if bpy.data.objects[node.parent.name] in joined_list and not node in children_list:
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

    version = 8197 + int(jms_version)
    node_checksum = 0
    node_count = len(node_list)
    material_count = len(material_list)
    marker_count = len(marker_list)
    region_count = len(region_list)

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
        if find_child_node == None:
            first_child_node = -1

        else:
            first_child_node = joined_list.index(find_child_node)

        if find_sibling_node == None:
            first_sibling_node = -1

        else:
            first_sibling_node = joined_list.index(find_sibling_node)

        if version >= 8205:
            if node.parent == None:
                parent_node = -1

            else:
                parent_node = joined_list.index(node.parent)

        else:
            if node.parent == None:
                parent_node = -1

            else:
                parent_node = joined_list.index(node)

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
        if version >= 8205:
            quat = bone_matrix.to_quaternion()

        else:
            quat = bone_matrix.to_quaternion().inverted()

        quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
        quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
        quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
        quat_w = Decimal(quat[0]).quantize(Decimal('1.0000000000'))
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
        '\n;\t<???/LOD/Permutation/Region>\n'
        )

    else:
        file.write(
            '\n%s' % (material_count)
            )

    for material in material_list:
        if obj.jms.Permutation == " ":
            Permutation = 'Default'

        else:
            Permutation = obj.jms.Permutation

        if obj.jms.Region == " ":
            Region = 'Default'

        else:
            Region = obj.jms.Region

        if version >= 8205:
            file.write(
            '\n;MATERIAL %s' % (material_list.index(material)) +
            '\n%s' % material.name +
            '\n%s %s\n' % (Permutation, Region)
            )

        else:
            if game_version == 'haloce':
                file.write(
                    '\n%s' % (material.name) +
                    '\n%s' % ('<none>')
                    )

            else:
                file.write(
                    '\n%s' % (material.name) +
                    '\n%s %s' % (Permutation, Region)
                    )

                if version >= 8205:
                    file.write(
                        '\n'
                        )

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
        name = marker.name.replace(' ', '')[+1:]
        fixed_name = name.split('.')[0]
        if obj.jms.Region == " ":
            region = region_list.index('unnamed')

        else:
            region = region_list.index(obj.jms.Region)

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
            '\n0' +
            '\n;\t<path to .MAX file>' +
            '\n;\t<name>\n'
            )

        #write instance markers
        file.write(
            '\n;### INSTANCE MARKERS ###' +
            '\n0' +
            '\n;\t<name>' +
            '\n;\t<unique identifier>' +
            '\n;\t<path index>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>\n'
            )

    #write vertices
    for geometry in geometry_list:
        if triangulate_faces:
            triangulate_object(geometry)

        c = 0
        vertexgroups.clear()
        for groups in geometry.vertex_groups:
            vertexgroups.append(geometry.vertex_groups[c].name)
            c = c + 1

        matrix = geometry.matrix_world

        uv_layer = geometry.data.uv_layers.active.data
        mesh_loops = geometry.data.loops
        mesh_verts = geometry.data.vertices

        for face in geometry.data.polygons:
            jms_triangle = JmsTriangle()
            triangles.append(jms_triangle)

            if obj.jms.Region == " ":
                region = region_list.index('unnamed')

            else:
                region = region_list.index(obj.jms.Region)

            jms_triangle.v0 = len(vertices)
            jms_triangle.v1 = len(vertices) + 1
            jms_triangle.v2 = len(vertices) + 2
            jms_triangle.region = region
            if len(geometry.material_slots)!=0:
                jms_triangle.material = material_list.index(geometry.data.materials[face.material_index])

            else:
                jms_triangle.material = -1

            for loop_index in face.loop_indices:
                vert = mesh_verts[mesh_loops[loop_index].vertex_index]
                uv = uv_layer[loop_index].uv

                jms_vertex = JmsVertex()
                vertices.append(jms_vertex)

                pos  = matrix@vert.co
                norm = matrix@(vert.co + vert.normal) - pos

                jms_vertex.pos = pos
                jms_vertex.norm = norm
                jms_vertex.uv = uv
                if len(vert.groups) != 0:
                    value = len(vert.groups)
                    if value > 4:
                        value = 4

                    jms_vertex.node_influence_count = value
                    for n in range(len(vert.groups)):
                        vertex_group = vert.groups[n].group
                        object_vertex_group = vertexgroups[vertex_group]
                        armature_obj = armature.data.bones[object_vertex_group]
                        if n == 0:
                            jms_vertex.node0 = joined_list.index(armature_obj)
                            jms_vertex.node0_weight = '%0.6f' % vert.groups[0].weight

                        if n == 1:
                            jms_vertex.node1 = joined_list.index(armature_obj)
                            jms_vertex.node1_weight = '%0.6f' % vert.groups[1].weight

                        if n == 2:
                            jms_vertex.node2 = joined_list.index(armature_obj)
                            jms_vertex.node2_weight = '%0.10f' % vert.groups[2].weight

                        if n == 3:
                            jms_vertex.node3 = joined_list.index(armature_obj)
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

        tex_coord_count = 1

        tex_u = Decimal(uv[0]).quantize(Decimal('1.000000'))
        tex_v = Decimal(uv[1]).quantize(Decimal('1.000000'))
        tex_w = 0

        if version >= 8205:
            if int(jms_vertex.node_influence_count) == 1:
                file.write(
                    '\n;VERTEX %s' % (vertices.index(jms_vertex)) +
                    decimal_3 % (pos_x, pos_y, pos_z) +
                    decimal_3 % (norm_i, norm_j, norm_k) +
                    '\n%s' % (jms_vertex.node_influence_count) +
                    '\n%s' % (jms_vertex.node0) +
                    decimal_1 % (float(jms_vertex.node0_weight)) +
                    '\n%s' % (tex_coord_count) +
                    decimal_2 % (tex_u, tex_v) +
                    '\n'
                    )

            if int(jms_vertex.node_influence_count) == 2:
                file.write(
                    '\n;VERTEX %s' % (vertices.index(jms_vertex)) +
                    decimal_3 % (pos_x, pos_y, pos_z) +
                    decimal_3 % (norm_i, norm_j, norm_k) +
                    '\n%s' % (jms_vertex.node_influence_count) +
                    '\n%s' % (jms_vertex.node0) +
                    decimal_1 % (float(jms_vertex.node0_weight)) +
                    '\n%s' % (jms_vertex.node1) +
                    decimal_1 % (float(jms_vertex.node1_weight)) +
                    '\n%s' % (tex_coord_count) +
                    decimal_2 % (tex_u, tex_v) +
                    '\n'
                    )

            if int(jms_vertex.node_influence_count) == 3:
                file.write(
                    '\n;VERTEX %s' % (vertices.index(jms_vertex)) +
                    decimal_3 % (pos_x, pos_y, pos_z) +
                    decimal_3 % (norm_i, norm_j, norm_k) +
                    '\n%s' % (jms_vertex.node_influence_count) +
                    '\n%s' % (jms_vertex.node0) +
                    decimal_1 % (float(jms_vertex.node0_weight)) +
                    '\n%s' % (jms_vertex.node1) +
                    decimal_1 % (float(jms_vertex.node1_weight)) +
                    '\n%s' % (jms_vertex.node2) +
                    decimal_1 % (float(jms_vertex.node2_weight)) +
                    '\n%s' % (tex_coord_count) +
                    decimal_2 % (tex_u, tex_v) +
                    '\n'
                    )

            if int(jms_vertex.node_influence_count) == 4:
                file.write(
                    '\n;VERTEX %s' % (vertices.index(jms_vertex)) +
                    decimal_3 % (pos_x, pos_y, pos_z) +
                    decimal_3 % (norm_i, norm_j, norm_k) +
                    '\n%s' % (jms_vertex.node_influence_count) +
                    '\n%s' % (jms_vertex.node0) +
                    decimal_1 % (float(jms_vertex.node0_weight)) +
                    '\n%s' % (jms_vertex.node1) +
                    decimal_1 % (float(jms_vertex.node1_weight)) +
                    '\n%s' % (jms_vertex.node2) +
                    decimal_1 % (float(jms_vertex.node2_weight)) +
                    '\n%s' % (jms_vertex.node3) +
                    decimal_1 % (float(jms_vertex.node3_weight)) +
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
            name = spheres.name.replace(' ', '')[+1:]
            sphere_materials = spheres.data.materials
            if len(sphere_materials) > 0:
                sphere_material_index = material_list.index(sphere_materials[0])

            else:
                sphere_material_index = -1

            parent_index = -1
            if armature_count == 0:
                if spheres.parent:
                    parent_bone = bpy.data.objects[spheres.parent.name]
                    parent_index = joined_list.index(parent_bone)

            else:
                if spheres.parent_bone:
                    parent_bone = armature.data.bones[spheres.parent_bone]
                    parent_index = joined_list.index(parent_bone)

            radius = abs(spheres.dimensions[0]/2)
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
            name = boxes.name.replace(' ', '')[+1:]
            box_materials = boxes.data.materials
            if len(box_materials) > 0:
                boxes_material_index = material_list.index(box_materials[0])

            else:
                boxes_material_index = -1

            parent_index = -1
            if armature_count == 0:
                if boxes.parent:
                    parent_bone = bpy.data.objects[boxes.parent.name]
                    parent_index = joined_list.index(parent_bone)

            else:
                if boxes.parent_bone:
                    parent_bone = armature.data.bones[boxes.parent_bone]
                    parent_index = joined_list.index(parent_bone)

            dimension_x = abs(boxes.dimensions[0]/2)
            dimension_y = abs(boxes.dimensions[1]/2)
            dimension_z = abs(boxes.dimensions[2]/2)
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
            name = capsule.name.replace(' ', '')[+1:]
            capsule_materials = capsule.data.materials
            if len(capsule_materials) > 0:
                capsule_material_index = material_list.index(capsule_materials[0])

            else:
                capsule_material_index = -1

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
            scale_x = obj.dimensions[0]
            scale_y = obj.dimensions[1]
            scale_z = obj.dimensions[2]

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
            name = convex_shape.name.replace(' ', '')[+1:]
            convex_shape_materials = convex_shape.data.materials
            if len(convex_shape_materials) > 0:
                convex_shape_material_index = material_list.index(convex_shape_materials[0])

            else:
                convex_shape_material_index = -1

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
                convex_matrix = parent_bone.matrix_local.inverted() @ convex_shape.matrix_local

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

        if version > 8209:
            #write rag dolls
            file.write(
                '\n;### RAGDOLLS ###' +
                '\n0' +
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
                '\n0' +
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

            #write car wheel
            file.write(
                '\n;### CAR WHEEL ###' +
                '\n0' +
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
                '\n0' +
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
                '\n0' +
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

        else:
            #write rag dolls
            file.write(
                '\n;### RAGDOLLS ###' +
                '\n0' +
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
                '\n0' +
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

        #write bounding sphere
        file.write(
            '\n;### BOUNDING SPHERE ###' +
            '\n0' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<radius>\n'
             )

    file.close()
    return {'FINISHED'}

class JMS_ObjectProps(Panel):
    bl_label = "JMS Object Properties"
    bl_idname = "JMS_PT_RegionPermutationPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        obj = context.object
        jms = obj.jms

        row = layout.row()
        row.prop(jms, "Region")

        row = layout.row()
        row.prop(jms, "Permutation")

        row = layout.row()
        row.prop(jms, "Object_Type")

class JMS_ObjectPropertiesGroup(PropertyGroup):
    Region : StringProperty(
        name = "Region",
        default = " ",
        description = "Set region name."
        )

    Permutation : StringProperty(
        name = "Permutation",
        default = " ",
        description = "Set permutation name."
        )

    Object_Type : EnumProperty(
        name="Object Type",
        description="Select object type to write mesh as",
        default = "CONVEX SHAPES",
        items=[ ('SPHERE', "Sphere", ""),
                ('BOX', "Box", ""),
                ('CAPSULES', "Pill", ""),
                ('CONVEX SHAPES', "Convex Shape", ""),
               ]
        )

class ExportJMS(Operator, ExportHelper):
    """Write a JMS file"""
    bl_idname = "export_jms.export"
    bl_label = "Export JMS"

    filename_ext = ''

    encoding: EnumProperty(
        name="Encoding:",
        description="What encoding to use for the model file",
        default="UTF-16LE",
        items=[ ('utf_8', "UTF-8", "For CE"),
                ('UTF-16LE', "UTF-16", "For H2"),
               ]
        )

    extension: EnumProperty(
        name="Extension:",
        description="What extension to use for the model file",
        items=[ ('.JMS', "JMS", "Jointed Model Skeleton CE/H2"),
                ('.JMP', "JMP", "Jointed Model Physics CE"),
               ]
        )

    jms_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="3",
        items=[ ('0', "8197", "CE/H2 Non-functional"),
                ('1', "8198", "CE/H2 Non-functional"),
                ('2', "8199", "CE/H2 Non-functional"),
                ('3', "8200", "CE/H2"),
                ('4', "8201", "H2"),
                ('5', "8202", "H2"),
                ('6', "8203", "H2"),
                ('7', "8204", "H2"),
                ('8', "8205", "H2"),
                ('9', "8206", "H2"),
                ('10', "8207", "H2"),
                ('11', "8208", "H2"),
                ('12', "8209", "H2"),
                ('13', "8210", "H2"),
               ]
        )

    game_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="halo2",
        items=[ ('haloce', "Halo CE", "Match Blitzkrieg for CE importing"),
                ('halo2', "Halo 2", "Changed the texture path into a region/permutation definition to match Halo 2's JMS parser"),
               ]
        )

    triangulate_faces: BoolProperty(
        name ="Triangulate faces",
        description = "Automatically triangulate all faces (recommended)",
        default = True,
        )

    filter_glob: StringProperty(
        default="*.jms;*.jmp",
        options={'HIDDEN'},
        )

    def execute(self, context):
        return export_jms(context, self.filepath, self.report, self.encoding, self.extension, self.jms_version, self.game_version, self.triangulate_faces)

classesjms = (
    JMS_ObjectPropertiesGroup,
    JMS_ObjectProps,
    ExportJMS
)

def menu_func_export(self, context):
    self.layout.operator(ExportJMS.bl_idname, text="Halo Jointed Model Skeleton (.jms)")

def register():
    for clsjms in classesjms:
        bpy.utils.register_class(clsjms)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.Object.jms = PointerProperty(type=JMS_ObjectPropertiesGroup, name="JMS Object Properties", description="JMS Object properties")

def unregister():
    for clsjms in reversed(classesjms):
        bpy.utils.unregister_class(clsjms)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    del bpy.types.Object.jms

if __name__ == '__main__':
    register()
