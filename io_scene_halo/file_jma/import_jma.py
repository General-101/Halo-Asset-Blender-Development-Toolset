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

from os import path
from enum import Flag, auto
from mathutils import Matrix
from ..file_jms import import_jms
from ..global_functions import mesh_processing, global_functions

class ParentIDFix():
    def __init__(self, pelvis = None, thigh0 = None, thigh1 = None, spine1 = None, clavicle0 = None, clavicle1 = None):
        self.pelvis = pelvis
        self.thigh0 = thigh0
        self.thigh1 = thigh1
        self.spine1 = spine1
        self.clavicle0 = clavicle0
        self.clavicle1 = clavicle1

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

    def __init__(self, filepath, game_version, report):
        super().__init__(filepath)
        extension = global_functions.get_true_extension(filepath, None, True)
        self.broken_skeleton = False
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
                    report({'WARNING'}, "Malformed node graph (bad parent index)")
                    self.broken_skeleton = True
                    break

                parent_node = self.nodes[node.parent]
                if parent_node.child:
                    node.sibling = parent_node.child

                else:
                    node.sibling = -1

                if node.sibling >= len(self.nodes):
                    report({'WARNING'}, "Malformed node graph (sibling index out of range)")
                    self.broken_skeleton = True
                    break

                parent_node.child = node_idx

        elif self.version >= 16392:
            for node_idx in range(node_count):
                node = self.nodes[node_idx]
                if node.child == -1:
                    continue # no child nodes, nothing to update

                if node.child >= len(self.nodes) or node.child == node_idx:
                    report({'WARNING'}, "Malformed node graph (bad child index)")
                    self.broken_skeleton = True
                    break

                child_node = self.nodes[node.child]
                while child_node != None:
                    child_node.parent = node_idx
                    if child_node.visited:
                        report({'WARNING'}, "Malformed node graph (circular reference)")
                        self.broken_skeleton = True
                        break

                    child_node.visited = True
                    if child_node.sibling >= len(self.nodes):
                        report({'WARNING'}, "Malformed node graph (sibling index out of range)")
                        self.broken_skeleton = True
                        break

                    if child_node.sibling != -1:
                        child_node = self.nodes[child_node.sibling]

                    else:
                        child_node = None

def generate_jms_skeleton(jms_a_transform, jms_a_nodes, jms_a_file, jms_b_transform, jms_b_nodes, jms_b_file, jma_file, armature):
    created_bone_list = []
    file_version = jma_file.version
    r_hand_idx = None
    file_type = "JMS"

    bpy.ops.object.mode_set(mode = 'EDIT')
    for idx, jma_node in enumerate(jma_file.nodes):
        created_bone_list.append(jma_node.name)
        current_bone = armature.data.edit_bones.new(jma_node.name)
        if "r_hand" in jma_node.name.lower() or "r hand" in jma_node.name.lower():
            r_hand_idx = idx

        current_bone.tail[2] = 5

        parent = None
        parent_name = None
        for a_idx, jms_a_node in enumerate(jms_a_nodes):
            if jma_node.name.lower() in jms_a_node.lower():
                file_version = jms_a_file.version
                parent_idx = jms_a_file.nodes[a_idx].parent
                parent_name = jms_a_file.nodes[parent_idx].name
                rest_position = jms_a_file.transforms[0]
                jms_node = rest_position[a_idx]

        for b_idx, jms_b_node in enumerate(jms_b_nodes):
            if jma_node.name.lower() in jms_b_node.lower():
                file_version = jms_b_file.version
                parent_idx = jms_b_file.nodes[b_idx].parent
                parent_name = jms_b_file.nodes[parent_idx].name
                rest_position = jms_b_file.transforms[0]
                jms_node = rest_position[b_idx]

        for bone_idx, bone in enumerate(created_bone_list):
            if bone in parent_name:
                parent = armature.data.edit_bones[bone_idx]

        matrix_translate = Matrix.Translation(jms_node.vector)
        matrix_rotation = jms_node.rotation.to_matrix().to_4x4()

        if not parent == None:
            current_bone.parent = parent

        elif "gun" in jma_node.name:
            current_bone.parent = armature.data.edit_bones[r_hand_idx]

        transform_matrix = matrix_translate @ matrix_rotation

        is_root = False
        if jma_node.name.lower() in jms_a_file.nodes[0].name.lower():
            is_root = True

        if jma_node.name.lower() in jms_b_file.nodes[0].name.lower():
            is_root = True

        if file_version < global_functions.get_version_matrix_check(file_type) and current_bone.parent and not is_root:
            transform_matrix = current_bone.parent.matrix @ transform_matrix

        current_bone.matrix = transform_matrix

def generate_jma_skeleton(jms_a_transform, jms_a_nodes, jms_a_file, jms_b_transform, jms_b_nodes, jms_b_file, jma_file, armature, parent_id_class):
    file_version = jma_file.version
    first_frame = jma_file.transforms[0]
    file_type = "JMA"
    if jms_a_transform:
        file_type = "JMS"

    bpy.ops.object.mode_set(mode = 'EDIT')
    for idx, jma_node in enumerate(jma_file.nodes):
        current_bone = armature.data.edit_bones.new(jma_node.name)
        current_bone.tail[2] = 5
        parent_idx = jma_node.parent

        if not parent_idx == -1 and not parent_idx == None:
            if 'thigh' in jma_node.name and not parent_id_class.pelvis == None and not parent_id_class.thigh0 == None and not parent_id_class.thigh1 == None:
                parent_idx = parent_id_class.pelvis

            elif 'clavicle' in jma_node.name and not parent_id_class.spine1 == None and not parent_id_class.clavicle0 == None and not parent_id_class.clavicle1 == None:
                parent_idx = parent_id_class.spine1

            parent = jma_file.nodes[parent_idx].name
            current_bone.parent = armature.data.edit_bones[parent]

        if jms_a_transform:
            for a_idx, jms_a_node in enumerate(jms_a_nodes):
                if jma_node.name.lower() in jms_a_node.lower():
                    file_version = jms_a_file.version
                    rest_position = jms_a_file.transforms[0]
                    jms_node = rest_position[a_idx]

            for b_idx, jms_b_node in enumerate(jms_b_nodes):
                if jma_node.name.lower() in jms_b_node.lower():
                    file_version = jms_b_file.version
                    rest_position = jms_b_file.transforms[0]
                    jms_node = rest_position[b_idx]

            matrix_translate = Matrix.Translation(jms_node.vector)
            matrix_rotation = jms_node.rotation.to_matrix().to_4x4()

        else:
            matrix_translate = Matrix.Translation(first_frame[idx].vector)
            matrix_rotation = first_frame[idx].rotation.to_matrix().to_4x4()

        is_root = False
        if jms_a_transform:
            if jma_node.name.lower() in jms_a_file.nodes[0].name.lower():
                is_root = True

        if jms_b_transform:
            if jma_node.name.lower() in jms_b_file.nodes[0].name.lower():
                is_root = True

        transform_matrix = matrix_translate @ matrix_rotation
        if file_version < global_functions.get_version_matrix_check(file_type) and current_bone.parent and not is_root:
            transform_matrix = current_bone.parent.matrix @ transform_matrix

        current_bone.matrix = transform_matrix

    bpy.ops.object.mode_set(mode = 'OBJECT')

def set_parent_id_class(jma_file, parent_id_class):
    for idx, jma_node in enumerate(jma_file.nodes):
        if 'pelvis' in jma_node.name:
            parent_id_class.pelvis = idx

        if 'thigh' in jma_node.name:
            if parent_id_class.thigh0 == None:
                parent_id_class.thigh0 = idx

            else:
                parent_id_class.thigh1 = idx

        elif 'spine1' in jma_node.name:
            parent_id_class.spine1 = idx

        elif 'clavicle' in jma_node.name:
            if parent_id_class.clavicle0 == None:
                parent_id_class.clavicle0 = idx

            else:
                parent_id_class.clavicle1 = idx

def jms_file_check(jms_a_transform, jms_b_transform, jms_a_file, jms_b_file, jma_nodes):
    jms_a_nodes = []
    jms_b_nodes = []
    warning = "No valid armature detected. One will be created but expect issues with visuals in scene due to no proper rest position"
    if jms_a_transform and not jms_b_transform:
        for jms_node in jms_a_file.nodes:
            jms_a_nodes.append(jms_node.name)

        for jms_node_name in jms_a_nodes:
            if not jms_node_name in jma_nodes:
                jms_a_transform = False
                warning = "Node '%s' from JMS skeleton not found in JMA skeleton." % jms_node_name

        warning = "No valid armature detected. One will be created and the referenced JMS will be used for the rest position"

    elif jms_a_transform and jms_b_transform:
        for jms_node in jms_a_file.nodes:
            jms_a_nodes.append(jms_node.name)

        for jms_node in jms_b_file.nodes:
            jms_b_nodes.append(jms_node.name)

        jms_nodes = jms_a_nodes + jms_b_nodes

        for jms_node_name in jms_nodes:
            if not jms_node_name in jma_nodes:
                jms_a_transform = False
                warning = "Node '%s' from JMS skeleton not found in JMA skeleton." % jms_node_name

        warning = "No valid armature detected. One will be created and the referenced JMS files will be used for the rest position"

    return jms_a_nodes, jms_b_nodes, warning

def load_file(context, filepath, report, fix_parents, game_version, jms_path_a, jms_path_b):
    jms_a_transform = False
    jms_a_file = None
    jms_b_transform = False
    jms_b_file = None

    jma_file = JMAAsset(filepath, game_version, report)
    if path.exists(bpy.path.abspath(jms_path_a)):
        jms_a_transform = True
        jms_a_file = import_jms.JMSAsset(bpy.path.abspath(jms_path_a), "auto")

    if path.exists(bpy.path.abspath(jms_path_a)) and path.exists(bpy.path.abspath(jms_path_b)):
        jms_b_transform = True
        jms_b_file = import_jms.JMSAsset(bpy.path.abspath(jms_path_b), "auto")

    collection = context.collection
    scene = context.scene
    view_layer = context.view_layer
    armature = None
    object_list = list(scene.objects)

    scene_nodes = []
    jma_nodes = []
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
                    mesh_processing.select_object(context, armature)

    for jma_node in jma_file.nodes:
        jma_nodes.append(jma_node.name)

    if len(scene_nodes) > 0:
        for jma_node in jma_nodes:
            if not jma_node in scene_nodes:
                report({'WARNING'}, "Node '%s' not found in an existing armature" % jma_node)

    if armature == None:
        parent_id_class = ParentIDFix()
        jms_a_nodes, jms_b_nodes, warning = jms_file_check(jms_a_transform, jms_b_transform, jms_a_file, jms_b_file, jma_nodes)
        report({'WARNING'}, warning)
        if not jma_file.broken_skeleton:
            if jma_file.version >= 16392:
                armdata = bpy.data.armatures.new('Armature')
                armature = bpy.data.objects.new('Armature', armdata)
                collection.objects.link(armature)
                mesh_processing.select_object(context, armature)
                if fix_parents:
                    if game_version == 'halo2' or game_version == 'halo3':
                        set_parent_id_class(jma_file, parent_id_class)

                generate_jma_skeleton(jms_a_transform, jms_a_nodes, jms_a_file, jms_b_transform, jms_b_nodes, jms_b_file, jma_file, armature, parent_id_class)

            else:
                report({'ERROR'}, "No valid armature detected and not enough information to build valid skeleton due to version. Import will now be aborted")
                return {'CANCELLED'}

        else:
            if jms_a_transform:
                if jma_file.version >= 16392:
                    armdata = bpy.data.armatures.new('Armature')
                    armature = bpy.data.objects.new('Armature', armdata)
                    collection.objects.link(armature)
                    mesh_processing.select_object(context, armature)

                    generate_jms_skeleton(jms_a_transform, jms_a_nodes, jms_a_file, jms_b_transform, jms_b_nodes, jms_b_file, jma_file, armature)

                else:
                    report({'ERROR'}, "No valid armature detected and not enough information to build valid skeleton due to version. Import will now be aborted")
                    return {'CANCELLED'}

            else:
                report({'ERROR'}, "No valid armature detected and animation graph is invalid. Import will now be aborted")
                return {'CANCELLED'}

    scene.frame_end = jma_file.frame_count
    scene.render.fps = jma_file.frame_rate
    bpy.ops.object.mode_set(mode = 'POSE')

    nodes = jma_file.nodes
    if jma_file.version == 16390:
        nodes = global_functions.sort_by_layer(list(armature.data.bones), armature)[0]

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

            view_layer.update()
            armature.keyframe_insert('location')
            armature.keyframe_insert('rotation_euler')

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
