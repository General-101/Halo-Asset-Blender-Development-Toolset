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

##############################
####### STRING TABLE #########
##############################
def getStrings():
    stringsList = {}

    temp = ({'string_table' : stringsList})

    return temp

##############################
##### NODES PROPERTIES #######
##############################

def getNodes():
    nodesList = {}

    halo_node_prefixes = ('#','b_','b ','frame_','frame ') # these prefixes indicate a mesh should not be written to meshes_properties

    for node in bpy.data.objects:
        if node.name.startswith(halo_node_prefixes):
            nodesList.update({node.name: getNodesProperties()})

    temp = ({'nodes_properties': nodesList})

    return temp

def getNodesProperties():
    node_props = {
        # OBJECT PROPERTIES
        "bungie_object_type": "_connected_geometry_object_type_frame"

    }

    return node_props

##############################
##### MESHES PROPERTIES ######
##############################

def getMeshes(use_selection=False, use_visible=False, use_active_collection=False):
    meshesList = {}

    halo_node_prefixes = ('b ', 'b_', 'frame ', 'frame_','bip ','bip_','bone ','bone_','#') # these prefixes indicate a mesh should not be written to meshes_properties



    for ob in bpy.data.objects:
        halo_mesh = ob.halo_json
        halo_mesh_name = ob.name
        
        if use_selection:
            if ob.type == 'MESH' and (not halo_mesh_name.startswith(halo_node_prefixes) or halo_mesh.Object_Type_All != 'MESH') and ob.select_get(): # if the name of a mesh starts with this, don't process it.
                meshesList.update({ob.name: getMeshProperties(halo_mesh, halo_mesh_name, ob)})
        if use_visible:
            if ob.type == 'MESH' and (not halo_mesh_name.startswith(halo_node_prefixes) or halo_mesh.Object_Type_All != 'MESH') and ob.visible_get(): # if the name of a mesh starts with this, don't process it.
                meshesList.update({ob.name: getMeshProperties(halo_mesh, halo_mesh_name, ob)})
        if not use_selection and not use_visible and not use_active_collection:
            if ob.type == 'MESH' and (not halo_mesh_name.startswith(halo_node_prefixes) or halo_mesh.Object_Type_All != 'MESH'): # if the name of a mesh starts with this, don't process it.
                meshesList.update({ob.name: getMeshProperties(halo_mesh, halo_mesh_name, ob)})

    temp = ({'meshes_properties': meshesList})

    return temp

def getMeshProperties(mesh, name, ob):
    print("here we go")

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
    if '_connected_geometry_mesh_type_decorator' in mesh_props.values():
        if mesh.Decorator_Name != '':
            mesh_props.update({"bungie_mesh_decorator_name": getDecoratorName(mesh.Decorator_Name)})
        mesh_props.update({"bungie_mesh_decorator_lod": getDecoratorLOD(mesh.Decorator_LOD)})
    # Poops
    if '_connected_geometry_mesh_type_poop' in mesh_props.values():
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
    if '_connected_geometry_mesh_type_planar_fog_volume' in mesh_props.values():
        if mesh.Fog_Name != '':
            mesh_props.update({"bungie_mesh_fog_name": mesh.Fog_Name[0:31]})
        if mesh.Fog_Appearance_Tag != '':
            mesh_props.update({"bungie_mesh_fog_appearance_tag": mesh.Fog_Appearance_Tag[0:31]})
        mesh_props.update({"bungie_mesh_fog_volume_depth": str(round(mesh.Fog_Volume_Depth, 6))})
    # Portal
    if '_connected_geometry_mesh_type_portal' in mesh_props.values():
        mesh_props.update({"bungie_mesh_portal_type": getPortalType(mesh.Portal_Type)})
        if mesh.Portal_AI_Deafening:
            mesh_props.update({"bungie_mesh_portal_ai_deafening": "1"})
        if mesh.Portal_Blocks_Sounds:
            mesh_props.update({"bungie_mesh_portal_blocks_sound": "1"})
        if mesh.Portal_Is_Door:
            mesh_props.update({"bungie_mesh_portal_is_door": "1"})
    # Seam
    if '_connected_geometry_mesh_type_seam' in mesh_props.values():
        if mesh.Seam_Name != '' or name.startswith('+seam:'):
            mesh_props.update({"bungie_mesh_seam_associated_bsp": getSeamName(mesh.Seam_Name, name)}),
    # Water Physics Volume
    if '_connected_geometry_mesh_type_water_physics_volume' in mesh_props.values():
        mesh_props.update({"bungie_mesh_water_volume_depth": str(round(mesh.Water_Volume_Depth, 6))})
        mesh_props.update({"bungie_mesh_water_volume_flow_direction": str(round(mesh.Water_Volume_Flow_Direction, 6))})
        mesh_props.update({"bungie_mesh_water_volume_flow_velocity": str(round(mesh.Water_Volume_Flow_Velocity, 6))})
        mesh_props.update({"bungie_mesh_water_volume_fog_color": getWaterFogColor(mesh.Water_Volume_Fog_Color.r, mesh.Water_Volume_Fog_Color.g, mesh.Water_Volume_Fog_Color.b)})
        mesh_props.update({"bungie_mesh_water_volume_fog_murkiness": str(round(mesh.Water_Volume_Fog_Murkiness, 6))})

    ###################
    # MESH BOUNDARY SUR
    # FACE PROPERTIES
    #mesh_props["bungie_region_name"] = getRegionName(mesh.Region_Name),
    #"bungie_face_type": getFaceType()

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
    color = str(round(red, 6)) + ' ' + str(round(green, 6)) + ' ' + str(round(blue, 6))

    return color

def getRegionName(region):
    if region == '':
        return 'default'
    else:
        return region

def getFaceType():
    return 'eyo'


##############################
#### MATERIAL PROPERTIES #####
##############################

def getMaterials():
    matList = {}

    halo_special_materials = ('+collision','+physics',"+portal","+seamsealer","+sky","+weatherpoly") # some special material names to match legacy
    
    for ob in bpy.data.objects:
        for mat_slot in ob.material_slots:
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
import tempfile
import ctypes
from subprocess import Popen

def export_asset(report, filePath="", export_gr2=False, delete_fbx=False, delete_json=False, use_selection=False, use_visible=False, use_active_collection=False):
    pathList = filePath.split(".")
    jsonPath = ""
    for x in range(len(pathList)-1):
        jsonPath += pathList[x]
    jsonPath += ".json"

    build_json(jsonPath, delete_json)

    if export_gr2:
        gr2Path = ""
        for x in range(len(pathList)-1):
            gr2Path += pathList[x]
            gr2Path += ".gr2"

        print('\nTool Path... %r' % toolPath)

        build_gr2(toolPath, filePath, jsonPath, gr2Path)
        if(file_exists(gr2Path)):
            report({'INFO'},"GR2 conversion finished!")
        else:
            report({'INFO'},"GR2 conversion failed!")
            ctypes.windll.user32.MessageBoxW(0, "Tool.exe failed to export your GR2 file. Blender may need to be run as an Administrator or there may be an issue with your project settings.", "GR2 EXPORT FAILED", 0)
        
        if delete_fbx:
            os.remove(filePath)
    return {'FINISHED'}

def build_json(jsonPath, delete_json, use_selection=False, use_visible=False, use_active_collection=False):
    jsonTemp = {}
    jsonTemp.update(getStrings())
    jsonTemp.update(getNodes())
    jsonTemp.update(getMeshes(use_selection, use_visible, use_active_collection))
    jsonTemp.update(getMaterials())

    if(delete_json):
        temp = tempfile.NamedTemporaryFile(delete=False, mode="w+", suffix=".json")
        json.dump(jsonTemp, temp)
        temp.flush()
        return temp.name
    else:
        haloJSON = json.dumps(jsonTemp, indent=4)

        jsonFile = open(jsonPath, "w")
        jsonFile.write(haloJSON)
        jsonFile.close()
        return ""

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

def save(operator, context, report,
        filepath="",
        use_selection=False,
        use_visible=False,
        use_active_collection=False,
        batch_mode='OFF',
        use_batch_own_dir=False,
        export_gr2=False,
        delete_fbx=False,
        delete_json=False,
        **kwargs
        ):
    export_asset(report, filepath, export_gr2, delete_fbx, delete_json, use_selection, use_visible, use_active_collection)
    return {'FINISHED'}

