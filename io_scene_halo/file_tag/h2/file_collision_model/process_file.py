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
from .format import CollisionAsset, CollisionFlags, ReportTypeEnum, ReportFlags, LeafFlags, SurfaceFlags, PathfindingSphereFlags
from ....global_functions import tag_format

XML_OUTPUT = False

def initilize_collision(COLLISION):
    COLLISION.import_info = []
    COLLISION.errors = []
    COLLISION.materials = []
    COLLISION.regions = []
    COLLISION.pathfinding_spheres = []
    COLLISION.nodes = []

def read_collision_body(COLLISION, TAG, input_stream, tag_node, XML_OUTPUT):
    COLLISION.collision_body_header = TAG.TagBlockHeader().read(input_stream, TAG)

    COLLISION.collision_body = COLLISION.CollisionBody()
    COLLISION.collision_body.import_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "import info"))
    COLLISION.collision_body.errors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "errors"))
    COLLISION.collision_body.flags = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", CollisionFlags))
    COLLISION.collision_body.materials_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "materials"))
    COLLISION.collision_body.regions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "regions"))
    COLLISION.collision_body.pathfinding_spheres_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "pathfinding spheres"))
    COLLISION.collision_body.nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "nodes"))

def read_import_info(COLLISION, TAG, input_stream, tag_node, XML_OUTPUT):
    if COLLISION.collision_body.import_info_tag_block.count > 0:
        import_info_node = tag_format.get_xml_node(XML_OUTPUT, COLLISION.collision_body.import_info_tag_block.count, tag_node, "name", "import info")
        COLLISION.import_info_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for import_info_idx in range(COLLISION.collision_body.import_info_tag_block.count):
            import_info_element_node = None
            if XML_OUTPUT:
                import_info_element_node = TAG.xml_doc.createElement('element')
                import_info_element_node.setAttribute('index', str(import_info_idx))
                import_info_node.appendChild(import_info_element_node)

            import_info = COLLISION.ImportInfo()
            import_info.build = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(import_info_element_node, "build"))
            import_info.version = TAG.read_string256(input_stream, TAG, tag_format.XMLData(import_info_element_node, "version"))
            import_info.import_date = TAG.read_string32(input_stream, TAG, tag_format.XMLData(import_info_element_node, "import date"))
            import_info.culprit = TAG.read_string32(input_stream, TAG, tag_format.XMLData(import_info_element_node, "culprit"))
            input_stream.read(96) # Padding?
            import_info.import_time = TAG.read_string32(input_stream, TAG, tag_format.XMLData(import_info_element_node, "import time"))
            input_stream.read(4) # Padding?
            import_info.files_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(import_info_element_node, "files"))
            input_stream.read(128) # Padding?

            COLLISION.import_info.append(import_info)

        for import_info_idx, import_info in enumerate(COLLISION.import_info):
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

                    file = COLLISION.File()
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

def read_errors(COLLISION, TAG, input_stream, tag_node, XML_OUTPUT):
    if COLLISION.collision_body.errors_tag_block.count > 0:
        errors_node = tag_format.get_xml_node(XML_OUTPUT, COLLISION.collision_body.errors_tag_block.count, tag_node, "name", "errors")
        COLLISION.errors_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for error_idx in range(COLLISION.collision_body.errors_tag_block.count):
            error_element_node = None
            if XML_OUTPUT:
                error_element_node = TAG.xml_doc.createElement('element')
                error_element_node.setAttribute('index', str(error_idx))
                errors_node.appendChild(error_element_node)

            error = COLLISION.Error()
            error.name = TAG.read_string256(input_stream, TAG, tag_format.XMLData(error_element_node, "name"))
            error.report_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(error_element_node, "report type", ReportTypeEnum))
            error.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(error_element_node, "flags", ReportFlags))
            input_stream.read(408) # Padding?
            error.reports_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(error_element_node, "reports"))

            COLLISION.errors.append(error)

        for error_idx, error in enumerate(COLLISION.errors):
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

                    report = COLLISION.Report()
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

                            vertex = COLLISION.ReportVertex()
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

                            vector = COLLISION.ReportVector()
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

                            line = COLLISION.ReportLine()
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

                            triangle = COLLISION.ReportTriangle()
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

                            quad = COLLISION.ReportQuad()
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

                            comment = COLLISION.ReportComment()
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

def read_materials(COLLISION, TAG, input_stream, tag_node, XML_OUTPUT):
    if COLLISION.collision_body.materials_tag_block.count > 0:
        materials_node = tag_format.get_xml_node(XML_OUTPUT, COLLISION.collision_body.materials_tag_block.count, tag_node, "name", "materials")
        COLLISION.materials_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for material_idx in range(COLLISION.collision_body.materials_tag_block.count):
            material_element_node = None
            if XML_OUTPUT:
                material_element_node = TAG.xml_doc.createElement('element')
                material_element_node.setAttribute('index', str(material_idx))
                materials_node.appendChild(material_element_node)

            material = COLLISION.Material()

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            material.name_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            COLLISION.materials.append(material)

        for material_idx, material in enumerate(COLLISION.materials):
            material_element_node = None
            if XML_OUTPUT:
                material_element_node = materials_node.childNodes[material_idx]

            if material.name_length > 0:
                material.name = TAG.read_variable_string_no_terminator(input_stream, material.name_length, TAG, tag_format.XMLData(material_element_node, "name"))

def read_regions(COLLISION, TAG, input_stream, tag_node, XML_OUTPUT):
    if COLLISION.collision_body.regions_tag_block.count > 0:
        regions_node = tag_format.get_xml_node(XML_OUTPUT, COLLISION.collision_body.regions_tag_block.count, tag_node, "name", "regions")
        COLLISION.materials_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for region_idx in range(COLLISION.collision_body.regions_tag_block.count):
            region_element_node = None
            if XML_OUTPUT:
                region_element_node = TAG.xml_doc.createElement('element')
                region_element_node.setAttribute('index', str(region_idx))
                regions_node.appendChild(region_element_node)

            region = COLLISION.Region()

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            region.name_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            region.permutations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(region_element_node, "permutations"))

            COLLISION.regions.append(region)

        for region_idx, region in enumerate(COLLISION.regions):
            region_element_node = None
            if XML_OUTPUT:
                region_element_node = regions_node.childNodes[region_idx]

            if region.name_length > 0:
                region.name = TAG.read_variable_string_no_terminator(input_stream, region.name_length, TAG, tag_format.XMLData(region_element_node, "name"))

            region.permutations = []
            if region.permutations_tag_block.count > 0:
                permutations_node = tag_format.get_xml_node(XML_OUTPUT, region.permutations_tag_block.count, region_element_node, "name", "permutations")
                region.permutations_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for permutation_idx in range(region.permutations_tag_block.count):
                    permutation_element_node = None
                    if XML_OUTPUT:
                        permutation_element_node = TAG.xml_doc.createElement('element')
                        permutation_element_node.setAttribute('index', str(permutation_idx))
                        permutations_node.appendChild(permutation_element_node)

                    permutation = COLLISION.Permutation()

                    TAG.big_endian = True
                    input_stream.read(2) # Padding?
                    permutation.name_length = TAG.read_signed_short(input_stream, TAG)
                    TAG.big_endian = False

                    permutation.bsps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(permutation_element_node, "bsps"))
                    permutation.bsp_physics_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(permutation_element_node, "bsp physics"))

                    region.permutations.append(permutation)

                for permutation_idx, permutation in enumerate(region.permutations):
                    permutation_element_node = None
                    if XML_OUTPUT:
                        permutation_element_node = permutations_node.childNodes[permutation_idx]

                    if region.name_length > 0:
                        permutation.name = TAG.read_variable_string_no_terminator(input_stream, permutation.name_length, TAG, tag_format.XMLData(permutation_element_node, "name"))

                    permutation.bsps = []
                    permutation.bsp_physics = []
                    if permutation.bsps_tag_block.count > 0:
                        collision_bsps_node = tag_format.get_xml_node(XML_OUTPUT, permutation.bsps_tag_block.count, permutation_element_node, "name", "bsps")
                        permutation.bsps_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for collision_bsp_idx in range(permutation.bsps_tag_block.count):
                            collision_bsp_element_node = None
                            if XML_OUTPUT:
                                collision_bsp_element_node = TAG.xml_doc.createElement('element')
                                collision_bsp_element_node.setAttribute('index', str(collision_bsp_idx))
                                collision_bsps_node.appendChild(collision_bsp_element_node)

                            collision_bsp = COLLISION.BSP()
                            collision_bsp.node_index = TAG.read_signed_short(input_stream, TAG)
                            input_stream.read(2) # Padding?
                            collision_bsp.bsp3d_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "bsp3d nodes"))
                            collision_bsp.planes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "planes"))
                            collision_bsp.leaves_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "leaves"))
                            collision_bsp.bsp2d_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "bsp2d references"))
                            collision_bsp.bsp2d_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "bsp2d nodes"))
                            collision_bsp.surfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "surfaces"))
                            collision_bsp.edges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "edges"))
                            collision_bsp.vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "vertices"))

                            permutation.bsps.append(collision_bsp)

                        for collision_bsp_idx, collision_bsp in enumerate(permutation.bsps):
                            collision_bsp_element_node = None
                            if XML_OUTPUT:
                                collision_bsp_element_node = collision_bsps_node.childNodes[collision_bsp_idx]

                            collision_bsp.cbsp_header = TAG.TagBlockHeader().read(input_stream, TAG)
                            collision_bsp.bsp3d_nodes = []
                            collision_bsp.planes = []
                            collision_bsp.leaves = []
                            collision_bsp.bsp2d_references = []
                            collision_bsp.bsp2d_nodes = []
                            collision_bsp.surfaces = []
                            collision_bsp.edges = []
                            collision_bsp.vertices = []
                            if collision_bsp.bsp3d_nodes_tag_block.count > 0:
                                collision_bsp.bsp3d_nodes_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                bsp3d_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.bsp3d_nodes_tag_block.count, collision_bsp_element_node, "name", "bsp3d nodes")
                                for bsp3d_node_idx in range(collision_bsp.bsp3d_nodes_tag_block.count):
                                    bsp3d_node_element_node = None
                                    if XML_OUTPUT:
                                        bsp3d_node_element_node = TAG.xml_doc.createElement('element')
                                        bsp3d_node_element_node.setAttribute('index', str(bsp3d_node_idx))
                                        bsp3d_node.appendChild(bsp3d_node_element_node)

                                    bsp3d = COLLISION.BSP3DNode()
                                    bsp3d.back_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp3d_node_element_node, "back child"))
                                    bsp3d.front_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp3d_node_element_node, "front child"))

                                    collision_bsp.bsp3d_nodes.append(bsp3d)

                            if collision_bsp.planes_tag_block.count > 0:
                                collision_bsp.planes_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                plane_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.planes_tag_block.count, collision_bsp_element_node, "name", "planes")
                                for plane_idx in range(collision_bsp.planes_tag_block.count):
                                    plane_element_node = None
                                    if XML_OUTPUT:
                                        plane_element_node = TAG.xml_doc.createElement('element')
                                        plane_element_node.setAttribute('index', str(plane_idx))
                                        plane_node.appendChild(plane_element_node)

                                    collision_bsp.planes.append(TAG.Plane3D().read(input_stream, TAG, tag_format.XMLData(plane_element_node, "plane")))

                            if collision_bsp.leaves_tag_block.count > 0:
                                collision_bsp.leaves_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                leaf_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.leaves_tag_block.count, collision_bsp_element_node, "name", "leaves")
                                for leaf_idx in range(collision_bsp.leaves_tag_block.count):
                                    leaf_element_node = None
                                    if XML_OUTPUT:
                                        leaf_element_node = TAG.xml_doc.createElement('element')
                                        leaf_element_node.setAttribute('index', str(leaf_idx))
                                        leaf_node.appendChild(leaf_element_node)

                                    leaf = COLLISION.Leaf()
                                    leaf.flags = TAG.read_flag_unsigned_byte(input_stream, TAG, tag_format.XMLData(leaf_element_node, "flags", LeafFlags))
                                    leaf.bsp2d_reference_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(leaf_element_node, "bsp2d reference count"))
                                    leaf.first_bsp2d_reference = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(leaf_element_node, "first bsp2d reference"))
                                    input_stream.read(1) # Padding?

                                    collision_bsp.leaves.append(leaf)

                            if collision_bsp.bsp2d_references_tag_block.count > 0:
                                collision_bsp.bsp2d_references_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                bsp2d_references_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.bsp2d_references_tag_block.count, collision_bsp_element_node, "name", "bsp2d references")
                                for bsp2d_reference_idx in range(collision_bsp.bsp2d_references_tag_block.count):
                                    bsp2d_reference_element_node = None
                                    if XML_OUTPUT:
                                        bsp2d_reference_element_node = TAG.xml_doc.createElement('element')
                                        bsp2d_reference_element_node.setAttribute('index', str(bsp2d_reference_idx))
                                        bsp2d_references_node.appendChild(bsp2d_reference_element_node)

                                    bsp2d_reference = COLLISION.BSP2DReference()
                                    bsp2d_reference.plane = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp2d_reference_element_node, "plane"))
                                    bsp2d_reference.bsp2d_node = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp2d_reference_element_node, "bsp2d node"))

                                    collision_bsp.bsp2d_references.append(bsp2d_reference)

                            if collision_bsp.bsp2d_nodes_tag_block.count > 0:
                                collision_bsp.bsp2d_nodes_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                bsp2d_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.bsp2d_nodes_tag_block.count, collision_bsp_element_node, "name", "bsp2d nodes")
                                for bsp2d_node_idx in range(collision_bsp.bsp2d_nodes_tag_block.count):
                                    bsp2d_node_element_node = None
                                    if XML_OUTPUT:
                                        bsp2d_node_element_node = TAG.xml_doc.createElement('element')
                                        bsp2d_node_element_node.setAttribute('index', str(bsp2d_node_idx))
                                        bsp2d_node.appendChild(bsp2d_node_element_node)

                                    bsp2d = COLLISION.BSP2DNode()
                                    bsp2d.plane = TAG.Plane2D().read(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "plane"))
                                    bsp2d.left_child = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "left child"))
                                    bsp2d.right_child = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "right child"))

                                    collision_bsp.bsp2d_nodes.append(bsp2d)

                            if collision_bsp.surfaces_tag_block.count > 0:
                                collision_bsp.surfaces_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                surfaces_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.surfaces_tag_block.count, collision_bsp_element_node, "name", "surfaces")
                                for surfaces_idx in range(collision_bsp.surfaces_tag_block.count):
                                    surface_element_node = None
                                    if XML_OUTPUT:
                                        surface_element_node = TAG.xml_doc.createElement('element')
                                        surface_element_node.setAttribute('index', str(surfaces_idx))
                                        surfaces_node.appendChild(surface_element_node)

                                    surface = COLLISION.Surface()
                                    surface.plane = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(surface_element_node, "plane"))
                                    surface.first_edge = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(surface_element_node, "first edge"))
                                    surface.flags = TAG.read_flag_unsigned_byte(input_stream, TAG, tag_format.XMLData(surface_element_node, "flags", SurfaceFlags))
                                    surface.breakable_surface = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(surface_element_node, "breakable surface"))
                                    surface.material = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(surface_element_node, "material"))
                                    input_stream.read(1) # Padding?

                                    collision_bsp.surfaces.append(surface)

                            if collision_bsp.edges_tag_block.count > 0:
                                collision_bsp.edges_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                edge_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.edges_tag_block.count, collision_bsp_element_node, "name", "edges")
                                for edge_idx in range(collision_bsp.edges_tag_block.count):
                                    edge_element_node = None
                                    if XML_OUTPUT:
                                        edge_element_node = TAG.xml_doc.createElement('element')
                                        edge_element_node.setAttribute('index', str(edge_idx))
                                        edge_node.appendChild(edge_element_node)

                                    edge = COLLISION.Edge()
                                    edge.start_vertex = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(edge_element_node, "start vertex"))
                                    edge.end_vertex = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(edge_element_node, "end vertex"))
                                    edge.forward_edge = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(edge_element_node, "forward edge"))
                                    edge.reverse_edge = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(edge_element_node, "reverse edge"))
                                    edge.left_surface = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(edge_element_node, "left surface"))
                                    edge.right_surface = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(edge_element_node, "right surface"))

                                    collision_bsp.edges.append(edge)

                            if collision_bsp.vertices_tag_block.count > 0:
                                collision_bsp.vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                vertex_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.vertices_tag_block.count, collision_bsp_element_node, "name", "vertices")
                                for vertex_idx in range(collision_bsp.vertices_tag_block.count):
                                    vertex_element_node = None
                                    if XML_OUTPUT:
                                        vertex_element_node = TAG.xml_doc.createElement('element')
                                        vertex_element_node.setAttribute('index', str(vertex_idx))
                                        vertex_node.appendChild(vertex_element_node)

                                    vertex = COLLISION.Vertex()
                                    vertex.translation = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(vertex_element_node, "translation"), True)
                                    vertex.first_edge = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(vertex_element_node, "first edge"))

                                    collision_bsp.vertices.append(vertex)

                    if permutation.bsp_physics_tag_block.count > 0:
                        bsp_physics_node = tag_format.get_xml_node(XML_OUTPUT, permutation.bsp_physics_tag_block.count, tag_node, "name", "bsps")
                        permutation.bsps_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for bsp_physics_idx in range(permutation.bsp_physics_tag_block.count):
                            bsp_physics_element_node = None
                            if XML_OUTPUT:
                                bsp_physics_element_node = TAG.xml_doc.createElement('element')
                                bsp_physics_element_node.setAttribute('index', str(bsp_physics_idx))
                                bsp_physics_node.appendChild(bsp_physics_element_node)

                            bsp_physics = COLLISION.BSPPhysics()
                            input_stream.read(4) # Padding?
                            bsp_physics.size_0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp_physics_element_node, "size"))
                            bsp_physics.count_0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp_physics_element_node, "count"))
                            input_stream.read(60) # Padding?
                            bsp_physics.size_1 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp_physics_element_node, "size"))
                            bsp_physics.count_1 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp_physics_element_node, "count"))
                            input_stream.read(12) # Padding?
                            bsp_physics.size_2 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp_physics_element_node, "size"))
                            bsp_physics.count_2 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp_physics_element_node, "count"))
                            input_stream.read(12) # Padding?
                            bsp_physics.mopp_code_data_ref = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(bsp_physics_element_node, "mopp code data"))
                            input_stream.read(8) # Padding?

                            permutation.bsp_physics.append(bsp_physics)

                        for bsp_physics in permutation.bsp_physics:
                            mopp_code_data_size = bsp_physics.mopp_code_data_ref.size
                            if mopp_code_data_size > 0:
                                bsp_physics.mopp_code_data = input_stream.read(mopp_code_data_size)

def read_pathfinding_spheres(COLLISION, TAG, input_stream, tag_node, XML_OUTPUT):
    if COLLISION.collision_body.pathfinding_spheres_tag_block.count > 0:
        pathfinding_spheres_node = tag_format.get_xml_node(XML_OUTPUT, COLLISION.collision_body.pathfinding_spheres_tag_block.count, tag_node, "name", "pathfinding spheres")
        COLLISION.pathfinding_spheres_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for pathfinding_sphere_idx in range(COLLISION.collision_body.pathfinding_spheres_tag_block.count):
            pathfinding_sphere_element_node = None
            if XML_OUTPUT:
                pathfinding_sphere_element_node = TAG.xml_doc.createElement('element')
                pathfinding_sphere_element_node.setAttribute('index', str(pathfinding_sphere_idx))
                pathfinding_spheres_node.appendChild(pathfinding_sphere_element_node)

            pathfinding_sphere = COLLISION.PathfindingSphere()
            pathfinding_sphere.node = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_sphere_element_node, "node", None, COLLISION.collision_body.nodes_tag_block.count, "nodes"))
            pathfinding_sphere.flags = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_sphere_element_node, "flags", PathfindingSphereFlags))
            pathfinding_sphere.center = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(pathfinding_sphere_element_node, "center"), True)
            pathfinding_sphere.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(pathfinding_sphere_element_node, "radius"), True)

            COLLISION.pathfinding_spheres.append(pathfinding_sphere)

def read_nodes(COLLISION, TAG, input_stream, tag_node, XML_OUTPUT):
    if COLLISION.collision_body.nodes_tag_block.count > 0:
        bone_node = tag_format.get_xml_node(XML_OUTPUT, COLLISION.collision_body.nodes_tag_block.count, tag_node, "name", "nodes")
        COLLISION.nodes_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for node_idx in range(COLLISION.collision_body.nodes_tag_block.count):
            node_element_node = None
            if XML_OUTPUT:
                node_element_node = TAG.xml_doc.createElement('element')
                node_element_node.setAttribute('index', str(node_idx))
                bone_node.appendChild(node_element_node)

            node = COLLISION.Node()

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            node.name_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            input_stream.read(2) # Padding?
            node.parent = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "parent node", None, COLLISION.collision_body.nodes_tag_block.count, "nodes"))
            node.child = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "child node", None, COLLISION.collision_body.nodes_tag_block.count, "nodes"))
            node.sibling = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "sibling node", None, COLLISION.collision_body.nodes_tag_block.count, "nodes"))

            COLLISION.nodes.append(node)

        for node_idx, node in enumerate(COLLISION.nodes):
            node_element_node = None
            if XML_OUTPUT:
                node_element_node = bone_node.childNodes[node_idx]

            if node.name_length > 0:
                node.name = TAG.read_variable_string_no_terminator(input_stream, node.name_length, TAG, tag_format.XMLData(node_element_node, "name"))

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    COLLISION = CollisionAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    COLLISION.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_collision(COLLISION)
    read_collision_body(COLLISION, TAG, input_stream, tag_node, XML_OUTPUT)
    read_import_info(COLLISION, TAG, input_stream, tag_node, XML_OUTPUT)
    read_errors(COLLISION, TAG, input_stream, tag_node, XML_OUTPUT)
    read_materials(COLLISION, TAG, input_stream, tag_node, XML_OUTPUT)
    read_regions(COLLISION, TAG, input_stream, tag_node, XML_OUTPUT)
    read_pathfinding_spheres(COLLISION, TAG, input_stream, tag_node, XML_OUTPUT)
    read_nodes(COLLISION, TAG, input_stream, tag_node, XML_OUTPUT)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    return COLLISION
