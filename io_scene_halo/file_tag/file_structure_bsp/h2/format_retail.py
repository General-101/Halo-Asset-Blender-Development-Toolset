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

from enum import Flag, Enum, auto
from mathutils import Vector, Quaternion

class LeafFlags(Flag):
    contains_double_sided_surfaces = auto()

class SurfaceFlags(Flag):
    two_sided = auto()
    invisible = auto()
    climbable = auto()
    breakable = auto()
    invalid = auto()
    conveyor = auto()

class ClusterPortalFlags(Flag):
    ai_cant_hear_through_this = auto()
    one_way = auto()
    door = auto()
    no_way = auto()
    one_way_reversed = auto()
    no_one_can_hear_through_this = auto()

class FogPlaneFlags(Flag):
    extend_infinitely_while_visible = auto()
    dont_floodfill = auto()
    aggressive_floodfill = auto()

class GeometryClassificationEnum(Enum):
    worldspace = 0
    rigid = auto()
    rigid_boned = auto()
    skinned = auto()
    unsupported = auto()

class GeometryCompressionFlags(Flag):
    compressed_position = auto()
    compressed_texcoord = auto()
    compressed_secondary_texcoord = auto()

class SectionLightingFlags(Flag):
    has_lm_texcoords = auto()
    has_lm_inc_rad = auto()
    has_lm_colors = auto()
    has_lm_prt = auto()

class ClusterFlags(Flag):
    one_way_portal = auto()
    door_portaL = auto()
    postprocessed_geometry = auto()
    is_the_sjy = auto()

class ResourceEnum(Enum):
    tag_block = 0
    tag_data = auto()
    vertex_buffer = auto()

class PartTypeEnum(Enum):
    not_drawn = 0
    opaque_shadow_only = auto()
    opaque_shadow_casting = auto()
    opaque_non_shadowing = auto()
    transparent = auto()
    lightmap_only = auto()

class PartFlags(Flag):
    decalable = auto()
    new_part_type = auto()
    dislikes_photons = auto()
    override_triangle_list = auto()
    ignored_by_lightmapper = auto()

class PredictedResourceTypeEnum(Enum):
    bitmap = 0
    sound = auto()
    render_model_geometry = auto()
    cluster_geometry = auto()
    cluster_instanced_geometry = auto()
    lightmap_geometry_object_buckets = auto()
    lightmap_geometry_instance_buckets = auto()
    lightmap_cluster_bitmaps = auto()
    lightmap_instance_bitmaps = auto()

class PropertyTypeEnum(Enum):
    lightmap_resolution = 0
    lightmap_power = auto()
    lightmap_half_life = auto()
    lightmap_diffuse_scale = auto()

class LevelAsset():
    def __init__(self):
        self.header = None
        self.level_header = None
        self.level_body = None
        self.import_info_header = None
        self.import_info = None
        self.collision_materials_header = None
        self.collision_materials = None
        self.collision_bsp_header = None
        self.collision_bsps = None
        self.unused_nodes_header = None
        self.unused_nodes = None
        self.leaves_header = None
        self.leaves = None
        self.surface_references_header = None
        self.surface_references = None
        self.cluster_data = None
        self.cluster_portals_header = None
        self.cluster_portals = None
        self.fog_planes_header = None
        self.fog_planes = None
        self.weather_palette_header = None
        self.weather_palette = None
        self.weather_polyhedra_header = None
        self.weather_polyhedra = None
        self.detail_objects_header = None
        self.detail_objects = None
        self.clusters_header = None
        self.clusters = None
        self.material_header = None
        self.materials = None

    class LevelBody:
        def __init__(self, import_info_tag_block=None, collision_materials_tag_block=None, collision_bsps_tag_block=None, vehicle_floor=0.0, vehicle_ceiling=0.0,
                     unused_nodes_tag_block=None, leaves_tag_block=None, world_bounds_x=(0.0, 0.0), world_bounds_y=(0.0, 0.0), world_bounds_z=(0.0, 0.0),
                     surface_references_tag_block=None, cluster_raw_data=None, cluster_portals_tag_block=None, fog_planes_tag_block=None, weather_palette_tag_block=None,
                     weather_polyhedra_tag_block=None, detail_objects_tag_block=None, clusters_tag_block=None, materials_tag_block=None, sky_owner_cluster_tag_block=None,
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
            self.surface_references_tag_block = surface_references_tag_block
            self.cluster_raw_data = cluster_raw_data
            self.cluster_portals_tag_block = cluster_portals_tag_block
            self.fog_planes_tag_block = fog_planes_tag_block
            self.weather_palette_tag_block = weather_palette_tag_block
            self.weather_polyhedra_tag_block = weather_polyhedra_tag_block
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
        def __init__(self, build=0, version="", import_date="", culprit="", import_time="", files_tag_block=None, files_header=None, files=None):
            self.build = build
            self.version = version
            self.import_date = import_date
            self.culprit = culprit
            self.import_time = import_time
            self.files_tag_block = files_tag_block
            self.files_header = files_header
            self.files = files

    class File:
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
                     surfaces_tag_block=None, edges_tag_block=None, vertices_tag_block=None, bsp3d_nodes_header=None, planes_header=None, leaves_header=None,
                     bsp2d_references_header=None, bsp2d_nodes_header=None, surfaces_header=None, edges_header=None, vertices_header=None, bsp3d_nodes=None, planes=None, leaves=None,
                     bsp2d_references=None, bsp2d_nodes=None, surfaces=None, edges=None, vertices=None):
            self.bsp3d_nodes_tag_block = bsp3d_nodes_tag_block
            self.planes_tag_block = planes_tag_block
            self.leaves_tag_block = leaves_tag_block
            self.bsp2d_references_tag_block = bsp2d_references_tag_block
            self.bsp2d_nodes_tag_block = bsp2d_nodes_tag_block
            self.surfaces_tag_block = surfaces_tag_block
            self.edges_tag_block = edges_tag_block
            self.vertices_tag_block = vertices_tag_block
            self.bsp3d_nodes_header = bsp3d_nodes_header
            self.planes_header = planes_header
            self.leaves_header = leaves_header
            self.bsp2d_references_header = bsp2d_references_header
            self.bsp2d_nodes_header = bsp2d_nodes_header
            self.surfaces_header = surfaces_header
            self.edges_header = edges_header
            self.vertices_header = vertices_header
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
        def __init__(self, plane=None, left_child=0, right_child=0):
            self.plane = plane
            self.left_child = left_child
            self.right_child = right_child

    class Surface:
        def __init__(self, plane=0, first_edge=0, flags=0, breakable_surface=0, material=0):
            self.plane = plane
            self.first_edge = first_edge
            self.flags = flags
            self.breakable_surface = breakable_surface
            self.material = material

    class Vertex:
        def __init__(self, translation=Vector(), first_edge=0):
            self.translation = translation
            self.first_edge = first_edge

    class Edge:
        def __init__(self, start_vertex=0, end_vertex=0, forward_edge=0, reverse_edge=0, left_surface=0, right_surface=0):
            self.start_vertex = start_vertex
            self.end_vertex = end_vertex
            self.forward_edge = forward_edge
            self.reverse_edge = reverse_edge
            self.left_surface = left_surface
            self.right_surface = right_surface

    class ClusterLeaf:
        def __init__(self, cluster=0, surface_reference_count=0, surface_reference=0):
            self.cluster = cluster
            self.surface_reference_count = surface_reference_count
            self.surface_reference = surface_reference

    class SurfaceReference:
        def __init__(self, strip_index=0, lightmap_triangle_index=0, bsp_node_index=0):
            self.strip_index = strip_index
            self.lightmap_triangle_index = lightmap_triangle_index
            self.bsp_node_index = bsp_node_index

    class ClusterPortal:
        def __init__(self, back_cluster=0, front_cluster=0, plane_index=0, centroid=Vector(), bounding_radius=0.0, flags=0, vertices_header=None, vertices_tag_block=None,
                     vertices=None):
            self.back_cluster = back_cluster
            self.front_cluster = front_cluster
            self.plane_index = plane_index
            self.centroid = centroid
            self.bounding_radius = bounding_radius
            self.flags = flags
            self.vertices_header = vertices_header
            self.vertices_tag_block = vertices_tag_block
            self.vertices = vertices

    class FogPlane:
        def __init__(self, scenario_planar_fog_index=0, plane=None, flags=0, priority=0):
            self.scenario_planar_fog_index = scenario_planar_fog_index
            self.plane = plane
            self.flags = flags
            self.priority = priority

    class WeatherPalette:
        def __init__(self, name="", weather_system=None, wind=None, wind_direction=Vector(), wind_magnitude=0, wind_scale_function=""):
            self.name = name
            self.weather_system = weather_system
            self.wind = wind
            self.wind_direction = wind_direction
            self.wind_magnitude = wind_magnitude
            self.wind_scale_function = wind_scale_function
    
    class WeatherPolyhedra:
        def __init__(self, bounding_sphere_center=Vector(), bounding_sphere_radius=0.0, planes_header=None, planes_tag_block=None, planes=None):
            self.bounding_sphere_center = bounding_sphere_center
            self.bounding_sphere_radius = bounding_sphere_radius
            self.planes_header = planes_header
            self.planes_tag_block = planes_tag_block
            self.planes = planes

    class DetailObject:
        def __init__(self, cells_header=None, cells_tag_block=None, cells=None, instances_header=None, instances_tag_block=None, instances=None, counts_header=None, 
                     counts_tag_block=None, counts=None, z_reference_vectors_header=None, z_reference_vectors_tag_block=None, z_reference_vectors=None):
            self.cells_header = cells_header
            self.cells_tag_block = cells_tag_block
            self.cells = cells
            self.instances_header = instances_header
            self.instances_tag_block = instances_tag_block
            self.instances = instances
            self.counts_header = counts_header
            self.counts_tag_block = counts_tag_block
            self.counts = counts
            self.z_reference_vectors_header = z_reference_vectors_header
            self.z_reference_vectors_tag_block = z_reference_vectors_tag_block
            self.z_reference_vectors = z_reference_vectors

    class Cell:
        def __init__(self, unknown_0=0, unknown_1=0, unknown_2=0, unknown_3=0, unknown_4=0, unknown_5=0, unknown_6=0):
            self.unknown_0 = unknown_0
            self.unknown_1 = unknown_1
            self.unknown_2 = unknown_2
            self.unknown_3 = unknown_3
            self.unknown_4 = unknown_4
            self.unknown_5 = unknown_5
            self.unknown_6 = unknown_6

    class Instances:
        def __init__(self, unknown_0=0, unknown_1=0, unknown_2=0, unknown_3=0, unknown_4=0):
            self.unknown_0 = unknown_0
            self.unknown_1 = unknown_1
            self.unknown_2 = unknown_2
            self.unknown_3 = unknown_3
            self.unknown_4 = unknown_4

    class ZReferenceVector:
        def __init__(self, unknown_0=0, unknown_1=0, unknown_2=0, unknown_3=0):
            self.unknown_0 = unknown_0
            self.unknown_1 = unknown_1
            self.unknown_2 = unknown_2
            self.unknown_3 = unknown_3

    class Cluster:
        def __init__(self, total_vertex_count=0, total_triangle_count=0, total_part_count=0, shadow_casting_triangle_count=0, shadow_casting_part_count=0, opaque_point_count=0, 
                     opaque_vertex_count=0, opaque_part_count=0, opaque_max_nodes_vertex=0, transparent_max_nodes_vertex=0, shadow_casting_rigid_triangle_count=0, 
                     geometry_classification=0, geometry_compression_flags=0, compression_info_header=None, compression_info_tag_block=None, hardware_node_count=0, node_map_size=0, 
                     software_plane_count=0, total_subpart_count=0, section_lighting_flags=0, block_offset=0, block_size=0, section_data_size=0, resource_data_size=0, 
                     resources_header=None, resources_tag_block=None, owner_tag_section_offset=0, cluster_data_header=None, cluster_data_tag_block=None, bounds_x=(0.0, 0.0), 
                     bounds_y=(0.0, 0.0), bounds_z=(0.0, 0.0), scenario_sky_index=0, media_index=0, scenario_visible_sky_index=0, scenario_atmospheric_fog_index=0, 
                     planar_fog_designator=0, visible_fog_plane_index=0, background_sound=0, sound_environment=0, weather=0, transition_structure_bsp=0, flags=0, 
                     predicted_resources_header=None, predicted_resources_tag_block=None, portals_header=None, portals_tag_block=None, checksum_from_structure=0, 
                     instanced_geometry_indices_header=None, instanced_geometry_indices_tag_block=None, index_reorder_table_header=None, index_reorder_table_tag_block=None, 
                     collision_mopp_code_data=None, sinf_header=None, blok_header=None, compression_info=None, cluster_data=None, predicted_resources=None, resources=None, portals=None, 
                     instanced_geometry_indices=None, index_reorder_table=None, collision_mopp_code=None):
            self.total_vertex_count = total_vertex_count
            self.total_triangle_count = total_triangle_count
            self.total_part_count = total_part_count
            self.shadow_casting_triangle_count = shadow_casting_triangle_count
            self.shadow_casting_part_count = shadow_casting_part_count
            self.opaque_point_count = opaque_point_count
            self.opaque_vertex_count = opaque_vertex_count
            self.opaque_part_count = opaque_part_count
            self.opaque_max_nodes_vertex = opaque_max_nodes_vertex
            self.transparent_max_nodes_vertex = transparent_max_nodes_vertex
            self.shadow_casting_rigid_triangle_count = shadow_casting_rigid_triangle_count
            self.geometry_classification = geometry_classification
            self.geometry_compression_flags = geometry_compression_flags
            self.compression_info_header = compression_info_header
            self.compression_info_tag_block = compression_info_tag_block
            self.hardware_node_count = hardware_node_count
            self.node_map_size = node_map_size
            self.software_plane_count = software_plane_count
            self.total_subpart_count = total_subpart_count
            self.section_lighting_flags = section_lighting_flags
            self.block_offset = block_offset
            self.block_size = block_size
            self.section_data_size = section_data_size
            self.resource_data_size = resource_data_size
            self.resources_header = resources_header
            self.resources_tag_block = resources_tag_block
            self.owner_tag_section_offset = owner_tag_section_offset
            self.cluster_data_header = cluster_data_header
            self.cluster_data_tag_block = cluster_data_tag_block
            self.bounds_x = bounds_x
            self.bounds_y = bounds_y
            self.bounds_z = bounds_z
            self.scenario_sky_index = scenario_sky_index
            self.media_index = media_index
            self.scenario_visible_sky_index = scenario_visible_sky_index
            self.scenario_atmospheric_fog_index = scenario_atmospheric_fog_index
            self.planar_fog_designator = planar_fog_designator
            self.visible_fog_plane_index = visible_fog_plane_index
            self.background_sound = background_sound
            self.sound_environment = sound_environment
            self.weather = weather
            self.transition_structure_bsp = transition_structure_bsp
            self.flags = flags
            self.predicted_resources_header = predicted_resources_header
            self.predicted_resources_tag_block = predicted_resources_tag_block
            self.portals_header = portals_header
            self.portals_tag_block = portals_tag_block
            self.checksum_from_structure = checksum_from_structure
            self.instanced_geometry_indices_header = instanced_geometry_indices_header
            self.instanced_geometry_indices_tag_block = instanced_geometry_indices_tag_block
            self.index_reorder_table_header = index_reorder_table_header
            self.index_reorder_table_tag_block = index_reorder_table_tag_block
            self.collision_mopp_code_data = collision_mopp_code_data
            self.sinf_header = sinf_header
            self.blok_header = blok_header
            self.compression_info = compression_info
            self.resources = resources
            self.cluster_data = cluster_data
            self.predicted_resources = predicted_resources
            self.portals = portals
            self.instanced_geometry_indices = instanced_geometry_indices
            self.index_reorder_table = index_reorder_table
            self.collision_mopp_code = collision_mopp_code

    class CompressionInfo:
        def __init__(self, position_bounds_x=(0.0, 0.0), position_bounds_y=(0.0, 0.0), position_bounds_z=(0.0, 0.0), texcoord_bounds_x=(0.0, 0.0), texcoord_bounds_y=(0.0, 0.0), 
                     secondary_texcoord_bounds_x=(0.0, 0.0), secondary_texcoord_bounds_y=(0.0, 0.0)):
            self.position_bounds_x = position_bounds_x
            self.position_bounds_y = position_bounds_y
            self.position_bounds_z = position_bounds_z
            self.texcoord_bounds_x = texcoord_bounds_x
            self.texcoord_bounds_y = texcoord_bounds_y
            self.secondary_texcoord_bounds_x = secondary_texcoord_bounds_x
            self.secondary_texcoord_bounds_y = secondary_texcoord_bounds_y

    class Resource:
        def __init__(self, type=0, primary_locator=0, secondary_locator=0, resource_data_size=0, resource_data_offset=0):
            self.type = type
            self.primary_locator = primary_locator
            self.secondary_locator = secondary_locator
            self.resource_data_size = resource_data_size
            self.resource_data_offset = resource_data_offset

    class ClusterData:
        def __init__(self, parts_header=None, parts_tag_block=None, subparts_header=None, subparts_tag_block=None, visibility_bounds_header=None,
                     visibility_bounds_tag_block=None, raw_vertices_header=None, raw_vertices_tag_block=None, strip_indices_header=None,
                     strip_indices_tag_block=None, visibility_mopp_code_data=0, mopp_reorder_table_header=None, mopp_reorder_table_tag_block=None,
                     vertex_buffers_header=None, vertex_buffers_tag_block=None, parts=None, subparts=None, visibility_bounds=None, raw_vertices=None,
                     strip_indices=None, visibility_mopp_code=None, mopp_reorder_table=None, vertex_buffers=None, sect_header=None):
            self.parts_header = parts_header
            self.parts_tag_block = parts_tag_block
            self.subparts_header = subparts_header
            self.subparts_tag_block = subparts_tag_block
            self.visibility_bounds_header = visibility_bounds_header
            self.visibility_bounds_tag_block = visibility_bounds_tag_block
            self.raw_vertices_header = raw_vertices_header
            self.raw_vertices_tag_block = raw_vertices_tag_block
            self.strip_indices_header = strip_indices_header
            self.strip_indices_tag_block = strip_indices_tag_block
            self.visibility_mopp_code_data = visibility_mopp_code_data
            self.mopp_reorder_table_header = mopp_reorder_table_header
            self.mopp_reorder_table_tag_block = mopp_reorder_table_tag_block
            self.vertex_buffers_header = vertex_buffers_header
            self.vertex_buffers_tag_block = vertex_buffers_tag_block
            self.parts = parts
            self.subparts = subparts
            self.visibility_bounds = visibility_bounds
            self.raw_vertices = raw_vertices
            self.strip_indices = strip_indices
            self.visibility_mopp_code = visibility_mopp_code
            self.mopp_reorder_table = mopp_reorder_table
            self.vertex_buffers = vertex_buffers
            self.sect_header = sect_header

    class Part:
        def __init__(self, part_type=0, flags=0, material_index=0, strip_start_index=0, strip_length=0, first_subpart_index=0, subpart_count=0,
                     max_nodes_vertex=0, contributing_compound_node_count=0, position=Vector(), node_index_0=0, node_index_1=0, node_index_2=0, node_index_3=0,
                     node_weight_0=0.0, node_weight_1=0.0, node_weight_2=0.0, node_weight_3=0.0, lod_mipmap_magic_number=0):
            self.part_type = part_type
            self.flags = flags
            self.material_index = material_index
            self.strip_start_index = strip_start_index
            self.strip_length = strip_length
            self.first_subpart_index = first_subpart_index
            self.subpart_count = subpart_count
            self.max_nodes_vertex = max_nodes_vertex
            self.contributing_compound_node_count = contributing_compound_node_count
            self.position = position
            self.node_index_0 = node_index_0
            self.node_index_1 = node_index_1
            self.node_index_2 = node_index_2
            self.node_index_3 = node_index_3
            self.node_weight_0 = node_weight_0
            self.node_weight_1 = node_weight_1
            self.node_weight_2 = node_weight_2
            self.node_weight_3 = node_weight_3
            self.lod_mipmap_magic_number = lod_mipmap_magic_number

    class PartCache(Part):
        def __init__(self, geometry_subclassification=0, first_strip_segment_index=0, strip_segment_count=0, first_vertex_index=0, vertex_count=0, first_triangle_index=0,
                     triangle_count=0, max_nodes_per_vertex=0, vertex_usage_flags=0):
            super().__init__()
            self.geometry_subclassification = geometry_subclassification
            self.first_strip_segment_index = first_strip_segment_index
            self.strip_segment_count = strip_segment_count
            self.first_vertex_index = first_vertex_index
            self.vertex_count = vertex_count
            self.first_triangle_index = first_triangle_index
            self.triangle_count = triangle_count
            self.max_nodes_per_vertex = max_nodes_per_vertex
            self.vertex_usage_flags = vertex_usage_flags

    class SubPart:
        def __init__(self, indices_start_index=0, indices_length=0, visibility_bounds_index=0, part_index=0):
            self.indices_start_index = indices_start_index
            self.indices_length = indices_length
            self.visibility_bounds_index = visibility_bounds_index
            self.part_index = part_index

    class VisibilityBounds:
        def __init__(self, position=Vector(), radius=0.0, node_0=0):
            self.position = position
            self.radius = radius
            self.node_0 = node_0

    class RawPoint:
        def __init__(self, position=Vector(), node_index_0_old=0, node_index_1_old=0, node_index_2_old=0, node_index_3_old=0, node_weight_0=0.0, node_weight_1=0.0,
                     node_weight_2=0.0, node_weight_3=0.0, node_index_0_new=0, node_index_1_new=0, node_index_2_new=0, node_index_3_new=0, uses_new_node_indices=0,
                     adjusted_compound_node_index=0):
            self.position = position
            self.node_index_0_old = node_index_0_old
            self.node_index_1_old = node_index_1_old
            self.node_index_2_old = node_index_2_old
            self.node_index_3_old = node_index_3_old
            self.node_weight_0 = node_weight_0
            self.node_weight_1 = node_weight_1
            self.node_weight_2 = node_weight_2
            self.node_weight_3 = node_weight_3
            self.node_index_0_new = node_index_0_new
            self.node_index_1_new = node_index_1_new
            self.node_index_2_new = node_index_2_new
            self.node_index_3_new = node_index_3_new
            self.uses_new_node_indices = uses_new_node_indices
            self.adjusted_compound_node_index = adjusted_compound_node_index

    class RawVertex(RawPoint):
        def __init__(self, texcoord=(0.0, 0.0), normal=Vector(), binormal=Vector(), tangent=Vector(), anisotropic_binormal=Vector(), secondary_texcoord=(0.0, 0.0),
                     primary_lightmap_color_RGBA=(0.0, 0.0, 0.0, 1.0), primary_lightmap_texcoord=(0.0, 0.0), primary_lightmap_incident_direction=Vector()):
            super().__init__()
            self.texcoord = texcoord
            self.normal = normal
            self.binormal = binormal
            self.tangent = tangent
            self.anisotropic_binormal = anisotropic_binormal
            self.secondary_texcoord = secondary_texcoord
            self.primary_lightmap_color_RGBA = primary_lightmap_color_RGBA
            self.primary_lightmap_texcoord = primary_lightmap_texcoord
            self.primary_lightmap_incident_direction = primary_lightmap_incident_direction

    class PredictedResource:
        def __init__(self, type=0, resource_index=0, tag_index=0):
            self.type = type
            self.resource_index = resource_index
            self.tag_index = tag_index

    class Material:
        def __init__(self, old_shader=None, shader=None, properties_header=None, properties_tag_block=None, breakable_surface_index=0, properties=None):
            self.old_shader = old_shader
            self.shader = shader
            self.properties_header = properties_header
            self.properties_tag_block = properties_tag_block
            self.breakable_surface_index = breakable_surface_index
            self.properties = properties

    class Property:
        def __init__(self, type=0, int_value=0, real_value=0.0):
            self.type = type
            self.int_value = int_value
            self.real_value = real_value
