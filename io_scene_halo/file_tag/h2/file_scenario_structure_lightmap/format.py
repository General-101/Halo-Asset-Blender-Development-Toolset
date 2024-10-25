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

from mathutils import Vector
from enum import Flag, Enum, auto

class GroupTypeEnum(Enum):
    normal = 0

class GroupFlags(Flag):
    unused = auto()

class GeometryClassificationEnum(Enum):
    worldspace = 0
    rigid = auto()
    rigid_boned = auto()
    skinned = auto()
    unsupported_reimport = auto()

class GeometryCompressionFlags(Flag):
    compressed_position = auto()
    compressed_texcoord = auto()
    compressed_secondary_texcoord = auto()

class SectionLightingFlags(Flag):
    has_lm_texcoords = auto()
    has_lm_inc_rad = auto()
    has_lm_colors = auto()
    has_lm_part = auto()

class ResourceTypeEnum(Enum):
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
    new_part_types = auto()
    dislikes_photons = auto()
    override_triangle_list = auto()
    ignored_by_lightmapper = auto()

class ProceduralOverrideEnum(Enum):
    no_override = 0
    cie_clear_sky = auto()
    cie_partly_cloudy = auto()
    cie_cloudy = auto()
    directional_light = auto()
    cone_light = auto()
    sphere_light = auto()
    hemisphere_light = auto()

class LightingEnvironmentFlags(Flag):
    lock_values = auto()

class GeometryBucketFlags(Flag):
    incident_direction = auto()
    color = auto()

class ErrorTypeEnum(Enum):
    silent = 0
    comment = auto()
    warning = auto()
    error = auto()

class ErrorFlags(Flag):
    rendered = auto()
    tangent_space = auto()
    non_critical = auto()
    lightmap_light = auto()
    report_key_is_valid = auto()

class LightmapAsset():
    def __init__(self, header=None, body_header=None, lightmap_groups_header=None, lightmap_groups=None, errors_header=None, errors=None, search_distance_lower_bound=0.0, 
                 search_distance_upper_bound=0.0, luminels_per_world_unit=0.0, output_white_reference=0.0, output_black_reference=0.0, output_schlick_parameter=0.0, 
                 diffuse_map_scale=0.0, sun_scale=0.0, sky_scale=0.0, indirect_scale=0.0, prt_scale=0.0, surface_light_scale=0.0, scenario_light_scale=0.0, 
                 lightprobe_interpolation_override=0.0, lightmap_groups_tag_block=None, errors_tag_block=None):
        self.header = header
        self.body_header = body_header
        self.lightmap_groups_header = lightmap_groups_header
        self.lightmap_groups = lightmap_groups
        self.errors_header = errors_header
        self.errors = errors
        self.search_distance_lower_bound = search_distance_lower_bound
        self.search_distance_upper_bound = search_distance_upper_bound
        self.luminels_per_world_unit = luminels_per_world_unit
        self.output_white_reference = output_white_reference
        self.output_black_reference = output_black_reference
        self.output_schlick_parameter = output_schlick_parameter
        self.diffuse_map_scale = diffuse_map_scale
        self.sun_scale = sun_scale
        self.sky_scale = sky_scale
        self.indirect_scale = indirect_scale
        self.prt_scale = prt_scale
        self.surface_light_scale = surface_light_scale
        self.scenario_light_scale = scenario_light_scale
        self.lightprobe_interpolation_override = lightprobe_interpolation_override
        self.lightmap_groups_tag_block = lightmap_groups_tag_block
        self.errors_tag_block = errors_tag_block

    class LightmapGroup:
        def __init__(self, group_type=0, group_flags=0, structure_checksum=0, section_palette_header=None, writable_palettes_header=None, clusters_header=None, 
                     cluster_render_info_header=None, poop_definitions_header=None, lighting_environments_header=None, geometry_buckets_header=None, instance_render_info_header=None, 
                     instance_bucket_refs_header=None, scenery_object_info_header=None, scenery_object_bucket_refs_header=None, section_palette_tag_block=None, 
                     writable_palettes_tag_block=None, bitmap_group_tag_ref=None, clusters_tag_block=None, cluster_render_info_tag_block=None, poop_definitions_tag_block=None, 
                     lighting_environments_tag_block=None, geometry_buckets_tag_block=None, instance_render_info_tag_block=None, instance_bucket_refs_tag_block=None, 
                     scenery_object_info_tag_block=None, scenery_object_bucket_refs_tag_block=None, section_palette=None, writable_palettes=None, clusters=None, 
                     cluster_render_info=None, poop_definitions=None, lighting_environments=None, geometry_buckets=None, instance_render_info=None, instance_bucket_refs=None, 
                     scenery_object_info=None, scenery_object_bucket_refs=None):
            self.group_type = group_type
            self.group_flags = group_flags
            self.structure_checksum = structure_checksum
            self.section_palette_header = section_palette_header
            self.writable_palettes_header = writable_palettes_header
            self.clusters_header = clusters_header
            self.cluster_render_info_header = cluster_render_info_header
            self.poop_definitions_header = poop_definitions_header
            self.lighting_environments_header = lighting_environments_header
            self.geometry_buckets_header = geometry_buckets_header
            self.instance_render_info_header = instance_render_info_header
            self.instance_bucket_refs_header = instance_bucket_refs_header
            self.scenery_object_info_header = scenery_object_info_header
            self.scenery_object_bucket_refs_header = scenery_object_bucket_refs_header
            self.section_palette_tag_block = section_palette_tag_block
            self.writable_palettes_tag_block = writable_palettes_tag_block
            self.bitmap_group_tag_ref = bitmap_group_tag_ref
            self.clusters_tag_block = clusters_tag_block
            self.cluster_render_info_tag_block = cluster_render_info_tag_block
            self.poop_definitions_tag_block = poop_definitions_tag_block
            self.lighting_environments_tag_block = lighting_environments_tag_block
            self.geometry_buckets_tag_block = geometry_buckets_tag_block
            self.instance_render_info_tag_block = instance_render_info_tag_block
            self.instance_bucket_refs_tag_block = instance_bucket_refs_tag_block
            self.scenery_object_info_tag_block = scenery_object_info_tag_block
            self.scenery_object_bucket_refs_tag_block = scenery_object_bucket_refs_tag_block
            self.section_palette = section_palette
            self.writable_palettes = writable_palettes
            self.clusters = clusters
            self.cluster_render_info = cluster_render_info
            self.poop_definitions = poop_definitions
            self.lighting_environments = lighting_environments
            self.geometry_buckets = geometry_buckets
            self.instance_render_info = instance_render_info
            self.instance_bucket_refs = instance_bucket_refs
            self.scenery_object_info = scenery_object_info
            self.scenery_object_bucket_refs = scenery_object_bucket_refs

    class PaletteColor:
        def __init__(self, first_palette_color=0, unknown=None):
            self.first_palette_color = first_palette_color
            self.unknown = unknown

    class Cluster:
        def __init__(self, total_vertex_count=0, total_triangle_count=0, total_part_count=0, shadow_casting_triangle_count=0, shadow_casting_part_count=0, opaque_point_count=0,
                     opaque_vertex_count=0, opaque_part_count=0, opaque_max_nodes_vertex=0, transparent_max_nodes_vertex=0, shadow_casting_rigid_triangle_count=0, 
                     unknown=bytes(), geometry_classification=0, geometry_compression_flags=0, compression_info_tag_block=None, hardware_node_count=0, node_map_size=0, 
                     software_plane_count=0, total_subpart_count=0, section_lighting_flags=0, cache_data_tag_block=None, block_offset=0, block_size=0, section_data_size=0, 
                     resource_data_size=0, resource_tag_block=None, owner_tag_section_offset=0, sinf_header=None, compression_info_header=None, blok_header=None, 
                     resources_header=None, cache_data_header=None, compression_info=None, resources=None, cache_data=None):
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
            self.unknown = unknown
            self.geometry_classification = geometry_classification
            self.geometry_compression_flags = geometry_compression_flags
            self.compression_info_tag_block = compression_info_tag_block
            self.hardware_node_count = hardware_node_count
            self.node_map_size = node_map_size
            self.software_plane_count = software_plane_count
            self.total_subpart_count = total_subpart_count
            self.section_lighting_flags = section_lighting_flags
            self.block_offset = block_offset
            self.block_size = block_size
            self.section_data_size = section_data_size
            self.resource_data_size = resource_data_size
            self.resource_tag_block = resource_tag_block
            self.owner_tag_section_offset = owner_tag_section_offset
            self.cache_data_tag_block = cache_data_tag_block
            self.sinf_header = sinf_header
            self.compression_info_header = compression_info_header
            self.blok_header = blok_header
            self.resources_header = resources_header
            self.cache_data_header = cache_data_header
            self.compression_info = compression_info
            self.resources = resources
            self.cache_data = cache_data

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

    class Resource:
        def __init__(self, resource_type=0, primary_locator=0, secondary_locator=0, resource_data_size=0, resource_data_offset=0):
            self.resource_type = resource_type
            self.primary_locator = primary_locator
            self.secondary_locator = secondary_locator
            self.resource_data_size = resource_data_size
            self.resource_data_offset = resource_data_offset

    class CacheData:
        def __init__(self, sect_header=None, parts_header=None, subparts_header=None, visibility_bounds_header=None, raw_vertices_header=None, strip_indices_header=None, 
                     mopp_reorder_table_header=None, vertex_buffers_header=None, parts_tag_block=None, subparts_tag_block=None, visibility_bounds_tag_block=None, 
                     raw_vertices_tag_block=None, strip_indices_tag_block=None, visibility_mopp_code_tag_data=None, mopp_reorder_table_tag_block=None, vertex_buffers_tag_block=None, 
                     parts=None, subparts=None, visibility_bounds=None, raw_vertices=None, strip_indices=None, mopp_reorder_table=None, vertex_buffers=None):
            self.sect_header = sect_header
            self.parts_header = parts_header
            self.subparts_header = subparts_header
            self.visibility_bounds_header = visibility_bounds_header
            self.raw_vertices_header = raw_vertices_header
            self.strip_indices_header = strip_indices_header
            self.mopp_reorder_table_header = mopp_reorder_table_header
            self.vertex_buffers_header = vertex_buffers_header
            self.parts_tag_block = parts_tag_block
            self.subparts_tag_block = subparts_tag_block
            self.visibility_bounds_tag_block = visibility_bounds_tag_block
            self.raw_vertices_tag_block = raw_vertices_tag_block
            self.strip_indices_tag_block = strip_indices_tag_block
            self.visibility_mopp_code_tag_data = visibility_mopp_code_tag_data
            self.mopp_reorder_table_tag_block = mopp_reorder_table_tag_block
            self.vertex_buffers_tag_block = vertex_buffers_tag_block
            self.parts = parts
            self.subparts = subparts
            self.visibility_bounds = visibility_bounds
            self.raw_vertices = raw_vertices
            self.strip_indices = strip_indices
            self.mopp_reorder_table = mopp_reorder_table
            self.vertex_buffers = vertex_buffers

    class Part:
        def __init__(self, part_type=0, flags=0, material_index=0, strip_start_index=0, strip_length=0, first_subpart_index=0, subpart_count=0,
                     max_nodes_vertex=0, contributing_compound_node_count=0, position=Vector(), node_index_0=0, node_index_1=0, node_index_2=0, node_index_3=0,
                     node_weight_0=0.0, node_weight_1=0.0, node_weight_2=0.0, lod_mipmap_magic_number=0, unknown=bytes()):
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
            self.lod_mipmap_magic_number = lod_mipmap_magic_number
            self.unknown = unknown

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
                     node_weight_2=0.0, node_weight_3=0.0, node_index_0_new=0, node_index_1_new=0, node_index_2_new=0, node_index_3_new=0, uses_new_node_indices=0,
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

    class RenderInfo:
        def __init__(self, bitmap_index=0, palette_index=0):
            self.bitmap_index = bitmap_index
            self.palette_index = palette_index

    class LightingEnvironment:
        def __init__(self, sample_point=Vector(), red_coefficient_0=0.0, red_coefficient_1=0.0, red_coefficient_2=0.0, red_coefficient_3=0.0, red_coefficient_4=0.0, red_coefficient_5=0.0,
                     red_coefficient_6=0.0, red_coefficient_7=0.0, red_coefficient_8=0.0, green_coefficient_0=0.0, green_coefficient_1=0.0, green_coefficient_2=0.0,
                     green_coefficient_3=0.0, green_coefficient_4=0.0, green_coefficient_5=0.0, green_coefficient_6=0.0, green_coefficient_7=0.0, green_coefficient_8=0.0,
                     blue_coefficient_0=0.0, blue_coefficient_1=0.0, blue_coefficient_2=0.0, blue_coefficient_3=0.0, blue_coefficient_4=0.0, blue_coefficient_5=0.0,
                     blue_coefficient_6=0.0, blue_coefficient_7=0.0, blue_coefficient_8=0.0, mean_incoming_light_direction=Vector(), incoming_light_intensity=Vector(),
                     specular_bitmap_index=0, rotation_axis=Vector(), rotation_speed=0.0, bump_direction=Vector(), color_tint_RGBA=(0.0, 0.0, 0.0, 1.0), procedural_override=0, flags=0,
                     procedural_param0=Vector(), procedural_param1_xyz=Vector(), procedural_param1_w=0.0):
            self.sample_point = sample_point
            self.red_coefficient_0 = red_coefficient_0
            self.red_coefficient_1 = red_coefficient_1
            self.red_coefficient_2 = red_coefficient_2
            self.red_coefficient_3 = red_coefficient_3
            self.red_coefficient_4 = red_coefficient_4
            self.red_coefficient_5 = red_coefficient_5
            self.red_coefficient_6 = red_coefficient_6
            self.red_coefficient_7 = red_coefficient_7
            self.red_coefficient_8 = red_coefficient_8
            self.green_coefficient_0 = green_coefficient_0
            self.green_coefficient_1 = green_coefficient_1
            self.green_coefficient_2 = green_coefficient_2
            self.green_coefficient_3 = green_coefficient_3
            self.green_coefficient_4 = green_coefficient_4
            self.green_coefficient_5 = green_coefficient_5
            self.green_coefficient_6 = green_coefficient_6
            self.green_coefficient_7 = green_coefficient_7
            self.green_coefficient_8 = green_coefficient_8
            self.blue_coefficient_0 = blue_coefficient_0
            self.blue_coefficient_1 = blue_coefficient_1
            self.blue_coefficient_2 = blue_coefficient_2
            self.blue_coefficient_3 = blue_coefficient_3
            self.blue_coefficient_4 = blue_coefficient_4
            self.blue_coefficient_5 = blue_coefficient_5
            self.blue_coefficient_6 = blue_coefficient_6
            self.blue_coefficient_7 = blue_coefficient_7
            self.blue_coefficient_8 = blue_coefficient_8
            self.mean_incoming_light_direction = mean_incoming_light_direction
            self.incoming_light_intensity = incoming_light_intensity
            self.specular_bitmap_index = specular_bitmap_index
            self.rotation_axis = rotation_axis
            self.rotation_speed = rotation_speed
            self.bump_direction = bump_direction
            self.color_tint_RGBA = color_tint_RGBA
            self.procedural_override = procedural_override
            self.flags = flags
            self.procedural_param0 = procedural_param0
            self.procedural_param1_xyz = procedural_param1_xyz
            self.procedural_param1_w = procedural_param1_w

    class GeometryBucket:
        def __init__(self, flags=0, raw_vertices_header=None, raw_vertices_tag_block=None, block_offset=0, block_size=0, section_data_size=0, resource_data_size=0, 
                     blok_header=None, resources_header=None, resources_tag_block=None, owner_tag_section_offset=0, cache_data_header=None, cache_data_tag_block=None, 
                     raw_vertices=None, resources=None, cache_data=None):
            self.flags = flags
            self.raw_vertices_header = raw_vertices_header
            self.raw_vertices_tag_block = raw_vertices_tag_block
            self.block_offset = block_offset
            self.block_size = block_size
            self.section_data_size = section_data_size
            self.resource_data_size = resource_data_size
            self.blok_header = blok_header
            self.resources_header = resources_header
            self.resources_tag_block = resources_tag_block
            self.owner_tag_section_offset = owner_tag_section_offset
            self.cache_data_header = cache_data_header
            self.cache_data_tag_block = cache_data_tag_block
            self.raw_vertices = raw_vertices
            self.resources = resources
            self.cache_data = cache_data

    class BucketRef:
        def __init__(self, flags=0, bucket_index=0, section_offsets_header=None, section_offsets_tag_block=None, section_offsets=None):
            self.flags = flags
            self.bucket_index = bucket_index
            self.section_offsets_header = section_offsets_header
            self.section_offsets_tag_block = section_offsets_tag_block
            self.section_offsets = section_offsets

    class SceneryObjectInfo:
        def __init__(self, unique_id=0, origin_bsp_index=0, object_type=0, source=0, render_model_checksum=0):
            self.unique_id = unique_id
            self.origin_bsp_index = origin_bsp_index
            self.object_type = object_type
            self.source = source
            self.render_model_checksum = render_model_checksum

    class Error:
        def __init__(self, name="", report_type=0, flags=0, reports_header=None, reports_tag_block=None, reports=None):
            self.name = name
            self.report_type = report_type
            self.flags = flags
            self.reports_header = reports_header
            self.reports_tag_block = reports_tag_block
            self.reports = reports

    class Report:
        def __init__(self, type=0, flags=0, text="", source_filename="", source_line_number=0, vertices_header=None, vectors_header=None, lines_header=None, triangles_header=None, quads_header=None, comments_header=None, vertices_tag_block=None, vectors_tag_block=None, lines_tag_block=None, triangles_tag_block=None, quads_tag_block=None, comments_tag_block=None, vertices=None, vectors=None, lines=None, triangles=None, quads=None, comments=None, report_key=0, node_index=0, bounds_x=(0.0, 0.0), bounds_y=(0.0, 0.0), bounds_z=(0.0, 0.0), color=(0.0, 0.0, 0.0, 0.0)):
            self.type = type
            self.flags = flags
            self.text = text
            self.source_filename = source_filename
            self.source_line_number = source_line_number
            self.vertices_header = vertices_header
            self.vectors_header = vectors_header
            self.lines_header = lines_header
            self.triangles_header = triangles_header
            self.quads_header = quads_header
            self.comments_header = comments_header
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
        def __init__(self, text="", text_length=0, position=Vector(), node_index_0=0, node_index_1=0, node_index_2=0, node_index_3=0, node_weight_0=0.0, node_weight_1=0.0,
                     node_weight_2=0.0, node_weight_3=0.0, color=(0.0, 0.0, 0.0, 0.0)):
            self.text = text
            self.text_length = text_length
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
