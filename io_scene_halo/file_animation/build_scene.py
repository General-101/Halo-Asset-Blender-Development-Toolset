# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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
from ..global_functions import mesh_processing, global_functions

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

def create_animation(scene, armature, animation, nodes, fix_rotations, view_layer):
    for frame_idx, frame in enumerate(animation.frame_data):
        scene.frame_set(frame_idx + 1)
        for node_idx, node in enumerate(nodes):
            pose_bone = armature.pose.bones[node.name]

            matrix_scale = Matrix.Scale(frame[node_idx].scale, 4, (1, 1, 1))
            matrix_rotation = frame[node_idx].rotation.inverted().to_matrix().to_4x4()
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
            pose_bone.rotation_euler = transform_matrix.to_euler()

            view_layer.update()

            pose_bone.keyframe_insert('location')
            pose_bone.keyframe_insert('rotation_euler')
            pose_bone.keyframe_insert('rotation_quaternion')
            pose_bone.keyframe_insert('scale')

def create_overlay_animation(scene, armature, animation, nodes, base_transforms, default_node_transforms, fix_rotations, view_layer):
    for frame_idx, frame in enumerate(animation.frame_data):
        absolute_matrices = []
        scene.frame_set(frame_idx + 1)
        for node_idx, node in enumerate(nodes):
            pose_bone = armature.pose.bones[node.name]

            matrix_scale = Matrix.Scale(frame[node_idx].scale, 4, (1, 1, 1))
            matrix_rotation = frame[node_idx].rotation.inverted().to_matrix().to_4x4()
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
            pose_bone.rotation_euler = transform_matrix.to_euler()

            view_layer.update()

            pose_bone.keyframe_insert('location')
            pose_bone.keyframe_insert('rotation_euler')
            pose_bone.keyframe_insert('rotation_quaternion')
            pose_bone.keyframe_insert('scale')

def build_scene(context, ANIMATION, fix_rotations, report):
    scene = context.scene
    view_layer = context.view_layer

    active_object = context.view_layer.objects.active
    armature = None
    if active_object and active_object.type == 'ARMATURE':
        armature = active_object

    if armature and len(armature.data.bones) == ANIMATION.animations[0].node_count:
        nodes = global_functions.sort_by_layer(list(armature.data.bones), armature)[0]
        default_node_transforms = []
        for node in nodes:
            pose_bone = armature.pose.bones[node.name]
            pose_bone_loc, pose_bone_rot, pose_bone_scale = pose_bone.matrix.decompose()
            pose_translation = Matrix.Translation(pose_bone_loc)
            pose_rotation = pose_bone_rot.to_matrix().to_4x4()
            pose_scale = Matrix.Scale(pose_bone_scale[0], 4, (1, 1, 1))
            pose_matrix = pose_translation @ pose_rotation @ pose_scale
            if pose_bone.parent:
                parent_node_idx = nodes.index(node.parent)
                pose_bone_parent_matrix = default_node_transforms[parent_node_idx]
                pose_matrix = pose_bone_parent_matrix @ pose_matrix

            default_node_transforms.append(pose_matrix)

        scene.render.fps = 30
        for animation in ANIMATION.animations:
            scene.frame_end = animation.frame_count + 1

            action = bpy.data.actions.get(animation.name)
            if action is None:
                action = bpy.data.actions.new(name=animation.name)

            mesh_processing.select_object(context, armature)
            armature.animation_data_create()
            armature.animation_data.action = action

            bpy.ops.object.mode_set(mode = 'POSE')

            if animation.type == 1:
                base_transforms = None
                animation_index = find_base_animation(ANIMATION, animation)
                if not animation_index == -1:
                    base_transforms = ANIMATION.animations[animation_index].frame_data[0]

                create_overlay_animation(scene, armature, animation, nodes, base_transforms, default_node_transforms, fix_rotations, view_layer)

            else:
                create_animation(scene, armature, animation, nodes, fix_rotations, view_layer)

            scene.frame_set(1)
            bpy.ops.object.mode_set(mode = 'OBJECT')

        report({'INFO'}, "Import completed successfully")

    else:
        report({'ERROR'}, "No valid armature is active. Import will now be aborted")
