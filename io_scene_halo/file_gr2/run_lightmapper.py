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
import ctypes
import platform
from io_scene_halo.gr2_utils import GetEKPath

def lightmapper(report, filepath, lightmap_quality='DIRECT', lightmap_all_bsps='TRUE', lightmap_specific_bsp='0'):
    full_path = filepath.rpartition('\\')[0]
    asset_path = CleanAssetPath(full_path)
    asset_name = asset_path.rpartition('\\')[2]
    bsp = GetBSPToLightmap(lightmap_all_bsps, lightmap_specific_bsp, asset_name)
    quality = GetQuality(lightmap_quality)
    high_quality_settings = ('medium', 'high', 'super_slow')

    pyCheck = platform.python_version().split('.')
    if int(pyCheck[0]) >= 3 or not platform.python_version() == None:
        try:
            lightmapCommand = 'python calc_lm_farm_local.py "{}" "{}" {}'.format(asset_path + '\\' + asset_name, bsp, quality)
            os.chdir(GetEKPath())
            p = Popen(lightmapCommand)
            p.wait()
            report({'INFO'},"Lightmapping process complete")

        except:
            report({'WARNING'},"Lightmapping process failed")
    else:
        ctypes.windll.user32.MessageBoxW(0, 'Python could not be found on this PC! Make sure it is installed in order to continue lightmapping', 'Python Not Found', 0)
        report({'WARNING'},"Lightmapping process failed")

def GetBSPToLightmap(lightmap_all_bsps, lightmap_specific_bsp, asset_name):
    bsp = 'all'
    if not lightmap_all_bsps:
        bsp = asset_name + '_' + "{0:03}".format(bsp)

    return bsp

def CleanAssetPath(path):
    path = path.replace('"','')
    path = path.strip('\\')
    path = path.replace(GetEKPath() + '\\data\\','')

    return path

def GetQuality(lightmap_quality):
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


def run_lightmapper(operator, context, report,
        filepath="",
        lightmap_quality='DIRECT',
        lightmap_all_bsps='TRUE',
        lightmap_specific_bsp='0',
        asset_path='',
        **kwargs
        ):
        lightmapper(report, filepath, lightmap_quality, lightmap_all_bsps, lightmap_specific_bsp)

        return {'FINISHED'}

# from subprocess import Popen
# import os
# import ctypes
# import platform
# from io_scene_halo.gr2_utils import GetEKPath
# import sys

# def lightmapper(report, filepath, lightmap_quality='DIRECT', lightmap_all_bsps='TRUE', lightmap_specific_bsp='0'):
#     full_path = filepath.rpartition('\\')[0]
#     asset_path = CleanAssetPath(full_path)
#     asset_name = asset_path.rpartition('\\')[2]
#     bsp = GetBSPToLightmap(lightmap_all_bsps, lightmap_specific_bsp, asset_name)
#     quality = GetQuality(lightmap_quality)
#     high_quality_settings = ('medium', 'high', 'super_slow')

#     try:
#         sys.path.insert(1, GetEKPath())
#         sys.argv = ['calc_lm_farm_local.py', os.path.join(asset_path, asset_name), bsp, quality]
#         print(sys.argv)
#         import calc_lm_farm_local
#         # lightmapCommand = 'python calc_lm_farm_local.py "{}" "{}" {}'.format(asset_path + '\\' + asset_name, bsp, quality)
#         # os.chdir(GetEKPath())
#         # p = Popen(lightmapCommand)
#         # p.wait()
#         # report({'INFO'},"Lightmapping process complete")

#     except:
#         report({'WARNING'},"Lightmapping process failed")