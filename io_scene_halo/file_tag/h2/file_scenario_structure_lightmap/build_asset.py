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
    LIGHTMAP.body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<f', LIGHTMAP.search_distance_lower_bound))
    output_stream.write(struct.pack('<f', LIGHTMAP.search_distance_upper_bound))
    output_stream.write(struct.pack('<f', LIGHTMAP.luminels_per_world_unit))
    output_stream.write(struct.pack('<f', LIGHTMAP.output_white_reference))
    output_stream.write(struct.pack('<f', LIGHTMAP.output_black_reference))
    output_stream.write(struct.pack('<f', LIGHTMAP.output_schlick_parameter))
    output_stream.write(struct.pack('<f', LIGHTMAP.diffuse_map_scale))
    output_stream.write(struct.pack('<f', LIGHTMAP.sun_scale))
    output_stream.write(struct.pack('<f', LIGHTMAP.sky_scale))
    output_stream.write(struct.pack('<f', LIGHTMAP.indirect_scale))
    output_stream.write(struct.pack('<f', LIGHTMAP.prt_scale))
    output_stream.write(struct.pack('<f', LIGHTMAP.surface_light_scale))
    output_stream.write(struct.pack('<f', LIGHTMAP.scenario_light_scale))
    output_stream.write(struct.pack('<f', LIGHTMAP.lightprobe_interpolation_override))
    output_stream.write(struct.pack('<72x'))
    LIGHTMAP.lightmap_groups_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<12x'))
    LIGHTMAP.errors_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<104x'))

def write_clusters(output_stream, clusters, clusters_header, TAG):
    if len(clusters) > 0:
        clusters_header.write(output_stream, TAG, True)
        for cluster_element in clusters:
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

        for cluster_element in clusters:
            cluster_element.sinf_header.write(output_stream, TAG, True)
            if len(cluster_element.compression_info) > 0:
                cluster_element.compression_info_header.write(output_stream, TAG, True)
                for compression_info_element in cluster_element.compression_info:
                    output_stream.write(struct.pack('<ff', *compression_info_element.position_bounds_x))
                    output_stream.write(struct.pack('<ff', *compression_info_element.position_bounds_y))
                    output_stream.write(struct.pack('<ff', *compression_info_element.position_bounds_z))
                    output_stream.write(struct.pack('<ff', *compression_info_element.texcoord_bounds_x))
                    output_stream.write(struct.pack('<ff', *compression_info_element.texcoord_bounds_y))
                    output_stream.write(struct.pack('<ff', *compression_info_element.secondary_texcoord_bounds_x))
                    output_stream.write(struct.pack('<ff', *compression_info_element.secondary_texcoord_bounds_y))

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

            write_clusters(output_stream, lightmap_group_element.clusters, lightmap_group_element.clusters_header, TAG)

            if len(lightmap_group_element.cluster_render_info) > 0:
                lightmap_group_element.cluster_render_info_header.write(output_stream, TAG, True)
                for cluster_render_info_element in lightmap_group_element.cluster_render_info:
                    output_stream.write(struct.pack('<h', cluster_render_info_element.bitmap_index))
                    output_stream.write(struct.pack('<h', cluster_render_info_element.palette_index))

            write_clusters(output_stream, lightmap_group_element.poop_definitions, lightmap_group_element.poop_definitions_header, TAG)

            if len(lightmap_group_element.lighting_environments) > 0:
                lightmap_group_element.lighting_environments_header.write(output_stream, TAG, True)
                for lighting_environment_element in lightmap_group_element.lighting_environments:
                    output_stream.write(struct.pack('<fff', *lighting_environment_element.sample_point))
                    output_stream.write(struct.pack('<f', lighting_environment_element.red_coefficient_0))
                    output_stream.write(struct.pack('<f', lighting_environment_element.red_coefficient_1))
                    output_stream.write(struct.pack('<f', lighting_environment_element.red_coefficient_2))
                    output_stream.write(struct.pack('<f', lighting_environment_element.red_coefficient_3))
                    output_stream.write(struct.pack('<f', lighting_environment_element.red_coefficient_4))
                    output_stream.write(struct.pack('<f', lighting_environment_element.red_coefficient_5))
                    output_stream.write(struct.pack('<f', lighting_environment_element.red_coefficient_6))
                    output_stream.write(struct.pack('<f', lighting_environment_element.red_coefficient_7))
                    output_stream.write(struct.pack('<f', lighting_environment_element.red_coefficient_8))
                    output_stream.write(struct.pack('<f', lighting_environment_element.green_coefficient_0))
                    output_stream.write(struct.pack('<f', lighting_environment_element.green_coefficient_1))
                    output_stream.write(struct.pack('<f', lighting_environment_element.green_coefficient_2))
                    output_stream.write(struct.pack('<f', lighting_environment_element.green_coefficient_3))
                    output_stream.write(struct.pack('<f', lighting_environment_element.green_coefficient_4))
                    output_stream.write(struct.pack('<f', lighting_environment_element.green_coefficient_5))
                    output_stream.write(struct.pack('<f', lighting_environment_element.green_coefficient_6))
                    output_stream.write(struct.pack('<f', lighting_environment_element.green_coefficient_7))
                    output_stream.write(struct.pack('<f', lighting_environment_element.green_coefficient_8))
                    output_stream.write(struct.pack('<f', lighting_environment_element.blue_coefficient_0))
                    output_stream.write(struct.pack('<f', lighting_environment_element.blue_coefficient_1))
                    output_stream.write(struct.pack('<f', lighting_environment_element.blue_coefficient_2))
                    output_stream.write(struct.pack('<f', lighting_environment_element.blue_coefficient_3))
                    output_stream.write(struct.pack('<f', lighting_environment_element.blue_coefficient_4))
                    output_stream.write(struct.pack('<f', lighting_environment_element.blue_coefficient_5))
                    output_stream.write(struct.pack('<f', lighting_environment_element.blue_coefficient_6))
                    output_stream.write(struct.pack('<f', lighting_environment_element.blue_coefficient_7))
                    output_stream.write(struct.pack('<f', lighting_environment_element.blue_coefficient_8))
                    output_stream.write(struct.pack('<fff', *lighting_environment_element.mean_incoming_light_direction))
                    output_stream.write(struct.pack('<fff', *lighting_environment_element.incoming_light_intensity))
                    output_stream.write(struct.pack('<i', lighting_environment_element.specular_bitmap_index))
                    output_stream.write(struct.pack('<fff', *lighting_environment_element.rotation_axis))
                    output_stream.write(struct.pack('<f', lighting_environment_element.rotation_speed))
                    output_stream.write(struct.pack('<fff', *lighting_environment_element.bump_direction))
                    R, G, B, A = lighting_environment_element.color_tint_RGBA
                    output_stream.write(struct.pack('<fff', R, G, B))
                    output_stream.write(struct.pack('<H', lighting_environment_element.procedural_override))
                    output_stream.write(struct.pack('<H', lighting_environment_element.flags))
                    output_stream.write(struct.pack('<fff', *lighting_environment_element.procedural_param0))
                    output_stream.write(struct.pack('<fff', *lighting_environment_element.procedural_param1_xyz))
                    output_stream.write(struct.pack('<f', lighting_environment_element.procedural_param1_w))

            if len(lightmap_group_element.geometry_buckets) > 0:
                lightmap_group_element.geometry_buckets_header.write(output_stream, TAG, True)
                for geometry_bucket_element in lightmap_group_element.geometry_buckets:
                    output_stream.write(struct.pack('<H', geometry_bucket_element.flags))
                    output_stream.write(struct.pack('<2x'))
                    geometry_bucket_element.raw_vertices_tag_block.write(output_stream, False)
                    output_stream.write(struct.pack('<i', geometry_bucket_element.block_offset))
                    output_stream.write(struct.pack('<i', geometry_bucket_element.block_size))
                    output_stream.write(struct.pack('<i', geometry_bucket_element.section_data_size))
                    output_stream.write(struct.pack('<i', geometry_bucket_element.resource_data_size))
                    geometry_bucket_element.resources_tag_block.write(output_stream, False)
                    output_stream.write(struct.pack('<4x'))
                    output_stream.write(struct.pack('<i', geometry_bucket_element.owner_tag_section_offset))
                    output_stream.write(struct.pack('<4x'))
                    geometry_bucket_element.cache_data_tag_block.write(output_stream, False)

                for geometry_bucket_element in lightmap_group_element.geometry_buckets:
                    if len(geometry_bucket_element.raw_vertices) > 0:
                        geometry_bucket_element.raw_vertices_header.write(output_stream, TAG, True)
                        for raw_vertex in geometry_bucket_element.raw_vertices:
                            R, G, B, A = raw_vertex.primary_lightmap_color_RGBA
                            output_stream.write(struct.pack('<fff', R, G, B))
                            output_stream.write(struct.pack('<fff', *raw_vertex.primary_lightmap_incident_direction))

                    geometry_bucket_element.blok_header.write(output_stream, TAG, True)
                    if len(geometry_bucket_element.resources) > 0:
                        geometry_bucket_element.resources_header.write(output_stream, TAG, True)
                        for resource in geometry_bucket_element.resources:
                            output_stream.write(struct.pack('<H', resource.resource_type))
                            output_stream.write(struct.pack('<2x'))
                            output_stream.write(struct.pack('<h', resource.primary_locator))
                            output_stream.write(struct.pack('<h', resource.secondary_locator))
                            output_stream.write(struct.pack('<i', resource.resource_data_size))
                            output_stream.write(struct.pack('<i', resource.resource_data_offset))

                    if len(geometry_bucket_element.cache_data) > 0:
                        geometry_bucket_element.cache_data_header.write(output_stream, TAG, True)
                        for cache_data in geometry_bucket_element.cache_data:
                            cache_data.vertex_buffers_tag_block.write(output_stream, False)

                        for cache_data in geometry_bucket_element.cache_data:
                            if len(cache_data.vertex_buffers) > 0:
                                cache_data.vertex_buffers_header.write(output_stream, TAG, True)
                                for vertex_buffer in cache_data.vertex_buffers:
                                    output_stream.write(vertex_buffer)

            if len(lightmap_group_element.instance_render_info) > 0:
                lightmap_group_element.instance_render_info_header.write(output_stream, TAG, True)
                for instance_render_info in lightmap_group_element.instance_render_info:
                    output_stream.write(struct.pack('<h', instance_render_info.bitmap_index))
                    output_stream.write(struct.pack('<h', instance_render_info.palette_index))

            if len(lightmap_group_element.instance_bucket_refs) > 0:
                lightmap_group_element.instance_bucket_refs_header.write(output_stream, TAG, True)
                for instance_bucket_ref in lightmap_group_element.instance_bucket_refs:
                    output_stream.write(struct.pack('<h', instance_bucket_ref.flags))
                    output_stream.write(struct.pack('<h', instance_bucket_ref.bucket_index))
                    instance_bucket_ref.section_offsets_tag_block.write(output_stream, False)

                for instance_bucket_ref in lightmap_group_element.instance_bucket_refs:
                    if len(instance_bucket_ref.section_offsets) > 0:
                        instance_bucket_ref.section_offsets_header.write(output_stream, TAG, True)
                        for section_offset in instance_bucket_ref.section_offsets:
                            output_stream.write(struct.pack('<h', section_offset))

            if len(lightmap_group_element.scenery_object_info) > 0:
                lightmap_group_element.scenery_object_info_header.write(output_stream, TAG, True)
                for scenery_object_info in lightmap_group_element.scenery_object_info:
                    output_stream.write(struct.pack('<i', scenery_object_info.unique_id))
                    output_stream.write(struct.pack('<h', scenery_object_info.origin_bsp_index))
                    output_stream.write(struct.pack('<b', scenery_object_info.object_type))
                    output_stream.write(struct.pack('<b', scenery_object_info.source))
                    output_stream.write(struct.pack('<i', scenery_object_info.render_model_checksum))

            if len(lightmap_group_element.scenery_object_bucket_refs) > 0:
                lightmap_group_element.scenery_object_bucket_refs_header.write(output_stream, TAG, True)
                for scenery_object_bucket_ref in lightmap_group_element.scenery_object_bucket_refs:
                    output_stream.write(struct.pack('<h', scenery_object_bucket_ref.flags))
                    output_stream.write(struct.pack('<h', scenery_object_bucket_ref.bucket_index))
                    scenery_object_bucket_ref.section_offsets_tag_block.write(output_stream, False)

                for scenery_object_bucket_ref in lightmap_group_element.scenery_object_bucket_refs:
                    if len(scenery_object_bucket_ref.section_offsets) > 0:
                        scenery_object_bucket_ref.section_offsets_header.write(output_stream, TAG, True)
                        for section_offset in scenery_object_bucket_ref.section_offsets:
                            output_stream.write(struct.pack('<h', section_offset))

def write_errors(output_stream, LIGHTMAP, TAG):
    if len(LIGHTMAP.errors) > 0:
        LIGHTMAP.errors_header.write(output_stream, TAG, True)
        for error in LIGHTMAP.errors:
            output_stream.write(struct.pack('<255sx', tag_format.string_to_bytes(error.name, False)))
            output_stream.write(struct.pack('<H', error.report_type))
            output_stream.write(struct.pack('<H', error.flags))
            output_stream.write(struct.pack('<408x'))
            error.reports_tag_block.write(output_stream, False)

        for error in LIGHTMAP.errors:
            if len(error.reports) > 0:
                error.reports_header.write(output_stream, TAG, True)
                for report in error.reports:
                    output_stream.write(struct.pack('<H', report.type))
                    output_stream.write(struct.pack('<H', report.flags))
                    output_stream.write(struct.pack('<h', report.report_length))
                    output_stream.write(struct.pack('<18x'))
                    output_stream.write(struct.pack('<31sx', tag_format.string_to_bytes(report.source_filename, False)))
                    output_stream.write(struct.pack('<i', report.source_line_number))
                    report.vertices_tag_block.write(output_stream, False)
                    report.vectors_tag_block.write(output_stream, False)
                    report.lines_tag_block.write(output_stream, False)
                    report.triangles_tag_block.write(output_stream, False)
                    report.quads_tag_block.write(output_stream, False)
                    report.comments_tag_block.write(output_stream, False)
                    output_stream.write(struct.pack('<380x'))
                    output_stream.write(struct.pack('<i', report.report_key))
                    output_stream.write(struct.pack('<i', report.node_index))
                    output_stream.write(struct.pack('<ff', *report.bounds_x))
                    output_stream.write(struct.pack('<ff', *report.bounds_y))
                    output_stream.write(struct.pack('<ff', *report.bounds_z))
                    R, G, B, A = report.color
                    output_stream.write(struct.pack('<ffff', A, R, G, B))
                    output_stream.write(struct.pack('<84x'))

                for report in error.reports:
                    if report.report_length > 0:
                        output_stream.write(struct.pack('<%ssx' % (len(report.text)), tag_format.string_to_bytes(report.text, False)))

                    if len(report.vertices) > 0:
                        report.vertices_header.write(output_stream, TAG, True)
                        for vertex in report.vertices:
                            output_stream.write(struct.pack('<fff', *vertex.position))
                            output_stream.write(struct.pack('<b', vertex.node_index_0))
                            output_stream.write(struct.pack('<b', vertex.node_index_1))
                            output_stream.write(struct.pack('<b', vertex.node_index_2))
                            output_stream.write(struct.pack('<b', vertex.node_index_3))
                            output_stream.write(struct.pack('<f', vertex.node_weight_0))
                            output_stream.write(struct.pack('<f', vertex.node_weight_1))
                            output_stream.write(struct.pack('<f', vertex.node_weight_2))
                            output_stream.write(struct.pack('<f', vertex.node_weight_3))
                            R, G, B, A = vertex.color
                            output_stream.write(struct.pack('<ffff', A, R, G, B))
                            output_stream.write(struct.pack('<f', vertex.screen_size))

                    if len(report.vectors) > 0:
                        report.vectors_header.write(output_stream, TAG, True)
                        for vector in report.vectors:
                            output_stream.write(struct.pack('<fff', *vector.position))
                            output_stream.write(struct.pack('<b', vector.node_index_0))
                            output_stream.write(struct.pack('<b', vector.node_index_1))
                            output_stream.write(struct.pack('<b', vector.node_index_2))
                            output_stream.write(struct.pack('<b', vector.node_index_3))
                            output_stream.write(struct.pack('<f', vector.node_weight_0))
                            output_stream.write(struct.pack('<f', vector.node_weight_1))
                            output_stream.write(struct.pack('<f', vector.node_weight_2))
                            output_stream.write(struct.pack('<f', vector.node_weight_3))
                            R, G, B, A = vector.color
                            output_stream.write(struct.pack('<ffff', A, R, G, B))
                            output_stream.write(struct.pack('<fff', *vector.normal))
                            output_stream.write(struct.pack('<f', vector.screen_length))

                    if len(report.lines) > 0:
                        report.lines_header.write(output_stream, TAG, True)
                        for line in report.lines:
                            output_stream.write(struct.pack('<fff', *line.position_a))
                            output_stream.write(struct.pack('<b', line.node_index_a_0))
                            output_stream.write(struct.pack('<b', line.node_index_a_1))
                            output_stream.write(struct.pack('<b', line.node_index_a_2))
                            output_stream.write(struct.pack('<b', line.node_index_a_3))
                            output_stream.write(struct.pack('<f', line.node_weight_a_0))
                            output_stream.write(struct.pack('<f', line.node_weight_a_1))
                            output_stream.write(struct.pack('<f', line.node_weight_a_2))
                            output_stream.write(struct.pack('<f', line.node_weight_a_3))
                            output_stream.write(struct.pack('<fff', *line.position_b))
                            output_stream.write(struct.pack('<b', line.node_index_b_0))
                            output_stream.write(struct.pack('<b', line.node_index_b_1))
                            output_stream.write(struct.pack('<b', line.node_index_b_2))
                            output_stream.write(struct.pack('<b', line.node_index_b_3))
                            output_stream.write(struct.pack('<f', line.node_weight_b_0))
                            output_stream.write(struct.pack('<f', line.node_weight_b_1))
                            output_stream.write(struct.pack('<f', line.node_weight_b_2))
                            output_stream.write(struct.pack('<f', line.node_weight_b_3))
                            R, G, B, A = line.color
                            output_stream.write(struct.pack('<ffff', A, R, G, B))

                    if len(report.triangles) > 0:
                        report.triangles_header.write(output_stream, TAG, True)
                        for triangle in report.triangles:
                            output_stream.write(struct.pack('<fff', *triangle.position_a))
                            output_stream.write(struct.pack('<b', triangle.node_index_a_0))
                            output_stream.write(struct.pack('<b', triangle.node_index_a_1))
                            output_stream.write(struct.pack('<b', triangle.node_index_a_2))
                            output_stream.write(struct.pack('<b', triangle.node_index_a_3))
                            output_stream.write(struct.pack('<f', triangle.node_weight_a_0))
                            output_stream.write(struct.pack('<f', triangle.node_weight_a_1))
                            output_stream.write(struct.pack('<f', triangle.node_weight_a_2))
                            output_stream.write(struct.pack('<f', triangle.node_weight_a_3))
                            output_stream.write(struct.pack('<fff', *triangle.position_b))
                            output_stream.write(struct.pack('<b', triangle.node_index_b_0))
                            output_stream.write(struct.pack('<b', triangle.node_index_b_1))
                            output_stream.write(struct.pack('<b', triangle.node_index_b_2))
                            output_stream.write(struct.pack('<b', triangle.node_index_b_3))
                            output_stream.write(struct.pack('<f', triangle.node_weight_b_0))
                            output_stream.write(struct.pack('<f', triangle.node_weight_b_1))
                            output_stream.write(struct.pack('<f', triangle.node_weight_b_2))
                            output_stream.write(struct.pack('<f', triangle.node_weight_b_3))
                            output_stream.write(struct.pack('<fff', *triangle.position_c))
                            output_stream.write(struct.pack('<b', triangle.node_index_c_0))
                            output_stream.write(struct.pack('<b', triangle.node_index_c_1))
                            output_stream.write(struct.pack('<b', triangle.node_index_c_2))
                            output_stream.write(struct.pack('<b', triangle.node_index_c_3))
                            output_stream.write(struct.pack('<f', triangle.node_weight_c_0))
                            output_stream.write(struct.pack('<f', triangle.node_weight_c_1))
                            output_stream.write(struct.pack('<f', triangle.node_weight_c_2))
                            output_stream.write(struct.pack('<f', triangle.node_weight_c_3))
                            R, G, B, A = triangle.color
                            output_stream.write(struct.pack('<ffff', A, R, G, B))

                    if len(report.quads) > 0:
                        report.quads_header.write(output_stream, TAG, True)
                        for quad in report.quads:
                            output_stream.write(struct.pack('<fff', *quad.position_a))
                            output_stream.write(struct.pack('<b', quad.node_index_a_0))
                            output_stream.write(struct.pack('<b', quad.node_index_a_1))
                            output_stream.write(struct.pack('<b', quad.node_index_a_2))
                            output_stream.write(struct.pack('<b', quad.node_index_a_3))
                            output_stream.write(struct.pack('<f', quad.node_weight_a_0))
                            output_stream.write(struct.pack('<f', quad.node_weight_a_1))
                            output_stream.write(struct.pack('<f', quad.node_weight_a_2))
                            output_stream.write(struct.pack('<f', quad.node_weight_a_3))
                            output_stream.write(struct.pack('<fff', *quad.position_b))
                            output_stream.write(struct.pack('<b', quad.node_index_b_0))
                            output_stream.write(struct.pack('<b', quad.node_index_b_1))
                            output_stream.write(struct.pack('<b', quad.node_index_b_2))
                            output_stream.write(struct.pack('<b', quad.node_index_b_3))
                            output_stream.write(struct.pack('<f', quad.node_weight_b_0))
                            output_stream.write(struct.pack('<f', quad.node_weight_b_1))
                            output_stream.write(struct.pack('<f', quad.node_weight_b_2))
                            output_stream.write(struct.pack('<f', quad.node_weight_b_3))
                            output_stream.write(struct.pack('<fff', *quad.position_c))
                            output_stream.write(struct.pack('<b', quad.node_index_c_0))
                            output_stream.write(struct.pack('<b', quad.node_index_c_1))
                            output_stream.write(struct.pack('<b', quad.node_index_c_2))
                            output_stream.write(struct.pack('<b', quad.node_index_c_3))
                            output_stream.write(struct.pack('<f', quad.node_weight_c_0))
                            output_stream.write(struct.pack('<f', quad.node_weight_c_1))
                            output_stream.write(struct.pack('<f', quad.node_weight_c_2))
                            output_stream.write(struct.pack('<f', quad.node_weight_c_3))
                            output_stream.write(struct.pack('<fff', *quad.position_d))
                            output_stream.write(struct.pack('<b', quad.node_index_d_0))
                            output_stream.write(struct.pack('<b', quad.node_index_d_1))
                            output_stream.write(struct.pack('<b', quad.node_index_d_2))
                            output_stream.write(struct.pack('<b', quad.node_index_d_3))
                            output_stream.write(struct.pack('<f', quad.node_weight_d_0))
                            output_stream.write(struct.pack('<f', quad.node_weight_d_1))
                            output_stream.write(struct.pack('<f', quad.node_weight_d_2))
                            output_stream.write(struct.pack('<f', quad.node_weight_d_3))
                            R, G, B, A = quad.color
                            output_stream.write(struct.pack('<ffff', A, R, G, B))

                    if len(report.comments) > 0:
                        report.comments_header.write(output_stream, TAG, True)
                        for comment in report.comments:
                            output_stream.write(struct.pack('<h', comment.text_length))
                            output_stream.write(struct.pack('<18x'))
                            output_stream.write(struct.pack('<fff', *comment.position))
                            output_stream.write(struct.pack('<b', comment.node_index_0))
                            output_stream.write(struct.pack('<b', comment.node_index_1))
                            output_stream.write(struct.pack('<b', comment.node_index_2))
                            output_stream.write(struct.pack('<b', comment.node_index_3))
                            output_stream.write(struct.pack('<f', comment.node_weight_0))
                            output_stream.write(struct.pack('<f', comment.node_weight_1))
                            output_stream.write(struct.pack('<f', comment.node_weight_2))
                            output_stream.write(struct.pack('<f', comment.node_weight_3))
                            R, G, B, A = comment.color
                            output_stream.write(struct.pack('<ffff', A, R, G, B))

                        for comment in report.comments:
                            if comment.text_length > 0:
                                output_stream.write(struct.pack('<%ssx' % (len(comment.text)), tag_format.string_to_bytes(comment.text, False)))

def build_asset(output_stream, LIGHTMAP, report):
    TAG = tag_format.TagAsset()
    TAG.big_endian = False

    LIGHTMAP.header.write(output_stream, False, True)
    write_body(output_stream, LIGHTMAP, TAG)
    write_lightmap_groups(output_stream, LIGHTMAP, TAG)
    write_errors(output_stream, LIGHTMAP, TAG)


