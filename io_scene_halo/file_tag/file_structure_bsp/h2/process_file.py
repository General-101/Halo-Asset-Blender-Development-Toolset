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

from .format import LevelAsset
from mathutils import Vector, Quaternion

DEBUG_PARSER = False
DEBUG_HEADER = True
DEBUG_BODY = True
DEBUG_IMPORT_INFO = True
DEBUG_FILES = True
DEBUG_COLLISION_MATERIALS = True
DEBUG_COLLISION_BSPS = True
DEBUG_BSP3D_NODES = True
DEBUG_PLANES = True
DEBUG_LEAVES = True
DEBUG_BSP2D_REFERENCES = True
DEBUG_BSP2D_NODES = True
DEBUG_SURFACES = True
DEBUG_EDGES = True
DEBUG_VERTICES = True

def process_file_retail(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    LEVEL = LevelAsset()

    header_struct = struct.unpack('<hbb32s4sIIIIHbb4s', input_stream.read(64))
    LEVEL.header = TAG.Header()
    LEVEL.header.unk1 = header_struct[0]
    LEVEL.header.flags = header_struct[1]
    LEVEL.header.type = header_struct[2]
    LEVEL.header.name = header_struct[3].decode().rstrip('\x00')
    LEVEL.header.tag_group = header_struct[4].decode().rstrip('\x00')
    LEVEL.header.checksum = header_struct[5]
    LEVEL.header.data_offset = header_struct[6]
    LEVEL.header.data_length = header_struct[7]
    LEVEL.header.unk2 = header_struct[8]
    LEVEL.header.version = header_struct[9]
    LEVEL.header.destination = header_struct[10]
    LEVEL.header.plugin_handle = header_struct[11]
    LEVEL.header.engine_tag = header_struct[12].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_HEADER:
        print(" ===== Tag Header ===== ")
        print("Unknown Value: ", LEVEL.header.unk1)
        print("Flags: ", LEVEL.header.flags)
        print("Type: ", LEVEL.header.type)
        print("Name: ", LEVEL.header.name)
        print("Tag Group: ", LEVEL.header.tag_group)
        print("Checksum: ", LEVEL.header.checksum)
        print("Data Offset: ", LEVEL.header.data_offset)
        print("Data Length:", LEVEL.header.data_length)
        print("Unknown Value: ", LEVEL.header.unk2)
        print("Version: ", LEVEL.header.version)
        print("Destination: ", LEVEL.header.destination)
        print("Plugin Handle: ", LEVEL.header.plugin_handle)
        print("Engine Tag: ", LEVEL.header.engine_tag)
        print(" ")

    level_tag_block_header = struct.unpack('<16x', input_stream.read(16))
    level_body_struct = struct.unpack('<iII4xiIIiIIffiIIiIIffffffiIIiiIIIiIIiII24xiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiiIIIiIIiIIiIIiIIiII4xiIIiIIiIIiIIiIIiIIiIIiIIiII96xffffiII4siiIiiIII4xffffffiiIIIiIIiIIiIIiIIiIIiII', input_stream.read(792))
    LEVEL.level_body = LEVEL.LevelBody()
    LEVEL.level_body.import_info_tag_block = TAG.TagBlock(level_body_struct[0], 0, level_body_struct[1], level_body_struct[2])
    LEVEL.level_body.collision_materials_tag_block = TAG.TagBlock(level_body_struct[3], 0, level_body_struct[4], level_body_struct[5])
    LEVEL.level_body.collision_bsps_tag_block = TAG.TagBlock(level_body_struct[6], 0, level_body_struct[7], level_body_struct[8])
    LEVEL.level_body.vehicle_floor = level_body_struct[9]
    LEVEL.level_body.vehicle_ceiling = level_body_struct[10]
    LEVEL.level_body.unused_nodes_tag_block = TAG.TagBlock(level_body_struct[11], 0, level_body_struct[12], level_body_struct[13])
    LEVEL.level_body.leaves_tag_block = TAG.TagBlock(level_body_struct[14], 0, level_body_struct[15], level_body_struct[16])
    LEVEL.level_body.world_bounds_x = (level_body_struct[17], level_body_struct[18])
    LEVEL.level_body.world_bounds_y = (level_body_struct[19], level_body_struct[20])
    LEVEL.level_body.world_bounds_z = (level_body_struct[21], level_body_struct[22])
    LEVEL.level_body.surfaces_references_tag_block = TAG.TagBlock(level_body_struct[23], 0, level_body_struct[24], level_body_struct[25])
    LEVEL.level_body.cluster_raw_data = TAG.RawData(level_body_struct[26], level_body_struct[27], level_body_struct[28], level_body_struct[29], level_body_struct[30])
    LEVEL.level_body.cluster_portals_tag_block = TAG.TagBlock(level_body_struct[31], 0, level_body_struct[32], level_body_struct[33])
    LEVEL.level_body.fog_planes_tag_block = TAG.TagBlock(level_body_struct[34], 0, level_body_struct[35], level_body_struct[36])
    LEVEL.level_body.weather_palettes_tag_block = TAG.TagBlock(level_body_struct[37], 0, level_body_struct[38], level_body_struct[39])
    LEVEL.level_body.weather_polyhedras_tag_block = TAG.TagBlock(level_body_struct[40], 0, level_body_struct[41], level_body_struct[42])
    LEVEL.level_body.detail_objects_tag_block = TAG.TagBlock(level_body_struct[43], 0, level_body_struct[44], level_body_struct[45])
    LEVEL.level_body.clusters_tag_block = TAG.TagBlock(level_body_struct[46], 0, level_body_struct[47], level_body_struct[48])
    LEVEL.level_body.materials_tag_block = TAG.TagBlock(level_body_struct[49], 0, level_body_struct[50], level_body_struct[51])
    LEVEL.level_body.sky_owner_cluster_tag_block = TAG.TagBlock(level_body_struct[52], 0, level_body_struct[53], level_body_struct[54])
    LEVEL.level_body.conveyor_surfaces_cluster_tag_block = TAG.TagBlock(level_body_struct[55], 0, level_body_struct[56], level_body_struct[57])
    LEVEL.level_body.breakable_surfaces_tag_block = TAG.TagBlock(level_body_struct[58], 0, level_body_struct[59], level_body_struct[60])
    LEVEL.level_body.pathfinding_data_tag_block = TAG.TagBlock(level_body_struct[61], 0, level_body_struct[62], level_body_struct[63])
    LEVEL.level_body.pathfinding_edges_tag_block = TAG.TagBlock(level_body_struct[64], 0, level_body_struct[65], level_body_struct[66])
    LEVEL.level_body.background_sounds_palette_tag_block = TAG.TagBlock(level_body_struct[67], 0, level_body_struct[68], level_body_struct[69])
    LEVEL.level_body.sound_environment_palette_tag_block = TAG.TagBlock(level_body_struct[70], 0, level_body_struct[71], level_body_struct[72])
    LEVEL.level_body.sound_pas_raw_data = TAG.RawData(level_body_struct[73], level_body_struct[74], level_body_struct[75], level_body_struct[76], level_body_struct[77])
    LEVEL.level_body.markers_tag_block = TAG.TagBlock(level_body_struct[78], 0, level_body_struct[79], level_body_struct[80])
    LEVEL.level_body.runtime_decals_tag_block = TAG.TagBlock(level_body_struct[81], 0, level_body_struct[82], level_body_struct[83])
    LEVEL.level_body.environment_object_palette_tag_block = TAG.TagBlock(level_body_struct[84], 0, level_body_struct[85], level_body_struct[86])
    LEVEL.level_body.environment_objects_tag_block = TAG.TagBlock(level_body_struct[87], 0, level_body_struct[88], level_body_struct[89])
    LEVEL.level_body.lightmaps_tag_block = TAG.TagBlock(level_body_struct[90], 0, level_body_struct[91], level_body_struct[92])
    LEVEL.level_body.leaf_map_leaves_tag_block = TAG.TagBlock(level_body_struct[93], 0, level_body_struct[94], level_body_struct[95])
    LEVEL.level_body.leaf_map_connections_tag_block = TAG.TagBlock(level_body_struct[96], 0, level_body_struct[97], level_body_struct[98])
    LEVEL.level_body.errors_tag_block = TAG.TagBlock(level_body_struct[99], 0, level_body_struct[100], level_body_struct[101])
    LEVEL.level_body.precomputed_lighting_tag_block = TAG.TagBlock(level_body_struct[102], 0, level_body_struct[103], level_body_struct[104])
    LEVEL.level_body.instanced_geometries_definition_tag_block = TAG.TagBlock(level_body_struct[105], 0, level_body_struct[106], level_body_struct[107])
    LEVEL.level_body.instanced_geometry_instances_tag_block = TAG.TagBlock(level_body_struct[108], 0, level_body_struct[109], level_body_struct[110])
    LEVEL.level_body.ambience_sound_clusters_tag_block = TAG.TagBlock(level_body_struct[111], 0, level_body_struct[112], level_body_struct[113])
    LEVEL.level_body.reverb_sound_clusters_tag_block = TAG.TagBlock(level_body_struct[114], 0, level_body_struct[115], level_body_struct[116])
    LEVEL.level_body.transparent_planes_tag_block = TAG.TagBlock(level_body_struct[117], 0, level_body_struct[118], level_body_struct[119])
    LEVEL.level_body.vehicle_spherical_limit_radius = level_body_struct[120]
    LEVEL.level_body.vehicle_spherical_limit_center = Vector((level_body_struct[121], level_body_struct[122], level_body_struct[123]))
    LEVEL.level_body.debug_info_tag_block = TAG.TagBlock(level_body_struct[124], 0, level_body_struct[125], level_body_struct[126])
    LEVEL.level_body.decorators_bitmaps_tag_ref = TAG.TagRef(level_body_struct[127].decode('utf-8', 'replace').rstrip('\x00'), "", level_body_struct[129] + 1, level_body_struct[128], level_body_struct[130])
    LEVEL.level_body.decorators_0_raw_data = TAG.RawData(level_body_struct[131], level_body_struct[132], level_body_struct[133], level_body_struct[134], level_body_struct[135])
    LEVEL.level_body.decorators_0_vector = Vector((level_body_struct[136], level_body_struct[137], level_body_struct[138]))
    LEVEL.level_body.decorators_1_vector = Vector((level_body_struct[139], level_body_struct[140], level_body_struct[141]))
    LEVEL.level_body.decorators_1_raw_data = TAG.RawData(level_body_struct[142], level_body_struct[143], level_body_struct[144], level_body_struct[145], level_body_struct[146])
    LEVEL.level_body.breakable_surface_tag_block = TAG.TagBlock(level_body_struct[147], 0, level_body_struct[148], level_body_struct[149])
    LEVEL.level_body.water_definitions_tag_block = TAG.TagBlock(level_body_struct[150], 0, level_body_struct[151], level_body_struct[152])
    LEVEL.level_body.portal_device_mapping_tag_block = TAG.TagBlock(level_body_struct[153], 0, level_body_struct[154], level_body_struct[155])
    LEVEL.level_body.audibility_tag_block = TAG.TagBlock(level_body_struct[156], 0, level_body_struct[157], level_body_struct[158])
    LEVEL.level_body.object_fake_lightprobes_tag_block = TAG.TagBlock(level_body_struct[159], 0, level_body_struct[160], level_body_struct[161])
    LEVEL.level_body.decorators_tag_block = TAG.TagBlock(level_body_struct[162], 0, level_body_struct[163], level_body_struct[164])

    if DEBUG_PARSER and DEBUG_BODY:
        print(" ===== SBSP Body ===== ")
        print("Import Info Tag Block Count: ", LEVEL.level_body.import_info_tag_block.count)
        print("Import Info Tag Block Maximum Count: ", LEVEL.level_body.import_info_tag_block.maximum_count)
        print("Import Info Tag Block Address: ", LEVEL.level_body.import_info_tag_block.address)
        print("Import Info Tag Block Definition: ", LEVEL.level_body.import_info_tag_block.definition)
        print("Collision Materials Tag Block Count: ", LEVEL.level_body.collision_materials_tag_block.count)
        print("Collision Materials Tag Block Maximum Count: ", LEVEL.level_body.collision_materials_tag_block.maximum_count)
        print("Collision Materials Tag Block Address: ", LEVEL.level_body.collision_materials_tag_block.address)
        print("Collision Materials Tag Block Definition: ", LEVEL.level_body.collision_materials_tag_block.definition)
        print("Collision BSP Tag Block Count: ", LEVEL.level_body.collision_bsps_tag_block.count)
        print("Collision BSP Tag Block Maximum Count: ", LEVEL.level_body.collision_bsps_tag_block.maximum_count)
        print("Collision BSP Tag Block Address: ", LEVEL.level_body.collision_bsps_tag_block.address)
        print("Collision BSP Tag Block Definition: ", LEVEL.level_body.collision_bsps_tag_block.definition)
        print("Vehicle Floor: ", LEVEL.level_body.vehicle_floor)
        print("Vehicle Floor: ", LEVEL.level_body.vehicle_ceiling)
        print("Unused Nodes Tag Block Count: ", LEVEL.level_body.unused_nodes_tag_block.count)
        print("Unused Nodes Tag Block Maximum Count: ", LEVEL.level_body.unused_nodes_tag_block.maximum_count)
        print("Unused Nodes Tag Block Address: ", LEVEL.level_body.unused_nodes_tag_block.address)
        print("Unused Nodes Tag Block Definition: ", LEVEL.level_body.unused_nodes_tag_block.definition)
        print("Leaves Tag Block Count: ", LEVEL.level_body.leaves_tag_block.count)
        print("Leaves Tag Block Maximum Count: ", LEVEL.level_body.leaves_tag_block.maximum_count)
        print("Leaves Tag Block Address: ", LEVEL.level_body.leaves_tag_block.address)
        print("Leaves Tag Block Definition: ", LEVEL.level_body.leaves_tag_block.definition)
        print("World Bounds X: ", LEVEL.level_body.world_bounds_x)
        print("World Bounds Y: ", LEVEL.level_body.world_bounds_y)
        print("World Bounds Z: ", LEVEL.level_body.world_bounds_z)
        print("Surface Reference Tag Block Count: ", LEVEL.level_body.surfaces_references_tag_block.count)
        print("Surface Reference Tag Block Maximum Count: ", LEVEL.level_body.surfaces_references_tag_block.maximum_count)
        print("Surface Reference Tag Block Address: ", LEVEL.level_body.surfaces_references_tag_block.address)
        print("Surface Reference Tag Block Definition: ", LEVEL.level_body.surfaces_references_tag_block.definition)
        print("Cluster Data Info Size: ", LEVEL.level_body.cluster_raw_data.size)
        print("Cluster Data Info Flags: ", LEVEL.level_body.cluster_raw_data.flags)
        print("Cluster Data Info Raw Pointer: ", LEVEL.level_body.cluster_raw_data.raw_pointer)
        print("Cluster Data Info Pointer: ", LEVEL.level_body.cluster_raw_data.pointer)
        print("Cluster Data Info ID: ", LEVEL.level_body.cluster_raw_data.id)
        print("Cluster Portals Tag Block Count: ", LEVEL.level_body.cluster_portals_tag_block.count)
        print("Cluster Portals Tag Block Maximum Count: ", LEVEL.level_body.cluster_portals_tag_block.maximum_count)
        print("Cluster Portals Tag Block Address: ", LEVEL.level_body.cluster_portals_tag_block.address)
        print("Cluster Portals Tag Block Definition: ", LEVEL.level_body.cluster_portals_tag_block.definition)
        print("Fog Planes Tag Block Count: ", LEVEL.level_body.fog_planes_tag_block.count)
        print("Fog Planes Tag Block Maximum Count: ", LEVEL.level_body.fog_planes_tag_block.maximum_count)
        print("Fog Planes Tag Block Address: ", LEVEL.level_body.fog_planes_tag_block.address)
        print("Fog Planes Tag Block Definition: ", LEVEL.level_body.fog_planes_tag_block.definition)
        print("Weather Palettes Tag Block Count: ", LEVEL.level_body.weather_palettes_tag_block.count)
        print("Weather Palettes Tag Block Maximum Count: ", LEVEL.level_body.weather_palettes_tag_block.maximum_count)
        print("Weather Palettes Tag Block Address: ", LEVEL.level_body.weather_palettes_tag_block.address)
        print("Weather Palettes Tag Block Definition: ", LEVEL.level_body.weather_palettes_tag_block.definition)
        print("Weather Polyhedras Tag Block Count: ", LEVEL.level_body.weather_polyhedras_tag_block.count)
        print("Weather Polyhedras Tag Block Maximum Count: ", LEVEL.level_body.weather_polyhedras_tag_block.maximum_count)
        print("Weather Polyhedras Tag Block Address: ", LEVEL.level_body.weather_polyhedras_tag_block.address)
        print("Weather Polyhedras Tag Block Definition: ", LEVEL.level_body.weather_polyhedras_tag_block.definition)
        print("Detail Objects Tag Block Count: ", LEVEL.level_body.detail_objects_tag_block.count)
        print("Detail Objects Tag Block Maximum Count: ", LEVEL.level_body.detail_objects_tag_block.maximum_count)
        print("Detail Objects Tag Block Address: ", LEVEL.level_body.detail_objects_tag_block.address)
        print("Detail Objects Tag Block Definition: ", LEVEL.level_body.detail_objects_tag_block.definition)
        print("Clusters Tag Block Count: ", LEVEL.level_body.clusters_tag_block.count)
        print("Clusters Tag Block Maximum Count: ", LEVEL.level_body.clusters_tag_block.maximum_count)
        print("Clusters Tag Block Address: ", LEVEL.level_body.clusters_tag_block.address)
        print("Clusters Tag Block Definition: ", LEVEL.level_body.clusters_tag_block.definition)
        print("Materials Tag Block Count: ", LEVEL.level_body.materials_tag_block.count)
        print("Materials Tag Block Maximum Count: ", LEVEL.level_body.materials_tag_block.maximum_count)
        print("Materials Tag Block Address: ", LEVEL.level_body.materials_tag_block.address)
        print("Materials Tag Block Definition: ", LEVEL.level_body.materials_tag_block.definition)
        print("Sky Owner Cluster Tag Block Count: ", LEVEL.level_body.sky_owner_cluster_tag_block.count)
        print("Sky Owner Cluster Tag Block Maximum Count: ", LEVEL.level_body.sky_owner_cluster_tag_block.maximum_count)
        print("Sky Owner Cluster Tag Block Address: ", LEVEL.level_body.sky_owner_cluster_tag_block.address)
        print("Sky Owner Cluster Tag Block Definition: ", LEVEL.level_body.sky_owner_cluster_tag_block.definition)
        print("Conveyor Surfaces Tag Block Count: ", LEVEL.level_body.conveyor_surfaces_cluster_tag_block.count)
        print("Conveyor Surfaces Tag Block Maximum Count: ", LEVEL.level_body.conveyor_surfaces_cluster_tag_block.maximum_count)
        print("Conveyor Surfaces Tag Block Address: ", LEVEL.level_body.conveyor_surfaces_cluster_tag_block.address)
        print("Conveyor Surfaces Tag Block Definition: ", LEVEL.level_body.conveyor_surfaces_cluster_tag_block.definition)
        print("Breakable Surfaces Tag Block Count: ", LEVEL.level_body.breakable_surfaces_tag_block.count)
        print("Breakable Surfaces Tag Block Maximum Count: ", LEVEL.level_body.breakable_surfaces_tag_block.maximum_count)
        print("Breakable Surfaces Tag Block Address: ", LEVEL.level_body.breakable_surfaces_tag_block.address)
        print("Breakable Surfaces Tag Block Definition: ", LEVEL.level_body.breakable_surfaces_tag_block.definition)
        print("Pathfinding Data Tag Block Count: ", LEVEL.level_body.pathfinding_data_tag_block.count)
        print("Pathfinding Data Tag Block Maximum Count: ", LEVEL.level_body.pathfinding_data_tag_block.maximum_count)
        print("Pathfinding Data Tag Block Address: ", LEVEL.level_body.pathfinding_data_tag_block.address)
        print("Pathfinding Data Tag Block Definition: ", LEVEL.level_body.pathfinding_data_tag_block.definition)
        print("Pathfinding Edges Tag Block Count: ", LEVEL.level_body.pathfinding_edges_tag_block.count)
        print("Pathfinding Edges Tag Block Maximum Count: ", LEVEL.level_body.pathfinding_edges_tag_block.maximum_count)
        print("Pathfinding Edges Tag Block Address: ", LEVEL.level_body.pathfinding_edges_tag_block.address)
        print("Pathfinding Edges Tag Block Definition: ", LEVEL.level_body.pathfinding_edges_tag_block.definition)
        print("Background Sounds Palettes Tag Block Count: ", LEVEL.level_body.background_sounds_palette_tag_block.count)
        print("Background Sounds Palettes Tag Block Maximum Count: ", LEVEL.level_body.background_sounds_palette_tag_block.maximum_count)
        print("Background Sounds Palettes Tag Block Address: ", LEVEL.level_body.background_sounds_palette_tag_block.address)
        print("Background Sounds Palettes Tag Block Definition: ", LEVEL.level_body.background_sounds_palette_tag_block.definition)
        print("Sound Environment Palette Tag Block Count: ", LEVEL.level_body.sound_environment_palette_tag_block.count)
        print("Sound Environment Palette Tag Block Maximum Count: ", LEVEL.level_body.sound_environment_palette_tag_block.maximum_count)
        print("Sound Environment Palette Tag Block Address: ", LEVEL.level_body.sound_environment_palette_tag_block.address)
        print("Sound Environment Palette Tag Block Definition: ", LEVEL.level_body.sound_environment_palette_tag_block.definition)
        print("Sound PAS Data Info Size: ", LEVEL.level_body.sound_pas_raw_data.size)
        print("Sound PAS Data Info Flags: ", LEVEL.level_body.sound_pas_raw_data.flags)
        print("Sound PAS Data Info Raw Pointer: ", LEVEL.level_body.sound_pas_raw_data.raw_pointer)
        print("Sound PAS Data Info Pointer: ", LEVEL.level_body.sound_pas_raw_data.pointer)
        print("Sound PAS Data Info ID: ", LEVEL.level_body.sound_pas_raw_data.id)
        print("Markers Tag Block Count: ", LEVEL.level_body.markers_tag_block.count)
        print("Markers Tag Block Maximum Count: ", LEVEL.level_body.markers_tag_block.maximum_count)
        print("Markers Tag Block Address: ", LEVEL.level_body.markers_tag_block.address)
        print("Markers Tag Block Definition: ", LEVEL.level_body.markers_tag_block.definition)
        print("Runtime Decals Tag Block Count: ", LEVEL.level_body.runtime_decals_tag_block.count)
        print("Runtime Decals Tag Block Maximum Count: ", LEVEL.level_body.runtime_decals_tag_block.maximum_count)
        print("Runtime Decals Tag Block Address: ", LEVEL.level_body.runtime_decals_tag_block.address)
        print("Runtime Decals Tag Block Definition: ", LEVEL.level_body.runtime_decals_tag_block.definition)
        print("Environment Object Palette Tag Block Count: ", LEVEL.level_body.environment_object_palette_tag_block.count)
        print("Environment Object Palette Tag Block Maximum Count: ", LEVEL.level_body.environment_object_palette_tag_block.maximum_count)
        print("Environment Object Palette Tag Block Address: ", LEVEL.level_body.environment_object_palette_tag_block.address)
        print("Environment Object Palette Tag Block Definition: ", LEVEL.level_body.environment_object_palette_tag_block.definition)
        print("Environment Objects Tag Block Count: ", LEVEL.level_body.environment_objects_tag_block.count)
        print("Environment Objects Tag Block Maximum Count: ", LEVEL.level_body.environment_objects_tag_block.maximum_count)
        print("Environment Objects Tag Block Address: ", LEVEL.level_body.environment_objects_tag_block.address)
        print("Environment Objects Tag Block Definition: ", LEVEL.level_body.environment_objects_tag_block.definition)
        print("Lightmaps Tag Block Count: ", LEVEL.level_body.lightmaps_tag_block.count)
        print("Lightmaps Tag Block Maximum Count: ", LEVEL.level_body.lightmaps_tag_block.maximum_count)
        print("Lightmaps Tag Block Address: ", LEVEL.level_body.lightmaps_tag_block.address)
        print("Lightmaps Tag Block Definition: ", LEVEL.level_body.lightmaps_tag_block.definition)
        print("Leaf Map Leaves Tag Block Count: ", LEVEL.level_body.leaf_map_leaves_tag_block.count)
        print("Leaf Map Leaves Tag Block Maximum Count: ", LEVEL.level_body.leaf_map_leaves_tag_block.maximum_count)
        print("Leaf Map Leaves Tag Block Address: ", LEVEL.level_body.leaf_map_leaves_tag_block.address)
        print("Leaf Map Leaves Tag Block Definition: ", LEVEL.level_body.leaf_map_leaves_tag_block.definition)
        print("Leaf Map Connections Tag Block Count: ", LEVEL.level_body.leaf_map_connections_tag_block.count)
        print("Leaf Map Connections Tag Block Maximum Count: ", LEVEL.level_body.leaf_map_connections_tag_block.maximum_count)
        print("Leaf Map Connections Tag Block Address: ", LEVEL.level_body.leaf_map_connections_tag_block.address)
        print("Leaf Map Connections Tag Block Definition: ", LEVEL.level_body.leaf_map_connections_tag_block.definition)
        print("Errors Tag Block Count: ", LEVEL.level_body.errors_tag_block.count)
        print("Errors Tag Block Maximum Count: ", LEVEL.level_body.errors_tag_block.maximum_count)
        print("Errors Tag Block Address: ", LEVEL.level_body.errors_tag_block.address)
        print("Errors Tag Block Definition: ", LEVEL.level_body.errors_tag_block.definition)
        print("Precomputed Lighting Tag Block Count: ", LEVEL.level_body.precomputed_lighting_tag_block.count)
        print("Precomputed Lighting Tag Block Maximum Count: ", LEVEL.level_body.precomputed_lighting_tag_block.maximum_count)
        print("Precomputed Lighting Tag Block Address: ", LEVEL.level_body.precomputed_lighting_tag_block.address)
        print("Precomputed Lighting Tag Block Definition: ", LEVEL.level_body.precomputed_lighting_tag_block.definition)
        print("Instanced Geometries Definition Tag Block Count: ", LEVEL.level_body.instanced_geometries_definition_tag_block.count)
        print("Instanced Geometries Definition Tag Block Maximum Count: ", LEVEL.level_body.instanced_geometries_definition_tag_block.maximum_count)
        print("Instanced Geometries Definition Tag Block Address: ", LEVEL.level_body.instanced_geometries_definition_tag_block.address)
        print("Instanced Geometries Definition Tag Block Definition: ", LEVEL.level_body.instanced_geometries_definition_tag_block.definition)
        print("Instanced Geometries Instances Tag Block Count: ", LEVEL.level_body.instanced_geometry_instances_tag_block.count)
        print("Instanced Geometries Instances Tag Block Maximum Count: ", LEVEL.level_body.instanced_geometry_instances_tag_block.maximum_count)
        print("Instanced Geometries Instances Tag Block Address: ", LEVEL.level_body.instanced_geometry_instances_tag_block.address)
        print("Instanced Geometries Instances Tag Block Definition: ", LEVEL.level_body.instanced_geometry_instances_tag_block.definition)
        print("Ambience Sound Clusters Tag Block Count: ", LEVEL.level_body.ambience_sound_clusters_tag_block.count)
        print("Ambience Sound Clusters Tag Block Maximum Count: ", LEVEL.level_body.ambience_sound_clusters_tag_block.maximum_count)
        print("Ambience Sound Clusters Tag Block Address: ", LEVEL.level_body.ambience_sound_clusters_tag_block.address)
        print("Ambience Sound Clusters Tag Block Definition: ", LEVEL.level_body.ambience_sound_clusters_tag_block.definition)
        print("Reverb Sound Clusters Tag Block Count: ", LEVEL.level_body.reverb_sound_clusters_tag_block.count)
        print("Reverb Sound Clusters Tag Block Maximum Count: ", LEVEL.level_body.reverb_sound_clusters_tag_block.maximum_count)
        print("Reverb Sound Clusters Tag Block Address: ", LEVEL.level_body.reverb_sound_clusters_tag_block.address)
        print("Reverb Sound Clusters Tag Block Definition: ", LEVEL.level_body.reverb_sound_clusters_tag_block.definition)
        print("Transparent Planes Tag Block Count: ", LEVEL.level_body.transparent_planes_tag_block.count)
        print("Transparent Planes Tag Block Maximum Count: ", LEVEL.level_body.transparent_planes_tag_block.maximum_count)
        print("Transparent Planes Tag Block Address: ", LEVEL.level_body.transparent_planes_tag_block.address)
        print("Transparent Planes Tag Block Definition: ", LEVEL.level_body.transparent_planes_tag_block.definition)
        print("Vehicle Spherical Limit Radius: ", LEVEL.level_body.vehicle_spherical_limit_radius)
        print("Vehicle Spherical Limit Center: ", LEVEL.level_body.vehicle_spherical_limit_center)
        print("Debug Info Tag Block Count: ", LEVEL.level_body.debug_info_tag_block.count)
        print("Debug Info Tag Block Maximum Count: ", LEVEL.level_body.debug_info_tag_block.maximum_count)
        print("Debug Info Tag Block Address: ", LEVEL.level_body.debug_info_tag_block.address)
        print("Debug Info Tag Block Definition: ", LEVEL.level_body.debug_info_tag_block.definition)
        print("Decorators Bitmap Tag Reference Group: ", LEVEL.level_body.decorators_bitmaps_tag_ref.tag_group)
        print("Decorators Bitmap Tag Reference Name: ", LEVEL.level_body.decorators_bitmaps_tag_ref.name)
        print("Decorators Bitmap Tag Reference Name Length: ", LEVEL.level_body.decorators_bitmaps_tag_ref.name_length)
        print("Decorators Bitmap Tag Reference Salt: ", LEVEL.level_body.decorators_bitmaps_tag_ref.salt)
        print("Decorators Bitmap Tag Reference Index: ", LEVEL.level_body.decorators_bitmaps_tag_ref.index)
        print("Decorators 0 Data Info Size: ", LEVEL.level_body.decorators_0_raw_data.size)
        print("Decorators 0 Data Info Flags: ", LEVEL.level_body.decorators_0_raw_data.flags)
        print("Decorators 0 Data Info Raw Pointer: ", LEVEL.level_body.decorators_0_raw_data.raw_pointer)
        print("Decorators 0 Data Info Pointer: ", LEVEL.level_body.decorators_0_raw_data.pointer)
        print("Decorators 0 Data Info ID: ", LEVEL.level_body.decorators_0_raw_data.id)
        print("Decorators 0: ", LEVEL.level_body.decorators_0_vector)
        print("Decorators 1: ", LEVEL.level_body.decorators_1_vector)
        print("Decorators 1 Data Info Size: ", LEVEL.level_body.decorators_1_raw_data.size)
        print("Decorators 1 Data Info Flags: ", LEVEL.level_body.decorators_1_raw_data.flags)
        print("Decorators 1 Data Info Raw Pointer: ", LEVEL.level_body.decorators_1_raw_data.raw_pointer)
        print("Decorators 1 Data Info Pointer: ", LEVEL.level_body.decorators_1_raw_data.pointer)
        print("Decorators 1 Data Info ID: ", LEVEL.level_body.decorators_1_raw_data.id)
        print("Breakable Surface Tag Block Count: ", LEVEL.level_body.breakable_surface_tag_block.count)
        print("Breakable Surface Tag Block Maximum Count: ", LEVEL.level_body.breakable_surface_tag_block.maximum_count)
        print("Breakable Surface Tag Block Address: ", LEVEL.level_body.breakable_surface_tag_block.address)
        print("Breakable Surface Tag Block Definition: ", LEVEL.level_body.breakable_surface_tag_block.definition)
        print("Water Definitions Tag Block Count: ", LEVEL.level_body.water_definitions_tag_block.count)
        print("Water Definitions Tag Block Maximum Count: ", LEVEL.level_body.water_definitions_tag_block.maximum_count)
        print("Water Definitions Tag Block Address: ", LEVEL.level_body.water_definitions_tag_block.address)
        print("Water Definitions Tag Block Definition: ", LEVEL.level_body.water_definitions_tag_block.definition)
        print("Portal Device Mapping Tag Block Count: ", LEVEL.level_body.portal_device_mapping_tag_block.count)
        print("Portal Device Mapping Tag Block Maximum Count: ", LEVEL.level_body.portal_device_mapping_tag_block.maximum_count)
        print("Portal Device Mapping Tag Block Address: ", LEVEL.level_body.portal_device_mapping_tag_block.address)
        print("Portal Device Mapping Tag Block Definition: ", LEVEL.level_body.portal_device_mapping_tag_block.definition)
        print("Audibility Tag Block Count: ", LEVEL.level_body.audibility_tag_block.count)
        print("Audibility Tag Block Maximum Count: ", LEVEL.level_body.audibility_tag_block.maximum_count)
        print("Audibility Tag Block Address: ", LEVEL.level_body.audibility_tag_block.address)
        print("Audibility Tag Block Definition: ", LEVEL.level_body.audibility_tag_block.definition)
        print("Object Fake Lightprobes Tag Block Count: ", LEVEL.level_body.object_fake_lightprobes_tag_block.count)
        print("Object Fake Lightprobes Tag Block Maximum Count: ", LEVEL.level_body.object_fake_lightprobes_tag_block.maximum_count)
        print("Object Fake Lightprobes Tag Block Address: ", LEVEL.level_body.object_fake_lightprobes_tag_block.address)
        print("Object Fake Lightprobes Tag Block Definition: ", LEVEL.level_body.object_fake_lightprobes_tag_block.definition)
        print("Decorators Tag Block Count: ", LEVEL.level_body.decorators_tag_block.count)
        print("Decorators Tag Block Maximum Count: ", LEVEL.level_body.decorators_tag_block.maximum_count)
        print("Decorators Tag Block Address: ", LEVEL.level_body.decorators_tag_block.address)
        print("Decorators Tag Block Definition: ", LEVEL.level_body.decorators_tag_block.definition)
        print(" ")

    import_info_count = LEVEL.level_body.import_info_tag_block.count
    if import_info_count > 0:
        import_info_tag_block_header = struct.unpack('<16x', input_stream.read(16))
        for import_info_idx in range(import_info_count):
            import_info_struct = struct.unpack('<i256s32s32s96x32s4xiII128x', input_stream.read(596))
            import_info = LEVEL.ImportInfo()
            import_info.build = import_info_struct[0]
            import_info.version = import_info_struct[1].decode().rstrip('\x00')
            import_info.import_date = import_info_struct[2].decode().rstrip('\x00')
            import_info.culprit = import_info_struct[3].decode().rstrip('\x00')
            import_info.import_time = import_info_struct[4].decode().rstrip('\x00')
            import_info.files_tag_block = TAG.TagBlock(import_info_struct[5], 0, import_info_struct[6], import_info_struct[7])

            LEVEL.import_info_blocks.append(import_info)

        file_tag_block_header = struct.unpack('<16x', input_stream.read(16))
        for import_info in LEVEL.import_info_blocks:
            files = []
            for file_idx in range(import_info.files_tag_block.count):
                file_struct = struct.unpack('<256s32s96xiii144x', input_stream.read(540))
                file = LEVEL.Files()
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
        for import_info_idx, import_info in enumerate(LEVEL.import_info_blocks):
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

    collision_materials_count = LEVEL.level_body.collision_materials_tag_block.count
    if collision_materials_count > 0:
        file_tag_block_header = struct.unpack('<16x', input_stream.read(16))
        for collision_material_idx in range(collision_materials_count):
            collision_material_struct = struct.unpack('<4siiI2xh4siiI', input_stream.read(36))
            collision_material = LEVEL.CollisionMaterial()
            collision_material.old_shader = TAG.TagRef(collision_material_struct[0].decode('utf-8', 'replace').rstrip('\x00'), "", collision_material_struct[2] + 1, collision_material_struct[1], collision_material_struct[3])
            collision_material.conveyor_surface_index = collision_material_struct[4]
            collision_material.new_shader = TAG.TagRef(collision_material_struct[5].decode('utf-8', 'replace').rstrip('\x00'), "", collision_material_struct[7] + 1, collision_material_struct[6], collision_material_struct[8])
            LEVEL.collision_materials.append(collision_material)

        for collision_material in LEVEL.collision_materials:
            if collision_material.old_shader.name_length > 1:
                tag_path = struct.unpack('<%ss' % collision_material.old_shader.name_length, input_stream.read(collision_material.old_shader.name_length))
                collision_material.old_shader.name = tag_path[0].decode().rstrip('\x00')

            if collision_material.new_shader.name_length > 1:
                tag_path = struct.unpack('<%ss' % collision_material.new_shader.name_length, input_stream.read(collision_material.new_shader.name_length))
                collision_material.new_shader.name = tag_path[0].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_COLLISION_MATERIALS:
        print(" ===== Collision Materials ===== ")
        for collision_material_idx, collision_material in enumerate(LEVEL.collision_materials):
            print(" ===== Collision Material %s ===== " % collision_material_idx)
            print("Old Shader Tag Reference Group: ", collision_material.old_shader.tag_group)
            print("Old Shader Tag Reference Name: ", collision_material.old_shader.name)
            print("Old Shader Tag Reference Name Length: ", collision_material.old_shader.name_length)
            print("Old Shader Tag Reference Salt: ", collision_material.old_shader.salt)
            print("Old Shader Tag Reference Index: ", collision_material.old_shader.index)
            print("Conveyor Surface Index: ", collision_material.conveyor_surface_index)
            print("New Shader Tag Reference Group: ", collision_material.new_shader.tag_group)
            print("New Shader Tag Reference Name: ", collision_material.new_shader.name)
            print("New Shader Tag Reference Name Length: ", collision_material.new_shader.name_length)
            print("New Shader Tag Reference Salt: ", collision_material.new_shader.salt)
            print("New Shader Tag Reference Index: ", collision_material.new_shader.index)
            print(" ")

    collision_bsps_count = LEVEL.level_body.collision_bsps_tag_block.count
    if collision_bsps_count > 0:
        collision_bsps_tag_block_header = struct.unpack('<16x', input_stream.read(16))
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

    if DEBUG_PARSER and DEBUG_COLLISION_BSPS:
        for collision_bsp_idx, collision_bsp in enumerate(LEVEL.collision_bsps):
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

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    return LEVEL
