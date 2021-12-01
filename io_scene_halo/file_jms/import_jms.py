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

from io import TextIOWrapper
import bpy
import bmesh

from math import radians
from mathutils import Vector, Matrix, Euler
from ..global_functions import mesh_processing, global_functions

class JMSAsset(global_functions.HaloAsset):
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

    class Material:
        def __init__(self, scene_name, texture_path=None, slot=None, lod=None, permutation=None, region=None):
            self.scene_name = scene_name
            self.texture_path = texture_path
            self.slot = slot
            self.lod = lod
            self.permutation = permutation
            self.region = region

    class Marker:
        def __init__(self, name, region=-1, parent=-1, rotation=None, translation=None, scale=0.0):
            self.name = name
            self.region = region
            self.parent = parent
            self.rotation = rotation
            self.translation = translation
            self.scale = scale

    class XREF_Path:
        def __init__(self, path=None, name=None):
            self.path = path
            self.name = name

    class XREF_Instance_Marker:
        def __init__(self, name, path_index=-1, unique_identifier=-1, rotation=None, translation=None):
            self.name = name
            self.path_index = path_index
            self.unique_identifier = unique_identifier
            self.rotation = rotation
            self.translation = translation

    class Region:
        def __init__(self, name):
            self.name = name

    class Vertex:
        def __init__(self,
                     node_influence_count=0,
                     node_set=None, region=-1,
                     translation=None,
                     normal=None,
                     color=None,
                     uv_set=None
                     ):

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
        def __init__(self,
                     name,
                     attached_index=-1,
                     referenced_index=-1,
                     attached_rotation=None,
                     attached_translation=None,
                     referenced_rotation=None,
                     referenced_translation=None,
                     min_twist=0.0,
                     max_twist=0.0,
                     min_cone=0.0,
                     max_cone=0.0,
                     min_plane=0.0,
                     max_plane=0.0,
                     friction_limit=0.0
                     ):

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
        def __init__(self, name, chassis_index=-1, wheel_index=-1, wheel_rotation=None, wheel_translation=None, suspension_rotation=None, suspension_translation=None, suspension_min_limit=0.0, suspension_max_limit=0.0, friction_limit=0.0, velocity=0.0, gain=0.0):
            self.name = name
            self.chassis_index = chassis_index
            self.wheel_index = wheel_index
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

        return JMSAsset.Transform(translation, rotation, None)

    def __init__(self, filepath, game_version):
        super().__init__(filepath)
        default_region = mesh_processing.get_default_region_permutation_name(game_version)
        default_permutation = mesh_processing.get_default_region_permutation_name(game_version)
        if not isinstance(filepath, TextIOWrapper):
            extension = global_functions.get_true_extension(filepath, None, True)
        else:
            extension = "JMS"
        self.version = int(self.next())
        self.game_version = game_version
        if game_version == 'auto':
            self.game_version = global_functions.get_game_version(self.version, 'JMS')

        version_list = (8197,
                        8198,
                        8199,
                        8200,
                        8201,
                        8202,
                        8203,
                        8204,
                        8205,
                        8206,
                        8207,
                        8208,
                        8209,
                        8210,
                        8211,
                        8212,
                        8213
                        )

        if not self.version in version_list:
            raise global_functions.AssetParseError("Importer does not support this " + extension + " version")

        if self.version < 8205:
            self.skip(1) # skip the node checksum

        node_count = int(self.next())
        self.nodes = []
        transforms_for_frame = []
        self.transforms = []
        self.materials = []
        self.markers = []
        self.xref_paths = []
        self.xref_instance_markers = []
        self.used_regions = []
        self.regions = []
        self.vertices = []
        self.triangles = []
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
        if self.version >= 8205:
            for _ in range(node_count):
                name = self.next()
                parent = int(self.next())
                self.nodes.append(JMSAsset.Node(name, parent=parent))
                transforms_for_frame.append(self.next_transform())

        else:
            for _ in range(node_count):
                name = self.next()
                child = int(self.next())
                sibling = int(self.next())
                self.nodes.append(JMSAsset.Node(name, child=child, sibling=sibling))
                transforms_for_frame.append(self.next_transform())

        self.transforms.append(transforms_for_frame)
        material_count = int(self.next())
        for material in range(material_count):
            name = self.next()
            if self.version >= 8203 and self.version <= 8204:
                texture_definition = self.next()

            material_definition = self.next()
            if self.game_version == 'haloce':
                self.materials.append(JMSAsset.Material(name, material_definition, None, None, None, None))

            elif self.game_version == 'halo2' or self.game_version == 'halo3':
                material_definition_items = material_definition.split()
                lod, permutation, region = global_functions.material_definition_parser(True, material_definition_items, default_region, default_permutation)

                self.materials.append(JMSAsset.Material(name, None, material, lod, permutation, region))

        marker_count = int(self.next())
        for marker in range(marker_count):
            name = self.next()
            region = -1
            if self.version >= 8198 and self.version < 8205:
                region = int(self.next())

            parent = int(self.next())
            rotation = self.next_quaternion()
            translation = self.next_vector()
            scale = 1
            if self.version >= 8200:
                scale = float(self.next())

            self.markers.append(JMSAsset.Marker(name, region, parent, rotation, translation, scale))

        if self.version >= 8201:
            xref_path_count = int(self.next())
            for xref in range(xref_path_count):
                xref_path = self.next()
                xref_name = None
                if self.version >= 8208:
                    xref_name = self.next()

                self.xref_paths.append(JMSAsset.XREF_Path(xref_path, xref_name))

            instance_markers_count = int(self.next())
            for xref in range(instance_markers_count):
                name = self.next()
                unique_identifier = None
                if self.version >= 8203:
                    unique_identifier = int(self.next())

                path_index = int(self.next())
                rotation = self.next_quaternion()
                translation = self.next_vector()
                self.xref_instance_markers.append(JMSAsset.XREF_Instance_Marker(name, path_index, unique_identifier, rotation, translation))

        if self.version < 8205:
            region_count = int(self.next())
            for region in range(region_count):
                name = self.next()
                if name == "__unnamed":
                    name = "unnamed"

                self.regions.append(JMSAsset.Region(name))

        vertex_count = int(self.next())
        for vertex in range(vertex_count):
            node_set = []
            uv_set = []
            region = None
            color = None
            if self.version >= 8205:
                translation = self.next_vector()
                normal = self.next_vector()
                node_influence_count = int(self.next())
                for node in range(node_influence_count):
                    node_index = int(self.next())
                    node_weight = float(self.next())
                    node_set.append([node_index, node_weight])

                uv_count = int(self.next())
                for uv in range(uv_count):
                    tex_u_value   = self.next()
                    tex_v_value   = self.next()
                    try:
                        tex_u = float(tex_u_value)

                    except ValueError:
                        tex_u = float(tex_u_value.rsplit('.', 1)[0])

                    try:
                        tex_v = float(tex_v_value)

                    except ValueError:
                        tex_v = float(tex_v_value.rsplit('.', 1)[0])

                    u = tex_u
                    v = tex_v
                    uv_set.append([u, v])
                if self.version >= 8211:
                    color = self.next_vector()

            else:
                node_influence_count = 0
                if self.version == 8197:
                    region = int(self.next())
                    self.used_regions.append(region)

                node_0_index = int(self.next())
                if self.version == 8204:
                    node_0_weight = float(self.next())

                translation = self.next_vector()
                normal = self.next_vector()
                node_1_index = int(self.next())
                node_1_weight = float(self.next())
                node_2_index = -1
                node_3_index = -1
                if self.version == 8204:
                    node_2_index = int(self.next())
                    node_2_weight = float(self.next())
                    node_3_index = int(self.next())
                    node_3_weight = float(self.next())

                if self.version >= 8204:
                    node_set.append([node_0_index, node_0_weight])

                else:
                    node_set.append([node_0_index, 1])

                node_set.append([node_1_index, node_1_weight])
                if self.version >= 8204:
                    node_set.append([node_2_index, node_2_weight])
                    node_set.append([node_3_index, node_3_weight])

                if not node_0_index == -1:
                    node_influence_count += 1

                if not node_1_index == -1:
                    node_influence_count += 1

                if not node_2_index == -1:
                    node_influence_count += 1

                if not node_3_index == -1:
                    node_influence_count += 1

                if self.version >= 8205:
                    uv_count = int(self.next())
                    for uv in range(uv_count):
                        tex_u_value   = self.next()
                        tex_v_value   = self.next()
                        try:
                            tex_u = float(tex_u_value)

                        except ValueError:
                            tex_u = float(tex_u_value.rsplit('.', 1)[0])

                        try:
                            tex_v = float(tex_v_value)

                        except ValueError:
                            tex_v = float(tex_v_value.rsplit('.', 1)[0])

                        u = tex_u
                        v = tex_v
                        uv_set.append([u, v])

                else:
                    tex_0_u_value = self.next()
                    tex_0_v_value = self.next()
                    if self.version >= 8203:
                        tex_1_u_value = self.next()
                        tex_1_v_value = self.next()
                        tex_2_u_value = self.next()
                        tex_2_v_value = self.next()
                        tex_3_u_value = self.next()
                        tex_3_v_value = self.next()

                    try:
                        tex_0_u = float(tex_0_u_value)

                    except ValueError:
                        tex_0_u = float(tex_0_u_value.rsplit('.', 1)[0])

                    try:
                        tex_0_v = float(tex_0_v_value)

                    except ValueError:
                        tex_0_v = float(tex_0_v_value.rsplit('.', 1)[0])

                    if self.version >= 8203:
                        try:
                            tex_1_u = float(tex_1_u_value)

                        except ValueError:
                            tex_1_u = float(tex_1_u_value.rsplit('.', 1)[0])

                        try:
                            tex_1_v = float(tex_1_v_value)

                        except ValueError:
                            tex_1_v = float(tex_1_v_value.rsplit('.', 1)[0])

                        try:
                            tex_2_u = float(tex_2_u_value)

                        except ValueError:
                            tex_2_u = float(tex_2_u_value.rsplit('.', 1)[0])

                        try:
                            tex_2_v = float(tex_2_v_value)

                        except ValueError:
                            tex_2_v = float(tex_2_v_value.rsplit('.', 1)[0])

                        try:
                            tex_3_u = float(tex_3_u_value)

                        except ValueError:
                            tex_3_u = float(tex_3_u_value.rsplit('.', 1)[0])

                        try:
                            tex_3_v = float(tex_3_v_value)

                        except ValueError:
                            tex_3_v = float(tex_3_v_value.rsplit('.', 1)[0])

                    if self.version >= 8203:
                        uv_set.append([tex_0_u, tex_0_v])
                        uv_set.append([tex_1_u, tex_1_v])
                        uv_set.append([tex_2_u, tex_2_v])
                        uv_set.append([tex_3_u, tex_3_v])

                    else:
                        uv_set.append([tex_0_u, tex_0_v])

                flags = None
                if self.version >= 8199:
                    flags = self.skip(1) #Unused int or boolean value. Don't know which but definitely not a float

            self.vertices.append(JMSAsset.Vertex(node_influence_count, node_set, region, translation, normal, color, uv_set))

        triangle_count = int(self.next())
        for triangle in range(triangle_count):
            region = None
            if self.version >= 8198 and self.version < 8205:
                region = int(self.next())
                self.used_regions.append(region)

            material_index = int(self.next())
            v0 = int(self.next())
            v1 = int(self.next())
            v2 = int(self.next())
            self.triangles.append(JMSAsset.Triangle(region, material_index, v0, v1, v2))

        if self.version >= 8206:
            sphere_count = int(self.next())
            for sphere in range(sphere_count):
                name = self.next()
                parent_index = int(self.next())
                material_index = None
                if self.version >= 8207:
                    material_index = int(self.next())

                rotation = self.next_quaternion()
                translation = self.next_vector()
                radius = float(self.next())
                self.spheres.append(JMSAsset.Sphere(name, parent_index, material_index, rotation, translation, radius))

            boxes_count = int(self.next())
            for box in range(boxes_count):
                name = self.next()
                parent_index = int(self.next())
                material_index = None
                if self.version >= 8207:
                    material_index = int(self.next())

                rotation = self.next_quaternion()
                translation = self.next_vector()
                width = float(self.next())
                length = float(self.next())
                height = float(self.next())
                self.boxes.append(JMSAsset.Box(name, parent_index, material_index, rotation, translation, width, length, height))

            capsules_count = int(self.next())
            for capsules in range(capsules_count):
                name = self.next()
                parent_index = int(self.next())
                material_index = None
                if self.version >= 8207:
                    material_index = int(self.next())

                rotation = self.next_quaternion()
                translation = self.next_vector()
                height = float(self.next())
                radius = float(self.next())
                self.capsules.append(JMSAsset.Capsule(name, parent_index, material_index, rotation, translation, height, radius))

            convex_shape_count = int(self.next())
            for convex_shape in range(convex_shape_count):
                vert = []
                name = self.next()
                parent_index = int(self.next())
                material_index = None
                if self.version >= 8207:
                    material_index = int(self.next())

                rotation = self.next_quaternion()
                translation = self.next_vector()
                vertex_count = int(self.next())
                for vertex in range(vertex_count):
                    vert.append(self.next_vector())

                self.convex_shapes.append(JMSAsset.Convex_Shape(name, parent_index, material_index, rotation, translation, vert))

            ragdoll_count  = int(self.next())
            for ragdoll in range(ragdoll_count):
                name = self.next()
                attached_index = int(self.next())
                referenced_index = int(self.next())
                attached_rotation = self.next_quaternion()
                attached_translation = self.next_vector()
                referenced_rotation = self.next_quaternion()
                referenced_translation = self.next_vector()
                min_twist = float(self.next())
                max_twist = float(self.next())
                min_cone = float(self.next())
                max_cone = float(self.next())
                min_plane = float(self.next())
                max_plane = float(self.next())
                friction_limit = 0.0
                if self.version >= 8213:
                    friction_limit = float(self.next())

                self.ragdolls.append(JMSAsset.Ragdoll(name, attached_index, referenced_index, attached_rotation, attached_translation, referenced_rotation, referenced_translation, min_twist, max_twist, min_cone, max_cone, min_plane, max_plane, friction_limit))

            hinge_count  = int(self.next())
            for hinge in range(hinge_count):
                name = self.next()
                body_a_index = int(self.next())
                body_b_index = int(self.next())
                body_a_rotation = self.next_quaternion()
                body_a_translation = self.next_vector()
                body_b_rotation = self.next_quaternion()
                body_b_translation = self.next_vector()
                is_limited = int(self.next())
                friction_limit = float(self.next())
                min_angle = float(self.next())
                max_angle = float(self.next())

                self.hinges.append(JMSAsset.Hinge(name, body_a_index, body_b_index, body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, is_limited, friction_limit, min_angle, max_angle))

        if self.version >= 8210:
            car_wheel_count  = int(self.next())
            for car_wheel in range(car_wheel_count):
                name = self.next()
                chassis_index = int(self.next())
                wheel_index = int(self.next())
                wheel_rotation = self.next_quaternion()
                wheel_translation = self.next_vector()
                suspension_rotation = self.next_quaternion()
                suspension_translation = self.next_vector()
                suspension_min_limit = float(self.next())
                suspension_max_limit = float(self.next())
                friction_limit = float(self.next())
                velocity = float(self.next())
                gain = float(self.next())

                self.car_wheels.append(JMSAsset.Car_Wheel(name, chassis_index, wheel_index, wheel_rotation, wheel_translation, suspension_rotation, suspension_translation, suspension_min_limit, suspension_max_limit, friction_limit, velocity, gain))

            point_to_point_count = int(self.next())
            for point_to_point in range(point_to_point_count):
                name = self.next()
                body_a_index = int(self.next())
                body_b_index = int(self.next())
                body_a_rotation = self.next_quaternion()
                body_a_translation = self.next_vector()
                body_b_rotation = self.next_quaternion()
                body_b_translation = self.next_vector()
                constraint_type = int(self.next())
                x_min_limit = float(self.next())
                x_max_limit = float(self.next())
                y_min_limit = float(self.next())
                y_max_limit = float(self.next())
                z_min_limit = float(self.next())
                z_max_limit = float(self.next())
                spring_length = float(self.next())

                self.point_to_points.append(JMSAsset.Point_to_Point(name, body_a_index, body_b_index, body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, constraint_type, x_min_limit, x_max_limit, y_min_limit, y_max_limit, z_min_limit, z_max_limit, spring_length))

            prismatic_count = int(self.next())
            for prismatic in range(prismatic_count):
                name = self.next()
                body_a_index = int(self.next())
                body_b_index = int(self.next())
                body_a_rotation = self.next_quaternion()
                body_a_translation = self.next_vector()
                body_b_rotation = self.next_quaternion()
                body_b_translation = self.next_vector()
                is_limited = int(self.next())
                friction_limit = float(self.next())
                min_limit = float(self.next())
                max_limit = float(self.next())

                self.prismatics.append(JMSAsset.Prismatic(name, body_a_index, body_b_index, body_a_rotation, body_a_translation, body_b_rotation, body_b_translation, is_limited, friction_limit, min_limit, max_limit))

        if self.version >= 8209:
            bounding_sphere_count = int(self.next())
            for bounding_sphere in range(bounding_sphere_count):
                translation = self.next_vector()
                radius = float(self.next())

                self.bounding_spheres.append(JMSAsset.Bounding_Sphere(translation, radius))

        if self.version >= 8212:
            skylight_count = int(self.next())
            for skylight in range(skylight_count):
                direction = self.next_vector()
                radiant_intensity = self.next_vector()
                solid_angle = float(self.next())

                self.skylights.append(JMSAsset.Skylight(direction, radiant_intensity, solid_angle))

        if self.left() != 0: # is something wrong with the parser?
            raise RuntimeError("%s elements left after parse end" % self.left())

        # update node graph
        if self.version >= 8205:
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
        else:
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

def generate_jms_skeleton(jms_file, armature, parent_id_class, fix_rotations):
    file_version = jms_file.version
    first_frame = jms_file.transforms[0]

    bpy.ops.object.mode_set(mode = 'EDIT')
    for idx, jms_node in enumerate(jms_file.nodes):
        current_bone = armature.data.edit_bones.new(jms_node.name)
        current_bone.tail[2] = mesh_processing.get_bone_distance(jms_file, None, None, idx, "JMS")
        parent_idx = jms_node.parent

        if not parent_idx == -1 and not parent_idx == None:
            if 'thigh' in jms_node.name and not parent_id_class.pelvis == None and not parent_id_class.thigh0 == None and not parent_id_class.thigh1 == None:
                parent_idx = parent_id_class.pelvis

            elif 'clavicle' in jms_node.name and not parent_id_class.spine1 == None and not parent_id_class.clavicle0 == None and not parent_id_class.clavicle1 == None:
                parent_idx = parent_id_class.spine1

            parent = jms_file.nodes[parent_idx].name
            current_bone.parent = armature.data.edit_bones[parent]

        matrix_translate = Matrix.Translation(first_frame[idx].vector)
        matrix_rotation = first_frame[idx].rotation.to_matrix().to_4x4()

        transform_matrix = matrix_translate @ matrix_rotation
        if fix_rotations:
            if file_version < 8205 and current_bone.parent:
                transform_matrix = (current_bone.parent.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

            current_bone.matrix = transform_matrix @ Matrix.Rotation(radians(-90.0), 4, 'Z')
        else:
            if file_version < 8205 and current_bone.parent:
                transform_matrix = current_bone.parent.matrix @ transform_matrix

            current_bone.matrix = transform_matrix

    bpy.ops.object.mode_set(mode = 'OBJECT')

def set_parent_id_class(jms_file, parent_id_class):
    for idx, jms_node in enumerate(jms_file.nodes):
        if 'pelvis' in jms_node.name:
            parent_id_class.pelvis = idx

        if 'thigh' in jms_node.name:
            if parent_id_class.thigh0 == None:
                parent_id_class.thigh0 = idx

            else:
                parent_id_class.thigh1 = idx

        elif 'spine1' in jms_node.name:
            parent_id_class.spine1 = idx

        elif 'clavicle' in jms_node.name:
            if parent_id_class.clavicle0 == None:
                parent_id_class.clavicle0 = idx

            else:
                parent_id_class.clavicle1 = idx

def load_file(context, filepath, report, game_version, reuse_armature, fix_parents, fix_rotations):
    jms_file = JMSAsset(filepath, game_version)

    collection = context.collection
    scene = context.scene
    armature = None
    object_list = list(scene.objects)
    region_permutation_list = []
    game_version = jms_file.game_version
    version = jms_file.version
    object_name = bpy.path.basename(filepath).rsplit('.', 1)[0]
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors

    mesh_processing.deselect_objects(context)

    for obj in object_list:
        if armature is None:
            if obj.type == 'ARMATURE':
                exist_count = 0
                armature_bone_list = []
                armature_bone_list = list(obj.data.bones)
                for node in armature_bone_list:
                    for jms_node in jms_file.nodes:
                        if node.name == jms_node.name:
                            exist_count += 1

                if exist_count == len(jms_file.nodes):
                    armature = obj

    if armature == None or not reuse_armature:
        parent_id_class = global_functions.ParentIDFix()

        armdata = bpy.data.armatures.new('Armature')
        armature = bpy.data.objects.new('Armature', armdata)
        collection.objects.link(armature)

        mesh_processing.select_object(context, armature)
        if fix_parents:
            if game_version == 'halo2' or game_version == 'halo3':
                set_parent_id_class(jms_file, parent_id_class)

        generate_jms_skeleton(jms_file, armature, parent_id_class, fix_rotations)

    for used_regions in jms_file.used_regions:
        name = jms_file.regions[used_regions].name
        if jms_file.game_version == 'haloce':
            if not name in region_permutation_list:
                region_permutation_list.append(name)

    for triangle in jms_file.triangles:
        triangle_material_index = triangle.material_index
        material = None
        region = None
        permutation = None
        if not triangle_material_index == -1:
            material = jms_file.materials[triangle_material_index]
            region = material.region
            permutation = material.permutation

        if jms_file.game_version == 'halo2' or jms_file.game_version == 'halo3':
            if not [region, permutation] in region_permutation_list:
                region_permutation_list.append([permutation, region])

    for marker_obj in jms_file.markers:
        parent_idx = marker_obj.parent
        marker_region_index = marker_obj.region
        radius = marker_obj.scale
        object_name_prefix = '#%s' % marker_obj.name
        marker_name_override = ""
        if context.scene.objects.get('#%s' % marker_obj.name):
            marker_name_override = marker_obj.name

        mesh = bpy.data.meshes.new(object_name_prefix)
        object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
        collection.objects.link(object_mesh)

        object_mesh.marker.name_override = marker_name_override

        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=1)
        bm.to_mesh(mesh)
        bm.free()

        if not marker_region_index == -1:
            object_mesh.face_maps.new(name=jms_file.regions[marker_region_index].name)

        mesh_processing.select_object(context, object_mesh)
        mesh_processing.select_object(context, armature)
        if not parent_idx == -1:
            bpy.ops.object.mode_set(mode='EDIT')
            armature.data.edit_bones.active = armature.data.edit_bones[jms_file.nodes[parent_idx].name]
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)

        else:
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        matrix_translate = Matrix.Translation(marker_obj.translation)
        matrix_rotation = marker_obj.rotation.to_matrix().to_4x4()

        transform_matrix = matrix_translate @ matrix_rotation
        if not parent_idx == -1:
            pose_bone = armature.pose.bones[jms_file.nodes[parent_idx].name]
            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix
            else:
                transform_matrix = pose_bone.matrix @ transform_matrix

        object_mesh.matrix_world = transform_matrix
        object_mesh.data.ass_jms.Object_Type = 'SPHERE'
        object_dimension = radius * 2
        object_mesh.dimensions = (object_dimension, object_dimension, object_dimension)
        object_mesh.select_set(False)
        armature.select_set(False)

    for xref_marker in jms_file.xref_instance_markers:
        xref_name = xref_marker.name

        mesh = bpy.data.meshes.new(xref_name)
        object_mesh = bpy.data.objects.new(xref_name, mesh)
        collection.objects.link(object_mesh)

        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bm.to_mesh(mesh)
        bm.free()

        object_mesh.data.ass_jms.Object_Type = 'BOX'
        if version >= 8205:
            xref_idx = xref_marker.path_index
            xref_path = jms_file.xref_paths[xref_idx].path
            object_mesh.data.ass_jms.XREF_path = xref_path

        mesh_processing.select_object(context, object_mesh)
        mesh_processing.select_object(context, armature)
        bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        matrix_translate = Matrix.Translation(xref_marker.translation)
        matrix_rotation = xref_marker.rotation.to_matrix().to_4x4()

        transform_matrix = matrix_translate @ matrix_rotation

        object_mesh.matrix_world = transform_matrix
        object_mesh.select_set(False)
        armature.select_set(False)

    #generate mesh object
    if not len(jms_file.vertices) == 0:
        object_name = bpy.path.basename(filepath).rsplit('.', 1)[0]
        if game_version == 'haloce':
            if 'physics' in filepath or 'collision' in filepath:
                object_name = '@%s' % object_name

        else:
            if 'collision' in filepath:
                object_name = '@%s' % object_name

        mesh = bpy.data.meshes.new(object_name)
        object_mesh = bpy.data.objects.new(object_name, mesh)
        collection.objects.link(object_mesh)
        bm, vert_normal_list = mesh_processing.process_mesh_import_data(game_version, jms_file, None, object_mesh, random_color_gen, 'JMS')
        bm.to_mesh(mesh)
        bm.free()
        object_mesh.data.normals_split_custom_set(vert_normal_list)
        object_mesh.data.use_auto_smooth = True
        object_mesh.parent = armature
        mesh_processing.add_modifier(context, object_mesh, False, None, armature)


    primitive_shapes = []
    for sphere in jms_file.spheres:
        parent_idx = sphere.parent_index
        name = sphere.name
        material_index = sphere.material_index
        radius = sphere.radius

        object_name_prefix = '$%s' % name

        mesh = bpy.data.meshes.new(object_name_prefix)
        object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
        collection.objects.link(object_mesh)

        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=1)
        bm.to_mesh(mesh)
        bm.free()

        mesh_processing.select_object(context, object_mesh)
        mesh_processing.select_object(context, armature)
        if not parent_idx == -1:
            bpy.ops.object.mode_set(mode='EDIT')
            armature.data.edit_bones.active = armature.data.edit_bones[jms_file.nodes[parent_idx].name]
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)

        else:
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        matrix_translate = Matrix.Translation(sphere.translation)
        matrix_rotation = sphere.rotation.to_matrix().to_4x4()

        transform_matrix = matrix_translate @ matrix_rotation
        if not parent_idx == -1:
            pose_bone = armature.pose.bones[jms_file.nodes[parent_idx].name]
            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix
            else:
                transform_matrix = pose_bone.matrix @ transform_matrix

        object_mesh.matrix_world = transform_matrix
        primitive_shapes.append((object_mesh, sphere.parent_index))

        if not material_index == -1:
            mat = jms_file.materials[material_index]
            current_region_permutation = global_functions.material_definition_helper(material_index, mat)
            object_mesh.face_maps.new(name=current_region_permutation)
            material_name = mat.scene_name
            mat = bpy.data.materials.get(material_name)
            if mat is None:
                mat = bpy.data.materials.new(name=material_name)

            if object_mesh.data.materials:
                object_mesh.data.materials[0] = mat

            else:
                object_mesh.data.materials.append(mat)

            mat.diffuse_color = random_color_gen.next()

        object_mesh.data.ass_jms.Object_Type = 'SPHERE'
        object_dimension = radius * 2
        object_mesh.dimensions = (object_dimension, object_dimension, object_dimension)
        object_mesh.select_set(False)
        armature.select_set(False)

    for box in jms_file.boxes:
        parent_idx = box.parent_index
        name = box.name
        material_index = box.material_index
        width = box.width
        length = box.length
        height = box.height

        object_name_prefix = '$%s' % name

        mesh = bpy.data.meshes.new(object_name_prefix)
        object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
        collection.objects.link(object_mesh)

        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bm.to_mesh(mesh)
        bm.free()

        mesh_processing.select_object(context, object_mesh)
        mesh_processing.select_object(context, armature)
        if not parent_idx == -1:
            bpy.ops.object.mode_set(mode='EDIT')
            armature.data.edit_bones.active = armature.data.edit_bones[jms_file.nodes[parent_idx].name]
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)

        else:
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        matrix_translate = Matrix.Translation(box.translation)
        matrix_rotation = box.rotation.to_matrix().to_4x4()

        transform_matrix = matrix_translate @ matrix_rotation
        if not parent_idx == -1:
            pose_bone = armature.pose.bones[jms_file.nodes[parent_idx].name]
            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix
            else:
                transform_matrix = pose_bone.matrix @ transform_matrix

        object_mesh.matrix_world = transform_matrix
        primitive_shapes.append((object_mesh, box.parent_index))

        if not material_index == -1:
            mat = jms_file.materials[material_index]
            current_region_permutation = global_functions.material_definition_helper(material_index, mat)
            object_mesh.face_maps.new(name=current_region_permutation)

            material_name = mat.scene_name
            mat = bpy.data.materials.get(material_name)
            if mat is None:
                mat = bpy.data.materials.new(name=material_name)

            if object_mesh.data.materials:
                object_mesh.data.materials[0] = mat

            else:
                object_mesh.data.materials.append(mat)

            mat.diffuse_color = random_color_gen.next()

        object_mesh.data.ass_jms.Object_Type = 'BOX'
        object_mesh.dimensions = (width, length, height)
        object_mesh.select_set(False)
        armature.select_set(False)

    for capsule in jms_file.capsules:
        parent_idx = capsule.parent_index
        name = capsule.name
        material_index = capsule.material_index
        height = capsule.height
        radius = capsule.radius

        object_name_prefix = '$%s' % name

        mesh = bpy.data.meshes.new(object_name_prefix)
        object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
        collection.objects.link(object_mesh)

        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, diameter1=1, diameter2=1, depth=2)
        bm.transform(Matrix.Translation((0, 0, 1)))
        bm.to_mesh(mesh)
        bm.free()

        mesh_processing.select_object(context, object_mesh)
        mesh_processing.select_object(context, armature)
        if not parent_idx == -1:
            bpy.ops.object.mode_set(mode='EDIT')
            armature.data.edit_bones.active = armature.data.edit_bones[jms_file.nodes[parent_idx].name]
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)

        else:
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        matrix_translate = Matrix.Translation(capsule.translation)
        matrix_rotation = capsule.rotation.to_matrix().to_4x4()

        transform_matrix = matrix_translate @ matrix_rotation
        if not parent_idx == -1:
            pose_bone = armature.pose.bones[jms_file.nodes[parent_idx].name]
            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix
            else:
                transform_matrix = pose_bone.matrix @ transform_matrix

        object_mesh.matrix_world = transform_matrix
        primitive_shapes.append((object_mesh, capsule.parent_index))

        if not material_index == -1:
            mat = jms_file.materials[material_index]
            current_region_permutation = global_functions.material_definition_helper(material_index, mat)
            object_mesh.face_maps.new(name=current_region_permutation)

            material_name = mat.scene_name
            mat = bpy.data.materials.get(material_name)
            if mat is None:
                mat = bpy.data.materials.new(name=material_name)

            if object_mesh.data.materials:
                object_mesh.data.materials[0] = mat

            else:
                object_mesh.data.materials.append(mat)

            mat.diffuse_color = random_color_gen.next()

        object_mesh.data.ass_jms.Object_Type = 'CAPSULES'
        object_dimension = radius * 2
        object_mesh.dimensions = (object_dimension, object_dimension, (object_dimension + height))
        object_mesh.select_set(False)
        armature.select_set(False)


    for convex_shape in jms_file.convex_shapes:
        parent_idx = convex_shape.parent_index
        name = convex_shape.name
        material_index = convex_shape.material_index
        verts = convex_shape.verts

        object_name_prefix = '$%s' % name

        mesh = bpy.data.meshes.new(object_name_prefix)
        object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
        collection.objects.link(object_mesh)

        bm = bmesh.new()
        for vert in verts:
            bm.verts.new((vert[0], vert[1], vert[2]))

        bm.to_mesh(mesh)
        bm.free()

        mesh_processing.select_object(context, object_mesh)
        mesh_processing.select_object(context, armature)
        if not parent_idx == -1:
            bpy.ops.object.mode_set(mode='EDIT')
            armature.data.edit_bones.active = armature.data.edit_bones[jms_file.nodes[parent_idx].name]
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)

        else:
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        matrix_translate = Matrix.Translation(convex_shape.translation)
        matrix_rotation = convex_shape.rotation.to_matrix().to_4x4()

        transform_matrix = matrix_translate @ matrix_rotation
        if not parent_idx == -1:
            pose_bone = armature.pose.bones[jms_file.nodes[parent_idx].name]
            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix
            else:
                transform_matrix = pose_bone.matrix @ transform_matrix

        object_mesh.matrix_world = transform_matrix
        primitive_shapes.append((object_mesh, convex_shape.parent_index))

        if not material_index == -1:
            mat = jms_file.materials[material_index]
            current_region_permutation = global_functions.material_definition_helper(material_index, mat)
            object_mesh.face_maps.new(name=current_region_permutation)

            material_name = mat.scene_name
            mat = bpy.data.materials.get(material_name)
            if mat is None:
                mat = bpy.data.materials.new(name=material_name)

            if object_mesh.data.materials:
                object_mesh.data.materials[0] = mat

            else:
                object_mesh.data.materials.append(mat)

            mat.diffuse_color = random_color_gen.next()

        mesh_processing.select_object(context, object_mesh)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.convex_hull(delete_unused=True, use_existing_faces=True, join_triangles=True)
        bpy.ops.object.mode_set(mode='OBJECT')
        object_mesh.data.ass_jms.Object_Type = 'CONVEX SHAPES'
        mesh_processing.deselect_objects(context)

    for ragdoll in jms_file.ragdolls:
        name = ragdoll.name
        ragdoll_attached_index = ragdoll.attached_index
        ragdoll_referenced_index = ragdoll.referenced_index

        ragdoll_attached_object = None
        ragdoll_referenced_object = None
        if not ragdoll_attached_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == ragdoll_attached_index:
                    ragdoll_attached_object = shape_object
                    if not not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)
                        shape_object.rigid_body.linear_damping = ragdoll.friction_limit

                    break

        if not ragdoll_referenced_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == ragdoll_referenced_index:
                    ragdoll_referenced_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)
                        shape_object.rigid_body.linear_damping = ragdoll.friction_limit
                    
                    break

        object_name_prefix = '$%s' % name

        object_empty = bpy.data.objects.new(object_name_prefix, None)
        collection.objects.link(object_empty)

        object_empty.empty_display_size = 2
        object_empty.empty_display_type = 'ARROWS'

        mesh_processing.select_object(context, object_empty)

        bpy.ops.rigidbody.constraint_add()

        object_empty.rigid_body_constraint.type = 'GENERIC'
        object_empty.rigid_body_constraint.use_limit_ang_x = True
        object_empty.rigid_body_constraint.use_limit_ang_y = True
        object_empty.rigid_body_constraint.use_limit_ang_z = True

        object_empty.rigid_body_constraint.use_limit_lin_x = True
        object_empty.rigid_body_constraint.use_limit_lin_y = True
        object_empty.rigid_body_constraint.use_limit_lin_z = True

        object_empty.rigid_body_constraint.limit_ang_x_lower = radians(ragdoll.min_twist)
        object_empty.rigid_body_constraint.limit_ang_x_upper = radians(ragdoll.max_twist)
        object_empty.rigid_body_constraint.limit_ang_y_lower = radians(ragdoll.min_cone)
        object_empty.rigid_body_constraint.limit_ang_y_upper = radians(ragdoll.max_cone)
        object_empty.rigid_body_constraint.limit_ang_z_lower = radians(ragdoll.min_plane)
        object_empty.rigid_body_constraint.limit_ang_z_upper = radians(ragdoll.max_plane)

        object_empty.rigid_body_constraint.limit_lin_x_lower = 0
        object_empty.rigid_body_constraint.limit_lin_x_upper = 0
        object_empty.rigid_body_constraint.limit_lin_y_lower = 0
        object_empty.rigid_body_constraint.limit_lin_y_upper = 0
        object_empty.rigid_body_constraint.limit_lin_z_lower = 0
        object_empty.rigid_body_constraint.limit_lin_z_upper = 0

        object_empty.rigid_body_constraint.object1 = ragdoll_attached_object
        object_empty.rigid_body_constraint.object2 = ragdoll_referenced_object

        mesh_processing.select_object(context, armature)
        bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)
        transform_matrix = Euler((0, 0, 0)).to_matrix().to_4x4()

        ragdoll_origin_index = None
        ragdoll_origin_is_attached = False
        if not ragdoll_attached_index == -1:
            ragdoll_origin_is_attached = True
            ragdoll_origin_index = ragdoll_attached_index
        elif not ragdoll_referenced_index == -1 and ragdoll_origin_index == None:
            ragdoll_origin_index = ragdoll_referenced_index

        if not ragdoll_origin_index == None:
            pose_bone = armature.pose.bones[ragdoll_origin_index]
            ragdoll_rotation = ragdoll.attached_rotation
            ragdoll_translation = ragdoll.attached_translation
            if not ragdoll_origin_is_attached:
                ragdoll_rotation = ragdoll.referenced_rotation
                ragdoll_translation = ragdoll.referenced_translation

            hinge_local_translate = Matrix.Translation(ragdoll_translation)
            hinge_local_rotation = ragdoll_rotation.to_matrix().to_4x4()
            hinge_local_matrix = hinge_local_translate @ hinge_local_rotation

            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ hinge_local_matrix

            else:
                transform_matrix = pose_bone.matrix @ hinge_local_matrix

        object_empty.matrix_world = transform_matrix
        object_empty.select_set(False)
        armature.select_set(False)

    for hinge in jms_file.hinges:
        name = hinge.name
        hinge_body_a_index = hinge.body_a_index
        hinge_body_b_index = hinge.body_b_index

        hinge_body_a_object = None
        hinge_body_b_object = None
        if not hinge_body_a_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == hinge_body_a_index:
                    hinge_body_a_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)
                        shape_object.rigid_body.linear_damping = hinge.friction_limit

                    break

        if not hinge_body_b_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == hinge_body_b_index:
                    hinge_body_b_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)
                        shape_object.rigid_body.linear_damping = hinge.friction_limit

                    break

        object_name_prefix = '$%s' % name

        object_empty = bpy.data.objects.new(object_name_prefix, None)
        collection.objects.link(object_empty)

        object_empty.empty_display_size = 2
        object_empty.empty_display_type = 'ARROWS'

        mesh_processing.select_object(context, object_empty)

        bpy.ops.rigidbody.constraint_add()

        object_empty.rigid_body_constraint.type = 'HINGE'
        object_empty.rigid_body_constraint.use_limit_ang_z = True

        object_empty.rigid_body_constraint.limit_ang_z_lower = radians(hinge.min_angle)
        object_empty.rigid_body_constraint.limit_ang_z_upper = radians(hinge.max_angle)

        object_empty.rigid_body_constraint.object1 = hinge_body_a_object
        object_empty.rigid_body_constraint.object2 = hinge_body_b_object

        mesh_processing.select_object(context, armature)
        bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)
        transform_matrix = Euler((0, 0, 0)).to_matrix().to_4x4()

        hinge_origin_index = None
        hinge_origin_is_attached = False
        if not hinge_body_a_index == -1:
            hinge_origin_is_attached = True
            hinge_origin_index = hinge_body_a_index
        elif not hinge_body_b_index == -1 and hinge_origin_index == None:
            hinge_origin_index = hinge_body_b_index

        if not hinge_origin_index == None:
            pose_bone = armature.pose.bones[hinge_origin_index]
            hinge_rotation = hinge.body_a_rotation
            hinge_translation = hinge.body_a_translation
            if not hinge_origin_is_attached:
                hinge_rotation = hinge.body_b_rotation
                hinge_translation = hinge.body_b_translation

            hinge_local_translate = Matrix.Translation(hinge_translation)
            hinge_local_rotation = hinge_rotation.to_matrix().to_4x4()
            hinge_local_matrix = hinge_local_translate @ hinge_local_rotation

            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ hinge_local_matrix

            else:
                transform_matrix = pose_bone.matrix @ hinge_local_matrix

        object_empty.matrix_world = transform_matrix
        object_empty.select_set(False)
        armature.select_set(False)

    for car_wheel in jms_file.car_wheels:
        name = car_wheel.name
        car_wheel_chassis_index = car_wheel.chassis_index
        car_wheel_wheel_index = car_wheel.wheel_index

        car_wheel_chassis_object = None
        car_wheel_wheel_object = None
        if not car_wheel_chassis_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == car_wheel_chassis_index:
                    car_wheel_chassis_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)
                        shape_object.rigid_body.linear_damping = hinge.friction_limit

                    break

        if not car_wheel_wheel_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == car_wheel_wheel_index:
                    car_wheel_wheel_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)
                        shape_object.rigid_body.linear_damping = hinge.friction_limit

                    break

        object_name_prefix = '$%s' % name

        object_empty = bpy.data.objects.new(object_name_prefix, None)
        collection.objects.link(object_empty)

        object_empty.empty_display_size = 2
        object_empty.empty_display_type = 'ARROWS'

        mesh_processing.select_object(context, object_empty)
        mesh_processing.select_object(context, armature)
        bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)
        transform_matrix = Euler((0, 0, 0)).to_matrix().to_4x4()

        car_wheel_origin_index = None
        car_wheel_origin_is_attached = False
        if not car_wheel_chassis_index == -1:
            car_wheel_origin_is_attached = True
            car_wheel_origin_index = car_wheel_chassis_index
        elif not car_wheel_wheel_index == -1 and car_wheel_origin_index == None:
            car_wheel_origin_index = car_wheel_wheel_index

        if not car_wheel_origin_index == None:
            pose_bone = armature.pose.bones[car_wheel_origin_index]
            car_wheel_rotation = car_wheel.wheel_rotation
            car_wheel_translation = car_wheel.wheel_translation
            if not car_wheel_origin_is_attached:
                car_wheel_rotation = car_wheel.suspension_rotation
                car_wheel_translation = car_wheel.suspension_translation

            car_wheel_local_translate = Matrix.Translation(car_wheel_translation)
            car_wheel_local_rotation = car_wheel_rotation.to_matrix().to_4x4()
            car_wheel_local_matrix = car_wheel_local_translate @ car_wheel_local_rotation

            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ car_wheel_local_matrix

            else:
                transform_matrix = pose_bone.matrix @ car_wheel_local_matrix

        object_empty.matrix_world = transform_matrix
        object_empty.select_set(False)
        armature.select_set(False)

    for point_to_point in jms_file.point_to_points:
        name = point_to_point.name
        point_to_point_body_a_index = point_to_point.body_a_index
        point_to_point_body_b_index = point_to_point.body_b_index

        point_to_point_body_a_object = None
        point_to_point_body_b_object = None
        if not point_to_point_body_a_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == point_to_point_body_a_index:
                    point_to_point_body_a_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)

                    break

        if not point_to_point_body_b_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == point_to_point_body_b_index:
                    point_to_point_body_b_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)

                    break

        object_name_prefix = '$%s' % name

        object_empty = bpy.data.objects.new(object_name_prefix, None)
        collection.objects.link(object_empty)

        object_empty.empty_display_size = 2
        object_empty.empty_display_type = 'ARROWS'

        mesh_processing.select_object(context, object_empty)

        bpy.ops.rigidbody.constraint_add()

        object_empty.rigid_body_constraint.type = 'GENERIC_SPRING'

        object_empty.rigid_body_constraint.object1 = point_to_point_body_a_object
        object_empty.rigid_body_constraint.object2 = point_to_point_body_b_object

        mesh_processing.select_object(context, armature)
        bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)
        transform_matrix = Euler((0, 0, 0)).to_matrix().to_4x4()

        point_to_point_origin_index = None
        point_to_point_origin_is_attached = False
        if not point_to_point_body_a_index == -1:
            point_to_point_origin_is_attached = True
            point_to_point_origin_index = point_to_point_body_a_index
        elif not point_to_point_body_b_index == -1 and point_to_point_origin_index == None:
            point_to_point_origin_index = point_to_point_body_b_index

        if not point_to_point_origin_index == None:
            pose_bone = armature.pose.bones[point_to_point_origin_index]
            point_to_point_rotation = point_to_point.body_a_rotation
            point_to_point_translation = point_to_point.body_a_translation
            if not point_to_point_origin_is_attached:
                point_to_point_rotation = point_to_point.body_b_rotation
                point_to_point_translation = point_to_point.body_b_translation

            point_to_point_local_translate = Matrix.Translation(point_to_point_translation)
            point_to_point_local_rotation = point_to_point_rotation.to_matrix().to_4x4()
            point_to_point_local_matrix = point_to_point_local_translate @ point_to_point_local_rotation

            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ point_to_point_local_matrix

            else:
                transform_matrix = pose_bone.matrix @ point_to_point_local_matrix

        object_empty.matrix_world = transform_matrix
        object_empty.select_set(False)
        armature.select_set(False)

    for prismatic in jms_file.prismatics:
        name = prismatic.name
        prismatic_body_a_index = prismatic.body_a_index
        prismatic_body_b_index = prismatic.body_b_index
        if not prismatic_body_a_index == -1:
            body_a_index = jms_file.nodes[prismatic_body_a_index].name

        if not prismatic_body_b_index == -1:
            body_b_index = jms_file.nodes[prismatic_body_b_index].name

        object_name_prefix = '$%s' % name

        object_empty = bpy.data.objects.new(object_name_prefix, None)
        collection.objects.link(object_empty)

        object_empty.empty_display_size = 2
        object_empty.empty_display_type = 'ARROWS'

        mesh_processing.select_object(context, object_empty)
        mesh_processing.select_object(context, armature)
        bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)
        matrix_translate = Matrix.Translation(prismatic.body_a_translation)
        matrix_rotation = prismatic.body_a_rotation.to_matrix().to_4x4()

        transform_matrix = matrix_translate @ matrix_rotation
        if not prismatic_body_a_index == -1:
            pose_bone = armature.pose.bones[jms_file.nodes[prismatic_body_a_index].name]
            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix
            else:
                transform_matrix = pose_bone.matrix @ transform_matrix

        object_empty.matrix_world = transform_matrix
        object_empty.select_set(False)
        armature.select_set(False)

    for idx, bounding_sphere in enumerate(jms_file.bounding_spheres):
        name = 'bounding_sphere_%s' % idx
        radius = bounding_sphere.radius

        mesh = bpy.data.meshes.new(name)
        object_mesh = bpy.data.objects.new(name, mesh)
        collection.objects.link(object_mesh)

        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=1)
        bm.to_mesh(mesh)
        bm.free()

        mesh_processing.select_object(context, object_mesh)
        mesh_processing.select_object(context, armature)
        bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        matrix_translate = Matrix.Translation(bounding_sphere.translation)

        transform_matrix = matrix_translate
        object_mesh.matrix_world = transform_matrix

        object_mesh.data.ass_jms.Object_Type = 'SPHERE'
        object_mesh.data.ass_jms.bounding_radius = True
        object_dimension = radius * 2
        object_mesh.dimensions = (object_dimension, object_dimension, object_dimension)
        object_mesh.select_set(False)
        armature.select_set(False)

    for idx, skylight in enumerate(jms_file.skylights):
        name = 'skylight_%s' % idx
        down_vector = Vector((0, 0, -1))

        light_data = bpy.data.lights.new(name, "SUN")
        object_mesh = bpy.data.objects.new(name, light_data)
        collection.objects.link(object_mesh)
        object_mesh.rotation_euler = down_vector.rotation_difference(skylight.direction).to_euler()
        object_mesh.data.color = (skylight.radiant_intensity)
        object_mesh.data.energy = (skylight.solid_angle)

        mesh_processing.select_object(context, object_mesh)
        mesh_processing.select_object(context, armature)
        bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        object_mesh.select_set(False)
        armature.select_set(False)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.jms()
