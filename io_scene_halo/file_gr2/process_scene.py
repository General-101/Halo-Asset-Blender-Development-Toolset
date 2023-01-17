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
from addon_utils import modules
from .nwo_utils import(
    get_perm,
    select_model_objects,
    select_model_objects_no_perm,
    select_bsp_objects,
    select_prefab_objects,
    get_ek_path,
    get_tool_path,
    deselect_all_objects,
    is_shared,
    get_structure_from_halo_objects,
    get_design_from_halo_objects,
    get_render_from_halo_objects,
    get_prefab_from_halo_objects,
    print_box,
    not_bungie_game,

    CheckType,
)

#####################################################################################
#####################################################################################
# MAIN FUNCTION

def process_scene(self, context, keywords, report, model_armature, asset_path, asset, skeleton_bones, halo_objects, timeline_start, timeline_end, lod_count, using_better_fbx, skip_lightmapper, selected_perms, selected_bsps, regions_dict, global_materials_dict,
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
                  export_hidden,
                  export_render,
                  export_collision,
                  export_physics,
                  export_markers,
                  export_animations,
                  export_structure,
                  export_design,
                  export_all_perms,
                  export_all_bsps,
                  export_sidecar_xml,
                  lightmap_structure,
                  lightmap_quality,
                  quick_export,
                  import_to_game,
                  #import_bitmaps,
                  export_gr2_files,
                  game_version,
                  **kwargs
    ):
    

    if using_better_fbx:
        print('Found Better FBX exporter')
    else:
        from io_scene_fbx.export_fbx_bin import save as export_fbx
        # print("Could not find Better FBX exporter (or it is not enabled). Using Blender's native fbx exporter")

    from .export_gr2 import export_gr2

    reports = []
    gr2_count = 0

    if CheckPath(filepath) and exists(f'{get_tool_path()}.exe'): # check the user is saving the file to a location in their editing kit data directory AND tool exists
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
        
            if export_gr2_files:

                if sidecar_type == 'MODEL':

                    if export_render:
                        perm_list = []
                        for ob in get_render_from_halo_objects(halo_objects):
                            perm = get_perm(ob)
                            if perm not in perm_list:
                                perm_list.append(perm)
                                if select_model_objects(get_render_from_halo_objects(halo_objects), perm, model_armature, export_hidden, export_all_perms, selected_perms):
                                    print_box(f'**Exporting {perm} render model**')
                                    if using_better_fbx:
                                        obj_selection = [obj for obj in context.selected_objects]
                                        export_better_fbx(context, False, **keywords)
                                        for obj in obj_selection:
                                            obj.select_set(True)
                                    else:
                                        export_fbx(self, context, **keywords)
                                    export_gr2(report, asset_path, asset, 'render', context.selected_objects, '', perm, model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                                    gr2_count += 1

                    if export_collision:
                        perm_list = []
                        for ob in halo_objects.collision:
                            perm = get_perm(ob)
                            if perm not in perm_list:
                                perm_list.append(perm)
                                if select_model_objects(halo_objects.collision, perm, model_armature, export_hidden, export_all_perms, selected_perms):
                                    print_box(f'**Exporting {perm} collision model**')
                                    if using_better_fbx:
                                        obj_selection = [obj for obj in context.selected_objects]
                                        export_better_fbx(context, False, **keywords)
                                        for obj in obj_selection:
                                            obj.select_set(True)
                                    else:
                                        export_fbx(self, context, **keywords)
                                    export_gr2(report, asset_path, asset, 'collision', context.selected_objects, '', perm, model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                                    gr2_count += 1

                    if export_physics:
                        perm_list = []
                        for ob in halo_objects.physics:
                            perm = get_perm(ob)
                            if perm not in perm_list:
                                perm_list.append(perm)
                                if select_model_objects(halo_objects.physics, perm, model_armature, export_hidden, export_all_perms, selected_perms):
                                    print_box(f'**Exporting {perm} physics model**')
                                    if using_better_fbx:
                                        obj_selection = [obj for obj in context.selected_objects]
                                        export_better_fbx(context, False, **keywords)
                                        for obj in obj_selection:
                                            obj.select_set(True)
                                    else:
                                        export_fbx(self, context, **keywords)
                                    export_gr2(report, asset_path, asset, 'physics', context.selected_objects, '', perm, model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                                    gr2_count += 1

                    if export_markers:
                        if select_model_objects_no_perm(halo_objects.markers, model_armature, export_hidden):
                            print_box('**Exporting markers**')
                            if using_better_fbx:
                                obj_selection = [obj for obj in context.selected_objects]
                                export_better_fbx(context, False, **keywords)
                                for obj in obj_selection:
                                    obj.select_set(True)
                            else:
                                export_fbx(self, context, **keywords)
                            export_gr2(report, asset_path, asset, 'markers', context.selected_objects, '', '', model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                            gr2_count += 1

                    if SelectModelSkeleton(model_armature):
                        print_box('**Exporting skeleton**')
                        if using_better_fbx:
                            export_better_fbx(context, False, **keywords)
                            model_armature.select_set(True)
                        else:
                            export_fbx(self, context, **keywords)
                        export_gr2(report, asset_path, asset, 'skeleton', [model_armature], '', '', model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                        gr2_count += 1

                    if export_animations and 1<=len(bpy.data.actions):
                        if SelectModelSkeleton(model_armature):
                            timeline = context.scene
                            for action in bpy.data.actions:
                                try:
                                    print_box(f'**Exporting Animation: {action.name}**')
                                    model_armature.animation_data.action = action
                                    if action.use_frame_range:
                                        timeline.frame_start = int(action.frame_start)
                                        timeline.frame_end = int(action.frame_end)
                                        context.scene.frame_set(int(action.frame_start))
                                    else:
                                        timeline.frame_start = timeline_start
                                        timeline.frame_end = timeline_end
                                        context.scene.frame_set(timeline_start)
                                    if using_better_fbx:
                                        export_better_fbx(context, True, **keywords)
                                        model_armature.select_set(True)
                                    else:
                                        export_fbx(self, context, **keywords)
                                    export_gr2(report, asset_path, asset, 'animations', [model_armature], '', '', model_armature, skeleton_bones, action.name, regions_dict, global_materials_dict, **keywords)
                                    gr2_count += 1
                                except:
                                    print(f'Encountered animation not in armature, skipping export of animation: {action.name}')
                            
                elif sidecar_type == 'SCENARIO':
                    
                    bsp_list = []
                    shared_bsp_exists = False

                    for ob in bpy.context.view_layer.objects:
                        if ob.nwo.bsp_name_locked != '':
                            if ob.nwo.bsp_name_locked != 'shared' and (ob.nwo.bsp_name_locked not in bsp_list):
                                bsp_list.append(ob.nwo.bsp_name_locked)
                        else:
                            if ob.nwo.bsp_name != 'shared' and (ob.nwo.bsp_name not in bsp_list):
                                bsp_list.append(ob.nwo.bsp_name)

                    for ob in context.view_layer.objects:
                        if ob.nwo.bsp_name_locked != '':
                            if ob.nwo.bsp_name_locked == 'shared':
                                shared_bsp_exists = True
                                break
                        else:
                            if ob.nwo.bsp_name == 'shared':
                                shared_bsp_exists = True
                                break
                    for bsp in bsp_list:
                        if export_structure:
                            perm_list = []
                            for ob in get_structure_from_halo_objects(halo_objects):
                                perm = get_perm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    if select_bsp_objects(get_structure_from_halo_objects(halo_objects), bsp, model_armature, False, perm, export_hidden, export_all_perms, selected_perms, export_all_bsps, selected_bsps):
                                        print_box(f'**Exporting {bsp} {perm} BSP**')
                                        if using_better_fbx:
                                            obj_selection = [obj for obj in context.selected_objects]
                                            export_better_fbx(context, False, **keywords)
                                            for obj in obj_selection:
                                                obj.select_set(True)
                                        else:
                                            export_fbx(self, context, **keywords)
                                        export_gr2(report, asset_path, asset, 'bsp', context.selected_objects, bsp, perm, model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                                        gr2_count += 1
                        # Design time!
                        bsp_list = []

                        for ob in bpy.context.scene.objects:
                            if ob.nwo.bsp_name_locked != '':
                                if ob.nwo.bsp_name_locked != 'shared' and (ob.nwo.bsp_name_locked not in bsp_list) and (CheckType.boundary_surface(ob) or CheckType.water_physics(ob) or CheckType.poop_rain_blocker(ob) or CheckType.fog(ob)):
                                    bsp_list.append(ob.nwo.bsp_name_locked)
                            else:
                                if ob.nwo.bsp_name != 'shared' and (ob.nwo.bsp_name not in bsp_list) and (CheckType.boundary_surface(ob) or CheckType.water_physics(ob) or CheckType.poop_rain_blocker(ob) or CheckType.fog(ob)):
                                    bsp_list.append(ob.nwo.bsp_name)

                        if export_design:
                            perm_list = []
                            for ob in get_design_from_halo_objects(halo_objects):
                                perm = get_perm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    if select_bsp_objects(get_design_from_halo_objects(halo_objects), bsp, model_armature, False, perm, export_hidden, export_all_perms, selected_perms, export_all_bsps, selected_bsps):
                                        print_box(f'**Exporting {bsp} {perm} Design**')
                                        if using_better_fbx:
                                            obj_selection = [obj for obj in context.selected_objects]
                                            export_better_fbx(context, False, **keywords)
                                            for obj in obj_selection:
                                                obj.select_set(True)
                                        else:
                                            export_fbx(self, context, **keywords)
                                        export_gr2(report, asset_path, asset, 'design', context.selected_objects, bsp, perm, model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                                        gr2_count += 1



                ############################
                ##### SHARED STRUCTURE #####
                ############################

                    if shared_bsp_exists:
                        if export_structure:
                            perm_list = []
                            for ob in get_structure_from_halo_objects(halo_objects):
                                if is_shared(ob):
                                    perm = get_perm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        if select_bsp_objects(get_structure_from_halo_objects(halo_objects), bsp, model_armature, True, perm, export_hidden, export_all_perms, selected_perms, export_all_bsps, selected_bsps):
                                            print_box(f'**Exporting shared {perm} bsp**')
                                            if using_better_fbx:
                                                obj_selection = [obj for obj in context.selected_objects]
                                                export_better_fbx(context, False, **keywords)
                                                for obj in obj_selection:
                                                    obj.select_set(True)
                                            else:
                                                export_fbx(self, context, **keywords)
                                            export_gr2(report, asset_path, asset, 'bsp', context.selected_objects, 'shared', perm, model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                                            gr2_count += 1

                elif sidecar_type == 'SKY':
                    if export_render:
                        perm_list = []
                        for ob in halo_objects.default:
                            perm = get_perm(ob)
                            if perm not in perm_list:
                                perm_list.append(perm)
                                if select_model_objects(halo_objects.default + halo_objects.lights + halo_objects.markers, perm, model_armature, export_hidden, export_all_perms, selected_perms):
                                    print_box(f'**Exporting sky render model**')
                                    if using_better_fbx:
                                        obj_selection = [obj for obj in context.selected_objects]
                                        export_better_fbx(context, False, **keywords)
                                        for obj in obj_selection:
                                            obj.select_set(True)
                                    else:
                                        export_fbx(self, context, **keywords)
                                    export_gr2(report, asset_path, asset, 'render', context.selected_objects, '', perm, model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                                    gr2_count += 1

                elif sidecar_type == 'DECORATOR SET': 
                    if export_render:
                        if select_model_objects_no_perm(halo_objects.decorators, model_armature, export_hidden):
                            print_box(f'**Exporting decorator set**')
                            if using_better_fbx:
                                obj_selection = [obj for obj in context.selected_objects]
                                export_better_fbx(context, False, **keywords)
                                for obj in obj_selection:
                                    obj.select_set(True)
                            else:
                                export_fbx(self, context, **keywords)
                            export_gr2(report, asset_path, asset, 'render', context.selected_objects, '', 'default', model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                            gr2_count += 1

                elif sidecar_type == 'PREFAB':
                    if select_prefab_objects(get_prefab_from_halo_objects(halo_objects), model_armature, export_hidden):
                        print_box(f'**Exporting prefab**')
                        if using_better_fbx:
                            obj_selection = [obj for obj in context.selected_objects]
                            export_better_fbx(context, False, **keywords)
                            for obj in obj_selection:
                                obj.select_set(True)
                        else:
                            export_fbx(self, context, **keywords)
                        export_gr2(report, asset_path, asset, 'prefab', context.selected_objects, '', '', model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                        gr2_count += 1

                else: # for particles
                    if export_render:
                        if select_model_objects_no_perm(halo_objects.default, model_armature, export_hidden):
                            print_box(f'**Exporting particle model**')
                            if using_better_fbx:
                                obj_selection = [obj for obj in context.selected_objects]
                                export_better_fbx(context, False, **keywords)
                                for obj in obj_selection:
                                    obj.select_set(True)
                            else:
                                export_fbx(self, context, **keywords)
                            export_gr2(report, asset_path, asset, 'particle_model', context.selected_objects, '', 'default', model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                            gr2_count += 1

            reports.append('Exported ' + str(gr2_count) + ' GR2 Files')
            if export_sidecar_xml:
                from .build_sidecar import export_sidecar
                export_sidecar(self, context, report, asset_path, halo_objects, model_armature, lod_count, regions_dict, global_materials_dict, **keywords)
                reports.append('Built ' + str.title(sidecar_type) + ' Sidecar')
            from .import_sidecar import import_sidecar
            if import_to_game:
                import_sidecar(self, context, report, **keywords)
                reports.append('Tag Export Processed')
            if lightmap_structure and not skip_lightmapper:
                from .run_lightmapper import run_lightmapper
                run_lightmapper(self, context, report, game_version in ('h4','h2a'), **keywords)
                if game_version not in ('h4','h2a'):
                    reports.append('Processed a Lightmap on ' + str.title(lightmap_quality) + ' Quality')
                else:
                    reports.append('Lightmapping complete')
            # if import_bitmaps:
            #     print("Temporary implementation, remove this later!")
            #     #import_bitmap.save(self, context, report, **keywords)

        else:
            report({'ERROR'},"No sidecar output tags selected")

    else:
        if get_ek_path() is None or get_ek_path() == '':
            ctypes.windll.user32.MessageBoxW(0, f"Invalid {self.game_version.upper()} Editing Kit path. Please check the {self.game_version.upper()} editing kit path in add-on preferences [Edit > Preferences > Add-ons > Halo Asset Blender Development Toolset].", f"INVALID {self.game_version.upper()} EK PATH", 0)
        elif not exists(f'{get_tool_path()}.exe'):
            ctypes.windll.user32.MessageBoxW(0, f"{self.game_version.upper()} Tool not found. Could not find {self.game_version.upper()} tool or tool_fast in your editing kit. Are you exporting to the correct game's editing kit data folder?", f"INVALID {self.game_version.upper()} TOOL PATH", 0)
        else:
            ctypes.windll.user32.MessageBoxW(0, f"The selected export folder is invalid, please ensure you are exporting to a directory within your {self.game_version.upper()} data folder.", f"INVALID {self.game_version.upper()} EXPORT PATH", 0)
    
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
    deselect_all_objects()
    arm.select_set(True)

    return True


#####################################################################################
#####################################################################################
# EXTRA FUNCTIONS

def CheckPath(filePath):
    return filePath.startswith(os.path.join(get_ek_path(), 'data'))

#####################################################################################
#####################################################################################
# BETTER FBX INTEGRATION

def export_better_fbx(context, export_animation, filepath, use_armature_deform_only, mesh_smooth_type_better, use_mesh_modifiers, use_triangles, global_scale, **kwargs):
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