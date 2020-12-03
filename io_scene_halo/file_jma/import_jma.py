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
import sys
import traceback

from os import path
from enum import Flag, auto
from io_scene_halo.file_jms import import_jms
from mathutils import Vector, Quaternion, Matrix, Euler
from io_scene_halo.global_functions import global_functions

class JMAAsset(global_functions.HaloAsset):
    """
    Reads a JMA file into memory\n
    self.node_checksum - checksum value or -1\n
    self.version - JMA version\n
    self.frame_rate - frame rate for animation\n
    self.nodes - included for 16392+\n
    self.node_count - included for 16390\n
    self.transforms - 2D array of transforms [frame_idx][node_idx]\n
    self.biped_controller_transforms - included for 16395
    self.biped_controller_frame_type - BipedControllerFrameType enum
    """
    class Transform:
        def __init__(self, vector, rotation, scale):
            self.vector = vector
            self.rotation = rotation
            self.scale = scale
    class Node:
        def __init__(self, name, parent=None, child=None, sibling=None):
            self.name = name
            self.parent = parent
            self.child = child
            self.sibling = sibling
            self.visited = False
    class BipedControllerFrameType(Flag):
        DISABLE = 0
        DX = auto()
        DY = auto()
        DZ = auto()
        DYAW = auto()

        JMA = DX | DY
        JMT = DX | DY | DYAW
        JMRX = DX | DY | DZ | DYAW

    def are_quaternions_inverted(self):
        return self.version < 16394

    def next_transform(self):
        translation = self.next_vector()
        rotation = self.next_quaternion()
        scale = float(self.next())
        return JMAAsset.Transform(translation, rotation, scale)

    def __init__(self, filepath, game_version):
        super().__init__(filepath)
        extension = global_functions.get_true_extension(filepath, None, True)
        self.node_checksum = -1
        self.version = int(self.next())
        version_list = (16390,16391,16392,16393,16394,16395)
        if not self.version in version_list:
            raise global_functions.AssetParseError("Importer does not support this " + extension + " version")
        self.game_version = game_version
        if game_version == 'auto':
            self.game_version = global_functions.get_game_version(self.version, 'JMA')
        if self.version >= 16394:
            self.node_checksum = int(self.next())
        transform_count = int(self.next())
        self.frame_rate = float(self.next())
        actor_count = int(self.next())
        self.actor_name = self.next()
        self.frame_count = transform_count

        if actor_count != 1:
            raise global_functions.AssetParseError(extension + " actor count must be 1!")

        node_count = int(self.next())
        if self.version < 16394:
            self.node_checksum = int(self.next())
        self.nodes = []
        self.transforms = []
        if self.version >= 16394:
            for _ in range(node_count):
                name = self.next()
                parent = int(self.next())
                self.nodes.append(JMAAsset.Node(name, parent=parent))
        elif self.version >= 16392:
            for _ in range(node_count):
                name = self.next()
                child = int(self.next())
                sibling = int(self.next())
                self.nodes.append(JMAAsset.Node(name, child=child, sibling=sibling))
        elif self.version == 16391:
            for _ in range(node_count):
              self.nodes.append(JMAAsset.Node(self.next()))
        else:
            self.node_count = node_count

        for _ in range(transform_count):
            transforms_for_frame = []

            for node_idx in range(node_count):
                transforms_for_frame.append(self.next_transform())

            self.transforms.append(transforms_for_frame)

        self.biped_controller_frame_type = JMAAsset.BipedControllerFrameType.DISABLE
        if self.version == 16395:
            self.biped_controller_transforms = []
            biped_controller_enabled = int(self.next())
            if biped_controller_enabled > 0:
                # different animation file types use the data differently
                if extension == 'jma':
                    self.biped_controller_frame_type = JMAAsset.BipedControllerFrameType.JMA
                elif extension == 'jmt':
                    self.biped_controller_frame_type = JMAAsset.BipedControllerFrameType.JMT
                elif extension == 'jmrx':
                    self.biped_controller_frame_type = JMAAsset.BipedControllerFrameType.JMRX

                for _ in range(transform_count):
                    self.biped_controller_transforms.append(self.next_transform())

        if self.left() != 0: # is something wrong with the parser?
            raise RuntimeError("%s elements left after parse end" % self.left())

        # update node graph
        if self.version >= 16394:
            # loop over nodes and
            for node_idx in range(node_count):
                node = self.nodes[node_idx]
                if node.parent == -1:
                    continue # this is a root node, nothing to update
                if node.parent >= len(self.nodes) or node.parent == node_idx:
                    raise global_functions.AssetParseError("Malformed node graph (bad parent index)")
                parent_node = self.nodes[node.parent]
                if parent_node.child:
                    node.sibling = parent_node.child
                else:
                    node.sibling = -1
                if node.sibling >= len(self.nodes):
                    raise global_functions.AssetParseError("Malformed node graph (sibling index out of range)")
                parent_node.child = node_idx
        elif self.version >= 16392:
            for node_idx in range(node_count):
                node = self.nodes[node_idx]
                if node.child == -1:
                    continue # no child nodes, nothing to update
                if node.child >= len(self.nodes) or node.child == node_idx:
                    raise global_functions.AssetParseError("Malformed node graph (bad child index)")
                child_node = self.nodes[node.child]
                while child_node != None:
                    child_node.parent = node_idx
                    if child_node.visited:
                        raise global_functions.AssetParseError("Malformed node graph (circular reference)")
                    child_node.visited = True
                    if child_node.sibling >= len(self.nodes):
                        raise global_functions.AssetParseError("Malformed node graph (sibling index out of range)")
                    if child_node.sibling != -1:
                        child_node = self.nodes[child_node.sibling]
                    else:
                        child_node = None

def load_file(context, filepath, report, fix_parents, game_version, jms_path_a, jms_path_b):
    jms_a_transform = False
    jms_b_transform = False

    try:
        jma_file = JMAAsset(filepath, game_version)
        if path.exists(jms_path_a):
            jms_a_transform = True
            jms_a_file = import_jms.JMSAsset(jms_path_a, "halo2")
        if path.exists(jms_path_a) and path.exists(jms_path_b):
            jms_b_transform = True
            jms_b_file = import_jms.JMSAsset(jms_path_b, "halo2")
    except global_functions.AssetParseError as parse_error:
        info = sys.exc_info()
        traceback.print_exception(info[0], info[1], info[2])
        report({'ERROR'}, "Bad file: {0}".format(parse_error))
        return {'CANCELLED'}
    except:
        info = sys.exc_info()
        traceback.print_exception(info[0], info[1], info[2])
        report({'ERROR'}, "Internal error: {1}({0})".format(info[1], info[0]))
        return {'CANCELLED'}

    collection = bpy.context.collection
    scene = bpy.context.scene
    view_layer = bpy.context.view_layer
    armature = None
    object_list = list(scene.objects)

    scene_nodes = []
    jma_nodes = []
    jms_a_nodes = []
    jms_b_nodes = []
    for obj in object_list:
        if armature is None:
            if obj.type == 'ARMATURE':
                is_armature_good = False
                if jma_file.version == 16390:
                    if len(obj.data.bones) == jma_file.node_count:
                        is_armature_good = True
                else:
                    exist_count = 0
                    armature_bone_list = list(obj.data.bones)
                    for node in armature_bone_list:
                        for jma_node in jma_file.nodes:
                            if node.name == jma_node.name:
                                scene_nodes.append(node.name)
                                exist_count += 1
                    if exist_count == len(jma_file.nodes):
                        is_armature_good = True

                if is_armature_good:
                    armature = obj
                    view_layer.objects.active = armature

    if armature == None:
        if jma_file.version >= 16392:
            for jma_node in jma_file.nodes:
                jma_nodes.append(jma_node.name)

            if len(scene_nodes) > 0:
                for jma_node in jma_nodes:
                    if not jma_node in scene_nodes:
                        report({'WARNING'}, "Node '%s' not found in an existing armature" % jma_node)

            if jms_a_transform and not jms_b_transform:
                for jms_node in jms_a_file.nodes:
                    jms_a_nodes.append(jms_node.name)

                for jms_node_name in jms_a_nodes:
                    if not jms_node_name in jma_nodes:
                        jms_a_transform = False
                        report({'WARNING'}, "Node '%s' from JMS skeleton not found in JMA skeleton." % jms_node_name)

                report({'WARNING'}, "No valid armature detected. One will be created and the referenced JMS will be used for the rest position")

            elif jms_a_transform and jms_b_transform:
                for jms_node in jms_a_file.nodes:
                    jms_a_nodes.append(jms_node.name)

                for jms_node in jms_b_file.nodes:
                    jms_b_nodes.append(jms_node.name)

                jms_nodes = jms_a_nodes + jms_b_nodes

                for jms_node_name in jms_nodes:
                    if not jms_node_name in jma_nodes:
                        jms_a_transform = False
                        report({'WARNING'}, "Node '%s' from JMS skeleton not found in JMA skeleton." % jms_node_name)

                report({'WARNING'}, "No valid armature detected. One will be created and the referenced JMS files will be used for the rest position")

            else:
                report({'WARNING'}, "No valid armature detected. One will be created but expect issues with visuals in scene due to no proper rest position")

            pelvis = None
            thigh0 = None
            thigh1 = None
            spine1 = None
            clavicle0 = None
            clavicle1 = None

            armdata = bpy.data.armatures.new('Armature')
            ob_new = bpy.data.objects.new('Armature', armdata)
            collection.objects.link(ob_new)
            armature = ob_new
            view_layer.objects.active = armature
            if fix_parents:
                if game_version == 'halo2':
                    for idx, jma_node in enumerate(jma_file.nodes):
                        if 'pelvis' in jma_node.name:
                            pelvis = idx
                        if 'thigh' in jma_node.name:
                            if thigh0 == None:
                                thigh0 = idx
                            else:
                                thigh1 = idx

                        elif 'spine1' in jma_node.name:
                            spine1 = idx
                        elif 'clavicle' in jma_node.name:
                            if clavicle0 == None:
                                clavicle0 = idx
                            else:
                                clavicle1 = idx

            first_frame = jma_file.transforms[0]
            for idx, jma_node in enumerate(jma_file.nodes):
                bpy.ops.object.mode_set(mode = 'EDIT')

                armature.data.edit_bones.new(jma_node.name)
                armature.data.edit_bones[jma_node.name].tail[2] = 5

                parent_idx = jma_node.parent

                if jms_a_transform:
                    if jma_node.name in jms_a_nodes:
                        node_idx = jms_a_nodes.index(jma_node.name)
                        rest_position = jms_a_file.transforms[0]
                        jms_node = rest_position[node_idx]

                    elif jma_node.name in jms_b_nodes:
                        node_idx = jms_b_nodes.index(jma_node.name)
                        rest_position = jms_b_file.transforms[0]
                        jms_node = rest_position[node_idx]

                    matrix_translate = Matrix.Translation(jms_node.vector)
                    matrix_scale = Matrix.Scale(1, 4, (1, 1, 1))
                    matrix_rotation = jms_node.rotation.to_matrix().to_4x4()
                else:
                    matrix_translate = Matrix.Translation(first_frame[idx].vector)
                    matrix_scale = Matrix.Scale(1, 4, (1, 1, 1))
                    matrix_rotation = first_frame[idx].rotation.to_matrix().to_4x4()

                if not parent_idx == -1 and not parent_idx == None:
                    parent = jma_file.nodes[parent_idx].name
                    if 'thigh' in jma_node.name and not pelvis == None and not thigh0 == None and not thigh1 == None:
                        parent = jma_file.nodes[pelvis].name
                    elif 'clavicle' in jma_node.name and not spine1 == None and not clavicle0 == None and not clavicle1 == None:
                        parent = jma_file.nodes[spine1].name

                    bpy.ops.object.mode_set(mode = 'EDIT')
                    armature.data.edit_bones[jma_node.name].parent = armature.data.edit_bones[parent]

                bpy.ops.object.mode_set(mode = 'POSE')
                pose_bone = armature.pose.bones[jma_node.name]
                transform_matrix = matrix_translate @ matrix_rotation @ matrix_scale
                if jma_file.version < 16394 and pose_bone.parent and not jma_node.name == jms_a_nodes[0] and not jma_node.name == jms_b_nodes[0]:
                    transform_matrix = pose_bone.parent.matrix @ transform_matrix

                armature.pose.bones[jma_node.name].matrix = transform_matrix

            bpy.ops.pose.armature_apply(selected=False)

        else:
            report({'ERROR'}, "No valid armature detected and not enough information to build valid skeleton due to version. Import will now be aborted")
            return {'CANCELLED'}

    scene.frame_end = jma_file.frame_count
    scene.render.fps = jma_file.frame_rate
    bpy.ops.object.mode_set(mode = 'POSE')

    nodes = jma_file.nodes
    if jma_file.version == 16390:
        nodes = global_functions.sort_by_layer(list(armature.data.bones), armature, False)

    for frame_idx, frame in enumerate(jma_file.transforms):
        scene.frame_set(frame_idx + 1)

        if jma_file.biped_controller_frame_type != JMAAsset.BipedControllerFrameType.DISABLE:
            controller_transform = jma_file.biped_controller_transforms[frame_idx]

            if jma_file.biped_controller_frame_type & JMAAsset.BipedControllerFrameType.DX:
                armature.location.x = controller_transform.vector[0]
            if jma_file.biped_controller_frame_type & JMAAsset.BipedControllerFrameType.DY:
                armature.location.y = controller_transform.vector[1]
            if jma_file.biped_controller_frame_type & JMAAsset.BipedControllerFrameType.DZ:
                armature.location.z = controller_transform.vector[2]

            if jma_file.biped_controller_frame_type & JMAAsset.BipedControllerFrameType.DYAW:
                armature.rotation_euler.z = controller_transform.rotation.to_euler().z

            armature.keyframe_insert('location')
            armature.keyframe_insert('rotation_euler')
            view_layer.update()

        for idx, node in enumerate(nodes):
            pose_bone = armature.pose.bones[node.name]

            matrix_scale = Matrix.Scale(frame[idx].scale, 4, (1, 1, 1))
            matrix_rotation = frame[idx].rotation.to_matrix().to_4x4()
            transform_matrix = Matrix.Translation(frame[idx].vector) @ matrix_rotation @ matrix_scale

            if jma_file.version < 16394 and pose_bone.parent:
                transform_matrix = pose_bone.parent.matrix @ transform_matrix

            pose_bone.matrix = transform_matrix
            view_layer.update()
            pose_bone.keyframe_insert('location')
            pose_bone.keyframe_insert('rotation_quaternion')
            pose_bone.keyframe_insert('scale')

    scene.frame_set(1)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    report({'INFO'}, "Import completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.jma()
