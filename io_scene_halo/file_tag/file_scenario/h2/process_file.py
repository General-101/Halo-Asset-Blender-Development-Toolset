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

from math import degrees
from .format import ScenarioAsset
from mathutils import Vector, Quaternion

DEBUG_PARSER = True
DEBUG_HEADER = True
DEBUG_BODY = True

def process_file(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    SCENARIO = ScenarioAsset()

    header_struct = struct.unpack('<hbb32s4sIIIIHbb4s', input_stream.read(64))
    SCENARIO.header = TAG.Header()
    SCENARIO.header.unk1 = header_struct[0]
    SCENARIO.header.flags = header_struct[1]
    SCENARIO.header.type = header_struct[2]
    SCENARIO.header.name = header_struct[3].decode().rstrip('\x00')
    SCENARIO.header.tag_group = header_struct[4].decode().rstrip('\x00')
    SCENARIO.header.checksum = header_struct[5]
    SCENARIO.header.data_offset = header_struct[6]
    SCENARIO.header.data_length = header_struct[7]
    SCENARIO.header.unk2 = header_struct[8]
    SCENARIO.header.version = header_struct[9]
    SCENARIO.header.destination = header_struct[10]
    SCENARIO.header.plugin_handle = header_struct[11]
    SCENARIO.header.engine_tag = header_struct[12].decode().rstrip('\x00')

    if DEBUG_PARSER and DEBUG_HEADER:
        print(" ===== Tag Header ===== ")
        print("Unknown Value: ", SCENARIO.header.unk1)
        print("Flags: ", SCENARIO.header.flags)
        print("Type: ", SCENARIO.header.type)
        print("Name: ", SCENARIO.header.name)
        print("Tag Group: ", SCENARIO.header.tag_group)
        print("Checksum: ", SCENARIO.header.checksum)
        print("Data Offset: ", SCENARIO.header.data_offset)
        print("Data Length:", SCENARIO.header.data_length)
        print("Unknown Value: ", SCENARIO.header.unk2)
        print("Version: ", SCENARIO.header.version)
        print("Destination: ", SCENARIO.header.destination)
        print("Plugin Handle: ", SCENARIO.header.plugin_handle)
        print("Engine Tag: ", SCENARIO.header.engine_tag)
        print(" ")

    level_tag_block_header = struct.unpack('<16x', input_stream.read(16))
    scenario_body_struct = struct.unpack('<4siiIiIIHHiIIfiIIiIIiiIIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiIIiII', input_stream.read(404))
    SCENARIO.scenario_body = SCENARIO.ScenarioBody()
    SCENARIO.scenario_body.unused_tag_ref = TAG.TagRef(scenario_body_struct[0].decode('utf-8', 'replace').rstrip('\x00'), "", scenario_body_struct[2] + 1, scenario_body_struct[1], scenario_body_struct[3])
    SCENARIO.scenario_body.skies_tag_block = TAG.TagBlock(scenario_body_struct[4], 0, scenario_body_struct[5], scenario_body_struct[6])
    SCENARIO.scenario_body.scenario_type = scenario_body_struct[7]
    SCENARIO.scenario_body.scenario_flags = scenario_body_struct[8]
    SCENARIO.scenario_body.child_scenarios_tag_block = TAG.TagBlock(scenario_body_struct[9], 0, scenario_body_struct[10], scenario_body_struct[11])
    SCENARIO.scenario_body.local_north = degrees(scenario_body_struct[12])
    SCENARIO.scenario_body.predicted_resources_tag_block = TAG.TagBlock(scenario_body_struct[13], 0, scenario_body_struct[14], scenario_body_struct[15])
    SCENARIO.scenario_body.functions_tag_block = TAG.TagBlock(scenario_body_struct[16], 0, scenario_body_struct[17], scenario_body_struct[18])
    SCENARIO.scenario_body.editor_scenario_data = TAG.RawData(scenario_body_struct[19], scenario_body_struct[20], scenario_body_struct[21], scenario_body_struct[22], scenario_body_struct[23])
    SCENARIO.scenario_body.comments_tag_block = TAG.TagBlock(scenario_body_struct[24], 0, scenario_body_struct[25], scenario_body_struct[26])
    SCENARIO.scenario_body.environment_objects_tag_block = TAG.TagBlock(scenario_body_struct[27], 0, scenario_body_struct[28], scenario_body_struct[29])
    SCENARIO.scenario_body.object_names_tag_block = TAG.TagBlock(scenario_body_struct[30], 0, scenario_body_struct[31], scenario_body_struct[32])
    SCENARIO.scenario_body.scenery_tag_block = TAG.TagBlock(scenario_body_struct[33], 0, scenario_body_struct[34], scenario_body_struct[35])
    SCENARIO.scenario_body.scenery_palette_tag_block = TAG.TagBlock(scenario_body_struct[36], 0, scenario_body_struct[37], scenario_body_struct[38])
    SCENARIO.scenario_body.bipeds_tag_block = TAG.TagBlock(scenario_body_struct[39], 0, scenario_body_struct[40], scenario_body_struct[41])
    SCENARIO.scenario_body.biped_palette_tag_block = TAG.TagBlock(scenario_body_struct[42], 0, scenario_body_struct[43], scenario_body_struct[44])
    SCENARIO.scenario_body.vehicles_tag_block = TAG.TagBlock(scenario_body_struct[45], 0, scenario_body_struct[46], scenario_body_struct[47])
    SCENARIO.scenario_body.vehicle_palette_tag_block = TAG.TagBlock(scenario_body_struct[48], 0, scenario_body_struct[49], scenario_body_struct[50])
    SCENARIO.scenario_body.equipment_tag_block = TAG.TagBlock(scenario_body_struct[51], 0, scenario_body_struct[52], scenario_body_struct[53])
    SCENARIO.scenario_body.equipment_palette_tag_block = TAG.TagBlock(scenario_body_struct[54], 0, scenario_body_struct[55], scenario_body_struct[56])
    SCENARIO.scenario_body.weapons_tag_block = TAG.TagBlock(scenario_body_struct[57], 0, scenario_body_struct[58], scenario_body_struct[59])
    SCENARIO.scenario_body.weapon_palette_tag_block = TAG.TagBlock(scenario_body_struct[60], 0, scenario_body_struct[61], scenario_body_struct[62])
    SCENARIO.scenario_body.device_groups_tag_block = TAG.TagBlock(scenario_body_struct[63], 0, scenario_body_struct[64], scenario_body_struct[65])
    SCENARIO.scenario_body.machines_tag_block = TAG.TagBlock(scenario_body_struct[66], 0, scenario_body_struct[67], scenario_body_struct[68])
    SCENARIO.scenario_body.machine_palette_tag_block = TAG.TagBlock(scenario_body_struct[69], 0, scenario_body_struct[70], scenario_body_struct[71])
    SCENARIO.scenario_body.controls_tag_block = TAG.TagBlock(scenario_body_struct[72], 0, scenario_body_struct[73], scenario_body_struct[74])
    SCENARIO.scenario_body.control_palette_tag_block = TAG.TagBlock(scenario_body_struct[75], 0, scenario_body_struct[76], scenario_body_struct[77])
    SCENARIO.scenario_body.light_fixtures_tag_block = TAG.TagBlock(scenario_body_struct[78], 0, scenario_body_struct[79], scenario_body_struct[80])
    SCENARIO.scenario_body.light_fixtures_palette_tag_block = TAG.TagBlock(scenario_body_struct[81], 0, scenario_body_struct[82], scenario_body_struct[83])
    SCENARIO.scenario_body.sound_scenery_tag_block = TAG.TagBlock(scenario_body_struct[84], 0, scenario_body_struct[85], scenario_body_struct[86])
    SCENARIO.scenario_body.sound_scenery_palette_tag_block = TAG.TagBlock(scenario_body_struct[87], 0, scenario_body_struct[88], scenario_body_struct[89])
    SCENARIO.scenario_body.light_volumes_tag_block = TAG.TagBlock(scenario_body_struct[90], 0, scenario_body_struct[91], scenario_body_struct[92])
    SCENARIO.scenario_body.light_volume_palette_tag_block = TAG.TagBlock(scenario_body_struct[93], 0, scenario_body_struct[94], scenario_body_struct[95])
    SCENARIO.scenario_body.player_starting_profile_tag_block = TAG.TagBlock(scenario_body_struct[96], 0, scenario_body_struct[97], scenario_body_struct[98])
    SCENARIO.scenario_body.player_starting_locations_tag_block = TAG.TagBlock(scenario_body_struct[99], 0, scenario_body_struct[100], scenario_body_struct[101])

    if DEBUG_PARSER and DEBUG_BODY:
        print(" ===== SCNR Body ===== ")
        print("Unused Tag Reference Group: ", SCENARIO.scenario_body.unused_tag_ref.tag_group)
        print("Unused Tag Reference Name: ", SCENARIO.scenario_body.unused_tag_ref.name)
        print("Unused Tag Reference Length: ", SCENARIO.scenario_body.unused_tag_ref.name_length)
        print("Unused Tag Reference Salt: ", SCENARIO.scenario_body.unused_tag_ref.salt)
        print("Unused Tag Reference Index: ", SCENARIO.scenario_body.unused_tag_ref.index)
        print("Skies Tag Block Count: ", SCENARIO.scenario_body.skies_tag_block.count)
        print("Skies Tag Block Maximum Count: ", SCENARIO.scenario_body.skies_tag_block.maximum_count)
        print("Skies Tag Block Address: ", SCENARIO.scenario_body.skies_tag_block.address)
        print("Skies Tag Block Definition: ", SCENARIO.scenario_body.skies_tag_block.definition)
        print("Scenario Type: ", SCENARIO.scenario_body.scenario_type)
        print("Scenario Flags: ", SCENARIO.scenario_body.scenario_flags)
        print("Child Scenarios Tag Block Count: ", SCENARIO.scenario_body.child_scenarios_tag_block.count)
        print("Child Scenarios Tag Block Maximum Count: ", SCENARIO.scenario_body.child_scenarios_tag_block.maximum_count)
        print("Child Scenarios Tag Block Address: ", SCENARIO.scenario_body.child_scenarios_tag_block.address)
        print("Child Scenarios Tag Block Definition: ", SCENARIO.scenario_body.child_scenarios_tag_block.definition)
        print("Local North: ", SCENARIO.scenario_body.local_north)
        print("Predicted Resources Tag Block Count: ", SCENARIO.scenario_body.predicted_resources_tag_block.count)
        print("Predicted Resources Tag Block Maximum Count: ", SCENARIO.scenario_body.predicted_resources_tag_block.maximum_count)
        print("Predicted Resources Tag Block Address: ", SCENARIO.scenario_body.predicted_resources_tag_block.address)
        print("Predicted Resources Tag Block Definition: ", SCENARIO.scenario_body.predicted_resources_tag_block.definition)
        print("Functions Tag Block Count: ", SCENARIO.scenario_body.functions_tag_block.count)
        print("Functions Tag Block Maximum Count: ", SCENARIO.scenario_body.functions_tag_block.maximum_count)
        print("Functions Tag Block Address: ", SCENARIO.scenario_body.functions_tag_block.address)
        print("Functions Tag Block Definition: ", SCENARIO.scenario_body.functions_tag_block.definition)
        print("Editor Scenario Data Size: ", SCENARIO.scenario_body.editor_scenario_data.size)
        print("Editor Scenario Data Flags: ", SCENARIO.scenario_body.editor_scenario_data.flags)
        print("Editor Scenario Data Raw Pointer: ", SCENARIO.scenario_body.editor_scenario_data.raw_pointer)
        print("Editor Scenario Data Pointer: ", SCENARIO.scenario_body.editor_scenario_data.pointer)
        print("Editor Scenario Data ID: ", SCENARIO.scenario_body.editor_scenario_data.id)
        print("Comments Tag Block Count: ", SCENARIO.scenario_body.comments_tag_block.count)
        print("Comments Tag Block Maximum Count: ", SCENARIO.scenario_body.comments_tag_block.maximum_count)
        print("Comments Tag Block Address: ", SCENARIO.scenario_body.comments_tag_block.address)
        print("Comments Tag Block Definition: ", SCENARIO.scenario_body.comments_tag_block.definition)
        print("Environment Objects Tag Block Count: ", SCENARIO.scenario_body.environment_objects_tag_block.count)
        print("Environment Objects Tag Block Maximum Count: ", SCENARIO.scenario_body.environment_objects_tag_block.maximum_count)
        print("Environment Objects Tag Block Address: ", SCENARIO.scenario_body.environment_objects_tag_block.address)
        print("Environment Objects Tag Block Definition: ", SCENARIO.scenario_body.environment_objects_tag_block.definition)
        print("Object Names Tag Block Count: ", SCENARIO.scenario_body.object_names_tag_block.count)
        print("Object Names Tag Block Maximum Count: ", SCENARIO.scenario_body.object_names_tag_block.maximum_count)
        print("Object Names Tag Block Address: ", SCENARIO.scenario_body.object_names_tag_block.address)
        print("Object Names Tag Block Definition: ", SCENARIO.scenario_body.object_names_tag_block.definition)
        print("Scenery Tag Block Count: ", SCENARIO.scenario_body.scenery_tag_block.count)
        print("Scenery Tag Block Maximum Count: ", SCENARIO.scenario_body.scenery_tag_block.maximum_count)
        print("Scenery Tag Block Address: ", SCENARIO.scenario_body.scenery_tag_block.address)
        print("Scenery Tag Block Definition: ", SCENARIO.scenario_body.scenery_tag_block.definition)
        print("Scenery Palette Tag Block Count: ", SCENARIO.scenario_body.scenery_palette_tag_block.count)
        print("Scenery Palette Tag Block Maximum Count: ", SCENARIO.scenario_body.scenery_palette_tag_block.maximum_count)
        print("Scenery Palette Tag Block Address: ", SCENARIO.scenario_body.scenery_palette_tag_block.address)
        print("Scenery Palette Tag Block Definition: ", SCENARIO.scenario_body.scenery_palette_tag_block.definition)
        print("Bipeds Tag Block Count: ", SCENARIO.scenario_body.bipeds_tag_block.count)
        print("Bipeds Tag Block Maximum Count: ", SCENARIO.scenario_body.bipeds_tag_block.maximum_count)
        print("Bipeds Tag Block Address: ", SCENARIO.scenario_body.bipeds_tag_block.address)
        print("Bipeds Tag Block Definition: ", SCENARIO.scenario_body.bipeds_tag_block.definition)
        print("Biped Palette Tag Block Count: ", SCENARIO.scenario_body.biped_palette_tag_block.count)
        print("Biped Palette Tag Block Maximum Count: ", SCENARIO.scenario_body.biped_palette_tag_block.maximum_count)
        print("Biped Palette Tag Block Address: ", SCENARIO.scenario_body.biped_palette_tag_block.address)
        print("Biped Palette Tag Block Definition: ", SCENARIO.scenario_body.biped_palette_tag_block.definition)
        print("Vehicles Tag Block Count: ", SCENARIO.scenario_body.vehicles_tag_block.count)
        print("Vehicles Tag Block Maximum Count: ", SCENARIO.scenario_body.vehicles_tag_block.maximum_count)
        print("Vehicles Tag Block Address: ", SCENARIO.scenario_body.vehicles_tag_block.address)
        print("Vehicles Tag Block Definition: ", SCENARIO.scenario_body.vehicles_tag_block.definition)
        print("Vehicle Palette Tag Block Count: ", SCENARIO.scenario_body.vehicle_palette_tag_block.count)
        print("Vehicle Palette Tag Block Maximum Count: ", SCENARIO.scenario_body.vehicle_palette_tag_block.maximum_count)
        print("Vehicle Palette Tag Block Address: ", SCENARIO.scenario_body.vehicle_palette_tag_block.address)
        print("Vehicle Palette Tag Block Definition: ", SCENARIO.scenario_body.vehicle_palette_tag_block.definition)
        print("Equipment Tag Block Count: ", SCENARIO.scenario_body.equipment_tag_block.count)
        print("Equipment Tag Block Maximum Count: ", SCENARIO.scenario_body.equipment_tag_block.maximum_count)
        print("Equipment Tag Block Address: ", SCENARIO.scenario_body.equipment_tag_block.address)
        print("Equipment Tag Block Definition: ", SCENARIO.scenario_body.equipment_tag_block.definition)
        print("Equipment Palette Tag Block Count: ", SCENARIO.scenario_body.equipment_palette_tag_block.count)
        print("Equipment Palette Tag Block Maximum Count: ", SCENARIO.scenario_body.equipment_palette_tag_block.maximum_count)
        print("Equipment Palette Tag Block Address: ", SCENARIO.scenario_body.equipment_palette_tag_block.address)
        print("Equipment Palette Tag Block Definition: ", SCENARIO.scenario_body.equipment_palette_tag_block.definition)
        print("Weapons Tag Block Count: ", SCENARIO.scenario_body.weapons_tag_block.count)
        print("Weapons Tag Block Maximum Count: ", SCENARIO.scenario_body.weapons_tag_block.maximum_count)
        print("Weapons Tag Block Address: ", SCENARIO.scenario_body.weapons_tag_block.address)
        print("Weapons Tag Block Definition: ", SCENARIO.scenario_body.weapons_tag_block.definition)
        print("Weapon Palette Tag Block Count: ", SCENARIO.scenario_body.weapon_palette_tag_block.count)
        print("Weapon Palette Tag Block Maximum Count: ", SCENARIO.scenario_body.weapon_palette_tag_block.maximum_count)
        print("Weapon Palette Tag Block Address: ", SCENARIO.scenario_body.weapon_palette_tag_block.address)
        print("Weapon Palette Tag Block Definition: ", SCENARIO.scenario_body.weapon_palette_tag_block.definition)
        print("Device Group Tag Block Count: ", SCENARIO.scenario_body.device_groups_tag_block.count)
        print("Device Group Tag Block Maximum Count: ", SCENARIO.scenario_body.device_groups_tag_block.maximum_count)
        print("Device Group Tag Block Address: ", SCENARIO.scenario_body.device_groups_tag_block.address)
        print("Device Group Tag Block Definition: ", SCENARIO.scenario_body.device_groups_tag_block.definition)
        print("Machines Tag Block Count: ", SCENARIO.scenario_body.machines_tag_block.count)
        print("Machines Tag Block Maximum Count: ", SCENARIO.scenario_body.machines_tag_block.maximum_count)
        print("Machines Tag Block Address: ", SCENARIO.scenario_body.machines_tag_block.address)
        print("Machines Tag Block Definition: ", SCENARIO.scenario_body.machines_tag_block.definition)
        print("Machine Palette Tag Block Count: ", SCENARIO.scenario_body.machine_palette_tag_block.count)
        print("Machine Palette Tag Block Maximum Count: ", SCENARIO.scenario_body.machine_palette_tag_block.maximum_count)
        print("Machine Palette Tag Block Address: ", SCENARIO.scenario_body.machine_palette_tag_block.address)
        print("Machine Palette Tag Block Definition: ", SCENARIO.scenario_body.machine_palette_tag_block.definition)
        print("Controls Tag Block Count: ", SCENARIO.scenario_body.controls_tag_block.count)
        print("Controls Tag Block Maximum Count: ", SCENARIO.scenario_body.controls_tag_block.maximum_count)
        print("Controls Tag Block Address: ", SCENARIO.scenario_body.controls_tag_block.address)
        print("Controls Tag Block Definition: ", SCENARIO.scenario_body.controls_tag_block.definition)
        print("Control Palette Tag Block Count: ", SCENARIO.scenario_body.control_palette_tag_block.count)
        print("Control Palette Tag Block Maximum Count: ", SCENARIO.scenario_body.control_palette_tag_block.maximum_count)
        print("Control Palette Tag Block Address: ", SCENARIO.scenario_body.control_palette_tag_block.address)
        print("Control Palette Tag Block Definition: ", SCENARIO.scenario_body.control_palette_tag_block.definition)
        print("Light Fixtures Tag Block Count: ", SCENARIO.scenario_body.light_fixtures_tag_block.count)
        print("Light Fixtures Tag Block Maximum Count: ", SCENARIO.scenario_body.light_fixtures_tag_block.maximum_count)
        print("Light Fixtures Tag Block Address: ", SCENARIO.scenario_body.light_fixtures_tag_block.address)
        print("Light Fixtures Tag Block Definition: ", SCENARIO.scenario_body.light_fixtures_tag_block.definition)
        print("Light Fixtures Palette Tag Block Count: ", SCENARIO.scenario_body.light_fixtures_palette_tag_block.count)
        print("Light Fixtures Palette Tag Block Maximum Count: ", SCENARIO.scenario_body.light_fixtures_palette_tag_block.maximum_count)
        print("Light Fixtures Palette Tag Block Address: ", SCENARIO.scenario_body.light_fixtures_palette_tag_block.address)
        print("Light Fixtures Palette Tag Block Definition: ", SCENARIO.scenario_body.light_fixtures_palette_tag_block.definition)
        print("Sound Scenery Tag Block Count: ", SCENARIO.scenario_body.sound_scenery_tag_block.count)
        print("Sound Scenery Tag Block Maximum Count: ", SCENARIO.scenario_body.sound_scenery_tag_block.maximum_count)
        print("Sound Scenery Tag Block Address: ", SCENARIO.scenario_body.sound_scenery_tag_block.address)
        print("Sound Scenery Tag Block Definition: ", SCENARIO.scenario_body.sound_scenery_tag_block.definition)
        print("Sound Scenery Palette Tag Block Count: ", SCENARIO.scenario_body.sound_scenery_palette_tag_block.count)
        print("Sound Scenery Palette Tag Block Maximum Count: ", SCENARIO.scenario_body.sound_scenery_palette_tag_block.maximum_count)
        print("Sound Scenery Palette Tag Block Address: ", SCENARIO.scenario_body.sound_scenery_palette_tag_block.address)
        print("Sound Scenery Palette Tag Block Definition: ", SCENARIO.scenario_body.sound_scenery_palette_tag_block.definition)
        print("Light Volumes Tag Block Count: ", SCENARIO.scenario_body.light_volumes_tag_block.count)
        print("Light Volumes Tag Block Maximum Count: ", SCENARIO.scenario_body.light_volumes_tag_block.maximum_count)
        print("Light Volumes Tag Block Address: ", SCENARIO.scenario_body.light_volumes_tag_block.address)
        print("Light Volumes Tag Block Definition: ", SCENARIO.scenario_body.light_volumes_tag_block.definition)
        print("Light Volume Palette Tag Block Count: ", SCENARIO.scenario_body.light_volume_palette_tag_block.count)
        print("Light Volume Palette Tag Block Maximum Count: ", SCENARIO.scenario_body.light_volume_palette_tag_block.maximum_count)
        print("Light Volume Palette Tag Block Address: ", SCENARIO.scenario_body.light_volume_palette_tag_block.address)
        print("Light Volume Palette Tag Block Definition: ", SCENARIO.scenario_body.light_volume_palette_tag_block.definition)
        print("Player Starting Profile Tag Block Count: ", SCENARIO.scenario_body.player_starting_profile_tag_block.count)
        print("Player Starting Profile Tag Block Maximum Count: ", SCENARIO.scenario_body.player_starting_profile_tag_block.maximum_count)
        print("Player Starting Profile Tag Block Address: ", SCENARIO.scenario_body.player_starting_profile_tag_block.address)
        print("Player Starting Profile Tag Block Definition: ", SCENARIO.scenario_body.player_starting_profile_tag_block.definition)
        print("Player Starting Locations Tag Block Count: ", SCENARIO.scenario_body.player_starting_locations_tag_block.count)
        print("Player Starting Locations Tag Block Maximum Count: ", SCENARIO.scenario_body.player_starting_locations_tag_block.maximum_count)
        print("Player Starting Locations Tag Block Address: ", SCENARIO.scenario_body.player_starting_locations_tag_block.address)
        print("Player Starting Locations Tag Block Definition: ", SCENARIO.scenario_body.player_starting_locations_tag_block.definition)
        print(" ")

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    return SCENARIO
