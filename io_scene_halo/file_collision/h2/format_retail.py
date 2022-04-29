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

from enum import Flag, auto
from mathutils import Vector, Quaternion

class SurfaceFlags(Flag):
    Two_Sided = auto()
    Invisible = auto()
    Climbable = auto()
    Breakable = auto()
    Invalid = auto()
    Conveyor = auto()

class CollisionAsset():
    def __init__(self):
        self.header = None
        self.collision_body = None
        self.import_info_blocks = []
        self.errors = []
        self.flags = 0
        self.materials = []
        self.regions = []
        self.pathfinding_spheres = []
        self.nodes = []

    class CollisionBody:
        def __init__(self, import_info_tag_block=None, errors_tag_block=None, flags=0, materials_tag_block=None, regions_tag_block=None, pathfinding_spheres_tag_block=None, 
                     nodes_tag_block=None):
            self.import_info_tag_block = import_info_tag_block
            self.errors_tag_block = errors_tag_block
            self.flags = flags
            self.materials_tag_block = materials_tag_block
            self.regions_tag_block = regions_tag_block
            self.pathfinding_spheres_tag_block = pathfinding_spheres_tag_block
            self.nodes_tag_block = nodes_tag_block

    class ImportInfo:
        def __init__(self, build=0, version="", import_date="", culprit="", import_time="", files_tag_block=None, 
                     files=[]):
            self.build = build
            self.version = version
            self.import_date = import_date
            self.culprit = culprit
            self.import_time = import_time
            self.files_tag_block = files_tag_block
            self.files = files

    class Files:
        def __init__(self, path="", modification_date="", checksum=0, size=0, zipped_data=0, uncompressed_data=None):
            self.path = path
            self.modification_date = modification_date
            self.checksum = checksum
            self.size = size
            self.zipped_data = zipped_data
            self.uncompressed_data = uncompressed_data 

    class Error:
        def __init__(self, name="", report_type=0, flags=0, reports_tag_block=None, reports=[]):
            self.name = name
            self.report_type = report_type
            self.flags = flags
            self.reports_tag_block = reports_tag_block
            self.reports = reports

    class Report:
        def __init__(self, type=0, flags=0, text="", source_filename="", source_line_number=0, vertices_tag_block=None, vectors_tag_block=None, 
                     lines_tag_block=None, triangles_tag_block=None, quads_tag_block=None, comments_tag_block=None, vertices=[], vectors=[], lines=[], triangles=[], quads=[], 
                     comments=[], report_key=0, node_index=0, bounds_x=(0.0, 0.0), bounds_y=(0.0, 0.0), bounds_z=(0.0, 0.0), color=(0.0, 0.0, 0.0, 0.0)):
            self.type = type
            self.flags = flags
            self.text = text
            self.source_filename = source_filename
            self.source_line_number = source_line_number
            self.vertices_tag_block = vertices_tag_block
            self.vectors_tag_block = vectors_tag_block
            self.lines_tag_block = lines_tag_block
            self.triangles_tag_block = triangles_tag_block
            self.quads_tag_block = quads_tag_block
            self.comments_tag_block = comments_tag_block
            self.vertices = vertices
            self.vectors = vectors
            self.lines = lines
            self.triangles = triangles
            self.quads = quads
            self.comments = comments
            self.report_key = report_key
            self.node_index = node_index
            self.bounds_x = bounds_x
            self.bounds_y = bounds_y
            self.bounds_z = bounds_z
            self.color = color

    class ReportVertex:
        def __init__(self, position=Vector(), node_index_0=0, node_index_1=0, node_index_2=0, node_index_3=0, node_weight_0=0.0, node_weight_1=0.0, node_weight_2=0.0, 
                     node_weight_3=0.0, color=(0.0, 0.0, 0.0, 0.0), screen_size=0.0):
            self.position = position
            self.node_index_0 = node_index_0
            self.node_index_1 = node_index_1
            self.node_index_2 = node_index_2
            self.node_index_3 = node_index_3
            self.node_weight_0 = node_weight_0
            self.node_weight_1 = node_weight_1
            self.node_weight_2 = node_weight_2
            self.node_weight_3 = node_weight_3
            self.color = color
            self.screen_size = screen_size

    class ReportVector:
        def __init__(self, position=Vector(), node_index_0=0, node_index_1=0, node_index_2=0, node_index_3=0, node_weight_0=0.0, node_weight_1=0.0, node_weight_2=0.0, 
                     node_weight_3=0.0, color=(0.0, 0.0, 0.0, 0.0), normal=Vector(), screen_length=0.0):
            self.position = position
            self.node_index_0 = node_index_0
            self.node_index_1 = node_index_1
            self.node_index_2 = node_index_2
            self.node_index_3 = node_index_3
            self.node_weight_0 = node_weight_0
            self.node_weight_1 = node_weight_1
            self.node_weight_2 = node_weight_2
            self.node_weight_3 = node_weight_3
            self.color = color
            self.normal = normal
            self.screen_length = screen_length

    class ReportLine:
        def __init__(self, position_a=Vector(), node_index_a_0=0, node_index_a_1=0, node_index_a_2=0, node_index_a_3=0, node_weight_a_0=0.0, node_weight_a_1=0.0, 
                     node_weight_a_2=0.0, node_weight_a_3=0.0, position_b=Vector(), node_index_b_0=0, node_index_b_1=0, node_index_b_2=0, node_index_b_3=0, node_weight_b_0=0.0, 
                     node_weight_b_1=0.0, node_weight_b_2=0.0, node_weight_b_3=0.0, color=(0.0, 0.0, 0.0, 0.0)):
            self.position_a = position_a
            self.node_index_a_0 = node_index_a_0
            self.node_index_a_1 = node_index_a_1
            self.node_index_a_2 = node_index_a_2
            self.node_index_a_3 = node_index_a_3
            self.node_weight_a_0 = node_weight_a_0
            self.node_weight_a_1 = node_weight_a_1
            self.node_weight_a_2 = node_weight_a_2
            self.node_weight_a_3 = node_weight_a_3
            self.position_b = position_b
            self.node_index_b_0 = node_index_b_0
            self.node_index_b_1 = node_index_b_1
            self.node_index_b_2 = node_index_b_2
            self.node_index_b_3 = node_index_b_3
            self.node_weight_b_0 = node_weight_b_0
            self.node_weight_b_1 = node_weight_b_1
            self.node_weight_b_2 = node_weight_b_2
            self.node_weight_b_3 = node_weight_b_3
            self.color = color

    class ReportTriangle:
        def __init__(self, position_a=Vector(), node_index_a_0=0, node_index_a_1=0, node_index_a_2=0, node_index_a_3=0, node_weight_a_0=0.0, node_weight_a_1=0.0, 
                     node_weight_a_2=0.0, node_weight_a_3=0.0, position_b=Vector(), node_index_b_0=0, node_index_b_1=0, node_index_b_2=0, node_index_b_3=0, node_weight_b_0=0.0, 
                     node_weight_b_1=0.0, node_weight_b_2=0.0, node_weight_b_3=0.0, position_c=Vector(), node_index_c_0=0, node_index_c_1=0, node_index_c_2=0, node_index_c_3=0, 
                     node_weight_c_0=0.0, node_weight_c_1=0.0, node_weight_c_2=0.0, node_weight_c_3=0.0, color=(0.0, 0.0, 0.0, 0.0)):
            self.position_a = position_a
            self.node_index_a_0 = node_index_a_0
            self.node_index_a_1 = node_index_a_1
            self.node_index_a_2 = node_index_a_2
            self.node_index_a_3 = node_index_a_3
            self.node_weight_a_0 = node_weight_a_0
            self.node_weight_a_1 = node_weight_a_1
            self.node_weight_a_2 = node_weight_a_2
            self.node_weight_a_3 = node_weight_a_3
            self.position_b = position_b
            self.node_index_b_0 = node_index_b_0
            self.node_index_b_1 = node_index_b_1
            self.node_index_b_2 = node_index_b_2
            self.node_index_b_3 = node_index_b_3
            self.node_weight_b_0 = node_weight_b_0
            self.node_weight_b_1 = node_weight_b_1
            self.node_weight_b_2 = node_weight_b_2
            self.node_weight_b_3 = node_weight_b_3
            self.position_c = position_c
            self.node_index_c_0 = node_index_c_0
            self.node_index_c_1 = node_index_c_1
            self.node_index_c_2 = node_index_c_2
            self.node_index_c_3 = node_index_c_3
            self.node_weight_c_0 = node_weight_c_0
            self.node_weight_c_1 = node_weight_c_1
            self.node_weight_c_2 = node_weight_c_2
            self.node_weight_c_3 = node_weight_c_3
            self.color = color

    class ReportQuad:
        def __init__(self, position_a=Vector(), node_index_a_0=0, node_index_a_1=0, node_index_a_2=0, node_index_a_3=0, node_weight_a_0=0.0, node_weight_a_1=0.0, 
                     node_weight_a_2=0.0, node_weight_a_3=0.0, position_b=Vector(), node_index_b_0=0, node_index_b_1=0, node_index_b_2=0, node_index_b_3=0, node_weight_b_0=0.0, 
                     node_weight_b_1=0.0, node_weight_b_2=0.0, node_weight_b_3=0.0, position_c=Vector(), node_index_c_0=0, node_index_c_1=0, node_index_c_2=0, node_index_c_3=0, 
                     node_weight_c_0=0.0, node_weight_c_1=0.0, node_weight_c_2=0.0, node_weight_c_3=0.0, position_d=Vector(), node_index_d_0=0, node_index_d_1=0, 
                     node_index_d_2=0, node_index_d_3=0, node_weight_d_0=0.0, node_weight_d_1=0.0, node_weight_d_2=0.0, node_weight_d_3=0.0, color=(0.0, 0.0, 0.0, 0.0)):
            self.position_a = position_a
            self.node_index_a_0 = node_index_a_0
            self.node_index_a_1 = node_index_a_1
            self.node_index_a_2 = node_index_a_2
            self.node_index_a_3 = node_index_a_3
            self.node_weight_a_0 = node_weight_a_0
            self.node_weight_a_1 = node_weight_a_1
            self.node_weight_a_2 = node_weight_a_2
            self.node_weight_a_3 = node_weight_a_3
            self.position_b = position_b
            self.node_index_b_0 = node_index_b_0
            self.node_index_b_1 = node_index_b_1
            self.node_index_b_2 = node_index_b_2
            self.node_index_b_3 = node_index_b_3
            self.node_weight_b_0 = node_weight_b_0
            self.node_weight_b_1 = node_weight_b_1
            self.node_weight_b_2 = node_weight_b_2
            self.node_weight_b_3 = node_weight_b_3
            self.position_c = position_c
            self.node_index_c_0 = node_index_c_0
            self.node_index_c_1 = node_index_c_1
            self.node_index_c_2 = node_index_c_2
            self.node_index_c_3 = node_index_c_3
            self.node_weight_c_0 = node_weight_c_0
            self.node_weight_c_1 = node_weight_c_1
            self.node_weight_c_2 = node_weight_c_2
            self.node_weight_c_3 = node_weight_c_3
            self.position_d = position_d
            self.node_index_d_0 = node_index_d_0
            self.node_index_d_1 = node_index_d_1
            self.node_index_d_2 = node_index_d_2
            self.node_index_d_3 = node_index_d_3
            self.node_weight_d_0 = node_weight_d_0
            self.node_weight_d_1 = node_weight_d_1
            self.node_weight_d_2 = node_weight_d_2
            self.node_weight_d_3 = node_weight_d_3
            self.color = color

    class ReportComment:
        def __init__(self, text="", position=Vector(), node_index_0=0, node_index_1=0, node_index_2=0, node_index_3=0, node_weight_0=0.0, node_weight_1=0.0, node_weight_2=0.0, 
                     node_weight_3=0.0, color=(0.0, 0.0, 0.0, 0.0)):
            self.text = text
            self.position = position
            self.node_index_0 = node_index_0
            self.node_index_1 = node_index_1
            self.node_index_2 = node_index_2
            self.node_index_3 = node_index_3
            self.node_weight_0 = node_weight_0
            self.node_weight_1 = node_weight_1
            self.node_weight_2 = node_weight_2
            self.node_weight_3 = node_weight_3
            self.color = color

    class Region:
        def __init__(self, name="", permutation_tag_block=None, permutations=[]):
            self.name = name
            self.permutation_tag_block = permutation_tag_block
            self.permutations = permutations

    class Permutations:
        def __init__(self, name="", bsps_tag_block=None, bsps_physics_tag_block=None, bsps=[], bsp_physics=[]):
            self.name = name
            self.bsps_tag_block = bsps_tag_block
            self.bsps_physics_tag_block = bsps_physics_tag_block
            self.bsps = bsps
            self.bsp_physics = bsp_physics

    class BSP:
        def __init__(self, node_index=0, bsp3d_nodes_tag_block=None, planes_tag_block=None, leaves_tag_block=None, bsp2d_references_tag_block=None, bsp2d_nodes_tag_block=None,
                     surfaces_tag_block=None, edges_tag_block=None, vertices_tag_block=None, bsp3d_nodes=[], planes=[], leaves=[], bsp2d_references=[], bsp2d_nodes=[], surfaces=[],
                     edges=[], vertices=[]):
            self.node_index = node_index
            self.bsp3d_nodes_tag_block = bsp3d_nodes_tag_block
            self.planes_tag_block = planes_tag_block
            self.leaves_tag_block = leaves_tag_block
            self.bsp2d_references_tag_block = bsp2d_references_tag_block
            self.bsp2d_nodes_tag_block = bsp2d_nodes_tag_block
            self.surfaces_tag_block = surfaces_tag_block
            self.edges_tag_block = edges_tag_block
            self.vertices_tag_block = vertices_tag_block
            self.bsp3d_nodes = bsp3d_nodes
            self.planes = planes
            self.leaves = leaves
            self.bsp2d_references = bsp2d_references
            self.bsp2d_nodes = bsp2d_nodes
            self.surfaces = surfaces
            self.edges = edges
            self.vertices = vertices

    class BSP3DNode:
        def __init__(self, plane=0, back_child=0, front_child=0):
            self.plane = plane
            self.back_child = back_child
            self.front_child = front_child

    class Plane:
        def __init__(self, translation=Vector(), distance=0.0):
            self.translation = translation
            self.distance = distance

    class Leaf:
        def __init__(self, flags=0, bsp2d_reference_count=0, first_bsp2d_reference=0):
            self.flags = flags
            self.bsp2d_reference_count = bsp2d_reference_count
            self.first_bsp2d_reference = first_bsp2d_reference

    class BSP2DReference:
        def __init__(self, plane=0, bsp2d_node=0):
            self.plane = plane
            self.bsp2d_node = bsp2d_node

    class BSP2DNode:
        def __init__(self, plane_i=0.0, plane_j=0.0, distance=0.0, left_child=0, right_child=0):
            self.plane_i = plane_i
            self.plane_j = plane_j
            self.distance = distance
            self.left_child = left_child
            self.right_child = right_child

    class Surface:
        def __init__(self, plane=0, first_edge=0, flags=0, breakable_surface=0, material=0):
            self.plane = plane
            self.first_edge = first_edge
            self.flags = flags
            self.breakable_surface = breakable_surface
            self.material = material

    class Edge:
        def __init__(self, start_vertex=0, end_vertex=0, forward_edge=0, reverse_edge=0, left_surface=0, right_surface=0):
            self.start_vertex = start_vertex
            self.end_vertex = end_vertex
            self.forward_edge = forward_edge
            self.reverse_edge = reverse_edge
            self.left_surface = left_surface
            self.right_surface = right_surface

    class Vertex:
        def __init__(self, translation=Vector(), first_edge=0):
            self.translation = translation
            self.first_edge = first_edge

    class BSPPhysics:
        def __init__(self, size_0=0, count_0=0, size_1=0, count_1=0, size_2=0, count_2=0, mopp_code_data_ref=None, mopp_code_data=None):
            self.size_0 = size_0
            self.count_0 = count_0
            self.size_1 = size_1
            self.count_1 = count_1
            self.size_2 = size_2
            self.count_2 = count_2
            self.mopp_code_data_ref = mopp_code_data_ref
            self.mopp_code_data = mopp_code_data

    class PathfindingSphere:
        def __init__(self, node=0, flags=0, center=Vector(), radius=0.0):
            self.node = node
            self.flags = flags
            self.center = center
            self.radius = radius

    class Node:
        def __init__(self, name="", parent_node=0, next_sibling_node=0, first_child_node=0):
            self.name = name
            self.parent_node = parent_node
            self.next_sibling_node = next_sibling_node
            self.first_child_node = first_child_node 
