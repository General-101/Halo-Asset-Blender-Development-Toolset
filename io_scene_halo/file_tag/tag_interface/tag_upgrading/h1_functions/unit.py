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

from enum import Flag, Enum, auto

class FunctionEnum(Enum):
    none = 0
    driver_seat_power = auto()
    gunner_seat_power = auto()
    aiming_change = auto()
    mouth_aperture = auto()
    integrated_light_power = auto()
    can_blink = auto()
    shield_sapping = auto()
    driver_seat_occupied = auto()
    gunner_seat_occupied = auto()

class MetaGameTypeEnum(Enum):
    brute = 0
    grunt = auto()
    jackal = auto()
    skirmisher = auto()
    marine = auto()
    spartan = auto()
    bugger = auto()
    hunter = auto()
    flood_infection = auto()
    flood_carrier = auto()
    flood_combat = auto()
    flood_pure = auto()
    sentinel = auto()
    elite = auto()
    engineer = auto()
    mule = auto()
    turret = auto()
    mongoose = auto()
    warthog = auto()
    scorpion = auto()
    hornet = auto()
    pelican = auto()
    revenant = auto()
    seraph = auto()
    shade = auto()
    watchtower = auto()
    ghost = auto()
    chopper = auto()
    mauler = auto()
    wraith = auto()
    banshee = auto()
    phantom = auto()
    scarab = auto()
    guntower = auto()
    tuning_fork = auto()
    broadsword = auto()
    mammoth = auto()
    lich = auto()
    mantis = auto()
    wasp = auto()
    phaeton = auto()
    bishop = auto()
    knight = auto()
    pawn = auto()

class MetaGameClassEnum(Enum):
    infantry = 0
    leader = auto()
    hero = auto()
    specialist = auto()
    light_vehicle = auto()
    heavy_vehicle = auto()
    giant_vehicle = auto()
    standard_vehicle = auto()

def get_hand_defaults(dump_dic):
    right_hand_node = ""
    left_hand_node = ""
    preferred_gun_node = ""
    tag_file_name = os.path.basename(dump_dic["TagName"]).lower().replace(" ", "_")
    if "brute" in tag_file_name:
        right_hand_node = "right_hand"
        left_hand_node = "left_hand"
        preferred_gun_node = "right_hand_brute"
    elif "elite" in tag_file_name:
        right_hand_node = "right_hand_elite"
        left_hand_node = "left_hand_elite"
    elif "grunt" in tag_file_name:
        right_hand_node = "right_hand"
        left_hand_node = "left_hand"
    elif "jackal" in tag_file_name:
        right_hand_node = "left_hand_jackal"
        left_hand_node = "left_hand"
        preferred_gun_node = "left_hand_jackal"
    elif "marine" in tag_file_name:
        right_hand_node = "right_hand"
        left_hand_node = "left_hand"
        preferred_gun_node = "left_hand_marine"
    elif "masterchief" in tag_file_name:
        right_hand_node = "right_hand"
        left_hand_node = "left_hand"
        preferred_gun_node = "right_hand_mc"

    return right_hand_node, left_hand_node, preferred_gun_node

def generate_new_hud_interface(dump_dic):
    new_hud_interface_block = []
    for new_hud_interface_element in dump_dic["Data"]["new hud interfaces"]:
        new_hud_interface_dict = {
            "new unit hud interface": new_hud_interface_element["hud"]
        }

        new_hud_interface_block.append(new_hud_interface_dict)

    return new_hud_interface_block

def generate_dialogue_variants(dump_dic):
    dialogue_variant_block = []
    for dialogue_variant_element in dump_dic["Data"]["dialogue variants"]:
        dialogue_variant_dict = {
            "variant number": dialogue_variant_element["variant number"],
            "dialogue": dialogue_variant_element["dialogue"]
        }

        dialogue_variant_block.append(dialogue_variant_dict)

    return dialogue_variant_block

def generate_powered_seats(dump_dic):
    powered_seats_block = []
    for powered_seat_element in dump_dic["Data"]["powered seats"]:
        powered_seat_dict = {
            "driver powerup time": powered_seat_element["driver powerup time"],
            "driver powerdown time": powered_seat_element["driver powerdown time"]
        }

        powered_seats_block.append(powered_seat_dict)

    return powered_seats_block

def generate_weapons(dump_dic):
    weapons_block = []
    for weapon_element in dump_dic["Data"]["weapons"]:
        weapon_dict = {
            "weapon": weapon_element["weapon"]
        }

        weapons_block.append(weapon_dict)

    return weapons_block

def generate_seats(dump_dic):
    seats_block = []
    for seat_element in dump_dic["Data"]["seats"]:
        i, j, k = seat_element["acceleration scale"]
        seat_dict = {
            "flags": seat_element["flags"],
            "label": seat_element["label"],
            "marker name": seat_element["marker name"],
            "entry marker(s) name": "",
            "boarding grenade marker": "",
            "boarding grenade string": "",
            "boarding melee string": "",
            "ping scale": 0.0,
            "turnover time": 0.0,
            "acceleration range": [(i * 30), (j * 30), (k * 30)],
            "accel action scale": 0.0,
            "accel attach scale": 0.0,
            "AI scariness": 0.0,
            "ai seat type": {
                "type": "ShortEnum",
                "value": 0,
                "value name": ""
            },
            "boarding seat": -1,
            "listener interpolation factor": 0.0,
            "yaw rate bounds": {
                "Min": seat_element["yaw rate"],
                "Max": seat_element["yaw rate"]
            },
            "pitch rate bounds": {
                "Min": seat_element["pitch rate"],
                "Max": seat_element["pitch rate"]
            },
            "min speed reference": 0.0,
            "max speed reference": 0.0,
            "speed exponent": 0.0,
            "camera marker name": seat_element["camera marker name"],
            "camera submerged marker name": seat_element["camera submerged marker name"],
            "pitch auto-level": seat_element["pitch auto level"],
            "pitch range": seat_element["pitch range"],
            "camera tracks": seat_element["camera tracks"],
            "unit hud interface": seat_element["hud interface"],
            "enter seat string": "",
            "yaw minimum": seat_element["yaw minimum"],
            "yaw maximum": seat_element["yaw maximum"],
            "built-in gunner": {
                "group name": "char",
                "path": seat_element["built in gunner"]["path"]
            },
            "entry radius": 0.0,
            "entry marker cone angle": 0.0,
            "entry marker facing angle": 0.0,
            "maximum relative velocity": 0.0,
            "invisible seat region": "",
            "runtime invisible seat region index": 0
        }

        seats_block.append(seat_dict)

    return seats_block

def get_metagame_data(dump_dic):
    unit_type = 0
    unit_class = 0
    tag_file_name = os.path.basename(dump_dic['TagName']).lower().replace(" ", "_")
    if "brute" in tag_file_name:
        unit_type = MetaGameTypeEnum.brute.value
        unit_class = MetaGameClassEnum.infantry.value
    elif "grunt" in tag_file_name:
        unit_type = MetaGameTypeEnum.grunt.value
        unit_class = MetaGameClassEnum.infantry.value
    elif "jackal" in tag_file_name:
        unit_type = MetaGameTypeEnum.jackal.value
        unit_class = MetaGameClassEnum.infantry.value
    elif "skirmisher" in tag_file_name:
        unit_type = MetaGameTypeEnum.skirmisher.value
    elif "marine" in tag_file_name:
        unit_type = MetaGameTypeEnum.marine.value
        unit_class = MetaGameClassEnum.infantry.value
    elif "masterchief" in tag_file_name or "cyborg" in tag_file_name:
        unit_type = MetaGameTypeEnum.spartan.value
        unit_class = MetaGameClassEnum.infantry.value
    elif "bugger" in tag_file_name:
        unit_type = MetaGameTypeEnum.bugger.value
        unit_class = MetaGameClassEnum.infantry.value
    elif "hunter" in tag_file_name:
        unit_type = MetaGameTypeEnum.hunter.value
        unit_class = MetaGameClassEnum.specialist.value
    elif "flood_infection" in tag_file_name:
        unit_type = MetaGameTypeEnum.flood_infection.value
        unit_class = MetaGameClassEnum.infantry.value
    elif "flood_carrier" in tag_file_name:
        unit_type = MetaGameTypeEnum.flood_carrier.value
        unit_class = MetaGameClassEnum.infantry.value
    elif "floodcombat" in tag_file_name:
        unit_type = MetaGameTypeEnum.flood_combat.value
        unit_class = MetaGameClassEnum.infantry.value
    elif "flood_pure" in tag_file_name:
        unit_type = MetaGameTypeEnum.flood_pure.value
    elif "sentinel" in tag_file_name:
        unit_type = MetaGameTypeEnum.sentinel.value
        unit_class = MetaGameClassEnum.infantry.value
    elif "elite" in tag_file_name:
        unit_type = MetaGameTypeEnum.elite.value
        unit_class = MetaGameClassEnum.infantry.value
    elif "engineer" in tag_file_name:
        unit_type = MetaGameTypeEnum.engineer.value
    elif "mule" in tag_file_name:
        unit_type = MetaGameTypeEnum.mule.value
    elif "turret" in tag_file_name:
        unit_type = MetaGameTypeEnum.turret.value
        unit_class = MetaGameClassEnum.light_vehicle.value
    elif "mongoose" in tag_file_name:
        unit_type = MetaGameTypeEnum.mongoose.value
        unit_class = MetaGameClassEnum.light_vehicle.value
    elif "warthog" in tag_file_name:
        unit_type = MetaGameTypeEnum.warthog.value
        unit_class = MetaGameClassEnum.standard_vehicle.value
    elif "scorpion" in tag_file_name:
        unit_type = MetaGameTypeEnum.scorpion.value
        unit_class = MetaGameClassEnum.heavy_vehicle.value
    elif "hornet" in tag_file_name:
        unit_type = MetaGameTypeEnum.hornet.value
    elif "pelican" in tag_file_name:
        unit_type = MetaGameTypeEnum.pelican.value
        unit_class = MetaGameClassEnum.giant_vehicle.value
    elif "revenant" in tag_file_name:
        unit_type = MetaGameTypeEnum.revenant.value
    elif "seraph" in tag_file_name:
        unit_type = MetaGameTypeEnum.seraph.value
    elif "creep" in tag_file_name:
        unit_type = MetaGameTypeEnum.shade.value
        unit_class = MetaGameClassEnum.standard_vehicle.value
    elif "watchtower" in tag_file_name:
        unit_type = MetaGameTypeEnum.watchtower.value
    elif "ghost" in tag_file_name:
        unit_type = MetaGameTypeEnum.ghost.value
        unit_class = MetaGameClassEnum.light_vehicle.value
    elif "chopper" in tag_file_name:
        unit_type = MetaGameTypeEnum.chopper.value
    elif "mauler" in tag_file_name:
        unit_type = MetaGameTypeEnum.mauler.value
    elif "wraith" in tag_file_name:
        unit_type = MetaGameTypeEnum.wraith.value
        unit_class = MetaGameClassEnum.heavy_vehicle.value
    elif "banshee" in tag_file_name:
        unit_type = MetaGameTypeEnum.banshee.value
        unit_class = MetaGameClassEnum.standard_vehicle.value
    elif "phantom" in tag_file_name:
        unit_type = MetaGameTypeEnum.phantom.value
        unit_class = MetaGameClassEnum.giant_vehicle.value
    elif "scarab" in tag_file_name:
        unit_type = MetaGameTypeEnum.scarab.value
    elif "guntower" in tag_file_name:
        unit_type = MetaGameTypeEnum.guntower.value
        unit_class = MetaGameClassEnum.standard_vehicle.value
    elif "tuning_fork" in tag_file_name:
        unit_type = MetaGameTypeEnum.tuning_fork.value
    elif "broadsword" in tag_file_name:
        unit_type = MetaGameTypeEnum.broadsword.value
    elif "mammoth" in tag_file_name:
        unit_type = MetaGameTypeEnum.mammoth.value
    elif "lich" in tag_file_name:
        unit_type = MetaGameTypeEnum.lich.value
    elif "mantis" in tag_file_name:
        unit_type = MetaGameTypeEnum.mantis.value
    elif "wasp" in tag_file_name:
        unit_type = MetaGameTypeEnum.wasp.value
    elif "phaeton" in tag_file_name:
        unit_type = MetaGameTypeEnum.phaeton.value
    elif "bishop" in tag_file_name:
        unit_type = MetaGameTypeEnum.bishop.value
    elif "knight" in tag_file_name:
        unit_type = MetaGameTypeEnum.knight.value
    elif "pawn" in tag_file_name:
        unit_type = MetaGameTypeEnum.pawn.value
        unit_class = MetaGameClassEnum.standard_vehicle.value

    return unit_type, unit_class

def get_driver_string(dump_dic, seat_label):
    entry_string = ""
    tag_file_name = os.path.basename(dump_dic['TagName']).lower().replace(" ", "_")

    if seat_label.endswith("_d"):
        if "banshee" in tag_file_name:
            entry_string = "banshee_enter"
        elif "turret" in tag_file_name:
            entry_string = "turret_enter"
        elif "creep" in tag_file_name:
            entry_string = "shadow_enter_driver"
        elif "ghost" in tag_file_name:
            entry_string = "ghost_enter"
        elif "scorpion" in tag_file_name:
            entry_string = "scorpion_enter_driver"
        elif "spectre" in tag_file_name:
            entry_string = "spectre_enter_driver"
        elif "warthog" in tag_file_name:
            entry_string = "warthog_enter_driver"
        elif "wraith" in tag_file_name:
            entry_string = "wraith_enter_driver"
    elif "_b_" in seat_label:
        if "banshee" in tag_file_name:
            entry_string = "banshee_board"
        elif "ghost" in tag_file_name:
            entry_string = "ghost_board"
        elif "scorpion" in tag_file_name:
            entry_string = "scorpion_board"
        elif "spectre" in tag_file_name:
            entry_string = "spectre_board"
        elif "warthog" in tag_file_name:
            entry_string = "warthog_board"
        elif "wraith" in tag_file_name:
            entry_string = "wraith_board"
        elif "plasma_turret" in tag_file_name:
            entry_string = "spectre_board"
        elif "chaingun" in tag_file_name:
            entry_string = "warthog_board"
        elif "gauss" in tag_file_name:
            entry_string = "warthog_board"
        elif "mortar" in tag_file_name:
            entry_string = "wraith_board"
    elif "_p" in seat_label:
        if "creep" in tag_file_name:
            entry_string = "shadow_enter_passenger"
        elif "scorpion" in tag_file_name:
            entry_string = "scorpion_enter_passenger"
        elif "spectre" in tag_file_name:
            entry_string = "spectre_enter_passenger"
        elif "warthog" in tag_file_name:
            entry_string = "warthog_enter_passenger"
    elif "_g" in seat_label:
        if "plasma_turret" in tag_file_name:
            entry_string = "spectre_enter_gunner"
        elif "chaingun" in tag_file_name:
            entry_string = "warthog_enter_gunner"
        elif "gauss" in tag_file_name:
            entry_string = "warthog_enter_gunner"
        elif "spectre" in tag_file_name:
            entry_string = "spectre_enter_gunner"
        elif "warthog" in tag_file_name:
            entry_string = "warthog_enter_gunner"

    return entry_string
