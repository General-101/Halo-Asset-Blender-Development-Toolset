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

import struct

from .format_retail import ModelAsset
from mathutils import Vector, Quaternion

DEBUG_PARSER = False
DEBUG_HEADER = True
DEBUG_BODY = True
DEBUG_MARKERS = True
DEBUG_INSTANCES = True
DEBUG_NODES = True
DEBUG_REGIONS = True
DEBUG_PERMUTATIONS = True
DEBUG_LOCAL_MARKERS = True
DEBUG_GEOMETRIES = True
DEBUG_PARTS = True
DEBUG_UNCOMPRESSED_VERTEX = True
DEBUG_COMPRESSED_VERTEX = True
DEBUG_TRIANGLE = True
DEBUG_SHADERS = True

def process_file_mode_retail(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    MODEL = ModelAsset()

    header_struct = struct.unpack('>hbb32s4sIIIIHbb4s', input_stream.read(64))
    MODEL.header = TAG.Header()
    MODEL.header.unk1 = header_struct[0]
    MODEL.header.flags = header_struct[1]
    MODEL.header.type = header_struct[2]
    MODEL.header.name = header_struct[3].decode().rstrip('\x00')
    MODEL.header.tag_group = header_struct[4].decode().rstrip('\x00')
    MODEL.header.checksum = header_struct[5]
    MODEL.header.data_offset = header_struct[6]
    MODEL.header.data_length = header_struct[7]
    MODEL.header.unk2 = header_struct[8]
    MODEL.header.version = header_struct[9]
    MODEL.header.destination = header_struct[10]
    MODEL.header.plugin_handle = header_struct[11]
    MODEL.header.engine_tag = header_struct[12].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_HEADER:
        print(" ===== Tag Header ===== ")
        print("Unknown Value: ", MODEL.header.unk1)
        print("Flags: ", MODEL.header.flags)
        print("Type: ", MODEL.header.type)
        print("Name: ", MODEL.header.name)
        print("Tag Group: ", MODEL.header.tag_group)
        print("Checksum: ", MODEL.header.checksum)
        print("Data Offset: ", MODEL.header.data_offset)
        print("Data Length:", MODEL.header.data_length)
        print("Unknown Value: ", MODEL.header.unk2)
        print("Version: ", MODEL.header.version)
        print("Destination: ", MODEL.header.destination)
        print("Plugin Handle: ", MODEL.header.plugin_handle)
        print("Engine Tag: ", MODEL.header.engine_tag)
        print(" ")

    body_struct = struct.unpack('>IIfffffhhhhh10xff116xiIIiIIiIIiIIiII', input_stream.read(232))
    MODEL.mode_body = MODEL.ModelBody()
    MODEL.mode_body.flags = body_struct[0]
    MODEL.mode_body.node_list_checksum = body_struct[1]
    MODEL.mode_body.superhigh_detail_cutoff = body_struct[2]
    MODEL.mode_body.high_detail_cutoff = body_struct[3]
    MODEL.mode_body.medium_detail_cutoff = body_struct[4]
    MODEL.mode_body.low_detail_cutoff = body_struct[5]
    MODEL.mode_body.superlow_cutoff = body_struct[6]
    MODEL.mode_body.superhigh_detail_nodes = body_struct[7]
    MODEL.mode_body.high_detail_nodes = body_struct[8]
    MODEL.mode_body.medium_detail_nodes = body_struct[9]
    MODEL.mode_body.low_detail_nodes = body_struct[10]
    MODEL.mode_body.superlow_nodes = body_struct[11]
    MODEL.mode_body.base_map_u_scale = body_struct[12]
    MODEL.mode_body.base_map_v_scale = body_struct[13]
    MODEL.mode_body.markers_tag_block = TAG.TagBlock(body_struct[14], 256, body_struct[15], body_struct[16])
    MODEL.mode_body.nodes_tag_block = TAG.TagBlock(body_struct[17], 64, body_struct[18], body_struct[19])
    MODEL.mode_body.regions_tag_block = TAG.TagBlock(body_struct[20], 32, body_struct[21], body_struct[22])
    MODEL.mode_body.geometries_tag_block = TAG.TagBlock(body_struct[23], 256, body_struct[24], body_struct[25])
    MODEL.mode_body.shaders_tag_block = TAG.TagBlock(body_struct[26], 256, body_struct[27], body_struct[28])

    if DEBUG_PARSER and DEBUG_BODY:
        print(" ===== Mode Body ===== ")
        print("Flags: ", MODEL.mode_body.flags)
        print("Node List Checksum: ", MODEL.mode_body.node_list_checksum)
        print("SuperHigh Detail Cutoff: ", MODEL.mode_body.superhigh_detail_cutoff)
        print("High Detail Cutoff: ", MODEL.mode_body.high_detail_cutoff)
        print("Medium Detail Cutoff: ", MODEL.mode_body.medium_detail_cutoff)
        print("Low Detail Cutoff: ", MODEL.mode_body.low_detail_cutoff)
        print("SuperLow Cutoff: ", MODEL.mode_body.superlow_cutoff)
        print("SuperHigh Detail Nodes: ", MODEL.mode_body.superhigh_detail_nodes)
        print("High Detail Nodes: ", MODEL.mode_body.high_detail_nodes)
        print("Medium Detail Nodes: ", MODEL.mode_body.medium_detail_nodes)
        print("Low Detail Nodes: ", MODEL.mode_body.low_detail_nodes)
        print("SuperLow Nodes: ", MODEL.mode_body.superlow_nodes)
        print("Base Map U Scale: ", MODEL.mode_body.base_map_u_scale)
        print("Base Map V Scale: ", MODEL.mode_body.base_map_v_scale)
        print("Marker Tag Block Count: ", MODEL.mode_body.markers_tag_block.count)
        print("Marker Tag Block Maximum Count: ", MODEL.mode_body.markers_tag_block.maximum_count)
        print("Marker Tag Block Address: ", MODEL.mode_body.markers_tag_block.address)
        print("Marker Tag Block Definition: ", MODEL.mode_body.markers_tag_block.definition)
        print("Nodes Tag Block Count: ", MODEL.mode_body.nodes_tag_block.count)
        print("Nodes Tag Block Maximum Count: ", MODEL.mode_body.nodes_tag_block.maximum_count)
        print("Nodes Tag Block Address: ", MODEL.mode_body.nodes_tag_block.address)
        print("Nodes Tag Block Definition: ", MODEL.mode_body.nodes_tag_block.definition)
        print("Regions Tag Block Count: ", MODEL.mode_body.regions_tag_block.count)
        print("Regions Tag Block Maximum Count: ", MODEL.mode_body.regions_tag_block.maximum_count)
        print("Regions Tag Block Address: ", MODEL.mode_body.regions_tag_block.address)
        print("Regions Tag Block Definition: ", MODEL.mode_body.regions_tag_block.definition)
        print("Geometries Tag Block Count: ", MODEL.mode_body.geometries_tag_block.count)
        print("Geometries Tag Block Maximum Count: ", MODEL.mode_body.geometries_tag_block.maximum_count)
        print("Geometries Tag Block Address: ", MODEL.mode_body.geometries_tag_block.address)
        print("Geometries Tag Block Definition: ", MODEL.mode_body.geometries_tag_block.definition)
        print("Shaders Tag Block Count: ", MODEL.mode_body.shaders_tag_block.count)
        print("Shaders Tag Block Maximum Count: ", MODEL.mode_body.shaders_tag_block.maximum_count)
        print("Shaders Tag Block Address: ", MODEL.mode_body.shaders_tag_block.address)
        print("Shaders Tag Block Definition: ", MODEL.mode_body.shaders_tag_block.definition)
        print(" ")

    for marker_idx in range(MODEL.mode_body.markers_tag_block.count):
        marker_struct = struct.unpack('>32sH18xiII', input_stream.read(64))
        marker = MODEL.Markers()
        marker.name = marker_struct[0].decode().rstrip('\x00')
        marker.magic_identifier = marker_struct[1]
        marker.instance_tag_block = TAG.TagBlock(marker_struct[2], 32, marker_struct[3], marker_struct[4])

        MODEL.markers.append(marker)

    for marker in MODEL.markers:
        instances = []
        for instance_idx in range(marker.instance_tag_block.count):
            instance_struct = struct.unpack('>bbb1xfffffff', input_stream.read(32))
            instance = MODEL.Instances()
            instance.region_index = instance_struct[0]
            instance.permutation_index = instance_struct[1]
            instance.node_index = instance_struct[2]
            instance.translation = Vector((instance_struct[3], instance_struct[4], instance_struct[5])) * 100
            instance.rotation = Quaternion((instance_struct[9], instance_struct[6], instance_struct[7], instance_struct[8])).inverted()

            instances.append(instance)

        marker.instances = instances

    if DEBUG_PARSER and DEBUG_MARKERS:
        print(" ===== Markers ===== ")
        for marker_idx, marker in enumerate(MODEL.markers):
            print(" ===== Marker %s ===== " % marker_idx)
            print("Marker Name: ", marker.name)
            print("Marker Magic Value: ", marker.magic_identifier)
            print("Instance Tag Block Count: ", marker.instance_tag_block.count)
            print("Instance Tag Block Maximum Count: ", marker.instance_tag_block.maximum_count)
            print("Instance Tag Block Address: ", marker.instance_tag_block.address)
            print("Instance Tag Block Definition: ", marker.instance_tag_block.definition)
            print(" ")
            if DEBUG_INSTANCES:
                for instance_idx, instance in enumerate(marker.instances):
                    print(" ===== Instance %s ===== " % instance_idx)
                    print("Instance Region Index: ", instance.region_index)
                    print("Instance Permutation Index: ", instance.permutation_index)
                    print("Instance Node Index: ", instance.node_index)
                    print("Instance Translation: ", instance.translation)
                    print("Instance Rotation: ", instance.rotation)
                    print(" ")

    transforms = []
    for nodes_idx in range(MODEL.mode_body.nodes_tag_block.count):
        node_struct = struct.unpack('>32shhh2xffffffff84x', input_stream.read(156))
        node = MODEL.Nodes()
        transform = MODEL.Transform()
        node.name = node_struct[0].decode().rstrip('\x00')
        node.sibling = node_struct[1]
        node.child = node_struct[2]
        node.parent = node_struct[3]
        transform.translation = Vector((node_struct[4], node_struct[5], node_struct[6])) * 100
        transform.rotation = Quaternion((node_struct[10], node_struct[7], node_struct[8], node_struct[9])).inverted()
        node.distance_from_parent = node_struct[11] * 100

        MODEL.nodes.append(node)
        transforms.append(transform)

    MODEL.transforms.append(transforms)

    if DEBUG_PARSER and DEBUG_NODES:
        print(" ===== Nodes ===== ")
        for node_idx, node in enumerate(MODEL.nodes):
            print(" ===== Node %s ===== " % node_idx)
            print("Node Name: ", node.name)
            print("Node Sibling: ", node.sibling)
            print("Node Child: ", node.child)
            print("Node Parent: ", node.parent)
            print("Node Translation: ", MODEL.transforms[0][node_idx].translation)
            print("Node Rotation: ", MODEL.transforms[0][node_idx].rotation)
            print("Node Distance From Parent: ", node.distance_from_parent)
            print(" ")

    for region_idx in range(MODEL.mode_body.regions_tag_block.count):
        region_struct = struct.unpack('>32s32xiII', input_stream.read(76))
        region = MODEL.Regions()
        region.name = region_struct[0].decode().rstrip('\x00')
        region.permutation_tag_block = TAG.TagBlock(region_struct[1], 32, region_struct[2], region_struct[3])

        MODEL.regions.append(region)

    for region in MODEL.regions:
        permutations = []
        for permutation_idx in range(region.permutation_tag_block.count):
            permutation_struct = struct.unpack('>32sIH26xhhhhh2xiII', input_stream.read(88))
            permutation = MODEL.Permutations()
            permutation.name = permutation_struct[0].decode().rstrip('\x00')
            permutation.flags = permutation_struct[1]
            permutation.permutation_set = permutation_struct[2]
            permutation.superlow_geometry_block = permutation_struct[3]
            permutation.low_geometry_block = permutation_struct[4]
            permutation.medium_geometry_block = permutation_struct[5]
            permutation.high_geometry_block = permutation_struct[6]
            permutation.superhigh_geometry_block = permutation_struct[7]
            permutation.local_marker_tag_block = TAG.TagBlock(permutation_struct[8], 32, permutation_struct[9], permutation_struct[10])

            permutations.append(permutation)

        for permutation in permutations:
            local_markers = []
            for local_marker_idx in range(permutation.local_marker_tag_block.count):
                local_marker_struct = struct.unpack('>32sh2xfffffff16x', input_stream.read(80))
                local_marker = MODEL.LocalMarkers()
                local_marker.name = local_marker_struct[0].decode().rstrip('\x00')
                local_marker.node_index = local_marker_struct[1]
                local_marker.rotation = Quaternion((local_marker_struct[5], local_marker_struct[2], local_marker_struct[3], local_marker_struct[4])).inverted()
                local_marker.translation = Vector((local_marker_struct[6], local_marker_struct[7], local_marker_struct[8])) * 100

                local_markers.append(local_marker)

            permutation.local_markers = local_markers

        region.permutations = permutations

    if DEBUG_PARSER and DEBUG_REGIONS:
        print(" ===== Regions ===== ")
        for region_idx, region in enumerate(MODEL.regions):
            print(" ===== Region %s ===== " % region_idx)
            print("Region Name: ", region.name)
            print("Permutation Tag Block Count: ", region.permutation_tag_block.count)
            print("Permutation Tag Block Maximum Count: ", region.permutation_tag_block.maximum_count)
            print("Permutation Tag Block Address: ", region.permutation_tag_block.address)
            print("Permutation Tag Block Definition: ", region.permutation_tag_block.definition)
            print(" ")
            if DEBUG_PERMUTATIONS:
                for permutation_idx, permutation in enumerate(region.permutations):
                    print(" ===== Permutation %s ===== " % permutation_idx)
                    print("Permutation Name: ", permutation.name)
                    print("Permutation Flags: ", permutation.flags)
                    print("Permutation Set: ", permutation.permutation_set)
                    print("Permutation SuperLow Geometry Block Index: ", permutation.superlow_geometry_block)
                    print("Permutation Low Geometry Block Index: ", permutation.low_geometry_block)
                    print("Permutation Medium Geometry Block Index: ", permutation.medium_geometry_block)
                    print("Permutation High Geometry Block Index: ", permutation.high_geometry_block)
                    print("Permutation SuperHigh Geometry Block Index: ", permutation.superhigh_geometry_block)
                    print("Local Marker Tag Block Count: ", permutation.local_marker_tag_block.count)
                    print("Local Marker Tag Block Maximum Count: ", permutation.local_marker_tag_block.maximum_count)
                    print("Local Marker Tag Block Address: ", permutation.local_marker_tag_block.address)
                    print("Local Marker Tag Block Definition: ", permutation.local_marker_tag_block.definition)
                    print(" ")
                    if DEBUG_LOCAL_MARKERS:
                        for local_marker_idx, local_marker in enumerate(permutation.local_markers):
                            print(" ===== Local Marker %s ===== " % local_marker_idx)
                            print("Local Marker Name: ", local_marker.name)
                            print("Local Marker Node Index: ", local_marker.node_index)
                            print("Local Marker Rotation: ", local_marker.rotation)
                            print("Local Marker Translation: ", local_marker.translation)
                            print(" ")


    for geometry_idx in range(MODEL.mode_body.geometries_tag_block.count):
        geometry_struct = struct.unpack('>36xiII', input_stream.read(48))
        geometry = MODEL.Geometries()
        geometry.parts_tag_block = TAG.TagBlock(geometry_struct[0], 32, geometry_struct[1], geometry_struct[2])

        MODEL.geometries.append(geometry)

    for geometry in MODEL.geometries:
        parts = []
        for part_idx in range(geometry.parts_tag_block.count):
            part_struct = struct.unpack('>IhbbhhfffffiIIiIIiIIH2xIIIH2xI4xII', input_stream.read(104))
            part = MODEL.Parts()
            part.flags = part_struct[0]
            part.shader_index = part_struct[1]
            part.previous_part_index = part_struct[2]
            part.next_part_index = part_struct[3]
            part.centroid_primary_node = part_struct[4]
            part.centroid_secondary_node = part_struct[5]
            part.centroid_primary_weight = part_struct[6]
            part.centroid_secondary_weight = part_struct[7]
            part.centroid_translation = Vector((part_struct[8], part_struct[9], part_struct[10])) * 100
            part.uncompressed_vertices_tag_block = TAG.TagBlock(part_struct[11], 32767, part_struct[12], part_struct[13])
            part.compressed_vertices_tag_block = TAG.TagBlock(part_struct[14], 32767, part_struct[15], part_struct[16])
            part.triangles_tag_block = TAG.TagBlock(part_struct[17], 32767, part_struct[18], part_struct[19])
            part.index_type = part_struct[20]
            part.index_count = part_struct[21]
            part.indices_offset = part_struct[22]
            part.indices_magic_offset = part_struct[23]
            part.vertex_type = part_struct[24]
            part.vertex_count = part_struct[25]
            part.vertices_offset = part_struct[26]
            part.vertices_magic_offset = part_struct[27]

            parts.append(part)

        for part in parts:
            uncompressed_vertices = []
            compressed_vertices = []
            triangles = []
            for uncompressed_vertex in range(part.uncompressed_vertices_tag_block.count):
                uncompressed_vertex_struct = struct.unpack('>ffffffffffffffhhff', input_stream.read(68))
                uncompressed_vertex = MODEL.Vertices()
                uncompressed_vertex.translation = Vector((uncompressed_vertex_struct[0], uncompressed_vertex_struct[1], uncompressed_vertex_struct[2])) * 100
                uncompressed_vertex.normal = Vector((uncompressed_vertex_struct[3], uncompressed_vertex_struct[4], uncompressed_vertex_struct[5]))
                uncompressed_vertex.binormal = Vector((uncompressed_vertex_struct[6], uncompressed_vertex_struct[7], uncompressed_vertex_struct[8]))
                uncompressed_vertex.tangent = Vector((uncompressed_vertex_struct[9], uncompressed_vertex_struct[10], uncompressed_vertex_struct[11]))
                uncompressed_vertex.UV = (uncompressed_vertex_struct[12], uncompressed_vertex_struct[13])
                uncompressed_vertex.node_0_index = uncompressed_vertex_struct[14]
                uncompressed_vertex.node_1_index = uncompressed_vertex_struct[15]
                uncompressed_vertex.node_0_weight = uncompressed_vertex_struct[16]
                uncompressed_vertex.node_1_weight = uncompressed_vertex_struct[17]

                uncompressed_vertices.append(uncompressed_vertex)

            for compressed_vertex in range(part.compressed_vertices_tag_block.count):
                compressed_vertex_struct = struct.unpack('>fffIIIhhbbh', input_stream.read(32))
                compressed_vertex = MODEL.Vertices()
                compressed_vertex.translation = Vector((compressed_vertex_struct[0], compressed_vertex_struct[1], compressed_vertex_struct[2])) * 100
                compressed_vertex.normal = compressed_vertex_struct[3]
                compressed_vertex.binormal = compressed_vertex_struct[4]
                compressed_vertex.tangent = compressed_vertex_struct[5]
                compressed_vertex.UV = (compressed_vertex_struct[6], compressed_vertex_struct[7])
                compressed_vertex.node_0_index = compressed_vertex_struct[8]
                compressed_vertex.node_1_index = compressed_vertex_struct[9]
                compressed_vertex.node_0_weight = compressed_vertex_struct[10]

                compressed_vertices.append(compressed_vertex)

            for triangle in range(part.triangles_tag_block.count):
                triangle_struct = struct.unpack('>hhh', input_stream.read(6))
                triangle = MODEL.Triangle()
                triangle.v0 = triangle_struct[0]
                triangle.v1 = triangle_struct[1]
                triangle.v2 = triangle_struct[2]

                triangles.append(triangle)

            part.uncompressed_vertices = uncompressed_vertices
            part.compressed_vertices = compressed_vertices
            part.triangles = triangles

        geometry.parts = parts

    if DEBUG_PARSER and DEBUG_GEOMETRIES:
        print(" ===== Geometry ===== ")
        for geometry_idx, geometry in enumerate(MODEL.geometries):
            print(" ===== Geometry %s ===== " % geometry_idx)
            print("Parts Tag Block Count: ", geometry.parts_tag_block.count)
            print("Parts Tag Block Maximum Count: ", geometry.parts_tag_block.maximum_count)
            print("Parts Tag Block Address: ", geometry.parts_tag_block.address)
            print("Parts Tag Block Definition: ", geometry.parts_tag_block.definition)
            print(" ")
            if DEBUG_PARTS:
                for part_idx, part in enumerate(geometry.parts):
                    print(" ===== Part %s ===== " % part_idx)
                    print("Flags: ", part.flags)
                    print("Shader Index: ", part.shader_index)
                    print("Previous Part Index: ", part.previous_part_index)
                    print("Next Part Index: ", part.next_part_index)
                    print("Centroid Secondary Node: ", part.centroid_primary_node)
                    print("Centroid Primary Node: ", part.centroid_secondary_node)
                    print("Centroid Secondary Weight: ", part.centroid_primary_weight)
                    print("Centroid Primary Weight: ", part.centroid_secondary_weight)
                    print("Centroid Translation: ", part.centroid_translation)
                    print("Uncompressed Vertices Tag Block Count: ", part.uncompressed_vertices_tag_block.count)
                    print("Uncompressed Vertices Tag Block Maximum Count: ", part.uncompressed_vertices_tag_block.maximum_count)
                    print("Uncompressed Vertices Tag Block Address: ", part.uncompressed_vertices_tag_block.address)
                    print("Uncompressed Vertices Tag Block Definition: ", part.uncompressed_vertices_tag_block.definition)
                    print("Compressed Vertices Tag Block Count: ", part.compressed_vertices_tag_block.count)
                    print("Compressed Vertices Tag Block Maximum Count: ", part.compressed_vertices_tag_block.maximum_count)
                    print("Compressed Vertices Tag Block Address: ", part.compressed_vertices_tag_block.address)
                    print("Compressed Vertices Tag Block Definition: ", part.compressed_vertices_tag_block.definition)
                    print("Triangles Tag Block Count: ", part.triangles_tag_block.count)
                    print("Triangles Tag Block Maximum Count: ", part.triangles_tag_block.maximum_count)
                    print("Triangles Tag Block Address: ", part.triangles_tag_block.address)
                    print("Triangles Tag Block Definition: ", part.triangles_tag_block.definition)
                    print("Index Type: ", part.index_type)
                    print("Index Count: ", part.index_count)
                    print("Indices Magic Offset: ", part.indices_magic_offset)
                    print("Indices Offset: ", part.indices_offset)
                    print("Vertex Type: ", part.vertex_type)
                    print("Vertex Count: ", part.vertex_count)
                    print("Vertices Magic Offset: ", part.vertices_magic_offset)
                    print("Vertices Offset: ", part.vertices_offset)
                    print("Local Node Count: ", part.local_node_count)
                    print("Local Nodes: ", part.local_nodes)
                    print(" ")
                    if DEBUG_UNCOMPRESSED_VERTEX:
                        for uncompressed_vertex_idx, uncompressed_vertex in enumerate(part.uncompressed_vertices):
                            print(" ===== Uncompressed Vertices %s ===== " % uncompressed_vertex_idx)
                            print("Uncompressed Translation: ", uncompressed_vertex.translation)
                            print("Uncompressed Normal: ", uncompressed_vertex.normal)
                            print("Uncompressed Binormal: ", uncompressed_vertex.binormal)
                            print("Uncompressed Tangent: ", uncompressed_vertex.tangent)
                            print("Uncompressed UV: ", uncompressed_vertex.UV)
                            print("Uncompressed Node 0 Index: ", uncompressed_vertex.node_0_index)
                            print("Uncompressed Node 1 Index: ", uncompressed_vertex.node_1_index)
                            print("Uncompressed Node 0 Weight: ", uncompressed_vertex.node_0_weight)
                            print("Uncompressed Node 1 Weight: ", uncompressed_vertex.node_1_weight)
                            print(" ")

                    if DEBUG_COMPRESSED_VERTEX:
                         for compressed_vertex_idx, compressed_vertex in enumerate(part.compressed_vertices):
                            print(" ===== Compressed Vertices %s ===== " % compressed_vertex_idx)
                            print("Compressed Translation: ", compressed_vertex.translation)
                            print("Compressed Normal: ", compressed_vertex.normal)
                            print("Compressed Binormal: ", compressed_vertex.binormal)
                            print("Compressed Tangent: ", compressed_vertex.tangent)
                            print("Compressed UV: ", compressed_vertex.UV)
                            print("Compressed Node 0 Index: ", compressed_vertex.node_0_index)
                            print("Compressed Node 1 Index: ", compressed_vertex.node_1_index)
                            print("Compressed Node 0 Weight: ", compressed_vertex.node_0_weight)
                            print(" ")

                    if DEBUG_TRIANGLE:
                        for triangle_idx, triangle in enumerate(part.triangles):
                            print(" ===== Triangle %s ===== " % triangle_idx)
                            print("Triangle V0: ", triangle.v0)
                            print("Triangle V1: ", triangle.v1)
                            print("Triangle V2: ", triangle.v2)
                            print(" ")

    shaders = []
    for shader_idx in range(MODEL.mode_body.shaders_tag_block.count):
        shader_struct = struct.unpack('>4siiIh14x', input_stream.read(32))
        shader = MODEL.Shaders()
        shader.tag_ref = TAG.TagRef(shader_struct[0].decode().rstrip('\x00'), "", shader_struct[2] + 1, shader_struct[1], shader_struct[3])
        shader.permutation_index = shader_struct[4]

        shaders.append(shader)

    for shader in shaders:
        tag_path = struct.unpack('>%ss' % shader.tag_ref.name_length, input_stream.read(shader.tag_ref.name_length))
        shader.tag_ref.name = tag_path[0].decode().rstrip('\x00')

    MODEL.shaders = shaders

    if DEBUG_PARSER and DEBUG_SHADERS:
        print(" ===== Shaders ===== ")
        for shader_idx, shader in enumerate(MODEL.shaders):
            print(" ===== Shader %s ===== " % shader_idx)
            print("Tag Reference Group: ", shader.tag_ref.tag_group)
            print("Tag Reference Name: ", shader.tag_ref.name)
            print("Tag Reference Name Length: ", shader.tag_ref.name_length)
            print("Tag Reference Salt: ", shader.tag_ref.salt)
            print("Tag Reference Index: ", shader.tag_ref.index)
            print("Permutation Index: ", shader.permutation_index)
            print(" ")

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    return MODEL
