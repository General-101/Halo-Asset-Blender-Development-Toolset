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
    RenderAsset, 
    RenderFlags, 
    GeometryClassificationEnum, 
    GeometryCompressionFlags,
    SectionLightingFlags,
    SectionFlags,
    ResourceEnum,
    PartTypeEnum,
    PartFlags,
    ISQFlags,
    DetailLevelsFlags,
    PropertyTypeEnum,
    ReportTypeEnum,
    ReportFlags,
    )

XML_OUTPUT = False

def initilize_render(RENDER):
    RENDER.import_info = []
    RENDER.compression_info = []
    RENDER.regions = []
    RENDER.sections = []
    RENDER.invalid_section_pair_bits = []
    RENDER.section_groups = []
    RENDER.nodes = []
    RENDER.transforms = []
    RENDER.node_map = []
    RENDER.marker_groups = []
    RENDER.materials = []
    RENDER.errors = []
    RENDER.prt_info = []
    RENDER.section_render_leaves = []

def read_render_body_v0(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    RENDER.render_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    RENDER.render_body = RenderAsset.RenderBody()

    RENDER.render_body.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(tag_node, "name"))
    RENDER.render_body.name_length = len(RENDER.render_body.name)
    RENDER.render_body.flags = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", RenderFlags))
    input_stream.read(6) # Padding?
    RENDER.render_body.import_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "import info"))
    RENDER.render_body.compression_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "compression info"))
    RENDER.render_body.regions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "regions"))
    RENDER.render_body.sections_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sections"))
    RENDER.render_body.invalid_section_pair_bits_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "invalid section pair bits"))
    RENDER.render_body.section_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "section groups"))
    RENDER.render_body.l1_section_group_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "l1 section group index"))
    RENDER.render_body.l2_section_group_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "l2 section group index"))
    RENDER.render_body.l3_section_group_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "l3 section group index"))
    RENDER.render_body.l4_section_group_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "l4 section group index"))
    RENDER.render_body.l5_section_group_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "l5 section group index"))
    RENDER.render_body.l6_section_group_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "l6 section group index"))
    input_stream.read(2) # Padding?
    RENDER.render_body.node_list_checksum = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(tag_node, "node list checksum"))
    RENDER.render_body.nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "nodes"))
    RENDER.render_body.node_map_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "node map"))
    RENDER.render_body.marker_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "marker groups"))
    RENDER.render_body.materials_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "materials"))
    RENDER.render_body.errors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "errors"))
    RENDER.render_body.dont_draw_over_camera_cosine_angle = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dont draw over camera cosine angle"))
    RENDER.render_body.prt_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "prt info"))
    RENDER.render_body.section_render_leaves_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "section render leaves"))

def read_render_body_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    RENDER.render_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    RENDER.render_body = RenderAsset.RenderBody()

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    RENDER.render_body.name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    RENDER.render_body.flags = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", RenderFlags))
    input_stream.read(6) # Padding?
    RENDER.render_body.import_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "import info"))
    RENDER.render_body.compression_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "compression info"))
    RENDER.render_body.regions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "regions"))
    RENDER.render_body.sections_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sections"))
    RENDER.render_body.invalid_section_pair_bits_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "invalid section pair bits"))
    RENDER.render_body.section_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "section groups"))
    RENDER.render_body.l1_section_group_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "l1 section group index"))
    RENDER.render_body.l2_section_group_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "l2 section group index"))
    RENDER.render_body.l3_section_group_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "l3 section group index"))
    RENDER.render_body.l4_section_group_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "l4 section group index"))
    RENDER.render_body.l5_section_group_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "l5 section group index"))
    RENDER.render_body.l6_section_group_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "l6 section group index"))
    input_stream.read(2) # Padding?
    RENDER.render_body.node_list_checksum = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(tag_node, "node list checksum"))
    RENDER.render_body.nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "nodes"))
    RENDER.render_body.node_map_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "node map"))
    RENDER.render_body.marker_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "marker groups"))
    RENDER.render_body.materials_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "materials"))
    RENDER.render_body.errors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "errors"))
    RENDER.render_body.dont_draw_over_camera_cosine_angle = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dont draw over camera cosine angle"))
    RENDER.render_body.prt_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "prt info"))
    RENDER.render_body.section_render_leaves_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "section render leaves"))

def read_import_info(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.import_info_tag_block.count > 0:
        import_info_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.import_info_tag_block.count, tag_node, "name", "import info")
        RENDER.import_info_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for import_info_idx in range(RENDER.render_body.import_info_tag_block.count):
            import_info_element_node = None
            if XML_OUTPUT:
                import_info_element_node = TAG.xml_doc.createElement('element')
                import_info_element_node.setAttribute('index', str(import_info_idx))
                import_info_node.appendChild(import_info_element_node)

            import_info = RENDER.ImportInfo()
            import_info.build = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(import_info_element_node, "build"))
            import_info.version = TAG.read_string256(input_stream, TAG, tag_format.XMLData(import_info_element_node, "version"))
            import_info.import_date = TAG.read_string32(input_stream, TAG, tag_format.XMLData(import_info_element_node, "import date"))
            import_info.culprit = TAG.read_string32(input_stream, TAG, tag_format.XMLData(import_info_element_node, "culprit"))
            input_stream.read(96) # Padding?
            import_info.import_time = TAG.read_string32(input_stream, TAG, tag_format.XMLData(import_info_element_node, "import time"))
            input_stream.read(4) # Padding?
            import_info.files_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(import_info_element_node, "files"))
            input_stream.read(128) # Padding?

            RENDER.import_info.append(import_info)

        for import_info_idx, import_info in enumerate(RENDER.import_info):
            import_info_element_node = None
            if XML_OUTPUT:
                import_info_element_node = import_info_node.childNodes[import_info_idx]

            import_info.files = []
            if import_info.files_tag_block.count > 0:
                files_node = tag_format.get_xml_node(XML_OUTPUT, import_info.files_tag_block.count, import_info_element_node, "name", "files")
                import_info.files_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for file_idx in range(import_info.files_tag_block.count):
                    file_element_node = None
                    if XML_OUTPUT:
                        file_element_node = TAG.xml_doc.createElement('element')
                        file_element_node.setAttribute('index', str(file_idx))
                        files_node.appendChild(file_element_node)

                    file = RENDER.File()
                    file.path = TAG.read_string256(input_stream, TAG, tag_format.XMLData(file_element_node, "path"))
                    file.modification_date = TAG.read_string32(input_stream, TAG, tag_format.XMLData(file_element_node, "modification date"))
                    input_stream.read(96) # Padding?
                    file.checksum = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(file_element_node, "checksum"))
                    file.size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(file_element_node, "size"))
                    file.zipped_data = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(file_element_node, "zipped data"))
                    input_stream.read(144) # Padding?

                    import_info.files.append(file)

                for file_idx, file in enumerate(import_info.files):
                    file_element_node = None
                    if XML_OUTPUT:
                        file_element_node = files_node.childNodes[file_idx]

                    file.uncompressed_data = input_stream.read(file.zipped_data)

def read_compression_info(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.compression_info_tag_block.count > 0:
        compression_info_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.compression_info_tag_block.count, tag_node, "name", "compression info")
        RENDER.compression_info_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for compression_info_idx in range(RENDER.render_body.compression_info_tag_block.count):
            compression_info_element_node = None
            if XML_OUTPUT:
                compression_info_element_node = TAG.xml_doc.createElement('element')
                compression_info_element_node.setAttribute('index', str(compression_info_idx))
                compression_info_node.appendChild(compression_info_element_node)

            compression_info = RENDER.CompressionInfo()
            compression_info.position_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds x"))
            compression_info.position_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds y"))
            compression_info.position_bounds_z = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds z"))
            compression_info.texcoord_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "texcoord bounds x"))
            compression_info.texcoord_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "texcoord bounds y"))
            compression_info.secondary_texcoord_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "secondary texcoord bounds x"))
            compression_info.secondary_texcoord_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "secondary texcoord bounds y"))

            RENDER.compression_info.append(compression_info)

def read_regions_v0(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.regions_tag_block.count > 0:
        regions_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.regions_tag_block.count, tag_node, "name", "regions")
        RENDER.region_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for region_idx in range(RENDER.render_body.regions_tag_block.count):
            region_element_node = None
            if XML_OUTPUT:
                region_element_node = TAG.xml_doc.createElement('element')
                region_element_node.setAttribute('index', str(region_idx))
                regions_node.appendChild(region_element_node)

            region = RENDER.Region()

            region.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(region_element_node, "name"))
            region.name_length = len(region.name)
            region.node_map_offset = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(region_element_node, "node map offset"))
            region.node_map_size = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(region_element_node, "node map size"))
            region.permutations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(region_element_node, "permutations"))

            RENDER.regions.append(region)

        for region_idx, region in enumerate(RENDER.regions):
            region_element_node = None
            if XML_OUTPUT:
                region_element_node = regions_node.childNodes[region_idx]

            region.permutations = []
            if region.permutations_tag_block.count > 0:
                permutations_node = tag_format.get_xml_node(XML_OUTPUT, region.permutations_tag_block.count, region_element_node, "name", "permutations")
                region.permutations_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for permutation_idx in range(region.permutations_tag_block.count):
                    permutation_element_node = None
                    if XML_OUTPUT:
                        permutation_element_node = TAG.xml_doc.createElement('element')
                        permutation_element_node.setAttribute('index', str(permutation_idx))
                        permutations_node.appendChild(permutation_element_node)

                    permutation = RENDER.Permutation()

                    permutation.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(permutation_element_node, "name"))
                    permutation.name_length = len(permutation.name)
                    permutation.l1_section_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "l1 section index"))
                    permutation.l2_section_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "l2 section index"))
                    permutation.l3_section_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "l3 section index"))
                    permutation.l4_section_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "l4 section index"))
                    permutation.l5_section_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "l5 section index"))
                    permutation.l6_section_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "l6 section index"))

                    region.permutations.append(permutation)

def read_regions_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.regions_tag_block.count > 0:
        regions_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.regions_tag_block.count, tag_node, "name", "regions")
        RENDER.region_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for region_idx in range(RENDER.render_body.regions_tag_block.count):
            region_element_node = None
            if XML_OUTPUT:
                region_element_node = TAG.xml_doc.createElement('element')
                region_element_node.setAttribute('index', str(region_idx))
                regions_node.appendChild(region_element_node)

            region = RENDER.Region()

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            region.name_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            region.node_map_offset = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(region_element_node, "node map offset"))
            region.node_map_size = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(region_element_node, "node map size"))
            region.permutations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(region_element_node, "permutations"))

            RENDER.regions.append(region)

        for region_idx, region in enumerate(RENDER.regions):
            region_element_node = None
            if XML_OUTPUT:
                region_element_node = regions_node.childNodes[region_idx]

            if region.name_length > 0:
                region.name = TAG.read_variable_string_no_terminator(input_stream, region.name_length, TAG, tag_format.XMLData(region_element_node, "name"))

            region.permutations = []
            if region.permutations_tag_block.count > 0:
                permutations_node = tag_format.get_xml_node(XML_OUTPUT, region.permutations_tag_block.count, region_element_node, "name", "permutations")
                region.permutations_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for permutation_idx in range(region.permutations_tag_block.count):
                    permutation_element_node = None
                    if XML_OUTPUT:
                        permutation_element_node = TAG.xml_doc.createElement('element')
                        permutation_element_node.setAttribute('index', str(permutation_idx))
                        permutations_node.appendChild(permutation_element_node)

                    permutation = RENDER.Permutation()

                    TAG.big_endian = True
                    input_stream.read(2) # Padding?
                    permutation.name_length = TAG.read_signed_short(input_stream, TAG)
                    TAG.big_endian = False

                    permutation.l1_section_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "l1 section index"))
                    permutation.l2_section_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "l2 section index"))
                    permutation.l3_section_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "l3 section index"))
                    permutation.l4_section_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "l4 section index"))
                    permutation.l5_section_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "l5 section index"))
                    permutation.l6_section_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "l6 section index"))

                    region.permutations.append(permutation)

                for permutation_idx, permutation in enumerate(region.permutations):
                    permutation_element_node = None
                    if XML_OUTPUT:
                        permutation_element_node = permutations_node.childNodes[permutation_idx]

                    if region.name_length > 0:
                        permutation.name = TAG.read_variable_string_no_terminator(input_stream, permutation.name_length, TAG, tag_format.XMLData(permutation_element_node, "name"))

def read_parts_v0(RENDER, section_data, TAG, input_stream, node_element):
    if section_data.parts_tag_block.count > 0:
        parts_node = tag_format.get_xml_node(XML_OUTPUT, section_data.parts_tag_block.count, node_element, "name", "parts")
        section_data.parts_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for part_idx in range(section_data.parts_tag_block.count):
            part_element_node = None
            if XML_OUTPUT:
                part_element_node = TAG.xml_doc.createElement('element')
                part_element_node.setAttribute('index', str(part_idx))
                parts_node.appendChild(part_element_node)

            part = RENDER.Part()
            part.part_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(part_element_node, "type", PartTypeEnum))
            part.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(part_element_node, "flags", PartFlags))
            part.material_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(part_element_node, "material", None, RENDER.render_body.materials_tag_block.count, "material"))
            input_stream.read(2) # Padding?
            part.strip_start_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(part_element_node, "strip start index"))
            part.strip_length = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(part_element_node, "strip length"))
            #part.first_subpart_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(part_element_node, "first subpart index"))
            #part.subpart_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(part_element_node, "subpart count"))
            input_stream.read(12) # Padding?
            part.max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "max nodes vertex"))
            part.contributing_compound_node_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "contributing compound node count"))
            input_stream.read(18) # Padding?
            part.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(part_element_node, "position"))
            part.node_index_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "node index 0"))
            part.node_index_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "node index 1"))
            part.node_index_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "node index 2"))
            part.node_index_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "node index 3"))
            part.node_weight_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(part_element_node, "node weight 0"))
            part.node_weight_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(part_element_node, "node weight 1"))
            part.node_weight_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(part_element_node, "node weight 2"))
            part.lod_mipmap_magic_number = TAG.read_float(input_stream, TAG, tag_format.XMLData(part_element_node, "lod mipmap magic number"))
            input_stream.read(24) # Padding?

            section_data.parts.append(part)

def read_parts_retail(RENDER, section_data, TAG, input_stream, node_element):
    if section_data.parts_tag_block.count > 0:
        parts_node = tag_format.get_xml_node(XML_OUTPUT, section_data.parts_tag_block.count, node_element, "name", "parts")
        section_data.parts_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for part_idx in range(section_data.parts_tag_block.count):
            part_element_node = None
            if XML_OUTPUT:
                part_element_node = TAG.xml_doc.createElement('element')
                part_element_node.setAttribute('index', str(part_idx))
                parts_node.appendChild(part_element_node)

            part = RENDER.Part()
            part.part_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(part_element_node, "type", PartTypeEnum))
            part.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(part_element_node, "flags", PartFlags))
            part.material_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(part_element_node, "material", None, RENDER.render_body.materials_tag_block.count, "material"))
            part.strip_start_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(part_element_node, "strip start index"))
            part.strip_length = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(part_element_node, "strip length"))
            part.first_subpart_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(part_element_node, "first subpart index"))
            part.subpart_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(part_element_node, "subpart count"))
            part.max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "max nodes vertex"))
            part.contributing_compound_node_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "contributing compound node count"))
            part.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(part_element_node, "position"))
            part.node_index_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "node index 0"))
            part.node_index_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "node index 1"))
            part.node_index_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "node index 2"))
            part.node_index_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(part_element_node, "node index 3"))
            part.node_weight_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(part_element_node, "node weight 0"))
            part.node_weight_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(part_element_node, "node weight 1"))
            part.node_weight_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(part_element_node, "node weight 2"))
            part.lod_mipmap_magic_number = TAG.read_float(input_stream, TAG, tag_format.XMLData(part_element_node, "lod mipmap magic number"))
            input_stream.read(24) # Padding?

            section_data.parts.append(part)

def read_subparts(RENDER, section_data, TAG, input_stream, node_element):
    if section_data.subparts_tag_block.count > 0:
        subparts_node = tag_format.get_xml_node(XML_OUTPUT, section_data.subparts_tag_block.count, node_element, "name", "subparts")
        section_data.subparts_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for subpart_idx in range(section_data.subparts_tag_block.count):
            subpart_element_node = None
            if XML_OUTPUT:
                subpart_element_node = TAG.xml_doc.createElement('element')
                subpart_element_node.setAttribute('index', str(subpart_idx))
                subparts_node.appendChild(subpart_element_node)

            sub_part = RENDER.SubPart()
            sub_part.indices_start_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subpart_element_node, "indices start index"))
            sub_part.indices_length = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subpart_element_node, "indices length"))
            sub_part.visibility_bounds_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subpart_element_node, "visibility bounds index"))
            sub_part.part_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subpart_element_node, "part index"))

            section_data.subparts.append(sub_part)

def read_visibility_bounds(RENDER, section_data, TAG, input_stream, node_element):
    if section_data.visibility_bounds_tag_block.count > 0:
        visibility_bounds_node = tag_format.get_xml_node(XML_OUTPUT, section_data.visibility_bounds_tag_block.count, node_element, "name", "visibility bounds")
        section_data.subparts_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for visibility_bound_idx in range(section_data.visibility_bounds_tag_block.count):
            visibility_bound_element_node = None
            if XML_OUTPUT:
                visibility_bound_element_node = TAG.xml_doc.createElement('element')
                visibility_bound_element_node.setAttribute('index', str(visibility_bound_idx))
                visibility_bounds_node.appendChild(visibility_bound_element_node)

            visibility_bound = RENDER.VisibilityBounds()
            visibility_bound.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(visibility_bound_element_node, "position"))
            visibility_bound.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(visibility_bound_element_node, "radius"))
            visibility_bound.node_0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(visibility_bound_element_node, "node 0"))
            input_stream.read(2) # Padding?

            section_data.visibility_bounds.append(visibility_bound)

def read_raw_vertices(RENDER, section_data, TAG, input_stream, node_element):
    if section_data.raw_vertices_tag_block.count > 0:
        raw_vertices_node = tag_format.get_xml_node(XML_OUTPUT, section_data.raw_vertices_tag_block.count, node_element, "name", "raw vertices")
        section_data.raw_vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for raw_vertex_idx in range(section_data.raw_vertices_tag_block.count):
            raw_vertex_element_node = None
            if XML_OUTPUT:
                raw_vertex_element_node = TAG.xml_doc.createElement('element')
                raw_vertex_element_node.setAttribute('index', str(raw_vertex_idx))
                raw_vertices_node.appendChild(raw_vertex_element_node)

            raw_vertex = RENDER.RawVertex()
            raw_vertex.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "position"), True)
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
            raw_vertex.anisotropic_binormal = TAG.read_vector(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "anisotropic tangent"))
            raw_vertex.secondary_texcoord = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "secondary texcoord"))
            raw_vertex.primary_lightmap_color_RGBA = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "primary lightmap color"))
            raw_vertex.primary_lightmap_texcoord = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "primary lightmap texcoord"))
            raw_vertex.primary_lightmap_incident_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(raw_vertex_element_node, "primary lightmap incident direction"))
            input_stream.read(32) # Padding?

            section_data.raw_vertices.append(raw_vertex)

def read_strip_indices(RENDER, section_data, TAG, input_stream, node_element):
    if section_data.strip_indices_tag_block.count > 0:
        strip_indices_node = tag_format.get_xml_node(XML_OUTPUT, section_data.strip_indices_tag_block.count, node_element, "name", "strip indices")
        section_data.strip_indices_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for strip_index_idx in range(section_data.strip_indices_tag_block.count):
            strip_index_element_node = None
            if XML_OUTPUT:
                strip_index_element_node = TAG.xml_doc.createElement('element')
                strip_index_element_node.setAttribute('index', str(strip_index_idx))
                strip_indices_node.appendChild(strip_index_element_node)

            section_data.strip_indices.append(TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(strip_index_element_node, "index")))

def read_mopp_reorder_table(RENDER, section_data, TAG, input_stream, node_element):
    if section_data.mopp_reorder_table_tag_block.count > 0:
        mopp_reorder_table_node = tag_format.get_xml_node(XML_OUTPUT, section_data.mopp_reorder_table_tag_block.count, node_element, "name", "mopp reorder table")
        section_data.mopp_reorder_table_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for mopp_reorder_table_idx in range(section_data.mopp_reorder_table_tag_block.count):
            mopp_reorder_table_element_node = None
            if XML_OUTPUT:
                mopp_reorder_table_element_node = TAG.xml_doc.createElement('element')
                mopp_reorder_table_element_node.setAttribute('index', str(mopp_reorder_table_idx))
                mopp_reorder_table_node.appendChild(mopp_reorder_table_element_node)

            section_data.mopp_reorder_table.append(TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(mopp_reorder_table_element_node, "index")))

def read_vertex_buffers(RENDER, section_data, TAG, input_stream, node_element):
    if section_data.vertex_buffers_tag_block.count > 0:
        vertex_buffers_node = tag_format.get_xml_node(XML_OUTPUT, section_data.vertex_buffers_tag_block.count, node_element, "name", "vertex buffers")
        section_data.mopp_reorder_table_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for vertex_buffer_idx in range(section_data.vertex_buffers_tag_block.count):
            vertex_buffer_element_node = None
            if XML_OUTPUT:
                vertex_buffer_element_node = TAG.xml_doc.createElement('element')
                vertex_buffer_element_node.setAttribute('index', str(vertex_buffer_idx))
                vertex_buffers_node.appendChild(vertex_buffer_element_node)

            input_stream.read(32) # Padding?

def read_raw_points(RENDER, section_data, TAG, input_stream, node_element):
    if section_data.raw_points_tag_block.count > 0:
        raw_points_node = tag_format.get_xml_node(XML_OUTPUT, section_data.raw_points_tag_block.count, node_element, "name", "raw points")
        section_data.raw_points_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for raw_point_idx in range(section_data.raw_points_tag_block.count):
            raw_point_element_node = None
            if XML_OUTPUT:
                raw_point_element_node = TAG.xml_doc.createElement('element')
                raw_point_element_node.setAttribute('index', str(raw_point_idx))
                raw_points_node.appendChild(raw_point_element_node)

            raw_point = RENDER.RawPoint()
            raw_point.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "position"), True)
            raw_point.node_index_0_old = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "node index 0 old"))
            raw_point.node_index_1_old = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "node index 1 old"))
            raw_point.node_index_2_old = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "node index 2 old"))
            raw_point.node_index_3_old = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "node index 3 old"))
            raw_point.node_weight_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "node weight 0"))
            raw_point.node_weight_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "node weight 1"))
            raw_point.node_weight_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "node weight 2"))
            raw_point.node_weight_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "node weight 3"))
            raw_point.node_index_0_new = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "node index 0 new"))
            raw_point.node_index_1_new = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "node index 1 new"))
            raw_point.node_index_2_new = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "node index 2 new"))
            raw_point.node_index_3_new = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "node index 3 new"))
            raw_point.uses_new_node_indices = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "uses new node indices"))
            raw_point.adjusted_compound_node_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(raw_point_element_node, "adjusted compound node index"))

            section_data.raw_points.append(raw_point)

def read_rigid_point_groups(RENDER, section_data, TAG, input_stream, node_element):
    if section_data.rigid_point_groups_tag_block.count > 0:
        rigid_point_groups_node = tag_format.get_xml_node(XML_OUTPUT, section_data.rigid_point_groups_tag_block.count, node_element, "name", "rigid point groups")
        section_data.rigid_point_groups_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for rigid_point_group_idx in range(section_data.rigid_point_groups_tag_block.count):
            rigid_point_group_element_node = None
            if XML_OUTPUT:
                rigid_point_group_element_node = TAG.xml_doc.createElement('element')
                rigid_point_group_element_node.setAttribute('index', str(rigid_point_group_idx))
                rigid_point_groups_node.appendChild(rigid_point_group_element_node)

            rigid_point_group = RENDER.RigidPointGroup()
            rigid_point_group.rigid_node_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(rigid_point_group_element_node, "rigid node index"))
            rigid_point_group.nodes_per_point = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(rigid_point_group_element_node, "nodes per point"))
            rigid_point_group.point_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(rigid_point_group_element_node, "point count"))

            section_data.rigid_point_groups.append(rigid_point_group)

def read_vertex_point_indices(RENDER, section_data, TAG, input_stream, node_element):
    if section_data.vertex_point_indices_tag_block.count > 0:
        vertex_point_indices_node = tag_format.get_xml_node(XML_OUTPUT, section_data.vertex_point_indices_tag_block.count, node_element, "name", "vertex point indices")
        section_data.vertex_point_indices_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for vertex_point_idx in range(section_data.vertex_point_indices_tag_block.count):
            vertex_point_element_node = None
            if XML_OUTPUT:
                vertex_point_element_node = TAG.xml_doc.createElement('element')
                vertex_point_element_node.setAttribute('index', str(vertex_point_idx))
                vertex_point_indices_node.appendChild(vertex_point_element_node)

            section_data.vertex_point_indices.append(TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(vertex_point_element_node, "index")))

def read_section_node_map(RENDER, section_data, TAG, input_stream, node_element):
    if section_data.node_map_tag_block.count > 0:
        node_map_node = tag_format.get_xml_node(XML_OUTPUT, section_data.node_map_tag_block.count, node_element, "name", "node map")
        section_data.node_map_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for node_map_idx in range(section_data.node_map_tag_block.count):
            node_map_element_node = None
            if XML_OUTPUT:
                node_map_element_node = TAG.xml_doc.createElement('element')
                node_map_element_node.setAttribute('index', str(node_map_idx))
                node_map_node.appendChild(node_map_element_node)

            section_data.node_map.append(TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_map_element_node, "node index")))

def read_sections_v0(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.sections_tag_block.count > 0:
        sections_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.sections_tag_block.count, tag_node, "name", "sections")
        RENDER.section_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for section_idx in range(RENDER.render_body.sections_tag_block.count):
            section_element_node = None
            if XML_OUTPUT:
                section_element_node = TAG.xml_doc.createElement('element')
                section_element_node.setAttribute('index', str(section_idx))
                sections_node.appendChild(section_element_node)

            section = RENDER.Section()
            section.global_geometry_classification = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(section_element_node, "global geometry classification", GeometryClassificationEnum))
            input_stream.read(2) # Padding?
            section.total_vertex_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "total vertex count"))
            section.total_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "total triangle count"))
            section.total_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "total part count"))
            section.shadow_casting_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "shadow casting triangle count"))
            section.shadow_casting_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "shadow casting part count"))
            section.opaque_point_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "opaque point count"))
            section.opaque_vertex_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "opaque vertex count"))
            section.opaque_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "opaque part count"))
            section.opaque_max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(section_element_node, "opaque max nodes vertex"))
            section.transparent_max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(section_element_node, "transparent max nodes vertex"))
            section.shadow_casting_rigid_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "shadow casting rigid triangle count"))
            section.geometry_classification = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(section_element_node, "geometry classification", GeometryClassificationEnum))
            section.geometry_compression_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(section_element_node, "geometry compression flags", GeometryCompressionFlags))
            section.compression_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_element_node, "compression info"))
            section.hardware_node_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(section_element_node, "hardware node count"))
            section.node_map_size = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(section_element_node, "node map size"))
            section.software_plane_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "software plane count"))
            if RENDER.section_header.size >= 104:
                section.total_subpart_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "total subpart count"))
                section.section_lighting_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(section_element_node, "section lighting flags", SectionLightingFlags))

            section.rigid_node = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "rigid node", None, RENDER.render_body.nodes_tag_block.count, "nodes"))
            section.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(section_element_node, "flags", SectionFlags))
            section.section_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_element_node, "section data"))
            section.block_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(section_element_node, "block offset"))
            section.block_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(section_element_node, "block size"))
            section.section_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(section_element_node, "section data size"))
            section.resource_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(section_element_node, "resource data size"))
            section.resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_element_node, "resources"))
            input_stream.read(4) # Padding?
            section.owner_tag_section_offset = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "owner tag section offset"))
            input_stream.read(6) # Padding?

            RENDER.sections.append(section)

        for section_idx, section in enumerate(RENDER.sections):
            section_element_node = None
            if XML_OUTPUT:
                section_element_node = sections_node.childNodes[section_idx]

            section.compression_info = []
            section.section_data = []
            section.resources = []

            section.sinf_header = TAG.TagBlockHeader().read(input_stream, TAG)
            if section.compression_info_tag_block.count > 0:
                compression_info_node = tag_format.get_xml_node(XML_OUTPUT, section.compression_info_tag_block.count, section_element_node, "name", "compression info")
                section.compression_info_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for compression_info_idx in range(section.compression_info_tag_block.count):
                    compression_info_element_node = None
                    if XML_OUTPUT:
                        compression_info_element_node = TAG.xml_doc.createElement('element')
                        compression_info_element_node.setAttribute('index', str(compression_info_idx))
                        compression_info_node.appendChild(compression_info_element_node)

                    compression_info = RENDER.CompressionInfo()
                    compression_info.position_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds x"))
                    compression_info.position_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds y"))
                    compression_info.position_bounds_z = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds z"))
                    compression_info.texcoord_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "texcoord bounds x"))
                    compression_info.texcoord_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "texcoord bounds y"))
                    compression_info.secondary_texcoord_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "secondary texcoord bounds x"))
                    compression_info.secondary_texcoord_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "secondary texcoord bounds y"))

                    section.compression_info.append(compression_info)

            if section.section_data_tag_block.count > 0:
                section_data_node = tag_format.get_xml_node(XML_OUTPUT, section.section_data_tag_block.count, section_element_node, "name", "section data")
                section.section_data_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for section_data_idx in range(section.section_data_tag_block.count):
                    section_data_element_node = None
                    if XML_OUTPUT:
                        section_data_element_node = TAG.xml_doc.createElement('element')
                        section_data_element_node.setAttribute('index', str(section_data_idx))
                        section_data_node.appendChild(section_data_element_node)

                    section_data = RENDER.LegacySectionData()

                    if section.section_data_header.version == 0:
                        if section.section_data_header.size == 524:
                            section_data.raw_vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "raw vertices"))
                            input_stream.read(128) # Padding?
                            section_data.vertex_buffers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "vertex buffers"))
                            section_data.strip_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "strip indices"))
                            section_data.parts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "parts"))
                            input_stream.read(96) # Padding?
                            section_data.raw_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "raw points"))
                            section_data.runtime_point_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "runtime point data"))
                            section_data.rigid_point_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "rigid point groups"))
                            section_data.vertex_point_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "vertex point indices"))
                            section_data.node_map_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "node map"))

                            section_data.isq_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(section_data_element_node, "flags", ISQFlags))
                            input_stream.read(2) # Padding?
                            section_data.raw_planes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "raw planes"))
                            section_data.runtime_plane_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "runtime plane data"))
                            section_data.rigid_plane_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "rigid plane groups"))
                            input_stream.read(32) # Padding?
                            section_data.explicit_edges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "explicit edges"))
                            section_data.forward_shared_edges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "forward shared edges"))
                            section_data.forward_shared_edge_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "forward shared edge groups"))
                            section_data.backward_shared_edges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "backward shared edges"))
                            section_data.backward_shared_edge_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "backward shared edge groups"))
                            section_data.dsq_raw_vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "dsq raw vertices"))
                            section_data.dsq_strip_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "dsq strip indices"))
                            section_data.dsq_silhouette_quads_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "dsq silhouette quads"))
                            section_data.carmack_silhouette_quad_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_data_element_node, "carmack silhouette quad count"))
                            input_stream.read(6) # Padding?

                            section_data.visibility_bounds_tag_block = TAG.TagBlock()
                            section_data.mopp_reorder_table_tag_block = TAG.TagBlock()

                        else:
                            section_data.parts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "parts"))
                            section_data.subparts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "subparts"))
                            section_data.visibility_bounds_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "visibility bounds"))
                            section_data.raw_vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "raw vertices"))
                            section_data.strip_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "strip indices"))
                            section_data.visibility_mopp_code_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "visibility mopp code"))
                            section_data.mopp_reorder_table_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "mopp reorder table"))
                            section_data.vertex_buffers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "vertex buffers"))
                            input_stream.read(4) # Padding?
                            section_data.raw_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "raw points"))
                            section_data.runtime_point_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "runtime point data"))
                            section_data.rigid_point_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "rigid point groups"))
                            section_data.vertex_point_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "vertex point indices"))
                            section_data.node_map_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "node map"))

                            section_data.isq_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(section_data_element_node, "flags", ISQFlags))
                            input_stream.read(2) # Padding?
                            section_data.raw_planes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "raw planes"))
                            section_data.runtime_plane_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "runtime plane data"))
                            section_data.rigid_plane_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "rigid plane groups"))
                            input_stream.read(32) # Padding?
                            section_data.explicit_edges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "explicit edges"))
                            section_data.forward_shared_edges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "forward shared edges"))
                            section_data.forward_shared_edge_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "forward shared edge groups"))
                            section_data.backward_shared_edges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "backward shared edges"))
                            section_data.backward_shared_edge_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "backward shared edge groups"))
                            section_data.dsq_raw_vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "dsq raw vertices"))
                            section_data.dsq_strip_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "dsq strip indices"))
                            section_data.dsq_silhouette_quads_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "dsq silhouette quads"))
                            section_data.carmack_silhouette_quad_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_data_element_node, "carmack silhouette quad count"))
                            input_stream.read(6) # Padding?

                    elif section.section_data_header.version == 1:
                        section_data.parts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "parts"))
                        section_data.subparts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "subparts"))
                        section_data.visibility_bounds_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "visibility bounds"))
                        section_data.raw_vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "raw vertices"))
                        section_data.strip_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "strip indices"))
                        section_data.visibility_mopp_code_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "visibility mopp code"))
                        section_data.mopp_reorder_table_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "mopp reorder table"))

                        section_data.vertex_buffers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "vertex buffers"))
                        input_stream.read(4) # Padding?
                        section_data.raw_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "raw points"))
                        section_data.runtime_point_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "runtime point data"))
                        section_data.rigid_point_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "rigid point groups"))
                        section_data.vertex_point_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "vertex point indices"))
                        section_data.node_map_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "node map"))

                        input_stream.read(4) # Padding?
                        section_data.raw_planes_tag_block = TAG.TagBlock()
                        section_data.runtime_plane_tag_data = TAG.RawData()
                        section_data.rigid_plane_groups_tag_block = TAG.TagBlock()
                        section_data.explicit_edges_tag_block = TAG.TagBlock()
                        section_data.forward_shared_edges_tag_block = TAG.TagBlock()
                        section_data.forward_shared_edge_groups_tag_block = TAG.TagBlock()
                        section_data.backward_shared_edges_tag_block = TAG.TagBlock()
                        section_data.backward_shared_edge_groups_tag_block = TAG.TagBlock()
                        section_data.dsq_raw_vertices_tag_block = TAG.TagBlock()
                        section_data.dsq_strip_indices_tag_block = TAG.TagBlock()
                        section_data.dsq_silhouette_quads_tag_block = TAG.TagBlock()
                    else:
                        print(input_stream.name)
                        print("Unknown Render Model Version: ", section.section_data_header.version)

                    section.section_data.append(section_data)

                for section_data_idx, section_data in enumerate(section.section_data):
                    section_data_element_node = None
                    if XML_OUTPUT:
                        section_data_element_node = section_data_node.childNodes[section_data_idx]

                    section_data.parts = []
                    section_data.subparts = []
                    section_data.visibility_bounds = []
                    section_data.raw_vertices = []
                    section_data.strip_indices = []
                    section_data.mopp_reorder_table = []
                    section_data.vertex_buffers = []
                    section_data.raw_points = []
                    section_data.rigid_point_groups = []
                    section_data.vertex_point_indices = []
                    section_data.node_map = []

                    section_data.sect_header = TAG.TagBlockHeader().read(input_stream, TAG)
                    if section.section_data_header.size == 524:
                        read_raw_vertices(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        read_vertex_buffers(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        read_strip_indices(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        read_parts_v0(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        section_data.pdat_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        read_raw_points(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        section_data.runtime_point_data = input_stream.read(section_data.runtime_point_tag_data.size)
                        read_rigid_point_groups(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        read_vertex_point_indices(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        read_section_node_map(RENDER, section_data, TAG, input_stream, section_data_element_node)

                    else:
                        read_parts_retail(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        read_subparts(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        read_visibility_bounds(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        read_raw_vertices(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        read_strip_indices(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        section_data.visibility_mopp_code = input_stream.read(section_data.visibility_mopp_code_data.size)
                        read_mopp_reorder_table(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        read_vertex_buffers(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        section_data.pdat_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        read_raw_points(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        section_data.runtime_point_data = input_stream.read(section_data.runtime_point_tag_data.size)
                        read_rigid_point_groups(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        read_vertex_point_indices(RENDER, section_data, TAG, input_stream, section_data_element_node)
                        read_section_node_map(RENDER, section_data, TAG, input_stream, section_data_element_node)

                    if section.section_data_header.version == 0:
                        isqi_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        if section_data.raw_planes_tag_block.count > 0:
                            raw_planes_header = TAG.TagBlockHeader().read(input_stream, TAG)
                            for raw_plane_idx in range(section_data.raw_planes_tag_block.count):
                                input_stream.read(raw_planes_header.size)

                        input_stream.read(section_data.runtime_plane_tag_data.size)

                        if section_data.rigid_plane_groups_tag_block.count > 0:
                            rigid_plane_groups_header = TAG.TagBlockHeader().read(input_stream, TAG)
                            for rigid_plane_group_idx in range(section_data.rigid_plane_groups_tag_block.count):
                                input_stream.read(rigid_plane_groups_header.size)

                        if section_data.explicit_edges_tag_block.count > 0:
                            explicit_edges_header = TAG.TagBlockHeader().read(input_stream, TAG)
                            for explicit_edge_idx in range(section_data.explicit_edges_tag_block.count):
                                input_stream.read(explicit_edges_header.size)

                        if section_data.forward_shared_edges_tag_block.count > 0:
                            forward_shared_edges_header = TAG.TagBlockHeader().read(input_stream, TAG)
                            for forward_shared_edge_idx in range(section_data.forward_shared_edges_tag_block.count):
                                input_stream.read(forward_shared_edges_header.size)

                        if section_data.forward_shared_edge_groups_tag_block.count > 0:
                            forward_shared_edge_groups_header = TAG.TagBlockHeader().read(input_stream, TAG)
                            for forward_shared_edge_group_idx in range(section_data.forward_shared_edge_groups_tag_block.count):
                                input_stream.read(forward_shared_edge_groups_header.size)

                        if section_data.backward_shared_edges_tag_block.count > 0:
                            backward_shared_edges_header = TAG.TagBlockHeader().read(input_stream, TAG)
                            for backward_shared_edge_idx in range(section_data.backward_shared_edges_tag_block.count):
                                input_stream.read(backward_shared_edges_header.size)

                        if section_data.backward_shared_edge_groups_tag_block.count > 0:
                            backward_shared_edge_groups_header = TAG.TagBlockHeader().read(input_stream, TAG)
                            for backward_shared_edge_group_idx in range(section_data.backward_shared_edge_groups_tag_block.count):
                                input_stream.read(backward_shared_edge_groups_header.size)

                        if section_data.dsq_raw_vertices_tag_block.count > 0:
                            dsq_raw_vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                            for dsq_raw_vertex_idx in range(section_data.dsq_raw_vertices_tag_block.count):
                                input_stream.read(dsq_raw_vertices_header.size)

                        if section_data.dsq_strip_indices_tag_block.count > 0:
                            dsq_strip_indices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                            for dsq_strip_idx in range(section_data.dsq_strip_indices_tag_block.count):
                                input_stream.read(dsq_strip_indices_header.size)

                        if section_data.dsq_silhouette_quads_tag_block.count > 0:
                            dsq_silhouette_quads_header = TAG.TagBlockHeader().read(input_stream, TAG)
                            for dsq_silhouette_quad_idx in range(section_data.dsq_silhouette_quads_tag_block.count):
                                input_stream.read(dsq_silhouette_quads_header.size)

            section.blok_header = TAG.TagBlockHeader().read(input_stream, TAG)

            if section.resources_tag_block.count > 0:
                resources_node = tag_format.get_xml_node(XML_OUTPUT, section.resources_tag_block.count, section_element_node, "name", "resources")
                section.resources_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for resource_idx in range(section.resources_tag_block.count):
                    resource_element_node = None
                    if XML_OUTPUT:
                        resource_element_node = TAG.xml_doc.createElement('element')
                        resource_element_node.setAttribute('index', str(resource_idx))
                        resources_node.appendChild(resource_element_node)

                    resource = RENDER.Resource()
                    resource.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "type", ResourceEnum))
                    input_stream.read(2) # Padding?
                    resource.primary_locator = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "primary locator"))
                    resource.secondary_locator = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "secondary locator"))
                    resource.resource_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource data size"))
                    resource.resource_data_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource data offset"))

                    section.resources.append(resource)

def read_sections_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.sections_tag_block.count > 0:
        sections_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.sections_tag_block.count, tag_node, "name", "sections")
        RENDER.section_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for section_idx in range(RENDER.render_body.sections_tag_block.count):
            section_element_node = None
            if XML_OUTPUT:
                section_element_node = TAG.xml_doc.createElement('element')
                section_element_node.setAttribute('index', str(section_idx))
                sections_node.appendChild(section_element_node)

            section = RENDER.Section()
            section.global_geometry_classification = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(section_element_node, "global geometry classification", GeometryClassificationEnum))
            input_stream.read(2) # Padding?
            section.total_vertex_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "total vertex count"))
            section.total_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "total triangle count"))
            section.total_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "total part count"))
            section.shadow_casting_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "shadow casting triangle count"))
            section.shadow_casting_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "shadow casting part count"))
            section.opaque_point_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "opaque point count"))
            section.opaque_vertex_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "opaque vertex count"))
            section.opaque_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "opaque part count"))
            section.opaque_max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(section_element_node, "opaque max nodes vertex"))
            section.transparent_max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(section_element_node, "transparent max nodes vertex"))
            section.shadow_casting_rigid_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "shadow casting rigid triangle count"))
            section.geometry_classification = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(section_element_node, "geometry classification", GeometryClassificationEnum))
            section.geometry_compression_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(section_element_node, "geometry compression flags", GeometryCompressionFlags))
            section.compression_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_element_node, "compression info"))
            section.hardware_node_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(section_element_node, "hardware node count"))
            section.node_map_size = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(section_element_node, "node map size"))
            section.software_plane_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "software plane count"))
            section.total_subpart_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "total subpart count"))
            section.section_lighting_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(section_element_node, "section lighting flags", SectionLightingFlags))
            section.rigid_node = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "rigid node", None, RENDER.render_body.nodes_tag_block.count, "nodes"))
            section.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(section_element_node, "flags", SectionFlags))
            section.section_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_element_node, "section data"))
            section.block_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(section_element_node, "block offset"))
            section.block_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(section_element_node, "block size"))
            section.section_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(section_element_node, "section data size"))
            section.resource_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(section_element_node, "resource data size"))
            section.resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_element_node, "resources"))
            input_stream.read(4) # Padding?
            section.owner_tag_section_offset = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(section_element_node, "owner tag section offset"))
            input_stream.read(6) # Padding?

            RENDER.sections.append(section)

        for section_idx, section in enumerate(RENDER.sections):
            section_element_node = None
            if XML_OUTPUT:
                section_element_node = sections_node.childNodes[section_idx]

            section.compression_info = []
            section.section_data = []
            section.resources = []

            section.sinf_header = TAG.TagBlockHeader().read(input_stream, TAG)
            if section.compression_info_tag_block.count > 0:
                compression_info_node = tag_format.get_xml_node(XML_OUTPUT, section.compression_info_tag_block.count, section_element_node, "name", "compression info")
                section.compression_info_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for compression_info_idx in range(section.compression_info_tag_block.count):
                    compression_info_element_node = None
                    if XML_OUTPUT:
                        compression_info_element_node = TAG.xml_doc.createElement('element')
                        compression_info_element_node.setAttribute('index', str(compression_info_idx))
                        compression_info_node.appendChild(compression_info_element_node)

                    compression_info = RENDER.CompressionInfo()
                    compression_info.position_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds x"))
                    compression_info.position_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds y"))
                    compression_info.position_bounds_z = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds z"))
                    compression_info.texcoord_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "texcoord bounds x"))
                    compression_info.texcoord_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "texcoord bounds y"))
                    compression_info.secondary_texcoord_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "secondary texcoord bounds x"))
                    compression_info.secondary_texcoord_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "secondary texcoord bounds y"))

                    section.compression_info.append(compression_info)

            if section.section_data_tag_block.count > 0:
                section_data_node = tag_format.get_xml_node(XML_OUTPUT, section.section_data_tag_block.count, section_element_node, "name", "section data")
                section.section_data_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for section_data_idx in range(section.section_data_tag_block.count):
                    section_data_element_node = None
                    if XML_OUTPUT:
                        section_data_element_node = TAG.xml_doc.createElement('element')
                        section_data_element_node.setAttribute('index', str(section_data_idx))
                        section_data_node.appendChild(section_data_element_node)

                    section_data = RENDER.SectionData()
                    section_data.parts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "parts"))
                    section_data.subparts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "subparts"))
                    section_data.visibility_bounds_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "visibility bounds"))
                    section_data.raw_vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "raw vertices"))
                    section_data.strip_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "strip indices"))
                    section_data.visibility_mopp_code_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "visibility mopp code"))
                    section_data.mopp_reorder_table_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "mopp reorder table"))
                    section_data.vertex_buffers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "vertex buffers"))
                    input_stream.read(4) # Padding?
                    section_data.raw_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "raw points"))
                    section_data.runtime_point_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "runtime point data"))
                    section_data.rigid_point_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "rigid point groups"))
                    section_data.vertex_point_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "vertex point indices"))
                    section_data.node_map_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_data_element_node, "node map"))
                    input_stream.read(4) # Padding?

                    section.section_data.append(section_data)

                for section_data_idx, section_data in enumerate(section.section_data):
                    section_data_element_node = None
                    if XML_OUTPUT:
                        section_data_element_node = section_data_node.childNodes[section_data_idx]

                    section_data.parts = []
                    section_data.subparts = []
                    section_data.visibility_bounds = []
                    section_data.raw_vertices = []
                    section_data.strip_indices = []
                    section_data.mopp_reorder_table = []
                    section_data.vertex_buffers = []
                    section_data.raw_points = []
                    section_data.rigid_point_groups = []
                    section_data.vertex_point_indices = []
                    section_data.node_map = []

                    section_data.sect_header = TAG.TagBlockHeader().read(input_stream, TAG)
                    read_parts_retail(RENDER, section_data, TAG, input_stream, section_data_element_node)
                    read_subparts(RENDER, section_data, TAG, input_stream, section_data_element_node)
                    read_visibility_bounds(RENDER, section_data, TAG, input_stream, section_data_element_node)
                    read_raw_vertices(RENDER, section_data, TAG, input_stream, section_data_element_node)
                    read_strip_indices(RENDER, section_data, TAG, input_stream, section_data_element_node)
                    section_data.visibility_mopp_code = input_stream.read(section_data.visibility_mopp_code_data.size)
                    read_mopp_reorder_table(RENDER, section_data, TAG, input_stream, section_data_element_node)
                    read_vertex_buffers(RENDER, section_data, TAG, input_stream, section_data_element_node)
                    section_data.pdat_header = TAG.TagBlockHeader().read(input_stream, TAG)
                    read_raw_points(RENDER, section_data, TAG, input_stream, section_data_element_node)
                    section_data.runtime_point_data = input_stream.read(section_data.runtime_point_tag_data.size)
                    read_rigid_point_groups(RENDER, section_data, TAG, input_stream, section_data_element_node)
                    read_vertex_point_indices(RENDER, section_data, TAG, input_stream, section_data_element_node)
                    read_section_node_map(RENDER, section_data, TAG, input_stream, section_data_element_node)

            section.blok_header = TAG.TagBlockHeader().read(input_stream, TAG)

            if section.resources_tag_block.count > 0:
                resources_node = tag_format.get_xml_node(XML_OUTPUT, section.resources_tag_block.count, section_element_node, "name", "resources")
                section.resources_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for resource_idx in range(section.resources_tag_block.count):
                    resource_element_node = None
                    if XML_OUTPUT:
                        resource_element_node = TAG.xml_doc.createElement('element')
                        resource_element_node.setAttribute('index', str(resource_idx))
                        resources_node.appendChild(resource_element_node)

                    resource = RENDER.Resource()
                    resource.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "type", ResourceEnum))
                    input_stream.read(2) # Padding?
                    resource.primary_locator = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "primary locator"))
                    resource.secondary_locator = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "secondary locator"))
                    resource.resource_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource data size"))
                    resource.resource_data_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource data offset"))

                    section.resources.append(resource)

def read_invalid_section_pair_bits(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.invalid_section_pair_bits_tag_block.count > 0:
        invalid_section_pair_bits_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.invalid_section_pair_bits_tag_block.count, tag_node, "name", "invalid section pair bits")
        RENDER.invalid_section_pair_bits_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for invalid_section_pair_bit_idx in range(RENDER.render_body.invalid_section_pair_bits_tag_block.count):
            invalid_section_pair_bit_element_node = None
            if XML_OUTPUT:
                invalid_section_pair_bit_element_node = TAG.xml_doc.createElement('element')
                invalid_section_pair_bit_element_node.setAttribute('index', str(invalid_section_pair_bit_idx))
                invalid_section_pair_bits_node.appendChild(invalid_section_pair_bit_element_node)

            RENDER.invalid_section_pair_bits.append(TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(invalid_section_pair_bit_element_node, "bits")))

def read_section_groups(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.section_groups_tag_block.count > 0:
        section_groups_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.section_groups_tag_block.count, tag_node, "name", "section groups")
        RENDER.section_groups_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for section_group_idx in range(RENDER.render_body.section_groups_tag_block.count):
            section_group_element_node = None
            if XML_OUTPUT:
                section_group_element_node = TAG.xml_doc.createElement('element')
                section_group_element_node.setAttribute('index', str(section_group_idx))
                section_groups_node.appendChild(section_group_element_node)

            section_group = RENDER.SectionGroup()
            section_group.detail_levels = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(section_group_element_node, "detail levels", DetailLevelsFlags))
            input_stream.read(2) # Padding?
            section_group.compound_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(section_group_element_node, "compound nodes"))

            RENDER.section_groups.append(section_group)

        for section_group_idx, section_group in enumerate(RENDER.section_groups):
            section_group_element_node = None
            if XML_OUTPUT:
                section_group_element_node = section_groups_node.childNodes[section_group_idx]

            section_group.compound_nodes = []
            if section_group.compound_nodes_tag_block.count > 0:
                compound_nodes_node = tag_format.get_xml_node(XML_OUTPUT, section_group.compound_nodes_tag_block.count, section_group_element_node, "name", "compound nodes")
                section_group.compound_nodes_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for compound_node_idx in range(section_group.compound_nodes_tag_block.count):
                    compound_node_element_node = None
                    if XML_OUTPUT:
                        compound_node_element_node = TAG.xml_doc.createElement('element')
                        compound_node_element_node.setAttribute('index', str(compound_node_idx))
                        compound_nodes_node.appendChild(compound_node_element_node)

                    compound_node = RENDER.CompoundNode()

                    compound_node.node_0_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(compound_node_element_node, "node index"))
                    compound_node.node_1_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(compound_node_element_node, "node index"))
                    compound_node.node_2_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(compound_node_element_node, "node index"))
                    compound_node.node_3_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(compound_node_element_node, "node index"))
                    compound_node.node_0_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(compound_node_element_node, "node weight"))
                    compound_node.node_1_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(compound_node_element_node, "node weight"))
                    compound_node.node_2_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(compound_node_element_node, "node weight"))

                    section_group.compound_nodes.append(compound_node)

def read_nodes_v0(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.nodes_tag_block.count > 0:
        nodes_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.nodes_tag_block.count, tag_node, "name", "nodes")
        RENDER.nodes_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for node_idx in range(RENDER.render_body.nodes_tag_block.count):
            node_element_node = None
            if XML_OUTPUT:
                node_element_node = TAG.xml_doc.createElement('element')
                node_element_node.setAttribute('index', str(node_idx))
                nodes_node.appendChild(node_element_node)

            node = RENDER.Node()
            node_transform = RENDER.Transform()

            node.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element_node, "name"))
            node.name_length = len(node.name)
            node.parent = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "parent node", None, RENDER.render_body.nodes_tag_block.count, "nodes"))
            node.child = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "child node", None, RENDER.render_body.nodes_tag_block.count, "nodes"))
            node.sibling = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "sibling node", None, RENDER.render_body.nodes_tag_block.count, "nodes"))
            node.import_node_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "import node index"))
            node_transform.translation = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element_node, "default translation"), True)
            node_transform.rotation = TAG.read_quaternion(input_stream, TAG,  tag_format.XMLData(node_element_node, "default rotation"), True)
            node_transform.inverse_forward = TAG.read_vector(input_stream, TAG, tag_format.XMLData(node_element_node, "inverse forward"))
            node_transform.inverse_left = TAG.read_vector(input_stream, TAG, tag_format.XMLData(node_element_node, "inverse left"))
            node_transform.inverse_up = TAG.read_vector(input_stream, TAG, tag_format.XMLData(node_element_node, "inverse up"))
            node_transform.inverse_position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element_node, "inverse position"), True)
            node_transform.inverse_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element_node, "inverse scale"))
            node.distance_from_parent = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element_node, "distance from parent"))

            RENDER.nodes.append(node)
            RENDER.transforms.append(node_transform)

def read_nodes_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.nodes_tag_block.count > 0:
        nodes_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.nodes_tag_block.count, tag_node, "name", "nodes")
        RENDER.nodes_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for node_idx in range(RENDER.render_body.nodes_tag_block.count):
            node_element_node = None
            if XML_OUTPUT:
                node_element_node = TAG.xml_doc.createElement('element')
                node_element_node.setAttribute('index', str(node_idx))
                nodes_node.appendChild(node_element_node)

            node = RENDER.Node()
            node_transform = RENDER.Transform()

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            node.name_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            node.parent = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "parent node", None, RENDER.render_body.nodes_tag_block.count, "nodes"))
            node.child = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "child node", None, RENDER.render_body.nodes_tag_block.count, "nodes"))
            node.sibling = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "sibling node", None, RENDER.render_body.nodes_tag_block.count, "nodes"))
            node.import_node_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "import node index"))
            node_transform.translation = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element_node, "default translation"), True)
            node_transform.rotation = TAG.read_quaternion(input_stream, TAG,  tag_format.XMLData(node_element_node, "default rotation"), True)
            node_transform.inverse_forward = TAG.read_vector(input_stream, TAG, tag_format.XMLData(node_element_node, "inverse forward"))
            node_transform.inverse_left = TAG.read_vector(input_stream, TAG, tag_format.XMLData(node_element_node, "inverse left"))
            node_transform.inverse_up = TAG.read_vector(input_stream, TAG, tag_format.XMLData(node_element_node, "inverse up"))
            node_transform.inverse_position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element_node, "inverse position"), True)
            node_transform.inverse_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element_node, "inverse scale"))
            node.distance_from_parent = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element_node, "distance from parent"))

            RENDER.nodes.append(node)
            RENDER.transforms.append(node_transform)

        for node_idx, node in enumerate(RENDER.nodes):
            node_element_node = None
            if XML_OUTPUT:
                node_element_node = nodes_node.childNodes[node_idx]

            if node.name_length > 0:
                node.name = TAG.read_variable_string_no_terminator(input_stream, node.name_length, TAG, tag_format.XMLData(node_element_node, "name"))

def read_node_map(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.node_map_tag_block.count > 0:
        node_map_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.node_map_tag_block.count, tag_node, "name", "node map")
        RENDER.node_map_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for node_map_idx in range(RENDER.render_body.node_map_tag_block.count):
            node_map_element_node = None
            if XML_OUTPUT:
                node_map_element_node = TAG.xml_doc.createElement('element')
                node_map_element_node.setAttribute('index', str(node_map_idx))
                node_map_node.appendChild(node_map_element_node)

            RENDER.node_map.append(TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_map_element_node, "node index")))

def read_marker_groups_v0(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.marker_groups_tag_block.count > 0:
        marker_groups_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.marker_groups_tag_block.count, tag_node, "name", "marker groups")
        RENDER.marker_group_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for marker_group_idx in range(RENDER.render_body.marker_groups_tag_block.count):
            marker_group_element_node = None
            if XML_OUTPUT:
                marker_group_element_node = TAG.xml_doc.createElement('element')
                marker_group_element_node.setAttribute('index', str(marker_group_idx))
                marker_groups_node.appendChild(marker_group_element_node)

            marker_group = RENDER.MarkerGroup()

            marker_group.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(marker_group_element_node, "name"))
            marker_group.name_length = len(marker_group.name)
            marker_group.markers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(marker_group_element_node, "markers"))

            RENDER.marker_groups.append(marker_group)

        for marker_group_idx, marker_group in enumerate(RENDER.marker_groups):
            marker_group_element_node = None
            if XML_OUTPUT:
                marker_group_element_node = marker_groups_node.childNodes[marker_group_idx]

            marker_group.markers = []
            if marker_group.markers_tag_block.count > 0:
                markers_node = tag_format.get_xml_node(XML_OUTPUT, marker_group.markers_tag_block.count, marker_group_element_node, "name", "markers")
                marker_group.markers_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for marker_idx in range(marker_group.markers_tag_block.count):
                    marker_element_node = None
                    if XML_OUTPUT:
                        marker_element_node = TAG.xml_doc.createElement('element')
                        marker_element_node.setAttribute('index', str(marker_idx))
                        markers_node.appendChild(marker_element_node)

                    marker = RENDER.Marker()

                    marker.region_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(marker_element_node, "region index"))
                    marker.permutation_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(marker_element_node, "permutation index"))
                    marker.node_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(marker_element_node, "node index"))
                    input_stream.read(1) # Padding?
                    marker.translation = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(marker_element_node, "translation"), True)
                    marker.rotation = TAG.read_quaternion(input_stream, TAG,  tag_format.XMLData(marker_element_node, "rotation"), True)
                    marker.scale = TAG.read_float(input_stream, TAG,  tag_format.XMLData(marker_element_node, "scale"))

                    marker_group.markers.append(marker)

def read_marker_groups_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.marker_groups_tag_block.count > 0:
        marker_groups_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.marker_groups_tag_block.count, tag_node, "name", "marker groups")
        RENDER.marker_group_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for marker_group_idx in range(RENDER.render_body.marker_groups_tag_block.count):
            marker_group_element_node = None
            if XML_OUTPUT:
                marker_group_element_node = TAG.xml_doc.createElement('element')
                marker_group_element_node.setAttribute('index', str(marker_group_idx))
                marker_groups_node.appendChild(marker_group_element_node)

            marker_group = RENDER.MarkerGroup()

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            marker_group.name_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            marker_group.markers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(marker_group_element_node, "markers"))

            RENDER.marker_groups.append(marker_group)

        for marker_group_idx, marker_group in enumerate(RENDER.marker_groups):
            marker_group_element_node = None
            if XML_OUTPUT:
                marker_group_element_node = marker_groups_node.childNodes[marker_group_idx]

            if marker_group.name_length > 0:
                marker_group.name = TAG.read_variable_string_no_terminator(input_stream, marker_group.name_length, TAG, tag_format.XMLData(marker_group_element_node, "name"))

            marker_group.markers = []
            if marker_group.markers_tag_block.count > 0:
                markers_node = tag_format.get_xml_node(XML_OUTPUT, marker_group.markers_tag_block.count, marker_group_element_node, "name", "markers")
                marker_group.markers_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for marker_idx in range(marker_group.markers_tag_block.count):
                    marker_element_node = None
                    if XML_OUTPUT:
                        marker_element_node = TAG.xml_doc.createElement('element')
                        marker_element_node.setAttribute('index', str(marker_idx))
                        markers_node.appendChild(marker_element_node)

                    marker = RENDER.Marker()

                    marker.region_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(marker_element_node, "region index"))
                    marker.permutation_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(marker_element_node, "permutation index"))
                    marker.node_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(marker_element_node, "node index"))
                    input_stream.read(1) # Padding?
                    marker.translation = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(marker_element_node, "translation"), True)
                    marker.rotation = TAG.read_quaternion(input_stream, TAG,  tag_format.XMLData(marker_element_node, "rotation"), True)
                    marker.scale = TAG.read_float(input_stream, TAG,  tag_format.XMLData(marker_element_node, "scale"))

                    marker_group.markers.append(marker)

def read_materials(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.materials_tag_block.count > 0:
        material_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.materials_tag_block.count, tag_node, "name", "materials")
        RENDER.material_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for material_idx in range(RENDER.render_body.materials_tag_block.count):
            material_element_node = None
            if XML_OUTPUT:
                material_element_node = TAG.xml_doc.createElement('element')
                material_element_node.setAttribute('index', str(material_idx))
                material_node.appendChild(material_element_node)

            material = RENDER.Material()
            material.old_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(material_element_node, "old shader"))
            material.shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(material_element_node, "shader"))
            material.properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(material_element_node, "properties"))
            input_stream.read(4) # Padding?
            material.breakable_surface_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(material_element_node, "breakable surface index"))
            input_stream.read(3) # Padding?

            RENDER.materials.append(material)

        for material_idx, material in enumerate(RENDER.materials):
            material_element_node = None
            if XML_OUTPUT:
                material_element_node = material_node.childNodes[material_idx]

            if material.old_shader.name_length > 0:
                material.old_shader.name = TAG.read_variable_string(input_stream, material.old_shader.name_length, TAG)

            if material.shader.name_length > 0:
                material.shader.name = TAG.read_variable_string(input_stream, material.shader.name_length, TAG)

            if XML_OUTPUT:
                old_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, material_element_node, "name", "old shader")
                shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, material_element_node, "name", "shader")
                material.old_shader.append_xml_attributes(old_shader_node)
                material.shader.append_xml_attributes(shader_node)

            material.properties = []
            if material.properties_tag_block.count > 0:
                property_node = tag_format.get_xml_node(XML_OUTPUT, material.properties_tag_block.count, material_element_node, "name", "properties")
                material.properties_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for property_idx in range(material.properties_tag_block.count):
                    property_element_node = None
                    if XML_OUTPUT:
                        property_element_node = TAG.xml_doc.createElement('element')
                        property_element_node.setAttribute('index', str(property_idx))
                        property_node.appendChild(property_element_node)

                    property = RENDER.Property()
                    property.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(property_element_node, "type", PropertyTypeEnum))
                    property.int_value = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(property_element_node, "int value"))
                    property.real_value = TAG.read_float(input_stream, TAG, tag_format.XMLData(property_element_node, "real value"))

                    material.properties.append(property)

def read_errors(RENDER, TAG, input_stream, tag_node, XML_OUTPUT):
    if RENDER.render_body.errors_tag_block.count > 0:
        errors_node = tag_format.get_xml_node(XML_OUTPUT, RENDER.render_body.errors_tag_block.count, tag_node, "name", "errors")
        RENDER.errors_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for error_idx in range(RENDER.render_body.errors_tag_block.count):
            error_element_node = None
            if XML_OUTPUT:
                error_element_node = TAG.xml_doc.createElement('element')
                error_element_node.setAttribute('index', str(error_idx))
                errors_node.appendChild(error_element_node)

            error = RENDER.Error()
            error.name = TAG.read_string256(input_stream, TAG, tag_format.XMLData(error_element_node, "name"))
            error.report_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(error_element_node, "report type", ReportTypeEnum))
            error.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(error_element_node, "flags", ReportFlags))
            input_stream.read(408) # Padding?
            error.reports_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(error_element_node, "reports"))

            RENDER.errors.append(error)

        for error_idx, error in enumerate(RENDER.errors):
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

                    report = RENDER.Report()
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

                            vertex = RENDER.ReportVertex()
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

                            vector = RENDER.ReportVector()
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

                            line = RENDER.ReportLine()
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

                            triangle = RENDER.ReportTriangle()
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

                            quad = RENDER.ReportQuad()
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

                            comment = RENDER.ReportComment()
                            comment.text_length = TAG.read_signed_short(input_stream, TAG)
                            input_stream.read(18) # Padding?
                            comment.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(vector_element_node, "position"))
                            comment.node_index_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(vector_element_node, "node index"))
                            comment.node_index_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(vector_element_node, "node index"))
                            comment.node_index_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(vector_element_node, "node index"))
                            comment.node_index_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(vector_element_node, "node index"))
                            comment.node_weight_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(vector_element_node, "node weight"))
                            comment.node_weight_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(vector_element_node, "node weight"))
                            comment.node_weight_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(vector_element_node, "node weight"))
                            comment.node_weight_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(vector_element_node, "node weight"))
                            comment.color = TAG.read_argb(input_stream, TAG, tag_format.XMLData(vector_element_node, "color"))

                            report.comments.append(comment)

                        for comment_idx, comment in enumerate(report.comments):
                            comment_element_node = None
                            if XML_OUTPUT:
                                comment_element_node = comments_node.childNodes[comment_idx]

                            if comment.text_length > 0:
                                comment.text = TAG.read_variable_string_no_terminator(input_stream, comment.text_length, TAG, tag_format.XMLData(comment_element_node, "text"))

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    RENDER = RenderAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    RENDER.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_render(RENDER)
    if RENDER.header.engine_tag == "BMAL":
        read_render_body_v0(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_import_info(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_compression_info(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_regions_v0(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_sections_v0(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_invalid_section_pair_bits(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_section_groups(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_nodes_v0(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_node_map(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_marker_groups_v0(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_materials(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_errors(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)

    elif RENDER.header.engine_tag == "BALM":
        read_render_body_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)

        if RENDER.render_body.name_length > 0:
            RENDER.render_body.name = TAG.read_variable_string_no_terminator(input_stream, RENDER.render_body.name_length, TAG, tag_format.XMLData(tag_node, "name"))

        read_import_info(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_compression_info(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_regions_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_sections_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_invalid_section_pair_bits(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_section_groups(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_nodes_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_node_map(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_marker_groups_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_materials(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_errors(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)

    elif RENDER.header.engine_tag == "!MLB":
        read_render_body_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)

        if RENDER.render_body.name_length > 0:
            RENDER.render_body.name = TAG.read_variable_string_no_terminator(input_stream, RENDER.render_body.name_length, TAG, tag_format.XMLData(tag_node, "name"))

        read_import_info(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_compression_info(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_regions_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_sections_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_invalid_section_pair_bits(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_section_groups(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_nodes_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_node_map(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_marker_groups_retail(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_materials(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)
        read_errors(RENDER, TAG, input_stream, tag_node, XML_OUTPUT)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, RENDER.header.tag_group, TAG.is_legacy, True)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return RENDER
