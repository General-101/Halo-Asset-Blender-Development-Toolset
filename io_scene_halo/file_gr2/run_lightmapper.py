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

    pyCheck = platform.python_version().split('.')
    if int(pyCheck[0]) >= 3 or not platform.python_version() == None:
        try:
            response = ctypes.windll.user32.MessageBoxW(0, 'Lightmapping can take a long time & cause Blender to be unresponsive during the process. Do you want to continue?', 'WARNING', 4)
            if response == 6:
                lightmapCommand = 'python calc_lm_farm_local.py "{}" "{}" {}'.format(asset_path + '\\' + asset_name, bsp, quality)
                os.chdir(GetEKPath())
                p = Popen(lightmapCommand)
                p.wait()
                report({'INFO'},"Lightmapping process complete")

        except:
            report({'WARNING'},"Lightmapping process failed")
    else:
        ctypes.windll.user32.MessageBoxW(0, 'Python could not be found on this PC! Make sure it is installed in order to continue lightmapping!', 'Python Not Found', 0)
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