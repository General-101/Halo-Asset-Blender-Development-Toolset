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
from .format import ScenarioAsset, ObjectFlags, UnitFlags, VehicleFlags, ItemFlags, DeviceFlags, MachineFlags, ControlFlags, NetGameEquipment
from ....global_functions import global_functions, tag_format

def get_palette_index(TAG, SCENARIO, tag_group, tag_path, palette_tag_block):
    palette_index = -1
    for palette_element_idx, palette_element in enumerate(palette_tag_block):
        if palette_element.name == tag_path:
            palette_index = palette_element_idx
            break

    if palette_index == -1 and not global_functions.string_empty_check(tag_group) and not global_functions.string_empty_check(tag_path):
        palette_tag_block.append(TAG.TagRef(tag_group, tag_path, len(tag_path)))
        palette_index = len(palette_tag_block) - 1

    return palette_index

def get_half_angle(angle):
    angle =  angle % 360
    angle = (angle + 360) % 360
    if angle > 180:
        angle -= 360

    return angle

def get_object_name_index(SCENARIO, object_name):
    object_name_index = -1
    if not global_functions.string_empty_check(object_name):
        if not object_name in SCENARIO.object_names:
            SCENARIO.object_names.append(object_name)

        object_name_index = SCENARIO.object_names.index(object_name)

    return object_name_index

def get_object_flags(ob):
    object_flags = 0
    if ob.tag_view.automatically:
        object_flags += ObjectFlags.automatically.value
    if ob.tag_view.on_easy:
        object_flags += ObjectFlags.on_easy.value
    if ob.tag_view.on_normal:
        object_flags += ObjectFlags.on_normal.value
    if ob.tag_view.on_hard:
        object_flags += ObjectFlags.on_hard.value
    if ob.tag_view.use_player_appearance:
        object_flags += ObjectFlags.use_player_appearance.value
    return object_flags

def get_unit_flags(ob):
    unit_flags = 0
    if ob.tag_view.unit_dead:
        unit_flags += UnitFlags.dead.value
    return unit_flags

def get_vehicle_flags(ob):
    vehicle_flags = 0
    if ob.tag_view.slayer_default:
        vehicle_flags += VehicleFlags.slayer_default.value
    if ob.tag_view.ctf_default:
        vehicle_flags += VehicleFlags.ctf_default.value
    if ob.tag_view.king_default:
        vehicle_flags += VehicleFlags.king_default.value
    if ob.tag_view.oddball_default:
        vehicle_flags += VehicleFlags.oddball_default.value
    if ob.tag_view.unused_0:
        vehicle_flags += VehicleFlags.unused0.value
    if ob.tag_view.unused_1:
        vehicle_flags += VehicleFlags.unused1.value
    if ob.tag_view.unused_2:
        vehicle_flags += VehicleFlags.unused2.value
    if ob.tag_view.unused_3:
        vehicle_flags += VehicleFlags.unused3.value
    if ob.tag_view.slayer_allowed:
        vehicle_flags += VehicleFlags.slayer_allowed.value
    if ob.tag_view.ctf_allowed:
        vehicle_flags += VehicleFlags.ctf_allowed.value
    if ob.tag_view.king_allowed:
        vehicle_flags += VehicleFlags.king_allowed.value
    if ob.tag_view.oddball_allowed:
        vehicle_flags += VehicleFlags.oddball_allowed.value
    if ob.tag_view.unused_4:
        vehicle_flags += VehicleFlags.unused4.value
    if ob.tag_view.unused_5:
        vehicle_flags += VehicleFlags.unused5.value
    if ob.tag_view.unused_6:
        vehicle_flags += VehicleFlags.unused6.value
    if ob.tag_view.unused_7:
        vehicle_flags += VehicleFlags.unused7.value

    return vehicle_flags

def get_item_flags(ob):
    item_flags = 0
    if ob.tag_view.initially_at_rest:
        item_flags += ItemFlags.initially_at_rest_doesnt_fall.value
    if ob.tag_view.obsolete:
        item_flags += ItemFlags.obsolete.value
    if ob.tag_view.does_accelerate:
        item_flags += ItemFlags.does_accelerate_moves_due_to_explosions.value

    return item_flags

def get_device_flags(ob):
    device_flags = 0
    if ob.tag_view.initially_open:
        device_flags += DeviceFlags.initially_open.value
    if ob.tag_view.initially_off:
        device_flags += DeviceFlags.initially_off.value
    if ob.tag_view.can_change_only_once:
        device_flags += DeviceFlags.can_change_only_once.value
    if ob.tag_view.position_reversed:
        device_flags += DeviceFlags.position_reversed.value
    if ob.tag_view.not_usable_from_any_side:
        device_flags += DeviceFlags.not_usable_from_any_side.value
    return device_flags

def get_machine_flags(ob):
    machine_flags = 0
    if ob.tag_view.does_not_operate_automatically:
        machine_flags += MachineFlags.does_not_operate_automatically.value
    if ob.tag_view.one_sided:
        machine_flags += MachineFlags.one_sided.value
    if ob.tag_view.never_appears_locked:
        machine_flags += MachineFlags.never_appears_locked.value
    if ob.tag_view.opened_by_melee_attack:
        machine_flags += MachineFlags.opened_by_melee_attack.value
    return machine_flags

def get_control_flags(ob):
    control_flags = 0
    if ob.tag_view.usable_from_both_sides:
        control_flags += ControlFlags.usable_from_both_sides.value
    return control_flags

def get_netgame_equipment_flags(ob):
    netgame_equipment_flags = 0
    if ob.tag_view.levitate:
        netgame_equipment_flags += NetGameEquipment.levitate.value
    return netgame_equipment_flags

def generate_comments(TAG, SCENARIO):
    comment_collection = bpy.data.collections.get("Comments")
    blender_comments = []
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
    if scenery_collection:
        for ob in scenery_collection.objects:
            scenery = SCENARIO.Object()
            scenery.type_index = get_palette_index(TAG, SCENARIO, "scen", ob.tag_view.tag_path, SCENARIO.scenery_palette)
            scenery.name_index = get_object_name_index(SCENARIO, ob.tag_view.object_name)
            scenery.placement_flags = get_object_flags(ob)
            scenery.desired_permutation = ob.tag_view.desired_permutation
            scenery.position = ob.location / 100
            rot = ob.rotation_euler
            scenery.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            scenery.appearance_player_index = ob.tag_view.appearance_player_index

            blender_scenery.append(scenery)

    SCENARIO.scenery = blender_scenery

def generate_bipeds(TAG, SCENARIO):
    biped_collection = bpy.data.collections.get("Biped")
    blender_bipeds = []
    if biped_collection:
        for ob in biped_collection.objects:
            biped = SCENARIO.Unit()
            biped.type_index = get_palette_index(TAG, SCENARIO, "bipd", ob.tag_view.tag_path, SCENARIO.biped_palette)
            biped.name_index = get_object_name_index(SCENARIO, ob.tag_view.object_name)
            biped.placement_flags = get_object_flags(ob)
            biped.desired_permutation = ob.tag_view.desired_permutation
            biped.position = ob.location / 100
            rot = ob.rotation_euler
            biped.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            biped.appearance_player_index = ob.tag_view.appearance_player_index
            biped.body_vitality = ob.tag_view.unit_vitality
            biped.flags = get_unit_flags(ob)

            blender_bipeds.append(biped)

    SCENARIO.bipeds = blender_bipeds

def generate_vehicles(TAG, SCENARIO):
    vehicle_collection = bpy.data.collections.get("Vehicle")
    blender_vehicles = []
    if vehicle_collection:
        for ob in vehicle_collection.objects:
            vehicle = SCENARIO.Vehicle()
            vehicle.type_index = get_palette_index(TAG, SCENARIO, "vehi", ob.tag_view.tag_path, SCENARIO.vehicle_palette)
            vehicle.name_index = get_object_name_index(SCENARIO, ob.tag_view.object_name)
            vehicle.placement_flags = get_object_flags(ob)
            vehicle.desired_permutation = ob.tag_view.desired_permutation
            vehicle.position = ob.location / 100
            rot = ob.rotation_euler
            vehicle.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            vehicle.appearance_player_index = ob.tag_view.appearance_player_index
            vehicle.body_vitality = ob.tag_view.unit_vitality
            vehicle.flags = get_unit_flags(ob)
            vehicle.multiplayer_team_index = ob.tag_view.multiplayer_team_index
            vehicle.multiplayer_spawn_flags = get_vehicle_flags(ob)

            blender_vehicles.append(vehicle)

    SCENARIO.vehicles = blender_vehicles

def generate_equipment(TAG, SCENARIO):
    equipment_collection = bpy.data.collections.get("Equipment")
    blender_equipment = []
    if equipment_collection:
        for ob in equipment_collection.objects:
            equipment = SCENARIO.Equipment()
            equipment.type_index = get_palette_index(TAG, SCENARIO, "eqip", ob.tag_view.tag_path, SCENARIO.equipment_palette)
            equipment.name_index = get_object_name_index(SCENARIO, ob.tag_view.object_name)
            equipment.placement_flags = get_object_flags(ob)
            equipment.desired_permutation = ob.tag_view.desired_permutation
            equipment.position = ob.location / 100
            rot = ob.rotation_euler
            equipment.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            equipment.appearance_player_index = ob.tag_view.appearance_player_index
            equipment.misc_flags = get_item_flags(ob)

            blender_equipment.append(equipment)

    SCENARIO.equipment = blender_equipment

def generate_weapons(TAG, SCENARIO):
    weapon_collection = bpy.data.collections.get("Weapons")
    blender_weapons = []
    if weapon_collection:
        for ob in weapon_collection.objects:
            weapon = SCENARIO.Weapon()
            weapon.type_index = get_palette_index(TAG, SCENARIO, "weap", ob.tag_view.tag_path, SCENARIO.weapon_palette)
            weapon.name_index = get_object_name_index(SCENARIO, ob.tag_view.object_name)
            weapon.placement_flags = get_object_flags(ob)
            weapon.desired_permutation = ob.tag_view.desired_permutation
            weapon.position = ob.location / 100
            rot = ob.rotation_euler
            weapon.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            weapon.appearance_player_index = ob.tag_view.appearance_player_index
            weapon.rounds_left = ob.tag_view.rounds_left
            weapon.rounds_loaded = ob.tag_view.rounds_loaded
            weapon.flags = get_item_flags(ob)

            blender_weapons.append(weapon)

    SCENARIO.weapons = blender_weapons

def generate_machines(TAG, SCENARIO):
    machines_collection = bpy.data.collections.get("Machines")
    blender_machines = []
    if machines_collection:
        for ob in machines_collection.objects:
            machine = SCENARIO.DeviceMachine()
            machine.type_index = get_palette_index(TAG, SCENARIO, "mach", ob.tag_view.tag_path, SCENARIO.device_machine_palette)
            machine.name_index = get_object_name_index(SCENARIO, ob.tag_view.object_name)
            machine.placement_flags = get_object_flags(ob)
            machine.desired_permutation = ob.tag_view.desired_permutation
            machine.position = ob.location / 100
            rot = ob.rotation_euler
            machine.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            machine.appearance_player_index = ob.tag_view.appearance_player_index
            machine.power_group_index = ob.tag_view.power_group
            machine.position_group_index = ob.tag_view.position_group
            machine.flags_0 = get_device_flags(ob)
            machine.flags_1 = get_machine_flags(ob)

            blender_machines.append(machine)

    SCENARIO.device_machines = blender_machines

def generate_controls(TAG, SCENARIO):
    controls_collection = bpy.data.collections.get("Controls")
    blender_controls = []
    if controls_collection:
        for ob in controls_collection.objects:
            control = SCENARIO.DeviceMachine()
            control.type_index = get_palette_index(TAG, SCENARIO, "ctrl", ob.tag_view.tag_path, SCENARIO.device_control_palette)
            control.name_index = get_object_name_index(SCENARIO, ob.tag_view.object_name)
            control.placement_flags = get_object_flags(ob)
            control.desired_permutation = ob.tag_view.desired_permutation
            control.position = ob.location / 100
            rot = ob.rotation_euler
            control.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            control.appearance_player_index = ob.tag_view.appearance_player_index
            control.power_group_index = ob.tag_view.power_group
            control.position_group_index = ob.tag_view.position_group
            control.flags_0 = get_device_flags(ob)
            control.flags_1 = get_control_flags(ob)
            control.unknown = ob.tag_view.control_value

            blender_controls.append(control)

    SCENARIO.device_controls = blender_controls

def generate_light_fixtures(TAG, SCENARIO):
    light_fixtures_collection = bpy.data.collections.get("Light Fixtures")
    blender_light_fixtures = []
    if light_fixtures_collection:
        for ob in light_fixtures_collection.objects:
            light_fixture = SCENARIO.DeviceLightFixture()
            light_fixture.type_index = get_palette_index(TAG, SCENARIO, "lifi", ob.tag_view.tag_path, SCENARIO.device_light_fixtures_palette)
            light_fixture.name_index = get_object_name_index(SCENARIO, ob.tag_view.object_name)
            light_fixture.placement_flags = get_object_flags(ob)
            light_fixture.desired_permutation = ob.tag_view.desired_permutation
            light_fixture.position = ob.location / 100
            rot = ob.rotation_euler
            light_fixture.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            light_fixture.appearance_player_index = ob.tag_view.appearance_player_index
            light_fixture.power_group_index = ob.tag_view.power_group
            light_fixture.position_group_index = ob.tag_view.position_group
            light_fixture.flags = get_device_flags(ob)
            light_fixture.color_RGBA = (ob.tag_view.color[0], ob.tag_view.color[1], ob.tag_view.color[2], 1)
            light_fixture.intensity = ob.tag_view.intensity
            light_fixture.falloff_angle = ob.tag_view.falloff_angle
            light_fixture.cutoff_angle = ob.tag_view.cutoff_angle

            blender_light_fixtures.append(light_fixture)

    SCENARIO.device_light_fixtures = blender_light_fixtures

def generate_sound_scenery(TAG, SCENARIO):
    sound_scenery_collection = bpy.data.collections.get("Sound Scenery")
    blender_sound_scenery = []
    if sound_scenery_collection:
        for ob in sound_scenery_collection.objects:
            sound_scenery = SCENARIO.Object()
            sound_scenery.type_index = get_palette_index(TAG, SCENARIO, "ssce", ob.tag_view.tag_path, SCENARIO.sound_scenery_palette)
            sound_scenery.name_index = get_object_name_index(SCENARIO, ob.tag_view.object_name)
            sound_scenery.placement_flags = get_object_flags(ob)
            sound_scenery.desired_permutation = ob.tag_view.desired_permutation
            sound_scenery.position = ob.location / 100
            rot = ob.rotation_euler
            sound_scenery.rotation = (get_half_angle(degrees(rot[2])), get_half_angle(degrees(-rot[0])), get_half_angle(degrees(-rot[1])))
            sound_scenery.appearance_player_index = ob.tag_view.appearance_player_index

            blender_sound_scenery.append(sound_scenery)

    SCENARIO.sound_scenery = blender_sound_scenery

def generate_player_starting_locations(TAG, SCENARIO):
    player_starting_locations_collection = bpy.data.collections.get("Player Starting Locations")
    blender_player_starting_locations = []
    if player_starting_locations_collection:
        for ob in player_starting_locations_collection.objects:
            player_starting_location = SCENARIO.PlayerStartingLocation()
            rot = ob.rotation_euler

            player_starting_location.position = ob.location / 100
            player_starting_location.facing = get_half_angle(degrees(rot[2]))
            player_starting_location.team_index = ob.tag_view.team_index
            player_starting_location.bsp_index = ob.tag_view.bsp_index
            player_starting_location.type_0 = int(ob.tag_view.type_0)
            player_starting_location.type_1 = int(ob.tag_view.type_1)
            player_starting_location.type_2 = int(ob.tag_view.type_2)
            player_starting_location.type_3 = int(ob.tag_view.type_3)

            blender_player_starting_locations.append(player_starting_location)

    SCENARIO.player_starting_locations = blender_player_starting_locations

def generate_trigger_volumes(TAG, SCENARIO):
    trigger_volumes_collection = bpy.data.collections.get("Trigger Volumes")
    blender_trigger_volumes = []
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

def generate_netgame_flags(TAG, SCENARIO):
    netgame_flags_collection = bpy.data.collections.get("Netgame Flags")
    blender_netgame_flags = []
    if netgame_flags_collection:
        for ob in netgame_flags_collection.objects:
            netgame_flag = SCENARIO.NetGameFlag()
            rot = ob.rotation_euler

            netgame_flag.position = ob.location / 100
            netgame_flag.facing = get_half_angle(degrees(rot[2]))
            netgame_flag.type = int(ob.tag_view.netgame_type)
            netgame_flag.usage_id = ob.tag_view.usage_id
            netgame_flag.weapon_group = TAG.TagRef("weap", ob.tag_view.tag_path, len(ob.tag_view.tag_path))

            blender_netgame_flags.append(netgame_flag)

    SCENARIO.netgame_flags = blender_netgame_flags

def generate_netgame_equipment(TAG, SCENARIO):
    netgame_equipment_collection = bpy.data.collections.get("Netgame Equipment")
    blender_netgame_equipment = []
    if netgame_equipment_collection:
        for ob in netgame_equipment_collection.objects:
            netgame_equipment = SCENARIO.NetGameEquipment()
            rot = ob.rotation_euler

            netgame_equipment.flags = get_netgame_equipment_flags(ob)
            netgame_equipment.type_0 = int(ob.tag_view.type_0)
            netgame_equipment.type_1 = int(ob.tag_view.type_1)
            netgame_equipment.type_2 = int(ob.tag_view.type_2)
            netgame_equipment.type_3 = int(ob.tag_view.type_3)
            netgame_equipment.team_index = ob.tag_view.team_index
            netgame_equipment.spawn_time = ob.tag_view.spawn_time
            netgame_equipment.position = ob.location / 100
            netgame_equipment.facing = get_half_angle(degrees(rot[2]))
            netgame_equipment.item_collection = TAG.TagRef("itmc", ob.tag_view.tag_path, len(ob.tag_view.tag_path))

            blender_netgame_equipment.append(netgame_equipment)

    SCENARIO.netgame_equipment = blender_netgame_equipment

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

    SCENARIO.dont_use_tag_ref = TAG.TagRef()
    SCENARIO.wont_use_tag_ref = TAG.TagRef()
    SCENARIO.cant_use_tag_ref = TAG.TagRef()
    SCENARIO.skies_tag_block = TAG.TagBlock()
    SCENARIO.child_scenarios_tag_block = TAG.TagBlock()
    SCENARIO.predicted_resources_tag_block = TAG.TagBlock()
    SCENARIO.functions_tag_block = TAG.TagBlock()
    SCENARIO.comments_tag_block = TAG.TagBlock()
    SCENARIO.scavenger_hunt_objects_tag_block = TAG.TagBlock()
    SCENARIO.object_names_tag_block = TAG.TagBlock()
    SCENARIO.scenery_tag_block = TAG.TagBlock()
    SCENARIO.scenery_palette_tag_block = TAG.TagBlock()
    SCENARIO.bipeds_tag_block = TAG.TagBlock()
    SCENARIO.biped_palette_tag_block = TAG.TagBlock()
    SCENARIO.vehicles_tag_block = TAG.TagBlock()
    SCENARIO.vehicle_palette_tag_block = TAG.TagBlock()
    SCENARIO.equipment_tag_block = TAG.TagBlock()
    SCENARIO.equipment_palette_tag_block = TAG.TagBlock()
    SCENARIO.weapons_tag_block = TAG.TagBlock()
    SCENARIO.weapon_palette_tag_block = TAG.TagBlock()
    SCENARIO.device_groups_tag_block = TAG.TagBlock()
    SCENARIO.machines_tag_block = TAG.TagBlock()
    SCENARIO.machine_palette_tag_block = TAG.TagBlock()
    SCENARIO.controls_tag_block = TAG.TagBlock()
    SCENARIO.control_palette_tag_block = TAG.TagBlock()
    SCENARIO.light_fixtures_tag_block = TAG.TagBlock()
    SCENARIO.light_fixtures_palette_tag_block = TAG.TagBlock()
    SCENARIO.sound_scenery_tag_block = TAG.TagBlock()
    SCENARIO.sound_scenery_palette_tag_block = TAG.TagBlock()
    SCENARIO.player_starting_profile_tag_block = TAG.TagBlock()
    SCENARIO.player_starting_locations_tag_block = TAG.TagBlock()
    SCENARIO.trigger_volumes_tag_block = TAG.TagBlock()
    SCENARIO.recorded_animations_tag_block = TAG.TagBlock()
    SCENARIO.netgame_flags_tag_block = TAG.TagBlock()
    SCENARIO.netgame_equipment_tag_block = TAG.TagBlock()
    SCENARIO.starting_equipment_tag_block = TAG.TagBlock()
    SCENARIO.bsp_switch_trigger_volumes_tag_block = TAG.TagBlock()
    SCENARIO.decals_tag_block = TAG.TagBlock()
    SCENARIO.decal_palette_tag_block = TAG.TagBlock()
    SCENARIO.detail_object_collection_palette_tag_block = TAG.TagBlock()
    SCENARIO.actor_palette_tag_block = TAG.TagBlock()
    SCENARIO.encounters_tag_block = TAG.TagBlock()
    SCENARIO.command_lists_tag_block = TAG.TagBlock()
    SCENARIO.ai_animation_references_tag_block = TAG.TagBlock()
    SCENARIO.ai_script_references_tag_block = TAG.TagBlock()
    SCENARIO.ai_recording_references_tag_block = TAG.TagBlock()
    SCENARIO.ai_conversations_tag_block = TAG.TagBlock()
    SCENARIO.script_syntax_data_tag_data = TAG.RawData()
    SCENARIO.script_string_data_tag_data = TAG.RawData()
    SCENARIO.scripts_tag_block = TAG.TagBlock()
    SCENARIO.globals_tag_block = TAG.TagBlock()
    SCENARIO.references_tag_block = TAG.TagBlock()
    SCENARIO.source_files_tag_block = TAG.TagBlock()
    SCENARIO.cutscene_flags_tag_block = TAG.TagBlock()
    SCENARIO.cutscene_camera_points_tag_block = TAG.TagBlock()
    SCENARIO.cutscene_titles_tag_block = TAG.TagBlock()
    SCENARIO.custom_object_names_tag_ref = TAG.TagRef()
    SCENARIO.chapter_title_text_tag_ref = TAG.TagRef()
    SCENARIO.hud_messages_tag_ref = TAG.TagRef()
    SCENARIO.structure_bsps_tag_block = TAG.TagBlock()

    SCENARIO.skies = []
    SCENARIO.child_scenarios = []
    SCENARIO.predicted_resources = []
    SCENARIO.functions = []
    SCENARIO.editor_scenario_data = TAG.RawData()
    SCENARIO.editor_scenario_data.data = bytes()
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
    SCENARIO.script_globals = []
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
    generate_netgame_flags(TAG, DONOR_ASSET)
    generate_netgame_equipment(TAG, DONOR_ASSET)

    DONOR_ASSET.comments_tag_block = TAG.TagBlock(len(DONOR_ASSET.comments))
    DONOR_ASSET.object_names_tag_block = TAG.TagBlock(len(DONOR_ASSET.object_names))
    DONOR_ASSET.scenery_tag_block = TAG.TagBlock(len(DONOR_ASSET.scenery))
    DONOR_ASSET.scenery_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.scenery_palette))
    DONOR_ASSET.bipeds_tag_block = TAG.TagBlock(len(DONOR_ASSET.bipeds))
    DONOR_ASSET.biped_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.biped_palette))
    DONOR_ASSET.vehicles_tag_block = TAG.TagBlock(len(DONOR_ASSET.vehicles))
    DONOR_ASSET.vehicle_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.vehicle_palette))
    DONOR_ASSET.equipment_tag_block = TAG.TagBlock(len(DONOR_ASSET.equipment))
    DONOR_ASSET.equipment_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.equipment_palette))
    DONOR_ASSET.weapons_tag_block = TAG.TagBlock(len(DONOR_ASSET.weapons))
    DONOR_ASSET.weapon_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.weapon_palette))
    DONOR_ASSET.machines_tag_block = TAG.TagBlock(len(DONOR_ASSET.device_machines))
    DONOR_ASSET.machine_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.device_machine_palette))
    DONOR_ASSET.controls_tag_block = TAG.TagBlock(len(DONOR_ASSET.device_controls))
    DONOR_ASSET.control_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.device_control_palette))
    DONOR_ASSET.light_fixtures_tag_block = TAG.TagBlock(len(DONOR_ASSET.device_light_fixtures))
    DONOR_ASSET.light_fixtures_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.device_light_fixtures_palette))
    DONOR_ASSET.sound_scenery_tag_block = TAG.TagBlock(len(DONOR_ASSET.sound_scenery))
    DONOR_ASSET.sound_scenery_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.sound_scenery_palette))
    DONOR_ASSET.player_starting_locations_tag_block = TAG.TagBlock(len(DONOR_ASSET.player_starting_locations))
    DONOR_ASSET.trigger_volumes_tag_block = TAG.TagBlock(len(DONOR_ASSET.trigger_volumes))
    DONOR_ASSET.netgame_flags_tag_block = TAG.TagBlock(len(DONOR_ASSET.netgame_flags))
    DONOR_ASSET.netgame_equipment_tag_block = TAG.TagBlock(len(DONOR_ASSET.netgame_equipment))

    return DONOR_ASSET
