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
from .format import (VehicleAsset,
                            ObjectFlags,
                            ObjectFunctionEnum,
                            UnitFlags,
                            TeamsEnum,
                            ConstantSoundVolumeEnum,
                            UnitFunctionEnum,
                            MotionSensorBlipSizeEnum,
                            MetaGameTypeEnum,
                            MetaGameClassEnum,
                            GrenadeTypeEnum,
                            VehicleFlags,
                            VehicleTypeEnum,
                            VehicleFunctionEnum)

XML_OUTPUT = False

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    VEHICLE = VehicleAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    VEHICLE.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    input_stream.read(2) # Padding?
    VEHICLE.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    VEHICLE.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    VEHICLE.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    VEHICLE.origin_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "origin offset"))
    VEHICLE.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    input_stream.read(4) # Padding?
    VEHICLE.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    VEHICLE.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    input_stream.read(40) # Padding?
    VEHICLE.collision_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision model"))
    VEHICLE.physics = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics"))
    VEHICLE.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    VEHICLE.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    input_stream.read(84) # Padding?
    VEHICLE.render_bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "render bounding radius"))
    VEHICLE.object_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ObjectFunctionEnum))
    VEHICLE.object_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ObjectFunctionEnum))
    VEHICLE.object_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ObjectFunctionEnum))
    VEHICLE.object_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ObjectFunctionEnum))
    input_stream.read(44) # Padding?
    VEHICLE.hud_text_message_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    VEHICLE.forced_shader_permutation_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "forced shader_permutation index"))
    VEHICLE.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    VEHICLE.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    VEHICLE.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    VEHICLE.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    VEHICLE.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    input_stream.read(2) # Padding?
    VEHICLE.unit_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", UnitFlags))
    VEHICLE.default_team = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "default team", TeamsEnum))
    VEHICLE.constant_sound_volume = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "constant sound volume", ConstantSoundVolumeEnum))
    VEHICLE.rider_damage_fraction = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "rider damage fraction"))
    VEHICLE.integrated_light_toggle = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "integrated light toggle"))
    VEHICLE.unit_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", UnitFunctionEnum))
    VEHICLE.unit_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", UnitFunctionEnum))
    VEHICLE.unit_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", UnitFunctionEnum))
    VEHICLE.unit_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", UnitFunctionEnum))
    VEHICLE.camera_field_of_view = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "camera field of view"))
    VEHICLE.camera_stiffness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera stiffness"))
    VEHICLE.camera_marker_name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(tag_node, "camera marker name"))
    VEHICLE.camera_submerged_marker_name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(tag_node, "camera submerged marker name"))
    VEHICLE.pitch_auto_level = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "pitch auto level"))
    VEHICLE.pitch_range = TAG.read_min_max_degree(input_stream, TAG, tag_format.XMLData(tag_node, "pitch range"))
    VEHICLE.camera_tracks_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "camera tracks"))
    VEHICLE.seat_acceleration_scale = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "seat acceleration scale"))
    input_stream.read(12) # Padding?
    VEHICLE.soft_ping_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "soft ping threshold"))
    VEHICLE.soft_ping_interrupt_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "soft ping interrupt time"))
    VEHICLE.hard_ping_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard ping threshold"))
    VEHICLE.hard_ping_interrupt_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard ping interrupt time"))
    VEHICLE.hard_death_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard death threshold"))
    VEHICLE.feign_death_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death threshold"))
    VEHICLE.feign_death_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death time"))
    VEHICLE.distance_of_evade_anim = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "distance of evade anim"))
    VEHICLE.distance_of_dive_anim = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "distance of dive anim"))
    input_stream.read(4) # Padding?
    VEHICLE.stunned_movement_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "stunned movement threshold"))
    VEHICLE.feign_death_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death chance"))
    VEHICLE.feign_repeat_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign repeat chance"))
    VEHICLE.spawned_actor = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "spawned actor"))
    VEHICLE.spawned_actor_count = TAG.read_min_max_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "spawned actor count"))
    VEHICLE.spawned_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "spawned velocity"))
    VEHICLE.aiming_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming velocity maximum"))
    VEHICLE.aiming_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming acceleration maximum"))
    VEHICLE.casual_aiming_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "casual aiming modifier"))
    VEHICLE.looking_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming acceleration maximum"))
    VEHICLE.looking_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming acceleration maximum"))
    input_stream.read(8) # Padding?
    VEHICLE.ai_vehicle_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai vehicle radius"))
    VEHICLE.ai_danger_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai danger radius"))
    VEHICLE.melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "melee damage"))
    VEHICLE.motion_sensor_blip_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "motion sensor blip size", MotionSensorBlipSizeEnum))
    input_stream.read(2) # Padding?
    VEHICLE.metagame_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "metagame type", MetaGameTypeEnum))
    VEHICLE.metagame_class = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "metagame class", MetaGameClassEnum))
    input_stream.read(8) # Padding?
    VEHICLE.new_hud_interfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "new hud interfaces"))
    VEHICLE.dialogue_variants_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "dialogue variants"))
    VEHICLE.grenade_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "grenade velocity"))
    VEHICLE.grenade_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade type", GrenadeTypeEnum))
    VEHICLE.grenade_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade count"))
    input_stream.read(4) # Padding?
    VEHICLE.powered_seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "powered seats"))
    VEHICLE.weapons_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapons"))
    VEHICLE.seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "seats"))
    input_stream.read(2) # Padding?
    VEHICLE.vehicle_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", VehicleFlags))
    VEHICLE.vehicle_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", VehicleTypeEnum))
    input_stream.read(2) # Padding?
    VEHICLE.maximum_forward_speed = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai vehicle radius"))
    VEHICLE.maximum_reverse_speed = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai vehicle radius"))
    VEHICLE.speed_acceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai vehicle radius"))
    VEHICLE.speed_deceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai vehicle radius"))
    VEHICLE.maximum_left_turn = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai vehicle radius"))
    VEHICLE.maximum_right_turn_negative = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai vehicle radius"))
    VEHICLE.wheel_circumference = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai vehicle radius"))
    VEHICLE.turn_rate = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai vehicle radius"))
    VEHICLE.blur_speed = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai vehicle radius"))
    VEHICLE.vehicle_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", VehicleFunctionEnum))
    VEHICLE.vehicle_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", VehicleFunctionEnum))
    VEHICLE.vehicle_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", VehicleFunctionEnum))
    VEHICLE.vehicle_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", VehicleFunctionEnum))
    input_stream.read(12) # Padding?
    VEHICLE.maximum_left_slide = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum left slide"))
    VEHICLE.maximum_right_slide = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum right slide"))
    VEHICLE.slide_acceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "slide acceleration"))
    VEHICLE.slide_deceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "slide deceleration"))
    VEHICLE.minimum_flipping_angular_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum flipping angular velocity"))
    VEHICLE.maximum_flipping_angular_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum flipping angular velocity"))
    input_stream.read(24) # Padding?
    VEHICLE.fixed_gun_yaw = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "fixed gun yaw"))
    VEHICLE.fixed_gun_pitch = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "fixed gun pitch"))
    input_stream.read(24) # Padding?
    VEHICLE.ai_sideslip_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai sideslip distance"))
    VEHICLE.ai_destination_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai destination radius"))
    VEHICLE.ai_avoidance_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai avoidance distance"))
    VEHICLE.ai_pathfinding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai pathfinding radius"))
    VEHICLE.ai_charge_repeat_timeout = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai charge repeat timeout"))
    VEHICLE.ai_strafing_abort_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai strafing abort range"))
    VEHICLE.ai_overstepping_bounds = TAG.read_min_max_degree(input_stream, TAG, tag_format.XMLData(tag_node, "ai overstepping bounds"))
    VEHICLE.ai_steering_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "ai steering maximum"))
    VEHICLE.ai_throttle_maximum = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai throttle maximum"))
    VEHICLE.ai_move_position_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai move position time"))
    input_stream.read(4) # Padding?
    VEHICLE.suspension_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "suspension sound"))
    VEHICLE.crash_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crash sound"))
    VEHICLE.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    VEHICLE.effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "effect"))

    if VEHICLE.model.name_length > 0:
        VEHICLE.model.name = TAG.read_variable_string(input_stream, VEHICLE.model.name_length, TAG)

    if VEHICLE.animation_graph.name_length > 0:
        VEHICLE.animation_graph.name = TAG.read_variable_string(input_stream, VEHICLE.animation_graph.name_length, TAG)

    if VEHICLE.collision_model.name_length > 0:
        VEHICLE.collision_model.name = TAG.read_variable_string(input_stream, VEHICLE.collision_model.name_length, TAG)

    if VEHICLE.physics.name_length > 0:
        VEHICLE.physics.name = TAG.read_variable_string(input_stream, VEHICLE.physics.name_length, TAG)

    if VEHICLE.modifier_shader.name_length > 0:
        VEHICLE.modifier_shader.name = TAG.read_variable_string(input_stream, VEHICLE.modifier_shader.name_length, TAG)

    if VEHICLE.creation_effect.name_length > 0:
        VEHICLE.creation_effect.name = TAG.read_variable_string(input_stream, VEHICLE.creation_effect.name_length, TAG)

    if VEHICLE.integrated_light_toggle.name_length > 0:
        VEHICLE.integrated_light_toggle.name = TAG.read_variable_string(input_stream, VEHICLE.integrated_light_toggle.name_length, TAG)

    if VEHICLE.spawned_actor.name_length > 0:
        VEHICLE.spawned_actor.name = TAG.read_variable_string(input_stream, VEHICLE.spawned_actor.name_length, TAG)

    if VEHICLE.melee_damage.name_length > 0:
        VEHICLE.melee_damage.name = TAG.read_variable_string(input_stream, VEHICLE.melee_damage.name_length, TAG)

    if VEHICLE.suspension_sound.name_length > 0:
        VEHICLE.suspension_sound.name = TAG.read_variable_string(input_stream, VEHICLE.suspension_sound.name_length, TAG)

    if VEHICLE.crash_sound.name_length > 0:
        VEHICLE.crash_sound.name = TAG.read_variable_string(input_stream, VEHICLE.crash_sound.name_length, TAG)

    if VEHICLE.material_effects.name_length > 0:
        VEHICLE.material_effects.name = TAG.read_variable_string(input_stream, VEHICLE.material_effects.name_length, TAG)

    if VEHICLE.effect.name_length > 0:
        VEHICLE.effect.name = TAG.read_variable_string(input_stream, VEHICLE.effect.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        animation_graph_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "animation graph")
        collision_model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "collision model")
        physics_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "physics")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        integrated_light_toggle_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "integrated light toggle")
        spawned_actor_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "spawned actor")
        melee_damage_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "melee damage")
        suspension_sound_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "suspension sound")
        crash_sound_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "crash sound")
        material_effects_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "material effects")
        effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "effect")
        VEHICLE.model.append_xml_attributes(model_node)
        VEHICLE.animation_graph.append_xml_attributes(animation_graph_node)
        VEHICLE.collision_model.append_xml_attributes(collision_model_node)
        VEHICLE.physics.append_xml_attributes(physics_node)
        VEHICLE.modifier_shader.append_xml_attributes(modifier_shader_node)
        VEHICLE.creation_effect.append_xml_attributes(creation_effect_node)
        VEHICLE.integrated_light_toggle.append_xml_attributes(integrated_light_toggle_node)
        VEHICLE.spawned_actor.append_xml_attributes(spawned_actor_node)
        VEHICLE.melee_damage.append_xml_attributes(melee_damage_node)
        VEHICLE.suspension_sound.append_xml_attributes(suspension_sound_node)
        VEHICLE.crash_sound.append_xml_attributes(crash_sound_node)
        VEHICLE.material_effects.append_xml_attributes(material_effects_node)
        VEHICLE.effect.append_xml_attributes(effect_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, VEHICLE.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return VEHICLE
