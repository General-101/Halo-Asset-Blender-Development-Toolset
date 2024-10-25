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

from enum import Flag, auto
from mathutils import Vector, Quaternion

class ModelFlags(Flag):
    blend_shared_normals = auto()
    parts_have_local_nodes = auto()
    ignore_skinning = auto()

class PermutationFlags(Flag):
    cannot_be_chosen_randomly = auto()

class PartFlags(Flag):
    stripped_internal = auto()
    zoner = auto()

class ModelAsset():
    def __init__(self, version=8200, header=None, markers=None, nodes=None, transforms=None, regions=None, geometries=None, shaders=None, flags=0, node_list_checksum=0, 
                 superhigh_detail_cutoff=0.0, high_detail_cutoff=0.0, medium_detail_cutoff=0.0, low_detail_cutoff=0.0, superlow_cutoff=0.0, superhigh_detail_nodes=0, 
                 high_detail_nodes=0, medium_detail_nodes=0, low_detail_nodes=0, superlow_nodes=0, base_map_u_scale=0.0, base_map_v_scale=0.0, markers_tag_block=None, 
                 nodes_tag_block=None, regions_tag_block=None, geometries_tag_block=None, shaders_tag_block=None):
        self.version = version
        self.header = header
        self.markers = markers
        self.nodes = nodes
        self.transforms = transforms
        self.regions = regions
        self.geometries = geometries
        self.shaders = shaders
        self.flags = flags
        self.node_list_checksum = node_list_checksum
        self.superhigh_detail_cutoff = superhigh_detail_cutoff
        self.high_detail_cutoff = high_detail_cutoff
        self.medium_detail_cutoff = medium_detail_cutoff
        self.low_detail_cutoff = low_detail_cutoff
        self.superlow_cutoff = superlow_cutoff
        self.superhigh_detail_nodes = superhigh_detail_nodes
        self.high_detail_nodes = high_detail_nodes
        self.medium_detail_nodes = medium_detail_nodes
        self.low_detail_nodes = low_detail_nodes
        self.superlow_nodes = superlow_nodes
        self.base_map_u_scale = base_map_u_scale
        self.base_map_v_scale = base_map_v_scale
        self.markers_tag_block = markers_tag_block
        self.nodes_tag_block = nodes_tag_block
        self.regions_tag_block = regions_tag_block
        self.geometries_tag_block = geometries_tag_block
        self.shaders_tag_block = shaders_tag_block

    class StubbsUnknown:
        def __init__(self, name="", unknown0=1.0, unknown1=1.0):
            self.name = name
            self.unknown0 = unknown0
            self.unknown1 = unknown1

    class Markers:
        def __init__(self, name="", magic_identifier=0, instance_tag_block=None, instances=None):
            self.name = name
            self.magic_identifier = magic_identifier
            self.instance_tag_block = instance_tag_block
            self.instances = instances

    class Instances:
        def __init__(self, region_index=0, permutation_index=0, node_index=0, translation=Vector(), rotation=Quaternion()):
            self.region_index = region_index
            self.permutation_index = permutation_index
            self.node_index = node_index
            self.translation = translation
            self.rotation = rotation

    class Nodes:
        def __init__(self, name="", sibling=0, child=0, parent=0, distance_from_parent=0.0):
            self.name = name
            self.sibling = sibling
            self.child = child
            self.parent = parent
            self.distance_from_parent = distance_from_parent

    class Transform:
        def __init__(self, translation=Vector, rotation=Quaternion()):
            self.translation = translation
            self.rotation = rotation

    class Regions:
        def __init__(self, name="", permutation_tag_block=None, permutations=None):
            self.name = name
            self.permutation_tag_block = permutation_tag_block
            self.permutations = permutations

    class Permutations:
        def __init__(self, name="", flags=0, superlow_geometry_block=0, low_geometry_block=0, medium_geometry_block=0, high_geometry_block=0, superhigh_geometry_block=0,
                     local_marker_tag_block=None, local_markers=None):
            self.name = name
            self.flags = flags
            self.superlow_geometry_block = superlow_geometry_block
            self.low_geometry_block = low_geometry_block
            self.medium_geometry_block = medium_geometry_block
            self.high_geometry_block = high_geometry_block
            self.superhigh_geometry_block = superhigh_geometry_block
            self.local_marker_tag_block = local_marker_tag_block
            self.local_markers = local_markers

    class LocalMarkers:
        def __init__(self, name="", node_index=0, rotation=Quaternion(), translation=Vector()):
            self.name = name
            self.node_index = node_index
            self.rotation = rotation
            self.translation = translation

    class Geometries:
        def __init__(self, flags=0, parts_tag_block=None, parts=None, visited=False):
            self.flags = flags
            self.parts_tag_block = parts_tag_block
            self.parts = parts
            self.visited = visited

    class Parts:
        def __init__(self, flags=0, shader_index=0, previous_part_index=0, next_part_index=0, centroid_primary_node=0, centroid_secondary_node=0, centroid_primary_weight=0.0,
                     centroid_secondary_weight=0, centroid_translation=Vector(), uncompressed_vertices_tag_block=None, compressed_vertices_tag_block=None,
                     triangles_tag_block=None, local_node_count=0, local_nodes=None, uncompressed_vertices=None, compressed_vertices=None, triangles=None):
            self.flags = flags
            self.shader_index = shader_index
            self.previous_part_index = previous_part_index
            self.next_part_index = next_part_index
            self.centroid_primary_node = centroid_primary_node
            self.centroid_secondary_node = centroid_secondary_node
            self.centroid_primary_weight = centroid_primary_weight
            self.centroid_secondary_weight = centroid_secondary_weight
            self.centroid_translation = centroid_translation
            self.uncompressed_vertices_tag_block = uncompressed_vertices_tag_block
            self.compressed_vertices_tag_block = compressed_vertices_tag_block
            self.triangles_tag_block = triangles_tag_block
            self.local_node_count = local_node_count
            self.local_nodes = local_nodes
            self.uncompressed_vertices = uncompressed_vertices
            self.compressed_vertices = compressed_vertices
            self.triangles = triangles

    class Vertices:
        def __init__(self, translation=Vector(), normal=Vector(), binormal=Vector(), tangent=Vector(), UV=(0.0, 0.0), node_0_index=0, node_1_index=0, node_0_weight=0.0,
                     node_1_weight=0.0):
            self.translation = translation
            self.normal = normal
            self.binormal = binormal
            self.tangent = tangent
            self.UV = UV
            self.node_0_index = node_0_index
            self.node_1_index = node_1_index
            self.node_0_weight = node_0_weight
            self.node_1_weight = node_1_weight

    class Triangle:
        def __init__(self, v0=0, v1=0, v2=0):
            self.v0 = v0
            self.v1 = v1
            self.v2 = v2

    class Groups:
        def __init__(self, count=0, node_index=0, secondary_node_index=0):
            self.count = count
            self.node_index = node_index
            self.secondary_node_index = secondary_node_index

    class Shader:
        def __init__(self, tag_ref=None, permutation_index=0):
            self.tag_ref = tag_ref
            self.permutation_index = permutation_index
