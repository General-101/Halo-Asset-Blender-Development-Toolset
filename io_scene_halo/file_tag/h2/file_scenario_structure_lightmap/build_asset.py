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

import struct
from ....global_functions import tag_format

def write_body(output_stream, LIGHTMAP, TAG):
    LIGHTMAP.lightmap_body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<f', LIGHTMAP.lightmap_body.search_distance_lower_bound))
    output_stream.write(struct.pack('<f', LIGHTMAP.lightmap_body.search_distance_upper_bound))
    output_stream.write(struct.pack('<f', LIGHTMAP.lightmap_body.luminels_per_world_unit))
    output_stream.write(struct.pack('<f', LIGHTMAP.lightmap_body.output_white_reference))
    output_stream.write(struct.pack('<f', LIGHTMAP.lightmap_body.output_black_reference))
    output_stream.write(struct.pack('<f', LIGHTMAP.lightmap_body.output_schlick_parameter))
    output_stream.write(struct.pack('<f', LIGHTMAP.lightmap_body.diffuse_map_scale))
    output_stream.write(struct.pack('<f', LIGHTMAP.lightmap_body.sun_scale))
    output_stream.write(struct.pack('<f', LIGHTMAP.lightmap_body.sky_scale))
    output_stream.write(struct.pack('<f', LIGHTMAP.lightmap_body.indirect_scale))
    output_stream.write(struct.pack('<f', LIGHTMAP.lightmap_body.prt_scale))
    output_stream.write(struct.pack('<f', LIGHTMAP.lightmap_body.surface_light_scale))
    output_stream.write(struct.pack('<f', LIGHTMAP.lightmap_body.scenario_light_scale))
    output_stream.write(struct.pack('<f', LIGHTMAP.lightmap_body.lightprobe_interpolation_override))
    output_stream.write(struct.pack('<72x'))
    LIGHTMAP.lightmap_body.lightmap_groups_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<12x'))
    LIGHTMAP.lightmap_body.errors_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<104x'))

def write_lightmap_groups(output_stream, LIGHTMAP, TAG):
    if len(LIGHTMAP.lightmap_groups) > 0:
        LIGHTMAP.lightmap_groups_header.write(output_stream, TAG, True)
        for lightmap_group_element in LIGHTMAP.lightmap_groups:
            output_stream.write(struct.pack('<H', lightmap_group_element.group_type))
            output_stream.write(struct.pack('<H', lightmap_group_element.group_flags))
            output_stream.write(struct.pack('<i', lightmap_group_element.structure_checksum))
            lightmap_group_element.section_palette_tag_block.write(output_stream, False)
            lightmap_group_element.writable_palettes_tag_block.write(output_stream, False)
            lightmap_group_element.bitmap_group_tag_ref.write(output_stream, False, True)
            lightmap_group_element.clusters_tag_block.write(output_stream, False)
            lightmap_group_element.cluster_render_info_tag_block.write(output_stream, False)
            lightmap_group_element.poop_definitions_tag_block.write(output_stream, False)
            lightmap_group_element.lighting_environments_tag_block.write(output_stream, False)
            lightmap_group_element.geometry_buckets_tag_block.write(output_stream, False)
            lightmap_group_element.instance_render_info_tag_block.write(output_stream, False)
            lightmap_group_element.instance_bucket_refs_tag_block.write(output_stream, False)
            lightmap_group_element.scenery_object_info_tag_block.write(output_stream, False)
            lightmap_group_element.scenery_object_bucket_refs_tag_block.write(output_stream, False)

        for lightmap_group_element in LIGHTMAP.lightmap_groups:
            if len(lightmap_group_element.section_palette) > 0:
                lightmap_group_element.section_palette_header.write(output_stream, TAG, True)
                for section_palette_element in lightmap_group_element.section_palette:
                    output_stream.write(struct.pack('<i', section_palette_element.first_palette_color))
                    output_stream.write(section_palette_element.unknown)

            if len(lightmap_group_element.writable_palettes) > 0:
                lightmap_group_element.writable_palettes_header.write(output_stream, TAG, True)
                for writable_palette_element in lightmap_group_element.writable_palettes:
                    output_stream.write(struct.pack('<i', writable_palette_element.first_palette_color))
                    output_stream.write(writable_palette_element.unknown)

            bitmap_group_name_length = len(lightmap_group_element.bitmap_group_tag_ref.name)
            if bitmap_group_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % bitmap_group_name_length, tag_format.string_to_bytes(lightmap_group_element.bitmap_group_tag_ref.name, False)))

            if len(lightmap_group_element.clusters) > 0:
                lightmap_group_element.clusters_header.write(output_stream, TAG, True)
                for cluster_element in lightmap_group_element.clusters:
                    output_stream.write(struct.pack('<h', cluster_element.total_vertex_count))
                    output_stream.write(struct.pack('<h', cluster_element.total_triangle_count))
                    output_stream.write(struct.pack('<h', cluster_element.total_part_count))
                    output_stream.write(struct.pack('<h', cluster_element.shadow_casting_triangle_count))
                    output_stream.write(struct.pack('<h', cluster_element.shadow_casting_part_count))
                    output_stream.write(struct.pack('<h', cluster_element.opaque_point_count))
                    output_stream.write(struct.pack('<h', cluster_element.opaque_vertex_count))
                    output_stream.write(struct.pack('<h', cluster_element.opaque_part_count))
                    output_stream.write(struct.pack('<b', cluster_element.opaque_max_nodes_vertex))
                    output_stream.write(struct.pack('<b', cluster_element.transparent_max_nodes_vertex))
                    output_stream.write(struct.pack('<b', cluster_element.shadow_casting_rigid_triangle_count))
                    output_stream.write(cluster_element.unknown)
                    output_stream.write(struct.pack('<H', cluster_element.geometry_classification))
                    output_stream.write(struct.pack('<H', cluster_element.geometry_compression_flags))
                    cluster_element.compression_info_tag_block.write(output_stream, False)
                    output_stream.write(struct.pack('<b', cluster_element.hardware_node_count))
                    output_stream.write(struct.pack('<b', cluster_element.node_map_size))
                    output_stream.write(struct.pack('<b', cluster_element.software_plane_count))
                    output_stream.write(struct.pack('<1x'))
                    output_stream.write(struct.pack('<h', cluster_element.total_subpart_count))
                    output_stream.write(struct.pack('<H', cluster_element.section_lighting_flags))
                    output_stream.write(struct.pack('<i', cluster_element.block_offset))
                    output_stream.write(struct.pack('<i', cluster_element.block_size))
                    output_stream.write(struct.pack('<i', cluster_element.section_data_size))
                    output_stream.write(struct.pack('<i', cluster_element.resource_data_size))
                    cluster_element.resource_tag_block.write(output_stream, False)
                    output_stream.write(struct.pack('<4x'))
                    output_stream.write(struct.pack('<i', cluster_element.owner_tag_section_offset))
                    output_stream.write(struct.pack('<4x'))
                    cluster_element.cache_data_tag_block.write(output_stream, False)

                for cluster_element in lightmap_group_element.clusters:
                    cluster_element.sinf_header.write(output_stream, TAG, True)
                    if len(cluster_element.compression_info) > 0:
                        cluster_element.compression_info_header.write(output_stream, TAG, True)
                        for compression_info_element in cluster_element.compression_info:
                            output_stream.write(struct.pack('<ff', compression_info_element.position_bounds_x))
                            output_stream.write(struct.pack('<ff', compression_info_element.position_bounds_y))
                            output_stream.write(struct.pack('<ff', compression_info_element.position_bounds_z))
                            output_stream.write(struct.pack('<ff', compression_info_element.texcoord_bounds_x))
                            output_stream.write(struct.pack('<ff', compression_info_element.texcoord_bounds_y))
                            output_stream.write(struct.pack('<ff', compression_info_element.secondary_texcoord_bounds_x))
                            output_stream.write(struct.pack('<ff', compression_info_element.secondary_texcoord_bounds_y))

                    cluster_element.blok_header.write(output_stream, TAG, True)
                    if len(cluster_element.resources) > 0:
                        cluster_element.resources_header.write(output_stream, TAG, True)
                        for resource_element in cluster_element.resources:
                            output_stream.write(struct.pack('<H', resource_element.resource_type))
                            output_stream.write(struct.pack('<2x'))
                            output_stream.write(struct.pack('<h', resource_element.primary_locator))
                            output_stream.write(struct.pack('<h', resource_element.secondary_locator))
                            output_stream.write(struct.pack('<i', resource_element.resource_data_size))
                            output_stream.write(struct.pack('<i', resource_element.resource_data_offset))

                    if len(cluster_element.cache_data) > 0:
                        cluster_element.cache_data_header.write(output_stream, TAG, True)
                        for cache_data_element in cluster_element.cache_data:
                            cache_data_element.parts_tag_block.write(output_stream, False)
                            cache_data_element.subparts_tag_block.write(output_stream, False)
                            cache_data_element.visibility_bounds_tag_block.write(output_stream, False)
                            cache_data_element.raw_vertices_tag_block.write(output_stream, False)
                            cache_data_element.strip_indices_tag_block.write(output_stream, False)
                            cache_data_element.visibility_mopp_code_tag_data.write(output_stream, False)
                            cache_data_element.mopp_reorder_table_tag_block.write(output_stream, False)
                            cache_data_element.vertex_buffers_tag_block.write(output_stream, False)
                            output_stream.write(struct.pack('<4x'))

                        for cache_data_element in cluster_element.cache_data:
                            cache_data_element.sect_header.write(output_stream, TAG, True)
                            if len(cache_data_element.parts) > 0:
                                cache_data_element.parts_header.write(output_stream, TAG, True)
                                for part_element in cache_data_element.parts:
                                    output_stream.write(struct.pack('<H', part_element.part_type))
                                    output_stream.write(struct.pack('<H', part_element.flags))
                                    output_stream.write(struct.pack('<h', part_element.material_index))
                                    output_stream.write(struct.pack('<h', part_element.strip_start_index))
                                    output_stream.write(struct.pack('<h', part_element.strip_length))
                                    output_stream.write(struct.pack('<h', part_element.first_subpart_index))
                                    output_stream.write(struct.pack('<h', part_element.subpart_count))
                                    output_stream.write(struct.pack('<b', part_element.max_nodes_vertex))
                                    output_stream.write(struct.pack('<b', part_element.contributing_compound_node_count))
                                    output_stream.write(struct.pack('<fff', *part_element.position))
                                    output_stream.write(struct.pack('<b', part_element.node_index_0))
                                    output_stream.write(struct.pack('<b', part_element.node_index_1))
                                    output_stream.write(struct.pack('<b', part_element.node_index_2))
                                    output_stream.write(struct.pack('<b', part_element.node_index_3))
                                    output_stream.write(struct.pack('<f', part_element.node_weight_0))
                                    output_stream.write(struct.pack('<f', part_element.node_weight_1))
                                    output_stream.write(struct.pack('<f', part_element.node_weight_2))
                                    output_stream.write(struct.pack('<f', part_element.lod_mipmap_magic_number))
                                    output_stream.write(part_element.unknown)

                            if len(cache_data_element.subparts) > 0:
                                cache_data_element.subparts_header.write(output_stream, TAG, True)
                                for subpart_element in cache_data_element.subparts:
                                    output_stream.write(struct.pack('<h', subpart_element.indices_start_index))
                                    output_stream.write(struct.pack('<h', subpart_element.indices_length))
                                    output_stream.write(struct.pack('<h', subpart_element.visibility_bounds_index))
                                    output_stream.write(struct.pack('<h', subpart_element.part_index))

                            if len(cache_data_element.visibility_bounds) > 0:
                                cache_data_element.visibility_bounds_header.write(output_stream, TAG, True)
                                for visibility_bound_element in cache_data_element.visibility_bounds:
                                    output_stream.write(struct.pack('<fff', *visibility_bound_element.position))
                                    output_stream.write(struct.pack('<f', visibility_bound_element.radius))
                                    output_stream.write(struct.pack('<h', visibility_bound_element.node_0))
                                    output_stream.write(struct.pack('<2x'))

                            if len(cache_data_element.raw_vertices) > 0:
                                cache_data_element.raw_vertices_header.write(output_stream, TAG, True)
                                for raw_vertex_element in cache_data_element.raw_vertices:
                                    output_stream.write(struct.pack('<fff', *raw_vertex_element.position))
                                    output_stream.write(struct.pack('<i', raw_vertex_element.node_index_0_old))
                                    output_stream.write(struct.pack('<i', raw_vertex_element.node_index_1_old))
                                    output_stream.write(struct.pack('<i', raw_vertex_element.node_index_2_old))
                                    output_stream.write(struct.pack('<i', raw_vertex_element.node_index_3_old))
                                    output_stream.write(struct.pack('<f', raw_vertex_element.node_weight_0))
                                    output_stream.write(struct.pack('<f', raw_vertex_element.node_weight_1))
                                    output_stream.write(struct.pack('<f', raw_vertex_element.node_weight_2))
                                    output_stream.write(struct.pack('<f', raw_vertex_element.node_weight_3))
                                    output_stream.write(struct.pack('<i', raw_vertex_element.node_index_0_new))
                                    output_stream.write(struct.pack('<i', raw_vertex_element.node_index_1_new))
                                    output_stream.write(struct.pack('<i', raw_vertex_element.node_index_2_new))
                                    output_stream.write(struct.pack('<i', raw_vertex_element.node_index_3_new))
                                    output_stream.write(struct.pack('<i', raw_vertex_element.uses_new_node_indices))
                                    output_stream.write(struct.pack('<i', raw_vertex_element.adjusted_compound_node_index))
                                    output_stream.write(struct.pack('<ff', *raw_vertex_element.texcoord))
                                    output_stream.write(struct.pack('<fff', *raw_vertex_element.normal))
                                    output_stream.write(struct.pack('<fff', *raw_vertex_element.binormal))
                                    output_stream.write(struct.pack('<fff', *raw_vertex_element.tangent))
                                    output_stream.write(struct.pack('<fff', *raw_vertex_element.anisotropic_binormal))
                                    output_stream.write(struct.pack('<ff', *raw_vertex_element.secondary_texcoord))
                                    R, G, B, A = raw_vertex_element.primary_lightmap_color_RGBA
                                    output_stream.write(struct.pack('<fff', R, G, B))
                                    output_stream.write(struct.pack('<ff', *raw_vertex_element.primary_lightmap_texcoord))
                                    output_stream.write(struct.pack('<fff', *raw_vertex_element.primary_lightmap_incident_direction))
                                    output_stream.write(struct.pack('<32x'))

                            if len(cache_data_element.strip_indices) > 0:
                                cache_data_element.strip_indices_header.write(output_stream, TAG, True)
                                for strip_index_element in cache_data_element.strip_indices:
                                    output_stream.write(struct.pack('<h', strip_index_element))
     
                            output_stream.write(cache_data_element.visibility_mopp_code_tag_data.data)

                            if len(cache_data_element.mopp_reorder_table) > 0:
                                cache_data_element.mopp_reorder_table_header.write(output_stream, TAG, True)
                                for mopp_reorder_table_element in cache_data_element.mopp_reorder_table:
                                    output_stream.write(struct.pack('<h', mopp_reorder_table_element))

                            if len(cache_data_element.vertex_buffers) > 0:
                                cache_data_element.vertex_buffers_header.write(output_stream, TAG, True)
                                for vertex_buffer_element in cache_data_element.vertex_buffers:
                                    output_stream.write(vertex_buffer_element)

            if len(lightmap_group_element.cluster_render_info) > 0:
                lightmap_group_element.cluster_render_info_header.write(output_stream, TAG, True)
                for cluster_render_info_element in lightmap_group_element.cluster_render_info:
                    output_stream.write(struct.pack('<h', cluster_render_info_element.bitmap_index))
                    output_stream.write(struct.pack('<h', cluster_render_info_element.palette_index))

def write_errors(output_stream, SCENARIO, TAG):
    print("TODO")

def build_asset(output_stream, LIGHTMAP, report):
    TAG = tag_format.TagAsset()
    TAG.big_endian = False

    LIGHTMAP.header.write(output_stream, False, True)
    write_body(output_stream, LIGHTMAP, TAG)
    write_lightmap_groups(output_stream, LIGHTMAP, TAG)
    write_errors(output_stream, LIGHTMAP, TAG)


