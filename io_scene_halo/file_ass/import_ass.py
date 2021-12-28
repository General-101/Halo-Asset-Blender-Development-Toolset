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
import bmesh

from math import radians
from mathutils import Matrix
from ..global_functions import mesh_processing, global_functions

class ASSAsset(global_functions.HaloAsset):
    class Transform:
        def __init__(self, rotation, vector, scale):
            self.rotation = rotation
            self.vector = vector
            self.scale = scale

    class Material:
        def __init__(self, scene_name=None, file_name=None, texture_path=None, slot=None, lod=None, permutation=None, region=None, material_effect=None, material_strings=None):
            self.scene_name = scene_name
            self.file_name = file_name
            self.texture_path = texture_path
            self.slot = slot
            self.lod = lod
            self.permutation = permutation
            self.region = region
            self.material_effect = material_effect
            self.material_strings = material_strings

    class Object:
        def __init__(self,
                     geo_class,
                     xref_filepath,
                     xref_objectname,
                     material_index=-1,
                     radius=0.0,
                     extents=None,
                     height=0.0,
                     vertices=None,
                     triangles=None,
                     light_properties=None,
                     node_index_list=None
                     ):

            self.geo_class = geo_class
            self.xref_filepath = xref_filepath
            self.xref_objectname = xref_objectname
            self.material_index = material_index
            self.radius = radius
            self.extents = extents
            self.height = height
            self.vertices = vertices
            self.triangles = triangles
            self.light_properties = light_properties
            self.node_index_list = node_index_list

    class Light:
        def __init__(self,
                     light_type,
                     light_color=None,
                     intensity=0.0,
                     hotspot_size=0.0,
                     hotspot_falloff_size=0.0,
                     uses_near_attenuation=0,
                     near_attenuation_start=0.0,
                     near_attenuation_end=0.0,
                     uses_far_attenuation=0,
                     far_attenuation_start=0,
                     far_attenuation_end=0.0,
                     light_shape=0,
                     light_aspect_ratio=0.0
                     ):

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
        def __init__(self, node_influence_count=0, node_set=None, translation=None, normal=None, color=None, uv_set=None):
            self.node_influence_count = node_influence_count
            self.node_set = node_set
            self.translation = translation
            self.normal = normal
            self.color = color
            self.uv_set = uv_set

    class Triangle:
        def __init__(self, material_index=-1, v0=-1, v1=-1, v2=-1):
            self.material_index = material_index
            self.v0 = v0
            self.v1 = v1
            self.v2 = v2

    class Instance:
        def __init__(self, name, object_index=-1, unique_id=-1, parent_id=-1, inheritance_flag=0, local_transform=None, pivot_transform=None):
            self.name = name
            self.object_index = object_index
            self.unique_id = unique_id
            self.parent_id = parent_id
            self.inheritance_flag = inheritance_flag
            self.local_transform = local_transform
            self.pivot_transform = pivot_transform

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

    def __init__(self, filepath):
        super().__init__(filepath)
        self.version = int(self.next())
        version_list = [1, 2, 3, 4, 5, 6, 7]
        if not self.version in version_list:
            raise global_functions.AssetParseError("Importer does not support this ASS version")

        self.skip(4) # skip header
        self.materials = []
        self.objects = []
        self.instances = []
        material_count = int(self.next())
        used_material_names = []
        for idx, material in enumerate(range(material_count)):
            name = self.next().strip('\"')
            scene_name = name
            file_name = ""
            if self.version >= 3:
                if scene_name in used_material_names:
                    file_name = name
                    duplicate_name = None
                    loop_count = 1
                    while duplicate_name == None:
                        while_name = name + "." + str(loop_count).zfill(3)
                        if not while_name in used_material_names:
                            duplicate_name = while_name

                        loop_count += 1

                    scene_name = duplicate_name

            used_material_names.append(scene_name)
            material_effect = self.next().strip('\"')
            material_strings = []
            if self.version >= 4:
                material_string_count = int(self.next())
                for string in range(material_string_count):
                    material_strings.append(self.next().strip('\"'))

            self.materials.append(ASSAsset.Material(scene_name, file_name, None, None, None, None, None, material_effect, material_strings))

        object_count = int(self.next())
        for object in range(object_count):
            vertices = []
            node_index_list = []
            triangles = []
            geo_class = self.next().strip('\"')
            xref_path = self.next().strip('\"')
            xref_name = self.next().strip('\"')
            material_index = -1
            radius = 2
            extents = [1.0, 1.0, 1.0]
            height = 1
            light_properties = None
            if geo_class == 'SPHERE':
                material_index = int(self.next())
                radius = float(self.next())

            elif geo_class == 'BOX':
                material_index = int(self.next())
                extents = self.next_vector()

            elif geo_class == 'PILL':
                material_index = int(self.next())
                height = float(self.next())
                radius = float(self.next())

            elif geo_class == 'MESH':
                vert_count = int(self.next())
                for vert in range(vert_count):
                    node_set = []
                    uv_set = []
                    color = None
                    translation = self.next_vector()
                    normal = self.next_vector()
                    if self.version >= 6:
                        color = self.next_vector()
                    node_influence_count = int(self.next())
                    for node in range(node_influence_count):
                        node_index = int(self.next())
                        if not node_index in node_index_list:
                            node_index_list.append(node_index)

                        node_weight = float(self.next())
                        node_set.append([node_index, node_weight])

                    uv_count = int(self.next())
                    for uv in range(uv_count):
                        tex_u_value = self.next()
                        tex_v_value = self.next()
                        tex_w_value = None
                        tex_w = None

                        try:
                            tex_u = float(tex_u_value)
                        except ValueError:
                            tex_u = float(tex_u_value.rsplit('.', 1)[0])

                        try:
                            tex_v = float(tex_v_value)
                        except ValueError:
                            tex_v = float(tex_v_value.rsplit('.', 1)[0])

                        if self.version >= 6:
                            tex_w_value = self.next()

                            try:
                                tex_w = float(tex_w_value)
                            except ValueError:
                                tex_w = float(tex_w_value.rsplit('.', 1)[0])

                        uv_set.append([tex_u, tex_v, tex_w])

                    vertices.append(ASSAsset.Vertex(node_influence_count, node_set, translation, normal, color, uv_set))

                triangle_count = int(self.next())
                for triangle in range(triangle_count):
                    material_index = int(self.next())
                    v0 = int(self.next())
                    v1 = int(self.next())
                    v2 = int(self.next())

                    triangles.append(ASSAsset.Triangle(material_index, v0, v1, v2))

            elif geo_class == 'GENERIC_LIGHT':
                light_type = self.next().strip('\"')
                light_color = self.next_vector()
                intensity = float(self.next())
                hotspot_size = float(self.next())
                hotspot_falloff_size = float(self.next())
                uses_near_attenuation = int(self.next())
                near_attenuation_start = float(self.next())
                near_attenuation_end = float(self.next())
                uses_far_attenuation = int(self.next())
                far_attenuation_start = float(self.next())
                far_attenuation_end = float(self.next())
                light_shape = int(self.next())
                light_aspect_ratio = float(self.next())

                light_properties = ASSAsset.Light(light_type, light_color, intensity, hotspot_size, hotspot_falloff_size, uses_near_attenuation, near_attenuation_start, near_attenuation_end, uses_far_attenuation, far_attenuation_start, far_attenuation_end, light_shape, light_aspect_ratio)

            else:
                print("Bad object")

            self.objects.append(ASSAsset.Object(geo_class,
                                                xref_path,
                                                xref_name,
                                                material_index,
                                                radius,
                                                extents,
                                                height,
                                                vertices,
                                                triangles,
                                                light_properties,
                                                node_index_list
                                                ))

        name_list = []
        instance_count = int(self.next())
        for instance in range(instance_count):
            object_index = int(self.next())
            bone_influence_count = 0
            if not object_index == -1:
                object_element = self.objects[object_index]
                bone_influence_count = len(object_element.node_index_list)

            name = self.next().strip('\"')
            if name in name_list:
                true_name = '%s_%s' % (name, instance)

            else:
                true_name = name

            name_list.append(name)
            unique_id = int(self.next())
            parent_id = int(self.next())
            inheritance_flag = int(self.next())
            if self.version == 1:
                local_transform = self.next_transform_legacy()
                pivot_transform = self.next_transform_legacy()

            else:
                local_transform = self.next_transform()
                pivot_transform = self.next_transform()

            if bone_influence_count > 0:
                self.skip(bone_influence_count)

            self.instances.append(ASSAsset.Instance(true_name, object_index, unique_id, parent_id, inheritance_flag, local_transform, pivot_transform))

        if self.left() != 0: # is something wrong with the parser?
            raise RuntimeError("%s elements left after parse end" % self.left())

def set_ass_material_properties(ass_mat, mat):
    material_effect = ass_mat.material_effect
    material_strings = ass_mat.material_strings
    mat.ass_jms.material_effect = material_effect
    if len(material_strings) > 0:
        mat.ass_jms.is_bm = True

    for string in material_strings:
        if string.startswith("BM_FLAGS"):
            string_bitfield = string.split()[1] #Split the string and retrieve the bitfield.
            mat.ass_jms.two_sided = int(string_bitfield[0])
            mat.ass_jms.transparent_1_sided = int(string_bitfield[1])
            mat.ass_jms.transparent_2_sided = int(string_bitfield[2])
            mat.ass_jms.render_only = int(string_bitfield[3])
            mat.ass_jms.collision_only = int(string_bitfield[4])
            mat.ass_jms.sphere_collision_only = int(string_bitfield[5])
            mat.ass_jms.fog_plane = int(string_bitfield[6])
            mat.ass_jms.ladder = int(string_bitfield[7])
            mat.ass_jms.breakable = int(string_bitfield[8])
            mat.ass_jms.ai_deafening = int(string_bitfield[9])
            mat.ass_jms.no_shadow = int(string_bitfield[10])
            mat.ass_jms.shadow_only = int(string_bitfield[11])
            mat.ass_jms.lightmap_only = int(string_bitfield[12])
            mat.ass_jms.precise = int(string_bitfield[13])
            mat.ass_jms.conveyor = int(string_bitfield[14])
            mat.ass_jms.portal_1_way = int(string_bitfield[15])
            mat.ass_jms.portal_door = int(string_bitfield[16])
            mat.ass_jms.portal_vis_blocker = int(string_bitfield[17])
            mat.ass_jms.ignored_by_lightmaps = int(string_bitfield[18])
            mat.ass_jms.blocks_sound = int(string_bitfield[19])
            mat.ass_jms.decal_offset = int(string_bitfield[20])
            mat.ass_jms.slip_surface = int(string_bitfield[21])

        elif string.startswith("BM_LMRES"):
            lmres_string_args = string.split()
            mat.ass_jms.lightmap_res = float(lmres_string_args[1])
            mat.ass_jms.photon_fidelity = int(lmres_string_args[2])
            mat.ass_jms.two_sided_transparent_tint = (float(lmres_string_args[3]), float(lmres_string_args[4]), float(lmres_string_args[5]))
            mat.ass_jms.override_lightmap_transparency = int(lmres_string_args[6])
            mat.ass_jms.additive_transparency = (float(lmres_string_args[7]), float(lmres_string_args[8]), float(lmres_string_args[9]))
            mat.ass_jms.use_shader_gel = int(lmres_string_args[10])
            if len(lmres_string_args) > 11:
                mat.ass_jms.ignore_default_res_scale = int(lmres_string_args[11])

        elif string.startswith("BM_LIGHTING_BASIC"):
            lighting_basic_args = string.split()
            mat.ass_jms.power = float(lighting_basic_args[1])
            mat.ass_jms.color = (float(lighting_basic_args[2]), float(lighting_basic_args[3]), float(lighting_basic_args[4]))
            mat.ass_jms.quality = float(lighting_basic_args[5])
            mat.ass_jms.power_per_unit_area = int(lighting_basic_args[6])
            mat.ass_jms.emissive_focus = float(lighting_basic_args[7])

        elif string.startswith("BM_LIGHTING_ATTEN"):
            lighting_attenuation_args = string.split()
            mat.ass_jms.attenuation_enabled = int(lighting_attenuation_args[1])
            mat.ass_jms.falloff_distance = float(lighting_attenuation_args[2])
            mat.ass_jms.cutoff_distance = float(lighting_attenuation_args[3])

        elif string.startswith("BM_LIGHTING_FRUS"):
            lighting_frus_args = string.split()
            mat.ass_jms.frustum_blend = float(lighting_frus_args[1])
            mat.ass_jms.frustum_falloff = float(lighting_frus_args[2])
            mat.ass_jms.frustum_cutoff = float(lighting_frus_args[3])


def set_primitive_material(object_material_index, ass_file, mesh):
    if not object_material_index == -1:
        mat = ass_file.materials[object_material_index]
        if mesh.materials:
            mesh.materials[0] = bpy.data.materials[mat.name]

def load_file(context, filepath, report):
    ass_file = ASSAsset(filepath)

    collection = context.collection
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors
    mesh_vertex_groups = []

    mesh_processing.deselect_objects(context)

    for idx, ass_mat in enumerate(ass_file.materials):
        material_name = ass_mat.scene_name

        mat = bpy.data.materials.get(material_name)
        if mat is None:
            mat = bpy.data.materials.new(name=material_name)

        set_ass_material_properties(ass_mat, mat)
        mat.ass_jms.name_override = ass_mat.file_name
        mat.diffuse_color = random_color_gen.next()

    object_list = []
    mesh_list = []
    object_index_list = []
    for idx, instance in enumerate(ass_file.instances):
        object_index = instance.object_index
        unique_id = instance.unique_id

        geo_class = 'EMPTY'
        object_radius = 2
        object_height = 1
        object_extents = [1.0, 1.0, 1.0]

        if not unique_id == -1:
            if not object_index in object_index_list:
                if not object_index == -1:
                    object_index_list.append(object_index)
                    object_element = ass_file.objects[object_index]
                    geo_class = object_element.geo_class
                    object_radius = object_element.radius
                    object_height = object_element.height
                    object_extents = object_element.extents
                    object_material_index = object_element.material_index

                    light_type = "POINT"
                    if geo_class == 'GENERIC_LIGHT':
                        if object_element.light_properties.light_type == 'SPOT_LGT':
                            light_type = "SPOT"

                        elif object_element.light_properties.light_type == 'DIRECT_LGT':
                            light_type = "AREA"

                        elif object_element.light_properties.light_type == 'OMNI_LGT':
                            light_type = "POINT"

                        elif object_element.light_properties.light_type == 'AMBIENT_LGT':
                            light_type = "SUN"

                    if geo_class == 'GENERIC_LIGHT':
                        object_data = bpy.data.lights.new(instance.name, light_type)
                    else:
                        object_data = bpy.data.meshes.new("%s" % idx)

                    object_mesh = bpy.data.objects.new(instance.name, object_data)
                    collection.objects.link(object_mesh)

                    object_mesh.data.ass_jms.XREF_path = object_element.xref_filepath

                    if geo_class == 'GENERIC_LIGHT':
                        object_mesh.data.color = (object_element.light_properties.light_color)
                        object_mesh.data.energy = (object_element.light_properties.intensity)
                        if object_element.light_properties.light_type == 'SPOT_LGT' or object_element.light_properties.light_type == 'DIRECT_LGT':
                            if object_element.light_properties.light_type == 'DIRECT_LGT':
                                light_shape_type = "DISK"
                                if not object_element.light_properties.light_shape == 0:
                                    light_shape_type = "RECTANGLE"

                                object_mesh.data.shape = light_shape_type

                            else:
                                object_mesh.data.spot_size = radians(object_element.light_properties.hotspot_size)
                                object_mesh.data.spot_blend = object_element.light_properties.hotspot_falloff_size / object_element.light_properties.hotspot_size

                            object_mesh.data.halo_light.spot_size = radians(object_element.light_properties.hotspot_size)
                            object_mesh.data.halo_light.spot_blend = object_element.light_properties.hotspot_falloff_size / object_element.light_properties.hotspot_size

                            object_mesh.data.halo_light.light_cone_shape = str(object_element.light_properties.light_shape)
                            object_mesh.data.halo_light.light_aspect_ratio = object_element.light_properties.light_aspect_ratio

                            object_mesh.data.halo_light.use_near_atten = bool(object_element.light_properties.uses_near_attenuation)
                            object_mesh.data.halo_light.near_atten_start = object_element.light_properties.near_attenuation_start
                            object_mesh.data.halo_light.near_atten_end = object_element.light_properties.near_attenuation_end
                            object_mesh.data.halo_light.use_far_atten = bool(object_element.light_properties.uses_far_attenuation)
                            object_mesh.data.halo_light.far_atten_start = object_element.light_properties.far_attenuation_start
                            object_mesh.data.halo_light.far_atten_end = object_element.light_properties.far_attenuation_end

                    elif geo_class == 'PILL':
                        set_primitive_material(object_material_index, ass_file, object_data)

                        bm = bmesh.new()
                        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, diameter1=1, diameter2=1, depth=2)
                        bm.transform(Matrix.Translation((0, 0, 1)))
                        bm.to_mesh(object_data)
                        bm.free()

                        object_mesh.data.ass_jms.Object_Type = 'CAPSULES'
                        object_dimension = object_radius * 2
                        object_mesh.dimensions = (object_dimension, object_dimension, (object_dimension + object_height))

                        mesh_processing.select_object(context, object_mesh)
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                        mesh_processing.deselect_objects(context)

                    elif geo_class == 'SPHERE':
                        set_primitive_material(object_material_index, ass_file, object_data)

                        bm = bmesh.new()
                        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
                        bm.to_mesh(object_data)
                        bm.free()

                        object_mesh.data.ass_jms.Object_Type = 'SPHERE'
                        object_dimension = object_radius * 2
                        object_mesh.dimensions = (object_dimension, object_dimension, object_dimension)

                        mesh_processing.select_object(context, object_mesh)
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                        mesh_processing.deselect_objects(context)

                    elif geo_class == 'BOX':
                        set_primitive_material(object_material_index, ass_file, object_data)

                        bm = bmesh.new()
                        bmesh.ops.create_cube(bm, size=1.0)
                        bm.to_mesh(object_data)
                        bm.free()

                        object_mesh.data.ass_jms.Object_Type = 'BOX'
                        object_mesh.dimensions = ((object_extents[0] * 2), (object_extents[1] * 2), (object_extents[2] * 2))

                        mesh_processing.select_object(context, object_mesh)
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                        mesh_processing.deselect_objects(context)

                    elif geo_class == 'MESH':
                        bm, vert_normal_list = mesh_processing.process_mesh_import_data('halo3', ass_file, object_element, object_mesh, random_color_gen, 'ASS')

                        bm.to_mesh(object_data)
                        bm.free()
                        object_mesh.data.normals_split_custom_set(vert_normal_list)
                        object_mesh.data.use_auto_smooth = True

                        for vertex_groups in mesh_vertex_groups:
                            for group in vertex_groups:
                                if not group in object_mesh.vertex_groups:
                                    object_mesh.vertex_groups.new(name = group)

                    mesh_list.append(object_data)

                else:
                    object_mesh = bpy.data.objects.new(instance.name, None)
                    collection.objects.link(object_mesh)

            else:
                object_mesh = bpy.data.objects.new(instance.name, mesh_list[object_index])
                collection.objects.link(object_mesh)

            object_list.append(object_mesh)

        else:
            if not None in object_list:
                object_list.append(None)

    for idx, instance in enumerate(ass_file.instances):
        object_index = instance.object_index
        unique_id = instance.unique_id

        geo_class = 'EMPTY'

        local_transform = instance.local_transform
        pivot_transform = instance.pivot_transform

        local_scale = (local_transform.scale, local_transform.scale, local_transform.scale)
        pivot_scale = (pivot_transform.scale, pivot_transform.scale, pivot_transform.scale)
        if ass_file.version == 1:
            local_scale = local_transform.scale
            pivot_scale = pivot_transform.scale

        if not unique_id == -1:
            if not object_index == -1:
                object_element = ass_file.objects[object_index]
                geo_class = object_element.geo_class

                output_rotation = local_transform.rotation @ pivot_transform.rotation
                output_position = local_transform.rotation @ pivot_transform.vector * local_scale[0] + local_transform.vector
                output_scale = local_scale[0] * pivot_scale[0]

                object_list[idx].location = output_position
                object_list[idx].rotation_euler =  output_rotation.to_euler()
                object_list[idx].scale = (output_scale, output_scale, output_scale)

            else:
                object_list[idx].location = local_transform.vector
                object_list[idx].rotation_euler = local_transform.rotation.to_euler()
                object_list[idx].scale = local_scale

            parent_index = instance.parent_id
            if not parent_index == -1:
                parent_instance = ass_file.instances[parent_index]
                parent_unique_id = parent_instance.unique_id
                parent_parent_id = parent_instance.parent_id
                if parent_unique_id >= -1 and parent_parent_id >= -1:
                    object_list[idx].parent = object_list[parent_index]


    report({'INFO'}, "Import completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.ass()
