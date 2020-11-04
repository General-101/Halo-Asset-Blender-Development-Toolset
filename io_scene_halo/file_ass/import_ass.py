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
import sys
import math
import bmesh
import random
import traceback

from mathutils import Vector, Quaternion, Matrix
from io_scene_halo.global_functions import global_functions

class ASSAsset(global_functions.HaloAsset):
    class Transform:
        def __init__(self, rotation, vector, scale):
            self.rotation = rotation
            self.vector = vector
            self.scale = scale

    class Material:
        def __init__(self, name, material_effect):
            self.name = name
            self.material_effect = material_effect

    class Object:
        def __init__(self, geo_class, xref_filepath, xref_objectname, material_index=-1, radius=0.0, extents=None, height=0.0, vertices=None, triangles=None, node_index_list=None):
            self.geo_class = geo_class
            self.xref_filepath = xref_filepath
            self.xref_objectname = xref_objectname
            self.material_index = material_index
            self.radius = radius
            self.extents = extents
            self.height = height
            self.vertices = vertices
            self.triangles = triangles
            self.node_index_list = node_index_list

    class Vertex:
        def __init__(self, node_influence_count=0, node_set=None, translation=None, normal=None, uv_set=None):
            self.node_influence_count = node_influence_count
            self.node_set = node_set
            self.translation = translation
            self.normal = normal
            self.uv_set = uv_set

    class Triangle:
        def __init__(self, material_index=-1, v0=-1, v1=-1, v2=-1):
            self.material_index = material_index
            self.v0 = v0
            self.v1 = v1
            self.v2 = v2

    class Instance:
        def __init__(self, name, object_index=-1, unique_id=-1, parent_id=-1, inheritance_flag=0, local_transform=None, pivot_transform=None):
            self.name = name
            self.object_index = object_index
            self.unique_id = unique_id
            self.parent_id = parent_id
            self.inheritance_flag = inheritance_flag
            self.local_transform = local_transform
            self.pivot_transform = pivot_transform

    def are_quaternions_inverted(self):
        return self.version < 1

    def next_transform(self, version):
        rotation = self.next_quaternion()
        translation = self.next_vector()
        if version >= 2:
            scale = float(self.next())
        else:
            scale = self.next_vector()
        return ASSAsset.Transform(rotation, translation, scale)

    def __init__(self, filepath):
        super().__init__(filepath)
        self.version = int(self.next())
        version_list = [1, 2, 3, 4, 5, 6, 7]
        if not self.version in version_list:
            raise global_functions.AssetParseError("Importer does not support this ASS version")

        self.skip(4) # skip header
        self.materials = []
        self.objects = []
        self.instances = []
        material_count = int(self.next())
        for material in range(material_count):
            name = self.next().strip('\"')
            material_effect = self.next().strip('\"')
            self.materials.append(ASSAsset.Material(name, material_effect))

        object_count = int(self.next())
        for object in range(object_count):
            vertices = []
            node_index_list = []
            triangles = []
            geo_class = self.next().strip('\"')
            xref_path = self.next().strip('\"')
            xref_name = self.next().strip('\"')
            material_index = -1
            radius = 2
            extents = [1.0, 1.0, 1.0]
            height = 1
            if geo_class == 'SPHERE':
                material_index = int(self.next())
                radius = float(self.next())

            elif geo_class == 'BOX':
                material_index = int(self.next())
                extents = self.next_vector()

            elif geo_class == 'PILL':
                material_index = int(self.next())
                height = float(self.next())
                radius = float(self.next())

            elif geo_class == 'MESH':
                vert_count = int(self.next())
                for vert in range(vert_count):
                    node_set = []
                    uv_set = []
                    translation = self.next_vector()
                    normal = self.next_vector()
                    node_influence_count = int(self.next())
                    for node in range(node_influence_count):
                        node_index = int(self.next())
                        if not node_index in node_index_list:
                            node_index_list.append(node_index)

                        node_weight = float(self.next())
                        node_set.append([node_index, node_weight])

                    uv_count = int(self.next())
                    for uv in range(uv_count):
                        tex_u = float(self.next())
                        tex_v = float(self.next())
                        uv_set.append([tex_u, tex_v])

                    vertices.append(ASSAsset.Vertex(node_influence_count, node_set, translation, normal, uv_set))

                triangle_count = int(self.next())
                for triangle in range(triangle_count):
                    material_index = int(self.next())
                    v0 = int(self.next())
                    v1 = int(self.next())
                    v2 = int(self.next())

                    triangles.append(ASSAsset.Triangle(material_index, v0, v1, v2))

            self.objects.append(ASSAsset.Object(geo_class, xref_path, xref_name, material_index, radius, extents, height, vertices, triangles, node_index_list))

        name_list = []
        instance_count = int(self.next())
        for instance in range(instance_count):
            object_index = int(self.next())
            object_element = self.objects[object_index]
            bone_influence_count = 0
            if not object_index == -1:
                bone_influence_count = len(object_element.node_index_list)

            name = self.next().strip('\"')
            if name in name_list:
                true_name = '%s_%s' % (name, instance)
            else:
                true_name = name
            name_list.append(name)
            unique_id = int(self.next())
            parent_id = int(self.next())
            inheritance_flag = int(self.next())
            local_transform = self.next_transform(self.version)
            pivot_transform = self.next_transform(self.version)
            if bone_influence_count > 0:
                self.skip(bone_influence_count)

            if not object_index == -1 and not unique_id == -1 and not parent_id == -1:
                self.instances.append(ASSAsset.Instance(true_name, object_index, unique_id, parent_id, inheritance_flag, local_transform, pivot_transform))

        if self.left() != 0: # is something wrong with the parser?
            raise RuntimeError("%s elements left after parse end" % self.left())

def load_file(context, filepath, report):
    try:
        ass_file = ASSAsset(filepath)
    except global_functions.AssetParseError as parse_error:
        info = sys.exc_info()
        traceback.print_exception(info[0], info[1], info[2])
        report({'ERROR'}, "Bad file: {0}".format(parse_error))
        return {'CANCELLED'}
    except:
        info = sys.exc_info()
        traceback.print_exception(info[0], info[1], info[2])
        report({'ERROR'}, "Internal error: {1}({0})".format(info[1], info[0]))
        return {'CANCELLED'}

    collection = bpy.context.collection
    view_layer = bpy.context.view_layer

    if view_layer.objects.active:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    sorted_parent_id = []
    for idx, instance in enumerate(ass_file.instances):
        sorted_parent_id.append((idx, instance.parent_id))

        mesh = bpy.data.meshes.new(instance.name)
        object_mesh = bpy.data.objects.new(instance.name, mesh)
        collection.objects.link(object_mesh)
        object_index = instance.object_index
        object_element = ass_file.objects[object_index]
        geo_class = object_element.geo_class
        object_material_index = object_element.material_index
        if not object_material_index == -1:
            mat = ass_file.materials[object_material_index]
            material_name = mat.name
            material_effect = mat.material_effect
            mat = bpy.data.materials.get(material_name)
            if mat is None:
                mat = bpy.data.materials.new(name=material_name)

            if object_mesh.data.materials:
                object_mesh.data.materials[0] = mat

            else:
                object_mesh.data.materials.append(mat)

            mat.ass_jms.material_effect = material_effect
            mat.diffuse_color = global_functions.get_random_color()

        if geo_class.lower() == 'pill':
            bm = bmesh.new()
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, diameter1=3, diameter2=3, depth=5)
            bm.transform(Matrix.Translation((0, 0, 2.5)))
            bm.to_mesh(mesh)
            bm.free()

        elif geo_class.lower() == 'sphere':
            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=1)
            bm.to_mesh(mesh)
            bm.free()

        elif geo_class.lower() == 'box':
            bm = bmesh.new()
            bmesh.ops.create_cube(bm, size=1.0)
            bm.to_mesh(mesh)
            bm.free()

        elif geo_class.lower() == 'mesh':
            vert_normal_list = []
            vertex_groups = []
            bm = bmesh.new()
            object_triangles = object_element.triangles
            for triangle in object_triangles:
                triangle_material_index = triangle.material_index
                if not triangle_material_index == -1:
                    mat = ass_file.materials[triangle_material_index]

                p1 = object_element.vertices[triangle.v0].translation
                p2 = object_element.vertices[triangle.v1].translation
                p3 = object_element.vertices[triangle.v2].translation

                v1 = bm.verts.new((float(p1[0]), float(p1[1]), float(p1[2])))
                v2 = bm.verts.new((float(p2[0]), float(p2[1]), float(p2[2])))
                v3 = bm.verts.new((float(p3[0]), float(p3[1]), float(p3[2])))
                bm.faces.new((v1, v2, v3))
                vert_list = [triangle.v0, triangle.v1, triangle.v2]
                for vert in vert_list:
                    vert_normals = []
                    ass_vert = object_element.vertices[vert]
                    for normal in ass_vert.normal:
                        vert_normals.append(normal)

                    vert_normal_list.append(vert_normals)
                    for node_values in ass_vert.node_set:
                        node_index = node_values[0]
                        if not node_index == -1 and not node_index in vertex_groups:
                            vertex_groups.append(node_index)
                            object_mesh.vertex_groups.new(name = ass_file.instances[node_index].name)

            bm.verts.ensure_lookup_table()
            bm.faces.ensure_lookup_table()
            vertex_groups_names = object_mesh.vertex_groups.keys()
            for idx, triangle in enumerate(object_triangles):
                triangle_material_index = triangle.material_index
                if not triangle_material_index == -1:
                    material_list = []
                    material_name = mat.name
                    mat = bpy.data.materials.get(material_name)
                    if mat is None:
                        mat = bpy.data.materials.new(name=material_name)

                    for slot in object_mesh.material_slots:
                        material_list.append(slot.material)

                    if not mat in material_list:
                        object_mesh.data.materials.append(mat)

                    mat.diffuse_color = global_functions.get_random_color()
                    material_index = material_list.index(bpy.data.materials[material_name])
                    bm.faces[idx].material_index = material_index

                vert_list = [triangle.v0, triangle.v1, triangle.v2]
                for vert_idx, vert in enumerate(vert_list):
                    vertex_index = (3 * idx) + vert_idx
                    ass_vert = object_element.vertices[vert]
                    bm.verts[vertex_index].normal = ass_vert.normal
                    for uv_idx, uv in enumerate(ass_vert.uv_set):
                        uv_name = 'UVMap_%s' % uv_idx
                        layer_uv = bm.loops.layers.uv.get(uv_name)
                        if layer_uv is None:
                            layer_uv = bm.loops.layers.uv.new(uv_name)

                        loop = bm.faces[idx].loops[vert_idx]
                        loop[layer_uv].uv = (uv[0], uv[1])

                    for node_values in ass_vert.node_set:
                        layer_deform = bm.verts.layers.deform.verify()
                        node_index = node_values[0]
                        node_weight = node_values[1]
                        if not node_index == -1:
                            group_name = ass_file.instances[node_index].name
                            group_index = vertex_groups_names.index(group_name)
                            vert_idx = bm.verts[vertex_index]
                            vert_idx[layer_deform][group_index] = node_weight

            bm.to_mesh(mesh)
            bm.free()
            object_mesh.data.normals_split_custom_set(vert_normal_list)
            object_mesh.data.use_auto_smooth = True

    sorted_parent_id.sort(key=lambda x:x[1])
    for idx, instance in enumerate(ass_file.instances):
        instance_id = sorted_parent_id[idx]
        current_instance = ass_file.instances[instance_id[0]]
        obj = bpy.data.objects[current_instance.name]

        object_index = current_instance.object_index
        object_element = ass_file.objects[object_index]

        geo_class = object_element.geo_class
        object_radius = object_element.radius
        object_height = object_element.height
        object_extents = object_element.extents

        parent_index = current_instance.parent_id - 1
        local_transform = current_instance.local_transform

        matrix_rotation = local_transform.rotation.to_matrix().to_4x4()
        matrix_translation = Matrix.Translation(local_transform.vector)

        local_transform_matrix = matrix_translation @ matrix_rotation

        if not parent_index == -1:
            parent_instance = ass_file.instances[parent_index]
            parent_instance_name = parent_instance.name
            obj.parent = bpy.data.objects[parent_instance_name]

        obj.matrix_local = local_transform_matrix
        view_layer.update()
        if ass_file.version >= 2:
            obj.scale = (local_transform.scale, local_transform.scale , local_transform.scale)
        else:
            obj.scale = (local_transform.scale[0], local_transform.scale[1], local_transform.scale[2])
        if geo_class.lower() == 'pill':
            obj.data.ass_jms.Object_Type = 'CAPSULES'
            object_dimension = object_radius * 2
            obj.dimensions = (object_dimension, object_dimension, (object_dimension + object_height))

        elif geo_class.lower() == 'sphere':
            obj.data.ass_jms.Object_Type = 'SPHERE'
            object_dimension = object_radius * 2
            obj.dimensions = (object_dimension, object_dimension, object_dimension)

        elif geo_class.lower() == 'box':
            obj.data.ass_jms.Object_Type = 'BOX'
            obj.dimensions = ((object_extents[0] * 2), (object_extents[1] * 2), (object_extents[2] * 2))


    report({'INFO'}, "Import completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.ass()
