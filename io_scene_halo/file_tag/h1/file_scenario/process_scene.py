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

import bpy

from math import degrees
from .format import ScenarioAsset
from ....global_functions import global_functions, tag_format

def get_palette_index(TAG, SCENARIO, tag_group, tag_path, palette_tag_block):
    palette_index = -1
    for palette_element_idx, palette_element in enumerate(palette_tag_block):
        if palette_element.name == tag_path:
            palette_index = palette_element_idx
            break

    if palette_index == -1 and not global_functions.string_empty_check(tag_group):
        palette_tag_block.append(TAG.TagRef(tag_group, tag_path, len(tag_path)))
        palette_index = len(palette_tag_block) - 1

    return palette_index

def get_half_angle(angle):
    angle =  angle % 360
    angle = (angle + 360) % 360
    if angle > 180:
        angle -= 360

    return angle

def generate_comments(TAG, SCENARIO):
    comment_collection = bpy.data.collections.get("Comments")
    blender_comments = []
    ob_index = 0
    if comment_collection:
        for ob in comment_collection.objects:
            comment = SCENARIO.Comment()
            comment.position = ob.location / 100
            comment.text = ob.data.body
            comment.data = TAG.RawData(len(comment.text) + 1)

            blender_comments.append(comment)

    SCENARIO.comments = blender_comments

def generate_scenery(TAG, SCENARIO):
    scenery_collection = bpy.data.collections.get("Scenery")
    blender_scenery = []
    ob_index = 0
    if scenery_collection:
        for ob in scenery_collection.objects:
            scenery = SCENARIO.Object()
            scenery.type_index = get_palette_index(TAG, SCENARIO, "scen", ob.ass_jms.tag_path, SCENARIO.scenery_palette)
            scenery.name_index = -1
            scenery.placement_flags = 0
            scenery.desired_permutation = 0
            scenery.position = ob.location / 100
            rot = ob.rotation_euler
            scenery.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            scenery.appearance_player_index = 0

            blender_scenery.append(scenery)

    SCENARIO.scenery = blender_scenery

def generate_bipeds(TAG, SCENARIO):
    biped_collection = bpy.data.collections.get("Bipeds")
    blender_bipeds = []
    ob_index = 0
    if biped_collection:
        for ob in biped_collection.objects:
            biped = SCENARIO.Unit()
            biped.type_index = get_palette_index(TAG, SCENARIO, "bipd", ob.ass_jms.tag_path, SCENARIO.biped_palette)
            biped.name_index = -1
            biped.placement_flags = 0
            biped.desired_permutation = 0
            biped.position = ob.location / 100
            rot = ob.rotation_euler
            biped.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            biped.appearance_player_index = 0
            biped.body_vitality = 0.0
            biped.flags = 0

            blender_bipeds.append(biped)

    SCENARIO.bipeds = blender_bipeds

def generate_vehicles(TAG, SCENARIO):
    vehicle_collection = bpy.data.collections.get("Vehicles")
    blender_vehicles = []
    ob_index = 0
    if vehicle_collection:
        for ob in vehicle_collection.objects:
            vehicle = SCENARIO.Vehicle()
            vehicle.type_index = get_palette_index(TAG, SCENARIO, "vehi", ob.ass_jms.tag_path, SCENARIO.vehicle_palette)
            vehicle.name_index = -1
            vehicle.placement_flags = 0
            vehicle.desired_permutation = 0
            vehicle.position = ob.location / 100
            rot = ob.matrix_world.to_euler
            vehicle.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            vehicle.appearance_player_index = 0
            vehicle.body_vitality = 0.0
            vehicle.flags = 0
            vehicle.multiplayer_team_index = 0
            vehicle.multiplayer_spawn_flags = 0

            blender_vehicles.append(vehicle)

    SCENARIO.vehicles = blender_vehicles

def generate_equipment(TAG, SCENARIO):
    equipment_collection = bpy.data.collections.get("Equipment")
    blender_equipment = []
    ob_index = 0
    if equipment_collection:
        for ob in equipment_collection.objects:
            equipment = SCENARIO.Equipment()
            equipment.type_index = get_palette_index(TAG, SCENARIO, "eqip", ob.ass_jms.tag_path, SCENARIO.equipment_palette)
            equipment.name_index = -1
            equipment.placement_flags = 0
            equipment.desired_permutation = 0
            equipment.position = ob.location / 100
            rot = ob.rotation_euler
            equipment.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            equipment.appearance_player_index = 0
            equipment.misc_flags = 0

            blender_equipment.append(equipment)

    SCENARIO.equipment = blender_equipment

def generate_weapons(TAG, SCENARIO):
    weapon_collection = bpy.data.collections.get("Weapons")
    blender_weapons = []
    ob_index = 0
    if weapon_collection:
        for ob in weapon_collection.objects:
            weapon = SCENARIO.Weapon()
            weapon.type_index = get_palette_index(TAG, SCENARIO, "weap", ob.ass_jms.tag_path, SCENARIO.weapon_palette)
            weapon.name_index = -1
            weapon.placement_flags = 0
            weapon.desired_permutation = 0
            weapon.position = ob.location / 100
            rot = ob.rotation_euler
            weapon.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            weapon.appearance_player_index = 0
            weapon.rounds_left = 0
            weapon.rounds_loaded = 0
            weapon.flags = 0

            blender_weapons.append(weapon)

    SCENARIO.weapons = blender_weapons

def generate_machines(TAG, SCENARIO):
    machines_collection = bpy.data.collections.get("Machines")
    blender_machines = []
    ob_index = 0
    if machines_collection:
        for ob in machines_collection.objects:
            machine = SCENARIO.DeviceMachine()
            machine.type_index = get_palette_index(TAG, SCENARIO, "mach", ob.ass_jms.tag_path, SCENARIO.device_machine_palette)
            machine.name_index = -1
            machine.placement_flags = 0
            machine.desired_permutation = 0
            machine.position = ob.location / 100
            rot = ob.rotation_euler
            machine.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            machine.appearance_player_index = 0
            machine.power_group_index = 0
            machine.position_group_index = 0
            machine.flags_0 = 0
            machine.flags_1 = 0

            blender_machines.append(machine)

    SCENARIO.device_machines = blender_machines

def generate_controls(TAG, SCENARIO):
    controls_collection = bpy.data.collections.get("Controls")
    blender_controls = []
    ob_index = 0
    if controls_collection:
        for ob in controls_collection.objects:
            control = SCENARIO.DeviceMachine()
            control.type_index = get_palette_index(TAG, SCENARIO, "ctrl", ob.ass_jms.tag_path, SCENARIO.device_control_palette)
            control.name_index = -1
            control.placement_flags = 0
            control.desired_permutation = 0
            control.position = ob.location / 100
            rot = ob.rotation_euler
            control.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            control.appearance_player_index = 0
            control.power_group_index = 0
            control.position_group_index = 0
            control.flags_0 = 0
            control.flags_1 = 0
            control.unknown = 0

            blender_controls.append(control)

    SCENARIO.device_controls = blender_controls

def generate_light_fixtures(TAG, SCENARIO):
    light_fixtures_collection = bpy.data.collections.get("Light Fixtures")
    blender_light_fixtures = []
    ob_index = 0
    if light_fixtures_collection:
        for ob in light_fixtures_collection.objects:
            light_fixture = SCENARIO.DeviceLightFixture()
            light_fixture.type_index = get_palette_index(TAG, SCENARIO, "lifi", ob.ass_jms.tag_path, SCENARIO.device_light_fixtures_palette)
            light_fixture.name_index = -1
            light_fixture.placement_flags = 0
            light_fixture.desired_permutation = 0
            light_fixture.position = ob.location / 100
            rot = ob.rotation_euler
            light_fixture.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            light_fixture.appearance_player_index = 0
            light_fixture.power_group_index = 0
            light_fixture.position_group_index = 0
            light_fixture.flags = 0
            light_fixture.color_RGBA = (0.0, 0.0, 0.0, 1.0)
            light_fixture.intensity = 0
            light_fixture.falloff_angle = 0
            light_fixture.cutoff_angle = 0

            blender_light_fixtures.append(light_fixture)

    SCENARIO.device_light_fixtures = blender_light_fixtures

def generate_sound_scenery(TAG, SCENARIO):
    sound_scenery_collection = bpy.data.collections.get("Sound Scenery")
    blender_sound_scenery = []
    ob_index = 0
    if sound_scenery_collection:
        for ob in sound_scenery_collection.objects:
            sound_scenery = SCENARIO.Object()
            sound_scenery.type_index = get_palette_index(TAG, SCENARIO, "ssce", ob.ass_jms.tag_path, SCENARIO.sound_scenery_palette)
            sound_scenery.name_index = -1
            sound_scenery.placement_flags = 0
            sound_scenery.desired_permutation = 0
            sound_scenery.position = ob.location / 100
            rot = ob.rotation_euler
            rot.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            sound_scenery.appearance_player_index = 0

            blender_sound_scenery.append(sound_scenery)

    SCENARIO.sound_scenery = blender_sound_scenery

def generate_player_starting_locations(TAG, SCENARIO):
    player_starting_locations_collection = bpy.data.collections.get("Player Starting Locations")
    blender_player_starting_locations = []
    ob_index = 0
    if player_starting_locations_collection:
        for ob in player_starting_locations_collection.objects:
            player_starting_location = SCENARIO.PlayerStartingLocation()
            rot = ob.rotation_euler

            player_starting_location.position = ob.location / 100
            player_starting_location.facing = get_half_angle(degrees(rot[2]))
            player_starting_location.team_index = 0
            player_starting_location.bsp_index = 0
            player_starting_location.type_0 = 0
            player_starting_location.type_1 = 0
            player_starting_location.type_2 = 0
            player_starting_location.type_3 = 0

            blender_player_starting_locations.append(player_starting_location)

    SCENARIO.player_starting_locations = blender_player_starting_locations

def generate_trigger_volumes(TAG, SCENARIO):
    trigger_volumes_collection = bpy.data.collections.get("Trigger Volumes")
    blender_trigger_volumes = []
    ob_index = 0
    if trigger_volumes_collection:
        for ob in trigger_volumes_collection.objects:
            trigger_volume = SCENARIO.TriggerVolume()
            rot = ob.matrix_world.normalized()

            trigger_volume.name = ob.name
            trigger_volume.forward = rot[0]
            trigger_volume.up = rot[2]
            trigger_volume.position = ob.location / 100
            trigger_volume.extents = ob.dimensions / 100

            blender_trigger_volumes.append(trigger_volume)

    SCENARIO.trigger_volumes = blender_trigger_volumes

def create_tag(TAG):
    SCENARIO = ScenarioAsset()
    TAG.is_legacy = False

    SCENARIO.header = TAG.Header()
    SCENARIO.header.unk1 = 0
    SCENARIO.header.flags = 0
    SCENARIO.header.type = 0
    SCENARIO.header.name = ""
    SCENARIO.header.tag_group = "scnr"
    SCENARIO.header.checksum = -1
    SCENARIO.header.data_offset = 64
    SCENARIO.header.data_length = 0
    SCENARIO.header.unk2 = 0
    SCENARIO.header.version = 2
    SCENARIO.header.destination = 0
    SCENARIO.header.plugin_handle = -1
    SCENARIO.header.engine_tag = "blam"

    SCENARIO.scenario_body = SCENARIO.ScenarioBody()
    SCENARIO.scenario_body.dont_use_tag_ref = TAG.TagRef()
    SCENARIO.scenario_body.wont_use_tag_ref = TAG.TagRef()
    SCENARIO.scenario_body.cant_use_tag_ref = TAG.TagRef()
    SCENARIO.scenario_body.skies_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.child_scenarios_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.predicted_resources_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.functions_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.editor_scenario_data = TAG.RawData()
    SCENARIO.scenario_body.comments_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.scavenger_hunt_objects_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.object_names_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.scenery_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.scenery_palette_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.bipeds_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.biped_palette_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.vehicles_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.vehicle_palette_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.equipment_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.equipment_palette_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.weapons_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.weapon_palette_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.device_groups_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.machines_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.machine_palette_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.controls_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.control_palette_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.light_fixtures_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.light_fixtures_palette_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.sound_scenery_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.sound_scenery_palette_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.player_starting_profile_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.player_starting_locations_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.trigger_volumes_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.recorded_animations_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.netgame_flags_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.netgame_equipment_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.starting_equipment_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.bsp_switch_trigger_volumes_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.decals_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.decal_palette_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.detail_object_collection_palette_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.actor_palette_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.encounters_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.command_lists_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.ai_animation_references_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.ai_script_references_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.ai_recording_references_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.ai_conversations_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.script_syntax_data_tag_data = TAG.RawData()
    SCENARIO.scenario_body.script_string_data_tag_data = TAG.RawData()
    SCENARIO.scenario_body.scripts_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.globals_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.references_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.source_files_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.cutscene_flags_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.cutscene_camera_points_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.cutscene_titles_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.custom_object_names_tag_ref = TAG.TagRef()
    SCENARIO.scenario_body.chapter_title_text_tag_ref = TAG.TagRef()
    SCENARIO.scenario_body.hud_messages_tag_ref = TAG.TagRef()
    SCENARIO.scenario_body.structure_bsps_tag_block = TAG.TagBlock()

    SCENARIO.skies = []
    SCENARIO.child_scenarios = []
    SCENARIO.predicted_resources = []
    SCENARIO.functions = []
    SCENARIO.editor_scenario_data = bytes()
    SCENARIO.comments = []
    SCENARIO.scavenger_hunt_objects = []
    SCENARIO.object_names = []
    SCENARIO.scenery = []
    SCENARIO.scenery_palette = []
    SCENARIO.bipeds = []
    SCENARIO.biped_palette = []
    SCENARIO.vehicles = []
    SCENARIO.vehicle_palette = []
    SCENARIO.equipment = []
    SCENARIO.equipment_palette = []
    SCENARIO.weapons = []
    SCENARIO.weapon_palette = []
    SCENARIO.device_groups = []
    SCENARIO.device_machines = []
    SCENARIO.device_machine_palette = []
    SCENARIO.device_controls = []
    SCENARIO.device_control_palette = []
    SCENARIO.device_light_fixtures = []
    SCENARIO.device_light_fixtures_palette = []
    SCENARIO.sound_scenery = []
    SCENARIO.sound_scenery_palette = []
    SCENARIO.player_starting_profiles = []
    SCENARIO.player_starting_locations = []
    SCENARIO.trigger_volumes = []
    SCENARIO.recorded_animations = []
    SCENARIO.netgame_flags = []
    SCENARIO.netgame_equipment = []
    SCENARIO.starting_equipment = []
    SCENARIO.bsp_switch_trigger_volumes = []
    SCENARIO.decals = []
    SCENARIO.decal_palette = []
    SCENARIO.detail_object_collection_palette  = []
    SCENARIO.actor_palette = []
    SCENARIO.encounters = []
    SCENARIO.command_lists = []
    SCENARIO.ai_animation_references = []
    SCENARIO.ai_script_references = []
    SCENARIO.ai_recording_references = []
    SCENARIO.ai_conversations = []
    SCENARIO.script_syntax_data = bytes()
    SCENARIO.script_string_data = bytes()
    SCENARIO.scripts = []
    SCENARIO.globals = []
    SCENARIO.references = []
    SCENARIO.source_files = []
    SCENARIO.cutscene_flags = []
    SCENARIO.cutscene_camera_points = []
    SCENARIO.cutscene_titles = []
    SCENARIO.structure_bsps = []

    return SCENARIO

def generate_scenario_scene(DONOR_ASSET):
    TAG = tag_format.TagAsset()

    if DONOR_ASSET == None:
        DONOR_ASSET = create_tag(TAG)

    generate_comments(TAG, DONOR_ASSET)
    generate_scenery(TAG, DONOR_ASSET)
    generate_bipeds(TAG, DONOR_ASSET)
    generate_vehicles(TAG, DONOR_ASSET)
    generate_equipment(TAG, DONOR_ASSET)
    generate_weapons(TAG, DONOR_ASSET)
    generate_machines(TAG, DONOR_ASSET)
    generate_controls(TAG, DONOR_ASSET)
    generate_light_fixtures(TAG, DONOR_ASSET)
    generate_sound_scenery(TAG, DONOR_ASSET)
    generate_player_starting_locations(TAG, DONOR_ASSET)
    generate_trigger_volumes(TAG, DONOR_ASSET)

    DONOR_ASSET.scenario_body.scenery_tag_block = TAG.TagBlock(len(DONOR_ASSET.scenery))
    DONOR_ASSET.scenario_body.scenery_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.scenery_palette))
    DONOR_ASSET.scenario_body.bipeds_tag_block = TAG.TagBlock(len(DONOR_ASSET.bipeds))
    DONOR_ASSET.scenario_body.biped_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.biped_palette))
    DONOR_ASSET.scenario_body.vehicles_tag_block = TAG.TagBlock(len(DONOR_ASSET.vehicles))
    DONOR_ASSET.scenario_body.vehicle_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.vehicle_palette))
    DONOR_ASSET.scenario_body.equipment_tag_block = TAG.TagBlock(len(DONOR_ASSET.equipment))
    DONOR_ASSET.scenario_body.equipment_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.equipment_palette))
    DONOR_ASSET.scenario_body.weapons_tag_block = TAG.TagBlock(len(DONOR_ASSET.weapons))
    DONOR_ASSET.scenario_body.weapon_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.weapon_palette))
    DONOR_ASSET.scenario_body.machines_tag_block = TAG.TagBlock(len(DONOR_ASSET.device_machines))
    DONOR_ASSET.scenario_body.machine_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.device_machine_palette))
    DONOR_ASSET.scenario_body.controls_tag_block = TAG.TagBlock(len(DONOR_ASSET.device_controls))
    DONOR_ASSET.scenario_body.control_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.device_control_palette))
    DONOR_ASSET.scenario_body.light_fixtures_tag_block = TAG.TagBlock(len(DONOR_ASSET.device_light_fixtures))
    DONOR_ASSET.scenario_body.light_fixtures_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.device_light_fixtures_palette))
    DONOR_ASSET.scenario_body.sound_scenery_tag_block = TAG.TagBlock(len(DONOR_ASSET.sound_scenery))
    DONOR_ASSET.scenario_body.sound_scenery_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.sound_scenery_palette))
    DONOR_ASSET.scenario_body.player_starting_locations_tag_block = TAG.TagBlock(len(DONOR_ASSET.player_starting_locations))
    DONOR_ASSET.scenario_body.trigger_volumes_tag_block = TAG.TagBlock(len(DONOR_ASSET.trigger_volumes))

    return DONOR_ASSET
