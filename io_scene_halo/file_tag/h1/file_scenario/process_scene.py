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

from mathutils import Euler, Matrix
from math import radians, degrees, cos, sin, asin, atan2
from .format import (ScenarioAsset, 
                     ScenarioFlags, 
                     ObjectFlags, 
                     UnitFlags, 
                     VehicleFlags, 
                     ItemFlags, 
                     DeviceFlags, 
                     MachineFlags, 
                     ControlFlags, 
                     NetGameEquipment,
                     EncounterFlags,
                     SquadFlags,
                     GroupFlags,
                     StartingLocationFlags,
                     PlatoonFlags,
                     CommandListFlags)
from ....global_functions import global_functions, tag_format

def get_palette_index(TAG, tag_path, palette_tag_block):
    palette_index = -1
    if not global_functions.string_empty_check(tag_path):
        tag_path, tag_group = tag_path.rsplit(".", 1)
        tag_group = tag_format.h1_tag_extensions_dic.get(tag_group)
        for palette_element_idx, palette_element in enumerate(palette_tag_block):
            if palette_element.name == tag_path and palette_element.tag_group == tag_group:
                palette_index = palette_element_idx
                break

        if palette_index == -1 and not global_functions.string_empty_check(tag_group) and not global_functions.string_empty_check(tag_path):
            palette_tag_block.append(TAG.TagRef(tag_group, tag_path, len(tag_path)))
            palette_index = len(palette_tag_block) - 1

    return palette_index

def get_tag_reference(TAG, tag_path):
    tag_ref = TAG.TagRef()
    if not global_functions.string_empty_check(tag_path):
        tag_path, tag_group = tag_path.rsplit(".", 1)
        tag_ref = TAG.TagRef(tag_format.h1_tag_extensions_dic.get(tag_group), tag_path, len(tag_path))

    return tag_ref

def get_collection_index(collection_block, referenced_collection):
    block_index = -1
    if not referenced_collection == None:
        for collection_idx, collection_element in enumerate(collection_block):
            if collection_element.name == referenced_collection.name:
                block_index = collection_idx

    return block_index

def matrix_to_euler(rot_matrix):
    yaw = -degrees(atan2(rot_matrix[1][0], rot_matrix[0][0]))
    pitch = degrees(asin(-rot_matrix[2][0]))
    roll = -degrees(atan2(rot_matrix[2][1], rot_matrix[2][2]))
    
    yaw = (yaw + 180) % 360 - 180
    pitch = (pitch + 180) % 360 - 180
    roll = (roll + 180) % 360 - 180
    
    return (yaw, pitch, roll)

def get_object_name_index(SCENARIO, object_name):
    object_name_index = -1
    if not global_functions.string_empty_check(object_name):
        if not object_name in SCENARIO.object_names:
            SCENARIO.object_names.append(object_name)

        object_name_index = SCENARIO.object_names.index(object_name)

    return object_name_index

def get_scenario_flags(ob):
    scenario_flags = 0
    if ob.tag_scenario.cortana_hack:
        scenario_flags += ScenarioFlags.cortana_hack.value
    if ob.tag_scenario.use_demo_ui:
        scenario_flags += ScenarioFlags.use_demo_ui.value
    if ob.tag_scenario.color_correction:
        scenario_flags += ScenarioFlags.color_correction_ntsc_srgb.value
    if ob.tag_scenario.disable_tag_patches:
        scenario_flags += ScenarioFlags.do_not_apply_bungie_campaign_patches.value

    return scenario_flags

def get_object_flags(ob):
    object_flags = 0
    if ob.tag_object.automatically:
        object_flags += ObjectFlags.automatically.value
    if ob.tag_object.on_easy:
        object_flags += ObjectFlags.on_easy.value
    if ob.tag_object.on_normal:
        object_flags += ObjectFlags.on_normal.value
    if ob.tag_object.on_hard:
        object_flags += ObjectFlags.on_hard.value
    if ob.tag_object.use_player_appearance:
        object_flags += ObjectFlags.use_player_appearance.value
    return object_flags

def get_unit_flags(ob):
    unit_flags = 0
    if ob.tag_unit.unit_dead:
        unit_flags += UnitFlags.dead.value
    return unit_flags

def get_vehicle_flags(ob):
    vehicle_flags = 0
    if ob.tag_unit.slayer_default:
        vehicle_flags += VehicleFlags.slayer_default.value
    if ob.tag_unit.ctf_default:
        vehicle_flags += VehicleFlags.ctf_default.value
    if ob.tag_unit.king_default:
        vehicle_flags += VehicleFlags.king_default.value
    if ob.tag_unit.oddball_default:
        vehicle_flags += VehicleFlags.oddball_default.value
    if ob.tag_unit.unused_0:
        vehicle_flags += VehicleFlags.unused0.value
    if ob.tag_unit.unused_1:
        vehicle_flags += VehicleFlags.unused1.value
    if ob.tag_unit.unused_2:
        vehicle_flags += VehicleFlags.unused2.value
    if ob.tag_unit.unused_3:
        vehicle_flags += VehicleFlags.unused3.value
    if ob.tag_unit.slayer_allowed:
        vehicle_flags += VehicleFlags.slayer_allowed.value
    if ob.tag_unit.ctf_allowed:
        vehicle_flags += VehicleFlags.ctf_allowed.value
    if ob.tag_unit.king_allowed:
        vehicle_flags += VehicleFlags.king_allowed.value
    if ob.tag_unit.oddball_allowed:
        vehicle_flags += VehicleFlags.oddball_allowed.value
    if ob.tag_unit.unused_4:
        vehicle_flags += VehicleFlags.unused4.value
    if ob.tag_unit.unused_5:
        vehicle_flags += VehicleFlags.unused5.value
    if ob.tag_unit.unused_6:
        vehicle_flags += VehicleFlags.unused6.value
    if ob.tag_unit.unused_7:
        vehicle_flags += VehicleFlags.unused7.value

    return vehicle_flags

def get_item_flags(ob):
    item_flags = 0
    if ob.tag_item.initially_at_rest:
        item_flags += ItemFlags.initially_at_rest_doesnt_fall.value
    if ob.tag_item.obsolete:
        item_flags += ItemFlags.obsolete.value
    if ob.tag_item.does_accelerate:
        item_flags += ItemFlags.does_accelerate_moves_due_to_explosions.value

    return item_flags

def get_device_flags(ob):
    device_flags = 0
    if ob.tag_device.initially_open:
        device_flags += DeviceFlags.initially_open.value
    if ob.tag_device.initially_off:
        device_flags += DeviceFlags.initially_off.value
    if ob.tag_device.can_change_only_once:
        device_flags += DeviceFlags.can_change_only_once.value
    if ob.tag_device.position_reversed:
        device_flags += DeviceFlags.position_reversed.value
    if ob.tag_device.not_usable_from_any_side:
        device_flags += DeviceFlags.not_usable_from_any_side.value
    return device_flags

def get_machine_flags(ob):
    machine_flags = 0
    if ob.tag_machine.does_not_operate_automatically:
        machine_flags += MachineFlags.does_not_operate_automatically.value
    if ob.tag_machine.one_sided:
        machine_flags += MachineFlags.one_sided.value
    if ob.tag_machine.never_appears_locked:
        machine_flags += MachineFlags.never_appears_locked.value
    if ob.tag_machine.opened_by_melee_attack:
        machine_flags += MachineFlags.opened_by_melee_attack.value
    return machine_flags

def get_control_flags(ob):
    control_flags = 0
    if ob.tag_control.usable_from_both_sides:
        control_flags += ControlFlags.usable_from_both_sides.value
    return control_flags

def get_netgame_equipment_flags(ob):
    netgame_equipment_flags = 0
    if ob.tag_netgame_equipment.levitate:
        netgame_equipment_flags += NetGameEquipment.levitate.value
    return netgame_equipment_flags

def get_encounter_flags(ob):
    encounter_flags = 0
    if ob.tag_encounter.not_initially_created:
        encounter_flags += EncounterFlags.not_initially_created.value
    if ob.tag_encounter.respawn_enabled:
        encounter_flags += EncounterFlags.respawn_enabled.value
    if ob.tag_encounter.initially_blind:
        encounter_flags += EncounterFlags.initially_blind.value
    if ob.tag_encounter.initially_deaf:
        encounter_flags += EncounterFlags.initially_deaf.value
    if ob.tag_encounter.initially_braindead:
        encounter_flags += EncounterFlags.initially_braindead.value
    if ob.tag_encounter.firing_positions:
        encounter_flags += EncounterFlags._3d_firing_positions.value
    if ob.tag_encounter.manual_bsp_index_specified:
        encounter_flags += EncounterFlags.manual_bsp_index_specified.value

    return encounter_flags

def get_squad_flags(ob):
    squad_flags = 0
    if ob.tag_squad.unused:
        squad_flags += SquadFlags.unused.value
    if ob.tag_squad.never_search:
        squad_flags += SquadFlags.never_search.value
    if ob.tag_squad.start_timer_immediately:
        squad_flags += SquadFlags.start_timer_immediately.value
    if ob.tag_squad.no_timer_delay_forever:
        squad_flags += SquadFlags.no_timer_delay_forever.value
    if ob.tag_squad.magic_sight_after_timer:
        squad_flags += SquadFlags.magic_sight_after_timer.value
    if ob.tag_squad.automatic_migration:
        squad_flags += SquadFlags.automatic_migration.value

    return squad_flags

def get_starting_location_flags(ob):
    starting_location_flags = 0
    if ob.tag_starting_location.required:
        starting_location_flags += StartingLocationFlags.required.value

    return starting_location_flags

def get_platoon_flags(ob):
    platoon_flags = 0
    if ob.tag_platoon.flee_when_maneuvering:
        platoon_flags += PlatoonFlags.flee_when_maneuvering.value
    if ob.tag_platoon.say_advancing_when_maneuver:
        platoon_flags += PlatoonFlags.say_advancing_when_maneuver.value
    if ob.tag_platoon.start_in_defending_state:
        platoon_flags += PlatoonFlags.start_in_defending_state.value

    return platoon_flags

def get_group_flags(group_string):
    group_flags = 0
    group_string = group_string.lower()
    for group in GroupFlags:
        if group.name in group_string:
            group_flags += group.value

    return group_flags

def get_command_list_flags(ob):
    command_list_flags = 0
    if ob.tag_command_list.allow_initiative:
        command_list_flags += CommandListFlags.allow_initiative.value
    if ob.tag_command_list.allow_targeting:
        command_list_flags += CommandListFlags.allow_targeting.value
    if ob.tag_command_list.disable_looking:
        command_list_flags += CommandListFlags.disable_looking.value
    if ob.tag_command_list.disable_communication:
        command_list_flags += CommandListFlags.disable_communication.value
    if ob.tag_command_list.disable_falling_damage:
        command_list_flags += CommandListFlags.disable_falling_damage.value
    if ob.tag_command_list.manual_bsp_index_flag:
        command_list_flags += CommandListFlags.manual_bsp_index.value

    return command_list_flags

def generate_skies(TAG, SCENARIO):
    comment_collection = bpy.data.collections.get("Skies")
    blender_skies = []
    if comment_collection:
        for coll in comment_collection.children:
            blender_skies.append(get_tag_reference(TAG, coll.tag_sky.sky_path))

    SCENARIO.skies = blender_skies

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

def generate_object_names(TAG, SCENARIO):
    for object_name in bpy.context.scene.object_names:
        if not object_name.name in SCENARIO.object_names and not global_functions.string_empty_check(object_name.name):
            SCENARIO.object_names.append(object_name.name)

def generate_scenery(TAG, SCENARIO):
    scenery_collection = bpy.data.collections.get("Scenery")
    blender_scenery = []
    if scenery_collection:
        for ob in scenery_collection.objects:
            scenery = SCENARIO.Object()
            scenery.type_index = get_palette_index(TAG, ob.tag_object.tag_path, SCENARIO.scenery_palette)
            scenery.name_index = get_object_name_index(SCENARIO, ob.tag_object.object_name)
            scenery.placement_flags = get_object_flags(ob)
            scenery.desired_permutation = ob.tag_object.desired_permutation
            scenery.position = ob.location / 100
            scenery.rotation = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())
            scenery.appearance_player_index = ob.tag_object.appearance_player_index

            blender_scenery.append(scenery)

    SCENARIO.scenery = blender_scenery

def generate_bipeds(TAG, SCENARIO):
    biped_collection = bpy.data.collections.get("Bipeds")
    blender_bipeds = []
    if biped_collection:
        for ob in biped_collection.objects:
            biped = SCENARIO.Unit()
            biped.type_index = get_palette_index(TAG, ob.tag_object.tag_path, SCENARIO.biped_palette)
            biped.name_index = get_object_name_index(SCENARIO, ob.tag_object.object_name)
            biped.placement_flags = get_object_flags(ob)
            biped.desired_permutation = ob.tag_object.desired_permutation
            biped.position = ob.location / 100
            biped.rotation = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())
            biped.appearance_player_index = ob.tag_object.appearance_player_index
            biped.body_vitality = ob.tag_unit.unit_vitality
            biped.flags = get_unit_flags(ob)

            blender_bipeds.append(biped)

    SCENARIO.bipeds = blender_bipeds

def generate_vehicles(TAG, SCENARIO):
    vehicle_collection = bpy.data.collections.get("Vehicles")
    blender_vehicles = []
    if vehicle_collection:
        for ob in vehicle_collection.objects:
            vehicle = SCENARIO.Vehicle()
            vehicle.type_index = get_palette_index(TAG, ob.tag_object.tag_path, SCENARIO.vehicle_palette)
            vehicle.name_index = get_object_name_index(SCENARIO, ob.tag_object.object_name)
            vehicle.placement_flags = get_object_flags(ob)
            vehicle.desired_permutation = ob.tag_object.desired_permutation
            vehicle.position = ob.location / 100
            vehicle.rotation = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())
            vehicle.appearance_player_index = ob.tag_object.appearance_player_index
            vehicle.body_vitality = ob.tag_unit.unit_vitality
            vehicle.flags = get_unit_flags(ob)
            vehicle.multiplayer_team_index = ob.tag_unit.multiplayer_team_index
            vehicle.multiplayer_spawn_flags = get_vehicle_flags(ob)

            blender_vehicles.append(vehicle)

    SCENARIO.vehicles = blender_vehicles

def generate_equipment(TAG, SCENARIO):
    equipment_collection = bpy.data.collections.get("Equipment")
    blender_equipment = []
    if equipment_collection:
        for ob in equipment_collection.objects:
            equipment = SCENARIO.Equipment()
            equipment.type_index = get_palette_index(TAG, ob.tag_object.tag_path, SCENARIO.equipment_palette)
            equipment.name_index = get_object_name_index(SCENARIO, ob.tag_object.object_name)
            equipment.placement_flags = get_object_flags(ob)
            equipment.desired_permutation = ob.tag_object.desired_permutation
            equipment.position = ob.location / 100
            equipment.rotation = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())
            equipment.appearance_player_index = ob.tag_object.appearance_player_index
            equipment.misc_flags = get_item_flags(ob)

            blender_equipment.append(equipment)

    SCENARIO.equipment = blender_equipment

def generate_weapons(TAG, SCENARIO):
    weapon_collection = bpy.data.collections.get("Weapons")
    blender_weapons = []
    if weapon_collection:
        for ob in weapon_collection.objects:
            weapon = SCENARIO.Weapon()
            weapon.type_index = get_palette_index(TAG, ob.tag_object.tag_path, SCENARIO.weapon_palette)
            weapon.name_index = get_object_name_index(SCENARIO, ob.tag_object.object_name)
            weapon.placement_flags = get_object_flags(ob)
            weapon.desired_permutation = ob.tag_object.desired_permutation
            weapon.position = ob.location / 100
            weapon.rotation = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())
            weapon.appearance_player_index = ob.tag_object.appearance_player_index
            weapon.rounds_left = ob.tag_weapon.rounds_left
            weapon.rounds_loaded = ob.tag_weapon.rounds_loaded
            weapon.flags = get_item_flags(ob)

            blender_weapons.append(weapon)

    SCENARIO.weapons = blender_weapons

def generate_machines(TAG, SCENARIO):
    machines_collection = bpy.data.collections.get("Machines")
    blender_machines = []
    if machines_collection:
        for ob in machines_collection.objects:
            machine = SCENARIO.DeviceMachine()
            machine.type_index = get_palette_index(TAG, ob.tag_object.tag_path, SCENARIO.device_machine_palette)
            machine.name_index = get_object_name_index(SCENARIO, ob.tag_object.object_name)
            machine.placement_flags = get_object_flags(ob)
            machine.desired_permutation = ob.tag_object.desired_permutation
            machine.position = ob.location / 100
            machine.rotation = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())
            machine.appearance_player_index = ob.tag_object.appearance_player_index
            machine.power_group_index = ob.tag_device.power_group
            machine.position_group_index = ob.tag_device.position_group
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
            control.type_index = get_palette_index(TAG, ob.tag_object.tag_path, SCENARIO.device_control_palette)
            control.name_index = get_object_name_index(SCENARIO, ob.tag_object.object_name)
            control.placement_flags = get_object_flags(ob)
            control.desired_permutation = ob.tag_object.desired_permutation
            control.position = ob.location / 100
            control.rotation = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())
            control.appearance_player_index = ob.tag_object.appearance_player_index
            control.power_group_index = ob.tag_device.power_group
            control.position_group_index = ob.tag_device.position_group
            control.flags_0 = get_device_flags(ob)
            control.flags_1 = get_control_flags(ob)
            control.unknown = ob.tag_control.control_value

            blender_controls.append(control)

    SCENARIO.device_controls = blender_controls

def generate_light_fixtures(TAG, SCENARIO):
    light_fixtures_collection = bpy.data.collections.get("Light Fixtures")
    blender_light_fixtures = []
    if light_fixtures_collection:
        for ob in light_fixtures_collection.objects:
            light_fixture = SCENARIO.DeviceLightFixture()
            light_fixture.type_index = get_palette_index(TAG, ob.tag_object.tag_path, SCENARIO.device_light_fixtures_palette)
            light_fixture.name_index = get_object_name_index(SCENARIO, ob.tag_object.object_name)
            light_fixture.placement_flags = get_object_flags(ob)
            light_fixture.desired_permutation = ob.tag_object.desired_permutation
            light_fixture.position = ob.location / 100
            light_fixture.rotation = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())
            light_fixture.appearance_player_index = ob.tag_object.appearance_player_index
            light_fixture.power_group_index = ob.tag_device.power_group
            light_fixture.position_group_index = ob.tag_device.position_group
            light_fixture.flags = get_device_flags(ob)
            light_fixture.color_RGBA = (ob.tag_light_fixture.color[0], ob.tag_light_fixture.color[1], ob.tag_light_fixture.color[2], 1)
            light_fixture.intensity = ob.tag_light_fixture.intensity
            light_fixture.falloff_angle = ob.tag_light_fixture.falloff_angle
            light_fixture.cutoff_angle = ob.tag_light_fixture.cutoff_angle

            blender_light_fixtures.append(light_fixture)

    SCENARIO.device_light_fixtures = blender_light_fixtures

def generate_sound_scenery(TAG, SCENARIO):
    sound_scenery_collection = bpy.data.collections.get("Sound Scenery")
    blender_sound_scenery = []
    if sound_scenery_collection:
        for ob in sound_scenery_collection.objects:
            sound_scenery = SCENARIO.Object()
            sound_scenery.type_index = get_palette_index(TAG, ob.tag_object.tag_path, SCENARIO.sound_scenery_palette)
            sound_scenery.name_index = get_object_name_index(SCENARIO, ob.tag_object.object_name)
            sound_scenery.placement_flags = get_object_flags(ob)
            sound_scenery.desired_permutation = ob.tag_object.desired_permutation
            sound_scenery.position = ob.location / 100
            sound_scenery.rotation = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())
            sound_scenery.appearance_player_index = ob.tag_object.appearance_player_index

            blender_sound_scenery.append(sound_scenery)

    SCENARIO.sound_scenery = blender_sound_scenery

def generate_player_starting_locations(TAG, SCENARIO):
    player_starting_locations_collection = bpy.data.collections.get("Player Starting Locations")
    blender_player_starting_locations = []
    if player_starting_locations_collection:
        for ob in player_starting_locations_collection.objects:
            player_starting_location = SCENARIO.PlayerStartingLocation()
            yaw, pitch, roll = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())

            player_starting_location.position = ob.location / 100
            player_starting_location.facing = yaw
            player_starting_location.team_index = ob.tag_player_starting_location.team_index
            player_starting_location.bsp_index = ob.tag_player_starting_location.bsp_index
            player_starting_location.type_0 = int(ob.tag_player_starting_location.type_0)
            player_starting_location.type_1 = int(ob.tag_player_starting_location.type_1)
            player_starting_location.type_2 = int(ob.tag_player_starting_location.type_2)
            player_starting_location.type_3 = int(ob.tag_player_starting_location.type_3)

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
            yaw, pitch, roll = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())

            netgame_flag.position = ob.location / 100
            netgame_flag.facing = yaw
            netgame_flag.type = int(ob.tag_netgame_flag.netgame_type)
            netgame_flag.usage_id = ob.tag_netgame_flag.usage_id
            netgame_flag.weapon_group = get_tag_reference(TAG, ob.tag_netgame_flag.weapon_group)

            blender_netgame_flags.append(netgame_flag)

    SCENARIO.netgame_flags = blender_netgame_flags

def generate_netgame_equipment(TAG, SCENARIO):
    netgame_equipment_collection = bpy.data.collections.get("Netgame Equipment")
    blender_netgame_equipment = []
    if netgame_equipment_collection:
        for ob in netgame_equipment_collection.objects:
            netgame_equipment = SCENARIO.NetGameEquipment()
            yaw, pitch, roll = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())

            netgame_equipment.flags = get_netgame_equipment_flags(ob)
            netgame_equipment.type_0 = int(ob.tag_netgame_equipment.type_0)
            netgame_equipment.type_1 = int(ob.tag_netgame_equipment.type_1)
            netgame_equipment.type_2 = int(ob.tag_netgame_equipment.type_2)
            netgame_equipment.type_3 = int(ob.tag_netgame_equipment.type_3)
            netgame_equipment.team_index = ob.tag_netgame_equipment.team_index
            netgame_equipment.spawn_time = ob.tag_netgame_equipment.spawn_time
            netgame_equipment.position = ob.location / 100
            netgame_equipment.facing = yaw
            netgame_equipment.item_collection = get_tag_reference(TAG, ob.tag_netgame_equipment.item_collection)

            blender_netgame_equipment.append(netgame_equipment)

    SCENARIO.netgame_equipment = blender_netgame_equipment

def generate_decals(TAG, SCENARIO):
    decal_collection = bpy.data.collections.get("Decals")
    blender_decals = []
    if decal_collection:
        for ob in decal_collection.objects:
            decal = SCENARIO.Decal()

            decal.palette_index = get_palette_index(TAG, ob.tag_decal.decal_type, SCENARIO.decal_palette)
            decal.yaw = ob.tag_decal.yaw
            decal.pitch = ob.tag_decal.pitch
            decal.position = ob.location / 100

            blender_decals.append(decal)

    SCENARIO.decals = blender_decals

def generate_encounters(TAG, SCENARIO):
    encounters_collection = bpy.data.collections.get("Encounters")
    blender_encounters = []
    if encounters_collection:
        for encounter_collection in encounters_collection.children:
            squad_collections = None
            platoon_collections = None
            firing_point_collection = None
            player_starting_location_collection = None
            for encounter_block in encounter_collection.children:
                block_name = encounter_block.name.lower().replace(" ", "_")
                if block_name.startswith("squads"):
                    squad_collections = encounter_block
                elif block_name.startswith("platoons"):
                    platoon_collections = encounter_block
                elif block_name.startswith("firing_points"):
                    firing_point_collection = encounter_block
                elif block_name.startswith("player_starting_locations"):
                    player_starting_location_collection = encounter_block

            encounter = SCENARIO.Encounter()

            encounter.name = encounter_collection.tag_encounter.name
            encounter.flags = get_encounter_flags(encounter_collection)
            encounter.team_index = int(encounter_collection.tag_encounter.team_index)
            encounter.search_behavior = int(encounter_collection.tag_encounter.search_behavior)
            encounter.manual_bsp_index = encounter_collection.tag_encounter.manual_bsp_index
            encounter.respawn_delay = (encounter_collection.tag_encounter.respawn_delay_min, encounter_collection.tag_encounter.respawn_delay_max)

            encounter.squads = []
            encounter.platoons = []
            encounter.firing_positions = []
            encounter.player_starting_locations = []
            if squad_collections:
                for squad_collection in squad_collections.children:
                    move_positions_collections = None
                    starting_locations_collection = None
                    for squad_block in squad_collection.children:
                        block_name = squad_block.name.lower().replace(" ", "_")
                        if block_name.startswith("move_positions"):
                            move_positions_collections = squad_block
                        elif block_name.startswith("starting_locations"):
                            starting_locations_collection = squad_block

                    squad = SCENARIO.Squad()

                    squad.name = squad_collection.tag_squad.name
                    squad.actor_type = get_palette_index(TAG, squad_collection.tag_squad.actor_type, SCENARIO.actor_palette)
                    squad.platoon = get_collection_index(platoon_collections.children, squad_collection.tag_squad.platoon)
                    squad.initial_state = int(squad_collection.tag_squad.initial_state)
                    squad.return_state = int(squad_collection.tag_squad.return_state)
                    squad.flags = get_squad_flags(squad_collection)
                    squad.unique_leader_type = int(squad_collection.tag_squad.unique_leader_type)
                    squad.maneuver_to_squad = get_collection_index(squad_collections.children, squad_collection.tag_squad.maneuver_to_squad)
                    squad.squad_delay_time = squad_collection.tag_squad.squad_delay_time
                    squad.attacking = get_group_flags(squad_collection.tag_squad.attacking_groups)
                    squad.attacking_search = get_group_flags(squad_collection.tag_squad.attacking_search_groups)
                    squad.attacking_guard = get_group_flags(squad_collection.tag_squad.attacking_guard_groups)
                    squad.defending = get_group_flags(squad_collection.tag_squad.defending_groups)
                    squad.defending_search = get_group_flags(squad_collection.tag_squad.defending_search_groups)
                    squad.defending_guard = get_group_flags(squad_collection.tag_squad.defending_guard_groups)
                    squad.pursuing = get_group_flags(squad_collection.tag_squad.pursuing_groups)
                    squad.normal_diff_count = squad_collection.tag_squad.normal_diff_count
                    squad.insane_diff_count = squad_collection.tag_squad.insane_diff_count
                    squad.major_upgrade = int(squad_collection.tag_squad.major_upgrade)
                    squad.respawn_min_actors = squad_collection.tag_squad.respawn_min_actors
                    squad.respawn_max_actors = squad_collection.tag_squad.respawn_max_actors
                    squad.respawn_total = squad_collection.tag_squad.respawn_total
                    squad.respawn_delay = (squad_collection.tag_squad.respawn_delay_min, squad_collection.tag_squad.respawn_delay_max)

                    squad.move_positions = []
                    squad.starting_locations = []
                    if move_positions_collections:
                        for move_position_ob in move_positions_collections.objects:
                            move_position = SCENARIO.MovePosition()
                            yaw, pitch, roll = matrix_to_euler(move_position_ob.rotation_euler.to_matrix().inverted())

                            move_position.position = move_position_ob.location / 100
                            move_position.facing = yaw
                            move_position.weight = squad_collection.tag_move_position.weight
                            move_position.time = (squad_collection.tag_move_position.time_min, squad_collection.tag_move_position.time_max)
                            move_position.animation = squad_collection.tag_move_position.animation_index
                            move_position.sequence_id = squad_collection.tag_move_position.sequence_id
                            move_position.surface_index = squad_collection.tag_move_position.surface_index

                            squad.move_positions.append(move_position)

                    if starting_locations_collection:
                        for starting_location_ob in starting_locations_collection.objects:
                            starting_location = SCENARIO.StartingLocation()
                            yaw, pitch, roll = matrix_to_euler(starting_location_ob.rotation_euler.to_matrix().inverted())

                            starting_location.position = starting_location_ob.location / 100
                            starting_location.facing = yaw
                            starting_location.sequence_id = starting_location_ob.tag_starting_location.sequence_id
                            starting_location.flags = get_starting_location_flags(starting_location_ob)
                            starting_location.return_state = int(starting_location_ob.tag_starting_location.return_state)
                            starting_location.initial_state = int(starting_location_ob.tag_starting_location.initial_state)
                            starting_location.actor_type = get_palette_index(TAG, starting_location_ob.tag_starting_location.actor_type, SCENARIO.actor_palette)
                            starting_location.command_list = -1
                            if not starting_location_ob.tag_starting_location.command_list == None:
                                starting_location.command_list = get_collection_index(bpy.data.collections.get("Command Lists").children, starting_location_ob.tag_starting_location.command_list)

                            squad.starting_locations.append(starting_location)

                    squad.move_positions_tag_block = TAG.TagBlock(len(squad.move_positions))
                    squad.starting_locations_tag_block = TAG.TagBlock(len(squad.starting_locations))

                    encounter.squads.append(squad)

            if platoon_collections:
                for platoon_collection in platoon_collections.children:
                    platoon = SCENARIO.Platoon()

                    platoon.name = platoon_collection.tag_platoon.name
                    platoon.flags = get_platoon_flags(platoon_collection)
                    platoon.change_attacking_defending_state = int(platoon_collection.tag_platoon.change_attacking_defending_state)
                    platoon.happens_to_a = get_collection_index(platoon_collections.children, platoon_collection.tag_platoon.happens_to_a)
                    platoon.maneuver_when = int(platoon_collection.tag_platoon.maneuver_when)
                    platoon.happens_to_b = get_collection_index(platoon_collections.children, platoon_collection.tag_platoon.happens_to_b)

                    encounter.platoons.append(platoon)

            if firing_point_collection:
                for firing_point_ob in firing_point_collection.objects:
                    firing_point = SCENARIO.FiringPosition()

                    firing_point.position = firing_point_ob.location / 100
                    firing_point.group_index = int(firing_point_ob.tag_firing_position.group_index)

                    encounter.firing_positions.append(firing_point)

            if player_starting_location_collection:
                for player_starting_location_ob in player_starting_location_collection.objects:
                    player_starting_location = SCENARIO.PlayerStartingLocation()
                    yaw, pitch, roll = matrix_to_euler(player_starting_location_ob.rotation_euler.to_matrix().inverted())

                    player_starting_location.position = player_starting_location_ob.location / 100
                    player_starting_location.facing = yaw
                    player_starting_location.team_index = player_starting_location_ob.tag_player_starting_location.team_index
                    player_starting_location.bsp_index = player_starting_location_ob.tag_player_starting_location.bsp_index
                    player_starting_location.type_0 = int(player_starting_location_ob.tag_player_starting_location.type_0)
                    player_starting_location.type_1 = int(player_starting_location_ob.tag_player_starting_location.type_1)
                    player_starting_location.type_2 = int(player_starting_location_ob.tag_player_starting_location.type_2)
                    player_starting_location.type_3 = int(player_starting_location_ob.tag_player_starting_location.type_3)

                    encounter.player_starting_locations.append(player_starting_location)

            encounter.squads_tag_block = TAG.TagBlock(len(encounter.squads))
            encounter.platoons_tag_block = TAG.TagBlock(len(encounter.platoons))
            encounter.firing_positions_tag_block = TAG.TagBlock(len(encounter.firing_positions))
            encounter.player_starting_locations_tag_block = TAG.TagBlock(len(encounter.player_starting_locations))

            blender_encounters.append(encounter)

    SCENARIO.encounters = blender_encounters

def generate_command_lists(TAG, SCENARIO):
    command_lists_collection = bpy.data.collections.get("Command Lists")
    blender_command_lists = []
    if command_lists_collection:
        for command_list_collection in command_lists_collection.children:
            command_collections = None
            point_collections = None
            for command_list_block in command_list_collection.children:
                block_name = command_list_block.name.lower().replace(" ", "_")
                if block_name.startswith("commands"):
                    command_collections = command_list_block
                elif block_name.startswith("points"):
                    point_collections = command_list_block

            command_list = SCENARIO.CommandList()

            command_list.name = command_list_collection.tag_command_list.name
            command_list.flags = get_command_list_flags(command_list_collection)
            command_list.manual_bsp_index = command_list_collection.tag_command_list.manual_bsp_index

            command_list.commands = []
            command_list.points = []

            point_names = []
            if point_collections:
                for point_ob in point_collections.objects:
                    point_names.append(point_ob.name)
                    command_list.points.append(point_ob.location / 100)

            if command_collections:
                collection_names = [command_collection.name for command_collection in command_collections.children]
                for command_collection in command_collections.children:
                    command = SCENARIO.Command()

                    command.atom_type = int(command_collection.tag_command.atom_type)
                    command.atom_modifier = command_collection.tag_command.atom_modifier
                    command.parameter1 = command_collection.tag_command.parameter_1
                    command.parameter2 = command_collection.tag_command.parameter_2
                    command.point_1 = -1
                    if not command_collection.tag_command.point_1 == None:
                        command.point_1 = point_names.index(command_collection.tag_command.point_1.name)

                    command.point_2 = -1
                    if not command_collection.tag_command.point_2 == None:
                        command.point_2 = point_names.index(command_collection.tag_command.point_2.name)

                    command.animation = command_collection.tag_command.animation_index
                    command.script = command_collection.tag_command.script_index
                    command.recording = command_collection.tag_command.recording_index
                    command.command = -1
                    if not command_collection.tag_command.command_index == None:
                        command.command = collection_names.index(command_collection.tag_command.command_index.name)

                    command.object_name = get_object_name_index(SCENARIO, command_collection.tag_command.object_name)

                    command_list.commands.append(command)

            command_list.command_tag_block = TAG.TagBlock(len(command_list.commands))
            command_list.points_tag_block = TAG.TagBlock(len(command_list.points))

            blender_command_lists.append(command_list)

    SCENARIO.command_lists = blender_command_lists

def generate_cutscene_flags(TAG, SCENARIO):
    cutscene_flag_collection = bpy.data.collections.get("Cutscene Flags")
    blender_cutscene_flags = []
    if cutscene_flag_collection:
        for ob in cutscene_flag_collection.objects:
            yaw, pitch, roll = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())

            cutscene_flag = SCENARIO.CutsceneFlag()

            cutscene_flag.name = ob.tag_cutscene_flag.name
            cutscene_flag.position = ob.location / 100
            cutscene_flag.facing = (yaw, pitch)

            blender_cutscene_flags.append(cutscene_flag)

    SCENARIO.cutscene_flags = blender_cutscene_flags

def generate_cutscene_cameras(TAG, SCENARIO):
    cutscene_cameras_collection = bpy.data.collections.get("Cutscene Cameras")
    blender_cutscene_cameras = []
    if cutscene_cameras_collection:
        for ob in cutscene_cameras_collection.objects:
            halo_camera_fixup = Euler()
            halo_camera_fixup.rotate_axis("Y", radians(90.0))
            halo_camera_fixup.rotate_axis("X", radians(-90.0))
            rot_matrix = ob.rotation_euler.to_matrix() @ halo_camera_fixup.to_matrix()

            cutscene_camera_point = SCENARIO.CutsceneCameraPoint()

            cutscene_camera_point.name = ob.tag_cutscene_camera.name
            cutscene_camera_point.position = ob.location / 100
            cutscene_camera_point.orientation = matrix_to_euler(rot_matrix.inverted())
            cutscene_camera_point.field_of_view = degrees(ob.data.angle)

            blender_cutscene_cameras.append(cutscene_camera_point)

    SCENARIO.cutscene_camera_points = blender_cutscene_cameras

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

def generate_scenario_scene(context, DONOR_ASSET):
    TAG = tag_format.TagAsset()

    if DONOR_ASSET == None:
        DONOR_ASSET = create_tag(TAG)

    generate_skies(TAG, DONOR_ASSET)
    generate_comments(TAG, DONOR_ASSET)
    generate_object_names(TAG, DONOR_ASSET)
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
    generate_decals(TAG, DONOR_ASSET)
    generate_encounters(TAG, DONOR_ASSET)
    generate_command_lists(TAG, DONOR_ASSET)
    generate_cutscene_flags(TAG, DONOR_ASSET)
    generate_cutscene_cameras(TAG, DONOR_ASSET)


    DONOR_ASSET.dont_use_tag_ref = get_tag_reference(TAG, context.scene.tag_scenario.dont_use)
    DONOR_ASSET.wont_use_tag_ref = get_tag_reference(TAG, context.scene.tag_scenario.wont_use)
    DONOR_ASSET.cant_use_tag_ref = get_tag_reference(TAG, context.scene.tag_scenario.cant_use)
    DONOR_ASSET.scenario_type = int(context.scene.tag_scenario.scenario_type_enum)
    DONOR_ASSET.scenario_flags = get_scenario_flags(context.scene)
    DONOR_ASSET.local_north = degrees(context.scene.tag_scenario.local_north)
    DONOR_ASSET.custom_object_names_tag_ref = get_tag_reference(TAG, context.scene.tag_scenario.custom_object_names)
    DONOR_ASSET.chapter_title_text_tag_ref = get_tag_reference(TAG, context.scene.tag_scenario.ingame_help_text)
    DONOR_ASSET.hud_messages_tag_ref = get_tag_reference(TAG, context.scene.tag_scenario.hud_messages)

    DONOR_ASSET.skies_tag_block = TAG.TagBlock(len(DONOR_ASSET.skies))
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
    DONOR_ASSET.decals_tag_block = TAG.TagBlock(len(DONOR_ASSET.decals))
    DONOR_ASSET.decal_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.decal_palette))
    DONOR_ASSET.actor_palette_tag_block = TAG.TagBlock(len(DONOR_ASSET.actor_palette))
    DONOR_ASSET.encounters_tag_block = TAG.TagBlock(len(DONOR_ASSET.encounters))
    DONOR_ASSET.command_lists_tag_block = TAG.TagBlock(len(DONOR_ASSET.command_lists))
    DONOR_ASSET.cutscene_flags_tag_block = TAG.TagBlock(len(DONOR_ASSET.cutscene_flags))
    DONOR_ASSET.cutscene_camera_points_tag_block = TAG.TagBlock(len(DONOR_ASSET.cutscene_camera_points))

    return DONOR_ASSET
