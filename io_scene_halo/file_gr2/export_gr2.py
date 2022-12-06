# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Generalkidd & Crisp
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

import shutil
import bpy
import json
import os
from os import path
from os.path import exists as file_exists
import ctypes
from subprocess import Popen

from ..gr2_utils import (
    GetDataPath,
    frame_prefixes,
    marker_prefixes,
    mesh_prefixes,
    special_materials,

    poop_render_only_prefixes,
    invalid_mesh_types,
    GetTagsPath,
    GetEKPath,
    sel_logic,
    GetToolType,
)

##############################
####### STRING TABLE #########
##############################

# def getStringTable():

##############################
##### NODES PROPERTIES #######
##############################

def getNodes(model_armature, skeleton_bones, halo_objects, not_bungie_game):
    nodesList = {}
    if model_armature != None:
        nodesList.update(skeleton_bones)

    for ob in halo_objects.lights:
        halo_light = ob.halo_json
        if ob.select_get():
            nodesList.update({ob.name: getLightProperties(halo_light, ob)})

    for ob in halo_objects.markers:
        halo_node = ob.halo_json
        halo_node_name = ob.name
        if ob.select_get():
            nodesList.update({ob.name: getNodeProperties(halo_node, halo_node_name, ob, not_bungie_game)})

    temp = ({'nodes_properties': nodesList})
    return temp

def getLightProperties(node, light):
    node_props = {}
    ###################
    # LIGHT PROPERTIES
    node_props.update({"bungie_object_type": "_connected_geometry_object_type_light"})
    node_props.update({"bungie_light_type_version": "1"})
    node_props.update({"bungie_light_type": getLightType(node.light_type_override, light.data.type)})
    node_props.update({"bungie_light_game_type": getLightGameType(node.Light_Game_Type)})
    node_props.update({"bungie_light_shape": getLightShape(node.Light_Shape)})
    node_props.update({"bungie_light_volume_distance": str(round(node.Light_Volume_Distance, 6))})
    node_props.update({"bungie_light_volume_intensity_scalar": str(round(node.Light_Volume_Intensity, 6))})
    # node_props.update({"bungie_light_fade_start_distance": str(round(node.Light_Fade_Start_Distance, 6))})
    # node_props.update({"bungie_light_fade_out_distance": str(round(node.Light_Fade_End_Distance, 6))})
    node_props.update({"bungie_light_color": getLightColor(node.Light_Color.r, node.Light_Color.g, node.Light_Color.b)})
    node_props.update({"bungie_light_intensity": str(round(node.Light_Intensity, 6))})
    node_props.update({"bungie_light_hotspot_size": str(round(node.Light_Hotspot_Size, 6))})
    node_props.update({"bungie_light_hotspot_falloff": str(round(node.Light_Hotspot_Falloff, 6))})
    node_props.update({"bungie_light_falloff_shape": str(round(node.Light_Falloff_Shape, 6))})
    node_props.update({"bungie_light_aspect": str(round(node.Light_Aspect, 6))})
    node_props.update({"bungie_light_frustum_width": str(round(node.Light_Frustum_Width, 6))})
    node_props.update({"bungie_light_frustum_height": str(round(node.Light_Frustum_Height, 6))})
    node_props.update({"bungie_light_bounce_light_ratio": str(round(node.Light_Bounce_Ratio, 6))})
    if node.Light_Tag_Override != '':
        node_props.update({"bungie_light_light_tag_override": node.Light_Tag_Override[0:127]})
    if node.Light_Shader_Reference != '':
        node_props.update({"bungie_light_shader_reference": node.Light_Shader_Reference[0:127]})
    if node.Light_Gel_Reference != '':
        node_props.update({"bungie_light_gel_reference": node.Light_Gel_Reference[0:127]})
    if node.Light_Lens_Flare_Reference != '':
        node_props.update({"bungie_light_lens_flare_reference": node.Light_Lens_Flare_Reference[0:127]})
    if node.Light_Ignore_BSP_Visibility:
        node_props.update({"bungie_light_ignore_bsp_visibility": "1"})
    if node.Light_Dynamic_Has_Bounce:
        node_props.update({"bungie_light_dynamic_light_has_bounce": "1"})
    if node.Light_Screenspace_Has_Specular:
        node_props.update({"bungie_light_screenspace_light_has_specular": "1"})
    # node_props.update({"bungie_light_clipping_size_x_pos": str(round(node.Light_Clipping_Size_X_Pos, 6))})
    # node_props.update({"bungie_light_clipping_size_y_pos": str(round(node.Light_Clipping_Size_Y_Pos, 6))})
    # node_props.update({"bungie_light_clipping_size_z_pos": str(round(node.Light_Clipping_Size_Z_Pos, 6))})
    # node_props.update({"bungie_light_clipping_size_x_neg": str(round(node.Light_Clipping_Size_X_Neg, 6))})
    # node_props.update({"bungie_light_clipping_size_y_neg": str(round(node.Light_Clipping_Size_Y_Neg, 6))})
    # node_props.update({"bungie_light_clipping_size_z_neg": str(round(node.Light_Clipping_Size_Z_Neg, 6))})
    if node.Light_Near_Attenuation_Start != 0:
        node_props.update({"bungie_light_near_attenuation_start": str(round(node.Light_Near_Attenuation_Start, 6))})
    elif node.Light_Game_Type == 'RERENDER': # added to prevent a sapien crash that occurs when light is rerender and no near attenuation start is set
        node_props.update({"bungie_light_near_attenuation_start": "1.000000"})
    if node.Light_Near_Attenuation_End != 0:
        node_props.update({"bungie_light_near_attenuation_end": str(round(node.Light_Near_Attenuation_End, 6))})
    if node.Light_Far_Attenuation_Start != 0:
        node_props.update({"bungie_light_far_attenuation_start": str(round(node.Light_Far_Attenuation_Start, 6))})
    if node.Light_Far_Attenuation_End != 0:
        node_props.update({"bungie_light_far_attenuation_end": str(round(node.Light_Far_Attenuation_End, 6))})
    node_props.update({"halo_export": "1"}),

    return node_props

def getLightType(halo_type, light_type):
    if light_type == 'POINT' or light_type == 'SUN':
        return '_connected_geometry_light_type_omni'
    else:
        if halo_type == 'SPOT':
            return '_connected_geometry_light_type_spot'
        else:
            return '_connected_geometry_light_type_directional'

def getLightGameType(type):
    match type:
        case 'DEFAULT':
            return '_connected_geometry_bungie_light_type_default'
        case 'INLINED':
            return '_connected_geometry_bungie_light_type_inlined'
        case 'RERENDER':
            return '_connected_geometry_bungie_light_type_rerender'
        case 'SCREEN SPACE':
            return '_connected_geometry_bungie_light_type_screen_space'
        case 'UBER':
            return '_connected_geometry_bungie_light_type_uber'

def getLightShape(shape):
    if shape == 'CIRCLE':
        return '_connected_geometry_light_shape_circle'
    else:
        return '_connected_geometry_light_shape_rectangle'

def getLightColor(red, green, blue):
    color = f'{str(1)} {str(round(red, 6))} {str(round(green, 6))} {str(round(blue, 6))}'

    return color

def getNodeProperties(node, name, ob, not_bungie_game):
    node_props = {}
    ###################
    # OBJECT PROPERTIES
    node_props.update({"bungie_object_type": getNodeType(node, name, ob)}),
    node_props.update({"bungie_object_id": node.object_id}),
    ###################
    # MARKER PROPERTIES
    if '_connected_geometry_object_type_marker' in node_props.values():
        node_props.update({"bungie_marker_type": getMarkerType(node.ObjectMarker_Type, node.Physics_Constraint_Type, node, not_bungie_game)})
        if node.Marker_All_Regions:
            node_props.update({"bungie_marker_all_regions": "1"})
        else:
            node_props.update({"bungie_marker_region": getMarkerRegion(node.Marker_Region)})
        if '_connected_geometry_mesh_type_object_instance' in node_props.values():
            if node.Marker_Region == '':
                node_props.update({"bungie_marker_all_regions": "1"})
            else:
                node_props.update({"bungie_marker_region": node.Marker_Region})
        if '_connected_geometry_marker_type_game_instance' in node_props.values() or '_connected_geometry_marker_type_prefab' in node_props.values():
            node_props.update({"bungie_marker_game_instance_tag_name": node.Marker_Game_Instance_Tag_Name})
            node_props.update({"bungie_marker_game_instance_variant_name": node.Marker_Game_Instance_Tag_Variant_Name})
        if '_connected_geometry_marker_type_model' in node_props.values() or '_connected_geometry_marker_type_hint' in node_props.values() or '_connected_geometry_marker_type_target' in node_props.values():
            node_props.update({"bungie_marker_model_group": getMarkerGroup(name)})
        if '_connected_geometry_marker_type_model' in node_props.values():
            if node.Marker_Velocity.x != 0 or node.Marker_Velocity.y != 0 or node.Marker_Velocity.z != 0:
                node_props.update({"bungie_marker_velocity": getMarkerVelocity(node.Marker_Velocity.x, node.Marker_Velocity.y, node.Marker_Velocity.z)})
        if '_connected_geometry_marker_type_pathfinding_sphere' in node_props.values():
            if node.Marker_Pathfinding_Sphere_Vehicle:
                node_props.update({"bungie_marker_pathfinding_sphere_vehicle_only": "1"})
            if node.Pathfinding_Sphere_Remains_When_Open:
                node_props.update({"bungie_marker_pathfinding_sphere_remains_when_open": "1"})
            if node.Pathfinding_Sphere_With_Sectors:
                node_props.update({"bungie_marker_pathfinding_sphere_with_sectors": "1"})
        if '_connected_geometry_marker_type_physics_hinge_constraint' in node_props.values() or '_connected_geometry_marker_type_physics_socket_constraint' in node_props.values():
            node_props.update({"bungie_physics_constraint_parent": node.Physics_Constraint_Parent})
            node_props.update({"bungie_physics_constraint_child": node.Physics_Constraint_Child})
            if node.Physics_Constraint_Uses_Limits:
                node_props.update({"bungie_physics_constraint_use_limits": "1"})
                if '_connected_geometry_marker_type_physics_hinge_constraint' in node_props.values():
                    node_props.update({"bungie_physics_constraint_hinge_min": str(round(node.Hinge_Constraint_Minimum, 6))})
                    node_props.update({"bungie_physics_constraint_hinge_max": str(round(node.Hinge_Constraint_Maximum, 6))})
                else:
                    node_props.update({"bungie_physics_constraint_cone_angle": str(round(node.Cone_Angle, 6))})
                    node_props.update({"bungie_physics_constraint_plane_min": str(round(node.Plane_Constraint_Minimum, 6))})
                    node_props.update({"bungie_physics_constraint_plane_max": str(round(node.Plane_Constraint_Maximum, 6))})
                    node_props.update({"bungie_physics_constraint_twist_start": str(round(node.Twist_Constraint_Start, 6))})
                    node_props.update({"bungie_physics_constraint_twist_end": str(round(node.Twist_Constraint_End, 6))})

    node_props.update({"halo_export": "1"}),
    ###################

    return node_props

def getNodeType(node, name, ob):
    if ob.type == 'LIGHT':
        return '_connected_geometry_object_type_light'
    elif ob.type == 'ARMATURE':
        return '_connected_geometry_object_type_frame' 
    elif ob.type == 'CAMERA':
        return '_connected_geometry_object_type_animation_camera'
    elif name.startswith(frame_prefixes):
        return '_connected_geometry_object_type_frame'
    elif name.startswith(marker_prefixes):
        return '_connected_geometry_object_type_marker'
    else:
        if ob.type == 'MESH':
            match node.Object_Type_All:
                case 'FRAME':
                    return '_connected_geometry_object_type_frame'
                case 'MARKER':
                    return '_connected_geometry_object_type_marker'
        else:
            match node.Object_Type_No_Mesh:
                case 'FRAME':
                    return '_connected_geometry_object_type_frame'
                case 'MARKER':
                    return '_connected_geometry_object_type_marker'

def getMarkerType(type, physics, node, not_bungie_game):
    if node.ObjectMarker_Type_Locked == 'GAME INSTANCE':
        if not not_bungie_game and node.Marker_Game_Instance_Tag_Name.endswith('.prefab'):
            return '_connected_geometry_marker_type_prefab'
        else:
            return '_connected_geometry_marker_type_game_instance'
    match type:
        case 'DEFAULT':
            return '_connected_geometry_marker_type_model'
        case 'EFFECTS':
            return '_connected_geometry_marker_type_effects'
        case 'GAME INSTANCE':
            if not not_bungie_game and node.Marker_Game_Instance_Tag_Name.endswith('.prefab'):
                return '_connected_geometry_marker_type_prefab'
            else:
                return '_connected_geometry_marker_type_game_instance'
        case 'GARBAGE':
            return '_connected_geometry_marker_type_garbage'
        case 'HINT':
            return '_connected_geometry_marker_type_hint'
        case 'PATHFINDING SPHERE':
            return '_connected_geometry_marker_type_pathfinding_sphere'
        case 'PHYSICS CONSTRAINT':
            if physics == 'HINGE':
                return '_connected_geometry_marker_type_physics_hinge_constraint'
            else:
                return '_connected_geometry_marker_type_physics_socket_constraint'
        case 'TARGET':
            return '_connected_geometry_marker_type_target'
        case 'WATER VOLUME FLOW':
            return '_connected_geometry_marker_type_water_volume_flow'

def getMarkerRegion(region):
    if region == '':
        return 'default'
    else:
        return region

def getMarkerGroup(name):
    group_name = name
    group_name = group_name.removeprefix('#')
    if group_name.rpartition('.')[0] != '':
        group_name = group_name.rpartition('.')[0]
    
    if group_name == '':
        group_name = 'null'

    return group_name

def getMarkerVelocity(x, y, z):
    velocity = f'{str(round(x, 6))} {str(round(y, 6))} {str(round(z, 6))}'

    return velocity

##############################
##### MESHES PROPERTIES ######
##############################

def getMeshes(halo_objects, asset_name, sidecar_type, not_bungie_game):
    meshesList = {}
    halo_mesh_objects = halo_objects.render + halo_objects.collision + halo_objects.physics + halo_objects.structure + halo_objects.poops + halo_objects.portals + halo_objects.seams + halo_objects.water_surfaces + halo_objects.lightmap_regions + halo_objects.fog + halo_objects.boundary_surfaces + halo_objects.water_physics + halo_objects.rain_occluders + halo_objects.decorator + halo_objects.particle
    for ob in halo_mesh_objects:
        halo_mesh = ob.halo_json
        halo_mesh_name = ob.name
        
        if ob.select_get(): # if the name of a mesh starts with this, don't process it.
            meshesList.update({ob.name: getMeshProperties(halo_mesh, halo_mesh_name, ob, asset_name, sidecar_type, not_bungie_game)})

    temp = ({'meshes_properties': meshesList})

    return temp

def getMeshProperties(mesh, name, ob, asset_name, sidecar_type, not_bungie_game):

    mesh_props = {}
    
    ###################
    # OBJECT PROPERTIES
    mesh_props.update({"bungie_object_type": "_connected_geometry_object_type_mesh"}),
    mesh_props.update({"bungie_object_id": mesh.object_id}),
    if not_bungie_game and sidecar_type == 'MODEL' and (mesh.Permutation_Name_Locked != '' or mesh.Permutation_Name != ''):
        if mesh.Permutation_Name_Locked != '':
            mesh_props.update({"bungie_permutation_name": mesh.Permutation_Name_Locked}),
        else:
            mesh_props.update({"bungie_permutation_name": mesh.Permutation_Name}),
    ###################
    # MESH PROPERTIES
    mesh_props.update({"bungie_mesh_type": getMeshType(mesh.ObjectMesh_Type, name, ob, sidecar_type, not_bungie_game)}),
    # Boundary Surface
    if '_connected_geometry_mesh_type_boundary_surface' in mesh_props.values():
        if mesh.Boundary_Surface_Name != '' or name.startswith(('+soft_ceiling:','+soft_kill:','+slip_surface:')):
            mesh_props.update({"bungie_mesh_boundary_surface_name": getBoundarySurfaceName(mesh.Boundary_Surface_Name, name)}),
        mesh_props.update({"bungie_mesh_boundary_surface_type": getBoundarySurfaceType(mesh.Boundary_Surface_Type, name)})
    # Decorator
    elif '_connected_geometry_mesh_type_decorator' in mesh_props.values():
        if mesh.Decorator_Name != '':
            mesh_props.update({"bungie_mesh_decorator_name": getDecoratorName(mesh.Decorator_Name)})
        mesh_props.update({"bungie_mesh_decorator_lod": getDecoratorLOD(mesh.Decorator_LOD)})
    # Poops
    elif '_connected_geometry_mesh_type_poop' in mesh_props.values():
        mesh_props.update({"bungie_mesh_poop_lighting": getPoopLighting(mesh.Poop_Lighting_Override, name)})
        mesh_props.update({"bungie_mesh_poop_pathfinding": getPoopPathfinding(mesh.Poop_Pathfinding_Override, name)})
        mesh_props.update({"bungie_mesh_poop_imposter_policy": getPoopImposter(mesh.Poop_Imposter_Policy)})
        if not mesh.Poop_Imposter_Transition_Distance_Auto:
            mesh_props.update({"bungie_mesh_poop_imposter_transition_distance": str(round(mesh.Poop_Imposter_Transition_Distance, 6))})
        # if mesh.Poop_Imposter_Fade_Range_Start != 36: # commented out 2022-11-01. Reason: appears to go unused, however this should be reinstated if there does appear to be some use
        #     mesh_props.update({"bungie_mesh_poop_fade_range_start": str(mesh.Poop_Imposter_Fade_Range_Start)})
        # if mesh.Poop_Imposter_Fade_Range_End != 30:
        #     mesh_props.update({"bungie_mesh_poop_fade_range_end": str(mesh.Poop_Imposter_Fade_Range_End)})
        # if mesh.Poop_Predominant_Shader_Name != '':
        #     mesh_props.update({"bungie_mesh_poop_poop_predominant_shader_name":mesh.Poop_Predominant_Shader_Name[0:1023]})
        mesh_props.update({"bungie_mesh_poop_decomposition_hulls": "-1"})
        if mesh.Poop_Render_Only or name.startswith(poop_render_only_prefixes):
            mesh_props.update({"bungie_mesh_poop_is_render_only": "1"})
        if mesh.Poop_Chops_Portals:
            mesh_props.update({"bungie_mesh_poop_chops_portals": "1"})
        if mesh.Poop_Does_Not_Block_AOE:
            mesh_props.update({"bungie_mesh_poop_does_not_block_aoe": "1"})
        if mesh.Poop_Excluded_From_Lightprobe:
            mesh_props.update({"bungie_mesh_poop_excluded_from_lightprobe": "1"})
        if mesh.Poop_Decal_Spacing:
            mesh_props.update({"bungie_mesh_poop_decal_spacing": "1"})
        if mesh.Poop_Precise_Geometry:
            mesh_props.update({"bungie_mesh_poop_precise_geometry": "1"})
        if mesh.Poop_Collision_Type != 'DEFAULT':
            mesh_props.update({"bungie_mesh_poop_collision_type": getPoopCollisionType(mesh.Poop_Collision_Type)}) 
    # Poop Collision
    elif '_connected_geometry_mesh_type_poop_collision' in mesh_props.values() and bpy.context.scene.halo.game_version in ('h4','h2a'):
        if mesh.Poop_Collision_Type != 'DEFAULT':
            mesh_props.update({"bungie_mesh_poop_collision_type": getPoopCollisionType(mesh.Poop_Collision_Type)}) 
        if mesh.Face_Global_Material != '':
            mesh_props.update({"bungie_mesh_poop_collision_override_global_material": "1"})
    # Fog Volume
    elif '_connected_geometry_mesh_type_planar_fog_volume' in mesh_props.values():
        if mesh.Fog_Name != '':
            mesh_props.update({"bungie_mesh_fog_name": mesh.Fog_Name[0:31]})
        if mesh.Fog_Appearance_Tag != '':
            mesh_props.update({"bungie_mesh_fog_appearance_tag": mesh.Fog_Appearance_Tag[0:31]})
        mesh_props.update({"bungie_mesh_fog_volume_depth": str(round(mesh.Fog_Volume_Depth, 6))})
    # Portal
    elif '_connected_geometry_mesh_type_portal' in mesh_props.values():
        mesh_props.update({"bungie_mesh_portal_type": getPortalType(mesh.Portal_Type)})
        if mesh.Portal_AI_Deafening:
            mesh_props.update({"bungie_mesh_portal_ai_deafening": "1"})
        if mesh.Portal_Blocks_Sounds:
            mesh_props.update({"bungie_mesh_portal_blocks_sound": "1"})
        if mesh.Portal_Is_Door:
            mesh_props.update({"bungie_mesh_portal_is_door": "1"})
    # Seam
    elif '_connected_geometry_mesh_type_seam' in mesh_props.values():
        mesh_props.update({"bungie_mesh_seam_associated_bsp": getSeamName(mesh, asset_name)}),
    # Water Physics Volume
    elif '_connected_geometry_mesh_type_water_physics_volume' in mesh_props.values():
        mesh_props.update({"bungie_mesh_water_volume_depth": str(round(mesh.Water_Volume_Depth, 6))})
        mesh_props.update({"bungie_mesh_water_volume_flow_direction": str(round(mesh.Water_Volume_Flow_Direction, 6))})
        mesh_props.update({"bungie_mesh_water_volume_flow_velocity": str(round(mesh.Water_Volume_Flow_Velocity, 6))})
        mesh_props.update({"bungie_mesh_water_volume_fog_color": getWaterFogColor(mesh.Water_Volume_Fog_Color.r, mesh.Water_Volume_Fog_Color.g, mesh.Water_Volume_Fog_Color.b)})
        mesh_props.update({"bungie_mesh_water_volume_fog_murkiness": str(round(mesh.Water_Volume_Fog_Murkiness, 6))})
    ###################
    # FACE PROPERTIES
    if mesh.ObjectMesh_Type not in invalid_mesh_types:
        if mesh.Face_Type != 'NORMAL':
            mesh_props.update({"bungie_face_type": getFaceType(mesh.Face_Type)})
        render_only_set = False
        if len(ob.children) > 0 and sel_logic.ObPoopsOnly(ob):
            for child in ob.children:
                if sel_logic.ObPoopsCollPhys(child):
                    mesh_props.update({"bungie_face_mode": '_connected_geometry_face_mode_render_only'})
                    render_only_set = True
                    break
        if not render_only_set:
            if mesh.Face_Mode != 'NORMAL':
                mesh_props.update({"bungie_face_mode": getFaceMode(mesh.Face_Mode)})
        if mesh.Face_Sides != 'ONE SIDED':
            mesh_props.update({"bungie_face_sides": getFaceSides(mesh.Face_Sides)})
        if mesh.Face_Draw_Distance != 'NORMAL':
            mesh_props.update({"bungie_face_draw_distance": getFaceDrawDistance(mesh.Face_Draw_Distance)})
        mesh_props.update({"bungie_face_region": getRegionName(mesh.Region_Name, mesh.Region_Name_Locked)})
        if '_connected_geometry_mesh_type_poop_collision' in mesh_props.values():
            mesh_props.update({"bungie_mesh_global_material": getGlobalMaterialName(mesh.Face_Global_Material)})
        else:
            mesh_props.update({"bungie_face_global_material": getGlobalMaterialName(mesh.Face_Global_Material)})
        if '_connected_geometry_face_type_sky' in mesh_props.values():
            mesh_props.update({"bungie_sky_permutation_index": str(mesh.Sky_Permutation_Index)})
        if mesh.Conveyor:
            mesh_props.update({"bungie_conveyor": "1"})
        if mesh.Ladder:
            mesh_props.update({"bungie_ladder": "1"})
        if mesh.Slip_Surface:
            mesh_props.update({"bungie_slip_surface": "1"})
        if mesh.Decal_Offset:
            mesh_props.update({"bungie_decal_offset": "1"})
        if mesh.Group_Transparents_By_Plane:
            mesh_props.update({"bungie_group_transparents_by_plane": "1"})
        if mesh.No_Shadow:
            mesh_props.update({"bungie_no_shadow": "1"})
        if mesh.Precise_Position:
            mesh_props.update({"bungie_precise_position": "1"})
    ###################
    # MATERIAL LIGHTING PROPERTIES
    if mesh.Material_Lighting_Enabled:
        mesh_props.update({"bungie_lighting_attenuation_cutoff": str(round(mesh.Material_Lighting_Attenuation_Cutoff, 6))})
        mesh_props.update({"bungie_lighting_attenuation_falloff": str(round(mesh.Material_Lighting_Attenuation_Falloff, 6))})
        mesh_props.update({"bungie_lighting_emissive_focus": str(round(mesh.Material_Lighting_Emissive_Focus, 6))})
        mesh_props.update({"bungie_lighting_emissive_color": getEmissiveColor(mesh.Material_Lighting_Emissive_Color.r, mesh.Material_Lighting_Emissive_Color.g, mesh.Material_Lighting_Emissive_Color.b)})
        mesh_props.update({"bungie_lighting_emissive_power": str(round(mesh.Material_Lighting_Emissive_Power, 6))})
        mesh_props.update({"bungie_lighting_emissive_quality": str(round(mesh.Material_Lighting_Emissive_Quality, 6))})
        mesh_props.update({"bungie_lighting_bounce_ratio": str(round(mesh.Material_Lighting_Bounce_Ratio, 6))})
        if mesh.Material_Lighting_Emissive_Per_Unit:
            mesh_props.update({"bungie_lighting_emissive_per_unit": "1"})
        if mesh.Material_Lighting_Use_Shader_Gel:
            mesh_props.update({"bungie_lighting_use_shader_gel": "1"})
    ###################
    # LIGHTMAP PROPERTIES
    if mesh.Lightmap_Settings_Enabled:
        mesh_props.update({"bungie_lightmap_additive_transparency": str(round(mesh.Lightmap_Additive_Transparency, 6))})
        if mesh.Lightmap_Resolution_Scale != 3:
            mesh_props.update({"bungie_lightmap_ignore_default_resolution_scale": "1"})
            mesh_props.update({"bungie_lightmap_resolution_scale": str(mesh.Lightmap_Resolution_Scale)})
        mesh_props.update({"bungie_lightmap_chart_group": str(mesh.Lightmap_Chart_Group)})
        mesh_props.update({"bungie_lightmap_type": getLightmapType(mesh.Lightmap_Type)})
        if mesh.Lightmap_Transparency_Override:
            mesh_props.update({"bungie_lightmap_transparency_override": "1"})
        mesh_props.update({"bungie_lightmap_analytical_bounce_modifier": str(round(mesh.Lightmap_Analytical_Bounce_Modifier, 6))})
        mesh_props.update({"bungie_lightmap_general_bounce_modifier": str(round(mesh.Lightmap_General_Bounce_Modifier, 6))})
        mesh_props.update({"bungie_lightmap_translucency_tint_color": getLightmapColor(mesh.Lightmap_Translucency_Tint_Color.r, mesh.Lightmap_Translucency_Tint_Color.g, mesh.Lightmap_Translucency_Tint_Color.b)})
        if mesh.Lightmap_Lighting_From_Both_Sides:
            mesh_props.update({"bungie_lightmap_lighting_from_both_sides": "1"})
    ###################
    # OTHER MESH PROPERTIES
    if mesh.ObjectMesh_Type not in invalid_mesh_types:
        if mesh.Mesh_Tesselation_Density != 'DEFAULT':
            mesh_props.update({"bungie_mesh_tessellation_density": getTesselationDensity(mesh.Mesh_Tesselation_Density)})
        if mesh.Mesh_Compression != 'DEFAULT':
            mesh_props.update({"bungie_mesh_additional_compression": getMeshCompression(mesh.Mesh_Compression)})
        if mesh.Mesh_Primitive_Type != 'NONE':
            mesh_props.update({"bungie_mesh_primitive_type": getPrimitiveType(mesh.Mesh_Primitive_Type)})
            if mesh.Mesh_Primitive_Type == 'BOX':
                mesh_props.update({"bungie_mesh_primitive_box_length": str(round(ob.dimensions.x, 6))})
                mesh_props.update({"bungie_mesh_primitive_box_width": str(round(ob.dimensions.y, 6))})
                mesh_props.update({"bungie_mesh_primitive_box_height": str(round(ob.dimensions.z, 6))})
            elif mesh.Mesh_Primitive_Type == 'PILL':
                mesh_props.update({"bungie_mesh_primitive_pill_radius": str(round(GetRadius(ob, False), 6))})
                mesh_props.update({"bungie_mesh_primitive_pill_height": str(round(ob.dimensions.z, 6))})
            elif mesh.Mesh_Primitive_Type == 'SPHERE':
                mesh_props.update({"bungie_mesh_primitive_sphere_radius": str(round(GetRadius(ob, True), 6))})

    mesh_props.update({"halo_export": "1"}),

    return mesh_props

def getMeshType(type, name, ob, sidecar_type, not_bungie_game):
    if name.startswith(('+soft_ceiling','+soft_kill','+slip_surface')):
        return '_connected_geometry_mesh_type_boundary_surface'
    elif name.startswith('@'):
        if sidecar_type == 'SCENARIO' and not_bungie_game:
            return '_connected_geometry_mesh_type_poop_collision'
        else:
            return '_connected_geometry_mesh_type_collision'
    elif name.startswith('+cookie'):
        return '_connected_geometry_mesh_type_cookie_cutter'
    elif name.startswith('%'):
        return '_connected_geometry_mesh_type_poop'
    elif name.startswith('+flair'):
        return '_connected_geometry_mesh_type_object_instance'
    elif name.startswith('$'):
        if sidecar_type == 'SCENARIO':
            return '_connected_geometry_mesh_type_poop_physics'
        else:
            return '_connected_geometry_mesh_type_physics'
    elif name.startswith('+fog'):
        return '_connected_geometry_mesh_type_planar_fog_volume'
    elif name.startswith('+portal'):
        return '_connected_geometry_mesh_type_portal'
    elif name.startswith('+seam'):
        return '_connected_geometry_mesh_type_seam'
    elif name.startswith('+water'):
        return '_connected_geometry_mesh_type_water_physics_volume'
    elif name.startswith('\''):
        return '_connected_geometry_mesh_type_water_surface'
    else:
        match type:
            case 'BOUNDARY SURFACE':
                return '_connected_geometry_mesh_type_boundary_surface'
            case 'COLLISION':
                if sidecar_type == 'SCENARIO':
                    return '_connected_geometry_mesh_type_poop_collision'
                else:
                    return '_connected_geometry_mesh_type_collision'
            case 'COOKIE CUTTER':
                return '_connected_geometry_mesh_type_cookie_cutter'
            case 'DECORATOR':
                return '_connected_geometry_mesh_type_decorator'
            case 'DEFAULT':
                return '_connected_geometry_mesh_type_default'
            case 'INSTANCED GEOMETRY':
                return '_connected_geometry_mesh_type_poop'
            case 'INSTANCED GEOMETRY MARKER':
                return '_connected_geometry_mesh_type_poop_marker'
            case 'INSTANCED GEOMETRY RAIN BLOCKER':
                return '_connected_geometry_mesh_type_poop_rain_blocker'
            case 'INSTANCED GEOMETRY VERTICAL RAIN SHEET':
                return '_connected_geometry_mesh_type_poop_vertical_rain_sheet'
            case 'LIGHTMAP REGION':
                return '_connected_geometry_mesh_type_lightmap_region'
            case 'OBJECT INSTANCE':
                return '_connected_geometry_mesh_type_object_instance'
            case 'PHYSICS':
                if sidecar_type == 'SCENARIO':
                    return '_connected_geometry_mesh_type_poop_physics'
                else:
                    return '_connected_geometry_mesh_type_physics'
            case 'PLANAR FOG VOLUME':
                return '_connected_geometry_mesh_type_planar_fog_volume'
            case 'PORTAL':
                return '_connected_geometry_mesh_type_portal'
            case 'SEAM':
                return '_connected_geometry_mesh_type_seam'
            case 'WATER PHYSICS VOLUME':
                return '_connected_geometry_mesh_type_water_physics_volume'
            case 'WATER SURFACE':
                return '_connected_geometry_mesh_type_water_surface'

def getBoundarySurfaceName(bs_name, name):
    var = ''
    if name.startswith(('+soft_ceiling:','+soft_kill:','+slip_surface:')) and name.rpartition(':')[2] != name:
        var = name.rpartition(':')[2]
    else:
        var = bs_name

    return var[0:31]

def getBoundarySurfaceType(type, name):
    if name.startswith('+soft_ceiling'):
        return '_connected_geometry_boundary_surface_type_soft_ceiling'
    elif name.startswith('+soft_kill'):
        return '_connected_geometry_boundary_surface_type_soft_kill'
    elif name.startswith('+slip_surface'):
        return '_connected_geometry_boundary_surface_type_slip_surface'
    else:
        match type:
            case 'SOFT CEILING':
                return '_connected_geometry_boundary_surface_type_soft_ceiling'
            case 'SOFT KILL':
                return '_connected_geometry_boundary_surface_type_soft_kill'
            case 'SLIP SURFACE':
                return '_connected_geometry_boundary_surface_type_slip_surface'

def getDecoratorName(dec_name):
    return dec_name[0:31]

def getDecoratorLOD(LOD):
    return str(LOD)

def getPoopLighting(policy, name):
    if name.startswith(('%!',     '%-!','%+!','%*!',     '%-*!','%+*!',     '%*-!','%*+!')):
        return '_connected_geometry_poop_lighting_per_pixel'
    elif name.startswith(('%?',     '%-?','%+?','%*?',     '%-*?','%+*?',     '%*-?','%*+?')):
        return '_connected_geometry_poop_lighting_per_vertex'
    elif name.startswith(('%>',     '%->','%+>','%*>',     '%-*>','%+*>',     '%*->','%*+>')):
        return '_connected_geometry_poop_lighting_single_probe'
    else:
        match policy:
            case 'PER PIXEL':
                return '_connected_geometry_poop_lighting_per_pixel'
            case 'PER VERTEX':
                return '_connected_geometry_poop_lighting_per_vertex'
            case 'SINGLE PROBE':
                return '_connected_geometry_poop_lighting_single_probe'

def getPoopPathfinding(policy, name):
    if name.startswith(('%-',     '%!-','%?-','%>-','%*-',     '%!*-','%?*-','%>*-',     '%*!-','%*?-','%*>-')):
        return '_connected_poop_instance_pathfinding_policy_none'
    elif name.startswith(('%+',     '%!+','%?+','%>+','%*+',     '%!*+','%?*+','%>*+',     '%*!+','%*?+','%*>+')):
        return '_connected_poop_instance_pathfinding_policy_static'
    else:
        match policy:
            case 'CUTOUT':
                return '_connected_poop_instance_pathfinding_policy_cutout'
            case 'NONE':
                return '_connected_poop_instance_pathfinding_policy_none'
            case 'STATIC':
                return '_connected_poop_instance_pathfinding_policy_static'

def getPoopImposter(policy):
    match policy:
        case 'POLYGON DEFAULT':
            return '_connected_poop_instance_imposter_policy_polygon_default'
        case 'POLYGON HIGH':
            return '_connected_poop_instance_imposter_policy_polygon_high'
        case 'CARD DEFAULT':
            return '_connected_poop_instance_imposter_policy_card_default'
        case 'CARD HIGH':
            return '_connected_poop_instance_imposter_policy_card_high'
        case 'NONE':
            return '_connected_poop_instance_imposter_policy_none'
        case 'NEVER':
            return '_connected_poop_instance_imposter_policy_never'

def getPoopCollisionType(type):
    match type:
        case 'PLAYER':
            return '_connected_geometry_poop_collision_type_play_collision'
        case 'BULLET':
            return '_connected_geometry_poop_collision_type_bullet_collision'

def getPortalType(type):
    match type:
        case 'NO WAY':
            return '_connected_geometry_portal_type_no_way'
        case 'ONE WAY':
            return '_connected_geometry_portal_type_one_way'
        case 'TWO WAY':
            return '_connected_geometry_portal_type_two_way'

def getSeamName(mesh, asset_name):
    bsp = ''
    if mesh.bsp_name_locked !='':
        bsp = mesh.bsp_name_locked
    else:
        bsp = mesh.bsp_name

    return f'{asset_name}_{bsp}'

def getWaterFogColor(red, green, blue):
    color = f'{str(1)} {str(round(red, 6))} {str(round(green, 6))} {str(round(blue, 6))}'

    return color

def getFaceType(type):
    match type:
        case 'SEAM SEALER':
            return '_connected_geometry_face_type_seam_sealer'
        case 'SKY':
            return '_connected_geometry_face_type_sky'
        case 'WEATHER POLYHEDRA':
            return '_connected_geometry_face_type_weather_polyhedra'

def getFaceMode(mode):
    match mode:
        case 'RENDER ONLY':
            return '_connected_geometry_face_mode_render_only'
        case 'COLLISION ONLY':
            return '_connected_geometry_face_mode_collision_only'
        case 'SPHERE COLLISION ONLY':
            return '_connected_geometry_face_mode_sphere_collision_only'
        case 'SHADOW ONLY':
            return '_connected_geometry_face_mode_shadow_only'
        case 'LIGHTMAP ONLY':
            return '_connected_geometry_face_mode_lightmap_only'
        case 'BREAKABLE':
            return '_connected_geometry_face_mode_breakable'

def getFaceSides(sides):
    match sides:
        case 'ONE SIDED':
            return '_connected_geometry_face_sides_one_sided'
        case 'ONE SIDED TRANSPARENT':
            return '_connected_geometry_face_sides_one_sided_transparent'
        case 'TWO SIDED':
            return '_connected_geometry_face_sides_two_sided'
        case 'TWO SIDED TRANSPARENT':
            return '_connected_geometry_face_sides_two_sided_transparent' 

def getFaceDrawDistance(distance):
    match distance:
        case 'NORMAL':
            return '_connected_geometry_face_draw_distance_normal'    
        case 'MID':
            return '_connected_geometry_face_draw_distance_detail_mid'
        case 'CLOSE':
            return '_connected_geometry_face_draw_distance_detail_close'

def getRegionName(region, region_locked):
    if region_locked != '':
        return region_locked
    elif region == '':
        return 'default'
    else:
        return region

def getGlobalMaterialName(mat):
    if mat == '':
        return 'default'
    else:
        return mat

def getLightmapType(type):
    match type:
        case 'PER PIXEL':
            return '_connected_material_lightmap_type_per_pixel'
        case 'PER VERTEX':
            return '_connected_material_lightmap_type_per_vertex'

def getLightmapColor(red, green, blue):
    color = str(1) + ' ' + str(round(red, 6)) + ' ' + str(round(green, 6)) + ' ' + str(round(blue, 6))

    return color 

def getEmissiveColor(red, green, blue):
    color = str(1) + ' ' + str(round(red, 6)) + ' ' + str(round(green, 6)) + ' ' + str(round(blue, 6))

    return color

def getTesselationDensity(density):
    match density:
        case '4X':
            return '_connected_geometry_mesh_tessellation_density_4x'
        case '9X':
            return '_connected_geometry_mesh_tessellation_density_9x'
        case '36X':
            return '_connected_geometry_mesh_tessellation_density_36x'

def getMeshCompression(compression):
    match compression:
        case 'FORCE OFF':
            return '_connected_geometry_mesh_additional_compression_force_off'
        case 'FORCE ON':
            return '_connected_geometry_mesh_additional_compression_force_on'

def getPrimitiveType(type):
    match type:
        case 'BOX':
            return '_connected_geometry_primitive_type_box'
        case 'PILL':
            return '_connected_geometry_primitive_type_pill'
        case 'SPHERE':
            return '_connected_geometry_primitive_type_sphere'

def GetRadius(ob, sphere):
    if sphere:
        diameter = max(ob.dimensions)
    else:
        diameter = max(ob.dimensions.x, ob.dimensions.y)
    radius = diameter / 2.0
    return radius

##############################
#### MATERIAL PROPERTIES #####
##############################

def getMaterials(not_bungie_game):
    matList = {}
    
    for ob in bpy.context.view_layer.objects:
        if 1<=len(ob.material_slots):
            for mat_slot in ob.material_slots:
                if mat_slot is not None:
                    halo_material = mat_slot.material.halo_json
                    halo_material_name = mat_slot.material.name

                    shaderPath = ''
                    shaderType = ''

                    if halo_material_name.lower().startswith(special_materials) or halo_material.material_override != 'NONE':
                        shaderType = 'override'
                        if halo_material_name.lower().startswith('+collision') or halo_material.material_override == 'COLLISION':
                            shaderPath = 'collisionVolume'
                        elif halo_material_name.lower().startswith('+physics') or halo_material.material_override == 'PHYSICS':
                            shaderPath = 'physicsVolume'
                        elif halo_material_name.lower().startswith('+portal') or halo_material.material_override == 'PORTAL':
                            shaderPath = 'bungie_mesh_type=_connected_geometry_mesh_type_portal'
                        elif halo_material_name.lower().startswith('+seamsealer') or halo_material.material_override == 'SEAM SEALER':
                            shaderPath = 'bungie_face_type=_connected_geometry_face_type_seam_sealer'
                        elif halo_material_name.lower().startswith('+sky') or halo_material.material_override == 'SKY':
                            shaderPath = 'bungie_face_type=_connected_geometry_face_type_sky'
                        elif halo_material_name.lower().startswith('+slip_surface') or halo_material.material_override == 'SLIP SURFACE':
                            shaderPath = 'slipSurface'
                        elif halo_material_name.lower().startswith('+soft_ceiling') or halo_material.material_override == 'SOFT CEILING':
                            shaderPath = 'softCeiling'
                        elif halo_material_name.lower().startswith('+soft_kill') or halo_material.material_override == 'SOFT KILL':
                            shaderPath = 'softKill'
                        elif halo_material_name.lower().startswith('+weatherpoly') or halo_material.material_override == 'WEATHERPOLY':
                            shaderPath = 'bungie_face_type=_connected_geometry_face_type_weather_polyhedra'
                        else:
                            shaderPath = 'Volume'

                    else:
                        if '.' in halo_material.shader_path:
                            shaderPath = halo_material.shader_path.rpartition('.')[0]
                        else:
                            shaderPath = halo_material.shader_path

                        #clean shader path
                        shaderPath = shaderPath.replace('"','')
                        shaderPath = shaderPath.strip('\\')
                        shaderPath = shaderPath.lower().replace(GetTagsPath().lower(),'')

                        if shaderPath == '':
                            shaderPath = 'shaders\invalid'
                        
                        if not_bungie_game:
                            shaderType = 'material'
                        else:
                            shaderType = halo_material.Shader_Type
                    if not_bungie_game:
                        if shaderType == 'override':
                            matList.update({halo_material_name : {"halo_shader_name": 'override', "halo_shader_path": shaderPath, "halo_shader_type": shaderType}})
                        else:
                            matList.update({halo_material_name : {"halo_shader_name": shaderPath.rpartition('\\')[2], "halo_shader_path": shaderPath, "halo_shader_type": shaderType}})
                    else:
                        matList.update({halo_material_name : {"bungie_shader_path": shaderPath, "bungie_shader_type": shaderType}})

    temp = ({'material_properties': matList})

    return temp

def export_asset(report, filePath="", keep_fbx=False, keep_json=False, asset_path="", asset_name="", tag_type='', perm='', is_windows=False, bsp='', model_armature='', skeleton_bones={}, halo_objects=None, sidecar_type=''):
    if tag_type != 'selected':
        fileName = GetFileName(asset_name, tag_type, perm, asset_path, bsp)
        rename_file(filePath, fileName)
    else:
        fileName = filePath
    pathList = fileName.split(".")
    jsonPath = ""
    for x in range(len(pathList)-1):
        jsonPath += pathList[x]
    jsonPath += ".json"

    build_json(jsonPath, model_armature, skeleton_bones, halo_objects, asset_name, sidecar_type)

    if(is_windows):
        gr2Path = ""
        for x in range(len(pathList)-1):
            gr2Path += pathList[x]
            gr2Path += ".gr2"

        build_gr2(fileName, jsonPath, gr2Path)
        if(file_exists(gr2Path)):
            report({'INFO'},"GR2 conversion finished!")
        else:
            report({'WARNING'},"GR2 conversion failed!")
            ctypes.windll.user32.MessageBoxW(0, "Tool.exe failed to export your GR2 file. Blender may need to be run as an Administrator or there may be an issue with your project settings.", "GR2 EXPORT FAILED", 0)
        
        if tag_type != 'selected':
            move_assets(fileName, jsonPath, gr2Path, asset_path, keep_fbx, keep_json, tag_type)
        else:
            CleanFiles(filePath, jsonPath, gr2Path)

        return {'FINISHED'}
    else:
        ctypes.windll.user32.MessageBoxW(0, "GR2 Not Created! Your current OS is not supported. The Halo tools only support Windows. FBX & JSON saved succesfully.", "OS NOT SUPPORTED", 0)
        return {'FINISHED'}

def CleanFiles(filePath, jsonPath, gr2Path):
    os.remove(filePath)
    os.remove(jsonPath)
    os.remove(gr2Path)

def rename_file(filePath, fileName=''):
    os.replace(filePath, fileName)

def GetFileName(asset_name, tag_type, perm='', asset_path='', bsp=''):
    # use information about the file to determine its name
    if tag_type == 'animations':
        name = bpy.context.active_object.animation_data.action.name
        if name.rpartition('.')[0] != '':
            name = name.rpartition('.')[0]
        name = path.join(asset_path, name)
    elif tag_type == 'particle_model':
        name = path.join(asset_path, asset_name)
    elif bsp == '':
        if perm != '' and perm != 'default':
            name = f"{path.join(asset_path, asset_name)}_{perm}_{tag_type}"
        else:
            name = f'{path.join(asset_path, asset_name)}_{tag_type}'
    else:
        if perm != '' and perm != 'default':
            name = f'{path.join(asset_path, asset_name)}_{bsp}_{tag_type}_{perm}'
        else:
            name = f'{path.join(asset_path, asset_name)}_{bsp}_{tag_type}'
    # remove data path from name
    name = name.replace(GetDataPath(), '')
    # return the name with the fbx extension
    return f'{name}.fbx'

def move_assets(fileName, jsonPath, gr2Path, asset_path, keep_fbx, keep_json, tag_type):
    if tag_type == 'animations':
        if not file_exists(path.join(asset_path, 'animations')) and (keep_fbx or keep_json):
            os.makedirs(path.join(asset_path, 'animations'))
        if not file_exists(path.join(asset_path, 'export', 'animations')):
            os.makedirs(path.join(asset_path, 'export', 'animations'))
        if keep_fbx:
            shutil.copy(fileName, path.join(asset_path, 'animations'))
        if keep_json:
            shutil.copy(jsonPath, path.join(asset_path, 'animations'))
        shutil.copy(gr2Path, path.join(asset_path, 'export', 'animations'))
    else: 
        if not file_exists(path.join(asset_path, 'models')) and (keep_fbx or keep_json):
            os.makedirs(path.join(asset_path, 'models'))
        if not file_exists(path.join(asset_path, 'export', 'models')):
            os.makedirs(path.join(asset_path, 'export', 'models'))
        if keep_fbx:
            shutil.copy(fileName, path.join(asset_path, 'models'))
        if keep_json:
            shutil.copy(jsonPath, path.join(asset_path, 'models'))
        shutil.copy(gr2Path, path.join(asset_path, 'export', 'models'))

    CleanFiles(fileName, jsonPath, gr2Path)

def build_json(jsonPath, model_armature, skeleton_bones, halo_objects, asset_name, sidecar_type):
    not_bungie_game = bpy.context.scene.halo.game_version in ('h4','h2a')
    jsonTemp = {}
    # jsonTemp.update(getStringTable(halo_objects))
    jsonTemp.update(getNodes(model_armature, skeleton_bones, halo_objects, not_bungie_game))
    jsonTemp.update(getMeshes(halo_objects, asset_name, sidecar_type, not_bungie_game))
    jsonTemp.update(getMaterials(not_bungie_game))

    haloJSON = json.dumps(jsonTemp, indent=4)

    with open(jsonPath, 'w') as j:
        j.write(haloJSON)

def build_gr2(filePath, jsonPath, gr2Path):
    try:            
        if not os.access(filePath, os.R_OK):
            ctypes.windll.user32.MessageBoxW(0, "GR2 Not Exported. Output Folder Is Read-Only! Try running Blender as an Administrator.", "ACCESS VIOLATION", 0)
        else:
            toolCommand = '{} fbx-to-gr2 "{}" "{}" "{}"'.format(GetToolType(), filePath, jsonPath, gr2Path)
            os.chdir(GetEKPath())
            p = Popen(toolCommand)
            p.wait()
            os.chdir(GetDataPath())
    except:
        ctypes.windll.user32.MessageBoxW(0, "GR2 Not Exported. Please check your editing kit path in add-on preferences and try again.", "INVALID EK PATH", 0)
        os.remove(filePath)
        os.remove(jsonPath)

def export_gr2(operator, context, report, asset_path, asset_name, is_windows, tag_type, halo_objects,
        bsp='',
        perm='',
        model_armature='',
        skeleton_bones=[],
        filepath="",
        keep_fbx=False,
        keep_json=False,
        sidecar_type='',
        **kwargs
        ):
    os.chdir(GetDataPath())
    filepath = filepath.replace(GetDataPath(), '')
    export_asset(report, filepath, keep_fbx, keep_json, asset_path, asset_name, tag_type, perm, is_windows, bsp, model_armature, skeleton_bones, halo_objects, sidecar_type)

    return {'FINISHED'}

