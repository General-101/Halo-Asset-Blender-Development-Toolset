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

import re
import bpy
import bmesh

from .format import Object
from mathutils import Vector
from ..global_functions import mesh_processing, global_functions

def infer_error_type(binding_type, mtl_diffuse_colors):
    '''
    Infer the type of error based on color used by Tool
    '''
    # thanks to dt192 for this trick!
    color_names = {
        "1.000000 0.000000 0.000000": "red",
        "0.000000 1.000000 0.000000": "green",
        "1.000000 0.500000 0.000000": "orange",
        "0.000000 1.000000 1.000000": "cyan",
        "1.000000 1.000000 0.000000": "yellow",
        "1.000000 0.000000 1.000000": "magenta",
        "0.000000 0.000000 0.000000": "black",
        "0.000000 0.000000 1.000000": "blue",
        # unconfirmed values:
        }

    color_info = " (white)"
    if mtl_diffuse_colors:
        found_colors = set()
        for color in mtl_diffuse_colors:
            color_name = color_names.get(color)
            found_colors.add(color_name)

        color_info = " (" + ", ".join(sorted(found_colors)) + ")"

        if binding_type == "PER_FACE":
            ### WARNING found nearly coplanar surfaces (red and green).
            if "red" in found_colors and "green" in found_colors:
                return "nearly coplanar surfaces" + color_info

            ### WARNING found #1 degenerate triangles.
            ### ERROR found z buffered triangles (red).
            if "red" in found_colors:
                return "degenerate or z-buffered triangle" + color_info

            ### WARNING: portal outside the bsp. [see magenta in error geometry]
            if "magenta" in found_colors:
                return "portal outside BSP" + color_info

        elif binding_type == "PER_VERTEX":
            ### ERROR edge #%d is open (red)
            ### ERROR couldn't update edge #%d (red)
            ### ERROR edge #%d is too short (red)
            # edge has more than four triangles (see red in error geometry)
            if "red" in found_colors:
                return "bad edge" + color_info
                
            ### WARNING unearthed edge (magenta boxed lines)
            ### WARNING found possible T-junction (pink).
            if "magenta" in found_colors:
                return "unearthed edge or T-junction" + color_info

        ### WARNING: a surface clipped to no leaves (see cyan in error geometry)
        if "cyan" in found_colors:
            return "surface clipped to no leaves" + color_info

        ### WARNING: portal doesn't divide any space (it may be coincident with seam sealer?). [see green in error geometry]
        if "green" in found_colors:
            return "portal does not divide space" + color_info

        ### ERROR: portal does not define two closed spaces. (see yellow in error geometry)
        if "yellow" in found_colors:
            return "portal does not define two closed spaces" + color_info

        ### WARNING: found duplicate triangle building connected geometry. YOU SHOULD FIX THIS. (see orange in error geometry)
        ### ERROR couldn't build bsp because of overlapping surfaces (orange)
        if "orange" in found_colors:
            return "duplicate triangle or overlapping surface" + color_info

        #two fog planes intersected in a cluster (see black in error geometry).
        if "black" in found_colors:
            return "two fog planes intersected in a cluster" + color_info

        #degenerate triangle [or triangle with bad uvs] (see blue in error geometry)
        if "blue" in found_colors:
            return "degenerate triangle or UVs" + color_info

    return "unknown" + color_info

def get_material_name(diffuse, error_type):
    mat_name = error_type
    if error_type == "nearly coplanar surfaces (green, red)":
        if diffuse == (1.0, 0.0, 0.0, 1.0):
            mat_name = "nearly coplanar surfaces (red)"

        elif diffuse == (0.0, 1.0, 0.0, 1.0):
            mat_name = "nearly coplanar surfaces (green)"

    return mat_name

def set_object_properties(context, object):
    mesh_processing.deselect_objects(context)
    mesh_processing.select_object(context, object)

    object.show_name = True
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

    mesh_processing.deselect_objects(context)

def build_object_list_old(WRL):
    error_list = []
    object_list = []
    for root_node_idx, root_node in enumerate(WRL.nodes):
        object = Object()
        error = ""
        diffuse_nodes = []
        material_binding = ""
        faces = []
        edges = []
        points = []
        for child_node in root_node.child_nodes:
            if child_node.header == "Coordinate3":
                for content_node in child_node.child_nodes:
                    point_list = []
                    for content in content_node.content.split(","):
                        for set in content.split(" "):
                            value = set.strip()
                            if not global_functions.string_empty_check(value):
                                point_list.append(value)

                    for point_idx in range(int(len(point_list) / 3)):
                        set_idx = 3 * point_idx
                        points.append(Vector((float(point_list[set_idx]), float(point_list[set_idx + 1]), float(point_list[set_idx + 2]))))

            elif child_node.header == "IndexedFaceSet":
                for content_node in child_node.child_nodes:
                    face_list = []
                    for content in content_node.content.split(","):
                        value = content.strip()
                        if not global_functions.string_empty_check(value):
                            face_list.append(value)

                    for face_idx in range(int(len(face_list) / 4)):
                        set_idx = 4 * face_idx
                        v0 = face_list[set_idx]
                        v1 = face_list[set_idx + 1]
                        v2 = face_list[set_idx + 2]
                        v3 = face_list[set_idx + 3]
                        faces.append((int(v0), int(v1), int(v2), int(v3)))

            elif child_node.header == "IndexedLineSet":
                for content_node in child_node.child_nodes:
                    edge_list = []
                    for content in content_node.content.split(","):
                        value = content.strip()
                        if not global_functions.string_empty_check(value):
                            edge_list.append(value)

                    for edge_idx in range(int(len(edge_list) / 3)):
                        set_idx = 3 * edge_idx
                        v0 = edge_list[set_idx]
                        v1 = edge_list[set_idx + 1]
                        v2 = edge_list[set_idx + 2]
                        edges.append((int(v0), int(v1), int(v2)))

            elif child_node.header == "MaterialBinding":
                value = child_node.content.split(" ")[1]
                material_binding = value

            elif child_node.header == "Material":
                for content_node in child_node.child_nodes:
                    if content_node.header == "diffuseColor":
                        for content in content_node.content.split(","):
                            value = content.strip()
                            if not global_functions.string_empty_check(value):
                                diffuse_nodes.append(value)

        error = infer_error_type(material_binding, diffuse_nodes)
        if not error in error_list:
            error_list.append(error)

        object.error = error
        object.diffuse_nodes = diffuse_nodes
        object.material_binding = material_binding
        object.faces = faces
        object.edges = edges
        object.points = points
        object_list.append(object)

    return error_list, object_list

def build_object_list_new(WRL):
    error_list = []
    object_list = []
    for root_node_idx, root_node in enumerate(WRL.nodes):
        object = Object()
        error = ""
        type = ""
        diffuse_nodes = []
        material_binding = ""
        faces = []
        edges = []
        points = []
        for child_node in root_node.child_nodes:
            geometry_header_list = child_node.header.split()
            error = re.findall(r'"([^"]*)"', child_node.header)[0]
            type = geometry_header_list[-1]
            material_binding = bool(child_node.content.split(" ")[1])
            for content_node in child_node.child_nodes:
                if content_node.header == "coord Coordinate":
                    for value_node in content_node.child_nodes:
                        if value_node.header == "point":
                            for point_idx in range(int(len(value_node.content) / 3)):
                                set_idx = 3 * point_idx
                                points.append(Vector((float(value_node.content[set_idx]), float(value_node.content[set_idx + 1]), float(value_node.content[set_idx + 2]))))

                        elif value_node.header == "coordIndex":
                            if type == "IndexedFaceSet":
                                for face_idx in range(int(len(value_node.content) / 4)):
                                    set_idx = 4 * face_idx
                                    v0 = value_node.content[set_idx]
                                    v1 = value_node.content[set_idx + 1]
                                    v2 = value_node.content[set_idx + 2]
                                    v3 = value_node.content[set_idx + 3]
                                    faces.append((int(v0), int(v1), int(v2), int(v3)))

                            elif type == "IndexedLineSet":
                                for edge_idx in range(int(len(value_node.content) / 3)):
                                    set_idx = 3 * edge_idx
                                    v0 = value_node.content[set_idx]
                                    v1 = value_node.content[set_idx + 1]
                                    v2 = value_node.content[set_idx + 2]
                                    edges.append((int(v0), int(v1), int(v2)))

                elif content_node.header == "color Color":
                    for value_node in content_node.child_nodes:
                        for value_idx in range(int(len(value_node.content) / 3)):
                            set_idx = 3 * value_idx
                            diffuse_nodes.append("%s %s %s" % (value_node.content[set_idx], value_node.content[set_idx + 1], value_node.content[set_idx + 2]))

        if not error in error_list:
            error_list.append(error)

        object.error = error
        object.diffuse_nodes = diffuse_nodes
        object.material_binding = material_binding
        object.faces = faces
        object.edges = edges
        object.points = points
        object_list.append(object)

    return error_list, object_list

def build_scene(context, WRL, report):
    if WRL.version == 1.0:
        error_list, object_list = build_object_list_old(WRL)

    elif WRL.version == 2.0: 
        error_list, object_list = build_object_list_new(WRL)

    for error in error_list:
        face_idx = 0
        mesh = bpy.data.meshes.new(error)
        object_mesh = bpy.data.objects.new(error, mesh)
        context.collection.objects.link(object_mesh)
        bm = bmesh.new()
        for object in  object_list:
            if object.error == error:
                if len(object.edges) > 0:
                    for edge in object.edges:
                        vert_list = []
                        if not edge[0] == -1:
                            vert_list.append(bm.verts.new(object.points[edge[0]]))

                        if not edge[1] == -1:
                            vert_list.append(bm.verts.new(object.points[edge[1]]))

                        if not edge[2] == -1:
                            vert_list.append(bm.verts.new(object.points[edge[2]]))

                        bm.edges.new(vert_list)

                    bm.edges.ensure_lookup_table()

                    for object_edge_idx, edge in enumerate(object.edges):
                        color = object.diffuse_nodes[object_edge_idx]
                        r, g, b = color.split()
                        diffuse = (float(r), float(g), float(b), 1.0)
                        mat_name = get_material_name(diffuse, object.error)
                        error_mat = bpy.data.materials.get(mat_name)
                        if error_mat is None:
                            error_mat = bpy.data.materials.new(name=mat_name)
                            error_mat.diffuse_color = diffuse
                            object_mesh.data.materials.append(error_mat)

                        else:
                            if error_mat not in list(object_mesh.data.materials):
                                object_mesh.data.materials.append(error_mat)

                if len(object.faces) > 0:
                    for face in object.faces:
                        vert_list = []
                        if not face[0] == -1:
                            vert_list.append(bm.verts.new(object.points[face[0]]))

                        if not face[1] == -1:
                            vert_list.append(bm.verts.new(object.points[face[1]]))

                        if not face[2] == -1:
                            vert_list.append(bm.verts.new(object.points[face[2]]))

                        if not face[3] == -1:
                            vert_list.append(bm.verts.new(object.points[face[3]]))

                        bm.faces.new(vert_list)

                    bm.faces.ensure_lookup_table()

                    for object_face_idx, face in enumerate(object.faces):
                        color = object.diffuse_nodes[object_face_idx]
                        r, g, b = color.split()
                        diffuse = (float(r), float(g), float(b), 1.0)
                        mat_name = get_material_name(diffuse, object.error)
                        error_mat = bpy.data.materials.get(mat_name)
                        if error_mat is None:
                            error_mat = bpy.data.materials.new(name=mat_name)
                            error_mat.diffuse_color = diffuse
                            object_mesh.data.materials.append(error_mat)

                        else:
                            if error_mat not in list(object_mesh.data.materials):
                                object_mesh.data.materials.append(error_mat)

                        bm_object_mesh_materials = list(object_mesh.data.materials)
                        bm.faces[face_idx].material_index = bm_object_mesh_materials.index(error_mat)

                        face_idx += 1

        bm.to_mesh(mesh)
        bm.free()
        set_object_properties(context, object_mesh)
