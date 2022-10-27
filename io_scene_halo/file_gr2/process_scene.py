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

from typing import final
import bpy
from os.path import exists
import os
import ctypes
import uuid
import platform
from subprocess import Popen
from addon_utils import modules
from ..gr2_utils import(
    GetPerm,
    IsWindows,
    SelectModelObject,
    SelectModelObjectNoPerm,
    SelectBSPObject,
    GetEKPath,
    GetToolPath,
    DeselectAllObjects,
    IsWindows,
    IsDesign,
    sel_logic,
)

#####################################################################################
#####################################################################################
# MAIN FUNCTION

def process_scene(self, context, keywords, report, model_armature, asset_path, asset, skeleton_bones, halo_objects, timeline_start, timeline_end, lod_count, using_better_fbx, skip_lightmapper,
                  filepath,
                  sidecar_type,
                  output_biped,
                  output_crate,
                  output_creature,
                  output_device_control,
                  output_device_machine,
                  output_device_terminal,
                  output_effect_scenery,
                  output_equipment,
                  output_giant,
                  output_scenery,
                  output_vehicle,
                  output_weapon,
                  export_method,
                  export_hidden,
                  export_render,
                  export_collision,
                  export_physics,
                  export_markers,
                  export_animations,
                  export_structure,
                  export_poops,
                  export_lights,
                  export_portals,
                  export_seams,
                  export_water_surfaces,
                  export_fog_planes,
                  export_cookie_cutters,
                  export_lightmap_regions,
                  export_boundary_surfaces,
                  export_water_physics,
                  export_rain_occluders,
                  export_all_perms,
                  export_specific_perm,
                  export_all_bsps,
                  export_specific_bsp,
                  export_sidecar_xml,
                  lightmap_structure,
                  lightmap_quality,
                  quick_export,
                  #import_bitmaps,
                  **kwargs
    ):
    
    if not IsWindows():
        using_better_fbx = False
        ctypes.windll.user32.MessageBoxW(0, "BetterFBX option is not supported on your OS. FBX output will use the standard FBX module instead.", "OS NOT SUPPORTED", 0)

    if using_better_fbx:
        print('Found Better FBX exporter')
    else:
        from io_scene_fbx.export_fbx_bin import save as export_fbx
        print("Could not find Better FBX exporter (or it is not enabled). Using Blender's native fbx exporter")

    from .export_gr2 import export_gr2

    reports = []
    gr2_count = 0

    if(CheckPath(filepath)): # check the user is saving the file to a location in their editing kit data directory
        if sidecar_type != 'MODEL' or (sidecar_type == 'MODEL' and(
                                                                    output_biped or
                                                                    output_crate or
                                                                    output_creature or
                                                                    output_device_control or
                                                                    output_device_machine or
                                                                    output_device_terminal or
                                                                    output_effect_scenery or
                                                                    output_equipment or
                                                                    output_giant or
                                                                    output_scenery or
                                                                    output_vehicle or
                                                                    output_weapon)
            ):
        
            if export_method == 'BATCH':

                if sidecar_type == 'MODEL':

                    if export_render:
                        perm_list = []
                        for ob in halo_objects.render:
                            perm = GetPerm(ob)
                            if perm not in perm_list:
                                perm_list.append(perm)
                                if SelectModelObject(halo_objects.render, perm, model_armature, export_hidden, export_all_perms, export_specific_perm):
                                    if using_better_fbx:
                                        obj_selection = [obj for obj in context.selected_objects]
                                        export_better_fbx(context, False, **keywords)
                                        for obj in obj_selection:
                                            obj.select_set(True)
                                    else:
                                        export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'render', halo_objects, '', perm, model_armature, skeleton_bones, **keywords)
                                    gr2_count += 1

                    if export_collision:
                        perm_list = []
                        for ob in halo_objects.collision:
                            perm = GetPerm(ob)
                            if perm not in perm_list:
                                perm_list.append(perm)
                                if SelectModelObject(halo_objects.collision, perm, model_armature, export_hidden, export_all_perms, export_specific_perm):
                                    if using_better_fbx:
                                        obj_selection = [obj for obj in context.selected_objects]
                                        export_better_fbx(context, False, **keywords)
                                        for obj in obj_selection:
                                            obj.select_set(True)
                                    else:
                                        export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'collision', halo_objects, '', perm, model_armature, skeleton_bones, **keywords)
                                    gr2_count += 1

                    if export_physics:
                        perm_list = []
                        for ob in halo_objects.physics:
                            perm = GetPerm(ob)
                            if perm not in perm_list:
                                perm_list.append(perm)
                                if SelectModelObject(halo_objects.physics, perm, model_armature, export_hidden, export_all_perms, export_specific_perm):
                                    if using_better_fbx:
                                        obj_selection = [obj for obj in context.selected_objects]
                                        export_better_fbx(context, False, **keywords)
                                        for obj in obj_selection:
                                            obj.select_set(True)
                                    else:
                                        export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'physics', halo_objects, '', perm, model_armature, skeleton_bones, **keywords)
                                    gr2_count += 1

                    if export_markers:
                        if SelectModelObjectNoPerm(halo_objects.markers, model_armature, export_hidden):
                            if using_better_fbx:
                                obj_selection = [obj for obj in context.selected_objects]
                                export_better_fbx(context, False, **keywords)
                                for obj in obj_selection:
                                    obj.select_set(True)
                            else:
                                export_fbx(self, context, **keywords)
                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'markers', halo_objects, '', '', model_armature, skeleton_bones, **keywords)
                            gr2_count += 1

                    if SelectModelSkeleton(model_armature):
                        if using_better_fbx:
                            obj_selection = [obj for obj in context.selected_objects]
                            export_better_fbx(context, False, **keywords)
                            for obj in obj_selection:
                                obj.select_set(True)
                        else:
                            export_fbx(self, context, **keywords)
                        export_gr2(self, context, report, asset_path, asset, IsWindows(), 'skeleton', halo_objects, '', '', model_armature, skeleton_bones, **keywords)
                        gr2_count += 1

                    if export_animations and 1<=len(bpy.data.actions):
                        if SelectModelSkeleton(model_armature):
                            timeline = context.scene
                            for action in bpy.data.actions:
                                try:
                                    model_armature.animation_data.action = action
                                    if action.use_frame_range:
                                        timeline.frame_start = int(action.frame_start)
                                        timeline.frame_end = int(action.frame_end)
                                    else:
                                        timeline.frame_start = timeline_start
                                        timeline.frame_end = timeline_end
                                    if using_better_fbx:
                                        obj_selection = [obj for obj in context.selected_objects]
                                        export_better_fbx(context, True, **keywords)
                                        for obj in obj_selection:
                                            obj.select_set(True)
                                    else:
                                        export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'animations', halo_objects, '', '', model_armature, skeleton_bones, **keywords)
                                    gr2_count += 1
                                except:
                                    print('Encountered animation not in armature, skipping export of animation: ' + action.name)
                            
                elif sidecar_type == 'SCENARIO':
                    
                    bsp_list = []
                    shared_bsp_exists = False

                    for ob in bpy.context.scene.objects:
                        if ob.halo_json.bsp_name_locked != '':
                            if not ob.halo_json.bsp_shared and (ob.halo_json.bsp_name_locked not in bsp_list):
                                bsp_list.append(ob.halo_json.bsp_name_locked)
                        else:
                            if not ob.halo_json.bsp_shared and (ob.halo_json.bsp_name not in bsp_list):
                                bsp_list.append(ob.halo_json.bsp_name)

                    for ob in context.scene.objects:
                        if ob.halo_json.bsp_shared:
                            shared_bsp_exists = True
                            break

                    for bsp in bsp_list:
                        if export_structure:
                            perm_list = []
                            for ob in halo_objects.structure:
                                if not ob.halo_json.bsp_shared:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.structure, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'bsp', halo_objects, bsp, perm, **keywords)
                                            gr2_count += 1

                            if export_poops:
                                perm_list = []
                                for ob in halo_objects.poops:
                                    if not ob.halo_json.bsp_shared:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectBSPObject(halo_objects.poops, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                                if using_better_fbx:
                                                    obj_selection = [obj for obj in context.selected_objects]
                                                    export_better_fbx(context, False, **keywords)
                                                    for obj in obj_selection:
                                                        obj.select_set(True)
                                                else:
                                                    export_fbx(self, context, **keywords)
                                                export_gr2(self, context, report, asset_path, asset, IsWindows(), 'poops', halo_objects, bsp, perm, **keywords)
                                                gr2_count += 1

                            if export_markers:
                                perm_list = []
                                for ob in halo_objects.markers:
                                    if not ob.halo_json.bsp_shared:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectBSPObject(halo_objects.markers, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                                if using_better_fbx:
                                                    obj_selection = [obj for obj in context.selected_objects]
                                                    export_better_fbx(context, False, **keywords)
                                                    for obj in obj_selection:
                                                        obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'markers', halo_objects, bsp, perm, **keywords)
                                            gr2_count += 1

                            if export_lights:
                                perm_list = []
                                for ob in halo_objects.lights:
                                    if not ob.halo_json.bsp_shared:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectBSPObject(halo_objects.lights, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                                if using_better_fbx:
                                                    obj_selection = [obj for obj in context.selected_objects]
                                                    export_better_fbx(context, False, **keywords)
                                                    for obj in obj_selection:
                                                        obj.select_set(True)
                                                else:
                                                    export_fbx(self, context, **keywords)
                                                export_gr2(self, context, report, asset_path, asset, IsWindows(), 'lights', halo_objects, bsp, perm, **keywords)
                                                gr2_count += 1

                            if export_portals:
                                perm_list = []
                                for ob in halo_objects.portals:
                                    if not ob.halo_json.bsp_shared:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectBSPObject(halo_objects.portals, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                                if using_better_fbx:
                                                    obj_selection = [obj for obj in context.selected_objects]
                                                    export_better_fbx(context, False, **keywords)
                                                    for obj in obj_selection:
                                                        obj.select_set(True)
                                                else:
                                                    export_fbx(self, context, **keywords)
                                                export_gr2(self, context, report, asset_path, asset, IsWindows(), 'portals', halo_objects, bsp, perm, **keywords)
                                                gr2_count += 1

                            if export_seams:
                                perm_list = []
                                for ob in halo_objects.seams:
                                    if not ob.halo_json.bsp_shared:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectBSPObject(halo_objects.seams, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                                if using_better_fbx:
                                                    obj_selection = [obj for obj in context.selected_objects]
                                                    export_better_fbx(context, False, **keywords)
                                                    for obj in obj_selection:
                                                        obj.select_set(True)
                                                else:
                                                    export_fbx(self, context, **keywords)
                                                export_gr2(self, context, report, asset_path, asset, IsWindows(), 'seams', halo_objects, bsp, perm, **keywords)
                                                gr2_count += 1

                            if export_water_surfaces:
                                perm_list = []
                                for ob in halo_objects.water_surfaces:
                                    if not ob.halo_json.bsp_shared:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectBSPObject(halo_objects.water_surfaces, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                                if using_better_fbx:
                                                    obj_selection = [obj for obj in context.selected_objects]
                                                    export_better_fbx(context, False, **keywords)
                                                    for obj in obj_selection:
                                                        obj.select_set(True)
                                                else:
                                                    export_fbx(self, context, **keywords)
                                                export_gr2(self, context, report, asset_path, asset, IsWindows(), 'water', halo_objects, bsp, perm, **keywords)
                                                gr2_count += 1


                            if export_lightmap_regions:
                                perm_list = []
                                for ob in halo_objects.lightmap_regions:
                                    if not ob.halo_json.bsp_shared:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectBSPObject(halo_objects.lightmap_regions, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                                if using_better_fbx:
                                                    obj_selection = [obj for obj in context.selected_objects]
                                                    export_better_fbx(context, False, **keywords)
                                                    for obj in obj_selection:
                                                        obj.select_set(True)
                                                else:
                                                    export_fbx(self, context, **keywords)
                                                export_gr2(self, context, report, asset_path, asset, IsWindows(), 'lightmap_region', halo_objects, bsp, perm, **keywords)
                                                gr2_count += 1
                            # Design time!
                            bsp_list = []

                            for ob in bpy.context.scene.objects:
                                if ob.halo_json.bsp_name_locked != '':
                                    if not ob.halo_json.bsp_shared and (ob.halo_json.bsp_name_locked not in bsp_list) and (sel_logic.ObBoundarys(ob) or sel_logic.ObWaterPhysics(ob) or sel_logic.ObPoopRains(ob) or sel_logic.ObFog(ob)):
                                        bsp_list.append(ob.halo_json.bsp_name_locked)
                                else:
                                    if not ob.halo_json.bsp_shared and (ob.halo_json.bsp_name not in bsp_list) and (sel_logic.ObBoundarys(ob) or sel_logic.ObWaterPhysics(ob) or sel_logic.ObPoopRains(ob) or sel_logic.ObFog(ob)):
                                        bsp_list.append(ob.halo_json.bsp_name)

                            if export_fog_planes:
                                perm_list = []
                                for ob in halo_objects.fog:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.fog, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'fog', halo_objects, bsp, perm, **keywords)
                                            gr2_count += 1

                            if export_boundary_surfaces:
                                perm_list = []
                                for ob in halo_objects.boundary_surfaces:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.boundary_surfaces, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'design', halo_objects, bsp, perm, **keywords)
                                            gr2_count += 1

                            if export_water_physics:
                                perm_list = []
                                for ob in halo_objects.water_physics:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.water_physics, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'water_physics', halo_objects, bsp, perm, **keywords)
                                            gr2_count += 1

                            if export_rain_occluders:
                                perm_list = []
                                for ob in halo_objects.rain_occluders:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.rain_occluders, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'rain_blockers', halo_objects, bsp, perm, **keywords)
                                            gr2_count += 1



                    ############################
                    ##### SHARED STRUCTURE #####
                    ############################

                    if shared_bsp_exists:
                        if export_structure:
                            perm_list = []
                            for ob in halo_objects.structure:
                                if ob.halo_json.bsp_shared:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.structure, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'bsp', halo_objects, 'shared', perm, **keywords)
                                            gr2_count += 1

                        if export_poops:
                            perm_list = []
                            for ob in halo_objects.poops:
                                if ob.halo_json.bsp_shared:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.poops, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'poops', halo_objects, 'shared', perm, **keywords)
                                            gr2_count += 1

                        if export_markers:
                            perm_list = []
                            for ob in halo_objects.markers:
                                if ob.halo_json.bsp_shared:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.markers, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'markers', halo_objects, 'shared', perm, **keywords)
                                            gr2_count += 1
                                    
                        if export_lights:
                            perm_list = []
                            for ob in halo_objects.lights:
                                if ob.halo_json.bsp_shared:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.lights, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'lights', halo_objects, 'shared', perm, **keywords)
                                            gr2_count += 1

                        if export_portals:
                            perm_list = []
                            for ob in halo_objects.portals:
                                if ob.halo_json.bsp_shared:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.portals, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'portals', halo_objects, 'shared', perm, **keywords)
                                            gr2_count += 1

                        if export_seams:
                            perm_list = []
                            for ob in halo_objects.seams:
                                if ob.halo_json.bsp_shared:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.seams, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'seams', halo_objects, 'shared', perm, **keywords)
                                            gr2_count += 1

                        if export_water_surfaces:
                            perm_list = []
                            for ob in halo_objects.water_surfaces:
                                if ob.halo_json.bsp_shared:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.water_surfaces, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'water', halo_objects, 'shared', perm, **keywords)
                                            gr2_count += 1

                        if export_lightmap_regions:
                            perm_list = []
                            for ob in halo_objects.lightmap_regions:
                                if ob.halo_json.bsp_shared:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.lightmap_regions, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'lightmap_region', halo_objects, 'shared', perm, **keywords)
                                            gr2_count += 1

                elif sidecar_type == 'SKY':
                    if export_render:
                        perm_list = []
                        for ob in halo_objects.render:
                            perm = GetPerm(ob)
                            if perm not in perm_list:
                                perm_list.append(perm)
                                if SelectModelObject(halo_objects.render + halo_objects.lights + halo_objects.markers, perm, model_armature, export_hidden, export_all_perms, export_specific_perm):
                                    if using_better_fbx:
                                        obj_selection = [obj for obj in context.selected_objects]
                                        export_better_fbx(context, False, **keywords)
                                        for obj in obj_selection:
                                            obj.select_set(True)
                                    else:
                                        export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'render', halo_objects, '', perm, model_armature, skeleton_bones, **keywords)
                                    gr2_count += 1

                elif sidecar_type == 'DECORATOR SET': 
                    if export_render:
                        if SelectModelObjectNoPerm(halo_objects.decorator, model_armature, export_hidden):
                            if using_better_fbx:
                                obj_selection = [obj for obj in context.selected_objects]
                                export_better_fbx(context, False, **keywords)
                                for obj in obj_selection:
                                    obj.select_set(True)
                            else:
                                export_fbx(self, context, **keywords)
                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'render', halo_objects, '', 'default', model_armature, skeleton_bones, **keywords)
                            gr2_count += 1

                else: # for particles
                    if export_render:
                        if SelectModelObjectNoPerm(halo_objects.particle, model_armature, export_hidden):
                            if using_better_fbx:
                                obj_selection = [obj for obj in context.selected_objects]
                                export_better_fbx(context, False, **keywords)
                                for obj in obj_selection:
                                    obj.select_set(True)
                            else:
                                export_fbx(self, context, **keywords)
                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'particle_model', halo_objects, '', 'default', model_armature, skeleton_bones, **keywords)
                            gr2_count += 1
            else:
                if using_better_fbx:
                    export_better_fbx(context, False, **keywords)
                else:
                    export_fbx(self, context, **keywords)
                export_gr2(self, context, report, asset_path, asset, IsWindows(), 'selected', **keywords)

            
            reports.append('Exported ' + str(gr2_count) + ' GR2 Files')
            if(IsWindows()):
                if export_sidecar_xml:
                    from .export_sidecar import export_sidecar
                    export_sidecar(self, context, report, asset_path, halo_objects, model_armature, lod_count, **keywords)
                    reports.append('Built ' + str.title(sidecar_type) + ' Sidecar')
                from .import_sidecar import import_sidecar
                import_sidecar(self, context, report, **keywords)
                reports.append('Tag Export Processed')
                if lightmap_structure and not skip_lightmapper:
                    from .run_lightmapper import run_lightmapper
                    run_lightmapper(self, context, report, **keywords)
                    reports.append('Processed a Lightmap on ' + str.title(lightmap_quality) + ' Quality')
                # if import_bitmaps:
                #     print("Temporary implementation, remove this later!")
                #     #import_bitmap.save(self, context, report, **keywords)

        elif(not export_sidecar_xml):
            export_fbx(self, context, **keywords)
            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'selected', **keywords)
        else:
            report({'ERROR'},"No sidecar output tags selected")

    else:
        if GetEKPath() == None or GetEKPath() == '' or not exists(GetToolPath()):
            ctypes.windll.user32.MessageBoxW(0, "Invalid Editing Kit path. Please check your editing kit path in add-on preferences and try again.", "INVALID EK PATH", 0)
        else:
            ctypes.windll.user32.MessageBoxW(0, "The selected export folder is invalid, please select one within the data folder of your HEK tools.", "INVALID EXPORT PATH", 0)
    
    final_report = ''
    for idx, r in enumerate(reports):
        final_report = final_report + r
        if idx + 1 < len(reports):
            final_report = final_report + ' | '

    if quick_export:
        context.scene.gr2_export.final_report = final_report
    else:
        report({'INFO'}, final_report)


#####################################################################################
#####################################################################################
# OBJECT SELECTION FUNCTIONS     

def SelectModelSkeleton(arm):
    DeselectAllObjects()
    arm.select_set(True)

    return True


#####################################################################################
#####################################################################################
# EXTRA FUNCTIONS

def CheckPath(filePath):
    if(filePath.startswith(os.path.abspath(GetEKPath() + "\\data")+os.sep)):
        return True
    else:
        return False

#####################################################################################
#####################################################################################
# BETTER FBX INTEGRATION

def export_better_fbx(context, export_animation, filepath, use_armature_deform_only, mesh_smooth_type_better, use_mesh_modifiers, use_triangles, global_scale, **kwargs):
    if IsWindows():
        better_fbx_folder = GetBetterFBXFolder()
        if platform.machine().endswith('64'):
            exe = os.path.join(better_fbx_folder, 'bin', 'Windows', 'x64', 'fbx-utility')
        else:
            exe = os.path.join(better_fbx_folder, 'bin', 'Windows', 'x86', 'fbx-utility')
        output = os.path.join(better_fbx_folder, 'data', uuid.uuid4().hex + '.txt')
        from better_fbx.exporter import write_some_data as SetFBXData
        data_args = GetDataArgs(context, output, export_animation, use_armature_deform_only, mesh_smooth_type_better, use_mesh_modifiers)
        SetFBXData(*data_args)
        fbx_command = GetExeArgs(exe, output, filepath, global_scale, use_triangles, mesh_smooth_type_better)
        p = Popen(fbx_command)
        p.wait()
        os.remove(output)
        return {'FINISHED'}
    else:
        ctypes.windll.user32.MessageBoxW(0, "BetterFBX option is not supported on your OS. Please use the standard FBX option.", "OS NOT SUPPORTED", 0)
        return {'FINISHED'}

def GetBetterFBXFolder():
    path = ''
    for mod in modules():
        if mod.bl_info['name'] == 'Better FBX Importer & Exporter':
            path = mod.__file__
            break
    path = path.rpartition('\\')[0]

    return path

def GetDataArgs(context, output, export_animation, use_armature_deform_only, mesh_smooth_type, use_mesh_modifiers):
    args = []
    args.append(context)
    args.append(output)
    args.append(context.selected_objects)
    args.append(export_animation)
    args.append(0) # animation offset
    args.append('active') # animation type
    args.append(use_armature_deform_only)
    args.append(False) # rigify armature
    args.append(True) # keep root bone
    args.append(False) # use only selected deform bones
    args.append('Unlimited') # number of bones that can be influenced per vertex
    args.append(False) # export vertex animation
    args.append('mcx') # vertex format
    args.append('world') # vertex space
    args.append(1) # vertex frame start
    args.append(10) # vertex frame end
    args.append(True) # export edge crease
    args.append(1.0) # scale of edge crease weights
    args.append(mesh_smooth_type)
    args.append(use_mesh_modifiers)
    args.append(False) # apply armature deform modifier on export
    args.append(False) # concat animations
    args.append(False) # embed media in fbx file
    args.append(False) # copy textures to user specified directory
    args.append('') # user directory name
    args.append([]) # texture file names

    return args

def GetExeArgs(exe, output, filepath, global_scale, use_triangles, mesh_smooth_type):
    args = []
    args.append(exe) 
    args.append(output) 
    args.append(filepath) 
    args.append(str(global_scale))
    args.append('binary')
    args.append('FBX202000') 
    args.append('MayaZUp')
    args.append('None') 
    args.append('None')
    args.append('False') 
    args.append('False')
    args.append('False') 
    args.append('None')
    args.append(str(use_triangles))
    args.append('None') 
    args.append('FBXSDK') 
    args.append('False')
    args.append('0') 
    args.append('1')
    args.append('Blender')
    args.append('False')

    return args