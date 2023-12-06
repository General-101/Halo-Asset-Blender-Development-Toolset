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
        PropertyTypeEnum,
        PathfindingSectorFlags,
        LinkFlags,
        ObjectRefFlags,
        NodeFlags,
        HintTypeEnum,
        GeometryFlags,
        ForceJumpHeightEnum,
        JumpControlFlags,
        HintFlags,
        WellTypeEnum,
        BackgroundScaleFlags,
        ReportTypeEnum,
        ReportFlags,
        LightTypeEnum,
        InstanceFlags,
        PathfindingPolicyEnum,
        LightmappingPolicyEnum
        )

XML_OUTPUT = False

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
    LEVEL.detail_objects = []
    LEVEL.clusters = []
    LEVEL.materials = []
    LEVEL.sky_owner_cluster = []
    LEVEL.conveyor_surfaces = []
    LEVEL.breakable_surfaces = []
    LEVEL.pathfinding_data = []
    LEVEL.pathfinding_edges = []
    LEVEL.background_sound_palette = []
    LEVEL.sound_environment_palette = []
    LEVEL.markers = []
    LEVEL.runtime_decals = []
    LEVEL.environment_object_palette = []
    LEVEL.environment_objects = []
    LEVEL.lightmaps = []
    LEVEL.leaf_map_leaves = []
    LEVEL.leaf_map_connections = []
    LEVEL.errors = []
    LEVEL.precomputed_lighting = []
    LEVEL.instanced_geometry_definition = []
    LEVEL.instanced_geometry_instances = []

def read_bsp_body(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
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
    LEVEL.level_body.conveyor_surfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "conveyor surfaces"))
    LEVEL.level_body.breakable_surfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "breakable surfaces"))
    LEVEL.level_body.pathfinding_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "pathfinding data"))
    LEVEL.level_body.pathfinding_edges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "pathfinding edges"))
    LEVEL.level_body.background_sound_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "background sound palette"))
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
    LEVEL.level_body.instanced_geometry_definition_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "instanced geometry definition"))
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

def read_import_info(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
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

                    import_info.files.append(file)

                for file_idx, file in enumerate(import_info.files):
                    file_element_node = None
                    if XML_OUTPUT:
                        file_element_node = files_node.childNodes[file_idx]

                    file.uncompressed_data = input_stream.read(file.zipped_data)

def read_collision_materials(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
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

def read_collision_bsps(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
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

def read_unused_nodes(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
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

def read_leaves(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
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

def read_surface_references(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
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

def read_cluster_portals(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
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

def read_fog_planes(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
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

def read_weather_palette(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
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
            input_stream.read(36) # Padding?
            weather_palette.wind = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "wind"))
            weather_palette.wind_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "wind direction"))
            weather_palette.wind_magnitude = TAG.read_float(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "wind magnitude"))
            input_stream.read(4) # Padding?
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

def read_weather_polyhedra(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
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

def read_detail_objects(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
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

                    unknown = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(count_element_node, "unknown"))
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
                    z_reference_vector.unknown_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(z_reference_vector_element_node, "unknown"))
                    z_reference_vector.unknown_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(z_reference_vector_element_node, "unknown"))
                    z_reference_vector.unknown_2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(z_reference_vector_element_node, "unknown"))
                    z_reference_vector.unknown_3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(z_reference_vector_element_node, "unknown"))

                    detail_object.z_reference_vectors.append(z_reference_vector)

def read_clusters(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
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
            cluster.background_sound = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(cluster_element_node, "background sound", None, LEVEL.level_body.background_sound_palette_tag_block.count, "structure_bsp_background_sound_palette_block"))
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

def read_materials(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
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

def read_sky_owner_cluster(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.sky_owner_cluster_tag_block.count > 0:
        sky_owner_cluster_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.sky_owner_cluster_tag_block.count, tag_node, "name", "sky owner cluster")
        LEVEL.conveyor_surfaces_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for sky_owner_cluster_idx in range(LEVEL.level_body.sky_owner_cluster_tag_block.count):
            sky_owner_cluster_element_node = None
            if XML_OUTPUT:
                sky_owner_cluster_element_node = TAG.xml_doc.createElement('element')
                sky_owner_cluster_element_node.setAttribute('index', str(sky_owner_cluster_idx))
                sky_owner_cluster_node.appendChild(sky_owner_cluster_element_node)

            LEVEL.sky_owner_cluster.append(TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(sky_owner_cluster_element_node, "cluster owner")))

def read_conveyor_surfaces(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.conveyor_surfaces_tag_block.count > 0:
        conveyor_surface_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.conveyor_surfaces_tag_block.count, tag_node, "name", "conveyor surfaces")
        LEVEL.conveyor_surfaces_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for conveyor_surface_idx in range(LEVEL.level_body.conveyor_surfaces_tag_block.count):
            conveyor_surface_element_node = None
            if XML_OUTPUT:
                conveyor_surface_element_node = TAG.xml_doc.createElement('element')
                conveyor_surface_element_node.setAttribute('index', str(conveyor_surface_idx))
                conveyor_surface_node.appendChild(conveyor_surface_element_node)

            conveyor_surface = LEVEL.ConveyorSurface()
            conveyor_surface.u = TAG.read_vector(input_stream, TAG, tag_format.XMLData(conveyor_surface_element_node, "u"))
            conveyor_surface.v = TAG.read_vector(input_stream, TAG, tag_format.XMLData(conveyor_surface_element_node, "v"))

            LEVEL.conveyor_surfaces.append(conveyor_surface)

def read_breakable_surfaces(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.breakable_surfaces_tag_block.count > 0:
        breakable_surface_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.breakable_surfaces_tag_block.count, tag_node, "name", "breakable surfaces")
        LEVEL.breakable_surfaces_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for breakable_surface_idx in range(LEVEL.level_body.breakable_surfaces_tag_block.count):
            breakable_surface_element_node = None
            if XML_OUTPUT:
                breakable_surface_element_node = TAG.xml_doc.createElement('element')
                breakable_surface_element_node.setAttribute('index', str(breakable_surface_idx))
                breakable_surface_node.appendChild(breakable_surface_element_node)

            breakable_surface = LEVEL.BreakableSurface()
            breakable_surface.instanced_geometry_instance = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(breakable_surface_element_node, "instanced geometry instance", None, LEVEL.level_body.instanced_geometry_instances_tag_block.count, "structure_bsp_instanced_geometry_instances_block"))
            breakable_surface.breakable_surface_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(breakable_surface_element_node, "breakable surface index"))
            breakable_surface.centroid = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(breakable_surface_element_node, "centroid"))
            breakable_surface.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(breakable_surface_element_node, "radius"))
            breakable_surface.collision_surface_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(breakable_surface_element_node, "collision surface index"))

            LEVEL.breakable_surfaces.append(breakable_surface)

def read_pathfinding_data(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.pathfinding_data_tag_block.count > 0:
        LEVEL.pathfinding_data_header = TAG.TagBlockHeader().read(input_stream, TAG)
        pathfinding_data_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.pathfinding_data_tag_block.count, tag_node, "name", "pathfinding data")
        for pathfinding_data_idx in range(LEVEL.level_body.pathfinding_data_tag_block.count):
            pathfinding_data_element_node = None
            if XML_OUTPUT:
                pathfinding_data_element_node = TAG.xml_doc.createElement('element')
                pathfinding_data_element_node.setAttribute('index', str(pathfinding_data_idx))
                pathfinding_data_node.appendChild(pathfinding_data_element_node)

            pathfinding_data = LEVEL.AIPathfindingData()
            pathfinding_data.sectors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(pathfinding_data_element_node, "sectors"))
            pathfinding_data.links_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(pathfinding_data_element_node, "links"))
            pathfinding_data.refs_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(pathfinding_data_element_node, "refs"))
            pathfinding_data.bsp2d_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(pathfinding_data_element_node, "bsp2d nodes"))
            pathfinding_data.surface_flags_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(pathfinding_data_element_node, "surface flags"))
            pathfinding_data.vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(pathfinding_data_element_node, "vertices"))
            pathfinding_data.object_refs_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(pathfinding_data_element_node, "object refs"))
            pathfinding_data.pathfinding_hints_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(pathfinding_data_element_node, "pathfinding hints"))
            pathfinding_data.instanced_geometry_refs_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(pathfinding_data_element_node, "instanced geometry refs"))
            pathfinding_data.structure_checksum = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(pathfinding_data_element_node, "structure checksum"))
            input_stream.read(32) # Padding?
            pathfinding_data.user_placed_hints_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(pathfinding_data_element_node, "user placed hints"))

            LEVEL.pathfinding_data.append(pathfinding_data)

        for pathfinding_data_idx, pathfinding_data in enumerate(LEVEL.pathfinding_data):
            pathfinding_data_element_node = None
            if XML_OUTPUT:
                pathfinding_data_element_node = pathfinding_data_node.childNodes[pathfinding_data_idx]

            pathfinding_data.sectors = []
            pathfinding_data.links = []
            pathfinding_data.refs = []
            pathfinding_data.bsp2d_nodes = []
            pathfinding_data.surface_flags = []
            pathfinding_data.vertices = []
            pathfinding_data.object_refs = []
            pathfinding_data.pathfinding_hints = []
            pathfinding_data.instanced_geometry_refs = []
            pathfinding_data.user_placed_hints = []
            if pathfinding_data.sectors_tag_block.count > 0:
                pathfinding_data.sectors_header = TAG.TagBlockHeader().read(input_stream, TAG)
                sector_node = tag_format.get_xml_node(XML_OUTPUT, pathfinding_data.sectors_tag_block.count, pathfinding_data_element_node, "name", "sectors")
                for sector_idx in range(pathfinding_data.sectors_tag_block.count):
                    sector_element_node = None
                    if XML_OUTPUT:
                        sector_element_node = TAG.xml_doc.createElement('element')
                        sector_element_node.setAttribute('index', str(sector_idx))
                        sector_node.appendChild(sector_element_node)

                    sector = LEVEL.Sector()

                    sector.pathfinding_sector_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(sector_element_node, "pathfinding sector flags", PathfindingSectorFlags))
                    sector.hint_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(sector_element_node, "hint index"))
                    sector.first_link = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(sector_element_node, "first link"))

                    pathfinding_data.sectors.append(sector)

            if pathfinding_data.links_tag_block.count > 0:
                pathfinding_data.links_header = TAG.TagBlockHeader().read(input_stream, TAG)
                link_node = tag_format.get_xml_node(XML_OUTPUT, pathfinding_data.links_tag_block.count, pathfinding_data_element_node, "name", "links")
                for link_idx in range(pathfinding_data.links_tag_block.count):
                    link_element_node = None
                    if XML_OUTPUT:
                        link_element_node = TAG.xml_doc.createElement('element')
                        link_element_node.setAttribute('index', str(link_idx))
                        link_node.appendChild(link_element_node)

                    link = LEVEL.Link()

                    link.vertex_1 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(link_element_node, "vertex 1"))
                    link.vertex_2 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(link_element_node, "vertex 2"))
                    link.link_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(link_element_node, "link flags", LinkFlags))
                    link.hint_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(link_element_node, "hint index"))
                    link.forward_link = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(link_element_node, "forward link"))
                    link.reverse_link = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(link_element_node, "reverse link"))
                    link.left_sector = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(link_element_node, "left sector"))
                    link.right_sector = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(link_element_node, "right sector"))

                    pathfinding_data.links.append(link)

            if pathfinding_data.refs_tag_block.count > 0:
                pathfinding_data.refs_header = TAG.TagBlockHeader().read(input_stream, TAG)
                ref_node = tag_format.get_xml_node(XML_OUTPUT, pathfinding_data.refs_tag_block.count, pathfinding_data_element_node, "name", "refs")
                for ref_idx in range(pathfinding_data.refs_tag_block.count):
                    ref_element_node = None
                    if XML_OUTPUT:
                        ref_element_node = TAG.xml_doc.createElement('element')
                        ref_element_node.setAttribute('index', str(ref_idx))
                        ref_node.appendChild(ref_element_node)

                    pathfinding_data.refs.append(TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(ref_element_node, "node ref or sector ref")))

            if pathfinding_data.bsp2d_nodes_tag_block.count > 0:
                pathfinding_data.bsp2d_nodes_header = TAG.TagBlockHeader().read(input_stream, TAG)
                bsp2d_node = tag_format.get_xml_node(XML_OUTPUT, pathfinding_data.bsp2d_nodes_tag_block.count, pathfinding_data_element_node, "name", "bsp2d nodes")
                for bsp2d_idx in range(pathfinding_data.bsp2d_nodes_tag_block.count):
                    bsp2d_element_node = None
                    if XML_OUTPUT:
                        bsp2d_element_node = TAG.xml_doc.createElement('element')
                        bsp2d_element_node.setAttribute('index', str(bsp2d_idx))
                        bsp2d_node.appendChild(bsp2d_element_node)

                    bsp2d_node = LEVEL.Bsp2DNode()

                    bsp2d_node.plane = TAG.Plane2D().read(input_stream, TAG, tag_format.XMLData(bsp2d_element_node, "plane"))
                    bsp2d_node.left_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp2d_element_node, "left child"))
                    bsp2d_node.right_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp2d_element_node, "right child"))

                    pathfinding_data.bsp2d_nodes.append(bsp2d_node)

            if pathfinding_data.surface_flags_tag_block.count > 0:
                pathfinding_data.surface_flags_header = TAG.TagBlockHeader().read(input_stream, TAG)
                surface_flags_node = tag_format.get_xml_node(XML_OUTPUT, pathfinding_data.surface_flags_tag_block.count, pathfinding_data_element_node, "name", "surface flags")
                for surface_flags_idx in range(pathfinding_data.surface_flags_tag_block.count):
                    surface_flags_element_node = None
                    if XML_OUTPUT:
                        surface_flags_element_node = TAG.xml_doc.createElement('element')
                        surface_flags_element_node.setAttribute('index', str(surface_flags_idx))
                        surface_flags_node.appendChild(surface_flags_element_node)

                    pathfinding_data.surface_flags.append(TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_flags_element_node, "flags")))

            if pathfinding_data.vertices_tag_block.count > 0:
                pathfinding_data.vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                vertices_node = tag_format.get_xml_node(XML_OUTPUT, pathfinding_data.vertices_tag_block.count, pathfinding_data_element_node, "name", "vertices")
                for vertex_idx in range(pathfinding_data.vertices_tag_block.count):
                    vertex_element_node = None
                    if XML_OUTPUT:
                        vertex_element_node = TAG.xml_doc.createElement('element')
                        vertex_element_node.setAttribute('index', str(vertex_idx))
                        vertices_node.appendChild(vertex_element_node)

                    pathfinding_data.vertices.append(TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(vertex_element_node, "position")))

            if pathfinding_data.object_refs_tag_block.count > 0:
                pathfinding_data.object_refs_header = TAG.TagBlockHeader().read(input_stream, TAG)
                object_refs_node = tag_format.get_xml_node(XML_OUTPUT, pathfinding_data.object_refs_tag_block.count, pathfinding_data_element_node, "name", "object refs")
                for object_ref_idx in range(pathfinding_data.object_refs_tag_block.count):
                    object_ref_element_node = None
                    if XML_OUTPUT:
                        object_ref_element_node = TAG.xml_doc.createElement('element')
                        object_ref_element_node.setAttribute('index', str(object_ref_idx))
                        object_refs_node.appendChild(object_ref_element_node)

                    object_ref = LEVEL.ObjectRef()

                    object_ref.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(object_ref_element_node, "flags", ObjectRefFlags))
                    object_ref.first_sector = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(object_ref_element_node, "first sector"))
                    object_ref.last_sector = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(object_ref_element_node, "last sector"))
                    object_ref.bsps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(object_ref_element_node, "bsps"))
                    object_ref.nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(object_ref_element_node, "nodes"))

                    pathfinding_data.object_refs.append(object_ref)

                for object_ref_idx, object_ref in enumerate(pathfinding_data.object_refs):
                    object_ref_element_node = None
                    if XML_OUTPUT:
                        object_ref_element_node = object_refs_node.childNodes[object_ref_idx]

                    object_ref.bsps = []
                    object_ref.nodes = []
                    if object_ref.bsps_tag_block.count > 0:
                        object_ref.bsps_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        bsp_node = tag_format.get_xml_node(XML_OUTPUT, object_ref.bsps_tag_block.count, object_ref_element_node, "name", "bsps")
                        for bsp_idx in range(object_ref.bsps_tag_block.count):
                            bsp_element_node = None
                            if XML_OUTPUT:
                                bsp_element_node = TAG.xml_doc.createElement('element')
                                bsp_element_node.setAttribute('index', str(bsp_idx))
                                bsp_node.appendChild(bsp_element_node)

                            bsp = LEVEL.BSP()

                            bsp.bsp_reference = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp_element_node, "bsp reference"))
                            bsp.first_sector = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp_element_node, "first sector"))
                            bsp.last_sector = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp_element_node, "last sector"))
                            bsp.node_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp_element_node, "node index"))
                            input_stream.read(2) # Padding?

                            object_ref.bsps.append(bsp)

                    if object_ref.nodes_tag_block.count > 0:
                        object_ref.nodes_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        node_node = tag_format.get_xml_node(XML_OUTPUT, object_ref.nodes_tag_block.count, object_ref_element_node, "name", "nodes")
                        for node_idx in range(object_ref.nodes_tag_block.count):
                            node_element_node = None
                            if XML_OUTPUT:
                                node_element_node = TAG.xml_doc.createElement('element')
                                node_element_node.setAttribute('index', str(node_idx))
                                node_node.appendChild(node_element_node)

                            node = LEVEL.Node()

                            node.reference_frame_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element_node, "reference frame index"))
                            node.projection_axis = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element_node, "projection axis"))
                            node.projection_sign = TAG.read_flag_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element_node, "projection sign", NodeFlags))

                            object_ref.nodes.append(node)

            if pathfinding_data.pathfinding_hints_tag_block.count > 0:
                pathfinding_data.pathfinding_hints_header = TAG.TagBlockHeader().read(input_stream, TAG)
                pathfinding_hint_node = tag_format.get_xml_node(XML_OUTPUT, pathfinding_data.pathfinding_hints_tag_block.count, pathfinding_data_element_node, "name", "pathfinding hints")
                for pathfinding_hint_idx in range(pathfinding_data.pathfinding_hints_tag_block.count):
                    pathfinding_hint_element_node = None
                    if XML_OUTPUT:
                        pathfinding_hint_element_node = TAG.xml_doc.createElement('element')
                        pathfinding_hint_element_node.setAttribute('index', str(pathfinding_hint_idx))
                        pathfinding_hint_node.appendChild(pathfinding_hint_element_node)

                    pathfinding_hint = LEVEL.PathfindingHint()

                    pathfinding_hint.hint_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(pathfinding_hint_element_node, "hint type", HintTypeEnum))
                    pathfinding_hint.next_hint_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_hint_element_node, "next hint index"))
                    pathfinding_hint.hint_data_0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_hint_element_node, "hint data 0"))
                    pathfinding_hint.hint_data_1 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_hint_element_node, "hint data 1"))
                    pathfinding_hint.hint_data_2 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_hint_element_node, "hint data 2"))
                    pathfinding_hint.hint_data_3 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_hint_element_node, "hint data 3"))
                    pathfinding_hint.hint_data_4 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_hint_element_node, "hint data 4"))
                    pathfinding_hint.hint_data_5 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_hint_element_node, "hint data 5"))
                    pathfinding_hint.hint_data_6 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_hint_element_node, "hint data 6"))
                    pathfinding_hint.hint_data_7 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_hint_element_node, "hint data 7"))

                    pathfinding_data.pathfinding_hints.append(pathfinding_hint)

            if pathfinding_data.instanced_geometry_refs_tag_block.count > 0:
                pathfinding_data.instanced_geometry_refs_header = TAG.TagBlockHeader().read(input_stream, TAG)
                instanced_geometry_ref_node = tag_format.get_xml_node(XML_OUTPUT, pathfinding_data.instanced_geometry_refs_tag_block.count, pathfinding_data_element_node, "name", "instanced geometry refs")
                for instanced_geometry_ref_idx in range(pathfinding_data.instanced_geometry_refs_tag_block.count):
                    instanced_geometry_ref_element_node = None
                    if XML_OUTPUT:
                        instanced_geometry_ref_element_node = TAG.xml_doc.createElement('element')
                        instanced_geometry_ref_element_node.setAttribute('index', str(instanced_geometry_ref_idx))
                        instanced_geometry_ref_node.appendChild(instanced_geometry_ref_element_node)

                    pathfinding_data.instanced_geometry_refs.append(TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_ref_element_node, "pathfinding_object_index")))
                    input_stream.read(2) # Padding?

            if pathfinding_data.user_placed_hints_tag_block.count > 0:
                pathfinding_data.user_placed_hints_header = TAG.TagBlockHeader().read(input_stream, TAG)
                user_placed_hint_node = tag_format.get_xml_node(XML_OUTPUT, pathfinding_data.user_placed_hints_tag_block.count, pathfinding_data_element_node, "name", "user placed hints")
                for user_placed_hint_idx in range(pathfinding_data.user_placed_hints_tag_block.count):
                    user_placed_hint_element_node = None
                    if XML_OUTPUT:
                        user_placed_hint_element_node = TAG.xml_doc.createElement('element')
                        user_placed_hint_element_node.setAttribute('index', str(user_placed_hint_idx))
                        user_placed_hint_node.appendChild(user_placed_hint_element_node)

                    user_placed_hint = LEVEL.UserPlacedHint()

                    user_placed_hint.point_geometry_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(user_placed_hint_element_node, "point geometry"))
                    user_placed_hint.ray_geometry_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(user_placed_hint_element_node, "ray geometry"))
                    user_placed_hint.line_segment_geometry_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(user_placed_hint_element_node, "line segment geometry"))
                    user_placed_hint.parallelogram_geometry_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(user_placed_hint_element_node, "parallelogram geometry"))
                    user_placed_hint.polygon_geometry_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(user_placed_hint_element_node, "polygon geometry"))
                    user_placed_hint.jump_hints_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(user_placed_hint_element_node, "jump hints"))
                    user_placed_hint.climb_hints_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(user_placed_hint_element_node, "climb hints"))
                    user_placed_hint.well_hints_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(user_placed_hint_element_node, "well hints"))
                    user_placed_hint.flight_hints_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(user_placed_hint_element_node, "flight hints"))

                    pathfinding_data.user_placed_hints.append(user_placed_hint)

                for user_placed_hint_idx, user_placed_hint in enumerate(pathfinding_data.user_placed_hints):
                    user_placed_hint_element_node = None
                    if XML_OUTPUT:
                        user_placed_hint_element_node = user_placed_hint_node.childNodes[user_placed_hint_idx]

                    user_placed_hint.point_geometry = []
                    user_placed_hint.ray_geometry = []
                    user_placed_hint.line_segment_geometry = []
                    user_placed_hint.parallelogram_geometry = []
                    user_placed_hint.polygon_geometry = []
                    user_placed_hint.jump_hints = []
                    user_placed_hint.climb_hints = []
                    user_placed_hint.well_hints = []
                    user_placed_hint.flight_hints = []
                    if user_placed_hint.point_geometry_tag_block.count > 0:
                        user_placed_hint.point_geometry_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        point_geometry_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.point_geometry_tag_block.count, user_placed_hint_element_node, "name", "point geometry")
                        for point_geometry_idx in range(user_placed_hint.point_geometry_tag_block.count):
                            point_geometry_element_node = None
                            if XML_OUTPUT:
                                point_geometry_element_node = TAG.xml_doc.createElement('element')
                                point_geometry_element_node.setAttribute('index', str(point_geometry_idx))
                                point_geometry_node.appendChild(point_geometry_element_node)

                            point_geometry = LEVEL.PointGeometry()

                            point_geometry.point = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(point_geometry_element_node, "point"))
                            point_geometry.reference_frame = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(point_geometry_element_node, "reference frame"))
                            input_stream.read(2) # Padding?

                            user_placed_hint.point_geometry.append(point_geometry)

                    if user_placed_hint.ray_geometry_tag_block.count > 0:
                        user_placed_hint.ray_geometry_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        ray_geometry_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.ray_geometry_tag_block.count, user_placed_hint_element_node, "name", "ray geometry")
                        for ray_geometry_idx in range(user_placed_hint.ray_geometry_tag_block.count):
                            ray_geometry_element_node = None
                            if XML_OUTPUT:
                                ray_geometry_element_node = TAG.xml_doc.createElement('element')
                                ray_geometry_element_node.setAttribute('index', str(ray_geometry_idx))
                                ray_geometry_node.appendChild(ray_geometry_element_node)

                            ray_geometry = LEVEL.RayGeometry()

                            ray_geometry.point = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(ray_geometry_element_node, "point"))
                            ray_geometry.reference_frame = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(ray_geometry_element_node, "reference frame"))
                            input_stream.read(2) # Padding?
                            ray_geometry.vector = TAG.read_vector(input_stream, TAG,  tag_format.XMLData(ray_geometry_element_node, "vector"))

                            user_placed_hint.ray_geometry.append(ray_geometry)

                    if user_placed_hint.line_segment_geometry_tag_block.count > 0:
                        user_placed_hint.line_segment_geometry_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        line_segment_geometry_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.line_segment_geometry_tag_block.count, user_placed_hint_element_node, "name", "line segment geometry")
                        for line_segment_geometry_idx in range(user_placed_hint.line_segment_geometry_tag_block.count):
                            line_segment_geometry_element_node = None
                            if XML_OUTPUT:
                                line_segment_geometry_element_node = TAG.xml_doc.createElement('element')
                                line_segment_geometry_element_node.setAttribute('index', str(line_segment_geometry_idx))
                                line_segment_geometry_node.appendChild(line_segment_geometry_element_node)

                            line_segment_geometry = LEVEL.LineSegmentGeometry()

                            line_segment_geometry.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(line_segment_geometry_element_node, "flags", GeometryFlags))
                            input_stream.read(2) # Padding?
                            line_segment_geometry.point_0 = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(line_segment_geometry_element_node, "point 0"))
                            line_segment_geometry.reference_frame_0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(line_segment_geometry_element_node, "reference frame"))
                            input_stream.read(2) # Padding?
                            line_segment_geometry.point_1 = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(line_segment_geometry_element_node, "point 1"))
                            line_segment_geometry.reference_frame_1 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(line_segment_geometry_element_node, "reference frame"))
                            input_stream.read(2) # Padding?

                            user_placed_hint.line_segment_geometry.append(line_segment_geometry)

                    if user_placed_hint.parallelogram_geometry_tag_block.count > 0:
                        user_placed_hint.parallelogram_geometry_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        parallelogram_geometry_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.parallelogram_geometry_tag_block.count, user_placed_hint_element_node, "name", "parallelogram geometry")
                        for parallelogram_geometry_idx in range(user_placed_hint.parallelogram_geometry_tag_block.count):
                            parallelogram_geometry_element_node = None
                            if XML_OUTPUT:
                                parallelogram_geometry_element_node = TAG.xml_doc.createElement('element')
                                parallelogram_geometry_element_node.setAttribute('index', str(parallelogram_geometry_idx))
                                parallelogram_geometry_node.appendChild(parallelogram_geometry_element_node)

                            parallelogram_geometry = LEVEL.ParallelogramGeometry()

                            parallelogram_geometry.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(parallelogram_geometry_element_node, "flags", GeometryFlags))
                            input_stream.read(2) # Padding?
                            parallelogram_geometry.point_0 = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(parallelogram_geometry_element_node, "point 0"))
                            parallelogram_geometry.reference_frame_0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(parallelogram_geometry_element_node, "reference frame"))
                            input_stream.read(2) # Padding?
                            parallelogram_geometry.point_1 = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(parallelogram_geometry_element_node, "point 1"))
                            parallelogram_geometry.reference_frame_1 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(parallelogram_geometry_element_node, "reference frame"))
                            input_stream.read(2) # Padding?
                            parallelogram_geometry.point_2 = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(parallelogram_geometry_element_node, "point 2"))
                            parallelogram_geometry.reference_frame_2 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(parallelogram_geometry_element_node, "reference frame"))
                            input_stream.read(2) # Padding?
                            parallelogram_geometry.point_3 = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(parallelogram_geometry_element_node, "point 3"))
                            parallelogram_geometry.reference_frame_3 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(parallelogram_geometry_element_node, "reference frame"))
                            input_stream.read(2) # Padding?

                            user_placed_hint.parallelogram_geometry.append(parallelogram_geometry)

                    if user_placed_hint.polygon_geometry_tag_block.count > 0:
                        user_placed_hint.polygon_geometry_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        polygon_geometry_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.polygon_geometry_tag_block.count, user_placed_hint_element_node, "name", "polygon geometry")
                        for polygon_geometry_idx in range(user_placed_hint.polygon_geometry_tag_block.count):
                            polygon_geometry_element_node = None
                            if XML_OUTPUT:
                                polygon_geometry_element_node = TAG.xml_doc.createElement('element')
                                polygon_geometry_element_node.setAttribute('index', str(polygon_geometry_idx))
                                polygon_geometry_node.appendChild(polygon_geometry_element_node)

                            polygon_geometry = LEVEL.Hint()

                            polygon_geometry.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(polygon_geometry_element_node, "flags", GeometryFlags))
                            input_stream.read(2) # Padding?
                            polygon_geometry.points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(polygon_geometry_element_node, "points"))

                            user_placed_hint.polygon_geometry.append(polygon_geometry)

                        for polygon_geometry_idx, polygon_geometry in enumerate(user_placed_hint.polygon_geometry):
                            polygon_geometry_element_node = None
                            if XML_OUTPUT:
                                polygon_geometry_element_node = polygon_geometry_node.childNodes[polygon_geometry_idx]

                            polygon_geometry.points = []
                            if polygon_geometry.points_tag_block.count > 0:
                                polygon_geometry.points_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                point_node = tag_format.get_xml_node(XML_OUTPUT, polygon_geometry.points_tag_block.count, polygon_geometry_element_node, "name", "points")
                                for point_idx in range(polygon_geometry.points_tag_block.count):
                                    point_element_node = None
                                    if XML_OUTPUT:
                                        point_element_node = TAG.xml_doc.createElement('element')
                                        point_element_node.setAttribute('index', str(point_idx))
                                        point_node.appendChild(point_element_node)

                                    point = LEVEL.PointGeometry()

                                    point.point = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(point_element_node, "point"))
                                    point.reference_frame = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(point_element_node, "reference frame"))
                                    input_stream.read(2) # Padding?

                                    polygon_geometry.points.append(point)

                    if user_placed_hint.jump_hints_tag_block.count > 0:
                        user_placed_hint.jump_hints_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        jump_hint_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.jump_hints_tag_block.count, user_placed_hint_element_node, "name", "jump hints")
                        for jump_hint_idx in range(user_placed_hint.jump_hints_tag_block.count):
                            jump_hint_element_node = None
                            if XML_OUTPUT:
                                jump_hint_element_node = TAG.xml_doc.createElement('element')
                                jump_hint_element_node.setAttribute('index', str(jump_hint_idx))
                                jump_hint_node.appendChild(jump_hint_element_node)

                            jump_hint = LEVEL.JumpHint()

                            jump_hint.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(jump_hint_element_node, "flags", GeometryFlags))
                            jump_hint.geometry_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(jump_hint_element_node, "geometry index", None, user_placed_hint.parallelogram_geometry_tag_block.count, "parallelogram_geometry_block"))
                            jump_hint.force_jump_height = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(jump_hint_element_node, "function", ForceJumpHeightEnum))
                            jump_hint.control_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(jump_hint_element_node, "flags", JumpControlFlags))

                            user_placed_hint.jump_hints.append(jump_hint)

                    if user_placed_hint.climb_hints_tag_block.count > 0:
                        user_placed_hint.climb_hints_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        climb_hint_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.climb_hints_tag_block.count, user_placed_hint_element_node, "name", "climb hints")
                        for climb_hint_node_idx in range(user_placed_hint.climb_hints_tag_block.count):
                            climb_hint_node_element_node = None
                            if XML_OUTPUT:
                                climb_hint_node_element_node = TAG.xml_doc.createElement('element')
                                climb_hint_node_element_node.setAttribute('index', str(climb_hint_node_idx))
                                climb_hint_node.appendChild(climb_hint_node_element_node)

                            climb_hint = LEVEL.ClimbHint()

                            climb_hint.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(climb_hint_node_element_node, "flags", GeometryFlags))
                            climb_hint.geometry_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(climb_hint_node_element_node, "geometry index", None, user_placed_hint.line_segment_geometry_tag_block.count, "line_segment_geometry_block"))

                            user_placed_hint.climb_hints.append(climb_hint)

                    if user_placed_hint.well_hints_tag_block.count > 0:
                        user_placed_hint.well_hints_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        well_hint_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.well_hints_tag_block.count, user_placed_hint_element_node, "name", "well hints")
                        for well_hint_idx in range(user_placed_hint.well_hints_tag_block.count):
                            well_hint_element_node = None
                            if XML_OUTPUT:
                                well_hint_element_node = TAG.xml_doc.createElement('element')
                                well_hint_element_node.setAttribute('index', str(well_hint_idx))
                                well_hint_node.appendChild(well_hint_element_node)

                            well_hint = LEVEL.Hint()

                            well_hint.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(well_hint_element_node, "flags", HintFlags))
                            input_stream.read(2) # Padding?
                            well_hint.points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(well_hint_element_node, "points"))

                            user_placed_hint.well_hints.append(well_hint)

                        for well_hint_idx, well_hint in enumerate(user_placed_hint.well_hints):
                            well_hint_element_node = None
                            if XML_OUTPUT:
                                well_hint_element_node = well_hint_node.childNodes[well_hint_idx]

                            well_hint.points = []
                            if well_hint.points_tag_block.count > 0:
                                well_hint.points_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                well_point_node = tag_format.get_xml_node(XML_OUTPUT, well_hint.points_tag_block.count, well_hint_element_node, "name", "points")
                                for well_point_idx in range(well_hint.points_tag_block.count):
                                    well_point_element_node = None
                                    if XML_OUTPUT:
                                        well_point_element_node = TAG.xml_doc.createElement('element')
                                        well_point_element_node.setAttribute('index', str(well_point_idx))
                                        well_point_node.appendChild(well_point_element_node)

                                    well_point = LEVEL.WellPoint()

                                    well_point.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(well_point_element_node, "type", WellTypeEnum))
                                    input_stream.read(2) # Padding?
                                    well_point.point = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(well_point_element_node, "point"))
                                    well_point.reference_frame = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(well_point_element_node, "reference frame"))
                                    input_stream.read(2) # Padding?
                                    well_point.sector_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(well_point_element_node, "sector index"))
                                    well_point.normal = TAG.read_degree_2d(input_stream, TAG, tag_format.XMLData(well_point_element_node, "normal"))

                                    well_hint.points.append(well_point)

                    if user_placed_hint.flight_hints_tag_block.count > 0:
                        user_placed_hint.flight_hints_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        flight_hint_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.flight_hints_tag_block.count, user_placed_hint_element_node, "name", "flight hints")
                        for flight_hint_idx in range(user_placed_hint.flight_hints_tag_block.count):
                            flight_hint_element_node = None
                            if XML_OUTPUT:
                                flight_hint_element_node = TAG.xml_doc.createElement('element')
                                flight_hint_element_node.setAttribute('index', str(flight_hint_idx))
                                flight_hint_node.appendChild(flight_hint_element_node)

                            flight_hint = LEVEL.FlightHint()

                            flight_hint.points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(flight_hint_element_node, "points"))

                            user_placed_hint.flight_hints.append(flight_hint)

                        for flight_hint_idx, flight_hint in enumerate(user_placed_hint.flight_hints):
                            flight_hint_element_node = None
                            if XML_OUTPUT:
                                flight_hint_element_node = flight_hint_node.childNodes[flight_hint_idx]

                            flight_hint.points = []
                            if flight_hint.points_tag_block.count > 0:
                                flight_hint.points_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                flight_point_node = tag_format.get_xml_node(XML_OUTPUT, flight_hint.points_tag_block.count, flight_hint_element_node, "name", "points")
                                for flight_point_idx in range(well_hint.points_tag_block.count):
                                    flight_point_element_node = None
                                    if XML_OUTPUT:
                                        flight_point_element_node = TAG.xml_doc.createElement('element')
                                        flight_point_element_node.setAttribute('index', str(flight_point_idx))
                                        flight_point_node.appendChild(flight_point_element_node)

                                    flight_hint.points.append(TAG.read_vector(input_stream, TAG, tag_format.XMLData(flight_point_element_node, "point")))

def read_pathfinding_edges(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.background_sound_palette_tag_block.count > 0:
        pathfinding_edges_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.background_sound_palette_tag_block.count, tag_node, "name", "pathfinding edges")
        LEVEL.background_sound_palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for pathfinding_edge_idx in range(LEVEL.level_body.background_sound_palette_tag_block.count):
            pathfinding_edge_element_node = None
            if XML_OUTPUT:
                pathfinding_edge_element_node = TAG.xml_doc.createElement('element')
                pathfinding_edge_element_node.setAttribute('index', str(pathfinding_edge_idx))
                pathfinding_edges_node.appendChild(pathfinding_edge_element_node)

            LEVEL.pathfinding_edges.append(TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(pathfinding_edge_element_node, "midpoint")))

def read_background_sound_palette(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.background_sound_palette_tag_block.count > 0:
        background_sound_palette_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.background_sound_palette_tag_block.count, tag_node, "name", "background sound palette")
        LEVEL.background_sound_palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for background_sound_palette_idx in range(LEVEL.level_body.background_sound_palette_tag_block.count):
            background_sound_palette_element_node = None
            if XML_OUTPUT:
                background_sound_palette_element_node = TAG.xml_doc.createElement('element')
                background_sound_palette_element_node.setAttribute('index', str(background_sound_palette_idx))
                background_sound_palette_node.appendChild(background_sound_palette_element_node)

            background_sound_palette = LEVEL.BackgroundSoundPalette()
            background_sound_palette.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "name"))
            background_sound_palette.background_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "background sound"))
            background_sound_palette.inside_cluster_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "inside cluster sound"))
            input_stream.read(20) # Padding?
            background_sound_palette.cutoff_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "cutoff distance"))
            background_sound_palette.scale_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "scale flags", BackgroundScaleFlags))
            background_sound_palette.interior_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "interior scale"))
            background_sound_palette.portal_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "portal scale"))
            background_sound_palette.exterior_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "exterior scale"))
            background_sound_palette.interpolation_speed = TAG.read_float(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "interpolation speed"))
            input_stream.read(8) # Padding?

            LEVEL.background_sound_palette.append(background_sound_palette)

        for background_sound_palette_idx, background_sound_palette in enumerate(LEVEL.background_sound_palette):
            background_sound_palette_element_node = None
            if XML_OUTPUT:
                background_sound_palette_element_node = background_sound_palette_node.childNodes[background_sound_palette_idx]

            if background_sound_palette.background_sound.name_length > 0:
                background_sound_palette.background_sound.name = TAG.read_variable_string(input_stream, background_sound_palette.background_sound.name_length, TAG)

            if background_sound_palette.inside_cluster_sound.name_length > 0:
                background_sound_palette.inside_cluster_sound.name = TAG.read_variable_string(input_stream, background_sound_palette.inside_cluster_sound.name_length, TAG)

            if XML_OUTPUT:
                background_sound_node = tag_format.get_xml_node(XML_OUTPUT, 1, background_sound_palette_element_node, "name", "background sound")
                inside_cluster_sound_node = tag_format.get_xml_node(XML_OUTPUT, 1, background_sound_palette_element_node, "name", "inside cluster sound")
                background_sound_palette.background_sound.append_xml_attributes(background_sound_node)
                background_sound_palette.inside_cluster_sound.append_xml_attributes(inside_cluster_sound_node)

def read_sound_environment_palette(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.sound_environment_palette_tag_block.count > 0:
        sound_environment_palette_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.sound_environment_palette_tag_block.count, tag_node, "name", "sound environment palette")
        LEVEL.sound_environment_palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for sound_environment_palette_idx in range(LEVEL.level_body.sound_environment_palette_tag_block.count):
            sound_environment_palette_element_node = None
            if XML_OUTPUT:
                sound_environment_palette_element_node = TAG.xml_doc.createElement('element')
                sound_environment_palette_element_node.setAttribute('index', str(sound_environment_palette_idx))
                sound_environment_palette_node.appendChild(sound_environment_palette_element_node)

            sound_environment_palette = LEVEL.SoundEnvironmentPalette()
            sound_environment_palette.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(sound_environment_palette_element_node, "name"))
            sound_environment_palette.sound_environment = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(sound_environment_palette_element_node, "sound environment"))
            sound_environment_palette.cutoff_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(sound_environment_palette_element_node, "cutoff distance"))
            sound_environment_palette.interpolation_speed = TAG.read_float(input_stream, TAG, tag_format.XMLData(sound_environment_palette_element_node, "interpolation speed"))
            input_stream.read(24) # Padding?

            LEVEL.sound_environment_palette.append(sound_environment_palette)

        for sound_environment_palette_idx, sound_environment_palette in enumerate(LEVEL.sound_environment_palette):
            sound_environment_palette_element_node = None
            if XML_OUTPUT:
                sound_environment_palette_element_node = sound_environment_palette_node.childNodes[sound_environment_palette_idx]

            if sound_environment_palette.sound_environment.name_length > 0:
                sound_environment_palette.sound_environment.name = TAG.read_variable_string(input_stream, sound_environment_palette.sound_environment.name_length, TAG)

            if XML_OUTPUT:
                sound_environment_node = tag_format.get_xml_node(XML_OUTPUT, 1, sound_environment_palette_element_node, "name", "sound environment")
                sound_environment_palette.sound_environment.append_xml_attributes(sound_environment_node)

def read_markers(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.markers_tag_block.count > 0:
        markers_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.markers_tag_block.count, tag_node, "name", "markers")
        LEVEL.markers_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for marker_idx in range(LEVEL.level_body.markers_tag_block.count):
            marker_element_node = None
            if XML_OUTPUT:
                marker_element_node = TAG.xml_doc.createElement('element')
                marker_element_node.setAttribute('index', str(marker_idx))
                markers_node.appendChild(marker_element_node)

            marker = LEVEL.Marker()
            marker.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(marker_element_node, "name"))
            marker.rotation = TAG.read_quaternion(input_stream, TAG, tag_format.XMLData(marker_element_node, "rotation"), True)
            marker.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(marker_element_node, "position"), True)

            LEVEL.markers.append(marker)

def read_runtime_decals(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.runtime_decals_tag_block.count > 0:
        runtime_decals_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.runtime_decals_tag_block.count, tag_node, "name", "runtime decals")
        LEVEL.runtime_decals_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for runtime_decal_idx in range(LEVEL.level_body.runtime_decals_tag_block.count):
            runtime_decal_element_node = None
            if XML_OUTPUT:
                runtime_decal_element_node = TAG.xml_doc.createElement('element')
                runtime_decal_element_node.setAttribute('index', str(runtime_decal_idx))
                runtime_decals_node.appendChild(runtime_decal_element_node)

            input_stream.read(16) # Padding?

def read_environment_object_palette(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.environment_object_palette_tag_block.count > 0:
        environment_object_palette_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.environment_object_palette_tag_block.count, tag_node, "name", "environment object palette")
        LEVEL.environment_object_palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for environment_object_palette_idx in range(LEVEL.level_body.environment_object_palette_tag_block.count):
            environment_object_palette_element_node = None
            if XML_OUTPUT:
                environment_object_palette_element_node = TAG.xml_doc.createElement('element')
                environment_object_palette_element_node.setAttribute('index', str(environment_object_palette_idx))
                environment_object_palette_node.appendChild(environment_object_palette_element_node)

            environment_object_palette = LEVEL.EnvironmentObjectPalette()
            environment_object_palette.definition = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(environment_object_palette_element_node, "definition"))
            environment_object_palette.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(environment_object_palette_element_node, "model"))
            input_stream.read(4) # Padding?

            LEVEL.environment_object_palette.append(environment_object_palette)

        for environment_object_palette_idx, environment_object_palette in enumerate(LEVEL.environment_object_palette):
            environment_object_palette_element_node = None
            if XML_OUTPUT:
                environment_object_palette_element_node = environment_object_palette_node.childNodes[environment_object_palette_idx]

            if environment_object_palette.definition.name_length > 0:
                environment_object_palette.definition.name = TAG.read_variable_string(input_stream, environment_object_palette.definition.name_length, TAG)

            if environment_object_palette.model.name_length > 0:
                environment_object_palette.model.name = TAG.read_variable_string(input_stream, environment_object_palette.model.name_length, TAG)

            if XML_OUTPUT:
                definition_node = tag_format.get_xml_node(XML_OUTPUT, 1, environment_object_palette_element_node, "name", "definition")
                model_node = tag_format.get_xml_node(XML_OUTPUT, 1, environment_object_palette_element_node, "name", "model")
                environment_object_palette.definition.append_xml_attributes(definition_node)
                environment_object_palette.model.append_xml_attributes(model_node)

def read_environment_object(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.environment_objects_tag_block.count > 0:
        environment_objects_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.environment_objects_tag_block.count, tag_node, "name", "environment objects")
        LEVEL.environment_objects_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for environment_object_idx in range(LEVEL.level_body.environment_objects_tag_block.count):
            environment_object_element_node = None
            if XML_OUTPUT:
                environment_object_element_node = TAG.xml_doc.createElement('element')
                environment_object_element_node.setAttribute('index', str(environment_object_idx))
                environment_objects_node.appendChild(environment_object_element_node)

            environment_object = LEVEL.EnvironmentObject()
            environment_object.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(environment_object_element_node, "name"))
            environment_object.rotation = TAG.read_quaternion(input_stream, TAG, tag_format.XMLData(environment_object_element_node, "rotation"), True)
            environment_object.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(environment_object_element_node, "position"), True)
            environment_object.palette_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(environment_object_element_node, "palette index", None, LEVEL.level_body.environment_object_palette_tag_block.count, "structure_bsp_environment_object_palette_block"))
            input_stream.read(2) # Padding?
            environment_object.unique_id = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(environment_object_element_node, "unique id"))
            environment_object.exported_object_type = TAG.read_variable_string_no_terminator_reversed(input_stream, 4, TAG, tag_format.XMLData(environment_object_element_node, "exported object type"))
            environment_object.scenario_object_name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(environment_object_element_node, "scenario object name"))

            LEVEL.environment_objects.append(environment_object)

def read_lightmaps(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.lightmaps_tag_block.count > 0:
        lightmaps_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.lightmaps_tag_block.count, tag_node, "name", "lightmaps")
        LEVEL.lightmaps_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for lightmap_idx in range(LEVEL.level_body.lightmaps_tag_block.count):
            lightmap_element_node = None
            if XML_OUTPUT:
                lightmap_element_node = TAG.xml_doc.createElement('element')
                lightmap_element_node.setAttribute('index', str(lightmap_idx))
                lightmaps_node.appendChild(lightmap_element_node)

            LEVEL.lightmaps.append(TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(lightmap_element_node, "bitmap group")))

        for lightmap_idx, lightmap in enumerate(LEVEL.lightmaps):
            lightmap_element_node = None
            if XML_OUTPUT:
                lightmap_element_node = lightmaps_node.childNodes[lightmap_idx]

            if lightmap.name_length > 0:
                lightmap.name = TAG.read_variable_string(input_stream, lightmap.name_length, TAG)

            if XML_OUTPUT:
                lightmap_node = tag_format.get_xml_node(XML_OUTPUT, 1, lightmap_element_node, "name", "bitmap group")
                lightmap.append_xml_attributes(lightmap_node)

def read_leaf_map_leaves(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.leaf_map_leaves_tag_block.count > 0:
        leaf_map_leaves_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.leaf_map_leaves_tag_block.count, tag_node, "name", "leaf map leaves")
        LEVEL.leaf_map_leaves_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for leaf_map_leaf_idx in range(LEVEL.level_body.leaf_map_leaves_tag_block.count):
            leaf_map_leaf_element_node = None
            if XML_OUTPUT:
                leaf_map_leaf_element_node = TAG.xml_doc.createElement('element')
                leaf_map_leaf_element_node.setAttribute('index', str(leaf_map_leaf_idx))
                leaf_map_leaves_node.appendChild(leaf_map_leaf_element_node)

            leaf_map_leaf = LEVEL.LeafMapLeaf()
            leaf_map_leaf.faces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(leaf_map_leaf_element_node, "faces"))
            leaf_map_leaf.connection_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(leaf_map_leaf_element_node, "connection indices"))

            LEVEL.leaf_map_leaves.append(leaf_map_leaf)

        for leaf_map_leaf_idx, leaf_map_leaf in enumerate(LEVEL.leaf_map_leaves):
            leaf_map_leaf_element_node = None
            if XML_OUTPUT:
                leaf_map_leaf_element_node = leaf_map_leaves_node.childNodes[leaf_map_leaf_idx]

            leaf_map_leaf.faces = []
            leaf_map_leaf.connection_indices = []
            if leaf_map_leaf.faces_tag_block.count > 0:
                faces_node = tag_format.get_xml_node(XML_OUTPUT, leaf_map_leaf.faces_tag_block.count, leaf_map_leaf_element_node, "name", "faces")
                leaf_map_leaf.faces_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for face_idx in range(leaf_map_leaf.faces_tag_block.count):
                    face_element_node = None
                    if XML_OUTPUT:
                        face_element_node = TAG.xml_doc.createElement('element')
                        face_element_node.setAttribute('index', str(face_idx))
                        faces_node.appendChild(face_element_node)

                    face = LEVEL.Face()
                    face.node_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(face_element_node, "node index"))
                    face.vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(face_element_node, "vertices"))

                    leaf_map_leaf.faces.append(face)

                for face_idx, face in enumerate(leaf_map_leaf.faces):
                    face_element_node = None
                    if XML_OUTPUT:
                        face_element_node = faces_node.childNodes[face_idx]

                    face.vertices = []
                    if face.vertices_tag_block.count > 0:
                        vertices_node = tag_format.get_xml_node(XML_OUTPUT, face.vertices_tag_block.count, face_element_node, "name", "vertices")
                        face.vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for vertex_idx in range(face.vertices_tag_block.count):
                            vertex_element_node = None
                            if XML_OUTPUT:
                                vertex_element_node = TAG.xml_doc.createElement('element')
                                vertex_element_node.setAttribute('index', str(vertex_idx))
                                vertices_node.appendChild(vertex_element_node)

                            face.vertices.append(TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(vertex_element_node, "vertex")))


            if leaf_map_leaf.connection_indices_tag_block.count > 0:
                connection_indices_node = tag_format.get_xml_node(XML_OUTPUT, leaf_map_leaf.connection_indices_tag_block.count, leaf_map_leaf_element_node, "name", "connection indices")
                leaf_map_leaf.connection_indices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for connection_idx in range(leaf_map_leaf.connection_indices_tag_block.count):
                    connection_element_node = None
                    if XML_OUTPUT:
                        connection_element_node = TAG.xml_doc.createElement('element')
                        connection_element_node.setAttribute('index', str(connection_idx))
                        connection_indices_node.appendChild(connection_element_node)

                    leaf_map_leaf.connection_indices.append(TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(connection_element_node, "connection index")))

def read_leaf_map_connections(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.leaf_map_connections_tag_block.count > 0:
        leaf_map_connections_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.leaf_map_connections_tag_block.count, tag_node, "name", "leaf map connections")
        LEVEL.leaf_map_connections_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for leaf_map_connection_idx in range(LEVEL.level_body.leaf_map_connections_tag_block.count):
            leaf_map_connection_element_node = None
            if XML_OUTPUT:
                leaf_map_connection_element_node = TAG.xml_doc.createElement('element')
                leaf_map_connection_element_node.setAttribute('index', str(leaf_map_connection_idx))
                leaf_map_connections_node.appendChild(leaf_map_connection_element_node)

            leaf_map_connection = LEVEL.LeafMapConnection()
            leaf_map_connection.plane_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(leaf_map_connection_element_node, "plane index"))
            leaf_map_connection.back_leaf_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(leaf_map_connection_element_node, "back leaf index"))
            leaf_map_connection.front_leaf_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(leaf_map_connection_element_node, "front leaf index"))
            leaf_map_connection.vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(leaf_map_connection_element_node, "vertices"))
            leaf_map_connection.area = TAG.read_float(input_stream, TAG, tag_format.XMLData(leaf_map_connection_element_node, "area"))

            LEVEL.leaf_map_connections.append(leaf_map_connection)

        for leaf_map_connection_idx, leaf_map_connection in enumerate(LEVEL.leaf_map_connections):
            leaf_map_connection_element_node = None
            if XML_OUTPUT:
                leaf_map_connection_element_node = leaf_map_connections_node.childNodes[leaf_map_connection_idx]

            leaf_map_connection.vertices = []
            if leaf_map_connection.vertices_tag_block.count > 0:
                vertices_node = tag_format.get_xml_node(XML_OUTPUT, leaf_map_connection.vertices_tag_block.count, leaf_map_connection_element_node, "name", "vertices")
                leaf_map_connection.vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for vertex_idx in range(leaf_map_connection.vertices_tag_block.count):
                    vertex_element_node = None
                    if XML_OUTPUT:
                        vertex_element_node = TAG.xml_doc.createElement('element')
                        vertex_element_node.setAttribute('index', str(vertex_idx))
                        vertices_node.appendChild(vertex_element_node)

                    leaf_map_connection.vertices.append(TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(vertex_element_node, "vertex")))

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

def read_precomputed_lighting(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.precomputed_lighting_tag_block.count > 0:
        precomputed_lighting_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.precomputed_lighting_tag_block.count, tag_node, "name", "precomputed lighting")
        LEVEL.precomputed_lighting_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for precomputed_lighting_idx in range(LEVEL.level_body.precomputed_lighting_tag_block.count):
            precomputed_lighting_element_node = None
            if XML_OUTPUT:
                precomputed_lighting_element_node = TAG.xml_doc.createElement('element')
                precomputed_lighting_element_node.setAttribute('index', str(precomputed_lighting_idx))
                precomputed_lighting_node.appendChild(precomputed_lighting_element_node)

            precomputed_lighting = LEVEL.PrecomputedLighting()
            precomputed_lighting.index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(precomputed_lighting_element_node, "index"))
            precomputed_lighting.light_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(precomputed_lighting_element_node, "light type", LightTypeEnum))
            precomputed_lighting.attachment_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(precomputed_lighting_element_node, "attachment index"))
            precomputed_lighting.object_type = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(precomputed_lighting_element_node, "object type"))
            precomputed_lighting.projection_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(precomputed_lighting_element_node, "projection count"))
            precomputed_lighting.cluster_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(precomputed_lighting_element_node, "cluster count"))
            precomputed_lighting.volume_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(precomputed_lighting_element_node, "volume count"))
            input_stream.read(2) # Padding?
            precomputed_lighting.projections_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(precomputed_lighting_element_node, "projections"))
            precomputed_lighting.visiblity_clusters_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(precomputed_lighting_element_node, "visiblity clusters"))
            precomputed_lighting.cluster_remap_table_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(precomputed_lighting_element_node, "cluster remap table"))
            precomputed_lighting.visibility_volumes_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(precomputed_lighting_element_node, "visibility volumes"))

            LEVEL.precomputed_lighting.append(precomputed_lighting)

        for precomputed_lighting_idx, precomputed_lighting in enumerate(LEVEL.precomputed_lighting):
            precomputed_lighting_element_node = None
            if XML_OUTPUT:
                precomputed_lighting_element_node = precomputed_lighting_node.childNodes[precomputed_lighting_idx]

            precomputed_lighting.projections = input_stream.read(precomputed_lighting.projections_data.size)
            precomputed_lighting.visiblity_clusters = input_stream.read(precomputed_lighting.visiblity_clusters_data.size)
            precomputed_lighting.cluster_remap_table = input_stream.read(precomputed_lighting.cluster_remap_table_data.size)
            precomputed_lighting.visibility_volumes = input_stream.read(precomputed_lighting.visibility_volumes_data.size)
            precomputed_lighting.svis_header = TAG.TagBlockHeader().read(input_stream, TAG)

def read_instanced_geometry_definition(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.instanced_geometry_definition_tag_block.count > 0:
        instanced_geometry_definition_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.instanced_geometry_definition_tag_block.count, tag_node, "name", "instanced geometry definition")
        LEVEL.instanced_geometry_definition_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for instanced_geometry_definition_idx in range(LEVEL.level_body.instanced_geometry_definition_tag_block.count):
            instanced_geometry_definition_element_node = None
            if XML_OUTPUT:
                instanced_geometry_definition_element_node = TAG.xml_doc.createElement('element')
                instanced_geometry_definition_element_node.setAttribute('index', str(instanced_geometry_definition_idx))
                instanced_geometry_definition_node.appendChild(instanced_geometry_definition_element_node)

            instance_geometry_definition = LEVEL.InstanceGeometryDefinition()
            instance_geometry_definition.total_vertex_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "total vertex count"))
            instance_geometry_definition.total_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "total triangle count"))
            instance_geometry_definition.total_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "total part count"))
            instance_geometry_definition.shadow_casting_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "shadow casting triangle count"))
            instance_geometry_definition.shadow_casting_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "shadow casting part count"))
            instance_geometry_definition.opaque_point_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "opaque point count"))
            instance_geometry_definition.opaque_vertex_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "opaque vertex count"))
            instance_geometry_definition.opaque_part_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "opaque part count"))
            instance_geometry_definition.opaque_max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "opaque max nodes vertex"))
            instance_geometry_definition.transparent_max_nodes_vertex = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "transparent max nodes vertex"))
            instance_geometry_definition.shadow_casting_rigid_triangle_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "shadow casting rigid triangle count"))
            instance_geometry_definition.geometry_classification = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "geometry classification", GeometryClassificationEnum))
            instance_geometry_definition.geometry_compression_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "geometry compression flags", GeometryCompressionFlags))
            instance_geometry_definition.compression_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "compression info"))
            instance_geometry_definition.hardware_node_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "hardware node count"))
            instance_geometry_definition.node_map_size = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "node map size"))
            instance_geometry_definition.software_plane_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "software plane count"))
            instance_geometry_definition.total_subpart_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "total subpart count"))
            instance_geometry_definition.section_lighting_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "section lighting flags", SectionLightingFlags))
            instance_geometry_definition.block_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "block offset"))
            instance_geometry_definition.block_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "block size"))
            instance_geometry_definition.section_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "section data size"))
            instance_geometry_definition.resource_data_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "resource data size"))
            instance_geometry_definition.resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "resources"))
            input_stream.read(4) # Padding?
            instance_geometry_definition.owner_tag_section_offset = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "owner tag section offset"))
            input_stream.read(6) # Padding?
            instance_geometry_definition.render_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "render data"))
            instance_geometry_definition.index_reorder_table_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "index reorder table"))
            instance_geometry_definition.checksum = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "checksum"))
            instance_geometry_definition.bounding_sphere_center = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "bounding sphere center"))
            instance_geometry_definition.bounding_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "bounding sphere radius"))
            instance_geometry_definition.bsp3d_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "bsp3d nodes"))
            instance_geometry_definition.planes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "planes"))
            instance_geometry_definition.leaves_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "leaves"))
            instance_geometry_definition.bsp2d_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "bsp2d references"))
            instance_geometry_definition.bsp2d_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "bsp2d nodes"))
            instance_geometry_definition.surfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "surfaces"))
            instance_geometry_definition.edges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "edges"))
            instance_geometry_definition.vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "vertices"))
            instance_geometry_definition.bsp_physics_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "bsp physics"))
            instance_geometry_definition.render_leaves_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "render leaves"))
            instance_geometry_definition.surface_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(instanced_geometry_definition_element_node, "surface references"))

            LEVEL.instanced_geometry_definition.append(instance_geometry_definition)

        for instanced_geometry_definition_idx, instanced_geometry_definition in enumerate(LEVEL.instanced_geometry_definition):
            instanced_geometry_definition_element_node = None
            if XML_OUTPUT:
                instanced_geometry_definition_element_node = instanced_geometry_definition_node.childNodes[instanced_geometry_definition_idx]

            instanced_geometry_definition.compression_info = []
            instanced_geometry_definition.resources = []
            instanced_geometry_definition.render_data = []
            instanced_geometry_definition.index_reorder_table = []
            instanced_geometry_definition.bsp3d_nodes = []
            instanced_geometry_definition.planes = []
            instanced_geometry_definition.leaves = []
            instanced_geometry_definition.bsp2d_references = []
            instanced_geometry_definition.bsp2d_nodes = []
            instanced_geometry_definition.surfaces = []
            instanced_geometry_definition.edges = []
            instanced_geometry_definition.vertices = []
            instanced_geometry_definition.bsp_physics = []
            instanced_geometry_definition.render_leaves = []
            instanced_geometry_definition.surface_references = []

            instanced_geometry_definition.igri_header = TAG.TagBlockHeader().read(input_stream, TAG)
            instanced_geometry_definition.sinf_header = TAG.TagBlockHeader().read(input_stream, TAG)
            if instanced_geometry_definition.compression_info_tag_block.count > 0:
                compression_info_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.compression_info_tag_block.count, instanced_geometry_definition_element_node, "name", "compression info")
                instanced_geometry_definition.compression_info_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for compression_info_idx in range(instanced_geometry_definition.compression_info_tag_block.count):
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

                    instanced_geometry_definition.compression_info.append(compression_info)

            instanced_geometry_definition.blok_header = TAG.TagBlockHeader().read(input_stream, TAG)

            if instanced_geometry_definition.resources_tag_block.count > 0:
                resources_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.resources_tag_block.count, instanced_geometry_definition_element_node, "name", "resources")
                instanced_geometry_definition.resources_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for resource_idx in range(instanced_geometry_definition.resources_tag_block.count):
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

                    instanced_geometry_definition.resources.append(resource)

            if instanced_geometry_definition.render_data_tag_block.count > 0:
                render_data_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.render_data_tag_block.count, instanced_geometry_definition_element_node, "name", "render data")
                instanced_geometry_definition.render_data_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for render_data_idx in range(instanced_geometry_definition.render_data_tag_block.count):
                    render_data_element_node = None
                    if XML_OUTPUT:
                        render_data_element_node = TAG.xml_doc.createElement('element')
                        render_data_element_node.setAttribute('index', str(render_data_idx))
                        render_data_node.appendChild(render_data_element_node)

                    render_data = LEVEL.ClusterData()
                    render_data.parts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(render_data_element_node, "parts"))
                    render_data.subparts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(render_data_element_node, "subparts"))
                    render_data.visibility_bounds_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(render_data_element_node, "visibility bounds"))
                    render_data.raw_vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(render_data_element_node, "raw vertices"))
                    render_data.strip_indices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(render_data_element_node, "strip indices"))
                    render_data.visibility_mopp_code_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(render_data_element_node, "visibility mopp code"))
                    render_data.mopp_reorder_table_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(render_data_element_node, "mopp reorder table"))
                    render_data.vertex_buffers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(render_data_element_node, "vertex buffers"))
                    input_stream.read(4) # Padding?
                    render_data.sect_header = TAG.TagBlockHeader().read(input_stream, TAG)

                    instanced_geometry_definition.render_data.append(render_data)

                for render_data_idx, render_data in enumerate(instanced_geometry_definition.render_data):
                    render_data_element_node = None
                    if XML_OUTPUT:
                        render_data_element_node = render_data_node.childNodes[render_data_idx]

                    render_data.parts = []
                    render_data.subparts = []
                    render_data.visibility_bounds = []
                    render_data.raw_vertices = []
                    render_data.strip_indices = []
                    render_data.mopp_reorder_table = []
                    render_data.vertex_buffers = []
                    if render_data.parts_tag_block.count > 0:
                        parts_node = tag_format.get_xml_node(XML_OUTPUT, render_data.parts_tag_block.count, render_data_element_node, "name", "parts")
                        render_data.parts_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for part_idx in range(render_data.parts_tag_block.count):
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

                            render_data.parts.append(part)

                    if render_data.subparts_tag_block.count > 0:
                        subparts_node = tag_format.get_xml_node(XML_OUTPUT, render_data.subparts_tag_block.count, render_data_element_node, "name", "subparts")
                        render_data.subparts_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for subpart_idx in range(render_data.subparts_tag_block.count):
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

                            render_data.subparts.append(sub_part)

                    if render_data.visibility_bounds_tag_block.count > 0:
                        visibility_bounds_node = tag_format.get_xml_node(XML_OUTPUT, render_data.visibility_bounds_tag_block.count, render_data_element_node, "name", "visibility bounds")
                        render_data.subparts_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for visibility_bound_idx in range(render_data.visibility_bounds_tag_block.count):
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

                            render_data.visibility_bounds.append(visibility_bound)

                    if render_data.raw_vertices_tag_block.count > 0:
                        raw_vertices_node = tag_format.get_xml_node(XML_OUTPUT, render_data.raw_vertices_tag_block.count, render_data_element_node, "name", "raw vertices")
                        render_data.raw_vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for raw_vertex_idx in range(render_data.raw_vertices_tag_block.count):
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

                            render_data.raw_vertices.append(raw_vertex)

                    if render_data.strip_indices_tag_block.count > 0:
                        strip_indices_node = tag_format.get_xml_node(XML_OUTPUT, render_data.strip_indices_tag_block.count, render_data_element_node, "name", "strip indices")
                        render_data.strip_indices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for strip_index_idx in range(render_data.strip_indices_tag_block.count):
                            strip_index_element_node = None
                            if XML_OUTPUT:
                                strip_index_element_node = TAG.xml_doc.createElement('element')
                                strip_index_element_node.setAttribute('index', str(strip_index_idx))
                                strip_indices_node.appendChild(strip_index_element_node)

                            render_data.strip_indices.append(TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(strip_index_element_node, "index")))

                    render_data.visibility_mopp_code = input_stream.read(render_data.visibility_mopp_code_data.size)

                    if render_data.mopp_reorder_table_tag_block.count > 0:
                        mopp_reorder_table_node = tag_format.get_xml_node(XML_OUTPUT, render_data.mopp_reorder_table_tag_block.count, render_data_element_node, "name", "mopp reorder table")
                        render_data.mopp_reorder_table_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for mopp_reorder_table_idx in range(render_data.mopp_reorder_table_tag_block.count):
                            mopp_reorder_table_element_node = None
                            if XML_OUTPUT:
                                mopp_reorder_table_element_node = TAG.xml_doc.createElement('element')
                                mopp_reorder_table_element_node.setAttribute('index', str(mopp_reorder_table_idx))
                                mopp_reorder_table_node.appendChild(mopp_reorder_table_element_node)

                            render_data.mopp_reorder_table.append(TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(mopp_reorder_table_element_node, "index")))

                    if render_data.vertex_buffers_tag_block.count > 0:
                        vertex_buffers_node = tag_format.get_xml_node(XML_OUTPUT, render_data.vertex_buffers_tag_block.count, render_data_element_node, "name", "vertex buffers")
                        render_data.mopp_reorder_table_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        for vertex_buffer_idx in range(render_data.vertex_buffers_tag_block.count):
                            vertex_buffer_element_node = None
                            if XML_OUTPUT:
                                vertex_buffer_element_node = TAG.xml_doc.createElement('element')
                                vertex_buffer_element_node.setAttribute('index', str(vertex_buffer_idx))
                                vertex_buffers_node.appendChild(vertex_buffer_element_node)

                            input_stream.read(32) # Padding?

            if instanced_geometry_definition.index_reorder_table_tag_block.count > 0:
                index_reorder_table_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.index_reorder_table_tag_block.count, instanced_geometry_definition_element_node, "name", "index reorder table")
                instanced_geometry_definition.index_reorder_table_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for index_reorder_table_idx in range(instanced_geometry_definition.index_reorder_table_tag_block.count):
                    index_reorder_table_element_node = None
                    if XML_OUTPUT:
                        index_reorder_table_element_node = TAG.xml_doc.createElement('element')
                        index_reorder_table_element_node.setAttribute('index', str(index_reorder_table_idx))
                        index_reorder_table_node.appendChild(index_reorder_table_element_node)

                    instanced_geometry_definition.index_reorder_table.append(TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(index_reorder_table_element_node, "index")))

            instanced_geometry_definition.cbsp_header = TAG.TagBlockHeader().read(input_stream, TAG)

            if instanced_geometry_definition.bsp3d_nodes_tag_block.count > 0:
                instanced_geometry_definition.bsp3d_nodes_header = TAG.TagBlockHeader().read(input_stream, TAG)
                bsp3d_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.bsp3d_nodes_tag_block.count, instanced_geometry_definition_element_node, "name", "bsp3d nodes")
                for bsp3d_node_idx in range(instanced_geometry_definition.bsp3d_nodes_tag_block.count):
                    bsp3d_node_element_node = None
                    if XML_OUTPUT:
                        bsp3d_node_element_node = TAG.xml_doc.createElement('element')
                        bsp3d_node_element_node.setAttribute('index', str(bsp3d_node_idx))
                        bsp3d_node.appendChild(bsp3d_node_element_node)

                    bsp3d = LEVEL.BSP3DNode()
                    bsp3d.back_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp3d_node_element_node, "back child"))
                    bsp3d.front_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp3d_node_element_node, "front child"))

                    instanced_geometry_definition.bsp3d_nodes.append(bsp3d)

            if instanced_geometry_definition.planes_tag_block.count > 0:
                instanced_geometry_definition.planes_header = TAG.TagBlockHeader().read(input_stream, TAG)
                plane_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.planes_tag_block.count, instanced_geometry_definition_element_node, "name", "planes")
                for plane_idx in range(instanced_geometry_definition.planes_tag_block.count):
                    plane_element_node = None
                    if XML_OUTPUT:
                        plane_element_node = TAG.xml_doc.createElement('element')
                        plane_element_node.setAttribute('index', str(plane_idx))
                        plane_node.appendChild(plane_element_node)

                    instanced_geometry_definition.planes.append(TAG.Plane3D().read(input_stream, TAG, tag_format.XMLData(plane_element_node, "plane")))

            if instanced_geometry_definition.leaves_tag_block.count > 0:
                instanced_geometry_definition.leaves_header = TAG.TagBlockHeader().read(input_stream, TAG)
                leaf_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.leaves_tag_block.count, instanced_geometry_definition_element_node, "name", "leaves")
                for leaf_idx in range(instanced_geometry_definition.leaves_tag_block.count):
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

                    instanced_geometry_definition.leaves.append(leaf)

            if instanced_geometry_definition.bsp2d_references_tag_block.count > 0:
                instanced_geometry_definition.bsp2d_references_header = TAG.TagBlockHeader().read(input_stream, TAG)
                bsp2d_references_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.bsp2d_references_tag_block.count, instanced_geometry_definition_element_node, "name", "bsp2d references")
                for bsp2d_reference_idx in range(instanced_geometry_definition.bsp2d_references_tag_block.count):
                    bsp2d_reference_element_node = None
                    if XML_OUTPUT:
                        bsp2d_reference_element_node = TAG.xml_doc.createElement('element')
                        bsp2d_reference_element_node.setAttribute('index', str(bsp2d_reference_idx))
                        bsp2d_references_node.appendChild(bsp2d_reference_element_node)

                    bsp2d_reference = LEVEL.BSP2DReference()
                    bsp2d_reference.plane = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp2d_reference_element_node, "plane"))
                    bsp2d_reference.bsp2d_node = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp2d_reference_element_node, "bsp2d node"))

                    instanced_geometry_definition.bsp2d_references.append(bsp2d_reference)

            if instanced_geometry_definition.bsp2d_nodes_tag_block.count > 0:
                instanced_geometry_definition.bsp2d_nodes_header = TAG.TagBlockHeader().read(input_stream, TAG)
                bsp2d_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.bsp2d_nodes_tag_block.count, instanced_geometry_definition_element_node, "name", "bsp2d nodes")
                for bsp2d_node_idx in range(instanced_geometry_definition.bsp2d_nodes_tag_block.count):
                    bsp2d_node_element_node = None
                    if XML_OUTPUT:
                        bsp2d_node_element_node = TAG.xml_doc.createElement('element')
                        bsp2d_node_element_node.setAttribute('index', str(bsp2d_node_idx))
                        bsp2d_node.appendChild(bsp2d_node_element_node)

                    bsp2d = LEVEL.BSP2DNode()
                    bsp2d.plane = TAG.Plane2D().read(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "plane"))
                    bsp2d.left_child = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "left child"))
                    bsp2d.right_child = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "right child"))

                    instanced_geometry_definition.bsp2d_nodes.append(bsp2d)

            if instanced_geometry_definition.surfaces_tag_block.count > 0:
                instanced_geometry_definition.surfaces_header = TAG.TagBlockHeader().read(input_stream, TAG)
                surfaces_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.surfaces_tag_block.count, instanced_geometry_definition_element_node, "name", "surfaces")
                for surfaces_idx in range(instanced_geometry_definition.surfaces_tag_block.count):
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

                    instanced_geometry_definition.surfaces.append(surface)

            if instanced_geometry_definition.edges_tag_block.count > 0:
                instanced_geometry_definition.edges_header = TAG.TagBlockHeader().read(input_stream, TAG)
                edge_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.edges_tag_block.count, instanced_geometry_definition_element_node, "name", "edges")
                for edge_idx in range(instanced_geometry_definition.edges_tag_block.count):
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

                    instanced_geometry_definition.edges.append(edge)

            if instanced_geometry_definition.vertices_tag_block.count > 0:
                instanced_geometry_definition.vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                vertex_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.vertices_tag_block.count, instanced_geometry_definition_element_node, "name", "vertices")
                for vertex_idx in range(instanced_geometry_definition.vertices_tag_block.count):
                    vertex_element_node = None
                    if XML_OUTPUT:
                        vertex_element_node = TAG.xml_doc.createElement('element')
                        vertex_element_node.setAttribute('index', str(vertex_idx))
                        vertex_node.appendChild(vertex_element_node)

                    vertex = LEVEL.Vertex()
                    vertex.translation = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(vertex_element_node, "translation"), True)
                    vertex.first_edge = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(vertex_element_node, "first edge"))

                    instanced_geometry_definition.vertices.append(vertex)

            if instanced_geometry_definition.bsp_physics_tag_block.count > 0:
                instanced_geometry_definition.bsp_physics_header = TAG.TagBlockHeader().read(input_stream, TAG)
                bsp_physics_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.bsp_physics_tag_block.count, instanced_geometry_definition_element_node, "name", "bsp physics")
                for bsp_physics_idx in range(instanced_geometry_definition.bsp_physics_tag_block.count):
                    bsp_physics_element_node = None
                    if XML_OUTPUT:
                        bsp_physics_element_node = TAG.xml_doc.createElement('element')
                        bsp_physics_element_node.setAttribute('index', str(bsp_physics_idx))
                        bsp_physics_node.appendChild(bsp_physics_element_node)

                    bsp_physics = LEVEL.BSPPhysics()
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
                    bsp_physics.mopp_code_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(bsp_physics_element_node, "mopp code data"))
                    input_stream.read(8) # Padding?

                    instanced_geometry_definition.bsp_physics.append(bsp_physics)

                for bsp_physics_idx, bsp_physics in enumerate(instanced_geometry_definition.bsp_physics):
                    bsp_physics_element_node = None
                    if XML_OUTPUT:
                        bsp_physics_element_node = bsp_physics_node.childNodes[bsp_physics_idx]

                    bsp_physics.mopp_code_data = input_stream.read(bsp_physics.mopp_code_tag_data.size)

            if instanced_geometry_definition.render_leaves_tag_block.count > 0:
                instanced_geometry_definition.render_leaves_header = TAG.TagBlockHeader().read(input_stream, TAG)
                render_leaves_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.render_leaves_tag_block.count, instanced_geometry_definition_element_node, "name", "render leaves")
                for render_leaf_idx in range(instanced_geometry_definition.render_leaves_tag_block.count):
                    render_leaf_element_node = None
                    if XML_OUTPUT:
                        render_leaf_element_node = TAG.xml_doc.createElement('element')
                        render_leaf_element_node.setAttribute('index', str(render_leaf_idx))
                        render_leaves_node.appendChild(render_leaf_element_node)

                    render_leaf = LEVEL.RenderLeaf()
                    render_leaf.cluster = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(render_leaf_element_node, "cluster"))
                    render_leaf.surface_reference_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(render_leaf_element_node, "surface reference count"))
                    render_leaf.first_surface_reference_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(render_leaf_element_node, "first surface reference index"))

                    instanced_geometry_definition.render_leaves.append(render_leaf)

            if instanced_geometry_definition.surface_references_tag_block.count > 0:
                instanced_geometry_definition.surface_references_header = TAG.TagBlockHeader().read(input_stream, TAG)
                surface_references_node = tag_format.get_xml_node(XML_OUTPUT, instanced_geometry_definition.surface_references_tag_block.count, instanced_geometry_definition_element_node, "name", "surface references")
                for surface_reference_idx in range(instanced_geometry_definition.surface_references_tag_block.count):
                    surface_reference_element_node = None
                    if XML_OUTPUT:
                        surface_reference_element_node = TAG.xml_doc.createElement('element')
                        surface_reference_element_node.setAttribute('index', str(surface_reference_idx))
                        surface_references_node.appendChild(surface_reference_element_node)

                    surface_reference = LEVEL.SurfaceReference()
                    surface_reference.strip_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(surface_reference_element_node, "strip index"))
                    surface_reference.lightmap_triangle_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(surface_reference_element_node, "lightmap triangle index"))
                    surface_reference.bsp_node_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_reference_element_node, "bsp node index"))

                    instanced_geometry_definition.surface_references.append(surface_reference)

def read_instanced_geometry_instances(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT):
    if LEVEL.level_body.instanced_geometry_instances_tag_block.count > 0:
        instanced_geometry_instances_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.instanced_geometry_instances_tag_block.count, tag_node, "name", "instanced geometry instances")
        LEVEL.instanced_geometry_instances_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for instanced_geometry_instance_idx in range(LEVEL.level_body.instanced_geometry_instances_tag_block.count):
            instanced_geometry_instance_element_node = None
            if XML_OUTPUT:
                instanced_geometry_instance_element_node = TAG.xml_doc.createElement('element')
                instanced_geometry_instance_element_node.setAttribute('index', str(instanced_geometry_instance_idx))
                instanced_geometry_instances_node.appendChild(instanced_geometry_instance_element_node)

            instanced_geometry_instance = LEVEL.InstancedGeometryInstance()
            instanced_geometry_instance.scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(instanced_geometry_instance_element_node, "scale"))
            instanced_geometry_instance.forward = TAG.read_vector(input_stream, TAG, tag_format.XMLData(instanced_geometry_instance_element_node, "forward"))
            instanced_geometry_instance.left = TAG.read_vector(input_stream, TAG, tag_format.XMLData(instanced_geometry_instance_element_node, "left"))
            instanced_geometry_instance.up = TAG.read_vector(input_stream, TAG, tag_format.XMLData(instanced_geometry_instance_element_node, "up"))
            instanced_geometry_instance.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(instanced_geometry_instance_element_node, "position"), True)
            instanced_geometry_instance.instance_definition = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_instance_element_node, "instance definition", None, LEVEL.level_body.instanced_geometry_definition_tag_block.count, "structure_bsp_instanced_geometry_definition_block"))
            instanced_geometry_instance.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_instance_element_node, "flags", InstanceFlags))
            input_stream.read(20) # Padding?
            instanced_geometry_instance.checksum = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(instanced_geometry_instance_element_node, "checksum"))

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            instanced_geometry_instance.name_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            instanced_geometry_instance.pathfinding_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_instance_element_node, "pathfinding policy", PathfindingPolicyEnum))
            instanced_geometry_instance.lightmapping_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_instance_element_node, "lightmapping policy", LightmappingPolicyEnum))

            LEVEL.instanced_geometry_instances.append(instanced_geometry_instance)

        for instanced_geometry_instance_idx, instanced_geometry_instance in enumerate(LEVEL.instanced_geometry_instances):
            instanced_geometry_instance_element_node = None
            if XML_OUTPUT:
                instanced_geometry_instance_element_node = instanced_geometry_instances_node.childNodes[instanced_geometry_instance_idx]

            if instanced_geometry_instance.name_length > 0:
                instanced_geometry_instance.name = TAG.read_variable_string_no_terminator(input_stream, instanced_geometry_instance.name_length, TAG, tag_format.XMLData(instanced_geometry_instance_element_node, "name"))

def process_file(input_stream, report):
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
    read_bsp_body(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_import_info(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_collision_materials(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_collision_bsps(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_unused_nodes(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_leaves(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_surface_references(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    LEVEL.cluster_data = input_stream.read(LEVEL.level_body.cluster_raw_data.size)
    read_cluster_portals(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_fog_planes(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_weather_palette(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_weather_polyhedra(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_detail_objects(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_clusters(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_materials(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_sky_owner_cluster(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_conveyor_surfaces(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_breakable_surfaces(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_pathfinding_data(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_pathfinding_edges(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_background_sound_palette(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_sound_environment_palette(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    LEVEL.sound_pas_data = input_stream.read(LEVEL.level_body.sound_pas_raw_data.size)
    read_markers(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_runtime_decals(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_environment_object_palette(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_environment_object(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_lightmaps(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_leaf_map_leaves(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_leaf_map_connections(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_errors(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_precomputed_lighting(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_instanced_geometry_definition(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)
    read_instanced_geometry_instances(LEVEL, TAG, input_stream, tag_node, XML_OUTPUT)

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
