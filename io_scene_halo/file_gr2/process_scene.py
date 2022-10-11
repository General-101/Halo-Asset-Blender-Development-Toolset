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
from ..gr2_utils import(
    GetPerm,
    IsWindows,
    SelectModelObject,
    SelectModelObjectNoPerm,
    SelectBSPObject,
    GetEKPath,
    GetToolPath,
    DeselectAllObjects
)

#####################################################################################
#####################################################################################
# MAIN FUNCTION

def process_scene(self, context, keywords, report, model_armature, asset_path, asset, skeleton_bones, halo_objects, timeline_start, timeline_end,
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

    from io_scene_fbx.export_fbx_bin import save as export_fbx # import fbx exporter code
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
                                    print('exporting render ' + perm)
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'render', '', perm, model_armature, skeleton_bones, **keywords)

                    if export_collision:
                        perm_list = []
                        for ob in halo_objects.collision:
                            perm = GetPerm(ob)
                            if perm not in perm_list:
                                perm_list.append(perm)
                                if SelectModelObject(halo_objects.collision, perm, model_armature, export_hidden, export_all_perms, export_specific_perm):
                                    print('exporting collision ' + perm)
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'collision', '', perm, model_armature, skeleton_bones, **keywords)

                    if export_physics:
                        perm_list = []
                        for ob in halo_objects.physics:
                            perm = GetPerm(ob)
                            if perm not in perm_list:
                                perm_list.append(perm)
                                if SelectModelObject(halo_objects.physics, perm, model_armature, export_hidden, export_all_perms, export_specific_perm):
                                    print('exporting physics ' + perm)
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'physics', '', perm, model_armature, skeleton_bones, **keywords)

                    if export_markers:
                        if SelectModelObjectNoPerm(halo_objects.markers, model_armature, export_hidden):
                            print('exporting markers ')
                            export_fbx(self, context, **keywords)
                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'markers', '', '', model_armature, skeleton_bones, **keywords)

                    if SelectModelSkeleton(model_armature):
                        export_fbx(self, context, **keywords)
                        export_gr2(self, context, report, asset_path, asset, IsWindows(), 'skeleton', '', '', model_armature, skeleton_bones, **keywords)

                    if export_animations and 1<=len(bpy.data.actions):
                        if SelectModelSkeleton(model_armature):
                            timeline = bpy.data.scene
                            for action in bpy.data.actions:
                                try:
                                    model_armature.animation_data.action = action
                                    if action.use_frame_range:
                                        timeline.frame_start = int(action.frame_start)
                                        timeline.frame_end = int(action.frame_end)
                                    else:
                                        timeline.frame_start = timeline_start
                                        timeline.frame_end = timeline_end
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'animations', '', '', model_armature, skeleton_bones, **keywords)
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
                                            print('exporting structure ' + perm)
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'bsp', "{0:03}".format(bsp), perm, **keywords)

                            if export_poops:
                                perm_list = []
                                for ob in halo_objects.poops:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.poops, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            print('exporting poops ' + perm)
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'poops', "{0:03}".format(bsp), perm, **keywords)

                            if export_markers:
                                perm_list = []
                                for ob in halo_objects.markers:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.markers, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'markers', "{0:03}".format(bsp), perm, **keywords)

                            if export_lights:
                                perm_list = []
                                for ob in halo_objects.lights:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.lights, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'lights', "{0:03}".format(bsp), perm, **keywords)

                            if export_portals:
                                perm_list = []
                                for ob in halo_objects.portals:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.portals, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            print('exporting portals ' + perm)
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'portals', "{0:03}".format(bsp), perm, **keywords)

                            if export_seams:
                                perm_list = []
                                for ob in halo_objects.seams:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.seams, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'seams', "{0:03}".format(bsp), perm, **keywords)

                            if export_water_surfaces:
                                perm_list = []
                                for ob in halo_objects.water_surfaces:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.water_surfaces, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'water', "{0:03}".format(bsp), perm, **keywords)

                            if export_fog_planes:
                                perm_list = []
                                for ob in halo_objects.fog:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.fog, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'fog', "{0:03}".format(bsp), perm, **keywords)

                            if export_cookie_cutters:
                                perm_list = []
                                for ob in halo_objects.cookie_cutters:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.cookie_cutters, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'cookie_cutters', "{0:03}".format(bsp), perm, **keywords)

                            if export_lightmap_regions:
                                perm_list = []
                                for ob in halo_objects.lightmap_regions:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.lightmap_regions, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'lightmap_region', "{0:03}".format(bsp), perm, **keywords)

                            if export_boundary_surfaces:
                                perm_list = []
                                for ob in halo_objects.boundary_surfaces:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.boundary_surfaces, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'design', "{0:03}".format(bsp), perm, **keywords)

                            if export_water_physics:
                                perm_list = []
                                for ob in halo_objects.water_physics:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.water_physics, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'water_physics', "{0:03}".format(bsp), perm, **keywords)

                            if export_rain_occluders:
                                perm_list = []
                                for ob in halo_objects.rain_occluders:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.rain_occluders, bsp, model_armature, False, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'rain_blockers', "{0:03}".format(bsp), perm, **keywords)



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
                                    SelectBSPObject(halo_objects.structure, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp)
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'bsp', 'shared', perm, **keywords)

                        if export_poops:
                            perm_list = []
                            for ob in halo_objects.poops:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    SelectBSPObject(halo_objects.poops, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp)
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'poops', 'shared', perm, **keywords)

                        if export_markers:
                            perm_list = []
                            for ob in halo_objects.markers:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    SelectBSPObject(halo_objects.markers, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp)
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'markers', 'shared', perm, **keywords)
                                    
                        if export_lights:
                            perm_list = []
                            for ob in halo_objects.lights:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    SelectBSPObject(halo_objects.lights, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp)
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'lights', 'shared', perm, **keywords)

                        if export_portals:
                            perm_list = []
                            for ob in halo_objects.portals:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    SelectBSPObject(halo_objects.portals, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp)
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'portals', 'shared', perm, **keywords)

                        if export_seams:
                            perm_list = []
                            for ob in halo_objects.seams:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    SelectBSPObject(halo_objects.seams, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp)
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'seams', 'shared', perm, **keywords)

                        if export_water_surfaces:
                            perm_list = []
                            for ob in halo_objects.water_surfaces:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    SelectBSPObject(halo_objects.water_surfaces, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp)
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'water', 'shared', perm, **keywords)

                        if export_lightmap_regions:
                            perm_list = []
                            for ob in halo_objects.lightmap_regions:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    SelectBSPObject(halo_objects.lightmap_regions, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp)
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'lightmap_region', 'shared', perm, **keywords)

                            if export_fog_planes:
                                perm_list = []
                                for ob in halo_objects.fog:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.fog, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'fog', 'shared', perm, **keywords)

                            if export_cookie_cutters:
                                perm_list = []
                                for ob in halo_objects.cookie_cutters:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if SelectBSPObject(halo_objects.cookie_cutters, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
                                            export_fbx(self, context, **keywords)
                                            export_gr2(self, context, report, asset_path, asset, IsWindows(), 'cookie_cutters', 'shared', perm, **keywords)

                        if export_boundary_surfaces:
                            perm_list = []
                            for ob in halo_objects.boundary_surfaces:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    SelectBSPObject(halo_objects.boundary_surfaces, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp)
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'design', 'shared', perm, **keywords)

                        if export_water_physics:
                            perm_list = []
                            for ob in halo_objects.water_physics:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    SelectBSPObject(halo_objects.water_physics, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp)
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'water_physics', 'shared', perm, **keywords)

                        if export_rain_occluders:
                            perm_list = []
                            for ob in halo_objects.rain_occluders:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    SelectBSPObject(halo_objects.rain_occluders, bsp, model_armature, True, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp)
                                    export_fbx(self, context, **keywords)
                                    export_gr2(self, context, report, asset_path, asset, IsWindows(), 'rain_blockers', 'shared', perm, **keywords)

                elif sidecar_type == 'DECORATOR':
                    print('not implemented')

                elif sidecar_type == 'PARTICLE MODEL':
                    print('not implemented')

            else:
                export_fbx(self, context, **keywords)
                export_gr2(self, context, report, asset_path, asset, IsWindows(), 'selected', **keywords)

            
            if(IsWindows()):
                if export_sidecar_xml:
                    from .export_sidecar import export_sidecar
                    export_sidecar(self, context, report, asset_path, model_armature, **keywords)
                from .import_sidecar import import_sidecar
                print('1')
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