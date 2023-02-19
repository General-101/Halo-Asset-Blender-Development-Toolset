# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Crisp
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

import uuid
import random

from .nwo_utils import(
    CheckType,
    not_bungie_game,
    mesh_type,
    marker_type,
    object_type,
    color_3p_str,
    color_4p_str,
    bool_str,
    jstr,
    vector_str,
    radius_str,
    true_bsp,
    true_region,
    clean_tag_path,
    shortest_string,

    frame_prefixes,
    marker_prefixes,
    poop_render_only_prefixes,
    object_prefix,
)

# OBJECT LEVEL
class NWOObject:
    def __init__(self, ob, sidecar_type, model_armature, world_frame, asset_name):
        # Set variables passed to this class
        self.ob = ob
        self.name = ob.name
        self.halo = ob.nwo
        self.sidecar_type = sidecar_type
        self.not_bungie_game = not_bungie_game()
        self.model_armature = model_armature
        self.world_frame = world_frame
        self.asset_name = asset_name
        self.bungie_object_type = self.object_type()
        self.bungie_object_ID = self.object_ID()
        self.halo_export = '1'
        if self.bungie_object_type == '_connected_geometry_object_type_frame':
            self.bungie_object_animates = self.object_animates()

    def cleanup(self):
        del self.ob
        del self.name
        del self.halo
        del self.sidecar_type
        del self.not_bungie_game
        del self.model_armature
        del self.world_frame
        del self.asset_name

    def object_type(self):
            if self.animation_control():
                return '_connected_geometry_object_type_animation_control'
            elif self.animation_event():
                return '_connected_geometry_object_type_animation_event'
            elif self.animation_camera():
                return '_connected_geometry_object_type_animation_camera'
            elif self.light():
                return '_connected_geometry_object_type_light'
            elif self.frame_pca():
                return '_connected_geometry_object_type_frame_pca'
            elif self.frame():
                return '_connected_geometry_object_type_frame'
            elif self.marker():
                return '_connected_geometry_object_type_marker'
            else:
                return '_connected_geometry_object_type_mesh'
        
    def object_ID(self):
        # Generate a seeded GUID based off object name. This way objects can retain their IDs and as blender objects must be unique, a unique ID is guaranteed.
        rnd = random.Random()
        rnd.seed(self.name)
        obj_id = str(uuid.UUID(int=rnd.getrandbits(128)))

        return obj_id

    def object_animates(self):
        return bool_str(self.sidecar_type == 'MODEL')

    def frame_pca(self):
        return self.halo.is_pca and not_bungie_game() and self.frame()

    def frame(self):
        return object_type(self.ob, ('_connected_geometry_object_type_frame'), (frame_prefixes)) and not self.ob.type == 'LIGHT'

    def marker(self):
        return object_type(self.ob, ('_connected_geometry_object_type_marker'), (marker_prefixes)) or (self.ob.type == 'EMPTY' and self.name.startswith('$'))

    def mesh(self):
        return self.ob.type == 'MESH' and self.ob.nwo.Object_Type_All in '_connected_geometry_object_type_mesh' and not object_prefix(self.ob, ((frame_prefixes + marker_prefixes)))

    def light(self):
        return self.ob.type == 'LIGHT'

    def animation_camera(self):
        return self.ob.type == 'CAMERA'

    def animation_control(self):
        return False # temporary until a system for setting these is created

    def animation_event(self):
        return False # temporary until a system for setting these is created

# ANIMATION CONTROL
#####################
class NWOAnimationControl(NWOObject):
    def __init__(self, ob, sidecar_type, model_armature, world_frame, asset_name):
        super().__init__(ob, sidecar_type, model_armature, world_frame, asset_name)
        self.bungie_animation_control_type = None
        self.bungie_animation_control_id = None
        self.bungie_animation_control_ik_chain = None
        self.bungie_animation_control_ik_effect = None
        self.bungie_animation_control_constraint_effect = None
        self.bungie_animation_control_proxy_target_marker = None
        self.bungie_animation_control_proxy_target_tag = None
        self.bungie_animation_control_proxy_target_usage = None

        self.cleanup()

# ANIMATION EVENT
#####################
class NWOAnimationEvent(NWOObject):
    def __init__(self, ob, sidecar_type, model_armature, world_frame, asset_name):
        super().__init__(ob, sidecar_type, model_armature, world_frame, asset_name)
        self.bungie_animation_event_type = None
        self.bungie_animation_event_start = None
        self.bungie_animation_event_end = None
        self.bungie_animation_event_id = None
        self.bungie_animation_event_wrinkle_map_face_region = None
        self.bungie_animation_event_wrinkle_map_effect = None
        self.bungie_animation_event_footstep_type = None
        self.bungie_animation_event_footstep_effect = None
        self.bungie_animation_event_ik_chain = None
        self.bungie_animation_event_ik_active_tag = None
        self.bungie_animation_event_ik_target_tag = None
        self.bungie_animation_event_ik_target_marker = None
        self.bungie_animation_event_ik_target_usage = None
        self.bungie_animation_event_ik_proxy_target_id = None
        self.bungie_animation_event_ik_pole_vector_id = None
        self.bungie_animation_event_ik_effector_id = None
        self.bungie_animation_event_cinematic_effect_tag = None
        self.bungie_animation_event_cinematic_effect_effect = None
        self.bungie_animation_event_cinematic_effect_marker = None
        self.bungie_animation_event_object_function_name = None
        self.bungie_animation_event_object_function_effect = None
        self.bungie_animation_event_frame_frame = None
        self.bungie_animation_event_frame_name = None
        self.bungie_animation_event_frame_trigger = None
        self.bungie_animation_event_import_frame = None
        self.bungie_animation_event_import_name = None
        self.bungie_animation_event_text = None

        self.cleanup()


# ANIMATION CAMERA
#####################

class NWOAnimationCamera(NWOObject):
    def __init__(self, ob, sidecar_type, model_armature, world_frame, asset_name):
        super().__init__(ob, sidecar_type, model_armature, world_frame, asset_name)

        self.cleanup()

# LIGHT
#####################
class NWOLight(NWOObject):
    def __init__(self, ob, sidecar_type, model_armature, world_frame, asset_name):
        super().__init__(ob, sidecar_type, model_armature, world_frame, asset_name)
        # SHARED
        self.bungie_light_type =  self.light_type()
        self.bungie_light_color = self.light_color()
        self.bungie_light_intensity = self.light_intensity()

        if self.not_bungie_game:
            # H4 ONLY
            self.bungie_light_mode = self.light_mode()
            self.bungie_lighting_mode = self.lighting_mode()
            self.bungie_light_near_attenuation_start = self.light_near_attenuation_start()
            self.bungie_light_near_attenuation_end = self.light_near_attenuation_end()
            self.bungie_light_fade_start_distance = self.light_fade_start_distance()
            self.bungie_light_fade_out_distance = self.light_fade_out_distance()
            self.bungie_light_far_attenuation_start = self.light_far_attenuation_start()
            self.bungie_light_far_attenuation_end = self.light_far_attenuation_end()
            # self.bungie_light_is_uber_light = self.is_uber_light()
            # self.bungie_light_indirect_only = self.light_indirect_only()
            # self.bungie_light_attenuation_near_radius = self.light_attenuation_near_radius()
            # self.bungie_light_attenuation_far_radius = self.light_attenuation_far_radius()
            # self.bungie_light_attenuation_power = self.light_attenuation_power()
            self.bungie_inner_cone_angle = self.inner_cone_angle()
            self.bungie_outer_cone_angle = self.outer_cone_angle()
            self.bungie_cone_projection_shape = self.cone_projection_shape()
            self.bungie_screenspace_light = self.screenspace_light()
            self.bungie_shadow_near_clipplane = self.shadow_near_clipplane()
            self.bungie_shadow_far_clipplane = self.shadow_far_clipplane()
            self.bungie_shadow_bias_offset = self.shadow_bias_offset()
            self.bungie_shadow_color = self.shadow_color()
            self.bungie_dynamic_shadow_quality = self.dynamic_shadow_quality()
            self.bungie_shadows = self.shadows()
            self.bungie_ignore_dynamic_objects = self.ignore_dynamic_objects()
            self.bungie_cinema_objects_only = self.cinema_objects_only()
            self.bungie_cinema_only = self.cinema_only()
            self.bungie_cinema_exclude = self.cinema_exclude()
            self.bungie_specular_contribution = self.specular_contribution()
            self.bungie_diffuse_contribution = self.diffuse_contribution()
            self.bungie_destroy_light_after = self.destroy_light_after()
            self.bungie_specular_power = self.specular_power()
            self.bungie_specular_intensity = self.specular_intensity()
            self.bungie_indirect_amplification_factor = self.indirect_amplification_factor()
            self.bungie_light_jitter_quality = self.light_jitter_quality()
            self.bungie_light_jitter_sphere_radius = self.light_jitter_sphere_radius()
            self.bungie_light_jitter_angle = self.light_jitter_angle()
            self.bungie_is_sun = self.is_sun()
            self.bungie_is_indirect_only = self.is_indirect_only()
            self.bungie_is_static_analytic = self.is_static_analytic()
                # self.bungie_light_indirect_amplification_factor = self.light_indirect_amplification_factor()
            
            # self.bungie_light_tag_name = self.light_tag_name()
        else:
            # REACH ONLY
            self.bungie_light_type_version = '1'
            self.bungie_light_game_type = self.light_game_type()
            self.bungie_light_shape = self.light_shape()
            self.bungie_light_near_attenuation_start = self.light_near_attenuation_start()
            self.bungie_light_near_attenuation_end = self.light_near_attenuation_end()
            self.bungie_light_fade_start_distance = self.light_fade_start_distance()
            self.bungie_light_fade_out_distance = self.light_fade_out_distance()
            self.bungie_light_far_attenuation_start = self.light_far_attenuation_start()
            self.bungie_light_far_attenuation_end = self.light_far_attenuation_end()
            # self.bungie_light_use_near_attenuation = self.light_use_near_attenuation()
            # self.bungie_light_use_far_attenuation = self.light_use_far_attenuation()
            self.bungie_light_ignore_bsp_visibility = self.light_ignore_bsp_visibility()
            # self.bungie_light_clipping_size_x_pos = None # not setting these currently
            # self.bungie_light_clipping_size_y_pos = None
            # self.bungie_light_clipping_size_z_pos = None
            # self.bungie_light_clipping_size_x_neg = None
            # self.bungie_light_clipping_size_y_neg = None
            # self.bungie_light_clipping_size_z_neg = None
            # self.bungie_light_use_clipping = None
            self.bungie_light_hotspot_size = self.light_hotspot_size()
            self.bungie_light_hotspot_falloff = self.light_hotspot_falloff()
            self.bungie_light_aspect = self.light_aspect()
            self.bungie_light_falloff_shape = self.light_falloff_shape()
            self.bungie_light_frustum_width = self.light_frustum_width()
            self.bungie_light_frustum_height = self.light_frustum_height()
            self.bungie_light_bounce_light_ratio = self.light_bounce_light_ratio()
            self.bungie_light_dynamic_light_has_bounce = self.light_dynamic_light_has_bounce()
            # self.bungie_light_screenspace_light_has_specular = self.light_screenspace_light_has_specular()
            self.bungie_light_light_tag_override = self.light_light_tag_override()
            self.bungie_light_shader_reference = self.light_shader_reference()
            self.bungie_light_gel_reference = self.light_gel_reference()
            self.bungie_light_lens_flare_reference = self.light_lens_flare_reference()
            self.bungie_light_volume_distance = self.light_volume_distance()
            self.bungie_light_volume_intensity_scalar = self.light_volume_intensity_scala()

        self.cleanup()

# --------------------------------

    def light_type(self):
        if self.not_bungie_game:
            if self.halo.light_type_h4 == '_connected_geometry_light_type_sun':
                return '_connected_geometry_light_type_directional'
            else:
                return self.halo.light_type_h4
        else:
            return self.halo.light_type_override
            
    def is_uber_light(self):
        return bool_str(self.halo.light_sub_type == '_connected_geometry_lighting_sub_type_uber')

    def light_fade_start_distance(self):
        return jstr(self.halo.Light_Fade_Start_Distance)

    def light_fade_out_distance(self):
        return jstr(self.halo.Light_Fade_End_Distance)

    def light_color(self):
        if self.not_bungie_game:
            return color_3p_str(self.halo.Light_Color)
        else:
            return color_4p_str(self.halo.Light_Color)

    def light_intensity(self):
        if self.not_bungie_game:
            return jstr(self.halo.Light_IntensityH4)
        else:
            return jstr(self.halo.Light_Intensity)

    def light_far_attenuation_start(self):
        if self.not_bungie_game:
            return jstr(self.halo.Light_Far_Attenuation_StartH4)
        else:
            return jstr(self.halo.Light_Far_Attenuation_Start)

    def light_far_attenuation_end(self):
        if self.not_bungie_game:
            return jstr(self.halo.Light_Far_Attenuation_EndH4)
        else:
            return jstr(self.halo.Light_Far_Attenuation_End)

    def light_near_attenuation_start(self):
        if self.not_bungie_game:
            return jstr(self.halo.Light_Near_Attenuation_StartH4)
        else:
            return jstr(self.halo.Light_Near_Attenuation_Start)

    def light_near_attenuation_end(self):
        if self.not_bungie_game:
            return jstr(self.halo.Light_Near_Attenuation_EndH4)
        else:
            return jstr(self.halo.Light_Near_Attenuation_End)

    def light_mode(self):
        return self.halo.light_mode

    def light_jitter_quality(self):
        return self.halo.light_jitter_quality

    def light_jitter_sphere_radius(self):
        return jstr(self.halo.light_jitter_sphere_radius)

    def light_jitter_angle(self):
        return jstr(self.halo.light_jitter_angle)

    def light_indirect_only(self):
        return bool_str(self.halo.light_indirect_only)

    def light_indirect_amplification_factor(self):
        return jstr(self.halo.light_amplification_factor)

    def light_attenuation_near_radius(self):
        return jstr(self.halo.light_attenuation_near_radius)

    def light_attenuation_far_radius(self):
        return jstr(self.halo.light_attenuation_far_radius)

    def light_attenuation_power(self):
        return jstr(self.halo.light_attenuation_power)

    def lighting_mode(self):
        return self.halo.light_lighting_mode

    def specular_power(self):
        return jstr(self.halo.light_specular_power)

    def specular_intensity(self):
        return jstr(self.halo.light_specular_intensity)

    def inner_cone_angle(self):
        return jstr(self.halo.light_inner_cone_angle)

    def outer_cone_angle(self):
        return jstr(self.halo.light_outer_cone_angle)

    def outer_cone_angle(self):
        return jstr(self.halo.light_outer_cone_angle)

    def cone_projection_shape(self):
        return self.halo.light_cone_projection_shape

    def cone_projection_shape(self):
        return self.halo.light_cone_projection_shape

    def shadow_near_clipplane(self):
        return jstr(self.halo.light_shadow_near_clipplane)

    def shadow_far_clipplane(self):
        return jstr(self.halo.light_shadow_far_clipplane)

    def shadow_bias_offset(self):
        return jstr(self.halo.light_shadow_bias_offset)

    def shadow_color(self):
        return color_3p_str(self.halo.light_shadow_color)

    def dynamic_shadow_quality(self):
        return self.halo.light_dynamic_shadow_quality

    def shadows(self):
        return bool_str(self.halo.light_shadows)

    def screenspace_light(self):
        return bool_str(self.halo.light_sub_type == '_connected_geometry_lighting_sub_type_screenspace')

    def ignore_dynamic_objects(self):
        return bool_str(self.halo.light_ignore_dynamic_objects)

    def cinema_objects_only(self):
        return bool_str(self.halo.light_cinema_objects_only) # NEED TO ADD TO UI

    def cinema_only(self):
        return bool_str(self.halo.light_cinema == '_connected_geometry_lighting_cinema_only')

    def cinema_exclude(self):
        return bool_str(self.halo.light_cinema == '_connected_geometry_lighting_cinema_exclude')

    def specular_contribution(self):
        return bool_str(self.halo.light_specular_contribution)

    def diffuse_contribution(self):
        return bool_str(self.halo.light_diffuse_contribution)

    def destroy_light_after(self):
        return jstr(self.halo.light_destroy_after)

    def indirect_amplification_factor(self):
        return jstr(self.halo.light_amplification_factor)

    def is_sun(self):
        return bool_str(self.halo.light_type_h4 == '_connected_geometry_light_type_sun')

    def is_indirect_only(self):
        return bool_str(self.halo.light_indirect_only)

    def is_static_analytic(self):
        return bool_str(self.halo.light_static_analytic)

    def light_tag_name(self):
        return clean_tag_path(self.halo.light_tag_name)

    def light_game_type(self):
        return self.halo.Light_Game_Type

    def light_shape(self):
        return self.halo.Light_Shape

    def light_ignore_bsp_visibility(self):
        return bool_str(self.halo.Light_Ignore_BSP_Visibility)

    def light_hotspot_size(self):
        return jstr(self.halo.Light_Hotspot_Size)

    def light_hotspot_falloff(self):
        return jstr(self.halo.Light_Hotspot_Falloff)

    def light_aspect(self):
        return jstr(self.halo.Light_Aspect)

    def light_falloff_shape(self):
        return jstr(self.halo.Light_Falloff_Shape)

    def light_frustum_width(self):
        return jstr(self.halo.Light_Frustum_Width)

    def light_frustum_height(self):
        return jstr(self.halo.Light_Frustum_Height)

    def light_bounce_light_ratio(self):
        return jstr(self.halo.Light_Bounce_Ratio)

    def light_dynamic_light_has_bounce(self):
        return bool_str(self.halo.Light_Dynamic_Has_Bounce)

    def light_dynamic_light_has_bounce(self):
        return bool_str(self.halo.Light_Screenspace_Has_Specular)

    def light_light_tag_override(self):
        return clean_tag_path(self.halo.Light_Tag_Override)

    def light_shader_reference(self):
        return clean_tag_path(self.halo.Light_Shader_Reference)

    def light_gel_reference(self):
        return clean_tag_path(self.halo.Light_Gel_Reference)

    def light_lens_flare_reference(self):
        return clean_tag_path(self.halo.Light_Lens_Flare_Reference, 'lens_flare')

    def light_volume_distance(self):
        return jstr(self.halo.Light_Volume_Distance)

    def light_volume_intensity_scala(self):
        return jstr(self.halo.Light_Volume_Intensity)

# --------------------------------


# FRAME PCA
#####################
class NWOFramePCA(NWOObject):
    def __init__(self, ob, sidecar_type, model_armature, world_frame, asset_name):
        super().__init__(ob, sidecar_type, model_armature, world_frame, asset_name)
        self.bungie_mesh_ispca =  self.mesh_ispca()
        
        self.cleanup()

    def mesh_ispca(self):
        return bool_str(self.ob.type == 'MESH')

# FRAME
#####################
class NWOFrame(NWOObject):
    def __init__(self, ob, sidecar_type, model_armature, world_frame, asset_name):
        super().__init__(ob, sidecar_type, model_armature, world_frame, asset_name)
        self.bungie_frame_ID1 = self.frame_ID1()
        self.bungie_frame_ID2 = self.frame_ID2()

        if self.not_bungie_game:
            self.bungie_frame_world = self.frame_world()

        self.cleanup()

    def frame_ID1(self):
        return '8078'


    def frame_ID2(self):
        return '378163771'

    def frame_world(self):
        if self.ob == self.model_armature or self.ob == self.world_frame:
            return '1'
        else:
            return '0'


# MARKER
#####################
class NWOMarker(NWOObject):
    def __init__(self, ob, sidecar_type, model_armature, world_frame, asset_name):
        super().__init__(ob, sidecar_type, model_armature, world_frame, asset_name)
        # SHARED
        self.bungie_marker_type = self.marker_type()
        if self.sidecar_type in ('MODEL', 'SKY'):
            self.bungie_marker_all_regions = self.marker_all_regions()
            self.bungie_marker_region = self.marker_region()
        if self.bungie_marker_type in ('_connected_geometry_marker_type_model', '_connected_geometry_marker_type_hint', '_connected_geometry_marker_type_target'):
            self.bungie_marker_model_group = self.marker_model_group()
            if self.bungie_marker_type == '_connected_geometry_marker_type_model' and vector_str(self.halo.Marker_Velocity) != "0.0 0.0 0.0":
                self.bungie_marker_velocity = self.marker_velocity()
        elif self.bungie_marker_type in ('_connected_geometry_marker_type_prefab', '_connected_geometry_marker_type_cheap_light', '_connected_geometry_marker_type_light', '_connected_geometry_marker_type_falling_leaf', '_connected_geometry_marker_type_game_instance'):
            self.bungie_marker_game_instance_tag_name = self.marker_game_instance_tag_name()
            self.bungie_marker_game_instance_variant_name = self.marker_game_instance_variant_name()
        elif self.bungie_marker_type == '_connected_geometry_marker_type_pathfinding_sphere':
            self.bungie_marker_pathfinding_sphere_vehicle_only = self.marker_pathfinding_sphere_vehicle_only()
            self.bungie_marker_pathfinding_sphere_remains_when_open = self.marker_pathfinding_sphere_remains_when_open()
            self.bungie_marker_pathfinding_sphere_with_sectors = self.marker_pathfinding_sphere_with_sectors()
        elif self.bungie_marker_type in ('_connected_geometry_marker_type_physics_hinge_constraint', '_connected_geometry_marker_type_physics_socket_constraint'):
            self.bungie_physics_constraint_parent = self.physics_constraint_parent()
            self.bungie_physics_constraint_child = self.physics_constraint_child()
            self.bungie_physics_constraint_use_limits = self.physics_constraint_use_limits()
            if self.bungie_physics_constraint_use_limits == '1':
                if self.bungie_marker_type == '_connected_geometry_marker_type_physics_hinge_constraint':
                    self.bungie_physics_constraint_hinge_min = self.physics_constraint_hinge_min()
                    self.bungie_physics_constraint_hinge_max = self.physics_constraint_hinge_max()
                elif self.bungie_marker_type == '_connected_geometry_marker_type_physics_socket_constraint':
                    self.bungie_physics_constraint_cone_angle = self.physics_constraint_cone_angle()
                    self.bungie_physics_constraint_plane_min = self.physics_constraint_plane_min()
                    self.bungie_physics_constraint_plane_max = self.physics_constraint_plane_max()
                    self.bungie_physics_constraint_twist_start = self.physics_constraint_twist_start()
                    self.bungie_physics_constraint_twist_end = self.physics_constraint_twist_end()
        # H4
        if self.not_bungie_game:
            if self.bungie_marker_type in ('_connected_geometry_marker_type_cheap_light', '_connected_geometry_marker_type_light', '_connected_geometry_marker_type_falling_leaf', '_connected_geometry_marker_type_game_instance'):
                self.bungie_marker_always_run_scripts = self.marker_always_run_scripts()
                if self.bungie_marker_type == '_connected_geometry_marker_type_cheap_light':
                    self.bungie_marker_cheap_light_tag_name = self.marker_cheap_light_tag_name()
                elif self.bungie_marker_type == '_connected_geometry_marker_type_light':
                    self.bungie_marker_light_tag_name = self.marker_light_tag_name()
                elif self.bungie_marker_type == '_connected_geometry_marker_type_falling_leaf':
                    self.bungie_marker_falling_leaf_tag_name = self.marker_falling_leaf_tag_name()
            elif self.bungie_marker_type == '_connected_geometry_marker_type_hint':
                self.bungie_marker_hint_length = self.marker_hint_length()
            elif self.bungie_marker_type == '_connected_geometry_marker_type_envfx':
                self.bungie_marker_looping_effect = self.marker_looping_effect()
            elif self.bungie_marker_type == '_connected_geometry_marker_type_airprobe':
                self.bungie_marker_airprobe = self.marker_airprobe()
            elif self.bungie_marker_type == '_connected_geometry_marker_type_lightCone':
                self.bungie_marker_light_tag = self.marker_light_tag()
                self.bungie_marker_light_color = self.marker_light_color()
                self.bungie_marker_light_cone_width = self.marker_light_cone_width()
                self.bungie_marker_light_cone_length = self.marker_light_cone_length()
                self.bungie_marker_light_color_alpha = self.marker_light_color_alpha()
                self.bungie_marker_light_cone_intensity = self.marker_light_cone_intensity()
                self.bungie_marker_light_cone_curve = self.marker_light_cone_curve()

        self.cleanup()

    def marker_type(self):
            if self.model():
                return '_connected_geometry_marker_type_model'
            elif self.effects():
                return '_connected_geometry_marker_type_effects'
            elif self.prefab():
                return '_connected_geometry_marker_type_prefab'
            elif self.cheap_light():
                return '_connected_geometry_marker_type_cheap_light'
            elif self.marker_light():
                return '_connected_geometry_marker_type_light'
            elif self.falling_leaf():
                return '_connected_geometry_marker_type_falling_leaf'
            elif self.game_instance():
                return '_connected_geometry_marker_type_game_instance'
            elif self.garbage():
                return '_connected_geometry_marker_type_garbage'
            elif self.hint():
                return '_connected_geometry_marker_type_hint'
            elif self.pathfinding_sphere():
                return '_connected_geometry_marker_type_pathfinding_sphere'
            elif self.physics_constraint():
                if self.halo.Physics_Constraint_Type == '_connected_geometry_marker_type_physics_hinge_constraint':
                    return '_connected_geometry_marker_type_physics_hinge_constraint'
                else:
                    return '_connected_geometry_marker_type_physics_socket_constraint'
            elif self.target():
                return '_connected_geometry_marker_type_target'
            elif self.water_volume_flow():
                return '_connected_geometry_marker_type_water_volume_flow'
            elif self.airprobe():
                return '_connected_geometry_marker_type_airprobe'
            elif self.envfx():
                return '_connected_geometry_marker_type_envfx'
            else:
                return '_connected_geometry_marker_type_lightCone'

    def marker_model_group(self):
        return self.halo.Marker_Group_Name

    def marker_all_regions(self):
        return bool_str(self.halo.Marker_All_Regions)

    def marker_region(self): 
        return true_region(self.halo).lower()

    def marker_game_instance_tag_name(self):
        return clean_tag_path(self.halo.Marker_Game_Instance_Tag_Name)

    def marker_game_instance_variant_name(self):
        return clean_tag_path(self.halo.Marker_Game_Instance_Tag_Variant_Name)

    def marker_velocity(self):
        return vector_str(self.halo.Marker_Velocity)

    def marker_pathfinding_sphere_vehicle_only(self):
        return bool_str(self.halo.Marker_Pathfinding_Sphere_Vehicle)

    def marker_pathfinding_sphere_remains_when_open(self):
        return bool_str(self.halo.Pathfinding_Sphere_Remains_When_Open)

    def marker_pathfinding_sphere_with_sectors(self):
        return bool_str(self.halo.Pathfinding_Sphere_With_Sectors)

    def physics_constraint_parent(self):
        return self.halo.Physics_Constraint_Parent

    def physics_constraint_child(self):
        return self.halo.Physics_Constraint_Child

    def physics_constraint_use_limits(self):
        return bool_str(self.halo.Physics_Constraint_Uses_Limits) 

    def physics_constraint_hinge_min(self):
        return jstr(self.halo.Hinge_Constraint_Minimum)

    def physics_constraint_hinge_max(self):
        return jstr(self.halo.Hinge_Constraint_Maximum)

    def physics_constraint_cone_angle(self):
        return jstr(self.halo.Cone_Angle)

    def physics_constraint_plane_min(self):
        return jstr(self.halo.Plane_Constraint_Minimum)

    def physics_constraint_plane_max(self):
        return jstr(self.halo.Plane_Constraint_Maximum)

    def physics_constraint_twist_start(self):
        return jstr(self.halo.Twist_Constraint_Start)

    def physics_constraint_twist_end(self):
        return jstr(self.halo.Twist_Constraint_End)

    def marker_always_run_scripts(self):
        return bool_str(self.halo.marker_game_instance_run_scripts)

    def marker_cheap_light_tag_name(self):
        return clean_tag_path(self.halo.Marker_Game_Instance_Tag_Name, 'cheap_light')

    def marker_light_tag_name(self):
        return clean_tag_path(self.halo.Marker_Game_Instance_Tag_Name, 'light')

    def marker_falling_leaf_tag_name(self):
        return clean_tag_path(self.halo.Marker_Game_Instance_Tag_Name)

    def marker_hint_length(self):
        return jstr(self.halo.marker_hint_length)

    def marker_looping_effect(self):
        return clean_tag_path(self.halo.marker_looping_effect, 'effect')

    def marker_airprobe(self):
        return self.halo.Marker_Group_Name

    def marker_light_tag(self):
        return clean_tag_path(self.halo.marker_light_cone_tag, 'light')

    def marker_light_color(self):
        return color_3p_str(self.halo.marker_light_cone_color)

    def marker_light_cone_width(self):
        return jstr(self.halo.marker_light_cone_width)

    def marker_light_cone_length(self):
        return jstr(self.halo.marker_light_cone_length)

    def marker_light_color_alpha(self):
        return jstr(self.halo.marker_light_cone_alpha)

    def marker_light_cone_intensity(self):
        return jstr(self.halo.marker_light_cone_intensity)     

    def marker_light_cone_curve(self):
        return clean_tag_path(self.halo.marker_light_cone_curve, 'curve_scalar')

    def model(self):
        return marker_type(self.ob, ('_connected_geometry_marker_type_model'))

    def effects(self):
        return marker_type(self.ob, ('_connected_geometry_marker_type_effects'))

    def game_instance(self):
        return marker_type(self.ob, ('_connected_geometry_marker_type_game_instance'), ('?'))

    def garbage(self):
        return marker_type(self.ob, ('_connected_geometry_marker_type_garbage'))

    def hint(self):
        return marker_type(self.ob, ('_connected_geometry_marker_type_hint'))

    def pathfinding_sphere(self):
        return marker_type(self.ob, ('_connected_geometry_marker_type_pathfinding_sphere'))

    def physics_constraint(self):
        return marker_type(self.ob, ('_connected_geometry_marker_type_physics_constraint'), ('$'))

    def target(self):
        return marker_type(self.ob, ('_connected_geometry_marker_type_target'))

    def water_volume_flow(self):
        return marker_type(self.ob, ('_connected_geometry_marker_type_water_volume_flow'))

    def airprobe(self): # H4+ ONLY
        return marker_type(self.ob, ('_connected_geometry_marker_type_airprobe'))

    def envfx(self): # H4+ ONLY
        return marker_type(self.ob, ('_connected_geometry_marker_type_envfx'))

    def lightCone(self): # H4+ ONLY
        return marker_type(self.ob, ('_connected_geometry_marker_type_lightCone'))

    def prefab(self): # H4+ ONLY
        return self.game_instance() and self.not_bungie_game and self.halo.Marker_Game_Instance_Tag_Name.lower().endswith('.prefab')

    def cheap_light(self): # H4+ ONLY
        return self.game_instance() and self.not_bungie_game and self.halo.Marker_Game_Instance_Tag_Name.lower().endswith('.cheap_light')

    def marker_light(self): # H4+ ONLY
        return self.game_instance() and self.not_bungie_game and self.halo.Marker_Game_Instance_Tag_Name.lower().endswith('.light')

    def falling_leaf(self):  # H4+ ONLY
        return self.game_instance() and self.not_bungie_game and self.halo.Marker_Game_Instance_Tag_Name.lower().endswith('.leaf')
        
# MESH
#####################
class NWOMesh(NWOObject):
    def __init__(self, ob, sidecar_type, model_armature, world_frame, asset_name):
        super().__init__(ob, sidecar_type, model_armature, world_frame, asset_name)
        # SHARED
        self.bungie_mesh_type = self.mesh_type()
        if self.sidecar_type in ('MODEL', 'SKY') and self.bungie_mesh_type in ('_connected_geometry_mesh_type_render', '_connected_geometry_mesh_type_physics', '_connected_geometry_mesh_type_collision', '_connected_geometry_mesh_type_default',):
            self.bungie_face_region = self.face_region()
        # PROPS FOR MESH TYPES WHICH HAVE RENDERED FACES
        if self.bungie_mesh_type in ('_connected_geometry_mesh_type_structure', '_connected_geometry_mesh_type_render', '_connected_geometry_mesh_type_default', '_connected_geometry_mesh_type_poop', '_connected_geometry_mesh_type_decorator', '_connected_geometry_mesh_type_object_instance', '_connected_geometry_mesh_type_water_surface'):
            self.bungie_face_type = self.face_type()
            self.bungie_face_mode = self.face_mode()
            self.bungie_face_sides = self.face_sides()
            self.bungie_face_draw_distance = self.face_draw_distance()
            self.bungie_texcoord_usage = self.texcoord_usage()
            self.bungie_conveyor = self.conveyor()
            self.bungie_ladder = self.ladder()
            self.bungie_slip_surface = self.slip_surface()
            self.bungie_decal_offset = self.decal_offset()
            self.bungie_group_transparents_by_plane = self.group_transparents_by_plane()
            self.bungie_no_shadow = self.no_shadow()
            self.bungie_precise_position = self.precise_position()
            self.bungie_mesh_tessellation_density = self.mesh_tessellation_density()
            self.bungie_mesh_additional_compression = self.mesh_additional_compression()
            if self.not_bungie_game:
                self.bungie_invisible_to_pvs = self.invisible_to_pvs()
                self.bungie_no_lightmap = self.no_lightmap()
                self.bungie_uvmirror_across_entire_model = self.uvmirror_across_entire_model()
                
            if self.bungie_face_type == '_connected_geometry_face_type_sky':
                self.bungie_sky_permutation_index = self.sky_permutation_index()

            if self.bungie_mesh_type in ('_connected_geometry_mesh_type_structure', '_connected_geometry_mesh_type_render', '_connected_geometry_mesh_type_default', '_connected_geometry_mesh_type_poop'):
                self.bungie_mesh_use_uncompressed_verts = self.mesh_use_uncompressed_verts()
        
        # SPECIFIC MESH TYPE PROPS
        if self.bungie_mesh_type == '_connected_geometry_mesh_type_boundary_surface':
            self.bungie_mesh_boundary_surface_type = self.mesh_boundary_surface_type()
            self.bungie_mesh_boundary_surface_name = self.mesh_boundary_surface_name()

        elif self.bungie_mesh_type in ('_connected_geometry_mesh_type_poop_collision',  '_connected_geometry_mesh_type_poop'):
            if self.not_bungie_game:
                self.bungie_mesh_poop_collision_type = self.mesh_poop_collision_type()
                self.bungie_mesh_poop_collision_override_global_material = self.mesh_poop_collision_override_global_material()
                if self.bungie_mesh_poop_collision_override_global_material == '1':
                    self.bungie_mesh_global_material = self.mesh_global_material()
            if self.bungie_mesh_type == '_connected_geometry_mesh_type_poop':
                self.bungie_mesh_poop_lighting = self.mesh_poop_lighting()
                self.bungie_mesh_poop_lightmap_resolution_scale = self.mesh_poop_lightmap_resolution_scale()
                self.bungie_mesh_poop_pathfinding = self.mesh_poop_pathfinding()
                self.bungie_mesh_poop_imposter_policy = self.mesh_poop_imposter_policy()
                self.bungie_mesh_poop_imposter_transition_distance = self.mesh_poop_imposter_brightness()
                # self.bungie_mesh_poop_fade_range_start = self.mesh_poop_fade_range_start()
                # self.bungie_mesh_poop_fade_range_end = self.mesh_poop_fade_range_end()
                # This needs to be Reach only otherwise tool complains. However, the flag is still in use in the UI as it is instead used to set instanced collision type to none
                if not self.not_bungie_game:
                    self.bungie_mesh_poop_is_render_only = self.mesh_poop_is_render_only()

                self.bungie_mesh_poop_chops_portals = self.mesh_poop_chops_portals()
                self.bungie_mesh_poop_does_not_block_aoe = self.mesh_poop_does_not_block_aoe()
                self.bungie_mesh_poop_excluded_from_lightprobe = self.mesh_poop_excluded_from_lightprobe()
                self.bungie_mesh_poop_decal_spacing = self.mesh_poop_decal_spacing()
                self.bungie_mesh_poop_precise_geometry = self.mesh_poop_precise_geometry()
                # self.bungie_mesh_poop_predominant_shader_name = self.mesh_poop_predominant_shader_name()
                # self.bungie_mesh_poop_light_channel_flags = self.mesh_poop_light_channel_flags()
                # H4 only
                if self.not_bungie_game:
                    self.bungie_mesh_poop_imposter_brightness = self.mesh_poop_imposter_brightness()
                    self.bungie_mesh_poop_streamingpriority = self.mesh_poop_streamingpriority()
                    self.bungie_mesh_poop_remove_from_shadow_geometry = self.mesh_poop_remove_from_shadow_geometry()
                    self.bungie_mesh_poop_cinema_only = self.mesh_poop_cinema_only()
                    self.bungie_mesh_poop_exclude_from_cinema = self.mesh_poop_exclude_from_cinema()
                    self.bungie_mesh_poop_disallow_object_lighting_samples = self.mesh_poop_disallow_object_lighting_samples()
                    self.bungie_mesh_poop_is_rain_occluder = self.mesh_poop_is_rain_occluder()

        elif self.bungie_mesh_type in ('_connected_geometry_mesh_type_physics', '_connected_geometry_mesh_type_collision', '_connected_geometry_mesh_type_structure', '_connected_geometry_mesh_type_default', '_connected_geometry_mesh_type_poop', '_connected_geometry_mesh_type_water_surface'):
            if self.halo.Face_Global_Material != '':
                self.bungie_face_global_material = self.face_global_material()


        elif self.bungie_mesh_type == '_connected_geometry_mesh_type_physics':
            self.bungie_mesh_primitive_type = self.mesh_primitive_type()
            if self.bungie_mesh_primitive_type == '_connected_geometry_primitive_type_box':
                self.bungie_mesh_primitive_box_length = self.mesh_primitive_box_length()
                self.bungie_mesh_primitive_box_width = self.mesh_primitive_box_width()
                self.bungie_mesh_primitive_box_height = self.mesh_primitive_box_height()
            elif self.bungie_mesh_primitive_type == '_connected_geometry_primitive_type_pill':
                self.bungie_mesh_primitive_pill_radius = self.mesh_primitive_pill_radius()
                self.bungie_mesh_primitive_pill_height = self.mesh_primitive_pill_height()
            elif self.bungie_mesh_primitive_type == '_connected_geometry_primitive_type_sphere':
                self.bungie_mesh_primitive_sphere_radius = self.mesh_primitive_sphere_radius()

        elif self.bungie_mesh_type == '_connected_geometry_mesh_type_portal':
            self.bungie_mesh_portal_type = self.mesh_portal_type()
            self.bungie_mesh_portal_ai_deafening = self.mesh_portal_ai_deafening()
            self.bungie_mesh_portal_blocks_sound = self.mesh_portal_blocks_sound()
            self.bungie_mesh_portal_is_door = self.mesh_portal_is_door()

        elif self.bungie_mesh_type == '_connected_geometry_mesh_type_decorator':
            self.bungie_mesh_decorator_lod = self.mesh_decorator_lod()
            self.bungie_mesh_decorator_name = self.mesh_decorator_name()

        elif self.bungie_mesh_type == '_connected_geometry_mesh_type_seam':
            self.bungie_mesh_seam_associated_bsp = self.mesh_seam_associated_bsp()
            # self.bungie_mesh_seam_front_bsp = self.mesh_seam_front_bsp()
            # self.bungie_mesh_seam_back_bsp = self.mesh_seam_back_bsp()

        elif self.bungie_mesh_type == '_connected_geometry_mesh_type_water_physics_volume':
            self.bungie_mesh_water_volume_depth = self.mesh_water_volume_depth()
            self.bungie_mesh_water_volume_flow_direction = self.mesh_water_volume_flow_direction()
            self.bungie_mesh_water_volume_flow_velocity = self.mesh_water_volume_flow_velocity()
            self.bungie_mesh_water_volume_fog_color = self.mesh_water_volume_fog_color()
            self.bungie_mesh_water_volume_fog_murkiness = self.mesh_water_volume_fog_murkiness()

        elif self.bungie_mesh_type == '_connected_geometry_mesh_type_planar_fog_volume':
            self.bungie_mesh_fog_name = self.mesh_fog_name()
            self.bungie_mesh_fog_appearance_tag = self.mesh_fog_appearance_tag()
            self.bungie_mesh_fog_volume_depth = self.mesh_fog_volume_depth()

        elif self.bungie_mesh_type == '_connected_geometry_mesh_type_obb_volume':
            self.bungie_mesh_obb_type = self.mesh_obb_type()

        # LIGHTMAP PROPERTIES
        if self.halo.Lightmap_Settings_Enabled:
            self.bungie_lightmap_additive_transparency = self.lightmap_additive_transparency()
            self.bungie_lightmap_ignore_default_resolution_scale = self.lightmap_ignore_default_resolution_scale()
            self.bungie_lightmap_resolution_scale = self.lightmap_resolution_scale()
            # self.bungie_lightmap_chart_group = self.lightmap_chart_group()
            self.bungie_lightmap_photon_fidelity = self.lightmap_photon_fidelity()
            self.bungie_lightmap_type = self.lightmap_type()
            self.bungie_lightmap_transparency_override = self.lightmap_transparency_override()
            # self.bungie_lightmap_analytical_bounce_modifier = self.lightmap_analytical_bounce_modifier()
            # self.bungie_lightmap_general_bounce_modifier = self.lightmap_general_bounce_modifier()
            # self.bungie_lightmap_analytical_absorb_ratio = self.lightmap_analytical_absorb_ratio()
            self.bungie_lightmap_translucency_tint_color = self.lightmap_translucency_tint_color()
            self.bungie_lightmap_lighting_from_both_sides = self.lightmap_lighting_from_both_sides()
            if self.not_bungie_game:
                self.bungie_mesh_per_vertex_lighting = self.mesh_per_vertex_lighting()
        # EMMISSIVE PROPERTIES
        if self.halo.Material_Lighting_Enabled:
            if not_bungie_game():
                self.bungie_lighting_attenuation_enabled = self.lighting_attenuation_enabled()
                self.bungie_lighting_frustum_blend = self.lighting_frustum_blend()
                self.bungie_lighting_frustum_cutoff = self.lighting_frustum_cutoff()
                self.bungie_lighting_frustum_falloff = self.lighting_frustum_falloff()
            if self.bungie_lighting_attenuation_enabled or not not_bungie_game():
                self.bungie_lighting_attenuation_cutoff = self.lighting_attenuation_cutoff()
                self.bungie_lighting_attenuation_falloff = self.lighting_attenuation_falloff()
            self.bungie_lighting_emissive_focus = self.lighting_emissive_focus()
            self.bungie_lighting_emissive_color = self.lighting_emissive_color()
            self.bungie_lighting_emissive_per_unit = self.lighting_emissive_per_unit()
            self.bungie_lighting_emissive_power = self.lighting_emissive_power()
            self.bungie_lighting_emissive_quality = self.lighting_emissive_quality()
            self.bungie_lighting_use_shader_gel = self.lighting_use_shader_gel()
            self.bungie_lighting_bounce_ratio = self.lighting_bounce_ratio()

        self.cleanup()

    def mesh_type(self):
        if self.boundary_surface():
            return '_connected_geometry_mesh_type_boundary_surface'
        elif self.collision():
            if (self.not_bungie_game and self.sidecar_type in ('SCENARIO', 'PREFAB')) or (self.sidecar_type == 'SCENARIO' and NWOMesh.poop(self.ob.parent)):
                return '_connected_geometry_mesh_type_poop_collision'
            else:
                return '_connected_geometry_mesh_type_collision'

        elif self.cookie_cutter():
            return '_connected_geometry_mesh_type_cookie_cutter'
        elif self.decorator():
            return '_connected_geometry_mesh_type_decorator'
        elif self.poop():
            return '_connected_geometry_mesh_type_poop'
        elif self.poop_marker():
            return '_connected_geometry_mesh_type_poop_marker'
        elif self.poop_rain_blocker():
            return '_connected_geometry_mesh_type_poop_rain_blocker'
        elif self.poop_vertical_rain_sheet():
            return '_connected_geometry_mesh_type_poop_vertical_rain_sheet'
        elif self.lightmap_region():
            return '_connected_geometry_mesh_type_lightmap_region'
        elif self.object_instance():
            return '_connected_geometry_mesh_type_object_instance'
        elif self.physics():
            return '_connected_geometry_mesh_type_physics'
        elif self.planar_fog_volume():
            return '_connected_geometry_mesh_type_planar_fog_volume'
        elif self.portal():
            return '_connected_geometry_mesh_type_portal'
        elif self.seam():
            return '_connected_geometry_mesh_type_seam'
        elif self.water_physics_volume():
            return '_connected_geometry_mesh_type_water_physics_volume'
        elif self.water_surface():
            return '_connected_geometry_mesh_type_water_surface'
        elif self.obb_volume():
            return '_connected_geometry_mesh_type_obb_volume'
        else:
            if self.not_bungie_game:
                if self.sidecar_type in ('SCENARIO', 'PREFAB'):
                    return '_connected_geometry_mesh_type_structure'
                else:
                    return '_connected_geometry_mesh_type_render'
            else:
                return '_connected_geometry_mesh_type_default'

    def mesh_global_material(self):
        return self.halo.Face_Global_Material

    def mesh_primitive_type(self):
        return self.halo.Mesh_Primitive_Type

    def mesh_primitive_box_length(self):
        return jstr(self.ob.dimensions.x)

    def mesh_primitive_box_width(self):
        return jstr(self.ob.dimensions.y)

    def mesh_primitive_box_height(self):
        return jstr(self.ob.dimensions.z)

    def mesh_primitive_pill_radius(self):
        return radius_str(self.ob)

    def mesh_primitive_pill_height(self):
        return jstr(self.ob.dimensions.z)

    def mesh_primitive_sphere_radius(self):
        return radius_str(self.ob)

    def mesh_boundary_surface_type(self):
        if self.ob.name.startswith('+soft_ceiling'):
            return '_connected_geometry_boundary_surface_type_soft_ceiling'
        elif self.ob.name.startswith('+soft_kill'):
            return '_connected_geometry_boundary_surface_type_soft_kill'
        elif self.ob.name.startswith('+slip_surface'):
            return '_connected_geometry_boundary_surface_type_slip_surface'
        else:
            return self.halo.Boundary_Surface_Type

    def mesh_boundary_surface_name(self):
        return self.halo.Boundary_Surface_Name

    def mesh_poop_lighting(self):
        if self.name.startswith(('%!',     '%-!','%+!','%*!',     '%-*!','%+*!',     '%*-!','%*+!')):
            return '_connected_geometry_poop_lighting_per_pixel'
        elif self.name.startswith(('%?',     '%-?','%+?','%*?',     '%-*?','%+*?',     '%*-?','%*+?')):
            return '_connected_geometry_poop_lighting_per_vertex'
        elif self.name.startswith(('%>',     '%->','%+>','%*>',     '%-*>','%+*>',     '%*->','%*+>')):
            return '_connected_geometry_poop_lighting_single_probe'
        else:
            return self.halo.Poop_Lighting_Override

    def mesh_poop_lightmap_resolution_scale(self):
        return jstr(self.halo.poop_lightmap_resolution_scale)

    def mesh_poop_pathfinding(self):
        if self.name.startswith(('%-',     '%!-','%?-','%>-','%*-',     '%!*-','%?*-','%>*-',     '%*!-','%*?-','%*>-')):
            return '_connected_poop_instance_pathfinding_policy_none'
        elif self.name.startswith(('%+',     '%!+','%?+','%>+','%*+',     '%!*+','%?*+','%>*+',     '%*!+','%*?+','%*>+')):
            return '_connected_poop_instance_pathfinding_policy_static'
        else:
            return self.halo.Poop_Pathfinding_Override

    def mesh_poop_imposter_policy(self):
        return self.halo.Poop_Imposter_Policy

    def mesh_poop_imposter_brightness(self):
        return jstr(self.halo.poop_imposter_brightness)

    # def mesh_poop_fade_range_start(self):
    #     return jstr(self.halo.Poop_Imposter_Fade_Range_Start)

    # def mesh_poop_fade_range_end(self):
    #     return jstr(self.halo.Poop_Imposter_Fade_Range_End)

    def mesh_poop_is_render_only(self):
        if self.name.startswith(poop_render_only_prefixes):
            return '1'
        else:
            return bool_str(self.halo.Poop_Render_Only)

    def mesh_poop_chops_portals(self):
        return bool_str(self.halo.Poop_Chops_Portals)

    def mesh_poop_does_not_block_aoe(self):
        return bool_str(self.halo.Poop_Does_Not_Block_AOE)

    def mesh_poop_excluded_from_lightprobe(self):
        return bool_str(self.halo.Poop_Excluded_From_Lightprobe)

    def mesh_poop_streamingpriority(self):
        return self.halo.poop_streaming_priority

    def mesh_poop_decal_spacing(self):
        return bool_str(self.halo.Poop_Decal_Spacing)

    def mesh_poop_precise_geometry(self):
        return bool_str(self.halo.Poop_Precise_Geometry)

    def mesh_poop_remove_from_shadow_geometry(self):
        return bool_str(self.halo.poop_remove_from_shadow_geometry)

    def mesh_poop_cinema_only(self):
        return bool_str(self.halo.poop_cinematic_properties == 'bungie_mesh_poop_cinema_only')

    def mesh_poop_exclude_from_cinema(self):
        return bool_str(self.halo.poop_cinematic_properties == 'bungie_mesh_poop_exclude_from_cinema')

    def mesh_poop_disallow_object_lighting_samples(self):
        return bool_str(self.halo.poop_disallow_lighting_samples)

    def mesh_poop_is_rain_occluder(self):
        return bool_str(self.halo.poop_rain_occluder)

    def mesh_tessellation_density(self):
        return self.halo.Mesh_Tessellation_Density

    def mesh_additional_compression(self):
        return self.halo.Mesh_Compression

    def mesh_use_uncompressed_verts(self):
        return bool_str(not self.halo.compress_verts)

    def uvmirror_across_entire_model(self):
        return bool_str(self.halo.uvmirror_across_entire_model)

    def mesh_per_vertex_lighting(self):
        return bool_str(self.halo.Lightmap_Type == '_connected_material_lightmap_type_per_vertex')

    def mesh_poop_collision_type(self):
        if self.halo.Poop_Render_Only:
            return '_connected_geometry_poop_collision_type_none'
        else:
            return self.halo.Poop_Collision_Type

    def mesh_poop_collision_override_global_material(self):
        return bool_str(self.halo.Face_Global_Material != '')

    def mesh_portal_type(self):
        return self.halo.Portal_Type

    def mesh_portal_ai_deafening(self):
        return bool_str(self.halo.Portal_AI_Deafening)

    def mesh_portal_blocks_sound(self):
        return bool_str(self.halo.Portal_Blocks_Sounds)

    def mesh_portal_is_door(self):
        return bool_str(self.halo.Portal_Is_Door)

    def mesh_decorator_lod(self):
        return str(self.halo.Decorator_LOD)

    def mesh_decorator_name(self):
        return self.halo.Decorator_Name

    def mesh_seam_associated_bsp(self):
        return f'{self.asset_name}_{true_bsp(self.halo)}'

    def mesh_water_volume_depth(self):
        return jstr(self.halo.Water_Volume_Depth)

    def mesh_water_volume_flow_direction(self):
        return jstr(self.halo.Water_Volume_Flow_Direction)

    def mesh_water_volume_flow_velocity(self):
        return jstr(self.halo.Water_Volume_Flow_Velocity)

    def mesh_water_volume_fog_color(self):
        if self.not_bungie_game:
            return color_3p_str(self.halo.Water_Volume_Fog_Color)
        else:
            return color_4p_str(self.halo.Water_Volume_Fog_Color)

    def mesh_water_volume_fog_murkiness(self):
        return jstr(self.halo.Water_Volume_Fog_Murkiness)

    def mesh_fog_name(self):
        return self.halo.Fog_Name

    def mesh_fog_appearance_tag(self):
        return clean_tag_path(self.halo.Fog_Appearance_Tag)

    def mesh_fog_volume_depth(self):
        return jstr(self.halo.Fog_Volume_Depth)

    def mesh_obb_type(self):
        return self.halo.obb_volume_type

    def face_type(self):
        return self.halo.Face_Type

    def face_mode(self):
        if not self.not_bungie_game and len(self.ob.children) > 0 and self.mesh_type == '_connected_geometry_mesh_type_poop':
            for child in self.ob.children:
                if CheckType.poop_collision_physics(child):
                    return '_connected_geometry_face_mode_render_only'
            else:
                return self.halo.Face_Mode
        else:
            return self.halo.Face_Mode


    def face_sides(self):
        return self.halo.Face_Sides

    def face_draw_distance(self):
        return self.halo.Face_Draw_Distance

    def face_global_material(self):
        return self.halo.Face_Global_Material

    def face_region(self):
        return true_region(self.halo)

    def texcoord_usage(self): # NEEDS ENTRY IN UI
        return self.halo.texcoord_usage

    def conveyor(self):
        return bool_str(self.halo.Conveyor)

    def ladder(self):
        return bool_str(self.halo.Ladder)

    def slip_surface(self):
        return bool_str(self.halo.Slip_Surface)

    def decal_offset(self):
        return bool_str(self.halo.Decal_Offset)

    def group_transparents_by_plane(self):
        return bool_str(self.halo.Group_Transparents_By_Plane)

    def no_shadow(self):
        return bool_str(self.halo.No_Shadow)

    def invisible_to_pvs(self):
        return bool_str(self.halo.no_pvs)

    def no_lightmap(self):
        return bool_str(self.halo.no_lightmap)

    def precise_position(self):
        return bool_str(self.halo.Precise_Position)

    def sky_permutation_index(self):
        return str(self.halo.Sky_Permutation_Index)

    def lightmap_additive_transparency(self):
        return jstr(self.halo.Lightmap_Additive_Transparency)

    def lightmap_ignore_default_resolution_scale(self):
        return bool_str(self.halo.Lightmap_Resolution_Scale)

    def lightmap_resolution_scale(self):
        return bool_str(self.halo.Lightmap_Resolution_Scale)

    def lightmap_photon_fidelity(self):
        return self.halo.lightmap_photon_fidelity

    def lightmap_type(self):
        return self.halo.Lightmap_Type

    def lightmap_transparency_override(self):
        return bool_str(self.halo.Lightmap_Transparency_Override)

    def lightmap_translucency_tint_color(self):
        if self.not_bungie_game:
            return color_3p_str(self.halo.Lightmap_Translucency_Tint_Color)
        else:
            return color_4p_str(self.halo.Lightmap_Translucency_Tint_Color)

    def lightmap_lighting_from_both_sides(self):
        return bool_str(self.halo.Lightmap_Lighting_From_Both_Sides)

    def lighting_attenuation_enabled(self): # NEEDS ENTRY IN UI
        return bool_str(self.halo.lighting_attenuation_enabled)

    def lighting_attenuation_cutoff(self):
        return jstr(self.halo.Material_Lighting_Attenuation_Cutoff)

    def lighting_attenuation_falloff(self):
        return jstr(self.halo.Material_Lighting_Attenuation_Falloff)

    def lighting_emissive_focus(self):
        return jstr(self.halo.Material_Lighting_Emissive_Focus)

    def lighting_emissive_color(self):
        return color_4p_str(self.halo.Material_Lighting_Emissive_Color)

    def lighting_emissive_per_unit(self):
        return bool_str(self.halo.Material_Lighting_Emissive_Per_Unit)

    def lighting_emissive_power(self):
        return jstr(self.halo.Material_Lighting_Emissive_Power)

    def lighting_emissive_quality(self):
        return jstr(self.halo.Material_Lighting_Emissive_Quality)

    def lighting_frustum_blend(self): # NEEDS ENTRY IN UI
        return jstr(self.halo.lighting_frustum_blend)

    def lighting_frustum_cutoff(self): # NEEDS ENTRY IN UI
        return jstr(self.halo.lighting_frustum_cutoff)

    def lighting_frustum_falloff(self): # NEEDS ENTRY IN UI
        return jstr(self.halo.lighting_frustum_falloff)

    def lighting_use_shader_gel(self):
        return bool_str(self.halo.Material_Lighting_Use_Shader_Gel)

    def lighting_bounce_ratio(self):
        return jstr(self.halo.Material_Lighting_Bounce_Ratio)

    def boundary_surface(self):
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_boundary_surface'), ('+soft_kill', '+soft_ceiling', '+slip_surface'))

    def collision(self):
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_collision'), ('@'))

    def cookie_cutter(self):
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_cookie_cutter'), ('+cookie'))

    def decorator(self):
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_decorator'), ('+decorator'))
    
    def default(self):
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_default'))

    def poop(self):
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_poop'), ('%'))

    def poop_marker(self): # REACH ONLY
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_poop_marker'))

    def poop_rain_blocker(self): # REACH ONLY
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_poop_rain_blocker'))

    def poop_vertical_rain_sheet(self): # REACH ONLY
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_poop_vertical_rain_sheet'))

    def lightmap_region(self): # REACH ONLY
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_lightmap_region'))

    def object_instance(self):
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_object_instance'), ('+flair'))

    def physics(self):
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_physics'), ('$'))

    def planar_fog_volume(self):
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_planar_fog_volume'), ('+fog'))

    def portal(self):
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_portal'), ('+portal'))

    def seam(self):
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_seam'), ('+seam'))

    def water_physics_volume(self):
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_water_physics_volume'), ('+water'))

    def water_surface(self):
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_water_surface'), ("'"))

    def obb_volume(self): # H4+ ONLY
        return mesh_type(self.ob, ('_connected_geometry_mesh_type_obb_volume')) 

class NWOMaterial:
    def __init__(self, material):
        self.material = material
        self.material_name = material.name
        self.halo = material.nwo
        self.is_override = self.override()
        if not_bungie_game():
            self.halo_shader_path = self.shader_path()
            self.halo_shader_name = self.shader_name()
            self.halo_shader_type = self.shader_type()
        else:
            self.bungie_shader_type = self.shader_type()
            self.bungie_shader_path = self.shader_path()

        del self.material
        del self.material_name
        del self.halo
        del self.is_override

    def shader_path(self):
        if self.is_override:
            return 'override'
        elif self.halo.shader_path == '':
            return 'shaders\\invalid'
        else:
            return clean_tag_path(self.halo.shader_path, '')


    def shader_name(self):
        if self.is_override:
            if self.material_name.startswith('+sky'):
                return 'InvisibleSky'
            elif self.material_name.startswith('+physics'):
                return 'Physics'
            elif self.material_name.startswith('+seam'):
                return 'Seam'
            elif self.material_name.startswith('+portal'):
                return 'Portal'
            elif self.material_name.startswith('+collision'):
                return 'Collision'
            elif self.material_name.startswith('+player_collision'):
                return 'playCollision'
            elif self.material_name.startswith('+wall_collision'):
                return 'wallCollision'
            elif self.material_name.startswith('+bullet_collision'):
                return 'bulletCollision'
            elif self.material_name.startswith('+cookie_cutter'):
                return 'CookieCutter'
            elif self.material_name.startswith('+rain_blocker'):
                return 'rainBlocker'
            elif self.material_name.startswith('+water_volume'):
                return 'waterVolume'
            elif self.material_name.startswith('+structure'):
                return 'Structure'
            elif self.material_name.startswith('+'):
                return 'override'
            else:
                return self.halo.material_override_h4
        
        else:
            temp_name = self.halo_shader_path
            return shortest_string(temp_name, temp_name.rpartition('\\')[2])

    def shader_type(self):
        if self.is_override:
            return 'override'
        elif not_bungie_game():
            return 'material'
        else:
            return self.halo.Shader_Type
            
            
    def override(self):
        if not_bungie_game():
            return self.material.name.startswith('+') or self.material.nwo.material_override_h4 != 'none'
        else:
            return self.material.name.startswith('+') or self.material.nwo.material_override != 'none'
