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

import os
import bpy

from enum import Flag, Enum, auto
from ...file_jma.format import JMAAsset
from ...global_functions import global_functions
from mathutils import Vector, Euler, Quaternion, Matrix
from ...file_tag.tag_interface.tag_definitions import h1, h2
from ...file_tag.tag_interface import tag_interface, tag_common
from ...file_tag.h1.file_model_animations.animation_parser import extract_animation, JMA_RETAIL_NODES

class AnimationTypeEnum(Enum):
    base = 0
    overlay = auto()
    replacement = auto()

class FrameInfoTypeEnum(Enum):
    none = 0
    dx_dy = auto()
    dx_dy_dyaw = auto()
    dx_dy_dz_dyaw = auto()

class AnimationFlags(Flag):
    compressed_data = auto()
    world_relative = auto()
    pal_25hz = auto()

class Nodes:
    def __init__(self, name="", sibling=-1, child=-1, parent=-1, flags=0, base_vector=Vector(), vector_range=0.0, visited=False):
        self.name = name
        self.sibling = sibling
        self.child = child
        self.parent = parent
        self.flags = flags
        self.base_vector = base_vector
        self.vector_range = vector_range
        self.visited = visited

class FrameTransform:
    def __init__(self, rotation=Quaternion(), translation=Vector(), scale=1.0):
        self.rotation = rotation
        self.translation = translation
        self.scale = scale

def build_scene(context, tag_ref, asset_cache, game_title, fix_rotations, empty_markers, report):
    if game_title == "halo1":
        tag_groups = tag_common.h1_tag_groups
    elif game_title == "halo2":
        tag_groups = tag_common.h2_tag_groups
    else:
        print("%s is not supported." % game_title)

    animation_data = tag_interface.get_disk_asset(tag_ref["path"], tag_groups.get(tag_ref["group name"]))["Data"]

    JMA = JMAAsset()
    JMA.version == 16392

    scene = context.scene
    view_layer = context.view_layer

    active_object = context.view_layer.objects.active
    armature = None
    if active_object and active_object.type == 'ARMATURE':
        armature = active_object

    if armature:
        nodes = None
        if len(animation_data["nodes"]) > 0:
            nodes = []
            for node_idx, node in enumerate(animation_data["nodes"]):
                if node_idx == 0:
                    # Captain animation had the parent node on the root node set to something instead of None. Not sure what that is about. - Gen
                    node["parent node"] = -1

                nodes.append(JMA.Node(node["name"], node["parent node"], node["first child node"], node["next sibling node"]))

        if nodes is None:
            asset_cache = {}

            output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h1_merged_output")
            tag_groups = tag_common.h1_tag_groups
            tag_extensions = tag_common.h1_tag_extensions
            engine_tag = tag_interface.EngineTag.H1Latest.value
            merged_defs = h1.generate_defs(tag_common.h1_defs_directory, output_dir)
            tags_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_tag_path
            
            tag_ref = {"group name": "mod2", "path": tag_ref["path"]}
    
            tag_interface.generate_tag_dictionary(game_title, tag_ref, tags_directory, tag_groups, engine_tag, merged_defs, asset_cache)

            gbxmodel_asset = tag_interface.get_disk_asset(tag_ref["path"], tag_groups.get(tag_ref["group name"]))
            if gbxmodel_asset is not None:
                nodes = []
                for node in gbxmodel_asset["Data"]["nodes"]:
                    name = node["name"]
                    sibling = node["next sibling node"]
                    child = node["first child node"]
                    parent = node["parent node"]
                    print(name, parent, child, sibling)
                    nodes.append(JMA.Node(name, parent, child, sibling))

        if nodes is None:
            if len(animation_data["animations"]) > 0:
                first_element = animation_data["animations"][0]
                anim_nodes = JMA_RETAIL_NODES.get((first_element["node count"], first_element["node list checksum"]))
                if anim_nodes is not None:
                    nodes = []
                    for node in anim_nodes:
                        name = node[0]
                        sibling = node[2]
                        child = node[1]
                        parent = node[3]

                        nodes.append(JMA.Node(name, parent, child, sibling))

        if nodes is None:
            game_title = "halo1"
            nodes = []
            sorted_list = global_functions.sort_by_layer(list(armature.data.bones), armature)
            joined_list = sorted_list[0]
            reversed_joined_list = sorted_list[1]

            for node in joined_list:
                is_bone = False
                if armature:
                    is_bone = True

                find_child_node = global_functions.get_child(node, reversed_joined_list, game_title, False)
                find_sibling_node = global_functions.get_sibling(armature, node, reversed_joined_list, game_title, False)

                first_child_node = -1
                first_sibling_node = -1
                parent_node = -1

                if not find_child_node == None:
                    first_child_node = joined_list.index(find_child_node)
                if not find_sibling_node == None:
                    first_sibling_node = joined_list.index(find_sibling_node)
                if not node.parent == None and not node.parent.name.startswith('!'):
                    if armature:
                        if node.parent.use_deform:
                            parent_node = joined_list.index(node.parent)
                    else:
                        parent_node = joined_list.index(node.parent)

                name = node.name
                child = first_child_node
                sibling = first_sibling_node
                parent = parent_node

                current_node_children = []
                children = []
                for child_node in node.children:
                    if child_node in joined_list:
                        current_node_children.append(child_node.name)

                current_node_children.sort()

                if is_bone:
                    for child_node in current_node_children:
                        children.append(joined_list.index(armature.data.bones[child_node]))

                else:
                    for child_node in current_node_children:
                        children.append(joined_list.index(bpy.data.objects[child_node]))

                nodes.append(JMA.Node(name, parent, child, sibling))

        JMA.nodes = nodes
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

        for animation_idx, animation in enumerate(animation_data["animations"]):
            extract_animation(armature, animation_idx, animation, animation_data)
            parsed_frame_data = []
            for frame_idx, frame in enumerate(animation["frames"]):
                parsed_frame = []
                for node in frame:
                    frame_transform = FrameTransform()
                    frame_transform.rotation = Quaternion((node.rot_w, node.rot_i, node.rot_j, node.rot_k))
                    frame_transform.translation = Vector((node.pos_x, node.pos_y, node.pos_z))
                    frame_transform.scale = node.scale
                    parsed_frame.append(frame_transform)
                parsed_frame_data.append(parsed_frame)

            if parsed_frame_data is None or len(parsed_frame_data) == 0:
                continue

            action = bpy.data.actions.get(animation["name"])
            if action is None:
                action = bpy.data.actions.new(name=animation["name"])

            action.use_fake_user = True
            action.use_frame_range = True
            action.frame_start = 1
            action.frame_end = animation["frame count"] + 1

            armature.animation_data_create()
            armature.animation_data.action = action

            global_functions.import_fcurve_data(action, armature, nodes, parsed_frame_data, JMA, fix_rotations, is_inverted)
            if (4, 4, 0) <= bpy.app.version:
                armature.animation_data.action_slot = action.slots[0]
        report({'INFO'}, "Import completed successfully")

    else:
        report({'ERROR'}, "No valid armature is active. Import will now be aborted")
