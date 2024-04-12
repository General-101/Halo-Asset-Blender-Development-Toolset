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
    is_the_sky = auto()

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

class PathfindingSectorFlags(Flag):
    sector_walkable = auto()
    sector_breakable = auto()
    sector_mobile = auto()
    sector_bsp_source = auto()
    floor = auto()
    ceiling = auto()
    wall_north = auto()
    wall_south = auto()
    wall_east = auto()
    wall_west = auto()
    crouchable = auto()
    aligned = auto()
    sector_step = auto()
    sector_interior = auto()

class LinkFlags(Flag):
    sector_link_from_collision_edge = auto()
    sector_intersection_link = auto()
    sector_link_bsp2d_creation_error = auto()
    sector_link_topology_error = auto()
    sector_link_chain_error = auto()
    sector_link_both_sectors_walkable = auto()
    sector_link_magic_hanging_link = auto()
    sector_link_threshold = auto()
    sector_link_crouchable = auto()
    sector_link_wall_base = auto()
    sector_link_ledge = auto()
    sector_link_leanable = auto()
    sector_link_start_corner = auto()
    sector_link_end_corner = auto()

class ObjectRefFlags(Flag):
    mobile = auto()

class NodeFlags(Flag):
    projection_sign = auto()

class HintTypeEnum(Enum):
    intersection_link = 0
    jump_link = auto()
    climb_link = auto()
    vault_link = auto()
    mount_link = auto()
    hoist_link = auto()
    wall_jump_link = auto()
    breakable_floor = auto()

class GeometryFlags(Flag):
    bidirectional = auto()
    closed = auto()

class ForceJumpHeightEnum(Enum):
    none = 0
    down = auto()
    step = auto()
    crouch = auto()
    stand = auto()
    storey = auto()
    tower = auto()
    infinite = auto()

class JumpControlFlags(Flag):
    magic_lift = auto()

class HintFlags(Flag):
    bidirectional = auto()

class WellTypeEnum(Enum):
    jump = 0
    climb = auto()
    hoist = auto()

class BackgroundScaleFlags(Flag):
    override_default_scale = auto()
    use_adjacent_cluster_as_portal_scale = auto()
    use_adjacent_cluster_as_exterior_scale = auto()
    scale_with_weather_intensity = auto()

class ReportTypeEnum(Enum):
    silent = 0
    comment = auto()
    warning = auto()
    error = auto()

class ReportFlags(Flag):
    rendered = auto()
    tangent_space = auto()
    non_critical = auto()
    lightmap_light = auto()
    report_key_is_valid = auto()

class LightTypeEnum(Enum):
    free_standing = 0
    attached_to_editor_object = auto()
    attached_to_structure_object = auto()

class InstanceFlags(Flag):
    not_in_lightprobes = auto()

class PathfindingPolicyEnum(Enum):
    cut_out = 0
    static = auto()
    none = auto()

class LightmappingPolicyEnum(Enum):
    per_pixel = 0
    per_vertex = auto()

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
        self.sky_owner_cluster_header = None
        self.sky_owner_cluster = None
        self.conveyor_surfaces_header = None
        self.conveyor_surfaces = None
        self.breakable_surfaces_header = None
        self.breakable_surfaces = None
        self.pathfinding_data_header = None
        self.pathfinding_data = None
        self.pathfinding_edges_header = None
        self.pathfinding_edges = None
        self.background_sound_palette_header = None
        self.background_sound_palette = None
        self.sound_environment_palette_header = None
        self.sound_environment_palette = None
        self.sound_pas_data = None
        self.markers_header = None
        self.markers = None
        self.runtime_decals_header = None
        self.runtime_decals = None
        self.environment_object_palette_header = None
        self.environment_object_palette = None
        self.environment_objects_header = None
        self.environment_objects = None
        self.lightmaps_header = None
        self.lightmaps = None
        self.leaf_map_leaves_header = None
        self.leaf_map_leaves = None
        self.leaf_map_connections_header = None
        self.leaf_map_connections = None
        self.errors_header = None
        self.errors = None
        self.precomputed_lighting_header = None
        self.precomputed_lighting = None
        self.instanced_geometry_definition_header = None
        self.instanced_geometry_definition = None
        self.instanced_geometry_instances_header = None
        self.instanced_geometry_instances = None

    class LevelBody:
        def __init__(self, import_info_tag_block=None, collision_materials_tag_block=None, collision_bsps_tag_block=None, vehicle_floor=0.0, vehicle_ceiling=0.0,
                     unused_nodes_tag_block=None, leaves_tag_block=None, world_bounds_x=(0.0, 0.0), world_bounds_y=(0.0, 0.0), world_bounds_z=(0.0, 0.0),
                     surface_references_tag_block=None, cluster_raw_data=None, cluster_portals_tag_block=None, fog_planes_tag_block=None, weather_palette_tag_block=None,
                     weather_polyhedra_tag_block=None, detail_objects_tag_block=None, clusters_tag_block=None, materials_tag_block=None, sky_owner_cluster_tag_block=None,
                     conveyor_surfaces_tag_block=None, breakable_surfaces_tag_block=None, pathfinding_data_tag_block=None, pathfinding_edges_tag_block=None,
                     background_sound_palette_tag_block=None, sound_environment_palette_tag_block=None, sound_pas_raw_data=None, markers_tag_block=None,
                     runtime_decals_tag_block=None, environment_object_palette_tag_block=None, environment_objects_tag_block=None, lightmaps_tag_block=None,
                     leaf_map_leaves_tag_block=None, leaf_map_connections_tag_block=None, errors_tag_block=None, precomputed_lighting_tag_block=None,
                     instanced_geometry_definition_tag_block=None, instanced_geometry_instances_tag_block=None, ambience_sound_clusters_tag_block=None,
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
            self.conveyor_surfaces_tag_block = conveyor_surfaces_tag_block
            self.breakable_surfaces_tag_block = breakable_surfaces_tag_block
            self.pathfinding_data_tag_block = pathfinding_data_tag_block
            self.pathfinding_edges_tag_block = pathfinding_edges_tag_block
            self.background_sound_palette_tag_block = background_sound_palette_tag_block
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
            self.instanced_geometry_definition_tag_block = instanced_geometry_definition_tag_block
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

    class Section:
        def __init__(self, total_vertex_count=0, total_triangle_count=0, total_part_count=0, shadow_casting_triangle_count=0, shadow_casting_part_count=0, opaque_point_count=0, 
                     opaque_vertex_count=0, opaque_part_count=0, opaque_max_nodes_vertex=0, transparent_max_nodes_vertex=0, shadow_casting_rigid_triangle_count=0, 
                     geometry_classification=0, geometry_compression_flags=0, compression_info_header=None, compression_info_tag_block=None, hardware_node_count=0, node_map_size=0, 
                     software_plane_count=0, total_subpart_count=0, section_lighting_flags=0, block_offset=0, block_size=0, section_data_size=0, resource_data_size=0, 
                     resources_header=None, resources_tag_block=None, owner_tag_section_offset=0):
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

    class Cluster(Section):
        def __init__(self, cluster_data_header=None, cluster_data_tag_block=None, bounds_x=(0.0, 0.0), bounds_y=(0.0, 0.0), bounds_z=(0.0, 0.0), scenario_sky_index=0, media_index=0, 
                     scenario_visible_sky_index=0, scenario_atmospheric_fog_index=0, planar_fog_designator=0, visible_fog_plane_index=0, background_sound=0, sound_environment=0, 
                     weather=0, transition_structure_bsp=0, flags=0, predicted_resources_header=None, predicted_resources_tag_block=None, portals_header=None, portals_tag_block=None, 
                     checksum_from_structure=0, instanced_geometry_indices_header=None, instanced_geometry_indices_tag_block=None, index_reorder_table_header=None, 
                     index_reorder_table_tag_block=None, collision_mopp_code_data=None, sinf_header=None, blok_header=None, compression_info=None, cluster_data=None, 
                     predicted_resources=None, resources=None, portals=None, instanced_geometry_indices=None, index_reorder_table=None, collision_mopp_code=None):
            super().__init__()
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
        def __init__(self, property_type=0, int_value=0, real_value=0.0):
            self.property_type = property_type
            self.int_value = int_value
            self.real_value = real_value

    class ConveyorSurface:
        def __init__(self, u=Vector(), v=Vector()):
            self.u = u
            self.v = v

    class BreakableSurface:
        def __init__(self, instanced_geometry_instance=0, breakable_surface_index=0, centroid=Vector(), radius=0.0, collision_surface_index=0):
            self.instanced_geometry_instance = instanced_geometry_instance
            self.breakable_surface_index = breakable_surface_index
            self.centroid = centroid
            self.radius = radius
            self.collision_surface_index = collision_surface_index

    class AIPathfindingData():
        def __init__(self, sectors_tag_block=None, sectors_header=None, sectors=None, links_tag_block=None, links_header=None, links=None, refs_tag_block=None, refs_header=None, 
                     refs=None, bsp2d_nodes_tag_block=None, bsp2d_nodes_header=None, bsp2d_nodes=None, surface_flags_tag_block=None, surface_flags_header=None, surface_flags=None, 
                     vertices_tag_block=None, vertices_header=None, vertices=None, object_refs_tag_block=None, object_refs_header=None, object_refs=None, 
                     pathfinding_hints_tag_block=None, pathfinding_hints_header=None, pathfinding_hints=None, instanced_geometry_refs_tag_block=None, 
                     instanced_geometry_refs_header=None, instanced_geometry_refs=None, structure_checksum=0, user_placed_hints_tag_block=None, user_placed_hints_header=None, 
                     user_placed_hints=None):
            self.sectors_tag_block = sectors_tag_block
            self.sectors_header = sectors_header
            self.sectors = sectors
            self.links_tag_block = links_tag_block
            self.links_header = links_header
            self.links = links
            self.refs_tag_block = refs_tag_block
            self.refs_header = refs_header
            self.refs = refs
            self.bsp2d_nodes_tag_block = bsp2d_nodes_tag_block
            self.bsp2d_nodes_header = bsp2d_nodes_header
            self.bsp2d_nodes = bsp2d_nodes
            self.surface_flags_tag_block = surface_flags_tag_block
            self.surface_flags_header = surface_flags_header
            self.surface_flags = surface_flags
            self.vertices_tag_block = vertices_tag_block
            self.vertices_header = vertices_header
            self.vertices = vertices
            self.object_refs_tag_block = object_refs_tag_block
            self.object_refs_header = object_refs_header
            self.object_refs = object_refs
            self.pathfinding_hints_tag_block = pathfinding_hints_tag_block
            self.pathfinding_hints_header = pathfinding_hints_header
            self.pathfinding_hints = pathfinding_hints
            self.instanced_geometry_refs_tag_block = instanced_geometry_refs_tag_block
            self.instanced_geometry_refs_header = instanced_geometry_refs_header
            self.instanced_geometry_refs = instanced_geometry_refs
            self.structure_checksum = structure_checksum
            self.user_placed_hints_tag_block = user_placed_hints_tag_block
            self.user_placed_hints_header = user_placed_hints_header
            self.user_placed_hints = user_placed_hints

    class Sector():
        def __init__(self, pathfinding_sector_flags=0, hint_index=0, first_link=0):
            self.pathfinding_sector_flags = pathfinding_sector_flags
            self.hint_index = hint_index
            self.first_link = first_link

    class Link():
        def __init__(self, vertex_1=0, vertex_2=0, link_flags=0, hint_index=0, forward_link=0, reverse_link=0, left_sector=0, right_sector=0):
            self.vertex_1 = vertex_1
            self.vertex_2 = vertex_2
            self.link_flags = link_flags
            self.hint_index = hint_index
            self.forward_link = forward_link
            self.reverse_link = reverse_link
            self.left_sector = left_sector
            self.right_sector = right_sector

    class Bsp2DNode():
        def __init__(self, plane=None, left_child=0, right_child=0):
            self.plane = plane
            self.left_child = left_child
            self.right_child = right_child

    class ObjectRef():
        def __init__(self, flags=0, first_sector=0, last_sector=0, bsps_tag_block=None, bsps_header=None, bsps=None, nodes_tag_block=None, nodes_header=None, nodes=None):
            self.flags = flags
            self.first_sector = first_sector
            self.last_sector = last_sector
            self.bsps_tag_block = bsps_tag_block
            self.bsps_header = bsps_header
            self.bsps = bsps
            self.nodes_tag_block = nodes_tag_block
            self.nodes_header = nodes_header
            self.nodes = nodes

    class BSP():
        def __init__(self, bsp_reference=0, first_sector=0, last_sector=0, node_index=0):
            self.bsp_reference = bsp_reference
            self.first_sector = first_sector
            self.last_sector = last_sector
            self.node_index = node_index

    class Node():
        def __init__(self, reference_frame_index=0, projection_axis=0, projection_sign=0):
            self.reference_frame_index = reference_frame_index
            self.projection_axis = projection_axis
            self.projection_sign = projection_sign

    class PathfindingHint():
        def __init__(self, hint_type=0, next_hint_index=0, hint_data_0=0, hint_data_1=0, hint_data_2=0, hint_data_3=0, hint_data_4=0, hint_data_5=0, hint_data_6=0, hint_data_7=0):
            self.hint_type = hint_type
            self.next_hint_index = next_hint_index
            self.hint_data_0 = hint_data_0
            self.hint_data_1 = hint_data_1
            self.hint_data_2 = hint_data_2
            self.hint_data_3 = hint_data_3
            self.hint_data_4 = hint_data_4
            self.hint_data_5 = hint_data_5
            self.hint_data_6 = hint_data_6
            self.hint_data_7 = hint_data_7

    class UserPlacedHint():
        def __init__(self, point_geometry_tag_block=None, point_geometry_header=None, point_geometry=None, ray_geometry_tag_block=None, ray_geometry_header=None, ray_geometry=None, 
                     line_segment_geometry_tag_block=None, line_segment_geometry_header=None, line_segment_geometry=None, parallelogram_geometry_tag_block=None, 
                     parallelogram_geometry_header=None, parallelogram_geometry=None, polygon_geometry_tag_block=None, polygon_geometry_header=None, polygon_geometry=None, 
                     jump_hints_tag_block=None, jump_hints_header=None, jump_hints=None, climb_hints_tag_block=None, climb_hints_header=None, climb_hints=None, 
                     well_hints_tag_block=None, well_hints_header=None, well_hints=None, flight_hints_tag_block=None, flight_hints_header=None, flight_hints=None):
            self.point_geometry_tag_block = point_geometry_tag_block
            self.point_geometry_header = point_geometry_header
            self.point_geometry = point_geometry
            self.ray_geometry_tag_block = ray_geometry_tag_block
            self.ray_geometry_header = ray_geometry_header
            self.ray_geometry = ray_geometry
            self.line_segment_geometry_tag_block = line_segment_geometry_tag_block
            self.line_segment_geometry_header = line_segment_geometry_header
            self.line_segment_geometry = line_segment_geometry
            self.parallelogram_geometry_tag_block = parallelogram_geometry_tag_block
            self.parallelogram_geometry_header = parallelogram_geometry_header
            self.parallelogram_geometry = parallelogram_geometry
            self.polygon_geometry_tag_block = polygon_geometry_tag_block
            self.polygon_geometry_header = polygon_geometry_header
            self.polygon_geometry = polygon_geometry
            self.jump_hints_tag_block = jump_hints_tag_block
            self.jump_hints_header = jump_hints_header
            self.jump_hints = jump_hints
            self.climb_hints_tag_block = climb_hints_tag_block
            self.climb_hints_header = climb_hints_header
            self.climb_hints = climb_hints
            self.well_hints_tag_block = well_hints_tag_block
            self.well_hints_header = well_hints_header
            self.well_hints = well_hints
            self.flight_hints_tag_block = flight_hints_tag_block
            self.flight_hints_header = flight_hints_header
            self.flight_hints = flight_hints

    class PointGeometry():
        def __init__(self, point=Vector(), reference_frame=0):
            self.point = point
            self.reference_frame = reference_frame

    class RayGeometry():
        def __init__(self, point=Vector(), reference_frame=0, vector=Vector()):
            self.point = point
            self.reference_frame = reference_frame
            self.vector = vector

    class LineSegmentGeometry():
        def __init__(self, flags=0, point_0=Vector(), reference_frame_0=0, point_1=Vector(), reference_frame_1=0):
            self.flags = flags
            self.point_0 = point_0
            self.reference_frame_0 = reference_frame_0
            self.point_1 = point_1
            self.reference_frame_1 = reference_frame_1

    class ParallelogramGeometry():
        def __init__(self, flags=0, point_0=Vector(), reference_frame_0=0, point_1=Vector(), reference_frame_1=0, point_2=Vector(), reference_frame_2=0, point_3=Vector(), 
                     reference_frame_3=0):
            self.flags = flags
            self.point_0 = point_0
            self.reference_frame_0 = reference_frame_0
            self.point_1 = point_1
            self.reference_frame_1 = reference_frame_1
            self.point_2 = point_2
            self.reference_frame_2 = reference_frame_2
            self.point_3 = point_3
            self.reference_frame_3 = reference_frame_3

    class Hint():
        def __init__(self, flags=0, points_tag_block=None, points_header=None, points=None):
            self.flags = flags
            self.points_tag_block = points_tag_block
            self.points_header = points_header
            self.points = points

    class JumpHint():
        def __init__(self, flags=0, geometry_index=0, force_jump_height=0, control_flags=0):
            self.flags = flags
            self.geometry_index = geometry_index
            self.force_jump_height = force_jump_height
            self.control_flags = control_flags

    class ClimbHint():
        def __init__(self, flags=0, geometry_index=0):
            self.flags = flags
            self.geometry_index = geometry_index

    class WellPoint():
        def __init__(self, type=0, point=Vector(), reference_frame=0, sector_index=0, normal=(0.0, 0.0)):
            self.type = type
            self.point = point
            self.reference_frame = reference_frame
            self.sector_index = sector_index
            self.normal = normal

    class FlightHint():
        def __init__(self, points_tag_block=None, points_header=None, points=None):
            self.points_tag_block = points_tag_block
            self.points_header = points_header
            self.points = points

    class BackgroundSoundPalette:
        def __init__(self, name="", background_sound=None, inside_cluster_sound=None, cutoff_distance=0.0, scale_flags=0, interior_scale=0, portal_scale=0, exterior_scale=0, 
                     interpolation_speed=0.0):
            self.name = name
            self.background_sound = background_sound
            self.inside_cluster_sound = inside_cluster_sound
            self.cutoff_distance = cutoff_distance
            self.scale_flags = scale_flags
            self.interior_scale = interior_scale
            self.portal_scale = portal_scale
            self.exterior_scale = exterior_scale
            self.interpolation_speed = interpolation_speed

    class SoundEnvironmentPalette:
        def __init__(self, name="", sound_environment=None, cutoff_distance=0.0, interpolation_speed=0.0):
            self.name = name
            self.sound_environment = sound_environment
            self.cutoff_distance = cutoff_distance
            self.interpolation_speed = interpolation_speed

    class Marker:
        def __init__(self, name="", rotation=Quaternion(), position=Vector()):
            self.name = name
            self.rotation = rotation
            self.position = position

    class EnvironmentObjectPalette:
        def __init__(self, definition=None, model=None):
            self.definition = definition
            self.model = model

    class EnvironmentObject:
        def __init__(self, name="", rotation=Quaternion(), position=Vector(), palette_index=0, unique_id=0, exported_object_type="", scenario_object_name=""):
            self.name = name
            self.rotation = rotation
            self.position = position
            self.palette_index = palette_index
            self.unique_id = unique_id
            self.exported_object_type = exported_object_type
            self.scenario_object_name = scenario_object_name

    class LeafMapLeaf():
        def __init__(self, faces_tag_block=None, faces_header=None, faces=None, connection_indices_tag_block=None, connection_indices_header=None, connection_indices=None):
            self.faces_tag_block = faces_tag_block
            self.faces_header = faces_header
            self.faces = faces
            self.connection_indices_tag_block = connection_indices_tag_block
            self.connection_indices_header = connection_indices_header
            self.connection_indices = connection_indices

    class Face():
        def __init__(self, node_index=0, vertices_tag_block=None, vertices_header=None, vertices=None):
            self.node_index = node_index
            self.vertices_tag_block = vertices_tag_block
            self.vertices_header = vertices_header
            self.vertices = vertices

    class LeafMapConnection():
        def __init__(self, plane_index=0, back_leaf_index=0, front_leaf_index=0, vertices_tag_block=None, vertices_header=None, vertices=None, area=0.0):
            self.plane_index = plane_index
            self.back_leaf_index = back_leaf_index
            self.front_leaf_index = front_leaf_index
            self.vertices_tag_block = vertices_tag_block
            self.vertices_header = vertices_header
            self.vertices = vertices
            self.area = area

    class Error:
        def __init__(self, name="", report_type=0, flags=0, reports_tag_block=None, reports_header=None, reports=None):
            self.name = name
            self.report_type = report_type
            self.flags = flags
            self.reports_tag_block = reports_tag_block
            self.reports_header = reports_header
            self.reports = reports

    class Report:
        def __init__(self, type=0, flags=0, report_length=0, text="", source_filename="", source_line_number=0, vertices_tag_block=None, vectors_tag_block=None,
                     lines_tag_block=None, triangles_tag_block=None, quads_tag_block=None, comments_tag_block=None, vertices_header=None, vectors_header=None,
                     lines_header=None, triangles_header=None, quads_header=None, comments_header=None, vertices=None, vectors=None, lines=None, triangles=None,
                     quads=None, comments=None, report_key=0, node_index=0, bounds_x=(0.0, 0.0), bounds_y=(0.0, 0.0), bounds_z=(0.0, 0.0), color=(0.0, 0.0, 0.0, 0.0)):
            self.type = type
            self.flags = flags
            self.report_length = report_length
            self.text = text
            self.source_filename = source_filename
            self.source_line_number = source_line_number
            self.vertices_tag_block = vertices_tag_block
            self.vectors_tag_block = vectors_tag_block
            self.lines_tag_block = lines_tag_block
            self.triangles_tag_block = triangles_tag_block
            self.quads_tag_block = quads_tag_block
            self.comments_tag_block = comments_tag_block
            self.vertices_header = vertices_header
            self.vectors_header = vectors_header
            self.lines_header = lines_header
            self.triangles_header = triangles_header
            self.quads_header = quads_header
            self.comments_header = comments_header
            self.vertices = vertices
            self.vectors = vectors
            self.lines = lines
            self.triangles = triangles
            self.quads = quads
            self.comments = comments
            self.report_key = report_key
            self.node_index = node_index
            self.bounds_x = bounds_x
            self.bounds_y = bounds_y
            self.bounds_z = bounds_z
            self.color = color

    class ReportVertex:
        def __init__(self, position=Vector(), node_index_0=0, node_index_1=0, node_index_2=0, node_index_3=0, node_weight_0=0.0, node_weight_1=0.0, node_weight_2=0.0,
                     node_weight_3=0.0, color=(0.0, 0.0, 0.0, 0.0), screen_size=0.0):
            self.position = position
            self.node_index_0 = node_index_0
            self.node_index_1 = node_index_1
            self.node_index_2 = node_index_2
            self.node_index_3 = node_index_3
            self.node_weight_0 = node_weight_0
            self.node_weight_1 = node_weight_1
            self.node_weight_2 = node_weight_2
            self.node_weight_3 = node_weight_3
            self.color = color
            self.screen_size = screen_size

    class ReportVector:
        def __init__(self, position=Vector(), node_index_0=0, node_index_1=0, node_index_2=0, node_index_3=0, node_weight_0=0.0, node_weight_1=0.0, node_weight_2=0.0,
                     node_weight_3=0.0, color=(0.0, 0.0, 0.0, 0.0), normal=Vector(), screen_length=0.0):
            self.position = position
            self.node_index_0 = node_index_0
            self.node_index_1 = node_index_1
            self.node_index_2 = node_index_2
            self.node_index_3 = node_index_3
            self.node_weight_0 = node_weight_0
            self.node_weight_1 = node_weight_1
            self.node_weight_2 = node_weight_2
            self.node_weight_3 = node_weight_3
            self.color = color
            self.normal = normal
            self.screen_length = screen_length

    class ReportLine:
        def __init__(self, position_a=Vector(), node_index_a_0=0, node_index_a_1=0, node_index_a_2=0, node_index_a_3=0, node_weight_a_0=0.0, node_weight_a_1=0.0,
                     node_weight_a_2=0.0, node_weight_a_3=0.0, position_b=Vector(), node_index_b_0=0, node_index_b_1=0, node_index_b_2=0, node_index_b_3=0, node_weight_b_0=0.0,
                     node_weight_b_1=0.0, node_weight_b_2=0.0, node_weight_b_3=0.0, color=(0.0, 0.0, 0.0, 0.0)):
            self.position_a = position_a
            self.node_index_a_0 = node_index_a_0
            self.node_index_a_1 = node_index_a_1
            self.node_index_a_2 = node_index_a_2
            self.node_index_a_3 = node_index_a_3
            self.node_weight_a_0 = node_weight_a_0
            self.node_weight_a_1 = node_weight_a_1
            self.node_weight_a_2 = node_weight_a_2
            self.node_weight_a_3 = node_weight_a_3
            self.position_b = position_b
            self.node_index_b_0 = node_index_b_0
            self.node_index_b_1 = node_index_b_1
            self.node_index_b_2 = node_index_b_2
            self.node_index_b_3 = node_index_b_3
            self.node_weight_b_0 = node_weight_b_0
            self.node_weight_b_1 = node_weight_b_1
            self.node_weight_b_2 = node_weight_b_2
            self.node_weight_b_3 = node_weight_b_3
            self.color = color

    class ReportTriangle:
        def __init__(self, position_a=Vector(), node_index_a_0=0, node_index_a_1=0, node_index_a_2=0, node_index_a_3=0, node_weight_a_0=0.0, node_weight_a_1=0.0,
                     node_weight_a_2=0.0, node_weight_a_3=0.0, position_b=Vector(), node_index_b_0=0, node_index_b_1=0, node_index_b_2=0, node_index_b_3=0, node_weight_b_0=0.0,
                     node_weight_b_1=0.0, node_weight_b_2=0.0, node_weight_b_3=0.0, position_c=Vector(), node_index_c_0=0, node_index_c_1=0, node_index_c_2=0, node_index_c_3=0,
                     node_weight_c_0=0.0, node_weight_c_1=0.0, node_weight_c_2=0.0, node_weight_c_3=0.0, color=(0.0, 0.0, 0.0, 0.0)):
            self.position_a = position_a
            self.node_index_a_0 = node_index_a_0
            self.node_index_a_1 = node_index_a_1
            self.node_index_a_2 = node_index_a_2
            self.node_index_a_3 = node_index_a_3
            self.node_weight_a_0 = node_weight_a_0
            self.node_weight_a_1 = node_weight_a_1
            self.node_weight_a_2 = node_weight_a_2
            self.node_weight_a_3 = node_weight_a_3
            self.position_b = position_b
            self.node_index_b_0 = node_index_b_0
            self.node_index_b_1 = node_index_b_1
            self.node_index_b_2 = node_index_b_2
            self.node_index_b_3 = node_index_b_3
            self.node_weight_b_0 = node_weight_b_0
            self.node_weight_b_1 = node_weight_b_1
            self.node_weight_b_2 = node_weight_b_2
            self.node_weight_b_3 = node_weight_b_3
            self.position_c = position_c
            self.node_index_c_0 = node_index_c_0
            self.node_index_c_1 = node_index_c_1
            self.node_index_c_2 = node_index_c_2
            self.node_index_c_3 = node_index_c_3
            self.node_weight_c_0 = node_weight_c_0
            self.node_weight_c_1 = node_weight_c_1
            self.node_weight_c_2 = node_weight_c_2
            self.node_weight_c_3 = node_weight_c_3
            self.color = color

    class ReportQuad:
        def __init__(self, position_a=Vector(), node_index_a_0=0, node_index_a_1=0, node_index_a_2=0, node_index_a_3=0, node_weight_a_0=0.0, node_weight_a_1=0.0,
                     node_weight_a_2=0.0, node_weight_a_3=0.0, position_b=Vector(), node_index_b_0=0, node_index_b_1=0, node_index_b_2=0, node_index_b_3=0, node_weight_b_0=0.0,
                     node_weight_b_1=0.0, node_weight_b_2=0.0, node_weight_b_3=0.0, position_c=Vector(), node_index_c_0=0, node_index_c_1=0, node_index_c_2=0, node_index_c_3=0,
                     node_weight_c_0=0.0, node_weight_c_1=0.0, node_weight_c_2=0.0, node_weight_c_3=0.0, position_d=Vector(), node_index_d_0=0, node_index_d_1=0,
                     node_index_d_2=0, node_index_d_3=0, node_weight_d_0=0.0, node_weight_d_1=0.0, node_weight_d_2=0.0, node_weight_d_3=0.0, color=(0.0, 0.0, 0.0, 0.0)):
            self.position_a = position_a
            self.node_index_a_0 = node_index_a_0
            self.node_index_a_1 = node_index_a_1
            self.node_index_a_2 = node_index_a_2
            self.node_index_a_3 = node_index_a_3
            self.node_weight_a_0 = node_weight_a_0
            self.node_weight_a_1 = node_weight_a_1
            self.node_weight_a_2 = node_weight_a_2
            self.node_weight_a_3 = node_weight_a_3
            self.position_b = position_b
            self.node_index_b_0 = node_index_b_0
            self.node_index_b_1 = node_index_b_1
            self.node_index_b_2 = node_index_b_2
            self.node_index_b_3 = node_index_b_3
            self.node_weight_b_0 = node_weight_b_0
            self.node_weight_b_1 = node_weight_b_1
            self.node_weight_b_2 = node_weight_b_2
            self.node_weight_b_3 = node_weight_b_3
            self.position_c = position_c
            self.node_index_c_0 = node_index_c_0
            self.node_index_c_1 = node_index_c_1
            self.node_index_c_2 = node_index_c_2
            self.node_index_c_3 = node_index_c_3
            self.node_weight_c_0 = node_weight_c_0
            self.node_weight_c_1 = node_weight_c_1
            self.node_weight_c_2 = node_weight_c_2
            self.node_weight_c_3 = node_weight_c_3
            self.position_d = position_d
            self.node_index_d_0 = node_index_d_0
            self.node_index_d_1 = node_index_d_1
            self.node_index_d_2 = node_index_d_2
            self.node_index_d_3 = node_index_d_3
            self.node_weight_d_0 = node_weight_d_0
            self.node_weight_d_1 = node_weight_d_1
            self.node_weight_d_2 = node_weight_d_2
            self.node_weight_d_3 = node_weight_d_3
            self.color = color

    class ReportComment:
        def __init__(self, text_length=0, text="", position=Vector(), node_index_0=0, node_index_1=0, node_index_2=0, node_index_3=0, node_weight_0=0.0, node_weight_1=0.0,
                     node_weight_2=0.0, node_weight_3=0.0, color=(0.0, 0.0, 0.0, 0.0)):
            self.text_length = text_length
            self.text = text
            self.position = position
            self.node_index_0 = node_index_0
            self.node_index_1 = node_index_1
            self.node_index_2 = node_index_2
            self.node_index_3 = node_index_3
            self.node_weight_0 = node_weight_0
            self.node_weight_1 = node_weight_1
            self.node_weight_2 = node_weight_2
            self.node_weight_3 = node_weight_3
            self.color = color

    class PrecomputedLighting:
        def __init__(self, index=0, light_type=0, attachment_index=0, object_type=0, projection_count=0, cluster_count=0, volume_count=0, projections_data=None, 
                     visiblity_clusters_data=None, cluster_remap_table_data=None, visibility_volumes_data=None, projections=None, visiblity_clusters=None, cluster_remap_table=None, 
                     visibility_volumes=None, svis_header=None):
            self.index = index
            self.light_type = light_type
            self.attachment_index = attachment_index
            self.object_type = object_type
            self.projection_count = projection_count
            self.cluster_count = cluster_count
            self.volume_count = volume_count
            self.projections_data = projections_data
            self.visiblity_clusters_data = visiblity_clusters_data
            self.cluster_remap_table_data = cluster_remap_table_data
            self.visibility_volumes_data = visibility_volumes_data
            self.projections = projections
            self.visiblity_clusters = visiblity_clusters
            self.cluster_remap_table = cluster_remap_table
            self.visibility_volumes = visibility_volumes
            self.svis_header = svis_header

    class InstanceGeometryDefinition(Section):
        def __init__(self, render_data_tag_block=None, render_data_header=None, render_data=None, index_reorder_table_tag_block=None, index_reorder_table_header=None, 
                     index_reorder_table=None, checksum=None, bounding_sphere_center=Vector(), bounding_sphere_radius=0.0, bsp3d_nodes_tag_block=None, bsp3d_nodes_header=None, 
                     bsp3d_nodes=None, planes_tag_block=None, planes_header=None, planes=None, leaves_tag_block=None, leaves_header=None, leaves=None, bsp2d_references_tag_block=None, 
                     bsp2d_references_header=None, bsp2d_references=None, bsp2d_nodes_tag_block=None, bsp2d_nodes_header=None, bsp2d_nodes=None, surfaces_tag_block=None, 
                     surfaces_header=None, surfaces=None, edges_tag_block=None, edges_header=None, edges=None, vertices_tag_block=None, vertices_header=None, vertices=None, 
                     bsp_physics_tag_block=None, bsp_physics_header=None, bsp_physics=None, render_leaves_tag_block=None, render_leaves_header=None, render_leaves=None, 
                     surface_references_tag_block=None, surface_references_header=None, surface_references=None, igri_header=None, sinf_header=None, cbsp_header=None):
            super().__init__()
            self.render_data_tag_block = render_data_tag_block
            self.render_data_header = render_data_header
            self.render_data = render_data
            self.index_reorder_table_tag_block = index_reorder_table_tag_block
            self.index_reorder_table_header = index_reorder_table_header
            self.index_reorder_table = index_reorder_table
            self.checksum = checksum
            self.bounding_sphere_center = bounding_sphere_center
            self.bounding_sphere_radius = bounding_sphere_radius
            self.bsp3d_nodes_tag_block = bsp3d_nodes_tag_block
            self.bsp3d_nodes_header = bsp3d_nodes_header
            self.bsp3d_nodes = bsp3d_nodes
            self.planes_tag_block = planes_tag_block
            self.planes_header = planes_header
            self.planes = planes
            self.leaves_tag_block = leaves_tag_block
            self.leaves_header = leaves_header
            self.leaves = leaves
            self.bsp2d_references_tag_block = bsp2d_references_tag_block
            self.bsp2d_references_header = bsp2d_references_header
            self.bsp2d_references = bsp2d_references
            self.bsp2d_nodes_tag_block = bsp2d_nodes_tag_block
            self.bsp2d_nodes_header = bsp2d_nodes_header
            self.bsp2d_nodes = bsp2d_nodes
            self.surfaces_tag_block = surfaces_tag_block
            self.surfaces_header = surfaces_header
            self.surfaces = surfaces
            self.edges_tag_block = edges_tag_block
            self.edges_header = edges_header
            self.edges = edges
            self.vertices_tag_block = vertices_tag_block
            self.vertices_header = vertices_header
            self.vertices = vertices
            self.bsp_physics_tag_block = bsp_physics_tag_block
            self.bsp_physics_header = bsp_physics_header
            self.bsp_physics = bsp_physics
            self.render_leaves_tag_block = render_leaves_tag_block
            self.render_leaves_header = render_leaves_header
            self.render_leaves = render_leaves
            self.surface_references_tag_block = surface_references_tag_block
            self.surface_references_header = surface_references_header
            self.surface_references = surface_references
            self.igri_header = igri_header
            self.sinf_header = sinf_header
            self.cbsp_header = cbsp_header

    class BSPPhysics:
        def __init__(self, size_0=0, count_0=0, size_1=0, count_1=0, size_2=0, count_2=0, mopp_code_tag_data=None, mopp_code_data=None):
            self.size_0 = size_0
            self.count_0 = count_0
            self.size_1 = size_1
            self.count_1 = count_1
            self.size_2 = size_2
            self.count_2 = count_2
            self.mopp_code_tag_data = mopp_code_tag_data
            self.mopp_code_data = mopp_code_data

    class RenderLeaf:
        def __init__(self, cluster=0, surface_reference_count=0, first_surface_reference_index=0):
            self.cluster = cluster
            self.surface_reference_count = surface_reference_count
            self.first_surface_reference_index = first_surface_reference_index

    class SurfaceReference:
        def __init__(self, strip_index=0, lightmap_triangle_index=0, bsp_node_index=0):
            self.strip_index = strip_index
            self.lightmap_triangle_index = lightmap_triangle_index
            self.bsp_node_index = bsp_node_index

    class InstancedGeometryInstance:
        def __init__(self, scale=0.0, forward=Vector(), left=Vector(), up=Vector(), position=Vector(), instance_definition=0, flags=0, checksum=0, name="", name_length=0, 
                     pathfinding_policy=0, lightmapping_policy=0):
            self.scale = scale
            self.forward = forward
            self.left = left
            self.up = up
            self.position = position
            self.instance_definition = instance_definition
            self.flags = flags
            self.checksum = checksum
            self.name = name
            self.name_length = name_length
            self.pathfinding_policy = pathfinding_policy
            self.lightmapping_policy = lightmapping_policy
