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
from ..file_object.format import ObjectFlags, LightmapShadowModeEnum, SweetenerSizeEnum
from ..file_unit.format import (
    UnitFlags,
    TeamsEnum,
    ConstantSoundVolumeEnum,
    MotionSensorBlipSizeEnum,
    MetaGameTypeEnum,
    MetaGameClassEnum,
    GrenadeTypeEnum
    )
from .format import (
    VehicleAsset,
    VehicleFlags,
    VehicleTypeEnum,
    VehicleControlEnum,
    SpecificTypeEnum,
    PlayerTrainingVehicleTypeEnum,
    VehicleSizeEnum,
    PhysicsFlags
    )

XML_OUTPUT = False

def initilize_vehicle(VEHICLE):
    VEHICLE.ai_properties = []
    VEHICLE.functions = []
    VEHICLE.attachments = []
    VEHICLE.widgets = []
    VEHICLE.old_functions = []
    VEHICLE.change_colors = []
    VEHICLE.predicted_resources = []
    VEHICLE.camera_tracks = []
    VEHICLE.postures = []
    VEHICLE.new_hud_interface = []
    VEHICLE.dialogue_variants = []
    VEHICLE.powered_seats = []
    VEHICLE.weapons = []
    VEHICLE.seats = []
    VEHICLE.gears = []
    VEHICLE.anti_gravity_point = []
    VEHICLE.friction_points = []
    VEHICLE.phantom_shapes = []

def read_vehicle_body(VEHICLE, TAG, input_stream, tag_node, XML_OUTPUT):
    VEHICLE.body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    input_stream.read(2) # Padding?
    VEHICLE.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    VEHICLE.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    VEHICLE.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    VEHICLE.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    VEHICLE.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    VEHICLE.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(4) # Padding?
    VEHICLE.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    VEHICLE.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    VEHICLE.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    VEHICLE.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    VEHICLE.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    VEHICLE.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    VEHICLE.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    VEHICLE.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    VEHICLE.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    VEHICLE.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    VEHICLE.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    VEHICLE.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    VEHICLE.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    VEHICLE.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    VEHICLE.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    VEHICLE.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    VEHICLE.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    VEHICLE.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    VEHICLE.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    VEHICLE.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    VEHICLE.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    VEHICLE.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    VEHICLE.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    VEHICLE.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    VEHICLE.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    VEHICLE.unit_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", UnitFlags))
    VEHICLE.default_team = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "default team", TeamsEnum))
    VEHICLE.constant_sound_volume = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "constant sound volume", ConstantSoundVolumeEnum))
    VEHICLE.integrated_light_toggle = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "integrated light toggle"))
    VEHICLE.camera_field_of_view = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "camera field of view"))
    VEHICLE.camera_stiffness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera stiffness"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    VEHICLE.camera_marker_name_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    VEHICLE.camera_submerged_marker_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    VEHICLE.pitch_auto_level = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "pitch auto level"))
    VEHICLE.pitch_range = TAG.read_min_max_degree(input_stream, TAG, tag_format.XMLData(tag_node, "pitch range"))
    VEHICLE.camera_tracks_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "camera tracks"))
    VEHICLE.acceleration_range = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration range"))
    VEHICLE.acceleration_action_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration action scale"))
    VEHICLE.acceleration_attach_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration attach scale"))
    VEHICLE.soft_ping_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "soft ping threshold"))
    VEHICLE.soft_ping_interrupt_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "soft ping interrupt time"))
    VEHICLE.hard_ping_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard ping threshold"))
    VEHICLE.hard_ping_interrupt_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard ping interrupt time"))
    VEHICLE.hard_death_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard death threshold"))
    VEHICLE.feign_death_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death threshold"))
    VEHICLE.feign_death_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death time"))
    VEHICLE.distance_of_evade_anim = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "distance of evade anim"))
    VEHICLE.distance_of_dive_anim = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "distance of dive anim"))
    VEHICLE.stunned_movement_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "stunned movement threshold"))
    VEHICLE.feign_death_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death chance"))
    VEHICLE.feign_repeat_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign repeat chance"))
    VEHICLE.spawned_turret_actor = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "spawned turret actor"))
    VEHICLE.spawned_actor_count = TAG.read_min_max_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "spawned actor count"))
    VEHICLE.spawned_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "spawned velocity"))
    VEHICLE.aiming_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming velocity maximum"))
    VEHICLE.aiming_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming acceleration maximum"))
    VEHICLE.casual_aiming_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "casual aiming modifier"))
    VEHICLE.looking_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "looking velocity maximum"))
    VEHICLE.looking_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "looking acceleration maximum"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    VEHICLE.right_hand_node_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    VEHICLE.left_hand_node_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    VEHICLE.preferred_gun_node_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    VEHICLE.melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "melee damage"))
    VEHICLE.boarding_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "boarding melee damage"))
    VEHICLE.boarding_melee_response = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "boarding melee response"))
    VEHICLE.landing_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "landing melee damage"))
    VEHICLE.flurry_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "flurry melee damage"))
    VEHICLE.obstacle_smash_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "obstacle smash damage"))
    VEHICLE.motion_sensor_blip_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "motion sensor blip size", MotionSensorBlipSizeEnum))
    VEHICLE.unit_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(tag_node, "type", MetaGameTypeEnum))
    VEHICLE.unit_class = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(tag_node, "class", MetaGameClassEnum))
    VEHICLE.postures_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "postures"))
    VEHICLE.new_hud_interfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "new hud interfaces"))
    VEHICLE.dialogue_variants_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "dialogue variants"))
    VEHICLE.grenade_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "grenade velocity"))
    VEHICLE.grenade_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade type", GrenadeTypeEnum))
    VEHICLE.grenade_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade count"))
    VEHICLE.powered_seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "powered seats"))
    VEHICLE.weapons_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapons"))
    VEHICLE.seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "seats"))
    VEHICLE.boost_peak_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost peak power"))
    VEHICLE.boost_rise_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost rise power"))
    VEHICLE.boost_peak_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost peak time"))
    VEHICLE.boost_fall_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost fall power"))
    VEHICLE.dead_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dead time"))
    VEHICLE.attack_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "attack weight"))
    VEHICLE.decay_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "decay weight"))

    VEHICLE.vehicle_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", VehicleFlags))
    input_stream.read(2) # Padding?
    VEHICLE.vehicle_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", VehicleTypeEnum))
    VEHICLE.vehicle_control = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "control", VehicleControlEnum))
    VEHICLE.maximum_forward_speed = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum forward speed"))
    VEHICLE.maximum_reverse_speed = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum reverse speed"))
    VEHICLE.speed_acceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "speed acceleration"))
    VEHICLE.speed_deceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "speed deceleration"))
    VEHICLE.maximum_left_turn = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum left turn"))
    VEHICLE.maximum_right_turn = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum right turn"))
    VEHICLE.wheel_circumference = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "wheel circumference"))
    VEHICLE.turn_rate = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "turn rate"))
    VEHICLE.blur_speed = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "blur speed"))
    VEHICLE.specific_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "specific type", SpecificTypeEnum))
    VEHICLE.player_training_vehicle_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "player training vehicle type", PlayerTrainingVehicleTypeEnum))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    VEHICLE.flip_message_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    VEHICLE.turn_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "turn scale"))
    VEHICLE.speed_turn_penalty_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "speed turn penalty power"))
    VEHICLE.speed_turn_penalty = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "speed turn penalty"))
    VEHICLE.maximum_left_slide = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum left slide"))
    VEHICLE.maximum_right_slide = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum right slide"))
    VEHICLE.slide_acceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "slide acceleration"))
    VEHICLE.slide_deceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "slide deceleration"))
    VEHICLE.minimum_flipping_angular_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum flipping angular velocity"))
    VEHICLE.maximum_flipping_angular_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum flipping angular velocity"))
    VEHICLE.vehicle_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "vehicle size", VehicleSizeEnum))
    input_stream.read(2) # Padding?
    VEHICLE.fixed_gun_yaw = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "fixed gun yaw"))
    VEHICLE.fixed_gun_pitch = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "fixed gun pitch"))
    VEHICLE.overdampen_cusp_angle = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "overdampen cusp angle"))
    VEHICLE.overdampen_exponent = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "overdampen exponent"))
    VEHICLE.crouch_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "crouch transition time"))
    input_stream.read(4) # Padding?
    VEHICLE.engine_moment = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "engine moment"))
    VEHICLE.engine_max_angular_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "engine max angular velocity"))
    VEHICLE.gears_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "gears"))
    VEHICLE.flying_torque_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "flying torque scale"))
    VEHICLE.seat_enterance_acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "seat enterance acceleration scale"))
    VEHICLE.seat_exit_acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "seat exit acceleration scale"))
    VEHICLE.air_friction_deceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "air friction deceleration"))
    VEHICLE.thrust_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "thrust scale"))
    VEHICLE.suspension_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "suspension sound"))
    VEHICLE.crash_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crash sound"))
    VEHICLE.unused = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused"))
    VEHICLE.special_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "special effect"))
    VEHICLE.unused_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused effect"))
    VEHICLE.physics_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", PhysicsFlags))
    input_stream.read(2) # Padding?
    VEHICLE.ground_fricton = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground fricton"))
    VEHICLE.ground_depth = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground depth"))
    VEHICLE.ground_damp_factor = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground damp factor"))
    VEHICLE.ground_moving_friction = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground moving friction"))
    VEHICLE.ground_maximum_slope_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground maximum slope 0"))
    VEHICLE.ground_maximum_slope_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground maximum slope 1"))
    input_stream.read(16) # Padding?
    VEHICLE.anti_gravity_bank_lift = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "anti gravity bank lift"))
    VEHICLE.steering_bank_reaction_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "steering bank reaction scale"))
    VEHICLE.gravity_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "gravity scale"))
    VEHICLE.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "radius"))
    VEHICLE.anti_gravity_point_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "anti gravity point"))
    VEHICLE.friction_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "friction points"))
    VEHICLE.phantom_shapes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "phantom shapes"))

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    VEHICLE = VehicleAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    VEHICLE.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_vehicle(VEHICLE)
    read_vehicle_body(VEHICLE, TAG, input_stream, tag_node, XML_OUTPUT)

    if VEHICLE.default_model_variant_length > 0:
        VEHICLE.default_model_variant = TAG.read_variable_string_no_terminator(input_stream, VEHICLE.default_model_variant_length, TAG, tag_format.XMLData(tag_node, "default model variant"))

    if VEHICLE.model.name_length > 0:
        VEHICLE.model.name = TAG.read_variable_string(input_stream, VEHICLE.model.name_length, TAG)

    if VEHICLE.crate_object.name_length > 0:
        VEHICLE.crate_object.name = TAG.read_variable_string(input_stream, VEHICLE.crate_object.name_length, TAG)

    if VEHICLE.modifier_shader.name_length > 0:
        VEHICLE.modifier_shader.name = TAG.read_variable_string(input_stream, VEHICLE.modifier_shader.name_length, TAG)

    if VEHICLE.creation_effect.name_length > 0:
        VEHICLE.creation_effect.name = TAG.read_variable_string(input_stream, VEHICLE.creation_effect.name_length, TAG)

    if VEHICLE.material_effects.name_length > 0:
        VEHICLE.material_effects.name = TAG.read_variable_string(input_stream, VEHICLE.material_effects.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        crate_object_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "crate object")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        material_effects_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "material effects")
        VEHICLE.model.append_xml_attributes(model_node)
        VEHICLE.crate_object.append_xml_attributes(crate_object_node)
        VEHICLE.modifier_shader.append_xml_attributes(modifier_shader_node)
        VEHICLE.creation_effect.append_xml_attributes(creation_effect_node)
        VEHICLE.material_effects.append_xml_attributes(material_effects_node)

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
