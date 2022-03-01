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
DEBUG_NODES = True
DEBUG_CLUSTER_LEAVES = True
DEBUG_LEAF_SURFACES = True
DEBUG_CLUSTER_SURFACES = True
DEBUG_LIGHTMAPS = True
DEBUG_MATERIALS = True
DEBUG_UNCOMPRESSED_RENDER_VERTICES = True
DEBUG_COMPRESSED_RENDER_VERTICES = True
DEBUG_UNCOMPRESSED_LIGHTMAP_VERTICES = True
DEBUG_COMPRESSED_LIGHTMAP_VERTICES = True
DEBUG_LENS_FLARES = True
DEBUG_LENS_FLARE_MARKERS = True
DEBUG_CLUSTERS = True
DEBUG_PREDICTED_RESOURCES = True
DEBUG_SUBCLUSTERS = True
DEBUG_SUBCLUSTERS_SURFACE_INDICES = True
DEBUG_SURFACE_INDICES = True
DEBUG_MIRRORS = True
DEBUG_MIRROR_VERTICES = True
DEBUG_PORTALS = True
DEBUG_CLUSTER_DATA = True
DEBUG_CLUSTER_PORTALS = True
DEBUG_PORTAL_VERTICES = True
DEBUG_BREAKABLE_SURFACES = True
DEBUG_FOG_PLANES = True
DEBUG_FOG_PLANE_VERTICES = True
DEBUG_FOG_REGIONS = True
DEBUG_FOG_PALETTES = True
DEBUG_WEATHER_PALETTES = True
DEBUG_WEATHER_POLYHEDRA = True
DEBUG_WEATHER_POLYHEDRA_PLANES = True
DEBUG_PATHFINDING_SURFACES = True
DEBUG_PATHFINDING_EDGES = True
DEBUG_BACKGROUND_SOUND_PALETTES = True
DEBUG_SOUND_ENVIRONMENT_PALETTES = True
DEBUG_MARKERS = True
DEBUG_DETAIL_OBJECTS = True
DEBUG_DETAIL_OBJECT_CELLS = True
DEBUG_DETAIL_OBJECT_INSTANCES = True
DEBUG_DETAIL_OBJECT_COUNTS = True
DEBUG_DETAIL_OBJECT_Z_REFERENCE_VECTORS = True
DEBUG_LEAF_MAP_LEAVES = True
DEBUG_LEAF_MAP_LEAF_FACES = True
DEBUG_FACE_VERTICES = True
DEBUG_LEAF_MAP_LEAF_PORTAL_INDICES = True
DEBUG_LEAF_MAP_PORTALS = True
DEBUG_LEAF_MAP_PORTAL_VERTICES = True

def process_file_retail(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    LEVEL = LevelAsset()

    header_struct = struct.unpack('>hbb32s4sIIIIHbb4s', input_stream.read(64))
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

    level_body_struct = struct.unpack('>4siiIff20xfff4xffffffffffff12xffffffffff4xiIIiIIiIIffffffiIIiIIiIIiII12xiIIiIIiIIiiIIIiII12xiIIiIIiIIiII24xiIIiII24xiIIiIIiIIiIIiiIIII20xiIIiIIiII12xiIIiII', input_stream.read(648))
    LEVEL.level_body = LEVEL.LevelBody()
    LEVEL.level_body.lightmap_bitmaps_tag_ref = TAG.TagRef(level_body_struct[0].decode().rstrip('\x00'), "", level_body_struct[2] + 1, level_body_struct[1], level_body_struct[3])
    LEVEL.level_body.vehicle_floor = level_body_struct[4]
    LEVEL.level_body.vehicle_ceiling = level_body_struct[5]
    LEVEL.level_body.default_ambient_color = (level_body_struct[6], level_body_struct[7], level_body_struct[8], 1.0)
    LEVEL.level_body.default_distant_light_0_color = (level_body_struct[9], level_body_struct[10], level_body_struct[11], 1.0)
    LEVEL.level_body.default_distant_light_0_direction = Vector((level_body_struct[12], level_body_struct[13], level_body_struct[14]))
    LEVEL.level_body.default_distant_light_1_color = (level_body_struct[15], level_body_struct[16], level_body_struct[17], 1.0)
    LEVEL.level_body.default_distant_light_1_direction = Vector((level_body_struct[18], level_body_struct[19], level_body_struct[20]))
    LEVEL.level_body.default_reflection_tint = (level_body_struct[21], level_body_struct[22], level_body_struct[23], level_body_struct[24])
    LEVEL.level_body.default_shadow_vector = Vector((level_body_struct[25], level_body_struct[26], level_body_struct[27]))
    LEVEL.level_body.default_shadow_color = (level_body_struct[28], level_body_struct[29], level_body_struct[30], 1.0)
    LEVEL.level_body.collision_materials_tag_block = TAG.TagBlock(level_body_struct[31], 512, level_body_struct[32], level_body_struct[33])
    LEVEL.level_body.collision_bsps_tag_block = TAG.TagBlock(level_body_struct[34], 1, level_body_struct[35], level_body_struct[36])
    LEVEL.level_body.nodes_tag_block = TAG.TagBlock(level_body_struct[37], 131072, level_body_struct[38], level_body_struct[39])
    LEVEL.level_body.world_bounds_x = (level_body_struct[40], level_body_struct[41])
    LEVEL.level_body.world_bounds_y = (level_body_struct[42], level_body_struct[43])
    LEVEL.level_body.world_bounds_z = (level_body_struct[44], level_body_struct[45])
    LEVEL.level_body.leaves_tag_block = TAG.TagBlock(level_body_struct[46], 65535, level_body_struct[47], level_body_struct[48])
    LEVEL.level_body.leaf_surfaces_tag_block = TAG.TagBlock(level_body_struct[49], 262144, level_body_struct[50], level_body_struct[51])
    LEVEL.level_body.surfaces_tag_block = TAG.TagBlock(level_body_struct[52], 131072, level_body_struct[53], level_body_struct[54])
    LEVEL.level_body.lightmaps_tag_block = TAG.TagBlock(level_body_struct[55], 128, level_body_struct[56], level_body_struct[57])
    LEVEL.level_body.lens_flares_tag_block = TAG.TagBlock(level_body_struct[58], 256, level_body_struct[59], level_body_struct[60])
    LEVEL.level_body.lens_flare_markers_tag_block = TAG.TagBlock(level_body_struct[61], 65535, level_body_struct[62], level_body_struct[63])
    LEVEL.level_body.clusters_tag_block = TAG.TagBlock(level_body_struct[64], 8192, level_body_struct[65], level_body_struct[66])
    LEVEL.level_body.cluster_data_raw_data = TAG.RawData(level_body_struct[67], level_body_struct[68], level_body_struct[69], level_body_struct[70], level_body_struct[71])
    LEVEL.level_body.cluster_portals_tag_block = TAG.TagBlock(level_body_struct[72], 512, level_body_struct[73], level_body_struct[74])
    LEVEL.level_body.breakable_surfaces_tag_block = TAG.TagBlock(level_body_struct[75], 256, level_body_struct[76], level_body_struct[77])
    LEVEL.level_body.fog_planes_tag_block = TAG.TagBlock(level_body_struct[78], 32, level_body_struct[79], level_body_struct[80])
    LEVEL.level_body.fog_regions_tag_block = TAG.TagBlock(level_body_struct[81], 32, level_body_struct[82], level_body_struct[83])
    LEVEL.level_body.fog_palettes_tag_block = TAG.TagBlock(level_body_struct[84], 32, level_body_struct[85], level_body_struct[86])
    LEVEL.level_body.weather_palettes_tag_block = TAG.TagBlock(level_body_struct[87], 32, level_body_struct[88], level_body_struct[89])
    LEVEL.level_body.weather_polyhedras_tag_block = TAG.TagBlock(level_body_struct[90], 32, level_body_struct[91], level_body_struct[92])
    LEVEL.level_body.pathfinding_surfaces_tag_block = TAG.TagBlock(level_body_struct[93], 131072, level_body_struct[94], level_body_struct[95])
    LEVEL.level_body.pathfinding_edges_tag_block = TAG.TagBlock(level_body_struct[96], 262144, level_body_struct[97], level_body_struct[98])
    LEVEL.level_body.background_sounds_palette_tag_block = TAG.TagBlock(level_body_struct[99], 64, level_body_struct[100], level_body_struct[101])
    LEVEL.level_body.sound_environments_palette_tag_block = TAG.TagBlock(level_body_struct[102], 64, level_body_struct[103], level_body_struct[104])
    LEVEL.level_body.sound_pas_raw_data = TAG.RawData(level_body_struct[105], level_body_struct[106], level_body_struct[107], level_body_struct[108], level_body_struct[109])
    LEVEL.level_body.unknown_0 = level_body_struct[110]
    LEVEL.level_body.markers_tag_block = TAG.TagBlock(level_body_struct[111], 1024, level_body_struct[112], level_body_struct[113])
    LEVEL.level_body.detail_objects_tag_block = TAG.TagBlock(level_body_struct[114], 1, level_body_struct[115], level_body_struct[116])
    LEVEL.level_body.runtime_decals_tag_block = TAG.TagBlock(level_body_struct[117], 6144, level_body_struct[118], level_body_struct[119])
    LEVEL.level_body.leaf_map_leaves_tag_block = TAG.TagBlock(level_body_struct[120], 65536, level_body_struct[121], level_body_struct[122])
    LEVEL.level_body.leaf_map_portals_tag_block = TAG.TagBlock(level_body_struct[123], 524288, level_body_struct[124], level_body_struct[125])

    if LEVEL.level_body.lightmap_bitmaps_tag_ref.name_length > 1:
        tag_path = struct.unpack('>%ss' % LEVEL.level_body.lightmap_bitmaps_tag_ref.name_length, input_stream.read(LEVEL.level_body.lightmap_bitmaps_tag_ref.name_length))
        LEVEL.level_body.lightmap_bitmaps_tag_ref.name = tag_path[0].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_BODY:
        print(" ===== SBSP Body ===== ")
        print("Lightmap Bitmap Tag Reference Group: ", LEVEL.level_body.lightmap_bitmaps_tag_ref.tag_group)
        print("Lightmap Bitmap Tag Reference Name: ", LEVEL.level_body.lightmap_bitmaps_tag_ref.name)
        print("Lightmap Bitmap Tag Reference Name Length: ", LEVEL.level_body.lightmap_bitmaps_tag_ref.name_length)
        print("Lightmap Bitmap Tag Reference Salt: ", LEVEL.level_body.lightmap_bitmaps_tag_ref.salt)
        print("Lightmap Bitmap Tag Reference Index: ", LEVEL.level_body.lightmap_bitmaps_tag_ref.index)
        print("Vehicle Floor: ", LEVEL.level_body.vehicle_floor)
        print("Vehicle Ceiling: ", LEVEL.level_body.vehicle_ceiling)
        print("Default Ambient Color: ", LEVEL.level_body.default_ambient_color)
        print("Default Distant Light 0 Color: ", LEVEL.level_body.default_distant_light_0_color)
        print("Default Distant Light 0 Direction: ", LEVEL.level_body.default_distant_light_0_direction)
        print("Default Distant Light 1 Color: ", LEVEL.level_body.default_distant_light_1_color)
        print("Default Distant Light 1 Direction: ", LEVEL.level_body.default_distant_light_1_direction)
        print("Default Reflection Tint: ", LEVEL.level_body.default_reflection_tint)
        print("Default Shadow Vector: ", LEVEL.level_body.default_shadow_vector)
        print("Default Shadow Color: ", LEVEL.level_body.default_shadow_color)
        print("Collision Materials Tag Block Count: ", LEVEL.level_body.collision_materials_tag_block.count)
        print("Collision Materials Tag Block Maximum Count: ", LEVEL.level_body.collision_materials_tag_block.maximum_count)
        print("Collision Materials Tag Block Address: ", LEVEL.level_body.collision_materials_tag_block.address)
        print("Collision Materials Tag Block Definition: ", LEVEL.level_body.collision_materials_tag_block.definition)
        print("Collision BSP Tag Block Count: ", LEVEL.level_body.collision_bsps_tag_block.count)
        print("Collision BSP Tag Block Maximum Count: ", LEVEL.level_body.collision_bsps_tag_block.maximum_count)
        print("Collision BSP Tag Block Address: ", LEVEL.level_body.collision_bsps_tag_block.address)
        print("Collision BSP Tag Block Definition: ", LEVEL.level_body.collision_bsps_tag_block.definition)
        print("Nodes Tag Block Count: ", LEVEL.level_body.nodes_tag_block.count)
        print("Nodes Tag Block Maximum Count: ", LEVEL.level_body.nodes_tag_block.maximum_count)
        print("Nodes Tag Block Address: ", LEVEL.level_body.nodes_tag_block.address)
        print("Nodes Tag Block Definition: ", LEVEL.level_body.nodes_tag_block.definition)
        print("World Bounds X: ", LEVEL.level_body.world_bounds_x)
        print("World Bounds Y: ", LEVEL.level_body.world_bounds_y)
        print("World Bounds Z: ", LEVEL.level_body.world_bounds_z)
        print("Leaves Tag Block Count: ", LEVEL.level_body.leaves_tag_block.count)
        print("Leaves Tag Block Maximum Count: ", LEVEL.level_body.leaves_tag_block.maximum_count)
        print("Leaves Tag Block Address: ", LEVEL.level_body.leaves_tag_block.address)
        print("Leaves Tag Block Definition: ", LEVEL.level_body.leaves_tag_block.definition)
        print("Leaves Tag Block Count: ", LEVEL.level_body.leaves_tag_block.count)
        print("Leaves Tag Block Maximum Count: ", LEVEL.level_body.leaves_tag_block.maximum_count)
        print("Leaves Tag Block Address: ", LEVEL.level_body.leaves_tag_block.address)
        print("Leaves Tag Block Definition: ", LEVEL.level_body.leaves_tag_block.definition)
        print("Leaf Surfaces Tag Block Count: ", LEVEL.level_body.leaf_surfaces_tag_block.count)
        print("Leaf Surfaces Tag Block Maximum Count: ", LEVEL.level_body.leaf_surfaces_tag_block.maximum_count)
        print("Leaf Surfaces Tag Block Address: ", LEVEL.level_body.leaf_surfaces_tag_block.address)
        print("Leaf Surfaces Tag Block Definition: ", LEVEL.level_body.leaf_surfaces_tag_block.definition)
        print("Surfaces Tag Block Count: ", LEVEL.level_body.surfaces_tag_block.count)
        print("Surfaces Tag Block Maximum Count: ", LEVEL.level_body.surfaces_tag_block.maximum_count)
        print("Surfaces Tag Block Address: ", LEVEL.level_body.surfaces_tag_block.address)
        print("Surfaces Tag Block Definition: ", LEVEL.level_body.surfaces_tag_block.definition)
        print("Lightmaps Tag Block Count: ", LEVEL.level_body.lightmaps_tag_block.count)
        print("Lightmaps Tag Block Maximum Count: ", LEVEL.level_body.lightmaps_tag_block.maximum_count)
        print("Lightmaps Tag Block Address: ", LEVEL.level_body.lightmaps_tag_block.address)
        print("Lightmaps Tag Block Definition: ", LEVEL.level_body.lightmaps_tag_block.definition)
        print("Lens Flares Tag Block Count: ", LEVEL.level_body.lens_flares_tag_block.count)
        print("Lens Flares Tag Block Maximum Count: ", LEVEL.level_body.lens_flares_tag_block.maximum_count)
        print("Lens Flares Tag Block Address: ", LEVEL.level_body.lens_flares_tag_block.address)
        print("Lens Flares Tag Block Definition: ", LEVEL.level_body.lens_flares_tag_block.definition)
        print("Lens Flare Markers Tag Block Count: ", LEVEL.level_body.lens_flare_markers_tag_block.count)
        print("Lens Flare Markers Tag Block Maximum Count: ", LEVEL.level_body.lens_flare_markers_tag_block.maximum_count)
        print("Lens Flare Markers Tag Block Address: ", LEVEL.level_body.lens_flare_markers_tag_block.address)
        print("Lens Flare Markers Tag Block Definition: ", LEVEL.level_body.lens_flare_markers_tag_block.definition)
        print("Clusters Tag Block Count: ", LEVEL.level_body.clusters_tag_block.count)
        print("Clusters Tag Block Maximum Count: ", LEVEL.level_body.clusters_tag_block.maximum_count)
        print("Clusters Tag Block Address: ", LEVEL.level_body.clusters_tag_block.address)
        print("Clusters Tag Block Definition: ", LEVEL.level_body.clusters_tag_block.definition)
        print("Cluster Data Info Size: ", LEVEL.level_body.cluster_data_raw_data.size)
        print("Cluster Data Info Flags: ", LEVEL.level_body.cluster_data_raw_data.flags)
        print("Cluster Data Info Raw Pointer: ", LEVEL.level_body.cluster_data_raw_data.raw_pointer)
        print("Cluster Data Info Pointer: ", LEVEL.level_body.cluster_data_raw_data.pointer)
        print("Cluster Data Info ID: ", LEVEL.level_body.cluster_data_raw_data.id)
        print("Cluster Portals Tag Block Count: ", LEVEL.level_body.cluster_portals_tag_block.count)
        print("Cluster Portals Tag Block Maximum Count: ", LEVEL.level_body.cluster_portals_tag_block.maximum_count)
        print("Cluster Portals Tag Block Address: ", LEVEL.level_body.cluster_portals_tag_block.address)
        print("Cluster Portals Tag Block Definition: ", LEVEL.level_body.cluster_portals_tag_block.definition)
        print("Breakable Surfaces Tag Block Count: ", LEVEL.level_body.breakable_surfaces_tag_block.count)
        print("Breakable Surfaces Tag Block Maximum Count: ", LEVEL.level_body.breakable_surfaces_tag_block.maximum_count)
        print("Breakable Surfaces Tag Block Address: ", LEVEL.level_body.breakable_surfaces_tag_block.address)
        print("Breakable Surfaces Tag Block Definition: ", LEVEL.level_body.breakable_surfaces_tag_block.definition)
        print("Fog Planes Tag Block Count: ", LEVEL.level_body.fog_planes_tag_block.count)
        print("Fog Planes Tag Block Maximum Count: ", LEVEL.level_body.fog_planes_tag_block.maximum_count)
        print("Fog Planes Tag Block Address: ", LEVEL.level_body.fog_planes_tag_block.address)
        print("Fog Planes Tag Block Definition: ", LEVEL.level_body.fog_planes_tag_block.definition)
        print("Fog Regions Tag Block Count: ", LEVEL.level_body.fog_regions_tag_block.count)
        print("Fog Regions Tag Block Maximum Count: ", LEVEL.level_body.fog_regions_tag_block.maximum_count)
        print("Fog Regions Tag Block Address: ", LEVEL.level_body.fog_regions_tag_block.address)
        print("Fog Regions Tag Block Definition: ", LEVEL.level_body.fog_regions_tag_block.definition)
        print("Fog Palettes Tag Block Count: ", LEVEL.level_body.fog_palettes_tag_block.count)
        print("Fog Palettes Tag Block Maximum Count: ", LEVEL.level_body.fog_palettes_tag_block.maximum_count)
        print("Fog Palettes Tag Block Address: ", LEVEL.level_body.fog_palettes_tag_block.address)
        print("Fog Palettes Tag Block Definition: ", LEVEL.level_body.fog_palettes_tag_block.definition)
        print("Weather Palette Tag Block Count: ", LEVEL.level_body.weather_palettes_tag_block.count)
        print("Weather Palette Tag Block Maximum Count: ", LEVEL.level_body.weather_palettes_tag_block.maximum_count)
        print("Weather Palette Tag Block Address: ", LEVEL.level_body.weather_palettes_tag_block.address)
        print("Weather Palette Tag Block Definition: ", LEVEL.level_body.weather_palettes_tag_block.definition)
        print("Weather Polyhedras Tag Block Count: ", LEVEL.level_body.weather_polyhedras_tag_block.count)
        print("Weather Polyhedras Tag Block Maximum Count: ", LEVEL.level_body.weather_polyhedras_tag_block.maximum_count)
        print("Weather Polyhedras Tag Block Address: ", LEVEL.level_body.weather_polyhedras_tag_block.address)
        print("Weather Polyhedras Tag Block Definition: ", LEVEL.level_body.weather_polyhedras_tag_block.definition)
        print("Pathfinding Surfaces Tag Block Count: ", LEVEL.level_body.pathfinding_surfaces_tag_block.count)
        print("Pathfinding Surfaces Tag Block Maximum Count: ", LEVEL.level_body.pathfinding_surfaces_tag_block.maximum_count)
        print("Pathfinding Surfaces Tag Block Address: ", LEVEL.level_body.pathfinding_surfaces_tag_block.address)
        print("Pathfinding Surfaces Tag Block Definition: ", LEVEL.level_body.pathfinding_surfaces_tag_block.definition)
        print("Pathfinding Edges Tag Block Count: ", LEVEL.level_body.pathfinding_edges_tag_block.count)
        print("Pathfinding Edges Tag Block Maximum Count: ", LEVEL.level_body.pathfinding_edges_tag_block.maximum_count)
        print("Pathfinding Edges Tag Block Address: ", LEVEL.level_body.pathfinding_edges_tag_block.address)
        print("Pathfinding Edges Tag Block Definition: ", LEVEL.level_body.pathfinding_edges_tag_block.definition)
        print("Background Sounds Palette Tag Block Count: ", LEVEL.level_body.background_sounds_palette_tag_block.count)
        print("Background Sounds Palette Tag Block Maximum Count: ", LEVEL.level_body.background_sounds_palette_tag_block.maximum_count)
        print("Background Sounds Palette Tag Block Address: ", LEVEL.level_body.background_sounds_palette_tag_block.address)
        print("Background Sounds Palette Tag Block Definition: ", LEVEL.level_body.background_sounds_palette_tag_block.definition)
        print("Sound Environments Palette Tag Block Count: ", LEVEL.level_body.sound_environments_palette_tag_block.count)
        print("Sound Environments Palette Tag Block Maximum Count: ", LEVEL.level_body.sound_environments_palette_tag_block.maximum_count)
        print("Sound Environments Palette Tag Block Address: ", LEVEL.level_body.sound_environments_palette_tag_block.address)
        print("Sound Environments Palette Tag Block Definition: ", LEVEL.level_body.sound_environments_palette_tag_block.definition)
        print("Sound PAS Data Size: ", LEVEL.level_body.sound_pas_raw_data.size)
        print("Sound PAS Data Flags: ", LEVEL.level_body.sound_pas_raw_data.flags)
        print("Sound PAS Data Raw Pointer: ", LEVEL.level_body.sound_pas_raw_data.raw_pointer)
        print("Sound PAS Data Pointer: ", LEVEL.level_body.sound_pas_raw_data.pointer)
        print("Sound PAS Data ID: ", LEVEL.level_body.sound_pas_raw_data.id)
        print("Unknown Value: ", LEVEL.level_body.unknown_0)
        print("Markers Tag Block Count: ", LEVEL.level_body.markers_tag_block.count)
        print("Markers Tag Block Maximum Count: ", LEVEL.level_body.markers_tag_block.maximum_count)
        print("Markers Tag Block Address: ", LEVEL.level_body.markers_tag_block.address)
        print("Markers Tag Block Definition: ", LEVEL.level_body.markers_tag_block.definition)
        print("Detail Objects Tag Block Count: ", LEVEL.level_body.detail_objects_tag_block.count)
        print("Detail Objects Tag Block Maximum Count: ", LEVEL.level_body.detail_objects_tag_block.maximum_count)
        print("Detail Objects Tag Block Address: ", LEVEL.level_body.detail_objects_tag_block.address)
        print("Detail Objects Tag Block Definition: ", LEVEL.level_body.detail_objects_tag_block.definition)
        print("Runtime Decals Tag Block Count: ", LEVEL.level_body.runtime_decals_tag_block.count)
        print("Runtime Decals Tag Block Maximum Count: ", LEVEL.level_body.runtime_decals_tag_block.maximum_count)
        print("Runtime Decals Tag Block Address: ", LEVEL.level_body.runtime_decals_tag_block.address)
        print("Runtime Decals Tag Block Definition: ", LEVEL.level_body.runtime_decals_tag_block.definition)
        print("Leaf Map Leaves Tag Block Count: ", LEVEL.level_body.leaf_map_leaves_tag_block.count)
        print("Leaf Map Leaves Tag Block Maximum Count: ", LEVEL.level_body.leaf_map_leaves_tag_block.maximum_count)
        print("Leaf Map Leaves Tag Block Address: ", LEVEL.level_body.leaf_map_leaves_tag_block.address)
        print("Leaf Map Leaves Tag Block Definition: ", LEVEL.level_body.leaf_map_leaves_tag_block.definition)
        print("Leaf Map Portals Tag Block Count: ", LEVEL.level_body.leaf_map_portals_tag_block.count)
        print("Leaf Map Portals Tag Block Maximum Count: ", LEVEL.level_body.leaf_map_portals_tag_block.maximum_count)
        print("Leaf Map Portals Tag Block Address: ", LEVEL.level_body.leaf_map_portals_tag_block.address)
        print("Leaf Map Portals Tag Block Definition: ", LEVEL.level_body.leaf_map_portals_tag_block.definition)
        print(" ")

    for collision_material_idx in range(LEVEL.level_body.collision_materials_tag_block.count):
        collision_material_struct = struct.unpack('>4siiII', input_stream.read(20))
        collision_material = LEVEL.CollisionMaterial()
        collision_material.shader_tag_ref = TAG.TagRef(collision_material_struct[0].decode().rstrip('\x00'), "", collision_material_struct[2] + 1, collision_material_struct[1], collision_material_struct[3])
        collision_material.unknown_0 = collision_material_struct[1]

        LEVEL.collision_materials.append(collision_material)

    for collision_material in LEVEL.collision_materials:
        if collision_material.shader_tag_ref.name_length > 1:
            tag_path = struct.unpack('>%ss' % collision_material.shader_tag_ref.name_length, input_stream.read(collision_material.shader_tag_ref.name_length))
            collision_material.shader_tag_ref.name = tag_path[0].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_COLLISION_MATERIALS:
        print(" ===== Collision Materials ===== ")
        for collision_material_idx, collision_material in enumerate(LEVEL.collision_materials):
            print(" ===== Collision Material %s ===== " % collision_material_idx)
            print("Collision Material Tag Reference Group: ",collision_material.shader_tag_ref.tag_group)
            print("Collision Material Tag Reference Name: ", collision_material.shader_tag_ref.name)
            print("Collision Material Tag Reference Name Length: ", collision_material.shader_tag_ref.name_length)
            print("Collision Material Tag Reference Salt: ", collision_material.shader_tag_ref.salt)
            print("Collision Material Tag Reference Index: ", collision_material.shader_tag_ref.index)
            print("Unknown Value: ", collision_material.unknown_0)
            print(" ")

    for collision_bsp_idx in range(LEVEL.level_body.collision_bsps_tag_block.count):
        collision_bsp_struct = struct.unpack('>iIIiIIiIIiIIiIIiIIiIIiII', input_stream.read(96))
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
        for bsp3d_node_idx in range(collision_bsp.bsp3d_nodes_tag_block.count):
            bsp_3d_node_struct = struct.unpack('>iii', input_stream.read(12))
            bsp_3d_node = LEVEL.BSP3DNode()
            bsp_3d_node.plane = bsp_3d_node_struct[0]
            bsp_3d_node.back_child = bsp_3d_node_struct[1]
            bsp_3d_node.front_child = bsp_3d_node_struct[2]

            bsp_3d_nodes.append(bsp_3d_node)

        for plane_idx in range(collision_bsp.planes_tag_block.count):
            plane_struct = struct.unpack('>ffff', input_stream.read(16))
            plane = LEVEL.Plane()
            plane.translation = Vector((plane_struct[0], plane_struct[1], plane_struct[2])) * 100
            plane.distance = plane_struct[3] * 100

            planes.append(plane)

        for leaf_idx in range(collision_bsp.leaves_tag_block.count):
            leaf_struct = struct.unpack('>hhi', input_stream.read(8))
            leaf = LEVEL.Leaf()
            leaf.flags = leaf_struct[0]
            leaf.bsp2d_reference_count = leaf_struct[1]
            leaf.first_bsp2d_reference = leaf_struct[2]

            leaves.append(leaf)

        for bsp2d_reference_idx in range(collision_bsp.bsp2d_references_tag_block.count):
            bsp2d_reference_struct = struct.unpack('>ii', input_stream.read(8))
            bsp2d_reference = LEVEL.BSP2DReference()
            bsp2d_reference.plane = bsp2d_reference_struct[0]
            bsp2d_reference.bsp2d_node = bsp2d_reference_struct[1]

            bsp2d_references.append(bsp2d_reference)

        for bsp2d_nodes_idx in range(collision_bsp.bsp2d_nodes_tag_block.count):
            bsp2d_node_struct = struct.unpack('>fffii', input_stream.read(20))
            bsp2d_node = LEVEL.BSP2DNode()
            bsp2d_node.plane_i = bsp2d_node_struct[0]
            bsp2d_node.plane_j = bsp2d_node_struct[1]
            bsp2d_node.distance = bsp2d_node_struct[2] * 100
            bsp2d_node.left_child = bsp2d_node_struct[3]
            bsp2d_node.right_child = bsp2d_node_struct[4]

            bsp2d_nodes.append(bsp2d_node)

        for surfaces_idx in range(collision_bsp.surfaces_tag_block.count):
            surfaces_struct = struct.unpack('>iibbh', input_stream.read(12))
            surface = LEVEL.Surface()
            surface.plane = surfaces_struct[0]
            surface.first_edge = surfaces_struct[1]
            surface.flags = surfaces_struct[2]
            surface.breakable_surface = surfaces_struct[3]
            surface.material = surfaces_struct[4]

            surfaces.append(surface)

        for edge_idx in range(collision_bsp.edges_tag_block.count):
            edge_struct = struct.unpack('>iiiiii', input_stream.read(24))
            edge = LEVEL.Edge()
            edge.start_vertex = edge_struct[0]
            edge.end_vertex = edge_struct[1]
            edge.forward_edge = edge_struct[2]
            edge.reverse_edge = edge_struct[3]
            edge.left_surface = edge_struct[4]
            edge.right_surface = edge_struct[5]

            edges.append(edge)

        for vertex_idx in range(collision_bsp.vertices_tag_block.count):
            vertex_struct = struct.unpack('>fffi', input_stream.read(16))
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

    for node_idx in range(LEVEL.level_body.nodes_tag_block.count):
        node_struct = struct.unpack('>bbbbbb', input_stream.read(6))
        node = LEVEL.Nodes()
        node.unknown_0 = node_struct[0]
        node.unknown_1 = node_struct[1]
        node.unknown_2 = node_struct[2]
        node.unknown_3 = node_struct[3]
        node.unknown_4 = node_struct[4]
        node.unknown_5 = node_struct[5]

        LEVEL.nodes.append(node)

    if DEBUG_PARSER and DEBUG_NODES:
        print(" ===== Nodes ===== ")
        for node_idx, node in enumerate(LEVEL.nodes):
            print(" ===== Node %s ===== " % node_idx)
            print("Unknown Value: ", node.unknown_0)
            print("Unknown Value: ", node.unknown_1)
            print("Unknown Value: ", node.unknown_2)
            print("Unknown Value: ", node.unknown_3)
            print("Unknown Value: ", node.unknown_4)
            print("Unknown Value: ", node.unknown_5)
            print(" ")

    for cluster_leaf_idx in range(LEVEL.level_body.leaves_tag_block.count):
        cluster_leaf_struct = struct.unpack('>hhhhhhi', input_stream.read(16))
        cluster_leaf = LEVEL.ClusterLeaf()
        cluster_leaf.unknown_0 = cluster_leaf_struct[0]
        cluster_leaf.unknown_1 = cluster_leaf_struct[1]
        cluster_leaf.unknown_2 = cluster_leaf_struct[2]
        cluster_leaf.unknown_3 = cluster_leaf_struct[3]
        cluster_leaf.cluster = cluster_leaf_struct[4]
        cluster_leaf.surface_reference_count = cluster_leaf_struct[5]
        cluster_leaf.surface_reference = cluster_leaf_struct[6]

        LEVEL.leaves.append(cluster_leaf)

    if DEBUG_PARSER and DEBUG_CLUSTER_LEAVES:
        print(" ===== Leaves ===== ")
        for leaf_idx, leaf in enumerate(LEVEL.leaves):
            print(" ===== Leaf %s ===== " % leaf_idx)
            print("Unknown Value: ", leaf.unknown_0)
            print("Unknown Value: ", leaf.unknown_1)
            print("Unknown Value: ", leaf.unknown_2)
            print("Unknown Value: ", leaf.unknown_3)
            print("Cluster: ", leaf.cluster)
            print("Reference Count: ", leaf.surface_reference_count)
            print("Surface Reference: ", leaf.surface_reference)
            print(" ")

    for leaf_surface_idx in range(LEVEL.level_body.leaf_surfaces_tag_block.count):
        leaf_surface_struct = struct.unpack('>ii', input_stream.read(8))
        leaf_surface = LEVEL.LeafSurface()
        leaf_surface.surface = leaf_surface_struct[0]
        leaf_surface.node = leaf_surface_struct[1]

        LEVEL.leaf_surfaces.append(leaf_surface)

    if DEBUG_PARSER and DEBUG_LEAF_SURFACES:
        print(" ===== Leaf Surfaces ===== ")
        for leaf_surface_idx, leaf_surface in enumerate(LEVEL.leaf_surfaces):
            print(" ===== Leaf Surface %s ===== " % leaf_surface_idx)
            print("Surface: ", leaf_surface.surface)
            print("Node: ", leaf_surface.node)
            print(" ")

    for surface_idx in range(LEVEL.level_body.surfaces_tag_block.count):
        surface_struct = struct.unpack('>hhh', input_stream.read(6))
        surface = LEVEL.ClusterSurface()
        surface.v0 = surface_struct[0]
        surface.v1 = surface_struct[1]
        surface.v2 = surface_struct[2]

        LEVEL.surfaces.append(surface)

    if DEBUG_PARSER and DEBUG_CLUSTER_SURFACES:
        print(" ===== Surfaces ===== ")
        for surface_idx, surface in enumerate(LEVEL.surfaces):
            print(" ===== Surface %s ===== " % surface_idx)
            print("Surface Point 0: ", surface.v0)
            print("Surface Point 1: ", surface.v1)
            print("Surface Point 2: ", surface.v2)
            print(" ")

    for lightmap_idx in range(LEVEL.level_body.lightmaps_tag_block.count):
        lightmap_struct = struct.unpack('>h18xiII', input_stream.read(32))
        lightmap = LEVEL.Lightmaps()
        lightmap.bitmap_index = lightmap_struct[0]
        lightmap.materials_tag_block = TAG.TagBlock(lightmap_struct[1], 2048, lightmap_struct[2], lightmap_struct[3])

        LEVEL.lightmaps.append(lightmap)

    for lightmap in LEVEL.lightmaps:
        materials = []
        for material_idx in range(lightmap.materials_tag_block.count):
            material_struct = struct.unpack('>4siiIhhiiffffffh2xffffffffffff12xffffffffffffffh6xiiIIH2xiiIIiiIIIiiIII', input_stream.read(256))
            material = LEVEL.Material()
            material.shader_tag_ref = TAG.TagRef(material_struct[0].decode().rstrip('\x00'), "", material_struct[2] + 1, material_struct[1], material_struct[3])
            material.shader_permutation = material_struct[4]
            material.flags = material_struct[5]
            material.surfaces = material_struct[6]
            material.surface_count = material_struct[7]
            material.centroid = Vector((material_struct[8], material_struct[9], material_struct[10]))
            material.ambient_color = (material_struct[11], material_struct[12], material_struct[13], 1.0)
            material.distant_light_count = material_struct[14]
            material.distant_light_0_color = (material_struct[15], material_struct[16], material_struct[17], 1.0)
            material.distant_light_0_direction = Vector((material_struct[18], material_struct[19], material_struct[20]))
            material.distant_light_1_color = (material_struct[21], material_struct[22], material_struct[23], 1.0)
            material.distant_light_1_direction = Vector((material_struct[24], material_struct[25], material_struct[26]))
            material.reflection_tint = (material_struct[27], material_struct[28], material_struct[29], material_struct[30])
            material.shadow_vector = Vector((material_struct[31], material_struct[32], material_struct[33]))
            material.shadow_color = (material_struct[34], material_struct[35], material_struct[36], 1.0)
            material.plane_translation = Vector((material_struct[37], material_struct[38], material_struct[39]))
            material.plane_distance = material_struct[40]
            material.breakable_surface = material_struct[41]
            material.vertices_count = material_struct[42]
            material.vertices_offset = material_struct[43]
            material.unknown_cache_offset0 = material_struct[44]
            material.vertices_cache_offset = material_struct[45]
            material.vertex_type = material_struct[46]
            material.lightmap_vertices_count = material_struct[47]
            material.lightmap_vertices_offset = material_struct[48]
            material.unknown_cache_offset1 = material_struct[49]
            material.lightmap_vertices_cache_offset = material_struct[50]
            material.uncompressed_vertices_raw_data = TAG.RawData(material_struct[51], material_struct[52], material_struct[53], material_struct[54], material_struct[55])
            material.compressed_vertices_raw_data = TAG.RawData(material_struct[56], material_struct[57], material_struct[58], material_struct[59], material_struct[60])

            materials.append(material)

        for material in materials:
            uncompressed_render_vertices = []
            uncompressed_lightmap_vertices = []
            compressed_render_vertices = []
            compressed_lightmap_vertices = []
            if material.shader_tag_ref.name_length > 1:
                tag_path = struct.unpack('>%ss' % material.shader_tag_ref.name_length, input_stream.read(material.shader_tag_ref.name_length))
                material.shader_tag_ref.name = tag_path[0].decode().rstrip('\x00')

            for uncompressed_render_vertex_idx in range(material.vertices_count):
                uncompressed_render_vertex = LEVEL.Vertices()
                uncompressed_render_vertex_struct = struct.unpack('<ffffffffffffff', input_stream.read(56))
                uncompressed_render_vertex.translation = Vector((uncompressed_render_vertex_struct[0], uncompressed_render_vertex_struct[1], uncompressed_render_vertex_struct[2])) * 100
                uncompressed_render_vertex.normal = Vector((uncompressed_render_vertex_struct[3], uncompressed_render_vertex_struct[4], uncompressed_render_vertex_struct[5]))
                uncompressed_render_vertex.binormal = Vector((uncompressed_render_vertex_struct[6], uncompressed_render_vertex_struct[7], uncompressed_render_vertex_struct[8]))
                uncompressed_render_vertex.tangent = Vector((uncompressed_render_vertex_struct[9], uncompressed_render_vertex_struct[10], uncompressed_render_vertex_struct[11]))
                uncompressed_render_vertex.UV = (uncompressed_render_vertex_struct[12], uncompressed_render_vertex_struct[13])

                uncompressed_render_vertices.append(uncompressed_render_vertex)

            for uncompressed_lightmap_vertex_idx in range(material.lightmap_vertices_count):
                uncompressed_lightmap_vertex = LEVEL.Vertices()
                uncompressed_lightmap_vertex_struct = struct.unpack('<fffff', input_stream.read(20))
                uncompressed_lightmap_vertex.normal = Vector((uncompressed_lightmap_vertex_struct[0], uncompressed_lightmap_vertex_struct[1], uncompressed_lightmap_vertex_struct[2]))
                uncompressed_lightmap_vertex.UV = (uncompressed_lightmap_vertex_struct[3], uncompressed_lightmap_vertex_struct[4])

                uncompressed_lightmap_vertices.append(uncompressed_lightmap_vertex)

            for compressed_render_vertex_idx in range(material.vertices_count):
                compressed_render_vertex = LEVEL.Vertices()
                compressed_render_vertex_struct = struct.unpack('<fffIIIff', input_stream.read(32))
                compressed_render_vertex.translation = Vector((compressed_render_vertex_struct[0], compressed_render_vertex_struct[1], compressed_render_vertex_struct[2])) * 100
                compressed_render_vertex.normal = compressed_render_vertex_struct[3]
                compressed_render_vertex.binormal = compressed_render_vertex_struct[4]
                compressed_render_vertex.tangent = compressed_render_vertex_struct[5]
                compressed_render_vertex.UV = (compressed_render_vertex_struct[6], compressed_render_vertex_struct[7])

                compressed_render_vertices.append(compressed_render_vertex)

            for compressed_lightmap_vertex_idx in range(material.lightmap_vertices_count):
                compressed_lightmap_vertex = LEVEL.Vertices()
                compressed_lightmap_vertex_struct = struct.unpack('<Ihh', input_stream.read(8))
                compressed_lightmap_vertex.normal = compressed_lightmap_vertex_struct[0]
                compressed_lightmap_vertex.UV = (compressed_lightmap_vertex_struct[1], compressed_lightmap_vertex_struct[2])

                compressed_lightmap_vertices.append(compressed_lightmap_vertex)

            material.uncompressed_render_vertices = uncompressed_render_vertices
            material.uncompressed_lightmap_vertices = uncompressed_lightmap_vertices
            material.compressed_render_vertices = compressed_render_vertices
            material.compressed_lightmap_vertices = compressed_lightmap_vertices

        lightmap.materials = materials

    if DEBUG_PARSER and DEBUG_LIGHTMAPS:
        for lightmap_idx, lightmap in enumerate(LEVEL.lightmaps):
            print(" ===== Lightmap %s ===== " % lightmap_idx)
            print("Bitmap Index: ", lightmap.bitmap_index)
            print("Materials Tag Block Count: ", lightmap.materials_tag_block.count)
            print("Materials Tag Block Maximum Count: ", lightmap.materials_tag_block.maximum_count)
            print("Materials Tag Block Address: ", lightmap.materials_tag_block.address)
            print("Materials Tag Block Definition: ", lightmap.materials_tag_block.definition)
            print(" ")
            if DEBUG_MATERIALS:
                for material_idx, material in enumerate(lightmap.materials):
                    print(" ===== Material %s ===== " % material_idx)
                    print("Shader Bitmap Tag Reference Group: ", material.shader_tag_ref.tag_group)
                    print("Shader Bitmap Tag Reference Name: ", material.shader_tag_ref.name)
                    print("Shader Bitmap Tag Reference Name Length: ", material.shader_tag_ref.name_length)
                    print("Shader Bitmap Tag Reference Salt: ", material.shader_tag_ref.salt)
                    print("Shader Bitmap Tag Reference Index: ", material.shader_tag_ref.index)
                    print("Shader Permutation: ", material.shader_permutation)
                    print("Flags: ", material.flags)
                    print("Surfaces: ", material.surfaces)
                    print("Surface Count: ", material.surface_count)
                    print("Centroid: ", material.centroid)
                    print("Ambient Color: ", material.ambient_color)
                    print("Distant Light Count: ", material.distant_light_count)
                    print("Distant Light 0 Color: ", material.distant_light_0_color)
                    print("Default Light 0 Direction: ", material.distant_light_0_direction)
                    print("Distant Light 1 Color: ", material.distant_light_1_color)
                    print("Default Light 1 Direction: ", material.distant_light_1_direction)
                    print("Reflection Tint: ", material.reflection_tint)
                    print("Shadow Vector: ", material.shadow_vector)
                    print("Shadow Color: ", material.shadow_color)
                    print("Plane Translation: ", material.plane_translation)
                    print("Plane Distance: ", material.plane_distance)
                    print("Breakable Surfaces: ", material.breakable_surface)
                    print("Vertex Count: ", material.vertices_count)
                    print("Vertex Offset: ", material.vertices_offset)
                    print("Unknown Cache Offset 0: ", material.unknown_cache_offset0)
                    print("Vertices Cache Offset: ", material.vertices_cache_offset)
                    print("Vertex Type: ", material.vertex_type)
                    print("Lightmap Vertices Count: ", material.lightmap_vertices_count)
                    print("Lightmap Vertices Offset: ", material.lightmap_vertices_offset)
                    print("Unknown Cache Offset 1: ", material.unknown_cache_offset1)
                    print("Lightmap Vertices Cache Offset: ", material.lightmap_vertices_cache_offset)
                    print("Uncompressed Vertices Size: ", material.uncompressed_vertices_raw_data.size)
                    print("Uncompressed Vertices Flags: ", material.uncompressed_vertices_raw_data.flags)
                    print("Uncompressed Vertices Raw Pointer: ", material.uncompressed_vertices_raw_data.raw_pointer)
                    print("Uncompressed Vertices Pointer: ", material.uncompressed_vertices_raw_data.pointer)
                    print("Uncompressed Vertices ID: ", material.uncompressed_vertices_raw_data.id)
                    print("Compressed Vertices Size: ", material.compressed_vertices_raw_data.size)
                    print("Compressed Vertices Flags: ", material.compressed_vertices_raw_data.flags)
                    print("Compressed Vertices Raw Pointer: ", material.compressed_vertices_raw_data.raw_pointer)
                    print("Compressed Vertices Pointer: ", material.compressed_vertices_raw_data.pointer)
                    print("Compressed Vertices ID: ", material.compressed_vertices_raw_data.id)
                    print(" ")
                    if DEBUG_UNCOMPRESSED_RENDER_VERTICES:
                        for uncompressed_render_vertex_idx, uncompressed_render_vertex in enumerate(material.uncompressed_render_vertices):
                            print(" ===== Uncompressed Vertices %s ===== " % uncompressed_render_vertex_idx)
                            print("Uncompressed Render Translation: ", uncompressed_render_vertex.translation)
                            print("Uncompressed Render Normal: ", uncompressed_render_vertex.normal)
                            print("Uncompressed Render Binormal: ", uncompressed_render_vertex.binormal)
                            print("Uncompressed Render Tangent: ", uncompressed_render_vertex.tangent)
                            print("Uncompressed Render UV: ", uncompressed_render_vertex.UV)
                            print(" ")

                    if DEBUG_COMPRESSED_RENDER_VERTICES:
                        for compressed_render_vertex_idx, compressed_render_vertex in enumerate(material.compressed_render_vertices):
                            print(" ===== Compressed Vertices %s ===== " % compressed_render_vertex_idx)
                            print("Compressed Render Translation: ", compressed_render_vertex.translation)
                            print("Compressed Render Normal: ", compressed_render_vertex.normal)
                            print("Compressed Render Binormal: ", compressed_render_vertex.binormal)
                            print("Compressed Render Tangent: ", compressed_render_vertex.tangent)
                            print("Compressed Render UV: ", compressed_render_vertex.UV)
                            print(" ")

                    if DEBUG_UNCOMPRESSED_LIGHTMAP_VERTICES:
                        for uncompressed_lightmap_vertex_idx, uncompressed_lightmap_vertex in enumerate(material.uncompressed_lightmap_vertices):
                            print(" ===== Uncompressed Lightmap Vertices %s ===== " % uncompressed_lightmap_vertex_idx)
                            print("Uncompressed Lightmap Normal: ", uncompressed_lightmap_vertex.normal)
                            print("Uncompressed Lightmap UV: ", uncompressed_lightmap_vertex.UV)
                            print(" ")

                    if DEBUG_COMPRESSED_LIGHTMAP_VERTICES:
                        for compressed_lightmap_vertex_idx, compressed_lightmap_vertex in enumerate(material.compressed_lightmap_vertices):
                            print(" ===== Compressed Lightmap Vertices %s ===== " % compressed_lightmap_vertex_idx)
                            print("Compressed Lightmap Normal: ", compressed_lightmap_vertex.normal)
                            print("Compressed Lightmap UV: ", compressed_lightmap_vertex.UV)
                            print(" ")

    for lens_flare_idx in range(LEVEL.level_body.lens_flares_tag_block.count):
        collision_material_struct = struct.unpack('>4siiI', input_stream.read(16))
        lens_flare_tag_ref = TAG.TagRef(collision_material_struct[0].decode().rstrip('\x00'), "", collision_material_struct[2] + 1, collision_material_struct[1], collision_material_struct[3])

        LEVEL.lens_flares.append(lens_flare_tag_ref)

    for lens_flare in LEVEL.lens_flares:
        if lens_flare.name_length > 1:
            tag_path = struct.unpack('>%ss' % lens_flare.name_length, input_stream.read(lens_flare.name_length))
            lens_flare.name = tag_path[0].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_LENS_FLARES:
        print(" ===== Lens Flares ===== ")
        for lens_flare_idx, lens_flare in enumerate(LEVEL.lens_flares):
            print(" ===== Lens Flare %s ===== " % lens_flare_idx)
            print("Lens Flare Tag Reference Group: ", lens_flare.tag_group)
            print("Lens Flare Tag Reference Name: ", lens_flare.name)
            print("Lens Flare Tag Reference Name Length: ", lens_flare.name_length)
            print("Lens Flare Tag Reference Salt: ", lens_flare.salt)
            print("Lens Flare Tag Reference Index: ", lens_flare.index)
            print(" ")

    for lens_flare_marker_idx in range(LEVEL.level_body.lens_flare_markers_tag_block.count):
        lens_flare_marker_struct = struct.unpack('>fffbbbb', input_stream.read(16))
        lens_flare_marker = LEVEL.LensFlareMarker()
        lens_flare_marker.position = Vector((lens_flare_marker_struct[0], lens_flare_marker_struct[1], lens_flare_marker_struct[2]))
        lens_flare_marker.direction_i_compenent = lens_flare_marker_struct[3]
        lens_flare_marker.direction_j_compenent = lens_flare_marker_struct[4]
        lens_flare_marker.direction_k_compenent = lens_flare_marker_struct[5]
        lens_flare_marker.lens_flare_index = lens_flare_marker_struct[6]

        LEVEL.lens_flare_markers.append(lens_flare_marker)

    if DEBUG_PARSER and DEBUG_LENS_FLARE_MARKERS:
        print(" ===== Lens Flare Markers ===== ")
        for lens_flare_marker_idx, lens_flare_marker in enumerate(LEVEL.lens_flare_markers):
            print(" ===== Lens Flare Marker %s ===== " % lens_flare_marker_idx)
            print("Lens Flare Marker Position: ", lens_flare_marker.position)
            print("Lens Flare Marker Direction i Compenent: ", lens_flare_marker.direction_i_compenent)
            print("Lens Flare Marker Direction j Compenent: ", lens_flare_marker.direction_j_compenent)
            print("Lens Flare Marker Direction k Compenent: ", lens_flare_marker.direction_k_compenent)
            print("Lens Flare Index: ", lens_flare_marker.lens_flare_index)
            print(" ")

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
            mirror.shader_tag_ref = TAG.TagRef(mirror_struct[4].decode().rstrip('\x00'), "", mirror_struct[6] + 1, mirror_struct[5], mirror_struct[7])
            mirror.vertices_tag_block = TAG.TagBlock(mirror_struct[8], 512, mirror_struct[9], mirror_struct[10])

            mirrors.append(mirror)

        for mirror in mirrors:
            mirror_vertices = []
            if mirror.shader_tag_ref.name_length > 1:
                tag_path = struct.unpack('>%ss' % mirror.shader_tag_ref.name_length, input_stream.read(mirror.shader_tag_ref.name_length))
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

    if DEBUG_PARSER and DEBUG_CLUSTERS:
        print(" ===== Clusters ===== ")
        for cluster_idx, cluster in enumerate(LEVEL.clusters):
            print(" ===== Cluster %s ===== " % cluster_idx)
            print("Cluster Sky: ", cluster.sky)
            print("Cluster Fog: ", cluster.fog)
            print("Cluster Background Sound: ", cluster.background_sound)
            print("Cluster Sound Environment: ", cluster.sound_environment)
            print("Cluster Weather: ", cluster.weather)
            print("Cluster Transition Structure BSP: ", cluster.transition_structure_bsp)
            print("Cluster First Decal Index: ", cluster.first_decal_index)
            print("Cluster Decal Count: ", cluster.decal_count)
            print("Cluster Predicted Resources Tag Block Count: ", cluster.predicted_resources_tag_block.count)
            print("Cluster Predicted Resources Tag Block Maximum Count: ", cluster.predicted_resources_tag_block.maximum_count)
            print("Cluster Predicted Resources Tag Block Address: ", cluster.predicted_resources_tag_block.address)
            print("Cluster Predicted Resources Tag Block Definition: ", cluster.predicted_resources_tag_block.definition)
            print("Cluster Subclusters Tag Block Count: ", cluster.subclusters_tag_block.count)
            print("Cluster Subclusters Tag Block Maximum Count: ", cluster.subclusters_tag_block.maximum_count)
            print("Cluster Subclusters Tag Block Address: ", cluster.subclusters_tag_block.address)
            print("Cluster Subclusters Tag Block Definition: ", cluster.subclusters_tag_block.definition)
            print("Cluster First Lens Flare Marker Index: ", cluster.first_lens_flare_marker_index)
            print("Cluster Lens Flare Marker Count: ", cluster.lens_flare_marker_count)
            print("Cluster Surface Indices Tag Block Count: ", cluster.surface_indices_tag_block.count)
            print("Cluster Surface Indices Tag Block Maximum Count: ", cluster.surface_indices_tag_block.maximum_count)
            print("Cluster Surface Indices Tag Block Address: ", cluster.surface_indices_tag_block.address)
            print("Cluster Surface Indices Tag Block Definition: ", cluster.surface_indices_tag_block.definition)
            print("Cluster Mirrors Tag Block Count: ", cluster.mirrors_tag_block.count)
            print("Cluster Mirrors Tag Block Maximum Count: ", cluster.mirrors_tag_block.maximum_count)
            print("Cluster Mirrors Tag Block Address: ", cluster.mirrors_tag_block.address)
            print("Cluster Mirrors Tag Block Definition: ", cluster.mirrors_tag_block.definition)
            print("Cluster Portals Tag Block Count: ", cluster.portals_tag_block.count)
            print("Cluster Portals Tag Block Maximum Count: ", cluster.portals_tag_block.maximum_count)
            print("Cluster Portals Tag Block Address: ", cluster.portals_tag_block.address)
            print("Cluster Portals Tag Block Definition: ", cluster.portals_tag_block.definition)
            print(" ")
            if DEBUG_PREDICTED_RESOURCES:
                for predicted_resource_idx, predicted_resource in enumerate(cluster.predicted_resources):
                    print(" ===== Predicted Resource %s ===== " % predicted_resource_idx)
                    print("Predicted Resource Type: ", predicted_resource.type)
                    print("Predicted Resource Index: ", predicted_resource.resource_index)
                    print("Predicted Resource Tag Index: ", predicted_resource.tag_index)
                    print(" ")

            if DEBUG_SUBCLUSTERS:
                for subcluster_idx, subcluster in enumerate(cluster.subclusters):
                    print(" ===== Subcluster %s ===== " % subcluster_idx)
                    print("Subcluster World Bounds X: ", subcluster.world_bounds_x)
                    print("Subcluster World Bounds Y: ", subcluster.world_bounds_y)
                    print("Subcluster World Bounds Z: ", subcluster.world_bounds_z)
                    print("Surface Indices Tag Block Count: ", subcluster.surface_indices_tag_block.count)
                    print("Surface Indices Tag Block Maximum Count: ", subcluster.surface_indices_tag_block.maximum_count)
                    print("Surface Indices Tag Block Address: ", subcluster.surface_indices_tag_block.address)
                    print("Surface Indices Tag Block Definition: ", subcluster.surface_indices_tag_block.definition)
                    print(" ")

                    if DEBUG_SUBCLUSTERS_SURFACE_INDICES:
                        for surface_index_idx, surface_index in enumerate(subcluster.surface_indices):
                            print(" ===== Surface Index %s ===== " % surface_index_idx)
                            print("Surface Index: ", surface_index)
                            print(" ")

            if DEBUG_SURFACE_INDICES:
                for surface_index_idx, surface_index in enumerate(cluster.surface_indices):
                    print(" ===== Surface Index %s ===== " % surface_index_idx)
                    print("Surface Index: ", surface_index)
                    print(" ")

            if DEBUG_MIRRORS:
                for mirror_idx, mirror in enumerate(cluster.mirrors):
                    print(" ===== Mirror Index %s ===== " % mirror_idx)
                    print("Mirror Plane Translation: ", mirror.plane_translation)
                    print("Mirror Plane Distance: ", mirror.plane_distance)
                    print("Mirror Shader Tag Reference Group: ", mirror.shader_tag_ref.tag_group)
                    print("Mirror Shader Tag Reference Name: ", mirror.shader_tag_ref.name)
                    print("Mirror Shader Tag Reference Name Length: ", mirror.shader_tag_ref.name_length)
                    print("Mirror Shader Tag Reference Salt: ", mirror.shader_tag_ref.salt)
                    print("Mirror Shader Tag Reference Index: ", mirror.shader_tag_ref.index)
                    print("Mirror Vertices Tag Block Count: ", mirror.vertices_tag_block.count)
                    print("Mirror Vertices Tag Block Maximum Count: ", mirror.vertices_tag_block.maximum_count)
                    print("Mirror Vertices Tag Block Address: ", mirror.vertices_tag_block.address)
                    print("Mirror Vertices Tag Block Definition: ", mirror.vertices_tag_block.definition)
                    print(" ")

                    if DEBUG_MIRROR_VERTICES:
                        for vertex_idx, vertex in enumerate(mirror.vertices):
                            print(" ===== Vertex Index %s ===== " % vertex_idx)
                            print("Vertex Translation: ", vertex.translation)
                            print(" ")

            if DEBUG_PORTALS:
                for portal_idx, portal in enumerate(cluster.portals):
                    print(" ===== Portal Index %s ===== " % portal_idx)
                    print("Portal Index: ", portal)
                    print(" ")

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
            data_set =+ 4

            LEVEL.cluster_data.append(cluster_data)

    if DEBUG_PARSER and DEBUG_CLUSTER_DATA:
        print(" ===== Cluster Data ===== ")
        for cluster_data_idx, cluster_data in enumerate(LEVEL.cluster_data):
            print(" ===== Cluster Data %s ===== " % cluster_data_idx)
            print("Cluster Data Unknown Value: ", cluster_data.unknown_0)
            print("Cluster Data Unknown Value: ", cluster_data.unknown_1)
            print("Cluster Data Unknown Value: ", cluster_data.unknown_2)
            print("Cluster Data Unknown Value: ", cluster_data.unknown_3)
            print(" ")

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
            vertex.translation = Vector((vertex_struct[0], vertex_struct[1], vertex_struct[2]))

            vertices.append(vertex)

        cluster_portal.vertices = vertices

    if DEBUG_PARSER and DEBUG_CLUSTER_PORTALS:
        print(" ===== Cluster Portals ===== ")
        for cluster_portal_idx, cluster_portal in enumerate(LEVEL.cluster_portals):
            print(" ===== Cluster Portal %s ===== " % cluster_portal_idx)
            print("Cluster Portal Front Cluster: ", cluster_portal.front_cluster)
            print("Cluster Portal Back Cluster: ", cluster_portal.back_cluster)
            print("Cluster Portal Plane Index: ", cluster_portal.plane_index)
            print("Cluster Portal Centroid: ", cluster_portal.centroid)
            print("Cluster Portal Bounding Radius: ", cluster_portal.bounding_radius)
            print("Cluster Portal Flags: ", cluster_portal.flags)
            print("Vertices Tag Block Count: ", cluster_portal.vertices_tag_block.count)
            print("Vertices Tag Block Maximum Count: ", cluster_portal.vertices_tag_block.maximum_count)
            print("Vertices Tag Block Address: ", cluster_portal.vertices_tag_block.address)
            print("Vertices Tag Block Definition: ", cluster_portal.vertices_tag_block.definition)
            print(" ")
            if DEBUG_PORTAL_VERTICES:
                for vertex_idx, vertex in enumerate(cluster_portal.vertices):
                    print(" ===== Vertex Index %s ===== " % vertex_idx)
                    print("Vertex Translation: ", vertex.translation)
                    print(" ")

    for breakable_surface_idx in range(LEVEL.level_body.breakable_surfaces_tag_block.count):
        breakable_surface_struct = struct.unpack('>ffffi28x', input_stream.read(48))
        breakable_surface = LEVEL.BreakableSurfaces()
        breakable_surface.centroid = Vector((breakable_surface_struct[0], breakable_surface_struct[1], breakable_surface_struct[2]))
        breakable_surface.radius = breakable_surface_struct[3]
        breakable_surface.collision_surface_index = breakable_surface_struct[4]

        LEVEL.breakable_surfaces.append(breakable_surface)

    if DEBUG_PARSER and DEBUG_BREAKABLE_SURFACES:
        print(" ===== Breakable Surfaces ===== ")
        for breakable_surface_idx, breakable_surface in enumerate(LEVEL.breakable_surfaces):
            print(" ===== Breakable Surface %s ===== " % breakable_surface_idx)
            print("Breakable Surface Centroid: ", breakable_surface.centroid)
            print("Breakable Surface Radius: ", breakable_surface.radius)
            print("Breakable Surface Collision Surface Index: ", breakable_surface.collision_surface_index)
            print(" ")

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
            vertex.translation = Vector((vertex_struct[0], vertex_struct[1], vertex_struct[2]))

            vertices.append(vertex)

        fog_plane.vertices = vertices

    if DEBUG_PARSER and DEBUG_FOG_PLANES:
        print(" ===== Fog Planes ===== ")
        for fog_plane_idx, fog_plane in enumerate(LEVEL.fog_planes):
            print(" ===== Fog Plane %s ===== " % fog_plane_idx)
            print("Fog Plane Front Region: ", fog_plane.front_region)
            print("Fog Plane Material Type: ", fog_plane.material_type)
            print("Fog Plane Translation: ", fog_plane.plane_translation)
            print("Fog Plane Distance: ", fog_plane.plane_distance)
            print("Vertices Tag Block Count: ", fog_plane.vertices_tag_block.count)
            print("Vertices Tag Block Maximum Count: ", fog_plane.vertices_tag_block.maximum_count)
            print("Vertices Tag Block Address: ", fog_plane.vertices_tag_block.address)
            print("Vertices Tag Block Definition: ", fog_plane.vertices_tag_block.definition)
            print(" ")
            if DEBUG_FOG_PLANE_VERTICES:
                for vertex_idx, vertex in enumerate(fog_plane.vertices):
                    print(" ===== Vertex Index %s ===== " % vertex_idx)
                    print("Vertex Translation: ", vertex.translation)
                    print(" ")

    for fog_region_idx in range(LEVEL.level_body.fog_regions_tag_block.count):
        fog_region_struct = struct.unpack('>36xhh', input_stream.read(40))
        fog_region = LEVEL.FogRegion()
        fog_region.fog_palette = fog_region_struct[0]
        fog_region.weather_palette = fog_region_struct[1]

        LEVEL.fog_regions.append(fog_region)

    if DEBUG_PARSER and DEBUG_FOG_REGIONS:
        print(" ===== Fog Regions ===== ")
        for fog_region_idx, fog_region in enumerate(LEVEL.fog_regions):
            print(" ===== Fog Region %s ===== " % fog_region_idx)
            print("Fog Region Fog Palette: ", fog_region.fog_palette)
            print("Fog Region Weather Palette: ", fog_region.weather_palette)
            print(" ")

    for fog_palette_idx in range(LEVEL.level_body.fog_palettes_tag_block.count):
        fog_palette_struct = struct.unpack('>32s4siiI4x32s52x', input_stream.read(136))
        fog_palette = LEVEL.FogPalette()
        fog_palette.name = fog_palette_struct[0].decode().rstrip('\x00')
        fog_palette.fog_tag_ref = TAG.TagRef(fog_palette_struct[1].decode().rstrip('\x00'), "", fog_palette_struct[3] + 1, fog_palette_struct[2], fog_palette_struct[4])
        fog_palette.fog_scale_function = fog_palette_struct[5].decode().rstrip('\x00')

        LEVEL.fog_palettes.append(fog_palette)

    for fog_palette in LEVEL.fog_palettes:
        if fog_palette.fog_tag_ref.name_length > 1:
            tag_path = struct.unpack('>%ss' % fog_palette.fog_tag_ref.name_length, input_stream.read(fog_palette.fog_tag_ref.name_length))
            fog_palette.fog_tag_ref.name = tag_path[0].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_FOG_PALETTES:
        print(" ===== Fog Palettes ===== ")
        for fog_palette_idx, fog_palette in enumerate(LEVEL.fog_palettes):
            print(" ===== Fog Palette %s ===== " % fog_palette_idx)
            print("Fog Palette Name: ", fog_palette.name)
            print("Fog Palette Tag Reference Group: ", fog_palette.fog_tag_ref.tag_group)
            print("Fog Palette Tag Reference Name: ", fog_palette.fog_tag_ref.name)
            print("Fog Palette Tag Reference Name Length: ", fog_palette.fog_tag_ref.name_length)
            print("Fog Palette Tag Reference Salt: ", fog_palette.fog_tag_ref.salt)
            print("Fog Palette Tag Reference Index: ", fog_palette.fog_tag_ref.index)
            print("Fog Scale Function: ", fog_palette.fog_scale_function)
            print(" ")

    for weather_palette_idx in range(LEVEL.level_body.weather_palettes_tag_block.count):
        weather_palette_struct = struct.unpack('>32s4siiI4x32s44x4siiIffff4x32s44x', input_stream.read(240))
        weather_palette = LEVEL.WeatherPalette()
        weather_palette.name = weather_palette_struct[0].decode().rstrip('\x00')
        weather_palette.particle_system_tag_ref = TAG.TagRef(weather_palette_struct[1].decode().rstrip('\x00'), "", weather_palette_struct[3] + 1, weather_palette_struct[2], weather_palette_struct[4])
        weather_palette.particle_system_scale_function = weather_palette_struct[5].decode().rstrip('\x00')
        weather_palette.wind_tag_ref = TAG.TagRef(weather_palette_struct[6].decode().rstrip('\x00'), "", weather_palette_struct[8] + 1, weather_palette_struct[7], weather_palette_struct[9])
        weather_palette.wind_direction = Vector((weather_palette_struct[10], weather_palette_struct[11], weather_palette_struct[12]))
        weather_palette.wind_magnitude = weather_palette_struct[13]
        weather_palette.wind_scale_function = weather_palette_struct[14].decode().rstrip('\x00')

        LEVEL.weather_palettes.append(weather_palette)

    for weather_palette in LEVEL.weather_palettes:
        if weather_palette.particle_system_tag_ref.name_length > 1:
            tag_path = struct.unpack('>%ss' % weather_palette.particle_system_tag_ref.name_length, input_stream.read(weather_palette.particle_system_tag_ref.name_length))
            weather_palette.particle_system_tag_ref.name = tag_path[0].decode().rstrip('\x00')

        if weather_palette.wind_tag_ref.name_length > 1:
            tag_path = struct.unpack('>%ss' % weather_palette.wind_tag_ref.name_length, input_stream.read(weather_palette.wind_tag_ref.name_length))
            weather_palette.wind_tag_ref.name = tag_path[0].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_WEATHER_PALETTES:
        print(" ===== Weather Palettes ===== ")
        for weather_palette_idx, weather_palette in enumerate(LEVEL.weather_palettes):
            print(" ===== Weather Palette %s ===== " % weather_palette_idx)
            print("Weather Palette Name: ", weather_palette.name)
            print("Weather Palette Particle System Tag Reference Group: ", weather_palette.particle_system_tag_ref.tag_group)
            print("Weather Palette Particle System Tag Reference Name: ", weather_palette.particle_system_tag_ref.name)
            print("Weather Palette Particle System Tag Reference Name Length: ", weather_palette.particle_system_tag_ref.name_length)
            print("Weather Palette Particle System Tag Reference Salt: ", weather_palette.particle_system_tag_ref.salt)
            print("Weather Palette Particle System Tag Reference Index: ", weather_palette.particle_system_tag_ref.index)
            print("Weather Partocle System Scale Function: ", weather_palette.particle_system_scale_function)
            print("Weather Palette Wind Tag Reference Group: ", weather_palette.wind_tag_ref.tag_group)
            print("Weather Palette Wind Tag Reference Name: ", weather_palette.wind_tag_ref.name)
            print("Weather Palette Wind Tag Reference Name Length: ", weather_palette.wind_tag_ref.name_length)
            print("Weather Palette Wind Tag Reference Salt: ", weather_palette.wind_tag_ref.salt)
            print("Weather Palette Wind Tag Reference Index: ", weather_palette.wind_tag_ref.index)
            print("Weather Palette Wind Direction: ", weather_palette.wind_direction)
            print("Weather Palette Wind Magnitude: ", weather_palette.wind_magnitude)
            print("Weather Palette Wind Scale Function: ", weather_palette.wind_scale_function)
            print(" ")

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
            plane = TAG.Plane()
            plane_struct = struct.unpack('>ffff', input_stream.read(16))
            plane.translation = Vector((plane_struct[0], plane_struct[1], plane_struct[2]))
            plane.distance = plane_struct[3]

            planes.append(plane)

        weather_polyhedra.planes = planes

    if DEBUG_PARSER and DEBUG_WEATHER_POLYHEDRA:
        print(" ===== Weather Polyhedras ===== ")
        for weather_polyhedra_idx, weather_polyhedra in enumerate(LEVEL.weather_polyhedras):
            print(" ===== Weather Polyhedra %s ===== " % weather_polyhedra_idx)
            print("Bounding Sphere Center: ", weather_polyhedra.bounding_sphere_center)
            print("Bounding Sphere Radius: ", weather_polyhedra.bounding_sphere_radius)
            print("Planes Tag Block Count: ", weather_polyhedra.planes_tag_block.count)
            print("Planes Tag Block Maximum Count: ", weather_polyhedra.planes_tag_block.maximum_count)
            print("Planes Tag Block Address: ", weather_polyhedra.planes_tag_block.address)
            print("Planes Tag Block Definition: ", weather_polyhedra.planes_tag_block.definition)
            print(" ")
            if DEBUG_WEATHER_POLYHEDRA_PLANES:
                for plane_idx, plane in enumerate(weather_polyhedra.planes):
                    print(" ===== Plane %s ===== " % plane_idx)
                    print("Plane Translation: ", plane.translation)
                    print("Plane Distance: ", plane.distance)
                    print(" ")

    for pathfinding_surface_idx in range(LEVEL.level_body.pathfinding_surfaces_tag_block.count):
        pathfinding_surface_struct = struct.unpack('>B', input_stream.read(1))

        LEVEL.pathfinding_surfaces.append(pathfinding_surface_struct[0])

    if DEBUG_PARSER and DEBUG_PATHFINDING_SURFACES:
        print(" ===== Pathfinding Surfaces ===== ")
        for pathfinding_surface_idx, pathfinding_surface in enumerate(LEVEL.pathfinding_surfaces):
            print(" ===== Pathfinding Surface %s ===== " % pathfinding_surface_idx)
            print("Pathfinding Surface: ", pathfinding_surface)
            print(" ")

    for pathfinding_edge_idx in range(LEVEL.level_body.pathfinding_edges_tag_block.count):
        pathfinding_edge_struct = struct.unpack('>B', input_stream.read(1))

        LEVEL.pathfinding_edges.append(pathfinding_edge_struct[0])

    if DEBUG_PARSER and DEBUG_PATHFINDING_EDGES:
        print(" ===== Pathfinding Edges ===== ")
        for pathfinding_edge_idx, pathfinding_edge in enumerate(LEVEL.pathfinding_edges):
            print(" ===== Pathfinding Edge %s ===== " % pathfinding_edge_idx)
            print("Pathfinding Edge: ", pathfinding_edge)
            print(" ")

    for background_sounds_palette_idx in range(LEVEL.level_body.background_sounds_palette_tag_block.count):
        background_sounds_palette_struct = struct.unpack('>32s4siiI4x32s32x', input_stream.read(116))
        background_sounds_palette = LEVEL.BackgroundSoundsPalette()
        background_sounds_palette.name = background_sounds_palette_struct[0].decode().rstrip('\x00')
        background_sounds_palette.background_sound_tag_ref = TAG.TagRef(background_sounds_palette_struct[1].decode().rstrip('\x00'), "", background_sounds_palette_struct[3] + 1, background_sounds_palette_struct[2], background_sounds_palette_struct[4])
        background_sounds_palette.scale_function = background_sounds_palette_struct[5].decode().rstrip('\x00')

        LEVEL.background_sounds_palettes.append(background_sounds_palette)

    for background_sounds_palette in LEVEL.background_sounds_palettes:
        if background_sounds_palette.background_sound_tag_ref.name_length > 1:
            tag_path = struct.unpack('>%ss' % background_sounds_palette.background_sound_tag_ref.name_length, input_stream.read(background_sounds_palette.background_sound_tag_ref.name_length))
            background_sounds_palette.background_sound_tag_ref.name = tag_path[0].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_BACKGROUND_SOUND_PALETTES:
        print(" ===== Background Sounds Palettes ===== ")
        for background_sounds_palette_idx, background_sounds_palette in enumerate(LEVEL.background_sounds_palettes):
            print(" ===== Background Sounds Palette %s ===== " % background_sounds_palette_idx)
            print("Background Sounds Palette Name: ", background_sounds_palette.name)
            print("Background Sounds Palette Tag Reference Group: ", background_sounds_palette.background_sound_tag_ref.tag_group)
            print("Background Sounds Palette Tag Reference Name: ", background_sounds_palette.background_sound_tag_ref.name)
            print("Background Sounds Palette Tag Reference Name Length: ", background_sounds_palette.background_sound_tag_ref.name_length)
            print("Background Sounds Palette Tag Reference Salt: ", background_sounds_palette.background_sound_tag_ref.salt)
            print("Background Sounds Palette Tag Reference Index: ", background_sounds_palette.background_sound_tag_ref.index)
            print("Background Sounds Palette Scale Function: ", background_sounds_palette.scale_function)
            print(" ")

    for sound_environments_palette_idx in range(LEVEL.level_body.sound_environments_palette_tag_block.count):
        sound_environments_palette_struct = struct.unpack('>32s4siiI32x', input_stream.read(80))
        sound_environments_palette = LEVEL.SoundEnvironmentsPalette()
        sound_environments_palette.name = sound_environments_palette_struct[0].decode().rstrip('\x00')
        sound_environments_palette.sound_environment_tag_ref = TAG.TagRef(sound_environments_palette_struct[1].decode().rstrip('\x00'), "", sound_environments_palette_struct[3] + 1, sound_environments_palette_struct[2], sound_environments_palette_struct[4])

        LEVEL.sound_environments_palettes.append(sound_environments_palette)

    for sound_environments_palette in LEVEL.sound_environments_palettes:
        if sound_environments_palette.sound_environment_tag_ref.name_length > 1:
            tag_path = struct.unpack('>%ss' % sound_environments_palette.sound_environment_tag_ref.name_length, input_stream.read(sound_environments_palette.sound_environment_tag_ref.name_length))
            sound_environments_palette.sound_environment_tag_ref.name = tag_path[0].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_SOUND_ENVIRONMENT_PALETTES:
        print(" ===== Sound Environment Palettes ===== ")
        for sound_environment_palette_idx, sound_environment_palette in enumerate(LEVEL.sound_environments_palettes):
            print(" ===== Sound Environment Palette %s ===== " % sound_environment_palette_idx)
            print("Sound Environment Palette Name: ", sound_environment_palette.name)
            print("Sound Environment Palette Tag Reference Group: ", sound_environment_palette.sound_environment_tag_ref.tag_group)
            print("Sound Environment Palette Tag Reference Name: ", sound_environment_palette.sound_environment_tag_ref.name)
            print("Sound Environment Palette Tag Reference Name Length: ", sound_environment_palette.sound_environment_tag_ref.name_length)
            print("Sound Environment Palette Tag Reference Salt: ", sound_environment_palette.sound_environment_tag_ref.salt)
            print("Sound Environment Palette Tag Reference Index: ", sound_environment_palette.sound_environment_tag_ref.index)
            print(" ")

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

    if DEBUG_PARSER and DEBUG_MARKERS:
        for marker_idx, marker in enumerate(LEVEL.markers):
            print(" ===== Marker %s ===== " % marker_idx)
            print("Marker Name: ", marker.name)
            print("Marker Rotation: ", marker.rotation)
            print("Marker Translation: ", marker.translation)
            print(" ")

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

    if DEBUG_PARSER and DEBUG_DETAIL_OBJECTS:
        for detail_object_idx, detail_object in enumerate(LEVEL.detail_objects):
            print(" ===== Detail Object %s ===== " % detail_object_idx)
            print("Detail Object Cells Tag Block Count: ", detail_object.cells_tag_block.count)
            print("Detail Object Cells Tag Block Maximum Count: ", detail_object.cells_tag_block.maximum_count)
            print("Detail Object Cells Tag Block Address: ", detail_object.cells_tag_block.address)
            print("Detail Object Cells Tag Block Definition: ", detail_object.cells_tag_block.definition)
            print("Detail Object Instances Tag Block Count: ", detail_object.instances_tag_block.count)
            print("Detail Object Instances Tag Block Maximum Count: ", detail_object.instances_tag_block.maximum_count)
            print("Detail Object Instances Tag Block Address: ", detail_object.instances_tag_block.address)
            print("Detail Object Instances Tag Block Definition: ", detail_object.instances_tag_block.definition)
            print("Detail Object Counts Tag Block Count: ", detail_object.counts_tag_block.count)
            print("Detail Object Counts Tag Block Maximum Count: ", detail_object.counts_tag_block.maximum_count)
            print("Detail Object Counts Tag Block Address: ", detail_object.counts_tag_block.address)
            print("Detail Object Counts Tag Block Definition: ", detail_object.counts_tag_block.definition)
            print("Detail Object Z Reference Vectors Tag Block Count: ", detail_object.z_reference_vectors_tag_block.count)
            print("Detail Object Z Reference Vectors Tag Block Maximum Count: ", detail_object.z_reference_vectors_tag_block.maximum_count)
            print("Detail Object Z Reference Vectors Tag Block Address: ", detail_object.z_reference_vectors_tag_block.address)
            print("Detail Object Z Reference Vectors Tag Block Definition: ", detail_object.z_reference_vectors_tag_block.definition)
            print("Detail Object Flags: ", detail_object.flags)
            print(" ")
            if DEBUG_DETAIL_OBJECT_CELLS:
                for cell_idx, cell in enumerate(detail_object.cells):
                    print(" ===== Cell %s ===== " % cell_idx)
                    print("Cell Translation: ", cell.cell_translation)
                    print("Cell Offset Z: ", cell.offset_z)
                    print("Cell Valid Layers Flag: ", cell.valid_layers_flag)
                    print("Start Index: ", cell.start_index)
                    print("Count Index: ", cell.count_index)
                    print(" ")

            if DEBUG_DETAIL_OBJECT_INSTANCES:
                for instance_idx, instance in enumerate(detail_object.instances):
                    print(" ===== Instance %s ===== " % instance_idx)
                    print("Instance Position: ", instance.position)
                    print("Instance Data: ", instance.data)
                    print("Instance Color: ", instance.color)
                    print(" ")

            if DEBUG_DETAIL_OBJECT_COUNTS:
                for count_idx, count in enumerate(detail_object.counts):
                    print(" ===== Count %s ===== " % count_idx)
                    print("Count: ", count)
                    print(" ")

            if DEBUG_DETAIL_OBJECT_Z_REFERENCE_VECTORS:
                for z_reference_vector_idx, z_reference_vector in enumerate(detail_object.z_reference_vectors):
                    print(" ===== Z Reference Vector %s ===== " % z_reference_vector_idx)
                    print("Z Reference Vector Unknown Value: ", z_reference_vector.unknown_0)
                    print("Z Reference Vector Unknown Value: ", z_reference_vector.unknown_1)
                    print(" ")

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

    if DEBUG_PARSER and DEBUG_LEAF_MAP_LEAVES:
        for leaf_map_leaf_idx, leaf_map_leaf in enumerate(LEVEL.leaf_map_leaves):
            print(" ===== Leaf Map Leaf %s ===== " % leaf_map_leaf_idx)
            print("Faces Tag Block Count: ", leaf_map_leaf.faces_tag_block.count)
            print("Faces Tag Block Maximum Count: ", leaf_map_leaf.faces_tag_block.maximum_count)
            print("Faces Tag Block Address: ", leaf_map_leaf.faces_tag_block.address)
            print("Faces Tag Block Definition: ", leaf_map_leaf.faces_tag_block.definition)
            print("Portal Indices Tag Block Count: ", leaf_map_leaf.portal_indices_tag_block.count)
            print("Portal Indices Tag Block Maximum Count: ", leaf_map_leaf.portal_indices_tag_block.maximum_count)
            print("Portal Indices Tag Block Address: ", leaf_map_leaf.portal_indices_tag_block.address)
            print("Portal Indices Tag Block Definition: ", leaf_map_leaf.portal_indices_tag_block.definition)
            print(" ")
            if DEBUG_LEAF_MAP_LEAF_FACES:
                for face_idx, face in enumerate(leaf_map_leaf.faces):
                    print(" ===== Face %s ===== " % face_idx)
                    print("Face Index: ", face.node_index)
                    print("Vertices Tag Block Count: ", face.vertices_tag_block.count)
                    print("Vertices Tag Block Maximum Count: ", face.vertices_tag_block.maximum_count)
                    print("Vertices Tag Block Address: ", face.vertices_tag_block.address)
                    print("Vertices Tag Block Definition: ", face.vertices_tag_block.definition)
                    print(" ")
                    if DEBUG_FACE_VERTICES:
                        for vertex_idx, vertex in enumerate(face.vertices):
                            print(" ===== Vertex %s ===== " % vertex_idx)
                            print("Vertex Position: ", vertex)
                            print(" ")

            if DEBUG_LEAF_MAP_LEAF_PORTAL_INDICES:
                for portal_index_idx, portal_index in enumerate(leaf_map_leaf.portal_indices):
                    print(" ===== Portal Index %s ===== " % portal_index_idx)
                    print("Portal Index: ", portal_index)
                    print(" ")

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

    if DEBUG_PARSER and DEBUG_LEAF_MAP_PORTALS:
        for leaf_map_portal_idx, leaf_map_portal in enumerate(LEVEL.leaf_map_portals):
            print(" ===== Leaf Map Portal %s ===== " % leaf_map_portal_idx)
            print("Plane Index: ", leaf_map_portal.plane_index)
            print("Back Leaf Index: ", leaf_map_portal.back_leaf_index)
            print("Front Leaf Index: ", leaf_map_portal.front_leaf_index)
            print("Vertices Tag Block Count: ", leaf_map_portal.vertices_tag_block.count)
            print("Vertices Tag Block Maximum Count: ", leaf_map_portal.vertices_tag_block.maximum_count)
            print("Vertices Tag Block Address: ", leaf_map_portal.vertices_tag_block.address)
            print("Vertices Tag Block Definition: ", leaf_map_portal.vertices_tag_block.definition)
            print(" ")
            if DEBUG_LEAF_MAP_PORTAL_VERTICES:
                for vertex_idx, vertex in enumerate(leaf_map_portal.vertices):
                    print(" ===== Vertex %s ===== " % vertex_idx)
                    print("Vertex Translation: ", vertex.translation)
                    print(" ")

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    return LEVEL
