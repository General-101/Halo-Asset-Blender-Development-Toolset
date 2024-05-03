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

    BIPED.biped_body = BIPED.BipedBody()
    input_stream.read(2) # Padding?
    BIPED.biped_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    BIPED.biped_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    BIPED.biped_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    BIPED.biped_body.origin_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "origin offset"))
    BIPED.biped_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    input_stream.read(4) # Padding?
    BIPED.biped_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    BIPED.biped_body.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    input_stream.read(40) # Padding?
    BIPED.biped_body.collision_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision model"))
    BIPED.biped_body.physics = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics"))
    BIPED.biped_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    BIPED.biped_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    input_stream.read(84) # Padding?
    BIPED.biped_body.render_bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "render bounding radius"))
    BIPED.biped_body.object_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ObjectFunctionEnum))
    BIPED.biped_body.object_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ObjectFunctionEnum))
    BIPED.biped_body.object_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ObjectFunctionEnum))
    BIPED.biped_body.object_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ObjectFunctionEnum))
    input_stream.read(44) # Padding?
    BIPED.biped_body.hud_text_message_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    BIPED.biped_body.forced_shader_permutation_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "forced shader_permutation index"))
    BIPED.biped_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    BIPED.biped_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    BIPED.biped_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    BIPED.biped_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    BIPED.biped_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    input_stream.read(2) # Padding?
    BIPED.biped_body.unit_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", UnitFlags))
    BIPED.biped_body.default_team = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "default team", TeamsEnum))
    BIPED.biped_body.constant_sound_volume = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "constant sound volume", ConstantSoundVolumeEnum))
    BIPED.biped_body.rider_damage_fraction = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "rider damage fraction"))
    BIPED.biped_body.integrated_light_toggle = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "integrated light toggle"))
    BIPED.biped_body.unit_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", UnitFunctionEnum))
    BIPED.biped_body.unit_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", UnitFunctionEnum))
    BIPED.biped_body.unit_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", UnitFunctionEnum))
    BIPED.biped_body.unit_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", UnitFunctionEnum))
    BIPED.biped_body.camera_field_of_view = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "camera field of view"))
    BIPED.biped_body.camera_stiffness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera stiffness"))
    BIPED.biped_body.camera_marker_name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(tag_node, "camera marker name"))
    BIPED.biped_body.camera_submerged_marker_name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(tag_node, "camera submerged marker name"))
    BIPED.biped_body.pitch_auto_level = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "pitch auto level"))
    BIPED.biped_body.pitch_range = TAG.read_min_max_degree(input_stream, TAG, tag_format.XMLData(tag_node, "pitch range"))
    BIPED.biped_body.camera_tracks_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "camera tracks"))
    BIPED.biped_body.seat_acceleration_scale = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "seat acceleration scale"))
    input_stream.read(12) # Padding?
    BIPED.biped_body.soft_ping_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "soft ping threshold"))
    BIPED.biped_body.soft_ping_interrupt_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "soft ping interrupt time"))
    BIPED.biped_body.hard_ping_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard ping threshold"))
    BIPED.biped_body.hard_ping_interrupt_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard ping interrupt time"))
    BIPED.biped_body.hard_death_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard death threshold"))
    BIPED.biped_body.feign_death_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death threshold"))
    BIPED.biped_body.feign_death_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death time"))
    BIPED.biped_body.distance_of_evade_anim = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "distance of evade anim"))
    BIPED.biped_body.distance_of_dive_anim = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "distance of dive anim"))
    input_stream.read(4) # Padding?
    BIPED.biped_body.stunned_movement_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "stunned movement threshold"))
    BIPED.biped_body.feign_death_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death chance"))
    BIPED.biped_body.feign_repeat_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign repeat chance"))
    BIPED.biped_body.spawned_actor = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "spawned actor"))
    BIPED.biped_body.spawned_actor_count = TAG.read_min_max_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "spawned actor count"))
    BIPED.biped_body.spawned_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "spawned velocity"))
    BIPED.biped_body.aiming_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming velocity maximum"))
    BIPED.biped_body.aiming_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming acceleration maximum"))
    BIPED.biped_body.casual_aiming_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "casual aiming modifier"))
    BIPED.biped_body.looking_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming acceleration maximum"))
    BIPED.biped_body.looking_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming acceleration maximum"))
    input_stream.read(8) # Padding?
    BIPED.biped_body.ai_vehicle_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai vehicle radius"))
    BIPED.biped_body.ai_danger_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ai danger radius"))
    BIPED.biped_body.melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "melee damage"))
    BIPED.biped_body.motion_sensor_blip_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "motion sensor blip size", MotionSensorBlipSizeEnum))
    input_stream.read(2) # Padding?
    BIPED.biped_body.metagame_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "metagame type", MetaGameTypeEnum))
    BIPED.biped_body.metagame_class = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "metagame class", MetaGameClassEnum))
    input_stream.read(8) # Padding?
    BIPED.biped_body.new_hud_interfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "new hud interfaces"))
    BIPED.biped_body.dialogue_variants_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "dialogue variants"))
    BIPED.biped_body.grenade_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "grenade velocity"))
    BIPED.biped_body.grenade_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade type", GrenadeTypeEnum))
    BIPED.biped_body.grenade_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade count"))
    input_stream.read(4) # Padding?
    BIPED.biped_body.powered_seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "powered seats"))
    BIPED.biped_body.weapons_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapons"))
    BIPED.biped_body.seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "seats"))
    BIPED.biped_body.moving_turning_speed = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "moving turning speed"))
    input_stream.read(2) # Padding?
    BIPED.biped_body.biped_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", BipedFlags))
    BIPED.biped_body.stationary_turning_threshold = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "stationary turning threshold"))
    input_stream.read(16) # Padding?
    BIPED.biped_body.biped_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", BipedFunctionEnum))
    BIPED.biped_body.biped_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", BipedFunctionEnum))
    BIPED.biped_body.biped_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", BipedFunctionEnum))
    BIPED.biped_body.biped_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", BipedFunctionEnum))
    BIPED.biped_body.dont_use = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "dont use"))
    BIPED.biped_body.bank_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "bank angle"))
    BIPED.biped_body.bank_apply_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bank apply time"))
    BIPED.biped_body.bank_decay_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bank decay time"))
    BIPED.biped_body.pitch_ratio = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "pitch ratio"))
    BIPED.biped_body.max_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max velocity"))
    BIPED.biped_body.max_sidestep_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max sidestep velocity"))
    BIPED.biped_body.acceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration"))
    BIPED.biped_body.deceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "deceleration"))
    BIPED.biped_body.angular_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "angular velocity maximum"))
    BIPED.biped_body.angular_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "angular acceleration maximum"))
    BIPED.biped_body.crouch_velocity_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "crouch velocity modifier"))
    input_stream.read(8) # Padding?
    BIPED.biped_body.maximum_slope_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "maximum slope angle"))
    BIPED.biped_body.downhill_falloff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "downhill falloff angle"))
    BIPED.biped_body.downhill_cuttoff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "downhill cuttoff angle"))
    BIPED.biped_body.downhill_velocity_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "downhill velocity scale"))
    BIPED.biped_body.uphill_falloff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "uphill falloff angle"))
    BIPED.biped_body.uphill_cuttoff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "uphill cuttoff angle"))
    BIPED.biped_body.uphill_velocity_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "uphill velocity scale"))
    input_stream.read(24) # Padding?
    BIPED.biped_body.footsteps = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "footsteps"))
    input_stream.read(24) # Padding?
    BIPED.biped_body.jump_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "jump velocity"))
    input_stream.read(28) # Padding?
    BIPED.biped_body.maximum_soft_landing_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum soft landing time"))
    BIPED.biped_body.maximum_hard_landing_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum hard landing time"))
    BIPED.biped_body.minimum_soft_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum soft landing velocity"))
    BIPED.biped_body.minimum_hard_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum hard landing velocity"))
    BIPED.biped_body.maximum_hard_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum hard landing velocity"))
    BIPED.biped_body.death_hard_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "death hard landing velocity"))
    input_stream.read(20) # Padding?
    BIPED.biped_body.standing_camera_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "standing camera height"))
    BIPED.biped_body.crouching_camera_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "crouching camera height"))
    BIPED.biped_body.crouch_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "crouch transition time"))
    input_stream.read(24) # Padding?
    BIPED.biped_body.standing_collision_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "standing collision height"))
    BIPED.biped_body.crouching_collision_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "crouching collision height"))
    BIPED.biped_body.collision_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "collision radius"))
    input_stream.read(40) # Padding?
    BIPED.biped_body.autoaim_width = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "autoaim width"))
    input_stream.read(140) # Padding?
    BIPED.biped_body.contact_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "contact points"))

    if BIPED.biped_body.model.name_length > 0:
        BIPED.biped_body.model.name = TAG.read_variable_string(input_stream, BIPED.biped_body.model.name_length, TAG)

    if BIPED.biped_body.animation_graph.name_length > 0:
        BIPED.biped_body.animation_graph.name = TAG.read_variable_string(input_stream, BIPED.biped_body.animation_graph.name_length, TAG)

    if BIPED.biped_body.collision_model.name_length > 0:
        BIPED.biped_body.collision_model.name = TAG.read_variable_string(input_stream, BIPED.biped_body.collision_model.name_length, TAG)

    if BIPED.biped_body.physics.name_length > 0:
        BIPED.biped_body.physics.name = TAG.read_variable_string(input_stream, BIPED.biped_body.physics.name_length, TAG)

    if BIPED.biped_body.modifier_shader.name_length > 0:
        BIPED.biped_body.modifier_shader.name = TAG.read_variable_string(input_stream, BIPED.biped_body.modifier_shader.name_length, TAG)

    if BIPED.biped_body.creation_effect.name_length > 0:
        BIPED.biped_body.creation_effect.name = TAG.read_variable_string(input_stream, BIPED.biped_body.creation_effect.name_length, TAG)

    if BIPED.biped_body.integrated_light_toggle.name_length > 0:
        BIPED.biped_body.integrated_light_toggle.name = TAG.read_variable_string(input_stream, BIPED.biped_body.integrated_light_toggle.name_length, TAG)

    if BIPED.biped_body.spawned_actor.name_length > 0:
        BIPED.biped_body.spawned_actor.name = TAG.read_variable_string(input_stream, BIPED.biped_body.spawned_actor.name_length, TAG)

    if BIPED.biped_body.melee_damage.name_length > 0:
        BIPED.biped_body.melee_damage.name = TAG.read_variable_string(input_stream, BIPED.biped_body.melee_damage.name_length, TAG)

    if BIPED.biped_body.dont_use.name_length > 0:
        BIPED.biped_body.dont_use.name = TAG.read_variable_string(input_stream, BIPED.biped_body.dont_use.name_length, TAG)

    if BIPED.biped_body.footsteps.name_length > 0:
        BIPED.biped_body.footsteps.name = TAG.read_variable_string(input_stream, BIPED.biped_body.footsteps.name_length, TAG)

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
        BIPED.biped_body.model.append_xml_attributes(model_node)
        BIPED.biped_body.animation_graph.append_xml_attributes(animation_graph_node)
        BIPED.biped_body.collision_model.append_xml_attributes(collision_model_node)
        BIPED.biped_body.physics.append_xml_attributes(physics_node)
        BIPED.biped_body.modifier_shader.append_xml_attributes(modifier_shader_node)
        BIPED.biped_body.creation_effect.append_xml_attributes(creation_effect_node)
        BIPED.biped_body.integrated_light_toggle.append_xml_attributes(integrated_light_toggle_node)
        BIPED.biped_body.spawned_actor.append_xml_attributes(spawned_actor_node)
        BIPED.biped_body.melee_damage.append_xml_attributes(melee_damage_node)
        BIPED.biped_body.dont_use.append_xml_attributes(dont_use_node)
        BIPED.biped_body.footsteps.append_xml_attributes(footsteps_node)

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
