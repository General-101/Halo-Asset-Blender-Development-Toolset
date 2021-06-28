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

import os
import bpy
import sys
import traceback

from io_scene_halo.file_jms import export_jms
from io_scene_halo.global_functions import global_functions

class JMIScene(global_functions.HaloAsset):
    def __init__(self, context, report, filepath):
        self.world_nodes = []
        self.children_sets = []

        global_functions.unhide_all_collections()
        scene = bpy.context.scene
        object_list = list(scene.objects)

        for obj in object_list:
            if obj.name[0:1].lower() == '!':
                global_functions.unhide_object(obj)
                self.world_nodes.append(obj)

        for node in self.world_nodes:
            self.children_sets.append(global_functions.get_children(node))

def write_file(context, filepath, report, jmi_version, jmi_version_h2, jmi_version_h3, apply_modifiers, triangulate_faces, folder_type, edge_split, use_edge_angle, use_edge_sharp, split_angle, clean_normalize_weights, scale_enum, scale_float, console, hidden_geo, export_render, export_collision, export_physics, game_version, encoding):
    version = global_functions.get_version(jmi_version, None, jmi_version_h2, jmi_version_h3, game_version, console)

    jmi_scene = JMIScene(context, report, filepath)

    filename = global_functions.get_filename(None, None, None, None, None, True, filepath)
    root_directory = global_functions.get_directory(None, None, None, folder_type, None, filepath)

    file = open(root_directory + os.sep + filename, 'w', encoding=encoding)

    #write header
    version_bounds = '8207-8210'
    if game_version == 'halo3mcc':
        version_bounds = '8207-8213'

    file.write(
        ';### VERSION ###' +
        '\n%s' % (version) +
        '\n;\t<%s>\n' % (version_bounds) +
        '\n'
        )

    file.write(
        ';### TOTAL OBJECTS ###' +
        '\n%s' % (len(jmi_scene.children_sets)) +
        '\n;\t<name>' +
        '\n'
        )

    for world_nodes in jmi_scene.children_sets:
        file.write('\n%s' % (world_nodes[0].name.split('!', 1)[1]))

    file.close()
    for world_nodes in jmi_scene.children_sets:
        world_name = world_nodes[0].name.split('!', 1)[1]
        world_set = root_directory + os.sep + world_name
        if not os.path.exists(world_set):
            os.makedirs(world_set)

        bulk_output = world_set + os.sep + world_name
        export_jms.command_queue(context, bulk_output, report, jmi_version, None, jmi_version_h2, jmi_version_h3, True, True, folder_type, apply_modifiers, triangulate_faces, edge_split, use_edge_angle, use_edge_sharp, split_angle, clean_normalize_weights, scale_enum, scale_float, console, None, None, hidden_geo, export_render, export_collision, export_physics, game_version, encoding, world_nodes)

    report({'INFO'}, "Export completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_scene.jmi()
