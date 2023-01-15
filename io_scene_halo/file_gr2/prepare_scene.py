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
from os import path
import csv
from math import radians
from mathutils import Matrix, Vector
from uuid import uuid4
from .nwo_utils import(
    deselect_all_objects,
    is_mesh,
    set_active_object,
    CheckType,
    select_halo_objects,
    select_all_objects,
    is_shader,
    get_tags_path,
    not_bungie_game,
    true_region,
)
#####################################################################################
#####################################################################################
# MAIN FUNCTION
def prepare_scene(context, report, sidecar_type, export_hidden, filepath, use_armature_deform_only, game_version, meshes_to_empties, **kwargs):
    ExitLocalView(context)
    enabled_exclude_collections = HideExcludedCollections(context)
    objects_selection, active_object = GetCurrentActiveObjectSelection(context)
    hidden_objects = UnhideObjects(export_hidden, context)                               # If the user has opted to export hidden objects, list all hidden objects and unhide them, return the list for later use
    mode = GetSceneMode(context)                                                      # get the current selected mode, save the mode for later, and then switch to object mode
    unselectable_objects = MakeSelectable(context)
    # update bsp/perm/region/global mat names in case any are null
    for ob in context.scene.objects:
        if ob.nwo.bsp_name == '':
            ob.nwo.bsp_name = '000'
        if ob.nwo.Permutation_Name == '':
            ob.nwo.Permutation_Name = 'default'
        if ob.nwo.Region_Name == '':
            ob.nwo.Region_Name = 'default'
        # if ob.nwo.Face_Global_Material == '':
        #     ob.nwo.Face_Global_Material = 'default'
    
    ApplyObjectIDs(context.view_layer.objects)
    regions_dict = get_regions_dict(context.view_layer.objects)
    global_materials_dict = get_global_materials_dict(context.view_layer.objects)
    mesh_node_names = {}
    temp_nodes = []
    if meshes_to_empties:
        mesh_node_names, temp_nodes = MeshesToEmpties(context)
    halo_objects = HaloObjects(sidecar_type)
    FixMissingMaterials(context, sidecar_type)
    # proxies = SetPoopProxies(context, h_objects.poops) 02-01-2023 commenting this out as I don't believe the workflow should be this way. Also causes issues in H4
    # for p in proxies:
    #     h_objects.poops.append(p)
    model_armature, temp_armature, no_parent_objects = GetSceneArmature(context, sidecar_type, game_version)                          # return the main armature in the scene, and create a temp one if a model armature does not exist
    skeleton_bones = {}
    if model_armature is not None:
        ParentToArmature(model_armature, temp_armature, no_parent_objects, context)                             # ensure all objects are parented to an armature on export. Render and collision mesh is parented with armature deform, the rest uses bone parenting
        skeleton_bones = GetBoneList(model_armature, use_armature_deform_only)      # return a list of bones attached to the model armature, ignoring control / non-deform bones
    # HaloBoner(model_armature.data.edit_bones, model_armature, context)
    #FixLightsRotations(h_objects.lights)                                         # adjust light rotations to match in game rotation, and return a list of lights for later use in repair_scene
    timeline_start, timeline_end, current_frame = SetTimelineRange(context)                      # set the timeline range so we can restore it later
    lod_count = GetDecoratorLODCount(halo_objects, sidecar_type == 'DECORATOR SET') # get the max LOD count in the scene if we're exporting a decorator
    selected_perms = GetSelectedPermutations(objects_selection)
    selected_bsps = GetSelectedBSPs(objects_selection)
    # ApplyPredominantShaderNames(h_objects.poops) # commented out 06-12-2022. I don't think it is needed
    # if sidecar_type == 'SCENARIO':
    #     RotateScene(context.view_layer.objects, model_armature)

    return objects_selection, active_object, hidden_objects, mode, model_armature, temp_armature, skeleton_bones, halo_objects, timeline_start, timeline_end, lod_count, unselectable_objects, enabled_exclude_collections, mesh_node_names, temp_nodes, selected_perms, selected_bsps, current_frame, regions_dict, global_materials_dict


#####################################################################################
#####################################################################################
# HALO CLASS

class HaloObjects():
    def __init__(self, asset_type):
        self.frame = select_halo_objects('frame', asset_type, ('MODEL', 'SKY', 'DECORATOR SET', 'PARTICLE MODEL', 'SCENARIO', 'PREFAB'))
        self.default = select_halo_objects('render', asset_type, ('MODEL', 'SKY', 'DECORATOR SET', 'PARTICLE MODEL', 'SCENARIO', 'PREFAB'))
        self.collision = select_halo_objects('collision', asset_type, (('MODEL', 'SKY', 'DECORATOR SET', 'PARTICLE MODEL', 'SCENARIO', 'PREFAB')))
        self.physics = select_halo_objects('physics', asset_type, ('MODEL', 'SKY', 'DECORATOR SET', 'PARTICLE MODEL', 'SCENARIO',))
        self.markers = select_halo_objects('marker', asset_type, ('MODEL', 'SKY', 'DECORATOR SET', 'PARTICLE MODEL', 'SCENARIO', 'PREFAB'))
        self.object_instances = select_halo_objects('object_instance', asset_type, ('MODEL'))

        self.decorators = select_halo_objects('decorator', asset_type, ('DECORATOR SET'))
        
        self.cookie_cutters = select_halo_objects('cookie_cutter', asset_type, ('SCENARIO', 'PREFAB'))
        self.poops = select_halo_objects('poop', asset_type, ('SCENARIO', 'PREFAB'))
        self.poop_markers = select_halo_objects('poop_marker', asset_type, ('SCENARIO'))
        self.misc = select_halo_objects('misc', asset_type, ('SCENARIO', 'PREFAB'))
        self.seams = select_halo_objects('seam', asset_type, ('SCENARIO'))
        self.portals = select_halo_objects('portal', asset_type, ('SCENARIO'))
        self.water_surfaces = select_halo_objects('water_surface', asset_type, ('SCENARIO', 'PREFAB'))
        self.lights = select_halo_objects('light', asset_type, ('SCENARIO', 'PREFAB', 'SKY'))
        
        self.boundary_surfaces = select_halo_objects('boundary_surface', asset_type, ('SCENARIO'))
        self.fog = select_halo_objects('fog', asset_type, ('SCENARIO'))
        self.water_physics = select_halo_objects('water_physics', asset_type, ('SCENARIO'))
        self.poop_rain_blockers = select_halo_objects('poop_rain_blocker', asset_type, ('SCENARIO'))

#####################################################################################
#####################################################################################
# VARIOUS FUNCTIONS
def GetSceneMode(context):
    mode = None
    try: # wrapped this in a try as the user can encounter an assert if no object is selected. No reason for this to crash the export
        if context.view_layer.objects.active == None: 
            context.view_layer.objects.active = context.view_layer.objects[0]

        mode = context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    except:
        print('WARNING: Unable to test mode')

    return mode

def get_regions_dict(objects):
    regions = {'default': '0'}
    index = 0
    for ob in objects:
        name = true_region(ob.nwo)
        if name not in regions.keys():
            index +=1
            regions.update({name: str(index)})

    return regions

def get_global_materials_dict(objects):
    global_materials = {'default': '0'}
    index = 0
    for ob in objects:
        name = ob.nwo.Face_Global_Material
        if name not in global_materials.keys() and name != '':
            index +=1
            global_materials.update({name: str(index)})

    return global_materials

def GetSelectedPermutations(selection):
    selected_perms = []
    # cycle through selected objects and get their permutation
    for ob in selection:
        perm = ''
        if ob.nwo.Permutation_Name_Locked != '':
            perm = ob.nwo.Permutation_Name_Locked
        else:
            perm = ob.nwo.Permutation_Name
        if perm not in selected_perms:
            selected_perms.append(perm)
    
    return selected_perms

def GetSelectedBSPs(selection):
    selected_bsps = []
    # cycle through selected objects and get their permutation
    for ob in selection:
        bsp = ''
        if ob.nwo.bsp_name_locked != '':
            bsp = ob.nwo.bsp_name_locked
        else:
            bsp = ob.nwo.bsp_name
        if bsp not in selected_bsps:
            selected_bsps.append(bsp)
    
    return selected_bsps

def ExitLocalView(context):
    for area in context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            if space.local_view:
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {'area': area, 'region': region}
                        bpy.ops.view3d.localview(override)

def ApplyObjectIDs(scene_obs):
    for ob in scene_obs:
        ob.nwo.object_id
        if ob.nwo.object_id == '':
            ob.nwo.object_id = str(uuid4())

def RotateScene(scene_obs, model_armature):
    deselect_all_objects()
    angle_z = radians(90)
    axis_z = (0, 0, 1)
    pivot = Vector((0.0, 0.0, 0.0))
    for ob in scene_obs:
        if ob != model_armature:
            M = (
                Matrix.Translation(pivot) @
                Matrix.Rotation(angle_z, 4, axis_z) @       
                Matrix.Translation(-pivot)
                )
            ob.matrix_world = M @ ob.matrix_world

def UnhideObjects(export_hidden, context):
    hidden_objects = []
    if export_hidden:
        for ob in tuple(context.view_layer.objects):
            if not ob.visible_get():
                hidden_objects.append(ob)
        
        for ob in hidden_objects:
            ob.hide_set(False)

    return hidden_objects # return a list of objects which should be hidden in repair_scene

def SetTimelineRange(context):
    scene = context.scene
    current_frame = scene.frame_current
    timeline_start = scene.frame_start
    timeline_end = scene.frame_end

    scene.frame_start = 0
    scene.frame_end = 0

    return timeline_start, timeline_end, current_frame

def GetCurrentActiveObjectSelection(context):
    objects_selection = None
    active_object = None
    try:
        objects_selection = context.selected_objects
        active_object = context.active_object
    except:
        print('ASSERT: Unable to attain active object & selection')

    return objects_selection, active_object

def FixLightsRotations(lights_list):
    deselect_all_objects()
    angle_x = radians(90)
    angle_z = radians(-90)
    axis_x = (1, 0, 0)
    axis_z = (0, 0, 1)
    for ob in lights_list:
        pivot = ob.location
        M = (
            Matrix.Translation(pivot) @
            Matrix.Rotation(angle_x, 4, axis_x) @
            Matrix.Rotation(angle_z, 4, axis_z) @       
            Matrix.Translation(-pivot)
            )
        ob.matrix_world = M @ ob.matrix_world


def GetDecoratorLODCount(halo_objects, asset_is_decorator):
    lod_count = 0
    if asset_is_decorator:
        for ob in halo_objects.decorators:
            ob_lod = ob.nwo.Decorator_LOD
            if ob_lod > lod_count:
                lod_count =  ob_lod
    
    return lod_count

def HideExcludedCollections(context):
    enabled_exclude_collections = []
    for layer in context.view_layer.layer_collection.children:
        if layer.collection.name.startswith('+exclude') and layer.is_visible:
            enabled_exclude_collections.append(layer)
        if layer.collection.name.startswith('+exclude'):
            layer.exclude = True

    return enabled_exclude_collections


#####################################################################################
#####################################################################################
# ARMATURE FUNCTIONS
def GetSceneArmature(context, sidecar_type, game_version):
    model_armature = None
    temp_armature = False
    no_parent_objects = []
    for ob in context.view_layer.objects:
        if ob.type == 'ARMATURE' and not ob.name.startswith('+'): # added a check for a '+' prefix in armature name, to support special animation control armatures in the future
            model_armature = ob
            break
    if model_armature is None and (sidecar_type not in ('SCENARIO', 'PREFAB', 'PARTICLE MODEL', 'DECORATOR SET') or (sidecar_type == 'SCENARIO' and not not_bungie_game())):
        model_armature, no_parent_objects = AddTempArmature(context)
        temp_armature = True

    return model_armature, temp_armature, no_parent_objects

def AddTempArmature(context):
    ops = bpy.ops
    ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    model_armature = context.view_layer.objects.active
    model_armature.data.edit_bones[0].name = 'implied_root_node'
    model_armature.data.edit_bones[0].tail[1] = 1
    model_armature.data.edit_bones[0].tail[2] = 0
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    no_parent_objects = []
    for ob in context.view_layer.objects:
        if ob.parent == None:
            ob.select_set(True)
            no_parent_objects.append(ob)

    set_active_object(model_armature)
    ops.object.parent_set(type='OBJECT')

    return model_armature, no_parent_objects

def ParentToArmature(model_armature, temp_armature, no_parent_objects, context):
    if temp_armature:
        for ob in no_parent_objects:
            ob.select_set(True)
        set_active_object(model_armature)
        bpy.ops.object.parent_set(type='BONE', keep_transform=True)
    else:
        for ob in context.view_layer.objects:
            if (ob.parent == model_armature and ob.parent_type == 'OBJECT') and not any(m != ' ARMATURE' for m in ob.modifiers):
                deselect_all_objects()
                ob.select_set(True)
                set_active_object(model_armature)
                if (CheckType.render or CheckType.collision):
                    bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)
                else:
                    bpy.ops.object.parent_set(type='BONE', keep_transform=True)
                    
#####################################################################################
#####################################################################################
# BONE FUNCTIONS

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
        if b.nwo.frame_id1 == '':
            FrameID1 = list(f1)[index]
        else:
            FrameID1 = b.nwo.frame_id1
        if b.nwo.frame_id2 == '':
            FrameID2 = list(f2)[index]
        else:
            FrameID2 = b.nwo.frame_id2
        index +=1
        boneslist.update({b.name: getBoneProperties(FrameID1, FrameID2, b.nwo.object_space_node, b.nwo.replacement_correction_node, b.nwo.fik_anchor_node)})

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
    if not_bungie_game():
        node_props.update({"bungie_frame_world": "1"}),

    return node_props

def getBoneProperties(FrameID1, FrameID2, object_space_node, replacement_correction_node, fik_anchor_node):
    node_props = {}

    node_props.update({"bungie_object_type": "_connected_geometry_object_type_frame"}),
    node_props.update({"bungie_frame_ID1": FrameID1}),
    node_props.update({"bungie_frame_ID2": FrameID2}),

    if object_space_node:
        node_props.update({"bungie_is_object_space_offset_node": "1"}),
    if replacement_correction_node:
        node_props.update({"bungie_is_replacement_correction_node": "1"}),
    if fik_anchor_node:
        node_props.update({"bungie_is_fik_anchor_node": "1"}),

    node_props.update({"bungie_object_animates": "1"}),
    node_props.update({"halo_export": "1"}),

    return node_props

def openCSV():
    script_folder_path = path.dirname(path.dirname(__file__))
    filepath = path.join(script_folder_path, "file_gr2", "frameidlist.csv")

    frameIDList = {}
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            frameIDList.update({row[0]: row[1]})

    return frameIDList

def ApplyPredominantShaderNames(poops):
    for ob in poops:
        ob.nwo.Poop_Predominant_Shader_Name = GetProminantShaderName(ob)

def GetProminantShaderName(ob):
    predominant_shader = ''
    slots = ob.material_slots
    for s in slots:
        material = s.material
        if is_shader(material):
            shader_path = material.nwo.shader_path
            if shader_path.rpartition('.')[0] != '':
                shader_path = shader_path.rpartition('.')[0]
            shader_path.replace(get_tags_path(), '')
            shader_path.replace(get_tags_path().lower(), '')
            shader_type = material.nwo.Shader_Type
            predominant_shader = f'{shader_path}.{shader_type}'
            break

    return predominant_shader

def SetPoopProxies(context, poops):
    proxies = []
    mesh_data = []
    proxy_collision = None
    proxy_physics = None
    proxy_cookie_cutter = None
    collision_offset = 0
    physics_offset = 0
    cookie_cutter_offset = 0
    poop_offset = 0
    deselect_all_objects()
    for ob in poops:
        if ob.data.name not in mesh_data:
            mesh_data.append(ob.data.name)
            for obj in poops:
                if (obj.data.name == ob.data.name) and (len(obj.children) > 0) and CheckType.poop(obj):
                    proxy_collision, collision_offset = GetPoopProxyCollision(obj, poops)
                    proxy_physics, physics_offset = GetPoopProxyPhysics(obj, poops)
                    proxy_cookie_cutter, cookie_cutter_offset = GetPoopProxyCookie(obj, poops)
                    obj.select_set(True)
                    break

            for obj in poops:
                if CheckType.poop(obj) and obj.data.name == ob.data.name and len(obj.children) <= 0:
                    deselect_all_objects()
                    obj.select_set(True)
                    poop_offset = obj.matrix_world
                    poop_proxies = AttachPoopProxies(obj, proxy_collision, proxy_physics, proxy_cookie_cutter, collision_offset, physics_offset, cookie_cutter_offset, poop_offset)
                    for p in poop_proxies:
                        proxies.append(p)

    return proxies

def AttachPoopProxies(obj, proxy_collision, proxy_physics, proxy_cookie_cutter, collision_offset, physics_offset, cookie_cutter_offset, poop_offset):
    ops = bpy.ops
    context = bpy.context
    proxy = []
    deselect_all_objects()
    if proxy_collision != None:
        proxy_collision.select_set(True)
    if proxy_physics != None:
        proxy_physics.select_set(True)
    if proxy_cookie_cutter != None:
        proxy_cookie_cutter.select_set(True)

    ops.object.duplicate(linked=True, mode='TRANSLATION')

    if proxy_collision != None:
        proxy_collision.select_set(False)
    if proxy_physics != None:
        proxy_physics.select_set(False)
    if proxy_cookie_cutter != None:
        proxy_cookie_cutter.select_set(False)

    proxy = [prox for prox in context.selected_objects]

    context.view_layer.objects.active = obj

    ops.object.parent_set(type='OBJECT', keep_transform=False)

    for ob in proxy:
        if CheckType.poop_collision(ob):
            ob.matrix_local = collision_offset
        elif CheckType.poop_physics(ob):
            ob.matrix_local = physics_offset
        else:
            ob.matrix_local = cookie_cutter_offset

    return proxy


def GetPoopProxyCollision(obj, poops):
    collision = None
    collision_offset = 0
    for child in obj.children:
        if child in poops and CheckType.poop_collision(child):
            collision = child
            collision_offset = collision.matrix_local
            break
    

    return collision, collision_offset

def GetPoopProxyPhysics(obj, poops):
    physics = None
    physics_offset = 0
    for child in obj.children:
        if child in poops and CheckType.poop_physics(child):
            physics = child
            physics_offset = physics.matrix_local
            break

    return physics, physics_offset

def GetPoopProxyCookie(obj, poops):
    cookie = None
    cookie_offset = 0
    for child in obj.children:
        if child in poops and CheckType.cookie_cutter(child):
            cookie = child
            cookie_offset = cookie.matrix_local
            break

    return cookie, cookie_offset

def MakeSelectable(context):
    unselectable_objects = []
    select_all_objects()
    for ob in context.view_layer.objects:
        if ob not in context.selected_objects:
            unselectable_objects.append(ob)
    
    for ob in unselectable_objects:
        ob.hide_select = False
    
    deselect_all_objects()

    return unselectable_objects


def FixMissingMaterials(context, sidecar_type):
    # set some locals
    ops = bpy.ops
    materials_list = bpy.data.materials
    mat = ''
    # loop through each object in the scene
    for ob in context.scene.objects:
        if is_mesh(ob): # check if we're processing a mesh
            # remove empty material slots
            for index, slot in enumerate(ob.material_slots.items()):
                if slot[0] == '':
                    context.object.active_material_index = index
                    ops.object.material_slot_remove()

            if len(ob.material_slots) <= 0: # if no material slots...
                # determine what kind of mesh this is
                if CheckType.collision(ob):
                    if not_bungie_game():
                        if ob.nwo.Poop_Collision_Type == '_connected_geometry_poop_collision_type_play_collision':
                            mat = '+player_collision'
                        elif ob.nwo.Poop_Collision_Type == '_connected_geometry_poop_collision_type_bullet_collision':
                            mat = '+bullet_collision'
                        elif ob.nwo.Poop_Collision_Type == '_connected_geometry_poop_collision_type_invisible_wall':
                            mat = '+wall_collision'
                        else:
                            mat = '+collision'
                    
                    else:
                        mat = '+collision'

                elif CheckType.physics(ob):
                    mat = '+physics'
                elif CheckType.portal(ob):
                    mat = '+portal'
                elif CheckType.seam(ob):
                    mat = '+seam'
                elif CheckType.cookie_cutter(ob):
                    mat = '+cookie_cutter'
                elif CheckType.water_physics(ob):
                    mat = '+water_volume'
                elif CheckType.poop(ob) and ob.nwo.poop_rain_occluder:
                    mat = '+rain_blocker'
                elif CheckType.default(ob) and ob.nwo.Face_Type == '_connected_geometry_face_type_sky':
                    mat = '+sky'
                elif (CheckType.default(ob) or CheckType.poop(ob)) and ob.nwo.Face_Type == '_connected_geometry_face_type_seam_sealer':
                    mat = '+seamsealer'
                elif CheckType.default(ob) and not_bungie_game() and sidecar_type == 'SCENARIO':
                    mat = '+structure'
                elif CheckType.default(ob) or CheckType.poop(ob) or CheckType.decorator(ob):
                    mat = 'invalid'
                else:
                    mat = '+override'
                
                # if this special material isn't already in the users scene, add it
                if mat not in materials_list:
                    materials_list.new(mat)

                # convert mat to a material object
                mat = materials_list.get(mat)
                # finally, append the new material to the object
                ob.data.materials.append(mat)

def MeshesToEmpties(context):
    # get a list of meshes which are nodes
    mesh_nodes = []
    for ob in context.view_layer.objects:
        if CheckType.marker(ob) and ob.type == 'MESH':
            mesh_nodes.append(ob)
    # For each mesh node create an empty with the same Halo props and transforms
    # Mesh objects need their names saved, so we make a dict. Names are stored so that the node can have the exact same name. We add a temp name to each mesh object
    mesh_node_names = {}
    temp_nodes = []
    for ob in mesh_nodes:
        deselect_all_objects()
        bpy.ops.object.empty_add(type='ARROWS')
        node = context.object
        node_name = TempName(ob.name)
        mesh_node_names.update({ob: node_name}) 
        ob.name = str(uuid4())
        node.name = node_name
        if ob.parent is not None:
            node.parent = ob.parent
            # Added 08-12-2022 to fix empty nodes not being bone parented
            node.parent_type = ob.parent_type
            if node.parent_type == 'BONE':
                node.parent_bone = ob.parent_bone

        node.matrix_local = ob.matrix_local
        node.scale = ob.scale
        # copy the node props from the mesh to the empty
        SetNodeProps(node, ob)
        # hide the mesh so it doesn't get included in the export
        ob.hide_set(True)
        temp_nodes.append(node)
    return mesh_node_names, temp_nodes

def TempName(name):
    return name + ''

def SetNodeProps(node, ob):
    node_halo = node.nwo
    ob_halo = ob.nwo

    if ob.users_collection[0].name != 'Scene Collection':
        try:
            bpy.data.collections[ob.users_collection[0].name].objects.link(node)
        except:
            pass # lazy try except as this can cause an assert.
    
    node_halo.bsp_name = ob_halo.bsp_name

    node_halo.Permutation_Name = ob_halo.Permutation_Name

    node_halo.ObjectMarker_Type = ob_halo.ObjectMarker_Type

    node_halo.Marker_Region = ob_halo.Marker_Region
    node_halo.Marker_All_Regions = ob_halo.Marker_All_Regions
    node_halo.Marker_Velocity = ob_halo.Marker_Velocity

    node_halo.Marker_Game_Instance_Tag_Name = ob_halo.Marker_Game_Instance_Tag_Name
    node_halo.Marker_Game_Instance_Tag_Variant_Name = ob_halo.Marker_Game_Instance_Tag_Variant_Name

    node_halo.Marker_Pathfinding_Sphere_Vehicle = ob_halo.Marker_Pathfinding_Sphere_Vehicle
    node_halo.Pathfinding_Sphere_Remains_When_Open = ob_halo.Pathfinding_Sphere_Remains_When_Open
    node_halo.Pathfinding_Sphere_With_Sectors = ob_halo.Pathfinding_Sphere_With_Sectors

    node_halo.Physics_Constraint_Parent = ob_halo.Physics_Constraint_Parent
    node_halo.Physics_Constraint_Child = ob_halo.Physics_Constraint_Child
    node_halo.Physics_Constraint_Type = ob_halo.Physics_Constraint_Type
    node_halo.Physics_Constraint_Uses_Limits = ob_halo.Physics_Constraint_Uses_Limits

    node_halo.object_id = ob_halo.object_id





