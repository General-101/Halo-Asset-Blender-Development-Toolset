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
import struct

from .. import config
from xml.dom import minidom
from math import degrees, sqrt, radians
from mathutils import Vector, Quaternion, Euler

class XMLData:
    def __init__(self, xml_node=None, element_name="", enum_class=None, block_count=0, block_name=""):
        self.xml_node = xml_node
        self.element_name = element_name
        self.enum_class = enum_class
        self.block_count = block_count
        self.block_name = block_name

def get_xml_node(XML_OUTPUT, block_count, element_node, attribute_name, attribute_value):
    xml_node = None
    if XML_OUTPUT and block_count > 0:
        for child in element_node.childNodes:
            if child.getAttribute(attribute_name) == attribute_value:
                xml_node = child
                break

    return xml_node

def vector_as_radians(vector):
    radian_vector = (radians(vector[0]), radians(vector[1]), radians(vector[2]))

    return radian_vector

def get_block_name(block_index, block_size, block_name):
    if not block_index >= 0 or not block_index < block_size:
        block_name = "NONE"

    return block_name

def xml_2d(float_a, float_b):
    v1 = '%0.6f' % round(float_a, 6)
    v2 = '%0.6f' % round(float_b, 6)
    point_2d_string = "%s,%s" % (v1, v2)

    return point_2d_string

def xml_vector(vector):
    v1 = '%0.6f' % round(vector[0], 6)
    v2 = '%0.6f' % round(vector[1], 6)
    v3 = '%0.6f' % round(vector[2], 6)
    vector_string = "%s,%s,%s" % (v1, v2, v3)

    return vector_string

def xml_vector_short(vector):
    v1 = vector[0]
    v2 = vector[1]
    v3 = vector[2]
    vector_string = "%s,%s,%s" % (v1, v2, v3)

    return vector_string

def xml_quaternion(quat):
    v1 = '%0.6f' % round(quat[0], 6)
    v2 = '%0.6f' % round(quat[1], 6)
    v3 = '%0.6f' % round(quat[2], 6)
    v4 = '%0.6f' % round(quat[3], 6)
    quat_string = "%s,%s,%s,%s" % (v2, v3, v4, v1)

    return quat_string

def xml_tuple(tuple):
    v1 = '%0.6f' % round(tuple[0], 6)
    v2 = '%0.6f' % round(tuple[1], 6)
    v3 = '%0.6f' % round(tuple[2], 6)
    v4 = '%0.6f' % round(tuple[3], 6)
    vector_string = "%s,%s,%s,%s" % (v1, v2, v3, v4)

    return vector_string

def xml_tuple_short(tuple):
    vector_string = "%s,%s,%s,%s" % (tuple[0], tuple[1], tuple[2], tuple[3])

    return vector_string

def xml_bounds_short(short_a, short_b):
    bounds_string = "%s,%s" % (short_a, short_b)

    return bounds_string

def xml_enum(enum, value):
    try:
        enum_string = "%s,%s" % (value, enum(value).name)
    except:
        enum_string = "%s" % value

    return enum_string

def append_xml_node(xml_data, value_type, value):
    xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", value_type)], value))

def create_xml_node(node_type, node_attributes=[], node_value=None, set_flags=[]):
    field_node = minidom.Document().createElement(node_type)
    for node_attribute in node_attributes:
        field_node.setAttribute(node_attribute[0], str(node_attribute[1]))

    if not node_value == None:
        field_text = minidom.Document().createTextNode(str(node_value))
        field_node.appendChild(field_text)

        for flag in set_flags:
            field_text = minidom.Document().createTextNode(str(flag.name))
            field_node.appendChild(field_text)

    return field_node

def append_xml_attributes(field_node, node_attributes=[], node_value=None, set_flags=[]):
    for node_attribute in node_attributes:
        field_node.setAttribute(node_attribute[0], str(node_attribute[1]))

    if not node_value == None:
        field_text = minidom.Document().createTextNode(str(node_value))
        field_node.appendChild(field_text)

        for flag in set_flags:
            field_text = minidom.Document().createTextNode(str(flag.name))
            field_node.appendChild(field_text)

    return field_node

def get_tag_path(file_path, is_legacy):
    local_path = file_path
    file_directory = os.path.dirname(file_path)
    tag_dir = "%stags" % os.sep
    tag_dir2 = "%s%s" % (tag_dir, os.sep)
    if tag_dir2 in file_directory:
        local_path = file_path.split(tag_dir2, 1)[1].rsplit(".", 1)[0]
    elif file_directory.endswith(tag_dir):
        local_path = file_path.split(tag_dir2, 1)[1].rsplit(".", 1)[0]

    return local_path

def get_tag_extension(tag_group):
    extension_name = tag_group
    if tag_group == "mode":
        extension_name = "model"

    elif tag_group == "mod2":
        extension_name = "gbxmodel"

    elif tag_group == "coll":
        extension_name = "collision"

    elif tag_group == "antr":
        extension_name = "animation"

    elif tag_group == "trak":
        extension_name = "camera_track"

    elif tag_group == "phys":
        extension_name = "physics"

    return extension_name

def get_tag_name(file_name):
    file_name_no_extension = file_name.rsplit(".", 1)[0]

    return file_name_no_extension

def check_file_size(input_stream):
    input_stream.seek(0, os.SEEK_END)
    filesize = input_stream.tell()
    input_stream.seek(0)

    return filesize

def check_group(input_stream, is_big_endian=True):
    valid_group =  ("mode", "mod2", "coll", "phys", "antr", "sbsp", "scnr", "ltmp", "trak", "snd!", "snpm", "senv", "soso", "sgla", "smet", "bitm", "actv", "bipd", "ctrl", "devi", "eqip", "item", "mach", "obje", "pane", "plac", "proj", "scen", "sens", "stat", "unit", "vehi", "weap")
    valid_engine = ('blam', 'BLM!', 'LAMB', 'MLAB')
    group_match = False

    input_stream.seek(36) # Position of tag group in all tags
    tag_group = input_stream.read(4).decode('utf-8', 'replace')
    input_stream.seek(60) # Position of engine tag in all tags
    engine_tag = input_stream.read(4).decode('utf-8', 'replace')
    input_stream.seek(0)
    if not is_big_endian:
        tag_group = tag_group[::-1]
        engine_tag = engine_tag[::-1]

    if tag_group in valid_group and engine_tag in valid_engine:
        group_match = True

    return tag_group, group_match, engine_tag

def get_endian_symbol(big_endian):
    endian_type = "<"
    if big_endian:
        endian_type = ">"

    return endian_type

def get_patch_set(patch_txt_path):
    upgrade_patches = None
    if os.path.isfile(patch_txt_path):
        upgrade_patches = []
        patch_txt = open(patch_txt_path, 'r')
        patch_lines = patch_txt.readlines()

        for line in patch_lines:
            patch_values = line.split("\t", 1)

            upgrade_patches.append((patch_values[0].strip(), patch_values[1].strip()))

        upgrade_patches = set(upgrade_patches)

    return upgrade_patches

def get_patched_name(upgrade_patches, name):
    patched_name = name
    if not upgrade_patches == None:
        for patch in upgrade_patches:
            prepatched_tag_path = patch[0]
            prepatched_tag_group = None
            patched_tag_path = patch[1]
            patched_tag_group = None
            if "," in prepatched_tag_path:
                result = prepatched_tag_path.rsplit(",", 1)
                if len(result) == 2 and len(result[1]) <= 4:
                    prepatched_tag_path = result[0].lower()
                    prepatched_tag_group = "{:<4}".format(result[1].lower())

            if "," in patched_tag_path:
                result = patched_tag_path.rsplit(",", 1)
                if len(result) == 2 and len(result[1]) <= 4:
                    patched_tag_path = result[0].lower()
                    patched_tag_group = "{:<4}".format(result[1].lower())

            if prepatched_tag_path == name:
                tag_name = patched_tag_path
                if patched_tag_group:
                    tag_name = "%s,%s" % (prepatched_tag_path, patched_tag_group)

                patched_name = tag_name
                break

            else:
                if prepatched_tag_path in name:
                    tag_name = prepatched_tag_path
                    if patched_tag_group:
                        tag_name = "%s,%s" % (prepatched_tag_path, patched_tag_group)

                    patched_name = tag_name.replace(prepatched_tag_path, patched_tag_path)
                    break

    return patched_name

def get_xml_path(input_path, tag_group, is_legacy, is_reversed=False):
    if is_legacy:
        tag_name = os.path.basename(input_path)
    else:
        tag_name = get_tag_name(os.path.basename(input_path))

    if is_reversed:
        tag_group = tag_group[::-1]

    xml_path = os.path.join(os.path.dirname(input_path), "%s_%s.XML" % (tag_name, tag_group))
    special_characters=['@','#','$','*','&']
    for i in special_characters:
        xml_path = xml_path.replace(i, " ")

    return xml_path

def string_to_bytes(string, reverse):
    if reverse:
        string = string[::-1]

    return bytes(string, 'utf-8')

class TagAsset():
    def __init__(self):
        self.big_endian = True
        self.xml_doc = None
        self.is_legacy = True
        self.upgrade_patches = None

    def string_to_bytes(self, string, reverse):
        if reverse:
            string = string[::-1]

        return bytes(string, 'utf-8')

    def vector_as_radians(self, vector):
        radian_vector = (radians(vector[0]), radians(vector[1]), radians(vector[2]))

        return radian_vector

    def read_signed_byte(self, input_stream, tag, xml_data=None):
        signed_byte = (struct.unpack('%sb' % get_endian_symbol(tag.big_endian), input_stream.read(1)))[0]
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "char integer")], signed_byte))

        return signed_byte

    def read_unsigned_byte(self, input_stream, big_endian):
        return (struct.unpack('%sB' % get_endian_symbol(big_endian), input_stream.read(1)))[0]

    def read_flag_unsigned_byte(self, input_stream, tag, xml_data=None):
        flags = (struct.unpack('%sB' % get_endian_symbol(tag.big_endian), input_stream.read(1)))[0]
        if not tag.xml_doc == None and not xml_data == None:
            flag_enums = []
            if not xml_data.enum_class == None:
                flag_enums = [flag for flag in xml_data.enum_class if flag in xml_data.enum_class(flags)]

            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "byte flags")], flags, flag_enums))

        return flags

    def read_enum_unsigned_byte(self, input_stream, tag, xml_data=None):
        unsigned_byte = (struct.unpack('%sB' % get_endian_symbol(tag.big_endian), input_stream.read(1)))[0]
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "enum")], xml_enum(xml_data.enum_class, unsigned_byte)))

        return unsigned_byte

    def read_signed_short(self, input_stream, tag, xml_data=None):
        signed_short = (struct.unpack('%sh' % get_endian_symbol(tag.big_endian), input_stream.read(2)))[0]
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "short integer")], signed_short))

        return signed_short

    def read_min_max_signed_short(self, input_stream, tag, xml_data=None):
        short_values = struct.unpack('%s2h' % get_endian_symbol(tag.big_endian), input_stream.read(4))
        short_min = short_values[0]
        short_max = short_values[1]

        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "short bounds")], xml_bounds_short(short_min, short_max)))

        return (short_min, short_max)

    def read_unsigned_short(self, input_stream, tag, xml_data=None):
        unsigned_short = (struct.unpack('%sH' % get_endian_symbol(tag.big_endian), input_stream.read(2)))[0]
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "short integer")], unsigned_short))

        return unsigned_short

    def read_enum_unsigned_short(self, input_stream, tag, xml_data=None):
        unsigned_short = (struct.unpack('%sH' % get_endian_symbol(tag.big_endian), input_stream.read(2)))[0]
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "enum")], xml_enum(xml_data.enum_class, unsigned_short)))

        return unsigned_short

    def read_block_index_signed_short(self, input_stream, tag, xml_data=None):
        signed_short = (struct.unpack('%sh' % get_endian_symbol(tag.big_endian), input_stream.read(2)))[0]
        if not tag.xml_doc == None and not xml_data == None:
                        xml_data.xml_node.appendChild(create_xml_node("block_index", [("name", xml_data.element_name), ("type", "short block index"), ("index", str(signed_short))], get_block_name(signed_short, xml_data.block_count, xml_data.block_name)))

        return signed_short

    def read_flag_unsigned_short(self, input_stream, tag, xml_data=None):
        flags = (struct.unpack('%sH' % get_endian_symbol(tag.big_endian), input_stream.read(2)))[0]
        if not tag.xml_doc == None and not xml_data == None:
            flag_enums = []
            if not xml_data.enum_class == None:
                flag_enums = [flag for flag in xml_data.enum_class if flag in xml_data.enum_class(flags)]

            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "word flags")], flags, flag_enums))

        return flags

    def read_point_2d_short(self, input_stream, tag, xml_data=None):
        short_a, short_b = struct.unpack('%shh' % get_endian_symbol(tag.big_endian), input_stream.read(4))
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "short point 2d")], xml_bounds_short(short_a, short_b)))

        return (short_a, short_b)

    def read_signed_integer(self, input_stream, tag, xml_data=None):
        signed_integer = (struct.unpack('%si' % get_endian_symbol(tag.big_endian), input_stream.read(4)))[0]
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "long integer")], signed_integer))

        return signed_integer

    def read_unsigned_integer(self, input_stream, tag, xml_data=None):
        unsigned_integer = (struct.unpack('%sI' % get_endian_symbol(tag.big_endian), input_stream.read(4)))[0]
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "long integer")], unsigned_integer))

        return unsigned_integer

    def read_flag_unsigned_integer(self, input_stream, tag, xml_data=None):
        flags = (struct.unpack('%sI' % get_endian_symbol(tag.big_endian), input_stream.read(4)))[0]
        if not tag.xml_doc == None and not xml_data == None:
            flag_enums = []
            if not xml_data.enum_class == None:
                flag_enums = [flag for flag in xml_data.enum_class if flag in xml_data.enum_class(flags)]

            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "long flags")], flags, flag_enums))

        return flags

    def read_block_index_signed_integer(self, input_stream, tag, xml_data=None):
        signed_short = (struct.unpack('%si' % get_endian_symbol(tag.big_endian), input_stream.read(4)))[0]
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("block_index", [("name", xml_data.element_name), ("type", "long block index"), ("index", str(signed_short))], get_block_name(signed_short, xml_data.block_count, xml_data.block_name)))

        return signed_short

    def read_enum_unsigned_integer(self, input_stream, tag, xml_data=None):
        unsigned_integer = (struct.unpack('%sI' % get_endian_symbol(tag.big_endian), input_stream.read(4)))[0]
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "enum")], xml_enum(xml_data.enum_class, unsigned_integer)))

        return unsigned_integer

    def read_enum_integer(self, input_stream, big_endian):
        unsigned_integer = (struct.unpack('%sI' % get_endian_symbol(big_endian), input_stream.read(4)))[0]

        return unsigned_integer

    def read_float(self, input_stream, tag, xml_data=None, increase_scale=False):
        float_value = (struct.unpack('%sf' % get_endian_symbol(tag.big_endian), input_stream.read(4)))[0]
        if not tag.xml_doc == None and not xml_data == None and not xml_data.xml_node == None:
            v1 = '%0.6f' % round(float_value, 6)
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "real")], v1))

        if increase_scale:
            float_value = float_value * 100

        return float_value

    def read_min_max(self, input_stream, tag, xml_data=None, increase_scale=False):
        float_values = struct.unpack('%sff' % get_endian_symbol(tag.big_endian), input_stream.read(8))
        float_min = float_values[0]
        float_max = float_values[1]
        if increase_scale:
            float_min = float_min * 100
            float_max = float_max * 100

        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "real bounds")], xml_2d(float_min, float_max)))

        return (float_min, float_max)

    def read_point_2d(self, input_stream, tag, xml_data=None, increase_scale=False):
        float_a, float_b = struct.unpack('%sff' % get_endian_symbol(tag.big_endian), input_stream.read(8))
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "real point 2d")], xml_2d(float_a, float_b)))

        if increase_scale:
            float_a *= 100
            float_b *= 100

        return (float_a, float_b)

    def read_degree_2d(self, input_stream, tag, xml_data=None):
        float_a, float_b = struct.unpack('%sff' % get_endian_symbol(tag.big_endian), input_stream.read(8))
        degree_a = degrees(float_a)
        degree_b = degrees(float_b)
        if not tag.xml_doc == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "real point 2d")], xml_2d(degree_a, degree_b)))

        return (degree_a, degree_b)

    def read_degree(self, input_stream, tag, xml_data=None):
        degree = degrees((struct.unpack('%sf' % get_endian_symbol(tag.big_endian), input_stream.read(4)))[0])
        if not tag.xml_doc == None and not xml_data == None:
            v1 = '%0.6f' % round(degree, 6)
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "angle")], v1))

        return degree

    def read_min_max_degree(self, input_stream, tag, xml_data=None):
        float_a, float_b = struct.unpack('%sff' % get_endian_symbol(tag.big_endian), input_stream.read(8))
        degree_a = degrees(float_a)
        degree_b = degrees(float_b)
        if not tag.xml_doc == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "angle bounds")], xml_2d(degree_a, degree_b)))

        return (degree_a, degree_b)

    def read_point_3d(self, input_stream, tag, xml_data=None, increase_scale=False):
        pos = struct.unpack('%s3f' % get_endian_symbol(tag.big_endian), input_stream.read(12))
        pos_vector = Vector((pos[0], pos[1], pos[2]))
        if not tag.xml_doc == None and not xml_data == None and not xml_data.xml_node == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "real point 3d")], xml_vector(pos_vector)))

        if increase_scale:
            pos_vector *= 100

        return pos_vector

    def read_euler_angles(self, input_stream, tag, xml_data=None):
        angles = struct.unpack('%s3f' % get_endian_symbol(tag.big_endian), input_stream.read(12))
        euler_angles = Euler((degrees(angles[0]), degrees(angles[1]), degrees(angles[2])))
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "real euler angles 3d")], xml_vector(euler_angles)))

        return euler_angles

    def read_vector(self, input_stream, tag, xml_data=None, increase_scale=False):
        pos = struct.unpack('%s3f' % get_endian_symbol(tag.big_endian), input_stream.read(12))
        pos_vector = Vector((pos[0], pos[1], pos[2]))
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "real vector 3d")], xml_vector(pos_vector)))

        if increase_scale:
            pos_vector *= 100

        return pos_vector

    def read_quaternion(self, input_stream, tag, xml_data=None, is_inverted=False):
        rot = struct.unpack('%s4f' % get_endian_symbol(tag.big_endian), input_stream.read(16))
        rot_value = Quaternion((rot[3], rot[0], rot[1], rot[2])) # Order is the way it is cause Halo stores quaternions as IJKW while Blender is WIJK. - General_101
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "real quaternion")], xml_quaternion(rot_value)))

        if is_inverted:
            rot_value = rot_value.inverted()

        return rot_value

    def read_quaternion_squared(self, input_stream, tag, xml_data=None, is_inverted=False):
        rot = struct.unpack('%s4h' % get_endian_symbol(tag.big_endian), input_stream.read(8))

        q0 = rot[0]
        q1 = rot[1]
        q2 = rot[2]
        q3 = rot[3]

        rot_len = q0**2 + q1**2 + q2**2 + q3**2
        if rot_len:
            rot_len = 1 / sqrt(rot_len)
            q0 *= rot_len
            q1 *= rot_len
            q2 *= rot_len
            q3 *= rot_len

        else:
            q0 = q1 = q2 = 0.0
            q3 = 1.0

        rot_value = Quaternion((q3, q0, q1, q2)) # Order is the way it is cause Halo stores quaternions as IJKW while Blender is WIJK. - General_101

        if not tag.xml_doc == None and not xml_data == None and not xml_data.xml_node == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "real quaternion")], xml_quaternion(rot_value)))

        if is_inverted:
            rot_value.inverted()

        return rot_value

    def read_rgb(self, input_stream, tag, xml_data=None):
        rgb = struct.unpack('%s3f' % get_endian_symbol(tag.big_endian), input_stream.read(12))
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "rgb color")], xml_vector(rgb)))

        return (rgb[0], rgb[1], rgb[2], 1)

    def read_bgr_byte(self, input_stream, tag, xml_data=None):
        bgr = struct.unpack('%s4b' % get_endian_symbol(tag.big_endian), input_stream.read(4))
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "rgb color")], xml_vector_short((bgr[2], bgr[1], bgr[0]))))

        return (bgr[2], bgr[1], bgr[0], 1) # Order is the way it is cause Halo stores color as BGR while Blender is RGBA. - General_101

    def read_argb(self, input_stream, tag, xml_data=None):
        argb = struct.unpack('%s4f' % get_endian_symbol(tag.big_endian), input_stream.read(16))
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "argb color")], xml_tuple(argb)))

        return (argb[1], argb[2], argb[3], argb[0]) # Order is the way it is cause Halo stores color as ARGB while Blender is RGBA. - General_101

    def read_argb_byte(self, input_stream, tag, xml_data=None):
        argb = struct.unpack('%s4B' % get_endian_symbol(tag.big_endian), input_stream.read(4))
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "argb color")], xml_tuple_short(argb)))

        return (argb[1], argb[2], argb[3], argb[0]) # Order is the way it is cause Halo stores color as ARGB while Blender is RGBA. - General_101

    def read_rectangle(self, input_stream, tag, xml_data=None):
        rec2d = struct.unpack('%s4h' % get_endian_symbol(tag.big_endian), input_stream.read(8))
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "rectangle 2d")], xml_tuple_short(rec2d)))

        return (rec2d[0], rec2d[1], rec2d[2], rec2d[3])

    def read_string32(self, input_stream, tag, xml_data=None):
        # Final byte is reserved for a null terminator. - General_101
        string_value = (struct.unpack('%s31sx' % get_endian_symbol(tag.big_endian), input_stream.read(32)))[0].decode('utf-8', 'replace').split('\x00', 1)[0].strip('\x20')
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "string")], string_value))

        return string_value

    def read_string256(self, input_stream, tag, xml_data=None):
        # Final byte is reserved for a null terminator. - General_101
        string_value = (struct.unpack('%s255sx' % get_endian_symbol(tag.big_endian), input_stream.read(256)))[0].decode('utf-8', 'replace').split('\x00', 1)[0].strip('\x20')
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "string")], string_value))

        return string_value

    def read_variable_string(self, input_stream, string_length, tag, xml_data=None):
        unpack_string = '%s%ssx' % (get_endian_symbol(tag.big_endian), string_length)

        string_value = (struct.unpack(unpack_string, input_stream.read(string_length + 1)))[0].decode('utf-8', 'replace').split('\x00', 1)[0].strip('\x20')
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "string")], string_value))

        return string_value

    def read_variable_string_no_terminator(self, input_stream, string_length, tag, xml_data=None):
        unpack_string = '%s%ss' % (get_endian_symbol(tag.big_endian), string_length)

        string_value = (struct.unpack(unpack_string, input_stream.read(string_length)))[0].decode('utf-8', 'replace').split('\x00', 1)[0].strip('\x20')
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "string")], string_value))

        return string_value

    def read_variable_string_no_terminator_reversed(self, input_stream, string_length, tag, xml_data=None):
        unpack_string = '%s%ss' % (get_endian_symbol(tag.big_endian), string_length)

        string_value = (struct.unpack(unpack_string, input_stream.read(string_length)))[0].decode('utf-8', 'replace').split('\x00', 1)[0].strip('\x20')[::-1]
        if not tag.xml_doc == None and not xml_data == None:
            xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "string")], string_value))

        return string_value

    class TagBlockHeader:
        def __init__(self, name="", version=0, count=0, size=0):
            self.name = name
            self.version = version
            self.count = count
            self.size = size

        def read(self, input_stream, tag):
            tag_block_header_struct = struct.unpack('%s4s3I' % get_endian_symbol(tag.big_endian), input_stream.read(16))
            self.name = tag_block_header_struct[0]
            self.version = tag_block_header_struct[1]
            self.count = tag_block_header_struct[2]
            self.size = tag_block_header_struct[3]

            return self

        def write(self, output_stream, tag, reverse=False):
            header = (string_to_bytes(self.name, reverse),
                      self.version,
                      self.count,
                      self.size)

            output_stream.write(struct.pack('%s4s3I' % get_endian_symbol(tag.big_endian), *header))

    class TagBlock:
        def __init__(self, count=0, maximum_count=0, address=0, definition=0):
            self.count = count
            self.maximum_count = maximum_count
            self.address = address
            self.definition = definition

        def read(self, input_stream, tag, xml_data=None, maximum_count=0):
            tag_block_struct = struct.unpack('%siII' % get_endian_symbol(tag.big_endian), input_stream.read(12))
            self.count = tag_block_struct[0]
            self.maximum_count = maximum_count
            self.address = tag_block_struct[1]
            self.definition = tag_block_struct[2]
            if not tag.xml_doc == None and self.count > 0:
                xml_data.xml_node.appendChild(create_xml_node("block", [("name", xml_data.element_name)]))

            return self

        def write(self, output_stream, big_endian):
            tag_block = (self.count,
                         self.address,
                         self.definition)

            output_stream.write(struct.pack('%siII' % get_endian_symbol(big_endian), *tag_block))

    class TagRef:
        def __init__(self, tag_group=None, name="", name_length=0, salt=0, index=-1, upgrade_patches=None):
            self.tag_group = tag_group
            self.name = name
            self.name_length = name_length
            self.salt = salt
            self.index = index

        def read(self, input_stream, tag, xml_data=None, is_reversed=False):
            tag_reference_struct = struct.unpack('%s4siii' % get_endian_symbol(tag.big_endian), input_stream.read(16))
            self.tag_group = tag_reference_struct[0].decode('utf-8', 'replace')
            if not tag.big_endian:
                self.tag_group = tag_reference_struct[0].decode('utf-8', 'replace')[::-1]

            self.name = ""
            self.name_length = tag_reference_struct[2]
            self.salt = tag_reference_struct[1]
            self.index = tag_reference_struct[3]
            if not tag.xml_doc == None and not xml_data == None:
                xml_data.xml_node.appendChild(create_xml_node("tag_reference", [("name", xml_data.element_name)]))

            return self

        def write(self, output_stream, big_endian, reverse=False, pad=0):
            if self.tag_group == None:
                output_stream.write(struct.pack('%siiii' % get_endian_symbol(big_endian), -1, self.salt, 0, self.index))
            else:
                tag_ref = (string_to_bytes(self.tag_group, reverse),
                        self.salt,
                        len(self.name) + pad,
                        self.index)

                output_stream.write(struct.pack('%s4siii' % get_endian_symbol(big_endian), *tag_ref))

        def append_xml_attributes(self, xml_node):
            append_xml_attributes(xml_node, [("type", self.tag_group)], self.name)

        def create_xml_node(self, xml_data):
            if not xml_data == None:
                xml_data.xml_node.appendChild(create_xml_node("tag_reference", [("name", xml_data.element_name), ("type", self.tag_group)], self.name))

        def get_patched_tag_ref(self, upgrade_patches):
            if not upgrade_patches == None and self.tag_group:
                for patch in upgrade_patches:
                    prepatched_tag_path = patch[0]
                    prepatched_tag_group = None
                    patched_tag_path = patch[1]
                    patched_tag_group = None
                    if "," in prepatched_tag_path:
                        result = prepatched_tag_path.rsplit(",", 1)
                        if len(result) == 2 and len(result[1]) <= 4:
                            prepatched_tag_path = result[0].lower()
                            prepatched_tag_group = "{:<4}".format(result[1].lower())

                    if "," in patched_tag_path:
                        result = patched_tag_path.rsplit(",", 1)
                        if len(result) == 2 and len(result[1]) <= 4:
                            patched_tag_path = result[0].lower()
                            patched_tag_group = "{:<4}".format(result[1].lower())

                    if not prepatched_tag_group == None:
                        if "%s,%s" % (prepatched_tag_path, prepatched_tag_group) == "%s,%s" % (self.name, self.tag_group):
                            self.tag_group = patched_tag_group
                            self.name = patched_tag_path
                            self.name_length = len(self.name)
                            break

                    else:
                        if prepatched_tag_path in self.name:
                            if patched_tag_group:
                                self.tag_group = patched_tag_group

                            self.name = self.name.replace(prepatched_tag_path, patched_tag_path)
                            self.name_length = len(self.name)
                            break

    class RawData:
        def __init__(self, size=0, flags=0, raw_pointer=0, pointer=0, id=0, data=None):
            self.size = size
            self.flags = flags
            self.raw_pointer = raw_pointer
            self.pointer = pointer
            self.id = id
            self.data = data

        def read(self, input_stream, tag, xml_data=None):
            tag_data_struct = struct.unpack('%siiIII' % get_endian_symbol(tag.big_endian), input_stream.read(20))
            self.size = tag_data_struct[0]
            self.flags = tag_data_struct[1]
            self.raw_pointer = tag_data_struct[2]
            self.pointer = tag_data_struct[3]
            self.id = tag_data_struct[4]
            if not tag.xml_doc == None:
                xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "data")]))

            return self

        def write(self, output_stream, big_endian):
            tag_data = (self.size,
                        self.flags,
                        self.raw_pointer,
                        self.pointer,
                        self.id)

            output_stream.write(struct.pack('%siiIII' % get_endian_symbol(big_endian), *tag_data))

    class Plane2D:
        def __init__(self, point_2d=(0.0, 0.0), distance=0.0):
            self.point_2d = point_2d
            self.distance = distance

        def read(self, input_stream, tag, xml_data=None):
            plane_struct = struct.unpack('%s3f' % get_endian_symbol(tag.big_endian), input_stream.read(12))
            self.point_2d = (plane_struct[0], plane_struct[1])
            self.distance = plane_struct[2]
            if not tag.xml_doc == None and not xml_data == None:
                xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "real plane 2d")], xml_vector((plane_struct[0], plane_struct[1], plane_struct[2]))))

            return self

    class Plane3D:
        def __init__(self, point_3d=Vector(), distance=0.0):
            self.point_3d = point_3d
            self.distance = distance

        def read(self, input_stream, tag, xml_data=None):
            plane_struct = struct.unpack('%s4f' % get_endian_symbol(tag.big_endian), input_stream.read(16))
            self.point_3d = Vector((plane_struct[0], plane_struct[1], plane_struct[2]))
            self.distance = plane_struct[3]
            if not tag.xml_doc == None and not xml_data == None:
                xml_data.xml_node.appendChild(create_xml_node("field", [("name", xml_data.element_name), ("type", "real plane 3d")], xml_tuple((plane_struct[0], plane_struct[1], plane_struct[2], plane_struct[3]))))

            return self

    class Header:
        def __init__(self, local_path="", unk1=0, flags=0, type=0, name="", tag_group="", checksum=0, data_offset=0, data_length=0, unk2=0, version=0, destination=0, plugin_handle=0,
                     engine_tag=""):
            self.local_path = local_path
            self.unk1 = unk1
            self.flags = flags
            self.type = type
            self.name = name
            self.tag_group = tag_group
            self.checksum = checksum
            self.data_offset = data_offset
            self.data_length = data_length
            self.unk2 = unk2
            self.version = version
            self.destination = destination
            self.plugin_handle = plugin_handle
            self.engine_tag = engine_tag

        def read(self, input_stream, tag):
            if config.HALO_1_TAG_PATH in input_stream.name:
                self.local_path = input_stream.name.split("%s%s" % (config.HALO_1_TAG_PATH, os.sep))[1].rsplit(".", 1)[0]
            elif config.HALO_2_TAG_PATH in input_stream.name:
                self.local_path = input_stream.name.split("%s%s" % (config.HALO_2_TAG_PATH, os.sep))[1].rsplit(".", 1)[0]
            else:
                self.local_path = input_stream.name.rsplit(".", 1)[0]

            header_struct = struct.unpack('%shbb32s4siiiihbb4s' % get_endian_symbol(tag.big_endian), input_stream.read(64))
            self.unk1 = header_struct[0]
            self.flags = header_struct[1]
            self.type = header_struct[2]
            self.name = header_struct[3].decode('utf-8', 'replace').split('\x00', 1)[0].strip('\x20')
            self.tag_group = header_struct[4].decode('utf-8', 'replace')
            if not tag.big_endian:
                self.tag_group = self.tag_group[::-1]

            self.checksum = header_struct[5]
            self.data_offset = header_struct[6]
            self.data_length = header_struct[7]
            self.unk2 = header_struct[8]
            self.version = header_struct[9]
            self.destination = header_struct[10]
            self.plugin_handle = header_struct[11]
            self.engine_tag = header_struct[12].decode('utf-8', 'replace')
            if not tag.big_endian:
                self.engine_tag = self.engine_tag[::-1]

            if not tag.xml_doc == None:
                tag_group = get_tag_extension(self.tag_group)
                tag_node = tag.xml_doc.createElement('tag')
                tag_node.setAttribute('group', tag_group)
                tag_node.setAttribute('id', get_tag_path(input_stream.name, tag.is_legacy))
                tag_node.setAttribute('version', str(self.version))
                tag.xml_doc.appendChild(tag_node)

            return self

        def write(self, output_stream, big_endian, reverse=False):
            header = (self.unk1,
                      self.flags,
                      self.type,
                      string_to_bytes(self.name, False),
                      string_to_bytes(self.tag_group, reverse),
                      self.checksum,
                      self.data_offset,
                      self.data_length,
                      self.unk2,
                      self.version,
                      self.destination,
                      self.plugin_handle,
                      string_to_bytes(self.engine_tag, reverse))

            output_stream.write(struct.pack('%shbb32s4siiiihbb4s' % get_endian_symbol(big_endian), *header))
