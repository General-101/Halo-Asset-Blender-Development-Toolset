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

from math import radians
from mathutils import Matrix

def find_base_animation(ANIMATION, current_animation):
    animation_index = -1
    animation_set = current_animation.name.split(' ')
    base_animation_name = animation_set[0]
    if len(animation_set) == 2:
        base_animation_name = "%s %s" % (animation_set[0], "exit")

    elif len(animation_set) == 3:
        animation_class = animation_set[2]
        base_animation_name = "%s %s %s" % (animation_set[0], animation_set[1], "idle")
        if "gut" in animation_class:
            base_animation_name = "%s %s %s" % ("s-kill", animation_set[1], "gut")

        if animation_class == "aim_move":
            base_animation_name = "%s %s %s" % (animation_set[0], animation_set[1], "move-front")

    for animation_idx, animation in enumerate(ANIMATION.animations):
        if animation.name.startswith(base_animation_name):
            animation_index = animation_idx

    return animation_index

def create_animation(scene, armature, animation, nodes, fix_rotations, view_layer, is_inverted):
    node_name = []
    for frame_idx, frame in enumerate(animation.frame_data):
        scene.frame_set(frame_idx + 1)
        #for node_idx in range(animation.node_count):
        #    pose_bone = armature.pose.bones[node_name[node_idx]]
        for node_idx, node in enumerate(nodes):
            pose_bone = armature.pose.bones[node.name]

            rotation = frame[node_idx].rotation
            if is_inverted:
                rotation = frame[node_idx].rotation.inverted()

            matrix_scale = Matrix.Scale(frame[node_idx].scale, 4)
            matrix_rotation = rotation.to_matrix().to_4x4()
            matrix_translation = Matrix.Translation(frame[node_idx].translation)
            transform_matrix = matrix_translation @ matrix_rotation @ matrix_scale

            if fix_rotations:
                if pose_bone.parent:
                    transform_matrix = (pose_bone.parent.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

                transform_matrix = transform_matrix @ Matrix.Rotation(radians(-90.0), 4, 'Z')

            else:
                if pose_bone.parent:
                    transform_matrix = pose_bone.parent.matrix @ transform_matrix

            pose_bone.matrix = transform_matrix

            view_layer.update()

            pose_bone.keyframe_insert('location')
            pose_bone.keyframe_insert('rotation_quaternion')
            pose_bone.keyframe_insert('scale')

def create_overlay_animation(scene, armature, animation, nodes, fix_rotations, view_layer, is_inverted):
    node_name = []
    for frame_idx, frame in enumerate(animation.frame_data):
        scene.frame_set(frame_idx + 1)
        #for node_idx in range(animation.node_count):
        #    pose_bone = armature.pose.bones[node_name[node_idx]]
        for node_idx, node in enumerate(nodes):
            pose_bone = armature.pose.bones[node.name]

            rotation = frame[node_idx].rotation
            if is_inverted:
                rotation = frame[node_idx].rotation.inverted()

            matrix_scale = Matrix.Scale(frame[node_idx].scale, 4)
            matrix_rotation = rotation.to_matrix().to_4x4()
            matrix_translation = Matrix.Translation(frame[node_idx].translation)
            transform_matrix = matrix_translation @ matrix_rotation @ matrix_scale

            if fix_rotations:
                if pose_bone.parent:
                    transform_matrix = (pose_bone.parent.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

                transform_matrix = transform_matrix @ Matrix.Rotation(radians(-90.0), 4, 'Z')

            else:
                if pose_bone.parent:
                    transform_matrix = pose_bone.parent.matrix @ transform_matrix

            pose_bone.matrix = transform_matrix

            view_layer.update()

            pose_bone.keyframe_insert('location')
            pose_bone.keyframe_insert('rotation_quaternion')
            pose_bone.keyframe_insert('scale')

def build_scene(context, ANIMATION, game_version, game_title, file_version, fix_rotations, empty_markers, report, mesh_processing, global_functions):
    scene = context.scene
    view_layer = context.view_layer

    active_object = context.view_layer.objects.active
    armature = None
    if active_object and active_object.type == 'ARMATURE':
        armature = active_object

    if armature:
        bone_count = len(armature.data.bones)
        nodes = global_functions.sort_by_layer(list(armature.data.bones), armature)[0]

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

            scene.frame_end = animation.frame_count + 1

            action = bpy.data.actions.get(animation.name)
            if action is None:
                action = bpy.data.actions.new(name=animation.name)

            action.use_fake_user = True
            mesh_processing.select_object(context, armature)
            armature.animation_data_create()
            armature.animation_data.action = action

            bpy.ops.object.mode_set(mode = 'POSE')

            if animation.type == 1:
                base_transforms = None
                animation_index = find_base_animation(ANIMATION, animation)
                if not animation_index == -1:
                    base_transforms = ANIMATION.animations[animation_index].frame_data[0]

                create_overlay_animation(scene, armature, animation, nodes, fix_rotations, view_layer, is_inverted)

            else:
                create_animation(scene, armature, animation, nodes, fix_rotations, view_layer, is_inverted)

            scene.frame_set(1)
            bpy.ops.object.mode_set(mode = 'OBJECT')

        report({'INFO'}, "Import completed successfully")

    else:
        report({'ERROR'}, "No valid armature is active. Import will now be aborted")
