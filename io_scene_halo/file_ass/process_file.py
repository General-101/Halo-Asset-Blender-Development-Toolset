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

from .format import ASSAsset
from ..global_functions import global_functions

def process_file(filepath):
    ASS = ASSAsset(filepath)

    ASS.version = int(ASS.next())
    version_list = [1, 2, 3, 4, 5, 6, 7]
    if not ASS.version in version_list:
        raise global_functions.AssetParseError("Importer does not support this ASS version")

    ASS.skip(4) # skip header
    material_count = int(ASS.next())
    used_material_names = []
    for material in range(material_count):
        name = ASS.next().strip('\"')
        scene_name = name
        file_name = ""
        if ASS.version >= 3:
            if scene_name in used_material_names:
                file_name = name
                duplicate_name = None
                loop_count = 1
                while duplicate_name == None:
                    while_name = name + "." + str(loop_count).zfill(3)
                    if not while_name in used_material_names:
                        duplicate_name = while_name

                    loop_count += 1

                scene_name = duplicate_name

        used_material_names.append(scene_name)
        material_effect = ASS.next().strip('\"')
        material_strings = []
        if ASS.version >= 4:
            material_string_count = int(ASS.next())
            for string in range(material_string_count):
                material_strings.append(ASS.next().strip('\"'))

        ASS.materials.append(ASSAsset.Material(scene_name, file_name, None, 0, None, None, None, material_effect, material_strings))

    object_count = int(ASS.next())
    for object in range(object_count):
        vertices = []
        node_index_list = []
        triangles = []
        geo_class = ASS.next().strip('\"')
        xref_path = ASS.next().strip('\"')
        xref_name = ASS.next().strip('\"')
        material_index = -1
        radius = 2
        extents = [1.0, 1.0, 1.0]
        height = 1
        light_properties = None
        if geo_class == 'SPHERE':
            material_index = int(ASS.next())
            radius = float(ASS.next())

        elif geo_class == 'BOX':
            material_index = int(ASS.next())
            extents = ASS.next_vector()

        elif geo_class == 'PILL':
            material_index = int(ASS.next())
            height = float(ASS.next())
            radius = float(ASS.next())

        elif geo_class == 'MESH':
            vert_count = int(ASS.next())
            for vert in range(vert_count):
                node_set = []
                uv_set = []
                color = None
                translation = ASS.next_vector()
                normal = ASS.next_vector()
                if ASS.version >= 6:
                    color = ASS.next_vector()

                node_influence_count = int(ASS.next())
                for node in range(node_influence_count):
                    node_index = int(ASS.next())
                    if not node_index in node_index_list:
                        node_index_list.append(node_index)

                    node_weight = float(ASS.next())
                    node_set.append([node_index, node_weight])

                uv_count = int(ASS.next())
                for uv in range(uv_count):
                    tex_u_value = ASS.next()
                    tex_v_value = ASS.next()
                    tex_w_value = None
                    tex_w = None

                    try:
                        tex_u = float(tex_u_value)

                    except ValueError:
                        tex_u = float(tex_u_value.rsplit('.', 1)[0])

                    try:
                        tex_v = float(tex_v_value)

                    except ValueError:
                        tex_v = float(tex_v_value.rsplit('.', 1)[0])

                    if ASS.version >= 5:
                        tex_w_value = ASS.next()

                        try:
                            tex_w = float(tex_w_value)

                        except ValueError:
                            tex_w = float(tex_w_value.rsplit('.', 1)[0])

                    uv_set.append([tex_u, tex_v, tex_w])

                vertices.append(ASSAsset.Vertex(node_influence_count, node_set, -1, translation, normal, color, uv_set))

            triangle_count = int(ASS.next())
            for triangle in range(triangle_count):
                material_index = int(ASS.next())
                v0 = int(ASS.next())
                v1 = int(ASS.next())
                v2 = int(ASS.next())

                triangles.append(ASSAsset.Triangle(-1, material_index, v0, v1, v2))

        elif geo_class == 'GENERIC_LIGHT':
            light_type = ASS.next().strip('\"')
            light_color = ASS.next_vector()
            intensity = float(ASS.next())
            hotspot_size = float(ASS.next())
            hotspot_falloff_size = float(ASS.next())
            uses_near_attenuation = int(ASS.next())
            near_attenuation_start = float(ASS.next())
            near_attenuation_end = float(ASS.next())
            uses_far_attenuation = int(ASS.next())
            far_attenuation_start = float(ASS.next())
            far_attenuation_end = float(ASS.next())
            light_shape = int(ASS.next())
            light_aspect_ratio = float(ASS.next())

            light_properties = ASSAsset.Light(light_type, light_color, intensity, hotspot_size, hotspot_falloff_size, uses_near_attenuation, near_attenuation_start, near_attenuation_end, uses_far_attenuation, far_attenuation_start, far_attenuation_end, light_shape, light_aspect_ratio)

        else:
            print("Bad object")

        ASS.objects.append(ASSAsset.Object(geo_class, xref_path, xref_name, material_index, radius, extents, height, vertices, triangles, node_index_list, light_properties))

    name_list = []
    instance_count = int(ASS.next())
    for instance in range(instance_count):
        object_index = int(ASS.next())
        bone_influence_count = 0
        if not object_index == -1:
            object_element = ASS.objects[object_index]
            bone_influence_count = len(object_element.node_index_list)

        name = ASS.next().strip('\"')
        if name in name_list:
            true_name = '%s_%s' % (name, instance)

        else:
            true_name = name

        name_list.append(name)
        unique_id = int(ASS.next())
        parent_id = int(ASS.next())
        inheritance_flag = int(ASS.next())
        if ASS.version == 1:
            local_transform = ASS.next_transform_legacy()
            pivot_transform = ASS.next_transform_legacy()

        else:
            local_transform = ASS.next_transform()
            pivot_transform = ASS.next_transform()

        if bone_influence_count > 0:
            ASS.skip(bone_influence_count)

        ASS.instances.append(ASSAsset.Instance(true_name, object_index, unique_id, parent_id, inheritance_flag, local_transform, pivot_transform))

    if ASS.left() != 0: # is something wrong with the parser?
        raise RuntimeError("%s elements left after parse end" % ASS.left())

    return ASS
