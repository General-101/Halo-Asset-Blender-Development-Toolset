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
    SCENARIO.scenario_body.device_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "device groups"))
    SCENARIO.scenario_body.machines_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "machines"))
    SCENARIO.scenario_body.machine_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "machine palette"))
    SCENARIO.scenario_body.controls_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "controls"))
    SCENARIO.scenario_body.control_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "control palette"))
    SCENARIO.scenario_body.light_fixtures_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "light fixtures"))
    SCENARIO.scenario_body.light_fixtures_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "light fixtures palette"))
    SCENARIO.scenario_body.next_machine_id_salt = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(tag_node, "next machine id salt"))
    SCENARIO.scenario_body.next_control_id_salt = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(tag_node, "next control id salt"))
    SCENARIO.scenario_body.next_light_fixture_id_salt = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(tag_node, "next light fixture id salt"))
    SCENARIO.scenario_body.editor_folders_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "editor folders"))

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    SCENARIO = ScenarioAsset()
    TAG.is_legacy = False
    TAG.big_endian = False
    tag_node = None
    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SCENARIO.header = TAG.Header().read(input_stream, TAG)
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    process_scenario.initilize_scenario(SCENARIO)
    read_scenario_body(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)

    process_scenario.read_environment_objects(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_object_names(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_structure_bsps(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_device_groups(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_machines(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_controls(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_light_fixtures(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
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
