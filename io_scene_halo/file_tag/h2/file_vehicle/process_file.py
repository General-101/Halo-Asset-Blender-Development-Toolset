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
    VehicleAsset, 
    ObjectFlags, 
    LightmapShadowModeEnum, 
    SweetenerSizeEnum, 
    UnitFlags, 
    TeamsEnum, 
    ConstantSoundVolumeEnum, 
    MotionSensorBlipSizeEnum, 
    MetaGameTypeEnum, 
    MetaGameClassEnum, 
    GrenadeTypeEnum, 
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
    VEHICLE.vehicle_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    VEHICLE.vehicle_body = VEHICLE.VehicleBody()
    input_stream.read(2) # Padding?
    VEHICLE.vehicle_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    VEHICLE.vehicle_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    VEHICLE.vehicle_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    VEHICLE.vehicle_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    VEHICLE.vehicle_body.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    VEHICLE.vehicle_body.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(4) # Padding?
    VEHICLE.vehicle_body.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    VEHICLE.vehicle_body.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    VEHICLE.vehicle_body.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    VEHICLE.vehicle_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    VEHICLE.vehicle_body.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    VEHICLE.vehicle_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    VEHICLE.vehicle_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    VEHICLE.vehicle_body.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    VEHICLE.vehicle_body.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    VEHICLE.vehicle_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    VEHICLE.vehicle_body.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    VEHICLE.vehicle_body.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    VEHICLE.vehicle_body.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    VEHICLE.vehicle_body.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    VEHICLE.vehicle_body.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    VEHICLE.vehicle_body.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    VEHICLE.vehicle_body.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    VEHICLE.vehicle_body.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    VEHICLE.vehicle_body.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    VEHICLE.vehicle_body.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    VEHICLE.vehicle_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    VEHICLE.vehicle_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    VEHICLE.vehicle_body.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    VEHICLE.vehicle_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    VEHICLE.vehicle_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    VEHICLE.vehicle_body.unit_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", UnitFlags))
    VEHICLE.vehicle_body.default_team = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "default team", TeamsEnum))
    VEHICLE.vehicle_body.constant_sound_volume = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "constant sound volume", ConstantSoundVolumeEnum))
    VEHICLE.vehicle_body.integrated_light_toggle = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "integrated light toggle"))
    VEHICLE.vehicle_body.camera_field_of_view = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "camera field of view"))
    VEHICLE.vehicle_body.camera_stiffness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera stiffness"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    VEHICLE.vehicle_body.camera_marker_name_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    VEHICLE.vehicle_body.camera_submerged_marker_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    VEHICLE.vehicle_body.pitch_auto_level = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "pitch auto level"))
    VEHICLE.vehicle_body.pitch_range = TAG.read_min_max_degree(input_stream, TAG, tag_format.XMLData(tag_node, "pitch range"))
    VEHICLE.vehicle_body.camera_tracks_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "camera tracks"))
    VEHICLE.vehicle_body.acceleration_range = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration range"))
    VEHICLE.vehicle_body.acceleration_action_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration action scale"))
    VEHICLE.vehicle_body.acceleration_attach_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration attach scale"))
    VEHICLE.vehicle_body.soft_ping_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "soft ping threshold"))
    VEHICLE.vehicle_body.soft_ping_interrupt_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "soft ping interrupt time"))
    VEHICLE.vehicle_body.hard_ping_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard ping threshold"))
    VEHICLE.vehicle_body.hard_ping_interrupt_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard ping interrupt time"))
    VEHICLE.vehicle_body.hard_death_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard death threshold"))
    VEHICLE.vehicle_body.feign_death_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death threshold"))
    VEHICLE.vehicle_body.feign_death_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death time"))
    VEHICLE.vehicle_body.distance_of_evade_anim = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "distance of evade anim"))
    VEHICLE.vehicle_body.distance_of_dive_anim = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "distance of dive anim"))
    VEHICLE.vehicle_body.stunned_movement_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "stunned movement threshold"))
    VEHICLE.vehicle_body.feign_death_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death chance"))
    VEHICLE.vehicle_body.feign_repeat_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign repeat chance"))
    VEHICLE.vehicle_body.spawned_turret_actor = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "spawned turret actor"))
    VEHICLE.vehicle_body.spawned_actor_count = TAG.read_min_max_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "spawned actor count"))
    VEHICLE.vehicle_body.spawned_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "spawned velocity"))
    VEHICLE.vehicle_body.aiming_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming velocity maximum"))
    VEHICLE.vehicle_body.aiming_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming acceleration maximum"))
    VEHICLE.vehicle_body.casual_aiming_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "casual aiming modifier"))
    VEHICLE.vehicle_body.looking_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "looking velocity maximum"))
    VEHICLE.vehicle_body.looking_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "looking acceleration maximum"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    VEHICLE.vehicle_body.right_hand_node_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    VEHICLE.vehicle_body.left_hand_node_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    VEHICLE.vehicle_body.preferred_gun_node_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    VEHICLE.vehicle_body.melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "melee damage"))
    VEHICLE.vehicle_body.boarding_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "boarding melee damage"))
    VEHICLE.vehicle_body.boarding_melee_response = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "boarding melee response"))
    VEHICLE.vehicle_body.landing_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "landing melee damage"))
    VEHICLE.vehicle_body.flurry_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "flurry melee damage"))
    VEHICLE.vehicle_body.obstacle_smash_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "obstacle smash damage"))
    VEHICLE.vehicle_body.motion_sensor_blip_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "motion sensor blip size", MotionSensorBlipSizeEnum))
    VEHICLE.vehicle_body.unit_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(tag_node, "type", MetaGameTypeEnum))
    VEHICLE.vehicle_body.unit_class = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(tag_node, "class", MetaGameClassEnum))
    VEHICLE.vehicle_body.postures_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "postures"))
    VEHICLE.vehicle_body.new_hud_interfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "new hud interfaces"))
    VEHICLE.vehicle_body.dialogue_variants_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "dialogue variants"))
    VEHICLE.vehicle_body.grenade_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "grenade velocity"))
    VEHICLE.vehicle_body.grenade_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade type", GrenadeTypeEnum))
    VEHICLE.vehicle_body.grenade_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade count"))
    VEHICLE.vehicle_body.powered_seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "powered seats"))
    VEHICLE.vehicle_body.weapons_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapons"))
    VEHICLE.vehicle_body.seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "seats"))
    VEHICLE.vehicle_body.boost_peak_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost peak power"))
    VEHICLE.vehicle_body.boost_rise_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost rise power"))
    VEHICLE.vehicle_body.boost_peak_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost peak time"))
    VEHICLE.vehicle_body.boost_fall_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost fall power"))
    VEHICLE.vehicle_body.dead_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dead time"))
    VEHICLE.vehicle_body.attack_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "attack weight"))
    VEHICLE.vehicle_body.decay_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "decay weight"))

    VEHICLE.vehicle_body.vehicle_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", VehicleFlags))
    input_stream.read(2) # Padding?
    VEHICLE.vehicle_body.vehicle_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", VehicleTypeEnum))
    VEHICLE.vehicle_body.vehicle_control = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "control", VehicleControlEnum))
    VEHICLE.vehicle_body.maximum_forward_speed = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum forward speed"))
    VEHICLE.vehicle_body.maximum_reverse_speed = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum reverse speed"))
    VEHICLE.vehicle_body.speed_acceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "speed acceleration"))
    VEHICLE.vehicle_body.speed_deceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "speed deceleration"))
    VEHICLE.vehicle_body.maximum_left_turn = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum left turn"))
    VEHICLE.vehicle_body.maximum_right_turn = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum right turn"))
    VEHICLE.vehicle_body.wheel_circumference = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "wheel circumference"))
    VEHICLE.vehicle_body.turn_rate = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "turn rate"))
    VEHICLE.vehicle_body.blur_speed = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "blur speed"))
    VEHICLE.vehicle_body.specific_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "specific type", SpecificTypeEnum))
    VEHICLE.vehicle_body.player_training_vehicle_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "player training vehicle type", PlayerTrainingVehicleTypeEnum))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    VEHICLE.vehicle_body.flip_message_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    VEHICLE.vehicle_body.turn_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "turn scale"))
    VEHICLE.vehicle_body.speed_turn_penalty_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "speed turn penalty power"))
    VEHICLE.vehicle_body.speed_turn_penalty = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "speed turn penalty"))
    VEHICLE.vehicle_body.maximum_left_slide = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum left slide"))
    VEHICLE.vehicle_body.maximum_right_slide = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum right slide"))
    VEHICLE.vehicle_body.slide_acceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "slide acceleration"))
    VEHICLE.vehicle_body.slide_deceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "slide deceleration"))
    VEHICLE.vehicle_body.minimum_flipping_angular_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum flipping angular velocity"))
    VEHICLE.vehicle_body.maximum_flipping_angular_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum flipping angular velocity"))
    VEHICLE.vehicle_body.vehicle_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "vehicle size", VehicleSizeEnum))
    input_stream.read(2) # Padding?
    VEHICLE.vehicle_body.fixed_gun_yaw = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "fixed gun yaw"))
    VEHICLE.vehicle_body.fixed_gun_pitch = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "fixed gun pitch"))
    VEHICLE.vehicle_body.overdampen_cusp_angle = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "overdampen cusp angle"))
    VEHICLE.vehicle_body.overdampen_exponent = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "overdampen exponent"))
    VEHICLE.vehicle_body.crouch_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "crouch transition time"))
    input_stream.read(4) # Padding?
    VEHICLE.vehicle_body.engine_moment = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "engine moment"))
    VEHICLE.vehicle_body.engine_max_angular_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "engine max angular velocity"))
    VEHICLE.vehicle_body.gears_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "gears"))
    VEHICLE.vehicle_body.flying_torque_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "flying torque scale"))
    VEHICLE.vehicle_body.seat_enterance_acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "seat enterance acceleration scale"))
    VEHICLE.vehicle_body.seat_exit_acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "seat exit acceleration scale"))
    VEHICLE.vehicle_body.air_friction_deceleration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "air friction deceleration"))
    VEHICLE.vehicle_body.thrust_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "thrust scale"))
    VEHICLE.vehicle_body.suspension_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "suspension sound"))
    VEHICLE.vehicle_body.crash_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crash sound"))
    VEHICLE.vehicle_body.unused = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused"))
    VEHICLE.vehicle_body.special_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "special effect"))
    VEHICLE.vehicle_body.unused_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused effect"))
    VEHICLE.vehicle_body.physics_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", PhysicsFlags))
    input_stream.read(2) # Padding?
    VEHICLE.vehicle_body.ground_fricton = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground fricton"))
    VEHICLE.vehicle_body.ground_depth = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground depth"))
    VEHICLE.vehicle_body.ground_damp_factor = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground damp factor"))
    VEHICLE.vehicle_body.ground_moving_friction = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground moving friction"))
    VEHICLE.vehicle_body.ground_maximum_slope_0 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground maximum slope 0"))
    VEHICLE.vehicle_body.ground_maximum_slope_1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ground maximum slope 1"))
    input_stream.read(16) # Padding?
    VEHICLE.vehicle_body.anti_gravity_bank_lift = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "anti gravity bank lift"))
    VEHICLE.vehicle_body.steering_bank_reaction_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "steering bank reaction scale"))
    VEHICLE.vehicle_body.gravity_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "gravity scale"))
    VEHICLE.vehicle_body.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "radius"))
    VEHICLE.vehicle_body.anti_gravity_point_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "anti gravity point"))
    VEHICLE.vehicle_body.friction_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "friction points"))
    VEHICLE.vehicle_body.phantom_shapes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "phantom shapes"))

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

    if VEHICLE.vehicle_body.default_model_variant_length > 0:
        VEHICLE.vehicle_body.default_model_variant = TAG.read_variable_string_no_terminator(input_stream, VEHICLE.vehicle_body.default_model_variant_length, TAG, tag_format.XMLData(tag_node, "default model variant"))

    if VEHICLE.vehicle_body.model.name_length > 0:
        VEHICLE.vehicle_body.model.name = TAG.read_variable_string(input_stream, VEHICLE.vehicle_body.model.name_length, TAG)

    if VEHICLE.vehicle_body.crate_object.name_length > 0:
        VEHICLE.vehicle_body.crate_object.name = TAG.read_variable_string(input_stream, VEHICLE.vehicle_body.crate_object.name_length, TAG)

    if VEHICLE.vehicle_body.modifier_shader.name_length > 0:
        VEHICLE.vehicle_body.modifier_shader.name = TAG.read_variable_string(input_stream, VEHICLE.vehicle_body.modifier_shader.name_length, TAG)

    if VEHICLE.vehicle_body.creation_effect.name_length > 0:
        VEHICLE.vehicle_body.creation_effect.name = TAG.read_variable_string(input_stream, VEHICLE.vehicle_body.creation_effect.name_length, TAG)

    if VEHICLE.vehicle_body.material_effects.name_length > 0:
        VEHICLE.vehicle_body.material_effects.name = TAG.read_variable_string(input_stream, VEHICLE.vehicle_body.material_effects.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        crate_object_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "crate object")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        material_effects_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "material effects")
        VEHICLE.vehicle_body.model.append_xml_attributes(model_node)
        VEHICLE.vehicle_body.crate_object.append_xml_attributes(crate_object_node)
        VEHICLE.vehicle_body.modifier_shader.append_xml_attributes(modifier_shader_node)
        VEHICLE.vehicle_body.creation_effect.append_xml_attributes(creation_effect_node)
        VEHICLE.vehicle_body.material_effects.append_xml_attributes(material_effects_node)

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
