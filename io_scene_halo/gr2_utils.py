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
from math import radians
from mathutils import Matrix
import os

###########
##GLOBALS##
###########

# Main Prefixes #
frame_prefixes = ('b ', 'b_', 'frame ', 'frame_','bip ','bip_','bone ','bone_')
marker_prefixes = ('#', '+tag')
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
special_materials = ('+collision', '+physics', '+portal', '+seamsealer','+sky', '+slip_surface', '+soft_ceiling', '+soft_kill', '+weatherpoly', '+override')
# Enums #
special_mesh_types = ('BOUNDARY SURFACE', 'COLLISION','DECORATOR','INSTANCED GEOMETRY','PLANAR FOG VOLUME','PORTAL','SEAM','WATER PHYSICS VOLUME',)
invalid_mesh_types = ('BOUNDARY SURFACE', 'COOKIE CUTTER', 'INSTANCED GEOMETRY MARKER', 'INSTANCED GEOMETRY RAIN BLOCKER', 'INSTANCED GEOMETRY VERTICAL RAIN SHEET', 'LIGHTMAP REGION', 'PLANAR FOG VOLUME', 'PORTAL', 'SEAM', 'WATER PHYSICS VOLUME')
# animations #
valid_animation_types = ('JMM', 'JMA', 'JMT', 'JMZ', 'JMV', 'JMO', 'JMOX', 'JMR', 'JMRX')

# shader exts #
shader_exts = ('.shader', '.shader_cortana', 'shader_custom', 'shader_decal', '.shader_foliage', '.shader_fur', '.shader_fur_stencil', '.shader_glass', '.shader_halogram', '.shader_mux', '.shader_mux_material', '.shader_screen', '.shader_skin', '.shader_terrain', '.shader_water', '.material')

#############
##FUNCTIONS##
#############

def GetEKPath():
    scene = bpy.context.scene
    scene_halo = scene.halo
    if scene_halo.game_version == 'h4':
        EKPath = bpy.context.preferences.addons[__package__].preferences.h4ek_path
    elif scene_halo.game_version == 'h2a':
        EKPath = bpy.context.preferences.addons[__package__].preferences.h2aek_path
    else:
        EKPath = bpy.context.preferences.addons[__package__].preferences.hrek_path

    EKPath = EKPath.replace('"','')
    EKPath = EKPath.strip('\\')

    return EKPath

def GetToolPath():
    EKPath = GetEKPath()
    toolPath = os.path.join(EKPath, GetToolType)

    return toolPath

def GetTagsPath():
    EKPath = GetEKPath()
    tagsPath = os.path.join(EKPath, 'tags', '')

    return tagsPath

def GetDataPath():
    EKPath = GetEKPath()
    dataPath = os.path.join(EKPath, 'data', '')

    return dataPath

def GetToolType():
    return bpy.context.preferences.addons[__package__].preferences.tool_type

def GetPerm(ob): # get the permutation of an object, return default if the perm is empty
    perm = 'default'
    if ob.halo_json.Permutation_Name_Locked != '':
        perm = ob.halo_json.Permutation_Name_Locked

    elif ob.halo_json.Permutation_Name != '':
            perm = ob.halo_json.Permutation_Name
        
    return perm

def IsWindows():
    return platform.system() == 'Windows'

def ObjectValid(ob, export_hidden, valid_perm='', evaluated_perm='', evalued_perm_locked = ''):
    if evalued_perm_locked != '':
        return ob in tuple(bpy.context.scene.view_layers[0].objects) and (ob.visible_get() or export_hidden) and valid_perm == evalued_perm_locked
    else:
        return ob in tuple(bpy.context.scene.view_layers[0].objects) and (ob.visible_get() or export_hidden) and valid_perm == evaluated_perm

def ExportPerm(perm, export_all_perms, export_specific_perm):
    return export_all_perms or perm == export_specific_perm

def ExportBSP(bsp, export_all_bsps, export_specific_bsp):
    return export_all_bsps or bsp == export_specific_bsp

def ResetPerm(perm): # resets a permutation to '' if it had been set to default
    if perm == 'default':
        perm = ''
    
    return perm

def GetPrefix(string, prefix_list): # gets a prefix from a list of prefixes
    prefix = ''
    for p in prefix_list:
        if string.startswith(p):
            prefix = p
            break
    
    return prefix

def SelectHaloObject(select_func, selected_asset_type, valid_asset_types):
    DeselectAllObjects()
    select_func = getattr(sel_logic, select_func)
    halo_objects = []
    if selected_asset_type in valid_asset_types:
        for ob in bpy.context.view_layer.objects:
            if select_func(ob):
                halo_objects.append(ob) 
    
    return halo_objects


def SelectModelObject(halo_objects, perm, arm, export_hidden, export_all_perms, export_specific_perm):
    DeselectAllObjects()
    perm = ResetPerm(perm)
    boolean = False
    arm.select_set(True)
    for ob in halo_objects:
        halo = ob.halo_json
        if ObjectValid(ob, export_hidden, perm, halo.Permutation_Name, halo.Permutation_Name_Locked) and ExportPerm(perm, export_all_perms, export_specific_perm):
            ob.select_set(True)
            boolean = True
    
    return boolean

def SelectModelObjectNoPerm(halo_objects, arm, export_hidden):
    DeselectAllObjects()
    boolean = False
    arm.select_set(True)
    for ob in halo_objects:
        if ObjectValid(ob, export_hidden):
            ob.select_set(True)
            boolean = True

    return boolean

def SelectBSPObject(halo_objects, bsp, arm, shared, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
    DeselectAllObjects()
    perm = ResetPerm(perm)
    boolean = False
    if arm is not None:
        arm.select_set(True)
    for ob in halo_objects:
        halo = ob.halo_json
        if halo.bsp_name_locked != '':
            bsp_value = halo.bsp_name_locked
        else:
            bsp_value = halo.bsp_name
        if bsp_value == bsp or shared:
            if ObjectValid(ob, export_hidden, perm, halo.Permutation_Name, halo.Permutation_Name_Locked) and ExportPerm(perm, export_all_perms, export_specific_perm) and ExportBSP(bsp, export_all_bsps, export_specific_bsp):
                ob.select_set(True)
                boolean = True

    return boolean


def DeselectAllObjects():
    bpy.ops.object.select_all(action='DESELECT')

def SelectAllObjects():
    bpy.ops.object.select_all(action='SELECT')

def SetActiveObject(ob):
    bpy.context.view_layer.objects.active = ob

def GetActiveObject():
    return bpy.context.view_layer.objects.active

def GetAssetInfo(filepath):
    asset_path = filepath.rpartition('\\')[0]
    asset = asset_path.rpartition('\\')[2]
    asset = asset.replace('.fbx', '')

    return asset_path, asset

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
        return MeshType(ob, ('INSTANCED GEOMETRY', 'COLLISION', 'PHYSICS', 'INSTANCED GEOMETRY MARKER', 'COOKIE CUTTER'), ('%', '@', '$', '+cookie'))

    def ObPoopsOnly(ob):
        return MeshType(ob, ('INSTANCED GEOMETRY'), ('%'))

    def ObPoopsCollPhys(ob):
        return MeshType(ob, ('COLLISION', 'PHYSICS'), ('@', '$'))

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

    def ObBoundarys(ob):
        return MeshType(ob, ('BOUNDARY SURFACE'), ('+soft_kill', '+soft_ceiling', '+slip_surface')) and NotParentedToPoop(ob)

    def ObWaterPhysics(ob):
        return MeshType(ob, ('WATER PHYSICS VOLUME'), ('+water')) and NotParentedToPoop(ob)

    def ObPoopRains(ob):
        return MeshType(ob, ('INSTANCED GEOMETRY RAIN BLOCKER', 'INSTANCED GEOMETRY VERTICAL RAIN SHEET'))

    def ObFrames(ob):
        return ObjectType(ob, ('FRAME'), (frame_prefixes)) and NotParentedToPoop(ob)

    def ObDecorator(ob):
        return MeshType(ob, ('DECORATOR'), (decorator_prefixes))

    def ObPoopCollision(ob):
        return MeshType(ob, ('COLLISION'), ('@'))

    def ObPoopPhysics(ob):
        return MeshType(ob, ('PHYSICS'), ('$'))

    def ObCookie(ob):
        return MeshType(ob, ('COOKIE CUTTER'), ('+cookie'))



def IsMesh(ob):
    return ob.type == 'MESH'

def MeshType(ob, types, valid_prefixes=()):
    if ob != None: # temp work around for 'ob' not being passed between functions correctly, and resolving to a NoneType
        return IsMesh(ob) and ((ob.halo_json.ObjectMesh_Type in types and not ObjectPrefix(ob, special_prefixes)) or ObjectPrefix(ob, valid_prefixes))

def ObjectType(ob, types=(), valid_prefixes=()):
    if ob != None: # temp work around for 'ob' not being passed between functions correctly, and resolving to a NoneType
        if ob.type == 'MESH':
            return ob.halo_json.Object_Type_All in types and not ObjectPrefix(ob, ((frame_prefixes + marker_prefixes)))
        elif ob.type == 'EMPTY':
            return ob.halo_json.Object_Type_No_Mesh in types or ObjectPrefix(ob, (valid_prefixes))
        elif ob.type == 'LIGHT' and (types != 'MARKER' and '#' not in valid_prefixes):
            return True
        elif ob.halo_json.Object_Type_All in types or ObjectPrefix(ob, (valid_prefixes)):
            return True
        else:
            return False

def ObjectPrefix(ob, prefixes):
    return ob.name.startswith(prefixes)

def NotParentedToPoop(ob):
    return (not MeshType(ob.parent, 'INSTANCED GEOMETRY') or (ObjectPrefix(ob.parent, special_prefixes) and not ObjectPrefix(ob.parent, '%')))

def IsDesign(ob):
    return sel_logic.ObFog(ob) or sel_logic.ObBoundarys(ob) or sel_logic.ObWaterPhysics(ob) or sel_logic.ObPoopRains(ob)

#############
#BONE SORTING#
#############





# class Halo_Bones():
#     def __init__(self):
#         self.nodes = []

#     class Node:
#         def __init__(self, name, children=None, child=-1, sibling=-1, parent=-1):
#             self.name = name
#             self.children = children
#             self.child = child
#             self.sibling = sibling
#             self.parent = parent
#             self.visited = False

#     def __iter__(self):
#         return self


# def SortList(model_armature):

#     halo_bones = []

#     sorted_list = bone_sort_by_layer(model_armature.data.bones, model_armature)
#     joined_list = sorted_list[0]
#     reversed_joined_list = sorted_list[1]
#     node_list = []
#     for node in joined_list:
#         is_bone = False
#         if model_armature:
#             is_bone = True

#         find_child_node = get_sorted_child(node, reversed_joined_list)
#         find_sibling_node = get_sorted_sibling(model_armature, node, reversed_joined_list)

#         first_child_node = -1
#         first_sibling_node = -1
#         parent_node = -1

#         if not find_child_node == None:
#             first_child_node = joined_list.index(find_child_node)
#         if not find_sibling_node == None:
#             first_sibling_node = joined_list.index(find_sibling_node)
#         if not node.parent == None and not node.parent.name.startswith('!'):
#             parent_node = joined_list.index(node.parent)

#         name = node.name
#         child = first_child_node
#         sibling = first_sibling_node
#         parent = parent_node

#         current_node_children = []
#         children = []
#         for child_node in node.children:
#             if child_node in joined_list:
#                 current_node_children.append(child_node.name)

#         current_node_children.sort()

#         if is_bone:
#             for child_node in current_node_children:
#                 children.append(joined_list.index(model_armature.data.bones[child_node]))

#         else:
#             for child_node in current_node_children:
#                 children.append(joined_list.index(bpy.data.objects[child_node]))
        
#         halo_bones.append(name)

#     return halo_bones

# def get_sorted_child(bone, bone_list):
#     set_node = None
#     child_nodes = []
#     for node in bone_list:
#         if bone == node.parent:
#             child_nodes.append(node)

#     child_nodes = sorted(child_nodes, key=lambda x: x.name)
#     if len(child_nodes) > 0:
#         set_node = child_nodes[0]

#     return set_node

# def get_sorted_sibling(armature, bone, bone_list):
#     sibling_list = []
#     set_sibling = None
#     for node in bone_list:
#         if bone.parent == node.parent:
#             sibling_list.append(node)

#     sibling_list = sorted(sibling_list, key=lambda x: x.name)
#     if len(sibling_list) > 1:
#         sibling_node = sibling_list.index(bone)
#         next_sibling_node = sibling_node + 1
#         if next_sibling_node >= len(sibling_list):
#             set_sibling = None

#         else:
#             if armature:
#                 set_sibling = armature.data.bones['%s' % sibling_list[next_sibling_node].name]

#             else:
#                 set_sibling = bpy.data.objects['%s' % sibling_list[next_sibling_node].name]

#     return set_sibling

# def bone_sort_by_layer(node_list, armature):
#     layer_count = []
#     layer_root = []
#     root_list = []
#     children_list = []
#     reversed_children_list = []
#     joined_list = []
#     reversed_joined_list = []
#     sort_list = []
#     reversed_sort_list = []
#     for node in node_list:
#         if node.parent == None and not node.name[0:1] == '!' or node.parent.name[0:1] == '!' and node.parent.parent == None:
#             layer_count.append(None)
#             layer_root.append(node)

#         else:
#             if not node.parent in layer_count:
#                 layer_count.append(node.parent)

#     for layer in layer_count:
#         joined_list = root_list + children_list
#         reversed_joined_list = root_list + reversed_children_list
#         layer_index = layer_count.index(layer)
#         if layer_index == 0:
#             if armature:
#                 root_list.append(armature.data.bones[0])

#             else:
#                 root_list.append(layer_root[0])

#         else:
#             for node in node_list:
#                 if armature:
#                     if node.parent != None:
#                         if armature.data.bones['%s' % node.parent.name] in joined_list and not node in children_list:
#                             sort_list.append(node.name)
#                             reversed_sort_list.append(node.name)

#                 else:
#                     if node.parent != None:
#                         if node.parent in joined_list and not node in children_list:
#                             sort_list.append(node.name)
#                             reversed_sort_list.append(node.name)

#             sort_list.sort()
#             reversed_sort_list.sort()
#             # reversed_sort_list.reverse()
#             for sort in sort_list:
#                 if armature:
#                     if not armature.data.bones['%s' % sort] in children_list:
#                         children_list.append(armature.data.bones['%s' % sort])

#                 else:
#                     if not bpy.data.objects[sort] in children_list:
#                         children_list.append(bpy.data.objects[sort])

#             for sort in reversed_sort_list:
#                 if armature:
#                     if not armature.data.bones['%s' % sort] in reversed_children_list:
#                         reversed_children_list.append(armature.data.bones['%s' % sort])

#                 else:
#                     if not bpy.data.objects[sort] in reversed_children_list:
#                         reversed_children_list.append(bpy.data.objects[sort])

#         joined_list = root_list + children_list
#         reversed_joined_list = root_list + reversed_children_list

#     return (joined_list, reversed_joined_list)

def SetBoneJSONValues(bones):
    print('tbd')

def HaloBoner(bones, model_armature, context):
    objects_in_scope = context.view_layer.objects
    ob_matrix = CreateObMatrixDict(objects_in_scope)
    SetActiveObject(model_armature)
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    for b in bones:
        pivot = b.head
        angle_x = radians(-90)
        axis_x = (1, 0, 0)
        M = (
            Matrix.Translation(pivot) @
            Matrix.Rotation(angle_x, 4, axis_x) @
            Matrix.Translation(-pivot)
            )
        b.matrix = M @ b.matrix

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    for ob in objects_in_scope:
        for key, value in ob_matrix.items():
            if key == ob:
                ob.matrix_world = value
                break

def HaloDeboner(bones, model_armature, context):
    objects_in_scope = context.view_layer.objects
    ob_matrix = CreateObMatrixDict(objects_in_scope)
    SetActiveObject(model_armature)
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    for b in bones:
        pivot = b.head
        angle_x = radians(90)
        axis_x = (1, 0, 0)
        M = (
            Matrix.Translation(pivot) @
            Matrix.Rotation(angle_x, 4, axis_x) @
            Matrix.Translation(-pivot)
            )
        b.matrix = M @ b.matrix

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    for ob in objects_in_scope:
        for key, value in ob_matrix.items():
            if key == ob:
                ob.matrix_world = value
                break

def HaloNoder(nodes, model_armature):
    SetActiveObject(model_armature)
    for n in nodes:
        pivot = model_armature.location
        angle_x = radians(-90)
        angle_z = radians(-180)
        axis_x = (1, 0, 0)
        axis_z = (0, 0, 1)
        M = (
            Matrix.Translation(pivot) @
            Matrix.Rotation(angle_x, 4, axis_x) @
            Matrix.Rotation(angle_z, 4, axis_z) @ 
            Matrix.Translation(-pivot)
            )
        n.matrix_world = M @ n.matrix_world

def HaloDenoder(nodes, model_armature):
    SetActiveObject(model_armature)
    for n in nodes:
        pivot = model_armature.location
        angle_x = radians(90)
        angle_z = radians(180)
        axis_x = (1, 0, 0)
        axis_z = (0, 0, 1)
        M = (
            Matrix.Translation(pivot) @
            Matrix.Rotation(angle_z, 4, axis_z) @ 
            Matrix.Rotation(angle_x, 4, axis_x) @
            Matrix.Translation(-pivot)
            )
        n.matrix_world = M @ n.matrix_world

def CreateObMatrixDict(objects_in_scope):
    ob_matrix = {}
    for ob in objects_in_scope:
        mtrx = Matrix(ob.matrix_world)
        ob_matrix.update({ob: mtrx})

    return ob_matrix

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


######################################
# MANAGER STUFF
######################################

def get_collection_parents(current_coll, all_collections):
    coll_list = [current_coll.name]
    keep_looping = True
    
    while keep_looping:
        for coll in all_collections:
            keep_looping = True
            if current_coll in tuple(coll.children):
                coll_list.append(coll.name)
                current_coll = coll
                break
            else:
                keep_looping = False

    return coll_list

def get_prop_from_collection(ob, prefixes):
    prop = ''
    if len(bpy.data.collections) > 0:
        collection = None
        all_collections = bpy.data.collections
        protected_word = 'default'
        if any(x in prefixes for x in ('+bsp:', '+design:')):
            protected_word = 'shared'
        # get direct parent collection
        for c in all_collections:
            if ob in tuple(c.objects):
                collection = c
                break
        # get collection parent tree
        if collection != None:
            collection_list = get_collection_parents(collection, all_collections)

            # test object collection parent tree
            for c in collection_list:
                if c.lower().startswith(prefixes[0]) or c.lower().startswith(prefixes[1]):
                    prop = c.rpartition(':')[2]
                    prop = prop.strip(' ')
                    prop = prop.replace(' ', '_')
                    prop = prop.lower()
                    if prop == protected_word:
                        prop = ''
                    break

    return prop


# returns true if this material is a halo shader
def IsShader(mat):
    halo_mat = mat.halo_json
    shader_path_not_empty = True if halo_mat.shader_path != '' else False
    no_material_override = True if halo_mat.material_override == 'NONE' else False
    no_special_material_name = True if not mat.name.lower().startswith(special_materials) else False

    return shader_path_not_empty and no_material_override and no_special_material_name