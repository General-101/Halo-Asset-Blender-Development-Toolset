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

import bpy

from ...file_jma.format import JMAAsset
from ...global_functions import global_functions

def build_scene(context, ANIMATION, game_version, game_title, file_version, fix_rotations, empty_markers, report):
    JMA = JMAAsset()
    JMA.version == 16392

    scene = context.scene
    view_layer = context.view_layer

    active_object = context.view_layer.objects.active
    armature = None
    if active_object and active_object.type == 'ARMATURE':
        armature = active_object

    if armature:
        bone_count = len(armature.data.bones)
        nodes = list(armature.data.bones)
        if game_title == "halo1":
            nodes = global_functions.sort_by_layer(list(armature.data.bones), armature)[0]
        else:
            nodes = ANIMATION.nodes

        node_names = []
        default_node_transforms = []
        for node_idx, node in enumerate(nodes):
            node_name = node.name
            node_names.append(node_name)
            pose_bone = armature.pose.bones[node_name]
            default_node_transforms.append(pose_bone.matrix)

        scene.render.fps = 30

        is_inverted = False
        if game_title == "halo1":
            is_inverted = True

        for animation in ANIMATION.animations:
            if len(animation.frame_data) == 0:
                continue

            action = bpy.data.actions.get(animation.name)
            if action is None:
                action = bpy.data.actions.new(name=animation.name)

            action.use_fake_user = True
            action.use_frame_range = True
            action.frame_start = 1
            action.frame_end = animation.frame_count + 1

            armature.animation_data_create()
            armature.animation_data.action = action

            global_functions.import_fcurve_data(action, armature, nodes, animation.frame_data, JMA, JMAAsset, fix_rotations, is_inverted)

        report({'INFO'}, "Import completed successfully")

    else:
        report({'ERROR'}, "No valid armature is active. Import will now be aborted")
