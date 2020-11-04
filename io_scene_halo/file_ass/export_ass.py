# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2020 Dave Barnes and Steven Garcia
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
import socket
import traceback

from decimal import *
from getpass import getuser
from io_scene_halo.global_functions import global_functions

class ASSScene(global_functions.HaloAsset):
    class Transform:
        def __init__(self, rotation=(0.0, 0.0, 0.0, 1.0), vector=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0)):
            self.rotation = rotation
            self.vector = vector
            self.scale = scale

    class Material:
        def __init__(self, name, effect):
            self.name = name
            self.effect = effect

    class Object:
        def __init__(self, geo_class, xref_filepath, xref_objectname, material_index=-1, radius=0.0, extents=None, height=0.0, verts=None, triangles=None, node_index_list=None):
            self.geo_class = geo_class
            self.xref_filepath = xref_filepath
            self.xref_objectname = xref_objectname
            self.material_index = material_index
            self.radius = radius
            self.extents = extents
            self.height = height
            self.verts = verts
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

    def __init__(self, context, report, version, game_version, apply_modifiers, triangulate_faces, edge_split, use_edge_angle, use_edge_sharp, split_angle, clean_normalize_weights, hidden_geo, custom_scale):
        global_functions.unhide_all_collections()
        view_layer = bpy.context.view_layer
        object_list = list(bpy.context.scene.objects)
        self.materials = []
        self.objects = []
        self.instances = []
        material_list = []
        armature = []
        geometry_list = []
        original_geometry_list = []
        unique_instance_geometry_list = []
        unique_instance_geometry_list_2 = []
        object_properties = []
        object_count = 0
        for obj in object_list:
            object_properties.append([obj.hide_get(), obj.hide_viewport])
            if hidden_geo:
                global_functions.unhide_object(obj)

            if obj.type == 'MESH':
                if global_functions.set_ignore(obj) == False or hidden_geo:
                    if clean_normalize_weights:
                        if len(obj.vertex_groups) > 0:
                            view_layer.objects.active = obj
                            bpy.ops.object.mode_set(mode = 'EDIT')
                            bpy.ops.mesh.select_all(action='SELECT')
                            bpy.ops.object.vertex_group_clean(group_select_mode='ALL', limit=0.0)
                            bpy.ops.object.vertex_group_normalize_all()
                            bpy.ops.object.mode_set(mode = 'OBJECT')

                modifier_list = []
                if apply_modifiers:
                    for modifier in obj.modifiers:
                        modifier.show_render = True
                        modifier.show_viewport = True
                        modifier.show_in_editmode = True
                        modifier_list.append(modifier.type)

                if triangulate_faces:
                    if not 'TRIANGULATE' in modifier_list:
                        obj.modifiers.new("Triangulate", type='TRIANGULATE')

                if edge_split:
                    if not 'EDGE_SPLIT' in modifier_list:
                        edge_split = obj.modifiers.new("EdgeSplit", type='EDGE_SPLIT')
                        edge_split.use_edge_angle = use_edge_angle
                        edge_split.split_angle = split_angle
                        edge_split.use_edge_sharp = use_edge_sharp
                    else:
                        modifier_idx = modifier_list.index('EDGE_SPLIT')
                        obj.modifiers[modifier_idx].use_edge_angle = use_edge_angle
                        obj.modifiers[modifier_idx].split_angle = split_angle
                        obj.modifiers[modifier_idx].use_edge_sharp = use_edge_sharp

        depsgraph = context.evaluated_depsgraph_get()

        for obj in object_list:
            if obj.type == 'ARMATURE':
                if global_functions.set_ignore(obj) == False or hidden_geo:
                    for bone in obj.data.bones:
                        if not bone.name in unique_instance_geometry_list:
                            unique_instance_geometry_list.append(bone.name)

                        geometry_list.append((bone, 'BONE', bone.name, bone.name))
                        original_geometry_list.append(bone)
                        object_count += 1

            elif obj.type== 'MESH' and len(obj.data.polygons) > 0:
                if global_functions.set_ignore(obj) == False or hidden_geo:
                    if not obj.data.name in unique_instance_geometry_list:
                        unique_instance_geometry_list.append(obj.data.name)
                        object_count += 1

                    if obj.data.ass_jms.Object_Type == 'SPHERE':
                        me = obj.to_mesh(preserve_all_data_layers=True)
                        geometry_list.append((me, 'SPHERE', obj.name, obj.data.name))
                        original_geometry_list.append(obj)

                    elif obj.data.ass_jms.Object_Type == 'BOX':
                        me = obj.to_mesh(preserve_all_data_layers=True)
                        geometry_list.append((me, 'BOX', obj.name, obj.data.name))
                        original_geometry_list.append(obj)

                    elif obj.data.ass_jms.Object_Type == 'CAPSULES':
                        me = obj.to_mesh(preserve_all_data_layers=True)
                        geometry_list.append((me, 'PILL', obj.name, obj.data.name))
                        original_geometry_list.append(obj)

                    elif obj.data.ass_jms.Object_Type == 'CONVEX SHAPES':
                        if apply_modifiers:
                            obj_for_convert = obj.evaluated_get(depsgraph)
                            me = obj_for_convert.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
                            geometry_list.append((me, 'MESH', obj.name, obj.data.name))
                            original_geometry_list.append(obj)

                        else:
                            me = obj.to_mesh(preserve_all_data_layers=True)
                            geometry_list.append((me, 'MESH', obj.name, obj.data.name))
                            original_geometry_list.append(obj)

        self.instances.append(ASSScene.Instance(name='Scene Root', local_transform=ASSScene.Transform(), pivot_transform=ASSScene.Transform()))
        for idx, geometry in enumerate(geometry_list):
            verts = []
            triangles = []
            node_index_list = []
            original_geo = original_geometry_list[idx]
            mesh = geometry[0]
            geo_class = geometry[1]
            geo_name = geometry[2]
            mesh_name = geometry[3]
            object_index = unique_instance_geometry_list.index(mesh_name)
            material_index = -1
            radius = 2
            extents = [1.0, 1.0, 1.0]
            height = 1
            parent_id = 0
            inheritance_flag = 0
            xref_name = ""
            is_bone = False
            if geo_class == 'BONE':
                armature_name = original_geo.id_data.name
                armature = bpy.data.objects[armature_name]
                parent = original_geo.parent
                is_bone = True
            else:
                if armature:
                    parent = original_geo.parent_bone
                else:
                    parent = original_geo.parent

            if not parent == None:
                if not geo_class == 'BONE':
                    if not original_geo.parent.type  == 'ARMATURE':
                        parent_id = original_geometry_list.index(parent) + 1
                else:
                    parent_id = original_geometry_list.index(parent) + 1

            geo_matrix = global_functions.get_matrix(original_geo, original_geo, True, armature, original_geometry_list, is_bone, version, 'ASS', 0)
            geo_dimensions = global_functions.get_dimensions(geo_matrix, original_geo, None, None, custom_scale, version, None, False, is_bone, armature, 'ASS')
            rotation = (geo_dimensions.quat_i_a, geo_dimensions.quat_j_a, geo_dimensions.quat_k_a, geo_dimensions.quat_w_a)
            translation = (geo_dimensions.pos_x_a, geo_dimensions.pos_y_a, geo_dimensions.pos_z_a)
            if geo_class == 'BONE':
                scale = armature.pose.bones[original_geo.name].scale
            else:
                scale = original_geo.scale
            local_transform = ASSScene.Transform(rotation, translation, scale)
            self.instances.append(ASSScene.Instance(geo_name, object_index, idx, parent_id, inheritance_flag, local_transform, pivot_transform=ASSScene.Transform()))
            if not mesh_name in unique_instance_geometry_list_2:
                unique_instance_geometry_list_2.append(mesh_name)
                if geo_class == 'BONE':
                    armature_name = mesh.id_data.name
                    armature = bpy.data.objects[armature_name]
                    xref_path = bpy.path.abspath(armature.data.ass_jms.XREF_path)
                    if xref_path != "":
                        xref_name = armature.name

                elif geo_class == 'SPHERE':
                    xref_path = bpy.path.abspath(original_geo.data.ass_jms.XREF_path)
                    if xref_path != "":
                        xref_name = original_geo.name

                    radius = geo_dimensions.radius_a
                    face = original_geo.data.polygons[0]
                    material = global_functions.get_material(game_version, original_geo, face, mesh, material_list, 'ASS', None, None,)
                    if not material == -1:
                        material_list = global_functions.gather_materials(game_version, material, material_list, 'ASS', None, None, None)
                        material_index = material_list.index(material)

                elif geo_class == 'BOX':
                    xref_path = bpy.path.abspath(original_geo.data.ass_jms.XREF_path)
                    if xref_path != "":
                        xref_name = original_geo.name

                    face = original_geo.data.polygons[0]
                    material = global_functions.get_material(game_version, original_geo, face, mesh, material_list, 'ASS', None, None,)
                    if not material == -1:
                        material_list = global_functions.gather_materials(game_version, material, material_list, 'ASS', None, None, None)
                        material_index = material_list.index(material)

                elif geo_class == 'PILL':
                    xref_path = bpy.path.abspath(original_geo.data.ass_jms.XREF_path)
                    if xref_path != "":
                        xref_name = original_geo.name

                    face = original_geo.data.polygons[0]
                    material = global_functions.get_material(game_version, original_geo, face, mesh, material_list, 'ASS', None, None,)
                    if not material == -1:
                        material_list = global_functions.gather_materials(game_version, material, material_list, 'ASS', None, None, None)
                        material_index = material_list.index(material)

                elif geo_class == 'MESH':
                    xref_path = bpy.path.abspath(original_geo.data.ass_jms.XREF_path)
                    if xref_path != "":
                        xref_name = original_geo.name

                    vertex_groups = original_geo.vertex_groups.keys()
                    for face in mesh.polygons:
                        v0 = len(verts)
                        v1 = len(verts) + 1
                        v2 = len(verts) + 2
                        material = global_functions.get_material(game_version, original_geo, face, mesh, material_list, 'ASS', None, None,)
                        material_index = -1
                        if not material == -1:
                            material_list = global_functions.gather_materials(game_version, material, material_list, 'ASS', None, None, None)
                            material_index = material_list.index(material)

                        triangles.append(ASSScene.Triangle(material_index, v0, v1, v2))
                        for loop_index in face.loop_indices:
                            vert = mesh.vertices[mesh.loops[loop_index].vertex_index]
                            translation = vert.co
                            normal = vert.normal
                            uv_set = []
                            for uv_index in range(len(mesh.uv_layers)):
                                mesh.uv_layers.active = mesh.uv_layers[uv_index]
                                uv = mesh.uv_layers.active.data[mesh.loops[loop_index].index].uv
                                uv_set.append(uv)

                            uv = uv_set
                            node_influence_count = 0
                            node_set = []
                            if len(vert.groups) != 0:
                                object_vert_group_list = []
                                vertex_vert_group_list = []
                                for group_index in range(len(vert.groups)):
                                    vert_group = vert.groups[group_index].group
                                    object_vertex_group = vertex_groups[vert_group]
                                    if armature:
                                        if object_vertex_group in armature.data.bones:
                                            vertex_vert_group_list.append(group_index)
                                            if armature.data.bones[object_vertex_group] in original_geometry_list:
                                                object_vert_group_list.append(vert_group)

                                    else:
                                        if object_vertex_group in bpy.data.objects:
                                            vertex_vert_group_list.append(group_index)
                                            if bpy.data.objects[object_vertex_group] in original_geometry_list:
                                                object_vert_group_list.append(vert_group)

                                value = len(object_vert_group_list)
                                if value > 4:
                                    value = 4

                                node_influence_count = int(value)
                                if len(object_vert_group_list) != 0:
                                    for idx, group_index in enumerate(object_vert_group_list):
                                        vert_index = int(vertex_vert_group_list[idx])
                                        vert_group = vert.groups[vert_index].group
                                        object_vertex_group = vertex_groups[vert_group]
                                        if armature:
                                            node_obj = armature.data.bones[object_vertex_group]

                                        else:
                                            node_obj = bpy.data.objects[object_vertex_group]

                                        node_index = int(original_geometry_list.index(node_obj))
                                        if not node_index in node_index_list:
                                            node_index_list.append(node_index)
                                        node_weight = float(vert.groups[vert_index].weight)
                                        node_set.append([node_index, node_weight])

                            verts.append(ASSScene.Vertex(node_influence_count, node_set, translation, normal, uv_set))


                self.objects.append(ASSScene.Object(geo_class, xref_path, xref_name, material_index, radius, extents, height, verts, triangles, node_index_list))

        for material in material_list:
            name = material.name
            effect_name = material.ass_jms.material_effect

            self.materials.append(ASSScene.Material(name, effect_name))

        for idx, obj in enumerate(object_list):
            property_value = object_properties[idx]
            obj.hide_set(property_value[0])
            obj.hide_viewport = property_value[1]

def write_file(context, filepath, report, ass_version, ass_version_h2, use_scene_properties, hidden_geo, apply_modifiers, triangulate_faces, edge_split, use_edge_angle, use_edge_sharp, split_angle, clean_normalize_weights, scale_enum, scale_float, console, game_version, encoding):
    custom_scale = global_functions.set_scale(scale_enum, scale_float)
    version = global_functions.get_version(ass_version, None, ass_version_h2, game_version, console)
    try:
        ass_scene = ASSScene(context, report, version, game_version, apply_modifiers, triangulate_faces, edge_split, use_edge_angle, use_edge_sharp, split_angle, clean_normalize_weights, hidden_geo, custom_scale)
    except global_functions.AssetParseError as parse_error:
        info = sys.exc_info()
        traceback.print_exception(info[0], info[1], info[2])
        report({'ERROR'}, "Bad scene: {0}".format(parse_error))
        return {'CANCELLED'}
    except:
        info = sys.exc_info()
        traceback.print_exception(info[0], info[1], info[2])
        report({'ERROR'}, "Internal error: {1}({0})".format(info[1], info[0]))
        return {'CANCELLED'}

    file = open(filepath, 'w', encoding=encoding)

    file.write(
        ';### HEADER ###' +
        '\n%s' % (version) +
        '\n"BLENDER"' +
        '\n"%s.%s"' % (bpy.app.version[0], bpy.app.version[1]) +
        '\n"%s"' % (getuser()) +
        '\n"%s"\n' % (socket.gethostname().upper())
    )

    file.write(
        '\n;### MATERIALS ###' +
        '\n%s\n' % (len(ass_scene.materials))
    )

    for idx, material in enumerate(ass_scene.materials):
        file.write(
            '\n;MATERIAL %s' % (idx) +
            '\n"%s"' % (material.name) +
            '\n"%s"\n' % (material.effect)
        )

    file.write(
        '\n;### OBJECTS ###' +
        '\n%s\n' % (len(ass_scene.objects))
    )

    for idx, geometry in enumerate(ass_scene.objects):
        if geometry.geo_class == 'BONE':
            file.write(
                '\n;OBJECT %s' % (idx) +
                '\n"%s"' % ('SPHERE') +
                '\n"%s"' % (geometry.xref_filepath) +
                '\n"%s"' % (geometry.xref_objectname) +
                '\n%s' % (geometry.material_index) +
                '\n%0.10f' % (geometry.radius) +
                '\n'
            )

        elif geometry.geo_class == 'SPHERE':
            file.write(
                '\n;OBJECT %s' % (idx) +
                '\n"%s"' % (geometry.geo_class) +
                '\n"%s"' % (geometry.xref_filepath) +
                '\n"%s"' % (geometry.xref_objectname) +
                '\n%s' % (geometry.material_index) +
                '\n%0.10f' % (geometry.radius) +
                '\n'
            )

        elif geometry.geo_class == 'BOX':
            file.write(
                '\n;OBJECT %s' % (idx) +
                '\n"%s"' % (geometry.geo_class) +
                '\n"%s"' % (geometry.xref_filepath) +
                '\n"%s"' % (geometry.xref_objectname) +
                '\n%s' % (geometry.material_index) +
                '\n%0.10f\t%0.10f\t%0.10f' % ((geometry.extents[0] / 2), (geometry.extents[1] / 2), (geometry.extents[2] / 2)) +
                '\n'
            )

        elif geometry.geo_class == 'PILL':
            file.write(
                '\n;OBJECT %s' % (idx) +
                '\n"%s"' % (geometry.geo_class) +
                '\n"%s"' % (geometry.xref_filepath) +
                '\n"%s"' % (geometry.xref_objectname) +
                '\n%s' % (geometry.material_index) +
                '\n%0.10f' % (geometry.height) +
                '\n%0.10f' % (geometry.radius) +
                '\n'
            )

        elif geometry.geo_class == 'MESH':
            file.write(
                '\n;OBJECT %s' % (idx) +
                '\n"%s"' % (geometry.geo_class) +
                '\n"%s"' % (geometry.xref_filepath) +
                '\n"%s"' % (geometry.xref_objectname) +
                '\n%s' % (len(geometry.verts))
            )

            for vert in geometry.verts:
                file.write(
                    '\n%0.10f\t%0.10f\t%0.10f' % (vert.translation[0], vert.translation[1], vert.translation[2]) +
                    '\n%0.10f\t%0.10f\t%0.10f' % (vert.normal[0], vert.normal[1], vert.normal[2])
                )

                file.write('\n%s' % (len(vert.node_set)))

                for node in vert.node_set:
                    node_index = node[0]
                    node_weight = node[1]
                    file.write(
                        '\n%s' % (node_index) +
                        '\n%0.10f' % (node_weight)
                    )

                file.write('\n%s' % (len(vert.uv_set)))
                for uv in vert.uv_set:
                    tex_u = uv[0]
                    tex_v = uv[1]
                    tex_w = 0
                    file.write('\n%0.10f\t%0.10f' % (tex_u, tex_v))

            file.write('\n%s' % (len(geometry.triangles)))
            for triangle in geometry.triangles:
                file.write(
                    '\n%s' % (triangle.material_index) +
                    '\n%s\n%s\n%s' % (triangle.v0, triangle.v1, triangle.v2)
                )

            file.write('\n')

    file.write(
        '\n;### INSTANCES ###' +
        '\n%s\n' % (len(ass_scene.instances))
    )

    for idx, instance in enumerate(ass_scene.instances):
        node_index_list = []
        if not instance.object_index == -1:
            instance_object = ass_scene.objects[instance.object_index]
            node_index_list = instance_object.node_index_list

        file.write(
            '\n;INSTANCE %s' % (idx) +
            '\n%s' % (instance.object_index) +
            '\n\"%s\"' % (instance.name) +
            '\n%s' % (instance.unique_id) +
            '\n%s' % (instance.parent_id) +
            '\n%s' % (instance.inheritance_flag) +
            '\n%0.10f\t%0.10f\t%0.10f\t%0.10f' % (instance.local_transform.rotation[0], instance.local_transform.rotation[1], instance.local_transform.rotation[2], instance.local_transform.rotation[3]) +
            '\n%0.10f\t%0.10f\t%0.10f' % (instance.local_transform.vector[0], instance.local_transform.vector[1], instance.local_transform.vector[2])
            )

        if version <= 1:
            file.write(
                '\n%0.10f\t%0.10f\t%0.10f\n' % (instance.local_transform.scale[0], instance.local_transform.scale[1], instance.local_transform.scale[2])
                )

        else:
            file.write(
                '\n%0.10f' % (instance.local_transform.scale[0])
                )

        file.write(
            '\n%0.10f\t%0.10f\t%0.10f\t%0.10f' % (instance.pivot_transform.rotation[0], instance.pivot_transform.rotation[1], instance.pivot_transform.rotation[2], instance.pivot_transform.rotation[3]) +
            '\n%0.10f\t%0.10f\t%0.10f' % (instance.pivot_transform.vector[0], instance.pivot_transform.vector[1], instance.pivot_transform.vector[2])
            )

        if version <= 1:
            file.write(
                '\n%0.10f\t%0.10f\t%0.10f\n' % (instance.pivot_transform.scale[0], instance.pivot_transform.scale[1], instance.pivot_transform.scale[2])
                )

        else:
            file.write(
                '\n%0.10f\n' % (instance.pivot_transform.scale[0])
                )

        for node_infex in node_index_list:
            file.write('%s\n' % node_infex)

    file.close()
    report({'INFO'}, "Export completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_scene.ass()
