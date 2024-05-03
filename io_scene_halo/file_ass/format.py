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

from mathutils import Vector
from ..global_functions import global_functions

class ASSAsset(global_functions.HaloAsset):
    def __init__(self, filepath=None):
        if filepath:
            super().__init__(filepath)

        self.version = 0
        self.materials = []
        self.objects = []
        self.instances = []

    class Transform:
        def __init__(self, rotation=(0.0, 0.0, 0.0, 1.0), translation=Vector(), scale=Vector((1.0, 1.0, 1.0))):
            self.rotation = rotation
            self.translation = translation
            self.scale = scale

    class Material:
        def __init__(self, name="", asset_name="", texture_path="", slot=0, lod="", permutation="", region="", material_strings=[]):
            self.name = name
            self.asset_name = asset_name
            self.texture_path = texture_path
            self.slot = slot
            self.lod = lod
            self.permutation = permutation
            self.region = region
            self.material_strings = material_strings

    class Object:
        def __init__(self, geo_class="", xref_filepath="", xref_objectname="", material_index=-1, radius=0.0, extents=Vector(), height=0.0, vertices=[], triangles=[], node_index_list=[], light_properties=None):
            self.geo_class = geo_class
            self.xref_filepath = xref_filepath
            self.xref_objectname = xref_objectname
            self.material_index = material_index
            self.radius = radius
            self.extents = extents
            self.height = height
            self.vertices = vertices
            self.triangles = triangles
            self.node_index_list = node_index_list
            self.light_properties = light_properties

    class Light:
        def __init__(self, light_type="", light_color=Vector(), intensity=0.0, hotspot_size=-1.0, hotspot_falloff_size=-1.0, uses_near_attenuation=0, near_attenuation_start=0.0, near_attenuation_end=0.0, uses_far_attenuation=0, far_attenuation_start=0, far_attenuation_end=0.0, light_shape=0, light_aspect_ratio=0.0):
            self.light_type = light_type
            self.light_color = light_color
            self.intensity = intensity
            self.hotspot_size = hotspot_size
            self.hotspot_falloff_size = hotspot_falloff_size
            self.uses_near_attenuation = uses_near_attenuation
            self.near_attenuation_start = near_attenuation_start
            self.near_attenuation_end = near_attenuation_end
            self.uses_far_attenuation = uses_far_attenuation
            self.far_attenuation_start = far_attenuation_start
            self.far_attenuation_end = far_attenuation_end
            self.light_shape = light_shape
            self.light_aspect_ratio = light_aspect_ratio

    class Vertex:
        def __init__(self, node_influence_count=0, node_set=[], region=-1, translation=Vector(), normal=Vector(), color=Vector(), uv_set=[]):
            self.node_influence_count = node_influence_count
            self.node_set = node_set
            self.region = region
            self.translation = translation
            self.normal = normal
            self.color = color
            self.uv_set = uv_set

    class Triangle:
        def __init__(self, region=-1, material_index=-1, v0=-1, v1=-1, v2=-1):
            self.region = region
            self.material_index = material_index
            self.v0 = v0
            self.v1 = v1
            self.v2 = v2

    class Instance:
        def __init__(self, name="", object_index=-1, unique_id=-1, parent_id=-1, inheritance_flag=0, local_transform=None, pivot_transform=None, bone_groups=None):
            self.name = name
            self.object_index = object_index
            self.unique_id = unique_id
            self.parent_id = parent_id
            self.inheritance_flag = inheritance_flag
            self.local_transform = local_transform
            self.pivot_transform = pivot_transform
            self.bone_groups = bone_groups

    def are_quaternions_inverted(self):
        return self.version < 1

    def next_transform(self):
        rotation = self.next_quaternion()
        translation = self.next_vector()
        scale = float(self.next())

        return ASSAsset.Transform(rotation, translation, scale)

    def next_transform_legacy(self):
        rotation = self.next_quaternion()
        translation = self.next_vector()
        scale = self.next_vector()

        return ASSAsset.Transform(rotation, translation, scale)
