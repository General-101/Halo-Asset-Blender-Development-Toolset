# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2023 Steven Garcia
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

from io import BytesIO, TextIOWrapper
import zipfile
import bpy
import bmesh

from os import path
from mathutils import Matrix
from ..file_jms.format import JMSAsset
from ..global_functions import mesh_processing
from ..file_jms.process_file_retail import process_file_retail

halo_one_array = (
("captain", (12.3111, 42.2709, 63.7826)),
("cortana", (2.66301, 8.74704, 17.708)),
("crewman", (12.8364, 66.7419, 63.4986)),
("spartan", (18.4183, 29.8282, 70.362)),
("elite", (32.298, 38.9082, 78.7431)),
("engineer", (51.4198, 50.6977, 60.3388)),
("flood_captain", (327.795, 440.535, 410.072)),
("flood_carrier", (30.1602, 38.0178, 66.9182)),
("flood_combat_elite", (41.6301, 52.8918, 77.6044)),
("flood_combat_human", (23.2195, 70.4576, 65.9787)),
("flood_infection", (33.413, 17.3191, 29.3818)),
("grunt", (39.373, 59.9387, 58.2778)),
("hunter", (40.7214, 79.3188, 97.2544)),
("jackal", (22.2103, 78.7578, 68.9278)),
("marine", (13.842, 65.999, 63.4986)),
("marine_armored", (14.3165, 65.999, 64.7352)),
("monitor", (18.4776, 16.6294, 18.2989)),
("pilot", (10.7193, 58.4392, 63.0268)),
("sentinel", (97.3894, 77.8164, 54.1884)),
("banshee", (181.696, 223.697, 153.003)),
("c_gun_turret", (144.126, 102.447, 86.9799)),
("c_dropship", (913.152, 590.52, 345.855)),
("fighterbomber", (2101.47, 2459.11, 422.88)),
("ghost", (138.052, 118.219, 57.9257)),
("lifepod", (346.175, 171.859, 132.772)),
("lifepod_entry", (346.175, 306.638, 292.345)),
("pelican", (1059.52, 768.222, 335.925)),
("rwarthog", (191.541, 97.507, 103.53)),
("scorpion", (330.661, 236, 134.611)),
("warthog", (191.541, 97.507, 103.53)),
("wraith", (285.149, 301.778, 120.056)))

halo_two_array = (
("arbiter", (36.8044, 36.6057, 74.5943)),
("brute", (36.3108, 62.7213, 94.4206)),
("bugger", (47.7398, 102.08, 74.2974)),
("cortana", (9.43609, 47.0279, 58.7835)),
("elite", (38.6935, 37.8494, 78.8009)),
("elite_heretic", (38.1226, 36.6057, 72.3174)),
("elite_ranger", (38.7561, 38.1855, 73.683)),
("flood_carrier", (30.1591, 38.4047, 66.993)),
("flood_combat_elite", (37.7746, 54.7906, 77.6044)),
("flood_combat_human", (24.836, 70.7481, 66.54)),
("flood_infection", (33.4114, 17.3191, 35.0402)),
("flood_juggernaut", (95.0128, 233.361, 268.477)),
("gravemind", (1212.6, 2048.22, 2765.54)),
("grunt", (40.0014, 62.4235, 58.6502)),
("grunt_heretic", (36.2111, 62.4235, 53.0942)),
("hunter", (48.8067, 95.1825, 125.199)),
("jackal", (42.0499, 60.2807, 73.1629)),
("lord_hood", (13.7251, 42.6697, 64.3284)),
("spartan", (31.4245, 37.1795, 70.385)),
("marine", (17.3255, 42.6651, 72.6993)),
("marine_odst", (15.3371, 42.6651, 64.1096)),
("miranda", (10.3354, 37.5698, 60.0175)),
("monitor", (19.0924, 16.6294, 18.2988)),
("prophet_mercy", (43.455, 68.6003, 71.9295)),
("prophet_minor", (43.455, 68.6003, 64.83)),
("prophet_regret", (111.196, 110.922, 112.837)),
("prophet_truth", (43.455, 68.6003, 94.2422)),
("sentinel_aggressor", (97.3894, 77.8163, 54.1884)),
("sentinel_constructor", (13.7275, 9.72803, 20.1384)),
("sentinel_enforcer", (230.857, 213.692, 178.438)),
("banshee", (182.354, 223.697, 153.003)),
("c_turret_ap", (86.5427, 58.1101, 70.2204)),
("falcon", (389.63, 232.298, 102.118)),
("ghost", (137.29, 118.219, 59.0579)),
("gravity_throne", (58.3561, 48.8965, 48.3635)),
("h_turret_ap", (50.7009, 44.9245, 58.03)),
("insertion_pod", (65.6357, 62.4232, 162.513)),
("longsword", (1050.73, 1229.56, 211.44)),
("pelican", (1002.92, 768.444, 358.889)),
("phantom", (1062.07, 668.449, 391.472)),
("scorpion", (330.661, 236, 78.8686)),
("shadow", (454.241, 268.548, 222.429)),
("spectre", (211.816, 165.91, 86.1823)),
("warthog", (196.471, 97.5279, 75.7276)),
("wraith", (285.526, 304.287, 91.9563)))

halo_three_array = (
("arbiter", (37.6219, 37.2558, 75.2782)),
("brute", (57.1543, 66.2881, 94.6532)),
("bugger", (44.0028, 102.07, 74.1832)),
("cortana", (8.7529, 47.1229, 59.1449)),
("elite", (38.6283, 39.3896, 79.7273)),
("flood_carrier", (43.2805, 39.6819, 72.2342)),
("flood_combat_brute", (45.6046, 79.447, 85.7513)),
("flood_combat_elite", (42.786, 66.2445, 84.376)),
("flood_combat_human", (35.6591, 57.1697, 65.4288)),
("flood_infection", (43.2821, 21.9043, 43.0903)),
("flood_ranged", (74.2284, 65.1949, 90.8217)),
("flood_stalker", (76.2962, 67.6971, 108.162)),
("flood_tank", (76.3723, 76.9674, 119.754)),
("grunt", (40.9928, 63.4244, 58.3307)),
("hunter", (48.5997, 100.363, 124.973)),
("jackal", (42.5687, 60.035, 73.3182)),
("lord_hood", (12.6568, 42.7395, 64.2509)),
("spartan", (31.7239, 37.2393, 70.2989)),
("marine", (18.3755, 43.0221, 71.9175)),
("marine_odst", (14.2101, 42.5174, 63.847)),
("miranda", (14.0764, 37.8095, 60.3959)),
("monitor", (20.3919, 17.4932, 18.9802)),
("prophet_truth", (40.353, 68.6003, 74.7206)),
("sentinel_aggressor", (97.3894, 77.8163, 54.1884)),
("sentinel_constructor", (13.7275, 9.72803, 20.1384)),
("worker", (11.7373, 42.6598, 64.5513)),
("banshee", (195.855, 225.765, 128.05)),
("chopper", (221.621, 97.7097, 98.4085)),
("cov_capital_ship", (28522.5, 11277.1, 3981.02)),
("cov_cruiser", (24224.6, 11468.3, 3663.55)),
("cov_cruiser_flood", (24224.6, 11468.3, 3663.55)),
("ghost", (138.574, 118.218, 61.7782)),
("gravity_throne", (58.353, 51.4155, 97.4521)),
("hornet", (314.269, 291.202, 148.801)),
("insertion_pod", (56.8505, 62.5648, 171.582)),
("longsword", (1094, 1100, 170)),
("prowler", (236.183, 137.775, 87.0731)),
("mongoose", (101.933, 60.0935, 50.7133)),
("pelican", (1009.16, 768.444, 321.431)),
("phantom", (1095.29, 668.449, 454.621)),
("scorpion", (338.856, 253.761, 92.27)),
("shade", (135.771, 119.026, 135.203)),
("warthog", (199.299, 101.492, 76.7727)),
("wraith", (299.835, 303.158, 93.8022)))

#  load a mesh from JMS and use it as a scale model
def generate_mesh(file, array_item, game_version):
    default_region = mesh_processing.get_default_region_permutation_name(game_version)
    default_permutation = mesh_processing.get_default_region_permutation_name(game_version)

    retail_JMS_version_list = (8197, 8198, 8199, 8200, 8201, 8202, 8203, 8204, 8205, 8206, 8207, 8208, 8209, 8210, 8211, 8212, 8213)

    JMS = JMSAsset(file)
    JMS = process_file_retail(JMS, game_version, "JMS", retail_JMS_version_list, default_region, default_permutation)
    item_name = array_item[0]

    mesh = bpy.data.meshes.new(item_name)
    if not len(JMS.vertices) == 0:
        vert_normal_list = []
        bm = bmesh.new()
        for triangle in JMS.triangles:
            p1 = JMS.vertices[triangle.v0].translation
            p2 = JMS.vertices[triangle.v1].translation
            p3 = JMS.vertices[triangle.v2].translation
            v1 = bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = bm.verts.new((p2[0], p2[1], p2[2]))
            v3 = bm.verts.new((p3[0], p3[1], p3[2]))
            bm.faces.new((v1, v2, v3))
            vert_list = [triangle.v0, triangle.v1, triangle.v2]
            for vert in vert_list:
                vert_normals = []
                jms_vert = JMS.vertices[vert]
                for normal in jms_vert.normal:
                    vert_normals.append(normal)

                vert_normal_list.append(vert_normals)

        bm.to_mesh(mesh)
        bm.free()
        mesh.normals_split_custom_set(vert_normal_list)
        mesh.use_auto_smooth = True

    return mesh

# if the JMS file is not found fall back to a box scale model
def generate_box(array_item):
    item_name = array_item[0]

    mesh = bpy.data.meshes.new(item_name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.transform(Matrix.Translation((0, 0, 0.5)))
    bm.to_mesh(mesh)
    bm.free()

    return mesh

def get_object_mesh(array_item, game_version):
    # root folder for the plugin (bit of a hack)
    script_folder_path = path.dirname(path.dirname(__file__))
    # relative path of the JMS from the resources path
    path_relative = game_version + "/" +  array_item[0] + ".jms"
    # expected on disk path of the JMS
    filepath = path.join(script_folder_path, "resources", path_relative)
    # resources zip file path (won't exist in dev builds)
    path_resources_zip = path.join(script_folder_path, "resources.zip")

    # first check the disk
    if path.exists(filepath):
        print(f"Loading {filepath} from disk")
        return generate_mesh(filepath, array_item, game_version), False
    elif path.exists(path_resources_zip):
        print(f"Loading {path_relative} from {path_resources_zip}")
        zip: zipfile.ZipFile = zipfile.ZipFile(path_resources_zip, mode = 'r')
        jms_file_data = zip.read(path_relative)
        stream: TextIOWrapper = TextIOWrapper(BytesIO(jms_file_data), encoding="utf-8")
        return generate_mesh(stream, array_item, game_version), False

    print(f"Couldn't find {array_item[0]}!")
    # if all else fails we return a BOX
    return generate_box(array_item), True

def generate_object(context, array_item, game_version):

    mesh, is_box = get_object_mesh(array_item, game_version)
    object_name = "scale_model_%s" % array_item[0]
    object_dimensions = array_item[1]

    object_mesh = bpy.data.objects.new(object_name, mesh)
    context.collection.objects.link(object_mesh)

    if is_box:
        object_mesh.dimensions = object_dimensions

    mesh_processing.select_object(context, object_mesh)

    object_mesh.location = context.scene.cursor.location

def create_model(context, game_version, halo_1_unit_index, halo_2_unit_index, halo_3_unit_index):
    if game_version == "halo1":
        array_item = halo_one_array[int(halo_1_unit_index)]

    elif game_version == "halo2":
        array_item = halo_two_array[int(halo_2_unit_index)]

    else:
        array_item = halo_three_array[int(halo_3_unit_index)]

    mesh_processing.deselect_objects(context)
    generate_object(context, array_item, game_version)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.scale_model()
