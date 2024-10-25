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
    BIPED.body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    input_stream.read(2) # Padding?
    BIPED.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    BIPED.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    BIPED.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    BIPED.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    BIPED.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    BIPED.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(4) # Padding?
    BIPED.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    BIPED.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    BIPED.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    BIPED.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    BIPED.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    BIPED.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    BIPED.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    BIPED.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    BIPED.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    BIPED.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    BIPED.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    BIPED.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    BIPED.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    BIPED.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    BIPED.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    BIPED.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    BIPED.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    BIPED.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    BIPED.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    BIPED.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    BIPED.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    BIPED.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    BIPED.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    BIPED.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    BIPED.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    BIPED.unit_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", UnitFlags))
    BIPED.default_team = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "default team", TeamsEnum))
    BIPED.constant_sound_volume = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "constant sound volume", ConstantSoundVolumeEnum))
    BIPED.integrated_light_toggle = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "integrated light toggle"))
    BIPED.camera_field_of_view = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "camera field of view"))
    BIPED.camera_stiffness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera stiffness"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    BIPED.camera_marker_name_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    BIPED.camera_submerged_marker_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    BIPED.pitch_auto_level = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "pitch auto level"))
    BIPED.pitch_range = TAG.read_min_max_degree(input_stream, TAG, tag_format.XMLData(tag_node, "pitch range"))
    BIPED.camera_tracks_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "camera tracks"))
    BIPED.acceleration_range = TAG.read_vector(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration range"))
    BIPED.acceleration_action_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration action scale"))
    BIPED.acceleration_attach_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration attach scale"))
    BIPED.soft_ping_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "soft ping threshold"))
    BIPED.soft_ping_interrupt_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "soft ping interrupt time"))
    BIPED.hard_ping_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard ping threshold"))
    BIPED.hard_ping_interrupt_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard ping interrupt time"))
    BIPED.hard_death_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "hard death threshold"))
    BIPED.feign_death_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death threshold"))
    BIPED.feign_death_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death time"))
    BIPED.distance_of_evade_anim = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "distance of evade anim"))
    BIPED.distance_of_dive_anim = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "distance of dive anim"))
    BIPED.stunned_movement_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "stunned movement threshold"))
    BIPED.feign_death_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign death chance"))
    BIPED.feign_repeat_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "feign repeat chance"))
    BIPED.spawned_turret_actor = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "spawned turret actor"))
    BIPED.spawned_actor_count = TAG.read_min_max_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "spawned actor count"))
    BIPED.spawned_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "spawned velocity"))
    BIPED.aiming_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming velocity maximum"))
    BIPED.aiming_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "aiming acceleration maximum"))
    BIPED.casual_aiming_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "casual aiming modifier"))
    BIPED.looking_velocity_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "looking velocity maximum"))
    BIPED.looking_acceleration_maximum = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "looking acceleration maximum"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    BIPED.right_hand_node_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    BIPED.left_hand_node_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    BIPED.preferred_gun_node_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    BIPED.melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "melee damage"))
    BIPED.boarding_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "boarding melee damage"))
    BIPED.boarding_melee_response = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "boarding melee response"))
    BIPED.landing_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "landing melee damage"))
    BIPED.flurry_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "flurry melee damage"))
    BIPED.obstacle_smash_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "obstacle smash damage"))
    BIPED.motion_sensor_blip_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "motion sensor blip size", MotionSensorBlipSizeEnum))
    BIPED.unit_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(tag_node, "type", MetaGameTypeEnum))
    BIPED.unit_class = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(tag_node, "class", MetaGameClassEnum))
    BIPED.postures_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "postures"))
    BIPED.new_hud_interfaces_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "new hud interfaces"))
    BIPED.dialogue_variants_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "dialogue variants"))
    BIPED.grenade_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "grenade velocity"))
    BIPED.grenade_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade type", GrenadeTypeEnum))
    BIPED.grenade_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade count"))
    BIPED.powered_seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "powered seats"))
    BIPED.weapons_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapons"))
    BIPED.seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "seats"))
    BIPED.boost_peak_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost peak power"))
    BIPED.boost_rise_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost rise power"))
    BIPED.boost_peak_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost peak time"))
    BIPED.boost_fall_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "boost fall power"))
    BIPED.dead_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dead time"))
    BIPED.attack_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "attack weight"))
    BIPED.decay_weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "decay weight"))
    BIPED.moving_turning_speed = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "moving turning speed"))
    BIPED.biped_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", BipedFlags))
    input_stream.read(2) # Padding?
    BIPED.stationary_turning_threshold = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "stationary turning threshold"))
    BIPED.jump_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "jump velocity"))
    BIPED.maximum_soft_landing_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum soft landing time"))
    BIPED.maximum_hard_landing_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum hard landing time"))
    BIPED.minimum_soft_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum soft landing velocity"))
    BIPED.minimum_hard_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum hard landing velocity"))
    BIPED.maximum_hard_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum hard landing velocity"))
    BIPED.death_hard_landing_velocity = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "death hard landing velocity"))
    BIPED.stun_duration = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "stun duration"))
    BIPED.standing_camera_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "standing camera height"))
    BIPED.crouching_camera_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "crouching camera height"))
    BIPED.crouching_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "crouching transition time"))
    BIPED.camera_interpolation_start = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "camera interpolation start"))
    BIPED.camera_interpolation_end = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "camera interpolation end"))
    BIPED.camera_forward_movement_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera forward movement scale"))
    BIPED.camera_side_movement_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera side movement scale"))
    BIPED.camera_vertical_movement_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera vertical movement scale"))
    BIPED.camera_exclusion_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "camera exclusion distance"))
    BIPED.autoaim_width = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "autoaim width"))
    BIPED.lock_on_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", LockOnFlags))
    input_stream.read(2) # Padding?
    BIPED.lock_on_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "lock on distance"))
    input_stream.read(16) # Padding?
    BIPED.head_shot_acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "head shot acceleration scale"))
    BIPED.area_damage_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "area damage effect"))
    BIPED.collision_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", CollisionFlags))
    input_stream.read(2) # Padding?
    BIPED.height_standing = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "height standing"))
    BIPED.height_crouching = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "height crouching"))
    BIPED.radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "radius"))
    BIPED.mass = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "mass"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    BIPED.living_material_name_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    BIPED.dead_material_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    input_stream.read(4) # Padding?
    BIPED.dead_sphere_shapes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "dead sphere shapes"))
    BIPED.pill_shapes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "pill shapes"))
    BIPED.sphere_shapes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sphere shapes"))
    BIPED.maximum_slope_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "maximum slope angle"))
    BIPED.downhill_falloff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "downhill falloff angle"))
    BIPED.downhill_cuttoff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "downhill cuttoff angle"))
    BIPED.uphill_falloff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "uphill falloff angle"))
    BIPED.uphill_cuttoff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "uphill cuttoff angle"))
    BIPED.downhill_velocity_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "downhill velocity scale"))
    BIPED.uphill_velocity_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "uphill velocity scale"))
    input_stream.read(20) # Padding?
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
    BIPED.contact_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "contact points"))
    BIPED.reanimation_character = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "reanimation character"))
    BIPED.death_spawn_character = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "death spawn character"))
    BIPED.death_spawn_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "death spawn count"))
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

    if BIPED.default_model_variant_length > 0:
        BIPED.default_model_variant = TAG.read_variable_string_no_terminator(input_stream, BIPED.default_model_variant_length, TAG, tag_format.XMLData(tag_node, "default model variant"))

    if BIPED.model.name_length > 0:
        BIPED.model.name = TAG.read_variable_string(input_stream, BIPED.model.name_length, TAG)

    if BIPED.crate_object.name_length > 0:
        BIPED.crate_object.name = TAG.read_variable_string(input_stream, BIPED.crate_object.name_length, TAG)

    if BIPED.modifier_shader.name_length > 0:
        BIPED.modifier_shader.name = TAG.read_variable_string(input_stream, BIPED.modifier_shader.name_length, TAG)

    if BIPED.creation_effect.name_length > 0:
        BIPED.creation_effect.name = TAG.read_variable_string(input_stream, BIPED.creation_effect.name_length, TAG)

    if BIPED.material_effects.name_length > 0:
        BIPED.material_effects.name = TAG.read_variable_string(input_stream, BIPED.material_effects.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        crate_object_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "crate object")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        material_effects_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "material effects")
        BIPED.model.append_xml_attributes(model_node)
        BIPED.crate_object.append_xml_attributes(crate_object_node)
        BIPED.modifier_shader.append_xml_attributes(modifier_shader_node)
        BIPED.creation_effect.append_xml_attributes(creation_effect_node)
        BIPED.material_effects.append_xml_attributes(material_effects_node)

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
