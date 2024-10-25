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

import bpy

from mathutils import Vector
from ....global_functions import global_functions, tag_format
from .format import LightmapAsset, GeometryClassificationEnum, GeometryCompressionFlags, SectionLightingFlags

def get_clusters(TAG, donor_lightmap_group, bsp_index):
    clusters = []
    bsp_collection = bpy.data.collections.get("BSPs")
    if bsp_collection:
        bsp = bsp_collection.children[bsp_index]
        for geo_type in bsp.children:
            if "lightmaps" in geo_type.name:
                for cluster_idx, cluster_ob in enumerate(geo_type.objects):
                    cluster_ob.data.uv_layers.active = cluster_ob.data.uv_layers[0]

                    donor_cluster = donor_lightmap_group.clusters[cluster_idx]
                    donor_cache_data = donor_cluster.cache_data[0]

                    material_indices = set({})
                    for poly in cluster_ob.data.polygons:
                        material_indices.add(poly.material_index)

                    total_vertex_count = len(cluster_ob.data.vertices)
                    total_triangle_count = len(cluster_ob.data.polygons)
                    total_part_count = len(material_indices)

                    cluster = LightmapAsset.Cluster()
                    cluster.total_vertex_count = total_vertex_count
                    cluster.total_triangle_count = total_triangle_count
                    cluster.total_part_count = total_part_count
                    cluster.shadow_casting_triangle_count = total_triangle_count
                    cluster.shadow_casting_part_count = total_part_count
                    cluster.opaque_point_count = 0
                    cluster.opaque_vertex_count = total_vertex_count
                    cluster.opaque_part_count = total_part_count
                    cluster.opaque_max_nodes_vertex = 0
                    cluster.transparent_max_nodes_vertex = 0
                    cluster.shadow_casting_rigid_triangle_count = total_triangle_count
                    cluster.unknown = donor_cluster.unknown # what is this?
                    cluster.geometry_classification = GeometryClassificationEnum.worldspace.value
                    cluster.geometry_compression_flags = GeometryCompressionFlags.compressed_secondary_texcoord.value
                    cluster.hardware_node_count = 0
                    cluster.node_map_size = 0
                    cluster.software_plane_count = 0
                    cluster.total_subpart_count = donor_cluster.total_subpart_count # Need to find out how this works
                    cluster.section_lighting_flags = SectionLightingFlags.has_lm_texcoords.value + SectionLightingFlags.has_lm_inc_rad.value
                    cluster.block_offset = 0
                    cluster.block_size = 0
                    cluster.section_data_size = 0
                    cluster.resource_data_size = 0
                    cluster.owner_tag_section_offset = 0

                    cluster.sinf_header = TAG.TagBlockHeader("SINF", 0, 1, 44)
                    cluster.blok_header = TAG.TagBlockHeader("BLOK", 0, 1, 40)

                    cluster.compression_info = []

                    compression_info_count = len(cluster.compression_info)
                    cluster.compression_info_header = TAG.TagBlockHeader("tbfd", 0, compression_info_count, 16)
                    cluster.compression_info_tag_block = TAG.TagBlock(compression_info_count)

                    cluster.resources = []

                    resources_count = len(cluster.resources)
                    cluster.resources_header = TAG.TagBlockHeader("tbfd", 0, resources_count, 16)
                    cluster.resource_tag_block = TAG.TagBlock(resources_count)

                    cluster.cache_data = []
                    cache_data = LightmapAsset.CacheData()

                    cache_data.sect_header = TAG.TagBlockHeader("SECT", 1, 1, 108)

                    cache_data.parts = []
                    for material_index in material_indices:
                        donor_part = donor_cache_data.parts[material_index]

                        part = LightmapAsset.Part()
                        part.part_type = donor_part.part_type
                        part.flags = donor_part.flags
                        part.material_index = donor_part.material_index
                        part.strip_start_index = donor_part.strip_start_index
                        part.strip_length = donor_part.strip_length
                        part.first_subpart_index = donor_part.first_subpart_index
                        part.subpart_count = donor_part.subpart_count
                        part.max_nodes_vertex = 0
                        part.contributing_compound_node_count = 0
                        part.position = donor_part.position
                        part.node_index_0 = 0
                        part.node_index_1 = 0
                        part.node_index_2 = 0
                        part.node_index_3 = 0
                        part.node_weight_0 = 0.0
                        part.node_weight_1 = 0.0
                        part.node_weight_2 = 0.0
                        part.lod_mipmap_magic_number = donor_part.lod_mipmap_magic_number
                        part.unknown = donor_part.unknown # what is this?

                        cache_data.parts.append(part)

                    part_count = len(cache_data.parts)
                    cache_data.parts_header = TAG.TagBlockHeader("tbfd", 0, part_count, 72)
                    cache_data.parts_tag_block = TAG.TagBlock(part_count)

                    cache_data.subparts = donor_cache_data.subparts

                    subpart_count = len(cache_data.subparts)
                    cache_data.subparts_header = TAG.TagBlockHeader("tbfd", 0, subpart_count, 8)
                    cache_data.subparts_tag_block = TAG.TagBlock(subpart_count)

                    cache_data.visibility_bounds = donor_cache_data.visibility_bounds

                    visibility_bound_count = len(cache_data.visibility_bounds)
                    cache_data.visibility_bounds_header = TAG.TagBlockHeader("tbfd", 0, visibility_bound_count, 20)
                    cache_data.visibility_bounds_tag_block = TAG.TagBlock(visibility_bound_count)

                    cache_data.raw_vertices = []
                    for cluster_vertex_idx, cluster_vertex in enumerate(cluster_ob.data.vertices):
                        donor_vertex = donor_cache_data.raw_vertices[cluster_vertex_idx]
                        vertex_loop = None
                        for loop in cluster_ob.data.loops:
                            if loop.vertex_index == cluster_vertex_idx:
                                vertex_loop = loop

                        uv = cluster_ob.data.uv_layers.active.data[vertex_loop.index].uv

                        vertex = LightmapAsset.RawVertex()
                        vertex.position = (cluster_ob.matrix_world @ cluster_vertex.co) / 100
                        vertex.node_index_0_old = 0
                        vertex.node_index_1_old = 0
                        vertex.node_index_2_old = 0
                        vertex.node_index_3_old = 0
                        vertex.node_weight_0 = 0.0
                        vertex.node_weight_1 = 0.0
                        vertex.node_weight_2 = 0.0
                        vertex.node_weight_3 = 0.0
                        vertex.node_index_0_new = 0
                        vertex.node_index_1_new = 0
                        vertex.node_index_2_new = 0
                        vertex.node_index_3_new = 0
                        vertex.uses_new_node_indices = 1
                        vertex.adjusted_compound_node_index = -1
                        vertex.texcoord = donor_vertex.texcoord
                        vertex.normal = donor_vertex.normal
                        vertex.binormal = donor_vertex.binormal
                        vertex.tangent = donor_vertex.tangent
                        vertex.anisotropic_binormal = donor_vertex.anisotropic_binormal
                        vertex.secondary_texcoord = donor_vertex.secondary_texcoord
                        vertex.primary_lightmap_color_RGBA = donor_vertex.primary_lightmap_color_RGBA
                        vertex.primary_lightmap_texcoord = uv
                        vertex.primary_lightmap_incident_direction = donor_vertex.primary_lightmap_incident_direction

                        cache_data.raw_vertices.append(vertex)

                    raw_vertex_count = len(cache_data.raw_vertices)
                    cache_data.raw_vertices_header = TAG.TagBlockHeader("tbfd", 0, raw_vertex_count, 196)
                    cache_data.raw_vertices_tag_block = TAG.TagBlock(raw_vertex_count)

                    cache_data.strip_indices = donor_cache_data.strip_indices

                    strip_index_count = len(cache_data.strip_indices)
                    cache_data.strip_indices_header = TAG.TagBlockHeader("tbfd", 0, strip_index_count, 2)
                    cache_data.strip_indices_tag_block = TAG.TagBlock(strip_index_count)

                    cache_data.visibility_mopp_code_tag_data = donor_cache_data.visibility_mopp_code_tag_data

                    cache_data.mopp_reorder_table = donor_cache_data.mopp_reorder_table

                    mopp_reorder_table_count = len(cache_data.mopp_reorder_table)
                    cache_data.mopp_reorder_table_header = TAG.TagBlockHeader("tbfd", 0, mopp_reorder_table_count, 2)
                    cache_data.mopp_reorder_table_tag_block = TAG.TagBlock(mopp_reorder_table_count)

                    cache_data.vertex_buffers = donor_cache_data.vertex_buffers

                    vertex_buffer_count = len(cache_data.vertex_buffers)
                    cache_data.vertex_buffers_header = TAG.TagBlockHeader("tbfd", 0, vertex_buffer_count, 32)
                    cache_data.vertex_buffers_tag_block = TAG.TagBlock(vertex_buffer_count)

                    cluster.cache_data.append(cache_data)
                    cache_data_count = len(cluster.cache_data)
                    cluster.cache_data_header = TAG.TagBlockHeader("tbfd", 0, cache_data_count, 108)
                    cluster.cache_data_tag_block = TAG.TagBlock(cache_data_count)

                    clusters.append(cluster)

    return clusters

def generate_lightmap_groups(TAG, DONOR_ASSET, bsp_index):
    donor_lightmap_group = None
    if DONOR_ASSET and len(DONOR_ASSET.lightmap_groups) > 0:
        donor_lightmap_group = DONOR_ASSET.lightmap_groups[0]

    lightmap_group = LightmapAsset.LightmapGroup()
    lightmap_group.section_palette = []
    lightmap_group.writable_palettes = []
    lightmap_group.clusters = []
    lightmap_group.bitmap_group_tag_ref = []
    lightmap_group.cluster_render_info = []
    lightmap_group.poop_definitions = []
    lightmap_group.lighting_environments = []
    lightmap_group.geometry_buckets = []
    lightmap_group.instance_render_info = []
    lightmap_group.instance_bucket_refs = []
    lightmap_group.scenery_object_info = []
    lightmap_group.scenery_object_bucket_refs = []
    if donor_lightmap_group:
        lightmap_group.group_type = donor_lightmap_group.group_type
        lightmap_group.group_flags = donor_lightmap_group.group_flags
        lightmap_group.structure_checksum = donor_lightmap_group.structure_checksum

        lightmap_group.section_palette = donor_lightmap_group.section_palette
        lightmap_group.writable_palettes = donor_lightmap_group.writable_palettes
        lightmap_group.clusters = get_clusters(TAG, donor_lightmap_group, bsp_index)
        lightmap_group.bitmap_group_tag_ref = donor_lightmap_group.bitmap_group_tag_ref
        lightmap_group.cluster_render_info = donor_lightmap_group.cluster_render_info
        lightmap_group.poop_definitions = donor_lightmap_group.poop_definitions
        lightmap_group.lighting_environments = donor_lightmap_group.lighting_environments
        lightmap_group.geometry_buckets = donor_lightmap_group.geometry_buckets
        lightmap_group.instance_render_info = donor_lightmap_group.instance_render_info
        lightmap_group.instance_bucket_refs = donor_lightmap_group.instance_bucket_refs
        lightmap_group.scenery_object_info = donor_lightmap_group.scenery_object_info
        lightmap_group.scenery_object_bucket_refs = donor_lightmap_group.scenery_object_bucket_refs

    section_palette_count = len(lightmap_group.section_palette)
    writable_palettes_count = len(lightmap_group.writable_palettes)
    clusters_count = len(lightmap_group.clusters)
    cluster_render_info_count = len(lightmap_group.cluster_render_info)
    poop_definitions_count = len(lightmap_group.poop_definitions)
    lighting_environments_count = len(lightmap_group.lighting_environments)
    geometry_buckets_count = len(lightmap_group.geometry_buckets)
    instance_render_info_count = len(lightmap_group.instance_render_info)
    instance_bucket_refs_count = len(lightmap_group.instance_bucket_refs)
    scenery_object_info_count = len(lightmap_group.instance_bucket_refs)
    scenery_object_bucket_refs_count = len(lightmap_group.instance_bucket_refs)

    lightmap_group.section_palette_header = TAG.TagBlockHeader("tbfd", 0, section_palette_count, 1024)
    lightmap_group.writable_palettes_header = TAG.TagBlockHeader("tbfd", 0, writable_palettes_count, 1024)
    lightmap_group.clusters_header = TAG.TagBlockHeader("tbfd", 0, clusters_count, 96)
    lightmap_group.cluster_render_info_header = TAG.TagBlockHeader("tbfd", 0, cluster_render_info_count, 4)
    lightmap_group.poop_definitions_header = TAG.TagBlockHeader("tbfd", 0, poop_definitions_count, 96)
    lightmap_group.lighting_environments_header = TAG.TagBlockHeader("tbfd", 0, lighting_environments_count, 220)
    lightmap_group.geometry_buckets_header = TAG.TagBlockHeader("tbfd", 0, geometry_buckets_count, 68)
    lightmap_group.instance_render_info_header = TAG.TagBlockHeader("tbfd", 0, instance_render_info_count, 4)
    lightmap_group.instance_bucket_refs_header = TAG.TagBlockHeader("tbfd", 0, instance_bucket_refs_count, 16)
    lightmap_group.scenery_object_info_header = TAG.TagBlockHeader("tbfd", 0, scenery_object_info_count, 12)
    lightmap_group.scenery_object_bucket_refs_header = TAG.TagBlockHeader("tbfd", 0, scenery_object_bucket_refs_count, 16)

    lightmap_group.section_palette_tag_block = TAG.TagBlock(section_palette_count)
    lightmap_group.writable_palettes_tag_block = TAG.TagBlock(writable_palettes_count)
    lightmap_group.clusters_tag_block = TAG.TagBlock(clusters_count)
    lightmap_group.cluster_render_info_tag_block = TAG.TagBlock(cluster_render_info_count)
    lightmap_group.poop_definitions_tag_block = TAG.TagBlock(poop_definitions_count)
    lightmap_group.lighting_environments_tag_block = TAG.TagBlock(lighting_environments_count)
    lightmap_group.geometry_buckets_tag_block = TAG.TagBlock(geometry_buckets_count)
    lightmap_group.instance_render_info_tag_block = TAG.TagBlock(instance_render_info_count)
    lightmap_group.instance_bucket_refs_tag_block = TAG.TagBlock(instance_bucket_refs_count)
    lightmap_group.scenery_object_info_tag_block = TAG.TagBlock(scenery_object_info_count)
    lightmap_group.scenery_object_bucket_refs_tag_block = TAG.TagBlock(scenery_object_bucket_refs_count)

    return lightmap_group

def create_tag(TAG):
    LIGHTMAP = LightmapAsset()
    TAG.is_legacy = False

    LIGHTMAP.header = TAG.Header()
    LIGHTMAP.header.unk1 = 0
    LIGHTMAP.header.flags = 0
    LIGHTMAP.header.type = 0
    LIGHTMAP.header.name = ""
    LIGHTMAP.header.tag_group = "ltmp"
    LIGHTMAP.header.checksum = -1
    LIGHTMAP.header.data_offset = 64
    LIGHTMAP.header.data_length = 0
    LIGHTMAP.header.unk2 = 0
    LIGHTMAP.header.version = 1
    LIGHTMAP.header.destination = 0
    LIGHTMAP.header.plugin_handle = -1
    LIGHTMAP.header.engine_tag = "BLM!"

    LIGHTMAP.body_header = TAG.TagBlockHeader("tbfd", 0, 1, 268)
    LIGHTMAP.lightmap_groups_header = TAG.TagBlockHeader("tbfd", 0, 1, 156)
    LIGHTMAP.errors_header = TAG.TagBlockHeader("tbfd", 0, 1, 680)

    LIGHTMAP.lightmap_groups = []
    LIGHTMAP.errors = []

    return LIGHTMAP

def process_scene(DONOR_ASSET, bsp_index):
    TAG = tag_format.TagAsset()
    LIGHTMAP = create_tag(TAG)

    LIGHTMAP.lightmap_groups.append(generate_lightmap_groups(TAG, DONOR_ASSET, bsp_index))
    #generate_errors(TAG, DONOR_ASSET)

    LIGHTMAP.lightmap_groups_tag_block = TAG.TagBlock(len(LIGHTMAP.lightmap_groups))
    LIGHTMAP.errors_tag_block = TAG.TagBlock(len(LIGHTMAP.errors))

    return LIGHTMAP
