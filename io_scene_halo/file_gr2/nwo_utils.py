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
import platform
from math import radians
from mathutils import Matrix
import os
from os.path import exists as file_exists
from subprocess import Popen
import shutil

###########
##GLOBALS##
###########

# Main Prefixes #
frame_prefixes = ('b ', 'b_', 'frame ', 'frame_','bip ','bip_','bone ','bone_')
marker_prefixes = ('#', '?')
mesh_prefixes = ('+soft_ceiling','+soft_kill','+slip_surface', '@','+cookie','+decorator','+flair', '%', '$','+fog','+portal', '+seam','+water', '\'')
special_prefixes = ('b ', 'b_', 'frame ', 'frame_','bip ','bip_','bone ','bone_','#', '?','+soft_ceiling','+soft_kill','+slip_surface', '@','+cookie','+decorator','+flair', '%', '$','+fog','+portal', '+seam','+water', '\'')


# Specific Mesh Prefixes #
boundary_surface_prefixes = ('+soft_ceiling','+soft_kill','+slip_surface') # boundary surface prefixes can take a name with +prefix:name e.g. +soft_ceiling:camera_ceiling_01
cookie_cutter_prefixes = ('+cookie')
decorator_prefixes = ('+decorator') # decorators can take a name with +decorator:name (not implemented)
fog_volume_prefixes = ('+fog') # fog volumes can take a name with +fog:name (not implemented)
object_instance_prefixes = ('+flair') # self-reminder: Flairs need to have marker_regions written to them in the json, this should match the face region
portal_prefixes = ('+portal') # portals can have properties automatically through the object name (once I get around to adding it)
seam_prefixes = ('+seam') # seams can take a name with +seam:name
water_volume_prefixes = ('+water')

no_perm_prefixes = ((frame_prefixes, marker_prefixes, boundary_surface_prefixes, decorator_prefixes, fog_volume_prefixes, portal_prefixes, seam_prefixes, water_volume_prefixes, cookie_cutter_prefixes, '+water', '\''))
# Instanced Geo Prefixes #
poop_lighting_prefixes = ('%!',     '%-!','%+!','%*!',     '%-*!','%+*!',     '%*-!','%*+!',          '%?',     '%-?','%+?','%*?',     '%-*?','%+*?',     '%*-?','%*+?'          '%>',     '%->','%+>','%*>',     '%-*>','%+*>',     '%*->','%*+>')
poop_pathfinding_prefixes = ('%+',     '%!+','%?+','%>+','%*+',     '%!*+','%?*+','%>*+',     '%*!+','%*?+','%*>+',          '%-',     '%!-','%?-','%>-','%*-',     '%!*-','%?*-','%>*-',     '%*!-','%*?-','%*>-')
poop_render_only_prefixes = ('%*',     '%!*','%?*','%>*','%-*','%+*',     '%!-*','%!+*','%?-*','%?+*','%>-*','%>+*')

all_prefixes = ('+slip_surface', '+soft_ceiling', '+soft_kill', '+decorator', '+portal', '+cookie', 'frame ', '%*+?%>', '+water', 'frame_', '+flair', '+seam', 'bone_', 'bone ', '%>+*', '%>-*', '%?+*', '%?-*', '%!+*', '%!-*', 'bip_', '+fog', '%*+>', '%*->', '%+*>', '%-*>', '%*>-', '%*?-', '%*!-', '%>*-', '%?*-', '%!*-', '%*+!', '%*-!', '%+*!', '%*-?', '%+*?', '%*>+', '%*?+', '%*!+', '%>*+', '%?*+', '%!*+', '%-*?', '%-*!', 'bip ', '%+*', '%-*', '%>*', '%?*', '%!*', '%-!', '%*-', '%>-', '%?-', '%!-', '%*!', '%*+', '%>+', '%?+', '%!+', '%+!', '%*>', '%+>', '%->', '%*?', '%+?', '%-?', '%*', '%-', '%+', '%?', '%!', 'b_', 'b ', "'", '$', '%', '@', '?', '#')

# Material Prefixes #
special_materials = ('+collision', '+physics', '+portal', '+seamsealer','+sky', '+slip_surface', '+soft_ceiling', '+soft_kill', '+weatherpoly', '+override')
special_materials_h4 = ('+sky', '+physics', '+seam', '+portal', '+collision', '+player_collision', '+wall_collision', '+bullet_collision', '+cookie_cutter', '+rain_blocker', '+water_volume', '+structure')
# Enums #
special_mesh_types = ('_connected_geometry_mesh_type_boundary_surface', '_connected_geometry_mesh_type_collision','_connected_geometry_mesh_type_decorator','_connected_geometry_mesh_type_poop','_connected_geometry_mesh_type_planar_fog_volume','_connected_geometry_mesh_type_portal','_connected_geometry_mesh_type_seam','_connected_geometry_mesh_type_water_physics_volume', '_connected_geometry_mesh_type_obb_volume')
invalid_mesh_types = ('_connected_geometry_mesh_type_boundary_surface', '_connected_geometry_mesh_type_cookie_cutter', '_connected_geometry_mesh_type_poop_marker', '_connected_geometry_mesh_type_poop_rain_blocker', '_connected_geometry_mesh_type_poop_vertical_rain_sheet', '_connected_geometry_mesh_type_lightmap_region', '_connected_geometry_mesh_type_planar_fog_volume', '_connected_geometry_mesh_type_portal', '_connected_geometry_mesh_type_seam', '_connected_geometry_mesh_type_water_physics_volume', '_connected_geometry_mesh_type_obb_volume')
# animations #
valid_animation_types = ('JMM', 'JMA', 'JMT', 'JMZ', 'JMV', 'JMO', 'JMOX', 'JMR', 'JMRX')

# shader exts #
shader_exts = ('.shader', '.shader_cortana', '.shader_custom', '.shader_decal', '.shader_foliage', '.shader_fur', '.shader_fur_stencil', '.shader_glass', '.shader_halogram', '.shader_mux', '.shader_mux_material', '.shader_screen', '.shader_skin', '.shader_terrain', '.shader_water', '.material')

package = 'io_scene_halo'

#############
##FUNCTIONS##
#############

def get_ek_path():
    scene = bpy.context.scene
    scene_halo = scene.halo
    if scene_halo.game_version == 'h4':
        EKPath = bpy.context.preferences.addons[package].preferences.h4ek_path
    elif scene_halo.game_version == 'h2a':
        EKPath = bpy.context.preferences.addons[package].preferences.h2aek_path
    else:
        EKPath = bpy.context.preferences.addons[package].preferences.hrek_path

    EKPath = EKPath.replace('"','')
    EKPath = EKPath.strip('\\')

    return EKPath

def get_tool_path():
    toolPath = os.path.join(get_ek_path(), get_tool_type())

    return toolPath

def get_tags_path():
    EKPath = get_ek_path()
    tagsPath = os.path.join(EKPath, 'tags', '')

    return tagsPath

def get_data_path():
    EKPath = get_ek_path()
    dataPath = os.path.join(EKPath, 'data', '')

    return dataPath

def get_tool_type():
    return bpy.context.preferences.addons[package].preferences.tool_type

def get_perm(ob): # get the permutation of an object, return default if the perm is empty
    if ob.nwo.Permutation_Name_Locked != '':
        return ob.nwo.Permutation_Name_Locked
    else:
        return ob.nwo.Permutation_Name
        

def is_windows():
    return platform.system() == 'Windows'

def not_bungie_game():
    return bpy.context.scene.halo.game_version in ('h4', 'h2a')

def object_valid(ob, export_hidden, valid_perm='', evaluated_perm='', evalued_perm_locked = ''):
    if evalued_perm_locked != '':
        return ob in tuple(bpy.context.scene.view_layers[0].objects) and (ob.visible_get() or export_hidden) and valid_perm == evalued_perm_locked
    else:
        return ob in tuple(bpy.context.scene.view_layers[0].objects) and (ob.visible_get() or export_hidden) and valid_perm == evaluated_perm

def export_perm(perm, export_all_perms, selected_perms):
    return export_all_perms == 'all' or perm in selected_perms

def export_bsp(bsp, export_all_bsps, selected_bsps):
    return export_all_bsps == 'all' or bsp in selected_bsps

def get_prefix(string, prefix_list): # gets a prefix from a list of prefixes
    prefix = ''
    for p in prefix_list:
        if string.startswith(p):
            prefix = p
            break
    
    return prefix

def select_halo_objects(select_func, selected_asset_type, valid_asset_types):
    deselect_all_objects()
    select_func = getattr(CheckType, select_func)
    halo_objects = []
    if selected_asset_type in valid_asset_types:
        for ob in bpy.context.view_layer.objects:
            if select_func(ob):
                halo_objects.append(ob) 
    
    return halo_objects


def select_model_objects(halo_objects, perm, arm, export_hidden, export_all_perms, selected_perms):
    deselect_all_objects()
    boolean = False
    if arm is not None:
        arm.select_set(True)
    for ob in halo_objects:
        halo = ob.nwo
        if object_valid(ob, export_hidden, perm, halo.Permutation_Name, halo.Permutation_Name_Locked) and export_perm(perm, export_all_perms, selected_perms):
            ob.select_set(True)
            boolean = True
    
    return boolean

def select_model_objects_no_perm(halo_objects, arm, export_hidden):
    deselect_all_objects()
    boolean = False
    if arm is not None:
        arm.select_set(True)
    for ob in halo_objects:
        if object_valid(ob, export_hidden):
            ob.select_set(True)
            boolean = True

    return boolean

def select_bsp_objects(halo_objects, bsp, arm, perm, export_hidden, export_all_perms, selected_perms, export_all_bsps, selected_bsps):
    deselect_all_objects()
    boolean = False
    if arm is not None:
        arm.select_set(True)
    for ob in halo_objects:
        halo = ob.nwo
        bsp_value = true_bsp(ob.nwo)
        if bsp_value == bsp:
            if object_valid(ob, export_hidden, perm, halo.Permutation_Name, halo.Permutation_Name_Locked) and export_perm(perm, export_all_perms, selected_perms) and export_bsp(bsp, export_all_bsps, selected_bsps):
                ob.select_set(True)
                boolean = True

    return boolean

def get_shared_objects(halo_objects):
    new_objects = []
    for ob in halo_objects:
        if true_bsp(ob.nwo) == 'shared':
            new_objects.append(ob)

    return new_objects

def select_prefab_objects(halo_objects, arm, export_hidden):
    deselect_all_objects()
    boolean = False
    if arm is not None:
        arm.select_set(True)
    for ob in halo_objects:
        if ob in tuple(bpy.context.scene.view_layers[0].objects) and (ob.visible_get() or export_hidden):
            ob.select_set(True)
            boolean = True

    return boolean


def deselect_all_objects():
    bpy.ops.object.select_all(action='DESELECT')

def select_all_objects():
    bpy.ops.object.select_all(action='SELECT')

def set_active_object(ob):
    bpy.context.view_layer.objects.active = ob

def get_active_object():
    return bpy.context.view_layer.objects.active

def get_asset_info(filepath):
    asset_path = filepath.rpartition('\\')[0]
    asset = asset_path.rpartition('\\')[2]
    asset = asset.replace('.fbx', '')

    return asset_path, asset

# -------------------------------------------------------------------------------------------------------------------

def mesh_type(ob, types, valid_prefixes=()):
    if ob != None: # temp work around for 'ob' not being passed between functions correctly, and resolving to a NoneType
        if not_bungie_game():
            return is_mesh(ob) and ((ob.nwo.ObjectMesh_Type_H4 in types and not object_prefix(ob, special_prefixes)) or object_prefix(ob, valid_prefixes))
        else:
            return is_mesh(ob) and ((ob.nwo.ObjectMesh_Type in types and not object_prefix(ob, special_prefixes)) or object_prefix(ob, valid_prefixes))

def marker_type(ob, types, valid_prefixes=()):
    if ob != None: # temp work around for 'ob' not being passed between functions correctly, and resolving to a NoneType
            if not_bungie_game():
                return is_marker(ob) and ((ob.nwo.ObjectMarker_Type_H4 in types and not object_prefix(ob, ('?', '$'))) or object_prefix(ob, valid_prefixes))
            else:
                return is_marker(ob) and ((ob.nwo.ObjectMarker_Type in types and not object_prefix(ob, ('?', '$'))) or object_prefix(ob, valid_prefixes))

def object_type(ob, types=(), valid_prefixes=()):
    if ob != None: # temp work around for 'ob' not being passed between functions correctly, and resolving to a NoneType
        if ob.type == 'MESH':
            return (ob.nwo.Object_Type_All in types and not object_prefix(ob, ((frame_prefixes + marker_prefixes))) or object_prefix(ob, (valid_prefixes)))
        elif ob.type == 'EMPTY':
            return ob.nwo.Object_Type_No_Mesh in types or object_prefix(ob, (valid_prefixes)) or len(ob.children) > 0
        elif ob.type == 'LIGHT' and (types != 'MARKER' and '#' not in valid_prefixes):
            return True
        elif ob.nwo.Object_Type_All in types or object_prefix(ob, (valid_prefixes)):
            return True
        else:
            return False

def object_prefix(ob, prefixes):
    return ob.name.startswith(prefixes)

def not_parented_to_poop(ob):
    return (not mesh_type(ob.parent, '_connected_geometry_mesh_type_poop') or (object_prefix(ob.parent, special_prefixes) and not object_prefix(ob.parent, '%')))

def is_design(ob):
    return CheckType.fog(ob) or CheckType.boundary_surface(ob) or CheckType.water_physics(ob) or CheckType.poop_rain_blocker(ob)

def is_marker(ob):
    if ob.type == 'MESH':
        return ((ob.nwo.Object_Type_All == '_connected_geometry_object_type_marker' and not ob.name.startswith(frame_prefixes)) or ob.name.startswith(marker_prefixes)) or ob.nwo.Object_Type_All_Locked == '_connected_geometry_object_type_marker'
    elif ob.type == 'EMPTY':
        return ((ob.nwo.Object_Type_No_Mesh == '_connected_geometry_object_type_marker' and not ob.name.startswith(frame_prefixes)) or ob.name.startswith(marker_prefixes)) or ob.nwo.Object_Type_No_Mesh_Locked == '_connected_geometry_object_type_marker'
    else:
        return False

def is_frame(ob):
    if ob.type == 'MESH':
        return (ob.nwo.Object_Type_All == '_connected_geometry_object_type_frame' and not ob.name.startswith(marker_prefixes)) or ob.name.startswith(frame_prefixes) or ob.nwo.Object_Type_All_Locked == '_connected_geometry_object_type_frame'
    elif ob.type == 'EMPTY':
        return (ob.nwo.Object_Type_No_Mesh == '_connected_geometry_object_type_frame' and not ob.name.startswith(('#', '?', '$'))) or ob.name.startswith(frame_prefixes) or ob.nwo.Object_Type_No_Mesh_Locked == '_connected_geometry_object_type_frame'
    else:
        return False

def is_mesh(ob):
    return not is_marker(ob) and not is_frame(ob) and ob.type == 'MESH'

def vector_str(velocity):
    x = velocity.x
    y = velocity.y
    z = velocity.z
    return f'{jstr(x)} {jstr(y)} {jstr(z)}'

def color_3p_str(color):
    red = color.r
    green = color.g
    blue = color.b
    return f'{jstr(red)} {jstr(green)} {jstr(blue)}'

def color_4p_str(color):
    red = color.r
    green = color.g
    blue = color.b
    return f'1 {jstr(red)} {jstr(green)} {jstr(blue)}'

def bool_str(bool_var):
    """Returns a boolean as a string. 1 if true, 0 if false"""
    if bool_var:
        return '1'
    else:
        return '0'

def radius_str(ob, pill = False):
    """Returns the radius of a sphere (or a pill if second arg is True) as a string"""
    if pill:
        diameter = max(ob.dimensions.x, ob.dimensions.y)
    else:
        diameter = max(ob.dimensions)

    radius = diameter / 2.0

    return jstr(radius)

def jstr(number):
    """Takes a number, rounds it to six decimal places and returns it as a string"""
    return str(round(number, 6))

def true_bsp(halo):
    if halo.bsp_name_locked !='':
        return halo.bsp_name_locked
    else:
        return halo.bsp_name

def true_region(halo):
    if halo.Region_Name_Locked !='':
        return halo.Region_Name_Locked
    else:
        return halo.Region_Name

def clean_tag_path(path, file_ext = None):
    """Cleans a path and attempts to make it appropriate for reading by Tool. Can accept a file extension (without a period) to force the existing one if it exists to be replaced"""
    if path != '':
        path = path.lower()
        # If a file ext is provided, replace the existing one / add it
        if file_ext is not None:
            path = shortest_string(path, path.rpartition('.')[0])
            path = f'{path}.{file_ext}'
        # remove any quotation characters from path
        path = path.replace('\"\'', '')
        # strip bad characters from the start and end of the path
        path = path.strip('\\/.')
        # # remove 'tags' if path starts with this
        # if path.startswith('tags'):
        #     path = path.replace('tags', '')
        #     # strip following backslash
        #     path = path.strip('\\')
        # attempt to make path tag relative
        path = path.replace(get_tags_path().lower(), '')
        # return the new path in lower case
        return path
    else:
        return ''

def is_shared(ob):
    return true_bsp(ob.nwo) == 'shared'

def shortest_string(*strings):
    """Takes strings and returns the shortest non null string"""
    string_list = [*strings]
    temp_string = ''
    while temp_string == '' and len(string_list) > 0:
        temp_string = min(string_list, key=len)
        string_list.remove(temp_string)

    return temp_string

def print_box(text, line_char='-', char_count=100):
    """Prints the specified text surrounded by lines created with the specified character. Optionally define the number of charactrers to repeat per line"""
    side_char_count = (char_count - len(text) - 2) // 2
    side_char_count = max(side_char_count, 0)
    side_fix = 0
    if side_char_count > 1:
        side_fix = 1 if (char_count - len(text) - 2) // 2 != (char_count - len(text) - 2) / 2 else 0
    print(line_char * char_count)
    print(f'{line_char * side_char_count} {text} {line_char * (side_char_count + side_fix)}')
    print(line_char * char_count)

class CheckType:
    @staticmethod
    def get(ob):
        if CheckType.animation_control(ob):
            return '_connected_geometry_object_type_animation_control'
        elif CheckType.animation_event(ob):
            return '_connected_geometry_object_type_animation_event'
        elif CheckType.animation_camera(ob):
            return '_connected_geometry_object_type_animation_camera'
        elif CheckType.light(ob):
            return '_connected_geometry_object_type_light'
        elif CheckType.frame_pca(ob):
            return '_connected_geometry_object_type_frame_pca'
        elif CheckType.frame(ob):
            return '_connected_geometry_object_type_frame'
        elif CheckType.marker(ob):
            return '_connected_geometry_object_type_marker'
        else:
            return '_connected_geometry_object_type_mesh'
    @staticmethod
    def render(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_default'))
    @staticmethod
    def collision(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_collision'), ('@'))
    @staticmethod
    def physics(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_physics'), ('$'))
    @staticmethod
    def default(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_default'))
    @staticmethod
    def marker(ob):
        return object_type(ob, ('_connected_geometry_object_type_marker'), ('#', '?'))
    @staticmethod
    def structure(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_default'))
    @staticmethod
    def poop(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_poop'), ('%'))
    @staticmethod
    def poop_marker(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_poop_marker'))
    @staticmethod
    def object_instance(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_object_instance'), ('+flair'))
    @staticmethod
    def poop_collision_physics(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_collision', '_connected_geometry_mesh_type_physics'), ('@', '$'))
    @staticmethod
    def light(ob):
        return ob.type == 'LIGHT'
    @staticmethod
    def portal(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_portal'), ('+portal'))
    @staticmethod
    def seam(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_seam'), ('+seam'))
    @staticmethod
    def water_surface(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_water_surface'), ('\''))
    @staticmethod
    def misc(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_lightmap_region', '_connected_geometry_mesh_type_obb_volume'))
    @staticmethod
    def fog(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_planar_fog_volume'), ('+fog'))
    @staticmethod
    def boundary_surface(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_boundary_surface'), ('+soft_kill', '+soft_ceiling', '+slip_surface'))
    @staticmethod
    def water_physics(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_water_physics_volume'), ('+water'))
    @staticmethod
    def poop_rain_blocker(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_poop_rain_blocker', '_connected_geometry_mesh_type_poop_vertical_rain_sheet'))
    @staticmethod
    def frame(ob):
        return object_type(ob, ('_connected_geometry_object_type_frame'), (frame_prefixes)) and not ob.type == 'LIGHT'and not ob.type == 'ARMATURE' # ignores objects we know must be frames (like bones / armatures) as these are handled seperately
    @staticmethod
    def decorator(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_decorator'), (decorator_prefixes))
    @staticmethod
    def poop_collision(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_collision'), ('@'))
    @staticmethod
    def poop_physics(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_physics'), ('$'))
    @staticmethod
    def cookie_cutter(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_cookie_cutter'), ('+cookie'))
    @staticmethod
    def obb_volume(ob):
        return mesh_type(ob, ('_connected_geometry_mesh_type_obb_volume'))
    @staticmethod
    def mesh(ob):
        return ob.type == 'MESH' and ob.nwo.Object_Type_All in '_connected_geometry_object_type_mesh' and not object_prefix(ob, ((frame_prefixes + marker_prefixes)))
    @staticmethod
    def model(ob):
        return marker_type(ob, ('_connected_geometry_marker_type_model'))
    @staticmethod
    def effects(ob):
        return marker_type(ob, ('_connected_geometry_marker_type_effects'))
    @staticmethod
    def game_instance(ob):
        return marker_type(ob, ('_connected_geometry_marker_type_game_instance'), ('?'))
    @staticmethod
    def garbage(ob):
        return marker_type(ob, ('_connected_geometry_marker_type_garbage'))
    @staticmethod
    def hint(ob):
        return marker_type(ob, ('_connected_geometry_marker_type_hint'))
    @staticmethod
    def pathfinding_sphere(ob):
        return marker_type(ob, ('_connected_geometry_marker_type_pathfinding_sphere'))
    @staticmethod
    def physics_constraint(ob):
        return marker_type(ob, ('_connected_geometry_marker_type_physics_constraint'), ('$'))
    @staticmethod
    def target(ob):
        return marker_type(ob, ('_connected_geometry_marker_type_target'))
    @staticmethod
    def water_volume_flow(ob):
        return marker_type(ob, ('_connected_geometry_marker_type_water_volume_flow'))
    @staticmethod
    def airprobe(ob): # H4+ ONLY
        return marker_type(ob, ('_connected_geometry_marker_type_airprobe'))
    @staticmethod
    def envfx(ob): # H4+ ONLY
        return marker_type(ob, ('_connected_geometry_marker_type_envfx'))
    @staticmethod
    def lightCone(ob): # H4+ ONLY
        return marker_type(ob, ('_connected_geometry_marker_type_lightCone'))
    @staticmethod
    def animation_event(ob):
        return False
    @staticmethod
    def animation_control(ob):
        return False
    @staticmethod
    def animation_camera(ob):
        return False
    @staticmethod
    def frame_pca(ob): # H4+ ONLY
        return False
    @staticmethod
    def override(material):
        if not_bungie_game():
            return material.name.startswith('+') or material.nwo.material_override_h4 != 'none'
        else:
            return material.name.startswith('+') or material.nwo.material_override != 'none'


def run_tool(*tool_args):
    """Runs Tool using the specified function and arguments. Do not include 'tool' in the string passed"""
    os.chdir(get_ek_path())
    command = f"""{get_tool_type()} {' '.join(f'"{arg}"' for arg in tool_args)}"""
    # print(command)
    p = Popen(command)
    p.wait()

def rename_file(file_path, new_file_path=''):
    os.replace(file_path, new_file_path)

def dot_partition(target_string):
    """Returns a string after partitioning it using period. If the returned string will be empty, the function will instead return the argument passed"""
    return shortest_string(target_string.rpartition('.')[0], target_string)

def comma_partition(target_string):
    """Returns a string after partitioning it using comma. If the returned string will be empty, the function will instead return the argument passed"""
    return shortest_string(target_string.rpartition(',')[0], target_string)

def write_error_report(asset_path, report_text, file_1 = None, file_2 = None, file_3 = None):
    errors_folder = os.path.join(asset_path, 'errors')

    if not file_exists(errors_folder):
        os.makedirs(errors_folder)

    with open(os.path.join(errors_folder, 'output.txt'), 'a+') as f:
        f.write(report_text)
        f.write('\n')

    if file_1 is not None and file_exists(file_1):
        shutil.copy(file_1, errors_folder)
    if file_2 is not None and file_exists(file_2):
        shutil.copy(file_2, errors_folder)
    if file_3 is not None and file_exists(file_3):
        shutil.copy(file_3, errors_folder)

    clean_files(file_1, file_2, file_3)

def clean_files(file_1, file_2, file_3):
    if file_1 is not None and file_exists(file_1):
        os.remove(file_1)
    if file_2 is not None and file_exists(file_2):
        os.remove(file_2)
    if file_3 != '' and file_3 is not None and file_exists(file_3):
        os.remove(file_3)

def get_structure_from_halo_objects(halo_objects, include_frames=True):
    """Gets structure objects when passed a HaloObjects instance"""
    objects = halo_objects.lights + halo_objects.default + halo_objects.collision + halo_objects.physics + halo_objects.markers + halo_objects.cookie_cutters + halo_objects.poops + halo_objects.poop_markers + halo_objects.misc + halo_objects.seams + halo_objects.portals + halo_objects.water_surfaces
    if include_frames:
        objects += halo_objects.frame
    return objects

def get_prefab_from_halo_objects(halo_objects):
    """Gets structure objects when passed a HaloObjects instance"""
    return halo_objects.lights + halo_objects.collision + halo_objects.markers + halo_objects.cookie_cutters + halo_objects.poops + halo_objects.water_surfaces + halo_objects.frame

def get_design_from_halo_objects(halo_objects, include_frames=True):
    """Gets structure design objects when passed a HaloObjects instance"""
    objects = halo_objects.boundary_surfaces + halo_objects.fog + halo_objects.water_physics + halo_objects.poop_rain_blockers
    if include_frames:
        objects += halo_objects.frame
    return objects

def get_render_from_halo_objects(halo_objects):
    """Gets render objects when passed a HaloObjects instance"""
    return halo_objects.default + halo_objects.object_instances + halo_objects.lights

def select_all_lights(halo_objects):
    for ob in halo_objects.lights:
        ob.select_set(True)

# def get_skeleton_from_halo_objects(halo_objects, model_armature=None):
#     """Gets skeleton objects when passed a HaloObjects instance"""
#     return halo_objects.frame + model_armature + model_armature.data.bones

def SetBoneJSONValues(bones):
    print('tbd')

def HaloBoner(bones, model_armature, context):
    objects_in_scope = context.view_layer.objects
    ob_matrix = create_ob_matric_dict(objects_in_scope)
    set_active_object(model_armature)
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    for b in bones:
        pivot = b.head
        angle_x = radians(-90)
        axis_x = (1, 0, 0)
        M = (
            Matrix.Translation(pivot) @
            Matrix.Rotation(angle_x, 4, axis_x) @
            Matrix.Translation(-pivot)
            )
        b.matrix = M @ b.matrix

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    for ob in objects_in_scope:
        for key, value in ob_matrix.items():
            if key == ob:
                ob.matrix_world = value
                break

def halo_deboner(bones, model_armature, context):
    objects_in_scope = context.view_layer.objects
    ob_matrix = create_ob_matric_dict(objects_in_scope)
    set_active_object(model_armature)
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    for b in bones:
        pivot = b.head
        angle_x = radians(90)
        axis_x = (1, 0, 0)
        M = (
            Matrix.Translation(pivot) @
            Matrix.Rotation(angle_x, 4, axis_x) @
            Matrix.Translation(-pivot)
            )
        b.matrix = M @ b.matrix

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    for ob in objects_in_scope:
        for key, value in ob_matrix.items():
            if key == ob:
                ob.matrix_world = value
                break

def halo_noder(nodes, model_armature):
    set_active_object(model_armature)
    for n in nodes:
        pivot = model_armature.location
        angle_x = radians(-90)
        angle_z = radians(-180)
        axis_x = (1, 0, 0)
        axis_z = (0, 0, 1)
        M = (
            Matrix.Translation(pivot) @
            Matrix.Rotation(angle_x, 4, axis_x) @
            Matrix.Rotation(angle_z, 4, axis_z) @ 
            Matrix.Translation(-pivot)
            )
        n.matrix_world = M @ n.matrix_world

def halo_denoder(nodes, model_armature):
    set_active_object(model_armature)
    for n in nodes:
        pivot = model_armature.location
        angle_x = radians(90)
        angle_z = radians(180)
        axis_x = (1, 0, 0)
        axis_z = (0, 0, 1)
        M = (
            Matrix.Translation(pivot) @
            Matrix.Rotation(angle_z, 4, axis_z) @ 
            Matrix.Rotation(angle_x, 4, axis_x) @
            Matrix.Translation(-pivot)
            )
        n.matrix_world = M @ n.matrix_world

def create_ob_matric_dict(objects_in_scope):
    ob_matrix = {}
    for ob in objects_in_scope:
        mtrx = Matrix(ob.matrix_world)
        ob_matrix.update({ob: mtrx})

    return ob_matrix

#################################

# import example #
# from ..gr2_utils import (
#     frame_prefixes,
#     marker_prefixes,
#     mesh_prefixes,
#     special_prefixes,
#     boundary_surface_prefixes,
#     cookie_cutter_prefixes,
#     decorator_prefixes,
#     fog_volume_prefixes,
#     object_instance_prefixes,
#     portal_prefixes,
#     seam_prefixes,
#     water_volume_prefixes,
#     no_perm_prefixes,
#     poop_lighting_prefixes,
#     poop_pathfinding_prefixes,
#     poop_render_only_prefixes,
#     special_materials,
#     special_mesh_types,
#     invalid_mesh_types,
#     GetEKPath,
#     GetToolPath,
#     GetTagsPath,
#     GetDataPath,
#     GetPerm,
#     IsWindows,
#     CheckPath,
#     ObjectValid,
#     ExportPerm,
#     ExportBSP,
#     ResetPerm,
# )


######################################
# MANAGER STUFF
######################################

def get_collection_parents(current_coll, all_collections):
    coll_list = [current_coll.name]
    keep_looping = True
    
    while keep_looping:
        for coll in all_collections:
            keep_looping = True
            if current_coll in tuple(coll.children):
                coll_list.append(coll.name)
                current_coll = coll
                break
            else:
                keep_looping = False

    return coll_list

def get_prop_from_collection(ob, prefixes):
    prop = ''
    if len(bpy.data.collections) > 0:
        collection = None
        all_collections = bpy.data.collections
        # get direct parent collection
        for c in all_collections:
            if ob in tuple(c.objects):
                collection = c
                break
        # get collection parent tree
        if collection != None:
            collection_list = get_collection_parents(collection, all_collections)

            # test object collection parent tree
            for c in collection_list:
                if c.lower().startswith(prefixes[0]) or c.lower().startswith(prefixes[1]):
                    prop = c.rpartition(':')[2]
                    prop = prop.strip(' ')
                    prop = prop.replace(' ', '_')
                    if prop.rpartition('.')[0] != '':
                        prop = prop.rpartition('.')[0]
                    prop = prop.lower()
                    break

    return prop

# returns true if this material is a halo shader
def is_shader(mat):
    halo_mat = mat.nwo
    shader_path_not_empty = True if halo_mat.shader_path != '' else False
    no_material_override = True if halo_mat.material_override == 'NONE' else False
    no_special_material_name = True if not mat.name.lower().startswith(special_materials) else False

    return shader_path_not_empty and no_material_override and no_special_material_name