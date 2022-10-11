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
)
from math import radians
from mathutils import Matrix

#####################################################################################
#####################################################################################
# MAIN FUNCTION     

def repair_scene(context, report, objects_selection, active_object, hidden_objects, mode, temp_armature, timeline_start, timeline_end, model_armature, lights, export_hidden, **kwargs):
    scene = context.scene
 
    RepairTimeline(scene, timeline_start, timeline_end)

    if export_hidden:
        for ob in hidden_objects:
            ob.hide_set(True)

    if objects_selection != None:
        for ob in objects_selection:
            ob.select_set(True)
    if active_object != None:
        bpy.context.view_layer.objects.active = active_object


    RestoreLightsRotations(lights)

    # try: # try this but don't assert if it fails
    #     if mode != '':
    #         bpy.ops.object.mode_set(mode=mode, toggle=False)
    # except:
    #     print('error occured when trying to replace mode')

    if temp_armature:
        DelTempArmature(context, model_armature)

#####################################################################################
#####################################################################################
# VARIOUS FUNCTIONS

def RepairTimeline(scene, timeline_start, timeline_end):
    scene.frame_start = timeline_start
    scene.frame_end = timeline_end

def DelTempArmature(context, model_armature):
    ops = bpy.ops
    DeselectAllObjects()
    model_armature.select_set(True)
    ops.object.delete(use_global=False, confirm=False)
    for ob in bpy.data.objects:
        context.view_layer.objects.active = ob
        ops.object.modifier_remove(modifier="Armature")
    DeselectAllObjects()

def RestoreLightsRotations(lights_list):
    DeselectAllObjects()
    angle_x = radians(90)
    angle_z = radians(180)
    axis_x = (1, 0, 0)
    axis_z = (0, 0, 1)
    for ob in lights_list:
        pivot = ob.location
        M = (
            Matrix.Translation(pivot) @
            Matrix.Rotation(angle_z, 4, axis_z) @  
            Matrix.Rotation(angle_x, 4, axis_x) @
            Matrix.Translation(-pivot)
            )
        ob.matrix_world = M @ ob.matrix_world