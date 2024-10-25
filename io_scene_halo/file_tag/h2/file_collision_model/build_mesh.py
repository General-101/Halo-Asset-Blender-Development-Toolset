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

import re
import bpy
import bmesh

from ....global_functions import global_functions
from .format import SurfaceFlags

def build_collision(context, armature, COLLISION, game_version):
    node_prefix_tuple = ('b ', 'b_', 'bone ', 'bone_', 'frame ', 'frame_', 'bip01 ', 'bip01_')
    collection = context.collection
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors
    for region_idx, region in enumerate(COLLISION.regions):
        for permutation_idx, permutation in enumerate(region.permutations):
            for bsp_idx, bsp in enumerate(permutation.bsps):
                parent_name = COLLISION.nodes[bsp.node_index].name
                for node_prefix in node_prefix_tuple:
                    if parent_name.lower().startswith(node_prefix):
                        parent_name = re.split(node_prefix, parent_name, maxsplit=1, flags=re.IGNORECASE)[1]

                active_region_permutations = []

                region_name = region.name
                permutation_name = permutation.name

                if region_name == "__unnamed":
                    region_name = "unnamed"

                if permutation_name == "__base":
                    permutation_name = "base"

                object_name = '@%s %s %s' % (region_name, permutation_name, parent_name)
                bm = bmesh.new()

                mesh = bpy.data.meshes.new(object_name)
                object_mesh = bpy.data.objects.new(object_name, mesh)
                collection.objects.link(object_mesh)

                for surface_idx, surface in enumerate(bsp.surfaces):
                    edge_index = surface.first_edge
                    surface_edges = []
                    vert_indices = []
                    while edge_index not in surface_edges:
                        surface_edges.append(edge_index)
                        edge = bsp.edges[edge_index]
                        if edge.left_surface == surface_idx:
                            vert_indices.append(bm.verts.new(bsp.vertices[edge.start_vertex].translation))
                            edge_index = edge.forward_edge

                        else:
                            vert_indices.append(bm.verts.new(bsp.vertices[edge.end_vertex].translation))
                            edge_index = edge.reverse_edge

                    is_invalid = False
                    if SurfaceFlags.invalid in SurfaceFlags(surface.flags):
                        is_invalid = True

                    if not is_invalid and len(vert_indices) >= 3:
                        bm.faces.new(vert_indices)

                bm.faces.ensure_lookup_table()
                for surface_idx, surface in enumerate(bsp.surfaces):
                    is_invalid = False
                    if SurfaceFlags.invalid in SurfaceFlags(surface.flags):
                        is_invalid = True

                    if not is_invalid:
                        ngon_material_index = surface.material
                        if not ngon_material_index == -1:
                            mat = COLLISION.materials[ngon_material_index]

                        current_region_permutation = "%s %s" % (permutation_name, region_name)

                        if not current_region_permutation in active_region_permutations:
                            active_region_permutations.append(current_region_permutation)
                            object_mesh.region_add(current_region_permutation)

                        if not ngon_material_index == -1:
                            material_name = mat.name

                            if SurfaceFlags.two_sided in SurfaceFlags(surface.flags):
                                material_name += "%"

                            if SurfaceFlags.invisible in SurfaceFlags(surface.flags):
                                material_name += "*"

                            if SurfaceFlags.climbable in SurfaceFlags(surface.flags):
                                material_name += "^"

                            if SurfaceFlags.breakable in SurfaceFlags(surface.flags):
                                material_name += "-"

                            if SurfaceFlags.conveyor in SurfaceFlags(surface.flags):
                                material_name += ">"

                            mat = bpy.data.materials.get(material_name)
                            if mat is None:
                                mat = bpy.data.materials.new(name=material_name)

                            if not mat in object_mesh.data.materials.values():
                                object_mesh.data.materials.append(mat)

                            mat.diffuse_color = random_color_gen.next()
                            material_index = object_mesh.data.materials.values().index(mat)
                            bm.faces[surface_idx].material_index = material_index

                        region_layer = bm.faces.layers.int.get('Region Assignment')
                        if region_layer == None:
                            region_layer = bm.faces.layers.int.new('Region Assignment')

                        face = bm.faces[surface_idx]
                        face[region_layer] = active_region_permutations.index(current_region_permutation) + 1

                bm.to_mesh(mesh)
                bm.free()

                object_mesh.parent = armature
                object_mesh.parent_type = "BONE"
                object_mesh.parent_bone = parent_name
                object_mesh.matrix_world = armature.pose.bones[parent_name].matrix
