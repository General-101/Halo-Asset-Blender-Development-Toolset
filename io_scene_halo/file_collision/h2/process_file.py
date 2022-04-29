# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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

from math import degrees
from .format import CollisionAsset
from mathutils import Vector, Quaternion

DEBUG_PARSER = True
DEBUG_HEADER = True
DEBUG_BODY = True
DEBUG_IMPORT_INFO = True
DEBUG_FILES = True
DEBUG_ERRORS = True
DEBUG_REPORTS = True
DEBUG_REPORT_VERTICES = True
DEBUG_REPORT_VECTORS = True
DEBUG_REPORT_LINES = True
DEBUG_REPORT_TRIANGLES = True
DEBUG_REPORT_QUADS = True
DEBUG_REPORT_COMMENTS = True
DEBUG_MATERIALS = True
DEBUG_REGIONS = True
DEBUG_PERMUTATIONS = True
DEBUG_BSPS = True
DEBUG_BSP3D_NODES = True
DEBUG_PLANES = True
DEBUG_LEAVES = True
DEBUG_BSP2D_REFERENCES = True
DEBUG_BSP2D_NODES = True
DEBUG_SURFACES = True
DEBUG_EDGES = True
DEBUG_VERTICES = True
DEBUG_BSP_PHYSICS = True
DEBUG_PATHFINDING_SPHERES = True
DEBUG_NODES = True

def process_file(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    COLLISION = CollisionAsset()

    header_struct = struct.unpack('<hbb32s4sIIIIHbb4s', input_stream.read(64))
    COLLISION.header = TAG.Header()
    COLLISION.header.unk1 = header_struct[0]
    COLLISION.header.flags = header_struct[1]
    COLLISION.header.type = header_struct[2]
    COLLISION.header.name = header_struct[3].decode().rstrip('\x00')
    COLLISION.header.tag_group = header_struct[4].decode().rstrip('\x00')
    COLLISION.header.checksum = header_struct[5]
    COLLISION.header.data_offset = header_struct[6]
    COLLISION.header.data_length = header_struct[7]
    COLLISION.header.unk2 = header_struct[8]
    COLLISION.header.version = header_struct[9]
    COLLISION.header.destination = header_struct[10]
    COLLISION.header.plugin_handle = header_struct[11]
    COLLISION.header.engine_tag = header_struct[12].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_HEADER:
        print(" ===== Tag Header ===== ")
        print("Unknown Value: ", COLLISION.header.unk1)
        print("Flags: ", COLLISION.header.flags)
        print("Type: ", COLLISION.header.type)
        print("Name: ", COLLISION.header.name)
        print("Tag Group: ", COLLISION.header.tag_group)
        print("Checksum: ", COLLISION.header.checksum)
        print("Data Offset: ", COLLISION.header.data_offset)
        print("Data Length:", COLLISION.header.data_length)
        print("Unknown Value: ", COLLISION.header.unk2)
        print("Version: ", COLLISION.header.version)
        print("Destination: ", COLLISION.header.destination)
        print("Plugin Handle: ", COLLISION.header.plugin_handle)
        print("Engine Tag: ", COLLISION.header.engine_tag)
        print(" ")

    collision_body_tag_block_header = struct.unpack('<16x', input_stream.read(16))
    collision_body_struct = struct.unpack('<iIIiIIiiIIiIIiIIiII', input_stream.read(76))
    COLLISION.collision_body = COLLISION.CollisionBody()
    COLLISION.collision_body.import_info_tag_block = TAG.TagBlock(collision_body_struct[0], 0, collision_body_struct[1], collision_body_struct[2])
    COLLISION.collision_body.errors_tag_block = TAG.TagBlock(collision_body_struct[3], 0, collision_body_struct[4], collision_body_struct[5])
    COLLISION.collision_body.flags = collision_body_struct[6]
    COLLISION.collision_body.materials_tag_block = TAG.TagBlock(collision_body_struct[7], 0, collision_body_struct[8], collision_body_struct[9])
    COLLISION.collision_body.regions_tag_block = TAG.TagBlock(collision_body_struct[10], 0, collision_body_struct[11], collision_body_struct[12])
    COLLISION.collision_body.pathfinding_spheres_tag_block = TAG.TagBlock(collision_body_struct[13], 0, collision_body_struct[14], collision_body_struct[15])
    COLLISION.collision_body.nodes_tag_block = TAG.TagBlock(collision_body_struct[16], 0, collision_body_struct[17], collision_body_struct[18])

    if DEBUG_PARSER and DEBUG_BODY:
        print(" ===== SBSP Body ===== ")
        print("Import Info Tag Block Count: ", COLLISION.collision_body.import_info_tag_block.count)
        print("Import Info Tag Block Maximum Count: ", COLLISION.collision_body.import_info_tag_block.maximum_count)
        print("Import Info Tag Block Address: ", COLLISION.collision_body.import_info_tag_block.address)
        print("Import Info Tag Block Definition: ", COLLISION.collision_body.import_info_tag_block.definition)
        print("Errors Tag Block Count: ", COLLISION.collision_body.errors_tag_block.count)
        print("Errors Tag Block Maximum Count: ", COLLISION.collision_body.errors_tag_block.maximum_count)
        print("Errors Tag Block Address: ", COLLISION.collision_body.errors_tag_block.address)
        print("Errors Tag Block Definition: ", COLLISION.collision_body.errors_tag_block.definition)
        print("Flags: ", COLLISION.collision_body.flags)
        print("Materials Tag Block Count: ", COLLISION.collision_body.materials_tag_block.count)
        print("Materials Tag Block Maximum Count: ", COLLISION.collision_body.materials_tag_block.maximum_count)
        print("Materials Tag Block Address: ", COLLISION.collision_body.materials_tag_block.address)
        print("Materials Tag Block Definition: ", COLLISION.collision_body.materials_tag_block.definition)
        print("Regions Tag Block Count: ", COLLISION.collision_body.regions_tag_block.count)
        print("Regions Tag Block Maximum Count: ", COLLISION.collision_body.regions_tag_block.maximum_count)
        print("Regions Tag Block Address: ", COLLISION.collision_body.regions_tag_block.address)
        print("Regions Tag Block Definition: ", COLLISION.collision_body.regions_tag_block.definition)
        print("Pathfinding Spheres Tag Block Count: ", COLLISION.collision_body.pathfinding_spheres_tag_block.count)
        print("Pathfinding Spheres Tag Block Maximum Count: ", COLLISION.collision_body.pathfinding_spheres_tag_block.maximum_count)
        print("Pathfinding Spheres Tag Block Address: ", COLLISION.collision_body.pathfinding_spheres_tag_block.address)
        print("Pathfinding Spheres Tag Block Definition: ", COLLISION.collision_body.pathfinding_spheres_tag_block.definition)
        print("Nodes Reference Tag Block Count: ", COLLISION.collision_body.nodes_tag_block.count)
        print("Nodes Reference Tag Block Maximum Count: ", COLLISION.collision_body.nodes_tag_block.maximum_count)
        print("Nodes Reference Tag Block Address: ", COLLISION.collision_body.nodes_tag_block.address)
        print("Nodes Reference Tag Block Definition: ", COLLISION.collision_body.nodes_tag_block.definition)
        print(" ")

    import_info_count = COLLISION.collision_body.import_info_tag_block.count
    if import_info_count > 0:
        import_info_tag_block_header = struct.unpack('<16x', input_stream.read(16))
        for import_info_idx in range(import_info_count):
            import_info_struct = struct.unpack('<i256s32s32s96x32s4xiII128x', input_stream.read(596))
            import_info = COLLISION.ImportInfo()
            import_info.build = import_info_struct[0]
            import_info.version = import_info_struct[1].decode().rstrip('\x00')
            import_info.import_date = import_info_struct[2].decode().rstrip('\x00')
            import_info.culprit = import_info_struct[3].decode().rstrip('\x00')
            import_info.import_time = import_info_struct[4].decode().rstrip('\x00')
            import_info.files_tag_block = TAG.TagBlock(import_info_struct[5], 0, import_info_struct[6], import_info_struct[7])

            COLLISION.import_info_blocks.append(import_info)

        file_tag_block_header = struct.unpack('<16x', input_stream.read(16))
        for import_info in COLLISION.import_info_blocks:
            files = []
            for file_idx in range(import_info.files_tag_block.count):
                file_struct = struct.unpack('<256s32s96xiii144x', input_stream.read(540))
                file = COLLISION.Files()
                file.path = file_struct[0].decode().rstrip('\x00')
                file.modification_date = file_struct[1].decode().rstrip('\x00')
                file.checksum = file_struct[2]
                file.size = file_struct[3]
                file.zipped_data = file_struct[4]
                file.uncompressed_data = input_stream.read(file_struct[4])

                files.append(file)

            import_info.files = files

    if DEBUG_PARSER and DEBUG_IMPORT_INFO:
        print(" ===== Import Info ===== ")
        for import_info_idx, import_info in enumerate(COLLISION.import_info_blocks):
            print(" ===== Import Info %s ===== " % import_info_idx)
            print("Build: ",import_info.build)
            print("Version: ", import_info.version)
            print("Import Date: ", import_info.import_date)
            print("Culprit: ", import_info.culprit)
            print("Import Time: ", import_info.import_time)
            print("Files Tag Block Count: ", import_info.files_tag_block.count)
            print("Files Tag Block Maximum Count: ", import_info.files_tag_block.maximum_count)
            print("Files Tag Block Address: ", import_info.files_tag_block.address)
            print("Files Tag Block Definition: ", import_info.files_tag_block.definition)
            print(" ")
            if DEBUG_FILES:
                for file_idx, file in enumerate(import_info.files):
                    print(" ===== File %s ===== " % file_idx)
                    print("Path: ",file.path)
                    print("Modification Date: ", file.modification_date)
                    print("Checksum: ", file.checksum)
                    print("Size: ", file.size)
                    print("Zipped Data: ", file.zipped_data)
                    print(" ")

    error_count = COLLISION.collision_body.errors_tag_block.count
    if error_count > 0:
        error_tag_block_header = struct.unpack('<16x', input_stream.read(16))
        for error_idx in range(error_count):
            error_struct = struct.unpack('<256shh408xiII', input_stream.read(680))
            error = COLLISION.Error()
            error.name = error_struct[0].decode().rstrip('\x00')
            error.report_type = error_struct[1]
            error.flags = error_struct[2]
            error.reports_tag_block = TAG.TagBlock(error_struct[3], 0, error_struct[4], error_struct[5])

            COLLISION.errors.append(error)

        for error in COLLISION.errors:
            report_count = error.reports_tag_block.count
            if report_count > 0:
                report_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                reports = []
                report_lengths = []
                for report_idx in range(report_count):
                    report_struct = struct.unpack('<hhh18x32siiIIiIIiIIiIIiIIiII380xiiffffffffff84x', input_stream.read(644))
                    report_block = COLLISION.Report()
                    report_block.type = report_struct[0]
                    report_block.flags = report_struct[1]
                    report_lengths.append(report_struct[2])
                    report_block.source_filename = report_struct[3].decode().rstrip('\x00')
                    report_block.source_line_number = report_struct[4]
                    report_block.vertices_tag_block = TAG.TagBlock(report_struct[5], 0, report_struct[6], report_struct[7])
                    report_block.vectors_tag_block = TAG.TagBlock(report_struct[8], 0, report_struct[9], report_struct[10])
                    report_block.lines_tag_block = TAG.TagBlock(report_struct[11], 0, report_struct[12], report_struct[13])
                    report_block.triangles_tag_block = TAG.TagBlock(report_struct[14], 0, report_struct[15], report_struct[16])
                    report_block.quads_tag_block = TAG.TagBlock(report_struct[17], 0, report_struct[18], report_struct[19])
                    report_block.comments_tag_block = TAG.TagBlock(report_struct[20], 0, report_struct[21], report_struct[22])
                    report_block.report_key = report_struct[23]
                    report_block.node_index = report_struct[24]
                    report_block.bounds_x = (report_struct[25], report_struct[26])
                    report_block.bounds_y = (report_struct[27], report_struct[28])
                    report_block.bounds_z = (report_struct[29], report_struct[30])
                    report_block.color = (report_struct[32], report_struct[33], report_struct[34], report_struct[31])

                    reports.append(report_block)

                for report_idx, report_block in enumerate(reports):
                    report_length = report_lengths[report_idx]
                    if report_length > 1:
                        report_text = struct.unpack('>%ss' % report_length, input_stream.read(report_length))
                        report_block.text = report_text[0].decode().rstrip('\x00')

                    report_vertices = []
                    report_vectors = []
                    report_lines = []
                    report_triangles = []
                    report_quads = []
                    report_comments = []
                    vertices_count = report_block.vertices_tag_block.count
                    if vertices_count > 0:
                        vertices_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                        for vertices_idx in range(vertices_count):
                            report_vertex_struct = struct.unpack('<fffbbbbfffffffff', input_stream.read(52))
                            report_vertex = COLLISION.ReportVertex()
                            report_vertex.position =  Vector((report_vertex_struct[0], report_vertex_struct[1], report_vertex_struct[2]))
                            report_vertex.node_index_0 = report_vertex_struct[3]
                            report_vertex.node_index_1 = report_vertex_struct[4]
                            report_vertex.node_index_2 = report_vertex_struct[5]
                            report_vertex.node_index_3 = report_vertex_struct[6]
                            report_vertex.node_weight_0 = report_vertex_struct[7]
                            report_vertex.node_weight_1 = report_vertex_struct[8]
                            report_vertex.node_weight_2 = report_vertex_struct[9]
                            report_vertex.node_weight_3 = report_vertex_struct[10]
                            report_vertex.color = (report_vertex_struct[12], report_vertex_struct[13], report_vertex_struct[14], report_vertex_struct[11])
                            report_vertex.screen_size = report_vertex_struct[15]

                            report_vertices.append(report_vertex)

                    vectors_count = report_block.vectors_tag_block.count
                    if vectors_count > 0:
                        vectors_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                        for vectors_idx in range(vectors_count):
                            report_vectors_struct = struct.unpack('<fffbbbbffffffffffff', input_stream.read(64))
                            report_vector = COLLISION.ReportVector()
                            report_vector.position =  Vector((report_vectors_struct[0], report_vectors_struct[1], report_vectors_struct[2]))
                            report_vector.node_index_0 = report_vectors_struct[3]
                            report_vector.node_index_1 = report_vectors_struct[4]
                            report_vector.node_index_2 = report_vectors_struct[5]
                            report_vector.node_index_3 = report_vectors_struct[6]
                            report_vector.node_weight_0 = report_vectors_struct[7]
                            report_vector.node_weight_1 = report_vectors_struct[8]
                            report_vector.node_weight_2 = report_vectors_struct[9]
                            report_vector.node_weight_3 = report_vectors_struct[10]
                            report_vector.color = (report_vectors_struct[12], report_vectors_struct[13], report_vectors_struct[14], report_vectors_struct[11])
                            report_vector.normal =  Vector((report_vectors_struct[15], report_vectors_struct[16], report_vectors_struct[17]))
                            report_vector.screen_length = report_vectors_struct[18]

                            report_vectors.append(report_vector)

                    lines_count = report_block.lines_tag_block.count
                    if lines_count > 0:
                        lines_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                        for lines_idx in range(lines_count):
                            report_line_struct = struct.unpack('<fffbbbbfffffffbbbbffffffff', input_stream.read(80))
                            report_line = COLLISION.ReportLine()
                            report_line.position_a =  Vector((report_line_struct[0], report_line_struct[1], report_line_struct[2]))
                            report_line.node_index_a_0 = report_line_struct[3]
                            report_line.node_index_a_1 = report_line_struct[4]
                            report_line.node_index_a_2 = report_line_struct[5]
                            report_line.node_index_a_3 = report_line_struct[6]
                            report_line.node_weight_a_0 = report_line_struct[7]
                            report_line.node_weight_a_1 = report_line_struct[8]
                            report_line.node_weight_a_2 = report_line_struct[9]
                            report_line.node_weight_a_3 = report_line_struct[10]
                            report_line.position_b =  Vector((report_line_struct[11], report_line_struct[12], report_line_struct[13]))
                            report_line.node_index_b_0 = report_line_struct[14]
                            report_line.node_index_b_1 = report_line_struct[15]
                            report_line.node_index_b_2 = report_line_struct[16]
                            report_line.node_index_b_3 = report_line_struct[17]
                            report_line.node_weight_b_0 = report_line_struct[18]
                            report_line.node_weight_b_1 = report_line_struct[19]
                            report_line.node_weight_b_2 = report_line_struct[20]
                            report_line.node_weight_b_3 = report_line_struct[21]
                            report_line.color = (report_line_struct[23], report_line_struct[24], report_line_struct[25], report_line_struct[22])

                            report_lines.append(report_line)

                    triangle_count = report_block.triangles_tag_block.count
                    if triangle_count > 0:
                        triangle_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                        for triangle_idx in range(triangle_count):
                            report_triangle_struct = struct.unpack('<fffbbbbfffffffbbbbfffffffbbbbffffffff', input_stream.read(112))
                            report_triangle = COLLISION.ReportTriangle()
                            report_triangle.position_a =  Vector((report_triangle_struct[0], report_triangle_struct[1], report_triangle_struct[2]))
                            report_triangle.node_index_a_0 = report_triangle_struct[3]
                            report_triangle.node_index_a_1 = report_triangle_struct[4]
                            report_triangle.node_index_a_2 = report_triangle_struct[5]
                            report_triangle.node_index_a_3 = report_triangle_struct[6]
                            report_triangle.node_weight_a_0 = report_triangle_struct[7]
                            report_triangle.node_weight_a_1 = report_triangle_struct[8]
                            report_triangle.node_weight_a_2 = report_triangle_struct[9]
                            report_triangle.node_weight_a_3 = report_triangle_struct[10]
                            report_triangle.position_b =  Vector((report_triangle_struct[11], report_triangle_struct[12], report_triangle_struct[13]))
                            report_triangle.node_index_b_0 = report_triangle_struct[14]
                            report_triangle.node_index_b_1 = report_triangle_struct[15]
                            report_triangle.node_index_b_2 = report_triangle_struct[16]
                            report_triangle.node_index_b_3 = report_triangle_struct[17]
                            report_triangle.node_weight_b_0 = report_triangle_struct[18]
                            report_triangle.node_weight_b_1 = report_triangle_struct[19]
                            report_triangle.node_weight_b_2 = report_triangle_struct[20]
                            report_triangle.node_weight_b_3 = report_triangle_struct[21]
                            report_triangle.position_c =  Vector((report_triangle_struct[22], report_triangle_struct[23], report_triangle_struct[24]))
                            report_triangle.node_index_c_0 = report_triangle_struct[25]
                            report_triangle.node_index_c_1 = report_triangle_struct[26]
                            report_triangle.node_index_c_2 = report_triangle_struct[27]
                            report_triangle.node_index_c_3 = report_triangle_struct[28]
                            report_triangle.node_weight_c_0 = report_triangle_struct[29]
                            report_triangle.node_weight_c_1 = report_triangle_struct[30]
                            report_triangle.node_weight_c_2 = report_triangle_struct[31]
                            report_triangle.node_weight_c_3 = report_triangle_struct[32]
                            report_triangle.color = (report_triangle_struct[34], report_triangle_struct[35], report_triangle_struct[36], report_triangle_struct[33])

                            report_triangles.append(report_triangle)

                    quad_count = report_block.quads_tag_block.count
                    if quad_count > 0:
                        quad_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                        for quad_idx in range(quad_count):
                            report_quad_struct = struct.unpack('<fffbbbbfffffffbbbbfffffffbbbbfffffffbbbbffffffff', input_stream.read(144))
                            report_quad = COLLISION.ReportQuad()
                            report_quad.position_a =  Vector((report_quad_struct[0], report_quad_struct[1], report_quad_struct[2]))
                            report_quad.node_index_a_0 = report_quad_struct[3]
                            report_quad.node_index_a_1 = report_quad_struct[4]
                            report_quad.node_index_a_2 = report_quad_struct[5]
                            report_quad.node_index_a_3 = report_quad_struct[6]
                            report_quad.node_weight_a_0 = report_quad_struct[7]
                            report_quad.node_weight_a_1 = report_quad_struct[8]
                            report_quad.node_weight_a_2 = report_quad_struct[9]
                            report_quad.node_weight_a_3 = report_quad_struct[10]
                            report_quad.position_b =  Vector((report_quad_struct[11], report_quad_struct[12], report_quad_struct[13]))
                            report_quad.node_index_b_0 = report_quad_struct[14]
                            report_quad.node_index_b_1 = report_quad_struct[15]
                            report_quad.node_index_b_2 = report_quad_struct[16]
                            report_quad.node_index_b_3 = report_quad_struct[17]
                            report_quad.node_weight_b_0 = report_quad_struct[18]
                            report_quad.node_weight_b_1 = report_quad_struct[19]
                            report_quad.node_weight_b_2 = report_quad_struct[20]
                            report_quad.node_weight_b_3 = report_quad_struct[21]
                            report_quad.position_c =  Vector((report_quad_struct[22], report_quad_struct[23], report_quad_struct[24]))
                            report_quad.node_index_c_0 = report_quad_struct[25]
                            report_quad.node_index_c_1 = report_quad_struct[26]
                            report_quad.node_index_c_2 = report_quad_struct[27]
                            report_quad.node_index_c_3 = report_quad_struct[28]
                            report_quad.node_weight_c_0 = report_quad_struct[29]
                            report_quad.node_weight_c_1 = report_quad_struct[30]
                            report_quad.node_weight_c_2 = report_quad_struct[31]
                            report_quad.node_weight_c_3 = report_quad_struct[32]
                            report_quad.position_d =  Vector((report_quad_struct[33], report_quad_struct[34], report_quad_struct[35]))
                            report_quad.node_index_d_0 = report_quad_struct[36]
                            report_quad.node_index_d_1 = report_quad_struct[37]
                            report_quad.node_index_d_2 = report_quad_struct[38]
                            report_quad.node_index_d_3 = report_quad_struct[39]
                            report_quad.node_weight_d_0 = report_quad_struct[40]
                            report_quad.node_weight_d_1 = report_quad_struct[41]
                            report_quad.node_weight_d_2 = report_quad_struct[42]
                            report_quad.node_weight_d_3 = report_quad_struct[43]
                            report_quad.color = (report_quad_struct[45], report_quad_struct[46], report_quad_struct[47], report_quad_struct[44])

                            report_quads.append(report_quad)

                    comment_count = report_block.comments_tag_block.count
                    if comment_count > 0:
                        comment_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                        comment_lengths = []
                        for comment_idx in range(comment_count):
                            report_comment_struct = struct.unpack('<h18xfffbbbbffffffff', input_stream.read(68))
                            report_comment = COLLISION.ReportComment()
                            comment_lengths.append(report_comment_struct[0])
                            report_comment.position =  Vector((report_comment_struct[1], report_comment_struct[2], report_comment_struct[3]))
                            report_comment.node_index_0 = report_comment_struct[4]
                            report_comment.node_index_1 = report_comment_struct[5]
                            report_comment.node_index_2 = report_comment_struct[6]
                            report_comment.node_index_3 = report_comment_struct[7]
                            report_comment.node_weight_0 = report_comment_struct[8]
                            report_comment.node_weight_1 = report_comment_struct[9]
                            report_comment.node_weight_2 = report_comment_struct[10]
                            report_comment.node_weight_3 = report_comment_struct[11]
                            report_comment.color = (report_comment_struct[13], report_comment_struct[14], report_comment_struct[15], report_comment_struct[12])

                            report_comments.append(report_comment)

                        for comment_idx, report_comment in enumerate(report_comments):
                            comment_length = comment_lengths[comment_idx]
                            if comment_length > 1:
                                comment_text = struct.unpack('>%ss' % comment_length, input_stream.read(comment_length))
                                report_comment.text = comment_text[0].decode().rstrip('\x00')

                    report_block.vertices = report_vertices
                    report_block.vectors = report_vectors
                    report_block.lines = report_lines
                    report_block.triangles = report_triangles
                    report_block.quads = report_quads
                    report_block.comments = report_comments

            error.reports = reports

    if DEBUG_PARSER and DEBUG_ERRORS:
        print(" ===== Errors ===== ")
        for error_idx, error in enumerate(COLLISION.errors):
            print(" ===== Error %s ===== " % error_idx)
            print("Name: ",error.name)
            print("Error Type: ", error.report_type)
            print("Flags: ", error.flags)
            print("Reports Tag Block Count: ", error.reports_tag_block.count)
            print("Reports Tag Block Maximum Count: ", error.reports_tag_block.maximum_count)
            print("Reports Tag Block Address: ", error.reports_tag_block.address)
            print("Reports Tag Block Definition: ", error.reports_tag_block.definition)
            print(" ")
            if DEBUG_REPORTS:
                for report_idx, report_block in enumerate(error.reports):
                    print(" ===== Report %s ===== " % report_idx)
                    print("Report Type: ",report_block.type)
                    print("Flags: ", report_block.flags)
                    print("Text: ", report_block.text)
                    print("Source Filename: ", report_block.source_filename)
                    print("Source Line Number: ", report_block.source_line_number)
                    print("Vertices Tag Block Count: ", report_block.vertices_tag_block.count)
                    print("Vertices Tag Block Maximum Count: ", report_block.vertices_tag_block.maximum_count)
                    print("Vertices Tag Block Address: ", report_block.vertices_tag_block.address)
                    print("Vertices Tag Block Definition: ", report_block.vertices_tag_block.definition)
                    print("Vectors Tag Block Count: ", report_block.vectors_tag_block.count)
                    print("Vectors Tag Block Maximum Count: ", report_block.vectors_tag_block.maximum_count)
                    print("Vectors Tag Block Address: ", report_block.vectors_tag_block.address)
                    print("Vectors Tag Block Definition: ", report_block.vectors_tag_block.definition)
                    print("Lines Tag Block Count: ", report_block.lines_tag_block.count)
                    print("Lines Tag Block Maximum Count: ", report_block.lines_tag_block.maximum_count)
                    print("Lines Tag Block Address: ", report_block.lines_tag_block.address)
                    print("Lines Tag Block Definition: ", report_block.lines_tag_block.definition)
                    print("Triangles Tag Block Count: ", report_block.triangles_tag_block.count)
                    print("Triangles Tag Block Maximum Count: ", report_block.triangles_tag_block.maximum_count)
                    print("Triangles Tag Block Address: ", report_block.triangles_tag_block.address)
                    print("Triangles Tag Block Definition: ", report_block.triangles_tag_block.definition)
                    print("Quads Tag Block Count: ", report_block.quads_tag_block.count)
                    print("Quads Tag Block Maximum Count: ", report_block.quads_tag_block.maximum_count)
                    print("Quads Tag Block Address: ", report_block.quads_tag_block.address)
                    print("Quads Tag Block Definition: ", report_block.quads_tag_block.definition)
                    print("Comments Tag Block Count: ", report_block.comments_tag_block.count)
                    print("Comments Tag Block Maximum Count: ", report_block.comments_tag_block.maximum_count)
                    print("Comments Tag Block Address: ", report_block.comments_tag_block.address)
                    print("Comments Tag Block Definition: ", report_block.comments_tag_block.definition)
                    print("Report Key: ", report_block.report_key)
                    print("Node Index: ", report_block.node_index)
                    print("Bounds X: ", report_block.bounds_x)
                    print("Bounds Y: ", report_block.bounds_y)
                    print("Bounds Z: ", report_block.bounds_z)
                    print("Color RGBA: ", report_block.color)
                    print(" ")
                    if DEBUG_REPORT_VERTICES:
                        for report_vertex_idx, report_vertex in enumerate(report_block.vertices):
                            print(" ===== Report Vertex %s ===== " % report_vertex_idx)
                            print("Position: ", report_vertex.position)
                            print("Node Index 0: ", report_vertex.node_index_0)
                            print("Node Index 1: ", report_vertex.node_index_1)
                            print("Node Index 2: ", report_vertex.node_index_2)
                            print("Node Index 3: ", report_vertex.node_index_3)
                            print("Node Weight 0: ", report_vertex.node_weight_0)
                            print("Node Weight 1: ", report_vertex.node_weight_1)
                            print("Node Weight 2: ", report_vertex.node_weight_2)
                            print("Node Weight 3: ", report_vertex.node_weight_3)
                            print("Color RGBA: ", report_vertex.color)
                            print("Screen Size: ", report_vertex.screen_size)
                            print(" ")

                    if DEBUG_REPORT_VECTORS:
                        for report_vector_idx, report_vector in enumerate(report_block.vectors):
                            print(" ===== Report Vector %s ===== " % report_vector_idx)
                            print("Position: ", report_vector.position)
                            print("Node Index 0: ", report_vector.node_index_0)
                            print("Node Index 1: ", report_vector.node_index_1)
                            print("Node Index 2: ", report_vector.node_index_2)
                            print("Node Index 3: ", report_vector.node_index_3)
                            print("Node Weight 0: ", report_vector.node_weight_0)
                            print("Node Weight 1: ", report_vector.node_weight_1)
                            print("Node Weight 2: ", report_vector.node_weight_2)
                            print("Node Weight 3: ", report_vector.node_weight_3)
                            print("Color RGBA: ", report_vector.color)
                            print("Normal: ", report_vector.normal)
                            print("Screen Length: ", report_vector.screen_length)
                            print(" ")

                    if DEBUG_REPORT_LINES:
                        for report_line_idx, report_line in enumerate(report_block.lines):
                            print(" ===== Report Line %s ===== " % report_line_idx)
                            print("Position: ", report_line.position_a)
                            print("Node Index 0: ", report_line.node_index_a_0)
                            print("Node Index 1: ", report_line.node_index_a_1)
                            print("Node Index 2: ", report_line.node_index_a_2)
                            print("Node Index 3: ", report_line.node_index_a_3)
                            print("Node Weight 0: ", report_line.node_weight_a_0)
                            print("Node Weight 1: ", report_line.node_weight_a_1)
                            print("Node Weight 2: ", report_line.node_weight_a_2)
                            print("Node Weight 3: ", report_line.node_weight_a_3)
                            print("Position: ", report_line.position_b)
                            print("Node Index 0: ", report_line.node_index_b_0)
                            print("Node Index 1: ", report_line.node_index_b_1)
                            print("Node Index 2: ", report_line.node_index_b_2)
                            print("Node Index 3: ", report_line.node_index_b_3)
                            print("Node Weight 0: ", report_line.node_weight_b_0)
                            print("Node Weight 1: ", report_line.node_weight_b_1)
                            print("Node Weight 2: ", report_line.node_weight_b_2)
                            print("Node Weight 3: ", report_line.node_weight_b_3)
                            print("Color RGBA: ", report_line.color)
                            print(" ")

                    if DEBUG_REPORT_TRIANGLES:
                        for report_triangle_idx, report_triangle in enumerate(report_block.triangles):
                            print(" ===== Report Triangle %s ===== " % report_triangle_idx)
                            print("Position: ", report_triangle.position_a)
                            print("Node Index 0: ", report_triangle.node_index_a_0)
                            print("Node Index 1: ", report_triangle.node_index_a_1)
                            print("Node Index 2: ", report_triangle.node_index_a_2)
                            print("Node Index 3: ", report_triangle.node_index_a_3)
                            print("Node Weight 0: ", report_triangle.node_weight_a_0)
                            print("Node Weight 1: ", report_triangle.node_weight_a_1)
                            print("Node Weight 2: ", report_triangle.node_weight_a_2)
                            print("Node Weight 3: ", report_triangle.node_weight_a_3)
                            print("Position: ", report_triangle.position_b)
                            print("Node Index 0: ", report_triangle.node_index_b_0)
                            print("Node Index 1: ", report_triangle.node_index_b_1)
                            print("Node Index 2: ", report_triangle.node_index_b_2)
                            print("Node Index 3: ", report_triangle.node_index_b_3)
                            print("Node Weight 0: ", report_triangle.node_weight_b_0)
                            print("Node Weight 1: ", report_triangle.node_weight_b_1)
                            print("Node Weight 2: ", report_triangle.node_weight_b_2)
                            print("Node Weight 3: ", report_triangle.node_weight_b_3)
                            print("Position: ", report_triangle.position_c)
                            print("Node Index 0: ", report_triangle.node_index_c_0)
                            print("Node Index 1: ", report_triangle.node_index_c_1)
                            print("Node Index 2: ", report_triangle.node_index_c_2)
                            print("Node Index 3: ", report_triangle.node_index_c_3)
                            print("Node Weight 0: ", report_triangle.node_weight_c_0)
                            print("Node Weight 1: ", report_triangle.node_weight_c_1)
                            print("Node Weight 2: ", report_triangle.node_weight_c_2)
                            print("Node Weight 3: ", report_triangle.node_weight_c_3)
                            print("Color RGBA: ", report_triangle.color)
                            print(" ")

                    if DEBUG_REPORT_QUADS:
                        for report_quads_idx, report_quad in enumerate(report_block.quads):
                            print(" ===== Report Quad %s ===== " % report_quads_idx)
                            print("Position: ", report_quad.position_a)
                            print("Node Index 0: ", report_quad.node_index_a_0)
                            print("Node Index 1: ", report_quad.node_index_a_1)
                            print("Node Index 2: ", report_quad.node_index_a_2)
                            print("Node Index 3: ", report_quad.node_index_a_3)
                            print("Node Weight 0: ", report_quad.node_weight_a_0)
                            print("Node Weight 1: ", report_quad.node_weight_a_1)
                            print("Node Weight 2: ", report_quad.node_weight_a_2)
                            print("Node Weight 3: ", report_quad.node_weight_a_3)
                            print("Position: ", report_quad.position_b)
                            print("Node Index 0: ", report_quad.node_index_b_0)
                            print("Node Index 1: ", report_quad.node_index_b_1)
                            print("Node Index 2: ", report_quad.node_index_b_2)
                            print("Node Index 3: ", report_quad.node_index_b_3)
                            print("Node Weight 0: ", report_quad.node_weight_b_0)
                            print("Node Weight 1: ", report_quad.node_weight_b_1)
                            print("Node Weight 2: ", report_quad.node_weight_b_2)
                            print("Node Weight 3: ", report_quad.node_weight_b_3)
                            print("Position: ", report_quad.position_c)
                            print("Node Index 0: ", report_quad.node_index_c_0)
                            print("Node Index 1: ", report_quad.node_index_c_1)
                            print("Node Index 2: ", report_quad.node_index_c_2)
                            print("Node Index 3: ", report_quad.node_index_c_3)
                            print("Node Weight 0: ", report_quad.node_weight_c_0)
                            print("Node Weight 1: ", report_quad.node_weight_c_1)
                            print("Node Weight 2: ", report_quad.node_weight_c_2)
                            print("Node Weight 3: ", report_quad.node_weight_c_3)
                            print("Position: ", report_quad.position_d)
                            print("Node Index 0: ", report_quad.node_index_d_0)
                            print("Node Index 1: ", report_quad.node_index_d_1)
                            print("Node Index 2: ", report_quad.node_index_d_2)
                            print("Node Index 3: ", report_quad.node_index_d_3)
                            print("Node Weight 0: ", report_quad.node_weight_d_0)
                            print("Node Weight 1: ", report_quad.node_weight_d_1)
                            print("Node Weight 2: ", report_quad.node_weight_d_2)
                            print("Node Weight 3: ", report_quad.node_weight_d_3)
                            print("Color RGBA: ", report_quad.color)
                            print(" ")

                    if DEBUG_REPORT_COMMENTS:
                        for report_comment_idx, report_comment in enumerate(report_block.comments):
                            print(" ===== Report Comment %s ===== " % report_comment_idx)
                            print("Text: ", report_comment.text)
                            print("Position: ", report_comment.position)
                            print("Node Index 0: ", report_comment.node_index_0)
                            print("Node Index 1: ", report_comment.node_index_1)
                            print("Node Index 2: ", report_comment.node_index_2)
                            print("Node Index 3: ", report_comment.node_index_3)
                            print("Node Weight 0: ", report_comment.node_weight_0)
                            print("Node Weight 1: ", report_comment.node_weight_1)
                            print("Node Weight 2: ", report_comment.node_weight_2)
                            print("Node Weight 3: ", report_comment.node_weight_3)
                            print("Color RGBA: ", report_comment.color)
                            print(" ")

    materials_count = COLLISION.collision_body.materials_tag_block.count
    if materials_count > 0:
        file_tag_block_header = struct.unpack('<16x', input_stream.read(16))
        material_name_lengths = []
        for collision_material_idx in range(materials_count):
            print(input_stream.tell())
            collision_material_struct = struct.unpack('>2xh', input_stream.read(4))
            material_name_lengths.append(collision_material_struct[0])

        for material_name_length in material_name_lengths:
            if material_name_length > 1:
                material_name = struct.unpack('>%ss' % material_name_length, input_stream.read(material_name_length))
                COLLISION.materials.append(material_name[0].decode())

    if DEBUG_PARSER and DEBUG_MATERIALS:
        print(" ===== Materials ===== ")
        for material_idx, material in enumerate(COLLISION.materials):
            print(" ===== Material %s ===== " % material_idx)
            print("Material Name: ", material)
            print(" ")

    region_count = COLLISION.collision_body.regions_tag_block.count
    if region_count > 0:
        region_tag_block_header = struct.unpack('<16x', input_stream.read(16))
        region_name_lengths = []
        for region_idx in range(region_count):
            region_name_struct = struct.unpack('>2xh', input_stream.read(4))
            region_struct = struct.unpack('<iII', input_stream.read(12))
            region = COLLISION.Region()
            region_name_lengths.append(region_name_struct[0])
            region.permutation_tag_block = TAG.TagBlock(region_struct[0], 0, region_struct[1], region_struct[2])

            COLLISION.regions.append(region)

        for region_idx, region in enumerate(COLLISION.regions):
            region_name_length = region_name_lengths[region_idx]
            if region_name_length > 1:
                region_name = struct.unpack('>%ss' % region_name_length, input_stream.read(region_name_length))
                region.name = region_name[0].decode()

            permutation_count = region.permutation_tag_block.count
            if permutation_count > 0:
                permutation_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                permutation_name_lengths = []
                permutations = []
                for permutation_idx in range(permutation_count):
                    permutation_name_struct = struct.unpack('>2xh', input_stream.read(4))
                    permutation_struct = struct.unpack('<iIIiII', input_stream.read(24))
                    permutation = COLLISION.Permutations()
                    permutation_name_lengths.append(permutation_name_struct[0])
                    permutation.bsps_tag_block = TAG.TagBlock(permutation_struct[0], 0, permutation_struct[1], permutation_struct[2])
                    permutation.bsps_physics_tag_block = TAG.TagBlock(permutation_struct[3], 0, permutation_struct[4], permutation_struct[5])

                    permutations.append(permutation)

                for permutation_idx, permutation in enumerate(permutations):
                    permutation_name_length = permutation_name_lengths[permutation_idx]
                    if permutation_name_length > 1:
                        permutation_name = struct.unpack('>%ss' % permutation_name_length, input_stream.read(permutation_name_length))
                        permutation.name = permutation_name[0].decode()

                    bsp_count = permutation.bsps_tag_block.count
                    if bsp_count > 0:
                        bsps = []
                        bsp_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                        for collision_bsp_idx in range(bsp_count):
                            bsp_struct = struct.unpack('<iiIIiIIiIIiIIiIIiIIiIIiII', input_stream.read(100))
                            bsp = COLLISION.BSP()
                            bsp.node_index = bsp_struct[0]
                            bsp.bsp3d_nodes_tag_block = TAG.TagBlock(bsp_struct[1], 131072, bsp_struct[2], bsp_struct[3])
                            bsp.planes_tag_block = TAG.TagBlock(bsp_struct[4], 65535, bsp_struct[5], bsp_struct[6])
                            bsp.leaves_tag_block = TAG.TagBlock(bsp_struct[7], 65535, bsp_struct[8], bsp_struct[9])
                            bsp.bsp2d_references_tag_block = TAG.TagBlock(bsp_struct[10], 131072, bsp_struct[11], bsp_struct[12])
                            bsp.bsp2d_nodes_tag_block = TAG.TagBlock(bsp_struct[13], 65535, bsp_struct[14], bsp_struct[15])
                            bsp.surfaces_tag_block = TAG.TagBlock(bsp_struct[16], 131072, bsp_struct[17], bsp_struct[18])
                            bsp.edges_tag_block = TAG.TagBlock(bsp_struct[19], 262144, bsp_struct[20], bsp_struct[21])
                            bsp.vertices_tag_block = TAG.TagBlock(bsp_struct[22], 131072, bsp_struct[23], bsp_struct[24])

                            bsps.append(bsp)

                        for collision_bsp in bsps:
                            bsp_3d_nodes = []
                            planes = []
                            leaves = []
                            bsp2d_references = []
                            bsp2d_nodes = []
                            surfaces = []
                            edges = []
                            vertices = []
                            collision_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                            bsp3d_nodes_count = collision_bsp.bsp3d_nodes_tag_block.count
                            if bsp3d_nodes_count > 0:
                                bsp3d_nodes_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                                for bsp3d_node_idx in range(bsp3d_nodes_count):
                                    bsp_3d_node_struct = struct.unpack('<ii', input_stream.read(8))
                                    bsp_3d_node = COLLISION.BSP3DNode()
                                    bsp_3d_node.back_child = bsp_3d_node_struct[0]
                                    bsp_3d_node.front_child = bsp_3d_node_struct[1]

                                    bsp_3d_nodes.append(bsp_3d_node)

                            planes_count = collision_bsp.planes_tag_block.count
                            if planes_count > 0:
                                planes_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                                for plane_idx in range(planes_count):
                                    plane_struct = struct.unpack('<ffff', input_stream.read(16))
                                    plane = COLLISION.Plane()
                                    plane.translation = Vector((plane_struct[0], plane_struct[1], plane_struct[2])) * 100
                                    plane.distance = plane_struct[3] * 100

                                    planes.append(plane)

                            leaves_count = collision_bsp.leaves_tag_block.count
                            if leaves_count > 0:
                                leaves_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                                for leaf_idx in range(leaves_count):
                                    leaf_struct = struct.unpack('<bbbx', input_stream.read(4))
                                    leaf = COLLISION.Leaf()
                                    leaf.flags = leaf_struct[0]
                                    leaf.bsp2d_reference_count = leaf_struct[1]
                                    leaf.first_bsp2d_reference = leaf_struct[2]

                                    leaves.append(leaf)

                            bsp2d_references_count = collision_bsp.bsp2d_references_tag_block.count
                            if bsp2d_references_count > 0:
                                bsp2d_references_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                                for bsp2d_reference_idx in range(bsp2d_references_count):
                                    bsp2d_reference_struct = struct.unpack('<hh', input_stream.read(4))
                                    bsp2d_reference = COLLISION.BSP2DReference()
                                    bsp2d_reference.plane = bsp2d_reference_struct[0]
                                    bsp2d_reference.bsp2d_node = bsp2d_reference_struct[1]

                                    bsp2d_references.append(bsp2d_reference)

                            bsp2d_nodes_count = collision_bsp.bsp2d_nodes_tag_block.count
                            if bsp2d_nodes_count > 0:
                                bsp2d_nodes_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                                for bsp2d_nodes_idx in range(bsp2d_nodes_count):
                                    bsp2d_node_struct = struct.unpack('<fffhh', input_stream.read(16))
                                    bsp2d_node = COLLISION.BSP2DNode()
                                    bsp2d_node.plane_i = bsp2d_node_struct[0]
                                    bsp2d_node.plane_j = bsp2d_node_struct[1]
                                    bsp2d_node.distance = bsp2d_node_struct[2] * 100
                                    bsp2d_node.left_child = bsp2d_node_struct[3]
                                    bsp2d_node.right_child = bsp2d_node_struct[4]

                                    bsp2d_nodes.append(bsp2d_node)

                            surfaces_count = collision_bsp.surfaces_tag_block.count
                            if surfaces_count > 0:
                                surfaces_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                                for surfaces_idx in range(surfaces_count):
                                    surfaces_struct = struct.unpack('<hhbbbx', input_stream.read(8))
                                    surface = COLLISION.Surface()
                                    surface.plane = surfaces_struct[0]
                                    surface.first_edge = surfaces_struct[1]
                                    surface.flags = surfaces_struct[2]
                                    surface.breakable_surface = surfaces_struct[3]
                                    surface.material = surfaces_struct[4]

                                    surfaces.append(surface)

                            edges_count = collision_bsp.edges_tag_block.count
                            if edges_count > 0:
                                edges_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                                for edge_idx in range(edges_count):
                                    edge_struct = struct.unpack('<hhhhhh', input_stream.read(12))
                                    edge = COLLISION.Edge()
                                    edge.start_vertex = edge_struct[0]
                                    edge.end_vertex = edge_struct[1]
                                    edge.forward_edge = edge_struct[2]
                                    edge.reverse_edge = edge_struct[3]
                                    edge.left_surface = edge_struct[4]
                                    edge.right_surface = edge_struct[5]

                                    edges.append(edge)

                            vertices_count = collision_bsp.vertices_tag_block.count
                            if vertices_count > 0:
                                vertices_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                                for vertex_idx in range(vertices_count):
                                    vertex_struct = struct.unpack('<fffi', input_stream.read(16))
                                    vertex = COLLISION.Vertex()
                                    vertex.translation = Vector((vertex_struct[0], vertex_struct[1], vertex_struct[2])) * 100
                                    vertex.first_edge = vertex_struct[3]

                                    vertices.append(vertex)

                            collision_bsp.bsp3d_nodes = bsp_3d_nodes
                            collision_bsp.planes = planes
                            collision_bsp.leaves = leaves
                            collision_bsp.bsp2d_references = bsp2d_references
                            collision_bsp.bsp2d_nodes = bsp2d_nodes
                            collision_bsp.surfaces = surfaces
                            collision_bsp.edges = edges
                            collision_bsp.vertices = vertices

                        permutation.bsps = bsps

                    bsp_physics_count = permutation.bsps_physics_tag_block.count
                    if bsp_physics_count > 0:
                        bsp_physics = []
                        bsp_physics_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                        for bsp_physics_idx in range(bsp_physics_count):
                            bsp_physics_struct = struct.unpack('<4xhh60xhh12xhh12xiiIII8x', input_stream.read(128))
                            bsp_physics_block = COLLISION.BSPPhysics()
                            bsp_physics_block.size_0 = bsp_physics_struct[0]
                            bsp_physics_block.count_0 = bsp_physics_struct[1]
                            bsp_physics_block.size_1 = bsp_physics_struct[2]
                            bsp_physics_block.count_1 = bsp_physics_struct[3]
                            bsp_physics_block.size_2 = bsp_physics_struct[4]
                            bsp_physics_block.count_2 = bsp_physics_struct[5]
                            bsp_physics_block.mopp_code_data_ref = TAG.RawData(bsp_physics_struct[6], bsp_physics_struct[7], bsp_physics_struct[8], bsp_physics_struct[9], bsp_physics_struct[10])

                            bsp_physics.append(bsp_physics_block)

                        for bsp_physics_block in bsp_physics:
                            mopp_code_data_size = bsp_physics_block.mopp_code_data_ref.size
                            if mopp_code_data_size > 0:
                                bsp_physics_struct = struct.unpack('<%sb' % mopp_code_data_size, input_stream.read(mopp_code_data_size))
                                bsp_physics_block.mopp_code_data = bsp_physics_struct[0]

                        permutation.bsp_physics = bsp_physics

                region.permutations = permutations

    if DEBUG_PARSER and DEBUG_REGIONS:
        print(" ===== Regions ===== ")
        for region_idx, region in enumerate(COLLISION.regions):
            print(" ===== Region %s ===== " % region_idx)
            print("Region Name: ", region.name)
            print("Permutations Tag Block Count: ", region.permutation_tag_block.count)
            print("Permutations Tag Block Maximum Count: ", region.permutation_tag_block.maximum_count)
            print("Permutations Tag Block Address: ", region.permutation_tag_block.address)
            print("Permutations Tag Block Definition: ", region.permutation_tag_block.definition)
            print(" ")
            if DEBUG_PERMUTATIONS:
                for permutation_idx, permutation in enumerate(region.permutations):
                    print(" ===== Permutation %s ===== " % permutation_idx)
                    print("Permutation Name: ", permutation.name)
                    print("BSP Tag Block Count: ", permutation.bsps_tag_block.count)
                    print("BSP Tag Block Maximum Count: ", permutation.bsps_tag_block.maximum_count)
                    print("BSP Tag Block Address: ", permutation.bsps_tag_block.address)
                    print("BSP Tag Block Definition: ", permutation.bsps_tag_block.definition)
                    print("BSP Physics Tag Block Count: ", permutation.bsps_physics_tag_block.count)
                    print("BSP Physics Tag Block Maximum Count: ", permutation.bsps_physics_tag_block.maximum_count)
                    print("BSP Physics Tag Block Address: ", permutation.bsps_physics_tag_block.address)
                    print("BSP Physics Tag Block Definition: ", permutation.bsps_physics_tag_block.definition)
                    print(" ")
                    if DEBUG_BSPS:
                        for collision_bsp_idx, collision_bsp in enumerate(permutation.bsps):
                            print(" ===== Collision BSP %s ===== " % collision_bsp_idx)
                            print("BSP3D Nodes Tag Block Count: ", collision_bsp.bsp3d_nodes_tag_block.count)
                            print("BSP3D Nodes Tag Block Maximum Count: ", collision_bsp.bsp3d_nodes_tag_block.maximum_count)
                            print("BSP3D Nodes Tag Block Address: ", collision_bsp.bsp3d_nodes_tag_block.address)
                            print("BSP3D Nodes Tag Block Definition: ", collision_bsp.bsp3d_nodes_tag_block.definition)
                            print("Planes Tag Block Count: ", collision_bsp.planes_tag_block.count)
                            print("Planes Tag Block Maximum Count: ", collision_bsp.planes_tag_block.maximum_count)
                            print("Planes Tag Block Address: ", collision_bsp.planes_tag_block.address)
                            print("Planes Tag Block Definition: ", collision_bsp.planes_tag_block.definition)
                            print("Leaves Tag Block Count: ", collision_bsp.leaves_tag_block.count)
                            print("Leaves Tag Block Maximum Count: ", collision_bsp.leaves_tag_block.maximum_count)
                            print("Leaves Tag Block Address: ", collision_bsp.leaves_tag_block.address)
                            print("Leaves Tag Block Definition: ", collision_bsp.leaves_tag_block.definition)
                            print("BSP2D References Tag Block Count: ", collision_bsp.bsp2d_references_tag_block.count)
                            print("BSP2D References Tag Block Maximum Count: ", collision_bsp.bsp2d_references_tag_block.maximum_count)
                            print("BSP2D References Tag Block Address: ", collision_bsp.bsp2d_references_tag_block.address)
                            print("BSP2D References Tag Block Definition: ", collision_bsp.bsp2d_references_tag_block.definition)
                            print("BSP2D Nodes Tag Block Count: ", collision_bsp.bsp2d_nodes_tag_block.count)
                            print("BSP2D Nodes Tag Block Maximum Count: ", collision_bsp.bsp2d_nodes_tag_block.maximum_count)
                            print("BSP2D Nodes Tag Block Address: ", collision_bsp.bsp2d_nodes_tag_block.address)
                            print("BSP2D Nodes Tag Block Definition: ", collision_bsp.bsp2d_nodes_tag_block.definition)
                            print("Surfaces Tag Block Count: ", collision_bsp.surfaces_tag_block.count)
                            print("Surfaces Tag Block Maximum Count: ", collision_bsp.surfaces_tag_block.maximum_count)
                            print("Surfaces Tag Block Address: ", collision_bsp.surfaces_tag_block.address)
                            print("Surfaces Tag Block Definition: ", collision_bsp.surfaces_tag_block.definition)
                            print("Edges Tag Block Count: ", collision_bsp.edges_tag_block.count)
                            print("Edges Tag Block Maximum Count: ", collision_bsp.edges_tag_block.maximum_count)
                            print("Edges Tag Block Address: ", collision_bsp.edges_tag_block.address)
                            print("Edges Tag Block Definition: ", collision_bsp.edges_tag_block.definition)
                            print("Vertices Tag Block Count: ", collision_bsp.vertices_tag_block.count)
                            print("Vertices Tag Block Maximum Count: ", collision_bsp.vertices_tag_block.maximum_count)
                            print("Vertices Tag Block Address: ", collision_bsp.vertices_tag_block.address)
                            print("Vertices Tag Block Definition: ", collision_bsp.vertices_tag_block.definition)
                            print(" ")
                            if DEBUG_BSP3D_NODES:
                                for bsp3d_node_idx, bsp3d_node in enumerate(collision_bsp.bsp3d_nodes):
                                    print(" ===== BSP3D Node %s ===== " % bsp3d_node_idx)
                                    print("Plane: ", bsp3d_node.plane)
                                    print("Back Child: ", bsp3d_node.back_child)
                                    print("Front Child: ", bsp3d_node.front_child)
                                    print(" ")

                            if DEBUG_PLANES:
                                for plane_idx, plane in enumerate(collision_bsp.planes):
                                    print(" ===== Plane %s ===== " % plane_idx)
                                    print("Plane Translation: ", plane.translation)
                                    print("Plane Distance: ", plane.distance)
                                    print(" ")

                            if DEBUG_LEAVES:
                                for leaf_idx, leaf in enumerate(collision_bsp.leaves):
                                    print(" ===== Leaf %s ===== " % leaf_idx)
                                    print("Leaf Flags: ", leaf.flags)
                                    print("Leaf BSP2D Reference Count: ", leaf.bsp2d_reference_count)
                                    print("Leaf First BSP2D Reference: ", leaf.first_bsp2d_reference)
                                    print(" ")

                            if DEBUG_BSP2D_REFERENCES:
                                for bsp2d_reference_idx, bsp2d_reference in enumerate(collision_bsp.bsp2d_references):
                                    print(" ===== BSP2D Reference %s ===== " % bsp2d_reference_idx)
                                    print("BSP2D Reference Plane: ", bsp2d_reference.plane)
                                    print("BSP2D Reference Node: ", bsp2d_reference.bsp2d_node)
                                    print(" ")

                            if DEBUG_BSP2D_NODES:
                                for bsp2d_node_idx, bsp2d_node in enumerate(collision_bsp.bsp2d_nodes):
                                    print(" ===== BSP2D Node %s ===== " % bsp2d_node_idx)
                                    print("Plane i: ", bsp2d_node.plane_i)
                                    print("Plane j: ", bsp2d_node.plane_j)
                                    print("Plane Distance: ", bsp2d_node.distance)
                                    print("Left Child: ", bsp2d_node.left_child)
                                    print("Right Child: ", bsp2d_node.right_child)
                                    print(" ")

                            if DEBUG_SURFACES:
                                for surface_idx, surface in enumerate(collision_bsp.surfaces):
                                    print(" ===== Surface %s ===== " % surface_idx)
                                    print("Surface Plane: ", surface.plane)
                                    print("Surface First Edge: ", surface.first_edge)
                                    print("Surface Flags: ", surface.flags)
                                    print("Surface Breakable Surface: ", surface.breakable_surface)
                                    print("Surface Material: ", surface.material)
                                    print(" ")

                            if DEBUG_EDGES:
                                for edge_idx, edge in enumerate(collision_bsp.edges):
                                    print(" ===== Edge %s ===== " % edge_idx)
                                    print("Edge Start Vertex: ", edge.start_vertex)
                                    print("Edge End Vertex: ", edge.end_vertex)
                                    print("Edge Forward : ", edge.forward_edge)
                                    print("Edge Reverse: ", edge.reverse_edge)
                                    print("Edge Left Surface: ", edge.left_surface)
                                    print("Edge Right Surface: ", edge.right_surface)
                                    print(" ")

                            if DEBUG_VERTICES:
                                for vertex_idx, vertex in enumerate(collision_bsp.vertices):
                                    print(" ===== Vertex %s ===== " % vertex_idx)
                                    print("Vertex Translation: ", vertex.translation)
                                    print("Vertex First Edge: ", vertex.first_edge)
                                    print(" ")

                    if DEBUG_BSP_PHYSICS:
                        for bsp_physics_idx, bsp_physics in enumerate(permutation.bsp_physics):
                            print(" ===== BSP Physics %s ===== " % bsp_physics_idx)
                            print("Size: ", bsp_physics.size_0)
                            print("Count: ", bsp_physics.count_0)
                            print("Size: ", bsp_physics.size_1)
                            print("Count: ", bsp_physics.count_1)
                            print("Size: ", bsp_physics.size_2)
                            print("Count: ", bsp_physics.count_2)
                            print("Mopp Code Data Ref Size: ", bsp_physics.mopp_code_data_ref.size)
                            print("Mopp Code Data Ref Flags: ", bsp_physics.mopp_code_data_ref.flags)
                            print("Mopp Code Data Ref Raw Pointer: ", bsp_physics.mopp_code_data_ref.raw_pointer)
                            print("Mopp Code Data Ref Pointer: ", bsp_physics.mopp_code_data_ref.pointer)
                            print("Mopp Code Data Ref ID: ", bsp_physics.mopp_code_data_ref.id)
                            print("Mopp Code Data: ", bsp_physics.mopp_code_data)
                            print(" ")

    pathfinding_spheres_count = COLLISION.collision_body.pathfinding_spheres_tag_block.count
    if pathfinding_spheres_count > 0:
        pathfinding_spheres_tag_block_header = struct.unpack('<16x', input_stream.read(16))
        for pathfinding_sphere_idx in range(pathfinding_spheres_count):
            pathfinding_sphere_struct = struct.unpack('<hhffff', input_stream.read(20))
            pathfinding_sphere = COLLISION.PathfindingSphere()
            pathfinding_sphere.node = pathfinding_sphere_struct[0]
            pathfinding_sphere.flags = pathfinding_sphere_struct[1]
            pathfinding_sphere.center = Vector((pathfinding_sphere_struct[2], pathfinding_sphere_struct[3], pathfinding_sphere_struct[4])) * 100
            pathfinding_sphere.radius = pathfinding_sphere_struct[5]

            COLLISION.pathfinding_spheres.append(pathfinding_sphere)

    if DEBUG_PARSER and DEBUG_PATHFINDING_SPHERES:
        print(" ===== Pathfinding Spheres ===== ")
        for pathfinding_sphere_idx, pathfinding_sphere in enumerate(COLLISION.pathfinding_spheres):
            print(" ===== Pathfinding Sphere %s ===== " % pathfinding_sphere_idx)
            print("Node: ", pathfinding_sphere.node)
            print("Flags: ", pathfinding_sphere.flags)
            print("Center: ", pathfinding_sphere.center)
            print("Radius: ", pathfinding_sphere.radius)
            print(" ")

    node_count = COLLISION.collision_body.nodes_tag_block.count
    if node_count > 0:
        node_tag_block_header = struct.unpack('<16x', input_stream.read(16))
        node_name_lengths = []
        for node_idx in range(node_count):
            node_name_struct = struct.unpack('>2xh', input_stream.read(4))
            node_struct = struct.unpack('<2xhhh', input_stream.read(8))
            node = COLLISION.Node()
            node_name_lengths.append(node_name_struct[0])
            node.parent_node = node_struct[0]
            node.next_sibling_node = node_struct[1]
            node.first_child_node = node_struct[2]

            COLLISION.nodes.append(node)

        for node_idx, node in enumerate(COLLISION.nodes):
            node_name_length = node_name_lengths[node_idx]
            if node_name_length > 1:
                node_name = struct.unpack('>%ss' % node_name_length, input_stream.read(node_name_length))
                node.name = node_name[0].decode()

    if DEBUG_PARSER and DEBUG_NODES:
        print(" ===== Nodes ===== ")
        for node_idx, node in enumerate(COLLISION.nodes):
            print(" ===== Node %s ===== " % node_idx)
            print("Name: ", node.name)
            print("Parent Node: ", node.parent_node)
            print("Next Sibling Node: ", node.next_sibling_node)
            print("First Child Node: ", node.first_child_node)
            print(" ")

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    return COLLISION
