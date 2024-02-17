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

from enum import Flag, Enum, auto
from mathutils import Vector

class CollisionFlags(Flag):
    contains_open_edges = auto()

class ReportTypeEnum(Enum):
    silent = 0
    comment = auto()
    warning = auto()
    error = auto()

class ReportFlags(Flag):
    rendered = auto()
    tangent_space = auto()
    non_critical = auto()
    lightmap_light = auto()
    report_key_is_valid = auto()

class LeafFlags(Flag):
    contains_double_sided_surfaces = auto()

class SurfaceFlags(Flag):
    two_sided = auto()
    invisible = auto()
    climbable = auto()
    breakable = auto()
    invalid = auto()
    conveyor = auto()

class PathfindingSphereFlags(Flag):
    remains_when_open = auto()
    vehicle_only = auto()
    with_sector = auto()

class CollisionAsset():
    def __init__(self):
        self.header = None
        self.collision_body_header = None
        self.collision_body = None
        self.import_info_header = None
        self.import_info = None
        self.errors_header = None
        self.errors = None
        self.materials_header = None
        self.materials = None
        self.regions_header = None
        self.regions = None
        self.pathfinding_spheres_header = None
        self.pathfinding_spheres = None
        self.nodes_header = None
        self.nodes = None

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
        def __init__(self, build=0, version="", import_date="", culprit="", import_time="", files_tag_block=None, files=None):
            self.build = build
            self.version = version
            self.import_date = import_date
            self.culprit = culprit
            self.import_time = import_time
            self.files_tag_block = files_tag_block
            self.files = files

    class File:
        def __init__(self, path="", modification_date="", checksum=0, size=0, zipped_data=None, uncompressed_data=None):
            self.path = path
            self.modification_date = modification_date
            self.checksum = checksum
            self.size = size
            self.zipped_data = zipped_data
            self.uncompressed_data = uncompressed_data

    class Error:
        def __init__(self, name="", report_type=0, flags=0, reports_tag_block=None, reports=None):
            self.name = name
            self.report_type = report_type
            self.flags = flags
            self.reports_tag_block = reports_tag_block
            self.reports = reports

    class Report:
        def __init__(self, type=0, flags=0, report_length=0, text="", source_filename="", source_line_number=0, vertices_tag_block=None, vectors_tag_block=None,
                     lines_tag_block=None, triangles_tag_block=None, quads_tag_block=None, comments_tag_block=None, vertices=None, vectors=None, lines=None, triangles=None,
                     quads=None, comments=None, report_key=0, node_index=0, bounds_x=(0.0, 0.0), bounds_y=(0.0, 0.0), bounds_z=(0.0, 0.0), color=(0.0, 0.0, 0.0, 0.0)):
            self.type = type
            self.flags = flags
            self.report_length = report_length
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
        def __init__(self, text_length=0, text="", position=Vector(), node_index_0=0, node_index_1=0, node_index_2=0, node_index_3=0, node_weight_0=0.0, node_weight_1=0.0,
                     node_weight_2=0.0, node_weight_3=0.0, color=(0.0, 0.0, 0.0, 0.0)):
            self.text_length = text_length
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

    class Material:
        def __init__(self, name="", name_length=0):
            self.name = name
            self.name_length = name_length

    class Region:
        def __init__(self, name="", name_length=0, permutations_tag_block=None, permutations_header=None, permutations=None):
            self.name = name
            self.name_length = name_length
            self.permutations_tag_block = permutations_tag_block
            self.permutations_header = permutations_header
            self.permutations = permutations

    class Permutation:
        def __init__(self, name="", name_length=0, bsps_tag_block=None, bsp_physics_tag_block=None, bsps_header=None, bsp_physics_header=None, bsps=None, bsp_physics=None):
            self.name = name
            self.name_length = name_length
            self.bsps_tag_block = bsps_tag_block
            self.bsp_physics_tag_block = bsp_physics_tag_block
            self.bsps_header = bsps_header
            self.bsp_physics_header = bsp_physics_header
            self.bsps = bsps
            self.bsp_physics = bsp_physics

    class BSP:
        def __init__(self, node_index=0, bsp3d_nodes_tag_block=None, planes_tag_block=None, leaves_tag_block=None, bsp2d_references_tag_block=None, bsp2d_nodes_tag_block=None,
                     surfaces_tag_block=None, edges_tag_block=None, vertices_tag_block=None, cbsp_header=None, bsp3d_nodes_header=None, planes_header=None, leaves_header=None,
                     bsp2d_references_header=None, bsp2d_nodes_header=None, surfaces_header=None, edges_header=None, vertices_header=None, bsp3d_nodes=None, planes=None, leaves=None,
                     bsp2d_references=None, bsp2d_nodes=None, surfaces=None, edges=None, vertices=None):
            self.node_index = node_index
            self.bsp3d_nodes_tag_block = bsp3d_nodes_tag_block
            self.planes_tag_block = planes_tag_block
            self.leaves_tag_block = leaves_tag_block
            self.bsp2d_references_tag_block = bsp2d_references_tag_block
            self.bsp2d_nodes_tag_block = bsp2d_nodes_tag_block
            self.surfaces_tag_block = surfaces_tag_block
            self.edges_tag_block = edges_tag_block
            self.vertices_tag_block = vertices_tag_block
            self.cbsp_header = cbsp_header
            self.bsp3d_nodes_header = bsp3d_nodes_header
            self.planes_header = planes_header
            self.leaves_header = leaves_header
            self.bsp2d_references_header = bsp2d_references_header
            self.bsp2d_nodes_header = bsp2d_nodes_header
            self.surfaces_header = surfaces_header
            self.edges_header = edges_header
            self.vertices_header = vertices_header
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
        def __init__(self, plane=None, left_child=0, right_child=0):
            self.plane = plane
            self.left_child = left_child
            self.right_child = right_child

    class Surface:
        def __init__(self, plane=0, first_edge=0, flags=0, breakable_surface=0, material=0):
            self.plane = plane
            self.first_edge = first_edge
            self.flags = flags
            self.breakable_surface = breakable_surface
            self.material = material

    class Vertex:
        def __init__(self, translation=Vector(), first_edge=0):
            self.translation = translation
            self.first_edge = first_edge

    class Edge:
        def __init__(self, start_vertex=0, end_vertex=0, forward_edge=0, reverse_edge=0, left_surface=0, right_surface=0):
            self.start_vertex = start_vertex
            self.end_vertex = end_vertex
            self.forward_edge = forward_edge
            self.reverse_edge = reverse_edge
            self.left_surface = left_surface
            self.right_surface = right_surface

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
