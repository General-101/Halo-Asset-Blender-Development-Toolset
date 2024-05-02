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

from mathutils import Vector, Euler
from enum import Flag, Enum, auto

class StructureBSPFlags(Flag):
    default_sky_enabled = auto()

class ObjectFlags(Flag):
    not_automatically = auto()
    unused_0 = auto()
    unused_1 = auto()
    unused_2 = auto()
    lock_type_to_env_object = auto()
    lock_transform_to_env_object = auto()
    never_placed = auto()
    lock_name_to_env_object = auto()
    create_at_rest = auto()

class TransformFlags(Flag):
    mirrored = auto()

class ObjectTypeFlags(Enum):
    biped = 0
    vehicle = auto()
    weapon = auto()
    equipment = auto()
    garbage = auto()
    projectile = auto()
    scenery = auto()
    machine = auto()
    control = auto()
    light_fixture = auto()
    sound_scenery = auto()
    crate = auto()
    creature = auto()

class ObjectSourceFlags(Enum):
    structure = 0
    editor = auto()
    dynamic = auto()
    legacy = auto()

class ObjectBSPPolicyFlags(Enum):
    default = 0
    always_placed = auto()
    manual_bsp_placement = auto()

class ObjectColorChangeFlags(Flag):
    primary = auto()
    secondary = auto()
    tertiary = auto()
    quaternary = auto()

class PathfindingPolicyEnum(Enum):
    tag_default = 0
    pathfinding_dynamic = auto()
    pathfinding_cut_out = auto()
    pathfinding_static = auto()
    pathfinding_none = auto()

class LightmappingPolicyEnum(Enum):
    tag_default = 0
    dynamic = auto()
    per_vertex = auto()

class ObjectGametypeEnum(Flag):
    ctf = auto()
    slayer = auto()
    oddball = auto()
    king = auto()
    juggernaut = auto()
    territories = auto()
    assault = auto()
    medic = auto()
    vip = auto()
    infection = auto()
    headhunter = auto()

class SceneryResourceAsset():
    def __init__(self):
        self.header = None
        self.resource_body_header = None
        self.resource_body = None
        self.object_names_header = None
        self.object_names = None
        self.environment_objects_header = None
        self.environment_objects = None
        self.structure_bsps_header = None
        self.structure_bsps = None
        self.scenery_palette_header = None
        self.scenery_palette = None
        self.scenery_header = None
        self.scenery = None
        self.crate_palette_header = None
        self.crate_palette = None
        self.crates_header = None
        self.crates = None
        self.editor_folders_header = None
        self.editor_folders = None

    class ResourceBody:
        def __init__(self, object_names_tag_block=None, environment_objects_tag_block=None, structure_bsps_tag_block=None, scenery_palette_tag_block=None, scenery_tag_block=None,
                     next_scenery_object_id_salt=0, crate_palette_tag_block=None, crates_tag_block=None, next_block_object_id_salt=0, editor_folders_tag_block=None):
            self.object_names_tag_block = object_names_tag_block
            self.environment_objects_tag_block = environment_objects_tag_block
            self.structure_bsps_tag_block = structure_bsps_tag_block
            self.scenery_palette_tag_block = scenery_palette_tag_block
            self.scenery_tag_block = scenery_tag_block
            self.next_scenery_object_id_salt = next_scenery_object_id_salt
            self.crate_palette_tag_block = crate_palette_tag_block
            self.crates_tag_block = crates_tag_block
            self.next_block_object_id_salt = next_block_object_id_salt
            self.editor_folders_tag_block = editor_folders_tag_block

    class ObjectName:
        def __init__(self, name="", object_type=0, placement_index=0):
            self.name = name
            self.object_type = object_type
            self.placement_index = placement_index

    class EnvironmentObject:
        def __init__(self, bsp_index=0, runtime_object_type=0, unique_id=0, object_definition_tag=0, environment_object=0):
            self.bsp_index = bsp_index
            self.runtime_object_type = runtime_object_type
            self.unique_id = unique_id
            self.object_definition_tag = object_definition_tag
            self.environment_object = environment_object

    class StructureBSP():
        def __init__(self, structure_bsp=None, structure_lightmap=None, unused_radiance_estimated_search_distance=0.0, unused_luminels_per_world_unit=0.0,
                     unused_output_white_reference=0.0, flags=0, default_sky=0):
            self.structure_bsp = structure_bsp
            self.structure_lightmap = structure_lightmap
            self.unused_radiance_estimated_search_distance = unused_radiance_estimated_search_distance
            self.unused_luminels_per_world_unit = unused_luminels_per_world_unit
            self.unused_output_white_reference = unused_output_white_reference
            self.flags = flags
            self.default_sky = default_sky

    class Object:
        def __init__(self, palette_index=0, name_index=0, placement_flags=0, position=Vector(), rotation=Euler(), scale=0.0, transform_flags=0, manual_bsp_flags=0, unique_id=0,
                     origin_bsp_index=0, object_type=0, source=0, bsp_policy=0, editor_folder_index=0):
            self.palette_index = palette_index
            self.name_index = name_index
            self.placement_flags = placement_flags
            self.position = position
            self.rotation = rotation
            self.scale = scale
            self.transform_flags = transform_flags
            self.manual_bsp_flags = manual_bsp_flags
            self.unique_id = unique_id
            self.origin_bsp_index = origin_bsp_index
            self.object_type = object_type
            self.source = source
            self.bsp_policy = bsp_policy
            self.editor_folder_index = editor_folder_index

    class Scenery(Object):
        def __init__(self, sobj_header=None, obj0_header=None, sper_header=None, sct3_header=None, variant_name="", variant_name_length=0, active_change_colors=0,
                     primary_color_BGRA=(0, 0, 0, 255), secondary_color_BGRA=(0, 0, 0, 255), tertiary_color_BGRA=(0, 0, 0, 255),
                     quaternary_color_BGRA=(0, 0, 0, 255), pathfinding_policy=0, lightmap_policy=0, pathfinding_references_header=None, pathfinding_references_tag_block=None,
                     valid_multiplayer_games=0, pathfinding_references=None):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.sper_header = sper_header
            self.sct3_header = sct3_header
            self.variant_name = variant_name
            self.variant_name_length = variant_name_length
            self.active_change_colors = active_change_colors
            self.primary_color_BGRA = primary_color_BGRA
            self.secondary_color_BGRA = secondary_color_BGRA
            self.tertiary_color_BGRA = tertiary_color_BGRA
            self.quaternary_color_BGRA = quaternary_color_BGRA
            self.pathfinding_policy = pathfinding_policy
            self.lightmap_policy = lightmap_policy
            self.pathfinding_references_header = pathfinding_references_header
            self.pathfinding_references_tag_block = pathfinding_references_tag_block
            self.valid_multiplayer_games = valid_multiplayer_games
            self.pathfinding_references = pathfinding_references

    class PathfindingReference:
        def __init__(self, bsp_index=0, pathfinding_object_index=0):
            self.bsp_index = bsp_index
            self.pathfinding_object_index = pathfinding_object_index

    class Crate(Object):
        def __init__(self, sobj_header=None, obj0_header=None, sper_header=None, variant_name="", variant_name_length=0, active_change_colors=0,
                     primary_color_BGRA=(0, 0, 0, 255), secondary_color_BGRA=(0, 0, 0, 255), tertiary_color_BGRA=(0, 0, 0, 255),
                     quaternary_color_BGRA=(0, 0, 0, 255)):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.sper_header = sper_header
            self.variant_name = variant_name
            self.variant_name_length = variant_name_length
            self.active_change_colors = active_change_colors
            self.primary_color_BGRA = primary_color_BGRA
            self.secondary_color_BGRA = secondary_color_BGRA
            self.tertiary_color_BGRA = tertiary_color_BGRA
            self.quaternary_color_BGRA = quaternary_color_BGRA

    class EditorFolder:
        def __init__(self, parent_folder=0, name=""):
            self.parent_folder = parent_folder
            self.name = name
