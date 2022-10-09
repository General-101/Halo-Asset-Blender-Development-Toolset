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
from os import path
import csv
from math import radians
from mathutils import Matrix
#from . import HREKPath
###########
##GLOBALS##
###########

# Main Prefixes #
frame_prefixes = ('b ', 'b_', 'frame ', 'frame_','bip ','bip_','bone ','bone_')
marker_prefixes = ('#')
mesh_prefixes = ('+soft_ceiling','+soft_kill','+slip_surface', '@','+cookie','+decorator','+flair', '%', '$','+fog','+portal', '+seam','+water', '\'')
special_prefixes = ('b ', 'b_', 'frame ', 'frame_','bip ','bip_','bone ','bone_','#','+soft_ceiling','+soft_kill','+slip_surface', '@','+cookie','+decorator','+flair', '%', '$','+fog','+portal', '+seam','+water', '\'')


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
special_materials = ('+collision', '+physics', '+portal', '+seamsealer','+sky', '+slip_surface', '+soft_ceiling', '+soft_kill', '+weatherpoly')
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
        return True
    else:
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

def GetSceneArmature():
    model_armature = None
    for ob in bpy.data.objects:
        if ob.type == 'ARMATURE':
            model_armature = ob
            break
    return model_armature

def GetPrefix(string, prefix_list): # gets a prefix from a list of prefixes
    prefix = ''
    for p in prefix_list:
        if string.startswith(p):
            prefix = p
            break
    
    return prefix


def SelectModelObject(perm, arm, export_hidden, export_all_perms, export_specific_perm, select_func):
    DeselectAllObjects()
    perm = ResetPerm(perm)
    boolean = False
    select_func = getattr(sel_logic, select_func)
    arm.select_set(True)
    for ob in bpy.data.objects:
        halo = ob.halo_json
        if ObjectValid(ob, export_hidden, perm, halo.Permutation_Name) and select_func(ob) and ExportPerm(perm, export_all_perms, export_specific_perm):
            ob.select_set(True)
            boolean = True
    
    return boolean

def SelectModelObjectNoPerm(arm, export_hidden, select_func):
    DeselectAllObjects()
    boolean = False
    select_func = getattr(sel_logic, select_func)
    arm.select_set(True)
    for ob in bpy.data.objects:
        if ObjectValid(ob, export_hidden) and select_func(ob):
            ob.select_set(True)
            boolean = True

    return boolean

def SelectBSPObject(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp, select_func):
    DeselectAllObjects()
    perm = ResetPerm(perm)
    boolean = False
    select_func = getattr(sel_logic, select_func)
    for ob in bpy.data.objects:
        halo = ob.halo_json
        if halo.bsp_index == index:
            if ObjectValid(ob, export_hidden, perm, halo.Permutation_Name) and select_func(ob) and ExportPerm(perm, export_all_perms, export_specific_perm) and ExportBSP(index, export_all_bsps, export_specific_bsp):
                ob.select_set(True)
                boolean = True

    return boolean


def DeselectAllObjects():
    bpy.ops.object.select_all(action='DESELECT')


#############
##CHECK TYPES##
#############


class sel_logic():
    def ObRender(ob):
        return MeshType(ob, ('DEFAULT'))

    def ObCollision(ob):
        return MeshType(ob, ('COLLISION'), ('@'))

    def ObPhysics(ob):
        return MeshType(ob, ('PHYSICS'), ('$'))

    def ObMarkers(ob):
        return (ObjectType(ob, ('MARKER'), ('#')) or MeshType(ob, ('MARKER'), ('#'))) and NotParentedToPoop(ob)

    def ObStructure(ob):
        return MeshType(ob, ('DEFAULT')) and NotParentedToPoop(ob)

    def ObPoops(ob):
        return MeshType(ob, ('INSTANCED GEOMETRY', 'INSTANCED GEOMETRY COLLISION', 'INSTANCED GEOMETRY PHYSICS', 'INSTANCED GEOMETRY MARKER'), ('%', '@', '$'))

    def ObLights(ob):
        return ObjectType(ob)

    def ObPortals(ob):
        return MeshType(ob, ('PORTAL'), ('+portal')) and NotParentedToPoop(ob)

    def ObSeams(ob):
        return MeshType(ob, ('SEAM'), ('+seam')) and NotParentedToPoop(ob)

    def ObWaterSurfaces(ob):
        return MeshType(ob, ('WATER SURFACE'), ('\'')) and NotParentedToPoop(ob)

    def ObLightMapRegions(ob):
        return MeshType(ob, ('LIGHTMAP REGION')) and NotParentedToPoop(ob)

    def ObFog(ob):
        return MeshType(ob, ('PLANAR FOG VOLUME'), ('+fog')) and NotParentedToPoop(ob)

    def ObCookie(ob):
        return MeshType(ob, ('COOKIE CUTTER'), ('+cookie'))

    def ObBoundarys(ob):
        return MeshType(ob, ('BOUNDARY SURFACE'), ('+soft_kill', '+soft_ceiling', '+slip_surface')) and NotParentedToPoop(ob)

    def ObWaterPhysics(ob):
        return MeshType(ob, ('WATER PHYSICS VOLUME'), ('+water')) and NotParentedToPoop(ob)

    def ObPoopRains(ob):
        return MeshType(ob, ('INSTANCED GEOMETRY RAIN BLOCKER', 'INSTANCED GEOMETRY VERTICAL RAIN SHEET'))

    def ObFrames(ob):
        return ObjectType(ob, ('FRAME'), (frame_prefixes)) and NotParentedToPoop(ob)



def IsMesh(ob):
    return ob.type == 'MESH'

def MeshType(ob, types, valid_prefixes=()):
    if ob != None: # temp work around for 'ob' not being passed between functions correctly, and resolving to a NoneType
        return IsMesh(ob) and ((ob.halo_json.ObjectMesh_Type in types and not ObjectPrefix(ob, special_prefixes)) or ObjectPrefix(ob, valid_prefixes))

def ObjectType(ob, types=(), valid_prefixes=()):
    if ob != None: # temp work around for 'ob' not being passed between functions correctly, and resolving to a NoneType
        if ob.type == 'MESH':
            return ob.halo_json.Object_Type_All in types and not ObjectPrefix(ob, ((frame_prefixes, marker_prefixes)))
        elif ob.type == 'EMPTY':
            return ob.halo_json.Object_Type_No_Mesh in types or ObjectPrefix(ob, (valid_prefixes))
        elif ob.type == 'LIGHT':
            return True
        elif ob.halo_json.Object_Type_All in types or ObjectPrefix(ob, (valid_prefixes)):
            return True
        else:
            return False

def ObjectPrefix(ob, prefixes):
    return ob.name.startswith(prefixes)

def NotParentedToPoop(ob):
    return (not MeshType(ob.parent, 'INSTANCED GEOMETRY') or (ObjectPrefix(ob.parent, special_prefixes) and not ObjectPrefix(ob.parent, '%')))

def FixMarkersRotation(model_armature, is_model, pivot):
    DeselectAllObjects()
    angle = radians(-90)
    axis = (0, 0, 1)
    markers_list = []
    pivot_reset = pivot
    for ob in bpy.data.objects:
        if sel_logic.ObMarkers(ob):
            if is_model:
                if ob.parent_type == 'BONE' and ob.parent_bone != '':
                    bone_name = ob.parent_bone
                    pivot = model_armature.data.bones[bone_name].vector
            M = (
                Matrix.Translation(pivot) @
                Matrix.Rotation(angle, 4, axis) @       
                Matrix.Translation(-pivot)
                )
            ob.matrix_world = M @ ob.matrix_world
            markers_list.append(ob)
            pivot = pivot_reset

    return markers_list


def RestoreMarkersRotation(model_armature, is_model, pivot, markers_list):
    DeselectAllObjects()
    angle = radians(90)
    axis = (0, 0, 1)
    pivot_reset = pivot
    for ob in markers_list:
        if is_model:
            if ob.parent_type == 'BONE' and ob.parent_bone != '':
                bone_name = ob.parent_bone
                pivot = model_armature.data.bones[bone_name].vector
        M = (
            Matrix.Translation(pivot) @
            Matrix.Rotation(angle, 4, axis) @       
            Matrix.Translation(-pivot)
            )
        ob.matrix_world = M @ ob.matrix_world
        pivot = pivot_reset

#############
#BONE SORTING#
#############


def GetBoneList(model_armature, deform_only):
    boneslist = {}
    arm = model_armature.name
    boneslist.update({arm: getArmatureProperties()})
    index = 0
    frameIDs = openCSV() #sample function call to get FrameIDs CSV values as dictionary
    f1 = frameIDs.keys()
    f2 = frameIDs.values()
    bone_list = model_armature.data.bones
    #bone_list = 
    #bone_list = SortList(model_armature)
    if deform_only:
        bone_list = GetDeformBonesOnly(bone_list)
    for b in bone_list:
        if b.halo_json.frame_id1 == '':
            FrameID1 = list(f1)[index]
        else:
            FrameID1 = b.halo_json.frame_id1
        if b.halo_json.frame_id2 == '':
            FrameID2 = list(f2)[index]
        else:
            FrameID2 = b.halo_json.frame_id2
        index +=1
        boneslist.update({b.name: getBoneProperties(FrameID1, FrameID2)})

    return boneslist

def GetDeformBonesOnly(bone_list):
    deform_list = []
    for b in bone_list:
        if b.use_deform:
            deform_list.append(b)
    
    return deform_list
        

def getArmatureProperties():
    node_props = {}

    node_props.update({"bungie_object_type": "_connected_geometry_object_type_frame"}),
    node_props.update({"bungie_frame_ID1": "8078"}),
    node_props.update({"bungie_frame_ID2": "378163771"}),

    return node_props

def getBoneProperties(FrameID1, FrameID2):
    node_props = {}

    node_props.update({"bungie_object_type": "_connected_geometry_object_type_frame"}),
    node_props.update({"bungie_frame_ID1": FrameID1}),
    node_props.update({"bungie_frame_ID2": FrameID2}),

    return node_props

def openCSV():
    script_folder_path = path.dirname(path.dirname(__file__))
    filepath = path.join(script_folder_path, "io_scene_halo\\file_gr2", "frameidlist.csv")

    frameIDList = {}
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            frameIDList.update({row[0]: row[1]})

    return frameIDList


class Halo_Bones():
    def __init__(self):
        self.nodes = []

    class Node:
        def __init__(self, name, children=None, child=-1, sibling=-1, parent=-1):
            self.name = name
            self.children = children
            self.child = child
            self.sibling = sibling
            self.parent = parent
            self.visited = False

    def __iter__(self):
        return self


def SortList(model_armature):

    halo_bones = []

    sorted_list = bone_sort_by_layer(model_armature.data.bones, model_armature)
    joined_list = sorted_list[0]
    reversed_joined_list = sorted_list[1]
    node_list = []
    for node in joined_list:
        is_bone = False
        if model_armature:
            is_bone = True

        find_child_node = get_sorted_child(node, reversed_joined_list)
        find_sibling_node = get_sorted_sibling(model_armature, node, reversed_joined_list)

        first_child_node = -1
        first_sibling_node = -1
        parent_node = -1

        if not find_child_node == None:
            first_child_node = joined_list.index(find_child_node)
        if not find_sibling_node == None:
            first_sibling_node = joined_list.index(find_sibling_node)
        if not node.parent == None and not node.parent.name.startswith('!'):
            parent_node = joined_list.index(node.parent)

        name = node.name
        child = first_child_node
        sibling = first_sibling_node
        parent = parent_node

        current_node_children = []
        children = []
        for child_node in node.children:
            if child_node in joined_list:
                current_node_children.append(child_node.name)

        current_node_children.sort()

        if is_bone:
            for child_node in current_node_children:
                children.append(joined_list.index(model_armature.data.bones[child_node]))

        else:
            for child_node in current_node_children:
                children.append(joined_list.index(bpy.data.objects[child_node]))
        
        halo_bones.append(name)

    return halo_bones

def get_sorted_child(bone, bone_list):
    set_node = None
    child_nodes = []
    for node in bone_list:
        if bone == node.parent:
            child_nodes.append(node)

    child_nodes = sorted(child_nodes, key=lambda x: x.name)
    if len(child_nodes) > 0:
        set_node = child_nodes[0]

    return set_node

def get_sorted_sibling(armature, bone, bone_list):
    sibling_list = []
    set_sibling = None
    for node in bone_list:
        if bone.parent == node.parent:
            sibling_list.append(node)

    sibling_list = sorted(sibling_list, key=lambda x: x.name)
    if len(sibling_list) > 1:
        sibling_node = sibling_list.index(bone)
        next_sibling_node = sibling_node + 1
        if next_sibling_node >= len(sibling_list):
            set_sibling = None

        else:
            if armature:
                set_sibling = armature.data.bones['%s' % sibling_list[next_sibling_node].name]

            else:
                set_sibling = bpy.data.objects['%s' % sibling_list[next_sibling_node].name]

    return set_sibling

def bone_sort_by_layer(node_list, armature):
    layer_count = []
    layer_root = []
    root_list = []
    children_list = []
    reversed_children_list = []
    joined_list = []
    reversed_joined_list = []
    sort_list = []
    reversed_sort_list = []
    for node in node_list:
        if node.parent == None and not node.name[0:1] == '!' or node.parent.name[0:1] == '!' and node.parent.parent == None:
            layer_count.append(None)
            layer_root.append(node)

        else:
            if not node.parent in layer_count:
                layer_count.append(node.parent)

    for layer in layer_count:
        joined_list = root_list + children_list
        reversed_joined_list = root_list + reversed_children_list
        layer_index = layer_count.index(layer)
        if layer_index == 0:
            if armature:
                root_list.append(armature.data.bones[0])

            else:
                root_list.append(layer_root[0])

        else:
            for node in node_list:
                if armature:
                    if node.parent != None:
                        if armature.data.bones['%s' % node.parent.name] in joined_list and not node in children_list:
                            sort_list.append(node.name)
                            reversed_sort_list.append(node.name)

                else:
                    if node.parent != None:
                        if node.parent in joined_list and not node in children_list:
                            sort_list.append(node.name)
                            reversed_sort_list.append(node.name)

            sort_list.sort()
            reversed_sort_list.sort()
            # reversed_sort_list.reverse()
            for sort in sort_list:
                if armature:
                    if not armature.data.bones['%s' % sort] in children_list:
                        children_list.append(armature.data.bones['%s' % sort])

                else:
                    if not bpy.data.objects[sort] in children_list:
                        children_list.append(bpy.data.objects[sort])

            for sort in reversed_sort_list:
                if armature:
                    if not armature.data.bones['%s' % sort] in reversed_children_list:
                        reversed_children_list.append(armature.data.bones['%s' % sort])

                else:
                    if not bpy.data.objects[sort] in reversed_children_list:
                        reversed_children_list.append(bpy.data.objects[sort])

        joined_list = root_list + children_list
        reversed_joined_list = root_list + reversed_children_list

    return (joined_list, reversed_joined_list)

def SetBoneJSONValues(bones):
    print('tbd')


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