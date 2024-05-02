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
from .format import (
        SceneryResourceAsset,
        StructureBSPFlags,
        ObjectFlags,
        TransformFlags,
        ObjectTypeFlags,
        ObjectSourceFlags,
        ObjectBSPPolicyFlags,
        ObjectColorChangeFlags,
        PathfindingPolicyEnum,
        LightmappingPolicyEnum,
        ObjectGametypeEnum
        )

XML_OUTPUT = True

def initilize_resource(RESOURCE):
    RESOURCE.object_names = []
    RESOURCE.environment_objects = []
    RESOURCE.structure_bsps = []
    RESOURCE.scenery_palette = []
    RESOURCE.scenery = []
    RESOURCE.crate_palette = []
    RESOURCE.crates = []
    RESOURCE.editor_folders = []

def read_resource_body(RESOURCE, TAG, input_stream, tag_node, XML_OUTPUT):
    RESOURCE.resource_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    RESOURCE.resource_body = RESOURCE.ResourceBody()
    RESOURCE.resource_body.object_names_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "object names"))
    RESOURCE.resource_body.environment_objects_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "environment objects"))
    RESOURCE.resource_body.structure_bsps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "structure bsps"))
    RESOURCE.resource_body.scenery_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scenery palette"))
    RESOURCE.resource_body.scenery_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scenery"))
    RESOURCE.resource_body.next_scenery_object_id_salt = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(tag_node, "next scenery object id salt"))
    RESOURCE.resource_body.crate_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate palette"))
    RESOURCE.resource_body.crates_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "crates"))
    RESOURCE.resource_body.next_block_object_id_salt = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(tag_node, "next block object id salt"))
    RESOURCE.resource_body.editor_folders_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "editor folders"))

def get_object_names(input_stream, RESOURCE, TAG, node_element):
    object_name = RESOURCE.ObjectName()
    object_name.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    object_name.object_type = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "object type", None, 1, ""))
    object_name.placement_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "placement index", None, 1, ""))

    return object_name

def get_environment_objects(input_stream, RESOURCE, TAG, node_element):
    environment_object = RESOURCE.EnvironmentObject()
    environment_object.bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "bsp", None, RESOURCE.resource_body.structure_bsps_tag_block.count, "scenario_bsp_block"))
    environment_object.runtime_object_type = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "runtime object type"))
    environment_object.unique_id = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "unique id"))
    input_stream.read(4) # Padding?
    environment_object.object_definition_tag = TAG.read_variable_string_no_terminator_reversed(input_stream, 4, TAG, tag_format.XMLData(node_element, "object definition tag"))
    environment_object.environment_object = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "object"))
    input_stream.read(44) # Padding?

    return environment_object

def get_structure_bsp(input_stream, RESOURCE, TAG, node_element):
    structure_bsp = RESOURCE.StructureBSP()

    input_stream.read(16) # Padding?
    structure_bsp.structure_bsp = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "structure bsp"))
    structure_bsp.structure_lightmap = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "structure lightmap"))
    input_stream.read(4) # Padding
    structure_bsp.unused_radiance_estimated_search_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "radiance estimated search distance"))
    input_stream.read(4) # Padding
    structure_bsp.unused_luminels_per_world_unit = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "luminels per world unit"))
    structure_bsp.unused_output_white_reference = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "output white reference"))
    input_stream.read(8) # Padding
    structure_bsp.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", StructureBSPFlags))
    structure_bsp.default_sky = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "default sky", None, 1, "scenario_skies_block"))
    input_stream.read(2) # Padding

    return structure_bsp

def object_helper(tag_element, TAG, input_stream, RESOURCE, node_element, palette_count, palette_name):
    tag_element.palette_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, palette_count, palette_name))
    tag_element.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, RESOURCE.resource_body.object_names_tag_block.count, "scenario_object_names_block"))
    tag_element.placement_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "placement flags", ObjectFlags))
    tag_element.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    tag_element.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    tag_element.scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "scale"))
    tag_element.transform_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "transform flags", TransformFlags))
    tag_element.manual_bsp_flags = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "manual bsp flags"))
    tag_element.unique_id = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "unique id"))
    tag_element.origin_bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "origin bsp index", None, RESOURCE.resource_body.structure_bsps_tag_block.count, "scenario_bsp_block"))
    tag_element.object_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "object type", ObjectTypeFlags))
    tag_element.source = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "source", ObjectSourceFlags))
    tag_element.bsp_policy = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "bsp policy", ObjectBSPPolicyFlags))
    input_stream.read(1) # Padding?
    tag_element.editor_folder_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "editor folder", None, RESOURCE.resource_body.editor_folders_tag_block.count, "scenario_editor_folder_block"))

def get_scenery(input_stream, RESOURCE, TAG, node_element):
    scenery = RESOURCE.Scenery()
    object_helper(scenery, TAG, input_stream, RESOURCE, node_element, RESOURCE.resource_body.scenery_palette_tag_block.count, "scenario_scenery_palette_block")

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    scenery.variant_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    scenery.active_change_colors = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "active change colors", ObjectColorChangeFlags))
    scenery.primary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "primary color"))
    scenery.secondary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "secondary color"))
    scenery.tertiary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "tertiary color"))
    scenery.quaternary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "quaternary color"))
    scenery.pathfinding_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "pathfinding policy", PathfindingPolicyEnum))
    scenery.lightmap_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "lightmap policy", LightmappingPolicyEnum))
    scenery.pathfinding_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "pathfinding references"))
    input_stream.read(2) # Padding?
    scenery.valid_multiplayer_games = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "valid multiplayer games", ObjectGametypeEnum))

    return scenery

def get_crates(input_stream, RESOURCE, TAG, node_element):
    crate = RESOURCE.Crate()
    object_helper(crate, TAG, input_stream, RESOURCE, node_element, RESOURCE.resource_body.crate_palette_tag_block.count, "scenario_scenery_palette_block")

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    crate.variant_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    crate.active_change_colors = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "active change colors", ObjectColorChangeFlags))
    crate.primary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "primary color"))
    crate.secondary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "secondary color"))
    crate.tertiary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "tertiary color"))
    crate.quaternary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "quaternary color"))

    return crate

def get_palette(input_stream, TAG, node_element, padding=32):
    tag_reference = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    input_stream.read(padding) # Padding?

    return tag_reference

def palette_helper(input_stream, palette_count, palette_name, palette_header, palette, node, TAG, padding=32):
    if palette_count > 0:
        palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        palette_node = tag_format.get_xml_node(XML_OUTPUT, palette_count, node, "name", palette_name)
        for palette_idx in range(palette_count):
            palette_element_node = None
            if XML_OUTPUT:
                palette_element_node = TAG.xml_doc.createElement('element')
                palette_element_node.setAttribute('index', str(palette_idx))
                palette_node.appendChild(palette_element_node)

            palette.append(get_palette(input_stream, TAG, palette_element_node, padding))

        for palette_idx, palette_element in enumerate(palette):
            palette_name_length = palette_element.name_length
            if palette_name_length > 0:
                palette_element.name = TAG.read_variable_string(input_stream, palette_name_length, TAG)

            if XML_OUTPUT:
                palette_element_node = palette_node.childNodes[palette_idx]
                palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, palette_element_node, "name", "name")
                palette_element.append_xml_attributes(palette_tag_ref_node)

def read_object_names(RESOURCE, TAG, input_stream, tag_node, XML_OUTPUT):
    if RESOURCE.resource_body.object_names_tag_block.count > 0:
        RESOURCE.object_name_header = TAG.TagBlockHeader().read(input_stream, TAG)
        object_name_node = tag_format.get_xml_node(XML_OUTPUT, RESOURCE.resource_body.object_names_tag_block.count, tag_node, "name", "object names")
        for object_name_idx in range(RESOURCE.resource_body.object_names_tag_block.count):
            object_name_element_node = None
            if XML_OUTPUT:
                object_name_element_node = TAG.xml_doc.createElement('element')
                object_name_element_node.setAttribute('index', str(object_name_idx))
                object_name_node.appendChild(object_name_element_node)

            RESOURCE.object_names.append(get_object_names(input_stream, RESOURCE, TAG, object_name_element_node))

def read_environment_objects(RESOURCE, TAG, input_stream, tag_node, XML_OUTPUT):
    if RESOURCE.resource_body.environment_objects_tag_block.count > 0:
        RESOURCE.environment_objects_header = TAG.TagBlockHeader().read(input_stream, TAG)
        environment_objects_node = tag_format.get_xml_node(XML_OUTPUT, RESOURCE.resource_body.environment_objects_tag_block.count, tag_node, "name", "environment objects")
        for environment_object_idx in range(RESOURCE.resource_body.environment_objects_tag_block.count):
            environment_object_element_node = None
            if XML_OUTPUT:
                environment_object_element_node = TAG.xml_doc.createElement('element')
                environment_object_element_node.setAttribute('index', str(environment_object_idx))
                environment_objects_node.appendChild(environment_object_element_node)

            RESOURCE.environment_objects.append(get_environment_objects(input_stream, RESOURCE, TAG, environment_object_element_node))

def read_structure_bsps(RESOURCE, TAG, input_stream, tag_node, XML_OUTPUT):
    if RESOURCE.resource_body.structure_bsps_tag_block.count > 0:
        RESOURCE.structure_bsps_header = TAG.TagBlockHeader().read(input_stream, TAG)
        structure_bsp_node = tag_format.get_xml_node(XML_OUTPUT, RESOURCE.resource_body.structure_bsps_tag_block.count, tag_node, "name", "structure bsps")
        for structure_bsp_idx in range(RESOURCE.resource_body.structure_bsps_tag_block.count):
            structure_bsp_element_node = None
            if XML_OUTPUT:
                structure_bsp_element_node = TAG.xml_doc.createElement('element')
                structure_bsp_element_node.setAttribute('index', str(structure_bsp_idx))
                structure_bsp_node.appendChild(structure_bsp_element_node)

            RESOURCE.structure_bsps.append(get_structure_bsp(input_stream, RESOURCE, TAG, structure_bsp_element_node))

        for structure_bsp_idx, structure_bsp in enumerate(RESOURCE.structure_bsps):
            structure_bsp_name_length = structure_bsp.structure_bsp.name_length
            structure_lightmap_name_length = structure_bsp.structure_lightmap.name_length
            if structure_bsp_name_length > 0:
                structure_bsp.structure_bsp.name = TAG.read_variable_string(input_stream, structure_bsp_name_length, TAG)

            if structure_lightmap_name_length > 0:
                structure_bsp.structure_lightmap.name = TAG.read_variable_string(input_stream, structure_lightmap_name_length, TAG)

            if XML_OUTPUT:
                structure_bsp_element_node = structure_bsp_node.childNodes[structure_bsp_idx]
                structure_bsp_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, structure_bsp_element_node, "name", "structure bsp")
                structure_lightmap_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, structure_bsp_element_node, "name", "structure lightmap")
                structure_bsp.structure_bsp.append_xml_attributes(structure_bsp_tag_ref_node)
                structure_bsp.structure_lightmap.append_xml_attributes(structure_lightmap_tag_ref_node)

def read_scenery(RESOURCE, TAG, input_stream, tag_node, XML_OUTPUT):
    palette_helper(input_stream, RESOURCE.resource_body.scenery_palette_tag_block.count, "scenery palette", RESOURCE.scenery_palette_header, RESOURCE.scenery_palette, tag_node, TAG)

    if RESOURCE.resource_body.scenery_tag_block.count > 0:
        RESOURCE.scenery_header = TAG.TagBlockHeader().read(input_stream, TAG)
        scenery_node = tag_format.get_xml_node(XML_OUTPUT, RESOURCE.resource_body.scenery_tag_block.count, tag_node, "name", "scenery")
        for scenery_idx in range(RESOURCE.resource_body.scenery_tag_block.count):
            scenery_element_node = None
            if XML_OUTPUT:
                scenery_element_node = TAG.xml_doc.createElement('element')
                scenery_element_node.setAttribute('index', str(scenery_idx))
                scenery_node.appendChild(scenery_element_node)

            RESOURCE.scenery.append(get_scenery(input_stream, RESOURCE, TAG, scenery_element_node))

        for scenery_idx, scenery in enumerate(RESOURCE.scenery):
            scenery_element_node = None
            if XML_OUTPUT:
                scenery_element_node = scenery_node.childNodes[scenery_idx]

            scenery.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            scenery.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            scenery.sper_header = TAG.TagBlockHeader().read(input_stream, TAG)
            if scenery.variant_name_length > 0:
                scenery.variant_name = TAG.read_variable_string_no_terminator(input_stream, scenery.variant_name_length, TAG, tag_format.XMLData(scenery_element_node, "variant name"))

            scenery.sct3_header = TAG.TagBlockHeader().read(input_stream, TAG)

            scenery.pathfinding_references = []
            if scenery.pathfinding_references_tag_block.count > 0:
                scenery.pathfinding_references_header = TAG.TagBlockHeader().read(input_stream, TAG)
                pathfinding_reference_node = tag_format.get_xml_node(XML_OUTPUT, scenery.pathfinding_references_tag_block.count, scenery_element_node, "name", "pathfinding references")
                for pathfinding_reference_idx in range(scenery.pathfinding_references_tag_block.count):
                    pathfinding_reference_element_node = None
                    if XML_OUTPUT:
                        pathfinding_reference_element_node = TAG.xml_doc.createElement('element')
                        pathfinding_reference_element_node.setAttribute('index', str(pathfinding_reference_idx))
                        pathfinding_reference_node.appendChild(pathfinding_reference_element_node)

                    pathfinding_reference = RESOURCE.PathfindingReference()
                    pathfinding_reference.bsp_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_reference_element_node, "bsp index"))
                    pathfinding_reference.pathfinding_object_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_reference_element_node, "pathfinding object index"))

                    scenery.pathfinding_references.append(pathfinding_reference)

def read_crates(RESOURCE, TAG, input_stream, tag_node, XML_OUTPUT):
    palette_helper(input_stream, RESOURCE.resource_body.crate_palette_tag_block.count, "crate palette", RESOURCE.crate_palette_header, RESOURCE.crate_palette, tag_node, TAG)

    if RESOURCE.resource_body.crates_tag_block.count > 0:
        RESOURCE.crate_header = TAG.TagBlockHeader().read(input_stream, TAG)
        crates_node = tag_format.get_xml_node(XML_OUTPUT, RESOURCE.resource_body.crates_tag_block.count, tag_node, "name", "crates")
        for crate_idx in range(RESOURCE.resource_body.crates_tag_block.count):
            crate_element_node = None
            if XML_OUTPUT:
                crate_element_node = TAG.xml_doc.createElement('element')
                crate_element_node.setAttribute('index', str(crate_idx))
                crates_node.appendChild(crate_element_node)

            RESOURCE.crates.append(get_crates(input_stream, RESOURCE, TAG, crate_element_node))

        for crate_idx, crate in enumerate(RESOURCE.crates):
            crate_element_node = None
            if XML_OUTPUT:
                crate_element_node = crates_node.childNodes[crate_idx]

            crate.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            crate.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            crate.sper_header = TAG.TagBlockHeader().read(input_stream, TAG)
            if crate.variant_name_length > 0:
                crate.variant_name = TAG.read_variable_string_no_terminator(input_stream, crate.variant_name_length, TAG, tag_format.XMLData(crate_element_node, "variant name"))

def read_editor_folders(RESOURCE, TAG, input_stream, tag_node, XML_OUTPUT):
    if RESOURCE.resource_body.editor_folders_tag_block.count > 0:
        RESOURCE.editor_folders_header = TAG.TagBlockHeader().read(input_stream, TAG)
        editor_folders_node = tag_format.get_xml_node(XML_OUTPUT, RESOURCE.resource_body.editor_folders_tag_block.count, tag_node, "name", "editor folders")
        for editor_folder_idx in range(RESOURCE.resource_body.editor_folders_tag_block.count):
            editor_folder_element_node = None
            if XML_OUTPUT:
                editor_folder_element_node = TAG.xml_doc.createElement('element')
                editor_folder_element_node.setAttribute('index', str(editor_folder_idx))
                editor_folders_node.appendChild(editor_folder_element_node)

            editor_folder = RESOURCE.EditorFolder()
            editor_folder.parent_folder = TAG.read_block_index_signed_integer(input_stream, TAG, tag_format.XMLData(editor_folder_element_node, "parent folder", None, 1, ""))
            editor_folder.name = TAG.read_string256(input_stream, TAG, tag_format.XMLData(editor_folder_element_node, "name"))

            RESOURCE.editor_folders.append(editor_folder)

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    RESOURCE = SceneryResourceAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    RESOURCE.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_resource(RESOURCE)
    read_resource_body(RESOURCE, TAG, input_stream, tag_node, XML_OUTPUT)
    read_object_names(RESOURCE, TAG, input_stream, tag_node, XML_OUTPUT)
    read_environment_objects(RESOURCE, TAG, input_stream, tag_node, XML_OUTPUT)
    read_structure_bsps(RESOURCE, TAG, input_stream, tag_node, XML_OUTPUT)
    read_scenery(RESOURCE, TAG, input_stream, tag_node, XML_OUTPUT)
    read_crates(RESOURCE, TAG, input_stream, tag_node, XML_OUTPUT)
    read_editor_folders(RESOURCE, TAG, input_stream, tag_node, XML_OUTPUT)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, RESOURCE.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return RESOURCE
