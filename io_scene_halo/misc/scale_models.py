# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2020 Steven Garcia
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
import bmesh

from os import path
from mathutils import Matrix
from io_scene_halo.file_jms import import_jms
from io_scene_halo.global_functions import global_functions

def halo_one_dimensions(model_name):
    object_dimensions = (1, 1, 1)
    if model_name == "captain":
        object_dimensions = (12.3111, 42.2709, 63.7826)
    elif model_name == "cortana":
        object_dimensions = (2.66301, 8.74704, 17.708)
    elif model_name == "crewman":
        object_dimensions = (12.8364, 66.7419, 63.4986)
    elif model_name == "spartan":
        object_dimensions = (18.4183, 29.8282, 70.362)
    elif model_name == "elite":
        object_dimensions = (32.298, 38.9082, 78.7431)
    elif model_name == "engineer":
        object_dimensions = (51.4198, 50.6977, 60.3388)
    elif model_name == "flood_captain":
        object_dimensions = (327.795, 440.535, 410.072)
    elif model_name == "flood_infection":
        object_dimensions = (33.413, 17.3191, 29.3818)
    elif model_name == "flood_carrier":
        object_dimensions = (30.1602, 38.0178, 66.9182)
    elif model_name == "floodcombat_elite":
        object_dimensions = (41.6301, 52.8918, 77.6044)
    elif model_name == "floodcombat_human":
        object_dimensions = (23.2195, 70.4576, 65.9787)
    elif model_name == "grunt":
        object_dimensions = (39.373, 59.9387, 58.2778)
    elif model_name == "hunter":
        object_dimensions = (40.7214, 79.3188, 97.2544)
    elif model_name == "jackal":
        object_dimensions = (22.2103, 78.7578, 68.9278)
    elif model_name == "marine":
        object_dimensions = (13.842, 65.999, 63.4986)
    elif model_name == "marine_armored":
        object_dimensions = (14.3165, 65.999, 64.7352)
    elif model_name == "monitor":
        object_dimensions = (18.4776, 16.6294, 18.2989)
    elif model_name == "pilot":
        object_dimensions = (10.7193, 58.4392, 63.0268)
    elif model_name == "sentinel":
        object_dimensions = (97.3894, 77.8164, 54.1884)
    elif model_name == "banshee":
        object_dimensions = (181.696, 223.697, 153.003)
    elif model_name == "c_gun_turret":
        object_dimensions = (144.126, 102.447, 86.9799)
    elif model_name == "c_dropship":
        object_dimensions = (913.152, 590.52, 345.855)
    elif model_name == "fighterbomber":
        object_dimensions = (2101.47, 2459.11, 422.88)
    elif model_name == "ghost":
        object_dimensions = (138.052, 118.219, 57.9257)
    elif model_name == "lifepod":
        object_dimensions = (346.175, 171.859, 132.772)
    elif model_name == "lifepod_entry":
        object_dimensions = (346.175, 306.638, 292.345)
    elif model_name == "pelican":
        object_dimensions = (1059.52, 768.222, 335.925)
    elif model_name == "rwarthog":
        object_dimensions = (191.541, 97.507, 103.53)
    elif model_name == "scorpion":
        object_dimensions = (330.661, 236, 134.611)
    elif model_name == "warthog":
        object_dimensions = (191.541, 97.507, 103.53)
    elif model_name == "wraith":
        object_dimensions = (285.149, 301.778, 120.056)

    return object_dimensions

def generate_mesh(filepath, model_name):
    jms_file = import_jms.JMSAsset( filepath, "halo3")

    #generate mesh object
    if not len(jms_file.vertices) == 0:
        vert_normal_list = []

        object_name = "Scale_Model_%s" % model_name

        mesh = bpy.data.meshes.new(object_name)
        object_mesh = bpy.data.objects.new(object_name, mesh)
        bpy.context.collection.objects.link(object_mesh)
        bm = bmesh.new()
        for idx, triangle in enumerate(jms_file.triangles):
            p1 = jms_file.vertices[triangle.v0].translation
            p2 = jms_file.vertices[triangle.v1].translation
            p3 = jms_file.vertices[triangle.v2].translation
            v1 = bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = bm.verts.new((p2[0], p2[1], p2[2]))
            v3 = bm.verts.new((p3[0], p3[1], p3[2]))
            bm.faces.new((v1, v2, v3))
            vert_list = [triangle.v0, triangle.v1, triangle.v2]
            for vert in vert_list:
                vert_normals = []
                jms_vert = jms_file.vertices[vert]
                for normal in jms_vert.normal:
                    vert_normals.append(normal)

                vert_normal_list.append(vert_normals)

        bm.to_mesh(mesh)
        bm.free()
        object_mesh.data.normals_split_custom_set(vert_normal_list)
        object_mesh.data.use_auto_smooth = True
        object_mesh.select_set(True)

def generate_box(model_name):
    mesh = bpy.data.meshes.new(model_name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.transform(Matrix.Translation((0, 0, 0.5)))
    bm.to_mesh(mesh)
    bm.free()

    object_mesh = bpy.data.objects.new("Scale_Model_%s" % model_name, mesh)
    bpy.context.collection.objects.link(object_mesh)

    object_mesh.dimensions = halo_one_dimensions(model_name)

def create_model(game_version, unit_type, char_model_name, vehi_model_name):
    print(unit_type)
    if unit_type == "character":
        model_name = char_model_name
    else:
        model_name = vehi_model_name

    script_folder_path = bpy.utils.script_path_user()
    filepath = script_folder_path + "\\addons\\io_scene_halo\\resources\\" + game_version + "\\" + model_name + ".jms"

    if path.exists(filepath):
        generate_mesh(filepath, model_name)
    else:
        generate_box(model_name)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.scale_model()
