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

from enum import Flag, auto
from mathutils import Vector, Quaternion

class LeafFlags(Flag):
    contains_double_sided_surfaces = auto()

class SurfaceFlags(Flag):
    two_sided = auto()
    invisible = auto()
    climbable = auto()
    breakable = auto()

class MaterialFlags(Flag):
    coplanar = auto()
    fog_plane = auto()

class ClusterPortalFlags(Flag):
    ai_cant_hear_through_this = auto()

class LevelAsset():
    def __init__(self, header=None, collision_materials=None, collision_bsps=None, nodes=None, leaves=None, leaf_surfaces=None, surfaces=None, lightmaps=None, 
                 lens_flares=None, lens_flare_markers=None, clusters=None, cluster_data=None, cluster_portals=None, breakable_surfaces=None, fog_planes=None, 
                 fog_regions=None, fog_palettes=None, weather_palettes=None, weather_polyhedras=None, pathfinding_surfaces=None, pathfinding_edges=None, 
                 background_sounds_palettes=None, sound_environments_palettes=None, markers=None, detail_objects=None, leaf_map_leaves=None, leaf_map_portals=None, 
                 lightmap_bitmaps_tag_ref=None, vehicle_floor=0.0, vehicle_ceiling=0.0, default_ambient_color=(0.0, 0.0, 0.0, 0.0), 
                 default_distant_light_0_color=(0.0, 0.0, 0.0, 0.0), default_distant_light_0_direction=Vector(), default_distant_light_1_color=(0.0, 0.0, 0.0, 0.0), 
                 default_distant_light_1_direction=Vector(), default_reflection_tint=(0.0, 0.0, 0.0, 0.0), default_shadow_vector=Vector(), 
                 default_shadow_color=(0.0, 0.0, 0.0, 0.0), collision_materials_tag_block=None, collision_bsps_tag_block=None, nodes_tag_block=None, 
                 world_bounds_x=(0.0, 0.0), world_bounds_y=(0.0, 0.0), world_bounds_z=(0.0, 0.0), leaves_tag_block=None, leaf_surfaces_tag_block=None, 
                 surfaces_tag_block=None, lightmaps_tag_block=None, lens_flares_tag_block=None, lens_flare_markers_tag_block=None, clusters_tag_block=None, 
                 cluster_data_raw_data=None, cluster_portals_tag_block=None, breakable_surfaces_tag_block=None, fog_planes_tag_block=None, fog_regions_tag_block=None, 
                 fog_palettes_tag_block=None, weather_palettes_tag_block=None, weather_polyhedras_tag_block=None, pathfinding_surfaces_tag_block=None, 
                 pathfinding_edges_tag_block=None, background_sounds_palette_tag_block=None, sound_environments_palette_tag_block=None, sound_pas_raw_data=None, 
                 unknown_0=0, markers_tag_block=None, detail_objects_tag_block=None, runtime_decals_tag_block=None, leaf_map_leaves_tag_block=None, 
                 leaf_map_portals_tag_block=None):
        self.header = header
        self.collision_materials = collision_materials
        self.collision_bsps = collision_bsps
        self.nodes = nodes
        self.leaves = leaves
        self.leaf_surfaces = leaf_surfaces
        self.surfaces = surfaces
        self.lightmaps = lightmaps
        self.lens_flares = lens_flares
        self.lens_flare_markers = lens_flare_markers
        self.clusters = clusters
        self.cluster_data = cluster_data
        self.cluster_portals = cluster_portals
        self.breakable_surfaces = breakable_surfaces
        self.fog_planes = fog_planes
        self.fog_regions = fog_regions
        self.fog_palettes = fog_palettes
        self.weather_palettes = weather_palettes
        self.weather_polyhedras = weather_polyhedras
        self.pathfinding_surfaces = pathfinding_surfaces
        self.pathfinding_edges = pathfinding_edges
        self.background_sounds_palettes = background_sounds_palettes
        self.sound_environments_palettes = sound_environments_palettes
        self.markers = markers
        self.detail_objects = detail_objects
        self.leaf_map_leaves = leaf_map_leaves
        self.leaf_map_portals = leaf_map_portals
        self.lightmap_bitmaps_tag_ref = lightmap_bitmaps_tag_ref
        self.vehicle_floor = vehicle_floor
        self.vehicle_ceiling = vehicle_ceiling
        self.default_ambient_color = default_ambient_color
        self.default_distant_light_0_color = default_distant_light_0_color
        self.default_distant_light_0_direction = default_distant_light_0_direction
        self.default_distant_light_1_color = default_distant_light_1_color
        self.default_distant_light_1_direction = default_distant_light_1_direction
        self.default_reflection_tint = default_reflection_tint
        self.default_shadow_vector = default_shadow_vector
        self.default_shadow_color = default_shadow_color
        self.collision_materials_tag_block = collision_materials_tag_block
        self.collision_bsps_tag_block = collision_bsps_tag_block
        self.nodes_tag_block = nodes_tag_block
        self.world_bounds_x = world_bounds_x
        self.world_bounds_y = world_bounds_y
        self.world_bounds_z = world_bounds_z
        self.leaves_tag_block = leaves_tag_block
        self.leaf_surfaces_tag_block = leaf_surfaces_tag_block
        self.surfaces_tag_block = surfaces_tag_block
        self.lightmaps_tag_block = lightmaps_tag_block
        self.lens_flares_tag_block = lens_flares_tag_block
        self.lens_flare_markers_tag_block = lens_flare_markers_tag_block
        self.clusters_tag_block = clusters_tag_block
        self.cluster_data_raw_data = cluster_data_raw_data
        self.cluster_portals_tag_block = cluster_portals_tag_block
        self.breakable_surfaces_tag_block = breakable_surfaces_tag_block
        self.fog_planes_tag_block = fog_planes_tag_block
        self.fog_regions_tag_block = fog_regions_tag_block
        self.fog_palettes_tag_block = fog_palettes_tag_block
        self.weather_palettes_tag_block = weather_palettes_tag_block
        self.weather_polyhedras_tag_block = weather_polyhedras_tag_block
        self.pathfinding_surfaces_tag_block = pathfinding_surfaces_tag_block
        self.pathfinding_edges_tag_block = pathfinding_edges_tag_block
        self.background_sounds_palette_tag_block = background_sounds_palette_tag_block
        self.sound_environments_palette_tag_block = sound_environments_palette_tag_block
        self.sound_pas_raw_data = sound_pas_raw_data
        self.unknown_0 = unknown_0
        self.markers_tag_block = markers_tag_block
        self.detail_objects_tag_block = detail_objects_tag_block
        self.runtime_decals_tag_block = runtime_decals_tag_block
        self.leaf_map_leaves_tag_block = leaf_map_leaves_tag_block
        self.leaf_map_portals_tag_block = leaf_map_portals_tag_block

    class CollisionMaterial:
        def __init__(self, shader_tag_ref=None, unknown_0=0):
            self.shader_tag_ref = shader_tag_ref
            self.unknown_0 = unknown_0

    class CollisionBSP:
        def __init__(self, bsp3d_nodes_tag_block=None, planes_tag_block=None, leaves_tag_block=None, bsp2d_references_tag_block=None, bsp2d_nodes_tag_block=None,
                     surfaces_tag_block=None, edges_tag_block=None, vertices_tag_block=None, bsp3d_nodes=None, planes=None, leaves=None, bsp2d_references=None, bsp2d_nodes=None,
                     surfaces=None, edges=None, vertices=None):
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

    class Nodes:
        def __init__(self, unknown_0=0, unknown_1=0, unknown_2=0, unknown_3=0, unknown_4=0, unknown_5=0):
            self.unknown_0 = unknown_0
            self.unknown_1 = unknown_1
            self.unknown_2 = unknown_2
            self.unknown_3 = unknown_3
            self.unknown_4 = unknown_4
            self.unknown_5 = unknown_5

    class ClusterLeaf:
        def __init__(self, unknown_0=0, unknown_1=0, unknown_2=0, unknown_3=0, cluster=0, surface_reference_count=0, surface_reference=0):
            self.unknown_0 = unknown_0
            self.unknown_1 = unknown_1
            self.unknown_2 = unknown_2
            self.unknown_3 = unknown_3
            self.cluster = cluster
            self.surface_reference_count = surface_reference_count
            self.surface_reference = surface_reference

    class LeafSurface:
        def __init__(self, surface=0, node=0):
            self.surface = surface
            self.node = node

    class ClusterSurface:
        def __init__(self, v0=0, v1=0, v2=0):
            self.v0 = v0
            self.v1 = v1
            self.v2 = v2

    class Lightmaps:
        def __init__(self, bitmap_index=0, materials_tag_block=None, materials=None):
            self.bitmap_index = bitmap_index
            self.materials_tag_block = materials_tag_block
            self.materials = materials

    class Material:
        def __init__(self, shader_tag_ref=None, shader_permutation=0, flags=0, surfaces=0, surface_count=0, centroid=Vector(), ambient_color=(0.0, 0.0, 0.0, 1.0),
                     distant_light_count=0, distant_light_0_color=(0.0, 0.0, 0.0, 1.0), distant_light_0_direction=Vector(), distant_light_1_color=(0.0, 0.0, 0.0, 1.0),
                     distant_light_1_direction=Vector(), reflection_tint=(0.0, 0.0, 0.0, 1.0), shadow_vector=Vector(), shadow_color=(0.0, 0.0, 0.0, 1.0),
                     plane=None, breakable_surface=0, vertices_count=0, vertices_offset=0, unknown_cache_offset0=0, vertices_cache_offset=0,
                     vertex_type=0, lightmap_vertices_count=0, lightmap_vertices_offset=0, unknown_cache_offset1=0, lightmap_vertices_cache_offset=0,
                     uncompressed_vertices_raw_data=None, compressed_vertices_raw_data=None, uncompressed_render_vertices=None, compressed_render_vertices=None,
                     uncompressed_lightmap_vertices=None, compressed_lightmap_vertices=None):
            self.shader_tag_ref = shader_tag_ref
            self.shader_permutation = shader_permutation
            self.flags = flags
            self.surfaces = surfaces
            self.surface_count = surface_count
            self.centroid = centroid
            self.ambient_color = ambient_color
            self.distant_light_count = distant_light_count
            self.distant_light_0_color = distant_light_0_color
            self.distant_light_0_direction = distant_light_0_direction
            self.distant_light_1_color = distant_light_1_color
            self.distant_light_1_direction = distant_light_1_direction
            self.reflection_tint = reflection_tint
            self.shadow_vector = shadow_vector
            self.shadow_color = shadow_color
            self.plane = plane
            self.breakable_surface = breakable_surface
            self.vertices_count = vertices_count
            self.vertices_offset = vertices_offset
            self.unknown_cache_offset0 = unknown_cache_offset0
            self.vertices_cache_offset = vertices_cache_offset
            self.vertex_type = vertex_type
            self.lightmap_vertices_count = lightmap_vertices_count
            self.lightmap_vertices_offset = lightmap_vertices_offset
            self.unknown_cache_offset1 = unknown_cache_offset1
            self.lightmap_vertices_cache_offset = lightmap_vertices_cache_offset
            self.uncompressed_vertices_raw_data = uncompressed_vertices_raw_data
            self.compressed_vertices_raw_data = compressed_vertices_raw_data
            self.uncompressed_render_vertices = uncompressed_render_vertices
            self.compressed_render_vertices = compressed_render_vertices
            self.uncompressed_lightmap_vertices = uncompressed_lightmap_vertices
            self.compressed_lightmap_vertices = compressed_lightmap_vertices

    class Vertices:
        def __init__(self, translation=None, normal=None, binormal=None, tangent=None, UV=None, node_0_index=0, node_1_index=0, node_0_weight=0.0, node_1_weight=0.0):
            self.translation = translation
            self.normal = normal
            self.binormal = binormal
            self.tangent = tangent
            self.UV = UV
            self.node_0_index = node_0_index
            self.node_1_index = node_1_index
            self.node_0_weight = node_0_weight
            self.node_1_weight = node_1_weight

    class LensFlareMarker:
        def __init__(self, position=Vector(), direction_i_compenent=0, direction_j_compenent=0, direction_k_compenent=0, lens_flare_index=0):
            self.position = position
            self.direction_i_compenent = direction_i_compenent
            self.direction_j_compenent = direction_j_compenent
            self.direction_k_compenent = direction_k_compenent
            self.lens_flare_index = lens_flare_index

    class Cluster:
        def __init__(self, sky=0, fog=0, background_sound=0, sound_environment=0, weather=0, transition_structure_bsp=0, first_decal_index=0, decal_count=0,
                     predicted_resources_tag_block=None, subclusters_tag_block=None, first_lens_flare_marker_index=0, lens_flare_marker_count=0, surface_indices_tag_block=None,
                     mirrors_tag_block=None, portals_tag_block=None, predicted_resources=None, subclusters=None, surface_indices=None, mirrors=None, portals=None):
            self.sky = sky
            self.fog = fog
            self.background_sound = background_sound
            self.sound_environment = sound_environment
            self.weather = weather
            self.transition_structure_bsp = transition_structure_bsp
            self.first_decal_index = first_decal_index
            self.decal_count = decal_count
            self.predicted_resources_tag_block = predicted_resources_tag_block
            self.subclusters_tag_block = subclusters_tag_block
            self.first_lens_flare_marker_index = first_lens_flare_marker_index
            self.lens_flare_marker_count = lens_flare_marker_count
            self.surface_indices_tag_block = surface_indices_tag_block
            self.mirrors_tag_block = mirrors_tag_block
            self.portals_tag_block = portals_tag_block
            self.predicted_resources = predicted_resources
            self.subclusters = subclusters
            self.surface_indices = surface_indices
            self.mirrors = mirrors
            self.portals = portals

    class PredictedResource:
        def __init__(self, type=0, resource_index=0, tag_index=0):
            self.type = type
            self.resource_index = resource_index
            self.tag_index = tag_index

    class Subcluster:
        def __init__(self, world_bounds_x=(0.0, 0.0), world_bounds_y=(0.0, 0.0), world_bounds_z=(0.0, 0.0), surface_indices_tag_block=None, surface_indices=None):
            self.world_bounds_x = world_bounds_x
            self.world_bounds_y = world_bounds_y
            self.world_bounds_z = world_bounds_z
            self.surface_indices_tag_block = surface_indices_tag_block
            self.surface_indices = surface_indices

    class Mirror:
        def __init__(self, plane_translation=Vector(), plane_distance=0.0, shader_tag_ref=None, vertices_tag_block=None, vertices=None):
            self.plane_translation = plane_translation
            self.plane_distance = plane_distance
            self.shader_tag_ref = shader_tag_ref
            self.vertices_tag_block = vertices_tag_block
            self.vertices = vertices

    class ClusterData:
        def __init__(self, unknown_0=0, unknown_1=0, unknown_2=0, unknown_3=0):
            self.unknown_0 = unknown_0
            self.unknown_1 = unknown_1
            self.unknown_2 = unknown_2
            self.unknown_3 = unknown_3

    class ClusterPortal:
        def __init__(self, front_cluster=0, back_cluster=0, plane_index=0, centroid=Vector(), bounding_radius=0.0, flags=0, vertices_tag_block=None, vertices=None):
            self.front_cluster = front_cluster
            self.back_cluster = back_cluster
            self.plane_index = plane_index
            self.centroid = centroid
            self.bounding_radius = bounding_radius
            self.flags = flags
            self.vertices_tag_block = vertices_tag_block
            self.vertices = vertices

    class BreakableSurfaces:
        def __init__(self, centroid=Vector(), radius=0.0, collision_surface_index=0):
            self.centroid = centroid
            self.radius = radius
            self.collision_surface_index = collision_surface_index

    class FogPlane:
        def __init__(self, front_region=0, material_type=0, plane_translation=Vector(), plane_distance=0.0, vertices_tag_block=None, vertices=None):
            self.front_region = front_region
            self.material_type = material_type
            self.plane_translation = plane_translation
            self.plane_distance = plane_distance
            self.vertices_tag_block = vertices_tag_block
            self.vertices = vertices

    class FogRegion:
        def __init__(self, fog_palette=0, weather_palette=0):
            self.fog_palette = fog_palette
            self.weather_palette = weather_palette

    class FogPalette:
        def __init__(self, name="", fog_tag_ref=None, fog_scale_function=""):
            self.name = name
            self.fog_tag_ref = fog_tag_ref
            self.fog_scale_function = fog_scale_function

    class WeatherPalette:
        def __init__(self, name="", particle_system_tag_ref=None, particle_system_scale_function="", wind_tag_ref=None, wind_direction=Vector(), wind_magnitude=0.0,
                     wind_scale_function=""):
            self.name = name
            self.particle_system_tag_ref = particle_system_tag_ref
            self.particle_system_scale_function = particle_system_scale_function
            self.wind_tag_ref = wind_tag_ref
            self.wind_direction = wind_direction
            self.wind_magnitude = wind_magnitude
            self.wind_scale_function = wind_scale_function

    class WeatherPolyhedras:
        def __init__(self, bounding_sphere_center=Vector(), bounding_sphere_radius=0.0, planes_tag_block=None, planes=None):
            self.bounding_sphere_center = bounding_sphere_center
            self.bounding_sphere_radius = bounding_sphere_radius
            self.planes_tag_block = planes_tag_block
            self.planes = planes

    class BackgroundSoundsPalette:
        def __init__(self, name="", background_sound_tag_ref=None, scale_function=""):
            self.name = name
            self.background_sound_tag_ref = background_sound_tag_ref
            self.scale_function = scale_function

    class SoundEnvironmentsPalette:
        def __init__(self, name="", sound_environment_tag_ref=None):
            self.name = name
            self.sound_environment_tag_ref = sound_environment_tag_ref

    class Markers:
        def __init__(self, name="", rotation=Quaternion(), translation=Vector()):
            self.name = name
            self.rotation = rotation
            self.translation = translation

    class DetailObject:
        def __init__(self, cells_tag_block=None, instances_tag_block=None, counts_tag_block=None, z_reference_vectors_tag_block=None, flags=0,
                     cells=None, instances=None, counts=None, z_reference_vectors=None):
            self.cells_tag_block = cells_tag_block
            self.instances_tag_block = instances_tag_block
            self.counts_tag_block = counts_tag_block
            self.z_reference_vectors_tag_block = z_reference_vectors_tag_block
            self.flags = flags
            self.cells = cells
            self.instances = instances
            self.counts = counts
            self.z_reference_vectors = z_reference_vectors

    class Cell:
        def __init__(self, cell_translation=Vector(), offset_z=0, valid_layers_flag=0, start_index=0, count_index=0):
            self.cell_translation = cell_translation
            self.offset_z = offset_z
            self.valid_layers_flag = valid_layers_flag
            self.start_index = start_index
            self.count_index = count_index

    class Instance:
        def __init__(self, position=Vector(), data=0, color=0):
            self.position = position
            self.data = data
            self.color = color

    class ZReferenceVector:
        def __init__(self, unknown_0=Vector(), unknown_1=0.0):
            self.unknown_0 = unknown_0
            self.unknown_1 = unknown_1

    class LeafMapLeaf:
        def __init__(self, faces_tag_block=None, portal_indices_tag_block=None, faces=None, portal_indices=None):
            self.faces_tag_block = faces_tag_block
            self.portal_indices_tag_block = portal_indices_tag_block
            self.faces = faces
            self.portal_indices = portal_indices

    class Face:
        def __init__(self, node_index=0, vertices_tag_block=None, vertices=None):
            self.node_index = node_index
            self.vertices_tag_block = vertices_tag_block
            self.vertices = vertices

    class LeafMapPortal:
        def __init__(self, plane_index=0, back_leaf_index=0, front_leaf_index=0, vertices_tag_block=None, vertices=None):
            self.plane_index = plane_index
            self.back_leaf_index = back_leaf_index
            self.front_leaf_index = front_leaf_index
            self.vertices_tag_block = vertices_tag_block
            self.vertices = vertices
