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
from .format import (
    WeaponAsset, 
    ObjectFlags, 
    LightmapShadowModeEnum, 
    SweetenerSizeEnum, 
    ItemFlags, 
    WeaponFlags, 
    SecondaryTriggerModeEnum,
    MeleeDamageReportingTypeEnum,
    MovementPenalizedEnum,
    MultiplayerWeaponTypeEnum,
    WeaponTypeEnum,
    TrackingTypeEnum
    )

XML_OUTPUT = False

def initilize_weapon(WEAPON):
    WEAPON.ai_properties = []
    WEAPON.functions = []
    WEAPON.attachments = []
    WEAPON.widgets = []
    WEAPON.old_functions = []
    WEAPON.change_colors = []
    WEAPON.predicted_resources = []
    WEAPON.predicted_bitmaps = []
    WEAPON.first_person = []
    WEAPON.weapon_predicted_resources = []
    WEAPON.magazines = []
    WEAPON.new_triggers = []
    WEAPON.barrels = []

def read_weapon_body(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT):
    WEAPON.weapon_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    WEAPON.weapon_body = WEAPON.WeaponBody()
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    WEAPON.weapon_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    WEAPON.weapon_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    WEAPON.weapon_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    WEAPON.weapon_body.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    WEAPON.weapon_body.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(4) # Padding?
    WEAPON.weapon_body.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    WEAPON.weapon_body.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    WEAPON.weapon_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    WEAPON.weapon_body.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    WEAPON.weapon_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    WEAPON.weapon_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    WEAPON.weapon_body.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    WEAPON.weapon_body.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    WEAPON.weapon_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    WEAPON.weapon_body.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    WEAPON.weapon_body.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    WEAPON.weapon_body.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    WEAPON.weapon_body.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    WEAPON.weapon_body.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    WEAPON.weapon_body.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    WEAPON.weapon_body.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    WEAPON.weapon_body.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    WEAPON.weapon_body.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    WEAPON.weapon_body.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    WEAPON.weapon_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    WEAPON.weapon_body.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    WEAPON.weapon_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    WEAPON.weapon_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    WEAPON.weapon_body.equipment_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ItemFlags))
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.old_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "old message index"))
    WEAPON.weapon_body.sort_order = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "sort order"))
    WEAPON.weapon_body.multiplayer_on_ground_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "multiplayer on ground scale"))
    WEAPON.weapon_body.campaign_on_ground_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "campaign on ground scale"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.pickup_message_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.swap_message_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.pickup_or_dual_message_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.swap_or_dual_message_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.dual_only_message_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.picked_up_message_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.singluar_quantity_message_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.plural_quantity_message_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.switch_to_message_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.switch_to_from_ai_message_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    WEAPON.weapon_body.unused = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused"))
    WEAPON.weapon_body.collision_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision sound"))
    WEAPON.weapon_body.predicted_bitmaps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted bitmaps"))
    WEAPON.weapon_body.detonation_damage_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonation damage effect"))
    WEAPON.weapon_body.detonation_delay = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "detonation delay"))
    WEAPON.weapon_body.detonating_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonating effect"))
    WEAPON.weapon_body.detonation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonation effect"))

    WEAPON.weapon_body.weapon_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", WeaponFlags))
    input_stream.read(2) # Padding?

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.unknown_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    WEAPON.weapon_body.secondary_trigger_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "secondary trigger mode", SecondaryTriggerModeEnum))
    WEAPON.weapon_body.maximum_alternate_shots_loaded = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "maximum alternate shots loaded"))
    WEAPON.weapon_body.turn_on_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "turn on time"))
    WEAPON.weapon_body.ready_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ready time"))
    WEAPON.weapon_body.ready_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "ready effect"))
    WEAPON.weapon_body.ready_damage_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "ready damage effect"))
    WEAPON.weapon_body.heat_recovery_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat recovery threshold"))
    WEAPON.weapon_body.overheated_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "overheated threshold"))
    WEAPON.weapon_body.heat_detonation_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat detonation threshold"))
    WEAPON.weapon_body.heat_detonation_fraction = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat detonation fraction"))
    WEAPON.weapon_body.heat_loss_per_second = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat loss per second"))
    WEAPON.weapon_body.heat_illumination = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat illumination"))
    WEAPON.weapon_body.overheated_loss_per_second = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "overheated loss per second"))
    WEAPON.weapon_body.overheated = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "overheated"))
    WEAPON.weapon_body.overheated_damage_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "overheated damage effect"))
    WEAPON.weapon_body.detonation = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonation"))
    WEAPON.weapon_body.weapon_detonation_damage_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonation damage effect"))
    WEAPON.weapon_body.player_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "player melee damage"))
    WEAPON.weapon_body.player_melee_response = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "player melee response"))
    WEAPON.weapon_body.magnetism_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "magnetism angle"))
    WEAPON.weapon_body.magnetism_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "magnetism range"))
    WEAPON.weapon_body.throttle_magnitude = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "throttle magnitude"))
    WEAPON.weapon_body.throttle_minimum_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "throttle minimum distance"))
    WEAPON.weapon_body.throttle_maximum_adjustment_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "throttle maximum adjustment angle"))
    WEAPON.weapon_body.damage_pyramid_angles = TAG.read_degree_2d(input_stream, TAG, tag_format.XMLData(tag_node, "damage pyramid angles"))
    WEAPON.weapon_body.damage_pyramid_depth = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "damage pyramid depth"))
    WEAPON.weapon_body.first_hit_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "first hit melee damage"))
    WEAPON.weapon_body.first_hit_melee_response = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "first hit melee response"))
    WEAPON.weapon_body.second_hit_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "second hit melee damage"))
    WEAPON.weapon_body.second_hit_melee_response = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "second hit melee response"))
    WEAPON.weapon_body.third_hit_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "third hit melee damage"))
    WEAPON.weapon_body.third_hit_melee_response = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "third hit melee response"))
    WEAPON.weapon_body.lunge_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "lunge melee damage"))
    WEAPON.weapon_body.lunge_melee_response = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "lunge melee response"))
    WEAPON.weapon_body.melee_damage_reporting_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "melee damage reporting type", MeleeDamageReportingTypeEnum))
    WEAPON.weapon_body.magnification_levels = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "magnification levels"))
    WEAPON.weapon_body.magnification_range = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "magnification range"))
    WEAPON.weapon_body.autoaim_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "autoaim angle"))
    WEAPON.weapon_body.autoaim_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "autoaim range"))
    WEAPON.weapon_body.weapon_aim_assist_magnetism_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "magnetism angle"))
    WEAPON.weapon_body.weapon_aim_assist_magnetism_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "magnetism range"))
    WEAPON.weapon_body.deviation_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "deviation angle"))
    input_stream.read(16) # Padding?
    WEAPON.weapon_body.movement_penalized = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "movement penalized", MovementPenalizedEnum))
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.forward_movement_penalty = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "forward movement penalty"))
    WEAPON.weapon_body.sideways_movement_penalty = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "sideways movement penalty"))
    WEAPON.weapon_body.ai_scariness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai scariness"))
    WEAPON.weapon_body.weapon_power_on_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "weapon power on time"))
    WEAPON.weapon_body.weapon_power_off_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "weapon power off time"))
    WEAPON.weapon_body.weapon_power_on_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapon power on effect"))
    WEAPON.weapon_body.weapon_power_off_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapon power off effect"))
    WEAPON.weapon_body.age_heat_recovery_penalty = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "age heat recovery penalty"))
    WEAPON.weapon_body.age_rate_of_fire_penalty = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "age rate of fire penalty"))
    WEAPON.weapon_body.age_misfire_start = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "age misfire start"))
    WEAPON.weapon_body.age_misfire_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "age misfire chance"))
    WEAPON.weapon_body.pickup_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "pickup sound"))
    WEAPON.weapon_body.zoom_in_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "zoom in sound"))
    WEAPON.weapon_body.zoom_out_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "zoom out sound"))
    WEAPON.weapon_body.active_camo_ding = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "active camo ding"))
    WEAPON.weapon_body.active_camo_regrowth_rate = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "active camo regrowth rate"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.handle_node_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.weapon_class_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.weapon_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    WEAPON.weapon_body.multiplayer_weapon_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "multiplayer weapon type", MultiplayerWeaponTypeEnum))
    WEAPON.weapon_body.weapon_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "weapon type", WeaponTypeEnum))
    WEAPON.weapon_body.tracking_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "tracking type", TrackingTypeEnum))
    input_stream.read(18) # Padding?
    WEAPON.weapon_body.first_person_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "first person"))
    WEAPON.weapon_body.new_hud_interface = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "new hud interface"))
    WEAPON.weapon_body.weapon_predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    WEAPON.weapon_body.magazines_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "magazines"))
    WEAPON.weapon_body.new_triggers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "new triggers"))
    WEAPON.weapon_body.barrels_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "barrels"))
    input_stream.read(8) # Padding?
    WEAPON.weapon_body.max_movement_acceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max movement acceleration"))
    WEAPON.weapon_body.max_movement_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max movement velocity"))
    WEAPON.weapon_body.max_turning_acceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max turning acceleration"))
    WEAPON.weapon_body.max_turning_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max turning velocity"))
    WEAPON.weapon_body.deployed_vehicle = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "deployed vehicle"))
    WEAPON.weapon_body.age_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "age effect"))
    WEAPON.weapon_body.aged_weapon = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "aged weapon"))
    WEAPON.weapon_body.first_person_weapon_offset = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "first person weapon offset"))
    WEAPON.weapon_body.first_person_scope_size = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(tag_node, "first person scope size"))

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    WEAPON = WeaponAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    WEAPON.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_weapon(WEAPON)
    read_weapon_body(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT)

    if WEAPON.weapon_body.default_model_variant_length > 0:
        WEAPON.weapon_body.default_model_variant = TAG.read_variable_string_no_terminator(input_stream, WEAPON.weapon_body.default_model_variant_length, TAG, tag_format.XMLData(tag_node, "default model variant"))

    if WEAPON.weapon_body.model.name_length > 0:
        WEAPON.weapon_body.model.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.model.name_length, TAG)

    if WEAPON.weapon_body.crate_object.name_length > 0:
        WEAPON.weapon_body.crate_object.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.crate_object.name_length, TAG)

    if WEAPON.weapon_body.modifier_shader.name_length > 0:
        WEAPON.weapon_body.modifier_shader.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.modifier_shader.name_length, TAG)

    if WEAPON.weapon_body.creation_effect.name_length > 0:
        WEAPON.weapon_body.creation_effect.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.creation_effect.name_length, TAG)

    if WEAPON.weapon_body.material_effects.name_length > 0:
        WEAPON.weapon_body.material_effects.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.material_effects.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        crate_object_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "crate object")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        material_effects_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "material effects")
        WEAPON.weapon_body.model.append_xml_attributes(model_node)
        WEAPON.weapon_body.crate_object.append_xml_attributes(crate_object_node)
        WEAPON.weapon_body.modifier_shader.append_xml_attributes(modifier_shader_node)
        WEAPON.weapon_body.creation_effect.append_xml_attributes(creation_effect_node)
        WEAPON.weapon_body.material_effects.append_xml_attributes(material_effects_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, WEAPON.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return WEAPON
