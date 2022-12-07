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

from subprocess import Popen
import os
from io_scene_halo.gr2_utils import GetEKPath

def lightmapper(report, filepath, not_bungie_game, lightmap_quality='DIRECT', lightmap_all_bsps='TRUE', lightmap_specific_bsp='000', lightmap_quality_h4='farm_draft_quality'):
    full_path = filepath.rpartition('\\')[0]
    asset_path = CleanAssetPath(full_path)
    asset_name = asset_path.rpartition('\\')[2]
    bsp = GetBSPToLightmap(lightmap_all_bsps, lightmap_specific_bsp, asset_name)
    quality = GetQuality(lightmap_quality, lightmap_quality_h4, not_bungie_game)

    try:
        lightmapCommand = f'python calc_lm_farm_local.py {os.path.join(asset_path, asset_name)} {bsp} {quality}'
        os.chdir(GetEKPath())
        print(lightmapCommand)
        p = Popen(lightmapCommand)
        p.wait()
        report({'INFO'},"Lightmapping process complete")

    except:
        report({'WARNING'},"Lightmapping process failed. You may need to add python to your PATH")

def GetBSPToLightmap(lightmap_all_bsps, lightmap_specific_bsp, asset_name):
    bsp = 'all'
    if not lightmap_all_bsps:
        bsp = f'{asset_name}_{lightmap_specific_bsp}'

    return bsp

def CleanAssetPath(path):
    path = path.replace('"','')
    path = path.strip('\\')
    path = path.replace(GetEKPath() + '\\data\\','')

    return path

def GetQuality(lightmap_quality, lightmap_quality_h4, not_bungie_game):
    if not_bungie_game:
        return lightmap_quality_h4
    match lightmap_quality:
        case 'DIRECT':
            return 'direct_only'
        case 'DRAFT':
            return 'draft'
        case 'LOW':
            return 'low'
        case 'MEDIUM':
            return 'medium'
        case 'HIGH':
            return 'high'
        case _:
            return 'super_slow'


def run_lightmapper(operator, context, report, not_bungie_game,
        filepath="",
        lightmap_quality='DIRECT',
        lightmap_all_bsps='TRUE',
        lightmap_specific_bsp='0',
        asset_path='',
        **kwargs
        ):
        lightmapper(report, filepath, not_bungie_game, lightmap_quality, lightmap_all_bsps, lightmap_specific_bsp)

        return {'FINISHED'}