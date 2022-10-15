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
from os.path import exists
import os
import ctypes
import uuid
import platform
from subprocess import Popen
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
)

#####################################################################################
#####################################################################################
# MAIN FUNCTION

def process_scene(self, context, keywords, report, model_armature, asset_path, asset, skeleton_bones, halo_objects, timeline_start, timeline_end, lod_count,
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
                  import_bitmaps,
                  **kwargs
    ):

    using_better_fbx = False

    try:
        from better_fbx.exporter import write_some_data as SetFBXData
        using_better_fbx = True
        print('Found Better FBX exporter')
    except:
        from io_scene_fbx.export_fbx_bin import save as export_fbx
        print("Could not find Better FBX exporter. Using Blender's native fbx exporter")

    from .export_gr2 import export_gr2

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

                    if SelectModelSkeleton(model_armature):
                        if using_better_fbx:
                            obj_selection = [obj for obj in context.selected_objects]
                            export_better_fbx(context, False, **keywords)
                            for obj in obj_selection:
                                obj.select_set(True)
                        else:
                            export_fbx(self, context, **keywords)
                        export_gr2(self, context, report, asset_path, asset, IsWindows(), 'skeleton', halo_objects, '', '', model_armature, skeleton_bones, **keywords)

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
                                except:
                                    print('Encountered animation not in armature, skipping export of animation: ' + action.name)
                            
                elif sidecar_type == 'SCENARIO':
                    
                    bsp_list = []
                    shared_bsp_exists = False

                    for ob in bpy.data.objects:
                        if not ob.halo_json.bsp_shared and (ob.halo_json.bsp_index not in bsp_list):
                            bsp_list.append(ob.halo_json.bsp_index)

                    for ob in bpy.data.objects:
                        if ob.halo_json.bsp_shared:
                            shared_bsp_exists = True
                            break

                    for bsp in bsp_list:
                        if not ob.halo_json.bsp_shared:
                            if export_structure:
                                perm_list = []
                                for ob in halo_objects.structure:
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
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'bsp', halo_objects, "{0:03}".format(bsp), perm, **keywords)

                            if export_poops:
                                perm_list = []
                                for ob in halo_objects.poops:
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
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'poops', halo_objects, "{0:03}".format(bsp), perm, **keywords)

                            if export_markers:
                                perm_list = []
                                for ob in halo_objects.markers:
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
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'markers', halo_objects, "{0:03}".format(bsp), perm, **keywords)

                            if export_lights:
                                perm_list = []
                                for ob in halo_objects.lights:
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
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'lights', halo_objects, "{0:03}".format(bsp), perm, **keywords)

                            if export_portals:
                                perm_list = []
                                for ob in halo_objects.portals:
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
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'portals', halo_objects, "{0:03}".format(bsp), perm, **keywords)

                            if export_seams:
                                perm_list = []
                                for ob in halo_objects.seams:
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
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'seams', halo_objects, "{0:03}".format(bsp), perm, **keywords)

                            if export_water_surfaces:
                                perm_list = []
                                for ob in halo_objects.water_surfaces:
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
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'water', halo_objects, "{0:03}".format(bsp), perm, **keywords)

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
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'fog', halo_objects, "{0:03}".format(bsp), perm, **keywords)

                            if export_cookie_cutters:
                                perm_list = []
                                for ob in halo_objects.cookie_cutters:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.cookie_cutters, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'cookie_cutters', halo_objects, "{0:03}".format(bsp), perm, **keywords)

                            if export_lightmap_regions:
                                perm_list = []
                                for ob in halo_objects.lightmap_regions:
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
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'lightmap_region', halo_objects, "{0:03}".format(bsp), perm, **keywords)

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
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'design', halo_objects, "{0:03}".format(bsp), perm, **keywords)

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
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'water_physics', halo_objects, "{0:03}".format(bsp), perm, **keywords)

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
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'rain_blockers', halo_objects, "{0:03}".format(bsp), perm, **keywords)



                    ############################
                    ##### SHARED STRUCTURE #####
                    ############################

                    if shared_bsp_exists:
                        if export_structure:
                            perm_list = []
                            for ob in halo_objects.structure:
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

                        if export_poops:
                            perm_list = []
                            for ob in halo_objects.poops:
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

                        if export_markers:
                            perm_list = []
                            for ob in halo_objects.markers:
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
                                    
                        if export_lights:
                            perm_list = []
                            for ob in halo_objects.lights:
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

                        if export_portals:
                            perm_list = []
                            for ob in halo_objects.portals:
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

                        if export_seams:
                            perm_list = []
                            for ob in halo_objects.seams:
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

                        if export_water_surfaces:
                            perm_list = []
                            for ob in halo_objects.water_surfaces:
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

                        if export_lightmap_regions:
                            perm_list = []
                            for ob in halo_objects.lightmap_regions:
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

                            if export_fog_planes:
                                perm_list = []
                                for ob in halo_objects.fog:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.fog, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'fog', halo_objects, 'shared', perm, **keywords)

                            if export_cookie_cutters:
                                perm_list = []
                                for ob in halo_objects.cookie_cutters:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.cookie_cutters, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'cookie_cutters', halo_objects, 'shared', perm, **keywords)

                        if export_boundary_surfaces:
                            perm_list = []
                            for ob in halo_objects.boundary_surfaces:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    if SelectBSPObject(halo_objects.boundary_surfaces, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                        if using_better_fbx:
                                            obj_selection = [obj for obj in context.selected_objects]
                                            export_better_fbx(context, False, **keywords)
                                            for obj in obj_selection:
                                                obj.select_set(True)
                                        else:
                                            export_fbx(self, context, **keywords)
                                        export_gr2(self, context, report, asset_path, asset, IsWindows(), 'design', halo_objects, 'shared', perm, **keywords)

                        if export_water_physics:
                            perm_list = []
                            for ob in halo_objects.water_physics:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    if SelectBSPObject(halo_objects.water_physics, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                        if using_better_fbx:
                                            obj_selection = [obj for obj in context.selected_objects]
                                            export_better_fbx(context, False, **keywords)
                                            for obj in obj_selection:
                                                obj.select_set(True)
                                        else:
                                            export_fbx(self, context, **keywords)
                                        export_gr2(self, context, report, asset_path, asset, IsWindows(), 'water_physics', halo_objects, 'shared', perm, **keywords)

                        if export_rain_occluders:
                            perm_list = []
                            for ob in halo_objects.rain_occluders:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    if SelectBSPObject(halo_objects.rain_occluders, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                        if using_better_fbx:
                                            obj_selection = [obj for obj in context.selected_objects]
                                            export_better_fbx(context, False, **keywords)
                                            for obj in obj_selection:
                                                obj.select_set(True)
                                        else:
                                            export_fbx(self, context, **keywords)
                                        export_gr2(self, context, report, asset_path, asset, IsWindows(), 'rain_blockers', halo_objects, 'shared', perm, **keywords)

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

                elif sidecar_type == 'DECORATOR SET': 
                    if export_render:
                        if SelectModelObjectNoPerm(halo_objects.decorator, model_armature, export_hidden):
                            print('found a decorator mesh')
                            if using_better_fbx:
                                obj_selection = [obj for obj in context.selected_objects]
                                export_better_fbx(context, False, **keywords)
                                for obj in obj_selection:
                                    obj.select_set(True)
                            else:
                                export_fbx(self, context, **keywords)
                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'render', halo_objects, '', 'default', model_armature, skeleton_bones, **keywords)

                else: # for particles
                    if export_render:
                        if SelectModelObjectNoPerm(halo_objects.particle, model_armature, export_hidden):
                            print('found a decorator mesh')
                            if using_better_fbx:
                                obj_selection = [obj for obj in context.selected_objects]
                                export_better_fbx(context, False, **keywords)
                                for obj in obj_selection:
                                    obj.select_set(True)
                            else:
                                export_fbx(self, context, **keywords)
                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'particle_model', halo_objects, '', 'default', model_armature, skeleton_bones, **keywords)

            else:
                if using_better_fbx:
                    export_better_fbx(context, False, **keywords)
                else:
                    export_fbx(self, context, **keywords)
                export_gr2(self, context, report, asset_path, asset, IsWindows(), 'selected', **keywords)

            
            if(IsWindows()):
                if export_sidecar_xml:
                    from .export_sidecar import export_sidecar
                    export_sidecar(self, context, report, asset_path, halo_objects, model_armature, lod_count, **keywords)
                from .import_sidecar import import_sidecar
                import_sidecar(self, context, report, **keywords)
                if lightmap_structure:
                    from .run_lightmapper import run_lightmapper
                    run_lightmapper(self, context, report, **keywords)
                if import_bitmaps:
                    print("Temporary implementation, remove this later!")
                    #import_bitmap.save(self, context, report, **keywords)

        elif(not export_sidecar_xml):
            export_fbx(self, context, **keywords)
            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'selected', **keywords)
        else:
            report({'ERROR'},"No sidecar output tags selected")

    else:
        if GetEKPath() == None or GetEKPath() == '' or not exists(GetToolPath()):
            ctypes.windll.user32.MessageBoxW(0, "Invalid Editing Kit path. Please check your editing kit path in add-on preferences and try again.", "Invalid EK Path", 0)
        else:
            ctypes.windll.user32.MessageBoxW(0, "The selected export folder is invalid, please select one within the data folder of your HEK tools.", "Invalid Export Path", 0)

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

def export_better_fbx(context, export_animation, filepath, use_armature_deform_only, mesh_smooth_type, use_mesh_modifiers, use_triangles, global_scale, **kwargs):
    print('start export_better_fbx')
    print(filepath)
    if IsWindows():
        scripts_folder = bpy.utils.user_resource('SCRIPTS')
        exe = os.path.join(scripts_folder, 'addons', 'better_fbx', 'bin', 'Windows', 'x64', 'fbx-utility')
        print('using x64 windows')
        print(exe)
        output = os.path.join(scripts_folder, 'addons', 'better_fbx', 'data', uuid.uuid4().hex + '.txt')
        from better_fbx.exporter import write_some_data as SetFBXData
        SetFBXData(context, output, context.selected_objects, export_animation, '0', 'active', use_armature_deform_only, False, True, False, 4, False, 'mcx', 'world', 1, 10, True, 1.0, mesh_smooth_type, use_mesh_modifiers, False, False, False, False, '', [])
        fbx_command = GetExeArgs(exe, output, filepath, global_scale, use_triangles, mesh_smooth_type)
        p = Popen(fbx_command)
        p.wait()

    return {'FINISHED'}

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