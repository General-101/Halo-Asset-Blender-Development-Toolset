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
from .format_retail import (
        LevelAsset,
        LeafFlags,
        SurfaceFlags
        )
from mathutils import Vector, Quaternion

XML_OUTPUT = False

def initilize_scenario(LEVEL):
    LEVEL.import_info = []
    LEVEL.collision_materials = []
    LEVEL.collision_bsps = []
    LEVEL.cluster_portals = []
    LEVEL.clusters = []
    LEVEL.materials = []

def read_bsp_body(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    LEVEL.level_header = TAG.TagBlockHeader().read(input_stream, TAG)
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

def read_import_info(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    if LEVEL.level_body.import_info_tag_block.count > 0:
        import_info_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.import_info_tag_block.count, tag_node, "name", "import info")
        LEVEL.import_info_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for import_info_idx in range(LEVEL.level_body.import_info_tag_block.count):
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
            if import_info.files_tag_block.count > 0:
                files_node = tag_format.get_xml_node(XML_OUTPUT, import_info.files_tag_block.count, import_info_element_node, "name", "files")
                import_info.files_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for file_idx in range(import_info.files_tag_block.count):
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

def read_collision_materials(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    if LEVEL.level_body.collision_materials_tag_block.count > 0:
        collision_materials_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.collision_materials_tag_block.count, tag_node, "name", "collision materials")
        LEVEL.collision_materials_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for collision_material_idx in range(LEVEL.level_body.collision_materials_tag_block.count):
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

def read_collision_bsps(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    if LEVEL.level_body.collision_bsps_tag_block.count > 0:
        collision_bsps_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.collision_bsps_tag_block.count, tag_node, "name", "collision bsps")
        LEVEL.collision_bsp_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for collision_bsp_idx in range(LEVEL.level_body.collision_bsps_tag_block.count):
            collision_bsp_element_node = None
            if XML_OUTPUT:
                collision_bsp_element_node = TAG.xml_doc.createElement('element')
                collision_bsp_element_node.setAttribute('index', str(collision_bsp_idx))
                collision_bsps_node.appendChild(collision_bsp_element_node)

            collision_bsp = LEVEL.CollisionBSP()
            collision_bsp.bsp3d_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "bsp3d nodes"))
            collision_bsp.planes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "planes"))
            collision_bsp.leaves_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "leaves"))
            collision_bsp.bsp2d_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "bsp2d references"))
            collision_bsp.bsp2d_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "bsp2d nodes"))
            collision_bsp.surfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "surfaces"))
            collision_bsp.edges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "edges"))
            collision_bsp.vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(collision_bsp_element_node, "vertices"))

            LEVEL.collision_bsps.append(collision_bsp)

        for collision_bsp_idx, collision_bsp in enumerate(LEVEL.collision_bsps):
            collision_bsp_element_node = None
            if XML_OUTPUT:
                collision_bsp_element_node = collision_bsps_node.childNodes[collision_bsp_idx]

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

                    bsp3d_node = LEVEL.BSP3DNode()
                    bsp3d_node.back_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp3d_node_element_node, "back child"))
                    bsp3d_node.front_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp3d_node_element_node, "front child"))

                    collision_bsp.bsp3d_nodes.append(bsp3d_node)

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

                    leaf = LEVEL.Leaf()
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

                    bsp2d_reference = LEVEL.BSP2DReference()
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

                    bsp2d_node = LEVEL.BSP2DNode()
                    bsp2d_node.plane = TAG.Plane2D().read(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "plane"))
                    bsp2d_node.left_child = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "left child"))
                    bsp2d_node.right_child = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "right child"))

                    collision_bsp.bsp2d_nodes.append(bsp2d_node)

            if collision_bsp.surfaces_tag_block.count > 0:
                collision_bsp.surfaces_header = TAG.TagBlockHeader().read(input_stream, TAG)
                surfaces_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.surfaces_tag_block.count, collision_bsp_element_node, "name", "surfaces")
                for surfaces_idx in range(collision_bsp.surfaces_tag_block.count):
                    surface_element_node = None
                    if XML_OUTPUT:
                        surface_element_node = TAG.xml_doc.createElement('element')
                        surface_element_node.setAttribute('index', str(surfaces_idx))
                        surfaces_node.appendChild(surface_element_node)

                    surface = LEVEL.Surface()
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

                    edge = LEVEL.Edge()
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

                    vertex = LEVEL.Vertex()
                    vertex.translation = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(vertex_element_node, "translation"), True)
                    vertex.first_edge = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(vertex_element_node, "first edge"))

                    collision_bsp.vertices.append(vertex)

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

    initilize_scenario(LEVEL)
    read_bsp_body(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)
    read_import_info(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)
    read_collision_materials(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)
    read_collision_bsps(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)

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
