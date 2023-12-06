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
from .format import CollisionAsset, CollisionFlags, MaterialTypeEnum, ShieldFailureFunctionEnum, MaterialFlags, RegionFlags, LeafFlags, SurfaceFlags

XML_OUTPUT = False

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    COLLISION = CollisionAsset()

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    COLLISION.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    COLLISION.coll_body = COLLISION.CollBody()
    COLLISION.coll_body.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", CollisionFlags))
    COLLISION.coll_body.indirect_damage_material = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "indirect damage material", None, 1, "collision_material_block"))
    input_stream.read(2) # Padding?
    COLLISION.coll_body.maximum_body_vitality = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum body vitality"))
    COLLISION.coll_body.body_system_shock = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "body system shock"))
    input_stream.read(52) # Padding?
    COLLISION.coll_body.friendly_damage_resistance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "friendly damage resistance"))
    input_stream.read(40) # Padding?
    COLLISION.coll_body.localized_damage_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "localized damage effect"))
    COLLISION.coll_body.area_damage_effect_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "area damage effect threshold"))
    COLLISION.coll_body.area_damage_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "area damage effect"))
    COLLISION.coll_body.body_damaged_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "body damaged threshold"))
    COLLISION.coll_body.body_damaged_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "body damaged effect"))
    COLLISION.coll_body.body_depleted_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "body depleted effect"))
    COLLISION.coll_body.body_destroyed_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "body destroyed threshold"))
    COLLISION.coll_body.body_destroyed_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "body destroyed effect"))
    COLLISION.coll_body.maximum_shield_vitality = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum shield vitality"))
    input_stream.read(2) # Padding?
    COLLISION.coll_body.shield_material_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "shield material type", MaterialTypeEnum))
    input_stream.read(24) # Padding?
    COLLISION.coll_body.shield_failure_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "shield failure function", ShieldFailureFunctionEnum))
    input_stream.read(2) # Padding?
    COLLISION.coll_body.shield_failure_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "shield failure threshold"))
    COLLISION.coll_body.shield_failing_leak_fraction = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "shield failing leak fraction"))
    input_stream.read(16) # Padding?
    COLLISION.coll_body.minimum_stun_damage = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum stun damage"))
    COLLISION.coll_body.stun_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "stun time"))
    COLLISION.coll_body.recharge_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "recharge time"))
    input_stream.read(112) # Padding?
    COLLISION.coll_body.shield_damaged_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "shield damaged threshold"))
    COLLISION.coll_body.shield_damaged_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "shield damaged effect"))
    COLLISION.coll_body.shield_depleted_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "shield depleted effect"))
    COLLISION.coll_body.shield_recharging_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "shield recharging effect"))
    input_stream.read(8) # Padding?
    COLLISION.coll_body.shield_recharge_rate = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "shield recharge rate"))
    input_stream.read(112) # Padding?
    COLLISION.coll_body.materials_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "materials"))
    COLLISION.coll_body.regions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "regions"))
    COLLISION.coll_body.modifiers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifiers"))
    input_stream.read(16) # Padding?
    COLLISION.coll_body.pathfinding_box_x = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "x"))
    COLLISION.coll_body.pathfinding_box_y = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "y"))
    COLLISION.coll_body.pathfinding_box_z = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "z"))
    COLLISION.coll_body.pathfinding_spheres_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "pathfinding spheres"))
    COLLISION.coll_body.nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "nodes"))

    if COLLISION.coll_body.localized_damage_effect.name_length > 0:
        COLLISION.coll_body.localized_damage_effect.name = TAG.read_variable_string(input_stream, COLLISION.coll_body.localized_damage_effect.name_length, TAG)

    if COLLISION.coll_body.area_damage_effect.name_length > 0:
        COLLISION.coll_body.area_damage_effect.name = TAG.read_variable_string(input_stream, COLLISION.coll_body.area_damage_effect.name_length, TAG)

    if COLLISION.coll_body.body_damaged_effect.name_length > 0:
        COLLISION.coll_body.body_damaged_effect.name = TAG.read_variable_string(input_stream, COLLISION.coll_body.body_damaged_effect.name_length, TAG)

    if COLLISION.coll_body.body_depleted_effect.name_length > 0:
        COLLISION.coll_body.body_depleted_effect.name = TAG.read_variable_string(input_stream, COLLISION.coll_body.body_depleted_effect.name_length, TAG)

    if COLLISION.coll_body.body_destroyed_effect.name_length > 0:
        COLLISION.coll_body.body_destroyed_effect.name = TAG.read_variable_string(input_stream, COLLISION.coll_body.body_destroyed_effect.name_length, TAG)

    if COLLISION.coll_body.shield_damaged_effect.name_length > 0:
        COLLISION.coll_body.shield_damaged_effect.name = TAG.read_variable_string(input_stream, COLLISION.coll_body.shield_damaged_effect.name_length, TAG)

    if COLLISION.coll_body.shield_depleted_effect.name_length > 0:
        COLLISION.coll_body.shield_depleted_effect.name = TAG.read_variable_string(input_stream, COLLISION.coll_body.shield_depleted_effect.name_length, TAG)

    if COLLISION.coll_body.shield_recharging_effect.name_length > 0:
        COLLISION.coll_body.shield_recharging_effect.name = TAG.read_variable_string(input_stream, COLLISION.coll_body.shield_recharging_effect.name_length, TAG)

    if XML_OUTPUT:
        localized_damage_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "localized damage effect")
        area_damage_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "area damage effect")
        body_damaged_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "body damaged effect")
        body_depleted_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "body depleted effect")
        body_destroyed_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "body destroyed effect")
        shield_damaged_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "shield damaged effect")
        shield_depleted_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "shield depleted effect")
        shield_recharging_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "shield recharging effect")
        COLLISION.coll_body.localized_damage_effect.append_xml_attributes(localized_damage_effect_node)
        COLLISION.coll_body.area_damage_effect.append_xml_attributes(area_damage_effect_node)
        COLLISION.coll_body.body_damaged_effect.append_xml_attributes(body_damaged_effect_node)
        COLLISION.coll_body.body_depleted_effect.append_xml_attributes(body_depleted_effect_node)
        COLLISION.coll_body.body_destroyed_effect.append_xml_attributes(body_destroyed_effect_node)
        COLLISION.coll_body.shield_damaged_effect.append_xml_attributes(shield_damaged_effect_node)
        COLLISION.coll_body.shield_depleted_effect.append_xml_attributes(shield_depleted_effect_node)
        COLLISION.coll_body.shield_recharging_effect.append_xml_attributes(shield_recharging_effect_node)

    COLLISION.materials = []
    material_node = tag_format.get_xml_node(XML_OUTPUT, COLLISION.coll_body.materials_tag_block.count, tag_node, "name", "materials")
    for materials_idx in range(COLLISION.coll_body.materials_tag_block.count):
        material_element_node = None
        if XML_OUTPUT:
            material_element_node = TAG.xml_doc.createElement('element')
            material_element_node.setAttribute('index', str(materials_idx))
            material_node.appendChild(material_element_node)

        material = COLLISION.Material()
        material.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(material_element_node, "name"))
        material.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(material_element_node, "flags", MaterialFlags))
        material.material_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(material_element_node, "material type", MaterialTypeEnum))
        input_stream.read(2) # Padding?
        material.shield_leak_percentage  = TAG.read_float(input_stream, TAG, tag_format.XMLData(material_element_node, "shield leak percentage"))
        material.shield_damage_multiplier = TAG.read_float(input_stream, TAG, tag_format.XMLData(material_element_node, "shield damage multiplier"))
        input_stream.read(12) # Padding?
        material.body_damage_multiplier = TAG.read_float(input_stream, TAG, tag_format.XMLData(material_element_node, "body damage multiplier"))
        input_stream.read(8) # Padding?

        COLLISION.materials.append(material)

    COLLISION.regions = []
    region_node = tag_format.get_xml_node(XML_OUTPUT, COLLISION.coll_body.regions_tag_block.count, tag_node, "name", "regions")
    for region_idx in range(COLLISION.coll_body.regions_tag_block.count):
        region_element_node = None
        if XML_OUTPUT:
            region_element_node = TAG.xml_doc.createElement('element')
            region_element_node.setAttribute('index', str(region_idx))
            region_node.appendChild(region_element_node)

        region = COLLISION.Region()
        region.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(material_element_node, "name"))
        region.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(material_element_node, "flags", RegionFlags))
        input_stream.read(4) # Padding?
        region.damage_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(material_element_node, "damage threshold"))
        input_stream.read(12) # Padding?
        region.destroyed_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "destroyed effect"))
        region.permutations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "permutations"))

        COLLISION.regions.append(region)

    for region_idx, region in enumerate(COLLISION.regions):
        region_element_node = None

        region.permutations = []
        if region.destroyed_effect.name_length > 0:
            region.destroyed_effect.name = TAG.read_variable_string(input_stream, region.destroyed_effect.name_length, TAG)

        if XML_OUTPUT:
            region_element_node = region_node.childNodes[region_idx]
            destroyed_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, region_element_node, "name", "destroyed effect")
            region.destroyed_effect.append_xml_attributes(destroyed_effect_node)

        permutation_node = tag_format.get_xml_node(XML_OUTPUT, region.permutations_tag_block.count, region_element_node, "name", "permutations")
        for permutation_idx in range(region.permutations_tag_block.count):
            permutation_element_node = None
            if XML_OUTPUT:
                permutation_element_node = TAG.xml_doc.createElement('element')
                permutation_element_node.setAttribute('index', str(permutation_idx))
                permutation_node.appendChild(permutation_element_node)

            permutation = COLLISION.Permutation()
            permutation.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(material_element_node, "name"))

            region.permutations.append(permutation)

    for modifier_idx in range(COLLISION.coll_body.modifiers_tag_block.count):
        input_stream.read(52) # Padding?

    COLLISION.pathfinding_spheres = []
    pathfinding_sphere_node = tag_format.get_xml_node(XML_OUTPUT, COLLISION.coll_body.pathfinding_spheres_tag_block.count, tag_node, "name", "pathfinding spheres")
    for pathfinding_sphere_idx in range(COLLISION.coll_body.pathfinding_spheres_tag_block.count):
        pathfinding_sphere_element_node = None
        if XML_OUTPUT:
            pathfinding_sphere_element_node = TAG.xml_doc.createElement('element')
            pathfinding_sphere_element_node.setAttribute('index', str(pathfinding_sphere_idx))
            pathfinding_sphere_node.appendChild(pathfinding_sphere_element_node)

        pathfinding_sphere = COLLISION.PathfindingSphere()
        pathfinding_sphere.node = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_sphere_element_node, "node", None, COLLISION.coll_body.nodes_tag_block.count, "collision_node_block"))
        input_stream.read(14) # Padding?
        pathfinding_sphere.center = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(pathfinding_sphere_element_node, "center"))
        pathfinding_sphere.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(pathfinding_sphere_element_node, "radius"))

        COLLISION.pathfinding_spheres.append(pathfinding_sphere)

    COLLISION.nodes = []
    bone_node = tag_format.get_xml_node(XML_OUTPUT, COLLISION.coll_body.nodes_tag_block.count, tag_node, "name", "nodes")
    for node_idx in range(COLLISION.coll_body.nodes_tag_block.count):
        bone_element_node = None
        if XML_OUTPUT:
            bone_element_node = TAG.xml_doc.createElement('element')
            bone_element_node.setAttribute('index', str(node_idx))
            bone_node.appendChild(bone_element_node)

        node = COLLISION.Node()
        node.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(bone_element_node, "name"))
        node.region = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(bone_element_node, "region", None, COLLISION.coll_body.regions_tag_block.count, "collision_region_block"))
        node.parent = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(bone_element_node, "parent node", None, COLLISION.coll_body.nodes_tag_block.count, "collision_node_block"))
        node.sibling = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(bone_element_node, "next sibling node", None, COLLISION.coll_body.nodes_tag_block.count, "collision_node_block"))
        node.child = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(bone_element_node, "first child node", None, COLLISION.coll_body.nodes_tag_block.count, "collision_node_block"))
        input_stream.read(12) # Padding?
        node.bsps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(bone_element_node, "bsps"))

        COLLISION.nodes.append(node)

    for node_idx, node in enumerate(COLLISION.nodes):
        bone_element_node = None
        if XML_OUTPUT:
            bone_element_node = bone_node.childNodes[node_idx]

        node.bsps = []
        bsp_node = tag_format.get_xml_node(XML_OUTPUT, node.bsps_tag_block.count, bone_element_node, "name", "bsps")
        for bsp_idx in range(node.bsps_tag_block.count):
            bsp_element_node = None
            if XML_OUTPUT:
                bsp_element_node = TAG.xml_doc.createElement('element')
                bsp_element_node.setAttribute('index', str(bsp_idx))
                bsp_node.appendChild(bsp_element_node)

            bsp = COLLISION.BSP()
            bsp.bsp3d_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(bsp_element_node, "bsp3d nodes"))
            bsp.planes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(bsp_element_node, "planes"))
            bsp.leaves_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(bsp_element_node, "leaves"))
            bsp.bsp2d_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(bsp_element_node, "bsp2d references"))
            bsp.bsp2d_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(bsp_element_node, "bsp2d nodes"))
            bsp.surfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(bsp_element_node, "surfaces"))
            bsp.edges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(bsp_element_node, "edges"))
            bsp.vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(bsp_element_node, "vertices"))

            node.bsps.append(bsp)

        for bsp_idx, bsp in enumerate(node.bsps):
            bsp_element_node = None
            if XML_OUTPUT:
                bsp_element_node = bsp_node.childNodes[bsp_idx]

            bsp.bsp_3d_nodes = []
            bsp.planes = []
            bsp.leaves = []
            bsp.bsp2d_references = []
            bsp.bsp2d_nodes = []
            bsp.surfaces = []
            bsp.edges = []
            bsp.vertices = []
            bsp3d_node = tag_format.get_xml_node(XML_OUTPUT, bsp.bsp3d_nodes_tag_block.count, bsp_element_node, "name", "bsp3d nodes")
            plane_node = tag_format.get_xml_node(XML_OUTPUT, bsp.planes_tag_block.count, bsp_element_node, "name", "planes")
            leaf_node = tag_format.get_xml_node(XML_OUTPUT, bsp.leaves_tag_block.count, bsp_element_node, "name", "leaves")
            bsp2d_reference_node = tag_format.get_xml_node(XML_OUTPUT, bsp.bsp2d_references_tag_block.count, bsp_element_node, "name", "bsp2d references")
            bsp2d_node_node = tag_format.get_xml_node(XML_OUTPUT, bsp.bsp2d_nodes_tag_block.count, bsp_element_node, "name", "bsp2d nodes")
            surface_node = tag_format.get_xml_node(XML_OUTPUT, bsp.surfaces_tag_block.count, bsp_element_node, "name", "surfaces")
            edge_node = tag_format.get_xml_node(XML_OUTPUT, bsp.edges_tag_block.count, bsp_element_node, "name", "edges")
            vertex_node = tag_format.get_xml_node(XML_OUTPUT, bsp.vertices_tag_block.count, bsp_element_node, "name", "vertices")
            for bsp3d_node_idx in range(bsp.bsp3d_nodes_tag_block.count):
                bsp3d_element_node = None
                if XML_OUTPUT:
                    bsp3d_element_node = TAG.xml_doc.createElement('element')
                    bsp3d_element_node.setAttribute('index', str(bsp3d_node_idx))
                    bsp3d_node.appendChild(bsp3d_element_node)

                bsp_3d_node = COLLISION.BSP3DNode()
                bsp_3d_node.plane = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp3d_element_node, "plane"))
                bsp_3d_node.back_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp3d_element_node, "back child"))
                bsp_3d_node.front_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp3d_element_node, "front child"))

                bsp.bsp_3d_nodes.append(bsp_3d_node)

            for plane_idx in range(bsp.planes_tag_block.count):
                plane_element_node = None
                if XML_OUTPUT:
                    plane_element_node = TAG.xml_doc.createElement('element')
                    plane_element_node.setAttribute('index', str(plane_idx))
                    plane_node.appendChild(plane_element_node)

                bsp.planes.append(TAG.Plane3D().read(input_stream, TAG, tag_format.XMLData(plane_element_node, "plane")))

            for leaf_idx in range(bsp.leaves_tag_block.count):
                leaf_element_node = None
                if XML_OUTPUT:
                    leaf_element_node = TAG.xml_doc.createElement('element')
                    leaf_element_node.setAttribute('index', str(leaf_idx))
                    leaf_node.appendChild(leaf_element_node)

                leaf = COLLISION.Leaf()
                leaf.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(leaf_element_node, "flags", LeafFlags))
                leaf.bsp2d_reference_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(leaf_element_node, "bsp2d reference count"))
                leaf.first_bsp2d_reference = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(leaf_element_node, "first bsp2d reference"))

                bsp.leaves.append(leaf)

            for bsp2d_reference_idx in range(bsp.bsp2d_references_tag_block.count):
                bsp2d_reference_element_node = None
                if XML_OUTPUT:
                    bsp2d_reference_element_node = TAG.xml_doc.createElement('element')
                    bsp2d_reference_element_node.setAttribute('index', str(bsp2d_reference_idx))
                    bsp2d_reference_node.appendChild(bsp2d_reference_element_node)

                bsp2d_reference = COLLISION.BSP2DReference()
                bsp2d_reference.plane = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp2d_reference_element_node, "first bsp2d reference"))
                bsp2d_reference.bsp2d_node = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp2d_reference_element_node, "first bsp2d reference"))

                bsp.bsp2d_references.append(bsp2d_reference)

            for bsp2d_nodes_idx in range(bsp.bsp2d_nodes_tag_block.count):
                bsp2d_node_element_node = None
                if XML_OUTPUT:
                    bsp2d_node_element_node = TAG.xml_doc.createElement('element')
                    bsp2d_node_element_node.setAttribute('index', str(bsp2d_nodes_idx))
                    bsp2d_node_node.appendChild(bsp2d_node_element_node)

                bsp2d_node = COLLISION.BSP2DNode()
                bsp2d_node.plane = TAG.Plane2D().read(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "plane"))
                bsp2d_node.left_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "first bsp2d reference"))
                bsp2d_node.right_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bsp2d_node_element_node, "first bsp2d reference"))

                bsp.bsp2d_nodes.append(bsp2d_node)

            for surfaces_idx in range(bsp.surfaces_tag_block.count):
                surface_element_node = None
                if XML_OUTPUT:
                    surface_element_node = TAG.xml_doc.createElement('element')
                    surface_element_node.setAttribute('index', str(surfaces_idx))
                    surface_node.appendChild(surface_element_node)

                surface = COLLISION.Surface()
                surface.plane = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "first bsp2d reference"))
                surface.first_edge = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "first bsp2d reference"))
                surface.flags = TAG.read_flag_unsigned_byte(input_stream, TAG, tag_format.XMLData(surface_element_node, "flags", SurfaceFlags))
                surface.breakable_surface = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(surface_element_node, "breakable surface"))
                surface.material = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(surface_element_node, "material"))

                bsp.surfaces.append(surface)

            for edge_idx in range(bsp.edges_tag_block.count):
                edge_element_node = None
                if XML_OUTPUT:
                    edge_element_node = TAG.xml_doc.createElement('element')
                    edge_element_node.setAttribute('index', str(edge_idx))
                    edge_node.appendChild(edge_element_node)

                edge = COLLISION.Edge()
                edge.start_vertex = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "start vertex"))
                edge.end_vertex = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "end vertex"))
                edge.forward_edge = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "forward edge"))
                edge.reverse_edge = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "reverse edge"))
                edge.left_surface = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "left surface"))
                edge.right_surface = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_element_node, "right surface"))

                bsp.edges.append(edge)

            for vertex_idx in range(bsp.vertices_tag_block.count):
                vertex_element_node = None
                if XML_OUTPUT:
                    vertex_element_node = TAG.xml_doc.createElement('element')
                    vertex_element_node.setAttribute('index', str(vertex_idx))
                    vertex_node.appendChild(vertex_element_node)

                vertex = COLLISION.Vertex()
                vertex.translation = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(vertex_element_node, "position"), True)
                vertex.first_edge = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(vertex_element_node, "first edge"))

                bsp.vertices.append(vertex)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, COLLISION.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return COLLISION
