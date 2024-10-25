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
from .format import (
    ActorVariantAsset,
    ActorVariantFlags,
    MetaGameTypeEnum,
    MetaGameClassEnum,
    MovementTypeEnum,
    SpecialFireModeEnum,
    SpecialFireSituationEnum,
    GrenadeTypeEnum,
    TrajectoryTypeEnum,
    GrenadeStimulusEnum
    )
from ....global_functions import tag_format

XML_OUTPUT = False

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    ACTORVARIANT = ActorVariantAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    ACTORVARIANT.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    ACTORVARIANT.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ActorVariantFlags))
    ACTORVARIANT.actor_definition = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "actor definition"))
    ACTORVARIANT.unit = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "unit"))
    ACTORVARIANT.major_variant = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "major variant"))
    ACTORVARIANT.metagame_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "metagame type", MetaGameTypeEnum))
    ACTORVARIANT.metagame_class = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "metagame class", MetaGameClassEnum))
    input_stream.read(20) # Padding
    ACTORVARIANT.movement_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "movement type", MovementTypeEnum))
    input_stream.read(2) # Padding
    ACTORVARIANT.initial_crouch_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "initial crouch chance"))
    ACTORVARIANT.crouch_time = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "crouch time"))
    ACTORVARIANT.run_time = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "run time"))
    ACTORVARIANT.weapon = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapon"))
    ACTORVARIANT.maximum_firing_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum firing distance"))
    ACTORVARIANT.rate_of_Fire = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "rate of fire"))
    ACTORVARIANT.projectile_error = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "projectile error"))
    ACTORVARIANT.first_burst_delay_time = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "first burst delay time"))
    ACTORVARIANT.new_target_firing_pattern_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "new-target firing pattern time"))
    ACTORVARIANT.surprise_delay_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "surprise delay time"))
    ACTORVARIANT.surprise_fire_wildly_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "surprise fire-wildly time"))
    ACTORVARIANT.death_fire_wildly_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "death fire-wildly chance"))
    ACTORVARIANT.death_fire_wildly_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "death fire-wildly time"))
    ACTORVARIANT.desired_combat_range = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "desired combat range"))
    ACTORVARIANT.custom_stand_gun_offset = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "custom stand gun offset"))
    ACTORVARIANT.custom_crouch_gun_offset = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "custom crouch gun offset"))
    ACTORVARIANT.target_tracking = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "target tracking"))
    ACTORVARIANT.target_leading = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "target leading"))
    ACTORVARIANT.weapon_damage_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "weapon damage modifier"))
    ACTORVARIANT.damage_per_second = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "damage per second"))
    ACTORVARIANT.burst_origin_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "burst origin radius"))
    ACTORVARIANT.burst_origin_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "burst origin angle"))
    ACTORVARIANT.burst_return_length = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "burst origin length"))
    ACTORVARIANT.burst_return_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "burst origin angle"))
    ACTORVARIANT.burst_duration = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "burst duration"))
    ACTORVARIANT.burst_seperation = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "burst seperation"))
    ACTORVARIANT.burst_angular_velocity = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "burst angular velocity"))
    input_stream.read(4) # Padding
    ACTORVARIANT.special_damage_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "special_damage_modifier"))
    ACTORVARIANT.speical_projectile_error = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "special projectile error"))
    ACTORVARIANT.new_target_burst_duration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "new-target burst duration"))
    ACTORVARIANT.new_target_burst_seperation = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "new-target burst seperation"))
    ACTORVARIANT.new_target_rate_of_fire = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "new-target rate of fire"))
    ACTORVARIANT.new_target_projectile_error = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "new-target projectile error"))
    input_stream.read(8) # Padding
    ACTORVARIANT.moving_burst_duration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "moving burst duration"))
    ACTORVARIANT.moving_burst_seperation = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "moving burst seperation"))
    ACTORVARIANT.moving_rate_of_fire = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "moving rate of fire"))
    ACTORVARIANT.moving_projectile_error = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "moving projectile error"))
    input_stream.read(8) # Padding
    ACTORVARIANT.berserk_burst_duration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "berserk burst duration"))
    ACTORVARIANT.berserk_burst_seperation = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "berserk burst seperation"))
    ACTORVARIANT.berserk_rate_of_fire = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "berserk rate of fire"))
    ACTORVARIANT.berserk_projectile_error = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "berserk projectile error"))
    input_stream.read(8) # Padding
    ACTORVARIANT.super_ballistic_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "super-ballistic range"))
    ACTORVARIANT.bombardment_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bombardment range"))
    ACTORVARIANT.modified_vision_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "modified vision range"))
    ACTORVARIANT.special_fire_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "special-fire mode", SpecialFireModeEnum))
    ACTORVARIANT.special_fire_situation = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "special-fire situation", SpecialFireSituationEnum))
    ACTORVARIANT.special_fire_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "special-fire chance"))
    ACTORVARIANT.special_fire_delay = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "special-fire delay"))
    ACTORVARIANT.melee_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "melee range"))
    ACTORVARIANT.melee_abort_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "melee abort range"))
    ACTORVARIANT.berserk_firing_ranges = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "berserk firing ranges"))
    ACTORVARIANT.berserk_melee_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "berserk melee range"))
    ACTORVARIANT.berserk_melee_abort_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "berserk melee abort range"))
    input_stream.read(8) # Padding
    ACTORVARIANT.grenade_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade type", GrenadeTypeEnum))
    ACTORVARIANT.trajectory_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "trajectory type", TrajectoryTypeEnum))
    ACTORVARIANT.grenade_stimulus = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade stimulus", GrenadeStimulusEnum))
    ACTORVARIANT.minimum_enemy_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "minimum enemy count"))
    ACTORVARIANT.enemy_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "enemy radius"))
    input_stream.read(4) # Padding
    ACTORVARIANT.grenade_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "grenade velocity"))
    ACTORVARIANT.grenade_ranges = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "grenade ranges"))
    ACTORVARIANT.collateral_damage_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "collateral damage radius"))
    ACTORVARIANT.grenade_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "grenade chance"))
    ACTORVARIANT.grenade_check_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "grenade check time"))
    ACTORVARIANT.encounter_grenade_timeout = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "encounter grenade timeout"))
    input_stream.read(20) # Padding
    ACTORVARIANT.equipment = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "equipment"))
    ACTORVARIANT.grenade_count = TAG.read_min_max_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade count"))
    ACTORVARIANT.dont_drop_grenades_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dont drop grenades chance"))
    ACTORVARIANT.drop_weapon_loaded = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "drop weapon loaded"))
    ACTORVARIANT.drop_weapon_ammo = TAG.read_min_max_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "drop weapon ammo"))
    input_stream.read(28) # Padding
    ACTORVARIANT.body_vitality = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "body vitality"))
    ACTORVARIANT.shield_vitality = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "shield vitality"))
    ACTORVARIANT.shield_sapping_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "shield sapping radius"))
    ACTORVARIANT.forced_shader_permutation = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "forced shader permutation"))
    input_stream.read(30) # Padding
    ACTORVARIANT.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))

    actor_definition_tag_ref = ACTORVARIANT.actor_definition
    unit_tag_ref = ACTORVARIANT.unit
    major_variant_tag_ref = ACTORVARIANT.major_variant
    weapon_tag_ref = ACTORVARIANT.weapon
    equipment_tag_ref = ACTORVARIANT.equipment
    actor_definition_name_length = actor_definition_tag_ref.name_length
    unit_name_length = unit_tag_ref.name_length
    major_variant_name_length = major_variant_tag_ref.name_length
    weapon_name_length = weapon_tag_ref.name_length
    equipment_name_length = equipment_tag_ref.name_length
    if actor_definition_name_length > 0:
        actor_definition_tag_ref.name = TAG.read_variable_string(input_stream, actor_definition_name_length, TAG)

    if unit_name_length > 0:
        unit_tag_ref.name = TAG.read_variable_string(input_stream, unit_name_length, TAG)

    if major_variant_name_length > 0:
        major_variant_tag_ref.name = TAG.read_variable_string(input_stream, major_variant_name_length, TAG)

    if weapon_name_length > 0:
        weapon_tag_ref.name = TAG.read_variable_string(input_stream, weapon_name_length, TAG)

    if equipment_name_length > 0:
        equipment_tag_ref.name = TAG.read_variable_string(input_stream, equipment_name_length, TAG)

    if XML_OUTPUT:
        actor_definition_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "actor definition")
        unit_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "unit")
        major_variant_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "major variant")
        weapon_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "weapon")
        equipment_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "equipment")
        actor_definition_tag_ref.append_xml_attributes(actor_definition_node)
        unit_tag_ref.append_xml_attributes(unit_node)
        major_variant_tag_ref.append_xml_attributes(major_variant_node)
        weapon_tag_ref.append_xml_attributes(weapon_node)
        equipment_tag_ref.append_xml_attributes(equipment_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, ACTORVARIANT.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return ACTORVARIANT
