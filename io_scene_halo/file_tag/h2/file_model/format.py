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

from enum import Flag, Enum, auto

SALT_SIZE = 64

class ShadowFadeDistanceEnum(Enum):
    fade_at_super_high_detail_level = 0
    fade_at_high_detail_level = auto()
    fade_at_medium_detail_level = auto()
    fade_at_low_detail_level = auto()
    fade_at_super_low_detail_level = auto()
    fade_never = auto()

class ModelFlags(Flag):
    active_camo_always_on = auto()
    active_camo_always_merge = auto()
    active_camo_never_merge = auto()

class RuntimeFlags(Flag):
    contains_runtime_nodes = auto()

class StateEnum(Enum):
    default = 0
    minor_damage = auto()
    medium_damage = auto()
    major_damage = auto()
    destroyed = auto()

class NewDamageInfoFlags(Flag):
    takes_shield_damage_for_children = auto()
    takes_body_damage_for_children = auto()
    always_shields_friendly_damage = auto()
    passes_area_damage_to_children = auto()
    parent_never_takes_body_damage_for_us = auto()
    only_damaged_by_explosives = auto()
    parent_never_takes_shield_damage_for_us = auto()
    cannot_die_from_damage = auto()
    passes_attached_damage_to_riders = auto()

class DamageSectionFlags(Flag):
    absorbs_body_damage = auto()
    takes_full_dmg_when_object_dies = auto()
    cannot_die_with_riders = auto()
    takes_full_dmg_when_obj_dstryd = auto()
    restored_on_ressurection = auto()
    unused_5 = auto()
    unused_6 = auto()
    heatshottable = auto()
    ignores_shields = auto()

class ModelAsset():
    def __init__(self):
        self.header = None
        self.model_body_header = None
        self.model_body = None
        self.variants_header = None
        self.variants = None
        self.materials_header = None
        self.materials = None
        self.new_damage_info_header = None
        self.new_damage_info = None
        self.targets_header = None
        self.targets = None
        self.runtime_regions_header = None
        self.runtime_regions = None
        self.runtime_nodes_header = None
        self.runtime_nodes = None
        self.model_object_data_header = None
        self.model_object_data = None
        self.scenario_load_parameters_header = None
        self.scenario_load_parameters = None

    class ModelBody:
        def __init__(self, render_model=None, collision_model=None, animation=None, physics=None, physics_model=None, disappear_distance=0.0, begin_fade_distance=0.0, 
                     reduce_to_l1=0.0, reduce_to_l2=0.0, reduce_to_l3=0.0, reduce_to_l4=0.0, reduce_to_l5=0.0, shadow_fade_distance=0, variants_tag_block=None, 
                     materials_tag_block=None, new_damage_info_tag_block=None, targets_tag_block=None, runtime_regions_tag_block=None, runtime_nodes_tag_block=None, 
                     model_object_data_tag_block=None, default_dialogue=None, unused=None, flags=0, default_dialogue_effect="", default_dialogue_effect_length=0, 
                     salt_array=None, runtime_flags=0, scenario_load_parameters_tag_block=None, hologram_shader=None, hologram_control_function="", 
                     hologram_control_function_length=0):
            self.render_model = render_model
            self.collision_model = collision_model
            self.animation = animation
            self.physics = physics
            self.physics_model = physics_model
            self.disappear_distance = disappear_distance
            self.begin_fade_distance = begin_fade_distance
            self.reduce_to_l1 = reduce_to_l1
            self.reduce_to_l2 = reduce_to_l2
            self.reduce_to_l3 = reduce_to_l3
            self.reduce_to_l4 = reduce_to_l4
            self.reduce_to_l5 = reduce_to_l5
            self.shadow_fade_distance = shadow_fade_distance
            self.variants_tag_block = variants_tag_block
            self.materials_tag_block = materials_tag_block
            self.new_damage_info_tag_block = new_damage_info_tag_block
            self.targets_tag_block = targets_tag_block
            self.runtime_regions_tag_block = runtime_regions_tag_block
            self.runtime_nodes_tag_block = runtime_nodes_tag_block
            self.model_object_data_tag_block = model_object_data_tag_block
            self.default_dialogue = default_dialogue
            self.unused = unused
            self.flags = flags
            self.default_dialogue_effect = default_dialogue_effect
            self.default_dialogue_effect_length = default_dialogue_effect_length
            self.salt_array = salt_array
            self.runtime_flags = runtime_flags
            self.scenario_load_parameters_tag_block = scenario_load_parameters_tag_block
            self.hologram_shader = hologram_shader
            self.hologram_control_function = hologram_control_function
            self.hologram_control_function_length = hologram_control_function_length

    class Variant:
        def __init__(self, name="", name_length=0, regions_tag_block=None, regions_header=None, regions=None, objects_tag_block=None, objects_header=None, 
                     objects=None, dialogue_sound_effect="", dialogue_sound_effect_length=0, dialogue=None):
            self.name = name
            self.name_length = name_length
            self.regions_tag_block = regions_tag_block
            self.regions_header = regions_header
            self.regions = regions
            self.objects_tag_block = objects_tag_block
            self.objects_header = objects_header
            self.objects = objects
            self.dialogue_sound_effect = dialogue_sound_effect
            self.dialogue_sound_effect_length = dialogue_sound_effect_length
            self.dialogue = dialogue

    class Region:
        def __init__(self, region_name="", region_name_length=0, parent_variant=0, permutations_tag_block=None, permutations_header=None, permutations=None, 
                     sort_order=0):
            self.region_name = region_name
            self.region_name_length = region_name_length
            self.parent_variant = parent_variant
            self.permutations_tag_block = permutations_tag_block
            self.permutations_header = permutations_header
            self.permutations = permutations
            self.sort_order = sort_order

    class Permutation:
        def __init__(self, permutation_name="", permutation_name_length=0, flags=0, probability=0.0, states_tag_block=None, states_header=None, 
                     states=None):
            self.permutation_name = permutation_name
            self.permutation_name_length = permutation_name_length
            self.flags = flags
            self.probability = probability
            self.states_tag_block = states_tag_block
            self.states_header = states_header
            self.states = states

    class State:
        def __init__(self, permutation_name="", permutation_name_length=0, property_flags=0, state=0, looping_effect=None, looping_effect_marker_name="", 
                     looping_effect_marker_name_length=0, initial_probability=0.0):
            self.permutation_name = permutation_name
            self.permutation_name_length = permutation_name_length
            self.property_flags = property_flags
            self.state = state
            self.looping_effect = looping_effect
            self.looping_effect_marker_name = looping_effect_marker_name
            self.looping_effect_marker_name_length = looping_effect_marker_name_length
            self.initial_probability = initial_probability

    class Object:
        def __init__(self, parent_marker_name="", parent_marker_name_length=0, child_marker_name="", child_marker_name_length=0, child_object=None):
            self.parent_marker_name = parent_marker_name
            self.parent_marker_name_length = parent_marker_name_length
            self.child_marker_name = child_marker_name
            self.child_marker_name_length = child_marker_name_length
            self.child_object = child_object

    class Materials:
        def __init__(self, material_name="", material_name_length=0, material_type=0, damage_section=0, global_material_name="", 
                     global_material_name_length=0):
            self.material_name = material_name
            self.material_name_length = material_name_length
            self.material_type = material_type
            self.damage_section = damage_section
            self.global_material_name = global_material_name
            self.global_material_name_length = global_material_name_length

    class NewDamageInfo:
        def __init__(self, flags=0, global_indirect_material_name="", global_indirect_material_name_length=0, indirect_damage_section=0, 
                     collision_damage_reporting_type=0, response_damage_reporting_type=0, maximum_vitality=0.0, body_minimum_stun_damage=0.0, 
                     body_stun_time=0.0, body_recharge_time=0.0, recharge_fraction=0.0, shield_damaged_first_person_shader=None, shield_damaged_shader=None, 
                     maximum_shield_vitality=0.0, global_shield_material_name="", global_shield_material_name_length=0, shield_minimum_stun_damage=0.0, 
                     shield_stun_time=0.0, shield_recharge_time=0.0, shield_damaged_threshold=0.0, shield_damaged_effect=None, shield_depleted_effect=None, 
                     shield_recharging_effect=None, damage_sections_tag_block=None, damage_sections_header=None, damage_sections=None, nodes_tag_block=None, 
                     nodes_header=None, nodes=None, damage_seats_tag_block=None, damage_seats_header=None, damage_seats=None, 
                     damage_constraints_tag_block=None, damage_constraints_header=None, damage_constraints=None, overshield_first_person_shader=None, 
                     overshield_shader=None):
            self.flags = flags
            self.global_indirect_material_name = global_indirect_material_name
            self.global_indirect_material_name_length = global_indirect_material_name_length
            self.indirect_damage_section = indirect_damage_section
            self.collision_damage_reporting_type = collision_damage_reporting_type
            self.response_damage_reporting_type = response_damage_reporting_type
            self.maximum_vitality = maximum_vitality
            self.body_minimum_stun_damage = body_minimum_stun_damage
            self.body_stun_time = body_stun_time
            self.body_recharge_time = body_recharge_time
            self.recharge_fraction = recharge_fraction
            self.shield_damaged_first_person_shader = shield_damaged_first_person_shader
            self.shield_damaged_shader = shield_damaged_shader
            self.maximum_shield_vitality = maximum_shield_vitality
            self.global_shield_material_name = global_shield_material_name
            self.global_shield_material_name_length = global_shield_material_name_length
            self.shield_minimum_stun_damage = shield_minimum_stun_damage
            self.shield_stun_time = shield_stun_time
            self.shield_recharge_time = shield_recharge_time
            self.shield_damaged_threshold = shield_damaged_threshold
            self.shield_damaged_effect = shield_damaged_effect
            self.shield_depleted_effect = shield_depleted_effect
            self.shield_recharging_effect = shield_recharging_effect
            self.damage_sections_tag_block = damage_sections_tag_block
            self.damage_sections_header = damage_sections_header
            self.damage_sections = damage_sections
            self.nodes_tag_block = nodes_tag_block
            self.nodes_header = nodes_header
            self.nodes = nodes
            self.damage_seats_tag_block = damage_seats_tag_block
            self.damage_seats_header = damage_seats_header
            self.damage_seats = damage_seats
            self.damage_constraints_tag_block = damage_constraints_tag_block
            self.damage_constraints_header = damage_constraints_header
            self.damage_constraints = damage_constraints
            self.overshield_first_person_shader = overshield_first_person_shader
            self.overshield_shader = overshield_shader

    class DamageSection:
        def __init__(self, name="", name_length=0, flags=0, vitality_percentage=0.0, instant_responses_tag_block=None, instant_responses_header=None, 
                     instant_responses=None, unknown_0_tag_block=None, unknown_0_header=None, unknown_0=None, unknown_1_tag_block=None, 
                     unknown_1_header=None, unknown_1=None, stun_time=0.0, recharge_time=0.0, resurrection_restored_region_name="", 
                     resurrection_restored_region_name_length=0):
            self.name = name
            self.name_length = name_length
            self.flags = flags
            self.vitality_percentage = vitality_percentage
            self.instant_responses_tag_block = instant_responses_tag_block
            self.instant_responses_header = instant_responses_header
            self.instant_responses = instant_responses
            self.unknown_0_tag_block = unknown_0_tag_block
            self.unknown_0_header = unknown_0_header
            self.unknown_0 = unknown_0
            self.unknown_1_tag_block = unknown_1_tag_block
            self.unknown_1_header = unknown_1_header
            self.unknown_1 = unknown_1
            self.stun_time = stun_time
            self.recharge_time = recharge_time
            self.resurrection_restored_region_name = resurrection_restored_region_name
            self.resurrection_restored_region_name_length = resurrection_restored_region_name_length

    class InstantResponse:
        def __init__(self, response_type=0, constraint_damage_type=0, flags=0, damage_threshold=0.0, transition_effect=None, transition_damage_effect=None, 
                     region="", region_length=0, new_state=0, runtime_region_index=0, effect_marker_name="", effect_marker_name_length=0, 
                     damage_effect_marker_name="", damage_effect_marker_name_length=0, response_delay=0.0, delay_effect=None, delay_effect_marker_name="", 
                     delay_effect_marker_name_length=0, constraint_group_name="", constraint_group_name_length=0, ejecting_seat_label="", 
                     ejecting_seat_label_length=0, skip_fraction=0.0, destroyed_child_object_marker_name="", destroyed_child_object_marker_name_length=0, 
                     total_damage_threshold=0.0, ires_header=None, irem_header=None):
            self.response_type = response_type
            self.constraint_damage_type = constraint_damage_type
            self.flags = flags
            self.damage_threshold = damage_threshold
            self.transition_effect = transition_effect
            self.transition_damage_effect = transition_damage_effect
            self.region = region
            self.region_length = region_length
            self.new_state = new_state
            self.runtime_region_index = runtime_region_index
            self.effect_marker_name = effect_marker_name
            self.effect_marker_name_length = effect_marker_name_length
            self.damage_effect_marker_name = damage_effect_marker_name
            self.damage_effect_marker_name_length = damage_effect_marker_name_length
            self.response_delay = response_delay
            self.delay_effect = delay_effect
            self.delay_effect_marker_name = delay_effect_marker_name
            self.delay_effect_marker_name_length = delay_effect_marker_name_length
            self.constraint_group_name = constraint_group_name
            self.constraint_group_name_length = constraint_group_name_length
            self.ejecting_seat_label = ejecting_seat_label
            self.ejecting_seat_label_length = ejecting_seat_label_length
            self.skip_fraction = skip_fraction
            self.destroyed_child_object_marker_name = destroyed_child_object_marker_name
            self.destroyed_child_object_marker_name_length = destroyed_child_object_marker_name_length
            self.total_damage_threshold = total_damage_threshold
            self.ires_header = ires_header
            self.irem_header = irem_header

    class DamageSeat:
        def __init__(self, seat_label="", seat_label_length=0, direct_damage_scale=0.0, damage_transfer_fall_off=0.0, maximum_transfer_damage_scale=0.0, 
                     minimum_transfer_damage_scale=0.0):
            self.seat_label = seat_label
            self.seat_label_length = seat_label_length
            self.direct_damage_scale = direct_damage_scale
            self.damage_transfer_fall_off = damage_transfer_fall_off
            self.maximum_transfer_damage_scale = maximum_transfer_damage_scale
            self.minimum_transfer_damage_scale = minimum_transfer_damage_scale

    class DamageConstraint:
        def __init__(self, physics_model_constraint_name="", physics_model_constraint_name_length=0, damage_constraint_name="", 
                     damage_constraint_name_length=0, damage_constraint_group_name="", damage_constraint_group_name_length=0, group_probability_scale=0.0):
            self.physics_model_constraint_name = physics_model_constraint_name
            self.physics_model_constraint_name_length = physics_model_constraint_name_length
            self.damage_constraint_name = damage_constraint_name
            self.damage_constraint_name_length = damage_constraint_name_length
            self.damage_constraint_group_name = damage_constraint_group_name
            self.damage_constraint_group_name_length = damage_constraint_group_name_length
            self.group_probability_scale = group_probability_scale
