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

from ..global_functions import global_functions

class JMSAsset(global_functions.HaloAsset):
    def __init__(self, filepath=None):
        if filepath:
            super().__init__(filepath)

        self.version = 0
        self.game_version = "haloce"
        self.node_checksum = 0
        self.nodes = []
        self.transforms = []
        self.materials = []
        self.markers = []
        self.xref_instances = []
        self.xref_markers = []
        self.regions = []
        self.active_regions = []
        self.geometry_list = []
        self.original_geometry_list = []
        self.triangles = []
        self.vertices = []
        self.spheres = []
        self.boxes = []
        self.capsules = []
        self.convex_shapes = []
        self.ragdolls = []
        self.hinges = []
        self.car_wheels = []
        self.point_to_points = []
        self.prismatics = []
        self.bounding_spheres = []
        self.skylights = []

    class Node:
        def __init__(self, name, children=None, child=-1, sibling=-1, parent=-1):
            self.name = name
            self.children = children
            self.child = child
            self.sibling = sibling
            self.parent = parent
            self.visited = False

    class Transform:
        def __init__(self, translation, rotation):
            self.translation = translation
            self.rotation = rotation

    class Material:
        def __init__(self, name, texture_path=None, slot=None, lod=None, permutation=None, region=None):
            self.name = name
            self.texture_path = texture_path
            self.slot = slot
            self.lod = lod
            self.permutation = permutation
            self.region = region

    class Marker:
        def __init__(self, name, region=-1, parent=-1, rotation=None, translation=None, radius=0.0):
            self.name = name
            self.region = region
            self.parent = parent
            self.rotation = rotation
            self.translation = translation
            self.radius = radius

    class XREF:
        def __init__(self, path, name):
            self.path = path
            self.name = name

    class XREF_Marker:
        def __init__(self, name, unique_identifier=-1, index=-1, rotation=None, translation=None):
            self.name = name
            self.unique_identifier = unique_identifier
            self.index = index
            self.rotation = rotation
            self.translation = translation

    class Region:
        def __init__(self, name):
            self.name = name

    class Vertex:
        def __init__(self, node_influence_count=0, node_set=None, region=-1, translation=None, normal=None, color=None, uv_set=None):
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

    class Sphere:
        def __init__(self, name, parent_index=-1, material_index=-1, rotation=None, translation=None, radius=0.0):
            self.name = name
            self.parent_index = parent_index
            self.material_index = material_index
            self.rotation = rotation
            self.translation = translation
            self.radius = radius

    class Box:
        def __init__(self, name, parent_index=-1, material_index=-1, rotation=None, translation=None, width=0.0, length=0.0, height=0.0):
            self.name = name
            self.parent_index = parent_index
            self.material_index = material_index
            self.rotation = rotation
            self.translation = translation
            self.width = width
            self.length = length
            self.height = height

    class Capsule:
        def __init__(self, name, parent_index=-1, material_index=-1, rotation=None, translation=None, height=0.0, radius=0.0):
            self.name = name
            self.parent_index = parent_index
            self.material_index = material_index
            self.rotation = rotation
            self.translation = translation
            self.height = height
            self.radius = radius

    class Convex_Shape:
        def __init__(self, name, parent_index=-1, material_index=-1, rotation=None, translation=None, verts=None):
            self.name = name
            self.parent_index = parent_index
            self.material_index = material_index
            self.rotation = rotation
            self.translation = translation
            self.verts = verts

    class Ragdoll:
        def __init__(self, name, attached_index=-1, referenced_index=-1, attached_rotation=None, attached_translation=None, referenced_rotation=None, referenced_translation=None, min_twist=0.0, max_twist=0.0, min_cone=0.0, max_cone=0.0, min_plane=0.0, max_plane=0.0, friction_limit=0.0):
            self.name = name
            self.attached_index = attached_index
            self.referenced_index = referenced_index
            self.attached_rotation = attached_rotation
            self.attached_translation = attached_translation
            self.referenced_rotation = referenced_rotation
            self.referenced_translation = referenced_translation
            self.min_twist = min_twist
            self.max_twist = max_twist
            self.min_cone = min_cone
            self.max_cone = max_cone
            self.min_plane = min_plane
            self.max_plane = max_plane
            self.friction_limit = friction_limit

    class Hinge:
        def __init__(self, name, body_a_index=-1, body_b_index=-1, body_a_rotation=None, body_a_translation=None, body_b_rotation=None, body_b_translation=None, is_limited=0, friction_limit=0.0, min_angle=0.0, max_angle=0.0):
            self.name = name
            self.body_a_index = body_a_index
            self.body_b_index = body_b_index
            self.body_a_rotation = body_a_rotation
            self.body_a_translation = body_a_translation
            self.body_b_rotation = body_b_rotation
            self.body_b_translation = body_b_translation
            self.is_limited = is_limited
            self.friction_limit = friction_limit
            self.min_angle = min_angle
            self.max_angle = max_angle

    class Car_Wheel:
        def __init__(self, name, chassis_index=-1, wheel_index=-1, chassis_rotation=None, chassis_translation=None, wheel_rotation=None, wheel_translation=None, suspension_rotation=None, suspension_translation=None, suspension_min_limit=0.0, suspension_max_limit=0.0, friction_limit=0.0, velocity=0.0, gain=0.0):
            self.name = name
            self.chassis_index = chassis_index
            self.wheel_index = wheel_index
            self.chassis_rotation = chassis_rotation
            self.chassis_translation = chassis_translation
            self.wheel_rotation = wheel_rotation
            self.wheel_translation = wheel_translation
            self.suspension_rotation = suspension_rotation
            self.suspension_translation = suspension_translation
            self.suspension_min_limit = suspension_min_limit
            self.suspension_max_limit = suspension_max_limit
            self.friction_limit = friction_limit
            self.velocity = velocity
            self.gain = gain

    class Point_to_Point:
        def __init__(self, name, body_a_index=-1, body_b_index=-1, body_a_rotation=None, body_a_translation=None, body_b_rotation=None, body_b_translation=None, constraint_type=0, x_min_limit=0.0, x_max_limit=0.0, y_min_limit=0.0, y_max_limit=0.0, z_min_limit=0.0, z_max_limit=0.0, spring_length=0.0):
            self.name = name
            self.body_a_index = body_a_index
            self.body_b_index = body_b_index
            self.body_a_rotation = body_a_rotation
            self.body_a_translation = body_a_translation
            self.body_b_rotation = body_b_rotation
            self.body_b_translation = body_b_translation
            self.constraint_type = constraint_type
            self.x_min_limit = x_min_limit
            self.x_max_limit = x_max_limit
            self.y_min_limit = y_min_limit
            self.y_max_limit = y_max_limit
            self.z_min_limit = z_min_limit
            self.z_max_limit = z_max_limit
            self.spring_length = spring_length

    class Prismatic:
        def __init__(self, name, body_a_index=-1, body_b_index=-1, body_a_rotation=None, body_a_translation=None, body_b_rotation=None, body_b_translation=None, is_limited=0, suspension_max_limit=0.0, friction_limit=0.0, min_limit=0.0, max_limit=0.0):
            self.name = name
            self.body_a_index = body_a_index
            self.body_b_index = body_b_index
            self.body_a_rotation = body_a_rotation
            self.body_a_translation = body_a_translation
            self.body_b_rotation = body_b_rotation
            self.body_b_translation = body_b_translation
            self.is_limited = is_limited
            self.friction_limit = friction_limit
            self.min_limit = min_limit
            self.max_limit = max_limit

    class Bounding_Sphere:
        def __init__(self, translation=None, radius=0.0):
            self.translation = translation
            self.radius = radius

    class Skylight:
        def __init__(self, direction=None, radiant_intensity=None, solid_angle=0.0):
            self.direction = direction
            self.radiant_intensity = radiant_intensity
            self.solid_angle = solid_angle

    def are_quaternions_inverted(self):
        return self.version < 8205

    def next_transform(self):
        rotation = self.next_quaternion()
        translation = self.next_vector()

        return JMSAsset.Transform(translation, rotation)
