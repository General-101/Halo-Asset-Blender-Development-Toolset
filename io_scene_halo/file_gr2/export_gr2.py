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

EKPath = bpy.context.preferences.addons['io_scene_halo'].preferences.hrek_path

#clean editing kit path
EKPath = EKPath.replace('"','')
EKPath = EKPath.strip('\\')

#get tool path
toolPath = EKPath + '\\tool_fast.exe'

#get tags path
tagsPath = EKPath + '\\tags\\'

frame_prefixes = ('b ', 'b_', 'frame ', 'frame_','bip ','bip_','bone ','bone_')
marker_prefixes = ('#')
mesh_prefixes = ('+soft_ceiling','+soft_kill','+slip_surface', '@','+cookie','+decorator','+flair', '%', '$','+fog','+portal', '+seam','+water', '\'')
special_prefixes = ('b ', 'b_', 'frame ', 'frame_','bip ','bip_','bone ','bone_','#','+soft_ceiling','+soft_kill','+slip_surface', '@','+cookie','+decorator','+flair', '%', '$','+fog','+portal', '+seam','+water', '\'')

halo_node_prefixes = ('b ', 'b_', 'frame ', 'frame_','bip ','bip_','bone ','bone_','#') # these prefixes indicate a mesh should not be written to meshes_properties

boundary_surface_prefixes = ('+soft_ceiling','+soft_kill','+slip_surface') # boundary surface prefixes can take a name with +prefix:name e.g. +soft_ceiling:camera_ceiling_01
cookie_cutter_prefixes = ('+cookie')
decorator_prefixes = ('+decorator') # decorators can take a name with +decorator:name (not implemented)
fog_volume_prefixes = ('+fog') # fog volumes can take a name with +fog:name (not implemented)
object_instance_prefixes = ('+flair') # self-reminder: Flairs need to have marker_regions written to them in the json, this should match the face region
portal_prefixes = ('+portal') # portals can have properties automatically through the object name (once I get around to adding it)
seam_prefixes = ('+seam') # seams can take a name with +seam:name
water_volume_prefixes = ('+water')

poop_lighting_prefixes = ('%!',     '%-!','%+!','%*!',     '%-*!','%+*!',     '%*-!','%*+!',          '%?',     '%-?','%+?','%*?',     '%-*?','%+*?',     '%*-?','%*+?'          '%>',     '%->','%+>','%*>',     '%-*>','%+*>',     '%*->','%*+>')
poop_pathfinding_prefixes = ('%+',     '%!+','%?+','%>+','%*+',     '%!*+','%?*+','%>*+',     '%*!+','%*?+','%*>+',          '%-',     '%!-','%?-','%>-','%*-',     '%!*-','%?*-','%>*-',     '%*!-','%*?-','%*>-')
poop_render_only_prefixes = ('%*',     '%!*','%?*','%>*','%-*','%+*',     '%!-*','%!+*','%?-*','%?+*','%>-*','%>+*')

special_materials = ('+collision', '+physics', '+portal','+seamsealer','+sky','+weatherpoly')

special_mesh_types = ('BOUNDARY SURFACE','DECORATOR','INSTANCED GEOMETRY','PLANAR FOG VOLUME','PORTAL','SEAM','WATER PHYSICS VOLUME',)
invalid_mesh_types = ('BOUNDARY SURFACE', 'COOKIE CUTTER', 'INSTANCED GEOMETRY MARKER', 'INSTANCED GEOMETRY RAIN BLOCKER', 'INSTANCED GEOMETRY VERTICAL RAIN SHEET', 'LIGHTMAP REGION', 'PLANAR FOG VOLUME', 'PORTAL', 'SEAM', 'WATER PHYSICS VOLUME')

##############################
##### NODES PROPERTIES #######
##############################

def getNodes():
    nodesList = {}

    # for arm in bpy.data.armatures:
    #     for bone in arm.bones:
    #         nodesList.update({bone.name: getBoneProperties()})

    for light in bpy.data.lights:
        halo_light = light.halo_json
        nodesList.update({light.name: getLightProperties(halo_light, light)})

    for ob in bpy.data.objects:
        halo_node = ob.halo_json
        halo_node_name = ob.name

        if ((ob.type == 'MESH' and halo_node.Object_Type_All != 'MESH') or ob.type == 'EMPTY' or (halo_node_name.startswith(halo_node_prefixes) and ob.type != 'LIGHT')) and ob.select_get(): # if the name of a mesh starts with this, don't process it.
            nodesList.update({ob.name: getNodeProperties(halo_node, halo_node_name, ob)})

    temp = ({'nodes_properties': nodesList})

    return temp

#ID1 = 0
#ID2 = 1000

def getBoneProperties():
    node_props = {}

    node_props.update({"bungie_object_type": "_connected_geometry_object_type_frame"}),
    node_props.update({"bungie_frame_ID1": getFrameID1()}),
    node_props.update({"bungie_frame_ID2": getFrameID2()}),

    return node_props

def getFrameID1():
    global ID1
    ID1 = ID1 + 1

    return str(ID1)

def getFrameID2():
    global ID2
    ID2 = ID2 + 1

    return str(ID2)

def getLightProperties(node, light):
    node_props = {}
    ###################
    # LIGHT PROPERTIES
    node_props.update({"bungie_object_type": "_connected_geometry_object_type_light"})
    node_props.update({"bungie_light_type_version": "1"})
    node_props.update({"bungie_light_type": getLightType(node.light_type_override, light.type)})
    node_props.update({"bungie_light_game_type": getLightGameType(node.Light_Game_Type)})
    node_props.update({"bungie_light_shape": getLightShape(node.Light_Shape)})
    node_props.update({"bungie_light_volume_distance": str(round(node.Light_Volume_Distance, 6))})
    node_props.update({"bungie_light_volume_intensity_scalar": str(round(node.Light_Volume_Intensity, 6))})
    node_props.update({"bungie_light_fade_start_distance": str(round(node.Light_Fade_Start_Distance, 6))})
    node_props.update({"bungie_light_fade_out_distance": str(round(node.Light_Fade_End_Distance, 6))})
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
    if node.Light_Use_Clipping:
        node_props.update({"bungie_light_use_clipping": "1"})
        node_props.update({"bungie_light_clipping_size_x_pos": str(round(node.Light_Clipping_Size_X_Pos, 6))})
        node_props.update({"bungie_light_clipping_size_y_pos": str(round(node.Light_Clipping_Size_Y_Pos, 6))})
        node_props.update({"bungie_light_clipping_size_z_pos": str(round(node.Light_Clipping_Size_Z_Pos, 6))})
        node_props.update({"bungie_light_clipping_size_x_neg": str(round(node.Light_Clipping_Size_X_Neg, 6))})
        node_props.update({"bungie_light_clipping_size_y_neg": str(round(node.Light_Clipping_Size_Y_Neg, 6))})
        node_props.update({"bungie_light_clipping_size_z_neg": str(round(node.Light_Clipping_Size_Z_Neg, 6))})
    if node.Light_Near_Attenuation:
        node_props.update({"bungie_light_use_near_attenuation": "1"})
        node_props.update({"bungie_light_near_attenuation_start": str(round(node.Light_Near_Attenuation_Start, 6))})
        node_props.update({"bungie_light_near_attenuation_end": str(round(node.Light_Near_Attenuation_End, 6))})
    if node.Light_Far_Attenuation:
        node_props.update({"bungie_light_use_far_attenuation": "1"})
        node_props.update({"bungie_light_far_attenuation_start": str(round(node.Light_Far_Attenuation_Start, 6))})
        node_props.update({"bungie_light_far_attenuation_end": str(round(node.Light_Far_Attenuation_End, 6))})

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
    color = str(1) + ' ' + str(round(red, 6)) + ' ' + str(round(green, 6)) + ' ' + str(round(blue, 6))

    return color

def getNodeProperties(node, name, ob):
    node_props = {}
    ###################
    # OBJECT PROPERTIES
    node_props.update({"bungie_object_type": getNodeType(node, name, ob)}),
    ###################
    # MARKER PROPERTIES
    if '_connected_geometry_object_type_marker' in node_props.values():
        node_props.update({"bungie_marker_type": getMarkerType(node.ObjectMarker_Type, node.Physics_Constraint_Type)})
        if node.Marker_All_Regions:
            node_props.update({"bungie_marker_all_regions": "1"})
        else:
            node_props.update({"bungie_marker_region": getMarkerRegion(node.Marker_Region)})
        if '_connected_geometry_mesh_type_object_instance' in node_props.values():
            if node.Marker_Region == '':
                node_props.update({"bungie_marker_all_regions": "1"})
            else:
                node_props.update({"bungie_marker_region": node.Marker_Region})
        if '_connected_geometry_marker_type_game_instance' in node_props.values():
            node_props.update({"bungie_marker_game_instance_tag_name": node.Marker_Game_Instance_Tag_Name[0:63]})
            node_props.update({"bungie_marker_game_instance_variant_name": node.Marker_Game_Instance_Tag_Name[0:63]})
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

def getMarkerType(type, physics):
    match type:
        case 'DEFAULT':
            return '_connected_geometry_marker_type_model'
        case 'EFFECTS':
            return '_connected_geometry_marker_type_effects'
        case 'GAME INSTANCE':
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
    velocity = str(round(x, 6)) + ' ' + str(round(y, 6)) + ' ' + str(round(z, 6))

    return velocity

##############################
##### MESHES PROPERTIES ######
##############################

def getMeshes():
    meshesList = {}

    for ob in bpy.data.objects:
        halo_mesh = ob.halo_json
        halo_mesh_name = ob.name
        
        if ob.type == 'MESH' and (not halo_mesh_name.startswith(halo_node_prefixes) and halo_mesh.Object_Type_All == 'MESH') and ob.select_get(): # if the name of a mesh starts with this, don't process it.
            meshesList.update({ob.name: getMeshProperties(halo_mesh, halo_mesh_name, ob)})

    temp = ({'meshes_properties': meshesList})

    return temp

def getMeshProperties(mesh, name, ob):

    mesh_props = {}
    
    ###################
    # OBJECT PROPERTIES
    mesh_props.update({"bungie_object_type": "_connected_geometry_object_type_mesh"}),
    ###################
    # MESH PROPERTIES
    mesh_props.update({"bungie_mesh_type": getMeshType(mesh.ObjectMesh_Type, name, ob)}),
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
        if mesh.Poop_Imposter_Transition_Distance != -1:
            mesh_props.update({"bungie_mesh_poop_imposter_transition_distance": str(round(mesh.Poop_Imposter_Transition_Distance, 6))})
        if mesh.Poop_Imposter_Fade_Range_Start != 36:
            mesh_props.update({"bungie_mesh_poop_fade_range_start": str(mesh.Poop_Imposter_Fade_Range_Start)})
        if mesh.Poop_Imposter_Fade_Range_End != 30:
            mesh_props.update({"bungie_mesh_poop_fade_range_end": str(mesh.Poop_Imposter_Fade_Range_End)})
        if mesh.Poop_Predominant_Shader_Name != '':
            mesh_props.update({"bungie_mesh_poop_poop_predominant_shader_name":mesh.Poop_Imposter_Fade_Range_End[0:1023]})
        mesh_props.update({"bungie_mesh_poop_decomposition_hulls": "4294967295"})
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
        if mesh.Seam_Name != '' or name.startswith('+seam:'):
            mesh_props.update({"bungie_mesh_seam_associated_bsp": getSeamName(mesh.Seam_Name, name)}),
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
        if mesh.Face_Mode != 'NORMAL':
            mesh_props.update({"bungie_face_mode": getFaceMode(mesh.Face_Mode)})
        if mesh.Face_Sides != 'ONE SIDED':
            mesh_props.update({"bungie_face_sides": getFaceSides(mesh.Face_Sides)})
        if mesh.Face_Draw_Distance != 'NORMAL':
            mesh_props.update({"bungie_face_draw_distance": getFaceDrawDistance(mesh.Face_Draw_Distance)})
        mesh_props.update({"bungie_face_region": getRegionName(mesh.Region_Name)})
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
                mesh_props.update({"bungie_mesh_primitive_box_length": str(round(mesh.Box_Length, 6))})
                mesh_props.update({"bungie_mesh_primitive_box_width": str(round(mesh.Box_Width, 6))})
                mesh_props.update({"bungie_mesh_primitive_box_height": str(round(mesh.Box_Height, 6))})
            elif mesh.Mesh_Primitive_Type == 'PILL':
                mesh_props.update({"bungie_mesh_primitive_pill_radius": str(round(mesh.Pill_Radius, 6))})
                mesh_props.update({"bungie_mesh_primitive_pill_height": str(round(mesh.Pill_Height, 6))})
            elif mesh.Mesh_Primitive_Type == 'SPHERE':
                mesh_props.update({"bungie_mesh_primitive_sphere_radius": str(round(mesh.Sphere_Radius, 6))})

    return mesh_props

def getMeshType(type, name, ob):
    if name.startswith(('+soft_ceiling','+soft_kill','+slip_surface')):
        return '_connected_geometry_mesh_type_boundary_surface'
    elif name.startswith('@'):
        if ob.parent and ((ob.parent.halo_json.ObjectMesh_Type == 'INSTANCED GEOMETRY' and not ob.parent.name.startswith(mesh_prefixes)) or ob.parent.name.startswith('%')):
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
        if ob.parent and ((ob.parent.halo_json.ObjectMesh_Type == 'INSTANCED GEOMETRY' and not ob.parent.name.startswith(mesh_prefixes)) or ob.parent.name.startswith('%')):
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
                return '_connected_geometry_mesh_type_collision'
            case 'COOKIE CUTTER':
                return '_connected_geometry_mesh_type_cookie_cutter'
            case 'DECORATOR':
                return '_connected_geometry_mesh_type_decorator'
            case 'DEFAULT':
                return '_connected_geometry_mesh_type_default'
            case 'INSTANCED GEOMETRY':
                return '_connected_geometry_mesh_type_poop'
            case 'INSTANCED GEOMETRY COLLISION':
                return '_connected_geometry_mesh_type_poop_collision'
            case 'INSTANCED GEOMETRY MARKER':
                return '_connected_geometry_mesh_type_poop_physics'
            case 'INSTANCED GEOMETRY PHYSICS':
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

def getPortalType(type):
    match type:
        case 'NO WAY':
            return '_connected_geometry_portal_type_no_way'
        case 'ONE WAY':
            return '_connected_geometry_portal_type_one_way'
        case 'TWO WAY':
            return '_connected_geometry_portal_type_two_way'

def getSeamName(seam_name, name):
    var = ''
    if name.startswith(('+seam:')) and name.rpartition(':')[2] != name:
        var = name.rpartition(':')[2]
    else:
        var = seam_name

    return var[0:31]

def getWaterFogColor(red, green, blue):
    color = str(1) + ' ' + str(round(red, 6)) + ' ' + str(round(green, 6)) + ' ' + str(round(blue, 6))

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

def getRegionName(region):
    if region == '':
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

##############################
#### MATERIAL PROPERTIES #####
##############################

def getMaterials():
    matList = {}

    halo_special_materials = ('+collision','+physics',"+portal","+seamsealer","+sky","+weatherpoly") # some special material names to match legacy
    
    for ob in bpy.data.objects:
        if 1<=len(ob.material_slots):
            for mat_slot in ob.material_slots:
                if mat_slot is not None:
                    halo_material = mat_slot.material.halo_json
                    halo_material_name = mat_slot.material.name

                    shaderPath = ''
                    shaderType = ''

                    if halo_material_name.startswith(halo_special_materials) or halo_material.material_override != 'NONE':
                        shaderType = 'override'
                        if halo_material_name.startswith('+collision') or halo_material.material_override == 'COLLISION':
                            shaderPath = 'collisionVolume'
                        elif halo_material_name.startswith('+physics') or halo_material.material_override == 'PHYSICS':
                            shaderPath = 'physicsVolume'
                        elif halo_material_name.startswith('+portal') or halo_material.material_override == 'PORTAL':
                            shaderPath = 'bungie_mesh_type=_connected_geometry_mesh_type_portal'
                        elif halo_material_name.startswith('+seamsealer') or halo_material.material_override == 'SEAM SEALER':
                            shaderPath = 'bungie_face_type=_connected_geometry_face_type_seam_sealer'
                        elif halo_material_name.startswith('+sky') or halo_material.material_override == 'SKY':
                            shaderPath = 'bungie_face_type=_connected_geometry_face_type_sky'
                        elif halo_material_name.startswith('+weatherpoly') or halo_material.material_override == 'WEATHERPOLY':
                            shaderPath = 'bungie_face_type=_connected_geometry_face_type_weather_polyhedra'

                    else:
                        if '.' in halo_material.shader_path:
                            shaderPath = halo_material.shader_path.rpartition('.')[0]
                        else:
                            shaderPath = halo_material.shader_path

                        #clean shader path
                        shaderPath = shaderPath.replace('"','')
                        shaderPath = shaderPath.strip('\\')
                        shaderPath = shaderPath.replace(tagsPath,'')

                        if shaderPath == '':
                            shaderPath = 'shaders\invalid'
                        
                        match halo_material.Shader_Type:
                            case 'SHADER':
                                shaderType = 'shader'
                            case 'SHADER CORTANA':
                                shaderType = 'shader_cortana'
                            case 'SHADER CUSTOM':
                                shaderType = 'shader_custom'
                            case 'SHADER DECAL':
                                shaderType = 'shader_decal'
                            case 'SHADER FOLIAGE':
                                shaderType = 'shader_foliage'
                            case 'SHADER FUR':
                                shaderType = 'shader_fur'
                            case 'SHADER FUR STENCIL':
                                shaderType = 'shader_fur_stencil'
                            case 'SHADER GLASS':
                                shaderType = 'shader_glass'
                            case 'SHADER HALOGRAM':
                                shaderType = 'shader_halogram'
                            case 'SHADER  MUX':
                                shaderType = 'shader_mux'
                            case 'SHADER MUX MATERIAL':
                                shaderType = 'shader_mux_material'
                            case 'SHADER SCREEN':
                                shaderType = 'shader_screen'
                            case 'SHADER SKIN':
                                shaderType = 'shader_skin'
                            case 'SHADER TERRAIN':
                                shaderType = 'shader_terrain'
                            case 'SHADER WATER':
                                shaderType = 'shader_water'

                    matList.update({halo_material_name : {"bungie_shader_path": shaderPath, "bungie_shader_type": shaderType}})

    temp = ({'material_properties': matList})

    return temp

import os
from os.path import exists as file_exists
import ctypes
from subprocess import Popen

def export_asset(report, filePath="", keep_fbx=False, keep_json=False, asset_path="", asset_name="", tag_type='', perm='', is_windows=False):
    if tag_type != 'selected':
        fileName = GetFileName(filePath, asset_name, tag_type, perm, asset_path)
        rename_file(filePath, asset_name, tag_type, perm, fileName)
    else:
        fileName = filePath

    pathList = fileName.split(".")
    jsonPath = ""
    for x in range(len(pathList)-1):
        jsonPath += pathList[x]
    jsonPath += ".json"

    build_json(jsonPath)

    if(is_windows):
        gr2Path = ""
        for x in range(len(pathList)-1):
            gr2Path += pathList[x]
            gr2Path += ".gr2"

        print('\nTool Path... %r' % toolPath)

        build_gr2(toolPath, fileName, jsonPath, gr2Path)
        if(file_exists(gr2Path)):
            report({'INFO'},"GR2 conversion finished!")
        else:
            report({'INFO'},"GR2 conversion failed!")
            ctypes.windll.user32.MessageBoxW(0, "Tool.exe failed to export your GR2 file. Blender may need to be run as an Administrator or there may be an issue with your project settings.", "GR2 EXPORT FAILED", 0)

        fbx_crushed = False
        json_binned = False

        if not keep_fbx:
            fbx_crushed = True
        if not keep_json:
            json_binned = True
        
        if tag_type != 'selected':
            move_assets(fileName, jsonPath, gr2Path, asset_path, fbx_crushed, json_binned, tag_type)
        else:
            CleanFiles(filePath, jsonPath, gr2Path, fbx_crushed, json_binned)

        return {'FINISHED'}
    else:
        ctypes.windll.user32.MessageBoxW(0, "GR2 Not Created! Your current OS is not supported. The Halo tools only support Windows. FBX & JSON saved succesfully.", "Unsuported OS", 0)
        return {'FINISHED'}

def CleanFiles(filePath, jsonPath, gr2Path, fbx_crushed, json_binned):
    if(fbx_crushed):
        os.remove(filePath)
    if(json_binned):
        os.remove(jsonPath)
    os.remove(gr2Path)

def rename_file(filePath, asset_name, tag_type, perm='', fileName=''):
    os.replace(filePath, fileName)

def GetFileName(filePath, asset_name, tag_type, perm='', asset_path=''):
    if tag_type == 'animations':
        name = bpy.context.active_object.animation_data.action.name
        name = name.rpartition('.')[0]
        name = asset_path + '\\' + name + '.fbx'
    else:
        if perm != '' and perm != 'default':
            name = asset_path + '\\' + asset_name + '_' + perm
            name = name + '_' + tag_type + '.fbx'
        else:
            name = asset_path + '\\' + asset_name + '_' + tag_type + '.fbx'
    return name

def move_assets(fileName, jsonPath, gr2Path, asset_path, fbx_crushed, json_binned, tag_type):
    if tag_type == 'animations':
        if not file_exists(asset_path + "\\animations"):
            os.makedirs(asset_path + "\\animations")
        if not file_exists(asset_path + "\\export\\animations"):
            os.makedirs(asset_path + "\\export\\animations")
        if not fbx_crushed:
            shutil.copy(fileName, asset_path + "\\animations")
        if not json_binned:
            shutil.copy(jsonPath, asset_path + "\\export\\animations")
        shutil.copy(gr2Path, asset_path + "\\export\\animations")
    else: 
        if not file_exists(asset_path + "\\models"):
            os.makedirs(asset_path + "\\models")
        if not file_exists(asset_path + "\\export\\models"):
            os.makedirs(asset_path + "\\export\\models")
        if not fbx_crushed:
            shutil.copy(fileName, asset_path + "\\models")
        if not json_binned:
            shutil.copy(jsonPath, asset_path + "\\export\\models")
        shutil.copy(gr2Path, asset_path + "\\export\\models")

    os.remove(fileName)
    os.remove(jsonPath)
    os.remove(gr2Path)

def build_json(jsonPath):
    jsonTemp = {}
    jsonTemp.update(getNodes())
    jsonTemp.update(getMeshes())
    jsonTemp.update(getMaterials())

    haloJSON = json.dumps(jsonTemp, indent=4)

    jsonFile = open(jsonPath, "w")
    jsonFile.write(haloJSON)
    jsonFile.close()

def build_gr2(toolPath, filePath, jsonPath, gr2Path):
    try:            
        if not os.access(filePath, os.R_OK):
            ctypes.windll.user32.MessageBoxW(0, "GR2 Not Exported. Output Folder Is Read-Only! Try running Blender as an Administrator.", "ACCESS VIOLATION", 0)
        else:
            toolCommand = '"{}" fbx-to-gr2 "{}" "{}" "{}"'.format(toolPath, filePath, jsonPath, gr2Path)
            print('\nRunning Tool command... %r' % toolCommand)
            p = Popen(toolCommand)
            p.wait()
    except:
        ctypes.windll.user32.MessageBoxW(0, "GR2 Not Exported. Please check your HREK editing kit path in add-on preferences and try again.", "Invalid HREK Path", 0)
        os.remove(filePath)
        os.remove(jsonPath)
    finally:
        return {'FINISHED'}

def save(operator, context, report, is_windows, tag_type,
        perm='',
        filepath="",
        keep_fbx=False,
        keep_json=False,
        asset_path='',
        asset_name='',
        **kwargs
        ):

    export_asset(report, filepath, keep_fbx, keep_json, asset_path, asset_name, tag_type, perm, is_windows)

    return {'FINISHED'}

