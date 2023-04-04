# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Crisp
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

import os
import bpy
import glob
from subprocess import Popen
from ...file_gr2.nwo_utils import (
    get_asset_info,
    get_data_path,
    get_ek_path,
    get_tags_path,
    not_bungie_game,
    nwo_asset_type,
    valid_nwo_asset,
)

def get_tag_if_exists(asset_path, asset_name, type, extra=''):
    tag = os.path.join(get_tags_path() + asset_path, f'{asset_name}.{type}')
    if os.path.exists(tag):
        return tag
    else:   
        return ''

def LaunchFoundation(settings, context):
    scene_gr2 = context.scene.gr2
    launch_args = []
    # set the launch args
    if settings.foundation_default == 'asset' and valid_nwo_asset(context):
        launch_args.append('/dontloadlastopenedwindows')
        asset_path, asset_name = get_asset_info(settings.sidecar_path)
        if nwo_asset_type() == 'MODEL':
            if settings.open_model:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'model'))
            if settings.open_render_model:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'render_model'))
            if settings.open_collision_model:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'collision_model'))
            if settings.open_physics_model:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'physics_model'))
            if settings.open_model_animation_graph and len(bpy.data.actions) > 0:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'model_animation_graph'))
            if settings.open_frame_event_list  and len(bpy.data.actions) > 0:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'frame_event_list'))

            if settings.open_biped and scene_gr2.output_biped:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'biped'))
            if settings.open_crate and scene_gr2.output_crate:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'crate'))
            if settings.open_creature and scene_gr2.output_creature:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'creature'))
            if settings.open_device_control and scene_gr2.output_device_control:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'device_control'))
            if settings.open_device_dispenser and scene_gr2.output_device_dispenser and not_bungie_game():
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'device_dispenser'))
            if settings.open_device_machine and scene_gr2.output_device_machine:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'device_machine'))
            if settings.open_device_terminal and scene_gr2.output_device_terminal:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'device_terminal'))
            if settings.open_effect_scenery and scene_gr2.output_effect_scenery:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'effect_scenery'))
            if settings.open_equipment and scene_gr2.output_equipment:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'equipment'))
            if settings.open_giant and scene_gr2.output_giant:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'giant'))
            if settings.open_scenery and scene_gr2.output_scenery:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'scenery'))
            if settings.open_vehicle and scene_gr2.output_vehicle:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'vehicle'))
            if settings.open_weapon and scene_gr2.output_weapon:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'weapon'))
        
        elif nwo_asset_type() == 'SCENARIO':
            if settings.open_scenario:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'scenario'))
            if settings.open_scenario_structure_bsp:
                if settings.bsp_name == '':
                    for file in glob.glob(os.path.join(get_tags_path() + asset_path, '*.scenario_structure_bsp')):
                        launch_args.append(file)
                else:
                    # get all bsps given by user and add asset name
                    bsps = settings.bsp_name.replace(' ', '')
                    bsps = bsps.split(',')
                    bsps = [asset_name + '_' + bsp for bsp in bsps]
                    bsps = tuple(bsps)
                    # added each to launch args
                    for file in glob.glob(os.path.join(get_tags_path() + asset_path, '*.scenario_structure_bsp')):
                        file = file.rpartition('.')[0]
                        if file.endswith(bsps):
                            launch_args.append(file + '.scenario_structure_bsp')

            if settings.open_scenario_lightmap_bsp_data:
                if settings.bsp_name == '':
                    for file in glob.glob(os.path.join(get_tags_path() + asset_path, '*.scenario_lightmap_bsp_data')):
                        launch_args.append(file)
                else:
                    # get all bsps given by user and add asset name
                    bsps = settings.bsp_name.replace(' ', '')
                    bsps = bsps.split(',')
                    bsps = [asset_name + '_' + bsp for bsp in bsps]
                    bsps = tuple(bsps)
                    # added each to launch args
                    for file in glob.glob(os.path.join(get_tags_path() + asset_path, '*.scenario_lightmap_bsp_data')):
                        file = file.rpartition('.')[0]
                        if file.endswith(bsps):
                            launch_args.append(file + '.scenario_lightmap_bsp_data')
            if settings.open_scenario_structure_lighting_info:
                if settings.bsp_name == '':
                    for file in glob.glob(os.path.join(get_tags_path() + asset_path, '*.scenario_structure_lighting_info')):
                        launch_args.append(file)
                else:
                    # get all bsps given by user and add asset name
                    bsps = settings.bsp_name.replace(' ', '')
                    bsps = bsps.split(',')
                    bsps = [asset_name + '_' + bsp for bsp in bsps]
                    bsps = tuple(bsps)
                    # added each to launch args
                    for file in glob.glob(os.path.join(get_tags_path() + asset_path, '*.scenario_structure_lighting_info')):
                        file = file.rpartition('.')[0]

                        if file.endswith(bsps):
                            launch_args.append(file + '.scenario_structure_lighting_info')

        elif nwo_asset_type() == 'SKY':
            if settings.open_model:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'model'))
            if settings.open_render_model:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'render_model'))
            if settings.open_scenery:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'scenery'))

        elif nwo_asset_type() == 'DECORATOR SET':
            if settings.open_decorator_set:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'decorator_set'))

        elif nwo_asset_type() == 'PARTICLE MODEL':
            if settings.open_particle_model:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'particle_model'))

        elif nwo_asset_type() == 'PREFAB':
            if settings.open_prefab:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'prefab'))
            if settings.open_scenario_structure_bsp:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'scenario_structure_bsp'))
            if settings.open_scenario_structure_lighting_info:
                launch_args.append(get_tag_if_exists(asset_path, asset_name, 'scenario_structure_lighting_info'))

    os.chdir(get_ek_path())
    command = f"""Foundation.exe {' '.join(f'"{arg}"' for arg in launch_args)}"""
    Popen(command)
    Popen('bin\\tools\\bonobo\\TagWatcher.exe')

    return {'FINISHED'}

def launch_game(is_sapien, settings, filepath):
    asset_path, asset_name = get_asset_info(settings.sidecar_path)
    using_filepath = filepath.endswith('.scenario')
    # get the program to launch
    if is_sapien:
        args = ['sapien.exe']
        # Sapien needs the scenario in the launch args so adding this here
        if nwo_asset_type() == 'SCENARIO' and settings.game_default == 'asset':
            args.append(get_tag_if_exists(asset_path, asset_name, 'scenario'))
        elif using_filepath:
            args.append(filepath)
    else:
        game_version = bpy.context.scene.halo.game_version
        if game_version == 'h4':
            args = ['halo4_tag_test.exe']
        elif game_version == 'h2a':
            args = ['halo2a_tag_test.exe']
        else:
            args = ['reach_tag_test.exe']

    os.chdir(get_ek_path())
    # Write the init file
    init = ''
    if is_sapien:
        if os.path.exists('editor_init.txt'):
            try:
                if os.path.exists('editor_init_old.txt'):
                    os.remove('editor_init_old.txt')
                os.rename('editor_init.txt', 'editor_init_old.txt')
                init = 'editor_init.txt'
            except:
                print("Unable to replace editor_init.txt. It is currently read only")
        else:
            init = 'editor_init.txt'
    else:
        if os.path.exists('bonobo_init.txt'):
            try:
                if os.path.exists('bonobo_init_old.txt'):
                    os.remove('bonobo_init_old.txt')
                os.rename('bonobo_init.txt', 'bonobo_init_old.txt')
                init = 'bonobo_init.txt'
            except:
                print("Unable to replace bonobo_init.txt. It is currently read only")
        else:
            init = 'bonobo_init.txt'

    if init != '':
        h4_plus = not_bungie_game()       
        with open(init, 'w') as file:
            if settings.prune_globals:
                if h4_plus:
                    file.write('prune_globals 1\n')
                else:
                    file.write('prune_global 1\n')

            if settings.prune_globals_keep_playable:
                if h4_plus:
                    file.write('prune_globals_keep_playable 1\n')
                else:
                    file.write('prune_global_keep_playable 1\n')
            if settings.prune_scenario_for_environment_editing:
                file.write('prune_scenario_for_environment_editing 1\n')
                if settings.prune_scenario_for_environment_editing:
                    if settings.prune_scenario_for_environment_editing_keep_cinematics:
                        file.write('prune_scenario_for_environment_editing_keep_cinematics 1\n')
                    if settings.prune_scenario_for_environment_editing_keep_scenery:
                        file.write('prune_scenario_for_environment_editing_keep_scenery 1\n')
                    if settings.prune_scenario_for_environment_editing_keep_decals:
                        file.write('prune_scenario_for_environment_editing_keep_decals 1\n')
                    if settings.prune_scenario_for_environment_editing_keep_crates:
                        file.write('prune_scenario_for_environment_editing_keep_crates 1\n')
                    if settings.prune_scenario_for_environment_editing_keep_creatures:
                        file.write('prune_scenario_for_environment_editing_keep_creatures 1\n')
                    if settings.prune_scenario_for_environment_editing_keep_pathfinding:
                        if h4_plus:
                            file.write('prune_scenario_for_environment_editing_keep_pathfinding 1\n')
                        else:
                            file.write('prune_scenario_for_environment_pathfinding 1\n')
                            
                    if settings.prune_scenario_for_environment_editing_keep_new_decorator_block:
                        file.write('prune_scenario_for_environmnet_editing_keep_new_decorator_block 1\n')
            if settings.prune_scenario_all_lightmaps:
                if h4_plus:
                    file.write('prune_scenario_all_lightmaps 1\n')
                else:
                    file.write('prune_scenario_lightmaps 1\n')
                    
            if settings.prune_all_materials_use_gray_shader:
                if h4_plus:
                    file.write('prune_all_materials_use_gray_shader 1\n')
                else:
                    file.write('prune_scenario_use_gray_shader 1\n')
            if settings.prune_all_material_effects:
                if h4_plus:
                    file.write('prune_all_material_effects 1\n')
                else:
                    file.write('prune_global_material_effects 1\n')

            if settings.prune_all_dialog_sounds:
                if h4_plus:
                    file.write('prune_all_dialog_sounds 1\n')
                else:
                    file.write('prune_global_dialog_sounds 1\n')
                    
            if settings.prune_all_error_geometry:
                if h4_plus:
                    file.write('prune_all_error_geometry 1\n')
                else:
                    file.write('prune_error_geometry 1\n')
            # H4+ only
            if h4_plus:
                if settings.prune_globals_use_empty:
                    file.write('prune_globals_use_empty 1\n')
                if settings.prune_models_enable_alternate_render_models:
                    file.write('prune_models_enable_alternate_render_models 1\n')
                if settings.prune_scenario_keep_scriptable_objects:
                    file.write('prune_scenario_keep_scriptable_objects 1\n')
                if settings.prune_all_materials_use_default_textures:
                    file.write('prune_all_materials_use_default_textures 1\n')
                if settings.prune_all_materials_use_default_textures_fx_textures:
                    file.write('prune_all_materials_use_default_textures_keep_fx_textures 1\n')
                if settings.prune_facial_animations:
                    file.write('prune_facial_animations 1\n')
                if settings.prune_first_person_animations:
                    file.write('prune_first_person_animations 1\n')
                if settings.prune_low_quality_animations:
                    file.write('prune_low_quality_animations 1\n')
                if settings.prune_use_imposters:
                    file.write('prune_use_imposters 1\n')
                if settings.prune_cinematic_effects:
                    file.write('prune_cinematic_effects 1\n')
            # Reach Only
            else:
                if settings.prune_scenario_force_solo_mode:
                    file.write('prune_scenario_force_solo_mode 1\n')
                if settings.prune_scenario_for_environment_editing:
                    if settings.prune_scenario_for_environment_finishing:
                        file.write('prune_scenario_for_environment_finishing 1\n')
                if settings.prune_scenario_force_single_bsp_zone_set:
                    file.write('prune_scenario_force_single_bsp_zone_set 1\n')
                if settings.prune_scenario_force_single_bsp_zones:
                    file.write('prune_scenario_add_single_bsp_zones 1\n')
                if settings.prune_keep_scripts:
                    file.write('pruning_keep_scripts 1\n')

            file.write(f'run_game_scripts {"1" if settings.run_game_scripts else "0"}\n')

            if not is_sapien:
                if using_filepath:
                    file.write(f'game_start "{filepath.replace(get_tags_path(), "").rpartition(".")[0]}"\n')
                else:
                    file.write(f'game_start "{get_tag_if_exists(asset_path, asset_name, "scenario").replace(get_tags_path(), "").rpartition(".")[0]}"\n')

            if settings.initial_zone_set != '':
                file.write(f'game_initial_zone_set {settings.initial_zone_set}\n')
            elif settings.initial_bsp != '' and h4_plus:
                file.write(f'game_initial_BSP {settings.initial_bsp}\n')

            if settings.insertion_point_index > -1: 
                file.write(f'game_insertion_point_set {settings.insertion_point_index}\n')

            if settings.enable_firefight and h4_plus:
                file.write(f'game_firefight {settings.enable_firefight}\n')
                if settings.firefight_mission == '':
                    file.write(f'game_set_variant "midnight_firefight_firefight"\n')
                else:
                    file.write(f'game_set_variant "{settings.firefight_mission}"\n')

            if settings.custom_functions != '':
                try:
                    for line in bpy.data.texts[settings.custom_functions].lines:
                        file.write(f'{line.body}\n')
                except:
                    if os.path.exists(f'{settings.custom_functions}.txt'):
                        with open(f'{settings.custom_functions}.txt', 'r') as custom_init:
                            new_lines = custom_init.readlines()

                        for line in new_lines:
                            file.write(f'{line}\n')
                    else:
                        file.write(f'{settings.custom_functions}\n')


    Popen(' '.join(f'"{arg}"' for arg in args))

    return {'FINISHED'}

def open_file_explorer(sidecar_path, using_asset, is_tags):
    os.chdir(get_ek_path())
    if using_asset:
        source_folder = sidecar_path.rpartition(os.sep)[0]
        if is_tags:
            source_folder = get_tags_path() + source_folder
        else:
            source_folder = get_data_path() + source_folder

        os.startfile(source_folder)

    else:
        if is_tags:
            os.startfile('tags')
        else:
            os.startfile('data')

    return {'FINISHED'}
