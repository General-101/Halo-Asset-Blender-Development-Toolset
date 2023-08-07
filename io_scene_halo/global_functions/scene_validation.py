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

from ..global_functions.global_functions import ParseError
from ..global_functions import resource_management

def validate_halo_jms_scene(game_version, version, blend_scene, object_list, is_jmi):
    node_count = len(blend_scene.node_list)
    root_nodes = resource_management.filter_root_nodes(blend_scene.node_list, is_jmi)

    if len(object_list) == 0:
        raise ParseError("No objects in scene.")

    elif node_count == 0:
        raise ParseError("No nodes in scene. Add an armature or object mesh named frame.")

    elif not is_jmi and len(root_nodes) > 1:
        raise ParseError("More than one root node. Please remove or rename objects until you only have one root frame object.")

    elif blend_scene.mesh_frame_count > 0 and blend_scene.armature_count > 0:
        raise ParseError("Using both armature and object mesh node setup. Choose one or the other.")

    elif game_version == "halo1" and version >= 8201:
        raise ParseError("This version is not supported for Halo CE. Choose from 8197-8200 if you wish to export for Halo CE.")

    elif game_version == "halo2" and version >= 8211:
        raise ParseError("This version is not supported for Halo 2. Choose from 8197-8210 if you wish to export for Halo 2.")

    elif game_version == "halo3" and version > 8213:
        raise ParseError("This version is not supported for Halo 3. Choose from 8197-8213 if you wish to export for Halo 3.")

    elif game_version == "halo1" and len(blend_scene.render_geometry_list + blend_scene.collision_geometry_list + blend_scene.marker_list) == 0:
        raise ParseError("No geometry in scene.")

    elif not game_version == "halo1" and len(blend_scene.render_geometry_list + blend_scene.collision_geometry_list + blend_scene.marker_list + blend_scene.hinge_list + blend_scene.ragdoll_list + blend_scene.point_to_point_list + blend_scene.sphere_list + blend_scene.box_list + blend_scene.capsule_list + blend_scene.convex_shape_list + blend_scene.xref_instances + blend_scene.car_wheel_list + blend_scene.prismatic_list + blend_scene.bounding_sphere_list + blend_scene.skylight_list) == 0:
        raise ParseError("No geometry in scene.")

    elif game_version == "halo1" and node_count > 64:
        raise ParseError("This model has more nodes than Halo CE supports. Please limit your node count to 64 nodes")

    elif game_version == "halo2" and node_count > 255:
        raise ParseError("This model has more nodes than Halo 2 supports. Please limit your node count to 255 nodes")

    elif game_version == "halo3" and node_count > 255:
        raise ParseError("This model has more nodes than Halo 3 supports. Please limit your node count to 255 nodes")

def validate_halo_jma_scene(game_title, jma_version, blend_scene, object_set, extension):
    h2_extension_list = ['.JMRX', '.JMH']
    node_count = len(blend_scene.node_list)

    if len(object_set) == 0:
        raise ParseError("No objects in scene.")

    elif node_count == 0:
        raise ParseError("No nodes in scene. Add an armature.")

    elif game_title == "halo1":
        if jma_version >= 16393:
            raise ParseError("This version is not supported for Halo 1. Choose from 16390-16392 if you wish to export for Halo 1.")

        elif node_count > 64:
            raise ParseError("This model has more nodes than Halo 1 supports. Please limit your node count to 64 nodes")

        elif extension.upper() in h2_extension_list:
            raise ParseError("This extension is not used in Halo 1.")

    elif game_title == "halo2":
        if jma_version >= 16396:
            raise ParseError("This version is not supported for Halo 2. Choose from 16390-16395 if you wish to export for Halo 2.")

        elif node_count > 255:
            raise ParseError("This model has more nodes than Halo 2 supports. Please limit your node count to 255 nodes")

    elif game_title == "halo3":
        if jma_version >= 16396:
            raise ParseError("This version is not supported for Halo 3. Choose from 16390-16395 if you wish to export for Halo 3.")

        elif node_count > 255:
            raise ParseError("This model has more nodes than Halo 3 supports. Please limit your node count to 255 nodes")
