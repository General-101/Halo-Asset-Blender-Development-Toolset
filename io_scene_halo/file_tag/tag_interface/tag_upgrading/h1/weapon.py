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

from mathutils import Vector
from ....global_functions import tag_format
from ....file_tag.h1.file_object.upgrade_object import generate_attachments, generate_widgets, generate_change_colors
from ....file_tag.h1.file_object.format import ObjectFunctionEnum, upgrade_h1_object_flags
from .format import (
    WeaponFlags,
    SecondaryTriggerModeEnum,
    WeaponFunctionEnum,
    MovementPenalizedEnum,
    WeaponTypeEnum,
    MagazineFlags,
    TriggerFlags,
    PredictionEnum,
    FiringNoiseEnum,
    OverchargedActionEnum,
    DistributionFunctionEnum,
    get_magazine,
    upgrade_h1_barrel_flags,
    generate_fire_recovery
    )
from ....file_tag.h2.file_weapon.format import (
    WeaponAsset,
    WeaponFlags,
    SecondaryTriggerModeEnum,
    MeleeDamageReportingTypeEnum,
    MovementPenalizedEnum,
    MultiplayerWeaponTypeEnum,
    WeaponTypeEnum,
    TrackingTypeEnum,
    BehaviorEnum,
    TriggerPredictionEnum,
    BarrelFlags,
    BarrelPredictionEnum
    )

def generate_first_person(H1_ASSET, TAG, WEAPON):
    first_person = WEAPON.FirstPerson()
    first_person.first_person_model = H1_ASSET.first_person_model
    first_person.first_person_animations = TAG.TagRef("jmad", H1_ASSET.first_person_animations.name, H1_ASSET.first_person_animations.name_length)
    if len(first_person.first_person_model.name) > 0 or len(first_person.first_person_animations.name) > 0:
        WEAPON.first_person.append(first_person)

    first_person_count = len(WEAPON.first_person)
    WEAPON.first_person_header = TAG.TagBlockHeader("tbfd", 0, first_person_count, 32)

    return TAG.TagBlock(first_person_count)

def generate_magazines(H1_ASSET, TAG, WEAPON):
    for magazine_stat_element in H1_ASSET.magazines:
        magazine_stat = WEAPON.MagazineStats()
        magazine_stat.flags = magazine_stat_element.flags
        magazine_stat.rounds_recharged = magazine_stat_element.rounds_recharged
        magazine_stat.rounds_total_initial = magazine_stat_element.rounds_total_initial
        magazine_stat.rounds_total_maximum = magazine_stat_element.rounds_total_maximum
        magazine_stat.rounds_loaded_maximum = magazine_stat_element.rounds_loaded_maximum
        magazine_stat.reload_time = magazine_stat_element.reload_time
        magazine_stat.rounds_reloaded = magazine_stat_element.rounds_reloaded
        magazine_stat.chamber_time = magazine_stat_element.chamber_time
        magazine_stat.reloading_effect = magazine_stat_element.reloading_effect
        magazine_stat.reloading_damage_effect = TAG.TagRef()
        magazine_stat.chambering_effect = magazine_stat_element.chambering_effect
        magazine_stat.chambering_damage_effect = TAG.TagRef()

        magazine_stat.magazines = []
        for magazine_element in magazine_stat_element.magazines:
            magazine = WEAPON.Magazine()
            magazine.rounds = magazine_element.rounds
            magazine.equipment = magazine_element.equipment

            magazine_stat.magazines.append(magazine)

        magazine_count = len(magazine_stat.magazines)
        magazine_stat.magazines_header = TAG.TagBlockHeader("tbfd", 1, magazine_count, 20)
        magazine_stat.magazines_tag_block = TAG.TagBlock(magazine_count)

        WEAPON.magazines.append(magazine_stat)

    magazine_stat_count = len(WEAPON.magazines)
    WEAPON.magazines_header = TAG.TagBlockHeader("tbfd", 1, magazine_stat_count, 128)

    return TAG.TagBlock(magazine_stat_count)

def generate_triggers_and_barrels(H1_ASSET, TAG, WEAPON):
    if len(H1_ASSET.triggers) > 0:
        new_trigger = WEAPON.NewTrigger()
        for trigger_idx, trigger_element in enumerate(H1_ASSET.triggers):
            if trigger_idx == 0:
                new_trigger.flags = 0
                new_trigger.input_type
                if not TriggerFlags.does_not_repeat_automatically in TriggerFlags(trigger_element.flags):
                    new_trigger.behavior = BehaviorEnum.spew.value
                    new_trigger.prediction = TriggerPredictionEnum.spew.value

                else:
                    if trigger_element.charging_time > 0.0:
                        new_trigger.behavior = BehaviorEnum.charge.value
                        new_trigger.prediction = TriggerPredictionEnum.charge.value

                    else:
                        if H1_ASSET.magnification_levels > 0:
                            if "rocket" in trigger_element.projectile.name:
                                new_trigger.behavior = BehaviorEnum.latch_rocketlauncher.value

                            else:
                                new_trigger.behavior = BehaviorEnum.latch_zoom.value

                        else:
                            new_trigger.behavior = BehaviorEnum.latch.value

                new_trigger.primary_barrel = trigger_idx
                new_trigger.autofire_time = 0.0
                new_trigger.autofire_throw = 0.0
                new_trigger.secondary_action = 0
                new_trigger.primary_action = 0
                new_trigger.charging_damage_effect = TAG.TagRef()

                new_trigger.charging_time = trigger_element.charging_time
                new_trigger.charged_time = trigger_element.charged_time
                new_trigger.overcharged_action = trigger_element.overcharged_action
                new_trigger.charged_illumination = trigger_element.charged_illumination
                new_trigger.spew_time = trigger_element.spew_time
                new_trigger.charging_effect = trigger_element.charging_effect

            else:
                new_trigger.secondary_barrel = trigger_idx

            barrel = WEAPON.Barrel()
            barrel.flags = upgrade_h1_barrel_flags(trigger_element.flags)
            barrel.rounds_per_second =  (trigger_element.rounds_per_second[0], trigger_element.rounds_per_second[1])
            barrel.firing_acceleration_time = trigger_element.firing_acceleration_time
            barrel.firing_deceleration_time = trigger_element.firing_deceleration_time
            barrel.barrel_spin_scale = 0.0
            barrel.blurred_rate_of_fire = trigger_element.blurred_rate_of_fire
            barrel.shots_per_fire = (1, 1)
            barrel.fire_recovery_time = generate_fire_recovery(trigger_element)
            barrel.soft_recovery_fraction = 0.0
            barrel.magazine = get_magazine(WEAPON, trigger_element.magazine)
            barrel.prediction_type = trigger_element.prediction_type
            barrel.rounds_per_shot = trigger_element.rounds_per_shot
            barrel.minimum_rounds_loaded = trigger_element.minimum_rounds_loaded
            barrel.rounds_between_tracers = trigger_element.rounds_between_tracers
            barrel.optional_barrel_marker_name = ""
            barrel.optional_barrel_marker_name_length = len(barrel.optional_barrel_marker_name)
            barrel.firing_noise = trigger_element.firing_noise
            barrel.error_acceleration_time = trigger_element.error_acceleration_time
            barrel.error_deceleration_time = trigger_element.error_deceleration_time
            barrel.damage_error = (0.0, 0.0)
            barrel.dual_acceleration_time = 0.0
            barrel.dual_deceleration_time = 0.0
            barrel.dual_minimum_error = 0.0
            barrel.dual_error_angle = (0.0, 0.0)
            barrel.dual_wield_damage_scale = 0.0
            barrel.distribution_function = trigger_element.distribution_function
            barrel.projectiles_per_shot = trigger_element.projectiles_per_shot
            barrel.distribution_angle = trigger_element.distribution_angle
            barrel.projectile_minimum_error = trigger_element.minimum_error
            barrel.projectile_error_angle = (trigger_element.error_angle[0], trigger_element.error_angle[1])
            barrel.first_person_offset = trigger_element.first_person_offset
            barrel.damage_effect_reporting_type = 0
            barrel.projectile = trigger_element.projectile
            barrel.damage_effect = TAG.TagRef()
            barrel.ejection_port_recovery_time = trigger_element.ejection_port_recovery_time
            barrel.illumination_recovery_time = trigger_element.illumination_recovery_time
            barrel.heat_generated_per_round = trigger_element.heat_generated_per_round
            barrel.age_generated_per_round = trigger_element.age_generated_per_round
            barrel.overload_time = trigger_element.overload_time
            barrel.angle_change_per_shot = (0.0, 0.0)
            barrel.recoil_acceleration_time = 0.0
            barrel.recoil_deceleration_time = 0.0
            barrel.angle_change_function = 0

            barrel.firing_effects = []
            for firing_effect_element in trigger_element.firing_effects:
                firing_effect = WEAPON.FiringEffect()
                firing_effect.shot_count_lower_bound = firing_effect_element.shot_count_lower_bound
                firing_effect.shot_count_upper_bound = firing_effect_element.shot_count_upper_bound
                firing_effect.firing_effect = firing_effect_element.firing_effect
                firing_effect.misfire_effect = firing_effect_element.misfire_effect
                firing_effect.empty_effect = firing_effect_element.empty_effect
                firing_effect.firing_damage = firing_effect_element.firing_damage
                firing_effect.misfire_damage = firing_effect_element.misfire_damage
                firing_effect.empty_damage = firing_effect_element.empty_damage

                barrel.firing_effects.append(firing_effect)

            firing_effect_count = len(barrel.firing_effects)
            barrel.firing_effects_header = TAG.TagBlockHeader("tbfd", 1, firing_effect_count, 100)
            barrel.firing_effects_tag_block = TAG.TagBlock(firing_effect_count)

            WEAPON.barrels.append(barrel)

        WEAPON.new_triggers.append(new_trigger)

    new_trigger_count = len(WEAPON.new_triggers)
    WEAPON.new_triggers_header = TAG.TagBlockHeader("tbfd", 0, new_trigger_count, 80)
    WEAPON.new_triggers_tag_block = TAG.TagBlock(new_trigger_count)

    barrel_count = len(WEAPON.barrels)
    WEAPON.barrels_header = TAG.TagBlockHeader("tbfd", 2, barrel_count, 256)
    WEAPON.barrels_tag_block = TAG.TagBlock(barrel_count)

def get_weapon_defaults(weapon_name):
    weapon_class = ""
    ai_scariness = 0
    multiplayer_weapon_type = MultiplayerWeaponTypeEnum.none.value
    tracking_type = TrackingTypeEnum.no_tracking.value
    if "assault_rifle" == weapon_name:
        weapon_class = "rifle"
        ai_scariness = 4
    elif "shotgun" == weapon_name:
        weapon_class = "rifle"
        ai_scariness = 4
    elif "sniper_rifle" == weapon_name:
        weapon_class = "rifle"
        ai_scariness = 8
    elif "pistol" == weapon_name:
        weapon_class = "pistol"
        ai_scariness = 4
    elif "needler" in weapon_name:
        weapon_class = "pistol"
        ai_scariness = 6
    elif "plasma_pistol" == weapon_name:
        weapon_class = "pistol"
        tracking_type = TrackingTypeEnum.plasma_tracking.value
        ai_scariness = 4
    elif "rocket_launcher" == weapon_name:
        weapon_class = "missile"
        tracking_type = TrackingTypeEnum.human_tracking.value
        ai_scariness = 12
    elif "plasma_cannon" == weapon_name:
        weapon_class = "missile"
        ai_scariness = 12
    elif "fuel_rod" in weapon_name:
        weapon_class = "missile"
        ai_scariness = 12
    elif "flamethrower" == weapon_name:
        weapon_class = "support"
        ai_scariness = 4
    elif "energy_sword" == weapon_name:
        weapon_class = "sword"
        ai_scariness = 16
    elif "ball" == weapon_name:
        weapon_class = "ball"
        multiplayer_weapon_type = MultiplayerWeaponTypeEnum.oddball_ball.value
    elif "flag" == weapon_name:
        weapon_class = "flag"
        multiplayer_weapon_type = MultiplayerWeaponTypeEnum.ctf_flag.value
    else:
        weapon_class = "fixed"

    return weapon_class, ai_scariness, multiplayer_weapon_type, tracking_type

def get_melee_aim_assist_defaults(weapon_name):
    magnetism_angle = 0.0
    magnetism_range = 0.0
    throttle_magnitude = 0.0
    throttle_minimum_distance = 0.0
    throttle_maximum_adjustment_angle = 0.0
    damage_pyramid_angles = (0.0, 0.0)
    damage_pyramid_depth = 0.0
    if "assault_rifle" == weapon_name:
        throttle_magnitude = 0.5
        throttle_minimum_distance = 0.1
        damage_pyramid_angles = (20.0, 10.0)
        damage_pyramid_depth = 0.6
    elif "shotgun" == weapon_name:
        magnetism_angle = 40.0
        magnetism_range = 1.0
        throttle_magnitude = 0.9
        throttle_minimum_distance = 0.1
        throttle_maximum_adjustment_angle = 20
        damage_pyramid_angles = (20.0, 10.0)
        damage_pyramid_depth = 0.6
    elif "sniper_rifle" == weapon_name:
        damage_pyramid_angles = (20.0, 10.0)
        damage_pyramid_depth = 0.6
    elif "pistol" == weapon_name:
        damage_pyramid_angles = (20.0, 10.0)
        damage_pyramid_depth = 0.6
    elif "needler" in weapon_name:
        damage_pyramid_angles = (20.0, 10.0)
        damage_pyramid_depth = 0.6
    elif "plasma_pistol" == weapon_name:
        damage_pyramid_angles = (20.0, 10.0)
        damage_pyramid_depth = 0.6
    elif "rocket_launcher" == weapon_name:
        damage_pyramid_angles = (20.0, 10.0)
        damage_pyramid_depth = 0.6
    elif "plasma_cannon" == weapon_name:
        magnetism_angle = 40.0
        magnetism_range = 1.0
        throttle_magnitude = 0.9
        throttle_minimum_distance = 0.1
        throttle_maximum_adjustment_angle = 20.0
        damage_pyramid_angles = (20.0, 10.0)
        damage_pyramid_depth = 0.6
    elif "fuel_rod" in weapon_name:
        magnetism_angle = 40.0
        magnetism_range = 1.0
        throttle_magnitude = 0.9
        throttle_minimum_distance = 0.1
        throttle_maximum_adjustment_angle = 20.0
        damage_pyramid_angles = (20.0, 10.0)
        damage_pyramid_depth = 0.6
    elif "flamethrower" == weapon_name:
        magnetism_angle = 40.0
        magnetism_range = 1.0
        throttle_magnitude = 0.9
        throttle_minimum_distance = 0.1
        throttle_maximum_adjustment_angle = 20.0
        damage_pyramid_angles = (20.0, 10.0)
        damage_pyramid_depth = 0.6
    elif "energy_sword" == weapon_name:
        damage_pyramid_angles = (25.0, 15.0)
        damage_pyramid_depth = 0.9
    elif "ball" == weapon_name:
        magnetism_angle = 30.0
        throttle_magnitude = 5.0
        throttle_minimum_distance = 0.2
        throttle_maximum_adjustment_angle = 45
        damage_pyramid_angles = (20.0, 10.0)
        damage_pyramid_depth = 0.6
    elif "flag" == weapon_name:
        magnetism_angle = 30.0
        throttle_magnitude = 5.0
        throttle_minimum_distance = 0.2
        throttle_maximum_adjustment_angle = 45
        damage_pyramid_angles = (20.0, 10.0)
        damage_pyramid_depth = 0.6

    return magnetism_angle, magnetism_range, throttle_magnitude, throttle_minimum_distance, throttle_maximum_adjustment_angle, damage_pyramid_angles, damage_pyramid_depth

def get_weapon_messages(weapon_name):
    pickup_message = ""
    swap_message = ""
    pickup_or_dual_msg = ""
    swap_or_dual_msg = ""
    dual_only_msg = ""
    picked_up_msg = ""
    singluar_quantity_msg = ""
    plural_quantity_msg = ""
    switch_to_msg = ""
    switch_to_from_ai_msg = ""
    if "assault_rifle" == weapon_name:
        pickup_message = "smg_pickup"
        swap_message = "smg_swap"
        pickup_or_dual_msg = "smg_pickup_or_dual"
        swap_or_dual_msg = "smg_swap_or_dual"
        dual_only_msg = "smg_dual"
        picked_up_msg = "smg_picked_up"
        singluar_quantity_msg = "smg_ammo_singular"
        plural_quantity_msg = "smg_ammo_plural"
        switch_to_msg = "smg_switch_to"
        switch_to_from_ai_msg = "smg_swap_ai"
    elif "shotgun" == weapon_name:
        pickup_message = "sg_pickup"
        swap_message = "sg_swap"
        picked_up_msg = "sg_picked_up"
        singluar_quantity_msg = "sg_ammo_singular"
        plural_quantity_msg = "sg_ammo_plural"
        switch_to_msg = "sg_switch_to"
        switch_to_from_ai_msg = "sg_swap_ai"
    elif "sniper_rifle" == weapon_name:
        pickup_message = "sn_pickup"
        swap_message = "sn_swap"
        pickup_or_dual_msg = "sn_pickup_or_dual"
        swap_or_dual_msg = "sn_swap_or_dual"
        dual_only_msg = "sn_dual"
        picked_up_msg = "sn_picked_up"
        singluar_quantity_msg = "sn_ammo_singular"
        plural_quantity_msg = "sn_ammo_plural"
        switch_to_msg = "sn_switch_to"
        switch_to_from_ai_msg = "sn_swap_ai"
    elif "pistol" == weapon_name:
        pickup_message = "mp_pickup"
        swap_message = "mp_swap"
        pickup_or_dual_msg = "mp_pickup_or_dual"
        swap_or_dual_msg = "mp_swap_or_dual"
        dual_only_msg = "mp_dual"
        picked_up_msg = "mp_picked_up"
        singluar_quantity_msg = "mp_ammo_singular"
        plural_quantity_msg = "mp_ammo_plural"
        switch_to_msg = "mp_switch_to"
        switch_to_from_ai_msg = "mp_swap_ai"
    elif "needler" in weapon_name:
        pickup_message = "nd_pickup"
        swap_message = "nd_swap"
        pickup_or_dual_msg = "nd_pickup_or_dual"
        swap_or_dual_msg = "nd_swap_or_dual"
        dual_only_msg = "nd_dual"
        picked_up_msg = "nd_picked_up"
        singluar_quantity_msg = "nd_ammo_singular"
        plural_quantity_msg = "nd_ammo_plural"
        switch_to_msg = "nd_switch_to"
        switch_to_from_ai_msg = "nd_swap_ai"
    elif "plasma_pistol" == weapon_name:
        pickup_message = "pp_pickup"
        swap_message = "pp_swap"
        pickup_or_dual_msg = "pp_pickup_or_dual"
        swap_or_dual_msg = "pp_swap_or_dual"
        dual_only_msg = "pp_dual"
        picked_up_msg = "pp_picked_up"
        singluar_quantity_msg = "pp_ammo_singular"
        plural_quantity_msg = "pp_ammo_plural"
        switch_to_msg = "pp_switch_to"
        switch_to_from_ai_msg = "pp_swap_ai"
    elif "rocket_launcher" == weapon_name:
        pickup_message = "rl_pickup"
        swap_message = "rl_swap"
        picked_up_msg = "rl_picked_up"
        singluar_quantity_msg = "rl_ammo_singular"
        plural_quantity_msg = "rl_ammo_plural"
        switch_to_msg = "rl_switch_to"
        switch_to_from_ai_msg = "rl_swap_ai"
    elif "plasma_cannon" == weapon_name:
        pickup_message = "fc_pickup"
        swap_message = "fc_swap"
        picked_up_msg = "fc_picked_up"
        singluar_quantity_msg = "fc_ammo_singular"
        plural_quantity_msg = "fc_ammo_plural"
        switch_to_msg = "fc_switch_to"
        switch_to_from_ai_msg = "fc_swap_ai"
    elif "fuel_rod" in weapon_name:
        pickup_message = "fc_pickup"
        swap_message = "fc_swap"
        picked_up_msg = "fc_picked_up"
        singluar_quantity_msg = "fc_ammo_singular"
        plural_quantity_msg = "fc_ammo_plural"
        switch_to_msg = "fc_switch_to"
        switch_to_from_ai_msg = "fc_swap_ai"
    elif "flamethrower" == weapon_name:
        pickup_message = "sen_b_pickup"
        swap_message = "sen_b_swap"
        picked_up_msg = "sen_b_picked_up"
        singluar_quantity_msg = "sen_b_ammo_singular"
        plural_quantity_msg = "sen_b_ammo_plural"
        switch_to_msg = "sen_b_switch_to"
        switch_to_from_ai_msg = "sen_b_swap_ai"
    elif "energy_sword" == weapon_name:
        pickup_message = "ps_pickup"
        swap_message = "ps_swap"
        picked_up_msg = "ps_picked_up"
        switch_to_msg = "ps_switch_to"
        switch_to_from_ai_msg = "ps_swap_ai"
    elif "ball" == weapon_name:
        pickup_message = "ob_pickup"
    elif "flag" == weapon_name:
        pickup_message = "fl_pickup"

    return pickup_message, swap_message, pickup_or_dual_msg, swap_or_dual_msg, dual_only_msg, picked_up_msg, singluar_quantity_msg, plural_quantity_msg, switch_to_msg, switch_to_from_ai_msg

def upgrade_weapon(H1_ASSET, patch_txt_path, report):
    TAG = tag_format.TagAsset()
    WEAPON = WeaponAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    WEAPON.header = TAG.Header()
    WEAPON.header.unk1 = 0
    WEAPON.header.flags = 0
    WEAPON.header.type = 0
    WEAPON.header.name = ""
    WEAPON.header.tag_group = "weap"
    WEAPON.header.checksum = 0
    WEAPON.header.data_offset = 64
    WEAPON.header.data_length = 0
    WEAPON.header.unk2 = 0
    WEAPON.header.version = 2
    WEAPON.header.destination = 0
    WEAPON.header.plugin_handle = -1
    WEAPON.header.engine_tag = "BLM!"

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

    weapon_path = H1_ASSET.header.local_path.lower().replace(" ", "_")
    weapon_name = os.path.basename(weapon_path)
    function_keywords = [("Object", ObjectFunctionEnum), ("Weapon", WeaponFunctionEnum)]

    weapon_class, ai_scariness, multiplayer_weapon_type, tracking_type = get_weapon_defaults(weapon_name)
    pickup_message, swap_message, pickup_or_dual_msg, swap_or_dual_msg, dual_only_msg, picked_up_msg, singluar_quantity_msg, plural_quantity_msg, switch_to_msg, switch_to_from_ai_msg = get_weapon_messages(weapon_name)
    magnetism_angle, magnetism_range, throttle_magnitude, throttle_minimum_distance, throttle_maximum_adjustment_angle, damage_pyramid_angles, damage_pyramid_depth = get_melee_aim_assist_defaults(weapon_name)

    WEAPON.body_header = TAG.TagBlockHeader("tbfd", 3, 1, 1128)
    WEAPON.object_flags = upgrade_h1_object_flags(H1_ASSET.object_flags)
    WEAPON.bounding_radius = H1_ASSET.bounding_radius
    WEAPON.bounding_offset = H1_ASSET.bounding_offset
    WEAPON.acceleration_scale = H1_ASSET.acceleration_scale
    WEAPON.lightmap_shadow_mode = 0
    WEAPON.sweetner_size = 0
    WEAPON.dynamic_light_sphere_radius = 0.0
    WEAPON.dynamic_light_sphere_offset = Vector()
    WEAPON.default_model_variant = ""
    WEAPON.default_model_variant_length = len(WEAPON.default_model_variant)
    WEAPON.model = TAG.TagRef("hlmt", weapon_path, len(weapon_path))
    WEAPON.crate_object = TAG.TagRef()
    WEAPON.modifier_shader = TAG.TagRef()
    WEAPON.creation_effect = TAG.TagRef()
    WEAPON.material_effects = TAG.TagRef()
    WEAPON.ai_properties_tag_block = TAG.TagBlock()
    WEAPON.functions_tag_block = TAG.TagBlock()
    WEAPON.apply_collision_damage_scale = 0.0
    WEAPON.min_game_acc = 0.0
    WEAPON.max_game_acc = 0.0
    WEAPON.min_game_scale = 0.0
    WEAPON.max_game_scale = 0.0
    WEAPON.min_abs_acc = 0.0
    WEAPON.max_abs_acc = 0.0
    WEAPON.min_abs_scale = 0.0
    WEAPON.max_abs_scale = 0.0
    WEAPON.hud_text_message_index = H1_ASSET.hud_text_message_index
    WEAPON.attachments_tag_block = generate_attachments(H1_ASSET, TAG, WEAPON, function_keywords)
    WEAPON.widgets_tag_block = generate_widgets(H1_ASSET, TAG, WEAPON)
    WEAPON.old_functions_tag_block = TAG.TagBlock()
    WEAPON.change_colors_tag_block = generate_change_colors(H1_ASSET, TAG, WEAPON, function_keywords)
    WEAPON.predicted_resources_tag_block = TAG.TagBlock()
    WEAPON.item_flags = H1_ASSET.item_flags
    WEAPON.old_message_index = H1_ASSET.message_index
    WEAPON.sort_order = H1_ASSET.sort_order
    WEAPON.multiplayer_on_ground_scale = H1_ASSET.scale
    WEAPON.campaign_on_ground_scale = H1_ASSET.scale
    WEAPON.pickup_message = pickup_message
    WEAPON.swap_message = swap_message
    WEAPON.pickup_or_dual_msg = pickup_or_dual_msg
    WEAPON.swap_or_dual_msg = swap_or_dual_msg
    WEAPON.dual_only_msg = dual_only_msg
    WEAPON.picked_up_msg = picked_up_msg
    WEAPON.singluar_quantity_msg = singluar_quantity_msg
    WEAPON.plural_quantity_msg = plural_quantity_msg
    WEAPON.switch_to_msg = switch_to_msg
    WEAPON.switch_to_from_ai_msg = switch_to_from_ai_msg
    WEAPON.pickup_message_length = len(WEAPON.pickup_message)
    WEAPON.swap_message_length = len(WEAPON.swap_message)
    WEAPON.pickup_or_dual_msg_length = len(WEAPON.pickup_or_dual_msg)
    WEAPON.swap_or_dual_msg_length = len(WEAPON.swap_or_dual_msg)
    WEAPON.dual_only_msg_length = len(WEAPON.dual_only_msg)
    WEAPON.picked_up_msg_length = len(WEAPON.picked_up_msg)
    WEAPON.singluar_quantity_msg_length = len(WEAPON.singluar_quantity_msg)
    WEAPON.plural_quantity_msg_length = len(WEAPON.plural_quantity_msg)
    WEAPON.switch_to_msg_length = len(WEAPON.switch_to_msg)
    WEAPON.switch_to_from_ai_msg_length = len(WEAPON.switch_to_from_ai_msg)
    WEAPON.unused = H1_ASSET.material_effects
    WEAPON.collision_sound = H1_ASSET.collision_sound
    WEAPON.predicted_bitmaps_tag_block = TAG.TagBlock()
    WEAPON.detonation_damage_effect = TAG.TagRef()
    WEAPON.detonation_delay = (H1_ASSET.detonation_delay[0], H1_ASSET.detonation_delay[1])
    WEAPON.detonating_effect = H1_ASSET.detonating_effect
    WEAPON.detonation_effect = H1_ASSET.detonation_effect
    WEAPON.weapon_flags = H1_ASSET.weapon_flags
    WEAPON.unknown = ""
    WEAPON.unknown_length = len(WEAPON.unknown)
    WEAPON.secondary_trigger_mode = H1_ASSET.secondary_trigger_mode
    WEAPON.maximum_alternate_shots_loaded = H1_ASSET.maximum_alternate_shots_loaded
    WEAPON.turn_on_time = 0.0
    WEAPON.ready_time = H1_ASSET.ready_time
    WEAPON.ready_effect = H1_ASSET.ready_effect
    WEAPON.ready_damage_effect = TAG.TagRef()
    WEAPON.heat_recovery_threshold = H1_ASSET.heat_recovery_threshold
    WEAPON.overheated_threshold = H1_ASSET.overheated_threshold
    WEAPON.heat_detonation_threshold = H1_ASSET.heat_detonation_threshold
    WEAPON.heat_detonation_fraction = H1_ASSET.heat_detonation_fraction
    WEAPON.heat_loss_per_second = H1_ASSET.heat_loss_per_second
    WEAPON.heat_illumination = H1_ASSET.heat_illumination
    WEAPON.overheated_loss_per_second = H1_ASSET.heat_loss_per_second
    WEAPON.overheated = H1_ASSET.overheated
    WEAPON.overheated_damage_effect = TAG.TagRef()
    WEAPON.detonation = H1_ASSET.detonation
    WEAPON.weapon_detonation_damage_effect = TAG.TagRef()
    WEAPON.player_melee_damage = H1_ASSET.player_melee_damage
    WEAPON.player_melee_response = H1_ASSET.player_melee_response
    WEAPON.magnetism_angle = magnetism_angle
    WEAPON.magnetism_range = magnetism_range
    WEAPON.throttle_magnitude = throttle_magnitude
    WEAPON.throttle_minimum_distance = throttle_minimum_distance
    WEAPON.throttle_maximum_adjustment_angle = throttle_maximum_adjustment_angle
    WEAPON.damage_pyramid_angles = damage_pyramid_angles
    WEAPON.damage_pyramid_depth = damage_pyramid_depth

    WEAPON.first_hit_melee_damage = H1_ASSET.player_melee_damage
    WEAPON.first_hit_melee_response = H1_ASSET.player_melee_response
    WEAPON.second_hit_melee_damage = H1_ASSET.player_melee_damage
    WEAPON.second_hit_melee_response = H1_ASSET.player_melee_response
    WEAPON.third_hit_melee_damage = H1_ASSET.player_melee_damage
    WEAPON.third_hit_melee_response = H1_ASSET.player_melee_response
    WEAPON.lunge_melee_damage = TAG.TagRef()
    WEAPON.lunge_melee_response = TAG.TagRef()
    WEAPON.melee_damage_reporting_type = MeleeDamageReportingTypeEnum.generic_melee_damage.value
    WEAPON.magnification_levels = H1_ASSET.magnification_levels
    WEAPON.magnification_range = (H1_ASSET.magnification_range[0], H1_ASSET.magnification_range[1])
    WEAPON.autoaim_angle = H1_ASSET.autoaim_angle
    WEAPON.autoaim_range = H1_ASSET.autoaim_range
    WEAPON.weapon_aim_assist_magnetism_angle = H1_ASSET.magnetism_angle
    WEAPON.weapon_aim_assist_magnetism_range = H1_ASSET.magnetism_range
    WEAPON.deviation_angle = H1_ASSET.deviation_angle
    WEAPON.movement_penalized = H1_ASSET.movement_penalized
    WEAPON.forward_movement_penalty = H1_ASSET.forward_movement_penalty
    WEAPON.sideways_movement_penalty = H1_ASSET.sideways_movement_penalty
    WEAPON.ai_scariness = ai_scariness
    WEAPON.weapon_power_on_time = H1_ASSET.light_power_on_time
    WEAPON.weapon_power_off_time = H1_ASSET.light_power_off_time
    WEAPON.weapon_power_on_effect = H1_ASSET.light_power_on_effect
    WEAPON.weapon_power_off_effect = H1_ASSET.light_power_off_effect
    WEAPON.age_heat_recovery_penalty = H1_ASSET.age_heat_recovery_penalty
    WEAPON.age_rate_of_fire_penalty = H1_ASSET.age_rate_of_fire_penalty
    WEAPON.age_misfire_start = H1_ASSET.age_misfire_start
    WEAPON.age_misfire_chance = H1_ASSET.age_misfire_chance
    WEAPON.pickup_sound = H1_ASSET.pickup_sound
    WEAPON.zoom_in_sound = H1_ASSET.zoom_in_sound
    WEAPON.zoom_out_sound = H1_ASSET.zoom_out_sound
    WEAPON.active_camo_ding = H1_ASSET.active_camo_ding
    WEAPON.active_camo_regrowth_rate = H1_ASSET.active_camo_regrowth_rate
    WEAPON.handle_node = ""
    WEAPON.weapon_class = weapon_class
    WEAPON.weapon_name = H1_ASSET.label
    WEAPON.handle_node_length = len(WEAPON.handle_node)
    WEAPON.weapon_class_length = len(WEAPON.weapon_class)
    WEAPON.weapon_name_length = len(WEAPON.weapon_name)
    WEAPON.multiplayer_weapon_type = multiplayer_weapon_type
    WEAPON.weapon_type = H1_ASSET.weapon_type
    WEAPON.tracking_type = tracking_type
    WEAPON.first_person_tag_block = generate_first_person(H1_ASSET, TAG, WEAPON)
    WEAPON.new_hud_interface = TAG.TagRef("nhdt", H1_ASSET.hud_interface.name, H1_ASSET.hud_interface.name_length)
    WEAPON.weapon_predicted_resources_tag_block = TAG.TagBlock()
    WEAPON.magazines_tag_block = generate_magazines(H1_ASSET, TAG, WEAPON)
    generate_triggers_and_barrels(H1_ASSET, TAG, WEAPON)
    WEAPON.max_movement_acceleration = 0.0
    WEAPON.max_movement_velocity = 0.0
    WEAPON.max_turning_acceleration = 0.0
    WEAPON.max_turning_velocity = 0.0
    WEAPON.deployed_vehicle = TAG.TagRef()
    WEAPON.age_effect = TAG.TagRef()
    WEAPON.aged_weapon = TAG.TagRef()
    WEAPON.first_person_weapon_offset = Vector()
    WEAPON.first_person_scope_size = (0.0, 0.0)

    return WEAPON
