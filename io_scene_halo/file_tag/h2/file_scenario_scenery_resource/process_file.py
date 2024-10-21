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
from ..file_scenario import process_file as process_scenario
from .format import ScenarioAsset

XML_OUTPUT = False

def read_scenario_body(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    SCENARIO.scenario_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    SCENARIO.scenario_body = SCENARIO.ScenarioBody()
    SCENARIO.scenario_body.skies_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.object_names_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "object names"))
    SCENARIO.scenario_body.environment_objects_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "environment objects"))
    SCENARIO.scenario_body.structure_bsps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "structure bsps"))
    SCENARIO.scenario_body.scenery_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scenery palette"))
    SCENARIO.scenario_body.scenery_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scenery"))
    SCENARIO.scenario_body.next_scenery_object_id_salt = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(tag_node, "next scenery object id salt"))
    SCENARIO.scenario_body.crate_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate palette"))
    SCENARIO.scenario_body.crates_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "crates"))
    SCENARIO.scenario_body.next_block_object_id_salt = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(tag_node, "next block object id salt"))
    SCENARIO.scenario_body.editor_folders_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "editor folders"))

def read_scenery(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    process_scenario.palette_helper(input_stream, SCENARIO.scenario_body.scenery_palette_tag_block.count, "scenery palette", SCENARIO.scenery_palette_header, SCENARIO.scenery_palette, tag_node, TAG)

    if SCENARIO.scenario_body.scenery_tag_block.count > 0:
        SCENARIO.scenery_header = TAG.TagBlockHeader().read(input_stream, TAG)
        scenery_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.scenery_tag_block.count, tag_node, "name", "scenery")
        for scenery_idx in range(SCENARIO.scenario_body.scenery_tag_block.count):
            scenery_element_node = None
            if XML_OUTPUT:
                scenery_element_node = TAG.xml_doc.createElement('element')
                scenery_element_node.setAttribute('index', str(scenery_idx))
                scenery_node.appendChild(scenery_element_node)

            SCENARIO.scenery.append(process_scenario.get_scenery(input_stream, SCENARIO, TAG, scenery_element_node))

        for scenery_idx, scenery in enumerate(SCENARIO.scenery):
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

                    pathfinding_reference = SCENARIO.PathfindingReference()
                    pathfinding_reference.bsp_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_reference_element_node, "bsp index"))
                    pathfinding_reference.pathfinding_object_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_reference_element_node, "pathfinding object index"))

                    scenery.pathfinding_references.append(pathfinding_reference)

def read_crates(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    process_scenario.palette_helper(input_stream, SCENARIO.scenario_body.crate_palette_tag_block.count, "crate palette", SCENARIO.crates_palette_header, SCENARIO.crates_palette, tag_node, TAG)

    if SCENARIO.scenario_body.crates_tag_block.count > 0:
        SCENARIO.crates_header = TAG.TagBlockHeader().read(input_stream, TAG)
        crates_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.crates_tag_block.count, tag_node, "name", "crates")
        for crate_idx in range(SCENARIO.scenario_body.crates_tag_block.count):
            crate_element_node = None
            if XML_OUTPUT:
                crate_element_node = TAG.xml_doc.createElement('element')
                crate_element_node.setAttribute('index', str(crate_idx))
                crates_node.appendChild(crate_element_node)

            SCENARIO.crates.append(process_scenario.get_crate(input_stream, SCENARIO, TAG, crate_element_node))

        for crate_idx, crate in enumerate(SCENARIO.crates):
            crate_element_node = None
            if XML_OUTPUT:
                crate_element_node = crates_node.childNodes[crate_idx]

            crate.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            crate.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            crate.sper_header = TAG.TagBlockHeader().read(input_stream, TAG)
            if crate.variant_name_length > 0:
                crate.variant_name = TAG.read_variable_string_no_terminator(input_stream, crate.variant_name_length, TAG, tag_format.XMLData(crate_element_node, "variant name"))

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    SCENARIO = ScenarioAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SCENARIO.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    process_scenario.initilize_scenario(SCENARIO)
    read_scenario_body(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_object_names(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_environment_objects(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_structure_bsps(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_scenery(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_crates(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_editor_folders(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, SCENARIO.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return SCENARIO
