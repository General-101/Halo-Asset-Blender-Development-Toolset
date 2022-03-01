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

from mathutils import Vector
from .format_retail import CollisionAsset
from ..global_functions.tag_format import TagAsset

DEBUG_PARSER = False
DEBUG_HEADER = True
DEBUG_BODY = True
DEBUG_MATERIALS = True
DEBUG_REGIONS = True
DEBUG_PERMUTATIONS = True
DEBUG_PATHFINDING_SPHERES = True
DEBUG_NODES = True
DEBUG_BSPS = True
DEBUG_BSP3D_NODES = True
DEBUG_PLANES = True
DEBUG_LEAVES = True
DEBUG_BSP2D_REFERENCES = True
DEBUG_BSP2D_NODES = True
DEBUG_SURFACES = True
DEBUG_EDGES = True
DEBUG_VERTICES = True

def process_file_retail(input_stream, report):
    TAG = TagAsset()
    COLLISION = CollisionAsset()

    header_struct = struct.unpack('>hbb32s4sIIIIHbb4s', input_stream.read(64))
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

    body_struct = struct.unpack('>Ih2xff52xf40x4s4xiIf4s4xiIf4s4xiI4s4xiIf4s4xiIf2xh24xh2xff16xfff112xf4s4xiI4s4xiI4s4xiI8xf112xiIIiIIiII16xffffffiIIiII', input_stream.read(664))
    COLLISION.coll_body = COLLISION.CollBody()
    COLLISION.coll_body.flags = body_struct[0]
    COLLISION.coll_body.indirect_damage_material = body_struct[1]
    COLLISION.coll_body.maximum_body_vitality = body_struct[2]
    COLLISION.coll_body.body_system_shock = body_struct[3]
    COLLISION.coll_body.friendly_damage_resistance = body_struct[4]
    COLLISION.coll_body.localized_damage_effect = TAG.TagRef(body_struct[5].decode().rstrip('\x00'), "", body_struct[6] + 1, body_struct[7], 0)
    COLLISION.coll_body.area_damage_effect_threshold = body_struct[8]
    COLLISION.coll_body.area_damage_effect = TAG.TagRef(body_struct[9].decode().rstrip('\x00'), "", body_struct[10] + 1, body_struct[11], 0)
    COLLISION.coll_body.body_damaged_threshold = body_struct[12]
    COLLISION.coll_body.body_damaged_effect = TAG.TagRef(body_struct[13].decode().rstrip('\x00'), "", body_struct[14] + 1, body_struct[15], 0)
    COLLISION.coll_body.body_depleted_effect = TAG.TagRef(body_struct[16].decode().rstrip('\x00'), "", body_struct[17] + 1, body_struct[18], 0)
    COLLISION.coll_body.body_destroyed_threshold = body_struct[19]
    COLLISION.coll_body.body_destroyed_effect = TAG.TagRef(body_struct[20].decode().rstrip('\x00'), "", body_struct[21] + 1, body_struct[22], 0)
    COLLISION.coll_body.maximum_shield_vitality = body_struct[23]
    COLLISION.coll_body.shield_material_type = body_struct[24]
    COLLISION.coll_body.shield_failure_function = body_struct[25]
    COLLISION.coll_body.shield_failure_threshold = body_struct[26]
    COLLISION.coll_body.shield_failing_leak_fraction = body_struct[27]
    COLLISION.coll_body.minimum_stun_damage = body_struct[28]
    COLLISION.coll_body.stun_time = body_struct[29]
    COLLISION.coll_body.recharge_time = body_struct[30]
    COLLISION.coll_body.shield_damaged_threshold = body_struct[31]
    COLLISION.coll_body.shield_damaged_effect = TAG.TagRef(body_struct[32].decode().rstrip('\x00'), "", body_struct[33] + 1, body_struct[34], 0)
    COLLISION.coll_body.shield_depleted_effect = TAG.TagRef(body_struct[35].decode().rstrip('\x00'), "", body_struct[36] + 1, body_struct[37], 0)
    COLLISION.coll_body.shield_recharging_effect = TAG.TagRef(body_struct[38].decode().rstrip('\x00'), "", body_struct[39] + 1, body_struct[40], 0)
    COLLISION.coll_body.shield_recharge_rate = body_struct[41]
    COLLISION.coll_body.materials_tag_block = TAG.TagBlock(body_struct[42], 32, body_struct[43], body_struct[44])
    COLLISION.coll_body.regions_tag_block = TAG.TagBlock(body_struct[45], 8, body_struct[46], body_struct[47])
    COLLISION.coll_body.modifiers_tag_block = TAG.TagBlock(body_struct[48], 0, body_struct[49], body_struct[50])
    COLLISION.coll_body.pathfinding_box = ((body_struct[51], body_struct[52]), (body_struct[53], body_struct[54]), (body_struct[55], body_struct[56]))
    COLLISION.coll_body.pathfinding_spheres_tag_block = TAG.TagBlock(body_struct[57], 32, body_struct[58], body_struct[59])
    COLLISION.coll_body.nodes_tag_block = TAG.TagBlock(body_struct[60], 64, body_struct[61], body_struct[62])

    if COLLISION.coll_body.localized_damage_effect.name_length > 1:
        tag_path = struct.unpack('>%ss' % COLLISION.coll_body.localized_damage_effect.name_length, input_stream.read(COLLISION.coll_body.localized_damage_effect.name_length))
        COLLISION.coll_body.localized_damage_effect.name = tag_path[0].decode().rstrip('\x00')

    if COLLISION.coll_body.area_damage_effect.name_length > 1:
        tag_path = struct.unpack('>%ss' % COLLISION.coll_body.area_damage_effect.name_length, input_stream.read(COLLISION.coll_body.area_damage_effect.name_length))
        COLLISION.coll_body.area_damage_effect.name = tag_path[0].decode().rstrip('\x00')

    if COLLISION.coll_body.body_damaged_effect.name_length > 1:
        tag_path = struct.unpack('>%ss' % COLLISION.coll_body.body_damaged_effect.name_length, input_stream.read(COLLISION.coll_body.body_damaged_effect.name_length))
        COLLISION.coll_body.body_damaged_effect.name = tag_path[0].decode().rstrip('\x00')

    if COLLISION.coll_body.body_depleted_effect.name_length > 1:
        tag_path = struct.unpack('>%ss' % COLLISION.coll_body.body_depleted_effect.name_length, input_stream.read(COLLISION.coll_body.body_depleted_effect.name_length))
        COLLISION.coll_body.body_depleted_effect.name = tag_path[0].decode().rstrip('\x00')

    if COLLISION.coll_body.body_destroyed_effect.name_length > 1:
        tag_path = struct.unpack('>%ss' % COLLISION.coll_body.body_destroyed_effect.name_length, input_stream.read(COLLISION.coll_body.body_destroyed_effect.name_length))
        COLLISION.coll_body.body_destroyed_effect.name = tag_path[0].decode().rstrip('\x00')

    if COLLISION.coll_body.shield_damaged_effect.name_length > 1:
        tag_path = struct.unpack('>%ss' % COLLISION.coll_body.shield_damaged_effect.name_length, input_stream.read(COLLISION.coll_body.shield_damaged_effect.name_length))
        COLLISION.coll_body.shield_damaged_effect.name = tag_path[0].decode().rstrip('\x00')

    if COLLISION.coll_body.shield_depleted_effect.name_length > 1:
        tag_path = struct.unpack('>%ss' % COLLISION.coll_body.shield_depleted_effect.name_length, input_stream.read(COLLISION.coll_body.shield_depleted_effect.name_length))
        COLLISION.coll_body.shield_depleted_effect.name = tag_path[0].decode().rstrip('\x00')

    if COLLISION.coll_body.shield_recharging_effect.name_length > 1:
        tag_path = struct.unpack('>%ss' % COLLISION.coll_body.shield_recharging_effect.name_length, input_stream.read(COLLISION.coll_body.shield_recharging_effect.name_length))
        COLLISION.coll_body.shield_recharging_effect.name = tag_path[0].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_BODY:
        print(" ===== Coll Body ===== ")
        print("Flags: ", COLLISION.coll_body.flags)
        print("Indirect Damage Material: ", COLLISION.coll_body.indirect_damage_material)
        print("Maximum Body Vitality: ", COLLISION.coll_body.maximum_body_vitality)
        print("Body System Shock: ", COLLISION.coll_body.body_system_shock)
        print("Friendly Damage Resistance: ", COLLISION.coll_body.friendly_damage_resistance)
        print("Localized Damage Effect Tag Reference Group: ", COLLISION.coll_body.localized_damage_effect.tag_group)
        print("Localized Damage Effect Tag Reference Name: ", COLLISION.coll_body.localized_damage_effect.name)
        print("Localized Damage Effect Tag Reference Name Length: ", COLLISION.coll_body.localized_damage_effect.name_length)
        print("Localized Damage Effect Tag Reference Salt: ", COLLISION.coll_body.localized_damage_effect.salt)
        print("Localized Damage Effect Tag Reference Index: ", COLLISION.coll_body.localized_damage_effect.index)
        print("Area Damage Effect Threshold: ", COLLISION.coll_body.area_damage_effect_threshold)
        print("Area Damage Effect Tag Reference Group: ", COLLISION.coll_body.area_damage_effect.tag_group)
        print("Area Damage Effect Tag Reference Name: ", COLLISION.coll_body.area_damage_effect.name)
        print("Area Damage Effect Tag Reference Name Length: ", COLLISION.coll_body.area_damage_effect.name_length)
        print("Area Damage Effect Tag Reference Salt: ", COLLISION.coll_body.area_damage_effect.salt)
        print("Area Damage Effect Tag Reference Index: ", COLLISION.coll_body.area_damage_effect.index)
        print("Body Damaged Threshold: ", COLLISION.coll_body.body_damaged_threshold)
        print("Body Damaged Effect Tag Reference Group: ", COLLISION.coll_body.body_damaged_effect.tag_group)
        print("Body Damaged Effect Tag Reference Name: ", COLLISION.coll_body.body_damaged_effect.name)
        print("Body Damaged Effect Tag Reference Name Length: ", COLLISION.coll_body.body_damaged_effect.name_length)
        print("Body Damaged Effect Tag Reference Salt: ", COLLISION.coll_body.body_damaged_effect.salt)
        print("Body Damaged Effect Tag Reference Index: ", COLLISION.coll_body.body_damaged_effect.index)
        print("Body Depleted Effect Tag Reference Group: ", COLLISION.coll_body.body_depleted_effect.tag_group)
        print("Body Depleted Effect Tag Reference Name: ", COLLISION.coll_body.body_depleted_effect.name)
        print("Body Depleted Effect Tag Reference Name Length: ", COLLISION.coll_body.body_depleted_effect.name_length)
        print("Body Depleted Effect Tag Reference Salt: ", COLLISION.coll_body.body_depleted_effect.salt)
        print("Body Depleted Effect Tag Reference Index: ", COLLISION.coll_body.body_depleted_effect.index)
        print("Body Destroyed Threshold: ", COLLISION.coll_body.body_destroyed_threshold)
        print("Body Destroyed Effect Tag Reference Group: ", COLLISION.coll_body.body_destroyed_effect.tag_group)
        print("Body Destroyed Effect Tag Reference Name: ", COLLISION.coll_body.body_destroyed_effect.name)
        print("Body Destroyed Effect Tag Reference Name Length: ", COLLISION.coll_body.body_destroyed_effect.name_length)
        print("Body Destroyed Effect Tag Reference Salt: ", COLLISION.coll_body.body_destroyed_effect.salt)
        print("Body Destroyed Effect Tag Reference Index: ", COLLISION.coll_body.body_destroyed_effect.index)
        print("Maximum Shield Vitality: ", COLLISION.coll_body.maximum_shield_vitality)
        print("Shield Material Type: ", COLLISION.coll_body.shield_material_type)
        print("Shield Failure Function: ", COLLISION.coll_body.shield_failure_function)
        print("Shield Failure Threshold: ", COLLISION.coll_body.shield_failure_threshold)
        print("Shield Failing Leak Fraction: ", COLLISION.coll_body.shield_failing_leak_fraction)
        print("Minimum Stun Damage: ", COLLISION.coll_body.minimum_stun_damage)
        print("Stun Time: ", COLLISION.coll_body.stun_time)
        print("Recharge Time: ", COLLISION.coll_body.recharge_time)
        print("Shield Damaged Threshold: ", COLLISION.coll_body.shield_damaged_threshold)
        print("Shield Damaged Effect Tag Reference Group: ", COLLISION.coll_body.shield_damaged_effect.tag_group)
        print("Shield Damaged Effect Tag Reference Name: ", COLLISION.coll_body.shield_damaged_effect.name)
        print("Shield Damaged Effect Tag Reference Name Length: ", COLLISION.coll_body.shield_damaged_effect.name_length)
        print("Shield Damaged Effect Tag Reference Salt: ", COLLISION.coll_body.shield_damaged_effect.salt)
        print("Shield Damaged Effect Tag Reference Index: ", COLLISION.coll_body.shield_damaged_effect.index)
        print("Shield Depleted Effect Tag Reference Group: ", COLLISION.coll_body.shield_depleted_effect.tag_group)
        print("Shield Depleted Effect Tag Reference Name: ", COLLISION.coll_body.shield_depleted_effect.name)
        print("Shield Depleted Effect Tag Reference Name Length: ", COLLISION.coll_body.shield_depleted_effect.name_length)
        print("Shield Depleted Effect Tag Reference Salt: ", COLLISION.coll_body.shield_depleted_effect.salt)
        print("Shield Depleted Effect Tag Reference Index: ", COLLISION.coll_body.shield_depleted_effect.index)
        print("Shield Recharging Effect Tag Reference Group: ", COLLISION.coll_body.shield_recharging_effect.tag_group)
        print("Shield Recharging Effect Tag Reference Name: ", COLLISION.coll_body.shield_recharging_effect.name)
        print("Shield Recharging Effect Tag Reference Name Length: ", COLLISION.coll_body.shield_recharging_effect.name_length)
        print("Shield Recharging Effect Tag Reference Salt: ", COLLISION.coll_body.shield_recharging_effect.salt)
        print("Shield Recharging Effect Tag Reference Index: ", COLLISION.coll_body.shield_recharging_effect.index)
        print("Shield Recharge Time: ", COLLISION.coll_body.shield_recharge_rate)
        print("Materials Tag Block Count: ", COLLISION.coll_body.materials_tag_block.count)
        print("Materials Tag Block Maximum Count: ", COLLISION.coll_body.materials_tag_block.maximum_count)
        print("Materials Tag Block Address: ", COLLISION.coll_body.materials_tag_block.address)
        print("Materials Tag Block Definition: ", COLLISION.coll_body.materials_tag_block.definition)
        print("Regions Tag Block Count: ", COLLISION.coll_body.regions_tag_block.count)
        print("Regions Tag Block Maximum Count: ", COLLISION.coll_body.regions_tag_block.maximum_count)
        print("Regions Tag Block Address: ", COLLISION.coll_body.regions_tag_block.address)
        print("Regions Tag Block Definition: ", COLLISION.coll_body.regions_tag_block.definition)
        print("Modifiers Tag Block Count: ", COLLISION.coll_body.modifiers_tag_block.count)
        print("Modifiers Tag Block Maximum Count: ", COLLISION.coll_body.modifiers_tag_block.maximum_count)
        print("Modifiers Tag Block Address: ", COLLISION.coll_body.modifiers_tag_block.address)
        print("Modifiers Tag Block Definition: ", COLLISION.coll_body.modifiers_tag_block.definition)
        print("Pathfinding Box: ", COLLISION.coll_body.pathfinding_box)
        print("Pathfinding Spheres Tag Block Count: ", COLLISION.coll_body.pathfinding_spheres_tag_block.count)
        print("Pathfinding Spheres Tag Block Maximum Count: ", COLLISION.coll_body.pathfinding_spheres_tag_block.maximum_count)
        print("Pathfinding Spheres Tag Block Address: ", COLLISION.coll_body.pathfinding_spheres_tag_block.address)
        print("Pathfinding Spheres Tag Block Definition: ", COLLISION.coll_body.pathfinding_spheres_tag_block.definition)
        print("Nodes Tag Block Count: ", COLLISION.coll_body.nodes_tag_block.count)
        print("Nodes Tag Block Maximum Count: ", COLLISION.coll_body.nodes_tag_block.maximum_count)
        print("Nodes Tag Block Address: ", COLLISION.coll_body.nodes_tag_block.address)
        print("Nodes Tag Block Definition: ", COLLISION.coll_body.nodes_tag_block.definition)
        print(" ")

    for materials_idx in range(COLLISION.coll_body.materials_tag_block.count):
        material_struct = struct.unpack('>32sIh2xff12xf8x', input_stream.read(72))
        material = COLLISION.Materials()
        material.name = material_struct[0].decode().rstrip('\x00')
        material.flags = material_struct[1]
        material.material_type = material_struct[2]
        material.shield_leak_percentage  = material_struct[3]
        material.shield_damage_multiplier = material_struct[4]
        material.body_damage_multiplier = material_struct[5]

        COLLISION.materials.append(material)

    if DEBUG_PARSER and DEBUG_MATERIALS:
        print(" ===== Materials ===== ")
        for material_idx, material in enumerate(COLLISION.materials):
            print(" ===== Material %s ===== " % material_idx)
            print("Material Name: ", material.name)
            print("Material Flags: ", material.flags)
            print("Material Type: ", material.material_type)
            print("Material Shield Leak Percentage: ", material.shield_leak_percentage)
            print("Material Shield Damage Multiplier: ", material.shield_damage_multiplier)
            print("Material Body Damage Multiplier: ", material.body_damage_multiplier)
            print(" ")

    for region_idx in range(COLLISION.coll_body.regions_tag_block.count):
        region_struct = struct.unpack('>32sI4xf12x4s4xiIiII', input_stream.read(84))
        region = COLLISION.Regions()
        region.name = region_struct[0].decode().rstrip('\x00')
        region.flags = region_struct[1]
        region.damage_threshold = region_struct[2]
        region.destroyed_effect = TAG.TagRef(region_struct[3].decode().rstrip('\x00'), "", region_struct[4] + 1, region_struct[5], 0)
        region.permutation_tag_block = TAG.TagBlock(region_struct[6], 32, region_struct[7], region_struct[8])

        COLLISION.regions.append(region)

    for region in COLLISION.regions:
        permutations = []
        if region.destroyed_effect.name_length > 1:
            tag_path = struct.unpack('>%ss' % region.destroyed_effect.name_length, input_stream.read(region.destroyed_effect.name_length))
            region.destroyed_effect.name = tag_path[0].decode().rstrip('\x00')

        for permutation_idx in range(region.permutation_tag_block.count):
            permutation_struct = struct.unpack('>32s', input_stream.read(32))
            permutation = COLLISION.Permutations()
            permutation.name = permutation_struct[0].decode().rstrip('\x00')

            permutations.append(permutation)

        region.permutations = permutations

    if DEBUG_PARSER and DEBUG_REGIONS:
        print(" ===== Regions ===== ")
        for region_idx, region in enumerate(COLLISION.regions):
            print(" ===== Region %s ===== " % region_idx)
            print("Region Name: ", region.name)
            print("Region Flags: ", region.flags)
            print("Region Damage Threshold: ", region.damage_threshold)
            print("Destroyed Effect Tag Reference Group: ", region.destroyed_effect.tag_group)
            print("Destroyed Effect Tag Reference Name: ", region.destroyed_effect.name)
            print("Destroyed Effect Tag Reference Name Length: ", region.destroyed_effect.name_length)
            print("Destroyed Effect Tag Reference Salt: ", region.destroyed_effect.salt)
            print("Destroyed Effect Tag Reference Index: ", region.destroyed_effect.index)
            print("Permutation Tag Block Count: ", region.permutation_tag_block.count)
            print("Permutation Tag Block Maximum Count: ", region.permutation_tag_block.maximum_count)
            print("Permutation Tag Block Address: ", region.permutation_tag_block.address)
            print("Permutation Tag Block Definition: ", region.permutation_tag_block.definition)
            print(" ")
            if DEBUG_PERMUTATIONS:
                for permutation_idx, permutation in enumerate(region.permutations):
                    print(" ===== Permutation %s ===== " % permutation_idx)
                    print("Permutation Name: ", permutation.name)
                    print(" ")

    for modifier_idx in range(COLLISION.coll_body.modifiers_tag_block.count):
        modifier_struct = struct.unpack('>52x', input_stream.read(52))

    for pathfinding_sphere_idx in range(COLLISION.coll_body.pathfinding_spheres_tag_block.count):
        pathfinding_sphere_struct = struct.unpack('>h14xffff', input_stream.read(32))
        pathfinding_sphere = COLLISION.PathfindingSphere()
        pathfinding_sphere.node = pathfinding_sphere_struct[0]
        pathfinding_sphere.center = Vector((pathfinding_sphere_struct[1], pathfinding_sphere_struct[2], pathfinding_sphere_struct[3])) * 100
        pathfinding_sphere.radius = pathfinding_sphere_struct[4]  * 100

        COLLISION.pathfinding_spheres.append(pathfinding_sphere)

    if DEBUG_PARSER and DEBUG_PATHFINDING_SPHERES:
        print(" ===== Pathfinding Spheres ===== ")
        for pathfinding_sphere_idx, pathfinding_sphere in enumerate(COLLISION.pathfinding_spheres):
            print(" ===== Pathfinding Sphere %s ===== " % pathfinding_sphere_idx)
            print("Pathfinding Sphere Node: ", pathfinding_sphere.node)
            print("Pathfinding Sphere Center: ", pathfinding_sphere.center)
            print("Pathfinding Sphere Radius: ", pathfinding_sphere.radius)
            print(" ")

    for node_idx in range(COLLISION.coll_body.nodes_tag_block.count):
        node_struct = struct.unpack('>32shhhh8xhhiII', input_stream.read(64))
        node = COLLISION.Nodes()
        node.name = node_struct[0].decode().rstrip('\x00')
        node.region = node_struct[1]
        node.parent = node_struct[2]
        node.sibling = node_struct[3]
        node.child = node_struct[4]
        node.unknown_0 = node_struct[5]
        node.unknown_1 = node_struct[6]
        node.bsps_tag_block = TAG.TagBlock(node_struct[7], 32, node_struct[8], node_struct[9])

        COLLISION.nodes.append(node)

    for node in COLLISION.nodes:
        bsps = []
        for bsp_idx in range(node.bsps_tag_block.count):
            bsp_struct = struct.unpack('>iIIiIIiIIiIIiIIiIIiIIiII', input_stream.read(96))
            bsp = COLLISION.BSP()
            bsp.bsp3d_nodes_tag_block = TAG.TagBlock(bsp_struct[0], 131072, bsp_struct[1], bsp_struct[2])
            bsp.planes_tag_block = TAG.TagBlock(bsp_struct[3], 65535, bsp_struct[4], bsp_struct[5])
            bsp.leaves_tag_block = TAG.TagBlock(bsp_struct[6], 65535, bsp_struct[7], bsp_struct[8])
            bsp.bsp2d_references_tag_block = TAG.TagBlock(bsp_struct[9], 131072, bsp_struct[10], bsp_struct[11])
            bsp.bsp2d_nodes_tag_block = TAG.TagBlock(bsp_struct[12], 65535, bsp_struct[13], bsp_struct[14])
            bsp.surfaces_tag_block = TAG.TagBlock(bsp_struct[15], 131072, bsp_struct[16], bsp_struct[17])
            bsp.edges_tag_block = TAG.TagBlock(bsp_struct[18], 262144, bsp_struct[19], bsp_struct[20])
            bsp.vertices_tag_block = TAG.TagBlock(bsp_struct[21], 131072, bsp_struct[22], bsp_struct[23])

            bsps.append(bsp)

        for bsp in bsps:
            bsp_3d_nodes = []
            planes = []
            leaves = []
            bsp2d_references = []
            bsp2d_nodes = []
            surfaces = []
            edges = []
            vertices = []
            for bsp3d_node_idx in range(bsp.bsp3d_nodes_tag_block.count):
                bsp_3d_node_struct = struct.unpack('>iii', input_stream.read(12))
                bsp_3d_node = COLLISION.BSP3DNode()
                bsp_3d_node.plane = bsp_3d_node_struct[0]
                bsp_3d_node.back_child = bsp_3d_node_struct[1]
                bsp_3d_node.front_child = bsp_3d_node_struct[2]

                bsp_3d_nodes.append(bsp_3d_node)

            for plane_idx in range(bsp.planes_tag_block.count):
                plane_struct = struct.unpack('>ffff', input_stream.read(16))
                plane = COLLISION.Plane()
                plane.translation = Vector((plane_struct[0], plane_struct[1], plane_struct[2])) * 100
                plane.distance = plane_struct[3] * 100

                planes.append(plane)

            for leaf_idx in range(bsp.leaves_tag_block.count):
                leaf_struct = struct.unpack('>hhi', input_stream.read(8))
                leaf = COLLISION.Leaf()
                leaf.flags = leaf_struct[0]
                leaf.bsp2d_reference_count = leaf_struct[1]
                leaf.first_bsp2d_reference = leaf_struct[2]

                leaves.append(leaf)

            for bsp2d_reference_idx in range(bsp.bsp2d_references_tag_block.count):
                bsp2d_reference_struct = struct.unpack('>ii', input_stream.read(8))
                bsp2d_reference = COLLISION.BSP2DReference()
                bsp2d_reference.plane = bsp2d_reference_struct[0]
                bsp2d_reference.bsp2d_node = bsp2d_reference_struct[1]

                bsp2d_references.append(bsp2d_reference)

            for bsp2d_nodes_idx in range(bsp.bsp2d_nodes_tag_block.count):
                bsp2d_node_struct = struct.unpack('>fffii', input_stream.read(20))
                bsp2d_node = COLLISION.BSP2DNode()
                bsp2d_node.plane_i = bsp2d_node_struct[0]
                bsp2d_node.plane_j = bsp2d_node_struct[1]
                bsp2d_node.distance = bsp2d_node_struct[2] * 100
                bsp2d_node.left_child = bsp2d_node_struct[3]
                bsp2d_node.right_child = bsp2d_node_struct[4]

                bsp2d_nodes.append(bsp2d_node)

            for surfaces_idx in range(bsp.surfaces_tag_block.count):
                surfaces_struct = struct.unpack('>iibbh', input_stream.read(12))
                surface = COLLISION.Surface()
                surface.plane = surfaces_struct[0]
                surface.first_edge = surfaces_struct[1]
                surface.flags = surfaces_struct[2]
                surface.breakable_surface = surfaces_struct[3]
                surface.material = surfaces_struct[4]

                surfaces.append(surface)

            for edge_idx in range(bsp.edges_tag_block.count):
                edge_struct = struct.unpack('>iiiiii', input_stream.read(24))
                edge = COLLISION.Edge()
                edge.start_vertex = edge_struct[0]
                edge.end_vertex = edge_struct[1]
                edge.forward_edge = edge_struct[2]
                edge.reverse_edge = edge_struct[3]
                edge.left_surface = edge_struct[4]
                edge.right_surface = edge_struct[5]

                edges.append(edge)

            for vertex_idx in range(bsp.vertices_tag_block.count):
                vertex_struct = struct.unpack('>fffi', input_stream.read(16))
                vertex = COLLISION.Vertex()
                vertex.translation = Vector((vertex_struct[0], vertex_struct[1], vertex_struct[2])) * 100
                vertex.first_edge = vertex_struct[3]

                vertices.append(vertex)

            bsp.bsp3d_nodes = bsp_3d_nodes
            bsp.planes = planes
            bsp.leaves = leaves
            bsp.bsp2d_references = bsp2d_references
            bsp.bsp2d_nodes = bsp2d_nodes
            bsp.surfaces = surfaces
            bsp.edges = edges
            bsp.vertices = vertices

        node.bsps = bsps

    if DEBUG_PARSER and DEBUG_NODES:
        print(" ===== Nodes ===== ")
        for node_idx, node in enumerate(COLLISION.nodes):
            print(" ===== Node %s ===== " % node_idx)
            print("Name: ", node.name)
            print("Region: ", node.region)
            print("Parent: ", node.parent)
            print("Sibling: ", node.sibling)
            print("Child: ", node.child)
            print("Unknown Value: ", node.unknown_0)
            print("Unknown Value: ", node.unknown_1)
            print("BSPs Tag Block Count: ", node.bsps_tag_block.count)
            print("BSPs Tag Block Maximum Count: ", node.bsps_tag_block.maximum_count)
            print("BSPs Tag Block Address: ", node.bsps_tag_block.address)
            print("BSPs Tag Block Definition: ", node.bsps_tag_block.definition)
            print(" ")
            if DEBUG_BSPS:
                for bsp_idx, bsp in enumerate(node.bsps):
                    print(" ===== BSP %s ===== " % bsp_idx)
                    print("BSP3D Nodes Tag Block Count: ", bsp.bsp3d_nodes_tag_block.count)
                    print("BSP3D Nodes Tag Block Maximum Count: ", bsp.bsp3d_nodes_tag_block.maximum_count)
                    print("BSP3D Nodes Tag Block Address: ", bsp.bsp3d_nodes_tag_block.address)
                    print("BSP3D Nodes Tag Block Definition: ", bsp.bsp3d_nodes_tag_block.definition)
                    print("Planes Tag Block Count: ", bsp.planes_tag_block.count)
                    print("Planes Tag Block Maximum Count: ", bsp.planes_tag_block.maximum_count)
                    print("Planes Tag Block Address: ", bsp.planes_tag_block.address)
                    print("Planes Tag Block Definition: ", bsp.planes_tag_block.definition)
                    print("Leaves Tag Block Count: ", bsp.leaves_tag_block.count)
                    print("Leaves Tag Block Maximum Count: ", bsp.leaves_tag_block.maximum_count)
                    print("Leaves Tag Block Address: ", bsp.leaves_tag_block.address)
                    print("Leaves Tag Block Definition: ", bsp.leaves_tag_block.definition)
                    print("BSP2D References Tag Block Count: ", bsp.bsp2d_references_tag_block.count)
                    print("BSP2D References Tag Block Maximum Count: ", bsp.bsp2d_references_tag_block.maximum_count)
                    print("BSP2D References Tag Block Address: ", bsp.bsp2d_references_tag_block.address)
                    print("BSP2D References Tag Block Definition: ", bsp.bsp2d_references_tag_block.definition)
                    print("BSP2D Nodes Tag Block Count: ", bsp.bsp2d_nodes_tag_block.count)
                    print("BSP2D Nodes Tag Block Maximum Count: ", bsp.bsp2d_nodes_tag_block.maximum_count)
                    print("BSP2D Nodes Tag Block Address: ", bsp.bsp2d_nodes_tag_block.address)
                    print("BSP2D Nodes Tag Block Definition: ", bsp.bsp2d_nodes_tag_block.definition)
                    print("Surfaces Tag Block Count: ", bsp.surfaces_tag_block.count)
                    print("Surfaces Tag Block Maximum Count: ", bsp.surfaces_tag_block.maximum_count)
                    print("Surfaces Tag Block Address: ", bsp.surfaces_tag_block.address)
                    print("Surfaces Tag Block Definition: ", bsp.surfaces_tag_block.definition)
                    print("Edges Tag Block Count: ", bsp.edges_tag_block.count)
                    print("Edges Tag Block Maximum Count: ", bsp.edges_tag_block.maximum_count)
                    print("Edges Tag Block Address: ", bsp.edges_tag_block.address)
                    print("Edges Tag Block Definition: ", bsp.edges_tag_block.definition)
                    print("Vertices Tag Block Count: ", bsp.vertices_tag_block.count)
                    print("Vertices Tag Block Maximum Count: ", bsp.vertices_tag_block.maximum_count)
                    print("Vertices Tag Block Address: ", bsp.vertices_tag_block.address)
                    print("Vertices Tag Block Definition: ", bsp.vertices_tag_block.definition)
                    print(" ")
                    if DEBUG_BSP3D_NODES:
                        for bsp3d_node_idx, bsp3d_node in enumerate(bsp.bsp3d_nodes):
                            print(" ===== BSP3D Node %s ===== " % bsp3d_node_idx)
                            print("Plane: ", bsp3d_node.plane)
                            print("Back Child: ", bsp3d_node.back_child)
                            print("Front Child: ", bsp3d_node.front_child)
                            print(" ")

                    if DEBUG_PLANES:
                         for plane_idx, plane in enumerate(bsp.planes):
                            print(" ===== Plane %s ===== " % plane_idx)
                            print("Plane Translation: ", plane.translation)
                            print("Plane Distance: ", plane.distance)
                            print(" ")

                    if DEBUG_LEAVES:
                        for leaf_idx, leaf in enumerate(bsp.leaves):
                            print(" ===== Leaf %s ===== " % leaf_idx)
                            print("Leaf Flags: ", leaf.flags)
                            print("Leaf BSP2D Reference Count: ", leaf.bsp2d_reference_count)
                            print("Leaf First BSP2D Reference: ", leaf.first_bsp2d_reference)
                            print(" ")

                    if DEBUG_BSP2D_REFERENCES:
                        for bsp2d_reference_idx, bsp2d_reference in enumerate(bsp.bsp2d_references):
                            print(" ===== BSP2D Reference %s ===== " % bsp2d_reference_idx)
                            print("BSP2D Reference Plane: ", bsp2d_reference.plane)
                            print("BSP2D Reference Node: ", bsp2d_reference.bsp2d_node)
                            print(" ")

                    if DEBUG_BSP2D_NODES:
                        for bsp2d_node_idx, bsp2d_node in enumerate(bsp.bsp2d_nodes):
                            print(" ===== BSP2D Node %s ===== " % bsp2d_node_idx)
                            print("Plane i: ", bsp2d_node.plane_i)
                            print("Plane j: ", bsp2d_node.plane_j)
                            print("Plane Distance: ", bsp2d_node.distance)
                            print("Left Child: ", bsp2d_node.left_child)
                            print("Right Child: ", bsp2d_node.right_child)
                            print(" ")

                    if DEBUG_SURFACES:
                         for surface_idx, surface in enumerate(bsp.surfaces):
                            print(" ===== Surface %s ===== " % surface_idx)
                            print("Surface Plane: ", surface.plane)
                            print("Surface First Edge: ", surface.first_edge)
                            print("Surface Flags: ", surface.flags)
                            print("Surface Breakable Surface: ", surface.breakable_surface)
                            print("Surface Material: ", surface.material)
                            print(" ")

                    if DEBUG_EDGES:
                        for edge_idx, edge in enumerate(bsp.edges):
                            print(" ===== Edge %s ===== " % edge_idx)
                            print("Edge Start Vertex: ", edge.start_vertex)
                            print("Edge End Vertex: ", edge.end_vertex)
                            print("Edge Forward : ", edge.forward_edge)
                            print("Edge Reverse: ", edge.reverse_edge)
                            print("Edge Left Surface: ", edge.left_surface)
                            print("Edge Right Surface: ", edge.right_surface)
                            print(" ")

                    if DEBUG_VERTICES:
                        for vertex_idx, vertex in enumerate(bsp.vertices):
                            print(" ===== Vertex %s ===== " % vertex_idx)
                            print("Vertex Translation: ", vertex.translation)
                            print("Vertex First Edge: ", vertex.first_edge)
                            print(" ")

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    return COLLISION
