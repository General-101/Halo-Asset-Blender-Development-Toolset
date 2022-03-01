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

import bpy
import bmesh

from math import radians
from mathutils import Vector, Matrix, Euler
from ..global_functions import mesh_processing, global_functions

def generate_jms_skeleton(JMS, armature, parent_id_class, fix_rotations):
    file_version = JMS.version
    first_frame = JMS.transforms[0]

    bpy.ops.object.mode_set(mode = 'EDIT')
    for idx, jms_node in enumerate(JMS.nodes):
        current_bone = armature.data.edit_bones.new(jms_node.name)
        current_bone.tail[2] = mesh_processing.get_bone_distance(JMS, idx, "JMS")
        parent_idx = jms_node.parent

        if not parent_idx == -1 and not parent_idx == None:
            if 'thigh' in jms_node.name and not parent_id_class.pelvis == None and not parent_id_class.thigh0 == None and not parent_id_class.thigh1 == None:
                parent_idx = parent_id_class.pelvis

            elif 'clavicle' in jms_node.name and not parent_id_class.spine1 == None and not parent_id_class.clavicle0 == None and not parent_id_class.clavicle1 == None:
                parent_idx = parent_id_class.spine1

            parent = JMS.nodes[parent_idx].name
            current_bone.parent = armature.data.edit_bones[parent]

        matrix_translate = Matrix.Translation(first_frame[idx].translation)
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

def set_parent_id_class(JMS, parent_id_class):
    for idx, jms_node in enumerate(JMS.nodes):
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

def jms_file_check(armature, JMS, report):
    JMS_node_names = []
    scene_bone_names = []
    for bone in armature.data.bones:
        scene_bone_names.append(bone.name)

    for jms_node in JMS.nodes:
        JMS_node_names.append(jms_node.name)

    for name in JMS_node_names:
        if not name in scene_bone_names:
            report({'WARNING'}, "Node '%s' from JMS skeleton not found in scene skeleton." % name)

def build_scene_retail(context, JMS, filepath, game_version, reuse_armature, fix_parents, fix_rotations, report):
    collection = context.collection
    scene = context.scene
    armature = None
    object_list = list(scene.objects)
    region_permutation_list = []
    game_version = JMS.game_version
    version = JMS.version
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
                    for jms_node in JMS.nodes:
                        if node.name == jms_node.name:
                            exist_count += 1

                if exist_count == len(JMS.nodes):
                    armature = obj

                else:
                    if exist_count > 0:
                        jms_file_check(obj, JMS, report)

    if armature == None or not reuse_armature:
        parent_id_class = global_functions.ParentIDFix()

        armdata = bpy.data.armatures.new('Armature')
        armature = bpy.data.objects.new('Armature', armdata)
        collection.objects.link(armature)

        mesh_processing.select_object(context, armature)
        if fix_parents:
            if game_version == 'halo2' or game_version == 'halo3':
                set_parent_id_class(JMS, parent_id_class)

        generate_jms_skeleton(JMS, armature, parent_id_class, fix_rotations)

    for region in JMS.active_regions:
        name = JMS.regions[region].name
        if JMS.game_version == 'haloce':
            if not name in region_permutation_list:
                region_permutation_list.append(name)

    for triangle in JMS.triangles:
        triangle_material_index = triangle.material_index
        material = None
        region = None
        permutation = None
        if not triangle_material_index == -1:
            material = JMS.materials[triangle_material_index]
            region = material.region
            permutation = material.permutation

        if JMS.game_version == 'halo2' or JMS.game_version == 'halo3':
            if not [region, permutation] in region_permutation_list:
                region_permutation_list.append([permutation, region])

    for marker_obj in JMS.markers:
        parent_idx = marker_obj.parent
        marker_region_index = marker_obj.region
        radius = marker_obj.radius
        object_name_prefix = '#%s' % marker_obj.name
        marker_name_override = ""
        if context.scene.objects.get('#%s' % marker_obj.name):
            marker_name_override = marker_obj.name

        mesh = bpy.data.meshes.new(object_name_prefix)
        object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
        collection.objects.link(object_mesh)

        if game_version == 'haloce':
            if 'physics' in filepath or 'collision' in filepath:
                object_mesh.marker.marker_mask_type = '1'

        else:
            if 'collision' in filepath:
                object_mesh.marker.marker_mask_type = '1'

            elif 'collision' in filepath:
                object_mesh.marker.marker_mask_type = '2'

        object_mesh.marker.name_override = marker_name_override

        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
        bm.to_mesh(mesh)
        bm.free()

        if not marker_region_index == -1:
            object_mesh.face_maps.new(name=JMS.regions[marker_region_index].name)

        mesh_processing.select_object(context, object_mesh)
        mesh_processing.select_object(context, armature)
        if not parent_idx == -1:
            bpy.ops.object.mode_set(mode='EDIT')
            armature.data.edit_bones.active = armature.data.edit_bones[JMS.nodes[parent_idx].name]
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)

        else:
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        matrix_translate = Matrix.Translation(marker_obj.translation)
        matrix_rotation = marker_obj.rotation.to_matrix().to_4x4()

        transform_matrix = matrix_translate @ matrix_rotation
        if not parent_idx == -1:
            pose_bone = armature.pose.bones[JMS.nodes[parent_idx].name]
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

    for xref_marker in JMS.xref_markers:
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
            xref_idx = xref_marker.index
            xref_path = JMS.xref_instances[xref_idx].path
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
    if not len(JMS.vertices) == 0:
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
        bm, vert_normal_list = mesh_processing.process_mesh_import_data(game_version, JMS, None, object_mesh, random_color_gen, 'JMS', 0, None, None, None, False)
        bm.to_mesh(mesh)
        bm.free()
        object_mesh.data.normals_split_custom_set(vert_normal_list)
        object_mesh.data.use_auto_smooth = True
        object_mesh.parent = armature
        mesh_processing.add_modifier(context, object_mesh, False, None, armature)


    primitive_shapes = []
    for sphere in JMS.spheres:
        parent_idx = sphere.parent_index
        name = sphere.name
        material_index = sphere.material_index
        radius = sphere.radius

        object_name_prefix = '$%s' % name

        mesh = bpy.data.meshes.new(object_name_prefix)
        object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
        collection.objects.link(object_mesh)

        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
        bm.to_mesh(mesh)
        bm.free()

        mesh_processing.select_object(context, object_mesh)
        mesh_processing.select_object(context, armature)
        if not parent_idx == -1:
            bpy.ops.object.mode_set(mode='EDIT')
            armature.data.edit_bones.active = armature.data.edit_bones[JMS.nodes[parent_idx].name]
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)

        else:
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        matrix_translate = Matrix.Translation(sphere.translation)
        matrix_rotation = sphere.rotation.to_matrix().to_4x4()

        transform_matrix = matrix_translate @ matrix_rotation
        if not parent_idx == -1:
            pose_bone = armature.pose.bones[JMS.nodes[parent_idx].name]
            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

            else:
                transform_matrix = pose_bone.matrix @ transform_matrix

        object_mesh.matrix_world = transform_matrix
        primitive_shapes.append((object_mesh, sphere.parent_index))

        if not material_index == -1:
            mat = JMS.materials[material_index]
            current_region_permutation = global_functions.material_definition_helper(material_index, mat)
            object_mesh.face_maps.new(name=current_region_permutation)
            material_name = mat.name
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

    for box in JMS.boxes:
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
            armature.data.edit_bones.active = armature.data.edit_bones[JMS.nodes[parent_idx].name]
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)

        else:
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        matrix_translate = Matrix.Translation(box.translation)
        matrix_rotation = box.rotation.to_matrix().to_4x4()

        transform_matrix = matrix_translate @ matrix_rotation
        if not parent_idx == -1:
            pose_bone = armature.pose.bones[JMS.nodes[parent_idx].name]
            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

            else:
                transform_matrix = pose_bone.matrix @ transform_matrix

        object_mesh.matrix_world = transform_matrix
        primitive_shapes.append((object_mesh, box.parent_index))

        if not material_index == -1:
            mat = JMS.materials[material_index]
            current_region_permutation = global_functions.material_definition_helper(material_index, mat)
            object_mesh.face_maps.new(name=current_region_permutation)

            material_name = mat.name
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

    for capsule in JMS.capsules:
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
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, radius1=1, radius2=1, depth=2)
        bm.transform(Matrix.Translation((0, 0, 1)))
        bm.to_mesh(mesh)
        bm.free()

        mesh_processing.select_object(context, object_mesh)
        mesh_processing.select_object(context, armature)
        if not parent_idx == -1:
            bpy.ops.object.mode_set(mode='EDIT')
            armature.data.edit_bones.active = armature.data.edit_bones[JMS.nodes[parent_idx].name]
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)

        else:
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        matrix_translate = Matrix.Translation(capsule.translation)
        matrix_rotation = capsule.rotation.to_matrix().to_4x4()

        transform_matrix = matrix_translate @ matrix_rotation
        if not parent_idx == -1:
            pose_bone = armature.pose.bones[JMS.nodes[parent_idx].name]
            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

            else:
                transform_matrix = pose_bone.matrix @ transform_matrix

        object_mesh.matrix_world = transform_matrix
        primitive_shapes.append((object_mesh, capsule.parent_index))

        if not material_index == -1:
            mat = JMS.materials[material_index]
            current_region_permutation = global_functions.material_definition_helper(material_index, mat)
            object_mesh.face_maps.new(name=current_region_permutation)

            material_name = mat.name
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


    for convex_shape in JMS.convex_shapes:
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
            armature.data.edit_bones.active = armature.data.edit_bones[JMS.nodes[parent_idx].name]
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)

        else:
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        matrix_translate = Matrix.Translation(convex_shape.translation)
        matrix_rotation = convex_shape.rotation.to_matrix().to_4x4()

        transform_matrix = matrix_translate @ matrix_rotation
        if not parent_idx == -1:
            pose_bone = armature.pose.bones[JMS.nodes[parent_idx].name]
            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

            else:
                transform_matrix = pose_bone.matrix @ transform_matrix

        object_mesh.matrix_world = transform_matrix
        primitive_shapes.append((object_mesh, convex_shape.parent_index))

        if not material_index == -1:
            mat = JMS.materials[material_index]
            current_region_permutation = global_functions.material_definition_helper(material_index, mat)
            object_mesh.face_maps.new(name=current_region_permutation)

            material_name = mat.name
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

    for ragdoll in JMS.ragdolls:
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

    for hinge in JMS.hinges:
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

    for car_wheel in JMS.car_wheels:
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

    for point_to_point in JMS.point_to_points:
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

    for prismatic in JMS.prismatics:
        name = prismatic.name
        prismatic_body_a_index = prismatic.body_a_index
        prismatic_body_b_index = prismatic.body_b_index
        if not prismatic_body_a_index == -1:
            body_a_index = JMS.nodes[prismatic_body_a_index].name

        if not prismatic_body_b_index == -1:
            body_b_index = JMS.nodes[prismatic_body_b_index].name

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
            pose_bone = armature.pose.bones[JMS.nodes[prismatic_body_a_index].name]
            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

            else:
                transform_matrix = pose_bone.matrix @ transform_matrix

        object_empty.matrix_world = transform_matrix
        object_empty.select_set(False)
        armature.select_set(False)

    for idx, bounding_sphere in enumerate(JMS.bounding_spheres):
        name = 'bounding_sphere_%s' % idx
        radius = bounding_sphere.radius

        mesh = bpy.data.meshes.new(name)
        object_mesh = bpy.data.objects.new(name, mesh)
        collection.objects.link(object_mesh)

        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
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

    for idx, skylight in enumerate(JMS.skylights):
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
