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
from ..gr2_utils import(
    DeselectAllObjects,
    IsMesh,
    SetActiveObject,
    sel_logic,
    GetAssetInfo,
    SelectHaloObject,
    SelectAllObjects,
    IsShader,
    HaloBoner,
)
#####################################################################################
#####################################################################################
# MAIN FUNCTION
def prepare_scene(context, report, sidecar_type, export_hidden, filepath, use_armature_deform_only, **kwargs):
    enabled_exclude_collections = HideExcludedCollections(context)
    objects_selection, active_object = GetCurrentActiveObjectSelection(context)
    hidden_objects = UnhideObjects(export_hidden, context)                               # If the user has opted to export hidden objects, list all hidden objects and unhide them, return the list for later use
    mode = GetSceneMode(context)                                                      # get the current selected mode, save the mode for later, and then switch to object mode
    unselectable_objects = MakeSelectable(context)
    # update bsp names in case any are null
    for ob in context.scene.objects:
        if ob.halo_json.bsp_name == '':
            ob.halo_json.bsp_name = '000'

    h_objects = halo_objects(sidecar_type)
    FixMissingMaterials(context, h_objects)
    proxies = SetPoopProxies(context, h_objects.poops)                                               # create and parent identical poop child objects to matching instances (collision, physics, cookie cutters). Keep them in a list so we can delete them later
    for p in proxies:
        h_objects.poops.append(p)
    model_armature, temp_armature, no_parent_objects = GetSceneArmature(context, sidecar_type)                          # return the main armature in the scene, and create a temp one if a model armature does not exist
    skeleton_bones = {}
    if model_armature is not None:
        ParentToArmature(model_armature, temp_armature, no_parent_objects, context)                             # ensure all objects are parented to an armature on export. Render and collision mesh is parented with armature deform, the rest uses bone parenting
        skeleton_bones = GetBoneList(model_armature, use_armature_deform_only)      # return a list of bones attached to the model armature, ignoring control / non-deform bones
    asset_path, asset = GetAssetInfo(filepath)                                  # get the asset name and path to the asset folder
    # HaloBoner(model_armature.data.edit_bones, model_armature, context)
    #FixLightsRotations(h_objects.lights)                                         # adjust light rotations to match in game rotation, and return a list of lights for later use in repair_scene
    timeline_start, timeline_end = SetTimelineRange(context)                      # set the timeline range so we can restore it later
    lod_count = GetDecoratorLODCount(h_objects, sidecar_type == 'DECORATOR SET') # get the max LOD count in the scene if we're exporting a decorator
    ApplyPredominantShaderNames(h_objects.poops)
    # if sidecar_type == 'SCENARIO':
    #     RotateScene(context.view_layer.objects, model_armature)
    ApplyObjectIDs(context.view_layer.objects)

    return objects_selection, active_object, hidden_objects, mode, model_armature, temp_armature, asset_path, asset, skeleton_bones, h_objects, timeline_start, timeline_end, lod_count, proxies, unselectable_objects, enabled_exclude_collections


#####################################################################################
#####################################################################################
# HALO CLASS

class halo_objects():
    def __init__(self, asset_type):
        self.render = SelectHaloObject('ObRender', asset_type, ('MODEL', 'SKY', 'CINEMATIC', 'DECORATOR', 'PARTICLE'))
        self.collision = SelectHaloObject('ObCollision', asset_type, ('MODEL', 'SKY', 'CINEMATIC', 'DECORATOR', 'PARTICLE'))
        self.physics = SelectHaloObject('ObPhysics', asset_type, ('MODEL', 'SKY', 'CINEMATIC', 'DECORATOR', 'PARTICLE'))
        self.markers = SelectHaloObject('ObMarkers', asset_type, ('MODEL', 'SCENARIO', 'SKY', 'CINEMATIC', 'DECORATOR', 'PARTICLE'))
        self.structure = SelectHaloObject('ObStructure', asset_type, ('SCENARIO', 'CINEMATIC'))
        self.poops = SelectHaloObject('ObPoops', asset_type, ('SCENARIO', 'CINEMATIC'))
        self.lights = SelectHaloObject('ObLights', asset_type, ('SCENARIO', 'SKY', 'CINEMATIC'))
        self.portals = SelectHaloObject('ObPortals', asset_type, ('SCENARIO', 'CINEMATIC'))
        self.seams = SelectHaloObject('ObSeams', asset_type, ('SCENARIO', 'CINEMATIC'))
        self.water_surfaces = SelectHaloObject('ObWaterSurfaces', asset_type, ('SCENARIO', 'CINEMATIC'))
        self.lightmap_regions = SelectHaloObject('ObLightMapRegions', asset_type, ('SCENARIO', 'CINEMATIC'))
        self.fog = SelectHaloObject('ObFog', asset_type, ('SCENARIO', 'CINEMATIC'))
        self.boundary_surfaces = SelectHaloObject('ObBoundarys', asset_type, ('SCENARIO', 'CINEMATIC'))
        self.water_physics = SelectHaloObject('ObWaterPhysics', asset_type, ('SCENARIO', 'CINEMATIC'))
        self.rain_occluders = SelectHaloObject('ObPoopRains', asset_type, ('SCENARIO', 'CINEMATIC'))
        self.decorator = SelectHaloObject('ObDecorator', asset_type, ('DECORATOR SET'))
        self.particle = SelectHaloObject('ObRender', asset_type, ('PARTICLE MODEL'))

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

def ApplyObjectIDs(scene_obs):
    for ob in scene_obs:
        ob.halo_json.object_id
        if ob.halo_json.object_id == '':
            ob.halo_json.object_id = str(uuid4())

def RotateScene(scene_obs, model_armature):
    DeselectAllObjects()
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
    timeline_start = scene.frame_start
    timeline_end = scene.frame_end

    scene.frame_start = 0
    scene.frame_end = 0

    return timeline_start, timeline_end

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
    DeselectAllObjects()
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
        for ob in halo_objects.decorator:
            ob_lod = ob.halo_json.Decorator_LOD
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
def GetSceneArmature(context, sidecar_type):
    model_armature = None
    temp_armature = False
    no_parent_objects = []
    for ob in context.view_layer.objects:
        if ob.type == 'ARMATURE' and not ob.name.startswith('+'): # added a check for a '+' prefix in armature name, to support special animation control armatures in the future
            model_armature = ob
            break
    if model_armature is None:
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

    SetActiveObject(model_armature)
    ops.object.parent_set(type='OBJECT')

    return model_armature, no_parent_objects

def ParentToArmature(model_armature, temp_armature, no_parent_objects, context):
    if temp_armature:
        for ob in no_parent_objects:
            ob.select_set(True)
        SetActiveObject(model_armature)
        bpy.ops.object.parent_set(type='BONE', keep_transform=True)
    else:
        for ob in context.view_layer.objects:
            if (ob.parent == model_armature and ob.parent_type == 'OBJECT') and not any(m != ' ARMATURE' for m in ob.modifiers):
                DeselectAllObjects()
                ob.select_set(True)
                SetActiveObject(model_armature)
                if (sel_logic.ObRender or sel_logic.ObCollision):
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
    filepath = path.join(script_folder_path, "file_gr2", "frameidlist.csv")

    frameIDList = {}
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            frameIDList.update({row[0]: row[1]})

    return frameIDList

def ApplyPredominantShaderNames(poops):
    for ob in poops:
        ob.halo_json.Poop_Predominant_Shader_Name = GetProminantShaderName(ob)

def GetProminantShaderName(ob):
    predominant_shader = ''
    slots = ob.material_slots
    for s in slots:
        material = s.material
        if IsShader(material):
            shader_path = material.halo_json.shader_path
            if shader_path.rpartition('.')[0] != '':
                shader_path = shader_path.rpartition('.')[0]
            shader_type = material.halo_json.Shader_Type
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
    DeselectAllObjects()
    for ob in poops:
        if ob.data.name not in mesh_data:
            mesh_data.append(ob.data.name)
            for obj in poops:
                if (obj.data.name == ob.data.name) and (len(obj.children) > 0) and sel_logic.ObPoopsOnly(obj):
                    proxy_collision, collision_offset = GetPoopProxyCollision(obj, poops)
                    proxy_physics, physics_offset = GetPoopProxyPhysics(obj, poops)
                    proxy_cookie_cutter, cookie_cutter_offset = GetPoopProxyCookie(obj, poops)
                    obj.select_set(True)
                    break

            for obj in poops:
                if sel_logic.ObPoopsOnly(obj) and obj.data.name == ob.data.name and len(obj.children) <= 0:
                    DeselectAllObjects()
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
    DeselectAllObjects()
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
        if sel_logic.ObPoopCollision(ob):
            ob.matrix_local = collision_offset
        elif sel_logic.ObPoopPhysics(ob):
            ob.matrix_local = physics_offset
        else:
            ob.matrix_local = cookie_cutter_offset

    return proxy


def GetPoopProxyCollision(obj, poops):
    collision = None
    collision_offset = 0
    for child in obj.children:
        if child in poops and sel_logic.ObPoopCollision(child):
            collision = child
            collision_offset = collision.matrix_local
            break
    

    return collision, collision_offset

def GetPoopProxyPhysics(obj, poops):
    physics = None
    physics_offset = 0
    for child in obj.children:
        if child in poops and sel_logic.ObPoopPhysics(child):
            physics = child
            physics_offset = physics.matrix_local
            break

    return physics, physics_offset

def GetPoopProxyCookie(obj, poops):
    cookie = None
    cookie_offset = 0
    for child in obj.children:
        if child in poops and sel_logic.ObCookie(child):
            cookie = child
            cookie_offset = cookie.matrix_local
            break

    return cookie, cookie_offset

def MakeSelectable(context):
    unselectable_objects = []
    SelectAllObjects()
    for ob in context.view_layer.objects:
        if ob not in context.selected_objects:
            unselectable_objects.append(ob)
    
    for ob in unselectable_objects:
        ob.hide_select = False
    
    DeselectAllObjects()

    return unselectable_objects


def FixMissingMaterials(context, halo_objects):
    # set some locals
    ops = bpy.ops
    materials_list = bpy.data.materials
    mat_collision = '+collision'
    mat_physics = '+physics'
    mat_portal = '+portal'
    mat_sky = '+sky'
    mat_seamsealer = '+seamsealer'
    mat_invalid = 'invalid'
    mat_override = '+override'
    mat = ''
    # loop through each object in the scene
    for ob in context.scene.objects:
        if IsMesh(ob): # check if we're processing a mesh
            # remove empty material slots
            for index, slot in enumerate(ob.material_slots.items()):
                if slot[0] == '':
                    context.object.active_material_index = index
                    ops.object.material_slot_remove()

            if len(ob.material_slots) <= 0: # if no material slots...
                # determine what kind of mesh this is
                if ob in halo_objects.collision:
                    mat = mat_collision
                elif ob in halo_objects.physics:
                    mat = mat_physics
                elif ob in halo_objects.portals:
                    mat = mat_portal
                elif ob.halo_json.Face_Type == 'SKY':
                    mat = mat_sky
                elif ob.halo_json.Face_Type == 'SEAM SEALER':
                    mat = mat_seamsealer
                elif sel_logic.ObRender(ob) or sel_logic.ObStructure(ob) or sel_logic.ObPoopsOnly(ob) or sel_logic.ObDecorator(ob):
                    mat = mat_invalid
                else:
                    mat = mat_override
                
                # if this special material isn't already in the users scene, add it
                if mat not in materials_list:
                    materials_list.new(mat)

                # convert mat to a material object
                mat = materials_list.get(mat)
                # finally, append the new material to the object
                ob.data.materials.append(mat)

