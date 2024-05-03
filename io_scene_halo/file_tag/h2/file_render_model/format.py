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

class RenderFlags(Flag):
    force_third_person = auto()
    force_carmack_reverse = auto()
    force_node_maps = auto()
    geometry_postprocessed = auto()

class GeometryClassificationEnum(Enum):
    worldspace = 0
    rigid = auto()
    rigid_boned = auto()
    skinned = auto()
    unsupported = auto()

class GeometryCompressionFlags(Flag):
    compressed_position = auto()
    compressed_texcoord = auto()
    compressed_secondary_texcoord = auto()

class SectionLightingFlags(Flag):
    has_lm_texcoords = auto()
    has_lm_inc_rad = auto()
    has_lm_colors = auto()
    has_lm_prt = auto()

class SectionFlags(Flag):
    geometry_postprocessed = auto()

class ResourceEnum(Enum):
    tag_block = 0
    tag_data = auto()
    vertex_buffer = auto()

class PartTypeEnum(Enum):
    not_drawn = 0
    opaque_shadow_only = auto()
    opaque_shadow_casting = auto()
    opaque_non_shadowing = auto()
    transparent = auto()
    lightmap_only = auto()

class PartFlags(Flag):
    decalable = auto()
    new_part_type = auto()
    dislikes_photons = auto()
    override_triangle_list = auto()
    ignored_by_lightmapper = auto()

class ISQFlags(Flag):
    compressed_planes = auto()
    swizzled_planes = auto()

class DetailLevelsFlags(Flag):
    l1 = auto()
    l2 = auto()
    l3 = auto()
    l4 = auto()
    l5 = auto()
    l6 = auto()

class PropertyTypeEnum(Enum):
    lightmap_resolution = 0
    lightmap_power = auto()
    lightmap_half_life = auto()
    lightmap_diffuse_scale = auto()

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

class RenderAsset():
    def __init__(self):
        self.version = 8210 # This is just here so that I don't have to rework parts of the mesh_processing code. Make me care.
        self.header = None
        self.render_body_header = None
        self.render_body = None
        self.import_info_header = None
        self.import_info = None
        self.compression_info_header = None
        self.compression_info = None
        self.region_header = None
        self.regions = None
        self.section_header = None
        self.sections = None
        self.invalid_section_pair_bits_header = None
        self.invalid_section_pair_bits = None
        self.section_groups_header = None
        self.section_groups = None
        self.nodes_header = None
        self.nodes = None
        self.node_map_header = None
        self.node_map = None
        self.transforms = None
        self.marker_group_header = None
        self.marker_groups = None
        self.material_header = None
        self.materials = None
        self.errors_header = None
        self.errors = None
        self.prt_info_header = None
        self.prt_info = None
        self.section_render_leaves_header = None
        self.section_render_leaves = None

    class RenderBody:
        def __init__(self, name="", name_length=0, flags=0, import_info_tag_block=None, compression_info_tag_block=None, regions_tag_block=None, sections_tag_block=None,
                     invalid_section_pair_bits_tag_block=None, section_groups_tag_block=None, l1_section_group_index=0, l2_section_group_index=0, l3_section_group_index=0,
                     l4_section_group_index=0, l5_section_group_index=0, l6_section_group_index=0, node_list_checksum=0, nodes_tag_block=None, node_map_tag_block=None,
                     marker_groups_tag_block=None, materials_tag_block=None, errors_tag_block=None, dont_draw_over_camera_cosine_angle=0.0, prt_info_tag_block=None,
                     section_render_leaves_tag_block=None):
            self.name = name
            self.name_length = name_length
            self.flags = flags
            self.import_info_tag_block = import_info_tag_block
            self.compression_info_tag_block = compression_info_tag_block
            self.regions_tag_block = regions_tag_block
            self.sections_tag_block = sections_tag_block
            self.invalid_section_pair_bits_tag_block = invalid_section_pair_bits_tag_block
            self.section_groups_tag_block = section_groups_tag_block
            self.l1_section_group_index = l1_section_group_index
            self.l2_section_group_index = l2_section_group_index
            self.l3_section_group_index = l3_section_group_index
            self.l4_section_group_index = l4_section_group_index
            self.l5_section_group_index = l5_section_group_index
            self.l6_section_group_index = l6_section_group_index
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

    class File:
        def __init__(self, path="", modification_date="", checksum=0, size=0, zipped_data=None, uncompressed_data=None):
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
        def __init__(self, name="", name_length=0, node_map_offset=0, node_map_size=0, permutations_tag_block_header=None, permutations_tag_block=None, permutations=None):
            self.name = name
            self.name_length = name_length
            self.node_map_offset = node_map_offset
            self.node_map_size = node_map_size
            self.permutations_tag_block_header = permutations_tag_block_header
            self.permutations_tag_block = permutations_tag_block
            self.permutations = permutations

    class Permutation:
        def __init__(self, name="", name_length=0, l1_section_index=0, l2_section_index=0, l3_section_index=0, l4_section_index=0, l5_section_index=0, l6_section_index=0):
            self.name = name
            self.name_length = name_length
            self.l1_section_index = l1_section_index
            self.l2_section_index = l2_section_index
            self.l3_section_index = l3_section_index
            self.l4_section_index = l4_section_index
            self.l5_section_index = l5_section_index
            self.l6_section_index = l6_section_index

    class Section:
        def __init__(self, global_geometry_classification=0, total_vertex_count=0, total_triangle_count=0, total_part_count=0, shadow_casting_triangle_count=0,
                     shadow_casting_part_count=0, opaque_point_count=0, opaque_vertex_count=0, opaque_part_count=0, opaque_max_nodes_vertex=0, transparent_max_nodes_vertex=0,
                     shadow_casting_rigid_triangle_count=0, geometry_classification=0, geometry_compression_flags=0, compression_info_header=None,
                     compression_info_tag_block=None, hardware_node_count=0, node_map_size=0, software_plane_count=0, total_subpart_count=0, section_lighting_flags=0,
                     rigid_node=0, flags=0, section_data_header=None, section_data_tag_block=None, block_offset=0, block_size=0, section_data_size=0, resource_data_size=0,
                     resources_header=None, resources_tag_block=None, owner_tag_section_offset=0, compression_info=None, section_data=None, resources=None, visited=False):
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
            self.compression_info_header = compression_info_header
            self.compression_info_tag_block = compression_info_tag_block
            self.hardware_node_count = hardware_node_count
            self.node_map_size = node_map_size
            self.software_plane_count = software_plane_count
            self.total_subpart_count = total_subpart_count
            self.section_lighting_flags = section_lighting_flags
            self.rigid_node = rigid_node
            self.flags = flags
            self.section_data_header = section_data_header
            self.section_data_tag_block = section_data_tag_block
            self.block_offset = block_offset
            self.block_size = block_size
            self.section_data_size = section_data_size
            self.resource_data_size = resource_data_size
            self.resources_header = resources_header
            self.resources_tag_block = resources_tag_block
            self.owner_tag_section_offset = owner_tag_section_offset
            self.compression_info = compression_info
            self.section_data = section_data
            self.resources = resources
            self.visited = visited

    class SectionData:
        def __init__(self, parts_header=None, parts_tag_block=None, subparts_header=None, subparts_tag_block=None, visibility_bounds_header=None,
                     visibility_bounds_tag_block=None, raw_vertices_header=None, raw_vertices_tag_block=None, strip_indices_header=None, strip_indices_tag_block=None,
                     visibility_mopp_code_data=0, mopp_reorder_table_header=None, mopp_reorder_table_tag_block=None, vertex_buffers_header=None, vertex_buffers_tag_block=None,
                     raw_points_header=None, raw_points_tag_block=None, runtime_point_tag_data=None, rigid_point_groups_header=None, rigid_point_groups_tag_block=None,
                     vertex_point_indices_header=None, vertex_point_indices_tag_block=None, node_map_header=None, node_map_tag_block=None, sinf_header=None, blok_header=None,
                     parts=None, subparts=None, visibility_bounds=None, raw_vertices=None, strip_indices=None, visibility_mopp_code=None, mopp_reorder_table=None,
                     vertex_buffers=None, raw_points=None, runtime_point_data=None, rigid_point_groups=None, vertex_point_indices=None, node_map=None, sect_header=None,
                     pdat_header=None):
            self.parts_header = parts_header
            self.parts_tag_block = parts_tag_block
            self.subparts_header = subparts_header
            self.subparts_tag_block = subparts_tag_block
            self.visibility_bounds_header = visibility_bounds_header
            self.visibility_bounds_tag_block = visibility_bounds_tag_block
            self.raw_vertices_header = raw_vertices_header
            self.raw_vertices_tag_block = raw_vertices_tag_block
            self.strip_indices_header = strip_indices_header
            self.strip_indices_tag_block = strip_indices_tag_block
            self.visibility_mopp_code_data = visibility_mopp_code_data
            self.mopp_reorder_table_header = mopp_reorder_table_header
            self.mopp_reorder_table_tag_block = mopp_reorder_table_tag_block
            self.vertex_buffers_header = vertex_buffers_header
            self.vertex_buffers_tag_block = vertex_buffers_tag_block
            self.raw_points_header = raw_points_header
            self.raw_points_tag_block = raw_points_tag_block
            self.runtime_point_tag_data = runtime_point_tag_data
            self.rigid_point_groups_header = rigid_point_groups_header
            self.rigid_point_groups_tag_block = rigid_point_groups_tag_block
            self.vertex_point_indices_header = vertex_point_indices_header
            self.vertex_point_indices_tag_block = vertex_point_indices_tag_block
            self.node_map_header = node_map_header
            self.node_map_tag_block = node_map_tag_block
            self.sinf_header = sinf_header
            self.blok_header = blok_header
            self.parts = parts
            self.subparts = subparts
            self.visibility_bounds = visibility_bounds
            self.raw_vertices = raw_vertices
            self.strip_indices = strip_indices
            self.visibility_mopp_code = visibility_mopp_code
            self.mopp_reorder_table = mopp_reorder_table
            self.vertex_buffers = vertex_buffers
            self.raw_points = raw_points
            self.runtime_point_data = runtime_point_data
            self.rigid_point_groups = rigid_point_groups
            self.vertex_point_indices = vertex_point_indices
            self.node_map = node_map
            self.sect_header = sect_header
            self.pdat_header = pdat_header

    class LegacySectionData(SectionData):
        def __init__(self, isq_flags=0, raw_planes_tag_block=None, runtime_plane_tag_data=None, rigid_plane_groups_tag_block=None, explicit_edges_tag_block=None,
                     forward_shared_edges_tag_block=None, forward_shared_edge_groups_tag_block=None, backward_shared_edges_tag_block=None,
                     backward_shared_edge_groups_tag_block=None, dsq_raw_vertices_tag_block=None, dsq_strip_indices_tag_block=None, dsq_silhouette_quads_tag_block=None,
                     carmack_silhouette_quad_count=0):
            super().__init__()
            self.isq_flags = isq_flags
            self.raw_planes_tag_block = raw_planes_tag_block
            self.runtime_plane_tag_data = runtime_plane_tag_data
            self.rigid_plane_groups_tag_block = rigid_plane_groups_tag_block
            self.explicit_edges_tag_block = explicit_edges_tag_block
            self.forward_shared_edges_tag_block = forward_shared_edges_tag_block
            self.forward_shared_edge_groups_tag_block = forward_shared_edge_groups_tag_block
            self.backward_shared_edges_tag_block = backward_shared_edges_tag_block
            self.backward_shared_edge_groups_tag_block = backward_shared_edge_groups_tag_block
            self.dsq_raw_vertices_tag_block = dsq_raw_vertices_tag_block
            self.dsq_strip_indices_tag_block = dsq_strip_indices_tag_block
            self.dsq_silhouette_quads_tag_block = dsq_silhouette_quads_tag_block
            self.carmack_silhouette_quad_count = carmack_silhouette_quad_count

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
                     triangle_count=0, max_nodes_per_vertex=0, vertex_usage_flags=0):
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

    class SubPart:
        def __init__(self, indices_start_index=0, indices_length=0, visibility_bounds_index=0, part_index=0):
            self.indices_start_index = indices_start_index
            self.indices_length = indices_length
            self.visibility_bounds_index = visibility_bounds_index
            self.part_index = part_index

    class VisibilityBounds:
        def __init__(self, position=Vector(), radius=0.0, node_0=0):
            self.position = position
            self.radius = radius
            self.node_0 = node_0

    class RawPoint:
        def __init__(self, position=Vector(), node_index_0_old=0, node_index_1_old=0, node_index_2_old=0, node_index_3_old=0, node_weight_0=0.0, node_weight_1=0.0,
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

    class RigidPlaneGroup:
        def __init__(self, rigid_node_index=0, part_index=0, triangle_count=0):
            self.rigid_node_index = rigid_node_index
            self.part_index = part_index
            self.triangle_count = triangle_count

    class Resource:
        def __init__(self, type=0, primary_locator=0, secondary_locator=0, resource_data_size=0, resource_data_offset=0):
            self.type = type
            self.primary_locator = primary_locator
            self.secondary_locator = secondary_locator
            self.resource_data_size = resource_data_size
            self.resource_data_offset = resource_data_offset

    class SectionGroup:
        def __init__(self, detail_levels=0, compound_nodes_tag_block=None, compound_nodes_header=None, compound_nodes=None):
            self.detail_levels = detail_levels
            self.compound_nodes_tag_block = compound_nodes_tag_block
            self.compound_nodes_header = compound_nodes_header
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
        def __init__(self, name="", name_length=0, markers_tag_block_header=None, markers_tag_block=None, markers=None):
            self.name = name
            self.name_length = name_length
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

    class Property:
        def __init__(self, property_type=0, int_value=0, real_value=0.0):
            self.property_type = property_type
            self.int_value = int_value
            self.real_value = real_value

    class Error:
        def __init__(self, name="", report_type=0, flags=0, reports_tag_block=None, reports_header=None, reports=None):
            self.name = name
            self.report_type = report_type
            self.flags = flags
            self.reports_tag_block = reports_tag_block
            self.reports_header = reports_header
            self.reports = reports

    class Report:
        def __init__(self, type=0, flags=0, report_length=0, text="", source_filename="", source_line_number=0, vertices_tag_block=None, vectors_tag_block=None,
                     lines_tag_block=None, triangles_tag_block=None, quads_tag_block=None, comments_tag_block=None, vertices_header=None, vectors_header=None,
                     lines_header=None, triangles_header=None, quads_header=None, comments_header=None, vertices=None, vectors=None, lines=None, triangles=None,
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
            self.vertices_header = vertices_header
            self.vectors_header = vectors_header
            self.lines_header = lines_header
            self.triangles_header = triangles_header
            self.quads_header = quads_header
            self.comments_header = comments_header
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
