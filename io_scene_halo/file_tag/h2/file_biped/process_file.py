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
    BipedAsset, 
    BipedFlags, 
    LockOnFlags, 
    CollisionFlags
    )

XML_OUTPUT = False

def initilize_biped(BIPED):
    BIPED.ai_properties = []
    BIPED.functions = []
    BIPED.attachments = []
    BIPED.widgets = []
    BIPED.old_functions = []
    BIPED.change_colors = []
    BIPED.predicted_resources = []
    BIPED.camera_tracks = []
    BIPED.postures = []
    BIPED.new_hud_interface = []
    BIPED.dialogue_variants = []
    BIPED.powered_seats = []
    BIPED.weapons = []
    BIPED.seats = []
    BIPED.dead_sphere_shapes = []
    BIPED.pill_shapes = []
    BIPED.sphere_shapes = []
    BIPED.contact_points = []

def read_biped_body(BIPED, TAG, input_stream, tag_node, XML_OUTPUT):
    BIPED.biped_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    BIPED.biped_body = BIPED.BipedBody()
    input_stream.read(2) # Padding?
    BIPED.biped_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    BIPED.biped_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    BIPED.biped_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    BIPED.biped_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    BIPED.biped_body.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    BIPED.biped_body.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(4) # Padding?
    BIPED.biped_body.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    BIPED.biped_body.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    BIPED.biped_body.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    BIPED.biped_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    BIPED.biped_body.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    BIPED.biped_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    BIPED.biped_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    BIPED.biped_body.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    BIPED.biped_body.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    BIPED.biped_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    BIPED.biped_body.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    BIPED.biped_body.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    BIPED.biped_body.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    BIPED.biped_body.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    BIPED.biped_body.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    BIPED.biped_body.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    BIPED.biped_body.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    BIPED.biped_body.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    BIPED.biped_body.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    BIPED.biped_body.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    BIPED.biped_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    BIPED.biped_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    BIPED.biped_body.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    BIPED.biped_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    BIPED.biped_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    BIPED.biped_body.unit_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", UnitFlags))
    BIPED.biped_body.default_team = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "default team", TeamsEnum))
    BIPED.biped_body.constant_sound_volume = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "constant sound volume", ConstantSoundVolumeEnum))
    BIPED.biped_body.integrated_light_toggle = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "integrated light toggle"))
    BIPED.biped_body.camera_field_of_view = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "camera field of view"))
    BIPED.biped_body.camera_stiffness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera stiffness"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    BIPED.biped_body.camera_marker_name_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    BIPED.biped_body.camera_submerged_marker_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    BIPED.biped_body.pitch_auto_level = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "pitch auto level"))
    BIPED.biped_body.pitch_range = TAG.read_min_max_degree(input_stream, TAG, tag_format.XMLData(tag_node, "pitch range"))
    BIPED.biped_body.camera_tracks_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "camera tracks"))
    BIPED.biped_body.acceleration_range = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration range"))
    BIPED.biped_body.acceleration_action_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration action scale"))
    BIPED.biped_body.acceleration_attach_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration attach scale"))
    BIPED.biped_body.soft_ping_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "soft ping threshold"))
    BIPED.biped_body.soft_ping_interrupt_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "soft ping interrupt time"))
    BIPED.biped_body.hard_ping_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard ping threshold"))
    BIPED.biped_body.hard_ping_interrupt_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard ping interrupt time"))
    BIPED.biped_body.hard_death_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard death threshold"))
    BIPED.biped_body.feign_death_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death threshold"))
    BIPED.biped_body.feign_death_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death time"))
    BIPED.biped_body.distance_of_evade_anim = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "distance of evade anim"))
    BIPED.biped_body.distance_of_dive_anim = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "distance of dive anim"))
    BIPED.biped_body.stunned_movement_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "stunned movement threshold"))
    BIPED.biped_body.feign_death_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death chance"))
    BIPED.biped_body.feign_repeat_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign repeat chance"))
    BIPED.biped_body.spawned_turret_actor = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "spawned turret actor"))
    BIPED.biped_body.spawned_actor_count = TAG.read_min_max_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "spawned actor count"))
    BIPED.biped_body.spawned_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "spawned velocity"))
    BIPED.biped_body.aiming_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming velocity maximum"))
    BIPED.biped_body.aiming_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming acceleration maximum"))
    BIPED.biped_body.casual_aiming_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "casual aiming modifier"))
    BIPED.biped_body.looking_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "looking velocity maximum"))
    BIPED.biped_body.looking_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "looking acceleration maximum"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    BIPED.biped_body.right_hand_node_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    BIPED.biped_body.left_hand_node_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    BIPED.biped_body.preferred_gun_node_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    BIPED.biped_body.melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "melee damage"))
    BIPED.biped_body.boarding_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "boarding melee damage"))
    BIPED.biped_body.boarding_melee_response = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "boarding melee response"))
    BIPED.biped_body.landing_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "landing melee damage"))
    BIPED.biped_body.flurry_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "flurry melee damage"))
    BIPED.biped_body.obstacle_smash_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "obstacle smash damage"))
    BIPED.biped_body.motion_sensor_blip_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "motion sensor blip size", MotionSensorBlipSizeEnum))
    BIPED.biped_body.unit_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(tag_node, "type", MetaGameTypeEnum))
    BIPED.biped_body.unit_class = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(tag_node, "class", MetaGameClassEnum))
    BIPED.biped_body.postures_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "postures"))
    BIPED.biped_body.new_hud_interfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "new hud interfaces"))
    BIPED.biped_body.dialogue_variants_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "dialogue variants"))
    BIPED.biped_body.grenade_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "grenade velocity"))
    BIPED.biped_body.grenade_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade type", GrenadeTypeEnum))
    BIPED.biped_body.grenade_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade count"))
    BIPED.biped_body.powered_seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "powered seats"))
    BIPED.biped_body.weapons_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapons"))
    BIPED.biped_body.seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "seats"))
    BIPED.biped_body.boost_peak_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost peak power"))
    BIPED.biped_body.boost_rise_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost rise power"))
    BIPED.biped_body.boost_peak_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost peak time"))
    BIPED.biped_body.boost_fall_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost fall power"))
    BIPED.biped_body.dead_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dead time"))
    BIPED.biped_body.attack_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "attack weight"))
    BIPED.biped_body.decay_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "decay weight"))
    BIPED.biped_body.moving_turning_speed = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "moving turning speed"))
    BIPED.biped_body.biped_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", BipedFlags))
    input_stream.read(2) # Padding?
    BIPED.biped_body.stationary_turning_threshold = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "stationary turning threshold"))
    BIPED.biped_body.jump_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "jump velocity"))
    BIPED.biped_body.maximum_soft_landing_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum soft landing time"))
    BIPED.biped_body.maximum_hard_landing_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum hard landing time"))
    BIPED.biped_body.minimum_soft_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum soft landing velocity"))
    BIPED.biped_body.minimum_hard_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum hard landing velocity"))
    BIPED.biped_body.maximum_hard_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum hard landing velocity"))
    BIPED.biped_body.death_hard_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "death hard landing velocity"))
    BIPED.biped_body.stun_duration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "stun duration"))
    BIPED.biped_body.standing_camera_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "standing camera height"))
    BIPED.biped_body.crouching_camera_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "crouching camera height"))
    BIPED.biped_body.crouching_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "crouching transition time"))
    BIPED.biped_body.camera_interpolation_start = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "camera interpolation start"))
    BIPED.biped_body.camera_interpolation_end = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "camera interpolation end"))
    BIPED.biped_body.camera_forward_movement_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera forward movement scale"))
    BIPED.biped_body.camera_side_movement_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera side movement scale"))
    BIPED.biped_body.camera_vertical_movement_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera vertical movement scale"))
    BIPED.biped_body.camera_exclusion_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera exclusion distance"))
    BIPED.biped_body.autoaim_width = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "autoaim width"))
    BIPED.biped_body.lock_on_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", LockOnFlags))
    input_stream.read(2) # Padding?
    BIPED.biped_body.lock_on_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lock on distance"))
    input_stream.read(16) # Padding?
    BIPED.biped_body.head_shot_acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "head shot acceleration scale"))
    BIPED.biped_body.area_damage_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "area damage effect"))
    BIPED.biped_body.collision_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", CollisionFlags))
    input_stream.read(2) # Padding?
    BIPED.biped_body.height_standing = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "height standing"))
    BIPED.biped_body.height_crouching = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "height crouching"))
    BIPED.biped_body.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "radius"))
    BIPED.biped_body.mass = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "mass"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    BIPED.biped_body.living_material_name_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    BIPED.biped_body.dead_material_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False
    
    input_stream.read(4) # Padding?
    BIPED.biped_body.dead_sphere_shapes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "dead sphere shapes"))
    BIPED.biped_body.pill_shapes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "pill shapes"))
    BIPED.biped_body.sphere_shapes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sphere shapes"))
    BIPED.biped_body.maximum_slope_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "maximum slope angle"))
    BIPED.biped_body.downhill_falloff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "downhill falloff angle"))
    BIPED.biped_body.downhill_cuttoff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "downhill cuttoff angle"))
    BIPED.biped_body.uphill_falloff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "uphill falloff angle"))
    BIPED.biped_body.uphill_cuttoff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "uphill cuttoff angle"))
    BIPED.biped_body.downhill_velocity_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "downhill velocity scale"))
    BIPED.biped_body.uphill_velocity_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "uphill velocity scale"))
    input_stream.read(20) # Padding?
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
    BIPED.biped_body.contact_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "contact points"))
    BIPED.biped_body.reanimation_character = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "reanimation character"))
    BIPED.biped_body.death_spawn_character = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "death spawn character"))
    BIPED.biped_body.death_spawn_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "death spawn count"))
    input_stream.read(2) # Padding?

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    BIPED = BipedAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    BIPED.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_biped(BIPED)
    read_biped_body(BIPED, TAG, input_stream, tag_node, XML_OUTPUT)

    if BIPED.biped_body.default_model_variant_length > 0:
        BIPED.biped_body.default_model_variant = TAG.read_variable_string_no_terminator(input_stream, BIPED.biped_body.default_model_variant_length, TAG, tag_format.XMLData(tag_node, "default model variant"))

    if BIPED.biped_body.model.name_length > 0:
        BIPED.biped_body.model.name = TAG.read_variable_string(input_stream, BIPED.biped_body.model.name_length, TAG)

    if BIPED.biped_body.crate_object.name_length > 0:
        BIPED.biped_body.crate_object.name = TAG.read_variable_string(input_stream, BIPED.biped_body.crate_object.name_length, TAG)

    if BIPED.biped_body.modifier_shader.name_length > 0:
        BIPED.biped_body.modifier_shader.name = TAG.read_variable_string(input_stream, BIPED.biped_body.modifier_shader.name_length, TAG)

    if BIPED.biped_body.creation_effect.name_length > 0:
        BIPED.biped_body.creation_effect.name = TAG.read_variable_string(input_stream, BIPED.biped_body.creation_effect.name_length, TAG)

    if BIPED.biped_body.material_effects.name_length > 0:
        BIPED.biped_body.material_effects.name = TAG.read_variable_string(input_stream, BIPED.biped_body.material_effects.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        crate_object_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "crate object")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        material_effects_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "material effects")
        BIPED.biped_body.model.append_xml_attributes(model_node)
        BIPED.biped_body.crate_object.append_xml_attributes(crate_object_node)
        BIPED.biped_body.modifier_shader.append_xml_attributes(modifier_shader_node)
        BIPED.biped_body.creation_effect.append_xml_attributes(creation_effect_node)
        BIPED.biped_body.material_effects.append_xml_attributes(material_effects_node)

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
