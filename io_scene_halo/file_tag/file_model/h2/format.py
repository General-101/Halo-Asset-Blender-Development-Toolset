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

from mathutils import Vector, Quaternion

class GeometryClassification(Enum):
    worldspace = 0
    rigid = 1
    rigid_boned = 2
    skinned = 3
    unsupported = 4

class RenderAsset():
    def __init__(self):
        self.version = 8210 # This is just here so that I don't have to rework parts of the mesh_processing code. Make me care.
        self.header = None
        self.render_body_header = None
        self.render_body = None
        self.region_header = None
        self.regions = None
        self.section_header = None
        self.sections = None
        self.nodes_header = None
        self.nodes = None
        self.transforms = None
        self.marker_group_header = None
        self.marker_groups = None
        self.material_header = None
        self.materials = None

    class RenderBody:
        def __init__(self, name="", name_length=0, flags=0, import_info_tag_block=None, compression_info_tag_block=None, regions_tag_block=None, sections_tag_block=None,
                     invalid_section_pair_bits_tag_block=None, section_groups_tag_block=None, l1_section_index=0, l2_section_index=0, l3_section_index=0, l4_section_index=0,
                     l5_section_index=0, l6_section_index=0, node_list_checksum=0, nodes_tag_block=None, node_map_tag_block=None, marker_groups_tag_block=None,
                     materials_tag_block=None, errors_tag_block=None, dont_draw_over_camera_cosine_angle=0.0, prt_info_tag_block=None, section_render_leaves_tag_block=None):
            self.name = name
            self.name_length = name_length
            self.flags = flags
            self.import_info_tag_block = import_info_tag_block
            self.compression_info_tag_block = compression_info_tag_block
            self.regions_tag_block = regions_tag_block
            self.sections_tag_block = sections_tag_block
            self.invalid_section_pair_bits_tag_block = invalid_section_pair_bits_tag_block
            self.section_groups_tag_block = section_groups_tag_block
            self.l1_section_index = l1_section_index
            self.l2_section_index = l2_section_index
            self.l3_section_index = l3_section_index
            self.l4_section_index = l4_section_index
            self.l5_section_index = l5_section_index
            self.l6_section_index = l6_section_index
            self.node_list_checksum = node_list_checksum
            self.nodes_tag_block = nodes_tag_block
            self.node_map_tag_block = node_map_tag_block
            self.marker_groups_tag_block = marker_groups_tag_block
            self.materials_tag_block = materials_tag_block
            self.errors_tag_block = errors_tag_block
            self.dont_draw_over_camera_cosine_angle = dont_draw_over_camera_cosine_angle
            self.prt_info_tag_block = prt_info_tag_block
            self.section_render_leaves_tag_block = section_render_leaves_tag_block

    class ImportInfo:
        def __init__(self, build=0, version="", import_date="", culprit="", import_time="", files_tag_block=None, files=None):
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

    class CompressionInfo:
        def __init__(self, position_bounds_x=(0.0, 0.0), position_bounds_y=(0.0, 0.0), position_bounds_z=(0.0, 0.0), texcoord_bounds_x=(0.0, 0.0), texcoord_bounds_y=(0.0, 0.0),
                     secondary_texcoord_bounds_x=(0.0, 0.0), secondary_texcoord_bounds_y=(0.0, 0.0)):
            self.position_bounds_x = position_bounds_x
            self.position_bounds_y = position_bounds_y
            self.position_bounds_z = position_bounds_z
            self.texcoord_bounds_x = texcoord_bounds_x
            self.texcoord_bounds_y = texcoord_bounds_y
            self.secondary_texcoord_bounds_x = secondary_texcoord_bounds_x
            self.secondary_texcoord_bounds_y = secondary_texcoord_bounds_y

    class Region:
        def __init__(self, name="", node_map_size=0, node_map_offset=0, permutations_tag_block_header=None, permutations_tag_block=None, permutations=[]):
            self.name = name
            self.node_map_size = node_map_size
            self.node_map_offset = node_map_offset
            self.permutations_tag_block_header = permutations_tag_block_header
            self.permutations_tag_block = permutations_tag_block
            self.permutations = permutations

    class Permutation:
        def __init__(self, name="", l1_section_index=0, l2_section_index=0, l3_section_index=0, l4_section_index=0, l5_section_index=0, l6_section_index=0):
            self.name = name
            self.l1_section_index = l1_section_index
            self.l2_section_index = l2_section_index
            self.l3_section_index = l3_section_index
            self.l4_section_index = l4_section_index
            self.l5_section_index = l5_section_index
            self.l6_section_index = l6_section_index

    class Section:
        def __init__(self, global_geometry_classification=0, total_vertex_count=0, total_triangle_count=0, total_part_count=0, shadow_casting_triangle_count=0,
                     shadow_casting_part_count=0, opaque_point_count=0, opaque_vertex_count=0, opaque_part_count=0, opaque_max_nodes_vertex=0, transparent_max_nodes_vertex=0,
                     shadow_casting_rigid_triangle_count=0, geometry_classification=0, geometry_compression_flags=0, compression_info_tag_block_header=None,
                     compression_info_tag_block=None, hardware_node_count=0, node_map_size=0, software_plane_count=0, total_subpart_count=0, section_lighting_flags=0,
                     rigid_node_index=0, flags=0, section_data_tag_block_header=None, section_data_tag_block=None, block_offset=0, block_size=0, section_data_size=0,
                     resource_tag_block_header=None, resource_data_size=0, resource_tag_block=None, owner_tag_section_offset=0, compression_info = None, section_data = None,
                     resources = None, visited=False):
            self.global_geometry_classification = global_geometry_classification
            self.total_vertex_count = total_vertex_count
            self.total_triangle_count = total_triangle_count
            self.total_part_count = total_part_count
            self.shadow_casting_triangle_count = shadow_casting_triangle_count
            self.shadow_casting_part_count = shadow_casting_part_count
            self.opaque_point_count = opaque_point_count
            self.opaque_vertex_count = opaque_vertex_count
            self.opaque_part_count = opaque_part_count
            self.opaque_max_nodes_vertex = opaque_max_nodes_vertex
            self.transparent_max_nodes_vertex = transparent_max_nodes_vertex
            self.shadow_casting_rigid_triangle_count = shadow_casting_rigid_triangle_count
            self.geometry_classification = geometry_classification
            self.geometry_compression_flags = geometry_compression_flags
            self.compression_info_tag_block_header = compression_info_tag_block_header
            self.compression_info_tag_block = compression_info_tag_block
            self.hardware_node_count = hardware_node_count
            self.node_map_size = node_map_size
            self.software_plane_count = software_plane_count
            self.total_subpart_count = total_subpart_count
            self.section_lighting_flags = section_lighting_flags
            self.rigid_node_index = rigid_node_index
            self.flags = flags
            self.section_data_tag_block_header = section_data_tag_block_header
            self.section_data_tag_block = section_data_tag_block
            self.block_offset = block_offset
            self.block_size = block_size
            self.section_data_size = section_data_size
            self.resource_data_size = resource_data_size
            self.resource_tag_block_header = resource_tag_block_header
            self.resource_tag_block = resource_tag_block
            self.owner_tag_section_offset = owner_tag_section_offset
            self.compression_info = compression_info
            self.section_data = section_data
            self.resources = resources
            self.visited = visited

    class SectionData:
        def __init__(self, parts_tag_block_header=None, parts_tag_block=None, subparts_tag_block_header=None, subparts_tag_block=None, visibility_bounds_tag_block_header=None,
                     visibility_bounds_tag_block=None, raw_vertices_tag_block_header=None, raw_vertices_tag_block=None, strip_indices_tag_block_header=None,
                     strip_indices_tag_block=None, visibility_mopp_code=0, mopp_reorder_table_tag_block_header=None, mopp_reorder_table_tag_block=None,
                     vertex_buffers_tag_block_header=None, vertex_buffers_tag_block=None, raw_points_tag_block_header=None, raw_points_tag_block=None, runtime_point_data=0,
                     rigid_point_groups_tag_block_header=None, rigid_point_groups_tag_block=None, vertex_point_indices_tag_block_header=None, vertex_point_indices_tag_block=None,
                     node_map_tag_block_header=None, node_map_tag_block=None, parts=None, subparts=None, visibility_bounds=None, raw_vertices=None, strip_indices=None,
                     mopp_reorder_table=None, vertex_buffers=None, raw_points=None, rigid_point_groups=None, vertex_point_indices=None, node_map=None):
            self.parts_tag_block_header = parts_tag_block_header
            self.parts_tag_block = parts_tag_block
            self.subparts_tag_block_header = subparts_tag_block_header
            self.subparts_tag_block = subparts_tag_block
            self.visibility_bounds_tag_block_header = visibility_bounds_tag_block_header
            self.visibility_bounds_tag_block = visibility_bounds_tag_block
            self.raw_vertices_tag_block_header = raw_vertices_tag_block_header
            self.raw_vertices_tag_block = raw_vertices_tag_block
            self.strip_indices_tag_block_header = strip_indices_tag_block_header
            self.strip_indices_tag_block = strip_indices_tag_block
            self.visibility_mopp_code = visibility_mopp_code
            self.mopp_reorder_table_tag_block_header = mopp_reorder_table_tag_block_header
            self.mopp_reorder_table_tag_block = mopp_reorder_table_tag_block
            self.vertex_buffers_tag_block_header = vertex_buffers_tag_block_header
            self.vertex_buffers_tag_block = vertex_buffers_tag_block
            self.raw_points_tag_block_header = raw_points_tag_block_header
            self.raw_points_tag_block = raw_points_tag_block
            self.runtime_point_data = runtime_point_data
            self.rigid_point_groups_tag_block_header = rigid_point_groups_tag_block_header
            self.rigid_point_groups_tag_block = rigid_point_groups_tag_block
            self.vertex_point_indices_tag_block_header = vertex_point_indices_tag_block_header
            self.vertex_point_indices_tag_block = vertex_point_indices_tag_block
            self.node_map_tag_block_header = node_map_tag_block_header
            self.node_map_tag_block = node_map_tag_block
            self.parts = parts
            self.subparts = subparts
            self.visibility_bounds = visibility_bounds
            self.raw_vertices = raw_vertices
            self.strip_indices = strip_indices
            self.mopp_reorder_table = mopp_reorder_table
            self.vertex_buffers = vertex_buffers
            self.raw_points = raw_points
            self.rigid_point_groups = rigid_point_groups
            self.vertex_point_indices = vertex_point_indices
            self.node_map = node_map

    class Part:
        def __init__(self, part_type=0, flags=0, material_index=0, strip_start_index=0, strip_length=0, first_subpart_index=0, subpart_count=0,
                     max_nodes_vertex=0, contributing_compound_node_count=0, position=Vector(), node_index_0=0, node_index_1=0, node_index_2=0, node_index_3=0,
                     node_weight_0=0.0, node_weight_1=0.0, node_weight_2=0.0, node_weight_3=0.0, lod_mipmap_magic_number=0):
            self.part_type = part_type
            self.flags = flags
            self.material_index = material_index
            self.strip_start_index = strip_start_index
            self.strip_length = strip_length
            self.first_subpart_index = first_subpart_index
            self.subpart_count = subpart_count
            self.max_nodes_vertex = max_nodes_vertex
            self.contributing_compound_node_count = contributing_compound_node_count
            self.position = position
            self.node_index_0 = node_index_0
            self.node_index_1 = node_index_1
            self.node_index_2 = node_index_2
            self.node_index_3 = node_index_3
            self.node_weight_0 = node_weight_0
            self.node_weight_1 = node_weight_1
            self.node_weight_2 = node_weight_2
            self.node_weight_3 = node_weight_3
            self.lod_mipmap_magic_number = lod_mipmap_magic_number

    class PartCache(Part):
        def __init__(self, geometry_subclassification=0, first_strip_segment_index=0, strip_segment_count=0, first_vertex_index=0, vertex_count=0, first_triangle_index=0,
                     triangle_count=0, max_nodes_per_vertex=0, vertex_usage_flags=0, position=Vector(), node_index_0=0, node_index_1=0, node_index_2=0, node_index_3=0,
                     node_weight_0=0.0, node_weight_1=0.0, node_weight_2=0.0, node_weight_3=0.0, lod_mipmap_magic_number=0):
            super().__init__()
            self.geometry_subclassification = geometry_subclassification
            self.first_strip_segment_index = first_strip_segment_index
            self.strip_segment_count = strip_segment_count
            self.first_vertex_index = first_vertex_index
            self.vertex_count = vertex_count
            self.first_triangle_index = first_triangle_index
            self.triangle_count = triangle_count
            self.max_nodes_per_vertex = max_nodes_per_vertex
            self.vertex_usage_flags = vertex_usage_flags
            self.position = position
            self.node_index_0 = node_index_0
            self.node_index_1 = node_index_1
            self.node_index_2 = node_index_2
            self.node_index_3 = node_index_3
            self.node_weight_0 = node_weight_0
            self.node_weight_1 = node_weight_1
            self.node_weight_2 = node_weight_2
            self.node_weight_3 = node_weight_3
            self.lod_mipmap_magic_number = lod_mipmap_magic_number

    class RawPoint:
        def __init__(self, position=Vector(), node_index_0_old=-1, node_index_1_old=-1, node_index_2_old=-1, node_index_3_old=-1, node_weight_0=0.0, node_weight_1=0.0,
                     node_weight_2=0.0, node_weight_3=0.0, node_index_0_new=-1, node_index_1_new=-1, node_index_2_new=-1, node_index_3_new=-1, uses_new_node_indices=0,
                     adjusted_compound_node_index=0):
            self.position = position
            self.node_index_0_old = node_index_0_old
            self.node_index_1_old = node_index_1_old
            self.node_index_2_old = node_index_2_old
            self.node_index_3_old = node_index_3_old
            self.node_weight_0 = node_weight_0
            self.node_weight_1 = node_weight_1
            self.node_weight_2 = node_weight_2
            self.node_weight_3 = node_weight_3
            self.node_index_0_new = node_index_0_new
            self.node_index_1_new = node_index_1_new
            self.node_index_2_new = node_index_2_new
            self.node_index_3_new = node_index_3_new
            self.uses_new_node_indices = uses_new_node_indices
            self.adjusted_compound_node_index = adjusted_compound_node_index

    class RawVertex(RawPoint):
        def __init__(self, texcoord=(0.0, 0.0), normal=Vector(), binormal=Vector(), tangent=Vector(), anisotropic_binormal=Vector(), secondary_texcoord=(0.0, 0.0),
                     primary_lightmap_color_RGBA=(0.0, 0.0, 0.0, 1.0), primary_lightmap_texcoord=(0.0, 0.0), primary_lightmap_incident_direction=Vector()):
            super().__init__()
            self.texcoord = texcoord
            self.normal = normal
            self.binormal = binormal
            self.tangent = tangent
            self.anisotropic_binormal = anisotropic_binormal
            self.secondary_texcoord = secondary_texcoord
            self.primary_lightmap_color_RGBA = primary_lightmap_color_RGBA
            self.primary_lightmap_texcoord = primary_lightmap_texcoord
            self.primary_lightmap_incident_direction = primary_lightmap_incident_direction

    class RigidPointGroup:
        def __init__(self, rigid_node_index=0, nodes_per_point=0, point_count=0):
            self.rigid_node_index = rigid_node_index
            self.nodes_per_point = nodes_per_point
            self.point_count = point_count

    class SectionGroup:
        def __init__(self, detail_levels=0, compound_nodes_tag_block=None, compound_nodes=None):
            self.detail_levels = detail_levels
            self.compound_nodes_tag_block = compound_nodes_tag_block
            self.compound_nodes = compound_nodes

    class CompoundNode:
        def __init__(self, node_0_index=0, node_1_index=0, node_2_index=0, node_3_index=0, node_0_weight=0, node_1_weight=0, node_2_weight=0):
            self.node_0_index = node_0_index
            self.node_1_index = node_1_index
            self.node_2_index = node_2_index
            self.node_3_index = node_3_index
            self.node_0_weight = node_0_weight
            self.node_1_weight = node_1_weight
            self.node_2_weight = node_2_weight

    class Node:
        def __init__(self, name="", name_length=0, parent_node_index=0, first_child_node_index=0, next_sibling_node_index=0, import_node_index=0, distance_from_parent=0.0):
            self.name = name
            self.name_length = name_length
            self.parent = parent_node_index
            self.child = first_child_node_index
            self.sibling = next_sibling_node_index
            self.import_node_index = import_node_index
            self.distance_from_parent = distance_from_parent

    class Transform:
        def __init__(self, translation=Vector(), rotation=Quaternion(), inverse_forward=Vector(), inverse_left=Vector(), inverse_up=Vector(),
                     inverse_position=Vector(), inverse_scale=0.0):
            self.translation = translation
            self.rotation = rotation
            self.inverse_forward = inverse_forward
            self.inverse_left = inverse_left
            self.inverse_up = inverse_up
            self.inverse_position = inverse_position
            self.inverse_scale = inverse_scale

    class MarkerGroup:
        def __init__(self, name="", markers_tag_block_header=None, markers_tag_block=None, markers=None):
            self.name = name
            self.markers_tag_block_header = markers_tag_block_header
            self.markers_tag_block = markers_tag_block
            self.markers = markers

    class Marker:
        def __init__(self, region_index=-1, permutation_index=-1, node_index=0, translation=Vector(), rotation=Quaternion()):
            self.region_index = region_index
            self.permutation_index = permutation_index
            self.node_index = node_index
            self.translation = translation
            self.rotation = rotation

    class Material:
        def __init__(self, old_shader=None, shader=None, properties_tag_block_header=None, properties_tag_block=None, breakable_surface_index=0, properties=None):
            self.old_shader = old_shader
            self.shader = shader
            self.properties_tag_block_header = properties_tag_block_header
            self.properties_tag_block = properties_tag_block
            self.breakable_surface_index = breakable_surface_index
            self.properties = properties
