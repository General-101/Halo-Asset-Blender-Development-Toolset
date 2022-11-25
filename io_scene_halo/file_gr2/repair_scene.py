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
from ..gr2_utils import(
    DeselectAllObjects,
    HaloDeboner,
)
from math import radians
from mathutils import Matrix, Vector

#####################################################################################
#####################################################################################
# MAIN FUNCTION     

def repair_scene(context, report, objects_selection, active_object, hidden_objects, mode, temp_armature, timeline_start, timeline_end, model_armature, lights, proxies, unselectable_objects, enabled_exclude_collections, mesh_node_names, temp_nodes, export_hidden, sidecar_type, **kwargs):
    # if sidecar_type == 'SCENARIO':
    #     FixSceneRotatation(context.view_layer.objects, model_armature)
        
    scene = context.scene
 
    RepairTimeline(scene, timeline_start, timeline_end)

    DeletePoopProxies(proxies)

    #RestoreLightsRotations(lights)

    # HaloDeboner(model_armature.data.edit_bones, model_armature, context)

    for ob in unselectable_objects:
        ob.hide_select = True

    if export_hidden:
        for ob in hidden_objects:
            ob.hide_set(True)

    if temp_armature:
        DelTempArmature(context, model_armature)

    RestoreNodeMeshes(mesh_node_names, temp_nodes, hidden_objects)

    try: # try this but don't assert if it fails
        if mode != None:
            bpy.ops.object.mode_set(mode=mode, toggle=False)
    except:
        print('error occured when trying to replace mode')

    # restore selection
    if objects_selection != None:
        for ob in objects_selection:
            ob.select_set(True)
    if active_object != None:
        bpy.context.view_layer.objects.active = active_object

    ShowExcludedCollections(enabled_exclude_collections)

#####################################################################################
#####################################################################################
# VARIOUS FUNCTIONS

def RepairTimeline(scene, timeline_start, timeline_end):
    scene.frame_start = timeline_start
    scene.frame_end = timeline_end

def FixSceneRotatation(scene_obs, model_armature):
    DeselectAllObjects()
    angle_z = radians(-90)
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

def DelTempArmature(context, model_armature):
    ops = bpy.ops
    DeselectAllObjects()
    model_armature.select_set(True)
    ops.object.delete(use_global=False, confirm=False)
    for ob in context.view_layer.objects:
        context.view_layer.objects.active = ob
        ops.object.modifier_remove(modifier="Armature")
    DeselectAllObjects()

def RestoreLightsRotations(lights_list):
    DeselectAllObjects()
    angle_x = radians(90)
    angle_z = radians(180)
    axis_x = (1, 0, 0)
    axis_z = (0, 0, 1)
    lights_list = []
    for ob in lights_list:
        pivot = ob.location
        M = (
            Matrix.Translation(pivot) @
            Matrix.Rotation(angle_x, 4, axis_x) @
            #Matrix.Rotation(angle_z, 4, axis_z) @       
            Matrix.Translation(-pivot)
            )
        ob.matrix_world = M @ ob.matrix_world

def DeletePoopProxies(proxies):
    DeselectAllObjects()
    for p in proxies:
        p.select_set(True)
    bpy.ops.object.delete(use_global=False, confirm=False)

def ShowExcludedCollections(enabled_exclude_collections):
    for coll in enabled_exclude_collections:
        coll.exclude = False

def RestoreNodeMeshes(mesh_node_names, temp_nodes, hidden_objects):
    # delete all temp nodes
    DeselectAllObjects()
    for ob in temp_nodes:
        ob.select_set(True)
    bpy.ops.object.delete()
    # restore mesh names
    for index, ob in enumerate(mesh_node_names.keys()):
        ob.name = mesh_node_names.get(ob)
        if ob not in hidden_objects:
            ob.hide_set(False)