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

import os
import json
import struct

from math import degrees, radians
from .format import ScenarioAsset, SALT_SIZE

DEBUG_PARSER = True
DEBUG_HEADER = True
DEBUG_BODY = True

def tag_block_header(TAG, header_group, version, count, size):
    TAGBLOCKHEADER = TAG.TagBlockHeader()
    TAGBLOCKHEADER.name = TAG.string_to_bytes(header_group, True)
    TAGBLOCKHEADER.version = version
    TAGBLOCKHEADER.count = count
    TAGBLOCKHEADER.size = size

    return TAGBLOCKHEADER

def tag_block(TAG, count, maximum_count, address, definition):
    TAGBLOCK = TAG.TagBlock()
    TAGBLOCK.count = count
    TAGBLOCK.maximum_count = maximum_count
    TAGBLOCK.address = address
    TAGBLOCK.definition = definition

    return TAGBLOCK

def get_object_names(dump_dic, TAG, SCENARIO):
    object_name_tag_block = dump_dic['Data']['Object Names']
    SCENARIO.object_names = []
    for object_name_element in object_name_tag_block:
        object_name = SCENARIO.ObjectName()
        object_name.name = TAG.string_to_bytes(object_name_element['Name'], False)
        object_name.object_type = -1
        object_name.placement_index = -1

        SCENARIO.object_names.append(object_name)

    SCENARIO.object_name_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.object_names), 36)

def get_scenery(dump_dic, TAG, SCENARIO):
    scenery_tag_block = dump_dic['Data']['Scenery']
    SCENARIO.scenery = []
    for scenery_element in scenery_tag_block:
        source = scenery_element['Source']['Value']
        if not source == 0: # We're doing this to exclude scenery pieces added as XREFs.
            primary = scenery_element['Primary Color']
            secondary = scenery_element['Secondary Color']
            tertiary = scenery_element['Tertiary Color']
            quaternary = scenery_element['Quaternary Color']

            scenery = SCENARIO.Scenery()

            scenery.sobj_header = tag_block_header(TAG, "sobj", 1, 1, 48)
            scenery.obj0_header = tag_block_header(TAG, "obj#", 0, 1, 8)
            scenery.sper_header = tag_block_header(TAG, "sper", 0, 1, 24)
            scenery.sct3_header = tag_block_header(TAG, "sct3", 0, 1, 20)

            scenery.palette_index = scenery_element['Palette Index']
            scenery.name_index = scenery_element['Name Index']
            scenery.placement_flags = scenery_element['Placement Flags']
            scenery.position = scenery_element['Position']
            scenery.rotation = scenery_element['Rotation']
            scenery.scale = scenery_element['Scale']
            scenery.transform_flags = scenery_element['Transform Flags']
            scenery.manual_bsp_flags = scenery_element['Manual BSP Flags']
            scenery.unique_id = scenery_element['Unique ID']
            scenery.origin_bsp_index = scenery_element['Origin BSP Index']
            scenery.object_type = scenery_element['Type']['Value']
            scenery.source = scenery_element['Source']['Value']
            scenery.bsp_policy = 0
            scenery.editor_folder_index = -1

            scenery.variant_name_length = 0
            scenery.active_change_colors = 0
            scenery.primary_color_BGRA = (primary['B'], primary['G'], primary['R'], 1)
            scenery.secondary_color_BGRA = (secondary['B'], secondary['G'], secondary['R'], 1)
            scenery.tertiary_color_BGRA = (tertiary['B'], tertiary['G'], tertiary['R'], 1)
            scenery.quaternary_color_BGRA = (quaternary['B'], quaternary['G'], quaternary['R'], 1)
            scenery.pathfinding_policy = scenery_element['Pathfinding Policy']['Value']
            scenery.lightmap_policy = scenery_element['Lightmapping Policy']['Value']
            scenery.valid_multiplayer_games = 0

            SCENARIO.scenery.append(scenery)

    SCENARIO.scenery_header = tag_block_header(TAG, "tbfd", 4, len(SCENARIO.scenery), 96)

def get_unit(dump_dic, TAG, SCENARIO, unit):
    unit_tag_block = dump_dic['Data'][unit]
    unit_list = []
    for unit_element in unit_tag_block:
        primary = unit_element['Primary Color']
        secondary = unit_element['Secondary Color']
        tertiary = unit_element['Tertiary Color']
        quaternary = unit_element['Quaternary Color']

        unit = SCENARIO.Unit()

        unit.sobj_header = tag_block_header(TAG, "sobj", 1, 1, 48)
        unit.obj0_header = tag_block_header(TAG, "obj#", 0, 1, 8)
        unit.sper_header = tag_block_header(TAG, "sper", 0, 1, 24)
        unit.sunt_header = tag_block_header(TAG, "sunt", 0, 1, 8)

        unit.palette_index = unit_element['Palette Index']
        unit.name_index = unit_element['Name Index']
        unit.placement_flags = unit_element['Placement Flags']
        unit.position = unit_element['Position']
        unit.rotation = unit_element['Rotation']
        unit.scale = unit_element['Scale']
        unit.transform_flags = unit_element['Transform Flags']
        unit.manual_bsp_flags = unit_element['Manual BSP Flags']
        unit.unique_id = unit_element['Unique ID']
        unit.origin_bsp_index = unit_element['Origin BSP Index']
        unit.object_type = unit_element['Type']['Value']
        unit.source = unit_element['Source']['Value']
        unit.bsp_policy = 0
        unit.editor_folder_index = -1

        unit.variant_name_length = 0
        unit.active_change_colors = 0
        unit.primary_color_BGRA = (primary['B'], primary['G'], primary['R'], 1)
        unit.secondary_color_BGRA = (secondary['B'], secondary['G'], secondary['R'], 1)
        unit.tertiary_color_BGRA = (tertiary['B'], tertiary['G'], tertiary['R'], 1)
        unit.quaternary_color_BGRA = (quaternary['B'], quaternary['G'], quaternary['R'], 1)
        unit.body_vitality = 0
        unit.flags = 0

        unit_list.append(unit)

    return tag_block_header(TAG, "tbfd", 2, len(unit_list), 84), unit_list

def get_equipment(dump_dic, TAG, SCENARIO):
    equipment_tag_block = dump_dic['Data']['Equipment']
    SCENARIO.equipment = []
    for equipment_element in equipment_tag_block:
        equipment = SCENARIO.Equipment()

        equipment.sobj_header = tag_block_header(TAG, "sobj", 1, 1, 48)
        equipment.obj0_header = tag_block_header(TAG, "obj#", 0, 1, 8)
        equipment.seqt_header = tag_block_header(TAG, "seqt", 0, 1, 4)

        equipment.palette_index = equipment_element['Palette Index']
        equipment.name_index = equipment_element['Name Index']
        equipment.placement_flags = equipment_element['Placement Flags']
        equipment.position = equipment_element['Position']
        equipment.rotation = equipment_element['Rotation']
        equipment.scale = equipment_element['Scale']
        equipment.transform_flags = equipment_element['Transform Flags']
        equipment.manual_bsp_flags = equipment_element['Manual BSP Flags']
        equipment.unique_id = equipment_element['Unique ID']
        equipment.origin_bsp_index = equipment_element['Origin BSP Index']
        equipment.object_type = equipment_element['Type']['Value']
        equipment.source = equipment_element['Source']['Value']
        equipment.bsp_policy = 0
        equipment.editor_folder_index = -1

        equipment.flags = 0

        SCENARIO.equipment.append(equipment)

    SCENARIO.equipment_header = tag_block_header(TAG, "tbfd", 2, len(SCENARIO.equipment), 56)

def get_weapon(dump_dic, TAG, SCENARIO):
    weapon_tag_block = dump_dic['Data']['Weapons']
    SCENARIO.weapons = []
    for weapon_element in weapon_tag_block:
        primary = weapon_element['Primary Color']
        secondary = weapon_element['Secondary Color']
        tertiary = weapon_element['Tertiary Color']
        quaternary = weapon_element['Quaternary Color']

        weapon = SCENARIO.Weapon()

        weapon.sobj_header = tag_block_header(TAG, "sobj", 1, 1, 48)
        weapon.obj0_header = tag_block_header(TAG, "obj#", 0, 1, 8)
        weapon.sper_header = tag_block_header(TAG, "sper", 0, 1, 24)
        weapon.swpt_header = tag_block_header(TAG, "swpt", 0, 1, 8)

        weapon.palette_index = weapon_element['Palette Index']
        weapon.name_index = weapon_element['Name Index']
        weapon.placement_flags = weapon_element['Placement Flags']
        weapon.position = weapon_element['Position']
        weapon.rotation = weapon_element['Rotation']
        weapon.scale = weapon_element['Scale']
        weapon.transform_flags = weapon_element['Transform Flags']
        weapon.manual_bsp_flags = weapon_element['Manual BSP Flags']
        weapon.unique_id = weapon_element['Unique ID']
        weapon.origin_bsp_index = weapon_element['Origin BSP Index']
        weapon.object_type = weapon_element['Type']['Value']
        weapon.source = weapon_element['Source']['Value']
        weapon.bsp_policy = 0
        weapon.editor_folder_index = -1

        weapon.variant_name_length = 0
        weapon.active_change_colors = 0
        weapon.primary_color_BGRA = (primary['B'], primary['G'], primary['R'], 1)
        weapon.secondary_color_BGRA = (secondary['B'], secondary['G'], secondary['R'], 1)
        weapon.tertiary_color_BGRA = (tertiary['B'], tertiary['G'], tertiary['R'], 1)
        weapon.quaternary_color_BGRA = (quaternary['B'], quaternary['G'], quaternary['R'], 1)
        weapon.rounds_left = 0
        weapon.rounds_loaded = 0
        weapon.flags = 0

        SCENARIO.weapons.append(weapon)

    SCENARIO.weapon_header = tag_block_header(TAG, "tbfd", 2, len(SCENARIO.weapons), 84)

def get_trigger_volumes(dump_dic, TAG, SCENARIO):
    trigger_volumes_tag_block = dump_dic['Data']['Kill Trigger Volumes']
    SCENARIO.trigger_volumes = []
    for trigger_volume_element in trigger_volumes_tag_block:
        trigger_volume = SCENARIO.TriggerVolume()

        trigger_volume.name = TAG.string_to_bytes(trigger_volume_element['Name'], False)
        trigger_volume.name_length = len(trigger_volume_element['Name'])
        trigger_volume.object_name_index = -1
        trigger_volume.node_name = TAG.string_to_bytes("", False)
        trigger_volume.forward = trigger_volume_element['Forward']
        trigger_volume.up = trigger_volume_element['Up']
        trigger_volume.position = trigger_volume_element['Position']
        trigger_volume.extents = trigger_volume_element['Extents']
        trigger_volume.kill_trigger_volume_index = -1

        SCENARIO.trigger_volumes.append(trigger_volume)

    SCENARIO.trigger_volumes_header = tag_block_header(TAG, "tbfd", 1, len(SCENARIO.trigger_volumes), 68)

def get_decals(dump_dic, TAG, SCENARIO):
    decals_tag_block = dump_dic['Data']['Decals']
    SCENARIO.decals = []
    for decal_element in decals_tag_block:
        decal = SCENARIO.Decal()

        decal.palette_index = decal_element['Palette Index']
        decal.yaw = decal_element['Yaw']
        decal.pitch = decal_element['Pitch']
        decal.position = decal_element['Position']

        SCENARIO.decals.append(decal)

    SCENARIO.decals_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.decals), 16)

def get_squad_groups(dump_dic, TAG, SCENARIO):
    squad_groups_tag_block = dump_dic['Data']['Squad Groups']
    SCENARIO.squad_groups = []
    for squad_group_element in squad_groups_tag_block:
        squad_group = SCENARIO.SquadGroups()

        squad_group.name = TAG.string_to_bytes(squad_group_element['Name'], False)
        squad_group.parent_index = squad_group_element['Parent Index']
        squad_group.initial_order_index = squad_group_element['Initial Order Index']

        SCENARIO.squad_groups.append(squad_group)

    SCENARIO.squad_groups_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.squad_groups), 36)

def get_squads(dump_dic, TAG, SCENARIO):
    squads_tag_block = dump_dic['Data']['Squads']
    SCENARIO.squads = []
    for squad_element in squads_tag_block:
        starting_locations_dic = squad_element['Starting Locations']
        starting_location_count = len(starting_locations_dic)

        squad = SCENARIO.Squad()

        squad.name = TAG.string_to_bytes(squad_element['Name'], False)
        squad.flags = squad_element['Flags']
        squad.team = squad_element['Team']['Value']
        squad.parent_squad_group_index = squad_element['Parent Squad Group Index']
        squad.squad_delay_time = squad_element['Squad Delay Time']
        squad.normal_difficulty_count = squad_element['Normal Difficulty Count']
        squad.insane_difficulty_count = squad_element['Insane Difficulty Count']
        squad.major_upgrade = squad_element['Major Upgrade']['Value']
        squad.vehicle_type_index = squad_element['Vehicle Type Index']
        squad.character_type_index = squad_element['Character Type Index']
        squad.initial_zone_index = squad_element['Initial Zone Index']
        squad.initial_weapon_index = squad_element['Initial Weapon Index']
        squad.initial_secondary_weapon_index = -1
        squad.grenade_type = squad_element['Grenade Type']['Value']
        squad.initial_order_index = squad_element['Initial Order Index']
        squad.vehicle_variant_length = 0
        squad.starting_locations_tag_block = tag_block(TAG, starting_location_count, 0, 0, 0)
        squad.placement_script = TAG.string_to_bytes("", False)

        if starting_location_count > 0:
            squad.starting_locations_header = tag_block_header(TAG, "tbfd", 6, starting_location_count, 100)
            starting_locations = []
            for starting_location_element in starting_locations_dic:
                starting_location = SCENARIO.StartingLocation()

                starting_location.name = TAG.string_to_bytes(starting_location_element['Name'], False)
                starting_location.name_length = len(starting_location_element['Name'])
                starting_location.position = starting_location_element['Position']
                starting_location.reference_frame = -1
                starting_location.facing_y = starting_location_element['Facing']
                starting_location.facing_p = 0
                starting_location.flags = 0
                starting_location.character_type_index = starting_location_element['Character Type Index']
                starting_location.initial_weapon_index = starting_location_element['Initial Weapon Index']
                starting_location.initial_secondary_weapon_index = -1
                starting_location.vehicle_type_index = starting_location_element['Vehicle Type Index']
                starting_location.seat_type = starting_location_element['Seat Type']['Value']
                starting_location.grenade_type = starting_location_element['Grenade Type']['Value']
                starting_location.swarm_count = 0
                starting_location.actor_variant_name_length = 0
                starting_location.vehicle_variant_name_length = 0
                starting_location.initial_movement_distance = 0
                starting_location.emitter_vehicle_index = -1
                starting_location.initial_movement_mode = 0
                starting_location.placement_script = TAG.string_to_bytes("", False)

                starting_locations.append(starting_location)

            squad.starting_locations = starting_locations

        SCENARIO.squads.append(squad)

    SCENARIO.squads_header = tag_block_header(TAG, "tbfd", 2, len(SCENARIO.squads), 120)

def get_zones(dump_dic, TAG, SCENARIO):
    zones_tag_block = dump_dic['Data']['Zones']
    SCENARIO.zones = []
    for zone_element in zones_tag_block:
        firing_positions_dic = zone_element['Firing Positions']
        firing_positions_count = len(firing_positions_dic)

        areas_dic = zone_element['Areas']
        areas_count = len(areas_dic)

        zone = SCENARIO.Zone()

        zone.name = TAG.string_to_bytes(zone_element['Name'], False)
        zone.flags = zone_element['Flags']
        zone.manual_bsp_index = zone_element['Manual BSP Index']
        zone.firing_positions_tag_block = tag_block(TAG, firing_positions_count, 0, 0, 0)
        zone.areas_tag_block = tag_block(TAG, areas_count, 0, 0, 0)
        zone.firing_positions = []
        zone.areas = []
        if firing_positions_count > 0:
            zone.firing_positions_header = tag_block_header(TAG, "tbfd", 3, firing_positions_count, 32)
            for firing_position_element in firing_positions_dic:
                firing_position = SCENARIO.FiringPosition()

                firing_position.position = firing_position_element['Position']
                firing_position.reference_frame = -1
                firing_position.flags = 0
                firing_position.area_index = firing_position_element['Area Index']
                firing_position.cluster_index = firing_position_element['Cluster Index']
                firing_position.normal_y = firing_position_element['Normal']

                zone.firing_positions.append(firing_position)

        if areas_count > 0:
            zone.areas_header = tag_block_header(TAG, "tbfd", 1, areas_count, 140)

            for areas_element in areas_dic:
                area = SCENARIO.Area()

                area.name = TAG.string_to_bytes(areas_element['Name'], False)
                area.flags = 0
                area.runtime_starting_index = 0
                area.runtime_count = 0
                area.manual_reference_frame = areas_element['Manual Reference Frame']
                area.flight_hints_tag_block = tag_block(TAG, 0, 0, 0, 0)

                zone.areas.append(area)

        SCENARIO.zones.append(zone)

    SCENARIO.zones_header = tag_block_header(TAG, "tbfd", 1, len(SCENARIO.zones), 64)

def get_scripting_data(dump_dic, TAG, SCENARIO):
    scripting_data_tag_block = dump_dic['Data']['Scripting Data']
    SCENARIO.scripting_data = []
    for scripting_data_element in scripting_data_tag_block:
        point_sets_dic = scripting_data_element['Point Sets']
        point_sets_count = len(point_sets_dic)

        scripting_data = SCENARIO.ScriptingData()

        scripting_data.point_sets_tag_block = tag_block(TAG, point_sets_count, 0, 0, 0)
        scripting_data.point_sets = []

        if point_sets_count > 0:
            scripting_data.point_sets_header = tag_block_header(TAG, "tbfd", 1, point_sets_count, 52)
            for point_set_element in point_sets_dic:
                points_dic = point_set_element['Points']
                points_count = len(points_dic)

                point_set = SCENARIO.PointSet()

                point_set.name = TAG.string_to_bytes(point_set_element['Name'], False)
                point_set.points_tag_block = tag_block(TAG, points_count, 0, 0, 0)
                point_set.bsp_index = point_set_element['BSP Index']
                point_set.manual_reference_frame = point_set_element['Manual Reference Frame']
                point_set.flags = point_set_element['Flags']
                point_set.points = []

                if points_count > 0:
                    point_set.points_header = tag_block_header(TAG, "tbfd", 1, points_count, 60)
                    for point_element in points_dic:
                        point = SCENARIO.Point()

                        point.name = TAG.string_to_bytes(point_element['Name'], False)
                        point.position = point_element['Position']
                        point.reference_frame = -1
                        point.surface_index = -1
                        point.facing_direction_y = 0.0
                        point.facing_direction_p = 0.0

                        point_set.points.append(point)

                scripting_data.point_sets.append(point_set)

        SCENARIO.scripting_data.append(scripting_data)

    SCENARIO.scripting_data_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.scripting_data), 132)

def get_cutscene_flags(dump_dic, TAG, SCENARIO):
    cutscene_flags_tag_block = dump_dic['Data']['Cutscene Flags']
    SCENARIO.cutscene_flags = []
    for cutscene_flag_element in cutscene_flags_tag_block:
        cutscene_flags = SCENARIO.CutsceneFlags()

        cutscene_flags.name = TAG.string_to_bytes(cutscene_flag_element['Name'], False)
        cutscene_flags.position = cutscene_flag_element['Position']
        cutscene_flags.facing_y = cutscene_flag_element['Facing'][0]
        cutscene_flags.facing_p = cutscene_flag_element['Facing'][1]

        SCENARIO.cutscene_flags.append(cutscene_flags)

    SCENARIO.cutscene_flags_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.cutscene_flags), 56)

def get_cutscene_camera_points(dump_dic, TAG, SCENARIO):
    cutscene_camera_points_tag_block = dump_dic['Data']['Cutscene Camera Points']
    SCENARIO.cutscene_camera_points = []
    for cutscene_camera_point_element in cutscene_camera_points_tag_block:
        cutscene_camera_point = SCENARIO.CutsceneCameraPoints()

        cutscene_camera_point.flags = cutscene_camera_point_element['Flags']
        cutscene_camera_point.camera_type = cutscene_camera_point_element['Type']['Value']
        cutscene_camera_point.name = TAG.string_to_bytes(cutscene_camera_point_element['Name'], False)
        cutscene_camera_point.position = cutscene_camera_point_element['Position']
        cutscene_camera_point.orientation = cutscene_camera_point_element['Orientation']

        SCENARIO.cutscene_camera_points.append(cutscene_camera_point)

    SCENARIO.cutscene_camera_points_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.cutscene_camera_points), 64)

def get_orders(dump_dic, TAG, SCENARIO):
    orders_tag_block = dump_dic['Data']['Orders']
    SCENARIO.orders = []
    for order_element in orders_tag_block:
        primary_area_set_dic = order_element['Primary Area Set']
        primary_area_set_count = len(primary_area_set_dic)

        #secondary_area_set_dic = order_element['Secondary Area Set']
        #secondary_area_set_count = len(secondary_area_set_dic)

        #secondary_set_trigger_dic = order_element['Secondary Set Trigger']
        #secondary_set_trigger_count = len(secondary_set_trigger_dic)

        #special_movement_dic = order_element['Special Movement']
        #special_movement_count = len(special_movement_dic)

        order_endings_dic = order_element['Order Endings']
        order_endings_count = len(order_endings_dic)

        order = SCENARIO.Order()

        order.name = TAG.string_to_bytes(order_element['Name'], False)
        order.style_index = order_element['Style Index']
        order.flags = order_element['Flags']
        order.force_combat_status = order_element['Force Combat Status']['Value']
        order.entry_script = TAG.string_to_bytes(order_element['Entry Script'], False)
        order.follow_squad = order_element['Follow Squad Index']
        order.follow_radius = order_element['Follow Radius']
        order.primary_area_set_tag_block = tag_block(TAG, primary_area_set_count, 0, 0, 0)
        order.secondary_area_set_tag_block = tag_block(TAG, 0, 0, 0, 0)
        order.secondary_set_trigger_tag_block = tag_block(TAG, 0, 0, 0, 0)
        order.special_movement_tag_block = tag_block(TAG, 0, 0, 0, 0)
        order.order_endings_tag_block = tag_block(TAG, order_endings_count, 0, 0, 0)

        order.primary_area_set = []
        order.order_endings = []

        if primary_area_set_count > 0:
            order.primary_area_set_header = tag_block_header(TAG, "tbfd", 1, primary_area_set_count, 8)
            for primary_area_set_element in primary_area_set_dic:
                primary_area_set = SCENARIO.PrimaryAreaSet()

                primary_area_set.area_type = primary_area_set_element['Area Type']['Value']
                primary_area_set.zone_index = primary_area_set_element['Zone Index']
                primary_area_set.area_index = primary_area_set_element['Area Index']

                order.primary_area_set.append(primary_area_set)

        if order_endings_count > 0:
            order.order_endings_header = tag_block_header(TAG, "tbfd", 0, order_endings_count, 24)
            for order_ending_element in order_endings_dic:
                triggers_dic = order_ending_element['Triggers']
                triggers_count = len(triggers_dic)

                order_ending = SCENARIO.OrderEnding()

                order_ending.next_order_index = order_ending_element['Next Order Index']
                order_ending.combination_rule = order_ending_element['Combination Rule']['Value']
                order_ending.delay_time = order_ending_element['Delay Time']
                order_ending.dialogue_type = order_ending_element['Dialogue Type']['Value']
                order_ending.triggers_tag_block = tag_block(TAG, triggers_count, 0, 0, 0)

                order_ending.triggers = []

                if len(triggers_dic) > 0:
                    order_ending.triggers_header = tag_block_header(TAG, "tbfd", 0, triggers_count, 8)
                    for trigger_element in triggers_dic:
                        trigger = SCENARIO.Trigger()

                        trigger.trigger_flags = trigger_element['Trigger Flags']
                        trigger.trigger_index = trigger_element['Trigger Index']

                        order_ending.triggers.append(trigger)

                order.order_endings.append(order_ending)

        SCENARIO.orders.append(order)

    SCENARIO.orders_header = tag_block_header(TAG, "tbfd", 2, len(SCENARIO.orders), 144)

def get_triggers(dump_dic, TAG, SCENARIO):
    triggers_tag_block = dump_dic['Data']['AI Triggers']
    SCENARIO.triggers = []
    for trigger_element in triggers_tag_block:
        conditions_dic = trigger_element['Conditions']
        conditions_count = len(conditions_dic)

        trigger = SCENARIO.AITrigger()

        trigger.name = TAG.string_to_bytes(trigger_element['Name'], False)
        trigger.trigger_flags = trigger_element['Trigger Flags']
        trigger.combination_rule = trigger_element['Combination Rule']['Value']
        trigger.conditions_tag_block = tag_block(TAG, conditions_count, 0, 0, 0)

        trigger.conditions = []

        if conditions_count > 0:
            trigger.conditions_header = tag_block_header(TAG, "tbfd", 0, conditions_count, 56)
            for condition_element in conditions_dic:
                condition = SCENARIO.Condition()

                condition.rule_type = condition_element['Rule Type']['Value']
                condition.squad_index = condition_element['Squad Index']
                condition.squad_group_index = condition_element['Squad Group Index']
                condition.a = condition_element['A']
                condition.x = condition_element['X']
                condition.trigger_volume_index = condition_element['Trigger Volume Index']
                condition.exit_condition_script = TAG.string_to_bytes(condition_element['Exit Condition Script'], False)
                condition.exit_condition_script_index = condition_element['Exit Condition Script Index']
                condition.flags = condition_element['Flags']

                trigger.conditions.append(condition)

        SCENARIO.triggers.append(trigger)

    SCENARIO.triggers_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.triggers), 52)

def get_palette(dump_dic, TAG, palette_element_keyword, palette_keyword, size):
    palette_tag_block = dump_dic['Data'][palette_keyword]
    palette_list = []
    for palette_element in palette_tag_block:
        tag_ref = palette_element[palette_element_keyword]
        tag_group = TAG.string_to_bytes(tag_ref['GroupName'], True)
        tag_path = TAG.string_to_bytes(os.path.normpath(tag_ref['Path']), False)
        tag_reference = TAG.TagRef()
        tag_reference.tag_group = tag_group
        tag_reference.name = tag_path
        tag_reference.name_length = len(tag_path)
        tag_reference.salt = 0
        tag_reference.index = -1

        palette_list.append(tag_reference)

    return tag_block_header(TAG, "tbfd", 0, len(palette_list), size), palette_list

def process_json(input_stream, tag_format, report):
    dump_dic = json.load(input_stream)

    TAG = tag_format.TagAsset()
    SCENARIO = ScenarioAsset()

    SCENARIO.header = TAG.Header()
    SCENARIO.header.unk1 = 0
    SCENARIO.header.flags = 0
    SCENARIO.header.type = 0
    SCENARIO.header.name = TAG.string_to_bytes("", False)
    SCENARIO.header.tag_group = TAG.string_to_bytes("scnr", True)
    SCENARIO.header.checksum = 0
    SCENARIO.header.data_offset = 64
    SCENARIO.header.data_length = 0
    SCENARIO.header.unk2 = 0
    SCENARIO.header.version = 2
    SCENARIO.header.destination = 0
    SCENARIO.header.plugin_handle = -1
    SCENARIO.header.engine_tag = TAG.string_to_bytes("BLM!", True)

    get_object_names(dump_dic, TAG, SCENARIO)

    get_scenery(dump_dic, TAG, SCENARIO)
    SCENARIO.scenery_palette_header, SCENARIO.scenery_palette = get_palette(dump_dic, TAG, 'Scenery', 'Scenery Palette', 48)

    SCENARIO.bipeds_header, SCENARIO.bipeds = get_unit(dump_dic, TAG, SCENARIO, 'Bipeds')
    SCENARIO.biped_palette_header, SCENARIO.biped_palette = get_palette(dump_dic, TAG, 'Biped', 'Biped Palette', 48)

    SCENARIO.vehicles_header, SCENARIO.vehicles = get_unit(dump_dic, TAG, SCENARIO, 'Vehicles')
    SCENARIO.vehicle_palette_header, SCENARIO.vehicle_palette = get_palette(dump_dic, TAG, 'Vehicle', 'Vehicle Palette', 48)

    get_equipment(dump_dic, TAG, SCENARIO)
    SCENARIO.equipment_palette_header, SCENARIO.equipment_palette = get_palette(dump_dic, TAG, 'Equipment', 'Equipment Palette', 48)

    get_weapon(dump_dic, TAG, SCENARIO)
    SCENARIO.weapon_palette_header, SCENARIO.weapon_palette = get_palette(dump_dic, TAG, 'Weapon', 'Weapon Palette', 48)

    get_trigger_volumes(dump_dic, TAG, SCENARIO)

    get_decals(dump_dic, TAG, SCENARIO)
    SCENARIO.decal_palette_header, SCENARIO.decal_palette = get_palette(dump_dic, TAG, 'Decal', 'Decal Palette', 16)

    SCENARIO.style_palette_header, SCENARIO.style_palette = get_palette(dump_dic, TAG, 'Style', 'Style Palette', 16)

    get_squad_groups(dump_dic, TAG, SCENARIO)

    get_squads(dump_dic, TAG, SCENARIO)

    get_zones(dump_dic, TAG, SCENARIO)

    SCENARIO.character_palette_header, SCENARIO.character_palette = get_palette(dump_dic, TAG, 'Character', 'Character Palette', 16)

    get_scripting_data(dump_dic, TAG, SCENARIO)

    get_cutscene_flags(dump_dic, TAG, SCENARIO)

    get_cutscene_camera_points(dump_dic, TAG, SCENARIO)

    get_orders(dump_dic, TAG, SCENARIO)

    get_triggers(dump_dic, TAG, SCENARIO)

    SCENARIO.scenario_body_header = tag_block_header(TAG, "tbfd", 2, 1, 1476)
    SCENARIO.scenario_body = SCENARIO.ScenarioBody()
    SCENARIO.scenario_body.unused_tag_ref = TAG.TagRef(TAG.string_to_bytes("sbsp", True), "", 0, 0, -1)
    SCENARIO.scenario_body.skies_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.scenario_type = 0
    SCENARIO.scenario_body.scenario_flags = 0
    SCENARIO.scenario_body.child_scenarios_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.local_north = radians(0)
    SCENARIO.scenario_body.predicted_resources_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.functions_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.editor_scenario_data = TAG.RawData(0, 0, 0, 0, 0)
    SCENARIO.scenario_body.comments_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.environment_objects_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.object_names_tag_block = TAG.TagBlock(len(SCENARIO.object_names), 0, 0, 0)
    SCENARIO.scenario_body.scenery_tag_block = TAG.TagBlock(len(SCENARIO.scenery), 0, 0, 0)
    SCENARIO.scenario_body.scenery_palette_tag_block = TAG.TagBlock(len(SCENARIO.scenery_palette), 0, 0, 0)
    SCENARIO.scenario_body.bipeds_tag_block = TAG.TagBlock(len(SCENARIO.bipeds), 0, 0, 0)
    SCENARIO.scenario_body.biped_palette_tag_block = TAG.TagBlock(len(SCENARIO.biped_palette), 0, 0, 0)
    SCENARIO.scenario_body.vehicles_tag_block = TAG.TagBlock(len(SCENARIO.vehicles), 0, 0, 0)
    SCENARIO.scenario_body.vehicle_palette_tag_block = TAG.TagBlock(len(SCENARIO.vehicle_palette), 0, 0, 0)
    SCENARIO.scenario_body.equipment_tag_block = TAG.TagBlock(len(SCENARIO.equipment), 0, 0, 0)
    SCENARIO.scenario_body.equipment_palette_tag_block = TAG.TagBlock(len(SCENARIO.equipment_palette), 0, 0, 0)
    SCENARIO.scenario_body.weapons_tag_block = TAG.TagBlock(len(SCENARIO.weapons), 0, 0, 0)
    SCENARIO.scenario_body.weapon_palette_tag_block = TAG.TagBlock(len(SCENARIO.weapon_palette), 0, 0, 0)
    SCENARIO.scenario_body.device_groups_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.machines_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.machine_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.controls_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.control_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.light_fixtures_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.light_fixtures_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.sound_scenery_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.sound_scenery_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.light_volumes_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.light_volume_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.player_starting_profile_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.player_starting_locations_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.trigger_volumes_tag_block = TAG.TagBlock(len(SCENARIO.trigger_volumes), 0, 0, 0)
    SCENARIO.scenario_body.recorded_animations_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.netgame_flags_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.netgame_equipment_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.starting_equipment_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.bsp_switch_trigger_volumes_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.decals_tag_block = TAG.TagBlock(len(SCENARIO.decals), 0, 0, 0)
    SCENARIO.scenario_body.decal_palette_tag_block = TAG.TagBlock(len(SCENARIO.decal_palette), 0, 0, 0)
    SCENARIO.scenario_body.detail_object_collection_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.style_palette_tag_block = TAG.TagBlock(len(SCENARIO.style_palette), 0, 0, 0)
    SCENARIO.scenario_body.squad_groups_tag_block = TAG.TagBlock(len(SCENARIO.squad_groups), 0, 0, 0)
    SCENARIO.scenario_body.squads_tag_block = TAG.TagBlock(len(SCENARIO.squads), 0, 0, 0)
    SCENARIO.scenario_body.zones_tag_block = TAG.TagBlock(len(SCENARIO.zones), 0, 0, 0)
    SCENARIO.scenario_body.mission_scenes_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.character_palette_tag_block = TAG.TagBlock(len(SCENARIO.character_palette), 0, 0, 0)
    SCENARIO.scenario_body.ai_pathfinding_data_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.ai_animation_references_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.ai_script_references_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.ai_recording_references_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.ai_conversations_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.script_syntax_data_tag_data = TAG.RawData(0, 0, 0, 0, 0)
    SCENARIO.scenario_body.script_string_data_tag_data = TAG.RawData(0, 0, 0, 0, 0)
    SCENARIO.scenario_body.scripts_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.globals_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.references_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.source_files_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.scripting_data_tag_block = TAG.TagBlock(len(SCENARIO.scripting_data), 0, 0, 0)
    SCENARIO.scenario_body.cutscene_flags_tag_block = TAG.TagBlock(len(SCENARIO.cutscene_flags), 0, 0, 0)
    SCENARIO.scenario_body.cutscene_camera_points_tag_block = TAG.TagBlock(len(SCENARIO.cutscene_camera_points), 0, 0, 0)
    SCENARIO.scenario_body.cutscene_titles_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.custom_object_names_tag_ref = TAG.TagRef(TAG.string_to_bytes("unic", True), "", 0, 0, -1)
    SCENARIO.scenario_body.chapter_title_text_tag_ref = TAG.TagRef(TAG.string_to_bytes("unic", True), "", 0, 0, -1)
    SCENARIO.scenario_body.hud_messages_tag_ref = TAG.TagRef(TAG.string_to_bytes("hmt ", True), "", 0, 0, -1)
    SCENARIO.scenario_body.structure_bsps_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.scenario_resources_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.old_structure_physics_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.hs_unit_seats_tag_block =TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.scenario_kill_triggers_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.hs_syntax_datums_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.orders_tag_block = TAG.TagBlock(len(SCENARIO.orders), 0, 0, 0)
    SCENARIO.scenario_body.triggers_tag_block = TAG.TagBlock(len(SCENARIO.triggers), 0, 0, 0)
    SCENARIO.scenario_body.background_sound_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.sound_environment_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.weather_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.unused_0_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.unused_1_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.unused_2_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.unused_3_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.scavenger_hunt_objects_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.scenario_cluster_data_tag_block = TAG.TagBlock(0, 0, 0, 0)

    SCENARIO.scenario_body.salt_array = []
    for salt_idx in range(SALT_SIZE):
        SCENARIO.scenario_body.salt_array.append(0)

    SCENARIO.scenario_body.spawn_data_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.sound_effect_collection_tag_ref = TAG.TagRef(TAG.string_to_bytes("sfx+", True), "", 0, 0, -1)
    SCENARIO.scenario_body.crates_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.crate_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.global_lighting_tag_ref = TAG.TagRef(TAG.string_to_bytes("gldf", True), "", 0, 0, -1)
    SCENARIO.scenario_body.atmospheric_fog_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.planar_fog_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.flocks_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.subtitles_tag_ref = TAG.TagRef(TAG.string_to_bytes("unic", True), "", 0, 0, -1)
    SCENARIO.scenario_body.decorators_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.creatures_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.creature_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.decorator_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.bsp_transition_volumes_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.structure_bsp_lighting_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.editor_folders_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.level_data_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.game_engine_strings_tag_ref = TAG.TagRef(TAG.string_to_bytes("unic", True), "", 0, 0, -1)
    SCENARIO.scenario_body.mission_dialogue_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.objectives_tag_ref = TAG.TagRef(TAG.string_to_bytes("unic", True), "", 0, 0, -1)
    SCENARIO.scenario_body.interpolators_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.shared_references_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.screen_effect_references_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.simulation_definition_table_tag_block = TAG.TagBlock(0, 0, 0, 0)

    return SCENARIO
