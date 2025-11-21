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
import base64

from mathutils import Euler
from math import radians, degrees, asin, atan2
from ....global_functions import global_functions
from ....file_tag.tag_interface import tag_common
from enum import Flag, Enum, auto

class ScenarioFlags(Flag):
    cortana_hack = auto()
    use_demo_ui = auto()
    color_correction_ntsc_srgb = auto()
    do_not_apply_bungie_campaign_patches = auto()

class ObjectFlags(Flag):
    automatically = auto()
    on_easy = auto()
    on_normal = auto()
    on_hard = auto()
    use_player_appearance = auto()

class UnitFlags(Flag):
    dead = auto()

class VehicleFlags(Flag):
    slayer_default = auto()
    ctf_default = auto()
    king_default = auto()
    oddball_default = auto()
    unused0 = auto()
    unused1 = auto()
    unused2 = auto()
    unused3 = auto()
    slayer_allowed = auto()
    ctf_allowed = auto()
    king_allowed = auto()
    oddball_allowed = auto()
    unused4 = auto()
    unused5 = auto()
    unused6 = auto()
    unused7 = auto()

class ItemFlags(Flag):
    initially_at_rest_doesnt_fall = auto()
    obsolete = auto()
    does_accelerate_moves_due_to_explosions = auto()

class DeviceFlags(Flag):
    initially_open = auto()
    initially_off = auto()
    can_change_only_once = auto()
    position_reversed = auto()
    not_usable_from_any_side = auto()

class MachineFlags(Flag):
    does_not_operate_automatically = auto()
    one_sided = auto()
    never_appears_locked = auto()
    opened_by_melee_attack = auto()

class ControlFlags(Flag):
    usable_from_both_sides = auto()

class NetGameEquipment(Flag):
    levitate = auto()

class EncounterFlags(Flag):
    not_initially_created = auto()
    respawn_enabled = auto()
    initially_blind = auto()
    initially_deaf = auto()
    initially_braindead = auto()
    _3d_firing_positions = auto()
    manual_bsp_index_specified = auto()

class SquadFlags(Flag):
    unused = auto()
    never_search = auto()
    start_timer_immediately = auto()
    no_timer_delay_forever = auto()
    magic_sight_after_timer = auto()
    automatic_migration = auto()

class StartingLocationFlags(Flag):
    required = auto()

class PlatoonFlags(Flag):
    flee_when_maneuvering = auto()
    say_advancing_when_maneuver = auto()
    start_in_defending_state = auto()

class GroupFlags(Flag):
    a = auto()
    b = auto()
    c = auto()
    d = auto()
    e = auto()
    f = auto()
    g = auto()
    h = auto()
    i = auto()
    j = auto()
    k = auto()
    l = auto()
    m = auto()
    n = auto()
    o = auto()
    p = auto()
    q = auto()
    r = auto()
    s = auto()
    t = auto()
    u = auto()
    v = auto()
    w = auto()
    x = auto()
    y = auto()
    z = auto()

class CommandListFlags(Flag):
    allow_initiative = auto()
    allow_targeting = auto()
    disable_looking = auto()
    disable_communication = auto()
    disable_falling_damage = auto()
    manual_bsp_index = auto()

def get_palette_index(scnr_dict, tag_path, block_key, field_key):
    palette_tag_block = scnr_dict["Data"].get(block_key)
    if palette_tag_block is None:
        palette_tag_block = scnr_dict["Data"][block_key] = []

    palette_index = -1
    tag_group = None
    if not global_functions.string_empty_check(tag_path):
        tag_path, tag_extension = tag_path.rsplit(".", 1)
        tag_group = tag_common.h1_tag_extensions.get(tag_extension)
        for palette_element_idx, palette_element in enumerate(palette_tag_block):
            tag_ref = palette_element[field_key]
            if tag_ref["path"] == tag_path and tag_ref["group name"] == tag_group:
                palette_index = palette_element_idx
                break

        if palette_index == -1 and not global_functions.string_empty_check(tag_group) and not global_functions.string_empty_check(tag_path):
            tag_ref = {"group name": tag_group, "path": tag_path}
            block_element = {"name": tag_ref}
            palette_tag_block.append(block_element)
            palette_index = len(palette_tag_block) - 1

    return palette_index

def get_tag_reference(tag_path):
    tag_ref = {"group name": None, "path": ""}
    if not global_functions.string_empty_check(tag_path):
        tag_path, tag_extension = tag_path.rsplit(".", 1)
        tag_group = tag_common.h1_tag_extensions.get(tag_extension)
        tag_ref = {"group name": tag_group, "path": tag_path}

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
    
    return [yaw, pitch, roll]

def get_object_name_index(scnr_dict, object_name):
    object_name_index = -1
    object_name_block = scnr_dict["Data"].get("object names")
    if object_name_block is None:
        object_name_block = scnr_dict["Data"]["object names"] = []

    if not global_functions.string_empty_check(object_name):
        for object_name_idx, object_name_element in enumerate(object_name_block):
            if object_name == object_name_element["name"]:
                object_name_index = object_name_idx

    if not global_functions.string_empty_check(object_name) and object_name_index == -1:
        object_name_element = {"name": object_name}
        object_name_block.append(object_name_element)
        object_name_index = len(object_name_block) - 1

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

def generate_skies(scnr_dict):
    sky_collection = bpy.data.collections.get("Skies")
    blender_skies = scnr_dict["Data"]["skies"] = []
    if sky_collection:
        for sky in sky_collection.children:
            sky_element = {"sky": get_tag_reference(sky.tag_sky.sky_path)}
            blender_skies.append(sky_element)

def generate_comments(scnr_dict):
    comment_collection = bpy.data.collections.get("Comments")
    blender_comments = scnr_dict["Data"]["comments"] = []
    if comment_collection:
        for ob in comment_collection.objects:
            comment = {
                "position": ob.location / 100,
                "comment": {"length": len(ob.data.body) + 1, "encoded": base64.b64encode(ob.data.body).decode('utf-8')}
            }

            blender_comments.append(comment)

def generate_object_names(scnr_dict):
    object_name_list = []
    blender_object_names = scnr_dict["Data"]["object names"] = []
    for object_name in bpy.context.scene.object_names:
        if not object_name.name in object_name_list and not global_functions.string_empty_check(object_name.name):
            object_name_list.append(object_name.name)

    for object_name in object_name_list:
        blender_object_names.append({"name": object_name})

def generate_scenery(scnr_dict):
    scenery_collection = bpy.data.collections.get("Scenery")
    blender_scenery = scnr_dict["Data"]["scenery"] = []
    if scenery_collection:
        for ob in scenery_collection.objects:
            scenery = {
                "type": get_palette_index(scnr_dict, ob.tag_object.tag_path, "scenery palette", "name"),
                "name": get_object_name_index(scnr_dict, ob.tag_object.object_name),
                "not placed": get_object_flags(ob),
                "desired permutation": ob.tag_object.desired_permutation,
                "position": list(ob.location / 100),
                "rotation": matrix_to_euler(ob.rotation_euler.to_matrix().inverted()),
                "appearance player index": ob.tag_object.appearance_player_index
            }

            blender_scenery.append(scenery)

def generate_bipeds(scnr_dict):
    biped_collection = bpy.data.collections.get("Bipeds")
    blender_bipeds = scnr_dict["Data"]["bipeds"] = []
    if biped_collection:
        for ob in biped_collection.objects:
            biped = {
                "type": get_palette_index(scnr_dict, ob.tag_object.tag_path, "biped palette", "name"),
                "name": get_object_name_index(scnr_dict, ob.tag_object.object_name),
                "not placed": get_object_flags(ob),
                "desired permutation": ob.tag_object.desired_permutation,
                "position": list(ob.location / 100),
                "rotation": matrix_to_euler(ob.rotation_euler.to_matrix().inverted()),
                "appearance player index": ob.tag_object.appearance_player_index,
                "body vitality": ob.tag_unit.unit_vitality,
                "flags": get_unit_flags(ob)
            }

            blender_bipeds.append(biped)

def generate_vehicles(scnr_dict):
    vehicle_collection = bpy.data.collections.get("Vehicles")
    blender_vehicles = scnr_dict["Data"]["vehicles"] = []
    if vehicle_collection:
        for ob in vehicle_collection.objects:
            vehicle = {
                "type": get_palette_index(scnr_dict, ob.tag_object.tag_path, "vehicle palette", "name"),
                "name": get_object_name_index(scnr_dict, ob.tag_object.object_name),
                "not placed": get_object_flags(ob),
                "desired permutation": ob.tag_object.desired_permutation,
                "position": list(ob.location / 100),
                "rotation": matrix_to_euler(ob.rotation_euler.to_matrix().inverted()),
                "appearance player index": ob.tag_object.appearance_player_index,
                "body vitality": ob.tag_unit.unit_vitality,
                "flags": get_unit_flags(ob),
                "multiplayer team index": ob.tag_unit.multiplayer_team_index,
                "multiplayer spawn flags": get_vehicle_flags(ob)
            }

            blender_vehicles.append(vehicle)

def generate_equipment(scnr_dict):
    equipment_collection = bpy.data.collections.get("Equipment")
    blender_equipment = scnr_dict["Data"]["equipment"] = []
    if equipment_collection:
        for ob in equipment_collection.objects:
            equipment = {
                "type": get_palette_index(scnr_dict, ob.tag_object.tag_path, "equipment palette", "name"),
                "name": get_object_name_index(scnr_dict, ob.tag_object.object_name),
                "not placed": get_object_flags(ob),
                "desired permutation": ob.tag_object.desired_permutation,
                "position": list(ob.location / 100),
                "rotation": matrix_to_euler(ob.rotation_euler.to_matrix().inverted()),
                "appearance player index": ob.tag_object.appearance_player_index,
                "misc flags": get_item_flags(ob)
            }

            blender_equipment.append(equipment)

def generate_weapons(scnr_dict):
    weapon_collection = bpy.data.collections.get("Weapons")
    blender_weapons = scnr_dict["Data"]["weapons"] = []
    if weapon_collection:
        for ob in weapon_collection.objects:
            weapon = {
                "type": get_palette_index(scnr_dict, ob.tag_object.tag_path, "weapon palette", "name"),
                "name": get_object_name_index(scnr_dict, ob.tag_object.object_name),
                "not placed": get_object_flags(ob),
                "desired permutation": ob.tag_object.desired_permutation,
                "position": list(ob.location / 100),
                "rotation": matrix_to_euler(ob.rotation_euler.to_matrix().inverted()),
                "appearance player index": ob.tag_object.appearance_player_index,
                "rounds reserved": ob.tag_weapon.rounds_left,
                "rounds loaded": ob.tag_weapon.rounds_loaded,
                "flags": get_item_flags(ob)
            }

            blender_weapons.append(weapon)

def generate_machines(scnr_dict):
    machines_collection = bpy.data.collections.get("Machines")
    blender_machines = scnr_dict["Data"]["machines"] = []
    if machines_collection:
        for ob in machines_collection.objects:
            machine = {
                "type": get_palette_index(scnr_dict, ob.tag_object.tag_path, "machine palette", "name"),
                "name": get_object_name_index(scnr_dict, ob.tag_object.object_name),
                "not placed": get_object_flags(ob),
                "desired permutation": ob.tag_object.desired_permutation,
                "position": list(ob.location / 100),
                "rotation": matrix_to_euler(ob.rotation_euler.to_matrix().inverted()),
                "appearance player index": ob.tag_object.appearance_player_index,
                "power group": ob.tag_device.power_group,
                "position group": ob.tag_device.position_group,
                "device flags": get_device_flags(ob),
                "machine flags": get_machine_flags(ob)
            }

            blender_machines.append(machine)

def generate_controls(scnr_dict):
    controls_collection = bpy.data.collections.get("Controls")
    blender_controls = scnr_dict["Data"]["controls"] = []
    if controls_collection:
        for ob in controls_collection.objects:
            control = {
                "type": get_palette_index(scnr_dict, ob.tag_object.tag_path, "control palette", "name"),
                "name": get_object_name_index(scnr_dict, ob.tag_object.object_name),
                "not placed": get_object_flags(ob),
                "desired permutation": ob.tag_object.desired_permutation,
                "position": list(ob.location / 100),
                "rotation": matrix_to_euler(ob.rotation_euler.to_matrix().inverted()),
                "appearance player index": ob.tag_object.appearance_player_index,
                "power group": ob.tag_device.power_group,
                "position group": ob.tag_device.position_group,
                "device flags": get_device_flags(ob),
                "control flags": get_control_flags(ob),
                "no name": ob.tag_control.control_value
            }

            blender_controls.append(control)

def generate_light_fixtures(scnr_dict):
    light_fixtures_collection = bpy.data.collections.get("Light Fixtures")
    blender_light_fixtures = scnr_dict["Data"]["light fixtures"] = []
    if light_fixtures_collection:
        for ob in light_fixtures_collection.objects:
            R, G, B = ob.tag_light_fixture.color
            light_fixture = {
                "type": get_palette_index(scnr_dict, ob.tag_object.tag_path, "light fixture palette", "name"),
                "name": get_object_name_index(scnr_dict, ob.tag_object.object_name),
                "not placed": get_object_flags(ob),
                "desired permutation": ob.tag_object.desired_permutation,
                "position": list(ob.location / 100),
                "rotation": matrix_to_euler(ob.rotation_euler.to_matrix().inverted()),
                "appearance player index": ob.tag_object.appearance_player_index,
                "power group": ob.tag_device.power_group,
                "position group": ob.tag_device.position_group,
                "device flags": get_device_flags(ob),
                "color": {"R": R, "G": G, "B": B},
                "intensity": ob.tag_light_fixture.intensity,
                "falloff angle": ob.tag_light_fixture.falloff_angle,
                "cutoff angle": ob.tag_light_fixture.cutoff_angle
            }

            blender_light_fixtures.append(light_fixture)

def generate_sound_scenery(scnr_dict):
    sound_scenery_collection = bpy.data.collections.get("Sound Scenery")
    blender_sound_scenery = scnr_dict["Data"]["sound scenery"] = []
    if sound_scenery_collection:
        for ob in sound_scenery_collection.objects:
            sound_scenery = {
                "type": get_palette_index(scnr_dict, ob.tag_object.tag_path, "sound scenery palette", "name"),
                "name": get_object_name_index(scnr_dict, ob.tag_object.object_name),
                "not placed": get_object_flags(ob),
                "desired permutation": ob.tag_object.desired_permutation,
                "position": list(ob.location / 100),
                "rotation": matrix_to_euler(ob.rotation_euler.to_matrix().inverted()),
                "appearance player index": ob.tag_object.appearance_player_index
            }

            blender_sound_scenery.append(sound_scenery)

def generate_player_starting_locations(scnr_dict):
    player_starting_locations_collection = bpy.data.collections.get("Player Starting Locations")
    blender_player_starting_locations = scnr_dict["Data"]["player starting locations"] = []
    if player_starting_locations_collection:
        for ob in player_starting_locations_collection.objects:
            yaw, pitch, roll = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())
            player_starting_location = {
                "position": list(ob.location / 100),
                "facing": yaw,
                "team index": ob.tag_player_starting_location.team_index,
                "bsp index": ob.tag_player_starting_location.bsp_index,
                "type 0": {"value": int(ob.tag_player_starting_location.type_0)},
                "type 1": {"value": int(ob.tag_player_starting_location.type_1)},
                "type 2": {"value": int(ob.tag_player_starting_location.type_2)},
                "type 3": {"value": int(ob.tag_player_starting_location.type_3)}
            }
            
            blender_player_starting_locations.append(player_starting_location)

def generate_trigger_volumes(scnr_dict):
    trigger_volumes_collection = bpy.data.collections.get("Trigger Volumes")
    blender_trigger_volumes = scnr_dict["Data"]["trigger volumes"] = []
    if trigger_volumes_collection:
        for ob in trigger_volumes_collection.objects:
            rot_matrix = ob.matrix_world.normalized()
            trigger_volume = {
                "name": ob.name,
                "rotation vector forward": list(rot_matrix[0][0:3]),
                "rotation vector up": list(rot_matrix[2][0:3]),
                "starting corner": list(ob.location / 100),
                "ending corner offset": list(ob.dimensions / 100)
            }
            
            blender_trigger_volumes.append(trigger_volume)

def generate_netgame_flags(scnr_dict):
    netgame_flags_collection = bpy.data.collections.get("Netgame Flags")
    blender_netgame_flags = scnr_dict["Data"]["netgame flags"] = []
    if netgame_flags_collection:
        for ob in netgame_flags_collection.objects:
            yaw, pitch, roll = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())
            netgame_flag = {
                "position": list(ob.location / 100),
                "facing": yaw,
                "type": {"value": int(ob.tag_netgame_flag.netgame_type)},
                "usage id": ob.tag_netgame_flag.usage_id,
                "weapon group": get_tag_reference(ob.tag_netgame_flag.weapon_group)
            }

            blender_netgame_flags.append(netgame_flag)

def generate_netgame_equipment(scnr_dict):
    netgame_equipment_collection = bpy.data.collections.get("Netgame Equipment")
    blender_netgame_equipment = scnr_dict["Data"]["netgame equipment"] = []
    if netgame_equipment_collection:
        for ob in netgame_equipment_collection.objects:
            yaw, pitch, roll = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())
            netgame_equipment = {
                "flags": get_netgame_equipment_flags(ob),
                "type 0": {"value": int(ob.tag_netgame_equipment.type_0)},
                "type 1": {"value": int(ob.tag_netgame_equipment.type_1)},
                "type 2": {"value": int(ob.tag_netgame_equipment.type_2)},
                "type 3": {"value": int(ob.tag_netgame_equipment.type_3)},
                "team index": ob.tag_netgame_equipment.team_index,
                "spawn time": ob.tag_netgame_equipment.spawn_time,
                "position": list(ob.location / 100),
                "facing": yaw,
                "item collection": get_tag_reference(ob.tag_netgame_equipment.item_collection)
            }
            
            blender_netgame_equipment.append(netgame_equipment)

def generate_decals(scnr_dict):
    decal_collection = bpy.data.collections.get("Decals")
    blender_decals = scnr_dict["Data"]["decals"] = []
    if decal_collection:
        for ob in decal_collection.objects:
            decal = {
                "decal type": get_palette_index(scnr_dict, ob.tag_decal.decal_type, "decal palette", "reference"),
                "yaw": ob.tag_decal.yaw,
                "pitch": ob.tag_decal.pitch,
                "position": list(ob.location / 100)
            }

            blender_decals.append(decal)

def generate_encounters(scnr_dict):
    encounters_collection = bpy.data.collections.get("Encounters")
    blender_encounters = scnr_dict["Data"]["encounters"] = []
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

            squads = []
            platoons = []
            firing_positions = []
            player_starting_locations = []
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

                    move_positions = []
                    starting_locations = []
                    if move_positions_collections:
                        for move_position_ob in move_positions_collections.objects:
                            yaw, pitch, roll = matrix_to_euler(move_position_ob.rotation_euler.to_matrix().inverted())

                            move_position = {
                                "position": list(move_position_ob.location / 100),
                                "facing": yaw,
                                "weight": squad_collection.tag_move_position.weight,
                                "time": {"Min": squad_collection.tag_move_position.time_min, "Max": squad_collection.tag_move_position.time_max},
                                "animation": squad_collection.tag_move_position.animation_index,
                                "sequence id": squad_collection.tag_move_position.sequence_id,
                                "surface index": squad_collection.tag_move_position.surface_index
                            }

                            move_positions.append(move_position)

                    if starting_locations_collection:
                        for starting_location_ob in starting_locations_collection.objects:
                            yaw, pitch, roll = matrix_to_euler(starting_location_ob.rotation_euler.to_matrix().inverted())
                            command_index = -1
                            if not starting_location_ob.tag_starting_location.command_list == None:
                                command_index = get_collection_index(bpy.data.collections.get("Command Lists").children, starting_location_ob.tag_starting_location.command_list)

                            starting_location = {
                                "position": list(starting_location_ob.location / 100),
                                "facing": yaw,
                                "sequence id": starting_location_ob.tag_starting_location.sequence_id,
                                "flags": get_starting_location_flags(starting_location_ob),
                                "return state": {"value": int(starting_location_ob.tag_starting_location.return_state)},
                                "initial state": {"value": int(starting_location_ob.tag_starting_location.initial_state)},
                                "actor type": get_palette_index(scnr_dict, starting_location_ob.tag_starting_location.actor_type, "actor palette", "reference"),
                                "command list": command_index
                            }

                            starting_locations.append(starting_location)

                    squad = {
                        "name": squad_collection.tag_squad.name,
                        "actor type": get_palette_index(scnr_dict, squad_collection.tag_squad.actor_type, "actor palette", "reference"),
                        "platoon": get_collection_index(platoon_collections.children, squad_collection.tag_squad.platoon),
                        "initial state": {"value": int(squad_collection.tag_squad.initial_state)},
                        "return state": {"value": int(squad_collection.tag_squad.return_state)},
                        "flags": get_squad_flags(squad_collection),
                        "unique leader type": {"value": int(squad_collection.tag_squad.unique_leader_type)},
                        "maneuver to squad": get_collection_index(squad_collections.children, squad_collection.tag_squad.maneuver_to_squad),
                        "squad delay time": squad_collection.tag_squad.squad_delay_time,
                        "attacking": get_group_flags(squad_collection.tag_squad.attacking_groups),
                        "attacking search": get_group_flags(squad_collection.tag_squad.attacking_search_groups),
                        "attacking guard": get_group_flags(squad_collection.tag_squad.attacking_guard_groups),
                        "defending": get_group_flags(squad_collection.tag_squad.defending_groups),
                        "defending search": get_group_flags(squad_collection.tag_squad.defending_search_groups),
                        "defending guard": get_group_flags(squad_collection.tag_squad.defending_guard_groups),
                        "pursuing": get_group_flags(squad_collection.tag_squad.pursuing_groups),
                        "normal diff count": squad_collection.tag_squad.normal_diff_count,
                        "insane diff count": squad_collection.tag_squad.insane_diff_count,
                        "major upgrade": {"value": int(squad_collection.tag_squad.major_upgrade)},
                        "respawn min actors": squad_collection.tag_squad.respawn_min_actors,
                        "respawn max actors": squad_collection.tag_squad.respawn_max_actors,
                        "respawn total": squad_collection.tag_squad.respawn_total,
                        "respawn delay": {"Min": squad_collection.tag_squad.respawn_delay_min, "Max": squad_collection.tag_squad.respawn_delay_max},
                        "move positions": move_positions,
                        "starting locations": starting_locations
                    }

                    squads.append(squad)

            if platoon_collections:
                for platoon_collection in platoon_collections.children:
                    platoon = {
                        "name": platoon_collection.tag_platoon.name,
                        "flags": get_platoon_flags(platoon_collection),
                        "change attacking defending state when": {"value": int(platoon_collection.tag_platoon.change_attacking_defending_state)},
                        "happens to": get_collection_index(platoon_collections.children, platoon_collection.tag_platoon.happens_to_a),
                        "maneuver when": {"value": int(platoon_collection.tag_platoon.maneuver_when)},
                        "happens to 1": get_collection_index(platoon_collections.children, platoon_collection.tag_platoon.happens_to_b)
                    }

                    platoons.append(platoon)

            if firing_point_collection:
                for firing_point_ob in firing_point_collection.objects:
                    firing_point = {
                        "position": list(firing_point_ob.location / 100),
                        "group index": {"value": int(firing_point_ob.tag_firing_position.group_index)}
                    }

                    firing_positions.append(firing_point)

            if player_starting_location_collection:
                for player_starting_location_ob in player_starting_location_collection.objects:
                    yaw, pitch, roll = matrix_to_euler(player_starting_location_ob.rotation_euler.to_matrix().inverted())
                    player_starting_location = {
                        "position": list(player_starting_location_ob.location / 100),
                        "facing": yaw,
                        "team index": player_starting_location_ob.tag_player_starting_location.team_index,
                        "bsp index": player_starting_location_ob.tag_player_starting_location.bsp_index,
                        "type 0": {"value": int(player_starting_location_ob.tag_player_starting_location.type_0)},
                        "type 1": {"value": int(player_starting_location_ob.tag_player_starting_location.type_1)},
                        "type 2": {"value": int(player_starting_location_ob.tag_player_starting_location.type_2)},
                        "type 3": {"value": int(player_starting_location_ob.tag_player_starting_location.type_3)}
                    }
                    
                    player_starting_locations.append(player_starting_location)

            encounter = {
                "name": encounter_collection.tag_encounter.name,
                "flags": get_encounter_flags(encounter_collection),
                "team index": {"value": int(encounter_collection.tag_encounter.team_index)},
                "search behavior": {"value": int(encounter_collection.tag_encounter.search_behavior)},
                "manual bsp index": encounter_collection.tag_encounter.manual_bsp_index,
                "respawn delay": {"Min": encounter_collection.tag_encounter.respawn_delay_min, "Max": encounter_collection.tag_encounter.respawn_delay_max},
                "squads": squads,
                "platoons": platoons,
                "firing positions": firing_positions,
                "player starting locations": player_starting_locations
            }

            blender_encounters.append(encounter)

def generate_command_lists(scnr_dict):
    command_lists_collection = bpy.data.collections.get("Command Lists")
    blender_command_lists = scnr_dict["Data"]["command lists"] = []
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

            commands = []
            points = []

            point_names = []
            if point_collections:
                for point_ob in point_collections.objects:
                    point_names.append(point_ob.name)
                    points.append({"position": list(point_ob.location / 100)})

            if command_collections:
                collection_names = [command_collection.name for command_collection in command_collections.children]
                for command_collection in command_collections.children:
                    command_point_1 = -1
                    if not command_collection.tag_command.point_1 == None:
                        command_point_1 = point_names.index(command_collection.tag_command.point_1.name)

                    command_point_2 = -1
                    if not command_collection.tag_command.point_2 == None:
                        command_point_2 = point_names.index(command_collection.tag_command.point_2.name)

                    command_index = -1
                    if not command_collection.tag_command.command_index == None:
                        command_index = collection_names.index(command_collection.tag_command.command_index.name)

                    command = {
                        "atom type": {"value": int(command_collection.tag_command.atom_type)},
                        "atom modifier": command_collection.tag_command.atom_modifier,
                        "parameter1": command_collection.tag_command.parameter_1,
                        "parameter2": command_collection.tag_command.parameter_2,
                        "point 1": command_point_1,
                        "point 2": command_point_2,
                        "animation": command_collection.tag_command.animation_index,
                        "script": command_collection.tag_command.script_index,
                        "recording": command_collection.tag_command.recording_index,
                        "command": command_index,
                        "object name": get_object_name_index(scnr_dict, command_collection.tag_command.object_name)
                    }

                    commands.append(command)

            command_list = {
                "name": command_list_collection.tag_command_list.name,
                "flags": get_command_list_flags(command_list_collection),
                "manual bsp index": command_list_collection.tag_command_list.manual_bsp_index,
                "commands": commands,
                "points": points
            }

            blender_command_lists.append(command_list)

def generate_cutscene_flags(scnr_dict):
    cutscene_flag_collection = bpy.data.collections.get("Cutscene Flags")
    blender_cutscene_flags = scnr_dict["Data"]["cutscene camera points"] = []
    blender_cutscene_flags = []
    if cutscene_flag_collection:
        for ob in cutscene_flag_collection.objects:
            yaw, pitch, roll = matrix_to_euler(ob.rotation_euler.to_matrix().inverted())

            cutscene_flag = {
                "name": ob.tag_cutscene_flag.name,
                "position": list(ob.location / 100),
                "facing": [yaw, pitch]
            }

            blender_cutscene_flags.append(cutscene_flag)

def generate_cutscene_cameras(scnr_dict):
    cutscene_cameras_collection = bpy.data.collections.get("Cutscene Cameras")
    blender_cutscene_cameras = scnr_dict["Data"]["cutscene camera points"] = []
    if cutscene_cameras_collection:
        for ob in cutscene_cameras_collection.objects:
            halo_camera_fixup = Euler()
            halo_camera_fixup.rotate_axis("Y", radians(90.0))
            halo_camera_fixup.rotate_axis("X", radians(-90.0))
            rot_matrix = ob.rotation_euler.to_matrix() @ halo_camera_fixup.to_matrix()

            cutscene_camera_point = {
                "name": ob.tag_cutscene_camera.name,
                "position": list(ob.location / 100),
                "orientation": matrix_to_euler(rot_matrix.inverted()),
                "field of view": degrees(ob.data.angle)
            }

            blender_cutscene_cameras.append(cutscene_camera_point)

def create_tag(file_path):
    tag_dict = {
        "TagName": file_path,
        "Header": {
            "unk1": 0,
            "flags": 0,
            "tag type": 0,
            "name": "",
            "tag group": "scnr",
            "checksum": -1,
            "data offset": 64,
            "data length": 0,
            "unk2": 0,
            "version": 2,
            "destination": 0,
            "plugin handle": -1,
            "engine tag": "blam"
        },
        "Data": {}
        }

    return tag_dict

def generate_scenario_scene(context, scnr_dict, file_path):
    if scnr_dict == None:
        scnr_dict = create_tag(file_path)

    generate_skies(scnr_dict)
    generate_comments(scnr_dict)
    generate_object_names(scnr_dict)
    generate_scenery(scnr_dict)
    generate_bipeds(scnr_dict)
    generate_vehicles(scnr_dict)
    generate_equipment(scnr_dict)
    generate_weapons(scnr_dict)
    generate_machines(scnr_dict)
    generate_controls(scnr_dict)
    generate_light_fixtures(scnr_dict)
    generate_sound_scenery(scnr_dict)
    generate_player_starting_locations(scnr_dict)
    generate_trigger_volumes(scnr_dict)
    generate_netgame_flags(scnr_dict)
    generate_netgame_equipment(scnr_dict)
    generate_decals(scnr_dict)
    generate_encounters(scnr_dict)
    generate_command_lists(scnr_dict)
    generate_cutscene_flags(scnr_dict)
    generate_cutscene_cameras(scnr_dict)

    scnr_dict["Data"]["dont use"] = get_tag_reference(context.scene.tag_scenario.dont_use)
    scnr_dict["Data"]["wont use"] = get_tag_reference(context.scene.tag_scenario.wont_use)
    scnr_dict["Data"]["cant use"] = get_tag_reference(context.scene.tag_scenario.cant_use)
    scnr_dict["Data"]["type"] = {"value": int(context.scene.tag_scenario.scenario_type_enum)}
    scnr_dict["Data"]["flags"] = get_scenario_flags(context.scene)
    scnr_dict["Data"]["local north"] = degrees(context.scene.tag_scenario.local_north)
    scnr_dict["Data"]["custom object names"] = get_tag_reference(context.scene.tag_scenario.custom_object_names)
    scnr_dict["Data"]["ingame help text"] = get_tag_reference(context.scene.tag_scenario.ingame_help_text)
    scnr_dict["Data"]["hud messages"] = get_tag_reference(context.scene.tag_scenario.hud_messages)

    return scnr_dict
