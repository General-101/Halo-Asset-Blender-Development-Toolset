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
import bpy
import socket

from getpass import getuser
from .process_scene import process_scene
from ..global_functions import global_functions

def build_asset(context, filepath, version, game_version, folder_structure, hidden_geo, exluded_collections, apply_modifiers, triangulate_faces, edge_split, clean_normalize_weights, custom_scale, report):
    ASS = process_scene(context, version, game_version, hidden_geo, exluded_collections, apply_modifiers, triangulate_faces, edge_split, clean_normalize_weights, custom_scale, report)

    filename = os.path.basename(filepath)
    root_directory = global_functions.get_directory(context, game_version, "render", folder_structure, "0", False, filepath)

    file = open(root_directory + os.sep + filename, 'w', encoding='utf_8')

    account_name = "missing string"
    pc_name = "missing string"
    try:
        account_name = getuser()
        
    except:
        report({'WARNING'}, "Something went wrong when we tried to retrieve the account name. Call a technician or a priest depending.")
        
    try:
        pc_name = socket.gethostname().upper()
        
    except:
        report({'WARNING'}, "Something went wrong when we tried to retrieve the PC name. Call a technician or a priest depending.")

    file.write(
        ';### HEADER ###' +
        '\n%s' % (version) +
        '\n"BLENDER"' +
        '\n"%s.%s"' % (bpy.app.version[0], bpy.app.version[1]) +
        '\n"%s"' % (account_name) +
        '\n"%s"\n' % (pc_name)
    )

    file.write(
        '\n;### MATERIALS ###' +
        '\n%s\n' % (len(ASS.materials))
    )

    for idx, material in enumerate(ASS.materials):
        file.write(
            '\n;MATERIAL %s' % (idx) +
            '\n"%s"' % (material.name)
        )

        if version >= 8: #3
            file.write(
                '\n"%s %s"\n' % (material.permutation, material.region)
            )

        else:
            file.write(
                '\n"%s"\n' % (material.material_effect)
            )

        if version >= 4:
            file.write(
                '%s\n' % (len(material.material_strings))
            )

            for string in material.material_strings:
                file.write(
                    '"%s"\n' % (string)
                )

    file.write(
        '\n;### OBJECTS ###' +
        '\n%s\n' % (len(ASS.objects))
    )

    for idx, geometry in enumerate(ASS.objects):
        if geometry.geo_class == 'SPOT_LGT' or geometry.geo_class == 'DIRECT_LGT' or geometry.geo_class == 'OMNI_LGT' or geometry.geo_class == 'AMBIENT_LGT':
            file.write(
                '\n;OBJECT %s' % (idx) +
                '\n"%s"' % ('GENERIC_LIGHT') +
                '\n"%s"' % (geometry.xref_filepath) +
                '\n"%s"' % (geometry.xref_objectname) +
                '\n"%s"' % (geometry.geo_class) +
                '\n%0.10f\t%0.10f\t%0.10f' % (geometry.light_properties.light_color[0], geometry.light_properties.light_color[1], geometry.light_properties.light_color[2]) +
                '\n%0.10f' % (geometry.light_properties.intensity) +
                '\n%0.10f' % (geometry.light_properties.hotspot_falloff_size) +
                '\n%0.10f' % (geometry.light_properties.hotspot_size) +
                '\n%s' % (geometry.light_properties.uses_near_attenuation) +
                '\n%0.10f' % (geometry.light_properties.near_attenuation_start) +
                '\n%0.10f' % (geometry.light_properties.near_attenuation_end) +
                '\n%s' % (geometry.light_properties.uses_far_attenuation) +
                '\n%0.10f' % (geometry.light_properties.far_attenuation_start) +
                '\n%0.10f' % (geometry.light_properties.far_attenuation_end) +
                '\n%s' % (geometry.light_properties.light_shape) +
                '\n%0.10f' % (geometry.light_properties.light_aspect_ratio) +
                '\n'
            )

        elif geometry.geo_class == 'BONE':
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
                '\n%s' % (len(geometry.vertices))
            )

            for vert in geometry.vertices:
                file.write(
                    '\n%0.10f\t%0.10f\t%0.10f' % (vert.translation[0], vert.translation[1], vert.translation[2]) +
                    '\n%0.10f\t%0.10f\t%0.10f' % (vert.normal[0], vert.normal[1], vert.normal[2])
                )

                if version >= 6:
                    file.write('\n%0.10f\t%0.10f\t%0.10f' % (vert.color[0], vert.color[1], vert.color[2]))

                file.write('\n%s' % (len(vert.node_set)))

                for node in vert.node_set:
                    node_index = node[0]
                    node_weight = node[1]
                    if version >= 3:
                        file.write(
                            '\n%s\t%0.10f' % (node_index, node_weight)
                        )

                    else:
                        file.write(
                            '\n%s' % (node_index) +
                            '\n%0.10f' % (node_weight)
                        )

                file.write('\n%s' % (len(vert.uv_set)))
                for uv in vert.uv_set:
                    tex_u = uv[0]
                    tex_v = uv[1]
                    tex_w = 0
                    if version >= 5:
                        file.write('\n%0.10f\t%0.10f\t%0.10f\n' % (tex_u, tex_v, tex_w))

                    else:
                        file.write('\n%0.10f\t%0.10f' % (tex_u, tex_v))

            file.write('\n%s' % (len(geometry.triangles)))
            for triangle in geometry.triangles:
                if version >= 3:
                    file.write(
                        '\n%s' % (triangle.material_index) +
                        '\t\t%s\t%s\t%s' % (triangle.v0, triangle.v1, triangle.v2)
                    )

                else:
                    file.write(
                        '\n%s' % (triangle.material_index) +
                        '\n%s\n%s\n%s' % (triangle.v0, triangle.v1, triangle.v2)
                    )

            file.write('\n')

        else:
            print("Bad object")

    file.write(
        '\n;### INSTANCES ###' +
        '\n%s\n' % (len(ASS.instances))
    )

    for idx, instance in enumerate(ASS.instances):
        node_index_list = []
        if not instance.object_index == -1:
            instance_object = ASS.objects[instance.object_index]
            if not instance_object.node_index_list == None:
                node_index_list = instance_object.node_index_list

        file.write(
            '\n;INSTANCE %s' % (idx) +
            '\n%s' % (instance.object_index) +
            '\n\"%s\"' % (instance.name) +
            '\n%s' % (instance.unique_id) +
            '\n%s' % (instance.parent_id) +
            '\n%s' % (instance.inheritance_flag) +
            '\n%0.10f\t%0.10f\t%0.10f\t%0.10f' % (instance.local_transform.rotation[0], instance.local_transform.rotation[1], instance.local_transform.rotation[2], instance.local_transform.rotation[3]) +
            '\n%0.10f\t%0.10f\t%0.10f' % (instance.local_transform.translation[0], instance.local_transform.translation[1], instance.local_transform.translation[2])
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
            '\n%0.10f\t%0.10f\t%0.10f' % (instance.pivot_transform.translation[0], instance.pivot_transform.translation[1], instance.pivot_transform.translation[2])
            )

        if version <= 1:
            file.write(
                '\n%0.10f\t%0.10f\t%0.10f\n' % (instance.pivot_transform.scale[0], instance.pivot_transform.scale[1], instance.pivot_transform.scale[2])
                )

        else:
            file.write(
                '\n%0.10f\n' % (instance.pivot_transform.scale[0])
                )

        for node_index in node_index_list:
            file.write('%s\n' % node_index)

    file.close()
