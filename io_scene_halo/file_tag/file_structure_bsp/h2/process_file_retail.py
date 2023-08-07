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
from .format_retail import LevelAsset
from mathutils import Vector, Quaternion

XML_OUTPUT = False

def process_file_retail(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    LEVEL = LevelAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    LEVEL.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    level_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG)
    LEVEL.level_body = LEVEL.LevelBody()
    LEVEL.level_body.import_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "import info"))
    input_stream.read(4) # Padding?
    LEVEL.level_body.collision_materials_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision materials"))
    LEVEL.level_body.collision_bsps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision bsps"))
    LEVEL.level_body.vehicle_floor = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "vehicle floor"))
    LEVEL.level_body.vehicle_ceiling = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "vehicle ceiling"))
    LEVEL.level_body.unused_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused nodes"))
    LEVEL.level_body.leaves_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "leaves"))
    LEVEL.level_body.world_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "world bounds x"))
    LEVEL.level_body.world_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "world bounds y"))
    LEVEL.level_body.world_bounds_z = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "world bounds z"))
    LEVEL.level_body.surfaces_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "surfaces references"))
    LEVEL.level_body.cluster_raw_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "cluster data"))
    LEVEL.level_body.cluster_portals_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "cluster portals"))
    LEVEL.level_body.fog_planes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "fog planes"))
    input_stream.read(24) # Padding?
    LEVEL.level_body.weather_palettes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weather palettes"))
    LEVEL.level_body.weather_polyhedras_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weather polyhedras"))
    LEVEL.level_body.detail_objects_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "detail objects"))
    LEVEL.level_body.clusters_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "clusters"))
    LEVEL.level_body.materials_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "materials"))
    LEVEL.level_body.sky_owner_cluster_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sky owner cluster"))
    LEVEL.level_body.conveyor_surfaces_cluster_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "conveyor surfaces cluster"))
    LEVEL.level_body.breakable_surfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "breakable surfaces"))
    LEVEL.level_body.pathfinding_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "pathfinding data"))
    LEVEL.level_body.pathfinding_edges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "pathfinding edges"))
    LEVEL.level_body.background_sounds_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "background sounds palette"))
    LEVEL.level_body.sound_environment_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sound environment palette"))
    LEVEL.level_body.sound_pas_raw_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "sound pas data"))
    LEVEL.level_body.markers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "markers"))
    LEVEL.level_body.runtime_decals_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "runtime decals"))
    LEVEL.level_body.environment_object_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "environment object palette"))
    LEVEL.level_body.environment_objects_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "environment objects"))
    LEVEL.level_body.lightmaps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "lightmaps"))
    input_stream.read(4) # Padding?
    LEVEL.level_body.leaf_map_leaves_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "leaf map leaves"))
    LEVEL.level_body.leaf_map_connections_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "leaf map connections"))
    LEVEL.level_body.errors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "errors"))
    LEVEL.level_body.precomputed_lighting_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "precomputed lighting"))
    LEVEL.level_body.instanced_geometries_definition_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "instanced geometries definition"))
    LEVEL.level_body.instanced_geometry_instances_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "instanced geometry instances"))
    LEVEL.level_body.ambience_sound_clusters_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ambience sound clusters"))
    LEVEL.level_body.reverb_sound_clusters_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "reverb sound clusters"))
    LEVEL.level_body.transparent_planes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "transparent planes"))
    input_stream.read(96) # Padding?
    LEVEL.level_body.vehicle_spherical_limit_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "vehicle spherical limit radius"))
    LEVEL.level_body.vehicle_spherical_limit_center = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "vehicle spherical limit center"))
    LEVEL.level_body.debug_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "debug info"))
    LEVEL.level_body.decorators_bitmaps_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "decorators bitmaps"))
    LEVEL.level_body.decorators_0_raw_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "decorators 0 data"))
    input_stream.read(4) # Padding?
    LEVEL.level_body.decorators_0_vector = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "decorators 0 vector"))
    LEVEL.level_body.decorators_1_vector = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "decorators 1 vector"))
    LEVEL.level_body.decorators_1_raw_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "decorators 1 data"))
    LEVEL.level_body.breakable_surface_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "breakable surface"))
    LEVEL.level_body.water_definitions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "water definitions"))
    LEVEL.level_body.portal_device_mapping_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "portal device mapping"))
    LEVEL.level_body.audibility_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "audibility"))
    LEVEL.level_body.object_fake_lightprobes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "object fake lightprobes"))
    LEVEL.level_body.decorators_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "decorators"))

    LEVEL.import_info = []
    import_info_count = LEVEL.level_body.import_info_tag_block.count
    if import_info_count > 0:
        import_info_node = tag_format.get_xml_node(XML_OUTPUT, import_info_count, tag_node, "name", "import info")
        import_info_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for import_info_idx in range(import_info_count):
            import_info_element_node = None
            if XML_OUTPUT:
                import_info_element_node = TAG.xml_doc.createElement('element')
                import_info_element_node.setAttribute('index', str(import_info_idx))
                import_info_node.appendChild(import_info_element_node)

            import_info = LEVEL.ImportInfo()
            import_info.build = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(import_info_element_node, "build"))
            import_info.version = TAG.read_string256(input_stream, TAG, tag_format.XMLData(import_info_element_node, "version"))
            import_info.import_date = TAG.read_string32(input_stream, TAG, tag_format.XMLData(import_info_element_node, "import date"))
            import_info.culprit = TAG.read_string32(input_stream, TAG, tag_format.XMLData(import_info_element_node, "culprit"))
            input_stream.read(96) # Padding?
            import_info.import_time = TAG.read_string32(input_stream, TAG, tag_format.XMLData(import_info_element_node, "import time"))
            input_stream.read(4) # Padding?
            import_info.files_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(import_info_element_node, "files"))
            input_stream.read(128) # Padding?

            LEVEL.import_info.append(import_info)

        for import_info_idx, import_info in enumerate(LEVEL.import_info):
            import_info_element_node = None
            if XML_OUTPUT:
                import_info_element_node = import_info_node.childNodes[import_info_idx]

            import_info.files = []
            files_count = import_info.files_tag_block.count
            if files_count > 0:
                files_node = tag_format.get_xml_node(XML_OUTPUT, files_count, import_info_element_node, "name", "files")
                files_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for file_idx in range(files_count):
                    file_element_node = None
                    if XML_OUTPUT:
                        file_element_node = TAG.xml_doc.createElement('element')
                        file_element_node.setAttribute('index', str(file_idx))
                        files_node.appendChild(file_element_node)

                    file = LEVEL.File()
                    file.path = TAG.read_string256(input_stream, TAG, tag_format.XMLData(file_element_node, "path"))
                    file.modification_date = TAG.read_string32(input_stream, TAG, tag_format.XMLData(file_element_node, "modification date"))
                    input_stream.read(96) # Padding?
                    file.checksum = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(file_element_node, "checksum"))
                    file.size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(file_element_node, "size"))
                    file.zipped_data = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(file_element_node, "zipped data"))
                    input_stream.read(144) # Padding?
                    file.uncompressed_data = input_stream.read(file.zipped_data)

                    import_info.files.append(file)

    LEVEL.collision_materials = []
    collision_materials_count = LEVEL.level_body.collision_materials_tag_block.count
    if collision_materials_count > 0:
        collision_materials_node = tag_format.get_xml_node(XML_OUTPUT, collision_materials_count, tag_node, "name", "collision materials")
        collision_materials_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for collision_material_idx in range(collision_materials_count):
            collision_material_element_node = None
            if XML_OUTPUT:
                collision_material_element_node = TAG.xml_doc.createElement('element')
                collision_material_element_node.setAttribute('index', str(collision_material_idx))
                collision_materials_node.appendChild(collision_material_element_node)

            collision_material = LEVEL.CollisionMaterial()
            collision_material.old_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(collision_material_element_node, "old shader"))
            input_stream.read(2) # Padding?
            collision_material.conveyor_surface_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(collision_material_element_node, "conveyor surface index"))
            collision_material.new_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(collision_material_element_node, "new shader"))

            LEVEL.collision_materials.append(collision_material)

        for collision_material_idx, collision_material in enumerate(LEVEL.collision_materials):
            collision_materials_element_node = None
            if XML_OUTPUT:
                collision_materials_element_node = collision_materials_node.childNodes[collision_material_idx]

            if collision_material.old_shader.name_length > 0:
                collision_material.old_shader.name = TAG.read_variable_string(input_stream, collision_material.old_shader.name_length, TAG)

            if collision_material.new_shader.name_length > 0:
                collision_material.new_shader.name = TAG.read_variable_string(input_stream, collision_material.new_shader.name_length, TAG)

            if XML_OUTPUT:
                old_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, collision_materials_element_node, "name", "old shader")
                new_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, collision_materials_element_node, "name", "new shader")
                collision_material.old_shader.append_xml_attributes(old_shader_node)
                collision_material.new_shader.append_xml_attributes(new_shader_node)

    LEVEL.collision_bsps = []
    collision_bsps_count = LEVEL.level_body.collision_bsps_tag_block.count
    if collision_bsps_count > 0:
        collision_bsps_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsps_count, tag_node, "name", "collision bsps")
        collision_bsps_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for collision_bsp_idx in range(collision_bsps_count):
            collision_bsp_element_node = None
            if XML_OUTPUT:
                collision_bsp_element_node = TAG.xml_doc.createElement('element')
                collision_bsp_element_node.setAttribute('index', str(collision_bsp_idx))
                collision_bsps_node.appendChild(collision_bsp_element_node)

    collision_bsps_count = LEVEL.level_body.collision_bsps_tag_block.count
    if collision_bsps_count > 0:
        collision_bsps_header = struct.unpack('<4siii', input_stream.read(16))
        LEVEL.level_body.collision_bsps_header = TAG.TagBlockHeader(collision_bsps_header[0], collision_bsps_header[1], collision_bsps_header[2], collision_bsps_header[3])
        for collision_bsp_idx in range(collision_bsps_count):
            collision_bsp_struct = struct.unpack('<iIIiIIiIIiIIiIIiIIiIIiII', input_stream.read(96))
            collision_bsp = LEVEL.CollisionBSP()
            collision_bsp.bsp3d_nodes_tag_block = TAG.TagBlock(collision_bsp_struct[0], 131072, collision_bsp_struct[1], collision_bsp_struct[2])
            collision_bsp.planes_tag_block = TAG.TagBlock(collision_bsp_struct[3], 65535, collision_bsp_struct[4], collision_bsp_struct[5])
            collision_bsp.leaves_tag_block = TAG.TagBlock(collision_bsp_struct[6], 65535, collision_bsp_struct[7], collision_bsp_struct[8])
            collision_bsp.bsp2d_references_tag_block = TAG.TagBlock(collision_bsp_struct[9], 131072, collision_bsp_struct[10], collision_bsp_struct[11])
            collision_bsp.bsp2d_nodes_tag_block = TAG.TagBlock(collision_bsp_struct[12], 65535, collision_bsp_struct[13], collision_bsp_struct[14])
            collision_bsp.surfaces_tag_block = TAG.TagBlock(collision_bsp_struct[15], 131072, collision_bsp_struct[16], collision_bsp_struct[17])
            collision_bsp.edges_tag_block = TAG.TagBlock(collision_bsp_struct[18], 262144, collision_bsp_struct[19], collision_bsp_struct[20])
            collision_bsp.vertices_tag_block = TAG.TagBlock(collision_bsp_struct[21], 131072, collision_bsp_struct[22], collision_bsp_struct[23])

            LEVEL.collision_bsps.append(collision_bsp)

        for collision_bsp in LEVEL.collision_bsps:
            bsp_3d_nodes = []
            planes = []
            leaves = []
            bsp2d_references = []
            bsp2d_nodes = []
            surfaces = []
            edges = []
            vertices = []
            bsp3d_nodes_count = collision_bsp.bsp3d_nodes_tag_block.count
            if bsp3d_nodes_count > 0:
                bsp3d_nodes_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                for bsp3d_node_idx in range(bsp3d_nodes_count):
                    bsp_3d_node_struct = struct.unpack('<ii', input_stream.read(8))
                    bsp_3d_node = LEVEL.BSP3DNode()
                    bsp_3d_node.back_child = bsp_3d_node_struct[0]
                    bsp_3d_node.front_child = bsp_3d_node_struct[1]

                    bsp_3d_nodes.append(bsp_3d_node)

            planes_count = collision_bsp.planes_tag_block.count
            if planes_count > 0:
                planes_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                for plane_idx in range(planes_count):
                    plane_struct = struct.unpack('<ffff', input_stream.read(16))
                    plane = LEVEL.Plane()
                    plane.translation = Vector((plane_struct[0], plane_struct[1], plane_struct[2])) * 100
                    plane.distance = plane_struct[3] * 100

                    planes.append(plane)

            leaves_count = collision_bsp.leaves_tag_block.count
            if leaves_count > 0:
                leaves_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                for leaf_idx in range(leaves_count):
                    leaf_struct = struct.unpack('<bbbx', input_stream.read(4))
                    leaf = LEVEL.Leaf()
                    leaf.flags = leaf_struct[0]
                    leaf.bsp2d_reference_count = leaf_struct[1]
                    leaf.first_bsp2d_reference = leaf_struct[2]

                    leaves.append(leaf)

            bsp2d_references_count = collision_bsp.bsp2d_references_tag_block.count
            if bsp2d_references_count > 0:
                bsp2d_references_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                for bsp2d_reference_idx in range(bsp2d_references_count):
                    bsp2d_reference_struct = struct.unpack('<hh', input_stream.read(4))
                    bsp2d_reference = LEVEL.BSP2DReference()
                    bsp2d_reference.plane = bsp2d_reference_struct[0]
                    bsp2d_reference.bsp2d_node = bsp2d_reference_struct[1]

                    bsp2d_references.append(bsp2d_reference)

            bsp2d_nodes_count = collision_bsp.bsp2d_nodes_tag_block.count
            if bsp2d_nodes_count > 0:
                bsp2d_nodes_tag_block_header = struct.unpack('<16x', input_stream.read(16))
                for bsp2d_nodes_idx in range(bsp2d_nodes_count):
                    bsp2d_node_struct = struct.unpack('<fffhh', input_stream.read(16))
                    bsp2d_node = LEVEL.BSP2DNode()
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
                    surface = LEVEL.Surface()
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
                    edge = LEVEL.Edge()
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
                    vertex = LEVEL.Vertex()
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

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, LEVEL.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return LEVEL
