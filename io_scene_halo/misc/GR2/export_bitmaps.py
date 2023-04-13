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
from io_scene_halo.file_gr2.nwo_utils import dot_partition, get_asset_info, get_data_path, run_tool

def save_image_as(image, path, name):
    scene = bpy.data.scenes.new("temp") 

    settings = scene.render.image_settings
    settings.file_format = 'TIFF'
    settings.color_mode = 'RGBA'
    settings.color_depth = '16' 
    settings.tiff_codec = 'NONE'
    
    name_tiff = dot_partition(name) + '.tiff'
    path = os.path.join(path, name_tiff)
    image.save_render(filepath=path, scene=scene)
    bpy.data.scenes.remove(scene)

def export_bitmaps(report, context, material, sidecar_path, overwrite, export_type, bitmaps_selection):
    if context.scene.gr2_export.show_output:
        bpy.ops.wm.console_toggle() # toggle the console so users can see progress of export

    context.scene.gr2_export.show_output = False

    asset_path, asset = get_asset_info(sidecar_path)
    # Create a bitmap folder in the asset directory
    bitmaps_data_dir = os.path.join(get_data_path() + asset_path, 'bitmaps')
    if not os.path.exists(bitmaps_data_dir):
        os.mkdir(bitmaps_data_dir)
        # get a list of textures associated with this material
    textures = []
    bitmap_count = 0
    if bitmaps_selection == 'active':
        for node in material.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                if node.image not in textures:
                    textures.append(node.image)
    else:
        for image in bpy.data.images:
            if image.name != 'Render Result':
                textures.append(image)
    # export each texture as a tiff to the asset bitmaps folder
    bitmap_paths = []
    texture_names = []
    for image in textures:
        # avoid textures with duplicate names being exported
        if image.name not in texture_names:
            texture_names.append(image.name)
            try:
                tiff_name = dot_partition(image.name) + '.tiff'

                if export_type != 'import':
                    if overwrite or not os.path.exists(os.path.join(bitmaps_data_dir, tiff_name)):
                        save_image_as(image, bitmaps_data_dir, image.name)
                        print(f"Exported {image.name} as tiff")

                    bitmap_count +=1

                bitmap_paths.append(os.path.join(asset_path, 'bitmaps', tiff_name))

            except:
                print(f"Failed to export {image.name}")

        else:
            print('\033[93m' + f'{image.name} is a duplicate name, please make it unique. Export skipped' + '\033[0m')


    if bitmap_count == 0:
        report({'WARNING'}, 'No Bitmaps exported')
    else:
        report({'INFO'}, f'Exported {bitmap_count} bitmaps')

    if export_type != 'export':
        for path in bitmap_paths:
            run_tool(['bitmap_single', path])

        report({'INFO'}, 'Bitmaps Import Complete')


    return {'FINISHED'}

