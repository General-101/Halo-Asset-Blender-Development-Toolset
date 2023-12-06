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

from xml.dom import minidom
from mathutils import Vector, Quaternion
from ....global_functions import tag_format
from .format import LevelAsset, LeafFlags, SurfaceFlags

XML_OUTPUT = False

def get_collision_material(input_stream, LEVEL, TAG, node_element):
    collision_material = LEVEL.CollisionMaterial()
    collision_material.shader_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "shader"))
    collision_material.unknown_0 = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "unknown 0"))

    return collision_material

def get_collision_bsp(input_stream, LEVEL, TAG, node_element):
    collision_bsp = LEVEL.CollisionBSP()
    collision_bsp.bsp3d_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "bsp3d nodes"))
    collision_bsp.planes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "planes"))
    collision_bsp.leaves_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "leaves"))
    collision_bsp.bsp2d_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "bsp2d references"))
    collision_bsp.bsp2d_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "bsp2d nodes"))
    collision_bsp.surfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "surfaces"))
    collision_bsp.edges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "edges"))
    collision_bsp.vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "vertices"))

    return collision_bsp

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    LEVEL = LevelAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    LEVEL.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    LEVEL.level_body = LEVEL.LevelBody()
    LEVEL.level_body.lightmap_bitmaps_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap bitmaps"))
    LEVEL.level_body.vehicle_floor = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "vehicle floor"))
    LEVEL.level_body.vehicle_ceiling = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "vehicle ceiling"))
    input_stream.read(20) # Padding?
    LEVEL.level_body.default_ambient_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "default ambient color"))
    input_stream.read(4) # Padding?
    LEVEL.level_body.default_distant_light_0_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "default distant light 0 color"))
    LEVEL.level_body.default_distant_light_0_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "default distant light 0 direction"))
    LEVEL.level_body.default_distant_light_1_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "default distant light 1 color"))
    LEVEL.level_body.default_distant_light_1_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "default distant light 1 direction"))
    input_stream.read(12) # Padding?
    LEVEL.level_body.default_reflection_tint = TAG.read_argb(input_stream, TAG, tag_format.XMLData(tag_node, "default reflection tint"))
    LEVEL.level_body.default_shadow_vector = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "default shadow vector"))
    LEVEL.level_body.default_shadow_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "default shadow color"))
    input_stream.read(4) # Padding?
    LEVEL.level_body.collision_materials_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision materials"))
    LEVEL.level_body.collision_bsps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision bsp"))
    LEVEL.level_body.nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "nodes"))
    LEVEL.level_body.world_bounds_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "world bounds x"))
    LEVEL.level_body.world_bounds_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "world bounds y"))
    LEVEL.level_body.world_bounds_z = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "world bounds z"))
    LEVEL.level_body.leaves_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "leaves"))
    LEVEL.level_body.leaf_surfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "leaf surfaces"))
    LEVEL.level_body.surfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "surfaces"))
    LEVEL.level_body.lightmaps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "lightmaps"))
    input_stream.read(12) # Padding?
    LEVEL.level_body.lens_flares_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "lens flares"))
    LEVEL.level_body.lens_flare_markers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "lens flare markers"))
    LEVEL.level_body.clusters_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "clusters"))
    LEVEL.level_body.cluster_data_raw_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "cluster data"))
    LEVEL.level_body.cluster_portals_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "cluster portals"))
    input_stream.read(12) # Padding?
    LEVEL.level_body.breakable_surfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "breakable surfaces"))
    LEVEL.level_body.fog_planes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "fog planes"))
    LEVEL.level_body.fog_regions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "fog regions"))
    LEVEL.level_body.fog_palettes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "fog palettes"))
    input_stream.read(24) # Padding?
    LEVEL.level_body.weather_palettes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weather palettes"))
    LEVEL.level_body.weather_polyhedras_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weather polyhedras"))
    input_stream.read(24) # Padding?
    LEVEL.level_body.pathfinding_surfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "pathfinding surfaces"))
    LEVEL.level_body.pathfinding_edges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "pathfinding edges"))
    LEVEL.level_body.background_sounds_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "background sounds palette"))
    LEVEL.level_body.sound_environments_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sound environments palette"))
    LEVEL.level_body.sound_pas_raw_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "sound pas data"))
    LEVEL.level_body.unknown_0 = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(tag_node, "unknown 0"))
    input_stream.read(20) # Padding?
    LEVEL.level_body.markers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "markers"))
    LEVEL.level_body.detail_objects_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "detail objects"))
    LEVEL.level_body.runtime_decals_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "runtime decals"))
    input_stream.read(12) # Padding?
    LEVEL.level_body.leaf_map_leaves_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "leaf map leaves"))
    LEVEL.level_body.leaf_map_portals_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "leaf map portals"))

    lightmap_bitmaps_tag_ref = LEVEL.level_body.lightmap_bitmaps_tag_ref
    lightmap_bitmaps_name_length = lightmap_bitmaps_tag_ref.name_length
    if lightmap_bitmaps_name_length > 0:
        lightmap_bitmaps_tag_ref.name = TAG.read_variable_string(input_stream, lightmap_bitmaps_name_length, TAG)

    if XML_OUTPUT:
        lightmap_bitmaps_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "lightmap bitmaps")
        lightmap_bitmaps_tag_ref.append_xml_attributes(lightmap_bitmaps_node)

    LEVEL.collision_materials = []
    LEVEL.collision_bsps = []
    LEVEL.nodes = []
    LEVEL.leaves = []
    LEVEL.leaf_surfaces = []
    LEVEL.surfaces = []
    LEVEL.lightmaps = []
    LEVEL.lens_flares = []
    LEVEL.lens_flare_markers = []
    LEVEL.clusters = []
    LEVEL.cluster_data = []
    LEVEL.cluster_portals = []
    LEVEL.breakable_surfaces = []
    LEVEL.fog_planes = []
    LEVEL.fog_regions = []
    LEVEL.fog_palettes = []
    LEVEL.weather_palettes = []
    LEVEL.weather_polyhedras = []
    LEVEL.pathfinding_surfaces = []
    LEVEL.pathfinding_edges = []
    LEVEL.background_sounds_palettes = []
    LEVEL.sound_environments_palettes = []
    LEVEL.markers = []
    LEVEL.detail_objects = []
    LEVEL.leaf_map_leaves = []
    LEVEL.leaf_map_portals = []

    collision_material_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.collision_materials_tag_block.count, tag_node, "name", "collision materials")
    for collision_material_idx in range(LEVEL.level_body.collision_materials_tag_block.count):
        collision_material_element_node = None
        if XML_OUTPUT:
            collision_material_element_node = TAG.xml_doc.createElement('element')
            collision_material_element_node.setAttribute('index', str(collision_material_idx))
            collision_material_node.appendChild(collision_material_element_node)

        LEVEL.collision_materials.append(get_collision_material(input_stream, LEVEL, TAG, collision_material_element_node))

    for collision_material_idx, collision_material in enumerate(LEVEL.collision_materials):
        collision_material_name_length = collision_material.shader_tag_ref.name_length
        if collision_material_name_length > 0:
            collision_material.shader_tag_ref.name = TAG.read_variable_string(input_stream, collision_material_name_length, TAG)

        if XML_OUTPUT:
            collision_material_element_node = collision_material_node.childNodes[collision_material_idx]
            control_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, collision_material_element_node, "name", "shader")
            collision_material.shader_tag_ref.append_xml_attributes(control_palette_tag_ref_node)

    collision_bsp_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.collision_bsps_tag_block.count, tag_node, "name", "collision bsp")
    for collision_bsp_idx in range(LEVEL.level_body.collision_bsps_tag_block.count):
        collision_bsp_element_node = None
        if XML_OUTPUT:
            collision_bsp_element_node = TAG.xml_doc.createElement('element')
            collision_bsp_element_node.setAttribute('index', str(collision_bsp_idx))
            collision_bsp_node.appendChild(collision_bsp_element_node)

        LEVEL.collision_bsps.append(get_collision_bsp(input_stream, LEVEL, TAG, collision_bsp_element_node))

    for collision_bsp_idx, collision_bsp in enumerate(LEVEL.collision_bsps):
        collision_bsp_element_node = None
        if XML_OUTPUT:
            collision_bsp_element_node = collision_bsp_node.childNodes[collision_bsp_idx]

        collision_bsp.bsp3d_nodes = []
        collision_bsp.planes = []
        collision_bsp.leaves = []
        collision_bsp.bsp2d_references = []
        collision_bsp.bsp2d_nodes = []
        collision_bsp.surfaces = []
        collision_bsp.edges = []
        collision_bsp.vertices = []
        bsp3d_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.bsp3d_nodes_tag_block.count, collision_bsp_element_node, "name", "bsp3d nodes")
        plane_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.planes_tag_block.count, collision_bsp_element_node, "name", "planes")
        leaf_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.leaves_tag_block.count, collision_bsp_element_node, "name", "leaves")
        bsp2d_reference_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.bsp2d_references_tag_block.count, collision_bsp_element_node, "name", "bsp2d references")
        bsp2d_node_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.bsp2d_nodes_tag_block.count, collision_bsp_element_node, "name", "bsp2d nodes")
        surface_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.surfaces_tag_block.count, collision_bsp_element_node, "name", "surfaces")
        edge_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.edges_tag_block.count, collision_bsp_element_node, "name", "edges")
        vertex_node = tag_format.get_xml_node(XML_OUTPUT, collision_bsp.vertices_tag_block.count, collision_bsp_element_node, "name", "vertices")
        for bsp3d_node_idx in range(collision_bsp.bsp3d_nodes_tag_block.count):
            bsp3d_node_element_node = None
            if XML_OUTPUT:
                bsp3d_node_element_node = TAG.xml_doc.createElement('element')
                bsp3d_node_element_node.setAttribute('index', str(bsp3d_node_idx))
                bsp3d_node.appendChild(bsp3d_node_element_node)

            bsp_3d_node = LEVEL.BSP3DNode()
            bsp_3d_node.plane = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp3d_node_element_node, "plane"))
            bsp_3d_node.back_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp3d_node_element_node, "back child"))
            bsp_3d_node.front_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp3d_node_element_node, "front child"))

            collision_bsp.bsp3d_nodes.append(bsp_3d_node)

        for plane_idx in range(collision_bsp.planes_tag_block.count):
            plane_element_node = None
            if XML_OUTPUT:
                plane_element_node = TAG.xml_doc.createElement('element')
                plane_element_node.setAttribute('index', str(plane_idx))
                plane_node.appendChild(plane_element_node)

            collision_bsp.planes.append(TAG.Plane3D().read(input_stream, TAG, tag_format.XMLData(plane_element_node, "plane")))

        for leaf_idx in range(collision_bsp.leaves_tag_block.count):
            leaf_element_node = None
            if XML_OUTPUT:
                leaf_element_node = TAG.xml_doc.createElement('element')
                leaf_element_node.setAttribute('index', str(leaf_idx))
                leaf_node.appendChild(leaf_element_node)

            leaf = LEVEL.Leaf()
            leaf.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(leaf_element_node, "flags", LeafFlags))
            leaf.bsp2d_reference_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(leaf_element_node, "bsp2d reference count"))
            leaf.first_bsp2d_reference = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(leaf_element_node, "first bsp2d reference"))

            collision_bsp.leaves.append(leaf)

        for bsp2d_reference_idx in range(collision_bsp.bsp2d_references_tag_block.count):
            bsp2d_reference_element_node = None
            if XML_OUTPUT:
                bsp2d_reference_element_node = TAG.xml_doc.createElement('element')
                bsp2d_reference_element_node.setAttribute('index', str(bsp2d_reference_idx))
                bsp2d_reference_node.appendChild(bsp2d_reference_element_node)

            bsp2d_reference = LEVEL.BSP2DReference()
            bsp2d_reference.plane = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp2d_reference_element_node, "first bsp2d reference"))
            bsp2d_reference.bsp2d_node = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp2d_reference_element_node, "first bsp2d reference"))

            collision_bsp.bsp2d_references.append(bsp2d_reference)

        for bsp2d_nodes_idx in range(collision_bsp.bsp2d_nodes_tag_block.count):
            bsp2d_node_element_node = None
            if XML_OUTPUT:
                bsp2d_node_element_node = TAG.xml_doc.createElement('element')
                bsp2d_node_element_node.setAttribute('index', str(bsp2d_nodes_idx))
                bsp2d_node_node.appendChild(bsp2d_node_element_node)

            bsp2d_node = LEVEL.BSP2DNode()
            bsp2d_node.plane = TAG.Plane2D().read(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "plane"))
            bsp2d_node.left_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "first bsp2d reference"))
            bsp2d_node.right_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "first bsp2d reference"))

            collision_bsp.bsp2d_nodes.append(bsp2d_node)

        for surfaces_idx in range(collision_bsp.surfaces_tag_block.count):
            surface_element_node = None
            if XML_OUTPUT:
                surface_element_node = TAG.xml_doc.createElement('element')
                surface_element_node.setAttribute('index', str(surfaces_idx))
                surface_node.appendChild(surface_element_node)

            surface = LEVEL.Surface()
            surface.plane = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "first bsp2d reference"))
            surface.first_edge = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "first bsp2d reference"))
            surface.flags = TAG.read_flag_unsigned_byte(input_stream, TAG, tag_format.XMLData(surface_element_node, "flags", SurfaceFlags))
            surface.breakable_surface = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(surface_element_node, "breakable surface"))
            surface.material = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(surface_element_node, "material"))

            collision_bsp.surfaces.append(surface)

        for edge_idx in range(collision_bsp.edges_tag_block.count):
            edge_element_node = None
            if XML_OUTPUT:
                edge_element_node = TAG.xml_doc.createElement('element')
                edge_element_node.setAttribute('index', str(edge_idx))
                edge_node.appendChild(edge_element_node)

            edge = LEVEL.Edge()
            edge.start_vertex = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "start vertex"))
            edge.end_vertex = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "end vertex"))
            edge.forward_edge = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "forward edge"))
            edge.reverse_edge = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "reverse edge"))
            edge.left_surface = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "left surface"))
            edge.right_surface = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "right surface"))

            collision_bsp.edges.append(edge)

        for vertex_idx in range(collision_bsp.vertices_tag_block.count):
            vertex_element_node = None
            if XML_OUTPUT:
                vertex_element_node = TAG.xml_doc.createElement('element')
                vertex_element_node.setAttribute('index', str(vertex_idx))
                vertex_node.appendChild(vertex_element_node)

            vertex = LEVEL.Vertex()
            vertex.translation = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(vertex_element_node, "position"), True)
            vertex.first_edge = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(vertex_element_node, "first edge"))

            collision_bsp.vertices.append(vertex)

    nodes_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.nodes_tag_block.count, tag_node, "name", "nodes")
    for node_idx in range(LEVEL.level_body.nodes_tag_block.count):
        node_element_node = None
        if XML_OUTPUT:
            node_element_node = TAG.xml_doc.createElement('element')
            node_element_node.setAttribute('index', str(node_idx))
            nodes_node.appendChild(node_element_node)

        node = LEVEL.Nodes()
        node.unknown_0 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element_node, "unknown 0"))
        node.unknown_1 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element_node, "unknown 1"))
        node.unknown_2 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element_node, "unknown 2"))
        node.unknown_3 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element_node, "unknown 3"))
        node.unknown_4 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element_node, "unknown 4"))
        node.unknown_5 = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element_node, "unknown 5"))

        LEVEL.nodes.append(node)

    cluster_leaf_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.leaves_tag_block.count, tag_node, "name", "leaves")
    for cluster_leaf_idx in range(LEVEL.level_body.leaves_tag_block.count):
        cluster_leaf_element_node = None
        if XML_OUTPUT:
            cluster_leaf_element_node = TAG.xml_doc.createElement('element')
            cluster_leaf_element_node.setAttribute('index', str(cluster_leaf_idx))
            cluster_leaf_node.appendChild(cluster_leaf_element_node)

        cluster_leaf = LEVEL.ClusterLeaf()
        cluster_leaf.unknown_0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_leaf_element_node, "unknown 0"))
        cluster_leaf.unknown_1 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_leaf_element_node, "unknown 0"))
        cluster_leaf.unknown_2 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_leaf_element_node, "unknown 0"))
        cluster_leaf.unknown_3 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_leaf_element_node, "unknown 0"))
        cluster_leaf.cluster = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_leaf_element_node, "cluster"))
        cluster_leaf.surface_reference_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(cluster_leaf_element_node, "surface reference count"))
        cluster_leaf.surface_reference = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(cluster_leaf_element_node, "surface reference"))

        LEVEL.leaves.append(cluster_leaf)

    leaf_surface_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.leaf_surfaces_tag_block.count, tag_node, "name", "leaf surfaces")
    for leaf_surface_idx in range(LEVEL.level_body.leaf_surfaces_tag_block.count):
        leaf_surface_element_node = None
        if XML_OUTPUT:
            leaf_surface_element_node = TAG.xml_doc.createElement('element')
            leaf_surface_element_node.setAttribute('index', str(leaf_surface_idx))
            leaf_surface_node.appendChild(leaf_surface_element_node)

        leaf_surface = LEVEL.LeafSurface()
        leaf_surface.surface = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(leaf_surface_element_node, "surface"))
        leaf_surface.node = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(leaf_surface_element_node, "node"))

        LEVEL.leaf_surfaces.append(leaf_surface)

    surface_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.surfaces_tag_block.count, tag_node, "name", "surfaces")
    for surface_idx in range(LEVEL.level_body.surfaces_tag_block.count):
        surface_element_node = None
        if XML_OUTPUT:
            surface_element_node = TAG.xml_doc.createElement('element')
            surface_element_node.setAttribute('index', str(surface_idx))
            surface_node.appendChild(surface_element_node)

        surface = LEVEL.ClusterSurface()
        surface.v0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(surface_element_node, "v0"))
        surface.v1 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(surface_element_node, "v1"))
        surface.v2 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(surface_element_node, "v2"))
        LEVEL.surfaces.append(surface)

    lightmap_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.lightmaps_tag_block.count, tag_node, "name", "lightmaps")
    for lightmap_idx in range(LEVEL.level_body.lightmaps_tag_block.count):
        lightmap_element_node = None
        if XML_OUTPUT:
            lightmap_element_node = TAG.xml_doc.createElement('element')
            lightmap_element_node.setAttribute('index', str(lightmap_idx))
            lightmap_node.appendChild(lightmap_element_node)

        lightmap = LEVEL.Lightmaps()
        lightmap.bitmap_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(lightmap_element_node, "bitmap index"))
        input_stream.read(18) # Padding?
        lightmap.materials_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(lightmap_element_node, "materials"))

        LEVEL.lightmaps.append(lightmap)

    for lightmap_idx, lightmap in enumerate(LEVEL.lightmaps):
        lightmap_element_node = None
        if XML_OUTPUT:
            lightmap_element_node = lightmap_node.childNodes[lightmap_idx]

        lightmap.materials = []
        material_node = tag_format.get_xml_node(XML_OUTPUT, lightmap.materials_tag_block.count, lightmap_element_node, "name", "materials")
        for material_idx in range(lightmap.materials_tag_block.count):
            material_element_node = None
            if XML_OUTPUT:
                material_element_node = TAG.xml_doc.createElement('element')
                material_element_node.setAttribute('index', str(material_idx))
                material_node.appendChild(material_element_node)

            material = LEVEL.Material()
            material.shader_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(material_element_node, "shader"))
            material.shader_permutation = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(material_element_node, "shader permutation"))
            material.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(material_element_node, "flags"))
            material.surfaces = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(material_element_node, "surfaces"))
            material.surface_count = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(material_element_node, "surface count"))
            material.centroid = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(material_element_node, "centroid"), True)
            material.ambient_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(material_element_node, "ambient color"))
            material.distant_light_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(material_element_node, "distant light count"))
            input_stream.read(2) # Padding?
            material.distant_light_0_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(material_element_node, "distant light 0 color"))
            material.distant_light_0_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(material_element_node, "distant light 0 direction"))
            material.distant_light_1_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(material_element_node, "distant light 1 color"))
            material.distant_light_1_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(material_element_node, "distant light 1 direction"))
            input_stream.read(12) # Padding?
            material.reflection_tint = TAG.read_argb(input_stream, TAG, tag_format.XMLData(material_element_node, "reflection tint"))
            material.shadow_vector = TAG.read_vector(input_stream, TAG, tag_format.XMLData(material_element_node, "shadow vector"))
            material.shadow_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(material_element_node, "shadow color"))
            material.plane = TAG.Plane3D().read(input_stream, TAG, tag_format.XMLData(material_element_node, "plane"))
            material.breakable_surface = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(material_element_node, "breakable surface"))
            input_stream.read(6) # Padding?
            material.vertices_count = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(material_element_node, "vertices count"))
            material.vertices_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(material_element_node, "vertices offset"))
            material.unknown_cache_offset0 = TAG.read_unsigned_integer(input_stream, TAG, tag_format.XMLData(material_element_node, "unknown cache offset0"))
            material.vertices_cache_offset = TAG.read_unsigned_integer(input_stream, TAG, tag_format.XMLData(material_element_node, "vertices cache offset"))
            material.vertex_type = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(material_element_node, "vertex type"))
            input_stream.read(2) # Padding?
            material.lightmap_vertices_count = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(material_element_node, "lightmap vertices count"))
            material.lightmap_vertices_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(material_element_node, "lightmap vertices offset"))
            material.unknown_cache_offset1 = TAG.read_unsigned_integer(input_stream, TAG, tag_format.XMLData(material_element_node, "unknown_cache_offset1"))
            material.lightmap_vertices_cache_offset = TAG.read_unsigned_integer(input_stream, TAG, tag_format.XMLData(material_element_node, "lightmap_vertices_cache_offset"))
            material.uncompressed_vertices_raw_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(material_element_node, "uncompressed vertices"))
            material.compressed_vertices_raw_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(material_element_node, "compressed vertices"))

            lightmap.materials.append(material)

        for material_idx, material in enumerate(lightmap.materials):
            material_element_node = None
            uncompressed_render_element_node = None
            uncompressed_lightmap_element_node = None
            compressed_render_element_node = None
            compressed_lightmap_element_node = None
            if XML_OUTPUT:
                material_element_node = material_node.childNodes[material_idx]

            material.uncompressed_render_vertices = []
            material.uncompressed_lightmap_vertices = []
            material.compressed_render_vertices = []
            material.compressed_lightmap_vertices = []
            uncompressed_vertex_node = tag_format.get_xml_node(XML_OUTPUT, material.uncompressed_vertices_raw_data.size, material_element_node, "name", "uncompressed vertices")
            compressed_vertex_node = tag_format.get_xml_node(XML_OUTPUT, material.compressed_vertices_raw_data.size, material_element_node, "name", "compressed vertices")
            if XML_OUTPUT:
                uncompressed_render_element_node = TAG.xml_doc.createElement('render')
                uncompressed_vertex_node.appendChild(uncompressed_render_element_node)
                uncompressed_lightmap_element_node = TAG.xml_doc.createElement('lightmap')
                uncompressed_vertex_node.appendChild(uncompressed_lightmap_element_node)
                compressed_render_element_node = TAG.xml_doc.createElement('render')
                compressed_vertex_node.appendChild(compressed_render_element_node)
                compressed_lightmap_element_node = TAG.xml_doc.createElement('lightmap')
                compressed_vertex_node.appendChild(compressed_lightmap_element_node)

            if material.shader_tag_ref.name_length > 0:
                material.shader_tag_ref.name = TAG.read_variable_string(input_stream, material.shader_tag_ref.name_length, TAG)

                if XML_OUTPUT:
                    material_shader_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, material_element_node, "name", "shader")
                    material.shader_tag_ref.append_xml_attributes(material_shader_tag_ref_node)

            TAG.big_endian = False

            for uncompressed_render_vertex_idx in range(material.vertices_count):
                uncompressed_render_vertex_element_node = None
                if XML_OUTPUT:
                    uncompressed_render_vertex_element_node = TAG.xml_doc.createElement('element')
                    uncompressed_render_vertex_element_node.setAttribute('index', str(uncompressed_render_vertex_idx))
                    uncompressed_render_element_node.appendChild(uncompressed_render_vertex_element_node)

                uncompressed_render_vertex = LEVEL.Vertices()
                uncompressed_render_vertex.translation = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(uncompressed_render_vertex_element_node, "position"), True)
                uncompressed_render_vertex.normal = TAG.read_vector(input_stream, TAG, tag_format.XMLData(uncompressed_render_vertex_element_node, "normal"))
                uncompressed_render_vertex.binormal = TAG.read_vector(input_stream, TAG, tag_format.XMLData(uncompressed_render_vertex_element_node, "binormal"))
                uncompressed_render_vertex.tangent = TAG.read_vector(input_stream, TAG, tag_format.XMLData(uncompressed_render_vertex_element_node, "tangent"))
                uncompressed_render_vertex.UV = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(uncompressed_render_vertex_element_node, "uv"))

                material.uncompressed_render_vertices.append(uncompressed_render_vertex)

            for uncompressed_lightmap_vertex_idx in range(material.lightmap_vertices_count):
                uncompressed_lightmap_vertex_element_node = None
                if XML_OUTPUT:
                    uncompressed_lightmap_vertex_element_node = TAG.xml_doc.createElement('element')
                    uncompressed_lightmap_vertex_element_node.setAttribute('index', str(uncompressed_lightmap_vertex_idx))
                    uncompressed_lightmap_element_node.appendChild(uncompressed_lightmap_vertex_element_node)

                uncompressed_lightmap_vertex = LEVEL.Vertices()
                uncompressed_lightmap_vertex.normal = TAG.read_vector(input_stream, TAG, tag_format.XMLData(uncompressed_lightmap_vertex_element_node, "normal"))
                uncompressed_lightmap_vertex.UV = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(uncompressed_lightmap_vertex_element_node, "uv"))

                material.uncompressed_lightmap_vertices.append(uncompressed_lightmap_vertex)

            for compressed_render_vertex_idx in range(material.vertices_count):
                compressed_render_vertex_element_node = None
                if XML_OUTPUT:
                    compressed_render_vertex_element_node = TAG.xml_doc.createElement('element')
                    compressed_render_vertex_element_node.setAttribute('index', str(compressed_render_vertex_idx))
                    compressed_render_element_node.appendChild(compressed_render_vertex_element_node)

                compressed_render_vertex = LEVEL.Vertices()
                compressed_render_vertex.translation = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(compressed_render_vertex_element_node, "position"), True)
                compressed_render_vertex.normal = TAG.read_unsigned_integer(input_stream, TAG, tag_format.XMLData(compressed_render_vertex_element_node, "normal"))
                compressed_render_vertex.binormal = TAG.read_unsigned_integer(input_stream, TAG, tag_format.XMLData(compressed_render_vertex_element_node, "binormal"))
                compressed_render_vertex.tangent = TAG.read_unsigned_integer(input_stream, TAG, tag_format.XMLData(compressed_render_vertex_element_node, "tangent"))
                compressed_render_vertex.UV = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(compressed_render_vertex_element_node, "uv"))

                material.compressed_render_vertices.append(compressed_render_vertex)

            for compressed_lightmap_vertex_idx in range(material.lightmap_vertices_count):
                compressed_lightmap_vertex_element_node = None
                if XML_OUTPUT:
                    compressed_lightmap_vertex_element_node = TAG.xml_doc.createElement('element')
                    compressed_lightmap_vertex_element_node.setAttribute('index', str(compressed_lightmap_vertex_idx))
                    compressed_lightmap_element_node.appendChild(compressed_lightmap_vertex_element_node)

                compressed_lightmap_vertex = LEVEL.Vertices()
                compressed_lightmap_vertex.normal = TAG.read_unsigned_integer(input_stream, TAG, tag_format.XMLData(compressed_lightmap_vertex_element_node, "normal"))
                compressed_lightmap_vertex.UV = TAG.read_point_2d_short(input_stream, TAG, tag_format.XMLData(compressed_lightmap_vertex_element_node, "uv"))

                material.compressed_lightmap_vertices.append(compressed_lightmap_vertex)

            TAG.big_endian = True

    for lens_flare_idx in range(LEVEL.level_body.lens_flares_tag_block.count):
        LEVEL.lens_flares.append(TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(material_element_node, "lensflare")))

    for lens_flare in LEVEL.lens_flares:
        if lens_flare.name_length > 0:
            lens_flare.name = TAG.read_variable_string(input_stream, lens_flare.name_length, TAG)

    lens_flare_marker_node = tag_format.get_xml_node(XML_OUTPUT, LEVEL.level_body.lens_flare_markers_tag_block.count, tag_node, "name", "lens flare markers")
    for lens_flare_marker_idx in range(LEVEL.level_body.lens_flare_markers_tag_block.count):
        lens_flare_marker_element_node = None
        if XML_OUTPUT:
            lens_flare_marker_element_node = TAG.xml_doc.createElement('element')
            lens_flare_marker_element_node.setAttribute('index', str(lens_flare_marker_idx))
            lens_flare_marker_node.appendChild(lens_flare_marker_element_node)

        lens_flare_marker = LEVEL.LensFlareMarker()
        lens_flare_marker.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(lens_flare_marker_element_node, "position"), True)
        lens_flare_marker.direction_i_compenent = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(lens_flare_marker_element_node, "direction i compenent"))
        lens_flare_marker.direction_j_compenent = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(lens_flare_marker_element_node, "direction j compenent"))
        lens_flare_marker.direction_k_compenent = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(lens_flare_marker_element_node, "direction k compenent"))
        lens_flare_marker.lens_flare_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(lens_flare_marker_element_node, "lens flare index"))

        LEVEL.lens_flare_markers.append(lens_flare_marker)

    for cluster_idx in range(LEVEL.level_body.clusters_tag_block.count):
        cluster_struct = struct.unpack('>hhhhhHHH24xiIIiIIhhiIIiIIiII', input_stream.read(104))
        cluster = LEVEL.Cluster()
        cluster.sky = cluster_struct[0]
        cluster.fog = cluster_struct[1]
        cluster.background_sound = cluster_struct[2]
        cluster.sound_environment = cluster_struct[3]
        cluster.weather = cluster_struct[4]
        cluster.transition_structure_bsp = cluster_struct[5]
        cluster.first_decal_index = cluster_struct[6]
        cluster.decal_count = cluster_struct[7]
        cluster.predicted_resources_tag_block = TAG.TagBlock(cluster_struct[8], 1024, cluster_struct[9], cluster_struct[10])
        cluster.subclusters_tag_block = TAG.TagBlock(cluster_struct[11], 4096, cluster_struct[12], cluster_struct[13])
        cluster.first_lens_flare_marker_index = cluster_struct[14]
        cluster.lens_flare_marker_count = cluster_struct[15]
        cluster.surface_indices_tag_block = TAG.TagBlock(cluster_struct[16], 32768, cluster_struct[17], cluster_struct[18])
        cluster.mirrors_tag_block = TAG.TagBlock(cluster_struct[19], 16, cluster_struct[20], cluster_struct[21])
        cluster.portals_tag_block = TAG.TagBlock(cluster_struct[22], 128, cluster_struct[23], cluster_struct[24])

        LEVEL.clusters.append(cluster)

    for cluster in LEVEL.clusters:
        predicted_resources = []
        subclusters = []
        surface_indices = []
        mirrors = []
        portals = []
        for predicted_resource_idx in range(cluster.predicted_resources_tag_block.count):
            predicted_resource = LEVEL.PredictedResource()
            predicted_resource_struct = struct.unpack('>hhI', input_stream.read(8))
            predicted_resource.type = predicted_resource_struct[0]
            predicted_resource.resource_index = predicted_resource_struct[1]
            predicted_resource.tag_index = predicted_resource_struct[2]

            predicted_resources.append(predicted_resource)

        for subclusters_idx in range(cluster.subclusters_tag_block.count):
            subcluster = LEVEL.Subcluster()
            subcluster_struct = struct.unpack('>ffffffiII', input_stream.read(36))
            subcluster.world_bounds_x = (subcluster_struct[0], subcluster_struct[1])
            subcluster.world_bounds_y = (subcluster_struct[2], subcluster_struct[3])
            subcluster.world_bounds_z = (subcluster_struct[4], subcluster_struct[5])
            subcluster.surface_indices_tag_block = TAG.TagBlock(subcluster_struct[6], 128, subcluster_struct[7], subcluster_struct[8])

            subclusters.append(subcluster)

        for subcluster in subclusters:
            sub_cluster_surface_indices = []
            for surface_indices_idx in range(subcluster.surface_indices_tag_block.count):
                surface_indices_struct = struct.unpack('>i', input_stream.read(4))

                sub_cluster_surface_indices.append(surface_indices_struct[0])

            subcluster.surface_indices = sub_cluster_surface_indices

        for surface_indices_idx in range(cluster.surface_indices_tag_block.count):
            surface_indices_struct = struct.unpack('>i', input_stream.read(4))

            surface_indices.append(surface_indices_struct[0])

        for mirror_idx in range(cluster.mirrors_tag_block.count):
            mirror = LEVEL.Mirror()
            mirror_struct = struct.unpack('>ffff20x4siiIiII', input_stream.read(64))
            mirror.plane_translation = Vector((mirror_struct[0], mirror_struct[1], mirror_struct[2]))
            mirror.plane_distance = mirror_struct[3]
            mirror.shader_tag_ref = TAG.TagRef(mirror_struct[4].decode().rstrip('\x00'), "", mirror_struct[6], mirror_struct[5], mirror_struct[7])
            mirror.vertices_tag_block = TAG.TagBlock(mirror_struct[8], 512, mirror_struct[9], mirror_struct[10])

            mirrors.append(mirror)

        for mirror in mirrors:
            mirror_vertices = []
            if mirror.shader_tag_ref.name_length > 0:
                tag_path = struct.unpack('>%ssx' % mirror.shader_tag_ref.name_length, input_stream.read(mirror.shader_tag_ref.name_length + 1))
                mirror.shader_tag_ref.name = tag_path[0].decode().rstrip('\x00')

            for vertex_idx in range(mirror.vertices_tag_block.count):
                vertex = LEVEL.Vertices()
                vertex_struct = struct.unpack('>fff', input_stream.read(12))
                vertex.translation = Vector((vertex_struct[0], vertex_struct[1], vertex_struct[2]))

                mirror_vertices.append(vertex)

            mirror.vertices = mirror_vertices

        for portal_idx in range(cluster.portals_tag_block.count):
            portal_struct = struct.unpack('>h', input_stream.read(2))

            portals.append(portal_struct[0])

        cluster.predicted_resources = predicted_resources
        cluster.subclusters = subclusters
        cluster.surface_indices = surface_indices
        cluster.mirrors = mirrors
        cluster.portals = portals

    cluster_data_size = LEVEL.level_body.cluster_data_raw_data.size
    if cluster_data_size > 0:
        cluster_raw_data = input_stream.read(LEVEL.level_body.cluster_data_raw_data.size)
        data_set = 0
        for cluster in LEVEL.clusters:
            cluster_data = LEVEL.ClusterData()
            cluster_data.unknown_0 = int.from_bytes(bytes(cluster_raw_data[0 + data_set]), "big")
            cluster_data.unknown_1 = int.from_bytes(bytes(cluster_raw_data[1 + data_set]), "big")
            cluster_data.unknown_2 = int.from_bytes(bytes(cluster_raw_data[2 + data_set]), "big")
            cluster_data.unknown_3 = int.from_bytes(bytes(cluster_raw_data[3 + data_set]), "big")
            data_set += 4

            LEVEL.cluster_data.append(cluster_data)

    for cluster_portal_idx in range(LEVEL.level_body.cluster_portals_tag_block.count):
        cluster_portal_struct = struct.unpack('>hhiffffi24xiII', input_stream.read(64))
        cluster_portal = LEVEL.ClusterPortal()
        cluster_portal.front_cluster = cluster_portal_struct[0]
        cluster_portal.back_cluster = cluster_portal_struct[1]
        cluster_portal.plane_index = cluster_portal_struct[2]
        cluster_portal.centroid = Vector((cluster_portal_struct[3], cluster_portal_struct[4], cluster_portal_struct[5]))
        cluster_portal.bounding_radius = cluster_portal_struct[6]
        cluster_portal.flags = cluster_portal_struct[7]
        cluster_portal.vertices_tag_block = TAG.TagBlock(cluster_portal_struct[8], 128, cluster_portal_struct[9], cluster_portal_struct[10])

        LEVEL.cluster_portals.append(cluster_portal)

    for cluster_portal in LEVEL.cluster_portals:
        vertices = []
        for vertex_idx in range(cluster_portal.vertices_tag_block.count):
            vertex = LEVEL.Vertices()
            vertex_struct = struct.unpack('>fff', input_stream.read(12))
            vertex.translation = Vector((vertex_struct[0], vertex_struct[1], vertex_struct[2])) * 100

            vertices.append(vertex)

        cluster_portal.vertices = vertices

    for breakable_surface_idx in range(LEVEL.level_body.breakable_surfaces_tag_block.count):
        breakable_surface_struct = struct.unpack('>ffffi28x', input_stream.read(48))
        breakable_surface = LEVEL.BreakableSurfaces()
        breakable_surface.centroid = Vector((breakable_surface_struct[0], breakable_surface_struct[1], breakable_surface_struct[2]))
        breakable_surface.radius = breakable_surface_struct[3]
        breakable_surface.collision_surface_index = breakable_surface_struct[4]

        LEVEL.breakable_surfaces.append(breakable_surface)

    for fog_plane_idx in range(LEVEL.level_body.fog_planes_tag_block.count):
        fog_plane_struct = struct.unpack('>hhffffiII', input_stream.read(32))
        fog_plane = LEVEL.FogPlane()
        fog_plane.front_region = fog_plane_struct[0]
        fog_plane.material_type = fog_plane_struct[1]
        fog_plane.plane_translation = Vector((fog_plane_struct[2], fog_plane_struct[3], fog_plane_struct[4]))
        fog_plane.plane_distance = fog_plane_struct[5]
        fog_plane.vertices_tag_block = TAG.TagBlock(fog_plane_struct[6], 128, fog_plane_struct[7], fog_plane_struct[8])

        LEVEL.fog_planes.append(fog_plane)

    for fog_plane in LEVEL.fog_planes:
        vertices = []
        for vertex_idx in range(fog_plane.vertices_tag_block.count):
            vertex = LEVEL.Vertices()
            vertex_struct = struct.unpack('>fff', input_stream.read(12))
            vertex.translation = Vector((vertex_struct[0], vertex_struct[1], vertex_struct[2])) * 100

            vertices.append(vertex)

        fog_plane.vertices = vertices

    for fog_region_idx in range(LEVEL.level_body.fog_regions_tag_block.count):
        fog_region_struct = struct.unpack('>36xhh', input_stream.read(40))
        fog_region = LEVEL.FogRegion()
        fog_region.fog_palette = fog_region_struct[0]
        fog_region.weather_palette = fog_region_struct[1]

        LEVEL.fog_regions.append(fog_region)

    for fog_palette_idx in range(LEVEL.level_body.fog_palettes_tag_block.count):
        fog_palette_struct = struct.unpack('>32s4siiI4x32s52x', input_stream.read(136))
        fog_palette = LEVEL.FogPalette()
        fog_palette.name = fog_palette_struct[0].decode().rstrip('\x00')
        fog_palette.fog_tag_ref = TAG.TagRef(fog_palette_struct[1].decode().rstrip('\x00'), "", fog_palette_struct[3], fog_palette_struct[2], fog_palette_struct[4])
        fog_palette.fog_scale_function = fog_palette_struct[5].decode().rstrip('\x00')

        LEVEL.fog_palettes.append(fog_palette)

    for fog_palette in LEVEL.fog_palettes:
        if fog_palette.fog_tag_ref.name_length > 0:
            tag_path = struct.unpack('>%ssx' % fog_palette.fog_tag_ref.name_length, input_stream.read(fog_palette.fog_tag_ref.name_length  + 1))
            fog_palette.fog_tag_ref.name = tag_path[0].decode().rstrip('\x00')

    for weather_palette_idx in range(LEVEL.level_body.weather_palettes_tag_block.count):
        weather_palette_struct = struct.unpack('>32s4siiI4x32s44x4siiIffff4x32s44x', input_stream.read(240))
        weather_palette = LEVEL.WeatherPalette()
        weather_palette.name = weather_palette_struct[0].decode().rstrip('\x00')
        weather_palette.particle_system_tag_ref = TAG.TagRef(weather_palette_struct[1].decode().rstrip('\x00'), "", weather_palette_struct[3], weather_palette_struct[2], weather_palette_struct[4])
        weather_palette.particle_system_scale_function = weather_palette_struct[5].decode().rstrip('\x00')
        weather_palette.wind_tag_ref = TAG.TagRef(weather_palette_struct[6].decode().rstrip('\x00'), "", weather_palette_struct[8], weather_palette_struct[7], weather_palette_struct[9])
        weather_palette.wind_direction = Vector((weather_palette_struct[10], weather_palette_struct[11], weather_palette_struct[12]))
        weather_palette.wind_magnitude = weather_palette_struct[13]
        weather_palette.wind_scale_function = weather_palette_struct[14].decode().rstrip('\x00')

        LEVEL.weather_palettes.append(weather_palette)

    for weather_palette in LEVEL.weather_palettes:
        if weather_palette.particle_system_tag_ref.name_length > 0:
            tag_path = struct.unpack('>%ssx' % weather_palette.particle_system_tag_ref.name_length, input_stream.read(weather_palette.particle_system_tag_ref.name_length + 1))
            weather_palette.particle_system_tag_ref.name = tag_path[0].decode().rstrip('\x00')

        if weather_palette.wind_tag_ref.name_length > 0:
            tag_path = struct.unpack('>%ssx' % weather_palette.wind_tag_ref.name_length, input_stream.read(weather_palette.wind_tag_ref.name_length + 1))
            weather_palette.wind_tag_ref.name = tag_path[0].decode().rstrip('\x00')

    for weather_polyhedra_idx in range(LEVEL.level_body.weather_polyhedras_tag_block.count):
        weather_polyhedra_struct = struct.unpack('>ffff4xiII', input_stream.read(32))
        weather_polyhedra = LEVEL.WeatherPolyhedras()
        weather_polyhedra.bounding_sphere_center = Vector((weather_polyhedra_struct[0], weather_polyhedra_struct[1], weather_polyhedra_struct[2]))
        weather_polyhedra.bounding_sphere_radius = weather_polyhedra_struct[3]
        weather_polyhedra.planes_tag_block = TAG.TagBlock(weather_polyhedra_struct[4], 16, weather_polyhedra_struct[5], weather_polyhedra_struct[6])

        LEVEL.weather_polyhedras.append(weather_polyhedra)

    for weather_polyhedra in LEVEL.weather_polyhedras:
        planes = []
        for plane_idx in range(weather_polyhedra.planes_tag_block.count):
            plane = TAG.Plane3D()
            plane_struct = struct.unpack('>ffff', input_stream.read(16))
            plane.point_3d = Vector((plane_struct[0], plane_struct[1], plane_struct[2]))
            plane.distance = plane_struct[3]

            planes.append(plane)

        weather_polyhedra.planes = planes

    for pathfinding_surface_idx in range(LEVEL.level_body.pathfinding_surfaces_tag_block.count):
        pathfinding_surface_struct = struct.unpack('>B', input_stream.read(1))

        LEVEL.pathfinding_surfaces.append(pathfinding_surface_struct[0])

    for pathfinding_edge_idx in range(LEVEL.level_body.pathfinding_edges_tag_block.count):
        pathfinding_edge_struct = struct.unpack('>B', input_stream.read(1))

        LEVEL.pathfinding_edges.append(pathfinding_edge_struct[0])

    for background_sounds_palette_idx in range(LEVEL.level_body.background_sounds_palette_tag_block.count):
        background_sounds_palette_struct = struct.unpack('>32s4siiI4x32s32x', input_stream.read(116))
        background_sounds_palette = LEVEL.BackgroundSoundsPalette()
        background_sounds_palette.name = background_sounds_palette_struct[0].decode().rstrip('\x00')
        background_sounds_palette.background_sound_tag_ref = TAG.TagRef(background_sounds_palette_struct[1].decode().rstrip('\x00'), "", background_sounds_palette_struct[3], background_sounds_palette_struct[2], background_sounds_palette_struct[4])
        background_sounds_palette.scale_function = background_sounds_palette_struct[5].decode().rstrip('\x00')

        LEVEL.background_sounds_palettes.append(background_sounds_palette)

    for background_sounds_palette in LEVEL.background_sounds_palettes:
        if background_sounds_palette.background_sound_tag_ref.name_length > 0:
            tag_path = struct.unpack('>%ssx' % background_sounds_palette.background_sound_tag_ref.name_length, input_stream.read(background_sounds_palette.background_sound_tag_ref.name_length + 1))
            background_sounds_palette.background_sound_tag_ref.name = tag_path[0].decode().rstrip('\x00')

    for sound_environments_palette_idx in range(LEVEL.level_body.sound_environments_palette_tag_block.count):
        sound_environments_palette_struct = struct.unpack('>32s4siiI32x', input_stream.read(80))
        sound_environments_palette = LEVEL.SoundEnvironmentsPalette()
        sound_environments_palette.name = sound_environments_palette_struct[0].decode().rstrip('\x00')
        sound_environments_palette.sound_environment_tag_ref = TAG.TagRef(sound_environments_palette_struct[1].decode().rstrip('\x00'), "", sound_environments_palette_struct[3], sound_environments_palette_struct[2], sound_environments_palette_struct[4])

        LEVEL.sound_environments_palettes.append(sound_environments_palette)

    for sound_environments_palette in LEVEL.sound_environments_palettes:
        if sound_environments_palette.sound_environment_tag_ref.name_length > 0:
            tag_path = struct.unpack('>%ssx' % sound_environments_palette.sound_environment_tag_ref.name_length, input_stream.read(sound_environments_palette.sound_environment_tag_ref.name_length + 1))
            sound_environments_palette.sound_environment_tag_ref.name = tag_path[0].decode().rstrip('\x00')

    sound_pas_raw_data_size = LEVEL.level_body.sound_pas_raw_data.size
    if cluster_data_size > 0:
        cluster_raw_data = input_stream.read(sound_pas_raw_data_size)

    for marker_idx in range(LEVEL.level_body.markers_tag_block.count):
        marker_struct = struct.unpack('>32sfffffff', input_stream.read(60))
        marker = LEVEL.Markers()
        marker.name = marker_struct[0].decode().rstrip('\x00')
        marker.rotation = Quaternion((marker_struct[4], marker_struct[1], marker_struct[2], marker_struct[3])).inverted()
        marker.translation = Vector((marker_struct[5], marker_struct[6], marker_struct[7])) * 100

        LEVEL.markers.append(marker)

    for detail_object_idx in range(LEVEL.level_body.detail_objects_tag_block.count):
        detail_object_struct = struct.unpack('>iIIiIIiIIiIIb15x', input_stream.read(64))
        detail_object = LEVEL.DetailObject()
        detail_object.cells_tag_block = TAG.TagBlock(detail_object_struct[0], 262144, detail_object_struct[1], detail_object_struct[2])
        detail_object.instances_tag_block = TAG.TagBlock(detail_object_struct[3], 2097152, detail_object_struct[4], detail_object_struct[5])
        detail_object.counts_tag_block = TAG.TagBlock(detail_object_struct[6], 8388608, detail_object_struct[7], detail_object_struct[8])
        detail_object.z_reference_vectors_tag_block = TAG.TagBlock(detail_object_struct[9], 262144, detail_object_struct[10], detail_object_struct[11])
        detail_object.flags = detail_object_struct[12]

        LEVEL.detail_objects.append(detail_object)

    for detail_object in LEVEL.detail_objects:
        cells = []
        instances = []
        counts = []
        z_reference_vectors = []
        for cell_idx in range(detail_object.cells_tag_block.count):
            cell = LEVEL.Cell()
            cell_struct = struct.unpack('>hhhhiii12x', input_stream.read(32))
            cell.cell_translation = Vector((cell_struct[0], cell_struct[1], cell_struct[2]))
            cell.offset_z = cell_struct[3]
            cell.valid_layers_flag = cell_struct[4]
            cell.start_index = cell_struct[5]
            cell.count_index = cell_struct[6]

            cells.append(cell)

        for instance_idx in range(detail_object.instances_tag_block.count):
            instance = LEVEL.Instance()
            instance_struct = struct.unpack('>bbbbh', input_stream.read(6))
            instance.position = Vector((instance_struct[0], instance_struct[1], instance_struct[2]))
            instance.data = instance_struct[3]
            instance.color = instance_struct[4]

            instances.append(instance)

        for count_idx in range(detail_object.counts_tag_block.count):
            count_struct = struct.unpack('>h', input_stream.read(2))

            counts.append(count_struct[0])

        for z_reference_vector_idx in range(detail_object.z_reference_vectors_tag_block.count):
            z_reference_vector = LEVEL.ZReferenceVector()
            z_reference_vector_struct = struct.unpack('>ffff', input_stream.read(16))
            z_reference_vector.unknown_0 = Vector((z_reference_vector_struct[0], z_reference_vector_struct[1], z_reference_vector_struct[2]))
            z_reference_vector.unknown_1 = z_reference_vector_struct[3]

            z_reference_vectors.append(z_reference_vector)

        detail_object.cells = cells
        detail_object.instances = instances
        detail_object.counts = counts
        detail_object.z_reference_vectors = z_reference_vectors

    for runtime_decals_idx in range(LEVEL.level_body.runtime_decals_tag_block.count):
        input_stream.read(16)

    for leaf_map_leaf_idx in range(LEVEL.level_body.leaf_map_leaves_tag_block.count):
        leaf_map_leaf_struct = struct.unpack('>iIIiII', input_stream.read(24))
        leaf_map_leaf = LEVEL.LeafMapLeaf()
        leaf_map_leaf.faces_tag_block = TAG.TagBlock(leaf_map_leaf_struct[0], 256, leaf_map_leaf_struct[1], leaf_map_leaf_struct[2])
        leaf_map_leaf.portal_indices_tag_block = TAG.TagBlock(leaf_map_leaf_struct[3], 256, leaf_map_leaf_struct[4], leaf_map_leaf_struct[5])

        LEVEL.leaf_map_leaves.append(leaf_map_leaf)

    for leaf_map_leaf in LEVEL.leaf_map_leaves:
        faces = []
        portal_indices = []
        for face_idx in range(leaf_map_leaf.faces_tag_block.count):
            face = LEVEL.Face()
            face_struct = struct.unpack('>iiII', input_stream.read(16))
            face.node_index = face_struct[0]
            face.vertices_tag_block = TAG.TagBlock(face_struct[1], 64, face_struct[2], face_struct[3])

            faces.append(face)

        for face in faces:
            vertices = []
            for vertex_idx in range(face.vertices_tag_block.count):
                vertex_struct = struct.unpack('>ff', input_stream.read(8))
                vertices.append((vertex_struct[0], vertex_struct[1]))

            face.vertices = vertices

        for portal_index_idx in range(leaf_map_leaf.portal_indices_tag_block.count):
            portal_index_struct = struct.unpack('>i', input_stream.read(4))

            portal_indices.append(portal_index_struct[0])

        leaf_map_leaf.faces = faces
        leaf_map_leaf.portal_indices = portal_indices

    for leaf_map_portal_idx in range(LEVEL.level_body.leaf_map_portals_tag_block.count):
        leaf_map_portal_struct = struct.unpack('>iiiiII', input_stream.read(24))
        leaf_map_portal = LEVEL.LeafMapPortal()
        leaf_map_portal.plane_index = leaf_map_portal_struct[0]
        leaf_map_portal.back_leaf_index = leaf_map_portal_struct[1]
        leaf_map_portal.front_leaf_index = leaf_map_portal_struct[2]
        leaf_map_portal.vertices_tag_block = TAG.TagBlock(leaf_map_portal_struct[3], 64, leaf_map_portal_struct[4], leaf_map_portal_struct[5])

        LEVEL.leaf_map_portals.append(leaf_map_portal)

    for leaf_map_portal in LEVEL.leaf_map_portals:
        vertices = []
        for vertex_idx in range(leaf_map_portal.vertices_tag_block.count):
            vertex = LEVEL.Vertices()
            vertex_struct = struct.unpack('>fff', input_stream.read(12))
            vertex.translation = Vector((vertex_struct[0], vertex_struct[1], vertex_struct[2]))

            vertices.append(vertex)

        leaf_map_portal.vertices = vertices

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
