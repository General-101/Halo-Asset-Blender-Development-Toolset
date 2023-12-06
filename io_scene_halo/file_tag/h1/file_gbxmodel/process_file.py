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

from xml.dom import minidom
from ....global_functions import tag_format
from ...h1.file_model.format import ModelAsset, ModelFlags, PermutationFlags, PartFlags

XML_OUTPUT = False

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    MODEL = ModelAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    MODEL.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    MODEL.mod2_body = MODEL.ModelBody()
    MODEL.mod2_body.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ModelFlags))
    MODEL.mod2_body.node_list_checksum = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(tag_node, "node list checksum"))
    MODEL.mod2_body.superhigh_detail_cutoff = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "super-high detail cutoff"))
    MODEL.mod2_body.high_detail_cutoff = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "high detail cutoff"))
    MODEL.mod2_body.medium_detail_cutoff = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "medium detail cutoff"))
    MODEL.mod2_body.low_detail_cutoff = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "low detail cutoff"))
    MODEL.mod2_body.superlow_cutoff = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "super-low cutoff"))
    MODEL.mod2_body.superhigh_detail_nodes = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "super-high detail node count"))
    MODEL.mod2_body.high_detail_nodes = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "high detail node count"))
    MODEL.mod2_body.medium_detail_nodes = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "medium detail node count"))
    MODEL.mod2_body.low_detail_nodes = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "low detail node count"))
    MODEL.mod2_body.superlow_nodes = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "super-low detail node count"))
    input_stream.read(10) # Padding?
    MODEL.mod2_body.base_map_u_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "base map u-scale"))
    MODEL.mod2_body.base_map_v_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "base map v-scale"))
    input_stream.read(116) # Padding?
    MODEL.mod2_body.markers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "markers"))
    MODEL.mod2_body.nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "nodes"))
    MODEL.mod2_body.regions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "regions"))
    MODEL.mod2_body.geometries_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "geometries"))
    MODEL.mod2_body.shaders_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "shaders"))

    MODEL.markers = []
    marker_node = tag_format.get_xml_node(XML_OUTPUT, MODEL.mod2_body.markers_tag_block.count, tag_node, "name", "markers")
    for marker_idx in range(MODEL.mod2_body.markers_tag_block.count):
        marker_element_node = None
        if XML_OUTPUT:
            marker_element_node = TAG.xml_doc.createElement('element')
            marker_element_node.setAttribute('index', str(marker_idx))
            marker_node.appendChild(marker_element_node)

        marker = MODEL.Markers()
        marker.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(marker_element_node, "name"))
        marker.magic_identifier = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(marker_element_node, "magic identifier"))
        input_stream.read(18) # Padding?
        marker.instance_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(marker_element_node, "instances"))

        MODEL.markers.append(marker)

    for marker_idx, marker in enumerate(MODEL.markers):
        marker_element_node = None
        if XML_OUTPUT:
            marker_element_node = marker_node.childNodes[marker_idx]

        marker.instances = []
        instance_node = tag_format.get_xml_node(XML_OUTPUT, marker.instance_tag_block.count, marker_element_node, "name", "instances")
        for instance_idx in range(marker.instance_tag_block.count):
            instance_element_node = None
            if XML_OUTPUT:
                instance_element_node = TAG.xml_doc.createElement('element')
                instance_element_node.setAttribute('index', str(instance_idx))
                instance_node.appendChild(instance_element_node)

            instance = MODEL.Instances()
            instance.region_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(instance_element_node, "region index"))
            instance.permutation_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(instance_element_node, "permutation index"))
            instance.node_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(instance_element_node, "node index"))
            input_stream.read(1) # Padding?
            instance.translation = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(instance_element_node, "translation"), True)
            instance.rotation = TAG.read_quaternion(input_stream, TAG,  tag_format.XMLData(instance_element_node, "rotation"), True)

            marker.instances.append(instance)

    MODEL.nodes = []
    MODEL.transforms = []
    transforms = []
    bone_node = tag_format.get_xml_node(XML_OUTPUT, MODEL.mod2_body.nodes_tag_block.count, tag_node, "name", "nodes")
    for node_idx in range(MODEL.mod2_body.nodes_tag_block.count):
        bone_element_node = None
        if XML_OUTPUT:
            bone_element_node = TAG.xml_doc.createElement('element')
            bone_element_node.setAttribute('index', str(node_idx))
            bone_node.appendChild(bone_element_node)

        node = MODEL.Nodes()
        transform = MODEL.Transform()
        node.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(bone_element_node, "name"))
        node.sibling = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(bone_element_node, "next sibling node index", None, MODEL.mod2_body.nodes_tag_block.count, "model_node_block"))
        node.child = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(bone_element_node, "first child node index", None, MODEL.mod2_body.nodes_tag_block.count, "model_node_block"))
        node.parent = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(bone_element_node, "parent node index", None, MODEL.mod2_body.nodes_tag_block.count, "model_node_block"))
        input_stream.read(2) # Padding?
        transform.translation = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(bone_element_node, "default translation"), True)
        transform.rotation = TAG.read_quaternion(input_stream, TAG, tag_format.XMLData(bone_element_node, "default rotation"), True)
        node.distance_from_parent = TAG.read_float(input_stream, TAG, tag_format.XMLData(bone_element_node, "node distance from parent"), True)
        input_stream.read(32) # Padding?
        input_stream.read(52) # Padding?

        MODEL.nodes.append(node)
        transforms.append(transform)

    MODEL.transforms.append(transforms)

    MODEL.regions = []
    region_node = tag_format.get_xml_node(XML_OUTPUT, MODEL.mod2_body.regions_tag_block.count, tag_node, "name", "regions")
    for region_idx in range(MODEL.mod2_body.regions_tag_block.count):
        region_element_node = None
        if XML_OUTPUT:
            region_element_node = TAG.xml_doc.createElement('element')
            region_element_node.setAttribute('index', str(region_idx))
            region_node.appendChild(region_element_node)

        region = MODEL.Regions()
        region.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(bone_element_node, "name"))
        input_stream.read(32) # Padding?
        region.permutation_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(region_element_node, "permutations"))

        MODEL.regions.append(region)

    for region_idx, region in enumerate(MODEL.regions):
        region_element_node = None
        if XML_OUTPUT:
            region_element_node = region_node.childNodes[region_idx]

        region.permutations = []
        permutation_node = tag_format.get_xml_node(XML_OUTPUT, region.permutation_tag_block.count, region_element_node, "name", "permutations")
        for permutation_idx in range(region.permutation_tag_block.count):
            permutation_element_node = None
            if XML_OUTPUT:
                permutation_element_node = TAG.xml_doc.createElement('element')
                permutation_element_node.setAttribute('index', str(permutation_idx))
                permutation_node.appendChild(permutation_element_node)

            permutation = MODEL.Permutations()
            permutation.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(permutation_element_node, "name"))
            permutation.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(permutation_element_node, "flags", PermutationFlags))
            input_stream.read(28) # Padding?
            permutation.superlow_geometry_block = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "super low", None, MODEL.mod2_body.geometries_tag_block.count, "model_geometry_block"))
            permutation.low_geometry_block = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "low", None, MODEL.mod2_body.geometries_tag_block.count, "model_geometry_block"))
            permutation.medium_geometry_block = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "medium", None, MODEL.mod2_body.geometries_tag_block.count, "model_geometry_block"))
            permutation.high_geometry_block = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "high", None, MODEL.mod2_body.geometries_tag_block.count, "model_geometry_block"))
            permutation.superhigh_geometry_block = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "super high", None, MODEL.mod2_body.geometries_tag_block.count, "model_geometry_block"))
            input_stream.read(2) # Padding?
            permutation.marker_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(permutation_element_node, "markers"))

            region.permutations.append(permutation)

        for permutation_idx, permutation in enumerate(region.permutations):
            permutation_element_node = None
            if XML_OUTPUT:
                permutation_element_node = permutation_node.childNodes[permutation_idx]

            permutation.local_markers = []
            marker_node = tag_format.get_xml_node(XML_OUTPUT, permutation.marker_tag_block.count, permutation_element_node, "name", "markers")
            for local_marker_idx in range(permutation.marker_tag_block.count):
                marker_element_node = None
                if XML_OUTPUT:
                    marker_element_node = TAG.xml_doc.createElement('element')
                    marker_element_node.setAttribute('index', str(local_marker_idx))
                    marker_node.appendChild(marker_element_node)

                local_marker = MODEL.Markers()
                local_marker.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(marker_element_node, "name"))
                local_marker.node_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(marker_element_node, "node index", None, MODEL.mod2_body.nodes_tag_block.count, "model_node_block"))
                input_stream.read(2) # Padding?
                local_marker.rotation = TAG.read_quaternion(input_stream, TAG, tag_format.XMLData(marker_element_node, "rotation"), True)
                local_marker.translation = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(marker_element_node, "translation"), True)
                input_stream.read(16) # Padding?

                permutation.local_markers.append(local_marker)

    MODEL.geometries = []
    geometry_node = tag_format.get_xml_node(XML_OUTPUT, MODEL.mod2_body.geometries_tag_block.count, tag_node, "name", "geometries")
    for geometry_idx in range(MODEL.mod2_body.geometries_tag_block.count):
        geometry_element_node = None
        if XML_OUTPUT:
            geometry_element_node = TAG.xml_doc.createElement('element')
            geometry_element_node.setAttribute('index', str(geometry_idx))
            geometry_node.appendChild(geometry_element_node)

        geometry = MODEL.Geometries()
        geometry.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(geometry_element_node, "flags", []))
        input_stream.read(32) # Padding?
        geometry.parts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(geometry_element_node, "parts"))

        MODEL.geometries.append(geometry)

    for geo_idx, geometry in enumerate(MODEL.geometries):
        geometry_element_node = None
        if XML_OUTPUT:
            geometry_element_node = geometry_node.childNodes[geo_idx]

        geometry.parts = []
        part_node = tag_format.get_xml_node(XML_OUTPUT, geometry.parts_tag_block.count, geometry_element_node, "name", "parts")
        for part_idx in range(geometry.parts_tag_block.count):
            part_element_node = None
            if XML_OUTPUT:
                part_element_node = TAG.xml_doc.createElement('element')
                part_element_node.setAttribute('index', str(part_idx))
                part_node.appendChild(part_element_node)

            part = MODEL.Parts()
            part.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(part_element_node, "flags", PartFlags))
            part.shader_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(part_element_node, "shader index", None, MODEL.mod2_body.shaders_tag_block.count, "model_shader_reference_block"))
            part.previous_part_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "prev filthy part index"))
            part.next_part_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "next filthy part index"))
            part.centroid_primary_node = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(part_element_node, "centroid primary node"))
            part.centroid_secondary_node = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(part_element_node, "centroid secondary node"))
            part.centroid_primary_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(part_element_node, "centroid primary weight"))
            part.centroid_secondary_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(part_element_node, "centroid secondary weight"))
            part.centroid_translation = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(part_element_node, "centroid"))
            part.uncompressed_vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(part_element_node, "uncompressed vertices"))
            part.compressed_vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(part_element_node, "compressed vertices"))
            part.triangles_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(part_element_node, "triangles"))
            input_stream.read(39) # Padding

            part.local_node_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "num_nodes"))
            part.local_nodes = []
            for local_node_idx in range(24):
                part.local_nodes.append(TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "node index")))

            geometry.parts.append(part)

        for part_idx, part in enumerate(geometry.parts):
            part_element_node = None
            if XML_OUTPUT:
                part_element_node = part_node.childNodes[part_idx]

            part.uncompressed_vertices = []
            part.compressed_vertices = []
            part.triangles = []
            uncompressed_vertex_node = tag_format.get_xml_node(XML_OUTPUT, part.uncompressed_vertices_tag_block.count, part_element_node, "name", "uncompressed vertices")
            compressed_vertex_node = tag_format.get_xml_node(XML_OUTPUT, part.compressed_vertices_tag_block.count, part_element_node, "name", "compressed vertices")
            triangle_node = tag_format.get_xml_node(XML_OUTPUT, part.triangles_tag_block.count, part_element_node, "name", "triangles")
            for uncompressed_vertex_idx in range(part.uncompressed_vertices_tag_block.count):
                uncompressed_vertex_element_node = None
                if XML_OUTPUT:
                    uncompressed_vertex_element_node = TAG.xml_doc.createElement('element')
                    uncompressed_vertex_element_node.setAttribute('index', str(uncompressed_vertex_idx))
                    uncompressed_vertex_node.appendChild(uncompressed_vertex_element_node)

                uncompressed_vertex = MODEL.Vertices()
                uncompressed_vertex.translation = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(uncompressed_vertex_element_node, "position"), True)
                uncompressed_vertex.normal = TAG.read_vector(input_stream, TAG, tag_format.XMLData(uncompressed_vertex_element_node, "normal"))
                uncompressed_vertex.binormal = TAG.read_vector(input_stream, TAG, tag_format.XMLData(uncompressed_vertex_element_node, "binormal"))
                uncompressed_vertex.tangent = TAG.read_vector(input_stream, TAG, tag_format.XMLData(uncompressed_vertex_element_node, "tangent"))
                uncompressed_vertex.UV = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(uncompressed_vertex_element_node, "texture coords"))
                uncompressed_vertex.node_0_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(uncompressed_vertex_element_node, "node0 index"))
                uncompressed_vertex.node_1_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(uncompressed_vertex_element_node, "node1 index"))
                uncompressed_vertex.node_0_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(uncompressed_vertex_element_node, "node0 weight"))
                uncompressed_vertex.node_1_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(uncompressed_vertex_element_node, "node1 weight"))

                part.uncompressed_vertices.append(uncompressed_vertex)

            for compressed_vertex_idx in range(part.compressed_vertices_tag_block.count):
                compressed_vertex_element_node = None
                if XML_OUTPUT:
                    compressed_vertex_element_node = TAG.xml_doc.createElement('element')
                    compressed_vertex_element_node.setAttribute('index', str(compressed_vertex_idx))
                    compressed_vertex_node.appendChild(compressed_vertex_element_node)

                compressed_vertex = MODEL.Vertices()
                compressed_vertex.translation = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(compressed_vertex_element_node, "position"), True)
                compressed_vertex.normal = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(compressed_vertex_element_node, "normal[11.11.10-bit]"))
                compressed_vertex.binormal = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(compressed_vertex_element_node, "binormal[11.11.10-bit]"))
                compressed_vertex.tangent = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(compressed_vertex_element_node, "tangent[11.11.10-bit]"))
                U = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(compressed_vertex_element_node, "texture coordinate u[16-bit]"))
                V = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(compressed_vertex_element_node, "texture coordinate v[16-bit]"))
                compressed_vertex.UV = (U, V)
                compressed_vertex.node_0_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(compressed_vertex_element_node, "node0 index(x3)"))
                compressed_vertex.node_1_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(compressed_vertex_element_node, "node1 index(x3)"))
                compressed_vertex.node_0_weight = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(compressed_vertex_element_node, "node0 weight[16-bit]"))

                part.compressed_vertices.append(compressed_vertex)

            for triangle_idx in range(part.triangles_tag_block.count):
                triangle_element_node = None
                if XML_OUTPUT:
                    triangle_element_node = TAG.xml_doc.createElement('element')
                    triangle_element_node.setAttribute('index', str(triangle_idx))
                    triangle_node.appendChild(triangle_element_node)

                triangle = MODEL.Triangle()
                triangle.v0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(triangle_element_node, "vertex0 index"))
                triangle.v1 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(triangle_element_node, "vertex1 index"))
                triangle.v2 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(triangle_element_node, "vertex2 index"))

                part.triangles.append(triangle)

    MODEL.shaders = []
    shader_node = tag_format.get_xml_node(XML_OUTPUT, MODEL.mod2_body.shaders_tag_block.count, tag_node, "name", "shaders")
    for shader_idx in range(MODEL.mod2_body.shaders_tag_block.count):
        shader_element_node = None
        if XML_OUTPUT:
            shader_element_node = TAG.xml_doc.createElement('element')
            shader_element_node.setAttribute('index', str(shader_idx))
            shader_node.appendChild(shader_element_node)

        shader = MODEL.Shader()
        shader.tag_ref = TAG.TagRef().read(input_stream, TAG)
        shader.permutation_index = TAG.read_signed_short(input_stream, TAG)
        input_stream.read(14)

        MODEL.shaders.append(shader)

    for shader_idx, shader in enumerate(MODEL.shaders):
        if shader.tag_ref.name_length > 0:
            shader.tag_ref.name = TAG.read_variable_string(input_stream, shader.tag_ref.name_length, TAG)

    if XML_OUTPUT:
        for shader_idx, shader in enumerate(MODEL.shaders):
            shader_element_node = shader_node.childNodes[shader_idx]

            shader.tag_ref.create_xml_node(tag_format.XMLData(shader_element_node, "shader"))
            tag_format.append_xml_node(tag_format.XMLData(shader_element_node, "permutation"), "short integer", shader.permutation_index)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, MODEL.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return MODEL
