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
from mathutils import Matrix
from ..gr2_utils import(
    DeselectAllObjects,
    SelectAllObjects,
    SetActiveObject,
    sel_logic,
    GetAssetInfo,
    SelectHaloObject
)
#####################################################################################
#####################################################################################
# MAIN FUNCTION
def prepare_scene(context, report, sidecar_type, export_hidden, filepath, use_armature_deform_only, **kwargs):
    objects_selection, active_object = GetCurrentActiveObjectSelection(context)
    hidden_objects = UnhideObjects(export_hidden)                               # If the user has opted to export hidden objects, list all hidden objects and unhide them, return the list for later use
    mode = GetSceneMode(context)                                                      # get the current selected mode, save the mode for later, and then switch to object mode
    model_armature, temp_armature = GetSceneArmature(context)                          # return the main armature in the scene, and create a temp one if a model armature does not exist
    ParentToArmature(model_armature, temp_armature)                             # ensure all objects are parented to an armature on export. Render and collision mesh is parented with armature deform, the rest uses bone parenting
    asset_path, asset = GetAssetInfo(filepath)                                  # get the asset name and path to the asset folder
    skeleton_bones = GetBoneList(model_armature, use_armature_deform_only)      # return a list of bones attached to the model armature, ignoring control / non-deform bones
    h_objects = halo_objects(sidecar_type)
    FixLightsRotations(h_objects.lights)                                         # adjust light rotations to match in game rotation, and return a list of lights for later use in repair_scene
    timeline_start, timeline_end = SetTimelineRange(context)
    print('Scene prepared')                                          
    return objects_selection, active_object, hidden_objects, mode, model_armature, temp_armature, asset_path, asset, skeleton_bones, h_objects, timeline_start, timeline_end

#####################################################################################
#####################################################################################
# HALO CLASS

class halo_objects():
    def __init__(self, asset_type):
        print('initialising halo objects')
        print(asset_type)
        self.render = SelectHaloObject('ObRender', asset_type, ('MODEL', 'SKY', 'CINEMATIC', 'DECORATOR', 'PARTICLE'))
        print(self.render)
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
        self.cookie_cutters = SelectHaloObject('ObCookie', asset_type, ('SCENARIO', 'CINEMATIC'))
        self.boundary_surfaces = SelectHaloObject('ObBoundarys', asset_type, ('SCENARIO', 'CINEMATIC'))
        self.water_physics = SelectHaloObject('ObWaterPhysics', asset_type, ('SCENARIO', 'CINEMATIC'))
        self.rain_occluders = SelectHaloObject('ObPoopRains', asset_type, ('SCENARIO', 'CINEMATIC'))

#####################################################################################
#####################################################################################
# VARIOUS FUNCTIONS
def GetSceneMode(context):
    mode = None
    # try: # wrapped this in a try as the user can encounter an assert if no object is selected. No reason for this to crash the export
    if len(context.selected_objects) > 0:
        mode = context.object.mode

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    # except:
    #     print('WARNING: Unable to test mode')

    return mode

def UnhideObjects(export_hidden):
    hidden_objects = []
    if export_hidden:
        for ob in tuple(bpy.data.scenes[0].view_layers[0].objects):
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
    angle_x = radians(-90)
    angle_z = radians(-180)
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

#####################################################################################
#####################################################################################
# ARMATURE FUNCTIONS
def GetSceneArmature(context):
    model_armature = None
    temp_armature = False
    for ob in bpy.data.objects:
        if ob.type == 'ARMATURE' and not ob.name.startswith('+'): # added a check for a '+' prefix in armature name, to support special animation control armatures in the future
            model_armature = ob
            break
    if model_armature == None:
        model_armature = AddTempArmature(context)
        temp_armature = True

    return model_armature, temp_armature

def AddTempArmature(context):
    ops = bpy.ops
    ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    model_armature = context.view_layer.objects.active
    model_armature.data.bones[0].name = 'implied_root_node'
    for ob in bpy.data.objects:
        if ob.parent == None:
            ob.select_set(True)

    SetActiveObject(model_armature)
    ops.object.parent_set(type='OBJECT')

    return model_armature

def ParentToArmature(model_armature, temp_armature):
    if temp_armature:
        SelectAllObjects()
        SetActiveObject(model_armature)
        bpy.ops.object.parent_set(type='BONE', keep_transform=True)
    else:
        for ob in bpy.data.objects:
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