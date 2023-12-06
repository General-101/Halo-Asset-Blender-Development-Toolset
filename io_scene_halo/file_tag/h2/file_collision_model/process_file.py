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

from mathutils import Vector
from .format import CollisionAsset
from ....global_functions import tag_format

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

def collision_body_1(COLLISION, TAG, input_stream):
    collision_body = COLLISION.CollisionBody()
    collision_body.import_info_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)
    collision_body.errors_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)
    collision_body.flags = TAG.read_signed_integer(input_stream, TAG.big_endian)
    collision_body.materials_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)
    collision_body.regions_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)
    collision_body.pathfinding_spheres_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)
    collision_body.nodes_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)

    return collision_body

def get_collision_body_tag_block(COLLISION, TAG, input_stream):
    collision_body_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)

    if collision_body_tag_block_header.version == 1:
        COLLISION.collision_body = collision_body_1(COLLISION, TAG, input_stream)


def import_info_0(COLLISION, TAG, input_stream):
    import_info = COLLISION.ImportInfo()
    import_info.build = TAG.read_signed_integer(input_stream, TAG.big_endian)
    import_info.version = TAG.read_string256(input_stream, TAG.big_endian)
    import_info.import_date = TAG.read_string32(input_stream, TAG.big_endian)
    import_info.culprit = TAG.read_string32(input_stream, TAG.big_endian)
    input_stream.read(96) # Padding?
    import_info.import_time = TAG.read_string32(input_stream, TAG.big_endian)
    input_stream.read(4) # Padding?
    import_info.files_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)
    input_stream.read(128) # Padding?

    return import_info

def files_0(COLLISION, TAG, input_stream):
    file = COLLISION.Files()
    file.path = TAG.read_string256(input_stream, TAG.big_endian)
    file.modification_date = TAG.read_string32(input_stream, TAG.big_endian)
    input_stream.read(96) # Padding?
    file.checksum = TAG.read_signed_integer(input_stream, TAG.big_endian)
    file.size = TAG.read_signed_integer(input_stream, TAG.big_endian)
    file.zipped_data = TAG.read_signed_integer(input_stream, TAG.big_endian)
    input_stream.read(144) # Padding?
    file.uncompressed_data = input_stream.read(file.zipped_data)

    return file

def get_import_info_tag_block(COLLISION, TAG, input_stream):
    import_info_count = COLLISION.collision_body.import_info_tag_block.count
    COLLISION.import_info_blocks = []
    if import_info_count > 0:
        import_info_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)
        import_info = None
        if import_info_tag_block_header.version == 0:
            import_info = import_info_0

        for import_info_idx in range(import_info_count):
            COLLISION.import_info_blocks.append(import_info(COLLISION, TAG, input_stream))

        file_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)
        file = None
        if file_tag_block_header.version == 0:
            file = files_0

        for import_info in COLLISION.import_info_blocks:
            import_info.files = []
            for file_idx in range(import_info.files_tag_block.count):
                import_info.files.append(file(COLLISION, TAG, input_stream))

def errors_0(COLLISION, TAG, input_stream):
    error = COLLISION.Error()
    error.name = TAG.read_string256(input_stream, TAG.big_endian)
    error.report_type = TAG.read_signed_short(input_stream, TAG.big_endian)
    error.flags = TAG.read_signed_short(input_stream, TAG.big_endian)
    input_stream.read(408) # Padding?
    error.reports_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)

    return error

def reports_0(COLLISION, TAG, input_stream):
    report_block = COLLISION.Report()
    report_block.type = TAG.read_signed_short(input_stream, TAG.big_endian)
    report_block.flags = TAG.read_signed_short(input_stream, TAG.big_endian)
    report_block.report_length = TAG.read_signed_short(input_stream, TAG.big_endian)
    input_stream.read(18) # Padding?
    report_block.source_filename = TAG.read_string32(input_stream, TAG.big_endian)
    report_block.source_line_number = TAG.read_signed_integer(input_stream, TAG.big_endian)
    report_block.vertices_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)
    report_block.vectors_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)
    report_block.lines_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)
    report_block.triangles_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)
    report_block.quads_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)
    report_block.comments_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)
    input_stream.read(380) # Padding?
    report_block.report_key = TAG.read_signed_integer(input_stream, TAG.big_endian)
    report_block.node_index = TAG.read_signed_integer(input_stream, TAG.big_endian)
    report_block.bounds_x = TAG.read_min_max(input_stream, TAG.big_endian)
    report_block.bounds_y = TAG.read_min_max(input_stream, TAG.big_endian)
    report_block.bounds_z = TAG.read_min_max(input_stream, TAG.big_endian)
    report_block.color = TAG.read_argb(input_stream, TAG.big_endian)
    input_stream.read(84) # Padding?

    return report_block

def vertex_0(COLLISION, TAG, input_stream):
    report_vertex = COLLISION.ReportVertex()
    report_vertex.position = TAG.read_vector(input_stream, TAG.big_endian)
    report_vertex.node_index_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_vertex.node_index_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_vertex.node_index_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_vertex.node_index_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_vertex.node_weight_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_vertex.node_weight_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_vertex.node_weight_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_vertex.node_weight_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_vertex.color = TAG.read_argb(input_stream, TAG.big_endian)
    report_vertex.screen_size = TAG.read_float(input_stream, TAG.big_endian)

    return report_vertex

def vector_0(COLLISION, TAG, input_stream):
    report_vector = COLLISION.ReportVector()
    report_vector.position = TAG.read_vector(input_stream, TAG.big_endian)
    report_vector.node_index_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_vector.node_index_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_vector.node_index_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_vector.node_index_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_vector.node_weight_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_vector.node_weight_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_vector.node_weight_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_vector.node_weight_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_vector.color = TAG.read_argb(input_stream, TAG.big_endian)
    report_vector.normal = TAG.read_vector(input_stream, TAG.big_endian)
    report_vector.screen_length = TAG.read_float(input_stream, TAG.big_endian)

    return report_vector

def line_0(COLLISION, TAG, input_stream):
    report_line = COLLISION.ReportLine()
    report_line.position_a = TAG.read_vector(input_stream, TAG.big_endian)
    report_line.node_index_a_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_line.node_index_a_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_line.node_index_a_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_line.node_index_a_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_line.node_weight_a_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_line.node_weight_a_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_line.node_weight_a_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_line.node_weight_a_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_line.position_b = TAG.read_vector(input_stream, TAG.big_endian)
    report_line.node_index_b_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_line.node_index_b_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_line.node_index_b_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_line.node_index_b_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_line.node_weight_b_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_line.node_weight_b_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_line.node_weight_b_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_line.node_weight_b_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_line.color = TAG.read_argb(input_stream, TAG.big_endian)

    return report_line

def triangle_0(COLLISION, TAG, input_stream):
    report_triangle = COLLISION.ReportTriangle()
    report_triangle.position_a = TAG.read_vector(input_stream, TAG.big_endian)
    report_triangle.node_index_a_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_triangle.node_index_a_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_triangle.node_index_a_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_triangle.node_index_a_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_triangle.node_weight_a_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_triangle.node_weight_a_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_triangle.node_weight_a_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_triangle.node_weight_a_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_triangle.position_b = TAG.read_vector(input_stream, TAG.big_endian)
    report_triangle.node_index_b_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_triangle.node_index_b_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_triangle.node_index_b_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_triangle.node_index_b_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_triangle.node_weight_b_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_triangle.node_weight_b_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_triangle.node_weight_b_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_triangle.node_weight_b_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_triangle.position_c = TAG.read_vector(input_stream, TAG.big_endian)
    report_triangle.node_index_c_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_triangle.node_index_c_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_triangle.node_index_c_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_triangle.node_index_c_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_triangle.node_weight_c_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_triangle.node_weight_c_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_triangle.node_weight_c_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_triangle.node_weight_c_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_triangle.color = TAG.read_argb(input_stream, TAG.big_endian)

    return report_triangle

def quad_0(COLLISION, TAG, input_stream):
    report_quad = COLLISION.ReportQuad()
    report_quad.position_a = TAG.read_vector(input_stream, TAG.big_endian)
    report_quad.node_index_a_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_a_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_a_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_a_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_weight_a_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_a_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_a_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_a_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.position_b = TAG.read_vector(input_stream, TAG.big_endian)
    report_quad.node_index_b_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_b_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_b_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_b_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_weight_b_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_b_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_b_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_b_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.position_c = TAG.read_vector(input_stream, TAG.big_endian)
    report_quad.node_index_c_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_c_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_c_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_c_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_weight_c_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_c_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_c_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_c_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.position_d = TAG.read_vector(input_stream, TAG.big_endian)
    report_quad.node_index_d_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_d_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_d_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_d_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_weight_d_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_d_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_d_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_d_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.color = TAG.read_argb(input_stream, TAG.big_endian)

    return report_quad

def comment_0(COLLISION, TAG, input_stream):
    report_quad = COLLISION.ReportQuad()
    report_quad.position_a = TAG.read_vector(input_stream, TAG.big_endian)
    report_quad.node_index_a_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_a_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_a_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_a_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_weight_a_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_a_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_a_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_a_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.position_b = TAG.read_vector(input_stream, TAG.big_endian)
    report_quad.node_index_b_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_b_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_b_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_b_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_weight_b_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_b_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_b_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_b_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.position_c = TAG.read_vector(input_stream, TAG.big_endian)
    report_quad.node_index_c_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_c_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_c_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_c_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_weight_c_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_c_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_c_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_c_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.position_d = TAG.read_vector(input_stream, TAG.big_endian)
    report_quad.node_index_d_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_d_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_d_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_index_d_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_quad.node_weight_d_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_d_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_d_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.node_weight_d_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_quad.color = TAG.read_argb(input_stream, TAG.big_endian)

    return report_quad

def comment_0(COLLISION, TAG, input_stream):
    report_comment = COLLISION.ReportComment()
    report_comment.text_length = TAG.read_signed_short(input_stream, TAG.big_endian)
    input_stream.read(18) # Padding?
    report_comment.position = TAG.read_vector(input_stream, TAG.big_endian)
    report_comment.node_index_0 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_comment.node_index_1 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_comment.node_index_2 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_comment.node_index_3 = TAG.read_signed_byte(input_stream, TAG.big_endian)
    report_comment.node_weight_0 = TAG.read_float(input_stream, TAG.big_endian)
    report_comment.node_weight_1 = TAG.read_float(input_stream, TAG.big_endian)
    report_comment.node_weight_2 = TAG.read_float(input_stream, TAG.big_endian)
    report_comment.node_weight_3 = TAG.read_float(input_stream, TAG.big_endian)
    report_comment.color = TAG.read_argb(input_stream, TAG.big_endian)

    return report_comment

def get_errors_tag_block(COLLISION, TAG, input_stream):
    error_count = COLLISION.collision_body.errors_tag_block.count
    COLLISION.errors = []
    if error_count > 0:
        error_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)
        error = None
        if error_tag_block_header.version == 0:
            error = errors_0

        for error_idx in range(error_count):
            COLLISION.errors.append(error(COLLISION, TAG, input_stream))

        for error in COLLISION.errors:
            report_count = error.reports_tag_block.count
            error.reports = []
            if report_count > 0:
                report_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)
                report = None
                if report_tag_block_header.version == 0:
                    report = reports_0

                for report_idx in range(report_count):
                    error.reports.append(report)

                for report_block in error.reports:
                    if report_block.report_length > 1:
                        report_block.text = TAG.read_variable_string(input_stream, report_block.report_length, TAG.big_endian)

                    report_block.vertices = []
                    report_block.vectors = []
                    report_block.lines = []
                    report_block.triangles = []
                    report_block.quads = []
                    report_block.comments = []

                    vertices_count = report_block.vertices_tag_block.count
                    if vertices_count > 0:
                        vertices_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)
                        vertex = None
                        if vertices_tag_block_header.version == 0:
                            vertex = vertex_0

                        for vertices_idx in range(vertices_count):
                            report_block.vertices.append(vertex(COLLISION, TAG, input_stream))

                    vectors_count = report_block.vectors_tag_block.count
                    if vectors_count > 0:
                        vectors_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)
                        vector = None
                        if vectors_tag_block_header.version == 0:
                            vector = vector_0

                        for vectors_idx in range(vectors_count):
                            report_block.vectors.append(vector(COLLISION, TAG, input_stream))

                    lines_count = report_block.lines_tag_block.count
                    if lines_count > 0:
                        lines_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)
                        line = None
                        if lines_tag_block_header.version == 0:
                            line = line_0

                        for lines_idx in range(lines_count):
                            report_block.lines.append(line(COLLISION, TAG, input_stream))

                    triangle_count = report_block.triangles_tag_block.count
                    if triangle_count > 0:
                        triangle_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)
                        triangle = None
                        if triangle_tag_block_header.version == 0:
                            triangle = triangle_0

                        for triangle_idx in range(triangle_count):
                            report_block.triangles.append(triangle(COLLISION, TAG, input_stream))

                    quad_count = report_block.quads_tag_block.count
                    if quad_count > 0:
                        quad_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)
                        quad = None
                        if quad_tag_block_header.version == 0:
                            quad = quad_0

                        for quad_idx in range(quad_count):
                            report_block.quads.append(quad(COLLISION, TAG, input_stream))

                    comment_count = report_block.comments_tag_block.count
                    if comment_count > 0:
                        comment_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)
                        comment = None
                        if comment_tag_block_header.version == 0:
                            comment = comment_0

                        for comment_idx in range(comment_count):
                            report_block.comments.append(comment(COLLISION, TAG, input_stream))

                        for report_comment in report_block.comments:
                            if report_comment.text_length > 1:
                                report_comment.text = TAG.read_variable_string(input_stream, report_block.text_length, TAG.big_endian)

def material_length_0(TAG, input_stream):
    input_stream.read(2) # Padding?
    material_name_length = TAG.read_signed_short(input_stream, TAG.big_endian)

    return material_name_length

def material_string_0(material_name_length, TAG, input_stream):
    material_name = TAG.read_variable_string(input_stream, material_name_length, TAG.big_endian)

    return material_name

def get_materials_tag_block(COLLISION, TAG, input_stream):
    materials_count = COLLISION.collision_body.materials_tag_block.count
    COLLISION.materials = []
    if materials_count > 0:
        materials_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)
        materials_length = None
        materials_name = None
        if materials_tag_block_header.version == 0:
            materials_length = material_length_0
            materials_name = material_string_0

        material_name_lengths = []
        for collision_material_idx in range(materials_count):
            material_name_lengths.append(materials_length(TAG, input_stream))

        for material_name_length in material_name_lengths:
            if material_name_length > 1:
                COLLISION.materials.append(materials_name(TAG, input_stream))

def region_0(COLLISION, TAG, input_stream):
    region = COLLISION.Region()
    input_stream.read(2) # Padding?
    region.name_length = TAG.read_signed_short(input_stream, TAG.big_endian)
    region.permutation_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)

    return region

def permutation_1(COLLISION, TAG, input_stream):
    permutation = COLLISION.Permutations()
    input_stream.read(2) # Padding?
    permutation.name_length = TAG.read_signed_short(input_stream, TAG.big_endian)
    permutation.bsps_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)
    permutation.bsps_physics_tag_block = TAG.TagBlock().read(input_stream, 0, TAG.big_endian)

    return permutation

def get_regions_tag_block(COLLISION, TAG, input_stream):
    region_count = COLLISION.collision_body.regions_tag_block.count
    COLLISION.regions = []
    if region_count > 0:
        region_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)
        region = None
        if region_tag_block_header.version == 0:
            region = region_0

        for region_idx in range(region_count):
            COLLISION.regions.append(region(COLLISION, TAG, input_stream))

        for region in COLLISION.regions:
            if region.name_length > 0:
                region.name = TAG.read_variable_string(input_stream, region.name_length, TAG.big_endian)

            permutation_count = region.permutation_tag_block.count
            region.permutations = []
            if permutation_count > 0:
                permutation_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)
                permutation = None
                if permutation_tag_block_header.version == 1:
                    permutation = permutation_1

                for permutation_idx in range(permutation_count):
                    region.permutations.append(permutation(COLLISION, TAG, input_stream))

                for permutation in enumerate(region.permutations):
                    if permutation.name_length > 0:
                        permutation.name = TAG.read_variable_string(input_stream, permutation.name_length, TAG.big_endian)

                    bsp_count = permutation.bsps_tag_block.count
                    permutation.bsps = []
                    if bsp_count > 0:
                        bsp_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG.big_endian)
                        bsp = None
                        if bsp_tag_block_header.version == 0:
                            bsp = bsp_0

                        for collision_bsp_idx in range(bsp_count):
                            bsp = COLLISION.BSP()
                            bsp.node_index = TAG.read_signed_integer(input_stream, TAG.big_endian)
                            bsp.bsp3d_nodes_tag_block = TAG.TagBlock().read(input_stream, 131072, TAG.big_endian)
                            bsp.planes_tag_block = TAG.TagBlock().read(input_stream, 65535, TAG.big_endian)
                            bsp.leaves_tag_block = TAG.TagBlock().read(input_stream, 65535, TAG.big_endian)
                            bsp.bsp2d_references_tag_block = TAG.TagBlock().read(input_stream, 131072, TAG.big_endian)
                            bsp.bsp2d_nodes_tag_block = TAG.TagBlock().read(input_stream, 65535, TAG.big_endian)
                            bsp.surfaces_tag_block = TAG.TagBlock().read(input_stream, 131072, TAG.big_endian)
                            bsp.edges_tag_block = TAG.TagBlock().read(input_stream, 262144, TAG.big_endian)
                            bsp.vertices_tag_block = TAG.TagBlock().read(input_stream, 131072, TAG.big_endian)

                            permutation.bsps.append(bsp)

                        for collision_bsp in permutation.bsps:
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
                                    surface.material_index = surfaces_struct[4]

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

                    bsp_physics_count = permutation.bsps_physics_tag_block.count
                    permutation.bsp_physics = []
                    if bsp_physics_count > 0:
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

                            permutation.bsp_physics.append(bsp_physics_block)

                        for bsp_physics_block in permutation.bsp_physics:
                            mopp_code_data_size = bsp_physics_block.mopp_code_data_ref.size
                            if mopp_code_data_size > 0:
                                bsp_physics_struct = struct.unpack('<%sb' % mopp_code_data_size, input_stream.read(mopp_code_data_size))
                                bsp_physics_block.mopp_code_data = bsp_physics_struct[0]

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    TAG.big_endian = False
    COLLISION = CollisionAsset()

    COLLISION.header = TAG.Header().read(input_stream, TAG.big_endian)

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

    get_collision_body_tag_block(COLLISION, TAG, input_stream)

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

    get_import_info_tag_block(COLLISION, TAG, input_stream)

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

    get_errors_tag_block(COLLISION, TAG, input_stream)

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

    get_materials_tag_block(COLLISION, TAG, input_stream)

    if DEBUG_PARSER and DEBUG_MATERIALS:
        print(" ===== Materials ===== ")
        for material_idx, material in enumerate(COLLISION.materials):
            print(" ===== Material %s ===== " % material_idx)
            print("Material Name: ", material)
            print(" ")

    get_regions_tag_block(COLLISION, TAG, input_stream)

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
                                    print("Surface Material: ", surface.material_index)
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
    COLLISION.pathfinding_spheres = []
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
    COLLISION.nodes = []
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
