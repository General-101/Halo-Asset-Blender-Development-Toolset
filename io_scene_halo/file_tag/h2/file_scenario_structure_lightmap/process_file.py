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

from xml.dom import minidom
from ....global_functions import tag_format
from .format import (
                LightmapAsset,
                GroupTypeEnum,
                GroupFlags,
                GeometryClassificationEnum,
                GeometryCompressionFlags,
                SectionLightingFlags,
                ResourceTypeEnum,
                PartTypeEnum,
                PartFlags,
                ProceduralOverrideEnum,
                LightingEnvironmentFlags,
                GeometryBucketFlags
                )

from ....file_tag.h2.file_scenario_structure_bsp.format import (
        ReportTypeEnum,
        ReportFlags
        )

from mathutils import Vector, Quaternion

XML_OUTPUT = False

def read_lightmap_groups(LIGHTMAP, TAG, input_stream, tag_node, XML_OUTPUT):
    LIGHTMAP.lightmap_groups = []
    lightmap_group_count = LIGHTMAP.lightmap_body.lightmap_groups_tag_block.count
    if lightmap_group_count > 0:
        lightmap_group_node = tag_format.get_xml_node(XML_OUTPUT, lightmap_group_count, tag_node, "name", "lightmap groups")
        LIGHTMAP.lightmap_groups_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for lightmap_group_idx in range(lightmap_group_count):
            lightmap_group_element_node = None
            if XML_OUTPUT:
                lightmap_group_element_node = TAG.xml_doc.createElement('element')
                lightmap_group_element_node.setAttribute('index', str(lightmap_group_idx))
                lightmap_group_node.appendChild(lightmap_group_element_node)

            lightmap_group = LIGHTMAP.LightmapGroup()
            lightmap_group.group_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "type", GroupTypeEnum))
            lightmap_group.group_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "flags", GroupFlags))
            lightmap_group.structure_checksum = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "structure checksum"))
            lightmap_group.section_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "section palette"))
            lightmap_group.writable_palettes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "writable palettes"))
            lightmap_group.bitmap_group_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "bitmap group"))
            lightmap_group.clusters_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "clusters"))
            lightmap_group.cluster_render_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "cluster render info"))
            lightmap_group.poop_definitions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "poop definitions"))
            lightmap_group.lighting_environments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "lighting environments"))
            lightmap_group.geometry_buckets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "geometry buckets"))
            lightmap_group.instance_render_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "instance render info"))
            lightmap_group.instance_bucket_refs_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "instance bucket refs"))
            lightmap_group.scenery_object_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "scenery object info"))
            lightmap_group.scenery_object_bucket_refs_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(lightmap_group_element_node, "scenery object bucket refs"))

            LIGHTMAP.lightmap_groups.append(lightmap_group)

        for lightmap_group_idx, lightmap_group in enumerate(LIGHTMAP.lightmap_groups):
            lightmap_group_element_node = None
            if XML_OUTPUT:
                lightmap_group_element_node = lightmap_group_node.childNodes[lightmap_group_idx]

            lightmap_group.section_palette = []
            section_palette_count = lightmap_group.section_palette_tag_block.count
            if section_palette_count > 0:
                section_palette_node = tag_format.get_xml_node(XML_OUTPUT, section_palette_count, lightmap_group_element_node, "name", "section palette")
                lightmap_group.section_palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for section_palette_idx in range(section_palette_count):
                    section_palette_element_node = None
                    if XML_OUTPUT:
                        section_palette_element_node = TAG.xml_doc.createElement('element')
                        section_palette_element_node.setAttribute('index', str(section_palette_idx))
                        section_palette_node.appendChild(section_palette_element_node)

                    palette_color = LIGHTMAP.PaletteColor()
                    palette_color.first_palette_color = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(section_palette_element_node, "first palette color"))
                    palette_color.unknown = input_stream.read(1020)

                    lightmap_group.section_palette.append(palette_color)

            lightmap_group.writable_palettes = []
            writable_palette_count = lightmap_group.writable_palettes_tag_block.count
            if writable_palette_count > 0:
                writable_palette_node = tag_format.get_xml_node(XML_OUTPUT, writable_palette_count, lightmap_group_element_node, "name", "writable palettes")
                lightmap_group.writable_palettes_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for writable_palette_idx in range(writable_palette_count):
                    writable_palette_element_node = None
                    if XML_OUTPUT:
                        writable_palette_element_node = TAG.xml_doc.createElement('element')
                        writable_palette_element_node.setAttribute('index', str(writable_palette_idx))
                        writable_palette_node.appendChild(writable_palette_element_node)

                    palette_color = LIGHTMAP.PaletteColor()
                    palette_color.first_palette_color = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(section_palette_element_node, "first palette color"))
                    palette_color.unknown = input_stream.read(1020)

                    lightmap_group.writable_palettes.append(palette_color)

            bitmap_group_name_length = lightmap_group.bitmap_group_tag_ref.name_length
            if bitmap_group_name_length > 0:
                lightmap_group.bitmap_group_tag_ref.name = TAG.read_variable_string(input_stream, bitmap_group_name_length, TAG)

            if XML_OUTPUT:
                bitmap_group_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, lightmap_group_element_node, "name", "bitmap group")
                lightmap_group.bitmap_group_tag_ref.append_xml_attributes(bitmap_group_tag_ref_node)

            lightmap_group.clusters = []
            clusters_count = lightmap_group.clusters_tag_block.count
            if clusters_count > 0:
                clusters_node = tag_format.get_xml_node(XML_OUTPUT, clusters_count, lightmap_group_element_node, "name", "clusters")
                lightmap_group.clusters_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for cluster_idx in range(clusters_count):
                    clusters_element_node = None
                    if XML_OUTPUT:
                        clusters_element_node = TAG.xml_doc.createElement('element')
                        clusters_element_node.setAttribute('index', str(cluster_idx))
                        clusters_node.appendChild(clusters_element_node)

                    cluster = LIGHTMAP.Cluster()
                    cluster.total_vertex_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(clusters_element_node, "total vertex count"))
                    cluster.total_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(clusters_element_node, "total triangle count"))
                    cluster.total_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(clusters_element_node, "total part count"))
                    cluster.shadow_casting_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(clusters_element_node, "shadow casting triangle count"))
                    cluster.shadow_casting_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(clusters_element_node, "shadow casting part count"))
                    cluster.opaque_point_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(clusters_element_node, "opaque point count"))
                    cluster.opaque_vertex_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(clusters_element_node, "opaque vertex count"))
                    cluster.opaque_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(clusters_element_node, "opaque part count"))
                    cluster.opaque_max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(clusters_element_node, "opaque max nodes vertex"))
                    cluster.transparent_max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(clusters_element_node, "transparent max nodes vertex"))
                    cluster.shadow_casting_rigid_triangle_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(clusters_element_node, "shadow casting rigid triangle count"))
                    cluster.unknown = input_stream.read(1)
                    cluster.geometry_classification = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(clusters_element_node, "geometry classification", GeometryClassificationEnum))
                    cluster.geometry_compression_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(clusters_element_node, "geometry compression flags", GeometryCompressionFlags))
                    cluster.compression_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(clusters_element_node, "compression info"))
                    cluster.hardware_node_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(clusters_element_node, "hardware node count"))
                    cluster.node_map_size = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(clusters_element_node, "node map size"))
                    cluster.software_plane_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(clusters_element_node, "software plane count"))
                    input_stream.read(1) # Padding?
                    cluster.total_subpart_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(clusters_element_node, "total subpart count"))
                    cluster.section_lighting_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(clusters_element_node, "section lighting flags", SectionLightingFlags))
                    cluster.block_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(clusters_element_node, "block offset"))
                    cluster.block_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(clusters_element_node, "block size"))
                    cluster.section_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(clusters_element_node, "section data size"))
                    cluster.resource_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(clusters_element_node, "resource data size"))
                    cluster.resource_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(clusters_element_node, "resources"))
                    input_stream.read(4) # Padding?
                    cluster.owner_tag_section_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(clusters_element_node, "owner tag section offset"))
                    input_stream.read(4) # Padding?
                    cluster.cache_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(clusters_element_node, "cache data"))

                    lightmap_group.clusters.append(cluster)

                for cluster_idx, cluster in enumerate(lightmap_group.clusters):
                    cluster_element_node = None
                    if XML_OUTPUT:
                        cluster_element_node = clusters_node.childNodes[cluster_idx]

                    cluster.compression_info = []
                    cluster.resources = []
                    cluster.cache_data = []
                    compression_info_count = cluster.compression_info_tag_block.count
                    resources_count = cluster.resource_tag_block.count
                    cache_data_count = cluster.cache_data_tag_block.count

                    cluster.sinf_header = TAG.TagBlockHeader().read(input_stream, TAG)

                    if compression_info_count > 0:
                        compression_info_node = tag_format.get_xml_node(XML_OUTPUT, compression_info_count, cluster_element_node, "name", "compression info")
                        cluster.compression_info_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for compression_info_idx in range(compression_info_count):
                            compression_info_element_node = None
                            if XML_OUTPUT:
                                compression_info_element_node = TAG.xml_doc.createElement('element')
                                compression_info_element_node.setAttribute('index', str(compression_info_idx))
                                compression_info_node.appendChild(compression_info_element_node)

                            compression_info = LIGHTMAP.CompressionInfo()
                            compression_info.position_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds x"))
                            compression_info.position_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds y"))
                            compression_info.position_bounds_z = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds z"))
                            compression_info.texcoord_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "texcoord bounds x"))
                            compression_info.texcoord_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "texcoord bounds y"))
                            compression_info.secondary_texcoord_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "secondary texcoord bounds x"))
                            compression_info.secondary_texcoord_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "secondary texcoord bounds y"))

                            cluster.compression_info.append(compression_info)

                    cluster.blok_header = TAG.TagBlockHeader().read(input_stream, TAG)

                    if resources_count > 0:
                        resources_node = tag_format.get_xml_node(XML_OUTPUT, resources_count, cluster_element_node, "name", "resources")
                        cluster.resources_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for resource_idx in range(resources_count):
                            resource_element_node = None
                            if XML_OUTPUT:
                                resource_element_node = TAG.xml_doc.createElement('element')
                                resource_element_node.setAttribute('index', str(resource_idx))
                                resources_node.appendChild(resource_element_node)

                            resource = LIGHTMAP.Resource()
                            resource.resource_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource type", ResourceTypeEnum))
                            input_stream.read(2) # Padding?
                            resource.primary_locator = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "primary locator"))
                            resource.secondary_locator = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "secondary locator"))
                            resource.resource_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource data size"))
                            resource.resource_data_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource data offset"))

                            cluster.resources.append(resource)

                    if cache_data_count > 0:
                        cache_data_node = tag_format.get_xml_node(XML_OUTPUT, cache_data_count, cluster_element_node, "name", "cache data")
                        cluster.cache_data_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for cache_data_idx in range(cache_data_count):
                            cache_data_element_node = None
                            if XML_OUTPUT:
                                cache_data_element_node = TAG.xml_doc.createElement('element')
                                cache_data_element_node.setAttribute('index', str(cache_data_idx))
                                cache_data_node.appendChild(cache_data_element_node)

                            cache_data = LIGHTMAP.CacheData()
                            cache_data.parts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "parts"))
                            cache_data.subparts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "subparts"))
                            cache_data.visibility_bounds_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "visibility bounds"))
                            cache_data.raw_vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "raw vertices"))
                            cache_data.strip_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "strip indices"))
                            cache_data.visibility_mopp_code_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "visibility mopp code"))
                            cache_data.mopp_reorder_table_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "mopp reorder table"))
                            cache_data.vertex_buffers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "vertex buffers"))
                            input_stream.read(4) # Padding?

                            cluster.cache_data.append(cache_data)

                        for cache_data_idx, cache_data in enumerate(cluster.cache_data):
                            cache_data_element_node = None
                            if XML_OUTPUT:
                                cache_data_element_node = cache_data_node.childNodes[cache_data_idx]

                            cache_data.parts = []
                            cache_data.subparts = []
                            cache_data.visibility_bounds = []
                            cache_data.raw_vertices = []
                            cache_data.strip_indices = []
                            cache_data.mopp_reorder_table = []
                            cache_data.vertex_buffers = []
                            parts_count = cache_data.parts_tag_block.count
                            subparts_count = cache_data.subparts_tag_block.count
                            visibility_bounds_count = cache_data.visibility_bounds_tag_block.count
                            raw_vertices_count = cache_data.raw_vertices_tag_block.count
                            strip_indices_count = cache_data.strip_indices_tag_block.count
                            mopp_reorder_table_count = cache_data.mopp_reorder_table_tag_block.count
                            vertex_buffers_count = cache_data.vertex_buffers_tag_block.count

                            cache_data.sect_header = TAG.TagBlockHeader().read(input_stream, TAG)

                            if parts_count > 0:
                                parts_node = tag_format.get_xml_node(XML_OUTPUT, parts_count, cache_data_element_node, "name", "parts")
                                cache_data.parts_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for parts_idx in range(parts_count):
                                    parts_element_node = None
                                    if XML_OUTPUT:
                                        parts_element_node = TAG.xml_doc.createElement('element')
                                        parts_element_node.setAttribute('index', str(parts_idx))
                                        parts_node.appendChild(parts_element_node)

                                    part = LIGHTMAP.Part()
                                    part.part_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(parts_element_node, "type", PartTypeEnum))
                                    part.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(parts_element_node, "flags", PartFlags))
                                    part.material_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(parts_element_node, "material", None, 1, "scenario_decal_palette_block"))
                                    part.strip_start_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(parts_element_node, "strip start index"))
                                    part.strip_length = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(parts_element_node, "strip length"))
                                    part.first_subpart_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(parts_element_node, "first subpart index"))
                                    part.subpart_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(parts_element_node, "subpart count"))
                                    part.max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(parts_element_node, "max nodes vertex"))
                                    part.contributing_compound_node_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(parts_element_node, "contributing compound node count"))
                                    part.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(parts_element_node, "position"))
                                    part.node_index_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(parts_element_node, "node index 0"))
                                    part.node_index_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(parts_element_node, "node index 1"))
                                    part.node_index_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(parts_element_node, "node index 2"))
                                    part.node_index_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(parts_element_node, "node index 3"))
                                    part.node_weight_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(parts_element_node, "node weight 0"))
                                    part.node_weight_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(parts_element_node, "node weight 1"))
                                    part.node_weight_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(parts_element_node, "node weight 2"))
                                    part.lod_mipmap_magic_number = TAG.read_float(input_stream, TAG, tag_format.XMLData(parts_element_node, "lod mipmap magic number"))
                                    part.unknown = input_stream.read(24)

                                    cache_data.parts.append(part)

                            if subparts_count > 0:
                                subparts_node = tag_format.get_xml_node(XML_OUTPUT, subparts_count, cache_data_element_node, "name", "subparts")
                                cache_data.subparts_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for subparts_idx in range(subparts_count):
                                    subparts_element_node = None
                                    if XML_OUTPUT:
                                        subparts_element_node = TAG.xml_doc.createElement('element')
                                        subparts_element_node.setAttribute('index', str(subparts_idx))
                                        subparts_node.appendChild(subparts_element_node)

                                    subpart = LIGHTMAP.SubPart()
                                    subpart.indices_start_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subparts_element_node, "indices start index"))
                                    subpart.indices_length = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subparts_element_node, "indices length"))
                                    subpart.visibility_bounds_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subparts_element_node, "visibility bounds index"))
                                    subpart.part_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subparts_element_node, "part index"))

                                    cache_data.subparts.append(subpart)

                            if visibility_bounds_count > 0:
                                visibility_bounds_node = tag_format.get_xml_node(XML_OUTPUT, visibility_bounds_count, cache_data_element_node, "name", "visibility bounds")
                                cache_data.visibility_bounds_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for visibility_bounds_idx in range(visibility_bounds_count):
                                    visibility_bounds_element_node = None
                                    if XML_OUTPUT:
                                        visibility_bounds_element_node = TAG.xml_doc.createElement('element')
                                        visibility_bounds_element_node.setAttribute('index', str(visibility_bounds_idx))
                                        visibility_bounds_node.appendChild(visibility_bounds_element_node)

                                    visibility_bounds = LIGHTMAP.VisibilityBounds()
                                    visibility_bounds.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(visibility_bounds_element_node, "position"))
                                    visibility_bounds.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(visibility_bounds_element_node, "radius"))
                                    visibility_bounds.node_0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(visibility_bounds_element_node, "node 0"))
                                    input_stream.read(2) # Padding?

                                    cache_data.visibility_bounds.append(visibility_bounds)

                            if raw_vertices_count > 0:
                                raw_vertices_node = tag_format.get_xml_node(XML_OUTPUT, raw_vertices_count, cache_data_element_node, "name", "raw vertices")
                                cache_data.raw_vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for raw_vertex_idx in range(raw_vertices_count):
                                    raw_vertex_element_node = None
                                    if XML_OUTPUT:
                                        raw_vertex_element_node = TAG.xml_doc.createElement('element')
                                        raw_vertex_element_node.setAttribute('index', str(raw_vertex_idx))
                                        raw_vertices_node.appendChild(raw_vertex_element_node)

                                    raw_vertex = LIGHTMAP.RawVertex()
                                    raw_vertex.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "position"))
                                    raw_vertex.node_index_0_old = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 0 old"))
                                    raw_vertex.node_index_1_old = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 1 old"))
                                    raw_vertex.node_index_2_old = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 2 old"))
                                    raw_vertex.node_index_3_old = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 3 old"))
                                    raw_vertex.node_weight_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node weight 0"))
                                    raw_vertex.node_weight_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node weight 1"))
                                    raw_vertex.node_weight_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node weight 2"))
                                    raw_vertex.node_weight_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node weight 3"))
                                    raw_vertex.node_index_0_new = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 0 new"))
                                    raw_vertex.node_index_1_new = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 1 new"))
                                    raw_vertex.node_index_2_new = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 2 new"))
                                    raw_vertex.node_index_3_new = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 3 new"))
                                    raw_vertex.uses_new_node_indices = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "uses new node indices"))
                                    raw_vertex.adjusted_compound_node_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "adjusted compound node index"))
                                    raw_vertex.texcoord = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "texcoord"))
                                    raw_vertex.normal = TAG.read_vector(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "normal"))
                                    raw_vertex.binormal = TAG.read_vector(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "binormal"))
                                    raw_vertex.tangent = TAG.read_vector(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "tangent"))
                                    raw_vertex.anisotropic_binormal = TAG.read_vector(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "anisotropic binormal"))
                                    raw_vertex.secondary_texcoord = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "secondary texcoord"))
                                    raw_vertex.primary_lightmap_color_RGBA = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "primary lightmap color"))
                                    raw_vertex.primary_lightmap_texcoord = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "primary lightmap texcoord"))
                                    raw_vertex.primary_lightmap_incident_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "primary lightmap incident direction"))
                                    input_stream.read(32) # Padding?

                                    cache_data.raw_vertices.append(raw_vertex)

                            if strip_indices_count > 0:
                                strip_indices_node = tag_format.get_xml_node(XML_OUTPUT, strip_indices_count, cache_data_element_node, "name", "strip indices")
                                cache_data.strip_indices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for strip_index_idx in range(strip_indices_count):
                                    strip_index_element_node = None
                                    if XML_OUTPUT:
                                        strip_index_element_node = TAG.xml_doc.createElement('element')
                                        strip_index_element_node.setAttribute('index', str(strip_index_idx))
                                        strip_indices_node.appendChild(strip_index_element_node)

                                    strip_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(strip_index_element_node, "index"))

                                    cache_data.strip_indices.append(strip_index)

                            cache_data.visibility_mopp_code_tag_data.data = input_stream.read(cache_data.visibility_mopp_code_tag_data.size)

                            if mopp_reorder_table_count > 0:
                                mopp_reorder_table_node = tag_format.get_xml_node(XML_OUTPUT, mopp_reorder_table_count, cache_data_element_node, "name", "mopp reorder table")
                                cache_data.mopp_reorder_table_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for mopp_reorder_table_idx in range(mopp_reorder_table_count):
                                    mopp_reorder_table_element_node = None
                                    if XML_OUTPUT:
                                        mopp_reorder_table_element_node = TAG.xml_doc.createElement('element')
                                        mopp_reorder_table_element_node.setAttribute('index', str(mopp_reorder_table_idx))
                                        mopp_reorder_table_node.appendChild(mopp_reorder_table_element_node)

                                    table_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(mopp_reorder_table_element_node, "index"))

                                    cache_data.mopp_reorder_table.append(table_index)

                            if vertex_buffers_count > 0:
                                vertex_buffers_node = tag_format.get_xml_node(XML_OUTPUT, vertex_buffers_count, cache_data_element_node, "name", "vertex buffers")
                                cache_data.vertex_buffers_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for vertex_buffer_idx in range(vertex_buffers_count):
                                    vertex_buffer_element_node = None
                                    if XML_OUTPUT:
                                        vertex_buffer_element_node = TAG.xml_doc.createElement('element')
                                        vertex_buffer_element_node.setAttribute('index', str(vertex_buffer_idx))
                                        vertex_buffers_node.appendChild(vertex_buffer_element_node)

                                    cache_data.vertex_buffers.append(input_stream.read(32))

            lightmap_group.cluster_render_info = []
            cluster_render_info_count = lightmap_group.cluster_render_info_tag_block.count
            if cluster_render_info_count > 0:
                cluster_render_info_node = tag_format.get_xml_node(XML_OUTPUT, cluster_render_info_count, lightmap_group_element_node, "name", "cluster render info")
                lightmap_group.cluster_render_info_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for cluster_render_info_idx in range(cluster_render_info_count):
                    cluster_render_info_element_node = None
                    if XML_OUTPUT:
                        cluster_render_info_element_node = TAG.xml_doc.createElement('element')
                        cluster_render_info_element_node.setAttribute('index', str(cluster_render_info_idx))
                        cluster_render_info_node.appendChild(cluster_render_info_element_node)

                    cluster_render_info = LIGHTMAP.RenderInfo()
                    cluster_render_info.bitmap_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_render_info_element_node, "bitmap index"))
                    cluster_render_info.palette_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_render_info_element_node, "palette index"))

                    lightmap_group.cluster_render_info.append(cluster_render_info)

            lightmap_group.poop_definitions = []
            poop_definitions_count = lightmap_group.poop_definitions_tag_block.count
            if poop_definitions_count > 0:
                poop_definitions_node = tag_format.get_xml_node(XML_OUTPUT, poop_definitions_count, lightmap_group_element_node, "name", "poop definitions")
                lightmap_group.poop_definitions_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for poop_definition_idx in range(poop_definitions_count):
                    poop_definition_node = None
                    if XML_OUTPUT:
                        poop_definition_node = TAG.xml_doc.createElement('element')
                        poop_definition_node.setAttribute('index', str(poop_definition_idx))
                        poop_definitions_node.appendChild(poop_definition_node)

                    poop_definition = LIGHTMAP.Cluster()
                    poop_definition.total_vertex_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(poop_definition_node, "total vertex count"))
                    poop_definition.total_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(poop_definition_node, "total triangle count"))
                    poop_definition.total_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(poop_definition_node, "total part count"))
                    poop_definition.shadow_casting_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(poop_definition_node, "shadow casting triangle count"))
                    poop_definition.shadow_casting_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(poop_definition_node, "shadow casting part count"))
                    poop_definition.opaque_point_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(poop_definition_node, "opaque point count"))
                    poop_definition.opaque_vertex_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(poop_definition_node, "opaque vertex count"))
                    poop_definition.opaque_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(poop_definition_node, "opaque part count"))
                    poop_definition.opaque_max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(poop_definition_node, "opaque max nodes vertex"))
                    poop_definition.transparent_max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(poop_definition_node, "transparent max nodes vertex"))
                    poop_definition.shadow_casting_rigid_triangle_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(poop_definition_node, "shadow casting rigid triangle count"))
                    input_stream.read(1) # Padding?
                    poop_definition.geometry_classification = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(poop_definition_node, "geometry classification", GeometryClassificationEnum))
                    poop_definition.geometry_compression_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(poop_definition_node, "geometry compression flags", GeometryCompressionFlags))
                    poop_definition.compression_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(poop_definition_node, "compression info"))
                    poop_definition.hardware_node_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(poop_definition_node, "hardware node count"))
                    poop_definition.node_map_size = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(poop_definition_node, "node map size"))
                    poop_definition.software_plane_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(poop_definition_node, "software plane count"))
                    input_stream.read(1) # Padding?
                    poop_definition.total_subpart_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(poop_definition_node, "total subpart count"))
                    poop_definition.section_lighting_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(poop_definition_node, "section lighting flags", SectionLightingFlags))
                    poop_definition.block_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(poop_definition_node, "block offset"))
                    poop_definition.block_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(poop_definition_node, "block size"))
                    poop_definition.section_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(poop_definition_node, "section data size"))
                    poop_definition.resource_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(poop_definition_node, "resource data size"))
                    poop_definition.resource_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(poop_definition_node, "resources"))
                    input_stream.read(4) # Padding?
                    poop_definition.owner_tag_section_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(poop_definition_node, "owner tag section offset"))
                    input_stream.read(4) # Padding?
                    poop_definition.cache_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(poop_definition_node, "cache data"))

                    lightmap_group.poop_definitions.append(poop_definition)

                for poop_definition_idx, poop_definition in enumerate(lightmap_group.poop_definitions):
                    poop_definition_element_node = None
                    if XML_OUTPUT:
                        poop_definition_element_node = poop_definitions_node.childNodes[poop_definition_idx]

                    poop_definition.compression_info = []
                    poop_definition.resources = []
                    poop_definition.cache_data = []
                    compression_info_count = poop_definition.compression_info_tag_block.count
                    resources_count = poop_definition.resource_tag_block.count
                    cache_data_count = poop_definition.cache_data_tag_block.count

                    poop_definition.sinf_header = TAG.TagBlockHeader().read(input_stream, TAG)

                    if compression_info_count > 0:
                        compression_info_node = tag_format.get_xml_node(XML_OUTPUT, compression_info_count, poop_definition_element_node, "name", "compression info")
                        poop_definition.compression_info_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for compression_info_idx in range(compression_info_count):
                            compression_info_element_node = None
                            if XML_OUTPUT:
                                compression_info_element_node = TAG.xml_doc.createElement('element')
                                compression_info_element_node.setAttribute('index', str(compression_info_idx))
                                compression_info_node.appendChild(compression_info_element_node)

                            compression_info = LIGHTMAP.CompressionInfo()
                            compression_info.position_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds x"))
                            compression_info.position_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds y"))
                            compression_info.position_bounds_z = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds z"))
                            compression_info.texcoord_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "texcoord bounds x"))
                            compression_info.texcoord_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "texcoord bounds y"))
                            compression_info.secondary_texcoord_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "secondary texcoord bounds x"))
                            compression_info.secondary_texcoord_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "secondary texcoord bounds y"))

                            poop_definition.compression_info.append(compression_info)

                    poop_definition.blok_header = TAG.TagBlockHeader().read(input_stream, TAG)

                    if resources_count > 0:
                        resources_node = tag_format.get_xml_node(XML_OUTPUT, resources_count, poop_definition_element_node, "name", "resources")
                        poop_definition.resources_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for resource_idx in range(resources_count):
                            resource_element_node = None
                            if XML_OUTPUT:
                                resource_element_node = TAG.xml_doc.createElement('element')
                                resource_element_node.setAttribute('index', str(resource_idx))
                                resources_node.appendChild(resource_element_node)

                            resource = LIGHTMAP.Resource()
                            resource.resource_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource type", ResourceTypeEnum))
                            input_stream.read(2) # Padding?
                            resource.primary_locator = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "primary locator"))
                            resource.secondary_locator = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "secondary locator"))
                            resource.resource_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource data size"))
                            resource.resource_data_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource data offset"))

                            poop_definition.resources.append(resource)

                    if cache_data_count > 0:
                        cache_data_node = tag_format.get_xml_node(XML_OUTPUT, cache_data_count, poop_definition_element_node, "name", "cache data")
                        poop_definition.cache_data_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for cache_data_idx in range(cache_data_count):
                            cache_data_element_node = None
                            if XML_OUTPUT:
                                cache_data_element_node = TAG.xml_doc.createElement('element')
                                cache_data_element_node.setAttribute('index', str(cache_data_idx))
                                cache_data_node.appendChild(cache_data_element_node)

                            cache_data = LIGHTMAP.CacheData()
                            cache_data.parts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "parts"))
                            cache_data.subparts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "subparts"))
                            cache_data.visibility_bounds_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "visibility bounds"))
                            cache_data.raw_vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "raw vertices"))
                            cache_data.strip_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "strip indices"))
                            cache_data.visibility_mopp_code_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "visibility mopp code"))
                            cache_data.mopp_reorder_table_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "mopp reorder table"))
                            cache_data.vertex_buffers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "vertex buffers"))
                            input_stream.read(4) # Padding?

                            poop_definition.cache_data.append(cache_data)

                        for cache_data_idx, cache_data in enumerate(poop_definition.cache_data):
                            cache_data_element_node = None
                            if XML_OUTPUT:
                                cache_data_element_node = cache_data_node.childNodes[cache_data_idx]

                            cache_data.parts = []
                            cache_data.subparts = []
                            cache_data.visibility_bounds = []
                            cache_data.raw_vertices = []
                            cache_data.strip_indices = []
                            cache_data.mopp_reorder_table = []
                            cache_data.vertex_buffers = []
                            parts_count = cache_data.parts_tag_block.count
                            subparts_count = cache_data.subparts_tag_block.count
                            visibility_bounds_count = cache_data.visibility_bounds_tag_block.count
                            raw_vertices_count = cache_data.raw_vertices_tag_block.count
                            strip_indices_count = cache_data.strip_indices_tag_block.count
                            mopp_reorder_table_count = cache_data.mopp_reorder_table_tag_block.count
                            vertex_buffers_count = cache_data.vertex_buffers_tag_block.count

                            cache_data.sect_header = TAG.TagBlockHeader().read(input_stream, TAG)

                            if parts_count > 0:
                                parts_node = tag_format.get_xml_node(XML_OUTPUT, parts_count, cache_data_element_node, "name", "parts")
                                cache_data.parts_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for parts_idx in range(parts_count):
                                    parts_element_node = None
                                    if XML_OUTPUT:
                                        parts_element_node = TAG.xml_doc.createElement('element')
                                        parts_element_node.setAttribute('index', str(parts_idx))
                                        parts_node.appendChild(parts_element_node)

                                    part = LIGHTMAP.Part()
                                    part.part_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(parts_element_node, "type", PartTypeEnum))
                                    part.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(parts_element_node, "flags", PartFlags))
                                    part.material_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(parts_element_node, "material", None, 1, "scenario_decal_palette_block"))
                                    part.strip_start_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(parts_element_node, "strip start index"))
                                    part.strip_length = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(parts_element_node, "strip length"))
                                    part.first_subpart_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(parts_element_node, "first subpart index"))
                                    part.subpart_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(parts_element_node, "subpart count"))
                                    part.max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(parts_element_node, "max nodes vertex"))
                                    part.contributing_compound_node_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(parts_element_node, "contributing compound node count"))
                                    part.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(parts_element_node, "position"))
                                    part.node_index_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(parts_element_node, "node index 0"))
                                    part.node_index_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(parts_element_node, "node index 1"))
                                    part.node_index_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(parts_element_node, "node index 2"))
                                    part.node_index_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(parts_element_node, "node index 3"))
                                    part.node_weight_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(parts_element_node, "node weight 0"))
                                    part.node_weight_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(parts_element_node, "node weight 1"))
                                    part.node_weight_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(parts_element_node, "node weight 2"))
                                    part.lod_mipmap_magic_number = TAG.read_float(input_stream, TAG, tag_format.XMLData(parts_element_node, "lod mipmap magic number"))
                                    input_stream.read(24) # Padding?

                                    cache_data.parts.append(part)

                            if subparts_count > 0:
                                subparts_node = tag_format.get_xml_node(XML_OUTPUT, subparts_count, cache_data_element_node, "name", "subparts")
                                cache_data.subparts_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for subparts_idx in range(subparts_count):
                                    subparts_element_node = None
                                    if XML_OUTPUT:
                                        subparts_element_node = TAG.xml_doc.createElement('element')
                                        subparts_element_node.setAttribute('index', str(subparts_idx))
                                        subparts_node.appendChild(subparts_element_node)

                                    subpart = LIGHTMAP.SubPart()
                                    subpart.indices_start_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subparts_element_node, "indices start index"))
                                    subpart.indices_length = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subparts_element_node, "indices length"))
                                    subpart.visibility_bounds_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subparts_element_node, "visibility bounds index"))
                                    subpart.part_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subparts_element_node, "part index"))

                                    cache_data.subparts.append(subpart)

                            if visibility_bounds_count > 0:
                                visibility_bounds_node = tag_format.get_xml_node(XML_OUTPUT, visibility_bounds_count, cache_data_element_node, "name", "visibility bounds")
                                cache_data.visibility_bounds_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for visibility_bounds_idx in range(visibility_bounds_count):
                                    visibility_bounds_element_node = None
                                    if XML_OUTPUT:
                                        visibility_bounds_element_node = TAG.xml_doc.createElement('element')
                                        visibility_bounds_element_node.setAttribute('index', str(visibility_bounds_idx))
                                        visibility_bounds_node.appendChild(visibility_bounds_element_node)

                                    visibility_bounds = LIGHTMAP.VisibilityBounds()
                                    visibility_bounds.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(visibility_bounds_element_node, "position"))
                                    visibility_bounds.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(visibility_bounds_element_node, "radius"))
                                    visibility_bounds.node_0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(visibility_bounds_element_node, "node 0"))
                                    input_stream.read(2) # Padding?

                                    cache_data.subparts.append(subpart)

                            if raw_vertices_count > 0:
                                raw_vertices_node = tag_format.get_xml_node(XML_OUTPUT, raw_vertices_count, cache_data_element_node, "name", "raw vertices")
                                cache_data.raw_vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for raw_vertex_idx in range(raw_vertices_count):
                                    raw_vertex_element_node = None
                                    if XML_OUTPUT:
                                        raw_vertex_element_node = TAG.xml_doc.createElement('element')
                                        raw_vertex_element_node.setAttribute('index', str(raw_vertex_idx))
                                        raw_vertices_node.appendChild(raw_vertex_element_node)

                                    raw_vertex = LIGHTMAP.RawVertex()
                                    raw_vertex.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "position"))
                                    raw_vertex.node_index_0_old = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 0 old"))
                                    raw_vertex.node_index_1_old = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 1 old"))
                                    raw_vertex.node_index_2_old = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 2 old"))
                                    raw_vertex.node_index_3_old = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 3 old"))
                                    raw_vertex.node_weight_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node weight 0"))
                                    raw_vertex.node_weight_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node weight 1"))
                                    raw_vertex.node_weight_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node weight 2"))
                                    raw_vertex.node_weight_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node weight 3"))
                                    raw_vertex.node_index_0_new = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 0 new"))
                                    raw_vertex.node_index_1_new = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 1 new"))
                                    raw_vertex.node_index_2_new = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 2 new"))
                                    raw_vertex.node_index_3_new = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "node index 3 new"))
                                    raw_vertex.uses_new_node_indices = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "uses new node indices"))
                                    raw_vertex.adjusted_compound_node_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "adjusted compound node index"))
                                    raw_vertex.texcoord = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "texcoord"))
                                    raw_vertex.normal = TAG.read_vector(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "normal"))
                                    raw_vertex.binormal = TAG.read_vector(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "binormal"))
                                    raw_vertex.tangent = TAG.read_vector(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "tangent"))
                                    raw_vertex.anisotropic_binormal = TAG.read_vector(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "anisotropic binormal"))
                                    raw_vertex.secondary_texcoord = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "secondary texcoord"))
                                    raw_vertex.primary_lightmap_color_RGBA = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "primary lightmap color"))
                                    raw_vertex.primary_lightmap_texcoord = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "primary lightmap texcoord"))
                                    raw_vertex.primary_lightmap_incident_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "primary lightmap incident direction"))
                                    input_stream.read(32) # Padding?

                                    cache_data.raw_vertices.append(raw_vertex)

                            if strip_indices_count > 0:
                                strip_indices_node = tag_format.get_xml_node(XML_OUTPUT, strip_indices_count, cache_data_element_node, "name", "strip indices")
                                cache_data.strip_indices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for strip_index_idx in range(strip_indices_count):
                                    strip_index_element_node = None
                                    if XML_OUTPUT:
                                        strip_index_element_node = TAG.xml_doc.createElement('element')
                                        strip_index_element_node.setAttribute('index', str(strip_index_idx))
                                        strip_indices_node.appendChild(strip_index_element_node)

                                    strip_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(strip_index_element_node, "index"))

                                    cache_data.strip_indices.append(strip_index)

                            cache_data.visibility_mopp_code_tag_data.data = input_stream.read(cache_data.visibility_mopp_code_tag_data.size)

                            if mopp_reorder_table_count > 0:
                                mopp_reorder_table_node = tag_format.get_xml_node(XML_OUTPUT, mopp_reorder_table_count, cache_data_element_node, "name", "mopp reorder table")
                                cache_data.mopp_reorder_table_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for mopp_reorder_table_idx in range(mopp_reorder_table_count):
                                    mopp_reorder_table_element_node = None
                                    if XML_OUTPUT:
                                        mopp_reorder_table_element_node = TAG.xml_doc.createElement('element')
                                        mopp_reorder_table_element_node.setAttribute('index', str(mopp_reorder_table_idx))
                                        mopp_reorder_table_node.appendChild(mopp_reorder_table_element_node)

                                    table_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(mopp_reorder_table_element_node, "index"))

                                    cache_data.mopp_reorder_table.append(table_index)

                            if vertex_buffers_count > 0:
                                vertex_buffers_node = tag_format.get_xml_node(XML_OUTPUT, vertex_buffers_count, cache_data_element_node, "name", "vertex buffers")
                                cache_data.vertex_buffers_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for vertex_buffer_idx in range(vertex_buffers_count):
                                    vertex_buffer_element_node = None
                                    if XML_OUTPUT:
                                        vertex_buffer_element_node = TAG.xml_doc.createElement('element')
                                        vertex_buffer_element_node.setAttribute('index', str(vertex_buffer_idx))
                                        vertex_buffers_node.appendChild(vertex_buffer_element_node)

                                    cache_data.vertex_buffers.append(input_stream.read(32)) # Padding?

            lightmap_group.lighting_environments = []
            lighting_environments_count = lightmap_group.lighting_environments_tag_block.count
            if lighting_environments_count > 0:
                lighting_environment_node = tag_format.get_xml_node(XML_OUTPUT, lighting_environments_count, lightmap_group_element_node, "name", "lighting environments")
                lightmap_group.lighting_environments_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for lighting_environment_idx in range(lighting_environments_count):
                    lighting_environment_element_node = None
                    if XML_OUTPUT:
                        lighting_environment_element_node = TAG.xml_doc.createElement('element')
                        lighting_environment_element_node.setAttribute('index', str(lighting_environment_idx))
                        lighting_environment_node.appendChild(lighting_environment_element_node)

                    lighting_environment = LIGHTMAP.LightingEnvironment()
                    lighting_environment.sample_point = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "sample point"))
                    lighting_environment.red_coefficient_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "red coefficient 0"))
                    lighting_environment.red_coefficient_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "red coefficient 1"))
                    lighting_environment.red_coefficient_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "red coefficient 2"))
                    lighting_environment.red_coefficient_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "red coefficient 3"))
                    lighting_environment.red_coefficient_4 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "red coefficient 4"))
                    lighting_environment.red_coefficient_5 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "red coefficient 5"))
                    lighting_environment.red_coefficient_6 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "red coefficient 6"))
                    lighting_environment.red_coefficient_7 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "red coefficient 7"))
                    lighting_environment.red_coefficient_8 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "red coefficient 8"))
                    lighting_environment.green_coefficient_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "green coefficient 0"))
                    lighting_environment.green_coefficient_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "green coefficient 0"))
                    lighting_environment.green_coefficient_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "green coefficient 0"))
                    lighting_environment.green_coefficient_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "green coefficient 0"))
                    lighting_environment.green_coefficient_4 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "green coefficient 0"))
                    lighting_environment.green_coefficient_5 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "green coefficient 0"))
                    lighting_environment.green_coefficient_6 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "green coefficient 0"))
                    lighting_environment.green_coefficient_7 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "green coefficient 0"))
                    lighting_environment.green_coefficient_8 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "green coefficient 0"))
                    lighting_environment.blue_coefficient_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "blue coefficient 0"))
                    lighting_environment.blue_coefficient_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "blue coefficient 1"))
                    lighting_environment.blue_coefficient_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "blue coefficient 2"))
                    lighting_environment.blue_coefficient_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "blue coefficient 3"))
                    lighting_environment.blue_coefficient_4 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "blue coefficient 4"))
                    lighting_environment.blue_coefficient_5 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "blue coefficient 5"))
                    lighting_environment.blue_coefficient_6 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "blue coefficient 6"))
                    lighting_environment.blue_coefficient_7 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "blue coefficient 7"))
                    lighting_environment.blue_coefficient_8 = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "blue coefficient 8"))
                    lighting_environment.mean_incoming_light_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "mean incoming light direction"))
                    lighting_environment.incoming_light_intensity = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "incoming light intensity"))
                    lighting_environment.specular_bitmap_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "specular bitmap index"))
                    lighting_environment.rotation_axis = TAG.read_vector(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "rotation axis"))
                    lighting_environment.rotation_speed = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "rotation speed"))
                    lighting_environment.bump_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "bump direction"))
                    lighting_environment.color_tint_RGBA = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "primary lightmap color"))
                    lighting_environment.procedural_override = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "procedural override", ProceduralOverrideEnum))
                    lighting_environment.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "flags", LightingEnvironmentFlags))
                    lighting_environment.procedural_param0 = TAG.read_vector(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "procedural param0"))
                    lighting_environment.procedural_param1_xyz = TAG.read_vector(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "procedural param1.xyz"))
                    lighting_environment.procedural_param1_w = TAG.read_float(input_stream, TAG, tag_format.XMLData(lighting_environment_element_node, "procedural param1.w"))

                    lightmap_group.lighting_environments.append(lighting_environment)

            lightmap_group.geometry_buckets = []
            geometry_buckets_count = lightmap_group.geometry_buckets_tag_block.count
            if geometry_buckets_count > 0:
                geometry_bucket_node = tag_format.get_xml_node(XML_OUTPUT, geometry_buckets_count, lightmap_group_element_node, "name", "geometry buckets")
                lightmap_group.geometry_buckets_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for geometry_bucket_idx in range(geometry_buckets_count):
                    geometry_bucket_element_node = None
                    if XML_OUTPUT:
                        geometry_bucket_element_node = TAG.xml_doc.createElement('element')
                        geometry_bucket_element_node.setAttribute('index', str(geometry_bucket_idx))
                        geometry_bucket_node.appendChild(geometry_bucket_element_node)

                    geometry_bucket = LIGHTMAP.GeometryBucket()
                    geometry_bucket.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(geometry_bucket_element_node, "flags", GeometryBucketFlags))
                    input_stream.read(2) # Padding?
                    geometry_bucket.raw_vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(geometry_bucket_element_node, "raw vertices"))
                    geometry_bucket.block_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(geometry_bucket_element_node, "block offset"))
                    geometry_bucket.block_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(geometry_bucket_element_node, "block size"))
                    geometry_bucket.section_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(geometry_bucket_element_node, "section data size"))
                    geometry_bucket.resource_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(geometry_bucket_element_node, "resource data size"))
                    geometry_bucket.resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(geometry_bucket_element_node, "resources"))
                    input_stream.read(4) # Padding?
                    geometry_bucket.owner_tag_section_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(geometry_bucket_element_node, "owner tag section offset"))
                    input_stream.read(4) # Padding?
                    geometry_bucket.cache_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(geometry_bucket_element_node, "cache data"))

                    lightmap_group.geometry_buckets.append(geometry_bucket)

                for geometry_bucket_idx, geometry_bucket in enumerate(lightmap_group.geometry_buckets):
                    geometry_bucket_element_node = None
                    if XML_OUTPUT:
                        geometry_bucket_element_node = geometry_bucket_node.childNodes[geometry_bucket_idx]

                    geometry_bucket.raw_vertices = []
                    geometry_bucket.resources = []
                    geometry_bucket.cache_data = []
                    raw_vertices_count = geometry_bucket.raw_vertices_tag_block.count
                    resources_count = geometry_bucket.resources_tag_block.count
                    cache_data_count = geometry_bucket.cache_data_tag_block.count

                    if raw_vertices_count > 0:
                        raw_vertices_node = tag_format.get_xml_node(XML_OUTPUT, raw_vertices_count, geometry_bucket_element_node, "name", "raw vertices")
                        geometry_bucket.raw_vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for raw_vertex_idx in range(raw_vertices_count):
                            raw_vertex_element_node = None
                            if XML_OUTPUT:
                                raw_vertex_element_node = TAG.xml_doc.createElement('element')
                                raw_vertex_element_node.setAttribute('index', str(raw_vertex_idx))
                                raw_vertices_node.appendChild(raw_vertex_element_node)

                            raw_vertex = LIGHTMAP.RawVertex()
                            raw_vertex.primary_lightmap_color_RGBA = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "primary lightmap color"))
                            raw_vertex.primary_lightmap_incident_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "primary lightmap incident direction"))

                            geometry_bucket.raw_vertices.append(raw_vertex)

                    geometry_bucket.blok_header = TAG.TagBlockHeader().read(input_stream, TAG)
                    if resources_count > 0:
                        resources_node = tag_format.get_xml_node(XML_OUTPUT, resources_count, geometry_bucket_element_node, "name", "resources")
                        geometry_bucket.resources_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for resource_idx in range(resources_count):
                            resource_element_node = None
                            if XML_OUTPUT:
                                resource_element_node = TAG.xml_doc.createElement('element')
                                resource_element_node.setAttribute('index', str(resource_idx))
                                resources_node.appendChild(resource_element_node)

                            resource = LIGHTMAP.Resource()
                            resource.resource_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource type", ResourceTypeEnum))
                            input_stream.read(2) # Padding?
                            resource.primary_locator = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "primary locator"))
                            resource.secondary_locator = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "secondary locator"))
                            resource.resource_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource data size"))
                            resource.resource_data_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource data offset"))

                            geometry_bucket.resources.append(resource)

                    if cache_data_count > 0:
                        cache_data_node = tag_format.get_xml_node(XML_OUTPUT, cache_data_count, geometry_bucket_element_node, "name", "cache data")
                        geometry_bucket.cache_data_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for cache_data_idx in range(cache_data_count):
                            cache_data_element_node = None
                            if XML_OUTPUT:
                                cache_data_element_node = TAG.xml_doc.createElement('element')
                                cache_data_element_node.setAttribute('index', str(cache_data_idx))
                                cache_data_node.appendChild(cache_data_element_node)

                            cache_data = LIGHTMAP.CacheData()
                            cache_data.vertex_buffers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cache_data_element_node, "vertex buffers"))

                            geometry_bucket.cache_data.append(cache_data)

                        for cache_data_idx, cache_data in enumerate(geometry_bucket.cache_data):
                            cache_data_element_node = None
                            if XML_OUTPUT:
                                cache_data_element_node = cache_data_node.childNodes[cache_data_idx]

                            cache_data.vertex_buffers = []
                            vertex_buffers_count = cache_data.vertex_buffers_tag_block.count

                            if vertex_buffers_count > 0:
                                vertex_buffers_node = tag_format.get_xml_node(XML_OUTPUT, vertex_buffers_count, cache_data_element_node, "name", "vertex buffers")
                                cache_data.vertex_buffers_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                for vertex_buffer_idx in range(vertex_buffers_count):
                                    vertex_buffer_element_node = None
                                    if XML_OUTPUT:
                                        vertex_buffer_element_node = TAG.xml_doc.createElement('element')
                                        vertex_buffer_element_node.setAttribute('index', str(vertex_buffer_idx))
                                        vertex_buffers_node.appendChild(vertex_buffer_element_node)

                                    cache_data.vertex_buffers.append(input_stream.read(32)) # Padding?

            lightmap_group.instance_render_info = []
            instance_render_info_count = lightmap_group.instance_render_info_tag_block.count
            if instance_render_info_count > 0:
                instance_render_info_node = tag_format.get_xml_node(XML_OUTPUT, instance_render_info_count, lightmap_group_element_node, "name", "instance render info")
                lightmap_group.instance_render_info_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for instance_render_info_idx in range(instance_render_info_count):
                    instance_render_info_element_node = None
                    if XML_OUTPUT:
                        instance_render_info_element_node = TAG.xml_doc.createElement('element')
                        instance_render_info_element_node.setAttribute('index', str(instance_render_info_idx))
                        instance_render_info_node.appendChild(instance_render_info_element_node)

                    instance_render_info = LIGHTMAP.RenderInfo()
                    instance_render_info.bitmap_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instance_render_info_element_node, "bitmap index"))
                    instance_render_info.palette_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instance_render_info_element_node, "palette index"))

                    lightmap_group.instance_render_info.append(instance_render_info)

            lightmap_group.instance_bucket_refs = []
            instance_bucket_refs_count = lightmap_group.instance_bucket_refs_tag_block.count
            if instance_bucket_refs_count > 0:
                instance_bucket_ref_node = tag_format.get_xml_node(XML_OUTPUT, instance_bucket_refs_count, lightmap_group_element_node, "name", "instance bucket refs")
                lightmap_group.instance_bucket_refs_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for instance_bucket_ref_idx in range(instance_bucket_refs_count):
                    instance_bucket_ref_element_node = None
                    if XML_OUTPUT:
                        instance_bucket_ref_element_node = TAG.xml_doc.createElement('element')
                        instance_bucket_ref_element_node.setAttribute('index', str(instance_bucket_ref_idx))
                        instance_bucket_ref_node.appendChild(instance_bucket_ref_element_node)

                    bucket_ref = LIGHTMAP.BucketRef()
                    bucket_ref.flags = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instance_bucket_ref_element_node, "flags"))
                    bucket_ref.bucket_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instance_bucket_ref_element_node, "bucket index"))
                    bucket_ref.section_offsets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instance_bucket_ref_element_node, "section offsets"))

                    lightmap_group.instance_bucket_refs.append(bucket_ref)

                for instance_bucket_ref_idx, instance_bucket_ref in enumerate(lightmap_group.instance_bucket_refs):
                    instance_bucket_ref_element_node = None
                    if XML_OUTPUT:
                        instance_bucket_ref_element_node = instance_bucket_ref_node.childNodes[instance_bucket_ref_idx]

                    instance_bucket_ref.section_offsets = []
                    section_offsets_count = instance_bucket_ref.section_offsets_tag_block.count

                    if section_offsets_count > 0:
                        section_offsets_node = tag_format.get_xml_node(XML_OUTPUT, section_offsets_count, instance_bucket_ref_element_node, "name", "section offsets")
                        instance_bucket_ref.section_offsets_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for section_offset_idx in range(section_offsets_count):
                            section_offset_element_node = None
                            if XML_OUTPUT:
                                section_offset_element_node = TAG.xml_doc.createElement('element')
                                section_offset_element_node.setAttribute('index', str(section_offset_idx))
                                section_offsets_node.appendChild(section_offset_element_node)

                            section_offset = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_offset_element_node, "section offset"))

                            instance_bucket_ref.section_offsets.append(section_offset)

            lightmap_group.scenery_object_info = []
            scenery_object_info_count = lightmap_group.scenery_object_info_tag_block.count
            if scenery_object_info_count > 0:
                scenery_object_info_node = tag_format.get_xml_node(XML_OUTPUT, scenery_object_info_count, lightmap_group_element_node, "name", "scenery object info")
                lightmap_group.scenery_object_info_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for scenery_object_info_idx in range(scenery_object_info_count):
                    scenery_object_info_element_node = None
                    if XML_OUTPUT:
                        scenery_object_info_element_node = TAG.xml_doc.createElement('element')
                        scenery_object_info_element_node.setAttribute('index', str(scenery_object_info_idx))
                        scenery_object_info_node.appendChild(scenery_object_info_element_node)

                    scenery_object_info = LIGHTMAP.SceneryObjectInfo()
                    scenery_object_info.unique_id = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(scenery_object_info_element_node, "unique id"))
                    scenery_object_info.origin_bsp_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(scenery_object_info_element_node, "origin bsp index"))
                    scenery_object_info.object_type = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(scenery_object_info_element_node, "type"))
                    scenery_object_info.source = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(scenery_object_info_element_node, "source"))
                    scenery_object_info.render_model_checksum = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(scenery_object_info_element_node, "render model checksum"))

                    lightmap_group.scenery_object_info.append(scenery_object_info)

            lightmap_group.scenery_object_bucket_refs = []
            scenery_object_bucket_refs_count = lightmap_group.scenery_object_bucket_refs_tag_block.count
            if scenery_object_bucket_refs_count > 0:
                scenery_object_bucket_ref_node = tag_format.get_xml_node(XML_OUTPUT, scenery_object_bucket_refs_count, lightmap_group_element_node, "name", "scenery object bucket refs")
                lightmap_group.scenery_object_bucket_refs_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for scenery_object_bucket_ref_idx in range(scenery_object_bucket_refs_count):
                    scenery_object_bucket_ref_element_node = None
                    if XML_OUTPUT:
                        scenery_object_bucket_ref_element_node = TAG.xml_doc.createElement('element')
                        scenery_object_bucket_ref_element_node.setAttribute('index', str(scenery_object_bucket_ref_idx))
                        scenery_object_bucket_ref_node.appendChild(scenery_object_bucket_ref_element_node)

                    bucket_ref = LIGHTMAP.BucketRef()
                    bucket_ref.flags = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(scenery_object_bucket_ref_element_node, "flags"))
                    bucket_ref.bucket_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(scenery_object_bucket_ref_element_node, "bucket index"))
                    bucket_ref.section_offsets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(scenery_object_bucket_ref_element_node, "section offsets"))

                    lightmap_group.scenery_object_bucket_refs.append(bucket_ref)

                for scenery_object_bucket_ref_idx, scenery_object_bucket_ref in enumerate(lightmap_group.scenery_object_bucket_refs):
                    scenery_object_bucket_ref_element_node = None
                    if XML_OUTPUT:
                        scenery_object_bucket_ref_element_node = scenery_object_bucket_ref_node.childNodes[scenery_object_bucket_ref_idx]

                    scenery_object_bucket_ref.section_offsets = []
                    section_offsets_count = scenery_object_bucket_ref.section_offsets_tag_block.count

                    if section_offsets_count > 0:
                        section_offsets_node = tag_format.get_xml_node(XML_OUTPUT, section_offsets_count, scenery_object_bucket_ref_element_node, "name", "section offsets")
                        scenery_object_bucket_ref.section_offsets_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for section_offset_idx in range(section_offsets_count):
                            section_offset_element_node = None
                            if XML_OUTPUT:
                                section_offset_element_node = TAG.xml_doc.createElement('element')
                                section_offset_element_node.setAttribute('index', str(section_offset_idx))
                                section_offsets_node.appendChild(section_offset_element_node)

                            section_offset = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_offset_element_node, "section offset"))

                            scenery_object_bucket_ref.section_offsets.append(section_offset)

def read_errors(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.errors_tag_block.count > 0:
        errors_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.errors_tag_block.count, tag_node, "name", "errors")
        LEVEL.errors_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for error_idx in range(LEVEL.level_body.errors_tag_block.count):
            error_element_node = None
            if XML_OUTPUT:
                error_element_node = TAG.xml_doc.createElement('element')
                error_element_node.setAttribute('index', str(error_idx))
                errors_node.appendChild(error_element_node)

            error = LEVEL.Error()
            error.name = TAG.read_string256(input_stream, TAG, tag_format.XMLData(error_element_node, "name"))
            error.report_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(error_element_node, "report type", ReportTypeEnum))
            error.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(error_element_node, "flags", ReportFlags))
            input_stream.read(408) # Padding?
            error.reports_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(error_element_node, "reports"))

            LEVEL.errors.append(error)

        for error_idx, error in enumerate(LEVEL.errors):
            error_element_node = None
            if XML_OUTPUT:
                error_element_node = errors_node.childNodes[error_idx]

            error.reports = []
            if error.reports_tag_block.count > 0:
                report_node = tag_format.get_xml_node(XML_OUTPUT, error.reports_tag_block.count, error_element_node, "name", "reports")
                error.reports_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for report_idx in range(error.reports_tag_block.count):
                    report_element_node = None
                    if XML_OUTPUT:
                        report_element_node = TAG.xml_doc.createElement('element')
                        report_element_node.setAttribute('index', str(report_idx))
                        report_node.appendChild(report_element_node)

                    report = LEVEL.Report()
                    report.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(report_element_node, "report type", ReportTypeEnum))
                    report.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(report_element_node, "flags", ReportFlags))
                    report.report_length = TAG.read_signed_short(input_stream, TAG)
                    input_stream.read(18) # Padding?
                    report.source_filename = TAG.read_string32(input_stream, TAG, tag_format.XMLData(report_element_node, "source filename"))
                    report.source_line_number = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(report_element_node, "source line number"))
                    report.vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(report_element_node, "vertices"))
                    report.vectors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(report_element_node, "vectors"))
                    report.lines_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(report_element_node, "lines"))
                    report.triangles_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(report_element_node, "triangles"))
                    report.quads_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(report_element_node, "quads"))
                    report.comments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(report_element_node, "comments"))
                    input_stream.read(380) # Padding?
                    report.report_key = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(report_element_node, "report key"))
                    report.node_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(report_element_node, "node index"))
                    report.bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(report_element_node, "bounds x"))
                    report.bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(report_element_node, "bounds y"))
                    report.bounds_z = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(report_element_node, "bounds z"))
                    report.color = TAG.read_argb(input_stream, TAG, tag_format.XMLData(report_element_node, "color"))
                    input_stream.read(84) # Padding?

                    error.reports.append(report)

                for report_idx, report in enumerate(error.reports):
                    report_element_node = None
                    if XML_OUTPUT:
                        report_element_node = report_node.childNodes[report_idx]

                    if report.report_length > 0:
                        report.text = TAG.read_variable_string_no_terminator(input_stream, report.report_length, TAG, tag_format.XMLData(report_element_node, "text"))

                    report.vertices = []
                    report.vectors = []
                    report.lines = []
                    report.triangles = []
                    report.quads = []
                    report.comments = []
                    if report.vertices_tag_block.count > 0:
                        vertices_node = tag_format.get_xml_node(XML_OUTPUT, report.vertices_tag_block.count, report_element_node, "name", "vertices")
                        report.vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for vertex_idx in range(report.vertices_tag_block.count):
                            vertex_element_node = None
                            if XML_OUTPUT:
                                vertex_element_node = TAG.xml_doc.createElement('element')
                                vertex_element_node.setAttribute('index', str(vertex_idx))
                                vertices_node.appendChild(vertex_element_node)

                            vertex = LEVEL.ReportVertex()
                            vertex.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(vertex_element_node, "position"), True)
                            vertex.node_index_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(vertex_element_node, "node index"))
                            vertex.node_index_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(vertex_element_node, "node index"))
                            vertex.node_index_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(vertex_element_node, "node index"))
                            vertex.node_index_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(vertex_element_node, "node index"))
                            vertex.node_weight_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(vertex_element_node, "node weight"))
                            vertex.node_weight_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(vertex_element_node, "node weight"))
                            vertex.node_weight_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(vertex_element_node, "node weight"))
                            vertex.node_weight_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(vertex_element_node, "node weight"))
                            vertex.color = TAG.read_argb(input_stream, TAG, tag_format.XMLData(vertex_element_node, "color"))
                            vertex.screen_size = TAG.read_float(input_stream, TAG, tag_format.XMLData(vertex_element_node, "screen size"))

                            report.vertices.append(vertex)

                    if report.vectors_tag_block.count > 0:
                        vectors_node = tag_format.get_xml_node(XML_OUTPUT, report.vectors_tag_block.count, report_element_node, "name", "vectors")
                        report.vectors_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for vector_idx in range(report.vectors_tag_block.count):
                            vector_element_node = None
                            if XML_OUTPUT:
                                vector_element_node = TAG.xml_doc.createElement('element')
                                vector_element_node.setAttribute('index', str(vector_idx))
                                vectors_node.appendChild(vector_element_node)

                            vector = LEVEL.ReportVector()
                            vector.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(vector_element_node, "position"))
                            vector.node_index_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(vector_element_node, "node index"))
                            vector.node_index_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(vector_element_node, "node index"))
                            vector.node_index_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(vector_element_node, "node index"))
                            vector.node_index_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(vector_element_node, "node index"))
                            vector.node_weight_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(vector_element_node, "node weight"))
                            vector.node_weight_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(vector_element_node, "node weight"))
                            vector.node_weight_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(vector_element_node, "node weight"))
                            vector.node_weight_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(vector_element_node, "node weight"))
                            vector.color = TAG.read_argb(input_stream, TAG, tag_format.XMLData(vector_element_node, "color"))
                            vector.normal = TAG.read_vector(input_stream, TAG, tag_format.XMLData(vector_element_node, "normal"))
                            vector.screen_length = TAG.read_float(input_stream, TAG, tag_format.XMLData(vector_element_node, "screen length"))

                            report.vectors.append(vector)

                    if report.lines_tag_block.count > 0:
                        lines_node = tag_format.get_xml_node(XML_OUTPUT, report.lines_tag_block.count, report_element_node, "name", "lines")
                        report.lines_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for line_idx in range(report.lines_tag_block.count):
                            line_element_node = None
                            if XML_OUTPUT:
                                line_element_node = TAG.xml_doc.createElement('element')
                                line_element_node.setAttribute('index', str(line_idx))
                                lines_node.appendChild(line_element_node)

                            line = LEVEL.ReportLine()
                            line.position_a = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(line_element_node, "position"))
                            line.node_index_a_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(line_element_node, "node index"))
                            line.node_index_a_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(line_element_node, "node index"))
                            line.node_index_a_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(line_element_node, "node index"))
                            line.node_index_a_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(line_element_node, "node index"))
                            line.node_weight_a_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(line_element_node, "node weight"))
                            line.node_weight_a_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(line_element_node, "node weight"))
                            line.node_weight_a_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(line_element_node, "node weight"))
                            line.node_weight_a_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(line_element_node, "node weight"))
                            line.position_b = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(line_element_node, "position"))
                            line.node_index_b_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(line_element_node, "node index"))
                            line.node_index_b_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(line_element_node, "node index"))
                            line.node_index_b_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(line_element_node, "node index"))
                            line.node_index_b_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(line_element_node, "node index"))
                            line.node_weight_b_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(line_element_node, "node weight"))
                            line.node_weight_b_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(line_element_node, "node weight"))
                            line.node_weight_b_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(line_element_node, "node weight"))
                            line.node_weight_b_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(line_element_node, "node weight"))
                            line.color = TAG.read_argb(input_stream, TAG, tag_format.XMLData(line_element_node, "color"))

                            report.lines.append(line)

                    if report.triangles_tag_block.count > 0:
                        triangles_node = tag_format.get_xml_node(XML_OUTPUT, report.triangles_tag_block.count, report_element_node, "name", "triangles")
                        report.triangles_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for triangle_idx in range(report.triangles_tag_block.count):
                            triangle_element_node = None
                            if XML_OUTPUT:
                                triangle_element_node = TAG.xml_doc.createElement('element')
                                triangle_element_node.setAttribute('index', str(triangle_idx))
                                triangles_node.appendChild(triangle_element_node)

                            triangle = LEVEL.ReportTriangle()
                            triangle.position_a = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(triangle_element_node, "position"))
                            triangle.node_index_a_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node index"))
                            triangle.node_index_a_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node index"))
                            triangle.node_index_a_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node index"))
                            triangle.node_index_a_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node index"))
                            triangle.node_weight_a_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node weight"))
                            triangle.node_weight_a_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node weight"))
                            triangle.node_weight_a_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node weight"))
                            triangle.node_weight_a_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node weight"))
                            triangle.position_b = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(triangle_element_node, "position"))
                            triangle.node_index_b_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node index"))
                            triangle.node_index_b_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node index"))
                            triangle.node_index_b_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node index"))
                            triangle.node_index_b_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node index"))
                            triangle.node_weight_b_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node weight"))
                            triangle.node_weight_b_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node weight"))
                            triangle.node_weight_b_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node weight"))
                            triangle.node_weight_b_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node weight"))
                            triangle.position_c = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(triangle_element_node, "position"))
                            triangle.node_index_c_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node index"))
                            triangle.node_index_c_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node index"))
                            triangle.node_index_c_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node index"))
                            triangle.node_index_c_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node index"))
                            triangle.node_weight_c_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node weight"))
                            triangle.node_weight_c_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node weight"))
                            triangle.node_weight_c_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node weight"))
                            triangle.node_weight_c_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(triangle_element_node, "node weight"))
                            triangle.color = TAG.read_argb(input_stream, TAG, tag_format.XMLData(triangle_element_node, "color"))

                            report.triangles.append(triangle)

                    if report.quads_tag_block.count > 0:
                        quads_node = tag_format.get_xml_node(XML_OUTPUT, report.quads_tag_block.count, report_element_node, "name", "quads")
                        report.quads_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for quad_idx in range(report.quads_tag_block.count):
                            quad_element_node = None
                            if XML_OUTPUT:
                                quad_element_node = TAG.xml_doc.createElement('element')
                                quad_element_node.setAttribute('index', str(quad_idx))
                                quads_node.appendChild(quad_element_node)

                            quad = LEVEL.ReportQuad()
                            quad.position_a = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(quad_element_node, "position"))
                            quad.node_index_a_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_index_a_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_index_a_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_index_a_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_weight_a_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.node_weight_a_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.node_weight_a_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.node_weight_a_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.position_b = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(quad_element_node, "position"))
                            quad.node_index_b_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_index_b_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_index_b_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_index_b_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_weight_b_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.node_weight_b_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.node_weight_b_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.node_weight_b_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.position_c = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(quad_element_node, "position"))
                            quad.node_index_c_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_index_c_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_index_c_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_index_c_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_weight_c_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.node_weight_c_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.node_weight_c_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.node_weight_c_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.position_d = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(quad_element_node, "position"))
                            quad.node_index_d_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_index_d_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_index_d_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_index_d_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(quad_element_node, "node index"))
                            quad.node_weight_d_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.node_weight_d_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.node_weight_d_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.node_weight_d_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(quad_element_node, "node weight"))
                            quad.color = TAG.read_argb(input_stream, TAG, tag_format.XMLData(quad_element_node, "color"))

                            report.quads.append(quad)

                    if report.comments_tag_block.count > 0:
                        comments_node = tag_format.get_xml_node(XML_OUTPUT, report.comments_tag_block.count, report_element_node, "name", "comments")
                        report.comments_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for comment_idx in range(report.comments_tag_block.count):
                            comment_element_node = None
                            if XML_OUTPUT:
                                comment_element_node = TAG.xml_doc.createElement('element')
                                comment_element_node.setAttribute('index', str(comment_idx))
                                comments_node.appendChild(comment_element_node)

                            comment = LEVEL.ReportComment()
                            comment.text_length = TAG.read_signed_short(input_stream, TAG)
                            input_stream.read(18) # Padding?
                            comment.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(comment_element_node, "position"))
                            comment.node_index_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(comment_element_node, "node index"))
                            comment.node_index_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(comment_element_node, "node index"))
                            comment.node_index_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(comment_element_node, "node index"))
                            comment.node_index_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(comment_element_node, "node index"))
                            comment.node_weight_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(comment_element_node, "node weight"))
                            comment.node_weight_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(comment_element_node, "node weight"))
                            comment.node_weight_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(comment_element_node, "node weight"))
                            comment.node_weight_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(comment_element_node, "node weight"))
                            comment.color = TAG.read_argb(input_stream, TAG, tag_format.XMLData(comment_element_node, "color"))

                            report.comments.append(comment)

                        for comment_idx, comment in enumerate(report.comments):
                            comment_element_node = None
                            if XML_OUTPUT:
                                comment_element_node = comments_node.childNodes[comment_idx]

                            if comment.text_length > 0:
                                comment.text = TAG.read_variable_string_no_terminator(input_stream, comment.text_length, TAG, tag_format.XMLData(comment_element_node, "text"))

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    LIGHTMAP = LightmapAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    LIGHTMAP.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    LIGHTMAP.lightmap_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    LIGHTMAP.lightmap_body = LIGHTMAP.LightmapBody()
    LIGHTMAP.lightmap_body.search_distance_lower_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "search distance lower bound"))
    LIGHTMAP.lightmap_body.search_distance_upper_bound = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "search distance upper bound"))
    LIGHTMAP.lightmap_body.luminels_per_world_unit = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "luminels per world unit"))
    LIGHTMAP.lightmap_body.output_white_reference = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "output white reference"))
    LIGHTMAP.lightmap_body.output_black_reference = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "output black reference"))
    LIGHTMAP.lightmap_body.output_schlick_parameter = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "output schlick parameter"))
    LIGHTMAP.lightmap_body.diffuse_map_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "diffuse map scale"))
    LIGHTMAP.lightmap_body.sun_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "sun scale"))
    LIGHTMAP.lightmap_body.sky_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "sky scale"))
    LIGHTMAP.lightmap_body.indirect_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "indirect scale"))
    LIGHTMAP.lightmap_body.prt_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "prt scale"))
    LIGHTMAP.lightmap_body.surface_light_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "surface light scale"))
    LIGHTMAP.lightmap_body.scenario_light_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "scenario light scale"))
    LIGHTMAP.lightmap_body.lightprobe_interpolation_override = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lightprobe interpolation override"))
    input_stream.read(72) # Padding?
    LIGHTMAP.lightmap_body.lightmap_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap groups"))
    input_stream.read(12) # Padding?
    LIGHTMAP.lightmap_body.errors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "errors"))
    input_stream.read(104) # Padding?

    read_lightmap_groups(LIGHTMAP, TAG, input_stream, tag_node, XML_OUTPUT)
    #read_errors(LIGHTMAP, TAG, input_stream, tag_node, XML_OUTPUT)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, LIGHTMAP.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return LIGHTMAP
