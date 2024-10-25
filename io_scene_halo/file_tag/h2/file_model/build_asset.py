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

import struct

from ....global_functions import tag_format

def write_body(output_stream, TAG, MODEL):
    MODEL.body_header.write(output_stream, TAG, True)
    MODEL.render_model.write(output_stream, False, True)
    MODEL.collision_model.write(output_stream, False, True)
    MODEL.animation.write(output_stream, False, True)
    MODEL.physics.write(output_stream, False, True)
    MODEL.physics_model.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', MODEL.disappear_distance))
    output_stream.write(struct.pack('<f', MODEL.begin_fade_distance))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<f', MODEL.reduce_to_l1))
    output_stream.write(struct.pack('<f', MODEL.reduce_to_l2))
    output_stream.write(struct.pack('<f', MODEL.reduce_to_l3))
    output_stream.write(struct.pack('<f', MODEL.reduce_to_l4))
    output_stream.write(struct.pack('<f', MODEL.reduce_to_l5))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<H', MODEL.shadow_fade_distance))
    output_stream.write(struct.pack('<2x'))
    MODEL.variants_tag_block.write(output_stream, False)
    MODEL.materials_tag_block.write(output_stream, False)
    MODEL.new_damage_info_tag_block.write(output_stream, False)
    MODEL.targets_tag_block.write(output_stream, False)
    MODEL.runtime_regions_tag_block.write(output_stream, False)
    MODEL.runtime_nodes_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<4x'))
    MODEL.model_object_data_tag_block.write(output_stream, False)
    MODEL.default_dialogue.write(output_stream, False, True)
    MODEL.unused.write(output_stream, False, True)
    output_stream.write(struct.pack('<I', MODEL.flags))
    output_stream.write(struct.pack('>I', len(MODEL.default_dialogue_effect)))
    for salt_element in MODEL.salt_array:
        output_stream.write(struct.pack('<b', salt_element))

    output_stream.write(struct.pack('<I', MODEL.runtime_flags))
    MODEL.scenario_load_parameters_tag_block.write(output_stream, False)
    MODEL.hologram_shader.write(output_stream, False, True)
    output_stream.write(struct.pack('>I', len(MODEL.hologram_control_function)))

def write_variants(output_stream, TAG, variants, variants_header):
    if len(variants) > 0:
        variants_header.write(output_stream, TAG, True)
        for variant_element in variants:
            output_stream.write(struct.pack('>I', len(variant_element.name)))
            output_stream.write(struct.pack('<16x'))
            variant_element.regions_tag_block.write(output_stream, False)
            variant_element.objects_tag_block.write(output_stream, False)
            output_stream.write(struct.pack('<8x'))
            output_stream.write(struct.pack('>I', len(variant_element.dialogue_sound_effect)))
            variant_element.dialogue.write(output_stream, False, True)

        for variant_element in variants:
            name_length = len(variant_element.name)
            if name_length > 0:
                output_stream.write(struct.pack('<%ss' % name_length, TAG.string_to_bytes(variant_element.name, False)))

            if len(variant_element.regions) > 0:
                variant_element.regions_header.write(output_stream, TAG, True)
                for region_element in variant_element.regions:
                    output_stream.write(struct.pack('>I', len(region_element.region_name)))
                    output_stream.write(struct.pack('<2x'))
                    output_stream.write(struct.pack('<h', region_element.parent_variant))
                    region_element.permutations_tag_block.write(output_stream, False)
                    output_stream.write(struct.pack('<H', region_element.sort_order))
                    output_stream.write(struct.pack('<2x'))

                for region_element in variant_element.regions:
                    region_name_length = len(region_element.region_name)
                    if region_name_length > 0:
                        output_stream.write(struct.pack('<%ss' % region_name_length, TAG.string_to_bytes(region_element.region_name, False)))

                    if len(region_element.permutations) > 0:
                        region_element.permutations_header.write(output_stream, TAG, True)
                        for permutation_element in region_element.permutations:
                            output_stream.write(struct.pack('>I', len(permutation_element.permutation_name)))
                            output_stream.write(struct.pack('<1x'))
                            output_stream.write(struct.pack('<B', permutation_element.flags))
                            output_stream.write(struct.pack('<2x'))
                            output_stream.write(struct.pack('<f', permutation_element.probability))
                            permutation_element.states_tag_block.write(output_stream, False)
                            output_stream.write(struct.pack('<12x'))

                        for permutation_element in region_element.permutations:
                            permutation_name_length = len(permutation_element.permutation_name)
                            if permutation_name_length > 0:
                                output_stream.write(struct.pack('<%ss' % permutation_name_length, TAG.string_to_bytes(permutation_element.permutation_name, False)))

                            if len(permutation_element.states) > 0:
                                permutation_element.states_header.write(output_stream, TAG, True)
                                for state_element in permutation_element.states:
                                    output_stream.write(struct.pack('>I', len(state_element.permutation_name)))
                                    output_stream.write(struct.pack('<1x'))
                                    output_stream.write(struct.pack('<B', state_element.property_flags))
                                    output_stream.write(struct.pack('<H', state_element.state))
                                    state_element.looping_effect.write(output_stream, False, True)
                                    output_stream.write(struct.pack('>I', len(state_element.looping_effect_marker_name)))
                                    output_stream.write(struct.pack('<f', state_element.initial_probability))

                                for state_element in permutation_element.states:
                                    permutation_name_length = len(state_element.permutation_name)
                                    if permutation_name_length > 0:
                                        output_stream.write(struct.pack('<%ss' % permutation_name_length, TAG.string_to_bytes(state_element.permutation_name, False)))

                                    looping_effect_length = len(state_element.looping_effect.name)
                                    if looping_effect_length > 0:
                                        output_stream.write(struct.pack('<%ssx' % looping_effect_length, TAG.string_to_bytes(state_element.looping_effect.name, False)))

                                    looping_effect_marker_name_length = len(state_element.looping_effect_marker_name)
                                    if looping_effect_marker_name_length > 0:
                                        output_stream.write(struct.pack('<%ss' % looping_effect_marker_name_length, TAG.string_to_bytes(state_element.looping_effect_marker_name, False)))

            if len(variant_element.objects) > 0:
                variant_element.objects_header.write(output_stream, TAG, True)
                for object_element in variant_element.objects:
                    output_stream.write(struct.pack('>I', len(object_element.parent_marker_name)))
                    output_stream.write(struct.pack('>I', len(object_element.child_marker_name)))
                    object_element.child_object.write(output_stream, False, True)

                for object_element in variant_element.objects:
                    parent_marker_name_length = len(object_element.parent_marker_name)
                    if parent_marker_name_length > 0:
                        output_stream.write(struct.pack('<%ss' % parent_marker_name_length, TAG.string_to_bytes(object_element.parent_marker_name, False)))

                    child_marker_name_length = len(object_element.child_marker_name)
                    if child_marker_name_length > 0:
                        output_stream.write(struct.pack('<%ss' % child_marker_name_length, TAG.string_to_bytes(object_element.child_marker_name, False)))

                    child_object_length = len(object_element.child_object.name)
                    if child_object_length > 0:
                        output_stream.write(struct.pack('<%ssx' % child_object_length, TAG.string_to_bytes(object_element.child_object.name, False)))

            dialogue_sound_effect_length = len(variant_element.dialogue_sound_effect)
            if dialogue_sound_effect_length > 0:
                output_stream.write(struct.pack('<%ss' % dialogue_sound_effect_length, TAG.string_to_bytes(variant_element.dialogue_sound_effect, False)))

            dialogue_length = len(variant_element.dialogue.name)
            if dialogue_length > 0:
                output_stream.write(struct.pack('<%ssx' % dialogue_length, TAG.string_to_bytes(variant_element.dialogue.name, False)))

def write_materials(output_stream, TAG, materials, materials_header):
    if len(materials) > 0:
        materials_header.write(output_stream, TAG, True)
        for material_element in materials:
            output_stream.write(struct.pack('>I', len(material_element.material_name)))
            output_stream.write(struct.pack('<H', material_element.material_type))
            output_stream.write(struct.pack('<h', material_element.damage_section))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('>I', len(material_element.global_material_name)))
            output_stream.write(struct.pack('<4x'))

        for material_element in materials:
            material_name_length = len(material_element.material_name)
            if material_name_length > 0:
                output_stream.write(struct.pack('<%ss' % material_name_length, TAG.string_to_bytes(material_element.material_name, False)))

            global_material_name_length = len(material_element.global_material_name)
            if global_material_name_length > 0:
                output_stream.write(struct.pack('<%ss' % global_material_name_length, TAG.string_to_bytes(material_element.global_material_name, False)))

def write_new_damage_info(output_stream, TAG, new_damage_info, new_damage_info_header):
    if len(new_damage_info) > 0:
        new_damage_info_header.write(output_stream, TAG, True)
        for new_damage_info_element in new_damage_info:
            output_stream.write(struct.pack('<I', new_damage_info_element.flags))
            output_stream.write(struct.pack('>I', len(new_damage_info_element.global_indirect_material_name)))
            output_stream.write(struct.pack('<h', new_damage_info_element.indirect_damage_section))
            output_stream.write(struct.pack('<6x'))
            output_stream.write(struct.pack('<B', new_damage_info_element.collision_damage_reporting_type))
            output_stream.write(struct.pack('<B', new_damage_info_element.response_damage_reporting_type))
            output_stream.write(struct.pack('<22x'))
            output_stream.write(struct.pack('<f', new_damage_info_element.maximum_vitality))
            output_stream.write(struct.pack('<f', new_damage_info_element.body_minimum_stun_damage))
            output_stream.write(struct.pack('<f', new_damage_info_element.body_stun_time))
            output_stream.write(struct.pack('<f', new_damage_info_element.body_recharge_time))
            output_stream.write(struct.pack('<f', new_damage_info_element.recharge_fraction))
            output_stream.write(struct.pack('<64x'))
            new_damage_info_element.shield_damaged_first_person_shader.write(output_stream, False, True)
            new_damage_info_element.shield_damaged_shader.write(output_stream, False, True)
            output_stream.write(struct.pack('<f', new_damage_info_element.maximum_shield_vitality))
            output_stream.write(struct.pack('>I', len(new_damage_info_element.global_shield_material_name)))
            output_stream.write(struct.pack('<f', new_damage_info_element.shield_minimum_stun_damage))
            output_stream.write(struct.pack('<f', new_damage_info_element.shield_stun_time))
            output_stream.write(struct.pack('<f', new_damage_info_element.shield_recharge_time))
            output_stream.write(struct.pack('<f', new_damage_info_element.shield_damaged_threshold))
            new_damage_info_element.shield_damaged_effect.write(output_stream, False, True)
            new_damage_info_element.shield_depleted_effect.write(output_stream, False, True)
            new_damage_info_element.shield_recharging_effect.write(output_stream, False, True)
            new_damage_info_element.damage_sections_tag_block.write(output_stream, False)
            new_damage_info_element.nodes_tag_block.write(output_stream, False)
            output_stream.write(struct.pack('<12x'))
            new_damage_info_element.damage_seats_tag_block.write(output_stream, False)
            new_damage_info_element.damage_constraints_tag_block.write(output_stream, False)
            new_damage_info_element.overshield_first_person_shader.write(output_stream, False, True)
            new_damage_info_element.overshield_shader.write(output_stream, False, True)

        for new_damage_info_element in new_damage_info:
            global_indirect_material_name_length = len(new_damage_info_element.global_indirect_material_name)
            if global_indirect_material_name_length > 0:
                output_stream.write(struct.pack('<%ss' % global_indirect_material_name_length, TAG.string_to_bytes(new_damage_info_element.global_indirect_material_name, False)))

            shield_damaged_first_person_shader_length = len(new_damage_info_element.shield_damaged_first_person_shader.name)
            if shield_damaged_first_person_shader_length > 0:
                output_stream.write(struct.pack('<%ssx' % shield_damaged_first_person_shader_length, TAG.string_to_bytes(new_damage_info_element.shield_damaged_first_person_shader.name, False)))

            shield_damaged_shader_length = len(new_damage_info_element.shield_damaged_shader.name)
            if shield_damaged_shader_length > 0:
                output_stream.write(struct.pack('<%ssx' % shield_damaged_shader_length, TAG.string_to_bytes(new_damage_info_element.shield_damaged_shader.name, False)))

            global_shield_material_name_length = len(new_damage_info_element.global_shield_material_name)
            if global_shield_material_name_length > 0:
                output_stream.write(struct.pack('<%ss' % global_shield_material_name_length, TAG.string_to_bytes(new_damage_info_element.global_shield_material_name, False)))

            shield_damaged_effect_length = len(new_damage_info_element.shield_damaged_effect.name)
            if shield_damaged_effect_length > 0:
                output_stream.write(struct.pack('<%ssx' % shield_damaged_effect_length, TAG.string_to_bytes(new_damage_info_element.shield_damaged_effect.name, False)))

            shield_depleted_effect_length = len(new_damage_info_element.shield_depleted_effect.name)
            if shield_depleted_effect_length > 0:
                output_stream.write(struct.pack('<%ssx' % shield_depleted_effect_length, TAG.string_to_bytes(new_damage_info_element.shield_depleted_effect.name, False)))

            shield_recharging_effect_length = len(new_damage_info_element.shield_recharging_effect.name)
            if shield_recharging_effect_length > 0:
                output_stream.write(struct.pack('<%ssx' % shield_recharging_effect_length, TAG.string_to_bytes(new_damage_info_element.shield_recharging_effect.name, False)))

            if len(new_damage_info_element.damage_sections) > 0:
                new_damage_info_element.damage_sections_header.write(output_stream, TAG, True)
                for damage_section_element in new_damage_info_element.damage_sections:
                    output_stream.write(struct.pack('>I', len(damage_section_element.name)))
                    output_stream.write(struct.pack('<I', damage_section_element.flags))
                    output_stream.write(struct.pack('<f', damage_section_element.vitality_percentage))
                    damage_section_element.instant_responses_tag_block.write(output_stream, False)
                    damage_section_element.unknown_0_tag_block.write(output_stream, False)
                    damage_section_element.unknown_1_tag_block.write(output_stream, False)
                    output_stream.write(struct.pack('<f', damage_section_element.stun_time))
                    output_stream.write(struct.pack('<f', damage_section_element.recharge_time))
                    output_stream.write(struct.pack('<4x'))
                    output_stream.write(struct.pack('>I', len(damage_section_element.resurrection_restored_region_name)))
                    output_stream.write(struct.pack('<4x'))

                for damage_section_element in new_damage_info_element.damage_sections:
                    name_length = len(damage_section_element.name)
                    if name_length > 0:
                        output_stream.write(struct.pack('<%ss' % name_length, TAG.string_to_bytes(damage_section_element.name, False)))

                    if len(damage_section_element.instant_responses) > 0:
                        damage_section_element.instant_responses_header.write(output_stream, TAG, True)
                        for instant_response_element in damage_section_element.instant_responses:
                            output_stream.write(struct.pack('<H', instant_response_element.response_type))
                            output_stream.write(struct.pack('<H', instant_response_element.constraint_damage_type))
                            output_stream.write(struct.pack('<I', instant_response_element.flags))
                            output_stream.write(struct.pack('<f', instant_response_element.damage_threshold))
                            instant_response_element.transition_effect.write(output_stream, False, True)
                            instant_response_element.transition_damage_effect.write(output_stream, False, True)
                            output_stream.write(struct.pack('>I', len(instant_response_element.region)))
                            output_stream.write(struct.pack('<H', instant_response_element.new_state))
                            output_stream.write(struct.pack('<h', instant_response_element.runtime_region_index))
                            output_stream.write(struct.pack('>I', len(instant_response_element.effect_marker_name)))
                            output_stream.write(struct.pack('>I', len(instant_response_element.damage_effect_marker_name)))
                            output_stream.write(struct.pack('<f', instant_response_element.response_delay))
                            instant_response_element.delay_effect.write(output_stream, False, True)
                            output_stream.write(struct.pack('>I', len(instant_response_element.delay_effect_marker_name)))
                            output_stream.write(struct.pack('>I', len(instant_response_element.constraint_group_name)))
                            output_stream.write(struct.pack('>I', len(instant_response_element.ejecting_seat_label)))
                            output_stream.write(struct.pack('<f', instant_response_element.skip_fraction))
                            output_stream.write(struct.pack('>I', len(instant_response_element.destroyed_child_object_marker_name)))
                            output_stream.write(struct.pack('<f', instant_response_element.total_damage_threshold))

                        for instant_response_element in damage_section_element.instant_responses:
                            transition_effect_length = len(instant_response_element.transition_effect.name)
                            if transition_effect_length > 0:
                                output_stream.write(struct.pack('<%ssx' % transition_effect_length, TAG.string_to_bytes(instant_response_element.transition_effect.name, False)))

                            instant_response_element.ires_header.write(output_stream, TAG, True)

                            transition_damage_effect_length = len(instant_response_element.transition_damage_effect.name)
                            if transition_damage_effect_length > 0:
                                output_stream.write(struct.pack('<%ssx' % transition_damage_effect_length, TAG.string_to_bytes(instant_response_element.transition_damage_effect.name, False)))

                            region_length = len(instant_response_element.region)
                            if region_length > 0:
                                output_stream.write(struct.pack('<%ss' % region_length, TAG.string_to_bytes(instant_response_element.region, False)))

                            effect_marker_name_length = len(instant_response_element.effect_marker_name)
                            if effect_marker_name_length > 0:
                                output_stream.write(struct.pack('<%ss' % effect_marker_name_length, TAG.string_to_bytes(instant_response_element.effect_marker_name, False)))

                            instant_response_element.irem_header.write(output_stream, TAG, True)

                            damage_effect_marker_name_length = len(instant_response_element.damage_effect_marker_name)
                            if damage_effect_marker_name_length > 0:
                                output_stream.write(struct.pack('<%ss' % damage_effect_marker_name_length, TAG.string_to_bytes(instant_response_element.damage_effect_marker_name, False)))

                            delay_effect_length = len(instant_response_element.delay_effect.name)
                            if delay_effect_length > 0:
                                output_stream.write(struct.pack('<%ssx' % delay_effect_length, TAG.string_to_bytes(instant_response_element.delay_effect.name, False)))

                            delay_effect_marker_name_length = len(instant_response_element.delay_effect_marker_name)
                            if delay_effect_marker_name_length > 0:
                                output_stream.write(struct.pack('<%ss' % delay_effect_marker_name_length, TAG.string_to_bytes(instant_response_element.delay_effect_marker_name, False)))

                            constraint_group_name_length = len(instant_response_element.constraint_group_name)
                            if constraint_group_name_length > 0:
                                output_stream.write(struct.pack('<%ss' % constraint_group_name_length, TAG.string_to_bytes(instant_response_element.constraint_group_name, False)))

                            ejecting_seat_label_length = len(instant_response_element.ejecting_seat_label)
                            if ejecting_seat_label_length > 0:
                                output_stream.write(struct.pack('<%ss' % ejecting_seat_label_length, TAG.string_to_bytes(instant_response_element.ejecting_seat_label, False)))

                            destroyed_child_object_marker_name_length = len(instant_response_element.destroyed_child_object_marker_name)
                            if destroyed_child_object_marker_name_length > 0:
                                output_stream.write(struct.pack('<%ss' % destroyed_child_object_marker_name_length, TAG.string_to_bytes(instant_response_element.destroyed_child_object_marker_name, False)))

                    resurrection_restored_region_name_length = len(damage_section_element.resurrection_restored_region_name)
                    if resurrection_restored_region_name_length > 0:
                        output_stream.write(struct.pack('<%ss' % resurrection_restored_region_name_length, TAG.string_to_bytes(damage_section_element.resurrection_restored_region_name, False)))

            overshield_first_person_shader_length = len(new_damage_info_element.overshield_first_person_shader.name)
            if overshield_first_person_shader_length > 0:
                output_stream.write(struct.pack('<%ssx' % overshield_first_person_shader_length, TAG.string_to_bytes(new_damage_info_element.overshield_first_person_shader.name, False)))

            overshield_shader_length = len(new_damage_info_element.overshield_shader.name)
            if overshield_shader_length > 0:
                output_stream.write(struct.pack('<%ssx' % overshield_shader_length, TAG.string_to_bytes(new_damage_info_element.overshield_shader.name, False)))

def build_asset(output_stream, MODEL, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    MODEL.header.write(output_stream, False, True)
    write_body(output_stream, TAG, MODEL)

    render_model_length = len(MODEL.render_model.name)
    if render_model_length > 0:
        output_stream.write(struct.pack('<%ssx' % render_model_length, TAG.string_to_bytes(MODEL.render_model.name, False)))

    collision_model_length = len(MODEL.collision_model.name)
    if collision_model_length > 0:
        output_stream.write(struct.pack('<%ssx' % collision_model_length, TAG.string_to_bytes(MODEL.collision_model.name, False)))

    animation_length = len(MODEL.animation.name)
    if animation_length > 0:
        output_stream.write(struct.pack('<%ssx' % animation_length, TAG.string_to_bytes(MODEL.animation.name, False)))

    physics_length = len(MODEL.physics.name)
    if physics_length > 0:
        output_stream.write(struct.pack('<%ssx' % physics_length, TAG.string_to_bytes(MODEL.physics.name, False)))

    physics_model_length = len(MODEL.physics_model.name)
    if physics_model_length > 0:
        output_stream.write(struct.pack('<%ssx' % physics_model_length, TAG.string_to_bytes(MODEL.physics_model.name, False)))

    write_variants(output_stream, TAG, MODEL.variants, MODEL.variants_header)
    write_materials(output_stream, TAG, MODEL.materials, MODEL.materials_header)
    write_new_damage_info(output_stream, TAG, MODEL.new_damage_info, MODEL.new_damage_info_header)
