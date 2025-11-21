# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2025 Steven Garcia
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

import io
import os
import re
import base64
import struct
import json
import hashlib
import traceback
import xml.etree.ElementTree as ET

from enum import Flag, Enum, auto
from math import degrees, radians, copysign

try:
    from . import tag_common
    from .tag_definitions import h1, h2, common
    from .tag_postprocessing.h1 import postprocess_functions as h1_postprocess_functions
    from .tag_postprocessing.h2 import postprocess_functions as h2_postprocess_functions, create_function
except ImportError:
    import tag_common
    from tag_definitions import h1, h2, common
    from tag_postprocessing.h1 import postprocess_functions as h1_postprocess_functions
    from tag_postprocessing.h2 import postprocess_functions as h2_postprocess_functions, create_function

class EngineTag(Enum):
    # halo 1 types
    H1 = "blam"
    H1Latest = H1
    # halo 2 types
    H2V1 = "ambl"
    H2V2 = "LAMB"
    H2V3 = "MLAB"
    H2V4 = "BLM!"
    H2Latest = H2V4

engine_tag_values = {e.value for e in EngineTag}

def obfuscation_buffer_prepare():
    obfuscation_buffer = [0] * 256
    for i in range(256):
        result = i
        for _ in range(8):
            if (result & 1) != 0:
                result = (result >> 1) ^ 0xEDB88320

            else:
                result >>= 1

        obfuscation_buffer[i] = result

    return obfuscation_buffer

def checksum_calculate(source_buffer, obfuscation_buffer):
    calculated_checksum = 0xFFFFFFFF
    for b in source_buffer:
        buffer_index = (calculated_checksum ^ b) & 0xFF
        obfuscated_output = obfuscation_buffer[buffer_index]
        calculated_checksum = obfuscated_output ^ (calculated_checksum >> 8)
        calculated_checksum &= 0xFFFFFFFF

    return calculated_checksum

def string_to_bytes(string, field_endian):
    if field_endian == "<":
        string = string[::-1]

    return bytes(string, 'utf-8')

class FileModeEnum(Enum):
    read = 0
    write = auto()

FILE_MODE = FileModeEnum.read
FIELD_ENDIAN = "<"

HAS_LEGACY_PADDING = False
HAS_LEGACY_STRINGS = False
HAS_LEGACY_HEADER = False

DUMP_JSON = False

GENERATE_CHECKSUM = True
CONVERT_RADIANS = True
PRESERVE_STRINGS = False
PRESERVE_PADDING = False
PRESERVE_VERSION = False
PRESERVE_SIZE = False

def read_field_header(tag_stream, field_endian="<", is_legacy=False):
    pack_string = "4s3i"
    tag_block_size = 16
    if is_legacy:
        pack_string = "4s2hi"
        tag_block_size = 12

    name, version, count, size = struct.unpack('%s%s' % (field_endian, pack_string), tag_stream.read(tag_block_size))
    name = name.decode('utf-8', 'replace')
    if field_endian == "<":
        name = name[::-1]

    return name, version, count, size

def write_field_header(tag_block_header, block_count, output_stream, field_endian="<", is_legacy=False):
    name, version, size = tag_block_header.values()
    name = string_to_bytes(name, field_endian)

    pack_string = "4s3i"
    if is_legacy:
        pack_string = "4s2hi"

    output_stream.write(struct.pack('%s%s' % (field_endian, pack_string), name, version, block_count, size))

def is_header_valid(tag_header, tag_groups):
    result = False
    valid_group = tag_groups.get(tag_header["tag group"])
    valid_engine = tag_header["engine tag"] in engine_tag_values
    if valid_group and valid_engine:
        result = True
    return result

def read_variable_string(tag_stream, length, field_endian="<", terminator_length=1, append_terminator=False):
    if PRESERVE_STRINGS:
        string_value = ""
        if length > 0:
            if not append_terminator:
                length -= terminator_length

            struct_string = '%s%ss%sx' % (field_endian, length, terminator_length)
            string_value = base64.b64encode(tag_stream.read(struct.calcsize(struct_string))).decode('utf-8')
    else:
        string_value = ""
        if length > 0:
            if not append_terminator:
                length -= terminator_length

            struct_string = '%s%ss%sx' % (field_endian, length, terminator_length)
            string_value = (struct.unpack(struct_string, tag_stream.read(struct.calcsize(struct_string))))[0].decode('utf-8', 'replace').split('\x00', 1)[0].strip('\x20')

    return string_value

def write_variable_string(output_stream, string_value, field_endian="<", fixed_length=32, terminator_length=1, append_terminator=False):
    if not string_value == None:
        if PRESERVE_STRINGS:
            struct_string = '%s%ss%sx' % (field_endian, fixed_length, terminator_length)
            output_stream.write(base64.b64decode(string_value))
        else:
            if len(string_value) > 0:
                if not append_terminator:
                    fixed_length -= terminator_length
            else:
                terminator_length = 0

            struct_string = '%s%ss%sx' % (field_endian, fixed_length, terminator_length)
            byte_data = string_to_bytes(string_value, field_endian)
            output_stream.write(struct.pack(struct_string, byte_data))

def fit_bytes_to_length(data, length, pad_byte=b"\x00"):
    if len(data) < length:
        return data + pad_byte * (length - len(data))
    else:
        return data[:length]

def get_pad_size(tag_field):
    pad_size = 0
    pad_key = tag_field.attrib.get('length')
    if not pad_key == None:
        pad_size = int(pad_key)
    else: 
        print("Undefined attribute for key: %s" % tag_field.tag)

    return pad_size

def is_tag_block_legacy(tag_header):
    global HAS_LEGACY_HEADER
    HAS_LEGACY_HEADER = False
    if tag_header["engine tag"] == EngineTag.H1Latest.value:
        HAS_LEGACY_HEADER = True
    elif tag_header["engine tag"] == EngineTag.H2V1.value:
        HAS_LEGACY_HEADER = True

def is_string_legacy(tag_header):
    global HAS_LEGACY_STRINGS
    HAS_LEGACY_STRINGS = False
    if tag_header["engine tag"] == EngineTag.H1Latest.value:
        HAS_LEGACY_STRINGS = True
    elif tag_header["engine tag"] == EngineTag.H2V1.value:
        HAS_LEGACY_STRINGS = True
    elif tag_header["engine tag"] == EngineTag.H2V2.value:
        HAS_LEGACY_STRINGS = True

def is_padding_legacy(tag_header):
    global HAS_LEGACY_PADDING
    HAS_LEGACY_PADDING = False
    if tag_header["engine tag"] == EngineTag.H1Latest.value:
        HAS_LEGACY_PADDING = True
    elif tag_header["engine tag"] == EngineTag.H2V1.value:
        HAS_LEGACY_PADDING = True
    elif tag_header["engine tag"] == EngineTag.H2V2.value:
        HAS_LEGACY_PADDING = True
    elif tag_header["engine tag"] == EngineTag.H2V3.value:
        HAS_LEGACY_PADDING = True

def replace_neg_zero(val):
    if isinstance(val, float) and val == 0.0 and copysign(1.0, val) == -1.0:
        val = "-0"
    return val

def set_result(field_key, tag_block_fields, result):
    if isinstance(result, (list, tuple)):
        new_result = type(result)(replace_neg_zero(item) for item in result)
        tag_block_fields[field_key] = new_result
    else:
        tag_block_fields[field_key] = replace_neg_zero(result)

def set_enum_result(field_key, field_node, tag_block_fields, result):
    tag_block_fields[field_key] = {"type": field_node.tag, "value": result, "value name": ""}

def set_color_result(field_key, tag_block_fields, result, has_alpha=False):
    if has_alpha:
        A, R, G, B = result
        formatted_field = {"A": A, "R": R, "G": G, "B": B}
    else:
        R, G, B = result
        formatted_field = {"R": R, "G": G, "B": B}

    tag_block_fields[field_key] = formatted_field

def set_bounds_result(field_key, tag_block_fields, result):
    min_value, max_value = result
    tag_block_fields[field_key] = {"Min": min_value, "Max": max_value}

def set_tag_reference_result(field_key, tag_block_fields, result):
    tag_group, unk1, length, unk2, path = result
    tag_block_fields[field_key]["group name"] = tag_group
    tag_block_fields[field_key]["unk1"] = unk1
    tag_block_fields[field_key]["length"] = length
    tag_block_fields[field_key]["unk2"] = unk2
    tag_block_fields[field_key]["path"] = path

def set_block_result(field_key, tag_block_fields):
    tag_block_fields[field_key] = []

def set_data_result(field_key, tag_block_fields, tag_stream, result):
    length, unk1, unk2, unk3, unk4 = result
    tag_block_fields[field_key]["length"] = length
    tag_block_fields[field_key]["unk1"] = unk1
    tag_block_fields[field_key]["unk2"] = unk2
    tag_block_fields[field_key]["unk3"] = unk3
    tag_block_fields[field_key]["unk4"] = unk4
    tag_block_fields[field_key]["encoded"] = base64.b64encode(tag_stream.read(length)).decode('utf-8')

def set_encoded_result(field_key, tag_block_fields, result):
    tag_block_fields[field_key] = base64.b64encode(result).decode('utf-8')

def restore_neg_zero(val):
    if val == "-0":
        val =  -0.0
    return val

def prepare_float_field(result):
    if isinstance(result, (list, tuple)):
        result = type(result)(restore_neg_zero(item) for item in result)
    else:
        result = restore_neg_zero(result)

    return result

def get_result(field_key, tag_block_fields):
    result = tag_block_fields.get(field_key)

    if isinstance(result, (list, tuple)):
        result = type(result)(restore_neg_zero(item) for item in result)
    else:
        result = restore_neg_zero(result)

    return result

def uppercase_struct_letters(struct_string):
    struct_letters = 'bhiqnl'
    result = []
    for char in struct_string:
        if char in struct_letters:
            result.append(char.upper())
        else:
            result.append(char)
    return ''.join(result)

def validate_function_struct(current_struct_field_set, tag_block_fields):
    valid_function = True
    # TODO: This requires some sort of setup to check that the data is correct. Not just that it doesn't exist. - Gen
    for field_node in current_struct_field_set:
        field_tag = field_node.tag
        if field_tag not in common.WHITELIST_TAGS:
            continue

        field_name = field_node.get("name")
        if field_name not in tag_block_fields:
            valid_function = False

    if not valid_function:
        create_function(current_struct_field_set, tag_block_fields, FIELD_ENDIAN, 1, 0, 0, 0, [], [], False)

def check_header(input_stream):
    valid_header = False
    valid_engine = ('blam', 'BLM!', 'LAMB', 'BALM')

    input_stream.seek(36) # Position of tag group in all tags
    tag_group = input_stream.read(4).decode('utf-8', 'replace')
    checksum = input_stream.read(4)
    input_stream.seek(60) # Position of engine tag in all tags
    engine_tag = input_stream.read(4).decode('utf-8', 'replace')
    input_stream.seek(0)

    tag_groups = tag_common.h1_tag_groups
    if engine_tag != "blam":
        tag_groups = tag_common.h2_tag_groups
        tag_group = tag_group[::-1]
        engine_tag = engine_tag[::-1]
        checksum = struct.unpack('<I', checksum)[0]
    else:
        checksum = struct.unpack('>I', checksum)[0]

    if tag_group in tag_groups and engine_tag in valid_engine:
        valid_header = True

    return valid_header, tag_group, checksum, engine_tag

def get_fields(tag_stream, block_stream, tag_header, tag_block_header, field_node, tag_block_fields, block_idx=0, struct_offset=0, return_size=False):
    result = None
    field_tag = field_node.tag
    field_attrib = field_node.attrib
    field_key = field_node.get("name")
    
    unsigned_key = field_node.get("unsigned")
    endian_override = FIELD_ENDIAN
    field_endian = field_node.get("endianOverride")
    if field_endian:
        endian_override = field_endian

    field_default = 0
    field_size = 0
    unread_data_size = 0
    if not return_size:
        unread_data_size = (((block_idx + 1) * tag_block_header["size"])) - (block_stream.tell() - struct_offset)
    if field_tag == "Angle":
        field_default = 0.0
        field_size = 4
        if return_size:
            return field_size
        struct_string = '%sf' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string , block_stream.read(field_size)))[0]
                if CONVERT_RADIANS:
                    result = degrees(result)
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    if CONVERT_RADIANS:
                        result = radians(result)
                    block_stream.write(struct.pack(struct_string, result))
                else:
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "AngleBounds":
        field_default = (0.0, 0.0)
        field_size = 8
        if return_size:
            return field_size
        struct_string = '%s2f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size))
                if CONVERT_RADIANS:
                    result = tuple(degrees(x) for x in result)
            set_bounds_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    result = result.values()
                    if CONVERT_RADIANS:
                        result = map(radians, result)
                    block_stream.write(struct.pack(struct_string, *result))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "ArgbColor":
        field_default = (0, 0, 0, 0)
        field_size = 4
        if return_size:
            return field_size
        struct_string = '%s4b' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size)) 
            set_color_result(field_key, tag_block_fields, result, True)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *result.values()))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "Block":
        field_default = (0, 0, 0)
        field_size = 12
        if return_size:
            return field_size
        struct_string = '%siii' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            tag_block_fields["TagBlock_%s" % field_key] = {"unk1": 0, "unk2": 0}
            tag_block_fields["TagBlockHeader_%s" % field_key] = {"name": "tbfd", "version": 0, "size": 0}
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(12))
            set_block_result(field_key, tag_block_fields)
            block_count, unk1, unk2 = result
            tag_block_fields["TagBlock_%s" % field_key] = {"unk1": unk1, "unk2": unk2}
            if block_count > 0:
                if tag_header["engine tag"] == EngineTag.H1Latest.value:
                    latest_field_set = None
                    for layout in field_node:
                        for current_field_set in layout:
                            if bool(current_field_set.attrib.get('isLatest')):
                                latest_field_set = current_field_set

                    if latest_field_set is None:
                        raise ValueError(f"Latest field set not found.")
                    
                    current_name = "tbfd"
                    current_version = int(latest_field_set.attrib.get('version'))
                    current_size = int(latest_field_set.attrib.get('sizeofValue'))

                    tag_block_fields["TagBlockHeader_%s" % field_key] = {"name": current_name, "version": current_version, "size": current_size}

                else:
                    current_name, current_version, current_count, current_size = read_field_header(tag_stream, is_legacy=HAS_LEGACY_HEADER)
                    tag_block_fields["TagBlockHeader_%s" % field_key] = {"name": current_name, "version": current_version, "size": current_size}

                current_tag_block_header = tag_block_fields["TagBlockHeader_%s" % field_key]
                block_size = block_count * current_size
                current_block_stream = io.BytesIO(tag_stream.read(block_size))
                for block_idx in range(block_count):
                    tag_block_element = {}
                    tag_block_fields[field_key].append(tag_block_element)

                    for layout in field_node:
                        block_field_set = layout[current_tag_block_header["version"]]
                        start_pos = current_block_stream.tell()
                        for block_field_node in block_field_set:
                            get_fields(tag_stream, current_block_stream, tag_header, current_tag_block_header, block_field_node, tag_block_element, block_idx)

                        current_read_size =  current_tag_block_header["size"] - (current_block_stream.tell() - start_pos)
                        if current_read_size > 0:
                            leftover_data = current_block_stream.read(current_read_size)
                            set_encoded_result("LeftOverData_%s" % field_key, tag_block_element, leftover_data)

        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                unk1 = 0
                unk2 = 0
                tag_block_padding = tag_block_fields.get("TagBlock_%s" % field_key)
                if tag_block_padding is not None and PRESERVE_PADDING:
                    unk1, unk2 = tag_block_padding.values()
                if result is not None:
                    block_stream.write(struct.pack(struct_string, len(result), unk1, unk2))
                else:
                    block_stream.write(struct.pack(struct_string, 0, unk1, unk2))

                block_field_set = None
                current_block = tag_block_fields.get(field_node.get("name"))
                current_field_header_data = tag_block_fields.get("TagBlockHeader_%s" % field_key)
                if current_field_header_data is None or not PRESERVE_VERSION:
                    for layout in field_node:
                        for field_set in layout:
                            if bool(field_set.attrib.get('isLatest')):
                                block_field_set = field_set

                    if block_field_set is None:
                        raise ValueError(f"Latest field set not found.")

                    field_set_size = 0
                    for current_field_node in block_field_set:
                        field_size = get_fields(None, None, None, None, current_field_node, None, None, return_size=True)
                        if field_size is not None:
                            field_set_size += field_size

                    current_version = int(block_field_set.attrib.get('version'))
                    current_field_header_data = {"name": "tbfd", "version": current_version, "size": field_set_size}
                else:
                    for layout in field_node:
                        for field_set in layout:
                            if int(field_set.attrib.get('version')) == current_field_header_data["version"]:
                                block_field_set = field_set
                    if block_field_set is None:
                        raise ValueError(f"Latest field set not found.")

                    if not PRESERVE_SIZE:
                        field_set_size = 0
                        for field_node in block_field_set:
                            field_size = get_fields(None, None, None, None, field_node, None, None, return_size=True)
                            if field_size is not None:
                                field_set_size += field_size

                        current_version = int(block_field_set.attrib.get('version'))
                        current_field_header_data = {"name": "tbfd", "version": current_version, "size": field_set_size}

                if current_block is not None:
                    tag_block_header_size = 16
                    if HAS_LEGACY_HEADER:
                        tag_block_header_size = 12

                    current_block_count = len(current_block)
                    if current_block_count > 0:
                        initial_size = (current_block_count * current_field_header_data["size"])
                        current_block_stream = io.BytesIO(b"\x00" * initial_size)
                        for block_idx, block_element in enumerate(current_block):
                            for field_node in block_field_set:
                                get_fields(tag_stream, current_block_stream, tag_header, current_field_header_data, field_node, block_element, block_idx)

                            leftover_data = get_result("LeftOverData_%s" % field_key, block_element)
                            if leftover_data is not None and PRESERVE_VERSION:
                                leftover_bytes = base64.b64decode(leftover_data)
                                if PRESERVE_PADDING:
                                    current_block_stream.write(leftover_bytes)
                                else:
                                    current_block_stream.write(bytes(len(leftover_bytes)))

                        pos = block_stream.tell()
                        block_stream.seek(0, io.SEEK_END)  
                        current_block_stream.seek(0)
                        if tag_header["engine tag"] == EngineTag.H1Latest.value:
                            block_stream.write(current_block_stream.getvalue())
                            block_stream.seek(pos)
                        else:
                            combined_stream = io.BytesIO()
                            tag_block_header_stream = io.BytesIO(b"\x00" * tag_block_header_size)
                            write_field_header(current_field_header_data, current_block_count, tag_block_header_stream, is_legacy=HAS_LEGACY_HEADER)
                            combined_stream.write(tag_block_header_stream.getvalue())
                            combined_stream.write(current_block_stream.getvalue())
                            block_stream.write(combined_stream.getvalue())
                            block_stream.seek(pos)
    elif field_tag == "ByteFlags":
        field_default = 0
        field_size = 1
        if return_size:
            return field_size
        struct_string = '%sb' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result))
                else:
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "CharBlockIndex":
        field_default = 0
        field_size = 1
        if return_size:
            return field_size
        struct_string = '%sb' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result))
                else:
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "CharEnum":
        field_default = 0
        field_size = 1
        if return_size:
            return field_size
        struct_string = '%sb' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]
            set_enum_result(field_key, field_node, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result["value"]))
                else:
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "CharInteger":
        field_default = 0
        field_size = 1
        if return_size:
            return field_size
        struct_string = '%sb' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result))
                else:
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "CustomLongBlockIndex":
        field_default = 0
        field_size = 4
        if return_size:
            return field_size
        struct_string = '%si' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result))
                else:    
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "CustomShortBlockIndex":
        field_default = -1
        field_size = 2
        if return_size:
            return field_size
        struct_string = '%sh' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result))
                else:    
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "Data":
        field_default = (0, 0, 0, 0, 0)
        field_size = 20
        if return_size:
            return field_size
        struct_string = '%siiiii' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            tag_block_fields[field_key] = {"length": 0, "unk1": 0, "unk2": 0, "unk3": 0, "unk4": 0, "encoded": ""}
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(20))
            set_data_result(field_key, tag_block_fields, tag_stream, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    length = result.get("length", 0)
                    unk1 = result.get("unk1", 0)
                    unk2 = result.get("unk2", 0)
                    unk3 = result.get("unk3", 0)
                    unk4 = result.get("unk4", 0)
                    encoded = result.get("encoded", "")
                    byte_data = base64.b64decode(encoded)
                    if PRESERVE_PADDING:
                        block_stream.write(struct.pack(struct_string, len(byte_data), unk1, unk2, unk3, unk4))
                    else:
                        block_stream.write(struct.pack(struct_string, len(byte_data), 0, 0, 0, 0))
                        
                    pos = block_stream.tell()
                    block_stream.seek(0, io.SEEK_END)  
                    block_stream.write(byte_data)
                    block_stream.seek(pos)
                    
                else:
                    block_stream.write(struct.pack(struct_string, 0, 0, 0, 0, 0))
    elif field_tag == "LongBlockIndex":
        field_default = 0
        field_size = 4
        if return_size:
            return field_size
        struct_string = '%si' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_default:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result))
                else:    
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "LongEnum":
        field_default = 0
        field_size = 4
        if return_size:
            return field_size
        struct_string = '%si' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]
            set_enum_result(field_key, field_node, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result["value"]))
                else:
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "LongFlags":
        field_default = 0
        field_size = 4
        if return_size:
            return field_size
        struct_string = '%si' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result))
                else:
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "LongInteger":
        field_default = 0
        field_size = 4
        if return_size:
            return field_size
        struct_string = '%si' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result))
                else:
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "LongString":
        field_default = ""
        field_size = 256
        if return_size:
            return field_size
        if FILE_MODE == FileModeEnum.read:
            tag_block_fields[field_key] = field_default
            result = field_default
            if not unread_data_size < 256:
                result = read_variable_string(block_stream, field_size, endian_override, terminator_length=1, append_terminator=False)
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    write_variable_string(block_stream, result, ">", fixed_length=field_size, terminator_length=1, append_terminator=False)
                else:
                    write_variable_string(block_stream, field_default, ">", fixed_length=field_size, terminator_length=1, append_terminator=False)
    elif field_tag == "OldStringId":
        field_default = 0
        field_size = 4
        if HAS_LEGACY_STRINGS:
            field_size = 32
        if return_size:
            return field_size

        field_resource_default = ""
        struct_string = '%s2H' % ">"
        if FILE_MODE == FileModeEnum.read:
            tag_block_fields[field_key] = field_resource_default
            result = field_resource_default
            string_pad = field_default
            if HAS_LEGACY_STRINGS:
                if not unread_data_size < field_size:
                    result = read_variable_string(block_stream, field_size, endian_override, terminator_length=1, append_terminator=False)
            else:
                if not unread_data_size < field_size:
                    string_pad, result = struct.unpack(struct_string, block_stream.read(field_size))
                    result = read_variable_string(tag_stream, result, "<", terminator_length=0, append_terminator=False)

            set_result("%s_pad" % field_key, tag_block_fields, string_pad)
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                string_pad = get_result("%s_pad" % field_key, tag_block_fields)
                if result is not None or not PRESERVE_VERSION:
                    string_pad = 0
                result = get_result(field_key, tag_block_fields)
                if HAS_LEGACY_STRINGS:
                    if result is not None:
                        write_variable_string(block_stream, result, ">", fixed_length=field_size, terminator_length=1, append_terminator=False)
                    else:
                        write_variable_string(block_stream, field_resource_default, ">", fixed_length=field_size, terminator_length=1, append_terminator=False)
                else:
                    if result is not None:
                        if PRESERVE_STRINGS:
                            length = len(base64.b64decode(result).decode('utf-8', 'replace').split('\x00', 1)[0].strip('\x20'))
                        else:
                            length = len(result)

                        block_stream.write(struct.pack(struct_string, string_pad, length))
                        pos = block_stream.tell()
                        block_stream.seek(0, io.SEEK_END)  
                        write_variable_string(block_stream, result, ">", fixed_length=len(result), terminator_length=0, append_terminator=False)
                        block_stream.seek(pos)
                    else:
                        block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "Pad":
        field_size = 0
        tag_attribute = field_attrib.get("tag")
        if not tag_attribute == "pd64":
            field_size = get_pad_size(field_node)

        if return_size:
            return field_size
        field_default = bytes(field_size)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = block_stream.read(field_size)
            if PRESERVE_PADDING:
                set_encoded_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None and PRESERVE_PADDING:
                    byte_data = base64.b64decode(result)
                    block_stream.write(fit_bytes_to_length(byte_data, field_size))
                else:
                    block_stream.write(field_default)
    elif field_tag == "Point2D":
        field_default = (0, 0)
        field_size = 4
        if return_size:
            return field_size
        struct_string = '%s2h' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size))
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *result))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "Ptr":
        field_default = bytes(4)
        field_size = 4
        if return_size:
            return field_size
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = block_stream.read(field_size)
            set_encoded_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    byte_data = base64.b64decode(result)
                    block_stream.write(fit_bytes_to_length(byte_data, field_size))
                else:
                    block_stream.write(field_default)
    elif field_tag == "Real":
        field_default = 0.0
        field_size = 4
        if return_size:
            return field_size
        struct_string = '%sf' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result))
                else:
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "RealArgbColor":
        field_default = (0.0, 0.0, 0.0, 0.0)
        field_size = 16
        if return_size:
            return field_size

        struct_string = '%s4f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size)) 
            set_color_result(field_key, tag_block_fields, result, True)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *result.values()))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "RealBounds":
        field_default = (0.0, 0.0)
        field_size = 8
        if return_size:
            return field_size
        struct_string = '%s2f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size))
            set_bounds_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    if not isinstance(result, dict):
                        result = {"Min": result, "Max": result}
                    block_stream.write(struct.pack(struct_string, *result.values()))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "RealEulerAngles2D":
        field_default = (0.0, 0.0)
        field_size = 8
        if return_size:
            return field_size
        struct_string = '%s2f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))
                if CONVERT_RADIANS:
                    result = tuple(degrees(x) for x in result)
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    if CONVERT_RADIANS:
                        result = map(radians, result)
                    block_stream.write(struct.pack(struct_string, *result))
                else:
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "RealEulerAngles3D":
        field_default = (0.0, 0.0, 0.0)
        field_size = 12
        if return_size:
            return field_size
        struct_string = '%s3f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))
                if CONVERT_RADIANS:
                    result = tuple(degrees(x) for x in result)
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    if CONVERT_RADIANS:
                        result = map(radians, result)
                    block_stream.write(struct.pack(struct_string, *result))
                else:
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "RealFraction":
        field_default = 0.0
        field_size = 4
        if return_size:
            return field_size
        struct_string = '%sf' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]  
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result))
                else:
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "RealFractionBounds":
        field_default = (0.0, 0.0)
        field_size = 8
        if return_size:
            return field_size
        struct_string = '%s2f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size))) 
            set_bounds_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *result.values()))
                else:
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "RealPlane2D":
        field_default = (0.0, 0.0, 0.0)
        field_size = 12
        if return_size:
            return field_size
        struct_string = '%s3f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size))
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *result))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "RealPlane3D":
        field_default = (0.0, 0.0, 0.0, 0.0)
        field_size = 16
        if return_size:
            return field_size
        struct_string = '%s4f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size))
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *result))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "RealPoint2D":
        field_default = (0.0, 0.0)
        field_size = 8
        if return_size:
            return field_size
        struct_string = '%s2f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size))
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *result))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "RealPoint3D":
        field_default = (0.0, 0.0, 0.0)
        field_size = 12
        if return_size:
            return field_size
        struct_string = '%s3f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size))
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *result))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "RealQuaternion":
        field_default = (0.0, 0.0, 0.0, 0.0)
        field_size = 16
        if return_size:
            return field_size
        struct_string = '%s4f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size))
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *result))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "RealRgbColor":
        field_default = (0.0, 0.0, 0.0)
        field_size = 12
        if return_size:
            return field_size
        struct_string = '%s3f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size))
            set_color_result(field_key, tag_block_fields, result, False)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *result.values()))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "RealVector2D":
        field_default = (0.0, 0.0)
        field_size = 8
        if return_size:
            return field_size
        struct_string = '%s2f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size))  
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *result))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "RealVector3D":
        field_default = (0.0, 0.0, 0.0)
        field_size = 12
        if return_size:
            return field_size
        struct_string = '%s3f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size))
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *result))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "Rectangle2D":
        field_default = (0, 0, 0, 0)
        field_size = 8
        if return_size:
            return field_size
        struct_string = '%s4h' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size))
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *result))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "RgbColor":
        field_default = (0, 0, 0)
        field_size = 4
        if return_size:
            return field_size
        struct_string = '%s4B' % endian_override
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            color_pad = 0
            if not unread_data_size < field_size:
                b, g, r, color_pad = struct.unpack(struct_string, block_stream.read(field_size)) 
                result = (r, g, b)
            set_color_result(field_key, tag_block_fields, result, False)
            set_result("%s_pad" % field_key, tag_block_fields, color_pad)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                color_pad_result = get_result("%s_pad" % field_key, tag_block_fields)
                if color_pad_result is None:
                    color_pad_result = 0
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *reversed(result.values()), color_pad_result))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default, color_pad_result))
    elif field_tag == "ShortBlockIndex":
        field_default = -1
        field_size = 2
        if return_size:
            return field_size
        struct_string = '%sh' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result))
                else:    
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "ShortBounds":
        field_default = (0, 0)
        field_size = 4
        if return_size:
            return field_size
        struct_string = '%s2h' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size))
            set_bounds_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *[round(v) for v in result.values()]))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))
    elif field_tag == "ShortEnum":
        field_default = 0
        field_size = 2
        if return_size:
            return field_size
        struct_string = '%sh' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]
            set_enum_result(field_key, field_node, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result["value"]))
                else:
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "ShortInteger":
        field_default = 0
        field_size = 2
        if return_size:
            return field_size
        struct_string = '%sh' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0]
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, round(result)))
                else:
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "Skip":
        field_size = 0
        tag_attribute = field_attrib.get("tag")
        if not tag_attribute == "pd64":
            field_size = get_pad_size(field_node)

        if return_size:
            return field_size
        field_default = bytes(field_size)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = block_stream.read(field_size)
            set_encoded_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    byte_data = base64.b64decode(result)
                    block_stream.write(fit_bytes_to_length(byte_data, field_size))
                else:
                    block_stream.write(field_default)
    elif field_tag == "String":
        field_default = ""
        field_size = 32
        if return_size:
            return field_size
        if FILE_MODE == FileModeEnum.read:
            tag_block_fields[field_key] = field_default
            result = field_default
            if not unread_data_size < field_size:
                result = read_variable_string(block_stream, field_size, endian_override, terminator_length=1, append_terminator=False)
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    write_variable_string(block_stream, result, ">", fixed_length=field_size, terminator_length=1, append_terminator=False)
                else:
                    write_variable_string(block_stream, field_default, ">", fixed_length=field_size, terminator_length=1, append_terminator=False)
    elif field_tag == "StringId":
        field_default = 0
        field_size = 4
        if return_size:
            return field_size
        field_resource_default = ""
        struct_string = '%s2H' % ">"
        if FILE_MODE == FileModeEnum.read:
            tag_block_fields[field_key] = field_resource_default
            result = field_resource_default
            string_pad = field_default
            if not unread_data_size < field_size:
                string_pad, result = (struct.unpack(struct_string, block_stream.read(field_size)))
                result = read_variable_string(tag_stream, result, "<", terminator_length=0, append_terminator=False)
            set_result("%s_pad" % field_key, tag_block_fields, string_pad)
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                string_pad = get_result("%s_pad" % field_key, tag_block_fields)
                if string_pad is None or not PRESERVE_VERSION:
                    string_pad = 0
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    if PRESERVE_STRINGS:
                        length = len(base64.b64decode(result))
                    else:
                        length = len(result)
                    block_stream.write(struct.pack(struct_string, string_pad, length))
                    pos = block_stream.tell()
                    block_stream.seek(0, io.SEEK_END)  
                    write_variable_string(block_stream, result, ">", fixed_length=length, terminator_length=0, append_terminator=False)
                    block_stream.seek(pos)
                else:
                    block_stream.write(struct.pack(struct_string, string_pad, field_default))
    elif field_tag == "Struct":
        field_default = 0
        field_size = 0
        if FILE_MODE == FileModeEnum.read:
            struct_header = None
            store_header = False
            if not tag_header["engine tag"] == EngineTag.H1Latest.value:
                # We don't use field size here cause field size is used for the total read data in the block chunk. Structs come from the resource chunk written after block data. - Gen
                pos = tag_stream.tell()
                if not (os.stat(tag_stream.name).st_size - pos) < 16:
                    def_tag = field_node[0].get("tag")
                    # TODO: Check if structs make use of the count. Seems to be one across the board but what happens if it's set manually? - Gen
                    struct_name, struct_version, struct_count, struct_size = read_field_header(tag_stream, is_legacy=HAS_LEGACY_HEADER)
                    if not def_tag == struct_name:
                        tag_stream.seek(pos)
                    else:
                        store_header = True
                        struct_header = {"name": struct_name, "version": struct_version, "size": struct_size}

            if struct_header is None:
                struct_field_set = None
                for struct_layout in field_node:
                    for current_struct_field_set in struct_layout:
                        if int(current_struct_field_set.attrib.get('version')) == 0:
                            struct_field_set = current_struct_field_set

                if struct_field_set is None:
                    raise ValueError(f"Latest field set not found.")

                struct_name = field_node[0].attrib.get('tag')
                struct_version = int(struct_field_set.attrib.get('version'))
                struct_count = 1
                struct_size = int(struct_field_set.attrib.get('sizeofValue'))
                struct_header = {"name": struct_name, "version": struct_version, "size": struct_size}

            if store_header:
                tag_block_fields[field_node.get("name")] = struct_header

            block_idx = 0
            struct_offset = block_stream.tell()
            if unread_data_size < struct_header["size"]:
                struct_header["size"] = unread_data_size

            for struct_layout in field_node:
                struct_field_set = struct_layout[struct_version]
                for struct_field_node in struct_field_set:
                    get_fields(tag_stream, block_stream, tag_header, struct_header, struct_field_node, tag_block_fields, block_idx, struct_offset, return_size)
        else:
            has_header = False
            current_struct_field_set = None
            struct_header = None
            if not return_size:
                struct_header = tag_block_fields.get(field_node.get("name"))
            if not PRESERVE_VERSION:
                for layout in field_node:
                    for struct_field_set in layout:
                        if bool(struct_field_set.attrib.get('isLatest')):
                            current_struct_field_set = struct_field_set

                if current_struct_field_set is None:
                    raise ValueError(f"Latest field set not found.")

                field_set_size = 0
                for current_field_node in current_struct_field_set:
                    field_size = get_fields(None, None, None, None, current_field_node, None, None, return_size=True)
                    if field_size is not None:
                        field_set_size += field_size

                if return_size:
                    return field_set_size

                struct_name = field_node[0].get("tag")
                struct_version = int(current_struct_field_set.get("version"))
                struct_header = {"name": struct_name, "version": struct_version, "size": field_set_size}
            else:
                if struct_header is not None:
                    has_header = True
                    for layout in field_node:
                        for struct_field_set in layout:
                            if int(struct_field_set.attrib.get('version')) == struct_header["version"]:
                                current_struct_field_set = struct_field_set

                    if current_struct_field_set is None:
                        raise ValueError(f"field set not found.")
                    
                    if not PRESERVE_SIZE:
                        field_set_size = 0
                        for current_field_node in current_struct_field_set:
                            field_size = get_fields(None, None, None, None, current_field_node, None, None, return_size=True)
                            if field_size is not None:
                                field_set_size += field_size

                        struct_header["size"] = field_set_size

                else:
                    for layout in field_node:
                        for struct_field_set in layout:
                            if int(struct_field_set.attrib.get('version')) == 0:
                                current_struct_field_set = struct_field_set

                    if current_struct_field_set is None:
                        raise ValueError(f"Latest field set not found.")

                    field_set_size = 0
                    for current_field_node in current_struct_field_set:
                        field_size = get_fields(None, None, None, None, current_field_node, None, None, return_size=True)
                        if field_size is not None:
                            field_set_size += field_size

                    if return_size:
                        return field_set_size

                    struct_name = field_node[0].attrib.get('tag')
                    struct_version = int(current_struct_field_set.attrib.get('version'))
                    struct_size = int(current_struct_field_set.attrib.get('sizeofValue'))
                    if not PRESERVE_SIZE:
                        struct_size = field_set_size
                    struct_header = {"name": struct_name, "version": struct_version, "size": struct_size}

            if not tag_header["engine tag"] == EngineTag.H1Latest.value and (has_header or not PRESERVE_VERSION):
                pos = block_stream.tell()
                block_stream.seek(0, io.SEEK_END)
                write_field_header(struct_header, 1, block_stream, is_legacy=HAS_LEGACY_HEADER)
                block_stream.seek(pos)

            block_idx = 0
            struct_offset = block_stream.tell()
            if unread_data_size < struct_header["size"]:
                struct_header["size"] = unread_data_size

            if struct_header["name"] == "MAPP":
                validate_function_struct(current_struct_field_set, tag_block_fields)
            for struct_field_node in current_struct_field_set:
                get_fields(tag_stream, block_stream, tag_header, struct_header, struct_field_node, tag_block_fields, block_idx, struct_offset)       
    elif field_tag == "Tag":
        field_default = ""
        field_size = 4
        if return_size:
            return field_size
        if FILE_MODE == FileModeEnum.read:
            tag_block_fields[field_key] = field_default
            result = field_default
            if not unread_data_size < field_size:
                result = read_variable_string(block_stream, field_size, endian_override, terminator_length=0)
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    write_variable_string(block_stream, result, "<", fixed_length=field_size, terminator_length=0, append_terminator=False)
                else:
                    write_variable_string(block_stream, field_default, "<", fixed_length=field_size, terminator_length=0, append_terminator=False)
    elif field_tag == "TagReference":
        field_default = (None, 0, 0, -1, "")
        field_size = 16
        if return_size:
            return field_size
        struct_string = '%s4siii' % endian_override
        struct_default_string = '%siiii' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
            struct_default_string = uppercase_struct_letters(struct_default_string)
        if FILE_MODE == FileModeEnum.read:
            tag_block_fields[field_key] = {"group name": None, "unk1": 0, "length": 0, "unk2": -1, "path": ""}
            result = field_default
            if not unread_data_size < field_size:
                tag_group, unk1, length, unk2 = struct.unpack(struct_string, block_stream.read(16))
                if int.from_bytes(tag_group, 'little' if endian_override == '<' else 'big', signed=True) == -1:
                    tag_group = None
                else:
                    tag_group = tag_group.decode('utf-8', 'replace')
                    if endian_override == "<":
                        tag_group = tag_group[::-1]

                path = read_variable_string(tag_stream, length, endian_override, terminator_length=1, append_terminator=True) 
                result = (tag_group, unk1, length, unk2, path)
            set_tag_reference_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    tag_group = result.get("group name", -1)
                    unk1 = result.get("unk1", 0)
                    length = result.get("length", 0)
                    unk2 = result.get("unk2", -1)
                    path = result.get("path", "")
                    if not PRESERVE_PADDING:
                        unk1 = 0
                        unk2 = -1
                    if PRESERVE_STRINGS:
                        length = len(base64.b64decode(path).decode('utf-8', 'replace').split('\x00', 1)[0].strip('\x20'))
                    else:
                        length = len(path)
                    if tag_group == None:
                        tag_group = -1
                        block_stream.write(struct.pack(struct_default_string, tag_group, unk1, length, unk2))
                    else:
                        tag_group = string_to_bytes(tag_group, endian_override)
                        block_stream.write(struct.pack(struct_string, tag_group, unk1, length, unk2))

                    pos = block_stream.tell()
                    block_stream.seek(0, io.SEEK_END)
                    write_variable_string(block_stream, path, ">", fixed_length=length, terminator_length=1, append_terminator=True)
                    block_stream.seek(pos)
                else:
                    block_stream.write(struct.pack(struct_default_string, -1, 0, 0, -1))
    elif field_tag == "UselessPad":
        field_size = 0
        if HAS_LEGACY_PADDING:
            field_size = get_pad_size(field_node)

        if return_size:
            return field_size
        field_default = bytes(field_size)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = block_stream.read(field_size)
            if PRESERVE_PADDING:
                set_encoded_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if HAS_LEGACY_PADDING:
                    if result is not None and PRESERVE_PADDING:
                        byte_data = base64.b64decode(result)
                        block_stream.write(fit_bytes_to_length(byte_data, field_size))
                    else:
                        block_stream.write(field_default)
    elif field_tag == "VertexBuffer":
        field_default = bytes(32)
        field_size = 32
        if return_size:
            return field_size
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = block_stream.read(field_size)
            if PRESERVE_PADDING:
                set_encoded_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None and PRESERVE_PADDING:
                    byte_data = base64.b64decode(result)
                    block_stream.write(fit_bytes_to_length(byte_data, field_size))
                else:
                    block_stream.write(field_default)
    elif field_tag == "WordBlockFlags":
        field_default = 0
        field_size = 2
        if return_size:
            return field_size
        struct_string = '%sh' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0] 
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result))
                else:
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "WordFlags":
        field_default = 0
        field_size = 2
        if return_size:
            return field_size
        struct_string = '%sh' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = (struct.unpack(struct_string, block_stream.read(field_size)))[0] 
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, result))
                else:
                    block_stream.write(struct.pack(struct_string, field_default))
    elif field_tag == "Matrix3x3":
        field_default = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        field_size = 36
        if return_size:
            return field_size
        struct_string = '%s9f' % endian_override
        if unsigned_key:
            struct_string = uppercase_struct_letters(struct_string)
        if FILE_MODE == FileModeEnum.read:
            result = field_default
            if not unread_data_size < field_size:
                result = struct.unpack(struct_string, block_stream.read(field_size))
            set_result(field_key, tag_block_fields, result)
        else:
            if not unread_data_size < field_size:
                result = get_result(field_key, tag_block_fields)
                if result is not None:
                    block_stream.write(struct.pack(struct_string, *result))
                else:    
                    block_stream.write(struct.pack(struct_string, *field_default))

def read_file(merged_defs, tag_directory, file_path="", engine_tag=EngineTag.H2Latest.value, file_endian_override=None):
    global PRESERVE_VERSION
    if engine_tag == EngineTag.H1Latest.value:
        file_endian = ">"
        if file_endian_override:
            file_endian = file_endian_override
    else:
        file_endian="<"
        if file_endian_override:
            file_endian = file_endian_override

    update_interface(FileModeEnum.read, file_endian)

    with open(file_path, "rb") as tag_stream:
        tag_dict = {}
        tag_dict["TagName"] = file_path
        header_struct = struct.unpack('%shbb32s4sIiiihbb4s' % file_endian, tag_stream.read(64))

        header_unk1 = header_struct[0]
        header_flags = header_struct[1]
        header_tag_type = header_struct[2]
        header_name = header_struct[3].decode('utf-8', 'replace').split('\x00', 1)[0].strip('\x20')
        header_tag_group = header_struct[4].decode('utf-8', 'replace')
        if file_endian == "<":
            header_tag_group = header_tag_group[::-1]
        header_checksum = header_struct[5]
        header_data_offset = header_struct[6]
        header_data_length = header_struct[7]
        header_unk2 = header_struct[8]
        header_version = header_struct[9]
        header_destination = header_struct[10]
        header_plugin_handle = header_struct[11]
        header_engine_tag = header_struct[12].decode('utf-8', 'replace')
        if file_endian == "<":
            header_engine_tag = header_engine_tag[::-1]

        tag_dict["Header"] = {"unk1": header_unk1, 
                              "flags": header_flags, 
                              "tag type": header_tag_type, 
                              "name": header_name, 
                              "tag group": header_tag_group, 
                              "checksum": header_checksum, 
                              "data offset": header_data_offset, 
                              "data length": header_data_length, 
                              "unk2": header_unk2, 
                              "version": header_version, 
                              "destination": header_destination, 
                              "plugin handle": header_plugin_handle, 
                              "engine tag": header_engine_tag}
    
        tag_header = tag_dict["Header"]
        if tag_header["engine tag"] == EngineTag.H1Latest.value:
            tag_groups = tag_common.h1_tag_groups
            tag_extensions = tag_common.h1_tag_extensions
            postprocess_functions =  h1_postprocess_functions
        else:
            tag_groups = tag_common.h2_tag_groups
            tag_extensions = tag_common.h2_tag_extensions
            postprocess_functions =  h2_postprocess_functions

        if not is_header_valid(tag_header, tag_groups):
            return {}

        tag_group = tag_header["tag group"]
        tag_extension = tag_groups.get(tag_group)

        is_tag_block_legacy(tag_header)
        is_string_legacy(tag_header)
        is_padding_legacy(tag_header)

        sound_hack = False
        if tag_group == "snd!" and not PRESERVE_VERSION:
            sound_hack = True
            #This is here because snd! tags are complicated. 
            # Essentially version 0-3 do not have the sound_info block and generate it through some process when going to latest.
            # It's not a simple conversion and I'm half thinking that making this work would be halfway to making a custom sound import pipeline. - Gen
            PRESERVE_VERSION = True
            PRESERVE_SIZE = True

        tag_def = merged_defs.get(tag_group)
        if tag_def is None:
            raise ValueError(f"Tag group {tag_group} not found for extension {tag_extension}.")
        
        tag_dict["TagBlockHeader_%s" % tag_extension] = {"name": "tbfd", "version": 0, "size": 0}
        tag_dict["Data"] = {}

        latest_field_set = None
        for layout in tag_def:
            for field_set in layout:
                if bool(field_set.attrib.get('isLatest')):
                    latest_field_set = field_set

        if latest_field_set is None:
            raise ValueError(f"Latest field set not found.")

        block_count = 1
        if tag_header["engine tag"] == EngineTag.H1Latest.value:
            version = int(latest_field_set.attrib.get('version'))
            size = int(latest_field_set.attrib.get('sizeofValue'))
            field_header = {"name": "tbfd", "version": version, "size": size}

        else:
            name, version, block_count, size = read_field_header(tag_stream, is_legacy=HAS_LEGACY_HEADER)
            field_header = {"name": name, "version": version, "size": size}
            if tag_header["tag group"] == "vrtx" and field_header["size"] == 20:
                field_header["version"] = -1

        tag_block_header = tag_dict["TagBlockHeader_%s" % tag_extension] = field_header
        block_stream = io.BytesIO(tag_stream.read(block_count * tag_block_header["size"]))
        for block_idx in range(block_count):
            for layout in tag_def:
                field_set = layout[tag_block_header["version"]]
                start_pos = block_stream.tell()
                for field_node in field_set:
                    get_fields(tag_stream, block_stream, tag_header, tag_block_header, field_node, tag_dict["Data"], block_idx)

                read_size =  tag_block_header["size"] - (block_stream.tell() - start_pos)
                if read_size > 0:
                    leftover_data = block_stream.read(read_size)
                    set_encoded_result("LeftOverData_%s" % tag_extension, tag_dict["Data"], leftover_data)

        postprocess_step = postprocess_functions.get(tag_header["tag group"])
        if postprocess_step is not None and not PRESERVE_VERSION:
            postprocess_step(merged_defs, tag_dict, file_endian, tag_directory)

        if sound_hack:
            #This is here because snd! tags are complicated. 
            # Essentially version 0-3 do not have the sound_info block and generate it through some process when going to latest.
            # It's not a simple conversion and I'm half thinking that making this work would be halfway to making a custom sound import pipeline. - Gen
            PRESERVE_VERSION = False
            PRESERVE_SIZE = False

        return tag_dict

def write_file(merged_defs, tag_dict, obfuscation_buffer, file_path="", engine_tag=EngineTag.H2Latest.value, file_endian_override=None):
    global PRESERVE_VERSION
    if engine_tag == EngineTag.H1Latest.value:
        file_endian = ">"
        if file_endian_override:
            file_endian = file_endian_override
        tag_groups = tag_common.h1_tag_groups
        tag_extensions = tag_common.h1_tag_extensions
        postprocess_functions =  h1_postprocess_functions
    else:
        file_endian="<"
        if file_endian_override:
            file_endian = file_endian_override
        tag_groups = tag_common.h2_tag_groups
        tag_extensions = tag_common.h2_tag_extensions
        postprocess_functions =  h2_postprocess_functions

    update_interface(FileModeEnum.write, file_endian)

    file_extension = file_path.rsplit(".", 1)[1]

    tag_group = tag_extensions.get(file_extension)
    tag_extension = file_extension
    tag_header = tag_dict.get("Header")
    if tag_header is not None:
        tag_group = tag_header["tag group"] 
        tag_extension = tag_groups.get(tag_group)

        tag_def = merged_defs.get(tag_group)

    else:
        tag_def = merged_defs.get(tag_extensions.get(file_extension))
        tag_header = {
            "unk1": 0, 
            "flags": 0, 
            "tag type": 0, 
            "name": "", 
            "tag group": tag_group, 
            "checksum": 0, 
            "data offset": 0, 
            "data length": 0, 
            "unk2": 0, 
            "version": int(tag_def.attrib.get('version')), 
            "destination": 0, 
            "plugin handle": -1, 
            "engine tag": engine_tag
            }

    sound_hack = False
    if tag_group == "snd!" and not PRESERVE_VERSION:
        sound_hack = True
        #This is here because snd! tags are complicated. 
        # Essentially version 0-3 do not have the sound_info block and generate it through some process when going to latest.
        # It's not a simple conversion and I'm half thinking that making this work would be halfway to making a custom sound import pipeline. - Gen
        PRESERVE_VERSION = True
        PRESERVE_SIZE = True

    if tag_group is None or tag_extension is None or tag_def is None:
        raise ValueError(f"Tag group {tag_group} not found for extension {tag_extension}.")

    if not PRESERVE_VERSION:
        tag_header["engine tag"] = engine_tag

    is_tag_block_legacy(tag_header)
    is_string_legacy(tag_header)
    is_padding_legacy(tag_header)

    block_field_set = None
    tag_block_header = tag_dict.get("TagBlockHeader_%s" % tag_extension)
    if PRESERVE_VERSION:
        if tag_block_header is not None:
            for layout in tag_def:
                for field_set in layout:
                    if int(field_set.attrib.get('version')) == tag_block_header["version"]:
                        block_field_set = field_set

    if block_field_set is None:
        for layout in tag_def:
            for field_set in layout:
                if bool(field_set.attrib.get('isLatest')):
                    block_field_set = field_set

        if block_field_set is None:
            raise ValueError(f"Latest field set not found.")

        field_set_size = 0
        for field_node in block_field_set:
            field_size = get_fields(None, None, None, None, field_node, None, None, return_size=True)
            if field_size is not None:
                field_set_size += field_size

        version = int(block_field_set.attrib.get('version'))
        tag_block_header = tag_dict["TagBlockHeader_%s" % tag_extension] = {"name": "tbfd", "version": version, "size": field_set_size}
    else:
        if not PRESERVE_SIZE:
            field_set_size = 0
            for field_node in block_field_set:
                field_size = get_fields(None, None, None, None, field_node, None, None, return_size=True)
                if field_size is not None:
                    field_set_size += field_size

            version = int(block_field_set.attrib.get('version'))
            tag_block_header = tag_dict["TagBlockHeader_%s" % tag_extension] = {"name": "tbfd", "version": version, "size": field_set_size}

    tag_block_header_size = 16
    if HAS_LEGACY_HEADER:
        tag_block_header_size = 12

    tag_stream = io.BytesIO()

    block_idx = 0
    initial_size =  (1 * tag_block_header["size"])
    block_stream = io.BytesIO(b"\x00" * initial_size)
    root = tag_dict["Data"]
    for field_node in block_field_set:
        get_fields(tag_stream, block_stream, tag_header, tag_block_header, field_node, root, block_idx)

    # TODO: This currently doesn't fix itself to take up the space that is left. 
    # It will start overwriting data from the next block if the previously defined size changes to be smaller so we need to resize it.
    # This also applies to the leftover data bit in the block section in the field reader function. - Gen
    leftover_data = get_result("LeftOverData_%s" % tag_extension, tag_dict["Data"])
    if leftover_data is not None and PRESERVE_VERSION:
        leftover_bytes = base64.b64decode(leftover_data)
        if PRESERVE_PADDING:
            block_stream.write(leftover_bytes)
        else:
            block_stream.write(bytes(len(leftover_bytes)))

    engine_tag = tag_header["engine tag"]
    tag_group = tag_header["tag group"]
    tag_header["name"] = string_to_bytes(tag_header["name"], file_endian)
    tag_header["tag group"] = string_to_bytes(tag_header["tag group"], file_endian)
    tag_header["engine tag"] = string_to_bytes(tag_header["engine tag"], file_endian)

    combined_streams = io.BytesIO()
    if not engine_tag == EngineTag.H1Latest.value:
        tag_block_header_stream = io.BytesIO(b"\x00" * tag_block_header_size)
        if tag_group == "vrtx" and tag_block_header["size"] == 20:
            tag_block_header["version"] = 0
        write_field_header(tag_block_header, 1, tag_block_header_stream, is_legacy=HAS_LEGACY_HEADER)
        combined_streams.write(tag_block_header_stream.getvalue())

    combined_streams.write(block_stream.getvalue())
    if GENERATE_CHECKSUM:
        tag_header["checksum"] = checksum_calculate(combined_streams.getvalue(), obfuscation_buffer)

    tag_stream.write(struct.pack('%shbb32s4sIiiihbb4s' % file_endian, *tag_header.values()))
    tag_stream.write(combined_streams.getvalue())
    with open(file_path, "wb") as f:
        f.write(tag_stream.getvalue())

    if sound_hack:
        #This is here because snd! tags are complicated. 
        # Essentially version 0-3 do not have the sound_info block and generate it through some process when going to latest.
        # It's not a simple conversion and I'm half thinking that making this work would be halfway to making a custom sound import pipeline. - Gen
        PRESERVE_VERSION = False
        PRESERVE_SIZE = False

def update_interface(mode_enum=FileModeEnum.read, file_endian="<"):
    global FILE_MODE
    global FIELD_ENDIAN

    FILE_MODE = mode_enum
    FIELD_ENDIAN = file_endian

def h1_single_tag():
    output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h1_merged_output")
    merged_defs = h1.generate_defs(tag_common.h1_defs_directory, output_dir)

    read_path = r"E:\Program Files (x86)\Steam\steamapps\common\Halo MCCEK\Halo Assets\1\Vanilla\tags\effects\blood aoe elite.effect"
    output_path = r"E:\Program Files (x86)\Steam\steamapps\common\Halo MCCEK\Halo Assets\1\Vanilla\tags\blood aoe elite.effect"
    tag_directory = r"E:\Program Files (x86)\Steam\steamapps\common\Halo MCCEK\Halo Assets\1\Vanilla\tags"

    tag_dict = read_file(merged_defs, tag_directory, read_path, engine_tag=EngineTag.H1Latest.value)
    with open(os.path.join(os.path.dirname(output_path), "%s.json" % os.path.basename(output_path).rsplit(".", 1)[0]), 'w', encoding ='utf8') as json_file:
        json.dump(tag_dict, json_file, ensure_ascii = True, indent=4)

    write_file(merged_defs, tag_dict, obfuscation_buffer_prepare(), output_path, engine_tag=EngineTag.H1Latest.value)

def h1_single_json():
    output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h1_merged_output")
    merged_defs = h1.generate_defs(tag_common.h1_defs_directory, output_dir)

    output_path = r"E:\Program Files (x86)\Steam\steamapps\common\Halo MCCEK\Halo Assets\1\Vanilla\tags\tag2.camera_track"

    with open(r"E:\Program Files (x86)\Steam\steamapps\common\Halo MCCEK\Halo Assets\1\Vanilla\tags\tag2.json", "r", encoding="utf8") as json_file:
        tag_dict = json.load(json_file)

        write_file(merged_defs, tag_dict, obfuscation_buffer_prepare(), output_path, engine_tag=EngineTag.H1Latest.value)

def h2_single_tag():
    output_dir = os.path.join(os.path.dirname(tag_common.h2_defs_directory), "h2_merged_output")
    merged_defs = h2.generate_defs(tag_common.h2_defs_directory, output_dir)

    read_path = r"E:\Program Files (x86)\Steam\steamapps\common\Halo MCCEK\Halo Assets\2\Vanilla\tags\tag1.biped"
    output_path = r"E:\Program Files (x86)\Steam\steamapps\common\Halo MCCEK\Halo Assets\2\Vanilla\tags\tag2.biped"
    tag_directory = r"E:\Program Files (x86)\Steam\steamapps\common\Halo MCCEK\Halo Assets\2\Vanilla\tags"

    tag_dict = read_file(merged_defs, tag_directory, read_path)
    with open(os.path.join(os.path.dirname(output_path), "%s.json" % os.path.basename(output_path).rsplit(".", 1)[0]), 'w', encoding ='utf8') as json_file:
        json.dump(tag_dict, json_file, ensure_ascii = True, indent=4)

    write_file(merged_defs, tag_dict, obfuscation_buffer_prepare(), output_path)

def h2_single_json():
    output_dir = os.path.join(os.path.dirname(tag_common.h2_defs_directory), "h2_merged_output")
    merged_defs = h2.generate_defs(tag_common.h2_defs_directory, output_dir)

    output_path = r"E:\Program Files (x86)\Steam\steamapps\common\Halo MCCEK\Halo Assets\2\Vanilla\tags\tag1.sound"

    with open(r"E:\Program Files (x86)\Steam\steamapps\common\Halo MCCEK\Halo Assets\2\Vanilla\tags\tag1.json", "r", encoding="utf8") as json_file:
        tag_dict = json.load(json_file)

        write_file(merged_defs, tag_dict, obfuscation_buffer_prepare(), output_path)

def compute_file_hash(path):
    """Compute SHA256 hash of a file in 64K chunks."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()

def h1_directory():
    input_dir = r"E:\Program Files (x86)\Steam\steamapps\common\Halo MCCEK\Halo Assets\1\Vanilla\tags"

    output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h1_merged_output")
    merged_defs = h1.generate_defs(tag_common.h1_defs_directory, output_dir)

    vanilla_root = os.path.dirname(input_dir)
    output_base_dir = os.path.join(vanilla_root, "blender_output")
    os.makedirs(output_base_dir, exist_ok=True)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(script_dir, "errors.txt")
    obfuscation_buffer = obfuscation_buffer_prepare()

    with open(log_path, "w", encoding="utf-8") as log_file:
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                read_path = os.path.join(root, file)
                tag_extension = read_path.rsplit(".", 1)[1]
                if tag_common.h1_tag_extensions.get(tag_extension):
                    print(read_path)
                    rel_path = os.path.relpath(read_path, input_dir)
                    output_dir = os.path.join(output_base_dir, os.path.dirname(rel_path))
                    os.makedirs(output_dir, exist_ok=True)
                    output_path = os.path.join(output_dir, file)

                    try:
                        tag_dict = read_file(merged_defs, input_dir, read_path, engine_tag=EngineTag.H1Latest.value)
                        if DUMP_JSON:
                            try:
                                json_filename = os.path.basename(output_path).rsplit(".", 1)[0] + ".json"
                                json_path = os.path.join(output_dir, json_filename)
                                with open(json_path, 'w', encoding='utf8') as json_file:
                                    json.dump(tag_dict, json_file, ensure_ascii=True, indent=4)
                            except Exception as e:
                                log_file.write(f"\nJSON Write Error:\n"
                                            f"  File: {json_path}\n"
                                            f"  Error: {type(e).__name__}: {e}\n"
                                            f"  While writing JSON for parsed tag.\n")
                                traceback.print_exc(file=log_file)

                        try:
                            write_file(merged_defs, tag_dict, obfuscation_buffer, output_path, engine_tag=EngineTag.H1Latest.value)
                            
                            # Hash check after write
                            original_hash = compute_file_hash(read_path)
                            output_hash = compute_file_hash(output_path)
                            if original_hash != output_hash:
                                log_file.write(f"\nHash Mismatch:\n"
                                            f"  File: {file}\n"
                                            f"  Read Path: {read_path}\n"
                                            f"  Output Path: {output_path}\n"
                                            f"  Original Hash: {original_hash}\n"
                                            f"  Output Hash:   {output_hash}\n"
                                            f"  The recompiled file differs from the original.\n")
                        except Exception as e:
                            log_file.write(f"\nWrite File Error:\n"
                                        f"  File: {output_path}\n"
                                        f"  Error: {type(e).__name__}: {e}\n"
                                        f"  While writing tag file after parsing.\n")
                            traceback.print_exc(file=log_file)

                    except Exception as e:
                        log_file.write(f"\nParse Error:\n"
                                    f"  File: {read_path}\n"
                                    f"  Error: {type(e).__name__}: {e}\n"
                                    f"  While parsing tag file.\n")
                        traceback.print_exc(file=log_file)

def h2_directory():
    input_dir = r"E:\Program Files (x86)\Steam\steamapps\common\Halo MCCEK\Halo Assets\2\Vanilla\tags"

    output_dir = os.path.join(os.path.dirname(tag_common.h2_defs_directory), "h2_merged_output")
    merged_defs = h2.generate_defs(tag_common.h2_defs_directory, output_dir)

    vanilla_root = os.path.dirname(input_dir)
    output_base_dir = os.path.join(vanilla_root, "blender_output")
    os.makedirs(output_base_dir, exist_ok=True)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(script_dir, "errors.txt")
    obfuscation_buffer = obfuscation_buffer_prepare()

    with open(log_path, "w", encoding="utf-8") as log_file:
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                read_path = os.path.join(root, file)
                tag_extension = read_path.rsplit(".", 1)[1]
                if tag_common.h2_tag_extensions.get(tag_extension):
                    print(read_path)
                    rel_path = os.path.relpath(read_path, input_dir)
                    output_dir = os.path.join(output_base_dir, os.path.dirname(rel_path))
                    os.makedirs(output_dir, exist_ok=True)
                    output_path = os.path.join(output_dir, file)

                    try:
                        tag_dict = read_file(merged_defs, input_dir, read_path)
                        
                        if DUMP_JSON:
                            try:
                                json_filename = os.path.basename(output_path).rsplit(".", 1)[0] + ".json"
                                json_path = os.path.join(output_dir, json_filename)
                                with open(json_path, 'w', encoding='utf8') as json_file:
                                    json.dump(tag_dict, json_file, ensure_ascii=True, indent=4)
                            except Exception as e:
                                log_file.write(f"\nJSON Write Error:\n"
                                            f"  File: {json_path}\n"
                                            f"  Error: {type(e).__name__}: {e}\n"
                                            f"  While writing JSON for parsed tag.\n")
                                traceback.print_exc(file=log_file)

                        try:
                            write_file(merged_defs, tag_dict, obfuscation_buffer, output_path)
                            
                            # Hash check after write
                            original_hash = compute_file_hash(read_path)
                            output_hash = compute_file_hash(output_path)
                            if original_hash != output_hash:
                                log_file.write(f"\nHash Mismatch:\n"
                                            f"  File: {file}\n"
                                            f"  Read Path: {read_path}\n"
                                            f"  Output Path: {output_path}\n"
                                            f"  Original Hash: {original_hash}\n"
                                            f"  Output Hash:   {output_hash}\n"
                                            f"  The recompiled file differs from the original.\n")
                        except Exception as e:
                            log_file.write(f"\nWrite File Error:\n"
                                        f"  File: {output_path}\n"
                                        f"  Error: {type(e).__name__}: {e}\n"
                                        f"  While writing tag file after parsing.\n")
                            traceback.print_exc(file=log_file)

                    except Exception as e:
                        log_file.write(f"\nParse Error:\n"
                                    f"  File: {read_path}\n"
                                    f"  Error: {type(e).__name__}: {e}\n"
                                    f"  While parsing tag file.\n")
                        traceback.print_exc(file=log_file)
                else:
                    log_file.write(f"\nInvalid File:\n"
                                f"  File: {read_path}\n")
                    traceback.print_exc(file=log_file)

def read_tag(tag_path, tag_group, tag_directory, tag_groups, engine_tag, merged_defs):
    asset = None

    tag_extension = tag_groups.get(tag_group)
    read_path = os.path.join(tag_directory, "%s.%s" % (tag_path, tag_extension))
    if os.path.isfile(read_path):
        asset = read_file(merged_defs, tag_directory, read_path, engine_tag)

    return asset

#This is just here to make tag importing not take forever during the Blender import process. 
# Add whatever you need or just get rid of the check in get_tag_reference if you just want to import everything - Gen
TAG_WHITELIST = ("bipd", "bitm", "trak", "coll", "bloc", "crea", "ctrl", "lifi", "mach", "eqip", "mod2", "itmc", "ligh", "MGS2", "hlmt", "coll", "phmo", "mode", 
                 "ai**", "*ipd", "cin*", "clu*", "/**/", "*rea", "dec*", "dc*s", "dgr*", "*qip", "*igh", "*cen", "*sce", "sbsp", "sslt", "ltmp", "trg*", "*ehi", 
                 "*eap", "scen", "shad", "senv", "soso", "stem", "schi", "scex", "sotr", "sgla", "smet", "spla", "swat", "sky ", "ssce", "vehi", "vehc", "weap")

def get_tag_references(field_node, tag_block_fields, tag_references, game_title, tag_directory, tag_groups, engine_tag, merged_defs, asset_cache, prepare_for_blender):
    field_tag = field_node.tag
    field_key = field_node.get("name")
    field_element = tag_block_fields.get(field_key)
    if field_tag in tag_common.float_fields:
        if prepare_for_blender and field_element is not None:
            tag_block_fields[field_key] = prepare_float_field(field_element)

    elif field_tag == "Block":
        tag_block_dict = tag_block_fields.get(field_key)
        if tag_block_dict is not None and len(tag_block_dict) > 0:
            latest_field_set = None
            for layout in field_node:
                for field_set in layout:
                    if bool(field_set.attrib.get('isLatest')):
                        latest_field_set = field_set
                        break

            if latest_field_set is None:
                raise ValueError(f"Latest field set not found.")

            for tag_block_element in tag_block_dict:
                for block_field_node in latest_field_set:
                    get_tag_references(block_field_node, tag_block_element, tag_references, game_title, tag_directory, tag_groups, engine_tag, merged_defs, asset_cache, prepare_for_blender)

    elif field_tag == "Struct":
        latest_struct_field_set = None
        for struct_layout in field_node:
            for struct_field_set in struct_layout:
                if int(struct_field_set.attrib.get('version')) == 0:
                    latest_struct_field_set = struct_field_set

        if latest_struct_field_set is None:
            raise ValueError(f"Latest field set not found.")

        for struct_field_node in latest_struct_field_set:
            get_tag_references(struct_field_node, tag_block_fields, tag_references, game_title, tag_directory, tag_groups, engine_tag, merged_defs, asset_cache, prepare_for_blender)
    
    elif field_tag == "TagReference":
        tag_reference_dict = tag_block_fields.get(field_key)
        if tag_reference_dict is not None:
            if game_title == "halo1" and tag_reference_dict["group name"] == "mode":
                tag_reference_dict["group name"] = "mod2"

            if tag_reference_dict["group name"] in TAG_WHITELIST:
                tag_references.append(tag_reference_dict)

def string_empty_check(string):
    is_empty = False
    if not string == None and (len(string) == 0 or string.isspace()):
        is_empty = True

    return is_empty

def get_disk_asset(tag_path, tag_extension):
    asset_dump = None
    disk_asset_path = os.path.join(os.path.expanduser("~"), "Blender Halo Toolset", "Asset Cache", "%s_%s.json" % (tag_path, tag_extension))
    if os.path.isfile(disk_asset_path):
        with open(disk_asset_path, 'r', encoding='utf8') as json_file:
            asset_dump = json.load(json_file)

    return asset_dump

def generate_tag_dictionary(game_title, root_tag_ref, tag_directory, tag_groups, engine_tag, merged_defs, asset_cache={}, prepare_for_blender=True):
    tag_group = root_tag_ref.get("group name", "")
    tag_extension = tag_groups.get(tag_group)
    tag_path = root_tag_ref.get("path", "")
    
    disk_asset_path = os.path.join(os.path.expanduser("~"), "Blender Halo Toolset", "Asset Cache", "%s_%s.json" % (tag_path, tag_extension))
    if string_empty_check(tag_path):
        return asset_cache

    if asset_cache.get(tag_group) is None:
        asset_cache[tag_group] = {}

    if asset_cache[tag_group].get(tag_path) is None:
        asset_cache[tag_group][tag_path] = {"blender_assets": {}, "has_disk_asset": False, "matching_checksum": False}

    if os.path.isfile(disk_asset_path):
        asset_cache[tag_group][tag_path]["has_disk_asset"] = True

    if asset_cache[tag_group][tag_path]["has_disk_asset"]:
        if not asset_cache[tag_group][tag_path]["matching_checksum"]:
            with open(os.path.join(tag_directory, "%s.%s" % (tag_path, tag_extension)), 'rb') as input_stream:
                valid_header, disk_tag_group, disk_checksum, disk_engine_tag = check_header(input_stream)

            parsed_asset = get_disk_asset(tag_path, tag_extension)
            if disk_checksum == parsed_asset["Header"]["checksum"]:
                asset_cache[tag_group][tag_path]["matching_checksum"] = True

                tag_def = merged_defs.get(tag_group)

                block_count = 1
                latest_field_set = None
                for layout in tag_def:
                    for field_set in layout:
                        if bool(field_set.attrib.get('isLatest')):
                            latest_field_set = field_set
                            break

                if latest_field_set is None:
                    raise ValueError(f"Latest field set not found.")

                tag_references = []
                for block_idx in range(block_count):
                    for field_node in latest_field_set:
                        get_tag_references(field_node, parsed_asset["Data"], tag_references, game_title, tag_directory, tag_groups, engine_tag, merged_defs, asset_cache, prepare_for_blender)

                for tag_ref in tag_references:
                    generate_tag_dictionary(game_title, tag_ref, tag_directory, tag_groups, engine_tag, merged_defs, asset_cache, prepare_for_blender)

            else:
                parsed_asset = read_tag(tag_path, tag_group, tag_directory, tag_groups, engine_tag, merged_defs)
                if parsed_asset is None:
                    return asset_cache
                else:
                    asset_cache[tag_group][tag_path]["has_disk_asset"] = True
                    asset_cache[tag_group][tag_path]["matching_checksum"] = True

                tag_def = merged_defs.get(tag_group)

                block_count = 1
                latest_field_set = None
                for layout in tag_def:
                    for field_set in layout:
                        if bool(field_set.attrib.get('isLatest')):
                            latest_field_set = field_set
                            break

                if latest_field_set is None:
                    raise ValueError(f"Latest field set not found.")

                tag_references = []
                for block_idx in range(block_count):
                    for field_node in latest_field_set:
                        get_tag_references(field_node, parsed_asset["Data"], tag_references, game_title, tag_directory, tag_groups, engine_tag, merged_defs, asset_cache, prepare_for_blender)

                directory_dump = os.path.dirname(disk_asset_path)
                if not os.path.exists(directory_dump):
                    os.makedirs(directory_dump)

                with open(disk_asset_path, 'w', encoding='utf8') as json_file:
                    json.dump(parsed_asset, json_file, ensure_ascii=True, indent=4)

                for tag_ref in tag_references:
                    generate_tag_dictionary(game_title, tag_ref, tag_directory, tag_groups, engine_tag, merged_defs, asset_cache, prepare_for_blender)

    else:
        parsed_asset = read_tag(tag_path, tag_group, tag_directory, tag_groups, engine_tag, merged_defs)
        if parsed_asset is None:
            return asset_cache
        else:
            asset_cache[tag_group][tag_path]["has_disk_asset"] = True
            asset_cache[tag_group][tag_path]["matching_checksum"] = True

        tag_def = merged_defs.get(tag_group)

        block_count = 1
        latest_field_set = None
        for layout in tag_def:
            for field_set in layout:
                if bool(field_set.attrib.get('isLatest')):
                    latest_field_set = field_set
                    break

        if latest_field_set is None:
            raise ValueError(f"Latest field set not found.")

        tag_references = []
        for block_idx in range(block_count):
            for field_node in latest_field_set:
                get_tag_references(field_node, parsed_asset["Data"], tag_references, game_title, tag_directory, tag_groups, engine_tag, merged_defs, asset_cache, prepare_for_blender)

        directory_dump = os.path.dirname(disk_asset_path)
        if not os.path.exists(directory_dump):
            os.makedirs(directory_dump)

        with open(disk_asset_path, 'w', encoding='utf8') as json_file:
            json.dump(parsed_asset, json_file, ensure_ascii=True, indent=4)

        for tag_ref in tag_references:
            generate_tag_dictionary(game_title, tag_ref, tag_directory, tag_groups, engine_tag, merged_defs, asset_cache, prepare_for_blender)

    return asset_cache

def print_skeleton_info():
    output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h1_merged_output")
    merged_defs = h1.generate_defs(tag_common.h1_defs_directory, output_dir)

    read_path = r"E:\Program Files (x86)\Steam\steamapps\common\Halo MCCEK\Halo Assets\1\Vanilla\tags\characters\cyborg\cyborg.gbxmodel"
    tag_directory = r"E:\Program Files (x86)\Steam\steamapps\common\Halo MCCEK\Halo Assets\1\Vanilla\tags"

    tag_dict = read_file(merged_defs, tag_directory, read_path, engine_tag=EngineTag.H1Latest.value)
    node_count = len(tag_dict["Data"]["nodes"])
    node_checksum = tag_dict["Data"]["node list checksum"]
    print("(%s, %s): (" % (node_count, node_checksum))
    for node in tag_dict["Data"]["nodes"]:
        print('        ["%s",        %s, %s, %s],' % (node["name"], node["first child node"], node["next sibling node"], node["parent node"]))
