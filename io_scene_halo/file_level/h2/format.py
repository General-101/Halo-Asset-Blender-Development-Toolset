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

from enum import Flag, auto
from mathutils import Vector, Quaternion

class SurfaceFlags(Flag):
    Two_Sided = auto()
    Invisible = auto()
    Climbable = auto()
    Breakable = auto()
    Invalid = auto()
    Conveyor = auto()

class LevelAsset():
    def __init__(self):
        self.header = None
        self.level_body = None
        self.import_info_blocks = []
        self.collision_materials = []
        self.collision_bsps = []
        self.surfaces = []
        self.lightmaps = []

    class LevelBody:
        def __init__(self, import_info_tag_block=None, collision_materials_tag_block=None, collision_bsps_tag_block=None, vehicle_floor=0.0, vehicle_ceiling=0.0, 
                     unused_nodes_tag_block=None, leaves_tag_block=None, world_bounds_x=(0.0, 0.0), world_bounds_y=(0.0, 0.0), world_bounds_z=(0.0, 0.0), 
                     surfaces_references_tag_block=None, cluster_raw_data=None, cluster_portals_tag_block=None, fog_planes_tag_block=None, weather_palettes_tag_block=None, 
                     weather_polyhedras_tag_block=None, detail_objects_tag_block=None, clusters_tag_block=None, materials_tag_block=None, sky_owner_cluster_tag_block=None, 
                     conveyor_surfaces_cluster_tag_block=None, breakable_surfaces_tag_block=None, pathfinding_data_tag_block=None, pathfinding_edges_tag_block=None, 
                     background_sounds_palette_tag_block=None, sound_environment_palette_tag_block=None, sound_pas_raw_data=None, markers_tag_block=None, 
                     runtime_decals_tag_block=None, environment_object_palette_tag_block=None, environment_objects_tag_block=None, lightmaps_tag_block=None, 
                     leaf_map_leaves_tag_block=None, leaf_map_connections_tag_block=None, errors_tag_block=None, precomputed_lighting_tag_block=None, 
                     instanced_geometries_definition_tag_block=None, instanced_geometry_instances_tag_block=None, ambience_sound_clusters_tag_block=None, 
                     reverb_sound_clusters_tag_block=None, transparent_planes_tag_block=None, vehicle_spherical_limit_radius=0.0, vehicle_spherical_limit_center=Vector(), 
                     debug_info_tag_block=None, decorators_bitmaps_tag_ref=None, decorators_0_raw_data=None, decorators_0_vector=Vector(), decorators_1_vector=Vector(), 
                     decorators_1_raw_data=None, breakable_surface_tag_block=None, water_definitions_tag_block=None, portal_device_mapping_tag_block=None, 
                     audibility_tag_block=None, object_fake_lightprobes_tag_block=None, decorators_tag_block=None):
            self.import_info_tag_block = import_info_tag_block
            self.collision_materials_tag_block = collision_materials_tag_block
            self.collision_bsps_tag_block = collision_bsps_tag_block
            self.vehicle_floor = vehicle_floor
            self.vehicle_ceiling = vehicle_ceiling
            self.unused_nodes_tag_block = unused_nodes_tag_block
            self.leaves_tag_block = leaves_tag_block
            self.world_bounds_x = world_bounds_x
            self.world_bounds_y = world_bounds_y
            self.world_bounds_z = world_bounds_z
            self.surfaces_references_tag_block = surfaces_references_tag_block
            self.cluster_raw_data = cluster_raw_data
            self.cluster_portals_tag_block = cluster_portals_tag_block
            self.fog_planes_tag_block = fog_planes_tag_block
            self.weather_palettes_tag_block = weather_palettes_tag_block
            self.weather_polyhedras_tag_block = weather_polyhedras_tag_block
            self.detail_objects_tag_block = detail_objects_tag_block
            self.clusters_tag_block = clusters_tag_block
            self.materials_tag_block = materials_tag_block
            self.sky_owner_cluster_tag_block = sky_owner_cluster_tag_block
            self.conveyor_surfaces_cluster_tag_block = conveyor_surfaces_cluster_tag_block
            self.breakable_surfaces_tag_block = breakable_surfaces_tag_block
            self.pathfinding_data_tag_block = pathfinding_data_tag_block
            self.pathfinding_edges_tag_block = pathfinding_edges_tag_block
            self.background_sounds_palette_tag_block = background_sounds_palette_tag_block
            self.sound_environment_palette_tag_block = sound_environment_palette_tag_block
            self.sound_pas_raw_data = sound_pas_raw_data
            self.markers_tag_block = markers_tag_block
            self.runtime_decals_tag_block = runtime_decals_tag_block
            self.environment_object_palette_tag_block = environment_object_palette_tag_block
            self.environment_objects_tag_block = environment_objects_tag_block
            self.lightmaps_tag_block = lightmaps_tag_block
            self.leaf_map_leaves_tag_block = leaf_map_leaves_tag_block
            self.leaf_map_connections_tag_block = leaf_map_connections_tag_block
            self.errors_tag_block = errors_tag_block
            self.precomputed_lighting_tag_block = precomputed_lighting_tag_block
            self.instanced_geometries_definition_tag_block = instanced_geometries_definition_tag_block
            self.instanced_geometry_instances_tag_block = instanced_geometry_instances_tag_block
            self.ambience_sound_clusters_tag_block = ambience_sound_clusters_tag_block
            self.reverb_sound_clusters_tag_block = reverb_sound_clusters_tag_block
            self.transparent_planes_tag_block = transparent_planes_tag_block
            self.vehicle_spherical_limit_radius = vehicle_spherical_limit_radius
            self.vehicle_spherical_limit_center = vehicle_spherical_limit_center
            self.debug_info_tag_block = debug_info_tag_block
            self.decorators_bitmaps_tag_ref = decorators_bitmaps_tag_ref
            self.decorators_0_raw_data = decorators_0_raw_data
            self.decorators_0_vector = decorators_0_vector
            self.decorators_1_vector = decorators_1_vector
            self.decorators_1_raw_data = decorators_1_raw_data
            self.breakable_surface_tag_block = breakable_surface_tag_block
            self.water_definitions_tag_block = water_definitions_tag_block
            self.portal_device_mapping_tag_block = portal_device_mapping_tag_block
            self.audibility_tag_block = audibility_tag_block
            self.object_fake_lightprobes_tag_block = object_fake_lightprobes_tag_block
            self.decorators_tag_block = decorators_tag_block

    class ImportInfo:
        def __init__(self, build=0, version="", import_date="", culprit="", import_time="", files_tag_block=None, 
                     files=[]):
            self.build = build
            self.version = version
            self.import_date = import_date
            self.culprit = culprit
            self.import_time = import_time
            self.files_tag_block = files_tag_block
            self.files = files

    class Files:
        def __init__(self, path="", modification_date="", checksum=0, size=0, zipped_data=0, uncompressed_data=None):
            self.path = path
            self.modification_date = modification_date
            self.checksum = checksum
            self.size = size
            self.zipped_data = zipped_data
            self.uncompressed_data = uncompressed_data 

    class CollisionMaterial:
        def __init__(self, old_shader=None, conveyor_surface_index=0, new_shader=None):
            self.old_shader = old_shader
            self.conveyor_surface_index = conveyor_surface_index
            self.new_shader = new_shader 

    class CollisionBSP:
        def __init__(self, bsp3d_nodes_tag_block=None, planes_tag_block=None, leaves_tag_block=None, bsp2d_references_tag_block=None, bsp2d_nodes_tag_block=None,
                     surfaces_tag_block=None, edges_tag_block=None, vertices_tag_block=None, bsp3d_nodes=[], planes=[], leaves=[], bsp2d_references=[], bsp2d_nodes=[], surfaces=[],
                     edges=[], vertices=[]):
            self.bsp3d_nodes_tag_block = bsp3d_nodes_tag_block
            self.planes_tag_block = planes_tag_block
            self.leaves_tag_block = leaves_tag_block
            self.bsp2d_references_tag_block = bsp2d_references_tag_block
            self.bsp2d_nodes_tag_block = bsp2d_nodes_tag_block
            self.surfaces_tag_block = surfaces_tag_block
            self.edges_tag_block = edges_tag_block
            self.vertices_tag_block = vertices_tag_block
            self.bsp3d_nodes = bsp3d_nodes
            self.planes = planes
            self.leaves = leaves
            self.bsp2d_references = bsp2d_references
            self.bsp2d_nodes = bsp2d_nodes
            self.surfaces = surfaces
            self.edges = edges
            self.vertices = vertices

    class BSP3DNode:
        def __init__(self, plane=0, back_child=0, front_child=0):
            self.plane = plane
            self.back_child = back_child
            self.front_child = front_child

    class Plane:
        def __init__(self, translation=Vector(), distance=0.0):
            self.translation = translation
            self.distance = distance

    class Leaf:
        def __init__(self, flags=0, bsp2d_reference_count=0, first_bsp2d_reference=0):
            self.flags = flags
            self.bsp2d_reference_count = bsp2d_reference_count
            self.first_bsp2d_reference = first_bsp2d_reference

    class BSP2DReference:
        def __init__(self, plane=0, bsp2d_node=0):
            self.plane = plane
            self.bsp2d_node = bsp2d_node

    class BSP2DNode:
        def __init__(self, plane_i=0.0, plane_j=0.0, distance=0.0, left_child=0, right_child=0):
            self.plane_i = plane_i
            self.plane_j = plane_j
            self.distance = distance
            self.left_child = left_child
            self.right_child = right_child

    class Surface:
        def __init__(self, plane=0, first_edge=0, flags=0, breakable_surface=0, material=0):
            self.plane = plane
            self.first_edge = first_edge
            self.flags = flags
            self.breakable_surface = breakable_surface
            self.material = material

    class Edge:
        def __init__(self, start_vertex=0, end_vertex=0, forward_edge=0, reverse_edge=0, left_surface=0, right_surface=0):
            self.start_vertex = start_vertex
            self.end_vertex = end_vertex
            self.forward_edge = forward_edge
            self.reverse_edge = reverse_edge
            self.left_surface = left_surface
            self.right_surface = right_surface

    class Vertex:
        def __init__(self, translation=Vector(), first_edge=0):
            self.translation = translation
            self.first_edge = first_edge
