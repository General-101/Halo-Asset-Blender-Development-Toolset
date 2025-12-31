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

from mathutils import Vector
from enum import Flag, Enum, auto

from ..h1_functions.object import (
    convert_object_flags, 
    generate_ai_properties, 
    generate_attachments, 
    generate_widgets, 
    generate_change_colors, 
    FunctionEnum as ObjectFunctionsEnum
    )

from ..h1_functions.materials import get_material_name

class H1ProjectileFlags(Flag):
    oriented_along_velocity = auto()
    ai_must_use_ballistic_aiming = auto()
    detonation_max_time_if_attached = auto()
    has_super_combining_explosion = auto()
    combine_initial_velocity_with_parent_velocity = auto()
    random_attached_detonation_time = auto()
    minimum_unattached_detonation_time = auto()

class H2ProjectileFlags(Flag):
    oriented_along_velocity = auto()
    ai_must_use_ballistic_aiming = auto()
    detonation_max_time_if_attached = auto()
    has_super_combining_explosion = auto()
    damage_scales_based_on_distance = auto()
    travels_instantaneously = auto()
    steering_adjusts_orientation = auto()
    dont_noise_up_steering = auto()
    can_track_behind_itself = auto()
    robotron_steering = auto()
    faster_when_owned_by_player = auto()

class ProjectileFunctionsEnum(Enum):
    none = 0
    range_remaining = auto()
    time_remaining = auto()
    tracer = auto()

class DamageReportingTypeEnum(Enum):
    teh_guardians11 = 0
    falling_damage = auto()
    generic_collision_damage = auto()
    generic_melee_damage = auto()
    generic_explosion = auto()
    magnum_pistol = auto()
    plasma_pistol = auto()
    needler = auto()
    smg = auto()
    plasma_rifle = auto()
    battle_rifle = auto()
    carbine = auto()
    shotgun = auto()
    sniper_rifle = auto()
    beam_rifle = auto()
    rocket_launcher = auto()
    flak_cannon = auto()
    brute_shot = auto()
    disintegrator = auto()
    brute_plasma_rifle = auto()
    energy_sword = auto()
    frag_grenade = auto()
    plasma_grenade = auto()
    flag_melee_damage = auto()
    bomb_melee_damage = auto()
    bomb_explosion_damage = auto()
    ball_melee_damage = auto()
    human_turret = auto()
    plasma_turret = auto()
    banshee = auto()
    ghost = auto()
    mongoose = auto()
    scorpion = auto()
    spectre_driver = auto()
    spectre_gunner = auto()
    warthog_driver = auto()
    warthog_gunner = auto()
    wraith = auto()
    tank = auto()
    sentinel_beam = auto()
    sentinel_rpg = auto()
    teleporter = auto()
    warthog_gunner_gauss = auto()
    warthog_gunner_rocket = auto()

class H1ResponseEnum(Enum):
    disappear = 0
    detonate = auto()
    reflect = auto()
    overpenetrate = auto()
    attach = auto()

class H2ResponseEnum(Enum):
    impact_detonate = 0
    fizzle = auto()
    overpenetrate = auto()
    attach = auto()
    bounce = auto()
    bounce_dud = auto()
    fizzle_ricochet = auto()

def convert_projectile_flags(object_flags):
    flags = 0
    active_h1_flags = H1ProjectileFlags(object_flags)
    if H1ProjectileFlags.oriented_along_velocity in active_h1_flags:
        flags += H2ProjectileFlags.oriented_along_velocity.value

    if H1ProjectileFlags.ai_must_use_ballistic_aiming in active_h1_flags:
        flags += H2ProjectileFlags.ai_must_use_ballistic_aiming.value

    if H1ProjectileFlags.detonation_max_time_if_attached in active_h1_flags:
        flags += H2ProjectileFlags.detonation_max_time_if_attached.value

    if H1ProjectileFlags.has_super_combining_explosion in active_h1_flags:
        flags += H2ProjectileFlags.has_super_combining_explosion.value

    return flags

def convert_legacy_response(response_index):
    h2_response_index = 0
    h1_response = H1ResponseEnum(response_index)
    if h1_response == H1ResponseEnum.disappear:
        h2_response_index = H2ResponseEnum.fizzle.value
    elif h1_response == H1ResponseEnum.detonate:
        h2_response_index = H2ResponseEnum.impact_detonate.value
    elif h1_response == H1ResponseEnum.reflect:
        h2_response_index = H2ResponseEnum.bounce.value
    elif h1_response == H1ResponseEnum.overpenetrate:
        h2_response_index = H2ResponseEnum.overpenetrate.value
    elif h1_response == H1ResponseEnum.attach:
        h2_response_index = H2ResponseEnum.attach.value
    return h2_response_index

def generate_projectile_defaults(dump_dic):
    combine_count = 0
    damage_report = DamageReportingTypeEnum.teh_guardians11.value
    if H1ProjectileFlags.has_super_combining_explosion in H1ProjectileFlags(dump_dic["Data"]["flags_1"]):
        # According to community members it takes 7 projectiles to do a super combine in Halo 1. 
        # In Halo 2 it is also 7 internally but because of how the check is done it becomes 8 effectively.
        # Doing 6 so that it's 7 ingame.
        combine_count = 6

    tag_path = dump_dic["TagName"].lower().replace(" ", "_").replace("-", "_")
    if tag_path.endswith(r"characters\sentinel\beam.projectile"):
        damage_report = DamageReportingTypeEnum.sentinel_beam.value
    elif tag_path.endswith(r"cinematics\effects\cortana_powerup_fx\info.projectile"):
        damage_report = DamageReportingTypeEnum.teh_guardians11.value
    elif tag_path.endswith(r"cinematics\effects\lights\covenant_blast_bolt\covenant_blast_bolt.projectile"):
        damage_report = DamageReportingTypeEnum.teh_guardians11.value
    elif tag_path.endswith(r"cinematics\effects\teleportation\teleport_ring.projectile"):
        damage_report = DamageReportingTypeEnum.teh_guardians11.value
    elif tag_path.endswith(r"cinematics\effects\teleportation\teleport_ring_fast.projectile"):
        damage_report = DamageReportingTypeEnum.teh_guardians11.value
    elif tag_path.endswith(r"digsite\ui\hud\effects\ar_reticle.projectile"):
        damage_report = DamageReportingTypeEnum.teh_guardians11.value
    elif tag_path.endswith(r"digsite\ui\hud\effects\reticle_ar.projectile"):
        damage_report = DamageReportingTypeEnum.teh_guardians11.value
    elif tag_path.endswith(r"digsite\ui\hud\effects\reticle_pr.projectile"):
        damage_report = DamageReportingTypeEnum.teh_guardians11.value
    elif tag_path.endswith(r"digsite\ui\hud\effects\reticle_rl.projectile"):
        damage_report = DamageReportingTypeEnum.teh_guardians11.value
    elif tag_path.endswith(r"digsite\vehicles\spectre\00_e3\c_spectre_gun_beam.projectile"):
        damage_report = DamageReportingTypeEnum.spectre_gunner.value
    elif tag_path.endswith(r"digsite\vehicles\spectre\_dig\spectre_dig.projectile"):
        damage_report = DamageReportingTypeEnum.spectre_gunner.value
    elif tag_path.endswith(r"digsite\vehicles\stealthtank\99_mac\shell_shrapnel.projectile"):
        damage_report = DamageReportingTypeEnum.scorpion.value
    elif tag_path.endswith(r"digsite\vehicles\stealthtank\99_mac\tank_shell.projectile"):
        damage_report = DamageReportingTypeEnum.scorpion.value
    elif tag_path.endswith(r"digsite\vehicles\warthog\00_e3\chaingun\h_assault_rifle_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.warthog_gunner.value
    elif tag_path.endswith(r"digsite\vehicles\warthog\00_e3\rocket\at_rocket.projectile"):
        damage_report = DamageReportingTypeEnum.warthog_gunner_rocket.value
    elif tag_path.endswith(r"digsite\vehicles\warthog\_dig\gauss\gauss.projectile"):
        damage_report = DamageReportingTypeEnum.warthog_gunner_gauss.value
    elif tag_path.endswith(r"digsite\vehicles\wraith\anti_air\anti_air_bolt.projectile"):
        damage_report = DamageReportingTypeEnum.wraith.value
    elif tag_path.endswith(r"digsite\weapons\assault_rifle\00_e3\h_assault_rifle_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.smg.value
    elif tag_path.endswith(r"digsite\weapons\assault_rifle\00_e3\h_assault_rifle_grenade.projectile"):
        damage_report = DamageReportingTypeEnum.frag_grenade.value
    elif tag_path.endswith(r"digsite\weapons\assault_rifle\99_mac\_dig\rifle_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.smg.value
    elif tag_path.endswith(r"digsite\weapons\assault_rifle\99_mac\rifle_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.smg.value
    elif tag_path.endswith(r"digsite\weapons\assault_rifle\99_mac\rifle_grenade.projectile"):
        damage_report = DamageReportingTypeEnum.frag_grenade.value
    elif tag_path.endswith(r"digsite\weapons\chaingun\99_mac\_dig\rifle_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.smg.value
    elif tag_path.endswith(r"digsite\weapons\chaingun\99_mac\rifle_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.smg.value
    elif tag_path.endswith(r"digsite\weapons\concussion_gun\99_mac\concussion.projectile"):
        damage_report = DamageReportingTypeEnum.shotgun.value
    elif tag_path.endswith(r"digsite\weapons\energy_sword\00_e3\slice.projectile"):
        damage_report = DamageReportingTypeEnum.energy_sword.value
    elif tag_path.endswith(r"digsite\weapons\energy_sword\00_e3\stab.projectile"):
        damage_report = DamageReportingTypeEnum.energy_sword.value
    elif tag_path.endswith(r"digsite\weapons\excavator\99_mac\rifle_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.shotgun.value
    elif tag_path.endswith(r"digsite\weapons\flak_cannon\99_mac\rifle_grenade.projectile"):
        damage_report = DamageReportingTypeEnum.frag_grenade.value
    elif tag_path.endswith(r"digsite\weapons\flamethrower\99_mac\flame.projectile"):
        damage_report = DamageReportingTypeEnum.disintegrator.value
    elif tag_path.endswith(r"digsite\weapons\fuel_rod_gun\99_mac\fuel_rod_rocket.projectile"):
        damage_report = DamageReportingTypeEnum.flak_cannon.value
    elif tag_path.endswith(r"digsite\weapons\machete\99_mac\slice.projectile"):
        damage_report = DamageReportingTypeEnum.energy_sword.value
    elif tag_path.endswith(r"digsite\weapons\machete\99_mac\stab.projectile"):
        damage_report = DamageReportingTypeEnum.energy_sword.value
    elif tag_path.endswith(r"digsite\weapons\microwave_gun\99_mac\beam.projectile"):
        damage_report = DamageReportingTypeEnum.disintegrator.value
    elif tag_path.endswith(r"digsite\weapons\missile_launcher\99_mac\aa_missile.projectile"):
        damage_report = DamageReportingTypeEnum.rocket_launcher.value
    elif tag_path.endswith(r"digsite\weapons\needler\00_e3\c_needle.projectile"):
        damage_report = DamageReportingTypeEnum.needler.value
    elif tag_path.endswith(r"digsite\weapons\particle_beam\00_e3\c_particle_beam_ray.projectile"):
        damage_report = DamageReportingTypeEnum.beam_rifle.value
    elif tag_path.endswith(r"digsite\weapons\particle_beam\99_mac\particle_beam.projectile"):
        damage_report = DamageReportingTypeEnum.beam_rifle.value
    elif tag_path.endswith(r"digsite\weapons\pistol\00_e3\h_pistol_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.magnum_pistol.value
    elif tag_path.endswith(r"digsite\weapons\pistol\99_mac\_dig\airstrike_round.projectile"):
        damage_report = DamageReportingTypeEnum.rocket_launcher.value
    elif tag_path.endswith(r"digsite\weapons\pistol\99_mac\_dig\pistol_tracer.projectile"):
        damage_report = DamageReportingTypeEnum.teh_guardians11.value
    elif tag_path.endswith(r"digsite\weapons\pistol\99_mac\pistol_laser.projectile"):
        damage_report = DamageReportingTypeEnum.teh_guardians11.value
    elif tag_path.endswith(r"digsite\weapons\pistol\99_mac\rifle_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.smg.value
    elif tag_path.endswith(r"digsite\weapons\plasma_pistol\99_mac\energy_ball.projectile"):
        damage_report = DamageReportingTypeEnum.plasma_pistol.value
    elif tag_path.endswith(r"digsite\weapons\plasma_rifle\00_e3\c_particle_beam_ray.projectile"):
        damage_report = DamageReportingTypeEnum.plasma_rifle.value
    elif tag_path.endswith(r"digsite\weapons\plasma_rifle\00_e3\charged_bolt.projectile"):
        damage_report = DamageReportingTypeEnum.plasma_rifle.value
    elif tag_path.endswith(r"digsite\weapons\plasma_rifle\01_beta\bolt.projectile"):
        damage_report = DamageReportingTypeEnum.plasma_rifle.value
    elif tag_path.endswith(r"digsite\weapons\plasma_rifle\01_beta\charged_bolt.projectile"):
        damage_report = DamageReportingTypeEnum.plasma_rifle.value
    elif tag_path.endswith(r"digsite\weapons\plasma_rifle\01_gs\c_particle_beam_ray.projectile"):
        damage_report = DamageReportingTypeEnum.plasma_rifle.value
    elif tag_path.endswith(r"digsite\weapons\plasma_rifle\99_mac\energy_ball.projectile"):
        damage_report = DamageReportingTypeEnum.plasma_rifle.value
    elif tag_path.endswith(r"digsite\weapons\rocket_launcher\99_mac\at_rocket.projectile"):
        damage_report = DamageReportingTypeEnum.rocket_launcher.value
    elif tag_path.endswith(r"digsite\weapons\shotgun\00_e3\h_shotgun_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.shotgun.value
    elif tag_path.endswith(r"digsite\weapons\shotgun\99_mac\rifle_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.shotgun.value
    elif tag_path.endswith(r"digsite\weapons\smg\99_mac\_dig\bullet.projectile"):
        damage_report = DamageReportingTypeEnum.smg.value
    elif tag_path.endswith(r"digsite\weapons\smg\99_mac\rifle_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.smg.value
    elif tag_path.endswith(r"digsite\weapons\sniper_rifle\00_e3\h_sniper_rifle_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.sniper_rifle.value
    elif tag_path.endswith(r"digsite\weapons\sniper_rifle\99_mac\rifle_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.sniper_rifle.value
    elif tag_path.endswith(r"digsite\weapons\speargun\99_mac\speargun_spear.projectile"):
        damage_report = DamageReportingTypeEnum.sniper_rifle.value
    elif tag_path.endswith(r"levels\a30\devices\beam_emitter\beam.projectile"):
        damage_report = DamageReportingTypeEnum.teh_guardians11.value
    elif tag_path.endswith(r"levels\c20\devices\index_platform\light.projectile"):
        damage_report = DamageReportingTypeEnum.teh_guardians11.value
    elif tag_path.endswith(r"vehicles\banshee\banshee_bolt.projectile"):
        damage_report = DamageReportingTypeEnum.banshee.value
    elif tag_path.endswith(r"vehicles\banshee\banshee_fuel_rod.projectile"):
        damage_report = DamageReportingTypeEnum.banshee.value
    elif tag_path.endswith(r"vehicles\banshee\mp_banshee_fuel_rod.projectile"):
        damage_report = DamageReportingTypeEnum.banshee.value
    elif tag_path.endswith(r"vehicles\c_gun_turret\c_gun_turret.projectile"):
        damage_report = DamageReportingTypeEnum.plasma_turret.value
    elif tag_path.endswith(r"vehicles\c_gun_turret\mp_gun_turret.projectile"):
        damage_report = DamageReportingTypeEnum.plasma_turret.value
    elif tag_path.endswith(r"vehicles\ghost\ghost_bolt.projectile"):
        damage_report = DamageReportingTypeEnum.ghost.value
    elif tag_path.endswith(r"vehicles\scorpion\bullet.projectile"):
        damage_report = DamageReportingTypeEnum.scorpion.value
    elif tag_path.endswith(r"vehicles\scorpion\tank_shell.projectile"):
        damage_report = DamageReportingTypeEnum.scorpion.value
    elif tag_path.endswith(r"vehicles\warthog\bullet.projectile"):
        damage_report = DamageReportingTypeEnum.warthog_gunner.value
    elif tag_path.endswith(r"vehicles\wraith\wraith_mortar.projectile"):
        damage_report = DamageReportingTypeEnum.wraith.value
    elif tag_path.endswith(r"weapons\assault_rifle\bullet.projectile"):
        damage_report = DamageReportingTypeEnum.smg.value
    elif tag_path.endswith(r"weapons\flamethrower\flame.projectile"):
        damage_report = DamageReportingTypeEnum.disintegrator.value
    elif tag_path.endswith(r"weapons\frag_grenade\frag_grenade.projectile"):
        damage_report = DamageReportingTypeEnum.frag_grenade.value
    elif tag_path.endswith(r"weapons\fuel_rod_gun\fuel_rod.projectile"):
        damage_report = DamageReportingTypeEnum.flak_cannon.value
    elif tag_path.endswith(r"weapons\needler\mp_needle.projectile"):
        damage_report = DamageReportingTypeEnum.needler.value
    elif tag_path.endswith(r"weapons\needler\needle.projectile"):
        damage_report = DamageReportingTypeEnum.needler.value
    elif tag_path.endswith(r"weapons\pistol\bullet.projectile"):
        damage_report = DamageReportingTypeEnum.magnum_pistol.value
    elif tag_path.endswith(r"weapons\plasma_cannon\plasma_cannon.projectile"):
        damage_report = DamageReportingTypeEnum.flak_cannon.value
    elif tag_path.endswith(r"weapons\plasma_grenade\plasma_grenade.projectile"):
        damage_report = DamageReportingTypeEnum.plasma_grenade.value
    elif tag_path.endswith(r"weapons\plasma_pistol\bolt.projectile"):
        damage_report = DamageReportingTypeEnum.plasma_pistol.value
    elif tag_path.endswith(r"weapons\plasma_rifle\bolt.projectile"):
        damage_report = DamageReportingTypeEnum.plasma_rifle.value
    elif tag_path.endswith(r"weapons\plasma_rifle\charged_bolt.projectile"):
        damage_report = DamageReportingTypeEnum.plasma_rifle.value
    elif tag_path.endswith(r"weapons\rocket_launcher\rocket.projectile"):
        damage_report = DamageReportingTypeEnum.rocket_launcher.value
    elif tag_path.endswith(r"weapons\shotgun\pellet.projectile"):
        damage_report = DamageReportingTypeEnum.shotgun.value
    elif tag_path.endswith(r"weapons\sniper_rifle\sniper_bullet.projectile"):
        damage_report = DamageReportingTypeEnum.sniper_rifle.value

    return combine_count, damage_report

def generate_material_responses(dump_dic):
    material_responses_block = []
    for response_idx, response_element in enumerate(dump_dic["Data"]["material response"]):
        material_response_dict = {
            "flags": response_element["flags"],
            "response": {
                "type": "ShortEnum",
                "value": convert_legacy_response(response_element["default response"]["value"]),
                "value name": ""
            },
            "DO NOT USE (OLD effect)": response_element["default effect"],
            "material name": get_material_name(response_idx),
            "response_1": {
                "type": "ShortEnum",
                "value": convert_legacy_response(response_element["potential response"]["value"]),
                "value name": ""
            },
            "flags_1": response_element["potential flags"],
            "chance fraction": response_element["potential skip fraction"],
            "between": {
                "Min": 0.0,
                "Max": 0.0
            },
            "and": response_element["potential and"],
            "DO NOT USE (OLD effect)_1": response_element["potential effect"],
            "scale effects by": {
                "type": "ShortEnum",
                "value": response_element["scale effects by"]["value"],
                "value name": ""
            },
            "angular noise": response_element["angular noise"],
            "velocity noise": response_element["velocity noise"],
            "DO NOT USE (OLD detonation effect)": response_element["detonation effect"],
            "initial friction": response_element["initial friction"],
            "maximum distance": response_element["maximum distance"],
            "parallel friction": response_element["parallel friction"],
            "perpendicular friction": response_element["perpendicular friction"],
        }

        material_responses_block.apppend(material_response_dict)
 
    return material_responses_block

def upgrade_projectile(h1_proj_asset, EngineTag):
    h1_proj_data = h1_proj_asset["Data"]

    function_keywords = [("Object", ObjectFunctionsEnum), ("Projectile", ProjectileFunctionsEnum)]

    combine_count, damage_report_value = generate_projectile_defaults(h1_proj_asset)

    h2_proj_asset = {
        "TagName": h1_proj_asset["TagName"],
        "Header": {
            "unk1": 0,
            "flags": 0,
            "tag type": 0,
            "name": "",
            "tag group": "proj",
            "checksum": 0,
            "data offset": 64,
            "data length": 0,
            "unk2": 0,
            "version": 5,
            "destination": 0,
            "plugin handle": -1,
            "engine tag": EngineTag.H2Latest.value
        },
        "Data": {
            "flags": convert_object_flags(h1_proj_data["flags"]),
            "bounding radius": h1_proj_data["bounding radius"],
            "bounding offset": h1_proj_data["bounding offset"],
            "acceleration scale": h1_proj_data["acceleration scale"],
            "model": {"group name": "hlmt", "path": ""},
            "ai properties": generate_ai_properties(h1_proj_asset),
            "hud text message index": h1_proj_data["hud text message index"],
            "attachments": generate_attachments(h1_proj_asset, function_keywords),
            "widgets": generate_widgets(h1_proj_asset),
            "change colors": generate_change_colors(h1_proj_asset, function_keywords),
            "flags_1": convert_projectile_flags(h1_proj_data["flags_1"]),
            "detonation timer starts": {
                "type": "ShortEnum",
                "value": h1_proj_data["detonation timer starts"]["value"],
                "value name": ""
            },
            "impact noise": {
                "type": "ShortEnum",
                "value": h1_proj_data["impact noise"]["value"],
                "value name": ""
            },
            "AI perception radius": h1_proj_data["ai perception radius"],
            "collision radius": h1_proj_data["collision radius"],
            "arming time": h1_proj_data["arming time"],
            "danger radius": h1_proj_data["danger radius"],
            "timer": h1_proj_data["timer"],
            "minimum velocity": h1_proj_data["minimum velocity"] * 30,
            "maximum range": h1_proj_data["maximum range"],
            "detonation noise": {
                "type": "ShortEnum",
                "value": h1_proj_data["detonation noise"]["value"],
                "value name": ""
            },
            "super det. projectile count": combine_count,
            "detonation started": h1_proj_data["detonation started"],
            "detonation effect (airborne)": {"group name": "effe", "path": ""},
            "detonation effect (ground)": {"group name": "effe", "path": ""},
            "detonation damage": {"group name": "jpt!", "path": ""},
            "attached detonation damage": h1_proj_data["attached detonation damage"],
            "super detonation": {"group name": "effe", "path": ""},
            "super detonation damage": {"group name": "jpt!", "path": ""},
            "detonation sound": {"group name": "snd!", "path": ""},
            "damage reporting type": {
                "type": "CharEnum",
                "value": damage_report_value,
                "value name": ""
            },
            "super attached detonation damage": {"group name": "jpt!", "path": ""},
            "material effect radius": 0.0,
            "flyby sound": h1_proj_data["flyby sound"],
            "impact effect": {"group name": "effe", "path": ""},
            "impact damage": h1_proj_data["impact damage"],
            "boarding detonation time": 0.0,
            "boarding detonation damage": {"group name": "jpt!", "path": ""},
            "boarding attached detonation damage": {"group name": "jpt!", "path": ""},
            "air gravity scale": h1_proj_data["air gravity scale"],
            "air damage range": h1_proj_data["air damage range"],
            "water gravity scale": h1_proj_data["water gravity scale"],
            "water damage range": h1_proj_data["water damage range"],
            "initial velocity": h1_proj_data["initial velocity"] * 30,
            "final velocity": h1_proj_data["final velocity"] * 30,
            "guided angular velocity (lower)": h1_proj_data["guided angular velocity"],
            "guided angular velocity (upper)": h1_proj_data["guided angular velocity"],
            "acceleration range": {
                "Min": 0.0,
                "Max": 0.0
            },
            "targeted leading fraction": 0.0,
            "material responses": generate_material_responses(h1_proj_asset)
        }
    }

    return h2_proj_asset
