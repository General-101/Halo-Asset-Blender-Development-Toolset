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

from ..global_functions import global_functions

class JMIAsset(global_functions.HaloAsset):
    def __init__(self):
        self.world_nodes = []
        self.children_sets = []

    class JMSArgs:
        def __init__(
            self,

            jmi_version=0,
            folder_type=0,
            hidden_geo=False,
            nonrender_geo=False,

            export_render=False,
            export_collision=False,
            export_physics=False,

            fix_rotations=False,
            use_maya_sorting=False,
            apply_modifiers=False,
            triangulate_faces=False,
            loop_normals=False,
            edge_split=None,
            clean_normalize_weights=False,
            scale_value=0.0,
        ):
            self.jmi_version = jmi_version

            self.folder_type = folder_type
            self.hidden_geo = hidden_geo
            self.nonrender_geo = nonrender_geo

            self.export_render = export_render
            self.export_collision = export_collision
            self.export_physics = export_physics

            self.fix_rotations = fix_rotations
            self.use_maya_sorting = use_maya_sorting
            self.apply_modifiers = apply_modifiers
            self.triangulate_faces = triangulate_faces
            self.loop_normals = loop_normals
            self.edge_split = edge_split
            self.clean_normalize_weights = clean_normalize_weights
            self.scale_value = scale_value
