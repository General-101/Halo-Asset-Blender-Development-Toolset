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
from addon_utils import module_bl_info
from os.path import exists
import os
import ctypes
from subprocess import Popen
from addon_utils import modules
import random
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
    CheckType,
    get_data_path,
)

#####################################################################################
#####################################################################################
# MAIN FUNCTION

def process_scene(self, context, keywords, report, model_armature, asset_path, asset, skeleton_bones, halo_objects, timeline_start, timeline_end, lod_count, using_better_fbx, selected_perms, selected_bsps, regions_dict, global_materials_dict, current_action,
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

    from .export_gr2 import export_gr2

    reports = []
    gr2_count = 0

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

            if sidecar_type in ('MODEL', 'FP ANIMATION'): # Added FP animation to this. FP animation only exports the skeleton and animations
                if sidecar_type == 'MODEL':

                    if export_render:
                        perm_list = []
                        for ob in get_render_from_halo_objects(halo_objects):
                            perm = get_perm(ob)
                            if perm not in perm_list:
                                perm_list.append(perm)
                                if select_model_objects(get_render_from_halo_objects(halo_objects), perm, model_armature, export_hidden, export_all_perms, selected_perms):
                                    print_box(f'**Exporting {perm} render model**')
                                    export_fbx(using_better_fbx, **keywords)
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
                                    export_fbx(using_better_fbx, **keywords)
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
                                    export_fbx(using_better_fbx, **keywords)
                                    export_gr2(report, asset_path, asset, 'physics', context.selected_objects, '', perm, model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                                    gr2_count += 1

                    if export_markers:
                        if select_model_objects_no_perm(halo_objects.markers, model_armature, export_hidden):
                            print_box('**Exporting markers**')
                            export_fbx(using_better_fbx, **keywords)
                            export_gr2(report, asset_path, asset, 'markers', context.selected_objects, '', '', model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                            gr2_count += 1

                if SelectModelSkeleton(model_armature):
                    print_box('**Exporting skeleton**')
                    export_fbx(using_better_fbx, **keywords)
                    export_gr2(report, asset_path, asset, 'skeleton', [model_armature], '', '', model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                    gr2_count += 1

                if export_animations != 'NONE' and 1<=len(bpy.data.actions):
                    if SelectModelSkeleton(model_armature):
                        timeline = context.scene
                        for action in bpy.data.actions:
                            try:
                                if export_animations == 'ALL' or current_action == action:
                                    animation_name = action.nwo.name_override
                                    print_box(f'**Exporting Animation: {animation_name}**')
                                    model_armature.animation_data.action = action
                                    if action.use_frame_range:
                                        timeline.frame_start = int(action.frame_start)
                                        timeline.frame_end = int(action.frame_end)
                                        context.scene.frame_set(int(action.frame_start))
                                    else:
                                        timeline.frame_start = timeline_start
                                        timeline.frame_end = timeline_end
                                        context.scene.frame_set(timeline_start)
                                    event_nodes = create_event_nodes(context, action.nwo.animation_events, timeline.frame_start, timeline.frame_end) # create objects which store animation event information
                                    if event_nodes is not None:
                                        for ob in event_nodes:
                                            ob.select_set(True)
                                    model_armature.select_set(True)
                                    export_fbx(using_better_fbx, **keywords)
                                    export_gr2(report, asset_path, asset, 'animations', context.selected_objects, '', '', model_armature, skeleton_bones, animation_name, regions_dict, global_materials_dict, **keywords)
                                    # delete the left over event nodes
                                    if event_nodes is not None:
                                        deselect_all_objects()
                                        for ob in event_nodes:
                                            ob.select_set(True)
                                        bpy.ops.object.delete()
                                    del event_nodes

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
                        for ob in get_structure_from_halo_objects(halo_objects, False):
                            if not is_shared(ob):
                                perm = get_perm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    if select_bsp_objects(get_structure_from_halo_objects(halo_objects, True), bsp, model_armature, perm, export_hidden, export_all_perms, selected_perms, export_all_bsps, selected_bsps):
                                        if perm != 'default':
                                            print_box(f'**Exporting {bsp} {perm} BSP**')
                                        else:
                                            print_box(f'**Exporting {bsp} BSP**')
                                        export_fbx(using_better_fbx, **keywords)
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
                        for ob in get_design_from_halo_objects(halo_objects, False):
                            perm = get_perm(ob)
                            if perm not in perm_list:
                                perm_list.append(perm)
                                if select_bsp_objects(get_design_from_halo_objects(halo_objects, True), bsp, model_armature, perm, export_hidden, export_all_perms, selected_perms, export_all_bsps, selected_bsps):
                                    if perm != 'default':
                                        print_box(f'**Exporting {bsp} {perm} Design**')
                                    else:
                                        print_box(f'**Exporting {bsp} Design**')
                                    export_fbx(using_better_fbx, **keywords)
                                    export_gr2(report, asset_path, asset, 'design', context.selected_objects, bsp, perm, model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                                    gr2_count += 1



            ############################
            ##### SHARED STRUCTURE #####
            ############################

                if shared_bsp_exists:
                    if export_structure:
                        perm_list = []
                        for ob in get_structure_from_halo_objects(halo_objects, False):
                            if is_shared(ob):
                                perm = get_perm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    if select_bsp_objects(get_structure_from_halo_objects(halo_objects, True), 'shared', model_armature, perm, export_hidden, export_all_perms, selected_perms, export_all_bsps, selected_bsps):
                                        if perm != 'default':
                                            print_box(f'**Exporting shared {perm} BSP**')
                                        else:
                                            print_box(f'**Exporting shared BSP**')
                                        export_fbx(using_better_fbx, **keywords)
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
                                export_fbx(using_better_fbx, **keywords)
                                export_gr2(report, asset_path, asset, 'render', context.selected_objects, '', perm, model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                                gr2_count += 1

            elif sidecar_type == 'DECORATOR SET': 
                if export_render:
                    if select_model_objects_no_perm(halo_objects.decorators, model_armature, export_hidden):
                        print_box(f'**Exporting decorator set**')
                        export_fbx(using_better_fbx, **keywords)
                        export_gr2(report, asset_path, asset, 'render', context.selected_objects, '', 'default', model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                        gr2_count += 1

            elif sidecar_type == 'PREFAB':
                if select_prefab_objects(get_prefab_from_halo_objects(halo_objects), model_armature, export_hidden):
                    print_box(f'**Exporting prefab**')
                    export_fbx(using_better_fbx, **keywords)
                    export_gr2(report, asset_path, asset, 'prefab', context.selected_objects, '', '', model_armature, skeleton_bones, '', regions_dict, global_materials_dict, **keywords)
                    gr2_count += 1

            else: # for particles
                if export_render:
                    if select_model_objects_no_perm(halo_objects.default, model_armature, export_hidden):
                        print_box(f'**Exporting particle model**')
                        export_fbx(using_better_fbx, **keywords)
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
        if lightmap_structure:
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
# ANIMATION EVENTS

def create_event_nodes(context, events, frame_start, frame_end):
    if len(events) < 1:
        return None
    event_nodes = []
    for event in events:
        # create the event node to store event info
        deselect_all_objects()
        bpy.ops.object.empty_add()
        event_node = context.active_object.nwo
        event_ob = context.active_object
        # Set this node to be an animation event
        event_node.is_animation_event = True
        # Set up the event node with the action start and end frame and id
        event_node.frame_start = frame_start + .4999
        event_node.frame_end = frame_end + .4999
        # add the user defined properties from the action
        event_node.event_id = event.event_id
        event_node.event_type = event.event_type
        event_node.wrinkle_map_face_region = event.wrinkle_map_face_region
        event_node.wrinkle_map_effect = event.wrinkle_map_effect
        event_node.footstep_type = event.footstep_type
        event_node.footstep_effect = event.footstep_effect
        event_node.ik_chain = event.ik_chain
        event_node.ik_active_tag = event.ik_active_tag
        event_node.ik_target_tag = event.ik_target_tag
        event_node.ik_target_marker = event.ik_target_marker
        event_node.ik_target_usage = event.ik_target_usage
        event_node.ik_proxy_target_id = event.ik_proxy_target_id
        event_node.ik_pole_vector_id = event.ik_pole_vector_id
        event_node.ik_effector_id = event.ik_effector_id
        event_node.cinematic_effect_tag = event.cinematic_effect_tag
        event_node.cinematic_effect_effect = event.cinematic_effect_effect
        event_node.cinematic_effect_marker = event.cinematic_effect_marker
        event_node.object_function_name = event.object_function_name
        event_node.object_function_effect = event.object_function_effect
        event_node.frame_frame = event.frame_frame
        event_node.frame_name = event.frame_name
        event_node.frame_trigger = event.frame_trigger
        event_node.import_frame = event.import_frame
        event_node.import_name = event.import_name
        event_node.text = event.text
        # set event node name
        event_ob.name = f'event_node_{str(event_node.event_id)}'
        # add it to the list
        event_nodes.append(event_ob)
        # duplicate for frame range
        if event.multi_frame == 'range' and event.frame_range > 1:
            for i in range(min(event.frame_range - 1, frame_end - event.frame_frame)):
                bpy.ops.object.duplicate()
                event_node_new = context.active_object.nwo
                event_node_ob = context.active_object
                event_node_new.event_id += 1
                event_node_new.frame_frame += 1
                event_node_ob.name = f'event_node_{str(event_node_new.event_id)}'
                event_nodes.append(event_node_ob)
                deselect_all_objects()
                event_node_ob.select_set(True)

    return event_nodes


#####################################################################################
#####################################################################################
# FBX

def export_fbx(using_better_fbx, filepath, global_scale, use_mesh_modifiers, mesh_smooth_type, use_triangles, use_armature_deform_only, mesh_smooth_type_better, **kwargs): # using_better_fbx
    if using_better_fbx:
        bpy.ops.better_export.fbx(filepath=filepath, check_existing=False, my_fbx_unit='m', use_selection=True, use_visible=True, use_only_deform_bones=use_armature_deform_only, use_apply_modifiers=use_mesh_modifiers, use_triangulate=use_triangles, my_scale=global_scale, use_optimize_for_game_engine=False, use_ignore_armature_node=False, my_edge_smoothing=mesh_smooth_type_better, my_material_style='Blender')
    else:
        bpy.ops.export_scene.fbx(filepath=filepath, check_existing=False, use_selection=True, use_visible=True, global_scale=global_scale, apply_scale_options='FBX_SCALE_UNITS', use_mesh_modifiers=use_mesh_modifiers, mesh_smooth_type=mesh_smooth_type, use_triangles=use_triangles, add_leaf_bones=False, use_armature_deform_only=use_armature_deform_only, bake_anim_use_all_bones=False, bake_anim_use_nla_strips=False, bake_anim_use_all_actions=False, bake_anim_force_startend_keying=False, bake_anim_simplify_factor=0, axis_forward='X', axis_up='Z')