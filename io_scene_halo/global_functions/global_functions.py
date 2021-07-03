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

import os
import bpy
import sys
import random, colorsys

from decimal import *
from mathutils import Vector, Quaternion, Matrix

class JmsDimensions:
    quat_i_a = '0.0000000000'
    quat_j_a = '0.0000000000'
    quat_k_a = '0.0000000000'
    quat_w_a = '0.0000000000'
    pos_x_a = '0.0000000000'
    pos_y_a = '0.0000000000'
    pos_z_a = '0.0000000000'
    scale_x_a = '0.0000000000'
    scale_y_a = '0.0000000000'
    scale_z_a = '0.0000000000'
    radius_a = '0.0000000000'
    pill_z_a = '0.0000000000'
    quat_i_b = '0.0000000000'
    quat_j_b = '0.0000000000'
    quat_k_b = '0.0000000000'
    quat_w_b = '0.0000000000'
    pos_x_b = '0.0000000000'
    pos_y_b = '0.0000000000'
    pos_z_b = '0.0000000000'
    scale_x_b = '0.0000000000'
    scale_y_b = '0.0000000000'
    scale_z_b = '0.0000000000'
    radius_b = '0.0000000000'
    pill_z_b = '0.0000000000'

def unhide_all_collections():
    for collection_viewport in bpy.context.view_layer.layer_collection.children:
        collection_viewport.exclude = False

    for collection_hide in bpy.data.collections:
        collection_hide.hide_viewport = False

def unhide_object(mesh):
    mesh.hide_set(False)
    mesh.hide_viewport = False

def get_child(bone, bone_list):
    set_node = None
    for node in bone_list:
        if bone == node.parent and not set_node:
            set_node = node

    return set_node

def get_sibling(armature, bone, bone_list):
    sibling_list = []
    set_sibling = None
    for node in bone_list:
        if bone.parent == node.parent:
            sibling_list.append(node)

    if len(sibling_list) <= 1:
        set_sibling = None

    else:
        sibling_node = sibling_list.index(bone)
        next_sibling_node = sibling_node + 1
        if next_sibling_node >= len(sibling_list):
            set_sibling = None

        else:
            if armature:
                set_sibling = armature.data.bones['%s' % sibling_list[next_sibling_node].name]

            else:
                set_sibling = bpy.data.objects['%s' % sibling_list[next_sibling_node].name]

    return set_sibling

def get_encoding(game_version):
    encoding = None
    if game_version == 'haloce' or game_version == 'halo2mcc' or game_version == 'halo3mcc':
        encoding = 'utf_8'

    elif game_version == 'halo2vista':
        encoding = 'utf-16le'

    return encoding

def sort_by_layer(node_list, armature):
    layer_count = []
    layer_root = []
    root_list = []
    children_list = []
    reversed_children_list = []
    joined_list = []
    reversed_joined_list = []
    sort_list = []
    reversed_sort_list = []
    for node in node_list:
        if node.parent == None:
            layer_count.append(None)
            layer_root.append(node)

        else:
            if not node.parent in layer_count:
                layer_count.append(node.parent)

    for layer in layer_count:
        joined_list = root_list + children_list
        reversed_joined_list = root_list + reversed_children_list
        layer_index = layer_count.index(layer)
        if layer_index == 0:
            if armature:
                root_list.append(armature.data.bones[0])

            else:
                root_list.append(layer_root[0])

        else:
            for node in node_list:
                if armature:
                    if node.parent != None:
                        if armature.data.bones['%s' % node.parent.name] in joined_list and not node in children_list:
                            sort_list.append(node.name)
                            reversed_sort_list.append(node.name)

                else:
                    if node.parent != None:
                        if node.parent in joined_list and not node in children_list:
                            sort_list.append(node.name)
                            reversed_sort_list.append(node.name)

            sort_list.sort()
            reversed_sort_list.sort()
            reversed_sort_list.reverse()
            for sort in sort_list:
                if armature:
                    if not armature.data.bones['%s' % sort] in children_list:
                        children_list.append(armature.data.bones['%s' % sort])

                else:
                    if not bpy.data.objects[sort] in children_list:
                        children_list.append(bpy.data.objects[sort])

            for sort in reversed_sort_list:
                if armature:
                    if not armature.data.bones['%s' % sort] in reversed_children_list:
                        reversed_children_list.append(armature.data.bones['%s' % sort])

                else:
                    if not bpy.data.objects[sort] in reversed_children_list:
                        reversed_children_list.append(bpy.data.objects[sort])

        joined_list = root_list + children_list
        reversed_joined_list = root_list + reversed_children_list

    return (joined_list, reversed_joined_list)

def sort_by_index(node_list):
    root_node = []
    child_nodes = []
    for node in node_list:
        if node.parent == None:
            root_node.append(node)

        else:
            child_nodes.append(node)

    sorted_list = root_node + child_nodes

    return (sorted_list, sorted_list)

def sort_list(node_list, armature, game_version, version, animation):
    version = int(version)
    sorted_list = []
    if game_version == 'haloce':
        sorted_list = sort_by_layer(node_list, armature)

    elif game_version == 'halo2' or game_version == 'halo3mcc':
        if animation:
            if version <= 16394:
                sorted_list = sort_by_layer(node_list, armature)

            else:
                sorted_list = sort_by_index(node_list)

        else:
            if version <= 8204:
                sorted_list = sort_by_layer(node_list, armature)

            else:
                sorted_list = sort_by_index(node_list)

    return sorted_list

def test_encoding(filepath):
    UTF_8_BOM = b'\xef\xbb\xbf'
    UTF_16_BE_BOM = b'\xfe\xff'
    UTF_16_LE_BOM = b'\xff\xfe'
    data = open(filepath, 'rb')
    file_size = os.path.getsize(filepath)
    BOM = data.read(3)
    encoding = None
    # first check the boms
    if BOM.startswith(UTF_8_BOM):
        encoding = 'utf-8-sig'
    elif BOM.startswith(UTF_16_BE_BOM) or BOM.startswith(UTF_16_LE_BOM):
        encoding = 'utf-16'
    else:
        if file_size % 2: # can't be USC-2/UTF-16 if the number of bytes is odd
            encoding = 'utf-8'
        else:
            # get the first half a kilobyte
            data.seek(0)
            sample_bytes = data.read(0x200)

            even_zeros = 0
            odd_zeros = 0

            for idx, byte in enumerate(sample_bytes):
                if byte != 0:
                    continue
                if idx % 2:
                    odd_zeros += 1
                else:
                    even_zeros += 1
            ## if there are no null bytes we assume we are dealing with a utf-8 file
            ## if there are null bytes, assume utf-16 and guess endianness based on where the null bytes are
            if even_zeros == 0 and odd_zeros == 0:
                encoding = 'utf-8'
            elif odd_zeros > even_zeros:
                encoding = 'utf-16-le'
            else:
                encoding = 'utf-16-be'


    data.close()
    return encoding

def get_version(file_version_console,
                file_version_ce,
                file_version_h2,
                file_version_h3,
                game_version,
                console
                ):

    version = None
    if console:
        version = int(file_version_console)

    else:
        if game_version == 'haloce':
            version = int(file_version_ce)

        elif game_version == 'halo2':
            version = int(file_version_h2)
        elif game_version == 'halo3mcc':
            version = int(file_version_h3)

    return version

def get_true_extension(filepath, extension, is_import):
    extension_list = ['.jma', '.jmm', '.jmt', '.jmo', '.jmr', '.jmrx', '.jmh', '.jmz', '.jmw', '.jms', '.jmp']
    true_extension = ''
    if is_import:
        true_extension = filepath.rsplit('.', 1)[1].lower()

    else:
        extension_char = (len(extension))
        if not filepath[-(extension_char):].lower() in extension_list or not filepath[-(extension_char):].lower() in extension.lower():
            true_extension = extension

    return true_extension

def get_matrix(obj_a, obj_b, is_local, armature, joined_list, is_node, version, filetype, constraint):
    object_matrix = Matrix.Translation((0, 0, 0))
    if is_node:
        if armature:
            pose_bone = armature.pose.bones['%s' % (obj_a.name)]
            object_matrix = pose_bone.matrix
            if pose_bone.parent and not version >= get_version_matrix_check(filetype):
                #Files at or above 8205 use absolute transform instead of local transform for nodes
                object_matrix = pose_bone.parent.matrix.inverted() @ pose_bone.matrix

        else:
            object_matrix = obj_a.matrix_world
            if obj_a.parent and not version >= get_version_matrix_check(filetype):
                #Files at or above 8205 use absolute transform instead of local transform for nodes
                object_matrix = obj_a.parent.matrix_world.inverted() @ obj_a.matrix_world

    else:
        if armature:
            object_matrix = obj_a.matrix_world
            bone_test = armature.data.bones.get(obj_b.parent_bone)
            if obj_b.parent_bone and is_local and bone_test:
                parent_object = get_parent(armature, obj_b, joined_list, -1)
                pose_bone = armature.pose.bones['%s' % (parent_object[1].name)]
                if constraint:
                    object_matrix = obj_a.matrix_world.inverted() @ pose_bone.matrix
                else:
                    object_matrix = pose_bone.matrix.inverted() @ obj_a.matrix_world

        else:
            object_matrix = obj_a.matrix_world
            if obj_b.parent and is_local:
                parent_object = get_parent(armature, obj_b, joined_list, -1)
                if constraint:
                    object_matrix = obj_a.matrix_world.inverted() @ parent_object[1].matrix_world
                else:
                    object_matrix = parent_object[1].matrix_world.inverted() @ obj_a.matrix_world

    return object_matrix

def get_dimensions(mesh_a_matrix, mesh_a, mesh_b_matrix, mesh_b, custom_scale, version, jms_vertex, is_vertex, is_bone, armature, filetype):
    object_dimensions = JmsDimensions()
    if is_vertex:
        JmsDimensions.pos_x_a = float(jms_vertex[0] * custom_scale)
        JmsDimensions.pos_y_a = float(jms_vertex[1] * custom_scale)
        JmsDimensions.pos_z_a = float(jms_vertex[2] * custom_scale)

    else:
        if mesh_a:
            pos  = mesh_a_matrix.translation
            quat = mesh_a_matrix.to_quaternion().inverted()
            if version >= get_version_matrix_check(filetype):
                quat = mesh_a_matrix.to_quaternion()

            if is_bone:
                pose_bone = armature.pose.bones[mesh_a.name]
                scale = pose_bone.scale

            else:
                scale = mesh_a.scale

            if not is_bone:
                dimension = mesh_a.dimensions

                #The reason this code exists is to try to copy how capsules work in 3DS Max.
                #To get original height for 3DS Max do (radius_jms * 2) + height_jms
                #The maximum value of radius is height / 2
                pill_radius = ((dimension[0] / 2) * custom_scale)
                pill_height = (dimension[2] * custom_scale) - (pill_radius * 2)
                if pill_height <= 0:
                    pill_height = 0

            JmsDimensions.quat_i_a = float(quat[1])
            JmsDimensions.quat_j_a = float(quat[2])
            JmsDimensions.quat_k_a = float(quat[3])
            JmsDimensions.quat_w_a = float(quat[0])
            JmsDimensions.pos_x_a = float(pos[0] * custom_scale)
            JmsDimensions.pos_y_a = float(pos[1] * custom_scale)
            JmsDimensions.pos_z_a = float(pos[2] * custom_scale)
            JmsDimensions.scale_x_a = float(scale[0])
            JmsDimensions.scale_y_a = float(scale[1])
            JmsDimensions.scale_z_a = float(scale[2])
            if not is_bone:
                JmsDimensions.dimension_x_a = float(dimension[0] * custom_scale)
                JmsDimensions.dimension_y_a = float(dimension[1] * custom_scale)
                JmsDimensions.dimension_z_a = float(dimension[2] * custom_scale)
                JmsDimensions.radius_a = float(pill_radius)
                JmsDimensions.pill_z_a = float(pill_height)

        if mesh_b:
            pos  = mesh_b_matrix.translation
            quat = mesh_b_matrix.to_quaternion().inverted()
            if version >= get_version_matrix_check(filetype):
                quat = mesh_a_matrix.to_quaternion()

            if is_bone:
                pose_bone = armature.pose.bones[mesh_b.name]
                scale = pose_bone.scale

            else:
                scale = mesh_b.scale

            if not is_bone:
                dimension = mesh_b.dimensions

                #The reason this code exists is to try to copy how capsules work in 3DS Max.
                #To get original height for 3DS Max do (radius_jms * 2) + height_jms
                #The maximum value of radius is height / 2
                pill_radius = ((dimension[0] / 2) * custom_scale)
                pill_height = (dimension[2] * custom_scale) - (pill_radius * 2)
                if pill_height <= 0:
                    pill_height = 0

            JmsDimensions.quat_i_b = float(quat[1])
            JmsDimensions.quat_j_b = float(quat[2])
            JmsDimensions.quat_k_b = float(quat[3])
            JmsDimensions.quat_w_b = float(quat[0])
            JmsDimensions.pos_x_b = float(pos[0] * custom_scale)
            JmsDimensions.pos_y_b = float(pos[1] * custom_scale)
            JmsDimensions.pos_z_b = float(pos[2] * custom_scale)
            JmsDimensions.scale_x_b = float(scale[0])
            JmsDimensions.scale_y_b = float(scale[1])
            JmsDimensions.scale_z_b = float(scale[2])
            if not is_bone:
                JmsDimensions.dimension_x_b = float(dimension[0] * custom_scale)
                JmsDimensions.dimension_y_b = float(dimension[1] * custom_scale)
                JmsDimensions.dimension_z_b = float(dimension[2] * custom_scale)
                JmsDimensions.radius_b = float(pill_radius)
                JmsDimensions.pill_z_b = float(pill_height)

    return object_dimensions

def get_extension(extension_console,
                  extension_ce,
                  extension_h2,
                  extension_h3,
                  game_version,
                  console
                  ):

    extension = None
    if console:
        extension = extension_console

    else:
        if game_version == 'haloce':
            extension = extension_ce

        elif game_version == 'halo2':
            extension = extension_h2

        elif game_version == 'halo3mcc':
            extension = extension_h3
    return extension

def get_hierarchy(mesh):
    hierarchy_list = [mesh]
    while mesh.parent:
        mesh = mesh.parent
        hierarchy_list.append(mesh)

    return hierarchy_list

def get_children(world_node):
    children_hierarchy = [world_node]
    for node in children_hierarchy:
        for child in node.children:
            children_hierarchy.append(child)

    return children_hierarchy

def get_parent(armature, mesh, joined_list, default_parent):
    parent_object = None
    parent_index = default_parent
    parent = None

    if mesh:
        if armature:
            parent = mesh.parent_bone
        else:
            parent = mesh.parent

        while parent:
            if armature:
                bone_test = armature.data.bones.get(mesh.parent_bone)
                if bone_test:
                    mesh = armature.data.bones[mesh.parent_bone]
                    if mesh in joined_list:
                        parent_object = mesh
                        break
                else:
                    break

            else:
                mesh = mesh.parent
                if mesh in joined_list and mesh.hide_viewport == False and mesh.hide_get() == False:
                    parent_object = mesh
                    break

        if parent_object:
            parent_index = joined_list.index(parent_object)

    return (parent_index, parent_object)

def set_scale(scale_enum, scale_float):
    scale = 1
    if scale_enum == '1':
        scale = float(100)

    if scale_enum == '2':
        scale = float(scale_float)

    return scale

def count_root_nodes(node_list):
    root_node_count = 0
    for node in node_list:
        if node.parent == None:
            root_node_count += 1
        elif not node.parent == None:
            if node.parent.name[0:1] == '!':
                root_node_count += 1

    return root_node_count

def get_version_matrix_check(filetype):
    matrix_version = None
    if filetype == 'JMA':
        matrix_version = 16394

    elif filetype == 'JMS':
        matrix_version = 8205

    elif filetype == 'ASS':
        matrix_version = 0

    return matrix_version

def gather_materials(game_version, material, material_list, export_type, region, permutation, lod):
    assigned_materials_list = []
    if material is not None:
        if material not in assigned_materials_list:
            assigned_materials_list.append(material)

    else:
        if game_version == 'haloce' and not None in material_list:
            material_list.append(None)

    if game_version == 'haloce':
        if material not in material_list:
            material_list.append(material)

    elif game_version == 'halo2' or game_version == 'halo3mcc':
        if export_type == 'JMS':
            if material not in material_list and material in assigned_materials_list:
                material_list.append(material)

        if export_type == 'ASS':
            if material not in material_list and material in assigned_materials_list:
                material_list.append(material)

    else:
        if game_version == 'haloce' and not None in material_list:
            material_list.append(None)

    return material_list

def set_ignore(mesh):
    collection_list = mesh.users_collection
    ignore = False
    if mesh.hide_viewport or mesh.hide_get():
        ignore = True

    for collection in collection_list:
        if not collection.name == 'Master Collection':
            access_collection = bpy.data.collections[collection.name]
            if access_collection.hide_viewport:
                ignore = True

    return ignore

def get_face_material(game_version, original_geo, face):
    object_materials = len(original_geo.material_slots) - 1
    assigned_material = None
    assigned_material = -1
    if len(original_geo.material_slots) != 0:
        if not face.material_index > object_materials:
            if face.material_index is not -1:
                assigned_material = face.material_index

    return assigned_material

def get_material(game_version, original_geo, face, geometry, material_list, export_type, region, permutation):
    object_materials = len(original_geo.material_slots) - 1
    assigned_material = None
    if game_version == 'haloce':
        if len(original_geo.material_slots) != 0:
            if not face.material_index > object_materials:
                if geometry.materials[face.material_index] is not None:
                    assigned_material = original_geo.material_slots[face.material_index].material

                else:
                    assigned_material = None

            else:
                assigned_material = None

        else:
            assigned_material = None

    elif game_version == 'halo2' or game_version == 'halo3mcc':
        assigned_material = -1
        if len(original_geo.material_slots) != 0:
            if not face.material_index > object_materials:
                if geometry.materials[face.material_index] is not None:
                    if export_type == 'JMS':
                        assigned_material = [original_geo.material_slots[face.material_index].material, original_geo.data.ass_jms.level_of_detail, region, permutation]

                    elif export_type == 'ASS':
                        assigned_material = original_geo.material_slots[face.material_index].material

    return assigned_material

class AssetParseError(Exception):
    pass

class SceneParseError(Exception):
    pass

class HaloAsset:
    """Helper class for reading in JMS/JMA/ASS files"""

    def __init__(self, filepath):
        self._elements = []
        self._index = 0
        with open(filepath, "r", encoding=test_encoding(filepath)) as file:
            for line in file:
                processed_line = line.split(";", 1)[0].strip()
                for element in processed_line.split("\t"):
                    if element != '': #Sternly written letters will be sent to the person or team who designed the split() function
                        self._elements.append(element)

    def left(self):
        """Returns the number of elements left"""
        if self._index < len(self._elements):
            return len(self._elements) - self._index
        else:
            return 0

    def skip(self, count):
        """Skip forwards n elements"""
        self._index += count

    def next(self):
        """Return the next element, raises AssetParseError on error"""
        try:
            self._index += 1
            return self._elements[self._index - 1]
        except:
            raise AssetParseError()

    def next_multiple(self, count):
        """Returns an array of the next n elements, raises AssetParseError on error"""
        try:
            list = self._elements[self._index: self._index + count]
            self._index += count
            return list
        except:
            raise AssetParseError()

    def next_vector(self):
        """Return the next vector as mathutils.Vector, raises AssetParseError on error"""
        return Vector((float(self.next()), float(self.next()), float(self.next())))

    def are_quaternions_inverted(self):
        """Override this to enable quaternion inversion for next_quaternion()"""
        return False

    def next_quaternion(self):
        """Return the next quaternion as mathutils.Quaternion, raises AssetParseError on error"""
        x = float(self.next())
        y = float(self.next())
        z = float(self.next())
        w = float(self.next())
        quat = Quaternion((w, x, y, z))
        if self.are_quaternions_inverted():
            quat.invert()
        return quat

def get_game_version(version, filetype):
    game_version = None
    if filetype == 'JMS':
        if version >= 8211:
            game_version = 'halo3'

        elif version >= 8201:
            game_version = 'halo2'

        else:
            game_version = 'haloce'

    elif filetype == 'JMA':
        if version >= 16393:
            game_version = 'halo2'

        else:
            game_version = 'haloce'

    return game_version

def lim32(n):
    """Simulate a 32 bit unsigned interger overflow"""
    return n & 0xFFFFFFFF

def rotl_32(x, n):
    """Rotate x left n-tims as a 32 bit interger"""
    return lim32(x << n) | (x >> 32 - n)

def rotr_32(x, n):
    """Rotate x right n-times as a 32 bit interger"""
    return (x >> n) | lim32(x << 32 - n)

def halo_string_checksum(string):
    """String checksum function matching halo exporter"""
    checksum = 0
    for byte in string.encode():
        checksum = rotl_32(checksum, 1)
        checksum += byte
    return lim32(checksum)

# Ported from https://github.com/preshing/RandomSequence
class PreshingSequenceGenerator32:
    """Peusdo-random sequence generator that repeats every 2**32 elements"""
    @staticmethod
    def __permuteQPR(x):
        prime = 4294967291
        if x >= prime: # The 5 integers out of range are mapped to themselves.
            return x
        residue = lim32(x**2 % prime)
        if x <= (prime // 2):
            return residue
        else:
            return lim32(prime - residue)
    def __init__(self, seed_base = None, seed_offset = None):
        import time
        if seed_base == None:
            seed_base = lim32(int(time.time() * 100000000)) ^ 0xac1fd838
        if seed_offset == None:
            seed_offset = lim32(int(time.time() * 100000000)) ^ 0x0b8dedd3
        self.__index = PreshingSequenceGenerator32.__permuteQPR(lim32(PreshingSequenceGenerator32.__permuteQPR(seed_base) + 0x682f0161))
        self.__intermediate_offset = PreshingSequenceGenerator32.__permuteQPR(lim32(PreshingSequenceGenerator32.__permuteQPR(seed_offset) + 0x46790905))

    def next(self):
        self.__index = lim32(self.__index + 1)
        index_permut = PreshingSequenceGenerator32.__permuteQPR(self.__index)
        return PreshingSequenceGenerator32.__permuteQPR(lim32(index_permut + self.__intermediate_offset) ^ 0x5bf03635)

class RandomColorGenerator(PreshingSequenceGenerator32):
    def next(self):
        rng = super().next()
        h = (rng >> 16) / 0xFFF # [0, 1]
        saturation_raw = (rng & 0xFF) / 0xFF
        brightness_raw = (rng >> 8 & 0xFF) / 0xFF
        v = brightness_raw * 0.3 + 0.5 # [0.5, 0.8]
        s = saturation_raw * 0.4 + 0.6 # [0.3, 1]
        rgb = colorsys.hsv_to_rgb(h, s, v)
        colors = (rgb[0], rgb[1] , rgb[2], 1)
        return colors

def node_hierarchy_checksum(nodes, node, checksum = 0):
    checksum = lim32(rotl_32(checksum, 1) + halo_string_checksum(node.name))
    checksum = rotl_32(checksum, 2)
    child_idx = node.child
    child_node = nodes[child_idx]
    while child_idx != -1:
        checksum = node_hierarchy_checksum(nodes, child_node, checksum)
        child_idx = nodes[child_idx].sibling
        child_node = nodes[child_idx]

    # we undo the rotation state from the recursion, but we leave
    # in the rotation from adding the string for this node.  This
    # way, the order of siblings matters to the checksum.
    return rotr_32(checksum, 2)

def get_filename(game_version,
                 permutation_ce,
                 level_of_detail_ce,
                 folder_structure,
                 model_type,
                 jmi,
                 filepath):

    ce_settings = ''
    extension = '.JMS'
    if jmi:
        extension = '.JMI'

    filename = filepath.rsplit(os.sep, 1)[1]

    if filename.lower().endswith('.jms') or filename.lower().endswith('.jmp') or filename.lower().endswith('.jmi'):
        filename = filename.rsplit('.', 1)[0]

    if game_version == 'haloce':
        if not permutation_ce == '' or not level_of_detail_ce == None:
            if not permutation_ce == '':
                ce_settings += '%s ' % (permutation_ce.replace(' ', '_').replace('\t', '_'))
            else:
                ce_settings += '%s ' % ('unnamed')

            if not level_of_detail_ce == None:
                ce_settings += '%s' % (level_of_detail_ce)
            else:
                ce_settings += '%s' % ('superhigh')

            filename = ce_settings

    model_string = ""
    if model_type == "collision":
        model_string = "_collision"

    elif model_type == "physics":
        model_string = "_physics"

    model_name = model_string
    if folder_structure and game_version == 'haloce' and not model_type == "physics":
        model_name = ""

    filename = filename + model_name + extension

    return filename

def get_directory(game_version,
                  model_type,
                  folder_structure,
                  asset_type,
                  jmi,
                  filepath):

    directory = filepath.rsplit(os.sep, 1)[0]
    blend_filename = bpy.path.basename(bpy.context.blend_data.filepath)

    parent_folder = 'default'
    if len(blend_filename) > 0:
        parent_folder = blend_filename.rsplit('.', 1)[0]

    if game_version == 'haloce':
        folder_type = "models"
    else:
        if asset_type == "0":
            folder_type = "structure"
        else:
            folder_type = "render"

    if model_type == "collision":
        if game_version == 'haloce':
            folder_type = "physics"
        else:
            folder_type = "collision"

    elif model_type == "physics":
        folder_type = "physics"

    elif model_type == "animations":
        folder_type = "animations"

    root_directory = directory

    if jmi:
        root_directory = directory + os.sep + folder_type
        if not os.path.exists(root_directory):
            os.makedirs(root_directory)

    if folder_structure and not jmi:
        folder_subdirectories = ("models", "structure", "render", "collision", "physics", "animations")
        true_directory = directory
        if not os.path.basename(directory) in folder_subdirectories:
            for name in os.listdir(directory):
                if os.path.isdir(os.path.join(directory, name)):
                    if name in folder_subdirectories and os.path.basename(directory) == parent_folder.lower():
                        true_directory = os.path.dirname(directory)
                        break
        else:
            if os.path.basename(os.path.dirname(directory)) == parent_folder.lower():
                true_directory = os.path.dirname(os.path.dirname(directory))

        root_directory = true_directory + os.sep + parent_folder + os.sep + folder_type
        if not os.path.exists(root_directory):
            os.makedirs(root_directory)

    return root_directory

def append_material_symbols(material, game_version):
    name = material.name
    if game_version == 'haloce':
        if material.ass_jms.two_sided:
            if "%" not in name:
                name = name + "%"
        if material.ass_jms.transparent_1_sided:
            if "#" not in name:
                name = name + "#"
        if material.ass_jms.render_only:
            if "!" not in name:
                name = name + "!"
        if material.ass_jms.sphere_collision_only:
            if "*" not in name:
                name = name + "*"
        if material.ass_jms.fog_plane:
            if "$" not in name:
                name = name + "$"
        if material.ass_jms.ladder:
            if "^" not in name:
                name = name + "^"
        if material.ass_jms.breakable:
            if "-" not in name:
                name = name + "-"
        if material.ass_jms.ai_deafening:
            if "&" not in name:
                name = name + "&"
        if material.ass_jms.collision_only:
            if "@" not in name:
                name = name + "@"
        if material.ass_jms.portal_exact:
            if "." not in name:
                name = name + "."
    return name

def run_code(code_string):
    def toolset_exec(code):
        from .. import config
        if config.ENABLE_PROFILING:
            import cProfile
            cProfile.runctx(code, globals(), caller_locals)
        else:
            exec(code, globals(), caller_locals)
    import inspect
    from .. import crash_report
    frame = inspect.currentframe()
    try:
        caller_locals = frame.f_back.f_locals
        report = caller_locals['self'].report

        # this hack is horrible but it works??
        toolset_exec(f"""locals()['__this_is_a_horrible_hack'] = {code_string}""")
        result = caller_locals['__this_is_a_horrible_hack']
        caller_locals.pop('__this_is_a_horrible_hack', None)
        return result

    except SceneParseError as parse_error:
        crash_report.report_crash()
        report({'ERROR'}, "Bad scene: {0}".format(parse_error))
        return {'CANCELLED'}
    except AssetParseError as parse_error:
        crash_report.report_crash()
        report({'ERROR'}, "Bad file: {0}".format(parse_error))
        return {'CANCELLED'}
    except:
        crash_report.report_crash()
        info = sys.exc_info()
        report({'ERROR'}, "Internal error: {1}({0})".format(info[1], info[0]))
        return {'CANCELLED'}
    finally:
        del frame
