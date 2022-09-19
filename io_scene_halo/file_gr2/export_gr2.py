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

def getMeshes():
    meshesList = {}

    halo_node_prefixes = ('#','b_','b ','frame_','frame ') # these prefixes indicate a mesh should not be written to meshes_properties

    for mesh in bpy.data.meshes:
        if (not mesh.name.startswith(halo_node_prefixes)): # if the name of a mesh starts with this, don't process it.
            meshesList.update({mesh.name: getMeshProperties()})

    temp = ({'meshes_properties': meshesList})

    return temp

def getMeshProperties():
    print("here we go")

    mesh_props = {
        # OBJECT PROPERTIES
        "bungie_object_type": "_connected_geometry_object_type_mesh",
        "bungie_region_name": getRegionName(),
        # FACE PROPERTIES
        "bungie_face_type": getFaceType()

    }

    return mesh_props

def getRegionName():
    return 'region'

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
                    shaderPath = 'collision'
                elif halo_material_name.startswith('+physics') or halo_material.material_override == 'PHYSICS':
                    shaderPath = 'physics'
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

def export_asset(report, filePath="", export_gr2=False, delete_fbx=False, delete_json=False):
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

def build_json(jsonPath, delete_json):
    jsonTemp = {}
    jsonTemp.update(getStrings())
    jsonTemp.update(getNodes())
    jsonTemp.update(getMeshes())
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
    export_asset(report, filepath, export_gr2, delete_fbx, delete_json)
    return {'FINISHED'}

