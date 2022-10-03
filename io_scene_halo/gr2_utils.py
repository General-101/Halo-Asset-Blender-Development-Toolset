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
import platform
import os
#from . import HREKPath
###########
##GLOBALS##
###########

# Main Prefixes #
frame_prefixes = ('b ', 'b_', 'frame ', 'frame_','bip ','bip_','bone ','bone_')
marker_prefixes = ('#')
mesh_prefixes = ('+soft_ceiling','+soft_kill','+slip_surface', '@','+cookie','+decorator','+flair', '%', '$','+fog','+portal', '+seam','+water', '\'')
special_prefixes = (str(frame_prefixes), str(marker_prefixes), str(mesh_prefixes))


# Specific Mesh Prefixes #
boundary_surface_prefixes = ('+soft_ceiling','+soft_kill','+slip_surface') # boundary surface prefixes can take a name with +prefix:name e.g. +soft_ceiling:camera_ceiling_01
cookie_cutter_prefixes = ('+cookie')
decorator_prefixes = ('+decorator') # decorators can take a name with +decorator:name (not implemented)
fog_volume_prefixes = ('+fog') # fog volumes can take a name with +fog:name (not implemented)
object_instance_prefixes = ('+flair') # self-reminder: Flairs need to have marker_regions written to them in the json, this should match the face region
portal_prefixes = ('+portal') # portals can have properties automatically through the object name (once I get around to adding it)
seam_prefixes = ('+seam') # seams can take a name with +seam:name
water_volume_prefixes = ('+water')

no_perm_prefixes = ((frame_prefixes, marker_prefixes, boundary_surface_prefixes, decorator_prefixes, fog_volume_prefixes, portal_prefixes, seam_prefixes, water_volume_prefixes, cookie_cutter_prefixes, '+water', '\''))
# Instanced Geo Prefixes #
poop_lighting_prefixes = ('%!',     '%-!','%+!','%*!',     '%-*!','%+*!',     '%*-!','%*+!',          '%?',     '%-?','%+?','%*?',     '%-*?','%+*?',     '%*-?','%*+?'          '%>',     '%->','%+>','%*>',     '%-*>','%+*>',     '%*->','%*+>')
poop_pathfinding_prefixes = ('%+',     '%!+','%?+','%>+','%*+',     '%!*+','%?*+','%>*+',     '%*!+','%*?+','%*>+',          '%-',     '%!-','%?-','%>-','%*-',     '%!*-','%?*-','%>*-',     '%*!-','%*?-','%*>-')
poop_render_only_prefixes = ('%*',     '%!*','%?*','%>*','%-*','%+*',     '%!-*','%!+*','%?-*','%?+*','%>-*','%>+*')
# Material Prefixes #
special_materials = ('+collision', '+physics', '+portal','+seamsealer','+sky','+weatherpoly')
# Enums #
special_mesh_types = ('BOUNDARY SURFACE','DECORATOR','INSTANCED GEOMETRY','PLANAR FOG VOLUME','PORTAL','SEAM','WATER PHYSICS VOLUME',)
invalid_mesh_types = ('BOUNDARY SURFACE', 'COOKIE CUTTER', 'INSTANCED GEOMETRY MARKER', 'INSTANCED GEOMETRY RAIN BLOCKER', 'INSTANCED GEOMETRY VERTICAL RAIN SHEET', 'LIGHTMAP REGION', 'PLANAR FOG VOLUME', 'PORTAL', 'SEAM', 'WATER PHYSICS VOLUME')
# animations #
valid_animation_types = ('JMM', 'JMA', 'JMT', 'JMZ', 'JMV', 'JMO', 'JMOX', 'JMR', 'JMRX')
#############
##FUNCTIONS##
#############

def GetEKPath():
    #scene = bpy.context.scene
    #scene_halo = scene.halo
    #if scene_halo.game_version == 'reach':
    EKPath = bpy.context.preferences.addons[__package__].preferences.hrek_path

    EKPath = EKPath.replace('"','')
    EKPath = EKPath.strip('\\')

    return EKPath

def GetToolPath():
    EKPath = GetEKPath()
    toolPath = EKPath + '\\tool_fast.exe'

    return toolPath

def GetTagsPath():
    EKPath = GetEKPath()
    tagsPath = EKPath + '\\tags\\'

    return tagsPath

def GetDataPath():
    EKPath = GetEKPath()
    dataPath = EKPath + '\\data\\'

    return dataPath

def GetPerm(ob): # get the permutation of an object, return default if the perm is empty
    if ob.halo_json.Permutation_Name == '':
        perm = 'default'
    else:
        perm = ob.halo_json.Permutation_Name

    return perm

def IsWindows():
    if(platform.system() == 'Windows'):
        return True
    else:
        return False

def CheckPath(filePath):
    if(filePath.startswith(os.path.abspath(GetEKPath() + "\\data")+os.sep)):
        print("Is Valid")
        return True
    else:
        print("Not Valid!")
        return False

def ObjectValid(ob, export_hidden, valid_perm='', evaluated_perm=''):
    return ob in tuple(bpy.data.scenes[0].view_layers[0].objects) and (ob.visible_get() or export_hidden) and valid_perm == evaluated_perm

def ExportPerm(perm, export_all_perms, export_specific_perm):
    return export_all_perms or perm == export_specific_perm

def ExportBSP(bsp, export_all_bsps, export_specific_bsp):
    return export_all_bsps or bsp == export_specific_bsp

def ResetPerm(perm): # resets a permutation to '' if it had been set to default
    if perm == 'default':
        perm = ''
    
    return perm

#############
##CHECK TYPES##
#############

def ObStructure(ob):
    return (
        (not ob.name.startswith(special_prefixes) or (ob.name.startswith('@') and not ob.parent.name.startswith('%'))) 
        or
        (not ob.name.startswith(special_prefixes) and (ob.halo_json.ObjectMesh_Type in ('DEFAULT', 'COLLISION')))
    )

#################################

# import example #
# from ..gr2_utils import (
#     frame_prefixes,
#     marker_prefixes,
#     mesh_prefixes,
#     special_prefixes,
#     boundary_surface_prefixes,
#     cookie_cutter_prefixes,
#     decorator_prefixes,
#     fog_volume_prefixes,
#     object_instance_prefixes,
#     portal_prefixes,
#     seam_prefixes,
#     water_volume_prefixes,
#     no_perm_prefixes,
#     poop_lighting_prefixes,
#     poop_pathfinding_prefixes,
#     poop_render_only_prefixes,
#     special_materials,
#     special_mesh_types,
#     invalid_mesh_types,
#     GetEKPath,
#     GetToolPath,
#     GetTagsPath,
#     GetDataPath,
#     GetPerm,
#     IsWindows,
#     CheckPath,
#     ObjectValid,
#     ExportPerm,
#     ExportBSP,
#     ResetPerm,
# )