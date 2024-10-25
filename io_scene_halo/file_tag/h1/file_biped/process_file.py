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
    BipedAsset,
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
    BipedFlags,
    BipedFunctionEnum
    )
from ....global_functions import tag_format

XML_OUTPUT = False

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    BIPED = BipedAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    BIPED.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    input_stream.read(2) # Padding?
    BIPED.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    BIPED.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    BIPED.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    BIPED.origin_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "origin offset"))
    BIPED.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    input_stream.read(4) # Padding?
    BIPED.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    BIPED.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    input_stream.read(40) # Padding?
    BIPED.collision_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision model"))
    BIPED.physics = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics"))
    BIPED.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    BIPED.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    input_stream.read(84) # Padding?
    BIPED.render_bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "render bounding radius"))
    BIPED.object_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ObjectFunctionEnum))
    BIPED.object_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ObjectFunctionEnum))
    BIPED.object_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ObjectFunctionEnum))
    BIPED.object_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ObjectFunctionEnum))
    input_stream.read(44) # Padding?
    BIPED.hud_text_message_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    BIPED.forced_shader_permutation_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "forced shader_permutation index"))
    BIPED.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    BIPED.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    BIPED.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    BIPED.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    BIPED.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    input_stream.read(2) # Padding?
    BIPED.unit_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", UnitFlags))
    BIPED.default_team = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "default team", TeamsEnum))
    BIPED.constant_sound_volume = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "constant sound volume", ConstantSoundVolumeEnum))
    BIPED.rider_damage_fraction = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "rider damage fraction"))
    BIPED.integrated_light_toggle = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "integrated light toggle"))
    BIPED.unit_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", UnitFunctionEnum))
    BIPED.unit_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", UnitFunctionEnum))
    BIPED.unit_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", UnitFunctionEnum))
    BIPED.unit_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", UnitFunctionEnum))
    BIPED.camera_field_of_view = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "camera field of view"))
    BIPED.camera_stiffness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera stiffness"))
    BIPED.camera_marker_name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(tag_node, "camera marker name"))
    BIPED.camera_submerged_marker_name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(tag_node, "camera submerged marker name"))
    BIPED.pitch_auto_level = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "pitch auto level"))
    BIPED.pitch_range = TAG.read_min_max_degree(input_stream, TAG, tag_format.XMLData(tag_node, "pitch range"))
    BIPED.camera_tracks_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "camera tracks"))
    BIPED.seat_acceleration_scale = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "seat acceleration scale"))
    input_stream.read(12) # Padding?
    BIPED.soft_ping_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "soft ping threshold"))
    BIPED.soft_ping_interrupt_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "soft ping interrupt time"))
    BIPED.hard_ping_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard ping threshold"))
    BIPED.hard_ping_interrupt_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard ping interrupt time"))
    BIPED.hard_death_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard death threshold"))
    BIPED.feign_death_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death threshold"))
    BIPED.feign_death_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death time"))
    BIPED.distance_of_evade_anim = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "distance of evade anim"))
    BIPED.distance_of_dive_anim = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "distance of dive anim"))
    input_stream.read(4) # Padding?
    BIPED.stunned_movement_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "stunned movement threshold"))
    BIPED.feign_death_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death chance"))
    BIPED.feign_repeat_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign repeat chance"))
    BIPED.spawned_actor = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "spawned actor"))
    BIPED.spawned_actor_count = TAG.read_min_max_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "spawned actor count"))
    BIPED.spawned_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "spawned velocity"))
    BIPED.aiming_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming velocity maximum"))
    BIPED.aiming_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming acceleration maximum"))
    BIPED.casual_aiming_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "casual aiming modifier"))
    BIPED.looking_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming acceleration maximum"))
    BIPED.looking_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming acceleration maximum"))
    input_stream.read(8) # Padding?
    BIPED.ai_vehicle_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai vehicle radius"))
    BIPED.ai_danger_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai danger radius"))
    BIPED.melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "melee damage"))
    BIPED.motion_sensor_blip_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "motion sensor blip size", MotionSensorBlipSizeEnum))
    input_stream.read(2) # Padding?
    BIPED.metagame_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "metagame type", MetaGameTypeEnum))
    BIPED.metagame_class = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "metagame class", MetaGameClassEnum))
    input_stream.read(8) # Padding?
    BIPED.new_hud_interfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "new hud interfaces"))
    BIPED.dialogue_variants_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "dialogue variants"))
    BIPED.grenade_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "grenade velocity"))
    BIPED.grenade_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade type", GrenadeTypeEnum))
    BIPED.grenade_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade count"))
    input_stream.read(4) # Padding?
    BIPED.powered_seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "powered seats"))
    BIPED.weapons_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapons"))
    BIPED.seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "seats"))
    BIPED.moving_turning_speed = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "moving turning speed"))
    input_stream.read(2) # Padding?
    BIPED.biped_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", BipedFlags))
    BIPED.stationary_turning_threshold = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "stationary turning threshold"))
    input_stream.read(16) # Padding?
    BIPED.biped_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", BipedFunctionEnum))
    BIPED.biped_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", BipedFunctionEnum))
    BIPED.biped_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", BipedFunctionEnum))
    BIPED.biped_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", BipedFunctionEnum))
    BIPED.dont_use = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "dont use"))
    BIPED.bank_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "bank angle"))
    BIPED.bank_apply_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bank apply time"))
    BIPED.bank_decay_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bank decay time"))
    BIPED.pitch_ratio = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "pitch ratio"))
    BIPED.max_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max velocity"))
    BIPED.max_sidestep_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max sidestep velocity"))
    BIPED.acceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration"))
    BIPED.deceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "deceleration"))
    BIPED.angular_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "angular velocity maximum"))
    BIPED.angular_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "angular acceleration maximum"))
    BIPED.crouch_velocity_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "crouch velocity modifier"))
    input_stream.read(8) # Padding?
    BIPED.maximum_slope_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "maximum slope angle"))
    BIPED.downhill_falloff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "downhill falloff angle"))
    BIPED.downhill_cuttoff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "downhill cuttoff angle"))
    BIPED.downhill_velocity_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "downhill velocity scale"))
    BIPED.uphill_falloff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "uphill falloff angle"))
    BIPED.uphill_cuttoff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "uphill cuttoff angle"))
    BIPED.uphill_velocity_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "uphill velocity scale"))
    input_stream.read(24) # Padding?
    BIPED.footsteps = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "footsteps"))
    input_stream.read(24) # Padding?
    BIPED.jump_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "jump velocity"))
    input_stream.read(28) # Padding?
    BIPED.maximum_soft_landing_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum soft landing time"))
    BIPED.maximum_hard_landing_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum hard landing time"))
    BIPED.minimum_soft_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum soft landing velocity"))
    BIPED.minimum_hard_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum hard landing velocity"))
    BIPED.maximum_hard_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum hard landing velocity"))
    BIPED.death_hard_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "death hard landing velocity"))
    input_stream.read(20) # Padding?
    BIPED.standing_camera_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "standing camera height"))
    BIPED.crouching_camera_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "crouching camera height"))
    BIPED.crouch_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "crouch transition time"))
    input_stream.read(24) # Padding?
    BIPED.standing_collision_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "standing collision height"))
    BIPED.crouching_collision_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "crouching collision height"))
    BIPED.collision_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "collision radius"))
    input_stream.read(40) # Padding?
    BIPED.autoaim_width = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "autoaim width"))
    input_stream.read(140) # Padding?
    BIPED.contact_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "contact points"))

    if BIPED.model.name_length > 0:
        BIPED.model.name = TAG.read_variable_string(input_stream, BIPED.model.name_length, TAG)

    if BIPED.animation_graph.name_length > 0:
        BIPED.animation_graph.name = TAG.read_variable_string(input_stream, BIPED.animation_graph.name_length, TAG)

    if BIPED.collision_model.name_length > 0:
        BIPED.collision_model.name = TAG.read_variable_string(input_stream, BIPED.collision_model.name_length, TAG)

    if BIPED.physics.name_length > 0:
        BIPED.physics.name = TAG.read_variable_string(input_stream, BIPED.physics.name_length, TAG)

    if BIPED.modifier_shader.name_length > 0:
        BIPED.modifier_shader.name = TAG.read_variable_string(input_stream, BIPED.modifier_shader.name_length, TAG)

    if BIPED.creation_effect.name_length > 0:
        BIPED.creation_effect.name = TAG.read_variable_string(input_stream, BIPED.creation_effect.name_length, TAG)

    if BIPED.integrated_light_toggle.name_length > 0:
        BIPED.integrated_light_toggle.name = TAG.read_variable_string(input_stream, BIPED.integrated_light_toggle.name_length, TAG)

    if BIPED.spawned_actor.name_length > 0:
        BIPED.spawned_actor.name = TAG.read_variable_string(input_stream, BIPED.spawned_actor.name_length, TAG)

    if BIPED.melee_damage.name_length > 0:
        BIPED.melee_damage.name = TAG.read_variable_string(input_stream, BIPED.melee_damage.name_length, TAG)

    if BIPED.dont_use.name_length > 0:
        BIPED.dont_use.name = TAG.read_variable_string(input_stream, BIPED.dont_use.name_length, TAG)

    if BIPED.footsteps.name_length > 0:
        BIPED.footsteps.name = TAG.read_variable_string(input_stream, BIPED.footsteps.name_length, TAG)

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
        dont_use_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "dont use")
        footsteps_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "footsteps")
        BIPED.model.append_xml_attributes(model_node)
        BIPED.animation_graph.append_xml_attributes(animation_graph_node)
        BIPED.collision_model.append_xml_attributes(collision_model_node)
        BIPED.physics.append_xml_attributes(physics_node)
        BIPED.modifier_shader.append_xml_attributes(modifier_shader_node)
        BIPED.creation_effect.append_xml_attributes(creation_effect_node)
        BIPED.integrated_light_toggle.append_xml_attributes(integrated_light_toggle_node)
        BIPED.spawned_actor.append_xml_attributes(spawned_actor_node)
        BIPED.melee_damage.append_xml_attributes(melee_damage_node)
        BIPED.dont_use.append_xml_attributes(dont_use_node)
        BIPED.footsteps.append_xml_attributes(footsteps_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, BIPED.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return BIPED
