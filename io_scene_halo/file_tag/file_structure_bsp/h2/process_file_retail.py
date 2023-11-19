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
        SurfaceFlags,
        ClusterPortalFlags,
        FogPlaneFlags,
        GeometryClassificationEnum,
        GeometryCompressionFlags,
        SectionLightingFlags,
        ClusterFlags,
        ResourceEnum,
        PartTypeEnum,
        PartFlags,
        PredictedResourceTypeEnum,
        PropertyTypeEnum
        )

XML_OUTPUT = True

def initilize_scenario(LEVEL):
    LEVEL.import_info = []
    LEVEL.collision_materials = []
    LEVEL.collision_bsps = []
    LEVEL.unused_nodes = []
    LEVEL.leaves = []
    LEVEL.surface_references = []
    LEVEL.cluster_portals = []
    LEVEL.fog_planes = []
    LEVEL.weather_palette = []
    LEVEL.weather_polyhedra = []
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
    LEVEL.level_body.surface_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "surface references"))
    LEVEL.level_body.cluster_raw_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "cluster data"))
    LEVEL.level_body.cluster_portals_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "cluster portals"))
    LEVEL.level_body.fog_planes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "fog planes"))
    input_stream.read(24) # Padding?
    LEVEL.level_body.weather_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weather palette"))
    LEVEL.level_body.weather_polyhedra_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weather polyhedra"))
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

                    bsp3d = LEVEL.BSP3DNode()
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

                    bsp2d = LEVEL.BSP2DNode()
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
                    vertex.translation = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(vertex_element_node, "translation"), True)
                    vertex.first_edge = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(vertex_element_node, "first edge"))

                    collision_bsp.vertices.append(vertex)

def read_unused_nodes(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    if LEVEL.level_body.unused_nodes_tag_block.count > 0:
        unused_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.unused_nodes_tag_block.count, tag_node, "name", "unused nodes")
        LEVEL.unused_nodes_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for unused_node_idx in range(LEVEL.level_body.unused_nodes_tag_block.count):
            unused_node_element_node = None
            if XML_OUTPUT:
                unused_node_element_node = TAG.xml_doc.createElement('element')
                unused_node_element_node.setAttribute('index', str(unused_node_idx))
                unused_node.appendChild(unused_node_element_node)

            input_stream.read(6) # Padding?

def read_leaves(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    if LEVEL.level_body.leaves_tag_block.count > 0:
        leaves_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.leaves_tag_block.count, tag_node, "name", "leaves")
        LEVEL.unused_nodes_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for leaf_idx in range(LEVEL.level_body.leaves_tag_block.count):
            leaf_element_node = None
            if XML_OUTPUT:
                leaf_element_node = TAG.xml_doc.createElement('element')
                leaf_element_node.setAttribute('index', str(leaf_idx))
                leaves_node.appendChild(leaf_element_node)

            cluster_leaf = LEVEL.ClusterLeaf()
            cluster_leaf.cluster = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(leaf_element_node, "cluster"))
            cluster_leaf.surface_reference_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(leaf_element_node, "surface reference count"))
            cluster_leaf.surface_reference = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(leaf_element_node, "surface reference"))

            LEVEL.leaves.append(cluster_leaf)

def read_surface_references(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    if LEVEL.level_body.surface_references_tag_block.count > 0:
        surface_reference_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.surface_references_tag_block.count, tag_node, "name", "surface references")
        LEVEL.surface_references_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for surface_reference_idx in range(LEVEL.level_body.surface_references_tag_block.count):
            surface_reference_element_node = None
            if XML_OUTPUT:
                surface_reference_element_node = TAG.xml_doc.createElement('element')
                surface_reference_element_node.setAttribute('index', str(surface_reference_idx))
                surface_reference_node.appendChild(surface_reference_element_node)

            surface_reference = LEVEL.SurfaceReference()
            surface_reference.strip_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(surface_reference_element_node, "cluster"))
            surface_reference.lightmap_triangle_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(surface_reference_element_node, "surface reference count"))
            surface_reference.bsp_node_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_reference_element_node, "surface reference"))

            LEVEL.surface_references.append(surface_reference)

def read_cluster_portals(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    if LEVEL.level_body.cluster_portals_tag_block.count > 0:
        cluster_portals_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.cluster_portals_tag_block.count, tag_node, "name", "cluster portals")
        LEVEL.cluster_portals_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for cluster_portal_idx in range(LEVEL.level_body.cluster_portals_tag_block.count):
            cluster_portal_element_node = None
            if XML_OUTPUT:
                cluster_portal_element_node = TAG.xml_doc.createElement('element')
                cluster_portal_element_node.setAttribute('index', str(cluster_portal_idx))
                cluster_portals_node.appendChild(cluster_portal_element_node)

            cluster_portal = LEVEL.ClusterPortal()
            cluster_portal.back_cluster = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_portal_element_node, "back cluster"))
            cluster_portal.front_cluster = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_portal_element_node, "front cluster"))
            cluster_portal.plane_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(cluster_portal_element_node, "plane index"))
            cluster_portal.centroid = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(cluster_portal_element_node, "centroid"))
            cluster_portal.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(cluster_portal_element_node, "bounding radius"))
            cluster_portal.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(cluster_portal_element_node, "flags", ClusterPortalFlags))
            cluster_portal.vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_portal_element_node, "vertices"))

            LEVEL.cluster_portals.append(cluster_portal)

        for cluster_portal_idx, cluster_portal in enumerate(LEVEL.cluster_portals):
            cluster_portal_element_node = None
            if XML_OUTPUT:
                cluster_portal_element_node = cluster_portals_node.childNodes[cluster_portal_idx]

            cluster_portal.vertices = []
            if cluster_portal.vertices_tag_block.count > 0:
                vertices_node = tag_format.get_xml_node(XML_OUTPUT, cluster_portal.vertices_tag_block.count, cluster_portal_element_node, "name", "vertices")
                cluster_portal.vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for vertex_idx in range(cluster_portal.vertices_tag_block.count):
                    vertex_element_node = None
                    if XML_OUTPUT:
                        vertex_element_node = TAG.xml_doc.createElement('element')
                        vertex_element_node.setAttribute('index', str(vertex_idx))
                        vertices_node.appendChild(vertex_element_node)

                    cluster_portal.vertices.append(TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(vertex_element_node, "point"), True))

def read_fog_planes(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    if LEVEL.level_body.fog_planes_tag_block.count > 0:
        fog_planes_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.fog_planes_tag_block.count, tag_node, "name", "fog planes")
        LEVEL.fog_planes_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for fog_plane_idx in range(LEVEL.level_body.fog_planes_tag_block.count):
            fog_plane_element_node = None
            if XML_OUTPUT:
                fog_plane_element_node = TAG.xml_doc.createElement('element')
                fog_plane_element_node.setAttribute('index', str(fog_plane_idx))
                fog_planes_node.appendChild(fog_plane_element_node)

            fog_plane = LEVEL.FogPlane()
            fog_plane.scenario_planar_fog_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(fog_plane_element_node, "scenario planar fog index"))
            input_stream.read(2) # Padding?
            fog_plane.plane = TAG.Plane3D().read(input_stream, TAG, tag_format.XMLData(fog_plane_element_node, "plane"))
            fog_plane.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(fog_plane_element_node, "flags", FogPlaneFlags))
            fog_plane.priority = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(fog_plane_element_node, "priority"))

            LEVEL.fog_planes.append(fog_plane)

def read_weather_palette(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    if LEVEL.level_body.weather_palette_tag_block.count > 0:
        weather_palette_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.weather_palette_tag_block.count, tag_node, "name", "weather palette")
        LEVEL.weather_palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for weather_palette_idx in range(LEVEL.level_body.weather_palette_tag_block.count):
            weather_palette_element_node = None
            if XML_OUTPUT:
                weather_palette_element_node = TAG.xml_doc.createElement('element')
                weather_palette_element_node.setAttribute('index', str(weather_palette_idx))
                weather_palette_node.appendChild(weather_palette_element_node)

            weather_palette = LEVEL.WeatherPalette()
            weather_palette.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "name"))
            weather_palette.weather_system = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "weather system"))
            weather_palette.wind = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "wind"))
            weather_palette.wind_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "wind direction"))
            weather_palette.wind_magnitude = TAG.read_float(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "wind magnitude"))
            weather_palette.wind_scale_function = TAG.read_string32(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "wind scale function"))

            LEVEL.weather_palette.append(weather_palette)

        for weather_palette_idx, weather_palette in enumerate(LEVEL.weather_palette):
            weather_palette_element_node = None
            if XML_OUTPUT:
                weather_palette_element_node = weather_palette_node.childNodes[weather_palette_idx]

            if weather_palette.weather_system.name_length > 0:
                weather_palette.weather_system.name = TAG.read_variable_string(input_stream, weather_palette.weather_system.name_length, TAG)

            if weather_palette.wind.name_length > 0:
                weather_palette.wind.name = TAG.read_variable_string(input_stream, weather_palette.wind.name_length, TAG)

            if XML_OUTPUT:
                weather_system_node = tag_format.get_xml_node(XML_OUTPUT, 1, weather_palette_element_node, "name", "weather system")
                wind_node = tag_format.get_xml_node(XML_OUTPUT, 1, weather_palette_element_node, "name", "wind")
                weather_palette.weather_system.append_xml_attributes(weather_system_node)
                weather_palette.wind.append_xml_attributes(wind_node)

def read_weather_polyhedra(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    if LEVEL.level_body.weather_polyhedra_tag_block.count > 0:
        weather_polyhedra_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.weather_polyhedra_tag_block.count, tag_node, "name", "weather polyhedra")
        LEVEL.weather_polyhedra_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for weather_polyhedra_idx in range(LEVEL.level_body.weather_polyhedra_tag_block.count):
            weather_polyhedra_element_node = None
            if XML_OUTPUT:
                weather_polyhedra_element_node = TAG.xml_doc.createElement('element')
                weather_polyhedra_element_node.setAttribute('index', str(weather_polyhedra_idx))
                weather_polyhedra_node.appendChild(weather_polyhedra_element_node)

            weather_polyhedra = LEVEL.WeatherPolyhedra()
            weather_polyhedra.bounding_sphere_center = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(weather_polyhedra_element_node, "bounding sphere center"))
            weather_polyhedra.bounding_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(weather_polyhedra_element_node, "bounding sphere radius"))
            weather_polyhedra.planes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(weather_polyhedra_element_node, "planes"))

            LEVEL.weather_polyhedra.append(weather_polyhedra)

        for weather_polyhedra_idx, weather_polyhedra in enumerate(LEVEL.weather_polyhedra):
            weather_polyhedra_element_node = None
            if XML_OUTPUT:
                weather_polyhedra_element_node = weather_polyhedra_node.childNodes[weather_polyhedra_idx]

            weather_polyhedra.planes = []
            if weather_polyhedra.planes_tag_block.count > 0:
                plane_node = tag_format.get_xml_node(XML_OUTPUT, weather_polyhedra.planes_tag_block.count, weather_polyhedra_element_node, "name", "planes")
                weather_polyhedra.planes_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for plane_idx in range(weather_polyhedra.planes_tag_block.count):
                    plane_element_node = None
                    if XML_OUTPUT:
                        plane_element_node = TAG.xml_doc.createElement('element')
                        plane_element_node.setAttribute('index', str(plane_idx))
                        plane_node.appendChild(plane_element_node)

                    weather_polyhedra.planes.append(TAG.Plane3D().read(input_stream, TAG, tag_format.XMLData(plane_element_node, "plane")))

def read_detail_objects(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    if LEVEL.level_body.detail_objects_tag_block.count > 0:
        detail_object_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.detail_objects_tag_block.count, tag_node, "name", "detail objects")
        LEVEL.detail_objects_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for detail_object_idx in range(LEVEL.level_body.detail_objects_tag_block.count):
            detail_object_element_node = None
            if XML_OUTPUT:
                detail_object_element_node = TAG.xml_doc.createElement('element')
                detail_object_element_node.setAttribute('index', str(detail_object_idx))
                detail_object_node.appendChild(detail_object_element_node)

            detail_object = LEVEL.DetailObject()
            detail_object.cells_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(detail_object_element_node, "cells"))
            detail_object.instances_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(detail_object_element_node, "instances"))
            detail_object.counts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(detail_object_element_node, "counts"))
            detail_object.z_reference_vectors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(detail_object_element_node, "z reference vectors"))
            input_stream.read(4) # Padding?

            LEVEL.detail_objects.append(detail_object)

        for detail_object_idx, detail_object in enumerate(LEVEL.detail_objects):
            detail_object_element_node = None
            if XML_OUTPUT:
                detail_object_element_node = detail_object_node.childNodes[detail_object_idx]

            detail_object.cells = []
            detail_object.instances = []
            detail_object.counts = []
            detail_object.z_reference_vectors = []
            if detail_object.cells_tag_block.count > 0:
                cell_node = tag_format.get_xml_node(XML_OUTPUT, detail_object.cells_tag_block.count, detail_object_element_node, "name", "cells")
                detail_object.cells_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for cell_idx in range(detail_object.cells_tag_block.count):
                    cell_element_node = None
                    if XML_OUTPUT:
                        cell_element_node = TAG.xml_doc.createElement('element')
                        cell_element_node.setAttribute('index', str(cell_idx))
                        cell_node.appendChild(cell_element_node)

                    cell = LEVEL.Cell()
                    cell.unknown_0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cell_element_node, "unknown"))
                    cell.unknown_1 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cell_element_node, "unknown"))
                    cell.unknown_2 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cell_element_node, "unknown"))
                    cell.unknown_3 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cell_element_node, "unknown"))
                    cell.unknown_4 = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(cell_element_node, "unknown"))
                    cell.unknown_5 = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(cell_element_node, "unknown"))
                    cell.unknown_6 = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(cell_element_node, "unknown"))
                    input_stream.read(12) # Padding?

                    detail_object.cells.append(cell)

            if detail_object.instances_tag_block.count > 0:
                instance_node = tag_format.get_xml_node(XML_OUTPUT, detail_object.instances_tag_block.count, detail_object_element_node, "name", "instances")
                detail_object.instances_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for instance_idx in range(detail_object.instances_tag_block.count):
                    instance_element_node = None
                    if XML_OUTPUT:
                        instance_element_node = TAG.xml_doc.createElement('element')
                        instance_element_node.setAttribute('index', str(instance_idx))
                        instance_node.appendChild(instance_element_node)

                    instance = LEVEL.Instances()
                    instance.unknown_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(instance_element_node, "unknown"))
                    instance.unknown_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(instance_element_node, "unknown"))
                    instance.unknown_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(instance_element_node, "unknown"))
                    instance.unknown_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(instance_element_node, "unknown"))
                    instance.unknown_4 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(instance_element_node, "unknown"))
                    input_stream.read(1) # Padding?

                    detail_object.instances.append(instance)

            if detail_object.counts_tag_block.count > 0:
                count_node = tag_format.get_xml_node(XML_OUTPUT, detail_object.counts_tag_block.count, detail_object_element_node, "name", "counts")
                detail_object.counts_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for count_idx in range(detail_object.counts_tag_block.count):
                    count_element_node = None
                    if XML_OUTPUT:
                        count_element_node = TAG.xml_doc.createElement('element')
                        count_element_node.setAttribute('index', str(count_idx))
                        count_node.appendChild(count_element_node)

                    unknown = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(instance_element_node, "unknown"))
                    input_stream.read(1) # Padding?

                    detail_object.counts.append(unknown)

            if detail_object.z_reference_vectors_tag_block.count > 0:
                z_reference_vector_node = tag_format.get_xml_node(XML_OUTPUT, detail_object.z_reference_vectors_tag_block.count, detail_object_element_node, "name", "z reference vectors")
                detail_object.z_reference_vectors_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for z_reference_vector_idx in range(detail_object.z_reference_vectors_tag_block.count):
                    z_reference_vector_element_node = None
                    if XML_OUTPUT:
                        z_reference_vector_element_node = TAG.xml_doc.createElement('element')
                        z_reference_vector_element_node.setAttribute('index', str(z_reference_vector_idx))
                        z_reference_vector_node.appendChild(z_reference_vector_element_node)

                    z_reference_vector = LEVEL.ZReferenceVector()
                    z_reference_vector.unknown_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "unknown"))
                    z_reference_vector.unknown_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "unknown"))
                    z_reference_vector.unknown_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "unknown"))
                    z_reference_vector.unknown_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "unknown"))

                    detail_object.z_reference_vectors.append(z_reference_vector)

def read_clusters(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    if LEVEL.level_body.clusters_tag_block.count > 0:
        cluster_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.clusters_tag_block.count, tag_node, "name", "clusters")
        LEVEL.clusters_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for cluster_idx in range(LEVEL.level_body.clusters_tag_block.count):
            cluster_element_node = None
            if XML_OUTPUT:
                cluster_element_node = TAG.xml_doc.createElement('element')
                cluster_element_node.setAttribute('index', str(cluster_idx))
                cluster_node.appendChild(cluster_element_node)

            cluster = LEVEL.Cluster()
            cluster.total_vertex_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "total vertex count"))
            cluster.total_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "total triangle count"))
            cluster.total_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "total part count"))
            cluster.shadow_casting_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "shadow casting triangle count"))
            cluster.shadow_casting_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "shadow casting part count"))
            cluster.opaque_point_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "opaque point count"))
            cluster.opaque_vertex_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "opaque vertex count"))
            cluster.opaque_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "opaque part count"))
            cluster.opaque_max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(cluster_element_node, "opaque max nodes vertex"))
            cluster.transparent_max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(cluster_element_node, "transparent max nodes vertex"))
            cluster.shadow_casting_rigid_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "shadow casting rigid triangle count"))
            cluster.geometry_classification = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "geometry classification", GeometryClassificationEnum))
            cluster.geometry_compression_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "geometry compression flags", GeometryCompressionFlags))
            cluster.compression_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_element_node, "compression info"))
            cluster.hardware_node_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(cluster_element_node, "hardware node count"))
            cluster.node_map_size = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(cluster_element_node, "node map size"))
            cluster.software_plane_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "software plane count"))
            cluster.total_subpart_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "total subpart count"))
            cluster.section_lighting_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "section lighting flags", SectionLightingFlags))
            cluster.block_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(cluster_element_node, "block offset"))
            cluster.block_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(cluster_element_node, "block size"))
            cluster.section_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(cluster_element_node, "section data size"))
            cluster.resource_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(cluster_element_node, "resource data size"))
            cluster.resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_element_node, "resources"))
            input_stream.read(4) # Padding?
            cluster.owner_tag_section_offset = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "owner tag section offset"))
            input_stream.read(6) # Padding?
            cluster.cluster_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_element_node, "cluster data"))
            cluster.bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(cluster_element_node, "bounds x"))
            cluster.bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(cluster_element_node, "bounds y"))
            cluster.bounds_z = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(cluster_element_node, "bounds z"))
            cluster.scenario_sky_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(cluster_element_node, "scenario sky index"))
            cluster.media_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(cluster_element_node, "media index"))
            cluster.scenario_visible_sky_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(cluster_element_node, "scenario visible sky index"))
            cluster.scenario_atmospheric_fog_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(cluster_element_node, "scenario atmospheric fog index"))
            cluster.planar_fog_designator = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(cluster_element_node, "planar fog designator"))
            cluster.visible_fog_plane_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(cluster_element_node, "visible fog plane index"))
            cluster.background_sound = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "background sound", None, LEVEL.level_body.background_sounds_palette_tag_block.count, "structure_bsp_background_sound_palette_block"))
            cluster.sound_environment = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "sound environment", None, LEVEL.level_body.sound_environment_palette_tag_block.count, "structure_bsp_sound_environment_palette_block"))
            cluster.weather = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "weather", None, LEVEL.level_body.weather_palette_tag_block.count, "structure_bsp_weather_palette_block"))
            cluster.transition_structure_bsp = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "transition structure bsp"))
            input_stream.read(6) # Padding?
            cluster.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(cluster_element_node, "flags", ClusterFlags))
            cluster.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_element_node, "predicted resources"))
            cluster.portals_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_element_node, "portals"))
            cluster.checksum_from_structure = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(cluster_element_node, "checksum from structure"))
            cluster.instanced_geometry_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_element_node, "instanced geometry indices"))
            cluster.index_reorder_table_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_element_node, "index reorder table"))
            cluster.collision_mopp_code_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(cluster_element_node, "collision mopp code"))

            LEVEL.clusters.append(cluster)

        for cluster_idx, cluster in enumerate(LEVEL.clusters):
            cluster_element_node = None
            if XML_OUTPUT:
                cluster_element_node = cluster_node.childNodes[cluster_idx]

            cluster.compression_info = []
            cluster.resources = []
            cluster.cluster_data = []
            cluster.predicted_resources = []
            cluster.portals = []
            cluster.instanced_geometry_indices = []
            cluster.index_reorder_table = []

            cluster.sinf_header = TAG.TagBlockHeader().read(input_stream, TAG)
            if cluster.compression_info_tag_block.count > 0:
                compression_info_node = tag_format.get_xml_node(XML_OUTPUT, cluster.compression_info_tag_block.count, cluster_element_node, "name", "compression info")
                cluster.compression_info_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for compression_info_idx in range(cluster.compression_info_tag_block.count):
                    compression_info_element_node = None
                    if XML_OUTPUT:
                        compression_info_element_node = TAG.xml_doc.createElement('element')
                        compression_info_element_node.setAttribute('index', str(compression_info_idx))
                        compression_info_node.appendChild(compression_info_element_node)

                    compression_info = LEVEL.CompressionInfo()
                    compression_info.position_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds x"))
                    compression_info.position_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds y"))
                    compression_info.position_bounds_z = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "position bounds z"))
                    compression_info.texcoord_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "texcoord bounds x"))
                    compression_info.texcoord_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "texcoord bounds y"))
                    compression_info.secondary_texcoord_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "secondary texcoord bounds x"))
                    compression_info.secondary_texcoord_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(compression_info_element_node, "secondary texcoord bounds y"))

                    cluster.compression_info.append(compression_info)

            cluster.blok_header = TAG.TagBlockHeader().read(input_stream, TAG)

            if cluster.resources_tag_block.count > 0:
                resources_node = tag_format.get_xml_node(XML_OUTPUT, cluster.resources_tag_block.count, cluster_element_node, "name", "resources")
                cluster.resources_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for resource_idx in range(cluster.resources_tag_block.count):
                    resource_element_node = None
                    if XML_OUTPUT:
                        resource_element_node = TAG.xml_doc.createElement('element')
                        resource_element_node.setAttribute('index', str(resource_idx))
                        resources_node.appendChild(resource_element_node)

                    resource = LEVEL.Resource()
                    resource.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "type", ResourceEnum))
                    input_stream.read(2) # Padding?
                    resource.primary_locator = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "primary locator"))
                    resource.secondary_locator = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(resource_element_node, "secondary locator"))
                    resource.resource_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource data size"))
                    resource.resource_data_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(resource_element_node, "resource data offset"))

                    cluster.resources.append(resource)

            if cluster.cluster_data_tag_block.count > 0:
                cluster_data_node = tag_format.get_xml_node(XML_OUTPUT, cluster.cluster_data_tag_block.count, cluster_element_node, "name", "cluster data")
                cluster.cluster_data_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for cluster_data_idx in range(cluster.cluster_data_tag_block.count):
                    cluster_data_element_node = None
                    if XML_OUTPUT:
                        cluster_data_element_node = TAG.xml_doc.createElement('element')
                        cluster_data_element_node.setAttribute('index', str(cluster_data_idx))
                        cluster_data_node.appendChild(cluster_data_element_node)

                    cluster_data = LEVEL.ClusterData()
                    cluster_data.parts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_data_element_node, "parts"))
                    cluster_data.subparts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_data_element_node, "subparts"))
                    cluster_data.visibility_bounds_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_data_element_node, "visibility bounds"))
                    cluster_data.raw_vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_data_element_node, "raw vertices"))
                    cluster_data.strip_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_data_element_node, "strip indices"))
                    cluster_data.visibility_mopp_code_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(cluster_data_element_node, "visibility mopp code"))
                    cluster_data.mopp_reorder_table_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_data_element_node, "mopp reorder table"))
                    cluster_data.vertex_buffers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(cluster_data_element_node, "vertex buffers"))
                    input_stream.read(4) # Padding?
                    cluster_data.sect_header = TAG.TagBlockHeader().read(input_stream, TAG)

                    cluster.cluster_data.append(cluster_data)

                for cluster_data_idx, cluster_data in enumerate(cluster.cluster_data):
                    cluster_data_element_node = None
                    if XML_OUTPUT:
                        cluster_data_element_node = cluster_data_node.childNodes[cluster_data_idx]

                    cluster_data.parts = []
                    cluster_data.subparts = []
                    cluster_data.visibility_bounds = []
                    cluster_data.raw_vertices = []
                    cluster_data.strip_indices = []
                    cluster_data.mopp_reorder_table = []
                    cluster_data.vertex_buffers = []
                    if cluster_data.parts_tag_block.count > 0:
                        parts_node = tag_format.get_xml_node(XML_OUTPUT, cluster_data.parts_tag_block.count, cluster_data_element_node, "name", "parts")
                        cluster_data.parts_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for part_idx in range(cluster_data.parts_tag_block.count):
                            part_element_node = None
                            if XML_OUTPUT:
                                part_element_node = TAG.xml_doc.createElement('element')
                                part_element_node.setAttribute('index', str(part_idx))
                                parts_node.appendChild(part_element_node)

                            part = LEVEL.Part()
                            part.part_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(part_element_node, "type", PartTypeEnum))
                            part.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(part_element_node, "flags", PartFlags))
                            part.material_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(part_element_node, "material", None, LEVEL.level_body.materials_tag_block.count, "material"))
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

                            cluster_data.parts.append(part)

                    if cluster_data.subparts_tag_block.count > 0:
                        subparts_node = tag_format.get_xml_node(XML_OUTPUT, cluster_data.subparts_tag_block.count, cluster_data_element_node, "name", "subparts")
                        cluster_data.subparts_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for subpart_idx in range(cluster_data.subparts_tag_block.count):
                            subpart_element_node = None
                            if XML_OUTPUT:
                                subpart_element_node = TAG.xml_doc.createElement('element')
                                subpart_element_node.setAttribute('index', str(subpart_idx))
                                subparts_node.appendChild(subpart_element_node)

                            sub_part = LEVEL.SubPart()
                            sub_part.indices_start_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subpart_element_node, "indices start index"))
                            sub_part.indices_length = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subpart_element_node, "indices length"))
                            sub_part.visibility_bounds_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subpart_element_node, "visibility bounds index"))
                            sub_part.part_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(subpart_element_node, "part index"))

                            cluster_data.subparts.append(sub_part)

                    if cluster_data.visibility_bounds_tag_block.count > 0:
                        visibility_bounds_node = tag_format.get_xml_node(XML_OUTPUT, cluster_data.visibility_bounds_tag_block.count, cluster_data_element_node, "name", "visibility bounds")
                        cluster_data.subparts_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for visibility_bound_idx in range(cluster_data.visibility_bounds_tag_block.count):
                            visibility_bound_element_node = None
                            if XML_OUTPUT:
                                visibility_bound_element_node = TAG.xml_doc.createElement('element')
                                visibility_bound_element_node.setAttribute('index', str(visibility_bound_idx))
                                visibility_bounds_node.appendChild(visibility_bound_element_node)

                            visibility_bound = LEVEL.VisibilityBounds()
                            visibility_bound.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(visibility_bound_element_node, "position"))
                            visibility_bound.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(visibility_bound_element_node, "radius"))
                            visibility_bound.node_0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(visibility_bound_element_node, "node 0"))
                            input_stream.read(2) # Padding?

                            cluster_data.visibility_bounds.append(visibility_bound)

                    if cluster_data.raw_vertices_tag_block.count > 0:
                        raw_vertices_node = tag_format.get_xml_node(XML_OUTPUT, cluster_data.raw_vertices_tag_block.count, cluster_data_element_node, "name", "raw vertices")
                        cluster_data.raw_vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for raw_vertex_idx in range(cluster_data.raw_vertices_tag_block.count):
                            raw_vertex_element_node = None
                            if XML_OUTPUT:
                                raw_vertex_element_node = TAG.xml_doc.createElement('element')
                                raw_vertex_element_node.setAttribute('index', str(raw_vertex_idx))
                                raw_vertices_node.appendChild(raw_vertex_element_node)

                            raw_vertex = LEVEL.RawVertex()
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

                            cluster_data.raw_vertices.append(raw_vertex)

                    if cluster_data.strip_indices_tag_block.count > 0:
                        strip_indices_node = tag_format.get_xml_node(XML_OUTPUT, cluster_data.strip_indices_tag_block.count, cluster_data_element_node, "name", "strip indices")
                        cluster_data.strip_indices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for strip_index_idx in range(cluster_data.strip_indices_tag_block.count):
                            strip_index_element_node = None
                            if XML_OUTPUT:
                                strip_index_element_node = TAG.xml_doc.createElement('element')
                                strip_index_element_node.setAttribute('index', str(strip_index_idx))
                                strip_indices_node.appendChild(strip_index_element_node)

                            cluster_data.strip_indices.append(TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(strip_index_element_node, "index")))

                    cluster_data.visibility_mopp_code = input_stream.read(cluster_data.visibility_mopp_code_data.size)

                    if cluster_data.mopp_reorder_table_tag_block.count > 0:
                        mopp_reorder_table_node = tag_format.get_xml_node(XML_OUTPUT, cluster_data.mopp_reorder_table_tag_block.count, cluster_data_element_node, "name", "mopp reorder table")
                        cluster_data.mopp_reorder_table_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for mopp_reorder_table_idx in range(cluster_data.mopp_reorder_table_tag_block.count):
                            mopp_reorder_table_element_node = None
                            if XML_OUTPUT:
                                mopp_reorder_table_element_node = TAG.xml_doc.createElement('element')
                                mopp_reorder_table_element_node.setAttribute('index', str(mopp_reorder_table_idx))
                                mopp_reorder_table_node.appendChild(mopp_reorder_table_element_node)

                            cluster_data.mopp_reorder_table.append(TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(mopp_reorder_table_element_node, "index")))

                    if cluster_data.vertex_buffers_tag_block.count > 0:
                        vertex_buffers_node = tag_format.get_xml_node(XML_OUTPUT, cluster_data.vertex_buffers_tag_block.count, cluster_data_element_node, "name", "vertex buffers")
                        cluster_data.mopp_reorder_table_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for vertex_buffer_idx in range(cluster_data.vertex_buffers_tag_block.count):
                            vertex_buffer_element_node = None
                            if XML_OUTPUT:
                                vertex_buffer_element_node = TAG.xml_doc.createElement('element')
                                vertex_buffer_element_node.setAttribute('index', str(vertex_buffer_idx))
                                vertex_buffers_node.appendChild(vertex_buffer_element_node)

                            input_stream.read(32) # Padding?

            if cluster.predicted_resources_tag_block.count > 0:
                predicted_resource_node = tag_format.get_xml_node(XML_OUTPUT, cluster.predicted_resources_tag_block.count, cluster_element_node, "name", "predicted resources")
                cluster.predicted_resources_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for predicted_resource_idx in range(cluster.predicted_resources_tag_block.count):
                    predicted_resource_element_node = None
                    if XML_OUTPUT:
                        predicted_resource_element_node = TAG.xml_doc.createElement('element')
                        predicted_resource_element_node.setAttribute('index', str(predicted_resource_idx))
                        predicted_resource_node.appendChild(predicted_resource_element_node)

                    predicted_resource = LEVEL.PredictedResource()
                    predicted_resource.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(predicted_resource_element_node, "type", PredictedResourceTypeEnum))
                    predicted_resource.resource_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(predicted_resource_element_node, "resource index"))
                    predicted_resource.tag_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(predicted_resource_element_node, "tag index"))

                    cluster.predicted_resources.append(predicted_resource)

            if cluster.predicted_resources_tag_block.count > 0:
                predicted_resource_node = tag_format.get_xml_node(XML_OUTPUT, cluster.predicted_resources_tag_block.count, cluster_element_node, "name", "predicted resources")
                cluster.predicted_resources_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for predicted_resource_idx in range(cluster.predicted_resources_tag_block.count):
                    predicted_resource_element_node = None
                    if XML_OUTPUT:
                        predicted_resource_element_node = TAG.xml_doc.createElement('element')
                        predicted_resource_element_node.setAttribute('index', str(predicted_resource_idx))
                        predicted_resource_node.appendChild(predicted_resource_element_node)

                    predicted_resource = LEVEL.PredictedResource()
                    predicted_resource.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(predicted_resource_element_node, "type", PredictedResourceTypeEnum))
                    predicted_resource.resource_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(predicted_resource_element_node, "resource index"))
                    predicted_resource.tag_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(predicted_resource_element_node, "tag index"))

                    cluster.predicted_resources.append(predicted_resource)

            if cluster.portals_tag_block.count > 0:
                portal_node = tag_format.get_xml_node(XML_OUTPUT, cluster.portals_tag_block.count, cluster_element_node, "name", "portals")
                cluster.portals_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for portal_idx in range(cluster.portals_tag_block.count):
                    portal_element_node = None
                    if XML_OUTPUT:
                        portal_element_node = TAG.xml_doc.createElement('element')
                        portal_element_node.setAttribute('index', str(portal_idx))
                        portal_node.appendChild(portal_element_node)

                    cluster.portals.append(TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(portal_element_node, "portal index")))

            if cluster.instanced_geometry_indices_tag_block.count > 0:
                instanced_geometry_indices_node = tag_format.get_xml_node(XML_OUTPUT, cluster.instanced_geometry_indices_tag_block.count, cluster_element_node, "name", "instanced geometry indices")
                cluster.instanced_geometry_indices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for instanced_geometry_idx in range(cluster.instanced_geometry_indices_tag_block.count):
                    instanced_geometry_element_node = None
                    if XML_OUTPUT:
                        instanced_geometry_element_node = TAG.xml_doc.createElement('element')
                        instanced_geometry_element_node.setAttribute('index', str(instanced_geometry_idx))
                        instanced_geometry_indices_node.appendChild(instanced_geometry_element_node)

                    cluster.instanced_geometry_indices.append(TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_element_node, "instanced geometry index")))

            if cluster.index_reorder_table_tag_block.count > 0:
                index_reorder_table_node = tag_format.get_xml_node(XML_OUTPUT, cluster.index_reorder_table_tag_block.count, cluster_element_node, "name", "index reorder table")
                cluster.index_reorder_table_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for index_reorder_table_idx in range(cluster.index_reorder_table_tag_block.count):
                    index_reorder_table_element_node = None
                    if XML_OUTPUT:
                        index_reorder_table_element_node = TAG.xml_doc.createElement('element')
                        index_reorder_table_element_node.setAttribute('index', str(index_reorder_table_idx))
                        index_reorder_table_node.appendChild(index_reorder_table_element_node)

                    cluster.instanced_geometry_indices.append(TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(index_reorder_table_element_node, "index")))

            cluster.collision_mopp_code = input_stream.read(cluster.collision_mopp_code_data.size)

def read_materials(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    if LEVEL.level_body.materials_tag_block.count > 0:
        material_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.materials_tag_block.count, tag_node, "name", "materials")
        LEVEL.material_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for material_idx in range(LEVEL.level_body.materials_tag_block.count):
            material_element_node = None
            if XML_OUTPUT:
                material_element_node = TAG.xml_doc.createElement('element')
                material_element_node.setAttribute('index', str(material_idx))
                material_node.appendChild(material_element_node)

            material = LEVEL.Material()
            material.old_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(material_element_node, "old shader"))
            material.shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(material_element_node, "shader"))
            material.properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(material_element_node, "properties"))
            input_stream.read(4) # Padding?
            material.breakable_surface_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(material_element_node, "breakable surface index"))
            input_stream.read(3) # Padding?

            LEVEL.materials.append(material)

        for material_idx, material in enumerate(LEVEL.materials):
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

                    property = LEVEL.Property()
                    property.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(property_element_node, "type", PropertyTypeEnum))
                    property.int_value = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(property_element_node, "int value"))
                    property.real_value = TAG.read_float(input_stream, TAG, tag_format.XMLData(property_element_node, "real value"))

                    material.properties.append(property)

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
    read_unused_nodes(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)
    read_leaves(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)
    read_surface_references(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)
    LEVEL.cluster_data = input_stream.read(LEVEL.level_body.cluster_raw_data.size)
    read_cluster_portals(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)
    read_fog_planes(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)
    read_weather_palette(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)
    read_weather_polyhedra(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)
    read_detail_objects(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)
    read_clusters(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)
    read_materials(LEVEL, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, LEVEL.header.tag_group, TAG.is_legacy, True)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return LEVEL
